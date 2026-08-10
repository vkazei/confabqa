# TriviaQA generalization check (qwen3_1_7b)

Phase 2 follow-up to the PopQA replication. Sample: 800 TriviaQA
`unfiltered.nocontext` validation items, uniform random with
`random.Random(0)`. TriviaQA was the primary closed-book QA dataset
Kadavath et al.\ (2022) leaned on for their P(IK) calibration probe,
so this is the most directly comparable head-to-head replication of
the null. Pipeline: identical to the v1 paper (greedy decoding,
`enable_thinking=False`, last-prompt-token hidden-state pickoff at
every layer, `StandardScaler -> PCA(16) -> LogReg` probe with 5-fold
CV, same prompt-feature baselines).

## Sample composition

- n total: 800
- judge labels: {'wrong': 485, 'correct': 304, 'refusal': 11}
- median answer word-length: 2
- per-answer-length correctness (top 6 most-common lengths):

| answer word-length | n | correct | accuracy |
|--:|--:|--:|--:|
| 1 | 364 | 139 | 38.2% |
| 2 | 285 | 71 | 24.9% |
| 3 | 85 | 13 | 15.3% |
| 4 | 26 | 5 | 19.2% |
| 5 | 12 | 1 | 8.3% |
| 6 | 9 | 0 | 0.0% |

Judge spot-check: see `triviaqa_rerun0_judge_spotcheck.md`. **Caveat:** the
judge has been calibrated on the v1.0/v1.3 question set (Cohen
$\kappa = 0.892$ on v1.0, Claude $\kappa = 1.0$ on v1.3), NOT on
the TriviaQA distribution. TriviaQA's aliases cover many but not
all surface forms; judge errors are unmeasured here and may shift
the correctness count by a few pp.

## (a) The null test on external data

Hidden-state correctness probe vs. the strongest prompt-feature
baseline (max of TF-IDF, engineered text-only, +domain, +category):

| split | n | probe peak (layer) | strongest baseline | h adds (pp) | within per-fold std? |
|---|--:|--:|--:|--:|--:|
| full | 800 | 76.75% (L21) | 71.62% (`text_only`) | +5.13 | NO |
| short_answer | 649 | 75.50% (L17) | 67.80% (`text_only`) | +7.70 | NO |
| long_answer | 151 | 86.75% (L0) | 86.75% (`tfidf`) | +0.00 | yes |

**Full baseline table (TriviaQA full sample, correctness target):**

| metric | value |
|---|--:|
| majority baseline | 71.25% |
| TF-IDF baseline | 70.50% |
| engineered text-only | 71.62% |
| +domain | 71.62% |
| +domain+category | 71.62% |
| **hidden-state probe peak** | **76.75%** (L21, $\pm$ 2.57 pp) |
| h adds vs strongest | **+5.13 pp** |

## (b) Answer-length split (TriviaQA's nearest analogue to PopQA's popularity axis)

TriviaQA has no continuous popularity axis. The nearest available
proxy is answer word-length: 1-word answers tend to be common
entities (e.g. `Hitler`, `Beethoven`); multi-word answers tend to
be more obscure (e.g. specific book titles, niche figures). Not as
clean as Wikipedia pageviews, but it's the only continuous-ish
axis the dataset provides without a Wikidata join.

- short-answer half (word-length $\le$ 2): h adds = +7.70 pp
- long-answer half (word-length $>$ 2): h adds = +0.00 pp
- short minus long: +7.70 pp

## (c) Refusal probe

Refusal count on TriviaQA = **11** (< 30).

Per the protocol caveat: TriviaQA items are mostly answerable static
facts, so refusals are expected to be rare. The refusal-vs-wrong
probe is declared **UNDERPOWERED on TriviaQA and skipped**, rather
than reporting a noisy number from a tiny positive class.

## What transferred / what could not be tested here

- **Cutoff disconfound: N/A.** TriviaQA is static trivia; the
  within-pre/within-obscure disconfound tests from the main paper
  cannot be re-run. The full TriviaQA sample is the closest
  analogue to the v1 paper's all-items `correct` target.
- **Surface-form concern: PARTIAL.** TriviaQA is human-written
  trivia, so the question-construction phrasing is less templated
  than PopQA's Wikidata-derived prompts, but the questions still
  have systematic phrasing patterns ("Who wrote X", "Who played
  Y", etc.) that a TF-IDF baseline can pick up. The point of
  running on TriviaQA specifically is that it's the dataset
  Kadavath et al.\ (2022) leaned on for their P(IK) probe -- so
  the head-to-head is on the original claim's home turf.
- **Refusal probe: NOT TESTED.** TriviaQA items are mostly
  answerable, refusals are rare; the refusal-vs-wrong probe is
  underpowered on this data. The v1 paper's refusal positive
  result is neither corroborated nor challenged here.
- **Judge calibration on TriviaQA: UNVALIDATED.** The same-model
  judge has been calibrated on v1.0/v1.3 but not on TriviaQA. Spot-
  check pack provided for visual inspection only.
