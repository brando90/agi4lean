"""Contamination check: overlap of training sets with ProofNet and MiniF2F (valid/test). CPU only.

Usage: PYTHONHASHSEED=0 python contam.py --data DATA_DIR --out results/
DATA_DIR holds one folder per Hugging Face repo, named ORG__NAME (see download.py).
Method: lowercase text, tokens = \\w+ or one punctuation char, n-gram = 8 consecutive tokens (hashed).
For each eval view (formal statement, informal statement, informal proof) and each training record,
containment = share of the view's distinct 8-grams that occur in the record.
  exact : containment 1 and the view's token sequence occurs contiguously in the record
  ge80, ge50 : containment >= 0.8 / >= 0.5 (near-duplicate, includes exact)
"""
import argparse, csv, glob, json, os, re, sys
from collections import defaultdict
import numpy as np
import pandas as pd

csv.field_size_limit(10**9)
N = 8
MIN_VIEW_TOKENS = 10
TOK = re.compile(r"\w+|[^\w\s]")
MULT = np.array([0x9E3779B97F4A7C15, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9, 0x27D4EB2F165667C5,
                 0x85EBCA77C2B2AE63, 0xFF51AFD7ED558CCD, 0xC4CEB9FE1A85EC53, 0xD6E8FEB86659FD93], dtype=np.uint64)

def toks(t): return TOK.findall(t.lower())

def ngram_hashes(tokens):
    h = np.fromiter((hash(t) for t in tokens), dtype=np.int64, count=len(tokens)).view(np.uint64)
    if len(h) < N: return h[:0]
    m = len(h) - N + 1
    w = np.zeros(m, dtype=np.uint64)
    for j in range(N):
        w += h[j:j + m] * MULT[j]
    return w

def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ("file_path",): continue
            yield from strings(v)
    elif isinstance(o, list):
        for v in o: yield from strings(v)

def read_jsonl(p, key=None):
    with open(p, encoding="utf-8") as f:
        for l in f:
            if l.strip(): yield json.loads(l)

def eval_items(data):
    """-> list of (bench, split, item, viewtype, text)"""
    V = []
    def add(b, s, item, vt, text):
        if isinstance(text, str) and text.strip(): V.append((b, s, item, vt, text))
    # ProofNet
    for s in ("valid", "test"):
        for r in read_jsonl(f"{data}/UDACA__proofnet-lean4/proofnet/{s}.jsonl"):
            add("ProofNet", s, r["name"], "formal_lean4", r["formal_statement"])
            add("ProofNet", s, r["name"], "informal_statement", re.sub(r"^\s*/--|-/\s*$", "", r["informal_prefix"]))
        for r in read_jsonl(f"{data}/hoskinson-center__proofnet/{s}.jsonl"):
            n = r["id"].split("|")[-1]
            add("ProofNet", s, n, "formal_lean3", r["formal_statement"])
            add("ProofNet", s, n, "informal_statement", r["nl_statement"])
            add("ProofNet", s, n, "informal_proof", r["nl_proof"])
    for v, sp in (("v2", "validation"), ("v3", "validation"), ("v2", "test"), ("v3", "test")):
        d = pd.read_parquet(glob.glob(f"{data}/UDACA__proofnet-{v}-lean4/data/{sp}-*.parquet")[0])
        s = "valid" if sp == "validation" else "test"
        for _, r in d.iterrows():
            add("ProofNet", s, r["name"], f"formal_lean4_{v}", r["formal_statement"])
            add("ProofNet", s, r["name"], "informal_statement", r["nl_statement"])
    # MiniF2F: UDACA and cat-searcher list the same 244 problems per split in the same order (checked on the
    # informal statements) but name some differently (aime1983_1 vs aime_1983_p1); the UDACA id is the item key.
    for sp in ("validation", "test"):
        s = "valid" if sp == "validation" else "test"
        d = pd.read_parquet(f"{data}/UDACA__minif2f-lean4/data/{sp}-00000-of-00001.parquet")
        for _, r in d.iterrows():
            add("MiniF2F", s, r["id"], "formal_lean4", r["formal_statement"])
            add("MiniF2F", s, r["id"], "informal_statement", r["nl_statement"])
            add("MiniF2F", s, r["id"], "informal_proof", r["nl_proof"])
        for (_, r), c in zip(d.iterrows(), read_jsonl(f"{data}/cat-searcher__minif2f-lean4/{s}.jsonl")):
            add("MiniF2F", s, r["id"], "formal_lean4", c["formal_statement"])
            add("MiniF2F", s, r["id"], "informal_statement", c["informal_stmt"])
            add("MiniF2F", s, r["id"], "informal_proof", c["informal_proof"])
    # dedupe identical normalized text within one item
    seen, out = set(), []
    for b, s, item, vt, t in V:
        k = (b, s, item, " ".join(toks(t)))
        if k in seen: continue
        seen.add(k); out.append((b, s, item, vt, t))
    return out

EXCLUDE = ("UDACA__proofnet", "UDACA__minif2f", "hoskinson-center__", "cat-searcher__", "UDACA__PileSubsets")

