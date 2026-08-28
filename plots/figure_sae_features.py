"""Feature-card figure: the refusal-register ensemble (pre-norm geometry).

Each panel shows one SAE feature's decoder-lens tokens and its top
max-activating ConfabQA prompts, from figures/sae_decompose_prenorm.json
(computed on true post-block-27 residuals, the SAE's declared hook).

Outputs: figures/sae_features_card.png
"""
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.family'] = ['Hiragino Sans GB', 'Helvetica Neue', 'DejaVu Sans']

DATA = json.load(open("figures/sae_decompose_prenorm.json"))
FEATS = [2191, 14034, 17077, 4314]
TITLES = {
    2191:  "Feature 2191 — canonical refusal-opener (causal anchor)",
    14034: "Feature 14034 — `Sorry`/`Oops` register",
    17077: "Feature 17077 — formal register",
    4314:  "Feature 4314 — `moment` hedge",
}
LEGENDS = {
    2191:  "Fires on every refusal; its decoder direction alone flips wrong items (§6.3.1)",
    14034: "Fires with refusals, but its apology vocabulary never wins the argmax race",
    17077: "hereby / respectfully / duly / pursuant: deferential officialese",
    4314:  "The strongest refusal-vs-wrong discriminator by diff-z",
}


def feature_panel(ax, fid):
    r = DATA["features"][str(fid)]
    ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.0, 0.96, TITLES[fid], fontsize=12, fontweight="bold", va="top")
    sub = (f"diff_z = {r['diff_z']:+.2f}    hit% refusal = "
           f"{r['hit_rate_refusal']*100:.0f}    hit% wrong = "
           f"{r['hit_rate_wrong']*100:.0f}    align = {r['decoder_alignment']:+.4f}")
    ax.text(0.0, 0.89, sub, fontsize=9, color="#555555", va="top", family="monospace")

    ax.text(0.0, 0.79, "Top decoder logit-lens tokens:", fontsize=9.5,
            fontweight="bold", va="top")
    chip_y, chip_x, line_h = 0.725, 0.0, 0.065
    for i, tok in enumerate(r["lens_top"][:8]):
        s = repr(tok)
        if len(s) > 22: s = s[:19] + "...'"
        ax.text(chip_x, chip_y, s, fontsize=10, va="top",
                family=["Menlo", "Hiragino Sans GB"], color="white",
                bbox=dict(facecolor="#1f77b4", alpha=0.85, pad=2.5,
                          edgecolor="none", boxstyle="round,pad=0.25"))
        chip_x += 0.25
        if (i + 1) % 4 == 0:
            chip_x = 0.0
            chip_y -= line_h

    ax.text(0.0, 0.50, "Top max-activating prompts (ConfabQA):",
            fontsize=9.5, fontweight="bold", va="top")
    y = 0.45
    for pr in r["max_activating"]:
        color = "#d62728" if pr["label"] == "refusal" else "#7f7f7f"
        ax.text(0.0, y, f"[{pr['label']:>7s}]", fontsize=8.5, color=color,
                family="monospace", va="top", fontweight="bold")
        q = pr["q"]
        if len(q) > 70: q = q[:67] + "..."
        ax.text(0.135, y, f"act={pr['act']:7.1f}  {q}", fontsize=8.5, va="top")
        y -= 0.052
    ax.text(0.0, 0.02, LEGENDS[fid], fontsize=8, color="#555555",
            va="bottom", style="italic")


fig, axes = plt.subplots(2, 2, figsize=(14, 9), dpi=140)
for ax, fid in zip(axes.flat, FEATS):
    feature_panel(ax, fid)
fig.suptitle("SAE decomposition of the Qwen3-1.7B refusal direction "
             "(post-block-27 residual, Qwen-Scope w32k-L50)\n"
             "Four members of the refusal-register ensemble: opener, apology,"
             " formal officialese, hedge",
             fontsize=12, fontweight="bold", y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.93])
out = Path("figures/sae_features_card.png")
plt.savefig(out, bbox_inches="tight", facecolor="white")
print(f"Wrote {out}")
