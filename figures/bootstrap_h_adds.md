# Bootstrap ranges (min to max over K=30 subsamples) on h_adds (probe − strongest prompt baseline)

Method: K=30 balanced 50/50 subsamples per cell. Each subsample: refit probe (StandardScaler→PCA(16)→LR, 5-fold CV, peak across 29 layers) and 4 prompt baselines on identical folds. Range = min to max of the K h_adds values (not a 95% CI).

| cell | n/class | mean h_adds | median | std | range | excludes 0? |
|---|--:|--:|--:|--:|---|:--:|
| `v13_qwen3_1_7b_correct` | 235 | **+4.30 pp** | +4.15 | 1.47 | [+1.70, +7.45] | **yes** |
| `v13_qwen3_1_7b_correct_within_pre` | 140 | **+1.25 pp** | +1.07 | 1.26 | [-1.07, +3.57] | no |
| `v13_qwen3_1_7b_correct_within_obscure` | 51 | **+0.95 pp** | +0.55 | 2.14 | [-2.05, +6.90] | no |
| `v13_gemma_2_2b_correct` | 250 | **+4.98 pp** | +5.00 | 1.18 | [+2.40, +7.20] | **yes** |
| `v13_gemma_2_2b_correct_within_pre` | 90 | **+2.54 pp** | +2.78 | 1.52 | [-0.56, +5.00] | no |
| `v13_gemma_2_2b_correct_within_obscure` | 55 | **+2.76 pp** | +2.73 | 1.76 | [-0.91, +6.36] | no |
| `v13_llama_3_2_3b_correct` | 240 | **+0.94 pp** | +0.83 | 0.44 | [+0.21, +1.88] | **yes** |
| `v13_llama_3_2_3b_correct_within_pre` | 57 | **+11.43 pp** | +11.42 | 3.48 | [+5.18, +19.45] | **yes** |
| `v13_llama_3_2_3b_correct_within_obscure` | 38 | **+12.26 pp** | +11.38 | 5.35 | [+2.67, +23.67] | **yes** |
| `popqa_qwen3_1_7b_full` | 354 | **+4.35 pp** | +4.38 | 0.94 | [+2.11, +6.50] | **yes** |
| `triviaqa_qwen3_1_7b_full` | 400 | **+9.57 pp** | +9.56 | 1.91 | [+5.13, +13.75] | **yes** |

**7/11** cells have a range that excludes 0: every one of the
K subsample margins is above zero. This is subsample spread, not an item-level
confidence interval.
