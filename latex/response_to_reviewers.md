# Response to reviewers (ICLR 2025 submission 8846, OpenReview Qdp7hlenr6)

Revision 1. Status as of 2026-11-01. "In the paper" means `iclr2025_conference.tex` / `.pdf` in this folder. Experiment folders are in `../experiments/`. Every number below says what ran; nothing here is Lean-checked unless it says so.

Meta-review reasons (small models only, one benchmark, one metric, novelty of backtranslation) map to C3, C1, C2 and C9.

| # | Complaint | Status | What changed or ran | Where |
|---|---|---|---|---|
| C1 | Only ProofNet | In progress | MiniF2F CE, TFA and Lean-checked pass@k for GPT-2 and Gemma-2-2B (experiment 03) and Llama-3-8B (experiment 04) are running; not in this revision | `03_passk_small_models`, `04_llama3_8b` |
| C2 | Only eval loss, no pass@k | In progress | Lean-checked pass@k (k sampled Lean formalizations per problem, counted when Lean compiles them) is being added; Limitations now says eval loss is not compilation | Limitations; experiments 03, 04 |
| C3 | Only GPT-2 124M | In progress | Gemma-2-2B (03) and Llama-3-8B base, gpt4-more, MMA and on-the-fly (04) on free hardware; Limitations names the scope | Limitations; experiments 03, 04 |
| C4 | ProofNet contamination | Done (text overlap, CPU, not Lean-checked) | All 40 files of AI4M and UDACA checked against ProofNet and MiniF2F valid/test. MMA and gpt4-more: 0 overlap, as are both individual-tactics sets and the regex sets. Several other released sets hold ProofNet or MiniF2F items | Section 4.2, Appendix D; `01_contamination_check` |
| C5 | Which proof types work | In progress | Per-category breakdown is part of experiment 03 | `03_passk_small_models` |
| C6 | Weak baseline, missing Lean Workbook, FormL4, FIMO | In progress | Same-token-budget fine-tuning on the public sets (experiment 05) | `05_*` (not yet on main) |
| C7 | No before/after on an existing method or larger LLM | In progress | Base vs fine-tuned pass@k on Llama-3-8B (04) | `04_llama3_8b` |
| C8 | Small gap, other methods do not beat MMA | Partly | Limitations says only GPT-4 data beat MMA here and the gap is small. No per-example losses were saved, so a significance test was not possible; experiment 03 saves them and adds seeds | Limitations; `002_examples_cost_datasets`; 03 |
| C9 | Novelty vs backtranslation and process reward models | Done (writing) | Claim narrowed in abstract, introduction ("What is not new") and Related Work: backtranslation is from machine translation, distilled backtranslation for autoformalization is ProofNet's, MMA scaled it, step-level supervision is the idea of process reward models (Lightman et al. 2023; Uesato et al. 2022). What we add: the on-the-fly variant, Lean proof states as context for tactic-level informalization, and a controlled comparison with MMA at small token budgets. Six-shot full-proof is stated to follow ProofNet's recipe | Abstract, Section 1, Section 6 |
| C10 | No examples in main text | Done | Figure 5: one before/after pair per method, drawn at random from the released data; five per method in the experiment folder | Section 4; `002_examples_cost_datasets` |
| C11 | No cost analysis | Done (estimates) | Table 2: pairs, tokens, estimated GPT-4 API cost per method at list price. They are lower bounds, no billing or wall-clock record exists. The paper's 1,754-token figure for individual tactics does not match either public set (20,261 or 50,145 tokens); both are reported | Section 4.1; `002_examples_cost_datasets` |
| C12 | GPT-4 vs Gemini informalization | Not started | Needs a Gemini key cleared for this use | experiment 05 |
| C13 | Other formal languages (Metamath) | Done (scope) | Limitations: Lean 4 only; methods rely on Lean tactic states, Metamath would need another step segmentation; no transfer claim | Section 8 |
| C14 | Human in the loop | Done (scope) | Limitations: all pairs are automatic, the only human-written text is the six prompt examples; human review or correction not studied | Section 8 |

## Open items for the next revision

- Table 3 (eval loss, GPT-2): preliminary re-evaluation of the released GPT-2 checkpoints with this repository's code gives a different gap than the paper's table (gpt4-more 3.30, MMA 3.41, base GPT-2 3.81; paper: 3.12, 3.88, 75.18). The ordering holds. Table 3 and the abstract are to be updated from experiment 03 once it lands.
- Fold in experiments 03, 04, 05 as they land (pass@k, MiniF2F, larger models, baseline datasets, Gemini informalization), and rewrite the abstract and Limitations to match.
- The four GPT-4 Lean4 datasets from the alignment version of the paper are not identified in any file; see `002_examples_cost_datasets`.
