"""Inventory of the public Hugging Face datasets of org AI4M (rows, columns, size, overlaps) -> datasets_inventory.csv.

Run: python inventory.py   (needs: requests-free, stdlib only; CPU only; downloads files under 120 MB into .cache/)
Answers which of the GPT-4 Lean4 datasets named in the slides exist publicly and how they relate to each other.
"""
import csv, json, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")
get = lambda u: json.load(urllib.request.urlopen(u, timeout=60))
ROLE = {  # what each dataset is, from the paper, the slides and the content checks in this folder
    "AI4M/gpt4-more": "GPT-4 MathLib4 (Full Proof): 348 pairs, the paper's 71,550-token set (6-shot GPT-4)",
    "AI4M/gpt-4fp_minif2f_mix": "gpt4-more (348, all included) + 186 MiniF2F statement pairs",
    "AI4M/willy_mix_1": "the 29 state_info_informalization pairs + the 186 MiniF2F statement pairs",
    "AI4M/michael-af": "train = 249 pairs, all inside gpt4-more; valid/test = MiniF2F statement pairs",
    "AI4M/state_info_informalization": "GPT-4 LeanDojo (Individual Tactics): 29 pairs (before-state, tactic, after-state); no overlap with the 100-pair set",
    "AI4M/stateInfoInformalizationBig": "GPT-4 LeanDojo (Individual Tactics): 100 pairs; the paper's 1,754 tokens match neither set",
    "AI4M/regexInformalizationData": "Regex-Parsed LeanDojo Proofs: 2,875 pairs, the paper's 124,782-token set",
    "AI4M/regex_gpt4": "2,974 rows: the regex pairs plus 99 GPT-4-written theorem informalizations (name says gpt4)",
    "AI4M/mma-dataset": "MMA Train baseline (autoformalization direction: input = natural language, output = Lean), 84,679 pairs",
    "AI4M/minif2f_dataset": "MiniF2F statement pairs, 186 (test.jsonl also has ids, header, NL proof)",
    "AI4M/miniF2FInformalizations": "same 186 MiniF2F pairs",
    "AI4M/minif2f_real": "244 paired MiniF2F statements, no overlap with the 186",
    "AI4M/leandojo-informalized": "31,127 LeanDojo theorems with traced tactics and an informalization (later, trains AI4M/llama3-8b-leandojo-informalized); generating model not stated in the card",
    "AI4M/claudedataset-2": "Claude informalizations (CS197 paper), not this paper",
    "AI4M/250ktokendataset": "Claude informalizations (CS197 paper), not this paper",
    "AI4M/102k_token_clean_claude_dataset": "Claude informalizations (CS197 paper), not this paper",
}


def rows_cols(path):
    t = open(path, encoding="utf-8").read()
    try:
        d = json.loads(t)
    except json.JSONDecodeError:
        d = [json.loads(l) for l in t.splitlines() if l.strip()]
    return len(d), sorted(d[0]) if isinstance(d, list) and d and isinstance(d[0], dict) else []


def main():
    out = []
    for ds in get("https://huggingface.co/api/datasets?author=AI4M&limit=200"):
        n = ds["id"]
        info = get(f"https://huggingface.co/api/datasets/{n}?blobs=true")
        for s in info["siblings"]:
            f, sz = s["rfilename"], s.get("size") or 0
            if f in (".gitattributes", "README.md"):
                continue
            rows, cols = "", ""
            if f.endswith((".json", ".jsonl")) and sz < 120e6:
                p = os.path.join(CACHE, n.replace("/", "__"), f)
                if not os.path.exists(p):
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    urllib.request.urlretrieve(f"https://huggingface.co/datasets/{n}/resolve/main/{f}", p)
                rows, cols = rows_cols(p)
            out.append({"dataset": n, "created": info.get("createdAt", "")[:10], "file": f, "bytes": sz,
                        "rows": rows, "columns": " ".join(cols), "what_it_is": ROLE.get(n, "data-selection set (ZIP-FIT/LESS/DSIR), not this paper's generation methods")})
    with open(os.path.join(HERE, "datasets_inventory.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    print(len(out), "files")


if __name__ == "__main__":
    main()
