"""Three recoveries of the Qwen3-1.7B refusal direction, in the 3-D span they define.

Companion to the Section 6.1 geometry figures. The refusal direction is recovered
three independent ways: (1) the linear probe direction, (2) SAE feature 2191 (the
"refusal opener" decoder column), and (3) the optimized refusal direction
(Section 6.3.1). Each unit direction lives in the 3-D subspace they span, so the
Gram-Schmidt basis [e1, e2, e3] preserves the true pairwise angles exactly. The
layer-28 refusal+wrong hidden states are projected into the same subspace.

Outputs:
  figures/qwen3_1_7b/refusal_directions_3d.png   (static, good viewing angle)
  figures/qwen3_1_7b/refusal_directions_3d.gif   (rotating 360-degree azimuth sweep)

Run from the repo root: python -m plots.figure_refusal_directions_3d
"""
import gc
import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Line3DCollection  # noqa: F401 (registers 3d)
from sae_lens import SAE

import analysis.make_probe_direction_atlas as atlas
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, set_seeds

# Colors, consistent with the existing figures.
C_REFUSAL = "#1f77b4"
C_WRONG = "#d62728"
C_PROBE = "#9467bd"
C_SAE = "#ff7f0e"
C_OPT = "#2ca02c"
C_REFUSAL_STAR = "#0b3d66"
C_WRONG_STAR = "#7f1d1d"


