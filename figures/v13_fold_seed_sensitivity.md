# v1.3 fold-seed sensitivity (Qwen3-1.7B / Gemma 2 2B / Llama 3.2 3B)

Fixed v1.3 paper data (n=784); only `random_state` of the 5-fold CV split varies. Tests how much of the reported `h_adds_vs_strongest` margin is sensitive to a particular fold split, holding the dataset and pipeline constant.

## qwen3_1_7b

### `correct` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 82.40% (L18, +/- 3.05) | `text_plus_domain_plus_cat` 79.97% | **+2.42 pp** |
| 1 | 83.29% (L21, +/- 1.94) | `text_plus_domain_plus_cat` 80.23% | **+3.06 pp** |
| 2 | 82.53% (L18, +/- 1.29) | `text_plus_domain_plus_cat` 79.46% | **+3.06 pp** |
| 3 | 82.91% (L19, +/- 2.24) | `text_plus_domain_plus_cat` 79.59% | **+3.32 pp** |
| 4 | 82.65% (L19, +/- 2.95) | `text_plus_domain_plus_cat` 79.97% | **+2.68 pp** |

**h_adds across 5 fold seeds: `+2.91 ± 0.35 pp`** (within fold std band? NO)

### `correct_within_pre` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 84.81% (L18, +/- 3.81) | `text_plus_domain_plus_cat` 81.77% | **+3.04 pp** |
| 1 | 83.79% (L17, +/- 4.98) | `text_plus_domain_plus_cat` 82.44% | **+1.35 pp** |
| 2 | 85.81% (L22, +/- 2.77) | `text_plus_domain` 82.44% | **+3.37 pp** |
| 3 | 84.45% (L21, +/- 2.02) | `text_plus_domain_plus_cat` 83.10% | **+1.35 pp** |
| 4 | 83.42% (L21, +/- 3.68) | `text_plus_domain_plus_cat` 82.76% | **+0.67 pp** |

**h_adds across 5 fold seeds: `+1.96 ± 1.18 pp`** (within fold std band? yes)

### `correct_within_obscure` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 80.47% (L7, +/- 6.30) | `text_only` 83.03% | **-2.56 pp** |
| 1 | 82.37% (L2, +/- 7.66) | `text_plus_domain` 80.43% | **+1.94 pp** |
| 2 | 78.99% (L7, +/- 6.40) | `text_only` 79.03% | **-0.04 pp** |
| 3 | 79.16% (L8, +/- 5.42) | `text_only` 79.76% | **-0.60 pp** |
| 4 | 79.87% (L2, +/- 15.54) | `text_plus_domain` 81.10% | **-1.23 pp** |

**h_adds across 5 fold seeds: `-0.50 ± 1.65 pp`** (within fold std band? yes)

## gemma_2_2b

### `correct` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 89.67% (L14, +/- 2.22) | `text_plus_domain_plus_cat` 88.01% | **+1.66 pp** |
| 1 | 89.79% (L14, +/- 1.94) | `text_plus_domain_plus_cat` 87.50% | **+2.30 pp** |
| 2 | 89.80% (L16, +/- 0.89) | `text_plus_domain_plus_cat` 88.26% | **+1.54 pp** |
| 3 | 89.54% (L16, +/- 1.04) | `text_plus_domain_plus_cat` 87.37% | **+2.17 pp** |
| 4 | 89.80% (L14, +/- 3.62) | `text_plus_domain_plus_cat` 87.63% | **+2.17 pp** |

**h_adds across 5 fold seeds: `+1.97 ± 0.34 pp`** (within fold std band? NO)

### `correct_within_pre` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 91.21% (L17, +/- 1.28) | `tfidf` 87.48% | **+3.73 pp** |
| 1 | 92.56% (L15, +/- 4.10) | `tfidf` 88.18% | **+4.39 pp** |
| 2 | 92.23% (L16, +/- 2.05) | `tfidf` 88.52% | **+3.71 pp** |
| 3 | 90.55% (L26, +/- 4.58) | `tfidf` 88.20% | **+2.35 pp** |
| 4 | 91.22% (L17, +/- 1.95) | `tfidf` 88.51% | **+2.71 pp** |

**h_adds across 5 fold seeds: `+3.38 ± 0.83 pp`** (within fold std band? NO)

### `correct_within_obscure` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 88.88% (L24, +/- 5.26) | `tfidf` 86.90% | **+1.98 pp** |
| 1 | 89.55% (L26, +/- 4.76) | `tfidf` 86.24% | **+3.31 pp** |
| 2 | 89.57% (L8, +/- 3.10) | `tfidf` 86.99% | **+2.58 pp** |
| 3 | 89.51% (L9, +/- 3.92) | `tfidf` 86.26% | **+3.25 pp** |
| 4 | 90.86% (L25, +/- 2.39) | `tfidf` 84.37% | **+6.49 pp** |

**h_adds across 5 fold seeds: `+3.52 ± 1.75 pp`** (within fold std band? yes)

## llama_3_2_3b

### `correct` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 94.26% (L13, +/- 1.28) | `text_plus_domain_plus_cat` 91.84% | **+2.42 pp** |
| 1 | 94.52% (L17, +/- 1.59) | `text_plus_domain_plus_cat` 91.96% | **+2.55 pp** |
| 2 | 94.26% (L27, +/- 1.27) | `text_plus_domain_plus_cat` 92.22% | **+2.04 pp** |
| 3 | 94.51% (L28, +/- 0.96) | `text_plus_domain_plus_cat` 91.84% | **+2.68 pp** |
| 4 | 94.38% (L24, +/- 2.48) | `text_plus_domain_plus_cat` 92.34% | **+2.04 pp** |

**h_adds across 5 fold seeds: `+2.35 ± 0.29 pp`** (within fold std band? NO)

### `correct_within_pre` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 85.16% (L13, +/- 4.22) | `tfidf` 80.41% | **+4.75 pp** |
| 1 | 85.47% (L28, +/- 4.36) | `text_plus_domain` 80.41% | **+5.07 pp** |
| 2 | 85.45% (L11, +/- 4.54) | `tfidf` 80.75% | **+4.70 pp** |
| 3 | 87.18% (L12, +/- 1.92) | `tfidf` 80.75% | **+6.43 pp** |
| 4 | 85.47% (L23, +/- 3.13) | `tfidf` 80.75% | **+4.73 pp** |

**h_adds across 5 fold seeds: `+5.14 ± 0.74 pp`** (within fold std band? NO)

### `correct_within_obscure` (n=)

| fold_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 81.72% (L13, +/- 3.77) | `tfidf` 75.18% | **+6.54 pp** |
| 1 | 79.74% (L10, +/- 3.77) | `tfidf` 75.18% | **+4.56 pp** |
| 2 | 79.16% (L12, +/- 6.47) | `tfidf` 75.18% | **+3.98 pp** |
| 3 | 78.49% (L11, +/- 5.03) | `tfidf` 75.18% | **+3.31 pp** |
| 4 | 80.43% (L14, +/- 3.92) | `tfidf` 75.18% | **+5.25 pp** |

**h_adds across 5 fold seeds: `+4.73 ± 1.24 pp`** (within fold std band? NO)

