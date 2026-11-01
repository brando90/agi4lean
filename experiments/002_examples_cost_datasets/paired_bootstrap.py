"""Paired bootstrap and sign-flip test for the gap in mean eval loss between two models, from per-example losses.

Use when experiment 003 has saved per-example (or per-block) cross-entropy for both models on the same eval items.
Input: two CSV files with columns id,loss (same ids); prints the mean gap, a 95% bootstrap interval and a paired p-value.
Example: python paired_bootstrap.py losses_gpt4more.csv losses_mma.csv --seed 0 --n 10000
Self-test with simulated losses: python paired_bootstrap.py --selftest
"""
import argparse, csv, random


def paired(a, b, n, seed):
    rng = random.Random(seed)
    d = [x - y for x, y in zip(a, b)]
    m = sum(d) / len(d)
    boots = sorted(sum(d[rng.randrange(len(d))] for _ in d) / len(d) for _ in range(n))
    lo, hi = boots[int(0.025 * n)], boots[int(0.975 * n) - 1]
    ge = sum(abs(sum(x if rng.random() < .5 else -x for x in d) / len(d)) >= abs(m) for _ in range(n))
    return m, lo, hi, (ge + 1) / (n + 1)


def read(p):
    return {r["id"]: float(r["loss"]) for r in csv.DictReader(open(p))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("a", nargs="?"); ap.add_argument("b", nargs="?")
    ap.add_argument("--n", type=int, default=10000); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        r = random.Random(1)
        base = [r.gauss(1.7, 0.6) for _ in range(185)]
        x = [v + r.gauss(0.03, 0.3) for v in base]
        print("simulated: true gap 0.03, per-item paired sd 0.3, 185 items ->", paired(x, base, a.n, a.seed))
    else:
        A, B = read(a.a), read(a.b)
        ids = sorted(set(A) & set(B))
        print(len(ids), "paired items; gap, 95% CI low, high, p =", paired([A[i] for i in ids], [B[i] for i in ids], a.n, a.seed))
