"""Lean-checked pass@k: sample k formalizations per problem with vLLM, count a problem when Lean compiles one.

Per task: n samples (T=0.7, top_p=0.95, max 256 new tokens, stop at ':='), each cut to one theorem statement ending
`:= sorry` (common.to_candidate; a sample that is not a single theorem statement counts as a failure) and compiled with
Lean 4.15 + Mathlib (same header the task ships with). A sample passes when Lean reports no error (sorry warning is
fine). This measures that the statement is well-formed Lean (compiles), NOT that it means the same as the gold
statement. pass@k = unbiased estimator of Chen et al. 2021 from n samples. `--gold-check` compiles the gold statements.
--format nl_eos : prompt "<informal><|end_of_text|>" (the training format; zero-shot for the base model)
--format fewshot: the 3-shot prompt of the lean4ai protocol (base-model reference; its examples are miniF2F AMC problems,
                  so use it on ProofNet only)
Example:
  python passk.py --name gpt4more --adapter runs/gpt4more/adapter --tasks proofnet_lean4:test minif2f_lean4:test \\
     --n 32 --out results/passk --lean-bin $L --mathlib $M
"""
import argparse, json, os, time
import numpy as np
from math import comb
from common import BASE, load_tasks, fmt_nl_eos, fewshot_prompt, to_candidate, gold_candidate
from lean_check import check_all


def pass_at_k(n, c, k):
    return 1.0 if n - c < k else 1.0 - comb(n - c, k) / comb(n, k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--format", default="nl_eos", choices=["nl_eos", "fewshot"])
    ap.add_argument("--tasks", nargs="+", required=True)
    ap.add_argument("--n", type=int, default=32)
    ap.add_argument("--ks", type=int, nargs="+", default=[1, 2, 4, 8, 16, 32])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-tasks", type=int, default=0)
    ap.add_argument("--gold-check", action="store_true")
    ap.add_argument("--gpu-util", type=float, default=0.85)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--lean-bin", required=True)
    ap.add_argument("--mathlib", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from vllm import LLM, SamplingParams
    from vllm.lora.request import LoRARequest
    llm = LLM(BASE, dtype="bfloat16", gpu_memory_utilization=a.gpu_util, max_model_len=4096, enable_lora=bool(a.adapter),
              max_lora_rank=64, seed=a.seed)
    tok = llm.get_tokenizer()
    lora = LoRARequest(a.name, 1, os.path.abspath(a.adapter)) if a.adapter else None
    sp = SamplingParams(n=a.n, temperature=0.7, top_p=0.95, max_tokens=256, stop=[":="], seed=a.seed)
    summary = {}
    for t in a.tasks:
        name, split = t.split(":")
        rows = load_tasks(name, split)
        if a.max_tasks:
            rows = rows[:a.max_tasks]
        if a.format == "nl_eos":
            prompts = [fmt_nl_eos(r["nl"], tok.eos_token) for r in rows]
        else:
            prompts = [fewshot_prompt(r["nl"]) for r in rows]
        t0 = time.time()
        outs = llm.generate(prompts, sp, lora_request=lora)
        t_gen = time.time() - t0
        samples = [[o.text for o in out.outputs] for out in outs]
        cands = []
        for ss in samples:
            c = []
            for s in ss:
                if a.format == "fewshot":
                    s = s.strip().lstrip("#").strip().split("##")[0]
                c.append(to_candidate(s))
            cands.append(c)
        json.dump(dict(prompts=prompts, samples=samples), open(f"{a.out}/{a.name}__{a.format}__{name}_{split}.raw_samples.json", "w"), ensure_ascii=False)
        items, idx = [], []
        for i, c in enumerate(cands):
            valid = [(j, x) for j, x in enumerate(c) if x is not None]
            items.append((rows[i]["header"], sorted({x for _, x in valid})))
        t0 = time.time()
        res = check_all(items, a.lean_bin, a.mathlib, a.workers)
        t_chk = time.time() - t0
        cs, per_task = [], []
        for i, c in enumerate(cands):
            ok = dict(zip(items[i][1], res[i]))
            flags = [bool(x is not None and ok.get(x, False)) for x in c]
            cs.append(sum(flags))
            per_task.append(dict(name=rows[i]["name"], c=cs[-1], n=len(c), n_valid_form=sum(x is not None for x in c),
                                 category=rows[i]["category"], samples=[dict(text=s, cand=x, ok=f) for s, x, f in zip(samples[i], c, flags)][:8]))
        r = {f"pass@{k}": float(np.mean([pass_at_k(a.n, c, k) for c in cs])) for k in a.ks if k <= a.n}
        r.update(tasks=len(rows), n_samples=a.n, frac_samples_single_theorem=float(np.mean([p["n_valid_form"] / p["n"] for p in per_task])),
                 seconds_generate=round(t_gen), seconds_lean_check=round(t_chk))
        if a.gold_check:
            gc = [(rw["header"], gold_candidate(rw["gold"])) for rw in rows]
            conv = [(h, [c]) for h, c in gc if c is not None]
            g = check_all(conv, a.lean_bin, a.mathlib, a.workers)
            r["gold_statements_compile"] = f"{sum(x[0] for x in g)}/{len(conv)} convertible gold statements ({len(rows) - len(conv)} of {len(rows)} gold entries are commented out or defs, cannot be turned into a theorem statement)"
        import lean_check
        r["tasks_rechecked_one_candidate_per_file"] = len(lean_check.HEADER_FALLBACKS)
        if lean_check.HEADER_FALLBACKS:
            json.dump(lean_check.HEADER_FALLBACKS, open(f"{a.out}/{a.name}__{a.format}__{name}_{split}.fallbacks.json", "w"))
        lean_check.HEADER_FALLBACKS.clear()
        summary[f"{name}:{split}"] = r
        json.dump(per_task, open(f"{a.out}/{a.name}__{a.format}__{name}_{split}.per_task.json", "w"), ensure_ascii=False)
        print(a.name, a.format, name, split, r, flush=True)
    json.dump(dict(model=a.name, adapter=a.adapter, format=a.format, seed=a.seed, results=summary,
                   criterion="Lean 4.15 + Mathlib reports no error on the sampled theorem statement (sorry allowed); not semantic equality with gold"),
              open(f"{a.out}/{a.name}__{a.format}.summary.json", "w"), indent=1)


if __name__ == "__main__":
    main()
