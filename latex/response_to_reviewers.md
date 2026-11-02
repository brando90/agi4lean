# Response to reviewers (ICLR 2025 submission 8846, OpenReview Qdp7hlenr6)

Revision 2. Status as of 2026-11-02. "In the paper" means `iclr2025_conference.tex` / `.pdf` in this folder. Experiment folders are in `../experiments/`. Every number below says what ran. All new results are Lean-checked compilation (Lean 4.15 with Mathlib, statement compiles with `sorry` allowed, not equal to gold) or cross-entropy on model log-probabilities; no language model judged any output. No differential testing (no DT) is involved. Sampling, training and cross-entropy ran on free university GPUs (skampere1), the Lean check on CPU.

Meta-review reasons (small models only, one benchmark, one metric, novelty of backtranslation) map to C3, C1, C2 and C9. Short answer: C1, C2, C3, C4, C5, C7, C9, C10, C11, C13, C14 are addressed; C8 is partly addressed; C6 and C12 are not done yet.

## Headline of the new results

- The GPT-2 evaluation-loss advantage of gpt4-more over MMA holds in order but not in size: 3.30 vs 3.41 on re-evaluation (paper table: 3.12 vs 3.88; slides: 2.33 vs 2.69). On formal tokens alone MMA is better (TFCE 3.03 vs 3.59).
- In Lean-checked pass@k the gpt4-more vs MMA gap has no single sign: Gemma-2-2B 5 epochs ProofNet pass@1 +4.7 points, MiniF2F -4.0; Gemma-2-2B 1 epoch ProofNet +0.3 (p = 0.60), MiniF2F -6.6; GPT-2 -5.6 and -11.8 (the GPT-2 gpt4-more checkpoint does not follow a usable prompt).
- Llama-3-8B (LoRA), pass@16 against the 3-shot base: on-the-fly backtranslation +6.4 points on ProofNet [0.9, 12.0], the only fine-tune above the base; gpt4-more -2.4 and MMA -3.6 within noise; MiniF2F base already 98.2%, every fine-tune 2.7 to 4.7 points lower.
- A compile check is not a faithfulness check: it accepts 94.5% of ProofNet gold statements taken from a different task and 99.1% on MiniF2F.

