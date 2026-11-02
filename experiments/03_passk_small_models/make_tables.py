"""Markdown tables for the README from results/*.csv and results/*.json.  Example: python make_tables.py > results/headline_tables.md"""
import csv, json, collections
ORDER = ["gpt2_gpt4more", "gpt2_mma", "gpt2_base", "gemma_gpt4more_1ep", "gemma_gpt4more_5ep", "gemma_mma", "gemma_base"]
SHORT = {"proofnet_lean4": "ProofNet", "minif2f_lean4": "MiniF2F"}
CE_SET = {"proofnet_lean3": "ProofNet Lean 3 (CE)", "proofnet_lean4": "ProofNet Lean 4 (CE)", "minif2f_lean4": "MiniF2F (CE)"}
pk = {}
for r in csv.DictReader(open("results/passk_table.csv")):
    pk[(r["model"], r["dataset"], r["metric"], r["k"])] = r
fmt = {}
for r in csv.DictReader(open("results/passk_table.csv")):
    fmt[r["model"]] = r["format"]

def cell(m, ds, k, metric="pass"):
    r = pk.get((m, ds, metric, str(k)))
    if not r:
        return "n/a"
    return f"{100*float(r['mean']):.1f} ± {100*float(r['sd_over_seeds']):.1f} [{100*float(r['ci95_lo']):.1f}, {100*float(r['ci95_hi']):.1f}]"

for ds in ("proofnet_lean4", "minif2f_lean4"):
    print(f"\n### Lean-checked pass@k on {SHORT[ds]} test (percent; mean ± sd over 3 seeds [95% bootstrap interval over tasks])\n")
    print("| model | prompt format | pass@1 | pass@4 | pass@16 | pass@32 | greedy compiles | theorem-shaped samples |")
    print("|---|---|---|---|---|---|---|---|")
    for m in ORDER:
        if (m, ds, "pass", "1") not in pk:
            continue
        g = float(pk[(m, ds, "greedy_pass", "g")]["mean"]) * 100
        s = float(pk[(m, ds, "theorem_shaped_rate", "g")]["mean"]) * 100
        print(f"| {m} | {fmt[m]} | " + " | ".join(cell(m, ds, k) for k in (1, 4, 16, 32)) + f" | {g:.1f} | {s:.1f} |")

print("\n### CE, TFCE and TFA, single released checkpoint (no training seeds), test split\n")
print("| model | ProofNet Lean 3 CE (paper style) | TFCE | TFA | ProofNet Lean 4 CE | TFCE | TFA | MiniF2F CE | TFCE | TFA |")
print("|---|---|---|---|---|---|---|---|---|---|")
ce = {}
for r in csv.DictReader(open("results/ce_tfa_table.csv")):
    if r["split"] == "test" and r["format"] == "nl_eos":
        ce[(r["model"], r["dataset"])] = r
for m in ORDER:
    row = [m]
    for ds in ("proofnet_lean3", "proofnet_lean4", "minif2f_lean4"):
        r = ce[(m, ds)]
        row += [f"{float(r['ce_full_paper_style']):.2f}", f"{float(r['tfce']):.2f}", f"{100*float(r['tfa']):.1f}%"]
    print("| " + " | ".join(row) + " |")

print("\n### Trust controls (same wrap, rename and Lean check as the samples)\n")
print("| set | control | tasks | compile | rate |")
print("|---|---|---|---|---|")
for c in json.load(open("results/trust_controls.json")):
    print(f"| {SHORT[c['dataset']]} | {c['control']} | {c['n']} | {c['compiles']} | {100*c['rate']:.1f}% |")

print("\n### gpt4-more vs mma gap (paired over tasks; difference = gpt4-more minus mma; p from a sign-flip test, 5000 flips)\n")
print("| set | pair | metric | difference [95% bootstrap interval] | p |")
print("|---|---|---|---|---|")
for g in json.load(open("results/gap_significance.json")):
    if g["kind"] == "pass":
        ds = g["dataset"]; name = f"Lean-checked pass@{g['k']} (prompt {g['fmt']})"
    else:
        f = g["file"]
        if not (f.endswith("nl_eos.per_task.json")):
            continue
        ds = f.split("__")[1]
        if not ds.endswith("_test"):
            continue
        ds = ds[:-5]
        if ds not in ("proofnet_lean3", "proofnet_lean4", "minif2f_lean4"):
            continue
        name = {"tfce": "TFCE", "tfa": "TFA", "ce_full": "CE (token mean)"}[g["kind"]]
    pair = f"{g['a']} vs {g['b']}"
    if pair.startswith("gemma_gpt4more vs") and False:
        pass
    if g["kind"] == "pass" or g["a"] in ORDER:
        sc = 100 if g["kind"] in ("pass", "tfa") else 1
        un = " points" if sc == 100 else ""
        p = "< 0.001" if g["p"] < 0.001 else f"{g['p']:.3f}"
        print(f"| {(SHORT[ds] if g["kind"] == "pass" else CE_SET[ds])} | {pair} | {name} | {sc*g['diff']:+.2f}{un} [{sc*g['ci'][0]:+.2f}, {sc*g['ci'][1]:+.2f}] | {p} |")
