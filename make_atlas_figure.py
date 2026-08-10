"""Build the v1.2 Confabulation Atlas figure (supervised projection).

Two orthogonalized probe hyperplanes at layer 23, geometric framing:

  X-axis = signed perpendicular distance from the *correctness hyperplane*.
           The hyperplane is the decision boundary of a logistic-regression probe
           trained on PCA(16) features of the layer-23 hidden state, with target
           `correct in {True, False}` over all n=784 items.
           Right of the dashed line = correctness side.

  Y-axis = signed perpendicular distance from the *refusal-vs-correct hyperplane*,
           orthogonalized against the correctness direction.
           Trained as a binary classifier on the refusal-or-correct subset only
           (n=366 = 130 refusal + 236 correct), with target `judge_label ==
           "refusal"`. The hyperplane is the direction that maximally separates
           refusals from correct answers in hidden-state space; we then evaluate
           the projection on all 784 points (wrong items fall in between by
           construction). Top of the dashed line = refusal side.

Both axis labels include the probe's 5-fold cross-validated accuracy at layer 23
(the within-pre-cutoff peak), so the figure quotes the hyperplane quality.

The two axes are not arbitrary projections: each is the actual direction the
probe uses to discriminate. Whatever separation is visible in the figure is the
separation the probe sees, up to the small noise from orthogonalizing Y.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import ACTIVATIONS_DIR, FIGURES_DIR, RESPONSES_DIR, SUMMARY_PATH, set_seeds

# Load correctness peak layer from summary if it exists, else default to 18
ATLAS_LAYER = 18
if SUMMARY_PATH.exists():
    try:
        with open(SUMMARY_PATH) as f:
            _summary = json.load(f)
        ATLAS_LAYER = _summary["probes"]["correct"]["peak_layer"]
    except Exception:
        pass

PCA_N = 16


def load_all():
    responses = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        with open(f) as fp:
            r = json.load(fp)
        act = torch.load(ACTIVATIONS_DIR / f"{r['question_id']}.pt", weights_only=False)
        r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
        responses.append(r)
    return responses


def _cv_accuracy(X, y):
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=PCA_N)),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    return cross_val_score(pipe, X, y, cv=cv, scoring="accuracy").mean()


def fit_two_hyperplanes(X, y_correct, y_judge):
    """Returns (axis_x, axis_y, intercept_x, intercept_y, acc_x, acc_y)."""
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    pca = PCA(n_components=PCA_N).fit(Xs)
    Xp = pca.transform(Xs)  # (n, 16)

    # X-axis: signed distance from correctness hyperplane.
    lr_x = LogisticRegression(max_iter=2000, C=1.0).fit(Xp, y_correct)
    w_x = lr_x.coef_[0]
    w_x_unit = w_x / np.linalg.norm(w_x)
    axis_x = Xp @ w_x_unit
    intercept_x = -lr_x.intercept_[0] / np.linalg.norm(w_x)

    # Y-axis: refusal-vs-correct hyperplane, fit on the subset of refusal+correct
    # items, then evaluated on all points (wrong items will fall in between).
    sub_mask = (y_judge == "refusal") | (y_judge == "correct")
    Xp_sub = Xp[sub_mask]
    y_sub = (y_judge[sub_mask] == "refusal").astype(int)
    lr_y = LogisticRegression(max_iter=2000, C=1.0).fit(Xp_sub, y_sub)
    w_y_raw = lr_y.coef_[0]
    w_y_perp = w_y_raw - (w_y_raw @ w_x_unit) * w_x_unit
    w_y_unit = w_y_perp / np.linalg.norm(w_y_perp)
    axis_y = Xp @ w_y_unit
    # Sign convention: refusals at TOP (positive Y).
    y_refusal = (y_judge == "refusal").astype(int)
    if axis_y[y_refusal == 1].mean() < axis_y[y_refusal == 0].mean():
        w_y_unit = -w_y_unit
        axis_y = -axis_y
    # Decision-boundary threshold on the orthogonalized Y axis: choose the
    # signed-distance value that maximizes balanced accuracy of (axis_y > thr)
    # as a refusal classifier. This places the horizontal dashed line at the
    # right visual cut between refusal and non-refusal in this projection.
    candidates = np.linspace(axis_y.min(), axis_y.max(), 200)
    best_thr, best_ba = 0.0, -1.0
    for thr in candidates:
        pred = (axis_y > thr).astype(int)
        # balanced accuracy: 0.5 * (TPR + TNR)
        tp = ((pred == 1) & (y_refusal == 1)).sum()
        fn = ((pred == 0) & (y_refusal == 1)).sum()
        tn = ((pred == 0) & (y_refusal == 0)).sum()
        fp = ((pred == 1) & (y_refusal == 0)).sum()
        tpr = tp / max(tp + fn, 1)
        tnr = tn / max(tn + fp, 1)
        ba = 0.5 * (tpr + tnr)
        if ba > best_ba:
            best_ba, best_thr = ba, thr
    intercept_y = float(best_thr)
    cos_theta = abs(w_y_raw @ w_x_unit) / np.linalg.norm(w_y_raw)
    angle_deg = float(np.degrees(np.arccos(np.clip(cos_theta, 0, 1))))
    print(f"  angle between refusal-vs-correct and correctness directions: "
          f"{angle_deg:.1f} deg "
          f"(90 deg would mean fully orthogonal)")

    # CV accuracies for axis labels:
    #   X = correctness probe (all items)
    #   Y = refusal-vs-correct probe (refusal+correct subset)
    acc_x = _cv_accuracy(X, y_correct)
    acc_y = _cv_accuracy(X[sub_mask], y_sub)
    return axis_x, axis_y, intercept_x, intercept_y, acc_x, acc_y, angle_deg


def _scatter(ax, X2, mask, color, marker, label, alpha=0.85, s=26, edge="black"):
    ax.scatter(X2[mask, 0], X2[mask, 1], s=s, c=color, marker=marker,
               edgecolor=edge, linewidths=0.3, alpha=alpha, label=label)


def main():
    set_seeds()
    FIGURES_DIR.mkdir(exist_ok=True)
    responses = load_all()
    print(f"Loaded {len(responses)} responses")

    X = np.stack([r["last_prompt_hidden"][ATLAS_LAYER] for r in responses])
    y_correct = np.array([r["correct"] for r in responses], dtype=int)
    y_refusal = np.array([r["judge_label"] == "refusal" for r in responses], dtype=int)
    y_judge = np.array([r["judge_label"] for r in responses])
    y_cat = np.array([r.get("category") or "unknown" for r in responses])
    y_dom = np.array([r["domain"] for r in responses])
    lp = np.array([r["mean_logprob"] for r in responses])

    print(f"Fitting two hyperplanes at layer {ATLAS_LAYER} (PCA({PCA_N})):")
    ax_x, ax_y, int_x, int_y, acc_x, acc_y, angle_deg = fit_two_hyperplanes(
        X, y_correct, y_judge)
    X2 = np.column_stack([ax_x, ax_y])
    sub_n = (y_judge == "refusal").sum() + (y_judge == "correct").sum()
    print(f"  correctness hyperplane (n={len(responses)}):       5-fold CV acc = {acc_x:.3f}")
    print(f"  refusal-vs-correct hyperplane (n={sub_n}): 5-fold CV acc = {acc_y:.3f}")
    print(f"  hyperplane angle (after orthogonalization in plot): 90.0 deg "
          f"(raw angle in 16-d PCA space was {angle_deg:.1f} deg)")
    print(f"  X range [{ax_x.min():.2f}, {ax_x.max():.2f}], "
          f"Y range [{ax_y.min():.2f}, {ax_y.max():.2f}]")

    lp_q = np.array([
        "q1 (lowest conf.)" if v <= np.quantile(lp, 0.25)
        else "q2" if v <= np.quantile(lp, 0.5)
        else "q3" if v <= np.quantile(lp, 0.75)
        else "q4 (highest conf.)"
        for v in lp
    ])

    fig, axes = plt.subplots(2, 3, figsize=(15.5, 9.5))
    axes = axes.flatten()
    fig.suptitle(
        f"Confabulation Atlas: signed distances from two probe hyperplanes "
        f"in Qwen3-1.7B's layer-{ATLAS_LAYER} hidden-state space  (n={len(responses)})",
        fontsize=12.5, y=0.995)

    bool_correct = y_correct.astype(bool)
    bool_refusal = y_refusal.astype(bool)

    xlabel = (f"signed distance from correctness hyperplane "
              f"(5-fold CV acc {acc_x:.1%})")
    ylabel = (f"signed distance from refusal-vs-correct hyperplane "
              f"(5-fold CV acc {acc_y:.1%} on n={sub_n} subset)")

    def draw_boundaries(ax):
        ax.axvline(int_x, color="#444", linestyle="--", linewidth=1, alpha=0.5)
        ax.axhline(int_y, color="#444", linestyle="--", linewidth=1, alpha=0.5)

    # Panel (a): correctness
    ax = axes[0]
    draw_boundaries(ax)
    _scatter(ax, X2, ~bool_correct, "#d62728", "X", "incorrect", alpha=0.75)
    _scatter(ax, X2, bool_correct, "#2ca02c", "o", "correct", alpha=0.85)
    ax.set_title("(a) by correctness", fontsize=11)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.legend(fontsize=8, loc="best"); ax.grid(True, alpha=0.2)

    # Panel (b): judge label
    ax = axes[1]
    draw_boundaries(ax)
    palette = {"correct": "#2ca02c", "refusal": "#1f77b4", "wrong": "#d62728"}
    markers = {"correct": "o", "refusal": "s", "wrong": "X"}
    for lbl, color in palette.items():
        mask = y_judge == lbl
        _scatter(ax, X2, mask, color, markers[lbl],
                 f"{lbl} (n={mask.sum()})", alpha=0.8)
    ax.set_title("(b) by judge label", fontsize=11)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.legend(fontsize=8, loc="best"); ax.grid(True, alpha=0.2)

    # Panel (c): category
    ax = axes[2]
    draw_boundaries(ax)
    palette = {"well_known": "#2ca02c", "obscure": "#ff7f0e", "post_cutoff": "#9467bd"}
    markers = {"well_known": "o", "obscure": "D", "post_cutoff": "s"}
    for cat, color in palette.items():
        mask = y_cat == cat
        _scatter(ax, X2, mask, color, markers[cat],
                 f"{cat} (n={mask.sum()})", alpha=0.8)
    ax.set_title("(c) by category", fontsize=11)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.legend(fontsize=8, loc="best"); ax.grid(True, alpha=0.2)

    # Panel (d): domain
    ax = axes[3]
    draw_boundaries(ax)
    palette = {"science": "#1f77b4", "history": "#2ca02c",
               "culture": "#9467bd", "cinema": "#e377c2"}
    for dom, color in palette.items():
        mask = y_dom == dom
        _scatter(ax, X2, mask, color, "o",
                 f"{dom} (n={mask.sum()})", alpha=0.8)
    ax.set_title("(d) by domain", fontsize=11)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.legend(fontsize=8, loc="best"); ax.grid(True, alpha=0.2)

    # Panel (e): mean log-prob quartile
    ax = axes[4]
    draw_boundaries(ax)
    palette = {
        "q1 (lowest conf.)": "#d62728",
        "q2": "#ff9933",
        "q3": "#ffd933",
        "q4 (highest conf.)": "#2ca02c",
    }
    for q, color in palette.items():
        mask = lp_q == q
        _scatter(ax, X2, mask, color, "o",
                 f"{q} (n={mask.sum()})", alpha=0.8)
    ax.set_title("(e) by mean-logprob quartile", fontsize=11)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.legend(fontsize=8, loc="best"); ax.grid(True, alpha=0.2)

    # Panel (f): UNSUPERVISED PCA(2) control on the same hidden states.
    # Shows what structure (if any) is recoverable in the raw geometry without
    # using any labels — sets a baseline for what the supervised projection
    # (panels a-e) contributes on top of generic variance directions.
    ax = axes[5]
    Xs_for_pca = StandardScaler().fit_transform(X)
    pca2 = PCA(n_components=2).fit(Xs_for_pca)
    X2u = pca2.transform(Xs_for_pca)
    ev = pca2.explained_variance_ratio_
    palette_j = {"correct": "#2ca02c", "refusal": "#1f77b4", "wrong": "#d62728"}
    markers_j = {"correct": "o", "refusal": "s", "wrong": "X"}
    for lbl, color in palette_j.items():
        mask = y_judge == lbl
        ax.scatter(X2u[mask, 0], X2u[mask, 1], s=26, c=color, marker=markers_j[lbl],
                   edgecolor="black", linewidths=0.3, alpha=0.8,
                   label=f"{lbl} (n={mask.sum()})")
    ax.set_title("(f) unsupervised PCA(2), same layer", fontsize=11)
    ax.set_xlabel(f"PC1 ({ev[0]:.1%} of variance)", fontsize=8)
    ax.set_ylabel(f"PC2 ({ev[1]:.1%} of variance)", fontsize=8)
    ax.legend(fontsize=8, loc="best"); ax.grid(True, alpha=0.2)

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    out = FIGURES_DIR / f"00_atlas_layer{ATLAS_LAYER}.png"
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
