"""CE, teacher-forced CE on the formal part (TFCE) and teacher-forced accuracy (TFA) of Llama-3-8B (+ optional LoRA adapter).

Same definitions as experiments/03_passk_small_models/ce_tfa.py (so rows are comparable with GPT-2 and Gemma-2-2B):
  ce_full : mean token cross-entropy over the whole sequence "<informal><eos><formal>" (the paper's eval_loss counts the
            natural-language part too); reported as the paper does (mean over batches of 4 of each batch's token mean,
            "paper_style") and as a plain token mean.
  tfce    : mean cross-entropy over the formal-statement tokens only, given the informal statement (teacher forcing).
  tfa     : fraction of formal-statement tokens whose argmax prediction equals the gold token.
Max 512 tokens; BOS added by the Llama-3 tokenizer.
Example:
  python ce_tfa.py --adapter runs/gpt4more/adapter --name gpt4more --tasks proofnet_lean3:test proofnet_lean4:test minif2f_lean4:test --out results/ce
  python ce_tfa.py --name base --tasks proofnet_lean3:test ... --out results/ce        (no adapter = base model)
"""
import argparse, json, os
import numpy as np, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from common import BASE, load_tasks, fmt_nl_eos

MAXLEN = 512


@torch.no_grad()
def score(tok, model, rows):
    out = []
    for r in rows:
        pid = tok(fmt_nl_eos(r["nl"], tok.eos_token), add_special_tokens=True)["input_ids"]
        fid = tok(r["gold"], add_special_tokens=False)["input_ids"]
        ids = (pid + fid)[:MAXLEN]
        x = torch.tensor([ids]).cuda()
        logits = model(x).logits[0].float()
        nll = -torch.log_softmax(logits[:-1], -1).gather(1, x[0, 1:, None])[:, 0]
        pred = logits[:-1].argmax(-1)
        tgt = x[0, 1:]
        fm = (torch.arange(1, len(ids)) >= len(pid)).cuda()
        nf = int(fm.sum())
        out.append(dict(name=r["name"], n_tok=len(tgt), nll_sum=float(nll.sum()), n_formal=nf,
                        tfce=float(nll[fm].mean()) if nf else float("nan"),
                        tfa=float((pred[fm] == tgt[fm]).float().mean()) if nf else float("nan")))
    return out


def summarize(rows):
    vals = []
    for i in range(0, len(rows), 4):
        b = rows[i:i + 4]
        vals.append(sum(r["nll_sum"] for r in b) / sum(r["n_tok"] for r in b))
    return dict(n=len(rows), ce_full_paper_style=float(np.mean(vals)),
                ce_full_token_mean=sum(r["nll_sum"] for r in rows) / sum(r["n_tok"] for r in rows),
                tfce_mean=float(np.nanmean([r["tfce"] for r in rows])),
                tfa_mean=float(np.nanmean([r["tfa"] for r in rows])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--name", required=True)
    ap.add_argument("--tasks", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(BASE)
    model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16).cuda().eval()
    if a.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, a.adapter).eval()
    res = {}
    for t in a.tasks:
        name, split = t.split(":")
        rows = load_tasks(name, split)
        sc = score(tok, model, rows)
        res[f"{name}:{split}"] = summarize(sc)
        json.dump(sc, open(f"{a.out}/{a.name}__{name}_{split}.per_task.json", "w"))
        print(a.name, name, split, res[f"{name}:{split}"], flush=True)
    json.dump(res, open(f"{a.out}/{a.name}.summary.json", "w"), indent=1)


if __name__ == "__main__":
    main()
