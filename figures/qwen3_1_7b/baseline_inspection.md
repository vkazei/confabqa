# Baseline inspection: what the prompt-feature classifiers key on
Phase 1 descriptive analysis. The four baselines below are refit on
the same cached `data/responses/qwen3_1_7b/` items as the paper,
using the same Pipeline definitions taken verbatim from
`03_analyze.py`. 5-fold CV accuracy column matches the paper's
`data/qwen3_1_7b_summary.json` numbers. Coefficients are extracted
from a single refit on the full subset (no held-out fold).

**Heuristic tag legend:**
- `YEAR/DATE` — 4-digit year token (e.g. `1978`, `in 2024`).
- `TEMPLATE-STRUCTURAL` — phrasing baked into the question template
  (e.g. `former`, `deputy`, `runner-up`, `first`, `latest`, month
  names, `won`, `released`, `directed`, `who`).
- `ENTITY-NAME` — capitalized word(s) that aren't in the structural
  vocabulary (proper nouns).
- `CONTENT-WORD` — lowercase content word not in stopwords/template
  vocabulary (e.g. `protein`, `album`).
- `TOKENIZER-ARTIFACT` — punctuation, single letters, or pure
  symbols.

Tag classification is heuristic and the raw token list is shown so
the reader can re-judge any borderline call.

---

## Target: `correct`

n=784 (235 positive); TF-IDF vocabulary size=1800; TF-IDF 5-fold CV acc = 0.7666

**Tag distribution in top 30 positive tokens:** CONTENT-WORD=13, TEMPLATE-STRUCTURAL=10, TOKENIZER-ARTIFACT=5, YEAR/DATE=2

**Tag distribution in top 30 negative tokens:** TEMPLATE-STRUCTURAL=18, YEAR/DATE=5, CONTENT-WORD=5, TOKENIZER-ARTIFACT=2

### Top 30 positive (predict CORRECT)

| rank | token | coef | tag |
|--:|---|--:|---|
| 1 | `is` | +1.298 | TOKENIZER-ARTIFACT |
| 2 | `which` | +1.279 | TOKENIZER-ARTIFACT |
| 3 | `painted the` | +1.136 | TEMPLATE-STRUCTURAL |
| 4 | `was the` | +1.054 | TEMPLATE-STRUCTURAL |
| 5 | `who wrote` | +0.972 | TEMPLATE-STRUCTURAL |
| 6 | `wrote` | +0.972 | TEMPLATE-STRUCTURAL |
| 7 | `first` | +0.968 | TEMPLATE-STRUCTURAL |
| 8 | `is the` | +0.857 | TEMPLATE-STRUCTURAL |
| 9 | `company` | +0.844 | CONTENT-WORD |
| 10 | `2025 which` | +0.822 | YEAR/DATE |
| 11 | `of the` | +0.810 | TEMPLATE-STRUCTURAL |
| 12 | `which company` | +0.785 | CONTENT-WORD |
| 13 | `war` | +0.782 | CONTENT-WORD |
| 14 | `2019` | +0.766 | YEAR/DATE |
| 15 | `what year` | +0.741 | TEMPLATE-STRUCTURAL |
| 16 | `ai` | +0.700 | TOKENIZER-ARTIFACT |
| 17 | `the first` | +0.693 | TEMPLATE-STRUCTURAL |
| 18 | `the president` | +0.685 | TEMPLATE-STRUCTURAL |
| 19 | `by` | +0.658 | TOKENIZER-ARTIFACT |
| 20 | `what is` | +0.654 | TOKENIZER-ARTIFACT |
| 21 | `observed` | +0.645 | CONTENT-WORD |
| 22 | `ended` | +0.643 | CONTENT-WORD |
| 23 | `discovered` | +0.613 | CONTENT-WORD |
| 24 | `saw` | +0.594 | CONTENT-WORD |
| 25 | `known` | +0.572 | CONTENT-WORD |
| 26 | `service` | +0.557 | CONTENT-WORD |
| 27 | `anthropic` | +0.545 | CONTENT-WORD |
| 28 | `declared` | +0.530 | CONTENT-WORD |
| 29 | `independence` | +0.520 | CONTENT-WORD |
| 30 | `introduced` | +0.518 | CONTENT-WORD |

