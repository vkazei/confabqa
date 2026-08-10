"""Merged hidden-state embedding figure (replaces 03_pca_layer_14 + 04_pca_layer_28).

The two figures 03_analyze.py emits are each a 1x2 panel showing the SAME points
colored once by correctness and once by cutoff class -- four panels, each a single
binary encoding. This script collapses all four into one figure with two larger
panels (a mid-network layer and the final layer), each a single scatter that encodes
three variables at once:

  - color   = judge label   (correct / refusal / wrong)   [3-way, richer than binary]
  - marker   = cutoff class  (pre = circle, post = triangle)
  - size     = mean per-token log-probability (bigger = more confident)

Reads the same cached responses + activations 03_analyze.py uses; writes
figures/qwen3_1_7b/embeddings_pca_merged.png. Does not modify any frozen script.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib.lines import Line2D
from sklearn.decomposition import PCA

from config import ACTIVATIONS_DIR, FIGURES_DIR, RESPONSES_DIR

LAYERS = [14, 28]                      # mid-network, final layer
PANEL_TITLES = ["Layer 14 (mid-network)", "Layer 28 (final layer)"]

# judge label -> color
LABEL_COLOR = {"correct": "#2ca02c", "refusal": "#1f77b4", "wrong": "#d62728"}
LABEL_ORDER = ["wrong", "correct", "refusal"]      # z-order: refusals drawn on top
# cutoff class -> marker
CUTOFF_MARKER = {"pre": "o", "post": "^"}


def load_all():
    out = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        r = json.load(open(f))
        act = torch.load(ACTIVATIONS_DIR / f"{r['question_id']}.pt", weights_only=False)
        r["h"] = act["last_prompt_hidden"].numpy()
        out.append(r)
    return out


def size_from_logprob(lp, lo, hi):
    """Map mean logprob (more negative = less confident) to marker area [22, 150]."""
    lp = np.clip(lp, lo, hi)
    frac = (lp - lo) / (hi - lo + 1e-9)          # 0 = least confident, 1 = most
    return 22 + frac * (150 - 22)


def main():
    resp = load_all()
    labels = np.array([r.get("judge_label", "wrong") for r in resp])
    cutoff = np.array([r["cutoff_class"] for r in resp])
    lp = np.array([r.get("mean_logprob", np.nan) for r in resp], dtype=float)
    lo, hi = np.nanpercentile(lp, 5), np.nanpercentile(lp, 95)
    sizes = size_from_logprob(lp, lo, hi)

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.1), dpi=200)

    for ax, layer, title in zip(axes, LAYERS, PANEL_TITLES):
        X = np.stack([r["h"][layer] for r in resp])
        pca = PCA(n_components=2)
        XY = pca.fit_transform(X)
        for lab in LABEL_ORDER:
            for cls, marker in CUTOFF_MARKER.items():
                m = (labels == lab) & (cutoff == cls)
                if not m.any():
                    continue
                ax.scatter(XY[m, 0], XY[m, 1], s=sizes[m], marker=marker,
                           facecolor=LABEL_COLOR[lab], edgecolor="white",
                           linewidths=0.4, alpha=0.62, zorder=2 + LABEL_ORDER.index(lab))
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%} var)", fontsize=10.5)
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%} var)", fontsize=10.5)
        ax.grid(True, alpha=0.25)
        ax.tick_params(labelsize=9)

    # ---- unified legend: color (label), shape (cutoff), size (confidence) ----
    color_handles = [
        Line2D([0], [0], marker="o", linestyle="", markersize=9,
               markerfacecolor=LABEL_COLOR[l], markeredgecolor="white",
               label=f"{l}  (n={int((labels==l).sum())})")
        for l in ["correct", "refusal", "wrong"]
    ]
    shape_handles = [
        Line2D([0], [0], marker=CUTOFF_MARKER["pre"], linestyle="", markersize=9,
               markerfacecolor="#888", markeredgecolor="white", label="pre-cutoff"),
        Line2D([0], [0], marker=CUTOFF_MARKER["post"], linestyle="", markersize=9,
               markerfacecolor="#888", markeredgecolor="white", label="post-cutoff"),
    ]
    size_handles = [
        Line2D([0], [0], marker="o", linestyle="", markersize=4.5,
               markerfacecolor="#888", markeredgecolor="white", label="less confident"),
        Line2D([0], [0], marker="o", linestyle="", markersize=10,
               markerfacecolor="#888", markeredgecolor="white", label="more confident"),
    ]
    leg1 = fig.legend(handles=color_handles, title="judge label (color)",
                      loc="lower center", bbox_to_anchor=(0.19, -0.02),
                      ncol=1, fontsize=10, title_fontsize=10, frameon=False)
    leg2 = fig.legend(handles=shape_handles, title="cutoff (shape)",
                      loc="lower center", bbox_to_anchor=(0.5, -0.02),
                      ncol=1, fontsize=10, title_fontsize=10, frameon=False)
    fig.legend(handles=size_handles, title="mean log-prob (size)",
               loc="lower center", bbox_to_anchor=(0.81, -0.02),
               ncol=1, fontsize=10, title_fontsize=10, frameon=False)
    fig.add_artist(leg1)
    fig.add_artist(leg2)

    fig.tight_layout(rect=[0, 0.14, 1, 1])
    out = FIGURES_DIR / "embeddings_pca_merged.png"
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
