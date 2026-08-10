"""Merge figures 8 (Qwen3 architecture) and 9 (probe pipeline) into one
two-panel methods figure, stacked **vertically** so each panel renders at
full page width.

Outputs: figures/methods_arch_and_pipeline.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

ARCH = "figures/08_qwen_architecture.png"
PIPE = "figures/09_probe_pipeline.png"
OUT = Path("figures/methods_arch_and_pipeline.png")

arch = mpimg.imread(ARCH)
pipe = mpimg.imread(PIPE)

# Vertical stack: each panel takes the full text width. Height per panel is
# proportional to source aspect ratio.
TEXT_WIDTH_IN = 6.5  # rendered width per panel (slightly > page text width
                     # so PDF includegraphics can scale down without aliasing)
arch_h = TEXT_WIDTH_IN * arch.shape[0] / arch.shape[1]
pipe_h = TEXT_WIDTH_IN * pipe.shape[0] / pipe.shape[1]

fig = plt.figure(figsize=(TEXT_WIDTH_IN, arch_h + pipe_h + 0.6), dpi=180)
gs = fig.add_gridspec(2, 1, height_ratios=[arch_h, pipe_h],
                      hspace=0.08, top=0.97, bottom=0.02, left=0.02, right=0.98)

ax_top = fig.add_subplot(gs[0])
ax_top.imshow(arch); ax_top.axis("off")
ax_top.set_title("(a) Qwen3-1.7B with last-prompt-token hidden-state pickoff",
                 fontsize=11, pad=2, loc="left")

ax_bot = fig.add_subplot(gs[1])
ax_bot.imshow(pipe); ax_bot.axis("off")
ax_bot.set_title("(b) Per-layer linear-probe pipeline",
                 fontsize=11, pad=2, loc="left")

plt.savefig(OUT, bbox_inches="tight", facecolor="white")
print(f"Wrote {OUT}")
