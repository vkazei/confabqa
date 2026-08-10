# Gemini regrade pack for ConfabQA-784

Goal: produce a third-annotator label set on the *real* benchmark so the paper can drop
the legacy ConfabQA-133 calibration entirely and report a Gemini-vs-Claude-vs-Qwen
three-way calibration on ConfabQA-784.

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

## What I'll do once you hand back `qwen3_1_7b_gemini_labels.jsonl`

1. Compute Gemini-vs-Qwen agreement and Cohen's κ on all 784 items (full-set, not 30-item sample).
2. Compute Gemini-vs-Claude agreement (need Claude labels regenerated on the full 784 too;
   currently we only have them on a 30-item sample — let me know if you want me to package
   that as a follow-up).
3. Compute the three-way Fleiss κ on whichever subset has all three annotators present.
4. Update §5 to report ConfabQA-784 calibration with the *real* annotator identities
   (Gemini 3.1 Pro replacing the "human author" label, which was inaccurate).
5. Drop every ConfabQA-133 mention from the paper, README, dataset card, and CITATION.cff.

## Notes

- The script uses `gemini-3-pro-preview` as the model id; edit `MODEL` at the top if the
  available id differs in your account.
- ~784 calls; at Gemini's typical ~1 req/s rate, plan for ~15 minutes wall clock.
- Cost is small (short prompt, single-token answer) but check current pricing.