### Top 30 negative (predict WRONG)

| rank | token | coef | tag |
|--:|---|--:|---|
| 1 | `2024` | -2.050 | YEAR/DATE |
| 2 | `2025` | -1.755 | YEAR/DATE |
| 3 | `won the` | -1.572 | TEMPLATE-STRUCTURAL |
| 4 | `won` | -1.518 | TEMPLATE-STRUCTURAL |
| 5 | `who won` | -1.165 | TEMPLATE-STRUCTURAL |
| 6 | `prize` | -0.996 | TEMPLATE-STRUCTURAL |
| 7 | `award` | -0.953 | TEMPLATE-STRUCTURAL |
| 8 | `award for` | -0.861 | TEMPLATE-STRUCTURAL |
| 9 | `prize in` | -0.828 | TEMPLATE-STRUCTURAL |
| 10 | `the 2025` | -0.822 | YEAR/DATE |
| 11 | `at` | -0.801 | TOKENIZER-ARTIFACT |
| 12 | `the 2024` | -0.782 | YEAR/DATE |
| 13 | `for best` | -0.750 | CONTENT-WORD |
| 14 | `november 2024` | -0.727 | YEAR/DATE |
| 15 | `nobel` | -0.711 | CONTENT-WORD |
| 16 | `artist` | -0.700 | CONTENT-WORD |
| 17 | `best` | -0.673 | CONTENT-WORD |
| 18 | `nobel prize` | -0.668 | TEMPLATE-STRUCTURAL |
| 19 | `november` | -0.659 | TEMPLATE-STRUCTURAL |
| 20 | `the nobel` | -0.656 | TEMPLATE-STRUCTURAL |
| 21 | `at the` | -0.653 | TEMPLATE-STRUCTURAL |
| 22 | `for` | -0.650 | TOKENIZER-ARTIFACT |
| 23 | `starred` | -0.631 | TEMPLATE-STRUCTURAL |
| 24 | `secretary` | -0.628 | CONTENT-WORD |
| 25 | `february` | -0.621 | TEMPLATE-STRUCTURAL |
| 26 | `elected` | -0.606 | TEMPLATE-STRUCTURAL |
| 27 | `month` | -0.600 | TEMPLATE-STRUCTURAL |
| 28 | `who starred` | -0.599 | TEMPLATE-STRUCTURAL |
| 29 | `september` | -0.597 | TEMPLATE-STRUCTURAL |
| 30 | `novel the` | -0.592 | TEMPLATE-STRUCTURAL |

### Engineered baselines (standardized coefficient magnitudes)

**`text_only` baseline** (n=784; CV acc = 0.7730)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +0.9405 | 0.9405 |
| `has_year` | -0.9005 | 0.9005 |
| `q_word_len` | -0.7271 | 0.7271 |
| `year_value` | -0.5361 | 0.5361 |
| `n_capwords` | -0.4508 | 0.4508 |
| `n_commas` | +0.4432 | 0.4432 |
| `n_digits` | +0.0774 | 0.0774 |
| `ends_questionmark` | +0.0000 | 0.0000 |

**`text_plus_domain` baseline** (n=784; CV acc = 0.7793)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +0.9468 | 0.9468 |
| `has_year` | -0.8822 | 0.8822 |
| `q_word_len` | -0.7400 | 0.7400 |
| `year_value` | -0.5174 | 0.5174 |
| `n_capwords` | -0.4362 | 0.4362 |
| `n_commas` | +0.4116 | 0.4116 |
| `domain=cinema` | -0.1533 | 0.1533 |
| `domain=culture` | +0.0972 | 0.0972 |
| `n_digits` | +0.0767 | 0.0767 |
| `domain=history` | +0.0447 | 0.0447 |
| `domain=science` | +0.0112 | 0.0112 |
| `ends_questionmark` | +0.0000 | 0.0000 |

