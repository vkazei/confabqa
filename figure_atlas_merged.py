"""Merged Confabulation Atlas figure: 6 panels -> 2.

Panels (a) correctness, (b) judge label, and (e) logprob quartile of the original
atlas are three views of the same points; they collapse into one multi-channel
scatter. Panel (c) category becomes the marker shape (well-known / obscure /
post-cutoff -- strictly finer than pre/post). Panel (d) domain is dropped
(never load-bearing in the atlas narrative; per-domain tables live in Appendix A).
Panel (f), the unsupervised PCA(2) control, is kept as the right panel with the
same encoding for direct comparison.

Left panel  : supervised projection (signed distances to the correctness and
              orthogonalized refusal-vs-correct hyperplanes), color = judge
              label, shape = category, size = mean per-token log-probability.
Right panel : unsupervised PCA(2) of the same layer-18 hidden states, same
              encoding.

Projection math is imported from make_atlas_figure.py verbatim, so distances,
accuracies, and the hyperplane angle are identical to the original figure.
Writes figures/qwen3_1_7b/atlas_merged_layer18.png.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from config import FIGURES_DIR, set_seeds
from make_atlas_figure import ATLAS_LAYER, fit_two_hyperplanes, load_all

LABEL_COLOR = {"correct": "#2ca02c", "refusal": "#1f77b4", "wrong": "#d62728"}
LABEL_ORDER = ["wrong", "correct", "refusal"]
CAT_MARKER = {"well_known": "o", "obscure": "D", "post_cutoff": "^"}
CAT_PRETTY = {"well_known": "well-known (pre)", "obscure": "obscure (pre)",
              "post_cutoff": "post-cutoff"}


def sizes_from_logprob(lp):
    lo, hi = np.nanpercentile(lp, 5), np.nanpercentile(lp, 95)
    frac = (np.clip(lp, lo, hi) - lo) / (hi - lo + 1e-9)
    return 20 + frac * (130 - 20)


def multi_scatter(ax, XY, labels, cats, sizes):
    for lab in LABEL_ORDER:
        for cat, marker in CAT_MARKER.items():
            m = (labels == lab) & (cats == cat)
            if not m.any():
                continue
            ax.scatter(XY[m, 0], XY[m, 1], s=sizes[m], marker=marker,
                       facecolor=LABEL_COLOR[lab], edgecolor="white",
                       linewidths=0.4, alpha=0.65,
                       zorder=2 + LABEL_ORDER.index(lab))


def main():
    set_seeds()
    resp = load_all()
    X = np.stack([r["last_prompt_hidden"][ATLAS_LAYER] for r in resp])
    y_correct = np.array([r["correct"] for r in resp], dtype=int)
    y_judge = np.array([r["judge_label"] for r in resp])
    y_cat = np.array([r.get("category") or "unknown" for r in resp])
    lp = np.array([r["mean_logprob"] for r in resp])
    sizes = sizes_from_logprob(lp)

    ax_x, ax_y, int_x, int_y, acc_x, acc_y, angle_deg = fit_two_hyperplanes(
        X, y_correct, y_judge)
    X2 = np.column_stack([ax_x, ax_y])
    sub_n = int(((y_judge == "refusal") | (y_judge == "correct")).sum())
    print(f"layer {ATLAS_LAYER}: acc_x={acc_x:.3f} acc_y={acc_y:.3f} "
          f"(n_sub={sub_n}) angle={angle_deg:.1f}")

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.3), dpi=200)

    # ---- left: supervised projection ----
    ax = axes[0]
    ax.axvline(int_x, color="#444", linestyle="--", linewidth=1, alpha=0.5)
    ax.axhline(int_y, color="#444", linestyle="--", linewidth=1, alpha=0.5)
    multi_scatter(ax, X2, y_judge, y_cat, sizes)
    ax.set_title("(a) supervised: two probe hyperplanes", fontsize=13, fontweight="bold")
    ax.set_xlabel(f"signed dist. from correctness hyperplane (CV acc {acc_x:.1%})",
                  fontsize=10.5)
    ax.set_ylabel(f"signed dist. from refusal-vs-correct hyperplane\n"
                  f"(CV acc {acc_y:.1%} on n={sub_n} subset)", fontsize=10.5)
    ax.grid(True, alpha=0.22)
    ax.tick_params(labelsize=9)

    # ---- right: unsupervised PCA(2) control, same encoding ----
    ax = axes[1]
    Xs = StandardScaler().fit_transform(X)
    pca2 = PCA(n_components=2).fit(Xs)
    X2u = pca2.transform(Xs)
    ev = pca2.explained_variance_ratio_
    multi_scatter(ax, X2u, y_judge, y_cat, sizes)
    ax.set_title("(b) unsupervised: PCA(2), same layer", fontsize=13, fontweight="bold")
    ax.set_xlabel(f"PC1 ({ev[0]:.1%} of variance)", fontsize=10.5)
    ax.set_ylabel(f"PC2 ({ev[1]:.1%} of variance)", fontsize=10.5)
    ax.grid(True, alpha=0.22)
    ax.tick_params(labelsize=9)

    # ---- one shared legend band ----
    color_h = [Line2D([0], [0], marker="o", ls="", ms=9.5,
                      markerfacecolor=LABEL_COLOR[l], markeredgecolor="white",
                      label=f"{l} (n={int((y_judge==l).sum())})")
               for l in ["correct", "refusal", "wrong"]]
    shape_h = [Line2D([0], [0], marker=m, ls="", ms=9,
                      markerfacecolor="#888", markeredgecolor="white",
                      label=CAT_PRETTY[c])
               for c, m in CAT_MARKER.items()]
    size_h = [Line2D([0], [0], marker="o", ls="", ms=4.5, markerfacecolor="#888",
                     markeredgecolor="white", label="less confident"),
              Line2D([0], [0], marker="o", ls="", ms=10, markerfacecolor="#888",
                     markeredgecolor="white", label="more confident")]
    l1 = fig.legend(handles=color_h, title="judge label (color)",
                    loc="lower center", bbox_to_anchor=(0.18, -0.015),
                    fontsize=10, title_fontsize=10, frameon=False)
    l2 = fig.legend(handles=shape_h, title="category (shape)",
                    loc="lower center", bbox_to_anchor=(0.5, -0.015),
                    fontsize=10, title_fontsize=10, frameon=False)
    fig.legend(handles=size_h, title="mean log-prob (size)",
               loc="lower center", bbox_to_anchor=(0.82, -0.015),
               fontsize=10, title_fontsize=10, frameon=False)
    fig.add_artist(l1)
    fig.add_artist(l2)

    fig.tight_layout(rect=[0, 0.14, 1, 1])
    out = FIGURES_DIR / f"atlas_merged_layer{ATLAS_LAYER}.png"
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
