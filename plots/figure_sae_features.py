"""Feature-card figure for the SAE decomposition of the Qwen3-1.7B refusal direction.

Each panel shows one SAE feature's:
  - top decoder-logit-lens tokens (as a chip cloud, ranked)
  - top max-activating prompts from v1.3 (labeled by judge_label)

Outputs: figures/sae_features_card.png
"""
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# CJK-capable font for refusal-opener glyphs
mpl.rcParams['font.family'] = ['Hiragino Sans GB', 'Helvetica Neue', 'DejaVu Sans']

DATA = json.load(open("figures/sae_decompose_refusal.json"))
FEATS = [2191, 14034, 18937, 21750]
TITLES = {
    2191:  "Feature 2191 — canonical refusal-opener",
    14034: "Feature 14034 — dormant `Sorry`/`Oops` opener",
    18937: "Feature 18937 — post-cutoff temporal cue",
    21750: "Feature 21750 — post-cutoff topical cue",
}
LEGENDS = {
    2191:  "Tokens this feature pushes to output: literal refusal openers from §6.6",
    14034: "Tokens this feature pushes to output: alternative apology pattern (never fires on ConfabQA-784)",
    18937: "Top prompts: recent dates that trigger Qwen3's `I can't answer that` pragmatics",
    21750: "Top prompts: recent cinema/award post-cutoff items",
}


def feature_panel(ax, fid):
    r = DATA["features"][str(fid)]
    diff_z = r["diff_z"]; hr = r["hit_rate_refusal"] * 100; hw = r["hit_rate_wrong"] * 100

    ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    # Title bar
    ax.text(0.0, 0.96, TITLES[fid], fontsize=12.5, fontweight="bold", va="top")
    sub = f"diff_z = {diff_z:+.2f}    hit% refusal = {hr:.0f}    hit% wrong = {hw:.0f}    align = {r['decoder_alignment']:+.4f}"
    ax.text(0.0, 0.89, sub, fontsize=9, color="#555555", va="top", family="monospace")

    # Top tokens as monospace chips (single column)
    ax.text(0.0, 0.79, "Top decoder logit-lens tokens:", fontsize=9.5, fontweight="bold", va="top")
    tokens = r["top_tokens"][:10]
    chip_y = 0.74
    chip_x = 0.0
    line_h = 0.045
    for i, tok in enumerate(tokens):
        s = repr(tok)
        if len(s) > 22: s = s[:19] + "...'"
        ax.text(chip_x, chip_y, s, fontsize=10, family="monospace",
                color="white", bbox=dict(facecolor="#1f77b4", alpha=0.85, pad=2.5,
                                          edgecolor="none", boxstyle="round,pad=0.25"))
        chip_x += 0.20
        if (i + 1) % 5 == 0:
            chip_x = 0.0
            chip_y -= line_h

    # Top max-activating prompts
    ax.text(0.0, 0.50, "Top max-activating prompts (ConfabQA-784):", fontsize=9.5, fontweight="bold", va="top")
    y = 0.45
    for p in r["top_prompts"]:
        color = "#d62728" if p["judge_label"] == "refusal" else "#7f7f7f"
        label = f"[{p['judge_label']:>7s}]"
        q = p["question"]
        if len(q) > 70: q = q[:67] + "..."
        ax.text(0.0, y, label, fontsize=8.5, color=color, family="monospace", va="top", fontweight="bold")
        ax.text(0.135, y, f"act={p['activation']:5.2f}  {q}", fontsize=8.5, va="top")
        y -= 0.052

    # Legend at bottom
    ax.text(0.0, 0.02, LEGENDS[fid], fontsize=8, color="#555555", va="bottom", style="italic")


fig, axes = plt.subplots(2, 2, figsize=(14, 9), dpi=140)
for ax, fid in zip(axes.flat, FEATS):
    feature_panel(ax, fid)

fig.suptitle("SAE decomposition of the Qwen3-1.7B refusal direction (layer 28, Qwen-Scope w32k-L50)\n"
             "Four features that together compose the recovered refusal direction "
             "— two refusal-opener vocabulary features (left) and two post-cutoff cue features (right)",
             fontsize=12, fontweight="bold", y=0.99)

plt.tight_layout(rect=[0, 0, 1, 0.93])
out = Path("figures/sae_features_card.png")
plt.savefig(out, bbox_inches="tight", facecolor="white")
print(f"Wrote {out}")
