"""Clean methods figure: three-panel schematic showing the probe pipeline
end to end. Replaces the dense merged-PNG of 08_qwen_architecture +
09_probe_pipeline with a focused single figure drawn from scratch.

Panel A: prompt → transformer with last-prompt-token hidden-state pickoff
         at every layer → hidden-state tensor.
Panel B: per-layer probe pipeline (StandardScaler → PCA(16) → LR + 5-fold CV).
Panel C: baselines applied to the same labels (majority class +
         prompt-text classifier).

Output: figures/methods_arch_and_pipeline.png  (replaces the existing
        merged file).
"""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# Color palette — data, operation, baseline
C_DATA = "#FFF3E0"     # light orange
C_DATA_EDGE = "#E65100"
C_OP = "#E3F2FD"       # light blue
C_OP_EDGE = "#0D47A1"
C_OUT = "#E8F5E9"      # light green
C_OUT_EDGE = "#1B5E20"
C_BASE = "#F3E5F5"     # light purple
C_BASE_EDGE = "#4A148C"
C_ARROW = "#37474F"

FIG_W = 8.5
FIG_H = 9.5

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=180)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(x, y, w, h, label, fc, ec, fontsize=9, ha="center", va="center",
        fontweight="normal"):
    """Draw a rounded rectangle with centered text."""
    bb = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                         linewidth=1.1, facecolor=fc, edgecolor=ec)
    ax.add_patch(bb)
    ax.text(x + w / 2, y + h / 2, label, ha=ha, va=va,
            fontsize=fontsize, fontweight=fontweight, color="#1a1a1a")


def arrow(x1, y1, x2, y2, label=None, label_offset=(0, 0)):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
        linewidth=1.4, color=C_ARROW))
    if label:
        ax.text((x1 + x2) / 2 + label_offset[0], (y1 + y2) / 2 + label_offset[1],
                label, fontsize=8, color="#555555", style="italic", ha="center")


# ====== PANEL A: Prompt → Transformer → Hidden-state tensor ======
ax.text(50, 97, "(A) Hidden-state capture", fontsize=12,
        fontweight="bold", ha="center", color="#1a1a1a")

# Prompt + tokenized
box(2, 84, 30, 7,
    "Prompt:\n“Who won the Nobel Prize in Physics in 1921?”",
    C_DATA, C_DATA_EDGE, fontsize=9)
arrow(17, 84, 17, 79)
box(2, 71, 30, 7,
    "Tokens: [USER] Who won …  1921? [ASST]\n"
    "                                                              ↑\n"
    "                                                last prompt token (position T)",
    C_DATA, C_DATA_EDGE, fontsize=8)
arrow(32, 74.5, 38, 74.5)

# Transformer block stack
tx, ty, tw, th = 38, 67, 28, 16
bb = FancyBboxPatch((tx, ty), tw, th, boxstyle="round,pad=0.4,rounding_size=1.5",
                     linewidth=1.1, facecolor=C_OP, edgecolor=C_OP_EDGE)
ax.add_patch(bb)
ax.text(tx + tw / 2, ty + th - 2, "Subject LM (e.g. Qwen3-1.7B):",
        ha="center", va="top", fontsize=9, fontweight="bold")
ax.text(tx + tw / 2, ty + th - 5,
        "L=28 transformer blocks", ha="center", va="top", fontsize=8,
        style="italic")
# Mini layer stack inside
for i in range(5):
    yy = ty + 2 + i * 2
    ax.add_patch(mpatches.Rectangle((tx + 9, yy), 10, 1.5,
                                     facecolor="#BBDEFB",
                                     edgecolor=C_OP_EDGE, lw=0.6))
ax.text(tx + tw / 2, ty + 1, "… capture h^(ℓ) at position T, every ℓ",
        ha="center", va="bottom", fontsize=7.5, style="italic", color="#555")

arrow(66, 74.5, 71, 74.5)

# Hidden-state tensor output
box(70, 71, 28, 7,
    "Hidden-state tensor\n(n items, L+1 layers, d_model)\n"
    "= (784, 29, 2048) for ConfabQA",
    C_OUT, C_OUT_EDGE, fontsize=8)

# Separator
ax.plot([5, 95], [62, 62], color="#cccccc", lw=0.6, linestyle="-")

# ====== PANEL B: Per-layer probe pipeline ======
ax.text(50, 59, "(B) Per-layer linear-probe pipeline", fontsize=12,
        fontweight="bold", ha="center")

# Input: slice at layer
box(2, 47, 22, 8,
    "Slice at layer ℓ:\nX = {h^(ℓ)} ∈ ℝ^(n×d)",
    C_DATA, C_DATA_EDGE, fontsize=8.5)
arrow(24, 51, 30, 51)

# Pipeline boxes (3 stacked operations)
box(30, 51, 18, 4, "StandardScaler", C_OP, C_OP_EDGE, fontsize=8.5)
arrow(48, 53, 50, 53)
box(50, 51, 18, 4, "PCA(n_components=16)", C_OP, C_OP_EDGE, fontsize=8.5)
arrow(68, 53, 70, 53)
box(70, 51, 18, 4, "LogReg(C=1.0)", C_OP, C_OP_EDGE, fontsize=8.5)

# Below: 5-fold CV
arrow(59, 51, 59, 46)
box(36, 39, 46, 6,
    "Stratified 5-fold CV  (random_state=0)\n→ per-layer probe accuracy",
    C_OUT, C_OUT_EDGE, fontsize=8.5)

# Probe targets list on left
box(2, 35, 22, 12,
    "Probe targets y ∈ {0,1}\n   correct\n   cutoff (pre/post)\n   refusal-vs-wrong\n   correct-within-pre",
    C_DATA, C_DATA_EDGE, fontsize=8, va="center")
arrow(24, 41, 36, 41)

# Separator
ax.plot([5, 95], [29, 29], color="#cccccc", lw=0.6, linestyle="-")

# ====== PANEL C: Baselines for honest comparison ======
ax.text(50, 26, "(C) Baselines (fit on the same labels, no hidden state)",
        fontsize=12, fontweight="bold", ha="center")

box(8, 14, 38, 8,
    "Majority baseline\n= max(P(y=1), P(y=0))",
    C_BASE, C_BASE_EDGE, fontsize=9)

box(54, 14, 38, 8,
    "Prompt-text classifier\nTF-IDF + LR on question text\n"
    "(+ engineered features, +domain, +category)",
    C_BASE, C_BASE_EDGE, fontsize=9)

# Verdict
ax.text(50, 7,
        "Probe is evidence of model-internal information   iff   "
        "probe accuracy  >  max(both baselines).",
        ha="center", fontsize=10, fontweight="bold", color="#1a1a1a")
ax.text(50, 3.5,
        "h_adds = probe peak  −  strongest baseline  (in pp; reported throughout §6).",
        ha="center", fontsize=9, style="italic", color="#555")

plt.tight_layout()
out = Path("figures/methods_arch_and_pipeline.png")
plt.savefig(out, bbox_inches="tight", facecolor="white")
print(f"Wrote {out}")
