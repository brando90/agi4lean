# 03 Lean-checked pass@k, CE and TFA for GPT-2 and Gemma-2-2B on ProofNet and MiniF2F

No DT anywhere in this experiment (no distribution-tracking training or evaluation), every metric is "no DT".

## Headline

1. **A Lean compile is not a faithfulness check.** The same wrap, rename and Lean check accepts 96.7% of ProofNet gold statements, 0% of gold statements with one `)` deleted, and 94.5% of the gold statement of a *different* task (183 ProofNet tasks; MiniF2F, 225 tasks: 99.1%, 0%, 99.1%). Exact match with the gold statement is at most 0.3% at pass@1 and at most 2.8% at pass@32 (Gemma mma on MiniF2F; at most 0.4% on ProofNet), while pass@32 compiles for up to 99% of problems (MiniF2F). So pass@k here only says "the model writes a theorem statement that Lean accepts".
2. **gpt4-more vs mma gap, Lean-checked.** GPT-2: the mma checkpoint is far ahead (ProofNet pass@1 5.8% vs 0.2%, pass@32 78.7% vs 6.0%), but the gpt4-more checkpoint writes a theorem-shaped statement in only 29% of samples, and it behaved like base GPT-2 (free text) under all 5 prompts I tried, so this gap measures "does the checkpoint follow any usable prompt", not the quality of its Lean. Gemma-2-2B: gpt4-more 5 epochs beats mma on ProofNet (pass@1 10.5% vs 5.7%, difference +4.7 points, p < 0.001) and loses on MiniF2F (15.6% vs 19.5%, difference -4.0 points, p < 0.001); gpt4-more 1 epoch ties mma on ProofNet (6.0% vs 5.7%, p = 0.60) and loses on MiniF2F (12.9% vs 19.5%). The sign of the gap depends on the model, the number of epochs and the benchmark.
3. **CE gap, token-level.** On ProofNet Lean 3 test, GPT-2 gpt4-more has the lower whole-sequence CE (paper style) than mma (3.30 vs 3.41, difference of per-task token means -0.13, 95% interval [-0.18, -0.07], p < 0.001), but on the formal tokens alone mma is better: TFCE 3.03 vs 3.59 and TFA 48.0% vs 33.7% (both p < 0.001). The whole-sequence CE gap of gpt4-more comes from the natural-language tokens. For Gemma-2-2B, mma has the lower CE, TFCE and higher TFA than both gpt4-more checkpoints on every set (all p < 0.001).
4. **The paper's GPT-2 CE values do not reproduce, the ordering does.** The paper's eval path, re-run unchanged on the released checkpoints (ProofNet Lean 3 test, 186 problems, batches of 4), gives gpt4-more 3.30 and mma 3.41 (and base GPT-2 3.81), not 2.33 vs 2.69. The ordering (gpt4-more lower than mma, both lower than base) holds; the absolute values and the size of the gap (0.11 here vs 0.36 in the paper) do not. The paper's base-model number (75.18) looks like an evaluation artifact, not a real loss (hypothesis, not tested: the newly added `[PAD]` embedding row).

## What ran where

| Step | What | Where |
|---|---|---|
| Sampling Lean formalizations (vLLM 0.21, T = 0.7, top-p 0.95, top-k 50, max 256 tokens, stop at `:=`, plus 1 greedy sample) | `generate.py` | skampere1 (Stanford lab server), 1 GPU per model, no paid GPUs; Gemma-2-2B base from a local copy of the weights |
| CE, TFCE, TFA | `ce_tfa.py`, `ce_paper_exact.py` (paper-style CE) | skampere1 GPU |
| Lean check | `check.py`, `lean_check.py`: Lean 4.15.0 + Mathlib (the version the dataset targets), 64 workers | skampere1 **CPU**, no LLM reading anywhere |
| Tables, bootstrap, tests | `analyze.py`, `make_tables.py` | skampere1 CPU |

Every number in this folder is Lean-checked (pass@k, controls) or computed from model log-probabilities (CE, TFCE, TFA). Nothing in it is an LLM reading. API keys are not used and not in this repository.

## Setup