**`text_plus_domain_plus_cat` baseline** (n=784; CV acc = 0.7997)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +1.3554 | 1.3554 |
| `q_word_len` | -0.9907 | 0.9907 |
| `has_year` | -0.6979 | 0.6979 |
| `category=well_known` | +0.5067 | 0.5067 |
| `n_commas` | +0.4768 | 0.4768 |
| `category=post_cutoff` | -0.4129 | 0.4129 |
| `n_capwords` | -0.4024 | 0.4024 |
| `domain=cinema` | -0.2047 | 0.2047 |
| `year_value` | -0.2004 | 0.2004 |
| `n_digits` | +0.1369 | 0.1369 |
| `domain=culture` | +0.1159 | 0.1159 |
| `domain=history` | +0.1076 | 0.1076 |
| `domain=science` | -0.0186 | 0.0186 |
| `category=obscure` | +0.0114 | 0.0114 |
| `ends_questionmark` | +0.0000 | 0.0000 |

---

## Target: `correct_within_pre`

n=296 (140 positive); TF-IDF vocabulary size=417; TF-IDF 5-fold CV acc = 0.7971

**Tag distribution in top 30 positive tokens:** TEMPLATE-STRUCTURAL=12, CONTENT-WORD=12, TOKENIZER-ARTIFACT=5, YEAR/DATE=1

**Tag distribution in top 30 negative tokens:** TEMPLATE-STRUCTURAL=15, CONTENT-WORD=9, YEAR/DATE=5, TOKENIZER-ARTIFACT=1

### Top 30 positive (predict CORRECT)

| rank | token | coef | tag |
|--:|---|--:|---|
| 1 | `painted the` | +0.915 | TEMPLATE-STRUCTURAL |
| 2 | `which` | +0.834 | TOKENIZER-ARTIFACT |
| 3 | `and` | +0.781 | TOKENIZER-ARTIFACT |
| 4 | `of the` | +0.656 | TEMPLATE-STRUCTURAL |
| 5 | `2019` | +0.614 | YEAR/DATE |
| 6 | `war` | +0.614 | CONTENT-WORD |
| 7 | `is` | +0.599 | TOKENIZER-ARTIFACT |
| 8 | `was` | +0.497 | TOKENIZER-ARTIFACT |
| 9 | `observed` | +0.458 | CONTENT-WORD |
| 10 | `china` | +0.450 | CONTENT-WORD |
| 11 | `is the` | +0.448 | TEMPLATE-STRUCTURAL |
| 12 | `wrote` | +0.441 | TEMPLATE-STRUCTURAL |
| 13 | `who wrote` | +0.441 | TEMPLATE-STRUCTURAL |
| 14 | `years` | +0.438 | CONTENT-WORD |
| 15 | `ended` | +0.437 | CONTENT-WORD |
| 16 | `president` | +0.427 | CONTENT-WORD |
| 17 | `released` | +0.425 | TEMPLATE-STRUCTURAL |
| 18 | `what` | +0.419 | TOKENIZER-ARTIFACT |
| 19 | `discovered` | +0.416 | CONTENT-WORD |
| 20 | `the first` | +0.407 | TEMPLATE-STRUCTURAL |
| 21 | `known` | +0.387 | CONTENT-WORD |
| 22 | `saw` | +0.386 | CONTENT-WORD |
| 23 | `the president` | +0.384 | TEMPLATE-STRUCTURAL |
| 24 | `one` | +0.381 | CONTENT-WORD |
| 25 | `new` | +0.380 | CONTENT-WORD |
| 26 | `in the` | +0.371 | TEMPLATE-STRUCTURAL |
| 27 | `president of` | +0.369 | CONTENT-WORD |
| 28 | `first` | +0.360 | TEMPLATE-STRUCTURAL |
| 29 | `was the` | +0.357 | TEMPLATE-STRUCTURAL |
| 30 | `released in` | +0.354 | TEMPLATE-STRUCTURAL |

### Top 30 negative (predict WRONG)

