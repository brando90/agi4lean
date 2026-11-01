# agi4lean

Code for **Lean-ing on Quality: How High-Quality Data Beats Diverse Multilingual Data in AutoFormalization**, arXiv: https://arxiv.org/abs/2502.15795

Models and data: Hugging Face org [AI4M](https://huggingface.co/AI4M).

The code was moved here from [brando90/lean4ai](https://github.com/brando90/lean4ai) with its git history (authors and dates preserved). It is a history-preserving copy: nothing was deleted from lean4ai.

## What each folder holds

- `src/lean4math/backtranslation/`: on-the-fly backtranslation. `train.py` fine-tunes GPT-2 and Gemma-2B for autoformalization, `unsupervised_trainer.py` is the Hugging Face `Trainer` subclass that generates data on the fly, `evaluate.py` evaluates a model on the ProofNet test set, `demo.py` tries translations by hand, `dataset_utils.py` and `dataset_metrics.py` load, preprocess and measure datasets, `finetune.py` is the Gemma fine-tuning script. Its own `README.md` lists the files.
- `src/lean4math/training/`: training and evaluation scripts for the Lean-to-natural-language models (`train.py`, `new_train.py`, `eval.py`, `utils.py`).
- `src/lean4math/dataset_gen/`: Lean 4 / Mathlib 4 dataset generation and token counting (`lean4math_dataset_gen.py`, `get_num_tokens.py`, a sample `lean_train.jsonl`).
- `src/lean4agi/`: formal-to-informal data generation with GPT-4 and Claude (`formal_2_informal_vlllm.py`, `vllmclaude.py`, `generate_boxed.py`, the prompt and cleaning scripts) and the datasets they produced (`*.json`, `claudeclean.jsonl`), plus fine-tuning scripts for GPT-3.5, Mistral and other models.
- `pyproject.toml`: dependencies (the package is still named `lean4ai` there).

## Stays in lean4ai

The CS197 paper `latex_paper/lean4agi_cs197`, the Pantograph SFT scaling experiments (`experiments/pantograph_sft_scaling_2026`) and the pass@k scripts stay in [brando90/lean4ai](https://github.com/brando90/lean4ai).

## Provenance note

No file in lean4ai states that this is the paper's code. The match rests on the backtranslation code, the commits by co-authors Jakob Nordhagen and Michael Souliman, and dataset names matching the AI4M Hugging Face org.

## License

Apache 2.0, see `LICENSE`.

## History note

An API key that was committed in early scripts of lean4ai was replaced by `REMOVED_KEY` in this copy's history before pushing (commit hashes here therefore differ from lean4ai's). Authors, dates and messages are unchanged.
