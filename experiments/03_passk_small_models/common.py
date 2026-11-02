"""Shared pieces: model registry, datasets, prompt formats, candidate post-processing.

All models are fine-tuned checkpoints of the 'Lean-ing on Quality' paper (HF org AI4M) plus the base models.
"""
import json, os, re, urllib.request

MODELS = {
    # key: (hf repo, family, training data)
    "gpt2_base":           ("gpt2", "gpt2", "none (base)"),
    "gpt2_gpt4more":       ("AI4M/gpt2-gpt4-more", "gpt2", "gpt4-more"),
    "gpt2_gpt4more_ds":    ("AI4M/gpt2-gpt4-more-dataset", "gpt2", "gpt4-more (second upload, same name suffix -dataset)"),
    "gpt2_mma":            ("AI4M/gpt2-mma-dataset", "gpt2", "mma"),
    "gemma_base":          ("google/gemma-2-2b", "gemma", "none (base)"),
    "gemma_gpt4more_1ep":  ("AI4M/gemma2-2b-gpt4-more-dataset", "gemma", "gpt4-more, 1 epoch"),
    "gemma_gpt4more_5ep":  ("AI4M/gemma2-2b-gpt4-more-5-epochs", "gemma", "gpt4-more, 5 epochs"),
    "gemma_gpt4more_feb14":("AI4M/gemma-2-2b-gpt4-more", "gemma", "gpt4-more (older upload, Feb 14)"),
    "gemma_mma":           ("AI4M/gemma-2-2b-mma-dataset", "gemma", "mma"),
}

MMA_PROMPT = "Statement in natural language:\n{nl}\nTranslate the statement in natural language to Lean:"

# prompt formats: name -> (function nl -> prompt text, separator between prompt and formal, stop string for generation)
# `{EOS}` is replaced by the tokenizer's eos token.
def _fewshot():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "fewshot_mma_train_examples.json")
    return "".join(d["input"] + "\n" + d["output"] + " sorry\n\n" for d in json.load(open(p)))


FORMATS = {
    "nl_eos":       (lambda nl: nl + "{EOS}", ""),
    "nl_nl":        (lambda nl: nl + "\n", ""),
    "nl_nlnl":      (lambda nl: nl + "\n\n", ""),
    "mma_nl":       (lambda nl: MMA_PROMPT.format(nl=nl) + "\n", ""),
    "mma_space":    (lambda nl: MMA_PROMPT.format(nl=nl) + " ", ""),
    "mma_eos":      (lambda nl: MMA_PROMPT.format(nl=nl) + "{EOS}", ""),
    # 3 fixed examples from the mma training set (data/fewshot_mma_train_examples.json), then the task in mma format
    "fs3_mma":      (lambda nl: _fewshot() + MMA_PROMPT.format(nl=nl) + "\n", ""),
    "informal_formal": (lambda nl: "Informal Statement: " + nl + "\nFormal Statement: ", ""),
}


def get_json(url):
    return json.load(urllib.request.urlopen(url, timeout=60))


def _rows(name, split):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"{name}_{split}.jsonl")
    return [json.loads(l) for l in open(p)]


def load_tasks(name, split="test"):
    """Return list of dicts: name, nl, gold, header, category. Data files in data/ are copies of the HF datasets
    UDACA/proofnet-v3-lean4, UDACA/minif2f-lean4 and hoskinson-center/proofnet (Lean 3, the paper's CE set)."""
    out = []
    if name == "proofnet_lean4":
        l3 = _rows("proofnet_lean3", split)
    for r in _rows(name, split):
        if name == "minif2f_lean4" and r["formal_statement"].lstrip().startswith("--"):
            continue  # 19 test tasks whose gold formalization is commented out upstream ("-- Error: ..."): no gold, dropped
        if name == "proofnet_lean4":
            # book of the exercise: the Lean 3 ProofNet row with the same exercise name and the closest NL statement
            import difflib
            cands = [x for x in l3 if x["id"].split("|")[1] == r["name"]]
            book = max(cands, key=lambda x: difflib.SequenceMatcher(None, x["nl_statement"], r["nl_statement"]).ratio())["id"].split("|")[0] if cands else "unknown"
            out.append(dict(name=r["name"], nl=r["nl_statement"], gold=r["formal_statement"],
                            header=r["header_no_import"], category=book))
        elif name == "minif2f_lean4":
            hdr = "\n".join(l for l in r["header"].split("\n") if not l.startswith("import"))
            i = r["id"]
            tok = i.split("_")[0]
            cat = "mathd_" + i.split("_")[1] if tok == "mathd" else ("aime" if tok.startswith("aime") else tok)
            out.append(dict(name=i, nl=r["nl_statement"], gold=r["formal_statement"], header=hdr, category=cat))
        elif name == "proofnet_lean3":
            out.append(dict(name=r["id"], nl=r["nl_statement"], gold=r["formal_statement"], header="", category=r["id"].split("|")[0]))
        else:
            raise ValueError(name)
    return out


START = re.compile(r"(?:^|\n|Statement:|Lean:)[ \t]*((?:noncomputable\s+def|theorem|lemma|def)\s+\S+)")
STMT_BAD_LINE = re.compile(r"^\s*(end|section|namespace|open|import|def|instance|axiom|macro|syntax|notation|#|attribute|set_option)\b", re.M)


def to_candidate(text):
    """Turn a sampled continuation into one Lean statement ending in `:= sorry`, theorem renamed.

    Returns None when the sample is not a single theorem/lemma/def statement (counts as a failure). `def` is
    accepted because 7 ProofNet gold statements are `def ... : CommGroup G`-style.
    The sample is cut at its first `:=` (the statement ends there), so a proof body the model wrote is ignored.
    """
    t = text.strip()
    # the statement starts at the first line (or `Statement:` / `Lean:` label) that begins with theorem/lemma/def
    m0 = START.search(t)
    if not m0:
        return None
    t = t[m0.start(1):]
    i = t.find(":=")
    stmt = (t if i < 0 else t[:i]).strip()
    m = re.match(r"(noncomputable\s+def|theorem|lemma|def)\s+(\S+)", stmt)
    if not m or STMT_BAD_LINE.search(stmt[m.end():]) or len(stmt) > 1500:
        return None
    kw = "theorem" if m.group(1) in ("theorem", "lemma") else re.sub(r"\s+", " ", m.group(1))
    return kw + " cand_thm" + stmt[m.end():] + " := sorry"


def gold_candidate(gold):
    return to_candidate(gold)


def norm(s):
    return re.sub(r"\s+", "", s)
