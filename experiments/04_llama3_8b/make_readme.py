"""Build README.md from the static parts (readme_parts/*.md) and the tables in results/.

Run make_tables.py and size_vs_gain.py first. Example: python make_readme.py   (uses results/pass_at_k_table.csv, results/ce/*.summary.json)
"""
import csv, json, os

R = "results"
rows = list(csv.DictReader(open(f"{R}/pass_at_k_table.csv")))
ce = {m: json.load(open(f"{R}/ce/{m}.summary.json"))["proofnet_lean3:test"] for m in ["base", "gpt4more", "mma", "otf2"]}
get = lambda model, s: next((r["pass@16"] for r in rows if r["model"] == model and r["task_set"] == s), "not run")
order = [("base (3-shot prompt)", "base"), ("base (training prompt, no shots)", "base"),
         ("+ gpt4-more (training prompt)", "gpt4more"), ("+ gpt4-more (3-shot prompt)", "gpt4more"),
         ("+ MMA (training prompt)", "mma"), ("+ MMA (3-shot prompt)", "mma"),
         ("+ on-the-fly backtranslation (training prompt)", "otf2"), ("+ on-the-fly backtranslation (3-shot prompt)", "otf2")]
top = ["| model | ProofNet pass@16 | MiniF2F pass@16 | TFA | CE |", "|---|---|---|---|---|"]
for label, m in order:
    p, q = get(label, "proofnet_lean4"), get(label, "minif2f_lean4")
    if p == "not run" and q == "not run":
        continue
    c = ce[m]
    top.append(f"| {label} | {p}% | {q}% | {100 * c['tfa_mean']:.1f}% | {c['ce_full_paper_style']:.2f} |" if p != "not run" or q != "not run" else "")
top = "\n".join(top).replace("not run%", "not run")
part = lambda n: open(f"readme_parts/{n}.md").read()
out = (part("head") + "\n## Results\n\n" + part("prompt_line") + "\n" + top + "\n\n" + part("table_note") + "\n" + part("findings") +
       "\n## Appendix: wide tables\n\n" + open(f"{R}/headline_tables.md").read() +
       "\n### Size vs gain (GPT-2 and Gemma-2-2B rows from experiments/03, Llama-3-8B from this folder)\n\n" + part("sizegain_note") + "\n" + open(f"{R}/size_vs_gain.md").read() +
       "\n" + part("tail"))
open("README.md", "w").write(out)
