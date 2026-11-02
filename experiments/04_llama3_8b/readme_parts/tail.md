## Failed first on-the-fly backtranslation run (not counted)
The first run (otf) did not write English: the model's informal side was often just "by" or Lean code, so it was not backtranslation. Its rows (ProofNet pass@10 34.8%, pass@100 72.1%; MiniF2F pass@10 83.8%) are kept in results/ for the record and are not in any table. Fixed with a 3-shot Lean-to-English prompt and a logged share of bad informal sides (0.15%), rerun as otf2 (the on-the-fly rows above). A second bug (one task's shared Lean file errored) was fixed by rechecking one candidate per file.

## Not done
- Base Llama-3-8B with the 3-shot prompt on MiniF2F pass@k: not run (no free job slot on the host when finishing), so the MiniF2F gain over base is not computed; the training-prompt base row is 0.0 only because the format is unseen. The 3-shot examples are MiniF2F AMC problems, so a MiniF2F few-shot base row needs a contamination note.
- MMA 1 epoch only; one sampling seed; no semantic-equality check.

## Files
- code: train_lora.py (gpt4-more, MMA), train_lora_v2.py (on-the-fly backtranslation), ce_tfa.py, passk.py, lean_check.py, common.py; make_tables.py, aggregate.py, size_vs_gain.py build the tables.
- results/ce, results/passk: summaries and per-task counts; results/results.csv, pass_at_k_table.csv, headline_tables.md, size_vs_gain.md.
- train_logs/: training meta and loss logs per fine-tune.
