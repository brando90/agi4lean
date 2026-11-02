"""Cross-entropy (CE), teacher-forced CE on the formal part (TFCE) and teacher-forced accuracy (TFA) per task.

Modes:
  --probe   find which prompt format each model was trained on: formal-part CE on 150 gpt4-more rows and 150 mma rows
  (default) CE / TFCE / TFA of the model on a task set in the model's chosen format (--format) plus the paper's format.
Definitions (no BOS added for GPT-2, tokenizer default BOS for Gemma; max 512 tokens as in the paper's eval.py):
  ce_full   : mean token cross-entropy over the whole sequence prompt+formal (what the paper's `eval_loss` is; the
              paper's loss also counts the natural-language part). Reported as the paper does: mean over batches of 4
              of each batch's token-mean ("paper_style"), and as a plain token mean ("token_mean").
  tfce      : mean cross-entropy over the formal-statement tokens only, given the prompt (teacher forcing).
  tfa       : fraction of formal-statement tokens whose argmax prediction equals the gold token (teacher forcing).
Example:
  python ce_tfa.py --model gpt2_gpt4more --tasks proofnet_lean3:test proofnet_lean4:test minif2f_lean4:test --out out/ce
"""
import argparse, json, os, sys, urllib.request
import torch, numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from common import MODELS, FORMATS, load_tasks

MAXLEN = 512


def load(key):
    repo = MODELS[key][0]
    tok = AutoTokenizer.from_pretrained(repo)
    dt = torch.bfloat16 if MODELS[key][1] == "gemma" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(repo, torch_dtype=dt).cuda().eval()
    return tok, model


def encode(tok, prompt_fn, nl, formal):
    p = prompt_fn(nl).replace("{EOS}", tok.eos_token)
    pid = tok(p, add_special_tokens=True)["input_ids"]
    fid = tok(formal, add_special_tokens=False)["input_ids"]
    ids = (pid + fid)[:MAXLEN]
    return ids, len(pid)


@torch.no_grad()
def score(tok, model, rows, fmt):
    """rows: dicts with nl, gold. Returns per-row dict of ce_full sum/count, tfce, tfa."""
    prompt_fn = FORMATS[fmt][0]
    out = []
    for r in rows:
        ids, lp = encode(tok, prompt_fn, r["nl"], r["gold"])
        x = torch.tensor([ids]).cuda()
        logits = model(x).logits[0].float()
        lp_ = torch.log_softmax(logits[:-1], -1)
        tgt = x[0, 1:]
        nll = -lp_.gather(1, tgt[:, None])[:, 0]
        pred = logits[:-1].argmax(-1)
        fm = torch.arange(1, len(ids)) >= lp  # target positions that are formal tokens
        fm = fm.cuda()
        nf = int(fm.sum())
        out.append(dict(name=r["name"], n_tok=len(tgt), nll_sum=float(nll.sum()), n_formal=nf,
                        tfce=float(nll[fm].mean()) if nf else float("nan"),
                        tfa=float((pred[fm] == tgt[fm]).float().mean()) if nf else float("nan")))
    return out


def paper_style(rows):
    """Mean over consecutive batches of 4 of (batch NLL sum / batch token count)."""
    vals = []
    for i in range(0, len(rows), 4):
        b = rows[i:i + 4]
        vals.append(sum(r["nll_sum"] for r in b) / sum(r["n_tok"] for r in b))
    return float(np.mean(vals))


def summarize(rows):
    return dict(n=len(rows), ce_full_paper_style=paper_style(rows),
                ce_full_token_mean=sum(r["nll_sum"] for r in rows) / sum(r["n_tok"] for r in rows),
                tfce_mean=float(np.nanmean([r["tfce"] for r in rows])),
                tfa_mean=float(np.nanmean([r["tfa"] for r in rows])))


def probe_rows():
    g = []
    for l in urllib.request.urlopen("https://huggingface.co/datasets/AI4M/gpt4-more/resolve/main/train.jsonl", timeout=60):
        d = json.loads(l)
        g.append(dict(name="g", nl=d["informal"], gold=d["formal"].strip()))
        if len(g) >= 150:
            break
    m = []
    for l in urllib.request.urlopen("https://huggingface.co/datasets/AI4M/mma-dataset/resolve/main/valid.jsonl", timeout=60):
        d = json.loads(l)
        nl = d["input"].split("Statement in natural language:\n", 1)[1].rsplit("\nTranslate the statement", 1)[0]
        m.append(dict(name="m", nl=nl, gold=d["output"].strip()))
        if len(m) >= 150:
            break
    return g, m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--format", default=None)
    ap.add_argument("--tasks", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tok, model = load(a.model)
    if a.probe:
        g, m = probe_rows()
        res = {}
        for fmt in FORMATS:
            sg = np.nanmean([r["tfce"] for r in score(tok, model, g, fmt)])
            sm = np.nanmean([r["tfce"] for r in score(tok, model, m, fmt)])
            res[fmt] = dict(tfce_gpt4more_rows=float(sg), tfce_mma_rows=float(sm), mean=float((sg + sm) / 2))
            print(a.model, fmt, res[fmt], flush=True)
        best = min(res, key=lambda f: res[f]["mean"])
        json.dump(dict(model=a.model, formats=res, best=best), open(f"{a.out}/probe_{a.model}.json", "w"), indent=1)
        print("BEST", a.model, best)
        return
    fmts = ["nl_eos"] + ([a.format] if a.format and a.format != "nl_eos" else [])
    allres = {}
    for t in a.tasks:
        name, split = t.split(":")
        rows = load_tasks(name, split)
        for fmt in fmts:
            sc = score(tok, model, rows, fmt)
            s = summarize(sc)
            allres[f"{name}:{split}:{fmt}"] = s
            json.dump(sc, open(f"{a.out}/{a.model}__{name}_{split}__{fmt}.per_task.json", "w"))
            print(a.model, name, split, fmt, s, flush=True)
    json.dump(allres, open(f"{a.out}/{a.model}.summary.json", "w"), indent=1)


if __name__ == "__main__":
    main()
