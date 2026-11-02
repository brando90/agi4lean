"""Sample Lean formalizations of the natural-language statements with vLLM (one model, one seed per call).

For each task set: n samples at T=0.7, top_p=0.95, top_k=50, max 256 new tokens, stop at ':=' (the statement ends
there; `to_candidate` appends ':= sorry'), plus one greedy sample. The seed is the vLLM seed of this process.
Example:
  python generate.py --model gpt2_mma --seed 0 --n 64 --formats mma_nl nl_eos --tasks proofnet_lean4:test minif2f_lean4:test --out out/gen
Writes out/gen/<model>__<format>__seed<seed>.jsonl (one file per format): one line per task with `samples` (n texts) and `greedy`.
"""
import argparse, json, os
from common import MODELS, FORMATS, load_tasks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n", type=int, default=64)
    ap.add_argument("--formats", nargs="+", default=["mma_nl"])
    ap.add_argument("--tasks", nargs="+", default=["proofnet_lean4:test", "minif2f_lean4:test"])
    ap.add_argument("--gpu-mem", type=float, default=0.2)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    todo = [f for f in a.formats if not os.path.exists(f"{a.out}/{a.model}__{f}__seed{a.seed}.jsonl")]
    if not todo:
        print("all exist"); return
    from vllm import LLM, SamplingParams
    llm = LLM(model=MODELS[a.model][0], dtype="bfloat16" if MODELS[a.model][1] == "gemma" else "float32",
              seed=a.seed, gpu_memory_utilization=a.gpu_mem, max_model_len=1024 if MODELS[a.model][1] == "gpt2" else 2048, enforce_eager=False)
    tok = llm.get_tokenizer()
    sp = SamplingParams(temperature=0.7, top_p=0.95, top_k=50, max_tokens=256, n=a.n, stop=[":="])
    sg = SamplingParams(temperature=0.0, max_tokens=256, n=1, stop=[":="])
    for fmt in todo:
        pf = FORMATS[fmt][0]
        rows = []
        for t in a.tasks:
            name, split = t.split(":")
            ts = load_tasks(name, split)
            prompts = [pf(r["nl"]).replace("{EOS}", tok.eos_token) for r in ts]
            outs = llm.generate(prompts, sp)
            gouts = llm.generate(prompts, sg)
            for r, o, g in zip(ts, outs, gouts):
                rows.append(dict(dataset=name, split=split, task=r["name"], samples=[c.text for c in o.outputs], greedy=g.outputs[0].text))
            print(a.model, fmt, a.seed, name, split, len(ts), flush=True)
        f_out = f"{a.out}/{a.model}__{fmt}__seed{a.seed}.jsonl"
        with open(f_out + ".tmp", "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        os.rename(f_out + ".tmp", f_out)


if __name__ == "__main__":
    main()