| rank | token | coef | tag |
|--:|---|--:|---|
| 1 | `won the` | -1.430 | TEMPLATE-STRUCTURAL |
| 2 | `won` | -1.430 | TEMPLATE-STRUCTURAL |
| 3 | `who won` | -1.291 | TEMPLATE-STRUCTURAL |
| 4 | `prize` | -1.082 | TEMPLATE-STRUCTURAL |
| 5 | `the nobel` | -1.044 | TEMPLATE-STRUCTURAL |
| 6 | `prize in` | -1.014 | TEMPLATE-STRUCTURAL |
| 7 | `nobel` | -0.969 | CONTENT-WORD |
| 8 | `nobel prize` | -0.969 | TEMPLATE-STRUCTURAL |
| 9 | `award` | -0.877 | TEMPLATE-STRUCTURAL |
| 10 | `academy award` | -0.788 | TEMPLATE-STRUCTURAL |
| 11 | `award for` | -0.788 | TEMPLATE-STRUCTURAL |
| 12 | `the academy` | -0.788 | TEMPLATE-STRUCTURAL |
| 13 | `for best` | -0.788 | CONTENT-WORD |
| 14 | `academy` | -0.788 | CONTENT-WORD |
| 15 | `for` | -0.780 | TOKENIZER-ARTIFACT |
| 16 | `ceremony` | -0.764 | TEMPLATE-STRUCTURAL |
| 17 | `1987` | -0.751 | YEAR/DATE |
| 18 | `best` | -0.707 | CONTENT-WORD |
| 19 | `novel the` | -0.673 | TEMPLATE-STRUCTURAL |
| 20 | `reach` | -0.605 | CONTENT-WORD |
| 21 | `reach the` | -0.605 | TEMPLATE-STRUCTURAL |
| 22 | `1979` | -0.580 | YEAR/DATE |
| 23 | `1982` | -0.560 | YEAR/DATE |
| 24 | `novel` | -0.519 | TEMPLATE-STRUCTURAL |
| 25 | `chemistry in` | -0.505 | CONTENT-WORD |
| 26 | `in chemistry` | -0.505 | CONTENT-WORD |
| 27 | `1913` | -0.503 | YEAR/DATE |
| 28 | `space in` | -0.499 | CONTENT-WORD |
| 29 | `1983` | -0.488 | YEAR/DATE |
| 30 | `physics in` | -0.481 | CONTENT-WORD |

### Engineered baselines (standardized coefficient magnitudes)

**`text_only` baseline** (n=296; CV acc = 0.8110)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +1.4180 | 1.4180 |
| `has_year` | -1.4083 | 1.4083 |
| `n_capwords` | -0.8941 | 0.8941 |
| `q_word_len` | -0.8256 | 0.8256 |
| `n_commas` | +0.3654 | 0.3654 |
| `year_value` | -0.2984 | 0.2984 |
| `n_digits` | +0.1661 | 0.1661 |
| `ends_questionmark` | +0.0000 | 0.0000 |

**`text_plus_domain` baseline** (n=296; CV acc = 0.8108)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +1.3697 | 1.3697 |
| `has_year` | -0.9443 | 0.9443 |
| `n_capwords` | -0.8854 | 0.8854 |
| `q_word_len` | -0.8780 | 0.8780 |
| `domain=history` | +0.4478 | 0.4478 |
| `domain=science` | -0.3791 | 0.3791 |
| `n_commas` | +0.3219 | 0.3219 |
| `year_value` | -0.1382 | 0.1382 |
| `domain=cinema` | -0.1357 | 0.1357 |
| `n_digits` | -0.1206 | 0.1206 |
| `domain=culture` | +0.0960 | 0.0960 |
| `ends_questionmark` | +0.0000 | 0.0000 |

**`text_plus_domain_plus_cat` baseline** (n=296; CV acc = 0.8177)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +1.7405 | 1.7405 |
| `q_word_len` | -1.0915 | 1.0915 |
| `has_year` | -0.9895 | 0.9895 |
| `n_capwords` | -0.8796 | 0.8796 |
| `domain=history` | +0.5010 | 0.5010 |
| `category=obscure` | -0.4429 | 0.4429 |
| `category=well_known` | +0.4429 | 0.4429 |
| `domain=science` | -0.4343 | 0.4343 |
| `n_commas` | +0.3258 | 0.3258 |
| `year_value` | -0.3156 | 0.3156 |
| `domain=cinema` | -0.1646 | 0.1646 |
| `domain=culture` | +0.1314 | 0.1314 |
| `n_digits` | +0.0634 | 0.0634 |
| `ends_questionmark` | +0.0000 | 0.0000 |

---

## Target: `correct_within_obscure`

n=153 (51 positive); TF-IDF vocabulary size=243; TF-IDF 5-fold CV acc = 0.7523

