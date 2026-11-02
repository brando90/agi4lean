"""Choose each model's generation prompt format on ProofNet-v3 Lean 4 *validation* (never the test split).

Reads out/gen_val (n=8 samples per task, seed 0, three formats) and out/lean_cache_val; for each model and format
reports the share of samples that are one theorem-shaped statement (`shaped`), the share that Lean compiles
(`compile`, mean of c/n over tasks = pass@1) and the share equal to the gold statement (`exact`). The format with the
highest `compile` is chosen (ties: highest `exact`). Writes out/format_choice.json and results/format_selection.csv.
Example: python select_format.py
"""
import glob, json, re, os
import numpy as np
from common import load_tasks, to_candidate, gold_candidate, norm

tasks = load_tasks("proofnet_lean4", "validation")
gold = {t["name"]: norm(gold_candidate(t["gold"])) for t in tasks}
cache = json.load(open("out/lean_cache_val/proofnet_lean4.json"))
res = {}
for f in sorted(glob.glob("out/gen_val/*.jsonl")):
    m, fmt, _ = re.match(r".*/(.+)__(.+)__seed(\d+)\.jsonl", f).groups()
    sh, co, ex = [], [], []
    for l in open(f):
        r = json.loads(l)
        cs = [to_candidate(s) for s in r["samples"]]
        sh.append(np.mean([bool(c) for c in cs]))
        co.append(np.mean([bool(c) and cache[r["task"]].get(c, False) for c in cs]))
        ex.append(np.mean([bool(c) and norm(c) == gold[r["task"]] for c in cs]))
    res.setdefault(m, {})[fmt] = dict(shaped=float(np.mean(sh)), compile=float(np.mean(co)), exact=float(np.mean(ex)), n_tasks=len(sh))
choice = {m: max(v, key=lambda k: (v[k]["compile"], v[k]["exact"])) for m, v in res.items()}
os.makedirs("results", exist_ok=True)
json.dump(dict(choice=choice, table=res), open("out/format_choice.json", "w"), indent=1)
with open("results/format_selection.csv", "w") as f:
    f.write("model,format,chosen,shaped,compile_pass1,exact_pass1,n_tasks\n")
    for m, v in res.items():
        for k, x in v.items():
            f.write(f"{m},{k},{int(choice[m] == k)},{x['shaped']:.4f},{x['compile']:.4f},{x['exact']:.4f},{x['n_tasks']}\n")
print(open("results/format_selection.csv").read())
