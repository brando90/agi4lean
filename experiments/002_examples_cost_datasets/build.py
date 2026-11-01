"""Build examples.md, cost_table.csv and datasets_inventory.csv for experiment 002 from the public AI4M data.

Run: python build.py   (needs: pip install tiktoken transformers requests; CPU only, no API key, about 1 minute)
Downloads the public Hugging Face datasets of org AI4M, never writes secrets.
"""
import csv, json, os, random, re, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")
GEN = os.path.join(HERE, "..", "..", "src", "lean4math", "dataset_gen", "lean4math_dataset_gen.py")
SEED = 0
PRICE_IN, PRICE_OUT = 30.0, 60.0  # USD per million tokens, OpenAI list price of gpt-4 (8k) in March 2024

# paper's generation method -> (Hugging Face dataset, file, how pairs are stored)
METHODS = {
    "MMA Train (baseline, not ours)": ("AI4M/mma-dataset", "train.jsonl", "output", "input"),
    "GPT-4 MathLib4 (Full Proof)": ("AI4M/gpt4-more", "train.jsonl", "formal", "informal"),
    "GPT-4 LeanDojo (Individual Tactics), 29-pair set": ("AI4M/state_info_informalization", "train.json", "formal", "informal"),
    "GPT-4 LeanDojo (Individual Tactics), 100-pair set": ("AI4M/stateInfoInformalizationBig", "stateInfoInformalization.json", "formal", "informal"),
    "Regex-Parsed LeanDojo Proofs": ("AI4M/regexInformalizationData", "regexInformalization.json", "formal", "informal"),
}
PAPER_TOKENS = {  # Table 1 of the paper (GPT-2 tokens, formal + informal)
    "MMA Train (baseline, not ours)": 10916097,
    "GPT-4 MathLib4 (Full Proof)": 71550,
    "GPT-4 LeanDojo (Individual Tactics), 29-pair set": 1754,
    "GPT-4 LeanDojo (Individual Tactics), 100-pair set": 1754,
    "Regex-Parsed LeanDojo Proofs": 124782,
}


def fetch(repo, fname):
    out = os.path.join(CACHE, repo.replace("/", "__"), fname)
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        urllib.request.urlretrieve(f"https://huggingface.co/datasets/{repo}/resolve/main/{fname}", out)
    return out


def load(path):
    t = open(path, encoding="utf-8").read()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return [json.loads(l) for l in t.splitlines() if l.strip()]


