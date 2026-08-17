"""The plane spanned by the probe refusal direction and SAE feature 2191.

Companion to the Section 6.1 geometry figure: layer-28 refusal+wrong
states projected onto span{w_probe, W_dec[2191]}, with class centroids,
1-sigma covariance ellipses, both direction arrows (the angle between
them is arccos 0.16, about 81 degrees), the probe decision boundary
(exact: its normal is the x-axis), and ring markers on the items where
feature 2191 actually fires (SAE activation > 0).

Outputs: figures/qwen3_1_7b/probe_sae_plane.png
Run from the repo root: python -m plots.figure_probe_sae_plane
"""
import json

import matplotlib.pyplot as plt
import numpy as np
import torch
from sae_lens import SAE

import analysis.make_probe_direction_atlas as atlas
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, set_seeds
from plots.figure_direction_geometry import cov_ellipse


def main():
    set_seeds()
    items = atlas.load_subset({"refusal", "wrong"})
    d = atlas.recover_direction(items, "refusal")
    w = d["direction_raw"]
    u1 = w / np.linalg.norm(w)

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    d_f = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID]
    d_f = d_f / np.linalg.norm(d_f)
    cos_full = float(np.dot(u1, d_f))

    v = d_f - np.dot(d_f, u1) * u1
    u2 = v / np.linalg.norm(v)
    H = np.stack([r["h"] for r in items])
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in items])
    Q = (H - H.mean(axis=0)) @ np.stack([u1, u2]).T

    with torch.no_grad():
        acts = sae.encode(torch.from_numpy(H).float()).numpy()[:, SAE_FEATURE_ID]
    fired = acts > 0

    fig, ax = plt.subplots(figsize=(7.4, 5.6), dpi=140)
    ax.scatter(*Q[y == 0].T, s=14, c="#d62728", alpha=0.45,
               label=f"wrong (n={int((y == 0).sum())})")
    ax.scatter(*Q[y == 1].T, s=14, c="#1f77b4", alpha=0.55,
               label=f"refusal (n={int((y == 1).sum())})")
    if fired.any():
        ax.scatter(*Q[fired].T, s=80, facecolors="none", edgecolors="#000000",
                   lw=1.3, label=f"feature 2191 fires (n={int(fired.sum())})")
    q_w = cov_ellipse(ax, Q[y == 0], "#d62728")
    q_r = cov_ellipse(ax, Q[y == 1], "#1f77b4")
    ax.plot(*q_w, marker="*", ms=16, c="#7f1d1d", zorder=5)
    ax.plot(*q_r, marker="*", ms=16, c="#0b3d66", zorder=5)

    span = np.linalg.norm(q_r - q_w)
    theta = float(np.arccos(cos_full))
    L = 0.9 * span
    tips = []
    for vec, color, label, off in [
            (np.array([1.0, 0.0]), "#9467bd", "probe direction",
             np.array([-0.02, -0.10])),
            (np.array([np.cos(theta), np.sin(theta)]), "#ff7f0e",
             "SAE feature 2191 (opener)", np.array([0.12, 0.06]))]:
        tip = L * vec
        tips.append(tip)
        ax.annotate("", xy=tip, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color=color))
        ax.text(*(tip + off * span), label, color=color, fontsize=9,
                ha="center")
    ax.update_datalim(np.array(tips) * 1.2)
    ax.autoscale_view()

    def decision_at(x):
        h = H.mean(axis=0) + x * u1
        xs = d["scaler"].transform(h[None, :])
        return float(d["lr"].decision_function(d["pca"].transform(xs))[0])
    g0, g1 = decision_at(0.0), decision_at(1.0)
    x_star = -g0 / (g1 - g0)
    ax.axvline(x_star, color="#333333", lw=1.4, ls=":")
    ax.text(x_star, ax.get_ylim()[0] + 2, " probe decision boundary",
            fontsize=8.5, color="#333333", ha="left", va="bottom", rotation=90)

    ax.set_xlabel("along probe direction")
    ax.set_ylabel("orthogonal complement of feature 2191")
    ax.set_title("Probe direction vs SAE opener feature 2191")
    ax.legend(loc="upper left", fontsize=9)
    ax.text(0.02, 0.02,
            f"cos(probe, 2191) = {cos_full:.2f}  "
            f"(angle {np.degrees(theta):.0f}°)\n"
            f"2191 fires on {int(fired[y == 1].sum())}/{int((y == 1).sum())} "
            f"refusal and {int(fired[y == 0].sum())}/{int((y == 0).sum())} "
            f"wrong items",
            transform=ax.transAxes, fontsize=8.5, color="#444444", va="bottom")
    plt.tight_layout()
    out = FIGURES_DIR / "probe_sae_plane.png"
    plt.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out}")
    print(json.dumps({"cos": round(cos_full, 4),
                      "angle_deg": round(float(np.degrees(theta)), 1),
                      "fired_refusal": int(fired[y == 1].sum()),
                      "fired_wrong": int(fired[y == 0].sum())}))


if __name__ == "__main__":
    main()
