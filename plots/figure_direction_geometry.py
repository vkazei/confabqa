"""Geometry of the two refusal-direction recoveries in PCA(2).

Layer-28 refusal+wrong hidden states projected onto their top two raw
principal components, with per-class centroids and 1-sigma covariance
ellipses, plus the in-plane projections of (a) the class-mean
difference (which by construction connects the two centroids) and
(b) the discriminative probe direction. Annotates the full-space
cosine between the two and the fraction of each direction's norm that
lies in the plotted plane.

Outputs: figures/qwen3_1_7b/direction_geometry.png
Run from the repo root: python -m plots.figure_direction_geometry
"""
import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA

import analysis.make_probe_direction_atlas as atlas
from config import FIGURES_DIR, set_seeds


def cov_ellipse(ax, pts, color):
    mu = pts.mean(axis=0)
    cov = np.cov(pts.T)
    vals, vecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(vecs[1, -1], vecs[0, -1]))
    w, h = 2 * np.sqrt(vals[-1]), 2 * np.sqrt(vals[0])
    ax.add_patch(Ellipse(mu, w, h, angle=angle, facecolor="none",
                         edgecolor=color, lw=1.6, ls="--", alpha=0.9))
    return mu


def main():
    set_seeds()
    items = atlas.load_subset({"refusal", "wrong"})
    d = atlas.recover_direction(items, "refusal")
    w_probe = d["direction_raw"]

    H = np.stack([r["h"] for r in items])
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in items])
    diff_means = H[y == 1].mean(axis=0) - H[y == 0].mean(axis=0)

    pca = PCA(n_components=2).fit(H)
    P = pca.transform(H)

    def inplane(v):
        p = pca.components_ @ v
        return p, float(np.linalg.norm(p) / np.linalg.norm(v))

    p_dm, frac_dm = inplane(diff_means)
    p_probe, frac_probe = inplane(w_probe)
    cos_full = float(np.dot(w_probe, diff_means)
                     / (np.linalg.norm(w_probe) * np.linalg.norm(diff_means)))

    fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=140)
    ax.scatter(*P[y == 0].T, s=14, c="#d62728", alpha=0.45,
               label=f"wrong (n={int((y == 0).sum())})")
    ax.scatter(*P[y == 1].T, s=14, c="#1f77b4", alpha=0.55,
               label=f"refusal (n={int((y == 1).sum())})")
    mu_w = cov_ellipse(ax, P[y == 0], "#d62728")
    mu_r = cov_ellipse(ax, P[y == 1], "#1f77b4")
    ax.plot(*mu_w, marker="*", ms=16, c="#7f1d1d", zorder=5)
    ax.plot(*mu_r, marker="*", ms=16, c="#0b3d66", zorder=5)

    # diff-means arrow: centroid to centroid (its in-plane projection)
    ax.annotate("", xy=mu_r, xytext=mu_w,
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#2ca02c"))
    # probe-direction arrow from the overall mean, scaled for display
    m = P.mean(axis=0)
    scale = 0.55 * np.linalg.norm(mu_r - mu_w) / max(np.linalg.norm(p_probe), 1e-9)
    ax.annotate("", xy=m + scale * p_probe, xytext=m,
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#9467bd"))
    ax.text(*(mu_w + 0.55 * (mu_r - mu_w) + np.array([10, 14])),
            "difference of means\n(connects centroids)",
            color="#2ca02c", fontsize=9, ha="center")
    ax.text(*(m + scale * p_probe + np.array([-4, -20])),
            "probe direction\n(in-plane projection)",
            color="#9467bd", fontsize=9, ha="center")

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.0%} var)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.0%} var)")
    ax.set_title("Layer-28 refusal vs wrong: two recoveries of \"the\" direction")
    ax.legend(loc="upper left", fontsize=9)
    ax.text(0.02, 0.02,
            f"full-space cosine(probe, diff-means) = {cos_full:.2f}\n"
            f"norm fraction in this plane: diff-means {frac_dm:.0%}, "
            f"probe {frac_probe:.0%}",
            transform=ax.transAxes, fontsize=8.5, color="#444444", va="bottom")
    plt.tight_layout()
    out = FIGURES_DIR / "direction_geometry.png"
    plt.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out}")
    print(json.dumps({"cos_full": round(cos_full, 4),
                      "frac_dm": round(frac_dm, 4),
                      "frac_probe": round(frac_probe, 4),
                      "evr": [round(float(v), 4)
                              for v in pca.explained_variance_ratio_]}))


if __name__ == "__main__":
    main()
