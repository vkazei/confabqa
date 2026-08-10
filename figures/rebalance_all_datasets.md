# Cross-dataset 50/50 class-balanced rebalance test

For each (dataset, model, target), sample N correct + N wrong items (N = min of class size and 400), refit probe + 4 prompt baselines with the standard 5-fold CV pipeline, repeat across 5 subsample seeds. Reports `h_adds vs strongest prompt baseline` as mean ± std across subsamples.

## Summary

| dataset/target | n per class | n subsamples | mean h_adds | std |
|---|--:|--:|--:|--:|
| `v13_qwen3_1_7b_correct` | 235 | 5 | **+5.36 pp** | 2.44 |
| `v13_qwen3_1_7b_correct_within_pre` | 140 | 5 | **+1.57 pp** | 0.65 |
| `v13_qwen3_1_7b_correct_within_obscure` | 51 | 5 | **+0.96 pp** | 1.88 |
| `v13_gemma_2_2b_correct` | 250 | 5 | **+4.92 pp** | 0.99 |
| `v13_gemma_2_2b_correct_within_pre` | 90 | 5 | **+3.00 pp** | 1.45 |
| `v13_gemma_2_2b_correct_within_obscure` | 55 | 5 | **+2.91 pp** | 1.63 |
| `v13_llama_3_2_3b_correct` | 240 | 5 | **+1.17 pp** | 0.43 |
| `v13_llama_3_2_3b_correct_within_pre` | 57 | 5 | **+11.20 pp** | 2.49 |
| `v13_llama_3_2_3b_correct_within_obscure` | 38 | 5 | **+8.95 pp** | 3.05 |
| `popqa_qwen3_1_7b_full` | 354 | 5 | **+4.43 pp** | 0.68 |
| `triviaqa_qwen3_1_7b_full` | 400 | 5 | **+9.50 pp** | 1.11 |

## Comparison to unbalanced (single-seed paper) numbers

| dataset/target | unbalanced single-seed | balanced 50/50 (mean±std) | delta |
|---|--:|--:|--:|
| `v13_qwen3_1_7b_correct` | +2.42 pp paper §6.5, single fold seed | **+5.36 ± 2.44 pp** | +2.94 pp |
| `v13_qwen3_1_7b_correct_within_pre` | +3.04 pp paper §6.5 | **+1.57 ± 0.65 pp** | -1.47 pp |
| `v13_qwen3_1_7b_correct_within_obscure` | -2.56 pp paper §6.5 — the 'cleanest refutation' | **+0.96 ± 1.88 pp** | +3.52 pp |
| `v13_gemma_2_2b_correct` | +1.66 pp paper §6.10 | **+4.92 ± 0.99 pp** | +3.26 pp |
| `v13_gemma_2_2b_correct_within_pre` | +3.73 pp | **+3.00 ± 1.45 pp** | -0.73 pp |
| `v13_gemma_2_2b_correct_within_obscure` | +1.98 pp | **+2.91 ± 1.63 pp** | +0.93 pp |
| `v13_llama_3_2_3b_correct` | +2.42 pp paper §6.10 | **+1.17 ± 0.43 pp** | -1.25 pp |
| `v13_llama_3_2_3b_correct_within_pre` | +4.75 pp | **+11.20 ± 2.49 pp** | +6.45 pp |
| `v13_llama_3_2_3b_correct_within_obscure` | +6.54 pp | **+8.95 ± 3.05 pp** | +2.41 pp |
| `popqa_qwen3_1_7b_full` | +0.50 pp PopQA seed=0 | **+4.43 ± 0.68 pp** | +3.93 pp |
| `triviaqa_qwen3_1_7b_full` | +4.54 pp TriviaQA 3-seed mean | **+9.50 ± 1.11 pp** | +4.96 pp |
