# Gemini regrade pack for ConfabQA

Independent annotator labels for all 784 ConfabQA items, used in the paper to check the
Qwen3-1.7B self-judge (agreement and Cohen's kappa in Appendix B.3).

## Files

| file                              | what                                                                       |
|----------------------------------|----------------------------------------------------------------------------|
| `judge_prompt.txt`               | Verbatim three-way grading rules + worked examples from `judge.py`         |
| `qwen3_1_7b_items.jsonl`         | 784 items, one JSON per line: id, question, gold, alternatives, answer, qwen_judge_label |
| `qwen3_1_7b_items.csv`           | Same items as a single CSV (useful for spreadsheet inspection / upload)    |
| `regrade_with_gemini.py`         | One-shot script: `GEMINI_API_KEY=... python data/gemini_regrade/regrade_with_gemini.py` |

## Expected output

`qwen3_1_7b_gemini_labels.jsonl`, one line per item:
```json
{"id": "cin_ob_01", "gemini_label": "wrong", "gemini_raw": "Label: WRONG"}
```

The script is resumable — it skips ids already present in the output file. Safe to ^C.

## Status

The labels used in the paper are `qwen3_1_7b_dr_labels.jsonl` (Gemini 3.1 Pro in Deep Research mode,
all 784 items). Agreement with the Qwen3-1.7B judge is 87.0% (Cohen's kappa 0.78); see the paper's
Appendix B.3. Claude labels exist only for the stratified 30-item sample (`data/claude_grading_v1.json`).

## Notes

- The script uses `gemini-3-pro-preview` as the model id; edit `MODEL` at the top if the
  available id differs in your account.
- ~784 calls; at Gemini's typical ~1 req/s rate, plan for ~15 minutes wall clock.
- Cost is small (short prompt, single-token answer) but check current pricing.
