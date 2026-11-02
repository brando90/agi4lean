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
