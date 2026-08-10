# Cross-dataset transfer of the correctness probe (llama_3_2_3b)

Train a llama_3_2_3b correctness probe on dataset A, apply (without refit) to dataset B.
Target = `judge_label == "correct"`. Pipeline: StandardScaler -> PCA(16) -> LR(C=1.0).

## Dataset sizes

| dataset | n | correct | %correct | majority baseline |
|---|--:|--:|--:|--:|
| ConfabQA-784 | 784 | 240 | 30.6% | 69.39% |
| PopQA | 800 | 102 | 12.8% | 87.25% |
| TriviaQA | 800 | 369 | 46.1% | 53.87% |

## Probe transfer matrix

Rows: train dataset. Columns: test dataset. Values: accuracy %.
Diagonal: within-dataset 5-fold CV (probe trained and evaluated on the same set).
Off-diagonal: train on row, test on column, no refit.

### Layer 7

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 89.54 | 22.88 | 54.25 |
| PopQA | 70.66 | 89.00 | 57.38 |
| TriviaQA | 77.55 | 22.75 | 66.62 |

### Layer 14

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 93.49 | 79.75 | 76.12 |
| PopQA | 94.01 | 92.88 | 78.62 |
| TriviaQA | 93.75 | 90.12 | 80.88 |

### Layer 21

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 93.24 | 83.38 | 72.25 |
| PopQA | 91.20 | 92.25 | 78.88 |
| TriviaQA | 93.75 | 90.00 | 81.12 |

### Layer 28

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 93.37 | 76.00 | 76.75 |
| PopQA | 92.35 | 92.00 | 74.12 |
| TriviaQA | 94.26 | 90.50 | 81.00 |

## Prompt-feature baseline transfer (TF-IDF on question text)

Control: same train/test split but the classifier sees only question text, no hidden state.

| train \ test | ConfabQA-784 | PopQA | TriviaQA |
|---|--:|--:|--:|
| ConfabQA-784 | 84.06 | 30.50 | 57.75 |
| PopQA | 69.39 | 87.25 | 53.87 |
| TriviaQA | 74.11 | 33.75 | 58.13 |

## Reading the matrix

- **Diagonal > off-diagonal**: probe overfits to dataset-specific features (signal is dataset-specific).
- **Diagonal ≈ off-diagonal**: probe captures a dataset-agnostic correctness signal.
- **Off-diagonal ≈ majority baseline**: transfer fails entirely; the probe's within-dataset accuracy was item-specific noise.
- **Off-diagonal > prompt-feature transfer**: hidden-state probe extracts something beyond question-text patterns even cross-dataset.
