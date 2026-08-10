# Refusal-channel test: is Llama's huge h_adds mostly a refusal-readout?

K=30 balanced 50/50 bootstrap subsamples per cell. Same probe + baseline pipeline as `bootstrap_h_adds.md`.

## Test A — drop refusals, probe correct vs wrong

If Llama's headline +25 pp was mostly refusal-readout, this collapses.
For reference, the unfiltered numbers are: Qwen-PopQA +4.35, Llama-PopQA **+24.94**, Qwen-TriviaQA +9.57, Llama-TriviaQA **+21.25**.

| cell | n/class | probe acc | baseline | h_adds | 95% CI |
|---|--:|--:|--:|--:|---|
| `popqa_qwen3_1_7b_drop_refusals` | 355 | 79.18% | 75.87% | **+3.31 pp** | [+1.55, +6.48] |
| `popqa_llama_3_2_3b_drop_refusals` | 102 | 82.37% | 61.61% | **+20.76 pp** | [+14.67, +27.94] |
| `triviaqa_qwen3_1_7b_drop_refusals` | 400 | 69.40% | 60.04% | **+9.36 pp** | [+6.50, +12.87] |
| `triviaqa_llama_3_2_3b_drop_refusals` | 179 | 74.23% | 56.52% | **+17.71 pp** | [+13.43, +21.78] |

## Test B — probe refusal directly

Target = judge_label == 'refusal'. Probe absolute accuracy is the interesting number here — if Llama's probe scores high and the baselines stay near 50% (majority of a 50/50 sample), refusal is the readable signal in the hidden state.

| cell | n/class | probe acc | baseline | h_adds | 95% CI |
|---|--:|--:|--:|--:|---|
| `popqa_qwen3_1_7b_refusal_vs_rest` | 39 | 86.27% | 76.04% | **+10.24 pp** | [+0.00, +20.42] |
| `popqa_llama_3_2_3b_refusal_vs_rest` | 297 | 84.47% | 66.03% | **+18.44 pp** | [+16.16, +21.72] |
| `triviaqa_qwen3_1_7b_refusal_vs_rest` | 28 | 73.34% | 57.37% | **+15.97 pp** | [-3.48, +32.27] |
| `triviaqa_llama_3_2_3b_refusal_vs_rest` | 252 | 90.23% | 64.80% | **+25.43 pp** | [+22.81, +29.76] |

## Interpretation cheat-sheet

- **Test A h_adds collapses for Llama** → headline is mostly refusal channel.
- **Test A h_adds holds for Llama** → genuine factual self-knowledge contributes.
- **Test B Llama probe ≫ Qwen probe** → Llama has a clean abstention representation Qwen lacks (or has in a non-linearly-decodable form).
- **Test B baselines near 50%** → refusal is not predictable from question text alone, so probe gain is a real readout of the model's internal state, not a question-difficulty leak.
