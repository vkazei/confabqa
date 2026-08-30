"""Composite geometry figure: the six refusal-direction candidates.

Panel (a): pairwise cosine matrix of the six recoveries (full-subset
probe, within-post probe, native pre-norm probe, pre-norm class-mean
difference, SAE 2191 decoder, directly optimized), chance ~0.02 in
2048-d. Panel (b): held-out first-token flip curves vs dose in
fractions of the mean state norm, from the stored artifacts.

Writes figures/qwen3_1_7b/direction_candidates.png.
Run from the repo root: python -m plots.figure_direction_candidates
"""
import json

import matplotlib.pyplot as plt
import numpy as np

import analysis.make_probe_direction_atlas as atlas
from analysis.cache_prenorm_states import load_prenorm
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, set_seeds


def unit(v):
    return v / np.linalg.norm(v)


def main():
    set_seeds()
    dirs = {}
    d_full = atlas.recover_direction(atlas.load_subset({"refusal", "wrong"}),
                                     "refusal")
    dirs["probe (full)"] = unit(d_full["direction_raw"])
    dirs["probe (within-post)"] = unit(np.load(
        FIGURES_DIR / "12_probe_direction_refusal_vs_wrong_within_post.npy"))

    items_pn, H_pn = load_prenorm({"refusal", "wrong"})
    for r, h in zip(items_pn, H_pn):
        r["h"] = h
    dirs["probe (native pre-norm)"] = unit(
        atlas.recover_direction(items_pn, "refusal")["direction_raw"])
    labs = np.array([r["judge_label"] for r in items_pn])
    dirs["class-mean diff"] = unit(H_pn[labs == "refusal"].mean(0)
                                   - H_pn[labs == "wrong"].mean(0))

    from sae_lens import SAE
    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    dirs["SAE 2191 decoder"] = unit(
        sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID])
    dirs["directly optimized"] = unit(
        np.load(FIGURES_DIR / "optimized_refusal_direction.npy"))

    names = list(dirs)
    n = len(names)
    C = np.zeros((n, n))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            C[i, j] = float(dirs[a] @ dirs[b])

    opt = json.load(open(FIGURES_DIR / "optimized_refusal_direction.json"))
    rev = json.load(open(FIGURES_DIR / "revision_analyses.json"))
    budgets = [50, 100, 200, 350, 500, 750, 1500]
    frac = [b / 1640 for b in budgets]
    curves = {
        "probe (within-post)": [opt["heldout_flip_rates"]["probe_within_post"][str(b)] for b in budgets],
        "probe (native pre-norm)": [rev["prenorm_refit"]["heldout_flips_prenorm_dir"][str(b)] for b in budgets],
        "class-mean diff": [opt["heldout_flip_rates"]["diff_means_prenorm"][str(b)] for b in budgets],
        "SAE 2191 decoder": [opt["heldout_flip_rates"]["sae_2191"][str(b)] for b in budgets],
        "directly optimized": [opt["heldout_flip_rates"]["optimized"][str(b)] for b in budgets],
    }
    colors = {"probe (within-post)": "#7b52ae", "probe (native pre-norm)": "#b085d6",
              "class-mean diff": "#2ca02c", "SAE 2191 decoder": "#ff7f0e",
              "directly optimized": "#d62728"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4), dpi=140,
                                   gridspec_kw={"width_ratios": [1.05, 1]})
    im = ax1.imshow(C, vmin=0, vmax=1, cmap="viridis")
    short = ["probe full", "probe w-post", "probe pre-norm", "mean diff",
             "2191 dec.", "optimized"]
    ax1.set_xticks(range(n), short, rotation=40, ha="right", fontsize=8)
    ax1.set_yticks(range(n), short, fontsize=8)
    for i in range(n):
        for j in range(n):
            ax1.text(j, i, f"{C[i, j]:.2f}", ha="center", va="center",
                     fontsize=7.5,
                     color="white" if C[i, j] < 0.55 else "black")
    ax1.set_title("(a) pairwise cosines (chance $\\approx 0.02$)", fontsize=10)
    fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.03)

    for name, ys in curves.items():
        ax2.plot(frac, ys, marker="o", ms=3.5, lw=1.8, color=colors[name],
                 label=name)
    ax2.set_xlabel("dose (fraction of mean state norm)")
    ax2.set_ylabel("held-out first-token refusal-opener rate")
    ax2.set_title("(b) causal dose-response ($n=201$ wrong items)", fontsize=10)
    ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=7.5, loc="lower right")
    ax2.grid(alpha=0.25)

    plt.tight_layout()
    out = FIGURES_DIR / "direction_candidates.png"
    plt.savefig(out, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out}")
    print(np.round(C, 3))


if __name__ == "__main__":
    main()
