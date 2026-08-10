# TriviaQA seed=0 vs seed=1 comparison
Same pipeline, same model (qwen3_1_7b), same hyperparameters; the only difference is `random.Random(seed)` for the 800-item sample from `mandarjoshi/trivia_qa unfiltered.nocontext` (validation split, n=11313 total). Overlap between samples is small (~7%).

## Sample composition

| metric | seed=0 | seed=1 |
|---|--:|--:|
| n | 800 | 800 |
| correct | 304 | 303 |
| refusal | 11 | 8 |
| wrong | 485 | 489 |

## Full-sample null test

| metric | seed=0 | seed=1 |
|---|--:|--:|
| majority baseline | 71.25% | 73.12% |
| TF-IDF | 70.50% | 74.00% |
| **TF-IDF − majority** | -0.75 pp | +0.88 pp |
| text-only | 71.62% | 73.12% |
| +domain | 71.62% | 73.12% |
| +category | 71.62% | 73.12% |
| strongest baseline (name) | `text_only` (71.62%) | `tfidf` (74.00%) |
| hidden-state probe peak | 76.63% (L21) | 77.12% (L17) |
| probe std at peak | 2.64 pp | 3.72 pp |
| **h adds vs strongest** | **+5.00 pp** | **+3.12 pp** |
| within per-fold std? | NO | yes |

## Read of the comparison

- TF-IDF below majority on one seed but not the other (-0.75 vs +0.88 pp). The seed=0
  result was at least partly sample-specific; the TF-IDF baseline
  hovers right around majority on TriviaQA but isn't reliably below it.
- Hidden-state margin over strongest baseline differs noticeably: +5.00 pp (seed=0) vs +3.12 pp (seed=1).
  Difference of +1.88 pp suggests the +5pp / 2σ result is
  partly sample-noise.