def train_files(data):
    for d in sorted(os.listdir(data)):
        if d.startswith(EXCLUDE): continue
        for p in sorted(glob.glob(f"{data}/{d}/**/*", recursive=True)):
            if os.path.isdir(p) or p.endswith((".md", "dataset_infos.json")): continue
            yield d, p

def records(p):
    """yield one text per training record"""
    if p.endswith(".jsonl"):
        for o in read_jsonl(p): yield "\n".join(strings(o))
    elif p.endswith(".json"):
        o = json.load(open(p, encoding="utf-8"))
        if isinstance(o, dict): o = list(o.values()) if all(isinstance(v, (dict, list)) for v in o.values()) else [o]
        for r in o: yield "\n".join(strings(r))
    elif p.endswith(".csv"):
        with open(p, encoding="utf-8", newline="") as f:
            rd = csv.reader(f); next(rd, None)
            for row in rd: yield "\n".join(row)
    elif p.endswith(".parquet"):
        d = pd.read_parquet(p)
        for _, r in d.iterrows(): yield "\n".join(str(x) for x in r.values if isinstance(x, str))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=""); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    views = eval_items(a.data)
    vtoks = [toks(v[4]) for v in views]
    skipped = [i for i, t in enumerate(vtoks) if len(t) < MIN_VIEW_TOKENS]
    vset = [set(ngram_hashes(t).tolist()) if len(t) >= MIN_VIEW_TOKENS else set() for t in vtoks]
    h2v = defaultdict(list)
    for i, s in enumerate(vset):
        for h in s: h2v[h].append(i)
    E = np.array(sorted(h2v), dtype=np.uint64)
    vstr = [" ".join(t) for t in vtoks]
    json.dump({"views": len(views), "skipped_short": len(skipped),
               "items": {f"{b}/{s}": len({v[2] for v in views if v[0] == b and v[1] == s}) for b, s, *_ in views},
               "views_by_type": {k: sum(1 for v in views if v[3] == k) for k in {v[3] for v in views}}},
              open(f"{a.out}/eval_summary.json", "w"), indent=1)
    for d, p in train_files(a.data):
        rel = os.path.relpath(p, a.data)
        if a.only and a.only not in rel: continue
        outp = f"{a.out}/{rel.replace('/', '__')}.json"
        if os.path.exists(outp): continue
        stats = defaultdict(lambda: {"exact": set(), "ge80": set(), "ge50": set(), "items_exact": set(), "items_ge80": set(), "items_ge50": set()})
        hits = []
        nrec = 0
        def flush(batch, base):
            if not batch: return
            tl = [toks(t) for t in batch]
            lens = np.array([len(t) for t in tl]); tot = int(lens.sum())
            if tot < N: return
            flat = [x for t in tl for x in t]
            w = ngram_hashes(flat)
            rid = np.repeat(np.arange(len(batch)), lens)
            ok = rid[:len(w)] == rid[N - 1:N - 1 + len(w)]
            idx = np.searchsorted(E, w); idx[idx >= len(E)] = 0
            m = ok & (E[idx] == w)
            pos = np.nonzero(m)[0]
            if not len(pos): return
            pairs = np.unique(np.stack([rid[pos].astype(np.uint64), w[pos]], 1), axis=0)
            cnt = defaultdict(int)
            for r, h in pairs.tolist():
                for v in h2v[h]: cnt[(r, v)] += 1
            starts = np.concatenate([[0], np.cumsum(lens)])
            joined = {}
            for (r, v), c in cnt.items():
                frac = c / len(vset[v])
                if frac < 0.5: continue
                exact = False
                if frac == 1.0:
                    if r not in joined: joined[r] = " " + " ".join(flat[starts[r]:starts[r + 1]]) + " "
                    exact = (" " + vstr[v] + " ") in joined[r]
                b, s, item, vt, text = views[v]
                st = stats[(b, s)]
                rec = base + r
                st["ge50"].add(rec); st["items_ge50"].add(item)
                if frac >= 0.8: st["ge80"].add(rec); st["items_ge80"].add(item)
                if exact: st["exact"].add(rec); st["items_exact"].add(item)
                hits.append({"record": rec, "bench": b, "split": s, "item": item, "view": vt, "containment": round(frac, 3),
                             "exact": exact, "view_text": text[:300], "record_text": batch[r][:600]})
        batch, base, ntok = [], 0, 0
        for t in records(p):
            batch.append(t); nrec += 1; ntok += len(t) // 3
            if ntok > 3_000_000 or len(batch) >= 20000:
                flush(batch, base); base += len(batch); batch, ntok = [], 0
        flush(batch, base)
        res = {"file": rel, "set": d, "records": nrec,
               "stats": {f"{b}/{s}": {k: len(v) for k, v in st.items()} for (b, s), st in stats.items()},
               "hits": sorted(hits, key=lambda h: (-h["exact"], -h["containment"]))}
        json.dump(res, open(outp, "w"), ensure_ascii=False)
        print(rel, nrec, {k: (v["exact"], v["ge80"], v["ge50"]) for k, v in res["stats"].items()}, flush=True)

if __name__ == "__main__": main()
