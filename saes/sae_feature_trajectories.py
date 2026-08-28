"""Feature-space (a-space) trajectories under h-space pushes.

The three views of Section 6.3 are static. This experiment adds the
dynamic view: the encoder a(h) is heavily nonlinear (TopK), so how an
h-space perturbation maps into a-space is not given by geometry alone.
For each wrong item's layer-28 state, sweep h + alpha * u along (i) the
unit probe refusal direction and (ii) the unit decoder direction of
feature 2191, encode each perturbed state, and record the mean
activation trajectories of the four Section 6.3 features plus the
active-set overlap with the unperturbed code (Jaccard), a direct
measure of the encoder's nonlinearity.

Writes figures/qwen3_1_7b/sae_feature_trajectories.{json,png}.
Run from the repo root: python -m saes.sae_feature_trajectories
"""
import json

import matplotlib.pyplot as plt
import numpy as np
import torch
from sae_lens import SAE

import analysis.make_probe_direction_atlas as atlas
from confabqa.constants import SAE_RELEASE, SAE_LAYER
from config import FIGURES_DIR, set_seeds

FEATURES = [2191, 14034, 18937, 21750]
ALPHAS = [-2000, -1000, -500, -200, 0, 200, 500, 1000, 1500, 2000, 3000]


def main():
    set_seeds()
    items = atlas.load_subset({"refusal", "wrong"})
    H = np.stack([r["h"] for r in items])
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in items])
    H_wrong = H[y == 0]

    d = atlas.recover_direction(items, "refusal")
    w = d["direction_raw"]
    u_probe = w / np.linalg.norm(w)

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    u_2191 = sae.W_dec.detach().cpu().numpy()[2191]
    u_2191 = u_2191 / np.linalg.norm(u_2191)

    def encode(X):
        with torch.no_grad():
            return sae.encode(torch.from_numpy(X).float()).numpy()

    base_codes = encode(H_wrong)
    base_sets = [set(np.nonzero(c)[0]) for c in base_codes]

    out = {"features": FEATURES, "alphas": ALPHAS,
           "n_wrong": int(H_wrong.shape[0]), "directions": {}}
    for name, u in [("probe", u_probe), ("d2191", u_2191)]:
        traj = {str(f): [] for f in FEATURES}
        active_frac_2191 = []
        jaccard = []
        for a in ALPHAS:
            codes = encode(H_wrong + a * u)
            for f in FEATURES:
                traj[str(f)].append(round(float(codes[:, f].mean()), 4))
            active_frac_2191.append(
                round(float((codes[:, 2191] > 0).mean()), 4))
            sets = [set(np.nonzero(c)[0]) for c in codes]
            j = [len(s & b) / len(s | b) for s, b in zip(sets, base_sets)]
            jaccard.append(round(float(np.mean(j)), 4))
        out["directions"][name] = {
            "mean_activation": traj,
            "frac_items_2191_active": active_frac_2191,
            "mean_jaccard_vs_alpha0": jaccard,
        }

    out_json = FIGURES_DIR / "sae_feature_trajectories.json"
    with open(out_json, "w") as f:
        json.dump(out, f, indent=1)
    print(f"Wrote {out_json}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=140, sharey=True)
    colors = {2191: "#ff7f0e", 14034: "#9467bd", 18937: "#2ca02c",
              21750: "#1f77b4"}
    titles = {"probe": "push along probe refusal direction",
              "d2191": "push along feature 2191 decoder direction"}
    for ax, name in zip(axes, ["probe", "d2191"]):
        data = out["directions"][name]
        for f in FEATURES:
            ax.plot(ALPHAS, data["mean_activation"][str(f)], marker="o",
                    ms=3.5, lw=1.8, color=colors[f], label=f"feature {f}")
        ax2 = ax.twinx()
        ax2.plot(ALPHAS, data["mean_jaccard_vs_alpha0"], ls=":", lw=1.6,
                 color="#666666")
        ax2.set_ylim(0, 1.05)
        if name == "d2191":
            ax2.set_ylabel("active-set overlap with $\\alpha=0$ (dotted)",
                           fontsize=8.5, color="#666666")
        else:
            ax2.set_yticklabels([])
        ax.set_title(titles[name], fontsize=10)
        ax.set_xlabel("$\\alpha$ (units of direction L2 norm)")
        ax.axvline(0, color="#bbbbbb", lw=0.8)
    axes[0].set_ylabel("mean feature activation (wrong items)")
    axes[0].legend(fontsize=8, loc="upper left")
    fig.suptitle("a-space trajectories of h-space pushes (n=%d wrong items)"
                 % out["n_wrong"], fontsize=11)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    out_png = FIGURES_DIR / "sae_feature_trajectories.png"
    plt.savefig(out_png, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out_png}")


if __name__ == "__main__":
    main()
