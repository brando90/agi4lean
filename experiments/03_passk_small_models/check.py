"""Lean-check every distinct candidate statement from all generations, once, with a cache.

Reads out/gen/*.jsonl, builds candidates with common.to_candidate, adds the trust controls (gold statements,
corrupted gold, gold of another task), compiles each distinct (task, candidate) with Lean 4 + Mathlib and writes
out/lean_cache/<dataset>.json: {task: {candidate: bool}}. Candidates already in the cache are skipped.
A candidate passes when Lean reports no error on it (`sorry` allowed): it is a well-formed Lean statement that
elaborates. This says nothing about faithfulness to the natural-language statement.
Example:
  python check.py --lean-bin $B/.elan/toolchains/leanprover--lean4---v4.15.0/bin/lean --mathlib $B/mathlib4_15_0 --workers 32
"""
import argparse, glob, json, os, re, random
from concurrent.futures import ThreadPoolExecutor, as_completed
from common import load_tasks, to_candidate, gold_candidate
from lean_check import check_chunked


def corrupt(c):
    """Known-bad control: delete the first ')' or, if none, the first ':' after the name (breaks the statement)."""
    i = c.find(")")
    if i >= 0:
        return c[:i] + c[i + 1:]
    j = c.find(":", len("theorem cand_thm"))
    return c[:j] + c[j + 1:] if j >= 0 else c + " ("


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", default="out/gen")
    ap.add_argument("--cache", default="out/lean_cache")
    ap.add_argument("--lean-bin", required=True)
    ap.add_argument("--mathlib", required=True)
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--datasets", nargs="+", default=["proofnet_lean4", "minif2f_lean4"])
    ap.add_argument("--split", default="test")
    ap.add_argument("--chunk-timeout", type=int, default=90)
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True)
    for ds in a.datasets:
        tasks = load_tasks(ds, a.split)
        hdr = {t["name"]: t["header"] for t in tasks}
        want = {t["name"]: set() for t in tasks}
        for i, t in enumerate(tasks):
            g = gold_candidate(t["gold"])
            want[t["name"]].add(g)
            want[t["name"]].add(corrupt(g))
            want[t["name"]].add(gold_candidate(tasks[(i + 1) % len(tasks)]["gold"]))  # wrong-task control
        for f in glob.glob(f"{a.gen}/*.jsonl"):
            for l in open(f):
                r = json.loads(l)
                if r["dataset"] != ds:
                    continue
                for s in r["samples"] + [r["greedy"]]:
                    c = to_candidate(s)
                    if c:
                        want[r["task"]].add(c)
        cf = f"{a.cache}/{ds}.json"
        cache = json.load(open(cf)) if os.path.exists(cf) else {}
        todo = []
        for k, cs in want.items():
            have = cache.get(k, {})
            new = sorted(c for c in cs if c not in have)
            if new:
                todo.append((k, new))
        print(ds, "tasks", len(tasks), "distinct candidates to check", sum(len(n) for _, n in todo), flush=True)

        items = [(k, new[i:i + 20]) for k, new in todo for i in range(0, len(new), 20)]

        def work(item):
            k, new = item
            return k, new, check_chunked(hdr[k], new, a.lean_bin, a.mathlib, timeout=a.chunk_timeout)
        done = 0
        with ThreadPoolExecutor(a.workers) as ex:
            futs = [ex.submit(work, it) for it in items]
            for fu in as_completed(futs):
                k, new, res = fu.result()
                cache.setdefault(k, {}).update(dict(zip(new, map(bool, res))))
                done += 1
                if done % 5 == 0 or len(items) < 50:
                    json.dump(cache, open(cf + ".tmp", "w")); os.replace(cf + ".tmp", cf)
                    print(ds, done, "/", len(items), flush=True)
        json.dump(cache, open(cf + ".tmp", "w")); os.replace(cf + ".tmp", cf)


if __name__ == "__main__":
    main()
