# Cross-Model Comparison Summary

| Metric / Probe | Qwen3-1.7B | Gemma 2 2B | Llama 3.2 3B |
|:---| ---: | ---: | ---: |
| **Dataset Size (n)** | 784 | 784 | 784 |
| **Overall Accuracy** | 30.0% | 31.9% | 30.6% |
| **Pre-cutoff Accuracy** | 47.3% | 69.6% | 80.7% |
| **Post-cutoff Accuracy** | 19.5% | 9.0% | 0.2% |
| **Refusal Rate on Post-cutoff Failures** | 37.4% (147/393) | 55.2% (245/444) | 97.5% (475/487) |
|   |   |   |   |
| *PROBE ACCURACIES (PEAK % [PEAK LAYER] vs BASELINE)* |   |   |   |
| **Correctness (all items)** | **82.4%** [L18]<br>(base 70.0%, +12.4 pp) | **89.7%** [L14]<br>(base 68.1%, +21.6 pp) | **94.3%** [L13]<br>(base 69.4%, +24.9 pp) |
| **Cutoff (all items)** | **98.2%** [L13]<br>(base 62.2%, +36.0 pp) | **98.9%** [L14]<br>(base 62.2%, +36.6 pp) | **99.4%** [L25]<br>(base 62.2%, +37.1 pp) |
| **Refusal-vs-Wrong (subset)** | **89.4%** [L28]<br>(base 73.2%, +16.2 pp) | **83.9%** [L19]<br>(base 53.6%, +30.3 pp) | **95.8%** [L28]<br>(base 91.9%, +3.9 pp) |
| **Correct within Pre-cutoff** | **84.8%** [L18]<br>(base 52.7%, +32.1 pp) | **91.2%** [L17]<br>(base 69.6%, +21.6 pp) | **85.2%** [L13]<br>(base 80.7%, +4.4 pp) |
| **Correct within Obscure** | **80.5%** [L7]<br>(base 66.7%, +13.8 pp) | **88.9%** [L24]<br>(base 64.1%, +24.9 pp) | **81.1%** [L13]<br>(base 75.2%, +5.9 pp) |
|   |   |   |   |
| *PROMPT FEATURE BASELINE COMPARISONS* |   |   |   |
| **Correctness vs +category** | Probe **82.4%** vs Base **80.0%**<br>(+2.4 pp) | Probe **89.7%** vs Base **88.0%**<br>(+1.7 pp) | Probe **94.3%** vs Base **91.8%**<br>(+2.4 pp) |
| **Refusal-vs-Wrong vs TF-IDF** | Probe **89.4%** vs Base **82.0%**<br>(+7.5 pp) | Probe **83.9%** vs Base **67.6%**<br>(+16.3 pp) | Probe **95.8%** vs Base **93.6%**<br>(+2.2 pp) |
| **Within-Pre Correct vs +category** | Probe **84.8%** vs Base **81.8%**<br>(+3.0 pp) | Probe **91.2%** vs Base **86.1%**<br>(+5.1 pp) | Probe **85.2%** vs Base **79.4%**<br>(+5.8 pp) |