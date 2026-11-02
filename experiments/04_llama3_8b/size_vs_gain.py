"""Size-vs-gain table: GPT-2 (124M) and Gemma-2-2B rows from ../03_passk_small_models, Llama-3-8B rows from results/.

Gain = fine-tuned minus base, same metric, same task set. Writes results/size_vs_gain.md. Example: python size_vs_gain.py
"""
import csv, json
S03 = "../03_passk_small_models/results"
p3 = {(r["model"], r["dataset"], r["k"]): float(r["mean"]) * 100 for r in csv.DictReader(open(f"{S03}/passk_table.csv")) if r["metric"] == "pass"}
c3 = {(r["model"], r["dataset"], r["format"]): r for r in csv.DictReader(open(f"{S03}/ce_tfa_table.csv")) if r["split"] == "test"}
def pk4(name, fm, s, k):
    import math
    pt = json.load(open(f"results/passk/{name}__{fm}__{s}_test.per_task.json"))
    f = lambda n, c: 1.0 if n - c < k else 1.0 - math.comb(n - c, k) / math.comb(n, k)
    return 100 * sum(f(t["n"], t["c"]) for t in pt) / len(pt)
ce4 = {m: json.load(open(f"results/ce/{m}.summary.json")) for m in ["base", "gpt4more", "mma", "otf2"]}
def ce3(m, key): return float(c3[(m, "proofnet_lean3", "nl_eos")][key])
rows = []
# (size, family, base id, fine-tune label, fine-tuned id, how)
fam = [("124M", "GPT-2", "gpt2_base", [("gpt4-more", "gpt2_gpt4more"), ("MMA", "gpt2_mma")]),
       ("2B", "Gemma-2-2B", "gemma_base", [("gpt4-more (1 ep)", "gemma_gpt4more_1ep"), ("gpt4-more (5 ep)", "gemma_gpt4more_5ep"), ("MMA", "gemma_mma")])]
out = ["| size | model | fine-tune data | CE ProofNet Lean 3: base -> fine-tuned (change) | TFA ProofNet Lean 3 (points) | ProofNet pass@16 base -> fine-tuned (points) | MiniF2F pass@16 base -> fine-tuned (points) |", "|---|---|---|---|---|---|---|"]
for size, f, base, fts in fam:
    for lab, ft in fts:
        cb, cf = ce3(base, "ce_full_paper_style"), ce3(ft, "ce_full_paper_style")
        tb, tf = 100 * ce3(base, "tfa"), 100 * ce3(ft, "tfa")
        if base == "gpt2_base":
            pn = mf = "base not sampled"
        else:
            pn = f"{p3[(base,'proofnet_lean4','16')]:.1f} -> {p3[(ft,'proofnet_lean4','16')]:.1f} ({p3[(ft,'proofnet_lean4','16')]-p3[(base,'proofnet_lean4','16')]:+.1f})"
            mf = f"{p3[(base,'minif2f_lean4','16')]:.1f} -> {p3[(ft,'minif2f_lean4','16')]:.1f} ({p3[(ft,'minif2f_lean4','16')]-p3[(base,'minif2f_lean4','16')]:+.1f})"
        out.append(f"| {size} | {f} | {lab} | {cb:.2f} -> {cf:.2f} ({cf-cb:+.2f}) | {tb:.1f} -> {tf:.1f} ({tf-tb:+.1f}) | {pn} | {mf} |")
cb = ce4["base"]["proofnet_lean3:test"]; tb = 100 * cb["tfa_mean"]
b16 = pk4("base", "fewshot", "proofnet_lean4", 16)
for lab, m in [("gpt4-more (3 ep, LoRA)", "gpt4more"), ("MMA (1 ep, LoRA)", "mma"), ("on-the-fly backtranslation (3 ep, LoRA)", "otf2")]:
    c = ce4[m]["proofnet_lean3:test"]; tf = 100 * c["tfa_mean"]
    p = pk4(m, "nl_eos", "proofnet_lean4", 16); q = pk4(m, "nl_eos", "minif2f_lean4", 16)
    out.append(f"| 8B | Llama-3-8B | {lab} | {cb['ce_full_paper_style']:.2f} -> {c['ce_full_paper_style']:.2f} ({c['ce_full_paper_style']-cb['ce_full_paper_style']:+.2f}) | {tb:.1f} -> {tf:.1f} ({tf-tb:+.1f}) | {b16:.1f} -> {p:.1f} ({p-b16:+.1f}) | base not run with a comparable prompt (0.0 with the training prompt) -> {q:.1f} |")
open("results/size_vs_gain.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))
