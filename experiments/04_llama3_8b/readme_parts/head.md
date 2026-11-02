# 04 Llama-3-8B: base and fine-tuned (gpt4-more, MMA, on-the-fly backtranslation)

STATUS: final (all rows run, 3-shot like-for-like rows included).

## What ran and where
- Model: meta-llama/Meta-Llama-3-8B. Fine-tuning is **LoRA** (r=64, alpha=128, dropout 0.05, all linear layers, lr 1e-4, bf16, batch 16, seed 0), not a full fine-tune: full fine-tuning of 8B needs more than 130 GB, more than one free A100-80GB.
- Hardware: skampere1 (Stanford), one A100-80GB per run, free hardware only. No paid API and no LLM reading anywhere in this folder.
- Fine-tuning data (train_logs/runs/*/train_meta.json):
  - gpt4-more: 348 pairs, 3 epochs, 66 steps, 5.5 min.
  - MMA: 84,679 pairs, **1 epoch** (the paper used 3 on GPT-2; cut for time), 5,293 steps, 1.9 h.
  - on-the-fly backtranslation: 2,000 Lean statements (formal sides of MMA, because the paper's LeanDojo theorem corpus is not on Hugging Face; deviation from the paper). During training the model being trained writes the English informal statement itself (3-shot Lean-to-English prompt), then is trained on (its own informal, Lean) pairs. 3 epochs, 375 steps, 58 min. Share of informal sides that were not English text: 0.15%.
- Evaluation, all on test splits: CE (paper style), TFCE and TFA on ProofNet Lean 3 (186 tasks, the paper's set), ProofNet-v3 Lean 4 (183 tasks) and MiniF2F Lean 4 (244 tasks); Lean-checked pass@k.
- Lean-checked pass@k: n = 100 sampled Lean formalizations per task, 1 sampling seed (vLLM + LoRA, temperature sampling), unbiased pass@k estimator, 95% bootstrap interval over tasks. A sample counts when Lean 4.15 + Mathlib reports no error on the theorem statement (sorry allowed). It is a compile check, **not** semantic equality with the gold statement. Gold statements compile 174/176 (ProofNet) and 223/225 (MiniF2F) among the convertible ones. Task loading and candidate cutting are copied from experiments/03_passk_small_models so rows match.
- "base" has two prompts: the training prompt (informal statement, Lean statement follows), where the base model has never seen the format and produces 0% theorem-shaped output, and the 3-shot prompt from lean4ai (reference row, and the like-for-like rows for the fine-tunes).
- Not DT: nothing here involves differential testing.
