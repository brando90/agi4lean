"""Build the tables of this folder from results/ce and results/passk (per-task counts, n = 100 samples per task).

Writes results/headline_tables.md, results/pass_at_k_table.csv. pass@k = Chen et al. unbiased estimator per task from
c compiling samples out of n = 100, averaged over tasks, with a 95% bootstrap interval over tasks (2000 resamples).
Example: python make_tables.py results
"""
import csv, json, os, sys
from math import comb
import numpy as np

d = sys.argv[1] if len(sys.argv) > 1 else "results"
rng = np.random.default_rng(0)
KS = [1, 4, 16, 32, 100]
runs = [("base (3-shot prompt)", "base", "fewshot", ["proofnet_lean4", "minif2f_lean4"]),
        ("base (training prompt, no shots)", "base", "nl_eos", ["proofnet_lean4", "minif2f_lean4"]),
        ("+ gpt4-more (training prompt)", "gpt4more", "nl_eos", ["proofnet_lean4", "minif2f_lean4"]),
        ("+ MMA (training prompt)", "mma", "nl_eos", ["proofnet_lean4", "minif2f_lean4"]),
        ("+ on-the-fly backtranslation (training prompt)", "otf2", "nl_eos", ["proofnet_lean4", "minif2f_lean4"]),
        ("+ gpt4-more (3-shot prompt)", "gpt4more", "fewshot", ["proofnet_lean4", "minif2f_lean4"]),
        ("+ MMA (3-shot prompt)", "mma", "fewshot", ["proofnet_lean4", "minif2f_lean4"]),
        ("+ on-the-fly backtranslation (3-shot prompt)", "otf2", "fewshot", ["proofnet_lean4", "minif2f_lean4"])]


def pk(n, c, k):
    return 1.0 if n - c < k else 1.0 - comb(n - c, k) / comb(n, k)


def boot(v):
    v = np.asarray(v)
    m = [rng.choice(v, len(v)).mean() for _ in range(2000)]
    return v.mean(), np.percentile(m, 2.5), np.percentile(m, 97.5)


rows, md = [], {}
for label, name, fm, sets in runs:
    for s in sets:
        fn = [p for p in (f"{d}/passk/{name}__{fm}__{s}_test.per_task.json", f"{d}/passk_fs/{name}__{fm}__{s}_test.per_task.json") if os.path.exists(p)]
        if not fn:
            continue  # run not available (yet)
        pt = json.load(open(fn[0]))
        r = dict(model=label, prompt=fm, task_set=s, tasks=len(pt))
        for k in KS:
            m, lo, hi = boot([pk(t["n"], t["c"], k) for t in pt])
            r[f"pass@{k}"] = round(100 * m, 1); r[f"pass@{k}_lo"] = round(100 * lo, 1); r[f"pass@{k}_hi"] = round(100 * hi, 1)
        r["theorem_shaped_samples_pct"] = round(100 * float(np.mean([t["n_valid_form"] / t["n"] for t in pt])), 1)
        rows.append(r)
with open(f"{d}/pass_at_k_table.csv", "w", newline="") as f:
    w = csv.DictWriter(f, list(rows[0].keys())); w.writeheader(); w.writerows(rows)


def table(s):
    out = ["| model | prompt | pass@1 | pass@4 | pass@16 | pass@32 | pass@100 | theorem-shaped samples |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["task_set"] == s:
            c = " | ".join(f"{r[f'pass@{k}']} [{r[f'pass@{k}_lo']}, {r[f'pass@{k}_hi']}]" for k in KS)
            out.append(f"| {r['model']} | {r['prompt']} | {c} | {r['theorem_shaped_samples_pct']}% |")
    return "\n".join(out)


ce = {m: json.load(open(f"{d}/ce/{m}.summary.json")) for m in ["base", "gpt4more", "mma", "otf2"]}
names = {"base": "base", "gpt4more": "+ gpt4-more", "mma": "+ MMA", "otf2": "+ on-the-fly backtranslation"}
cet = ["| model | ProofNet Lean 3 CE | TFCE | TFA | ProofNet Lean 4 CE | TFCE | TFA | MiniF2F CE | TFCE | TFA |", "|---|---|---|---|---|---|---|---|---|---|"]
for m in ce:
    c = []
    for t in ["proofnet_lean3:test", "proofnet_lean4:test", "minif2f_lean4:test"]:
        x = ce[m][t]; c += [f"{x['ce_full_paper_style']:.2f}", f"{x['tfce_mean']:.2f}", f"{100 * x['tfa_mean']:.1f}%"]
    cet.append(f"| {names[m]} | " + " | ".join(c) + " |")
open(f"{d}/headline_tables.md", "w").write(
    "### Lean-checked pass@k, ProofNet-v3 Lean 4 test, 183 tasks (percent, [95% bootstrap interval over tasks]; n = 100 samples per task, 1 sampling seed)\n\n" + table("proofnet_lean4") +
    "\n\n### Lean-checked pass@k, MiniF2F Lean 4 test, 244 tasks (same)\n\n" + table("minif2f_lean4") +
    "\n\n### CE (paper style), TFCE and TFA, test splits (single run each)\n\n" + "\n".join(cet) + "\n")
print(open(f"{d}/headline_tables.md").read())
