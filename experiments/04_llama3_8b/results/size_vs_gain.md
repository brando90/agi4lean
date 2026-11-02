| size | model | fine-tune data | CE ProofNet Lean 3: base -> fine-tuned (change) | TFA ProofNet Lean 3 (points) | ProofNet pass@16, base (3-shot) -> fine-tuned (points) | MiniF2F pass@16, base (3-shot) -> fine-tuned (points) |
|---|---|---|---|---|---|---|
| 124M | GPT-2 | gpt4-more | 3.81 -> 3.30 (-0.51) | 25.2 -> 33.7 (+8.5) | base not sampled | base not sampled |
| 124M | GPT-2 | MMA | 3.81 -> 3.41 (-0.40) | 25.2 -> 48.0 (+22.8) | base not sampled | base not sampled |
| 2B | Gemma-2-2B | gpt4-more (1 ep) | 2.50 -> 2.23 (-0.28) | 40.2 -> 56.1 (+16.0) | 15.6 -> 51.6 (+36.0) | 67.7 -> 84.6 (+16.9) |
| 2B | Gemma-2-2B | gpt4-more (5 ep) | 2.50 -> 2.71 (+0.21) | 40.2 -> 56.0 (+15.9) | 15.6 -> 64.0 (+48.5) | 67.7 -> 86.9 (+19.2) |
| 2B | Gemma-2-2B | MMA | 2.50 -> 1.81 (-0.70) | 40.2 -> 60.2 (+20.0) | 15.6 -> 47.0 (+31.5) | 67.7 -> 93.6 (+25.9) |
| 8B | Llama-3-8B | gpt4-more (3 ep, LoRA), training prompt | 1.97 -> 1.61 (-0.37) | 57.3 -> 66.4 (+9.1) | 41.4 -> 24.0 (-17.4) | 98.2 -> 70.9 (-27.3) |
| 8B | Llama-3-8B | gpt4-more (3 ep, LoRA), 3-shot prompt | 1.97 -> 1.61 (-0.37) | 57.3 -> 66.4 (+9.1) | 41.4 -> 38.9 (-2.4) | 98.2 -> 93.4 (-4.7) |
| 8B | Llama-3-8B | MMA (1 ep, LoRA), training prompt | 1.97 -> 1.80 (-0.18) | 57.3 -> 65.3 (+8.0) | 41.4 -> 23.6 (-17.8) | 98.2 -> 80.0 (-18.2) |
| 8B | Llama-3-8B | MMA (1 ep, LoRA), 3-shot prompt | 1.97 -> 1.80 (-0.18) | 57.3 -> 65.3 (+8.0) | 41.4 -> 37.8 (-3.6) | 98.2 -> 94.2 (-3.9) |
| 8B | Llama-3-8B | on-the-fly backtranslation (3 ep, LoRA), training prompt | 1.97 -> 1.76 (-0.21) | 57.3 -> 66.5 (+9.2) | 41.4 -> 37.7 (-3.7) | 98.2 -> 83.9 (-14.3) |
| 8B | Llama-3-8B | on-the-fly backtranslation (3 ep, LoRA), 3-shot prompt | 1.97 -> 1.76 (-0.21) | 57.3 -> 66.5 (+9.2) | 41.4 -> 47.8 (+6.4) | 98.2 -> 95.5 (-2.7) |