| # | Complaint | Status | What changed or ran | Where |
|---|---|---|---|---|
| C1 | Only ProofNet | Done | MiniF2F added: CE, TFA, Lean-checked pass@k for GPT-2 and Gemma-2-2B (225 tasks with a usable gold statement) and Llama-3-8B (244 tasks) | Section 6, Tables 4 and 5; `03_passk_small_models`, `04_llama3_8b` |
| C2 | Only eval loss, no pass@k | Done | Lean-checked pass@1/4/16/32 (3 sampling seeds for GPT-2 and Gemma, n = 32; 1 seed, n = 100 for Llama) next to CE, TFCE and TFA. Trust controls show pass@k is a compile rate, stated in Limitations | Section 6, Limitations |
| C3 | Only GPT-2 124M | Done for 2B and 8B | Gemma-2-2B (released checkpoints) and Llama-3-8B (LoRA rank 64: base, gpt4-more, MMA 1 epoch, on-the-fly backtranslation on 2,000 MMA formal statements). Size-vs-gain: TFA gain +8.5 to +22.8 (GPT-2), +16 to +20 (Gemma), +8 to +9 (Llama); ProofNet pass@16 gain +31 to +48 (Gemma) vs at most +6.4 (Llama). Llemma-7B and other math models not run | Section 6; `04_llama3_8b/results/size_vs_gain.md` |
| C4 | ProofNet contamination | Done (text overlap, CPU, not Lean-checked) | All 40 files of AI4M and UDACA checked against ProofNet and MiniF2F valid/test. MMA, gpt4-more, both individual-tactics sets and the regex sets: 0 overlap | Section 4.2, Appendix D; `01_contamination_check` |
| C5 | Which proof types work | Done | Per-category pass@1: ProofNet by book, MiniF2F by family. Gemma gpt4-more 5 epochs leads on Artin, Dummit-Foote, Herstein (17.6, 14.3, 19.4% vs MMA 6.9, 5.5, 5.8%); MMA leads on Pugh and every MiniF2F family except algebra; Rudin, Munkres, Axler hardest (at most 6.6%) | Section 6 (findings); `03_passk_small_models/results/per_category.csv` |
| C6 | Weak baseline, missing Lean Workbook, FormL4, FIMO | Not done | Same-token-budget fine-tuning on the public sets (experiment 05) has not run; it is listed in Limitations as open | Limitations |
| C7 | No before/after on an existing method or larger LLM | Done | Base vs fine-tuned pass@k for Gemma-2-2B (15.6 -> 47.0 to 64.0 ProofNet pass@16) and Llama-3-8B (41.4 -> 37.8 to 47.8), same 3-shot prompt for base and fine-tune | Section 6, Tables 4 and 5 |
| C8 | Small gap, other methods do not beat MMA | Partly | Paired sign-flip tests and bootstrap intervals over tasks on the gpt4-more vs MMA gap, 3 sampling seeds. There are no training seeds: the released checkpoints are single runs, stated in Limitations. The paper's CE gap does not reproduce in size (0.11 vs 0.76) | Section 6, Table 3, Limitations; `03_passk_small_models` |
| C9 | Novelty vs backtranslation and process reward models | Done (writing) | Claim narrowed in abstract, introduction ("What is not new") and Related Work: backtranslation is from machine translation, distilled backtranslation for autoformalization is ProofNet's, MMA scaled it, step-level supervision is the idea of process reward models (Lightman et al. 2023; Uesato et al. 2022). What we add: the on-the-fly variant, Lean proof states as context for tactic-level informalization, and a controlled comparison with MMA. The new Llama-3-8B result is the first test of the on-the-fly variant beyond GPT-2 | Abstract, Section 1, Section 7 |
| C10 | No examples in main text | Done | Figure 5: one before/after pair per method from the released data; five per method in the experiment folder | Section 4; `002_examples_cost_datasets` |
| C11 | No cost analysis | Done (estimates) | Table 2: pairs, tokens, estimated GPT-4 API cost per method at list price (lower bounds; no billing or wall-clock record exists). The paper's 1,754-token figure for individual tactics matches neither public set (20,261 or 50,145 tokens) | Section 4.1; `002_examples_cost_datasets` |
| C12 | GPT-4 vs Gemini informalization | Not done | Needs a Gemini key cleared for this use; open in Limitations | Limitations |
| C13 | Other formal languages (Metamath) | Done (scope) | Limitations: Lean 4 only; methods rely on Lean tactic states; no transfer claim | Limitations |
| C14 | Human in the loop | Done (scope) | Limitations: all pairs automatic, only human-written text is the six prompt examples; human review or correction not studied | Limitations |

## Changes to claims

- Table 3 now shows the first-reported and the re-evaluated eval loss side by side. The four rows not re-evaluated (individual tactics, regex, on-the-fly, and the baseline's original 75.18) keep their original values and say so. The baseline of 75.18 does not reproduce (3.81); the cause was not found.
- Takeaways 1 and 3, the first observation in Section 5, the Discussion and the Conclusion were weakened: the six-shot data wins on GPT-2 evaluation loss only; in pass@k the result depends on model size and benchmark.
- The title ("How High-Quality Data Beats Diverse Multilingual Data") is unchanged and is stronger than the new evidence supports; the authors decide whether to change it.

## Caveats

- Main text is now 12 pages (the ICLR limit was 10); Section 6 can move to an appendix if a limit applies.
- The Llama-3-8B rows use LoRA, MMA for 1 epoch (not 3) and one sampling seed; on-the-fly backtranslation was trained on 2,000 MMA formal statements because the LeanDojo corpus is not on Hugging Face.
- Prompts for GPT-2 and Gemma were chosen per model on ProofNet validation (5 formats), so models are compared at their own best prompt.

## Open items

- Experiment 05 (Lean Workbook, FormL4, FIMO at the same token budget; Gemini informalization): not run.
- The four GPT-4 Lean4 datasets from the alignment version of the paper are not identified in any file; see `002_examples_cost_datasets`.