def main():
    from transformers import GPT2TokenizerFast
    import tiktoken
    gpt2 = GPT2TokenizerFast.from_pretrained("gpt2")
    gpt4 = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
    n2 = lambda L: sum(len(x) for x in gpt2(L)["input_ids"])
    n4 = lambda L: sum(len(x) for x in gpt4.encode_batch(L))

    # the real 6-shot prompt the generation script sent to GPT-4
    src = open(GEN, encoding="utf-8").read()
    sysp = re.search(r'gpt_assistant_prompt = "(.*?)"', src).group(1)
    userp = re.search(r'gpt_user_prompt = """(.*?)"""', src, re.S).group(1)
    prompt_tokens = len(gpt4.encode(sysp)) + len(gpt4.encode(userp))

    rng = random.Random(SEED)
    ex_md = ["# Before/after examples per generation method\n",
             f"Five pairs per method, drawn at random (seed {SEED}) from the real saved data, not picked by hand. "
             "Before = the formal Lean text, after = the informal text that the method produced. "
             "Text longer than 1,200 characters is cut with `[...]`; the full pairs are in `examples.jsonl`.\n"]
    ex_rows, cost_rows = [], []
    for name, (repo, fname, fk, ik) in METHODS.items():
        d = load(fetch(repo, fname))
        f = [x[fk] for x in d]; i = [x[ik] for x in d]
        t2 = n2(f) + n2(i)  # as stored, same as the paper's count
        if repo == "AI4M/mma-dataset":  # stored as autoformalization pairs: input = wrapped informal text, output = Lean
            i = [re.sub(r"^Statement in natural language:\n|\nTranslate the statement in natural language to Lean:\s*$", "", x) for x in i]
        idx = sorted(rng.sample(range(len(d)), 5))
        ex_md.append(f"\n## {name}\n\nSource: `{repo}/{fname}`, {len(d):,} pairs, row indices {idx}.\n")
        for k, j in enumerate(idx, 1):
            cut = lambda s: s if len(s) <= 1200 else s[:1200] + " [...]"
            ex_md.append(f"**Example {k} (row {j})**\n\nBefore (formal):\n```lean\n{cut(f[j])}\n```\nAfter (informal):\n```text\n{cut(i[j])}\n```\n")
            ex_rows.append({"method": name, "source": f"{repo}/{fname}", "row": j, "formal": f[j], "informal": i[j]})
        tf4, ti4 = n4(f), n4(i)
        if name.startswith("GPT-4 MathLib4"):
            # prompt = fixed 6-shot text + the theorem; output = the ('formal','informal') tuple, so it echoes the formal text
            tin = len(d) * prompt_tokens + tf4
            tout = tf4 + ti4
            note = (f"input = 6-shot prompt ({prompt_tokens} tokens, from lean4math_dataset_gen.py) x {len(d)} calls + formal tokens; "
                    "output = formal echo + informal; counts only the 348 kept pairs, so a lower bound (calls that were dropped or retried are not logged)")
        elif name.startswith("GPT-4 LeanDojo"):
            tin, tout = tf4, ti4
            note = "zero-shot prompt text not in any repo, so input = the data only; lower bound; no generation script or log found"
        elif name.startswith("MMA"):
            tin, tout = tf4, ti4
            note = "not paid by us (public MMA data); the price if it were regenerated with GPT-4, instruction text not counted"
        else:
            tin = tout = None
            note = "rule-based regex templates, no API call"
        usd = None if tin is None else round((tin * PRICE_IN + tout * PRICE_OUT) / 1e6, 2)
        cost_rows.append({
            "method": name, "pairs": len(d), "gpt2_tokens_formal+informal": t2,
            "paper_table1_tokens": PAPER_TOKENS[name], "matches_paper": t2 == PAPER_TOKENS[name],
            "gpt4_tokens_in_estimated": tin, "gpt4_tokens_out_estimated": tout,
            "api_usd_estimated_gpt4_list_price": usd, "wall_clock": "not logged", "note": note})
    cost_rows.append({"method": "On-the-Fly Backtranslation", "pairs": "none saved", "gpt2_tokens_formal+informal": "none saved",
                      "paper_table1_tokens": "not in table", "matches_paper": "", "gpt4_tokens_in_estimated": 0, "gpt4_tokens_out_estimated": 0,
                      "api_usd_estimated_gpt4_list_price": 0,
                      "wall_clock": "not logged (train.py prints elapsed time; no output saved)",
                      "note": "the synthetic informal text is generated inside the training loop (unsupervised_trainer.py) and never written to disk; no API; GPU time only"})
    ex_md.append("\n## On-the-Fly Backtranslation\n\nNo examples: the synthetic informal text is generated inside the training loop and never saved "
                 "(`src/lean4math/backtranslation/unsupervised_trainer.py` has no save or log call). Folder 003 can add a short run that dumps the generated pairs.\n")
    open(os.path.join(HERE, "examples.md"), "w", encoding="utf-8").write("\n".join(ex_md))
    with open(os.path.join(HERE, "examples.jsonl"), "w", encoding="utf-8") as fh:
        for r in ex_rows: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(HERE, "cost_table.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cost_rows[0])); w.writeheader(); w.writerows(cost_rows)
    for r in cost_rows: print(r["method"], r["pairs"], r["gpt2_tokens_formal+informal"], r["matches_paper"], r["api_usd_estimated_gpt4_list_price"])


if __name__ == "__main__":
    main()
