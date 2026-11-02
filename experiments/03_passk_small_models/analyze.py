"""Tables from out/gen (samples), out/lean_cache (Lean results) and out/ce (CE/TFA per task).

pass@k: unbiased estimator per task (Chen et al. 2021) from n samples, averaged over tasks; one value per seed,
reported as mean over seeds with the sd over seeds, and a 95% bootstrap interval over tasks (pooled seeds).
`pass` = the sample is one theorem statement that Lean 4 + Mathlib compiles (sorry allowed).
`exact` = the sample equals the gold statement after removing whitespace (no Lean involved).
Example: python analyze.py --out results
"""
import argparse, glob, json, os, re, collections
import numpy as np
from common import load_tasks, to_candidate, gold_candidate, norm, MODELS
from check import corrupt

KS = [1, 4, 16, 32]
rng = np.random.default_rng(0)


def pak(n, c, k):
    if n - c < k:
        return 1.0
    return float(1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))


def boot_ci(per_task, B=2000):
    """95% bootstrap interval of the mean over tasks."""
    x = np.asarray(per_task, float)
    idx = rng.integers(0, len(x), (B, len(x)))
    m = x[idx].mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", default="out/gen")
    ap.add_argument("--cache", default="out/lean_cache")
    ap.add_argument("--ce", default="out/ce")
    ap.add_argument("--out", default="results")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    cache = {ds: json.load(open(f"{a.cache}/{ds}.json")) for ds in ["proofnet_lean4", "minif2f_lean4"]}
    tasks = {ds: load_tasks(ds, "test") for ds in cache}
    cat = {ds: {t["name"]: t["category"] for t in tasks[ds]} for ds in tasks}
    gold = {ds: {t["name"]: norm(gold_candidate(t["gold"])) for t in tasks[ds]} for ds in tasks}

    # ---- per (model, format, dataset, seed): per-task c (passes) and e (exact matches), n
    runs = collections.defaultdict(dict)  # (model, fmt, ds) -> seed -> {task: (n, c, e, greedy_pass)}
    for f in sorted(glob.glob(f"{a.gen}/*.jsonl")):
        m, fmt, sd = re.match(r".*/(.+)__(.+)__seed(\d+)\.jsonl", f).groups()
        for l in open(f):
            r = json.loads(l)
            ds, tk = r["dataset"], r["task"]
            cands = [to_candidate(s) for s in r["samples"]]
            ok = [bool(c) and cache[ds][tk].get(c, False) for c in cands]
            ex = [bool(c) and norm(c) == gold[ds][tk] for c in cands]
            gc = to_candidate(r["greedy"])
            runs[(m, fmt, ds)].setdefault(int(sd), {})[tk] = (len(cands), sum(ok), sum(ex), bool(gc) and cache[ds][tk].get(gc, False),
                                                              len([c for c in cands if c]))
    rows = []
    percat = []
    for (m, fmt, ds), seeds in sorted(runs.items()):
        names = [t["name"] for t in tasks[ds]]
        for metric, ci in (("pass", 1), ("exact", 2)):
            res = {}
            for k in KS:
                per_seed = []
                pooled = np.zeros(len(names))
                for sd, d in seeds.items():
                    v = [pak(d[t][0], d[t][ci], k) if d[t][0] >= k else np.nan for t in names]
                    per_seed.append(np.nanmean(v)); pooled += np.nan_to_num(v) / len(seeds)
                if all(next(iter(d.values()))[0] >= k for d in seeds.values()):
                    lo, hi = boot_ci(pooled)
                    res[k] = (float(np.mean(per_seed)), float(np.std(per_seed, ddof=1)) if len(per_seed) > 1 else float("nan"), lo, hi)
            rows.append(dict(model=m, fmt=fmt, dataset=ds, metric=metric, n_seeds=len(seeds), res=res))
        # greedy and well-formed rate
        gp = np.mean([[d[t][3] for t in names] for d in seeds.values()])
        wf = np.mean([[d[t][4] / d[t][0] for t in names] for d in seeds.values()])
        rows.append(dict(model=m, fmt=fmt, dataset=ds, metric="greedy_pass", n_seeds=len(seeds), res={"g": (float(gp), 0, 0, 0)}))
        rows.append(dict(model=m, fmt=fmt, dataset=ds, metric="theorem_shaped_rate", n_seeds=len(seeds), res={"g": (float(wf), 0, 0, 0)}))
        # per category: pass@1 and pass@max-k pooled over seeds
        kmax = max(k for k in KS if k <= next(iter(next(iter(seeds.values())).values()))[0])
        for c in sorted(set(cat[ds].values())):
            ts = [t for t in names if cat[ds][t] == c]
            p1 = np.mean([[pak(d[t][0], d[t][1], 1) for t in ts] for d in seeds.values()])
            pk = np.mean([[pak(d[t][0], d[t][1], kmax) for t in ts] for d in seeds.values()])
            percat.append(dict(model=m, fmt=fmt, dataset=ds, category=c, n_tasks=len(ts), pass1=float(p1), passk=float(pk), k=kmax))
    json.dump(rows, open(f"{a.out}/passk_summary.json", "w"), indent=1)
    json.dump(percat, open(f"{a.out}/per_category.json", "w"), indent=1)
    with open(f"{a.out}/passk_table.csv", "w") as f:
        f.write("model,format,dataset,metric,n_seeds,k,mean,sd_over_seeds,ci95_lo,ci95_hi\n")
        for r in rows:
            for k, (mu, sd, lo, hi) in r["res"].items():
                f.write(f"{r['model']},{r['fmt']},{r['dataset']},{r['metric']},{r['n_seeds']},{k},{mu:.4f},{sd:.4f},{lo:.4f},{hi:.4f}\n")
    with open(f"{a.out}/per_category.csv", "w") as f:
        f.write("model,format,dataset,category,n_tasks,pass1,k,passk\n")
        for r in percat:
            f.write(f"{r['model']},{r['fmt']},{r['dataset']},{r['category']},{r['n_tasks']},{r['pass1']:.4f},{r['k']},{r['passk']:.4f}\n")

    # ---- trust controls: same pipeline on gold, corrupted gold, gold of another task
    ctrl = []
    for ds in cache:
        ts = tasks[ds]
        for name, fn in (("gold (known good)", lambda i: gold_candidate(ts[i]["gold"])),
                         ("gold with one ')' deleted (known bad)", lambda i: corrupt(gold_candidate(ts[i]["gold"]))),
                         ("gold of another task (compiles, wrong)", lambda i: gold_candidate(ts[(i + 1) % len(ts)]["gold"]))):
            ok = [cache[ds][ts[i]["name"]].get(fn(i), False) for i in range(len(ts))]
            ctrl.append(dict(dataset=ds, control=name, n=len(ts), compiles=int(sum(ok)), rate=float(np.mean(ok))))
    json.dump(ctrl, open(f"{a.out}/trust_controls.json", "w"), indent=1)

    # ---- gpt4more vs mma gap: paired bootstrap over tasks on pass@1 (pooled seeds) and on CE per task
    gaps = []
    pairs = [("gpt2_gpt4more", "gpt2_mma"), ("gemma_gpt4more_1ep", "gemma_mma"), ("gemma_gpt4more_5ep", "gemma_mma")]
    for ds in cache:
        names = [t["name"] for t in tasks[ds]]
        for fmt in sorted({k[1] for k in runs}):
            for A, Bm in pairs:
                if (A, fmt, ds) not in runs or (Bm, fmt, ds) not in runs:
                    continue
                for k in (1, 16):
                    def pooled(m):
                        S = runs[(m, fmt, ds)]
                        return np.mean([[pak(d[t][0], d[t][1], k) for t in names] for d in S.values()], axis=0)
                    diff = pooled(A) - pooled(Bm)
                    lo, hi = boot_ci(diff)
                    # sign-flip permutation test on the paired differences
                    obs = abs(diff.mean())
                    flips = np.abs((rng.choice([-1, 1], (5000, len(diff))) * diff).mean(1))
                    gaps.append(dict(kind="pass", dataset=ds, fmt=fmt, a=A, b=Bm, k=k, diff=float(diff.mean()), ci=[lo, hi], p=float((flips >= obs).mean())))
    for A, Bm in pairs:
        for key in sorted(glob.glob(f"{a.ce}/{A}__*.per_task.json")):
            kb = key.replace(f"/{A}__", f"/{Bm}__")
            if not os.path.exists(kb):
                continue
            ra, rb = json.load(open(key)), json.load(open(kb))
            for metric in ("tfce", "tfa"):
                diff = np.array([x[metric] - y[metric] for x, y in zip(ra, rb)])
                lo, hi = boot_ci(diff)
                obs = abs(np.nanmean(diff))
                flips = np.abs((rng.choice([-1, 1], (5000, len(diff))) * diff).mean(1))
                gaps.append(dict(kind=metric, file=os.path.basename(key), a=A, b=Bm, diff=float(np.nanmean(diff)), ci=[lo, hi], p=float((flips >= obs).mean())))
            # whole-sequence CE gap (per-task token-mean NLL)
            da = np.array([x["nll_sum"] / x["n_tok"] for x in ra]) - np.array([y["nll_sum"] / y["n_tok"] for y in rb])
            lo, hi = boot_ci(da)
            flips = np.abs((rng.choice([-1, 1], (5000, len(da))) * da).mean(1))
            gaps.append(dict(kind="ce_full", file=os.path.basename(key), a=A, b=Bm, diff=float(da.mean()), ci=[lo, hi], p=float((flips >= abs(da.mean())).mean())))
    json.dump(gaps, open(f"{a.out}/gap_significance.json", "w"), indent=1)

    # ---- CE summary table
    with open(f"{a.out}/ce_tfa_table.csv", "w") as f:
        f.write("model,dataset,split,format,n,ce_full_paper_style,ce_full_token_mean,tfce,tfa,ce_full_ci95_lo,ce_full_ci95_hi\n")
        for fs in sorted(glob.glob(f"{a.ce}/*.summary.json")):
            m = os.path.basename(fs).replace(".summary.json", "")
            for key, s in json.load(open(fs)).items():
                ds, sp, fmt = key.split(":")
                per = json.load(open(f"{a.ce}/{m}__{ds}_{sp}__{fmt}.per_task.json"))
                lo, hi = boot_ci([x["nll_sum"] / x["n_tok"] for x in per])
                f.write(f"{m},{ds},{sp},{fmt},{s['n']},{s['ce_full_paper_style']:.4f},{s['ce_full_token_mean']:.4f},{s['tfce_mean']:.4f},{s['tfa_mean']:.4f},{lo:.4f},{hi:.4f}\n")
    print("wrote", os.listdir(a.out))


if __name__ == "__main__":
    main()
