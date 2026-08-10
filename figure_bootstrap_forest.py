"""Forest plot of bootstrap 95% CIs on h_adds across the 13 cells.

Reads:
  figures/bootstrap_h_adds.json     (11 v1.3 + Qwen-external cells)
  figures/bootstrap_llama_external.json  (2 Llama-external cells)

Writes:
  figures/bootstrap_forest.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
    main_path = Path("figures/bootstrap_h_adds.json")
    llama_path = Path("figures/bootstrap_llama_external.json")
    qwen4b_path = Path("figures/bootstrap_qwen3_4b.json")
    results = json.load(open(main_path))
    results.update(json.load(open(llama_path)))
    results.update(json.load(open(qwen4b_path)))

    order = [
        "v13_qwen3_1_7b_correct",
        "v13_qwen3_1_7b_correct_within_pre",
        "v13_qwen3_1_7b_correct_within_obscure",
        "v13_gemma_2_2b_correct",
        "v13_gemma_2_2b_correct_within_pre",
        "v13_gemma_2_2b_correct_within_obscure",
        "v13_llama_3_2_3b_correct",
        "v13_llama_3_2_3b_correct_within_pre",
        "v13_llama_3_2_3b_correct_within_obscure",
        "popqa_qwen3_1_7b_full",
        "popqa_qwen3_4b_full",
        "triviaqa_qwen3_1_7b_full",
        "popqa_llama_3_2_3b_full",
        "triviaqa_llama_3_2_3b_full",
    ]

    pretty = {
        "v13_qwen3_1_7b_correct": "ConfabQA  ·  Qwen3-1.7B  ·  correct (all)",
        "v13_qwen3_1_7b_correct_within_pre": "ConfabQA  ·  Qwen3-1.7B  ·  within-pre",
        "v13_qwen3_1_7b_correct_within_obscure": "ConfabQA  ·  Qwen3-1.7B  ·  within-obscure",
        "v13_gemma_2_2b_correct": "ConfabQA  ·  Gemma 2 2B  ·  correct (all)",
        "v13_gemma_2_2b_correct_within_pre": "ConfabQA  ·  Gemma 2 2B  ·  within-pre",
        "v13_gemma_2_2b_correct_within_obscure": "ConfabQA  ·  Gemma 2 2B  ·  within-obscure",
        "v13_llama_3_2_3b_correct": "ConfabQA  ·  Llama-3.2-3B  ·  correct (all)",
        "v13_llama_3_2_3b_correct_within_pre": "ConfabQA  ·  Llama-3.2-3B  ·  within-pre",
        "v13_llama_3_2_3b_correct_within_obscure": "ConfabQA  ·  Llama-3.2-3B  ·  within-obscure",
        "popqa_qwen3_1_7b_full": "PopQA  ·  Qwen3-1.7B  ·  correct (full)",
        "popqa_qwen3_4b_full": "PopQA  ·  Qwen3-4B  ·  correct (full)  [scaling control]",
        "triviaqa_qwen3_1_7b_full": "TriviaQA  ·  Qwen3-1.7B  ·  correct (full)",
        "popqa_llama_3_2_3b_full": "PopQA  ·  Llama-3.2-3B  ·  correct (full)",
        "triviaqa_llama_3_2_3b_full": "TriviaQA  ·  Llama-3.2-3B  ·  correct (full)",
    }

    means = [results[k]["mean"] for k in order]
    lows = [results[k]["ci_95_low"] for k in order]
    highs = [results[k]["ci_95_high"] for k in order]
    excl_zero = [results[k]["ci_excludes_zero"] for k in order]
    n_per_class = [results[k]["n_per_class"] for k in order]

    ys = np.arange(len(order))[::-1]

    fig, ax = plt.subplots(figsize=(10.5, 7.5), dpi=140)

    for i, (y, m, lo, hi, ex, n) in enumerate(zip(ys, means, lows, highs, excl_zero, n_per_class)):
        color = "#1f77b4" if ex else "#999999"
        ax.errorbar(m, y, xerr=[[m - lo], [hi - m]], fmt="o", color=color,
                    markersize=7, capsize=4, lw=1.6, markeredgecolor="black",
                    markeredgewidth=0.6)
        label_x = hi + 0.7
        ax.text(label_x, y, f"  {m:+.2f}  [{lo:+.1f}, {hi:+.1f}]   n/class={n}",
                fontsize=8.5, va="center",
                color="#000000" if ex else "#666666",
                fontweight="bold" if (ex and abs(m) > 15) else "normal")

    ax.axvline(0, color="#444444", lw=0.8, linestyle="--", alpha=0.7)
    ax.axvspan(0, 30, color="#1f77b4", alpha=0.04)

    ax.set_yticks(ys)
    ax.set_yticklabels([pretty[k] for k in order], fontsize=9)
    ax.set_xlabel(r"$h_{adds}$ (pp): probe peak accuracy $-$ strongest prompt-feature baseline",
                  fontsize=10)
    ax.set_xlim(-7, 36)
    ax.set_ylim(-0.6, len(order) - 0.4)

    ax.set_title("Bootstrap 95% CIs on $h_{adds}$ across 14 (dataset × model × target) cells\n"
                 r"K=30 balanced 50/50 subsamples per cell; blue = CI excludes 0",
                 fontsize=11, pad=12)

    sep_ys = [ys[2] - 0.5, ys[5] - 0.5, ys[8] - 0.5, ys[11] - 0.5]
    for sy in sep_ys:
        ax.axhline(sy, color="#bbbbbb", lw=0.5, alpha=0.6)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis="x", color="#eeeeee", lw=0.6)
    ax.set_axisbelow(True)

    plt.tight_layout()
    out = Path("figures/bootstrap_forest.png")
    plt.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