**Tag distribution in top 30 positive tokens:** CONTENT-WORD=10, TOKENIZER-ARTIFACT=9, TEMPLATE-STRUCTURAL=7, YEAR/DATE=4

**Tag distribution in top 30 negative tokens:** TEMPLATE-STRUCTURAL=17, CONTENT-WORD=9, TOKENIZER-ARTIFACT=3, YEAR/DATE=1

### Top 30 positive (predict CORRECT)

| rank | token | coef | tag |
|--:|---|--:|---|
| 1 | `which` | +0.829 | TOKENIZER-ARTIFACT |
| 2 | `and` | +0.817 | TOKENIZER-ARTIFACT |
| 3 | `the first` | +0.638 | TEMPLATE-STRUCTURAL |
| 4 | `first` | +0.578 | TEMPLATE-STRUCTURAL |
| 5 | `to` | +0.534 | TOKENIZER-ARTIFACT |
| 6 | `year` | +0.528 | TEMPLATE-STRUCTURAL |
| 7 | `what` | +0.510 | TOKENIZER-ARTIFACT |
| 8 | `by` | +0.494 | TOKENIZER-ARTIFACT |
| 9 | `1953` | +0.478 | YEAR/DATE |
| 10 | `1917` | +0.458 | YEAR/DATE |
| 11 | `1955` | +0.430 | YEAR/DATE |
| 12 | `jazz` | +0.425 | CONTENT-WORD |
| 13 | `revolution` | +0.416 | CONTENT-WORD |
| 14 | `in` | +0.411 | TOKENIZER-ARTIFACT |
| 15 | `china` | +0.408 | CONTENT-WORD |
| 16 | `discovered` | +0.403 | CONTENT-WORD |
| 17 | `is the` | +0.396 | TEMPLATE-STRUCTURAL |
| 18 | `woman to` | +0.393 | CONTENT-WORD |
| 19 | `as` | +0.385 | TOKENIZER-ARTIFACT |
| 20 | `with` | +0.384 | TOKENIZER-ARTIFACT |
| 21 | `of the` | +0.384 | TEMPLATE-STRUCTURAL |
| 22 | `over` | +0.376 | TOKENIZER-ARTIFACT |
| 23 | `war` | +0.375 | CONTENT-WORD |
| 24 | `1898` | +0.371 | YEAR/DATE |
| 25 | `african` | +0.354 | CONTENT-WORD |
| 26 | `year did` | +0.347 | TEMPLATE-STRUCTURAL |
| 27 | `did` | +0.347 | TEMPLATE-STRUCTURAL |
| 28 | `american` | +0.341 | CONTENT-WORD |
| 29 | `which jazz` | +0.332 | CONTENT-WORD |
| 30 | `observed` | +0.330 | CONTENT-WORD |

### Top 30 negative (predict WRONG)

| rank | token | coef | tag |
|--:|---|--:|---|
| 1 | `won the` | -0.927 | TEMPLATE-STRUCTURAL |
| 2 | `won` | -0.927 | TEMPLATE-STRUCTURAL |
| 3 | `who won` | -0.915 | TEMPLATE-STRUCTURAL |
| 4 | `the nobel` | -0.804 | TEMPLATE-STRUCTURAL |
| 5 | `prize in` | -0.717 | TEMPLATE-STRUCTURAL |
| 6 | `prize` | -0.717 | TEMPLATE-STRUCTURAL |
| 7 | `nobel prize` | -0.687 | TEMPLATE-STRUCTURAL |
| 8 | `nobel` | -0.687 | CONTENT-WORD |
| 9 | `who` | -0.615 | TOKENIZER-ARTIFACT |
| 10 | `award` | -0.605 | TEMPLATE-STRUCTURAL |
| 11 | `for` | -0.597 | TOKENIZER-ARTIFACT |
| 12 | `who directed` | -0.550 | TEMPLATE-STRUCTURAL |
| 13 | `directed the` | -0.550 | TEMPLATE-STRUCTURAL |
| 14 | `directed` | -0.550 | TEMPLATE-STRUCTURAL |
| 15 | `academy award` | -0.517 | TEMPLATE-STRUCTURAL |
| 16 | `ceremony` | -0.517 | TEMPLATE-STRUCTURAL |
| 17 | `academy` | -0.517 | CONTENT-WORD |
| 18 | `the academy` | -0.517 | TEMPLATE-STRUCTURAL |
| 19 | `best` | -0.517 | CONTENT-WORD |
| 20 | `award for` | -0.517 | TEMPLATE-STRUCTURAL |
| 21 | `for best` | -0.517 | CONTENT-WORD |
| 22 | `the film` | -0.485 | TEMPLATE-STRUCTURAL |
| 23 | `on` | -0.457 | TOKENIZER-ARTIFACT |
| 24 | `1982` | -0.440 | YEAR/DATE |
| 25 | `peace` | -0.430 | CONTENT-WORD |
| 26 | `novel the` | -0.416 | TEMPLATE-STRUCTURAL |
| 27 | `in physics` | -0.412 | CONTENT-WORD |
| 28 | `physics` | -0.412 | CONTENT-WORD |
| 29 | `physics in` | -0.412 | CONTENT-WORD |
| 30 | `chemistry` | -0.399 | CONTENT-WORD |

