"""Build results.csv, results_by_set.md and examples.md from the per-file JSON written by contam.py.
Usage: python summarize.py --res results_raw/ --out .
"""
import argparse, glob, json, os, csv
ap = argparse.ArgumentParser(); ap.add_argument("--res", required=True); ap.add_argument("--out", required=True); a = ap.parse_args()
KEYS = ["ProofNet/valid", "ProofNet/test", "MiniF2F/valid", "MiniF2F/test"]
rows, ex, vrows = [], [], []
for p in sorted(glob.glob(f"{a.res}/*.json")):
    if p.endswith("eval_summary.json"): continue
    r = json.load(open(p))
    for k in KEYS:
        s = r["stats"].get(k, {})
        g = lambda n: s.get(n, 0)
        rows.append({"set": r["set"].replace("__", "/"), "file": r["file"].split("/", 1)[1], "records": r["records"], "eval": k,
                     "exact_records": g("exact"), "ge80_records": g("ge80"), "ge50_records": g("ge50"),
                     "exact_items": g("items_exact"), "ge80_items": g("items_ge80"), "ge50_items": g("items_ge50")})
    agg = {}
    for h in r["hits"]:
        vt = "formal" if h["view"].startswith("formal") else h["view"]
        d = agg.setdefault((h["bench"] + "/" + h["split"], vt), {"exact": set(), "ge80": set(), "ge50": set()})
        d["ge50"].add(h["item"])
        if h["containment"] >= 0.8: d["ge80"].add(h["item"])
        if h["exact"]: d["exact"].add(h["item"])
    for (k, vt), d in sorted(agg.items()):
        vrows.append({"set": r["set"].replace("__", "/"), "file": r["file"].split("/", 1)[1], "eval": k, "view": vt,
                      "exact_items": len(d["exact"]), "ge80_items": len(d["ge80"]), "ge50_items": len(d["ge50"])})
    seen = set()
    for h in r["hits"]:
        key = (h["bench"], h["split"], h["item"], h["view"])
        if key in seen: continue
        seen.add(key)
        if len([e for e in ex if e["file"] == r["file"]]) < 6: ex.append({**h, "file": r["file"]})
with open(f"{a.out}/results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with open(f"{a.out}/results_by_view.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(vrows[0])); w.writeheader(); w.writerows(vrows)
with open(f"{a.out}/examples.md", "w") as f:
    f.write("# Examples of hits (up to 6 per file; exact first, then highest containment)\n\n")
    cur = None
    for e in ex:
        if e["file"] != cur: f.write(f"\n## {e['file']}\n"); cur = e["file"]
        f.write(f"\n- {e['bench']}/{e['split']} item `{e['item']}`, view `{e['view']}`, containment {e['containment']}, exact={e['exact']}\n")
        f.write("  - eval text: `" + e["view_text"].replace("`", "'").replace("\n", " ")[:250] + "`\n")
        f.write("  - training record: `" + e["record_text"].replace("`", "'").replace("\n", " ")[:350] + "`\n")
print(len(rows), "rows,", len(ex), "examples")
