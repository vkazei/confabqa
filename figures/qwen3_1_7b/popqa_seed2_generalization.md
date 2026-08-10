# PopQA generalization check (qwen3_1_7b)

Phase 2 deliverable. Sample: 800 PopQA test items, stratified into
5 quintile bins by `o_pop` (object Wikipedia pageviews; 160 per bin).
Pipeline: identical to the v1 paper (greedy decoding, `enable_thinking=False`, last-prompt-token hidden-state pickoff at
every layer, `StandardScaler -> PCA(16) -> LogReg` probe with 5-fold
CV, same prompt-feature baselines).

## Sample composition

- n total: 800
- judge labels: {'wrong': 651, 'correct': 137, 'refusal': 12}
- median `o_pop`: 16360
- per-bin correctness:

| bin | n | correct | accuracy |
|--:|--:|--:|--:|
| 0 | 160 | 3 | 1.9% |
| 1 | 160 | 7 | 4.4% |
| 2 | 160 | 17 | 10.6% |
| 3 | 160 | 28 | 17.5% |
| 4 | 160 | 82 | 51.2% |

Judge spot-check: see `popqa_seed2_judge_spotcheck.md`. **Caveat:** the judge has been calibrated on the v1.0/v1.3 question
set (Cohen $\kappa = 0.892$ / Claude $\kappa = 1.0$), NOT on the
PopQA distribution. Judge errors on PopQA -- especially around city-vs-
country gold mismatches and alias coverage -- are unmeasured and may
inflate or deflate the correctness count by a few pp.

## (a) The null test on external data

Hidden-state correctness probe vs. the strongest prompt-feature
baseline (max of TF-IDF, engineered text-only, +domain, +category):

| split | n | probe peak (layer) | strongest baseline | h adds (pp) | within per-fold std? |
|---|--:|--:|--:|--:|--:|
| full | 800 | 89.00% (L13) | 88.25% (`text_plus_domain`) | +0.75 | yes |
| low_o_pop | 400 | 97.25% (L27) | 97.00% (`text_plus_domain`) | +0.25 | yes |
| high_o_pop | 400 | 81.50% (L3) | 81.50% (`tfidf`) | -0.00 | yes |

**Full baseline table (PopQA full sample, correctness target):**

| metric | value |
|---|--:|
| majority baseline | 82.88% |
| TF-IDF baseline | 87.62% |
| engineered text-only | 83.25% |
| +domain | 88.25% |
| +domain+category | 88.25% |
| **hidden-state probe peak** | **89.00%** (L13, $\pm$ 1.96 pp) |
| h adds vs strongest | **+0.75 pp** |

## (b) Popularity question

Does the hidden state add MORE in the low-popularity half (where the
prompt is less informative)?

- low-popularity half (`o_pop` < 16360): h adds = +0.25 pp
- high-popularity half (`o_pop` >= 16360): h adds = -0.00 pp
- low minus high: +0.25 pp

## (c) Refusal probe

Refusal count on PopQA = **12** (< 30).

Per the protocol caveat: PopQA items are mostly answerable static
facts, so refusals are expected to be rare. The refusal-vs-wrong
probe is declared **UNDERPOWERED on PopQA and skipped**, rather
than reporting a noisy number from a tiny positive class.

## What transferred / what could not be tested here

- **Cutoff disconfound: N/A.** PopQA is built from static Wikidata
  triples with no cutoff structure; the within-pre/within-obscure
  disconfound tests from the main paper cannot be re-run on this
  data. The full PopQA sample is the closest analogue to the v1
  paper's all-items `correct` target.
- **Surface-form concern: PARTIAL.** PopQA is itself templated
  from Wikidata triples (e.g. "What is X's occupation?"), so it
  does not fully escape the construction-artifact problem flagged
  in Phase 1. Its value is (i) independent construction, (ii) a
  continuous popularity variable (Wikipedia pageviews), and (iii)
  a different distribution from the v1 question set -- not
  template-freeness.
- **Refusal probe: NOT TESTED.** PopQA items are mostly
  answerable, refusals are rare; the refusal-vs-wrong probe is
  underpowered on this data. The v1 paper's refusal positive
  result is neither corroborated nor challenged here.
- **Judge calibration on PopQA: UNVALIDATED.** The same-model
  judge has been calibrated on v1.0/v1.3 but not on PopQA. Spot-
  check pack provided for visual inspection only.