- Models (7 in the tables): GPT-2 `AI4M/gpt2-gpt4-more`, `AI4M/gpt2-mma-dataset`, base `gpt2` (CE only, no sampling); Gemma-2-2B `AI4M/gemma2-2b-gpt4-more-dataset` (1 epoch), `AI4M/gemma2-2b-gpt4-more-5-epochs`, `AI4M/gemma-2-2b-mma-dataset`, base `google/gemma-2-2b`. Two further uploads (`AI4M/gpt2-gpt4-more-dataset`, `AI4M/gemma-2-2b-gpt4-more`) are in `results/ce_tfa_table.csv` only; the GPT-2 `-dataset` upload has identical CE to `AI4M/gpt2-gpt4-more`.
- Sets: ProofNet-v3 Lean 4 test (183 problems, `UDACA/proofnet-v3-lean4`), MiniF2F Lean 4 test (`UDACA/minif2f-lean4`, 244 problems, 19 of which have a commented-out gold statement; pass@k uses the other 225, CE uses all 244), ProofNet Lean 3 test (186, the paper's CE set, `hoskinson-center/proofnet`).
- pass@k: **k sampled Lean formalizations per problem, counted when Lean compiles them** (Chen et al. unbiased estimator per problem from n = 32 samples, averaged over problems). Reported for k = 1, 4, 16, 32. A sample counts when it is one theorem statement (cut at `:=`, renamed to `cand_thm`, `:= sorry` appended) that compiles in the problem's header with `import Mathlib`. "Exact" means equal to the gold statement after removing whitespace.
- Seeds: 3 sampling seeds (0, 1, 2) per model and format, each with n = 32. Tables show mean ± sd over the 3 seeds and a 95% bootstrap interval over problems (2000 resamples, seeds pooled). There are no *training* seeds: each model is one released checkpoint, so CE, TFCE and TFA vary over problems only (intervals are bootstrap over problems).
- Prompt formats: the checkpoints are full-sequence fine-tunes and do not follow instructions, so a prompt format was picked per model on ProofNet-v3 Lean 4 **validation** only (182 problems, 8 samples, seed 0; 5 formats: `nl_eos`, `mma_nl`, `mma_eos`, `fs3_mma` = 3 fixed mma-train examples then the problem in mma format, `informal_formal` = "Informal Statement: ... Formal Statement: "; the highest compile rate wins). `results/format_selection.csv` has the whole validation table, `results/format_choice.json` the choice. The choice: `fs3_mma` for GPT-2 (both) and Gemma base, `informal_formal` for Gemma gpt4-more (1 and 5 epochs) and Gemma mma. Because prompts were tuned per model, pass@k compares each model at its own best of these 5 prompts, not at one shared prompt. Other prompts could change the ranking, especially for GPT-2 gpt4-more.
- CE: `ce_full_paper_style` = whole-sequence token loss (natural-language part, EOS and formal part), batches of 4, mean of the batch means, as in the paper's code. TFCE = cross entropy on the formal tokens only given the problem. TFA = share of formal tokens whose argmax equals the gold token. The tables use format `nl_eos` (problem text, EOS, formal), `results/ce_tfa_table.csv` also has `mma_nl`.
- Trust control: gold statements, gold statements with the first `)` deleted, and the gold statement of the next problem, all through the same pipeline as the samples.
- Significance of the gpt4-more vs mma gap: paired over problems, bootstrap interval of the mean difference and a sign-flip test (5000 flips; "p < 0.001" means no flip reached the observed difference). pass@k uses seeds pooled per problem; it ignores seed-to-seed variation, which is small next to the gaps (sd over seeds 0.2 to 0.6 points on pass@1).

## Results

All tables are in [`results/headline_tables.md`](results/headline_tables.md) (copied below for the main ones), the raw numbers in `results/*.csv` and `results/*.json`.

### Lean-checked pass@k on ProofNet test (percent; mean ± sd over 3 seeds [95% bootstrap interval over tasks])

| model | prompt format | pass@1 | pass@4 | pass@16 | pass@32 | greedy compiles | theorem-shaped samples |
|---|---|---|---|---|---|---|---|
| gpt2_gpt4more | fs3_mma | 0.2 ± 0.1 [0.1, 0.3] | 0.8 ± 0.4 [0.5, 1.1] | 3.0 ± 1.5 [2.0, 4.1] | 6.0 ± 2.9 [3.8, 8.2] | 0.5 | 29.1 |
| gpt2_mma | fs3_mma | 5.8 ± 0.4 [5.2, 6.4] | 20.8 ± 1.5 [19.1, 22.5] | 57.0 ± 3.9 [53.6, 60.2] | 78.7 ± 2.9 [75.0, 82.3] | 1.6 | 96.2 |
| gemma_gpt4more_1ep | informal_formal | 6.0 ± 0.3 [5.2, 6.9] | 20.7 ± 0.8 [18.2, 23.3] | 51.6 ± 2.0 [46.7, 56.7] | 67.0 ± 3.7 [61.6, 72.5] | 6.2 | 92.7 |
| gemma_gpt4more_5ep | informal_formal | 10.5 ± 0.4 [9.2, 11.9] | 31.9 ± 1.0 [28.4, 35.3] | 64.0 ± 1.8 [59.2, 68.7] | 77.4 ± 1.4 [72.7, 82.0] | 8.9 | 96.9 |
| gemma_mma | informal_formal | 5.7 ± 0.2 [4.9, 6.7] | 19.1 ± 0.7 [16.4, 21.8] | 47.0 ± 1.8 [42.3, 51.7] | 63.7 ± 3.1 [58.7, 69.0] | 3.6 | 72.0 |
| gemma_base | fs3_mma | 1.4 ± 0.1 [1.0, 1.8] | 5.0 ± 0.3 [3.9, 6.5] | 15.6 ± 1.4 [12.4, 18.8] | 24.4 ± 3.8 [19.7, 29.1] | 2.4 | 99.5 |

### Lean-checked pass@k on MiniF2F test (percent; mean ± sd over 3 seeds [95% bootstrap interval over tasks])

| model | prompt format | pass@1 | pass@4 | pass@16 | pass@32 | greedy compiles | theorem-shaped samples |
|---|---|---|---|---|---|---|---|
| gpt2_gpt4more | fs3_mma | 0.1 ± 0.0 [0.1, 0.1] | 0.3 ± 0.1 [0.2, 0.5] | 1.3 ± 0.5 [0.7, 1.9] | 2.5 ± 1.1 [1.3, 3.7] | 0.0 | 30.6 |
| gpt2_mma | fs3_mma | 11.8 ± 0.6 [11.0, 12.7] | 38.4 ± 1.6 [36.3, 40.5] | 81.9 ± 1.8 [79.6, 84.1] | 95.3 ± 0.7 [93.5, 96.7] | 8.9 | 96.7 |
| gemma_gpt4more_1ep | informal_formal | 12.9 ± 0.5 [12.1, 13.7] | 41.3 ± 1.3 [39.3, 43.4] | 84.6 ± 0.8 [82.3, 86.9] | 96.4 ± 0.9 [94.8, 98.1] | 11.4 | 92.6 |
| gemma_gpt4more_5ep | informal_formal | 15.6 ± 0.6 [14.5, 16.7] | 46.9 ± 1.6 [44.5, 49.4] | 86.9 ± 1.7 [84.5, 89.0] | 96.3 ± 0.9 [94.7, 97.9] | 15.0 | 95.6 |
| gemma_mma | informal_formal | 19.5 ± 0.5 [18.4, 20.8] | 55.6 ± 1.1 [53.3, 57.8] | 93.6 ± 0.8 [92.1, 94.8] | 99.0 ± 0.3 [98.1, 99.7] | 16.0 | 83.6 |
| gemma_base | fs3_mma | 12.9 ± 0.3 [11.3, 14.9] | 35.4 ± 1.1 [32.0, 39.0] | 67.7 ± 1.7 [63.3, 71.7] | 81.2 ± 2.0 [77.0, 85.2] | 11.6 | 99.0 |

### CE, TFCE and TFA, single released checkpoint (no training seeds), test split

| model | ProofNet Lean 3 CE (paper style) | TFCE | TFA | ProofNet Lean 4 CE | TFCE | TFA | MiniF2F CE | TFCE | TFA |
|---|---|---|---|---|---|---|---|---|---|
| gpt2_gpt4more | 3.30 | 3.59 | 33.7% | 3.52 | 3.97 | 31.0% | 3.12 | 3.59 | 35.7% |
| gpt2_mma | 3.41 | 3.03 | 48.0% | 3.49 | 3.22 | 48.8% | 3.52 | 3.29 | 47.1% |
| gpt2_base | 3.81 | 4.38 | 25.2% | 3.98 | 4.67 | 24.3% | 3.51 | 4.36 | 28.4% |
| gemma_gpt4more_1ep | 2.23 | 2.57 | 56.1% | 2.40 | 2.89 | 55.0% | 1.95 | 2.28 | 63.6% |
| gemma_gpt4more_5ep | 2.71 | 3.21 | 56.0% | 2.91 | 3.56 | 54.5% | 2.29 | 2.81 | 62.7% |
| gemma_mma | 1.81 | 1.97 | 60.2% | 1.87 | 2.10 | 60.9% | 1.72 | 1.88 | 65.0% |
| gemma_base | 2.50 | 3.25 | 40.2% | 2.74 | 3.67 | 38.0% | 2.08 | 2.65 | 54.7% |

### Trust controls (same wrap, rename and Lean check as the samples)

| set | control | tasks | compile | rate |
|---|---|---|---|---|
| ProofNet | gold (known good) | 183 | 177 | 96.7% |
| ProofNet | gold with one ')' deleted (known bad) | 183 | 0 | 0.0% |
| ProofNet | gold of another task (compiles, wrong) | 183 | 173 | 94.5% |
| MiniF2F | gold (known good) | 225 | 223 | 99.1% |
| MiniF2F | gold with one ')' deleted (known bad) | 225 | 0 | 0.0% |
| MiniF2F | gold of another task (compiles, wrong) | 225 | 223 | 99.1% |

### gpt4-more vs mma gap (paired over tasks; difference = gpt4-more minus mma; p from a sign-flip test, 5000 flips)

| set | pair | metric | difference [95% bootstrap interval] | p |
|---|---|---|---|---|
| ProofNet | gpt2_gpt4more vs gpt2_mma | Lean-checked pass@1 (prompt fs3_mma) | -5.64 points [-6.26, -5.07] | < 0.001 |
| ProofNet | gpt2_gpt4more vs gpt2_mma | Lean-checked pass@16 (prompt fs3_mma) | -53.94 points [-57.48, -50.26] | < 0.001 |
| ProofNet | gemma_gpt4more_1ep vs gemma_mma | Lean-checked pass@1 (prompt informal_formal) | +0.28 points [-0.69, +1.22] | 0.601 |
| ProofNet | gemma_gpt4more_1ep vs gemma_mma | Lean-checked pass@16 (prompt informal_formal) | +4.53 points [-0.67, +9.61] | 0.091 |
| ProofNet | gemma_gpt4more_5ep vs gemma_mma | Lean-checked pass@1 (prompt informal_formal) | +4.74 points [+3.22, +6.26] | < 0.001 |
| ProofNet | gemma_gpt4more_5ep vs gemma_mma | Lean-checked pass@16 (prompt informal_formal) | +17.00 points [+11.66, +22.62] | < 0.001 |
| MiniF2F | gpt2_gpt4more vs gpt2_mma | Lean-checked pass@1 (prompt fs3_mma) | -11.76 points [-12.58, -10.93] | < 0.001 |
| MiniF2F | gpt2_gpt4more vs gpt2_mma | Lean-checked pass@16 (prompt fs3_mma) | -80.59 points [-82.80, -78.23] | < 0.001 |
| MiniF2F | gemma_gpt4more_1ep vs gemma_mma | Lean-checked pass@1 (prompt informal_formal) | -6.64 points [-7.93, -5.30] | < 0.001 |
| MiniF2F | gemma_gpt4more_1ep vs gemma_mma | Lean-checked pass@16 (prompt informal_formal) | -8.96 points [-11.19, -6.81] | < 0.001 |
| MiniF2F | gemma_gpt4more_5ep vs gemma_mma | Lean-checked pass@1 (prompt informal_formal) | -3.95 points [-5.58, -2.43] | < 0.001 |
| MiniF2F | gemma_gpt4more_5ep vs gemma_mma | Lean-checked pass@16 (prompt informal_formal) | -6.70 points [-8.96, -4.27] | < 0.001 |
| MiniF2F (CE) | gpt2_gpt4more vs gpt2_mma | TFCE | +0.30 [+0.25, +0.34] | < 0.001 |
| MiniF2F (CE) | gpt2_gpt4more vs gpt2_mma | TFA | -11.31 points [-12.14, -10.52] | < 0.001 |
| MiniF2F (CE) | gpt2_gpt4more vs gpt2_mma | CE (token mean) | -0.41 [-0.46, -0.36] | < 0.001 |
| ProofNet Lean 3 (CE) | gpt2_gpt4more vs gpt2_mma | TFCE | +0.56 [+0.51, +0.61] | < 0.001 |
| ProofNet Lean 3 (CE) | gpt2_gpt4more vs gpt2_mma | TFA | -14.30 points [-15.35, -13.25] | < 0.001 |
| ProofNet Lean 3 (CE) | gpt2_gpt4more vs gpt2_mma | CE (token mean) | -0.13 [-0.18, -0.07] | < 0.001 |
| ProofNet Lean 4 (CE) | gpt2_gpt4more vs gpt2_mma | TFCE | +0.75 [+0.69, +0.81] | < 0.001 |
| ProofNet Lean 4 (CE) | gpt2_gpt4more vs gpt2_mma | TFA | -17.84 points [-18.91, -16.72] | < 0.001 |
| ProofNet Lean 4 (CE) | gpt2_gpt4more vs gpt2_mma | CE (token mean) | +0.01 [-0.05, +0.07] | 0.797 |
| MiniF2F (CE) | gemma_gpt4more_1ep vs gemma_mma | TFCE | +0.40 [+0.37, +0.43] | < 0.001 |
| MiniF2F (CE) | gemma_gpt4more_1ep vs gemma_mma | TFA | -1.43 points [-1.97, -0.92] | < 0.001 |
| MiniF2F (CE) | gemma_gpt4more_1ep vs gemma_mma | CE (token mean) | +0.25 [+0.23, +0.27] | < 0.001 |
| ProofNet Lean 3 (CE) | gemma_gpt4more_1ep vs gemma_mma | TFCE | +0.60 [+0.55, +0.65] | < 0.001 |
| ProofNet Lean 3 (CE) | gemma_gpt4more_1ep vs gemma_mma | TFA | -4.03 points [-4.88, -3.15] | < 0.001 |
| ProofNet Lean 3 (CE) | gemma_gpt4more_1ep vs gemma_mma | CE (token mean) | +0.42 [+0.39, +0.45] | < 0.001 |
| ProofNet Lean 4 (CE) | gemma_gpt4more_1ep vs gemma_mma | TFCE | +0.80 [+0.74, +0.85] | < 0.001 |
| ProofNet Lean 4 (CE) | gemma_gpt4more_1ep vs gemma_mma | TFA | -5.84 points [-6.72, -4.99] | < 0.001 |
| ProofNet Lean 4 (CE) | gemma_gpt4more_1ep vs gemma_mma | CE (token mean) | +0.54 [+0.51, +0.58] | < 0.001 |
| MiniF2F (CE) | gemma_gpt4more_5ep vs gemma_mma | TFCE | +0.93 [+0.88, +0.98] | < 0.001 |
| MiniF2F (CE) | gemma_gpt4more_5ep vs gemma_mma | TFA | -2.28 points [-2.80, -1.76] | < 0.001 |
| MiniF2F (CE) | gemma_gpt4more_5ep vs gemma_mma | CE (token mean) | +0.62 [+0.58, +0.65] | < 0.001 |
| ProofNet Lean 3 (CE) | gemma_gpt4more_5ep vs gemma_mma | TFCE | +1.24 [+1.17, +1.31] | < 0.001 |
| ProofNet Lean 3 (CE) | gemma_gpt4more_5ep vs gemma_mma | TFA | -4.10 points [-4.95, -3.22] | < 0.001 |
| ProofNet Lean 3 (CE) | gemma_gpt4more_5ep vs gemma_mma | CE (token mean) | +0.91 [+0.87, +0.97] | < 0.001 |
| ProofNet Lean 4 (CE) | gemma_gpt4more_5ep vs gemma_mma | TFCE | +1.47 [+1.39, +1.54] | < 0.001 |
| ProofNet Lean 4 (CE) | gemma_gpt4more_5ep vs gemma_mma | TFA | -6.39 points [-7.20, -5.50] | < 0.001 |
| ProofNet Lean 4 (CE) | gemma_gpt4more_5ep vs gemma_mma | CE (token mean) | +1.06 [+1.00, +1.11] | < 0.001 |

### Per-category breakdown

`results/per_category.csv`: pass@1 and pass@32 per source book (ProofNet: Artin, Axler, Dummit-Foote, Herstein, Ireland-Rosen, Munkres, Pugh, Putnam, Rudin, Shakarchi) and per problem family (MiniF2F: aime, algebra, amc12, amc12a, amc12b, imo, induction, mathd_algebra, mathd_numbertheory, numbertheory), seeds pooled. Some groups have 6 to 8 problems, so treat single rows as noisy. Pattern: Gemma gpt4-more 5 epochs is ahead of Gemma mma on the algebra books (Artin, Dummit-Foote, Herstein: pass@1 17.6, 14.3, 19.4% vs 6.9, 5.5, 5.8%) and Gemma mma is ahead on Pugh and on every MiniF2F family but algebra. The analysis books (Rudin, Munkres, Axler) are hardest for every model (pass@1 below 6.6%).

## Caveats

- Compile means a theorem statement that Lean accepts with `sorry`; it can be unrelated to the problem (control above). Nothing here measures faithfulness. Exact match with gold is near 0 (see headline 1).
- Pass@k on MiniF2F is saturated for the Gemma models at k = 32 (96 to 99%).
- GPT-2 gpt4-more produced theorem-shaped text for 29% of samples under its best prompt, and most of the rest is not Lean. Its low pass@k is a statement about that checkpoint under these prompts; I did not train or fix it.
- Lean timeouts: a chunk of 20 candidates got a 90 s limit (60 s for most of MiniF2F, 30 s for a last handful), a timed-out chunk is bisected, and a single candidate that times out counts as failing. Validation-set results used a 600 s chunk limit. Candidates whose chunk errors in lines before the first candidate are bisected the same way.
- Sampling is T = 0.7 for all models; no per-model temperature tuning.
- CE: one checkpoint per model, no training seeds. MiniF2F CE uses all 244 problems.

## Reproduce

```
python generate.py --model gemma_mma --seed 0 --n 32 --formats informal_formal --tasks proofnet_lean4:test minif2f_lean4:test --out out/gen
python check.py --gen out/gen --cache out/lean_cache --split test --lean-bin <lean 4.15.0> --mathlib <mathlib checkout> --workers 64
python ce_tfa.py --model gemma_mma --format mma_nl --tasks proofnet_lean3:test proofnet_lean4:test minif2f_lean4:test --out out/ce   # writes nl_eos and mma_nl
python ce_paper_exact.py --models gpt2 AI4M/gpt2-gpt4-more AI4M/gpt2-mma-dataset --out out/ce_paper_exact_gpt2.json
python analyze.py --out results && python make_tables.py > results/headline_tables.md
```

Raw generations (80 MB) and the Lean verdict cache (25 MB) are on skampere1 in `at2362/out/gen` and `at2362/out/lean_cache` and are not in this repository.

## Files

`common.py` (models, prompts, candidate extraction), `generate.py`, `lean_check.py`, `check.py`, `select_format.py`, `ce_tfa.py`, `ce_paper_exact.py`, `analyze.py`, `make_tables.py`, `data/` (copies of the evaluation sets and the 3 few-shot examples), `results/`.
