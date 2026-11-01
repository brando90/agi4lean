# 01 Contamination check: every training set against ProofNet and MiniF2F (complaint C4)

**What ran:** text overlap only, on CPU (this agent's Linux VM, 1 core, Python 3 + numpy + pandas, about 25 min). No Lean, no GPU, no API call, no model. Counts below are text matches, not Lean-checked results. Date: 2026-11-01.

## Headline

- The paper's two main training sets are clean: `AI4M/mma-dataset` (train, valid, test: 88,536 records) and `AI4M/gpt4-more` (348 records) have **0** records overlapping any ProofNet or MiniF2F valid/test item, even at 50% of 8-grams. So do `regex_gpt4`, the Claude datasets, `UDACA/AF`, and all Isabelle MMA files.
- Several other AI4M and UDACA datasets contain eval items. Pairs sets built from ProofNet itself hold ProofNet test or valid in full. The data-selection sets (LESS, ZipFit, DSIR) hold ProofNet valid. `Code-Mixed-Dataset` and the LESS-ranked file hold the Lean 3 MiniF2F valid and test files.
- Whether a trained model used one of these sets is not known from this check. Check each model's training data before citing its ProofNet or MiniF2F numbers.

## Training sets and eval sets

Training sets (40 files from 33 repos): all datasets of the Hugging Face orgs AI4M (23) and UDACA (10 of its 14: the 4 ProofNet and MiniF2F repos are eval sets), each file separately (so mma-dataset has train, valid, test). That covers MMA, GPT4-more, the MathLib4/LeanDojo-derived sets (`leandojo-informalized`, LESS, ZipFit, DSIR, `Code-Mixed-Dataset`) and every other AI4M dataset. `UDACA/PileSubsets` is private (401) and was not checked.

Eval sets: ProofNet valid (180 distinct item names) and test (181), from UDACA/proofnet-lean4 (Lean 4, v1), proofnet-v2/v3 (changed statements), hoskinson-center/proofnet (Lean 3 statement, informal statement, informal proof); MiniF2F valid (244) and test (244), from UDACA/minif2f-lean4 and cat-searcher/minif2f-lean4 (same 244 problems in the same order, some named differently; the UDACA id is used). Each item has up to 3 kinds of view: formal statement (Lean 3 or 4, 1 to 3 variants), informal statement, informal proof. 3,240 views in total; 10 views shorter than 10 tokens were not matched (too short for n-grams).

## Method (`contam.py`)

- Text lowercased; tokens = word runs or single punctuation characters; n-gram = 8 consecutive tokens. A training record is one row (all text fields joined); `Code-Mixed-Dataset` and the LESS/math-select files are one record per line, which can be a whole file.
- For each eval view and each training record: containment = share of the view's distinct 8-grams found in the record.
- **exact**: containment 1 and the view's token sequence appears contiguously in the record (checked by string search, not only by n-grams).
- **near-duplicate**: containment at least 0.8 (the table), at least 0.5 (in `results.csv`). Near-duplicate includes exact.
- Counted per distinct eval item (an item is hit if any of its views is). `results.csv` also has record counts; `results_by_view.csv` splits by formal statement, informal statement and informal proof.

## Results

Table of distinct eval items hit, exact / at least 80% (all 40 files, per split): see `results_table.md`. Rows with any hit:

| training set (file) | records | ProofNet valid (180) | ProofNet test (181) | MiniF2F valid (244) | MiniF2F test (244) |
|---|---|---|---|---|---|
| michael-af (valid) | 185 | 180/180 | 0/3 | 0/0 | 0/0 |
| michael-af (test) | 186 | 0/3 | 181/181 | 0/0 | 0/0 |
| miniF2FInformalizations | 186 | 0/3 | 181/181 | 0/0 | 0/0 |
| minif2f_dataset (minif2fdata) | 186 | 0/3 | 181/181 | 0/0 | 0/0 |
| minif2f_dataset (test) | 186 | 3/6 | 181/181 | 0/0 | 0/0 |
| gpt-4fp_minif2f_mix | 534 | 0/3 | 181/181 | 0/0 | 0/0 |
| willy_mix_1 | 215 | 0/3 | 181/181 | 0/0 | 0/0 |
| minif2f_real | 244 | 0/0 | 0/0 | 244/244 | 1/1 |
| less-proofnet-lean4-ranked | 189,109 | 180/180 | 60/67 | 0/164 | 0/162 |
| less-proofnet-lean4-top1M | 1,115 | 180/180 | 32/37 | 0/11 | 0/6 |
| math-select-less-llama8b | 82,619 | 179/179 | 3/6 | 0/4 | 0/3 |
| zipfit-TOP1M-AF | 12,521 | 180/180 | 0/3 | 0/0 | 0/0 |
| zipfit-AF-TOP1M | 1,500 | 180/180 | 0/3 | 0/0 | 0/0 |
| ZIPFIT-train (UDACA) | 1,000 | 53/53 | 0/1 | 0/0 | 0/1 |
| DSIR-train (UDACA) | 1,000 | 38/38 | 0/0 | 0/1 | 0/2 |
| dsir-TOP1M-AF | 2,826 | 4/4 | 0/0 | 0/1 | 0/1 |
| Code-Mixed-Dataset | 185,587 | 65/68 | 60/66 | 0/164 | 0/162 |
| leandojo-informalized | 31,127 | 0/0 | 0/1 | 3/4 | 0/0 |

What the hits are (examples in `examples.md`, from `results_by_view.csv`):

- **Datasets that are ProofNet or MiniF2F.** `michael-af` valid and test are ProofNet valid and test (formal and informal statement of all 180 / 181 items). `AI4M/minif2f_dataset`, `miniF2FInformalizations`, `gpt-4fp_minif2f_mix` and `willy_mix_1` are named after MiniF2F but contain ProofNet test (181/181 items by formal statement), and `minif2f_dataset/test.jsonl` also has the ProofNet informal proofs (180). `minif2f_real` is MiniF2F valid (244/244), not test. Only `michael-af` train (249) has no overlap.
- **Selection sets built against ProofNet valid.** LESS, ZipFit, DSIR and math-select files contain ProofNet valid statements (about 180/180 for the ranked and ZipFit files); by their names this looks like the selection target, an inference not checked against their code. ProofNet test overlap is lower: 60/181 informal statements in the LESS-ranked file but only 3 by formal Lean 4 statement (exact).
- **Code-Mixed-Dataset (and the LESS-ranked file drawn from it).** Two records (one per split) are the whole OpenAI Lean 3 MiniF2F valid and test files; their statements are in Lean 3 syntax, so MiniF2F items reach 0.8 to 0.99 containment but none is exact (0/164 and 0/162 exact). 60+ ProofNet informal statements appear exactly inside Isabelle files (`theory Rudin ...`) in the same set.
- **leandojo-informalized.** 3 MiniF2F valid informal proofs appear exactly inside LLM informalizations of Mathlib theorems. These are short generic proofs, so treat as weak evidence of overlap.

## Caveats

- Text overlap, not model-based: a paraphrased or re-formalized item (different Lean version, renamed variables, a different informal wording) can fall below 0.8. Lean 3 vs Lean 4 syntax lowers containment, as seen with MiniF2F.
- 8-gram containment on short views can match common phrases (informal proofs of one line); formal-statement and informal-statement hits are the stronger signal.
- Dataset files were read as downloaded on 2026-11-01; no check of which datasets each model of the paper was trained on.

## Files

- `contam.py`: the check. `summarize.py`: builds the tables. `download.py`: fetches the data (4.7 GB).
- `results.csv` (per file and eval split: record and item counts), `results_by_view.csv`, `results_table.md` (all files), `examples.md` (up to 6 examples per file).
- `results_raw/`: one JSON per file with every hit at 0.5 or more (view text, record text up to 600 characters).
- Run: `python download.py --out data && PYTHONHASHSEED=0 python contam.py --data data --out results_raw && python summarize.py --res results_raw --out .`
- Folder number follows the task (01); the other experiment folder uses three digits (001).
