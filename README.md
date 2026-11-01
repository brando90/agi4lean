# agi4lean

Code, paper source and experiments for **Lean-ing on Quality: How High-Quality Data Beats Diverse Multilingual Data in AutoFormalization** (AI4Math).

## Links

- Paper: [arXiv 2502.15795](https://arxiv.org/abs/2502.15795) ([PDF](https://arxiv.org/pdf/2502.15795))
- Reviews: [OpenReview forum Qdp7hlenr6](https://openreview.net/forum?id=Qdp7hlenr6) (ICLR 2025, rejected; 5 reviews and a meta-review)
- Slides: [Lean-ing on Quality](https://docs.google.com/presentation/d/1ZT8ABFxaZFYrGovLRtjVMBk31NrmoL-kDbI5K8cWW2M/edit) and [Lean-ing on Quality (and Alignment)](https://docs.google.com/presentation/d/1Mpc9R-k-u8jQ93xdGsbZGxWHzkyvd9pgAzSkwbTZGCs/edit)
- Models and data: Hugging Face org [AI4M](https://huggingface.co/AI4M)
- Where the code came from: [brando90/lean4ai](https://github.com/brando90/lean4ai) (the old mixed repo, public). The CS197 paper (`latex_paper/lean4agi_cs197`, with its code `src/lean4agi`) and Soonho Kong's merged results stay in lean4ai.

## Layout

- `src/lean4math/`: the paper's code
  - `backtranslation/`: on-the-fly backtranslation. `train.py` fine-tunes GPT-2 and Gemma-2B for autoformalization, `unsupervised_trainer.py` is the Hugging Face `Trainer` subclass that generates data on the fly, `evaluate.py` evaluates on the ProofNet test set, `demo.py` tries translations by hand, `dataset_utils.py` and `dataset_metrics.py` load and measure datasets, `finetune.py` is the Gemma fine-tuning script.
  - `training/`: training and evaluation scripts for the Lean-to-natural-language models (`train.py`, `new_train.py`, `eval.py`, `utils.py`).
  - `dataset_gen/`: Lean 4 / Mathlib 4 dataset generation and token counting.
- `latex/`: paper source (ICLR 2025 template) and the compiled `iclr2025_conference.pdf`
- `experiments/`: one numbered folder per experiment, each with a README; the index is `experiments/README.md`
- `pyproject.toml`: dependencies (the package is still named `lean4ai` there)

## Provenance

- The code was moved from lean4ai with its git history (authors and dates kept: Jakob Nordhagen, Michael Souliman, Brando Miranda and others). Nothing was lost from lean4ai: it was tagged `archive/pre-agi4lean-split-2026-11-01` before anything was removed.
- No file in lean4ai states that this is the paper's code. The match rests on the backtranslation code, the commits by co-authors Jakob Nordhagen and Michael Souliman, and dataset names matching the AI4M Hugging Face org.
- An API key committed in early scripts of lean4ai was replaced by `REMOVED_KEY` in this copy's history before pushing, so commit hashes here differ from lean4ai's.
- The GPT-3.5/Mistral/Claude informalization scripts (`src/lean4agi`) belong to the CS197 paper (authors Shane Mion, Ameya Jadhav, Rishi Padmanabhan), so they stay in lean4ai. An earlier commit here held a copy of them; this repo's history still has it.

## License

Apache 2.0, see `LICENSE`.
