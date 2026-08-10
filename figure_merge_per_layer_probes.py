"""Merge §6.4's four per-layer probe figures into a single comparison plot.

All four have the same axes (layer 0..28 vs probe accuracy) but live as
separate figures, which makes it hard to compare the *shape* of the per-
layer curves. This script reads the saved per-layer accuracies from
`data/qwen3_1_7b_summary.json` and replots all five targets on a single
axis with consistent colours, plus per-target majority baselines as dashed
lines.

Targets:
  correct (n=784)
  cutoff (n=784)
  refusal_vs_wrong (n=549)
  correct_within_pre (n=296)
  correct_within_obscure (n=153)

Output: figures/per_layer_probes_merged.png
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

SUMMARY = json.load(open("data/qwen3_1_7b_summary.json"))
P = SUMMARY["probes"]

# Order, colours, labels
TARGETS = [
    ("correct",                "#1f77b4", "correct (all, n=784)"),
    ("cutoff",                 "#ff7f0e", "cutoff (all, n=784)"),
    ("refusal_vs_wrong",       "#2ca02c", "refusal-vs-wrong (n=549)"),
    ("correct_within_pre",     "#d62728", "correct within pre-cutoff (n=296)"),
    ("correct_within_obscure", "#9467bd", "correct within obscure (n=153)"),
]

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=160)
for key, color, label in TARGETS:
    d = P[key]
    accs = [a * 100 for a in d["per_layer_acc"]]
    layers = list(range(len(accs)))
    ax.plot(layers, accs, color=color, lw=1.8, label=label)
    # Per-target majority baseline as faint dashed horizontal
    base = d["baseline"] * 100
    ax.axhline(base, color=color, lw=0.8, ls=":", alpha=0.5)
    # Mark peak
    peak_layer = max(range(len(accs)), key=lambda i: accs[i])
    ax.plot(peak_layer, accs[peak_layer], "o", color=color, ms=6,
            markeredgecolor="black", markeredgewidth=0.6)
    ax.annotate(f"L{peak_layer}", xy=(peak_layer, accs[peak_layer]),
                xytext=(3, 4), textcoords="offset points",
                fontsize=8, color=color, fontweight="bold")

ax.set_xlabel("layer  (0 = embedding, 28 = final residual stream)", fontsize=10)
ax.set_ylabel("probe accuracy (%)", fontsize=10)
ax.set_xlim(0, 28); ax.set_xticks(range(0, 29, 2))
ax.set_ylim(50, 100)
ax.set_title("Per-layer probe accuracy on Qwen3-1.7B (ConfabQA-784)\n"
             "Solid lines: probe accuracy. Dotted lines: per-target majority baseline. "
             "Dot: per-target peak layer.",
             fontsize=10.5, pad=8)
ax.grid(alpha=0.25)
ax.legend(loc="lower right", fontsize=9, framealpha=0.95)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

plt.tight_layout()
out = Path("figures/per_layer_probes_merged.png")
plt.savefig(out, bbox_inches="tight", facecolor="white")
print(f"Wrote {out}")
