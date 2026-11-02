# experiments

One folder per experiment, numbered `NNN_short_name`, each with its own `README.md` (goal, exact setup, how to run, results). Results go straight to main.

| Folder | What |
|---|---|
| `001_openreview_reviews_and_missing_experiments` | The 14 complaints from the ICLR 2025 reviews (OpenReview forum Qdp7hlenr6) and the 9 missing experiments from the slide decks (E1 to E9), with the fix for each. No experiment has run yet. |
| `002_examples_cost_datasets` | Before/after examples per generation method, token and estimated API cost table, inventory of the public GPT-4 Lean4 datasets, and why the 0.03 eval-loss gap cannot be tested yet (no per-example losses saved). CPU only. |
| `01_contamination_check` | Overlap of every AI4M/UDACA training set with ProofNet and MiniF2F valid/test (complaint C4). MMA and GPT4-more: 0 overlap; several other sets hold ProofNet or MiniF2F items. CPU text overlap, not Lean-checked. |
| `03_passk_small_models` | Lean-checked pass@k (k up to 32, 3 seeds), CE, TFCE and TFA for GPT-2 and Gemma-2-2B (gpt4-more, mma, base) on ProofNet and MiniF2F, with trust controls, per-category breakdown and the gpt4-more vs mma significance. Ran on skampere1 GPUs, Lean check on CPU. |

Related runs that live (or will be committed) in [brando90/lean4ai](https://github.com/brando90/lean4ai) for now: the Qwen3 reproduction of the pass@k protocol (`experiments/qwen3_repro_2026_11_01`) and Soonho Kong's results.
