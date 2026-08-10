# Cross-dataset transfer of the correctness probe (gemma_2_2b)

Train a gemma_2_2b correctness probe on dataset A, apply (without refit) to dataset B.
Target = `judge_label == "correct"`. Pipeline: StandardScaler -> PCA(16) -> LR(C=1.0).

## Dataset sizes

| dataset | n | correct | %correct | majority baseline |
|---|--:|--:|--:|--:|
| ConfabQA-784 | 784 | 250 | 31.9% | 68.11% |
| PopQA | 800 | 158 | 19.8% | 80.25% |
| TriviaQA | 800 | 448 | 56.0% | 56.00% |

## Probe transfer matrix

Rows: train dataset. Columns: test dataset. Values: accuracy %.
Diagonal: within-dataset 5-fold CV (probe trained and evaluated on the same set).
Off-diagonal: train on row, test on column, no refit.

### Layer 6

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 85.59 | 19.62 | 57.88 |
| PopQA | 42.47 | 83.38 | 55.88 |
| TriviaQA | 58.80 | 20.38 | 63.62 |

### Layer 13

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 87.75 | 38.25 | 59.50 |
| PopQA | 75.64 | 85.50 | 65.75 |
| TriviaQA | 80.61 | 46.75 | 70.50 |

### Layer 20

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 88.65 | 29.62 | 56.38 |
| PopQA | 67.35 | 84.00 | 64.12 |
| TriviaQA | 80.10 | 68.62 | 69.00 |

### Layer 26

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 88.65 | 55.38 | 57.38 |
| PopQA | 73.60 | 84.50 | 62.62 |
| TriviaQA | 76.79 | 72.75 | 68.12 |

## Prompt-feature baseline transfer (TF-IDF on question text)

Control: same train/test split but the classifier sees only question text, no hidden state.

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 84.69 | 23.50 | 55.50 |
| PopQA | 68.11 | 80.62 | 44.25 |
| TriviaQA | 56.38 | 59.75 | 58.38 |

## Reading the matrix

- **Diagonal > off-diagonal**: probe overfits to dataset-specific features (signal is dataset-specific).
- **Diagonal ≈ off-diagonal**: probe captures a dataset-agnostic correctness signal.
- **Off-diagonal ≈ majority baseline**: transfer fails entirely; the probe's within-dataset accuracy was item-specific noise.
- **Off-diagonal > prompt-feature transfer**: hidden-state probe extracts something beyond question-text patterns even cross-dataset.
