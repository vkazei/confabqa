"""Generate the two schematic figures for the paper:

  figures/08_qwen_architecture.png  -- decoder-only transformer block schematic
                                       with last-prompt-token hidden-state pickoff
  figures/09_probe_pipeline.png      -- per-layer hidden-state extraction +
                                       StandardScaler -> PCA -> LogReg + 5-fold CV
"""
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from config import FIGURES_DIR


def _bbox(ax, x, y, w, h, text, fc="#e8eef7", ec="#33486b", fontsize=9, **kw):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.02",
                         linewidth=1.0, facecolor=fc, edgecolor=ec, **kw)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, color="#1a1a1a", zorder=5)


def _arrow(ax, x1, y1, x2, y2, color="#33486b", style="-|>", lw=1.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                  arrowstyle=style, color=color, lw=lw,
                                  mutation_scale=11, zorder=3))


def figure_qwen_architecture(out_path):
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis("off")
    ax.set_title("Qwen3-1.7B decoder-only transformer with last-prompt-token hidden-state pickoff",
                 fontsize=12, pad=8)

    # tokens row
    tokens = ["[USER]", "Who", "won", "Super", "Bowl", "LIX", "?", "[ASST]"]
    n = len(tokens)
    x0, dx = 0.5, 1.05
    for i, t in enumerate(tokens):
        is_last = (i == n - 1)
        _bbox(ax, x0 + i * dx, 0.2, 0.95, 0.4, t,
              fc="#fde9d6" if is_last else "#f6efe3",
              ec="#a85a1a" if is_last else "#a17a3a",
              fontsize=8)
    ax.text(5.0, -0.05, "tokenized prompt (T tokens) -- T is the last prompt position",
            ha="center", fontsize=8, color="#555", style="italic")

    # embedding layer
    _bbox(ax, 0.5, 0.9, 8.95, 0.4, "Token embedding (layer 0)  --  shape (T, d=2048)",
          fc="#dde6f3", ec="#33486b", fontsize=9)
    for i in range(n):
        _arrow(ax, x0 + i * dx + 0.475, 0.6, x0 + i * dx + 0.475, 0.9)

    # transformer blocks
    block_x, block_w = 0.5, 8.95
    block_h = 0.36
    y_base = 1.30
    n_blocks_shown = 8
    label_map = {0: "Block 1", 1: "Block 7", 2: "Block 13", 3: "Block 18",
                 4: "Block 22", 5: "Block 24", 6: "Block 26", 7: "Block 28"}
    peak_indices = {1, 2, 3, 7}  # blocks 7, 13, 18, 28 are the v1.3 (re-run) peaks
    peak_caption = {1: "<- peak: correct_within_obscure (80.5%)",
                    2: "<- peak: cutoff (98.2%)",
                    3: "<- peak: correct all-items (82.4%) AND correct_within_pre (84.8%)",
                    7: "<- peak: refusal_vs_wrong (89.4%)"}
    for k in range(n_blocks_shown):
        y = y_base + k * (block_h + 0.04)
        is_peak = k in peak_indices
        fc = "#fde9d6" if is_peak else "#e8eef7"
        ec = "#a85a1a" if is_peak else "#33486b"
        _bbox(ax, block_x, y, block_w, block_h,
              f"{label_map[k]}:  RMSNorm -> Multi-head self-attn -> RMSNorm -> SwiGLU MLP",
              fc=fc, ec=ec, fontsize=8)
        if is_peak:
            ax.text(block_x + block_w + 1.85, y + block_h / 2,
                    peak_caption[k], fontsize=7.5, color="#a85a1a",
                    va="center", ha="left", style="italic")

    # ellipsis between sparse blocks
    for k in [1, 3, 5]:
        y_eli = y_base + k * (block_h + 0.04) + block_h + 0.005
        ax.text(0.7, y_eli, "...", fontsize=9, color="#888")

    # final norm + LM head
    y_top = y_base + n_blocks_shown * (block_h + 0.04) + 0.05
    _bbox(ax, block_x, y_top, block_w, 0.4, "Final RMSNorm  +  LM head (tied embedding)",
          fc="#dde6f3", ec="#33486b", fontsize=9)
    ax.text(block_x + block_w + 0.05, y_top + 0.2, "-> p(x_{T+1} | x_{1:T})",
            fontsize=9, va="center", color="#555")

    # pickoff strip
    pick_x = block_x + block_w + 0.95
    ax.add_patch(Rectangle((pick_x - 0.05, y_base - 0.1), 0.7,
                            y_top - y_base + 0.5,
                            linewidth=1.2, edgecolor="#a85a1a",
                            facecolor="#fff7ec", linestyle="--", zorder=2))
    ax.text(pick_x + 0.3, y_top + 0.6, "h^(l)_T",
            ha="center", fontsize=10, color="#a85a1a", weight="bold")
    ax.text(pick_x + 0.3, y_top + 0.35, "l=0..28",
            ha="center", fontsize=8, color="#a85a1a")

    # arrows from each block into the pickoff
    for k in range(n_blocks_shown):
        y = y_base + k * (block_h + 0.04) + block_h / 2
        _arrow(ax, block_x + block_w + 0.02, y, pick_x - 0.02, y,
               color="#a85a1a", lw=0.8)
    # also from embedding layer
    _arrow(ax, block_x + block_w + 0.02, 1.1, pick_x - 0.02, 1.1,
           color="#a85a1a", lw=0.8)

    # legend at top
    ax.text(5.5, 7.25,
            "Architecture: L = 28 transformer blocks, hidden dim d = 2048.  "
            "The hidden state at the LAST prompt token (position T) is captured at every layer "
            "(0 = embedding, 1..28 = transformer blocks) and stacked into a tensor of shape (29, 2048) per question.  "
            "Highlighted blocks (7, 13, 18, 28) are the layers at which the v1.3 probes peak.",
            fontsize=8, color="#444", ha="center", va="center", style="italic", wrap=True)

    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def figure_probe_pipeline(out_path):
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.set_title("Per-layer linear-probe pipeline",
                 fontsize=12, pad=10)

    # Stage 1: hidden state tensor
    _bbox(ax, 0.3, 4.5, 2.4, 1.2,
          "Hidden state tensor\n(n, L+1, d)\n= (784, 29, 2048)",
          fc="#fff7ec", ec="#a85a1a", fontsize=9)
    ax.text(1.5, 4.35, "captured during prefill", fontsize=7, ha="center",
            color="#666", style="italic")

    # Stage 2: slice by layer
    _arrow(ax, 2.7, 5.1, 3.2, 5.1)
    _bbox(ax, 3.2, 4.5, 2.4, 1.2,
          "For each layer l:\nX_l = h^(l)_T over n items\nshape (n, d) = (784, 2048)",
          fc="#e8eef7", ec="#33486b", fontsize=9)

    # Stage 3: pipeline
    _arrow(ax, 5.6, 5.1, 6.1, 5.1)
    _bbox(ax, 6.1, 5.0, 3.6, 0.7,
          "StandardScaler (zero-mean, unit-var per feature)",
          fc="#e2efe3", ec="#3a7a4a", fontsize=8)
    _bbox(ax, 6.1, 4.2, 3.6, 0.7,
          "PCA(n_components=16)  (top-16 principal directions)",
          fc="#e2efe3", ec="#3a7a4a", fontsize=8)
    _bbox(ax, 6.1, 3.4, 3.6, 0.7,
          "LogisticRegression(C=1.0, max_iter=2000)",
          fc="#e2efe3", ec="#3a7a4a", fontsize=8)
    _arrow(ax, 7.9, 5.0, 7.9, 4.9)
    _arrow(ax, 7.9, 4.2, 7.9, 4.1)

    # Stage 4: 5-fold CV
    _arrow(ax, 7.9, 3.4, 7.9, 2.9)
    _bbox(ax, 6.1, 2.0, 3.6, 0.9,
          "StratifiedKFold(n_splits=5, shuffle=True, random_state=0)\n"
          "score: accuracy on held-out fold",
          fc="#e8eef7", ec="#33486b", fontsize=8)

    # Stage 5: per-layer accuracy curve
    _arrow(ax, 7.9, 2.0, 7.9, 1.5)

    # inline a small accuracy-curve sparkline
    sparkline_ax = fig.add_axes([0.62, 0.07, 0.34, 0.13])
    layers = np.arange(29)
    # synthetic accuracy curve roughly matching the real one for illustration
    acc = 0.7 + 0.18 * np.exp(-((layers - 20) ** 2) / 60)
    sparkline_ax.plot(layers, acc, color="#33486b", lw=1.5)
    sparkline_ax.axhline(0.638, color="#888", ls=":", lw=1)
    sparkline_ax.set_xlabel("layer", fontsize=7)
    sparkline_ax.set_ylabel("CV acc", fontsize=7)
    sparkline_ax.set_xlim(0, 28); sparkline_ax.set_ylim(0.5, 1.0)
    sparkline_ax.tick_params(labelsize=6)
    sparkline_ax.set_title("per-layer CV accuracy", fontsize=8, pad=2)

    # left side: probe targets
    _bbox(ax, 0.3, 2.5, 2.8, 1.6,
          "Probe targets (binary):\n"
          " - correct         (all items)\n"
          " - cutoff           (all items)\n"
          " - refusal_vs_wrong   (subset)\n"
          " - correct_within_pre  (subset)",
          fc="#f3e6ef", ec="#6b3367", fontsize=8)
    _arrow(ax, 1.7, 2.5, 1.7, 1.5)
    _bbox(ax, 0.3, 0.8, 2.8, 0.6,
          "y in {0, 1}, one label per item",
          fc="#f3e6ef", ec="#6b3367", fontsize=8)
    _arrow(ax, 3.1, 1.1, 6.0, 1.1, color="#6b3367")
    ax.text(4.5, 1.25, "supervision", fontsize=7, color="#6b3367",
            style="italic", ha="center")

    plt.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def main():
    FIGURES_DIR.mkdir(exist_ok=True)
    figure_qwen_architecture(FIGURES_DIR / "08_qwen_architecture.png")
    figure_probe_pipeline(FIGURES_DIR / "09_probe_pipeline.png")
    print("Wrote figures/08_qwen_architecture.png and figures/09_probe_pipeline.png")


if __name__ == "__main__":
    main()
