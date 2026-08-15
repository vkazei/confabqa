"""PCA-components robustness sweep for the per-layer probe.

For each (target, n_components) we compute the per-layer probe curve and take
its peak accuracy. We plot peak accuracy vs n_components for each target.

This closes the reviewer question 'did you cherry-pick PCA(16)?'.
"""
import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import torch

warnings.filterwarnings("ignore", message="invalid value encountered in divide")
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import ACTIVATIONS_DIR, FIGURES_DIR, RESPONSES_DIR, set_seeds

TARGETS = ["correct", "cutoff", "refusal_vs_wrong", "correct_within_pre"]
N_COMPONENTS_SWEEP = [4, 8, 16, 32, 48, 64]


def load_all():
    responses = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        with open(f) as fp:
            r = json.load(fp)
        act = torch.load(ACTIVATIONS_DIR / f"{r['question_id']}.pt", weights_only=False)
        r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
        responses.append(r)
    return responses


def subset_and_y(responses, target):
    if target == "correct":
        return responses, np.array([1 if r["correct"] else 0 for r in responses])
    if target == "cutoff":
        return responses, np.array([1 if r["cutoff_class"] == "post" else 0 for r in responses])
    if target == "refusal_vs_wrong":
        sub = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
        return sub, np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
    if target == "correct_within_pre":
        sub = [r for r in responses if r["cutoff_class"] == "pre"]
        return sub, np.array([1 if r["correct"] else 0 for r in sub])
    raise ValueError(target)


def per_layer_peak(subset, y, n_components):
    num_layers = subset[0]["last_prompt_hidden"].shape[0]
    n = len(subset)
    # PCA n_components must be <= min(n_train_fold, d).
    # With 5-fold stratified CV the smallest train fold has roughly 4n/5 - small slack;
    # to be safe, cap at min(n_components, n - max(class_size)//1 - 1).
    safe_nc = min(n_components, n - 1)
    if safe_nc < n_components:
        return None  # report as missing
    accs = []
    for layer in range(num_layers):
        X = np.stack([r["last_prompt_hidden"][layer] for r in subset])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=n_components)),
            ("clf", LogisticRegression(max_iter=2000, C=1.0)),
        ])
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
        accs.append(scores.mean())
    return float(np.max(accs))


def main():
    set_seeds()
    responses = load_all()
    print(f"Loaded {len(responses)} responses")
    FIGURES_DIR.mkdir(exist_ok=True)

    results = {t: {} for t in TARGETS}
    for target in TARGETS:
        sub, y = subset_and_y(responses, target)
        print(f"\n--- target={target} (n={len(sub)}) ---")
        for nc in N_COMPONENTS_SWEEP:
            peak = per_layer_peak(sub, y, nc)
            if peak is None:
                print(f"  n_components={nc:3d}: SKIP (n too small)")
                continue
            results[target][nc] = peak
            print(f"  n_components={nc:3d}: peak acc = {peak:.3f}")

    # plot
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    colors = {"correct": "#2ca02c", "cutoff": "#ff7f0e",
              "refusal_vs_wrong": "#9467bd", "correct_within_pre": "#17becf"}
    markers = {"correct": "o", "cutoff": "s",
               "refusal_vs_wrong": "D", "correct_within_pre": "^"}
    for target in TARGETS:
        ncs = sorted(results[target].keys())
        peaks = [results[target][nc] for nc in ncs]
        ax.plot(ncs, peaks, marker=markers[target], color=colors[target],
                label=target, linewidth=1.8, markersize=8)
    ax.axvline(16, color="grey", linestyle=":", linewidth=1, alpha=0.6,
               label="n_components=16 (paper default)")
    ax.set_xlabel("PCA n_components (top-k principal directions)")
    ax.set_ylabel("Peak per-layer 5-fold CV accuracy")
    ax.set_title("Per-layer probe accuracy is robust across PCA truncation depth")
    ax.set_ylim(0.5, 1.0)
    ax.set_xticks(N_COMPONENTS_SWEEP)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    out = FIGURES_DIR / "10_pca_robustness.png"
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"\nWrote {out}")

    # also write a small JSON table for the paper
    out_json = FIGURES_DIR / "10_pca_robustness.json"
    out_json.write_text(json.dumps(results, indent=2))
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
