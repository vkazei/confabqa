# TriviaQA multi-seed comparison
Same pipeline, same model (qwen3_1_7b), same hyperparameters. The only variation is `random.Random(seed)` over the validation split (n=11313). 'seed=0 rerun' uses the *same* seed=0 and therefore the *same* 800 question IDs as the original seed=0 run; the only thing that differs in the rerun is the model forward pass and judge re-eval (testing pipeline-level non-determinism from BF16/MPS).

## Sample composition

| metric | seed=0 | seed=0 rerun | seed=1 | seed=2 |
|---|--:|--:|--:|--:|
| n | 800 | 800 | 800 | 800 |
| correct | 304 | 304 | 303 | 295 |
| refusal | 11 | 11 | 8 | 10 |
| wrong | 485 | 485 | 489 | 495 |

## Full-sample null test

| metric | seed=0 | seed=0 rerun | seed=1 | seed=2 |
|---|--:|--:|--:|--:|
| majority baseline | 71.25% | 71.25% | 73.12% | 73.38% |
| TF-IDF | 70.50% | 70.50% | 74.00% | 73.25% |
| **TF-IDF − majority** | -0.75 pp | -0.75 pp | +0.88 pp | -0.12 pp |
| text-only | 71.62% | 71.62% | 73.12% | 73.38% |
| +domain | 71.62% | 71.62% | 73.12% | 73.38% |
| +category | 71.62% | 71.62% | 73.12% | 73.38% |
| strongest baseline | `text_only` (71.62%) | `text_only` (71.62%) | `tfidf` (74.00%) | `text_only` (73.38%) |
| probe peak | 76.63% (L21) | 76.75% (L21) | 77.12% (L17) | 78.88% (L22) |
| probe std at peak | 2.64 pp | 2.57 pp | 3.72 pp | 4.26 pp |
| **h adds vs strongest** | **+5.00 pp** | **+5.13 pp** | **+3.12 pp** | **+5.50 pp** |
| within per-fold std? | **NO** | **NO** | yes | **NO** |

## Determinism check (seed=0 vs seed=0 rerun)

Same 800 question IDs in both runs; differences below are from BF16/MPS forward-pass non-determinism propagating through generation, judge, and probe.

| metric | seed=0 − rerun | |
|---|--:|---|
| probe peak acc | -0.125 pp | |
| strongest baseline | +0.000 pp | |
| h adds vs strongest | -0.125 pp | |
| TF-IDF acc | +0.000 pp | |

**Pipeline is effectively deterministic** (max metric swing < 0.5 pp). Forward-pass non-determinism is
not driving any of the inter-seed differences below.

## Sample variance across distinct seeds

Across the three distinct samples (seed=0, seed=1, seed=2; excludes seed=0 rerun, which is for determinism only):

| metric | values | mean ± std |
|---|---|---:|
| probe peak acc | 76.63%, 77.12%, 78.88% | 77.54% ± 1.18 pp |
| strongest baseline | 71.62%, 74.00%, 73.38% | 73.00% ± 1.23 pp |
| **h adds vs strongest** | +5.00 pp, +3.12 pp, +5.50 pp | **+4.54 ± 1.25 pp** |

**Headline number for the paper:** `+4.5 ± 1.3 pp` (TriviaQA, n=800 per sample, 3 reshuffles).

For context: the average per-fold std at the probe peak is 3.54 pp. The seed-to-seed std of the h-adds margin (1.25 pp) is smaller than the per-fold noise -- so the sample variance and the fit variance are on the same order.
