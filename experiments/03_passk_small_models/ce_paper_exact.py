"""CE exactly as the paper's evaluation code computes it (src/lean4math/backtranslation/evaluate.py + training/eval.py).

Steps copied: tokenizer.add_special_tokens({'pad_token': '[PAD]'}); model.resize_token_embeddings(len(tokenizer));
input = nl_statement + eos + formal_statement, padded to 512; labels = input_ids with pad -> -100 (the loss covers the
natural-language part too); eval_loss = mean over batches of 4 of the model's own batch loss (what Trainer.evaluate reports); dataset hoskinson-center/proofnet.
If the checkpoint's embedding matrix has no row for [PAD], resize_token_embeddings adds a randomly initialised row.
Example: python ce_paper_exact.py --models gpt2 AI4M/gpt2-gpt4-more AI4M/gpt2-mma-dataset --out out/ce_paper_exact.json
"""
import argparse, json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from common import load_tasks


def run(repo, split):
    tok = AutoTokenizer.from_pretrained(repo)
    model = AutoModelForCausalLM.from_pretrained(repo)
    rows0 = model.get_input_embeddings().weight.shape[0]
    tok.add_special_tokens({"pad_token": "[PAD]"})
    model.resize_token_embeddings(len(tok))
    rows = load_tasks("proofnet_lean3", split)
    feats = []
    for r in rows:
        enc = tok(r["nl"] + tok.eos_token + r["gold"], max_length=512, padding="max_length", truncation=True)
        lab = [(-100 if i == tok.pad_token_id else i) for i in enc["input_ids"]]
        feats.append(dict(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"], labels=lab))
    model.cuda().eval()
    losses = []
    with torch.no_grad():
        for i in range(0, len(feats), 4):  # per_device_eval_batch_size=4; eval_loss = mean of the batch losses
            b = {k: torch.tensor([f[k] for f in feats[i:i + 4]]).cuda() for k in ("input_ids", "attention_mask", "labels")}
            losses.append(float(model(**b).loss))
    return dict(model=repo, split=split, eval_loss=sum(losses) / len(losses), embedding_rows_in_checkpoint=rows0, rows_after_resize=len(tok))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = [run(m, s) for m in a.models for s in ("test",)]
    for r in res:
        print(r)
    json.dump(res, open(a.out, "w"), indent=1)
