# Cross-dataset transfer of the correctness probe (Qwen3-1.7B)

Train a Qwen3-1.7B correctness probe on dataset A, apply (without refit) to dataset B.
Target = `judge_label == "correct"`. Pipeline: StandardScaler -> PCA(16) -> LR(C=1.0).

## Dataset sizes

| dataset | n | correct | %correct | majority baseline |
|---|--:|--:|--:|--:|
| ConfabQA-784 | 784 | 235 | 30.0% | 70.03% |
| PopQA | 2264 | 355 | 15.7% | 84.32% |
| TriviaQA | 2242 | 843 | 37.6% | 62.40% |

## Probe transfer matrix

Rows: train dataset. Columns: test dataset. Values: accuracy %.
Diagonal: within-dataset 5-fold CV (probe trained and evaluated on the same set).
Off-diagonal: train on row, test on column, no refit.

### Layer 14

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 81.00 | 70.58 | 56.51 |
| PopQA | 70.66 | 87.28 | 62.27 |
| TriviaQA | 77.30 | 82.51 | 69.80 |

### Layer 18

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 82.40 | 75.80 | 55.62 |
| PopQA | 74.23 | 87.77 | 56.78 |
| TriviaQA | 77.68 | 86.04 | 72.66 |

### Layer 22

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 81.76 | 75.49 | 51.20 |
| PopQA | 76.15 | 87.10 | 55.08 |
| TriviaQA | 78.95 | 85.91 | 71.63 |

### Layer 28

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 80.10 | 74.65 | 54.28 |
| PopQA | 75.64 | 87.19 | 63.83 |
| TriviaQA | 76.79 | 84.67 | 70.25 |

## Prompt-feature baseline transfer (TF-IDF on question text)

Control: same train/test split but the classifier sees only question text, no hidden state.

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 76.66 | 58.48 | 55.31 |
| PopQA | 70.03 | 85.11 | 62.40 |
| TriviaQA | 70.03 | 75.71 | 65.66 |

## Reading the matrix

- **Diagonal > off-diagonal**: probe overfits to dataset-specific features (signal is dataset-specific).
- **Diagonal ≈ off-diagonal**: probe captures a dataset-agnostic correctness signal.
- **Off-diagonal ≈ majority baseline**: transfer fails entirely; the probe's within-dataset accuracy was item-specific noise.
- **Off-diagonal > prompt-feature transfer**: hidden-state probe extracts something beyond question-text patterns even cross-dataset.
