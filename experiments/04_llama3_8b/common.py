"""Shared pieces for the Llama-3-8B experiment: prompt formats, task loading, candidate post-processing.

Task loading and candidate post-processing are copied from experiments/03_passk_small_models so that the
GPT-2, Gemma and Llama-3 rows are scored the same way.
"""
import json, re

BASE = "meta-llama/Meta-Llama-3-8B"

# Training and evaluation format (the paper's finetune.py format): "<informal><eos><formal>".
# Llama-3's tokenizer adds <|begin_of_text|> itself; eos is <|end_of_text|>.
def fmt_nl_eos(nl, eos):
    return nl + eos

# 3-shot prompt of the lean4ai pass@k protocol (used only for the base-model few-shot reference row).
FEWSHOT = (
    "Your task is translate the natural language version of the mathematical statement "
    "to a formal Lean statement version, using the following format:\n"
    "natural language statement:\nLet $z=\\frac{1+i}{\\sqrt{2}}.$What is $\\left(z^{1^2}+z^{2^2}+z^{3^2}+\\dots+z^{{12}^2}\\right) \\cdot "
    "\\left(\\frac{1}{z^{1^2}}+\\frac{1}{z^{2^2}}+\\frac{1}{z^{3^2}}+\\dots+\\frac{1}{z^{{12}^2}}\\right)?$ "
    "$\\textbf{(A)}\\ 18 \\qquad \\textbf{(B)}\\ 72-36\\sqrt2 \\qquad \\textbf{(C)}\\ 36 \\qquad \\textbf{(D)}\\ 72 \\qquad \\textbf{(E)}\\ 72+36\\sqrt2$ "
    "Show that it is \\textbf{(C)}\\ 36.\n"
    "formal Lean language statement:##\ntheorem amc12a_2019_p21 (z : ℂ) (h₀ : z = (1 + Complex.I) / Real.sqrt 2) : "
    "(∑ k in Finset.Icc 1 12, (z^(k^2))) * (∑ k in Finset.Icc 1 12, (1 / z^(k^2))) = 36 := sorry\n##"
    "natural language statement:\nIntegers $x$ and $y$ with $x>y>0$ satisfy $x+y+xy=80$. What is $x$? "
    "$\\textbf{(A)}\\ 8 \\qquad\\textbf{(B)}\\ 10 \\qquad\\textbf{(C)}\\ 15 \\qquad\\textbf{(D)}\\ 18 \\qquad\\textbf{(E)}\\ 26$ Show that it is \\textbf{(E)}\\ 26.\n"
    "formal Lean language statement:##\ntheorem amc12a_2015_p10 (x y : ℤ) (h₀ : 0 < y) (h₁ : y < x) "
    "(h₂ : x + y + (x * y) = 80) : x = 26 := sorry\n##"
    "natural language statement:\nWhat is the [[volume]] of a [[cube]] whose [[surface area]] is twice that of a cube with volume 1? "
    "$\\mathrm{(A)}\\ \\sqrt{2}\\qquad\\mathrm{(B)}\\ 2\\qquad\\mathrm{(C)}\\ 2\\sqrt{2}\\qquad\\mathrm{(D)}\\ 4\\qquad\\mathrm{(E)}\\ 8$ Show that it is \\mathrm{(C)}.\n"
    "formal Lean language statement:##\ntheorem amc12a_2008_p8 (x y : ℝ) (h₀ : 0 < x ∧ 0 < y) "
    "(h₁ : y^3 = 1) (h₂ : 6 * x^2 = 2 * (6 * y^2)) : x^3 = 2 * Real.sqrt 2 := sorry\n##"
)


def fewshot_prompt(nl):
    return FEWSHOT + f"natural language statement:\n{nl}\nformal Lean language statement:"


def load_tasks(name, split="test"):
    """Return list of dicts: name, nl, gold, header_no_import, category, dataset."""
    from datasets import load_dataset
    out = []
    if name == "proofnet_lean4":  # ProofNet v3 Lean 4: used for pass@k, CE, TFA
        ds = load_dataset("UDACA/proofnet-v3-lean4", split=split)
        for r in ds:
            out.append(dict(name=r["name"], nl=r["nl_statement"], gold=r["formal_statement"],
                            header=r["header_no_import"], category=None))
    elif name == "minif2f_lean4":
        ds = load_dataset("UDACA/minif2f-lean4", split=split)
        for r in ds:
            hdr = "\n".join(l for l in r["header"].split("\n") if not l.startswith("import"))
            cat = re.sub(r"_\d+.*$", "", r["id"]) if r["id"].startswith(("mathd", "algebra", "numbertheory", "induction")) else re.split(r"_", r["id"])[0]
            out.append(dict(name=r["id"], nl=r["nl_statement"], gold=r["formal_statement"], header=hdr, category=cat))
    elif name == "proofnet_lean3":  # the paper's CE set (Lean 3 formal statements)
        ds = load_dataset("hoskinson-center/proofnet", split=split)
        for r in ds:
            out.append(dict(name=r["id"], nl=r["nl_statement"], gold=r["formal_statement"], header="", category=r["id"].split("|")[0]))
    else:
        raise ValueError(name)
    return out


STMT_BAD_LINE = re.compile(r"^\s*(end|section|namespace|open|import|def|instance|axiom|macro|syntax|notation|#|attribute|set_option)\b", re.M)


def to_candidate(text):
    """Turn a sampled continuation into one Lean statement ending in `:= sorry`, theorem renamed.

    Returns None when the sample is not a single theorem/lemma statement (counts as a failure).
    The sample is cut at its first `:=` (the statement ends there), so a proof body the model wrote is ignored.
    """
    t = text.strip()
    i = t.find(":=")
    stmt = (t if i < 0 else t[:i]).strip()
    m = re.match(r"(theorem|lemma)\s+(\S+)", stmt)
    if not m or STMT_BAD_LINE.search(stmt[m.end():]) or len(stmt) > 1500:
        return None
    return "theorem cand_thm" + stmt[m.end():] + " := sorry"


def gold_candidate(gold):
    return to_candidate(gold)


def norm(s):
    return re.sub(r"\s+", "", s)
