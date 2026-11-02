
### gpt4-more vs mma gap, CE, TFCE and TFA (paired over tasks; difference = gpt4-more minus mma; p from a sign-flip test, 5000 flips)

| set | pair | metric | difference [95% bootstrap interval] | p |
|---|---|---|---|---|
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
