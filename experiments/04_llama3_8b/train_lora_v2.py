"""LoRA fine-tune Llama-3-8B for autoformalization (informal -> Lean) on one of three data sources.

  --data gpt4more : AI4M/gpt4-more (GPT-4 6-shot informalizations of Mathlib4 theorems, 348 pairs)
  --data mma      : AI4M/mma-dataset train (MMA, GPT-4 zero-shot informalizations, 84,679 pairs)
  --data otf      : on-the-fly backtranslation. Only the Lean side is given (2,000 Lean statements, the formal side of
                    MMA train rows, informal side discarded). Every batch, the model being trained writes the
                    informal side itself (prompt "3-shot Lean -> English prompt"), then trains on
                    "<its informal><eos><lean>". Same idea as src/lean4math/backtranslation/unsupervised_trainer.py.

Format of every training row: "<informal><|end_of_text|><formal>", loss on the whole sequence (what the paper's
finetune.py does: labels = input ids). Max 512 tokens. LoRA (not a full fine-tune): r=64, alpha=128, all linear layers,
AdamW lr 1e-4, cosine schedule, 3% warmup, bf16 autocast, gradient checkpointing.

Example:
  python train_lora.py --data gpt4more --epochs 3 --out runs/gpt4more
"""
import argparse, json, math, os, random, re, time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from common import BASE

MAXLEN = 512


def load_pairs(which, seed):
    from huggingface_hub import hf_hub_download
    if which == "gpt4more":
        p = hf_hub_download("AI4M/gpt4-more", "train.jsonl", repo_type="dataset")
        return [(d["informal"].strip(), d["formal"].strip()) for d in map(json.loads, open(p))]
    p = hf_hub_download("AI4M/mma-dataset", "train.jsonl", repo_type="dataset")
    rows = []
    for l in open(p):
        d = json.loads(l)
        nl = d["input"].split("Statement in natural language:\n", 1)[1].rsplit("\nTranslate the statement", 1)[0]
        rows.append((nl.strip(), d["output"].strip()))
    if which == "mma":
        return rows
    rnd = random.Random(seed)
    rnd.shuffle(rows)
    return [(None, f) for _, f in rows[:2000]]  # on-the-fly: Lean side only


def encode_batch(tok, pairs, dev):
    ids = []
    for nl, f in pairs:
        a = tok(nl + tok.eos_token, add_special_tokens=True)["input_ids"]
        b = tok(f, add_special_tokens=False)["input_ids"]
        ids.append((a + b)[:MAXLEN])
    L = max(len(x) for x in ids)
    x = torch.full((len(ids), L), tok.pad_token_id)
    y = torch.full((len(ids), L), -100)
    m = torch.zeros((len(ids), L), dtype=torch.long)
    for i, s in enumerate(ids):
        x[i, :len(s)] = torch.tensor(s)
        y[i, :len(s)] = torch.tensor(s)
        m[i, :len(s)] = 1
    return x.to(dev), m.to(dev), y.to(dev), sum(len(s) for s in ids)


BT_SHOTS = None


def bt_prompt_prefix():
    """3 fixed Lean -> informal examples from gpt4-more (shortest Lean sides), so the model answers in English."""
    global BT_SHOTS
    if BT_SHOTS is None:
        pairs = sorted(load_pairs("gpt4more", 0), key=lambda p: len(p[1]))[20:23]
        BT_SHOTS = "".join(f"Lean 4 statement:\n{f}\nInformal statement in English:\n{nl}\n\n" for nl, f in pairs)
    return BT_SHOTS


