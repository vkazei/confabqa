# Bootstrap ranges (min to max over K=30 subsamples) on h_adds — Llama-3.2-3B on external datasets

Method: K=30 balanced 50/50 subsamples per cell. Same pipeline as `bootstrap_h_adds.md`. Range = min to max of the K values (not a 95% CI).

| cell | n/class | mean h_adds | median | std | range | excludes 0? |
|---|--:|--:|--:|--:|---|:--:|
| `popqa_llama_3_2_3b_full` | 131 | **+24.94 pp** | +24.81 | 2.37 | [+20.57, +29.03] | **yes** |
| `triviaqa_llama_3_2_3b_full` | 356 | **+21.25 pp** | +21.28 | 0.89 | [+19.52, +22.89] | **yes** |
