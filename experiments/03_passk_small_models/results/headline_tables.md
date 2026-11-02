
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