def main():
    set_seeds()

    # --- Direction 1: linear probe direction (raw 2048-d) ---------------------
    items = atlas.load_subset({"refusal", "wrong"})
    d = atlas.recover_direction(items, "refusal")
    w = d["direction_raw"]
    u_probe = w / np.linalg.norm(w)

    # --- Direction 2: SAE feature 2191 decoder column -------------------------
    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    d_2191 = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID].astype(np.float64)
    # Free the SAE immediately; we only need the one decoder column (16 GB M1).
    del sae
    gc.collect()
    d_2191 = d_2191 / np.linalg.norm(d_2191)

    # --- Direction 3: optimized refusal direction -----------------------------
    u_opt = np.load(FIGURES_DIR / "optimized_refusal_direction.npy").astype(np.float64)
    u_opt = u_opt / np.linalg.norm(u_opt)

    u_probe = u_probe.astype(np.float64)

    # --- Pairwise cosines / angles (geometry-independent, full 2048-d) --------
    cos_probe_2191 = float(np.dot(u_probe, d_2191))
    cos_2191_opt = float(np.dot(d_2191, u_opt))
    cos_probe_opt = float(np.dot(u_probe, u_opt))
    ang_probe_2191 = float(np.degrees(np.arccos(np.clip(cos_probe_2191, -1, 1))))
    ang_2191_opt = float(np.degrees(np.arccos(np.clip(cos_2191_opt, -1, 1))))
    ang_probe_opt = float(np.degrees(np.arccos(np.clip(cos_probe_opt, -1, 1))))

    print("pairwise cosines / angles (full 2048-d):")
    print(f"  probe . 2191      cos = {cos_probe_2191:.4f}  angle = {ang_probe_2191:.1f} deg")
    print(f"  2191  . optimized cos = {cos_2191_opt:.4f}  angle = {ang_2191_opt:.1f} deg")
    print(f"  probe . optimized cos = {cos_probe_opt:.4f}  angle = {ang_probe_opt:.1f} deg")

    # Sanity gate against the paper's reported values.
    if not (abs(cos_probe_2191 - 0.16) < 0.05):
        raise SystemExit(
            f"STOP: cos(probe, 2191) = {cos_probe_2191:.4f}, expected ~0.16")
    if not (abs(cos_2191_opt - 0.64) < 0.06):
        raise SystemExit(
            f"STOP: cos(2191, optimized) = {cos_2191_opt:.4f}, expected ~0.64")

    # --- Orthonormal basis by Gram-Schmidt on [u_probe, d_2191, u_opt] --------
    e1 = u_probe
    v2 = d_2191 - np.dot(d_2191, e1) * e1
    e2 = v2 / np.linalg.norm(v2)
    v3 = u_opt - np.dot(u_opt, e1) * e1 - np.dot(u_opt, e2) * e2
    e3 = v3 / np.linalg.norm(v3)
    B = np.stack([e1, e2, e3])  # (3, 2048)

    # In-basis coordinates of the three unit directions (exact; angles preserved)
    p_probe = B @ u_probe
    p_2191 = B @ d_2191
    p_opt = B @ u_opt

    # --- Point cloud projected into the same 3-D subspace ---------------------
    H = np.stack([r["h"] for r in items]).astype(np.float64)
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in items])
    Q = (H - H.mean(axis=0)) @ B.T  # (n, 3)

    Qr, Qw = Q[y == 1], Q[y == 0]
    cen_r, cen_w = Qr.mean(axis=0), Qw.mean(axis=0)
    span = float(np.linalg.norm(cen_r - cen_w))
    L = 0.9 * span  # arrow length: clearly visible against the cloud spread

    tips = {
        "probe": L * p_probe,
        "2191": L * p_2191,
        "opt": L * p_opt,
    }

    n_r, n_w = int((y == 1).sum()), int((y == 0).sum())

    # --- Figure ---------------------------------------------------------------
    fig = plt.figure(figsize=(7.4, 7.4), dpi=130, facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("white")

    # Wrong: many, small, faint. Refusal: fewer, larger, bolder, so the small
    # refusal cluster stays legible instead of being swamped by the wrongs.
    h_wrong = ax.scatter(*Qw.T, s=8, c=C_WRONG, alpha=0.28, depthshade=True,
                         label=f"wrong (n={n_w})")
    h_ref = ax.scatter(*Qr.T, s=17, c=C_REFUSAL, alpha=0.70, depthshade=True,
                       label=f"refusal (n={n_r})")

    # Class centroids as large stars.
    ax.scatter(*cen_w, marker="*", s=360, c=C_WRONG_STAR, edgecolors="white",
               linewidths=0.7, depthshade=False, zorder=6)
    ax.scatter(*cen_r, marker="*", s=360, c=C_REFUSAL_STAR, edgecolors="white",
               linewidths=0.7, depthshade=False, zorder=6)

    # Three unit-direction arrows from the data mean. Labelled via the legend
    # (not inline text) so nothing overlaps the point cloud.
    arrows = [
        (tips["probe"], C_PROBE, "probe direction"),
        (tips["2191"], C_SAE, "SAE feature 2191 (opener)"),
        (tips["opt"], C_OPT, "optimized direction"),
    ]
    for tip, color, _label in arrows:
        ax.quiver(0, 0, 0, tip[0], tip[1], tip[2], color=color, lw=3.0,
                  arrow_length_ratio=0.16, zorder=8)

    # Frame centered on the two centroids' midpoint, sized to the arrows and the
    # cluster cores (92nd percentile), so the intrinsically thin cloud fills the
    # view instead of being pushed into a corner; a few extreme wrong outliers
    # clip. Equal box aspect keeps the projected angles reading true.
    ctr = 0.5 * (cen_r + cen_w)
    core = float(np.percentile(np.abs(Q - ctr), 92, axis=0).max())
    tip_ext = float(np.max(np.abs(np.array(list(tips.values())) - ctr)))
    rng = max(core, tip_ext) * 1.10
    ax.set_xlim(ctr[0] - rng, ctr[0] + rng)
    ax.set_ylim(ctr[1] - rng, ctr[1] + rng)
    ax.set_zlim(ctr[2] - rng, ctr[2] + rng)
    ax.set_box_aspect((1, 1, 1))

    # Clean, light 3-D axes.
    ax.set_xlabel("e1 (probe axis)", fontsize=9, labelpad=2)
    ax.set_ylabel("e2 (2191 residual)", fontsize=9, labelpad=2)
    ax.set_zlabel("e3 (optimized residual)", fontsize=9, labelpad=2)
    ax.tick_params(labelsize=7, pad=0)
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.pane.set_facecolor((1, 1, 1, 1))
        pane.pane.set_edgecolor((0.85, 0.85, 0.85, 1))
        pane.pane.set_alpha(1.0)
    ax.grid(True, color="#e6e6e6", linewidth=0.5)

    ax.set_title("Three recoveries of the Qwen3-1.7B refusal direction",
                 fontsize=12, pad=6)
    arrow_handles = [Line2D([0], [0], color=c, lw=3.0, label=l)
                     for _, c, l in arrows]
    ax.legend(handles=[h_wrong, h_ref, *arrow_handles], loc="upper left",
              fontsize=8.5, framealpha=0.92)

    # Angle box.
    box = (f"pairwise angles\n"
           f"probe – 2191: {ang_probe_2191:.0f}°\n"
           f"2191 – optimized: {ang_2191_opt:.0f}°\n"
           f"probe – optimized: {ang_probe_opt:.0f}°")
    ax.text2D(0.02, 0.02, box, transform=ax.transAxes, fontsize=8.5,
              color="#333333", va="bottom", ha="left",
              bbox=dict(boxstyle="round", fc="white", ec="#cccccc", alpha=0.9))

    elev = 16
    ax.view_init(elev=elev, azim=-72)

    png_path = FIGURES_DIR / "refusal_directions_3d.png"
    fig.savefig(png_path, bbox_inches="tight", facecolor="white")
    print(f"Wrote {png_path}")

    # --- Rotating 360-degree GIF ---------------------------------------------
    # A full azimuth turn with a gentle two-beat elevation bob, so the thin
    # cloud tips toward and away from the camera instead of doing a flat spin.
    # Integer azimuth turn (1) and elevation periods (2) keep the loop seamless.
    n_frames = 72
    az0, elev0, elev_amp = -72.0, 22.0, 12.0

    def update(i):
        frac = i / n_frames
        ax.view_init(elev=elev0 + elev_amp * np.sin(2 * np.pi * 2 * frac),
                     azim=az0 + 360.0 * frac)
        return []

    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000 / 24,
                         blit=False)
    gif_path = FIGURES_DIR / "refusal_directions_3d.gif"
    anim.save(gif_path, writer=PillowWriter(fps=24), dpi=100,
              savefig_kwargs={"facecolor": "white"})
    size_mb = gif_path.stat().st_size / 1e6
    print(f"Wrote {gif_path} ({size_mb:.2f} MB)")

    plt.close(fig)

    print(json.dumps({
        "cos_probe_2191": round(cos_probe_2191, 4),
        "angle_probe_2191_deg": round(ang_probe_2191, 1),
        "cos_2191_opt": round(cos_2191_opt, 4),
        "angle_2191_opt_deg": round(ang_2191_opt, 1),
        "cos_probe_opt": round(cos_probe_opt, 4),
        "angle_probe_opt_deg": round(ang_probe_opt, 1),
        "png": str(png_path),
        "gif": str(gif_path),
        "gif_mb": round(size_mb, 2),
    }))


if __name__ == "__main__":
    main()