### Engineered baselines (standardized coefficient magnitudes)

**`text_only` baseline** (n=153; CV acc = 0.8303)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +1.6109 | 1.6109 |
| `has_year` | -1.1932 | 1.1932 |
| `q_word_len` | -0.6927 | 0.6927 |
| `n_capwords` | -0.6236 | 0.6236 |
| `year_value` | -0.5692 | 0.5692 |
| `n_digits` | +0.4315 | 0.4315 |
| `n_commas` | +0.1517 | 0.1517 |
| `ends_questionmark` | +0.0000 | 0.0000 |

**`text_plus_domain` baseline** (n=153; CV acc = 0.8110)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +1.7565 | 1.7565 |
| `has_year` | -0.7601 | 0.7601 |
| `q_word_len` | -0.7437 | 0.7437 |
| `n_capwords` | -0.6728 | 0.6728 |
| `domain=history` | +0.4710 | 0.4710 |
| `domain=cinema` | -0.4242 | 0.4242 |
| `year_value` | -0.3142 | 0.3142 |
| `domain=science` | -0.1476 | 0.1476 |
| `n_digits` | +0.1359 | 0.1359 |
| `domain=culture` | +0.1135 | 0.1135 |
| `n_commas` | +0.1063 | 0.1063 |
| `ends_questionmark` | +0.0000 | 0.0000 |

**`text_plus_domain_plus_cat` baseline** (n=153; CV acc = 0.8110)

| feature | coef (standardized) | |coef| |
|---|--:|--:|
| `q_char_len` | +1.7565 | 1.7565 |
| `has_year` | -0.7601 | 0.7601 |
| `q_word_len` | -0.7437 | 0.7437 |
| `n_capwords` | -0.6728 | 0.6728 |
| `domain=history` | +0.4710 | 0.4710 |
| `domain=cinema` | -0.4242 | 0.4242 |
| `year_value` | -0.3142 | 0.3142 |
| `domain=science` | -0.1476 | 0.1476 |
| `n_digits` | +0.1359 | 0.1359 |
| `domain=culture` | +0.1135 | 0.1135 |
| `n_commas` | +0.1063 | 0.1063 |
| `ends_questionmark` | +0.0000 | 0.0000 |
| `category=obscure` | +0.0000 | 0.0000 |

---

## Verdict: `correct_within_obscure`

**Tag distribution across top 60 tokens (pos + neg) for the obscure cell:**

| tag | count | share |
|---|--:|--:|
| TEMPLATE-STRUCTURAL | 24 | 40.0% |
| CONTENT-WORD | 19 | 31.7% |
| TOKENIZER-ARTIFACT | 12 | 20.0% |
| YEAR/DATE | 5 | 8.3% |

VERDICT: the TF-IDF baseline on `correct_within_obscure` is primarily riding CONSTRUCTION ARTIFACTS (year/date tokens, template-structural phrasing, tokenizer fragments). The current framing 'prompt encodes the answer' should be softened to 'prompt encodes ANSWERABILITY, partly via construction artifacts': the baseline wins not because the prompt text contains the answer, but because the question's surface form leaks how hard the question is to answer.
