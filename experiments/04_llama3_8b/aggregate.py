"""Collect results/ce/*.summary.json and results/passk/*.summary.json into results/results.csv and markdown tables.

Example: python aggregate.py results
"""
import csv, glob, json, os, sys

d = sys.argv[1] if len(sys.argv) > 1 else "results"
order = ["base", "gpt4more", "mma", "otf"]
label = {"base": "Llama-3-8B base", "gpt4more": "+ gpt4-more (LoRA, 3 ep)", "mma": "+ MMA (LoRA, 1 ep)",
         "otf": "+ on-the-fly backtranslation (LoRA, 3 ep)"}
ce, pk = {}, {}
for f in glob.glob(f"{d}/ce/*.summary.json"):
    ce[os.path.basename(f).split(".")[0]] = json.load(open(f))
for f in glob.glob(f"{d}/passk/*.summary.json"):
    j = json.load(open(f))
    pk[(j["model"], j["format"])] = j["results"]
rows = []
for m in order:
    for t in ["proofnet_lean3:test", "proofnet_lean4:test", "minif2f_lean4:test"]:
        if m in ce and t in ce[m]:
            c = ce[m][t]
            r = dict(model=m, task_set=t, ce_paper_style=round(c["ce_full_paper_style"], 3), ce_token_mean=round(c["ce_full_token_mean"], 3),
                     tfce=round(c["tfce_mean"], 3), tfa=round(c["tfa_mean"], 4))
        else:
            r = dict(model=m, task_set=t)
        for fm in ["nl_eos", "fewshot"]:
            p = pk.get((m, fm), {}).get(t)
            if p:
                for k in ["pass@1", "pass@5", "pass@10", "pass@50", "pass@100"]:
                    r[f"{fm}_{k}"] = round(p[k], 4)
                r[f"{fm}_single_theorem_frac"] = round(p["frac_samples_single_theorem"], 3)
        rows.append(r)
keys = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("model", "task_set"), k))
with open(f"{d}/results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, keys); w.writeheader(); w.writerows(rows)
print(open(f"{d}/results.csv").read())
