# Lean-ing on Quality: OpenReview complaints and missing experiments

Source of complaints: OpenReview forum Qdp7hlenr6 (ICLR 2025, submission 8846, Reject). Read 2026-11-01, signed in. 5 reviews (ratings 3, 5, 6, 3, 3), the authors' replies, the meta-review.
Source of missing experiments: slide deck "Lean-ing on Quality" (1ZT8...W2M) and "Lean-ing on Quality (and Alignment)" (1Mpc...GCs).

Meta-review reasons for rejection: small models only, one benchmark, one metric, generalization; novelty of backtranslation; the authors gave no extra experiments in rebuttal.

## Complaints and proposed fix

| # | Complaint (who) | Fix |
|---|---|---|
| C1 | Only ProofNet; generalization unclear (qeFS, 9sKw, meta) | Add MiniF2F (and Putnam if time): CE, TFA, pass@k, same models |
| C2 | Only eval loss (CE); want Lean-compiled pass@k / pass rate (uaWA, vw3k, 9hHs, meta) | Add pass@k with the Lean checker on ProofNet and MiniF2F; keep CE and TFA |
| C3 | Only GPT-2 124M; no larger or math-specialised models, no scaling (all five, meta) | Fine-tune and eval GPT-2, Gemma-2-2B, Llama-3-8B (Llemma-7B / Qwen-math / DeepSeek-math if free hardware allows); plot size vs gain |
| C4 | ProofNet contamination not addressed (qeFS) | Overlap check of every training set (MMA, GPT4-more, MathLib4/LeanDojo parts) against ProofNet and MiniF2F; report counts |
| C5 | No analysis of which proof types work (qeFS) | Per-category breakdown of ProofNet and MiniF2F results |
| C6 | Weak baseline MMA; missing Lean Workbook, FormL4, ProofNet data, FIMO (vw3k, 9hHs) | Same-token-budget fine-tuning comparison with those datasets where public |
| C7 | No before/after on an existing autoformalization method or SOTA LLM (uaWA, vw3k) | Base vs fine-tuned pass@k on the larger open models (C3) |
| C8 | Only GPT-4 data beats MMA; other generation methods do not (uaWA); CE gap 0.03 may be noise (slides) | Seeds and confidence intervals for the CE and pass@k gaps; report the negative variants plainly |
| C9 | Novelty vs known backtranslation and PRM (vw3k, uaWA, meta) | Writing: state exactly what is new (online variant, proof-state line-by-line), cite ProofNet distilled backtranslation, narrow the claim |
| C10 | No examples of generated data in the main text (uaWA, 9hHs) | Move before/after examples from Appendices A, B into the main text |
| C11 | No cost analysis (9hHs) | Table: tokens, API cost and wall-clock per generation method |
| C12 | Compare GPT-4 vs Gemini for informalization (9hHs) | Informalize the same sample with Gemini, compare CE of fine-tuned models |
| C13 | Other formal languages (Metamath) (9sKw) | Out of scope for this paper: say so in limitations |
| C14 | Human-in-the-loop (9hHs) | Out of scope: say so in limitations |

## Missing experiments from the slides (Elyas discussion)

| # | Experiment | State in slides |
|---|---|---|
| E1 | Llama-3-8B: CE, TFA, pass@k on ProofNet, base and trained on gpt4-more (and MMA) | only base TFA 58.28 |
| E2 | GPT-2 and Gemma-2-2B: pass@k on ProofNet (models AI4M/gpt2-gpt4-more, gpt2-mma-dataset, gemma2-2b-gpt4-more-dataset, -5-epochs, gemma-2-2b-mma-dataset) | CE and TFA only |
| E3 | MiniF2F Lean4: CE, pass@k, tfce for GPT-2, Gemma-2-2B, Llama-3-8B | not run |
| E4 | Gemma-2-2B gpt4-more eval loss (eval code TODO) and whether the 0.03 CE gap (1.709 vs 1.67) is significant | TODO |
| E5 | Reproduce the GPT-2 paper values (CE 2.33 gpt4-more vs 2.69 MMA) with TFA and pass@k | CE and TFA done, no pass@k |
| E6 | pass@k variability and trust control | TODO |
| E7 | On-the-fly backtranslation training on Llama-3-8B | TODO |
| E8 | Missing GPT-4 Lean4 datasets from the "Lean-ing for alignment" version (4 datasets sent, BM) | TODO |
| E9 | Putnam Lean4 eval | listed in notes only |