@torch.no_grad()
def backtranslate(model, tok, formals, dev, max_new=128):
    """The model being trained writes the informal side of each Lean statement (greedy), 3-shot prompt Lean -> English.
    Keeps text up to the first blank line or the next 'Lean 4 statement:'."""
    model.eval()
    model.gradient_checkpointing_disable() if hasattr(model, "gradient_checkpointing_disable") else None
    tok.padding_side = "left"
    pre = bt_prompt_prefix()
    prompts = [pre + f"Lean 4 statement:\n{f}\nInformal statement in English:\n" for f in formals]
    enc = tok(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(dev)
    with torch.autocast("cuda", dtype=torch.bfloat16):
        out = model.generate(**enc, max_new_tokens=max_new, do_sample=False, pad_token_id=tok.pad_token_id,
                             use_cache=True)
    texts = tok.batch_decode(out[:, enc["input_ids"].shape[1]:], skip_special_tokens=True)
    tok.padding_side = "right"
    model.train()
    return [re.split(r"\n\s*\n|Lean 4 statement:", t.strip())[0].strip() or "(empty)" for t in texts]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", choices=["gpt4more", "mma", "otf"], required=True)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--micro-bs", type=int, default=8)
    ap.add_argument("--batch", type=int, default=16, help="rows per optimizer step")
    ap.add_argument("--max-steps", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    random.seed(a.seed); torch.manual_seed(a.seed)
    dev = "cuda"
    tok = AutoTokenizer.from_pretrained(BASE)
    tok.pad_token = "<|reserved_special_token_0|>" if tok.pad_token is None else tok.pad_token
    model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16).to(dev)
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    model = get_peft_model(model, LoraConfig(r=64, lora_alpha=128, lora_dropout=0.05, task_type="CAUSAL_LM",
                           target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]))
    model.print_trainable_parameters()
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=a.lr, weight_decay=0.0)
    data = load_pairs(a.data, a.seed)
    n_steps = a.epochs * math.ceil(len(data) / a.batch)
    if a.max_steps:
        n_steps = min(n_steps, a.max_steps)
    warm = max(1, int(0.03 * n_steps))
    sched = lambda s: (s + 1) / warm if s < warm else 0.5 * (1 + math.cos(math.pi * (s - warm) / max(1, n_steps - warm)))
    log = open(f"{a.out}/train_log.jsonl", "w")
    model.train()
    step, tokens, t0 = 0, 0, time.time()
    examples = []; bad_rows = n_rows = 0
    for ep in range(a.epochs):
        order = list(range(len(data)))
        random.Random(a.seed + ep).shuffle(order)
        for b0 in range(0, len(order), a.batch):
            if step >= n_steps:
                break
            batch = [data[i] for i in order[b0:b0 + a.batch]]
            if a.data == "otf":
                inf = []
                for c0 in range(0, len(batch), 16):
                    inf += backtranslate(model, tok, [f for _, f in batch[c0:c0 + 16]], dev)
                batch = [(i, f) for i, (_, f) in zip(inf, batch)]
                bad = sum(1 for i, _ in batch if i == "(empty)" or ":=" in i or "theorem " in i or len(re.findall(r"[A-Za-z]{3,}", i)) < 3)
                bad_rows += bad; n_rows += len(batch)  # a "bad" informal side: empty, Lean code, or fewer than 3 English-looking words
                if step % 10 == 0:
                    examples.append(dict(step=step, informal_written_by_model=batch[0][0], lean=batch[0][1], bad_share_so_far=round(bad_rows / n_rows, 3)))
                model.gradient_checkpointing_enable()
                model.enable_input_require_grads()
            loss_sum, ntok_batch = 0.0, 0
            for m0 in range(0, len(batch), a.micro_bs):
                x, m, y, nt = encode_batch(tok, batch[m0:m0 + a.micro_bs], dev)
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    logits = model(input_ids=x, attention_mask=m).logits
                lo = torch.nn.functional.cross_entropy(logits[:, :-1].float().reshape(-1, logits.size(-1)),
                                                       y[:, 1:].reshape(-1), ignore_index=-100, reduction="sum")
                cnt = int((y[:, 1:] != -100).sum())
                (lo / (a.batch * 100)).backward()  # constant scale; renormalised below
                loss_sum += float(lo); ntok_batch += cnt; tokens += nt
            for p in params:
                if p.grad is not None:
                    p.grad.mul_(a.batch * 100 / max(1, ntok_batch))
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            for g in opt.param_groups:
                g["lr"] = a.lr * sched(step)
            opt.step(); opt.zero_grad(set_to_none=True)
            step += 1
            rec = dict(step=step, epoch=ep, loss=loss_sum / max(1, ntok_batch), lr=opt.param_groups[0]["lr"],
                       tokens=tokens, sec=round(time.time() - t0))
            log.write(json.dumps(rec) + "\n"); log.flush()
            if step % 10 == 0 or step == n_steps:
                print(rec, flush=True)
    model.save_pretrained(f"{a.out}/adapter")
    json.dump(dict(data=a.data, rows=len(data), epochs=a.epochs, steps=step, batch=a.batch, lr=a.lr, tokens_seen=tokens,
                   train_seconds=round(time.time() - t0), gpu=torch.cuda.get_device_name(0), base=BASE,
                   lora=dict(r=64, alpha=128, dropout=0.05, targets="all linear"), seed=a.seed,
                   otf_examples=examples[:40], otf_bad_informal_share=(round(bad_rows / n_rows, 4) if n_rows else None)), open(f"{a.out}/train_meta.json", "w"), indent=1, ensure_ascii=False)
    print("done", step, "steps", round(time.time() - t0), "s")


if __name__ == "__main__":
    main()
