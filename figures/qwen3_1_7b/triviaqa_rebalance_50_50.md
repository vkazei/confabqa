# TriviaQA 50/50 class-balanced subsample test

Pool: 2242 unique TriviaQA items across seed=0/1/2 (deduped by `triviaqa_qid`); 615 judged correct, 1627 judged wrong.

Method: sample 400 correct + 400 wrong = 800 balanced items, refit probe + 4 prompt baselines on the subsample. Repeated across 5 subsample seeds for variance.

## Per-subsample results

| sub_seed | probe peak | strongest baseline | **h adds** |
|--:|--:|--:|--:|
| 0 | 71.88% (L19, +/-1.98) | `tfidf` 61.75% | **+10.13 pp** |
| 1 | 71.12% (L28, +/-2.32) | `tfidf` 62.50% | **+8.63 pp** |
| 2 | 71.62% (L18, +/-2.39) | `tfidf` 61.25% | **+10.37 pp** |
| 3 | 69.00% (L11, +/-3.03) | `tfidf` 61.00% | **+8.00 pp** |
| 4 | 70.25% (L15, +/-4.48) | `tfidf` 59.88% | **+10.37 pp** |

**Mean across 5 balanced subsamples: `+9.50 ± 1.11 pp`**

## Comparison to unbalanced TriviaQA

| | unbalanced (38% correct, 3 sample seeds) | balanced 50/50 (5 subsample seeds) |
|---|--:|--:|
| **h adds vs strongest prompt baseline** | +4.54 ± 1.25 pp | **+9.50 ± 1.11 pp** |

**Read:** Balanced > unbalanced -> signal is genuine and stronger when class imbalance is removed
