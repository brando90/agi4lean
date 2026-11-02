# 04 Llama-3-8B: base and fine-tuned (gpt4-more, MMA, on-the-fly backtranslation)

STATUS: 3-shot rows on MiniF2F and for the fine-tunes are running (second review round); other rows final.

## What ran and where
- Model: meta-llama/Meta-Llama-3-8B. Fine-tuning is **LoRA** (r=64, alpha=128, dropout 0.05, all linear layers, lr 1e-4, bf16, batch 16, seed 0), not a full fine-tune: full fine-tuning of 8B needs more than 130 GB, more than one free A100-80GB.
- Hardware: skampere1 (Stanford), one A100-80GB per run, free hardware only. No paid API and no LLM reading anywhere in this folder.
- Fine-tuning data (train_logs/runs/*/train_meta.json):
  - gpt4-more: 348 pairs, 3 epochs, 66 steps, 5.5 min.
  - MMA: 84,679 pairs, **1 epoch** (the paper used 3 on GPT-2; cut for time), 5,293 steps, 1.9 h.
  - on-the-fly backtranslation: 2,000 Lean statements (formal sides of MMA, because the paper's LeanDojo theorem corpus is not on Hugging Face; deviation from the paper). During training the model being trained writes the English informal statement itself (3-shot Lean-to-English prompt), then is trained on (its own informal, Lean) pairs. 3 epochs, 375 steps, 58 min. Share of informal sides that were not English text: 0.15%.
- Evaluation, all on test splits: CE (paper style), TFCE and TFA on ProofNet Lean 3 (186 tasks, the paper's set), ProofNet-v3 Lean 4 (183 tasks) and MiniF2F Lean 4 (244 tasks); Lean-checked pass@k.
- Lean-checked pass@k: n = 100 sampled Lean formalizations per task, 1 sampling seed (vLLM + LoRA, temperature sampling), unbiased pass@k estimator, 95% bootstrap interval over tasks. A sample counts when Lean 4.15 + Mathlib reports no error on the theorem statement (sorry allowed). It is a compile check, **not** semantic equality with the gold statement. Gold statements compile 174/176 (ProofNet) and 223/225 (MiniF2F) among the convertible ones. Task loading and candidate cutting are copied from experiments/03_passk_small_models so rows match.
- "base" has two prompts: the training prompt (informal statement, Lean statement follows), where the base model has never seen the format and produces 0% theorem-shaped output, and the 3-shot prompt from lean4ai (reference row, ProofNet only).
- Not DT: nothing here involves differential testing.

## Results

Labels: no DT, Lean-checked compile, LoRA r=64, skampere1 A100-80GB, 1 sampling seed. **Prompt used: "training prompt" rows score the fine-tuned model zero-shot with the prompt it was trained on; "3-shot prompt" rows give the model the same 3 worked examples as the base row. The base model scores 0.0 with the training prompt, so compare base (3-shot) with the 3-shot rows for a like-for-like comparison.** pass@16 is in percent; TFA and CE are on ProofNet Lean 3 test.

| model | ProofNet pass@16 | MiniF2F pass@16 | TFA | CE |
|---|---|---|---|---|
| base (3-shot prompt) | 41.4% | not run | 57.3% | 1.97 |
| base (training prompt, no shots) | 0.0% | 0.0% | 57.3% | 1.97 |
| + gpt4-more (training prompt) | 24.0% | 70.9% | 66.4% | 1.61 |
| + MMA (training prompt) | 23.6% | 80.0% | 65.3% | 1.80 |
| + on-the-fly backtranslation (training prompt) | 37.7% | 83.9% | 66.5% | 1.76 |

Note on "base (training prompt, no shots)": 0.0% does not mean the base model cannot do the task. The base model never saw the training format (informal statement followed by the end-of-text token), so it does not write a Lean theorem after it. With 3 shots it does (row above). Wide tables (all k, bootstrap intervals, all three CE columns per task set) are in the appendix and in results/.


## Findings
PENDING: rewritten after the 3-shot runs.

## Appendix: wide tables

### Lean-checked pass@k, ProofNet-v3 Lean 4 test, 183 tasks (percent, [95% bootstrap interval over tasks]; n = 100 samples per task, 1 sampling seed)

| model | prompt | pass@1 | pass@4 | pass@16 | pass@32 | pass@100 | theorem-shaped samples |
|---|---|---|---|---|---|---|---|
| base (3-shot prompt) | fewshot | 9.5 [7.3, 11.9] | 23.1 [18.9, 27.7] | 41.4 [35.7, 47.5] | 50.9 [44.6, 56.9] | 65.0 [57.9, 72.1] | 95.0% |
| base (training prompt, no shots) | nl_eos | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0% |
| + gpt4-more (training prompt) | nl_eos | 5.7 [3.7, 7.7] | 13.4 [9.7, 17.3] | 24.0 [19.1, 29.3] | 30.9 [25.1, 36.7] | 42.1 [35.0, 49.2] | 99.1% |
| + MMA (training prompt) | nl_eos | 7.3 [4.7, 10.1] | 14.6 [10.5, 19.0] | 23.6 [18.5, 28.8] | 28.8 [23.1, 34.4] | 38.3 [31.1, 45.4] | 100.0% |
| + on-the-fly backtranslation (training prompt) | nl_eos | 8.3 [6.2, 10.7] | 20.5 [16.4, 24.8] | 37.7 [32.1, 43.5] | 47.3 [41.2, 53.3] | 63.9 [56.3, 71.0] | 100.0% |

### Lean-checked pass@k, MiniF2F Lean 4 test, 244 tasks (same)

| model | prompt | pass@1 | pass@4 | pass@16 | pass@32 | pass@100 | theorem-shaped samples |
|---|---|---|---|---|---|---|---|
| base (training prompt, no shots) | nl_eos | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0% |
| + gpt4-more (training prompt) | nl_eos | 23.4 [20.3, 26.4] | 48.2 [43.6, 52.8] | 70.9 [66.2, 75.3] | 79.5 [75.3, 83.5] | 89.8 [85.7, 93.4] | 99.7% |
| + MMA (training prompt) | nl_eos | 32.2 [28.4, 35.9] | 57.3 [52.8, 61.7] | 80.0 [76.1, 83.7] | 87.3 [83.6, 90.7] | 94.3 [91.0, 97.1] | 100.0% |
| + on-the-fly backtranslation (training prompt) | nl_eos | 32.9 [29.6, 36.3] | 62.1 [57.8, 66.1] | 83.9 [80.4, 87.2] | 90.9 [88.0, 93.5] | 97.1 [95.1, 98.8] | 100.0% |

### CE (paper style), TFCE and TFA, test splits (single run each)

| model | ProofNet Lean 3 CE | TFCE | TFA | ProofNet Lean 4 CE | TFCE | TFA | MiniF2F CE | TFCE | TFA |
|---|---|---|---|---|---|---|---|---|---|
| base | 1.97 | 2.59 | 57.3% | 2.07 | 2.75 | 54.4% | 1.90 | 2.49 | 61.6% |
| + gpt4-more | 1.61 | 1.70 | 66.4% | 1.65 | 1.77 | 66.0% | 1.66 | 1.70 | 69.1% |
| + MMA | 1.80 | 1.66 | 65.3% | 1.75 | 1.58 | 66.5% | 1.72 | 1.45 | 68.5% |
| + on-the-fly backtranslation | 1.76 | 1.69 | 66.5% | 1.73 | 1.64 | 66.6% | 1.79 | 1.45 | 70.0% |

### Size vs gain (GPT-2 and Gemma-2-2B rows from experiments/03, Llama-3-8B from this folder)

Gain = fine-tuned minus base, same metric, same task set. Llama-3-8B base pass@16 is the 3-shot prompt row. GPT-2 base was not sampled in 03. Gemma and GPT-2 rows are full fine-tunes (see 03), Llama-3-8B is LoRA, so size and fine-tune method change together.

| size | model | fine-tune data | CE ProofNet Lean 3: base -> fine-tuned (change) | TFA ProofNet Lean 3 (points) | ProofNet pass@16, base (3-shot) -> fine-tuned (points) | MiniF2F pass@16, base (3-shot) -> fine-tuned (points) |
|---|---|---|---|---|---|---|
| 124M | GPT-2 | gpt4-more | 3.81 -> 3.30 (-0.51) | 25.2 -> 33.7 (+8.5) | base not sampled | base not sampled |
| 124M | GPT-2 | MMA | 3.81 -> 3.41 (-0.40) | 25.2 -> 48.0 (+22.8) | base not sampled | base not sampled |
| 2B | Gemma-2-2B | gpt4-more (1 ep) | 2.50 -> 2.23 (-0.28) | 40.2 -> 56.1 (+16.0) | 15.6 -> 51.6 (+36.0) | 67.7 -> 84.6 (+16.9) |
| 2B | Gemma-2-2B | gpt4-more (5 ep) | 2.50 -> 2.71 (+0.21) | 40.2 -> 56.0 (+15.9) | 15.6 -> 64.0 (+48.5) | 67.7 -> 86.9 (+19.2) |
| 2B | Gemma-2-2B | MMA | 2.50 -> 1.81 (-0.70) | 40.2 -> 60.2 (+20.0) | 15.6 -> 47.0 (+31.5) | 67.7 -> 93.6 (+25.9) |
| 8B | Llama-3-8B | gpt4-more (3 ep, LoRA), training prompt | 1.97 -> 1.61 (-0.37) | 57.3 -> 66.4 (+9.1) | 41.4 -> 24.0 (-17.4) | not run |
| 8B | Llama-3-8B | MMA (1 ep, LoRA), training prompt | 1.97 -> 1.80 (-0.18) | 57.3 -> 65.3 (+8.0) | 41.4 -> 23.6 (-17.8) | not run |
| 8B | Llama-3-8B | on-the-fly backtranslation (3 ep, LoRA), training prompt | 1.97 -> 1.76 (-0.21) | 57.3 -> 66.5 (+9.2) | 41.4 -> 37.7 (-3.7) | not run |

## Failed first on-the-fly backtranslation run (not counted)
The first run (otf) did not write English: the model's informal side was often just "by" or Lean code, so it was not backtranslation. Its rows (ProofNet pass@10 34.8%, pass@100 72.1%; MiniF2F pass@10 83.8%) are kept in results/ for the record and are not in any table. Fixed with a 3-shot Lean-to-English prompt and a logged share of bad informal sides (0.15%), rerun as otf2 (the on-the-fly rows above). A second bug (one task's shared Lean file errored) was fixed by rechecking one candidate per file.

## Not done
- Base Llama-3-8B with the 3-shot prompt on MiniF2F pass@k: not run (no free job slot on the host when finishing), so the MiniF2F gain over base is not computed; the training-prompt base row is 0.0 only because the format is unseen. The 3-shot examples are MiniF2F AMC problems, so a MiniF2F few-shot base row needs a contamination note.
- MMA 1 epoch only; one sampling seed; no semantic-equality check.

## Files
- code: train_lora.py (gpt4-more, MMA), train_lora_v2.py (on-the-fly backtranslation), ce_tfa.py, passk.py, lean_check.py, common.py; make_tables.py, aggregate.py, size_vs_gain.py build the tables.
- results/ce, results/passk: summaries and per-task counts; results/results.csv, pass_at_k_table.csv, headline_tables.md, size_vs_gain.md.
- train_logs/: training meta and loss logs per fine-tune.
