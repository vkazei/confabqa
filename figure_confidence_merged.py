"""Merged text-level confidence figure (replaces 01_logprob_histogram +
02_calibration_scatter with one two-panel figure, print-scaled).

Panel (a): histogram of mean per-token log-probability by judge correctness
           (same encoding as the original 01 figure).
Panel (b): mean log-probability vs. mean entropy; color = cutoff class,
           marker = correct/wrong (same encoding as the original 02 figure).

Reads the same cached responses 03_analyze.py uses; no frozen script touched.
Writes figures/qwen3_1_7b/confidence_merged.png.
"""
import json

import matplotlib.pyplot as plt
import numpy as np

from config import FIGURES_DIR, RESPONSES_DIR


def load():
    return [json.load(open(f)) for f in sorted(RESPONSES_DIR.glob("*.json"))]


def main():
    resp = load()

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.3), dpi=200)

    # ---- (a) histogram by correctness ----
    ax = axes[0]
    correct = [r["mean_logprob"] for r in resp if r["correct"]]
    wrong = [r["mean_logprob"] for r in resp if not r["correct"]]
    bins = np.linspace(min(correct + wrong), max(correct + wrong), 18)
    ax.hist(correct, bins=bins, alpha=0.7, color="#2ca02c",
            label=f"correct (n={len(correct)})")
    ax.hist(wrong, bins=bins, alpha=0.7, color="#d62728",
            label=f"incorrect (n={len(wrong)})")
    ax.axvline(np.mean(correct), color="#2ca02c", linestyle="--", alpha=0.8)
    ax.axvline(np.mean(wrong), color="#d62728", linestyle="--", alpha=0.8)
    ax.set_title("(a) confidence by correctness", fontsize=13, fontweight="bold")
    ax.set_xlabel("mean per-token log-probability", fontsize=10.5)
    ax.set_ylabel("count", fontsize=10.5)
    ax.legend(fontsize=10)
    ax.tick_params(labelsize=9)

    # ---- (b) calibration scatter ----
    ax = axes[1]
    colors = {"pre": "#1f77b4", "post": "#ff7f0e"}
    for cls in ["pre", "post"]:
        subset = [r for r in resp if r["cutoff_class"] == cls]
        for corr, marker, alpha in [(True, "o", 1.0), (False, "X", 0.85)]:
            items = [r for r in subset if r["correct"] == corr]
            ax.scatter([r["mean_logprob"] for r in items],
                       [r["mean_entropy"] for r in items],
                       marker=marker, s=34, color=colors[cls], alpha=alpha,
                       edgecolor="black" if corr else "none", linewidths=0.5,
                       label=f"{cls} {'correct' if corr else 'wrong'} (n={len(items)})")
    ax.set_title("(b) log-probability vs. entropy", fontsize=13, fontweight="bold")
    ax.set_xlabel("mean per-token log-probability (higher = more confident)",
                  fontsize=10.5)
    ax.set_ylabel("mean per-token entropy", fontsize=10.5)
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=9)

    fig.tight_layout()
    out = FIGURES_DIR / "confidence_merged.png"
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
