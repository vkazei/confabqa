import json
import re
import statistics
import warnings
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import torch

warnings.filterwarnings("ignore", message="invalid value encountered in divide")
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (balanced_accuracy_score, confusion_matrix,
                             recall_score, roc_auc_score)
from sklearn.model_selection import (StratifiedKFold, cross_val_predict,
                                     cross_val_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import ACTIVATIONS_DIR, FIGURES_DIR, RESPONSES_DIR, SUMMARY_PATH, set_seeds


def load_all():
    responses = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        with open(f) as fp:
            r = json.load(fp)
        act = torch.load(ACTIVATIONS_DIR / f"{r['question_id']}.pt", weights_only=False)
        r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
        r["first_gen_hidden"] = (
            act["first_gen_hidden"].numpy() if act["first_gen_hidden"] is not None else None
        )
        if "judge_label" not in r:
            r["judge_label"] = "correct" if r.get("correct") else "wrong"
        responses.append(r)
    return responses


def print_summary(responses):
    by_class = defaultdict(list)
    by_domain = defaultdict(list)
    by_cd = defaultdict(list)
    for r in responses:
        by_class[r["cutoff_class"]].append(r)
        by_domain[r["domain"]].append(r)
        by_cd[(r["cutoff_class"], r["domain"])].append(r)

    def stat(items):
        n = len(items)
        if n == 0:
            return 0, 0, 0.0, 0.0
        c = sum(1 for r in items if r["correct"])
        lp = statistics.mean(r["mean_logprob"] for r in items)
        ent = statistics.mean(r["mean_entropy"] for r in items)
        return n, c, lp, ent

    print(f"\n=== Overall ({len(responses)} questions) ===")
    n, c, lp, ent = stat(responses)
    print(f"  correct={c}/{n} ({c/n:.1%})  mean_logprob={lp:.3f}  mean_entropy={ent:.3f}")

    print(f"\n=== By cutoff class ===")
    for cls in ["pre", "post"]:
        n, c, lp, ent = stat(by_class[cls])
        acc_str = f"({c/n:5.1%})" if n > 0 else "(N/A)"
        print(f"  {cls:5s}  n={n:2d}  correct={c}/{n} {acc_str}  "
              f"mean_logprob={lp:+.3f}  mean_entropy={ent:.3f}")

    print(f"\n=== By domain ===")
    for dom in sorted(by_domain):
        n, c, lp, ent = stat(by_domain[dom])
        print(f"  {dom:8s}  n={n:2d}  correct={c}/{n} ({c/n:5.1%})  "
              f"mean_logprob={lp:+.3f}")

    print(f"\n=== By domain x cutoff ===")
    print(f"  {'domain':8s}  {'pre':>12s}  {'post':>12s}")
    for dom in sorted(by_domain):
        line = f"  {dom:8s}"
        for cls in ["pre", "post"]:
            items = by_cd[(cls, dom)]
            c = sum(1 for r in items if r["correct"])
            acc_str = f"({c/len(items):5.1%})" if len(items) > 0 else "(N/A)"
            line += f"  {c}/{len(items):2d} {acc_str}"
        print(line)

    if any(r.get("category") for r in responses):
        print(f"\n=== By category (v1) ===")
        by_cat = defaultdict(list)
        for r in responses:
            if r.get("category"):
                by_cat[r["category"]].append(r)
        for cat in ["well_known", "obscure", "post_cutoff"]:
            items = by_cat.get(cat, [])
            if not items:
                continue
            n = len(items)
            c = sum(1 for r in items if r["correct"])
            lp = statistics.mean(r["mean_logprob"] for r in items)
            print(f"  {cat:12s}  n={n:2d}  correct={c}/{n} ({c/n:5.1%})  "
                  f"mean_logprob={lp:+.3f}")

    print(f"\n=== Confidence split by correctness ===")
    for label, items in [("Correct  ", [r for r in responses if r["correct"]]),
                        ("Incorrect", [r for r in responses if not r["correct"]])]:
        if not items:
            continue
        n = len(items)
        lp = statistics.mean(r["mean_logprob"] for r in items)
        ent = statistics.mean(r["mean_entropy"] for r in items)
        first_lp = statistics.mean(r["token_logprobs"][0] for r in items if r["token_logprobs"])
        print(f"  {label}  n={n:2d}  mean_logprob={lp:+.3f}  "
              f"mean_entropy={ent:.3f}  first_token_logprob={first_lp:+.3f}")

    print(f"\n=== By judge label ===")
    label_counts = defaultdict(int)
    for r in responses:
        label_counts[r["judge_label"]] += 1
    for lbl in ["correct", "refusal", "wrong"]:
        n = label_counts[lbl]
        if n:
            print(f"  {lbl:8s} n={n} ({n/len(responses):5.1%})")

    print(f"\n=== Judge label x cutoff ===")
    print(f"  {'cutoff':6s} {'correct':>10s} {'refusal':>10s} {'wrong':>10s}")
    for cls in ["pre", "post"]:
        subset = [r for r in responses if r["cutoff_class"] == cls]
        cnts = defaultdict(int)
        for r in subset:
            cnts[r["judge_label"]] += 1
        line = f"  {cls:6s}"
        for lbl in ["correct", "refusal", "wrong"]:
            n = cnts[lbl]
            line += f"  {n:2d} ({n/len(subset):5.1%})" if subset else f"   0 (  0.0%)"
        print(line)

    print(f"\n=== Top 5 confident confabulations (judge_label=wrong with highest mean_logprob) ===")
    wrong = sorted(
        [r for r in responses if r["judge_label"] == "wrong"],
        key=lambda r: -r["mean_logprob"],
    )[:5]
    for r in wrong:
        print(f"  [{r['cutoff_class']}/{r['domain']}] {r['question_id']}: lp={r['mean_logprob']:+.3f}")
        print(f"    Q: {r['question']}")
        print(f"    Expected: {r['expected_answer']}")
        print(f"    Got: {r['answer_text'][:120]}")

    print(f"\n=== Top 5 confident refusals (judge_label=refusal with highest mean_logprob) ===")
    refusals = sorted(
        [r for r in responses if r["judge_label"] == "refusal"],
        key=lambda r: -r["mean_logprob"],
    )[:5]
    for r in refusals:
        print(f"  [{r['cutoff_class']}/{r['domain']}] {r['question_id']}: lp={r['mean_logprob']:+.3f}")
        print(f"    Q: {r['question']}")
        print(f"    Got: {r['answer_text'][:120]}")

    print(f"\n=== Top 5 uncertain-but-correct (correct with lowest mean_logprob) ===")
    right = sorted(
        [r for r in responses if r["correct"]],
        key=lambda r: r["mean_logprob"],
    )[:5]
    for r in right:
        print(f"  [{r['cutoff_class']}/{r['domain']}] {r['question_id']}: lp={r['mean_logprob']:+.3f}")
        print(f"    Q: {r['question']}")
        print(f"    Got: {r['answer_text'][:120]}")


def plot_logprob_histogram(responses, out_path):
    correct = [r["mean_logprob"] for r in responses if r["correct"]]
    wrong = [r["mean_logprob"] for r in responses if not r["correct"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    bins = np.linspace(min(correct + wrong), max(correct + wrong), 18)
    ax.hist(correct, bins=bins, alpha=0.7, color="#2ca02c", label=f"correct (n={len(correct)})")
    ax.hist(wrong, bins=bins, alpha=0.7, color="#d62728", label=f"incorrect (n={len(wrong)})")
    ax.axvline(np.mean(correct), color="#2ca02c", linestyle="--", alpha=0.8)
    ax.axvline(np.mean(wrong), color="#d62728", linestyle="--", alpha=0.8)
    ax.set_xlabel("mean token logprob")
    ax.set_ylabel("count")
    ax.set_title("Generation confidence by correctness")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_calibration_scatter(responses, out_path):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {"pre": "#1f77b4", "post": "#ff7f0e"}
    for cls in ["pre", "post"]:
        subset = [r for r in responses if r["cutoff_class"] == cls]
        for correct, marker, alpha in [(True, "o", 1.0), (False, "X", 0.85)]:
            items = [r for r in subset if r["correct"] == correct]
            xs = [r["mean_logprob"] for r in items]
            ys = [r["mean_entropy"] for r in items]
            label = f"{cls} {'correct' if correct else 'wrong'} (n={len(items)})"
            ax.scatter(xs, ys, marker=marker, s=90, color=colors[cls],
                       alpha=alpha, edgecolor="black" if correct else "none",
                       linewidths=0.7, label=label)
    ax.set_xlabel("mean token logprob (higher = more confident)")
    ax.set_ylabel("mean token entropy")
    ax.set_title("Calibration: confidence vs correctness by cutoff class")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_pca_layer(responses, layer_idx, out_path):
    X = np.stack([r["last_prompt_hidden"][layer_idx] for r in responses])
    y_correct = np.array([r["correct"] for r in responses])
    y_cutoff = np.array([r["cutoff_class"] for r in responses])
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    for label, marker, color in [(True, "o", "#2ca02c"), (False, "X", "#d62728")]:
        mask = y_correct == label
        axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1], marker=marker, s=80,
                        color=color, edgecolor="black", linewidths=0.5,
                        label=f"correct={label}")
    axes[0].set_title(f"Layer {layer_idx} hidden state PCA — by correctness")
    axes[0].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    axes[0].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    for cls, marker, color in [("pre", "o", "#1f77b4"), ("post", "s", "#ff7f0e")]:
        mask = y_cutoff == cls
        axes[1].scatter(X_pca[mask, 0], X_pca[mask, 1], marker=marker, s=80,
                        color=color, edgecolor="black", linewidths=0.5,
                        label=f"cutoff={cls}")
    axes[1].set_title(f"Layer {layer_idx} hidden state PCA — by cutoff class")
    axes[1].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    axes[1].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def per_layer_probe(responses, target):
    if target == "correct":
        y = np.array([1 if r["correct"] else 0 for r in responses])
    elif target == "cutoff":
        y = np.array([1 if r["cutoff_class"] == "post" else 0 for r in responses])
    elif target == "refusal_vs_wrong":
        responses = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
        y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in responses])
    elif target == "refusal_vs_wrong_within_post":
        responses = [r for r in responses
                     if r["judge_label"] in ("refusal", "wrong") and r["cutoff_class"] == "post"]
        y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in responses])
    elif target == "correct_within_pre":
        responses = [r for r in responses if r["cutoff_class"] == "pre"]
        y = np.array([1 if r["correct"] else 0 for r in responses])
    elif target == "correct_within_obscure":
        responses = [r for r in responses if r.get("category") == "obscure"]
        y = np.array([1 if r["correct"] else 0 for r in responses])
    else:
        raise ValueError(target)

    num_layers = responses[0]["last_prompt_hidden"].shape[0]
    accs = []
    stds = []
    for layer in range(num_layers):
        X = np.stack([r["last_prompt_hidden"][layer] for r in responses])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=min(16, len(responses) - 1))),
            ("clf", LogisticRegression(max_iter=2000, C=1.0)),
        ])
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
        accs.append(scores.mean())
        stds.append(scores.std())
    return np.array(accs), np.array(stds), len(responses)


def plot_per_layer_probe(responses, out_path):
    acc_correct, std_correct, n_correct_total = per_layer_probe(responses, "correct")
    acc_cutoff, std_cutoff, _ = per_layer_probe(responses, "cutoff")
    chance_correct = max(
        sum(1 for r in responses if r["correct"]) / len(responses),
        sum(1 for r in responses if not r["correct"]) / len(responses),
    )
    chance_cutoff = 0.5

    fig, ax = plt.subplots(figsize=(10, 5.5))
    layers = np.arange(len(acc_correct))
    ax.plot(layers, acc_correct, marker="o", color="#2ca02c", label=f"predict correctness (n={n_correct_total})")
    ax.fill_between(layers, acc_correct - std_correct, acc_correct + std_correct,
                    color="#2ca02c", alpha=0.15)
    ax.plot(layers, acc_cutoff, marker="s", color="#ff7f0e", label="predict pre/post cutoff")
    ax.fill_between(layers, acc_cutoff - std_cutoff, acc_cutoff + std_cutoff,
                    color="#ff7f0e", alpha=0.15)
    ax.axhline(chance_correct, color="#2ca02c", linestyle=":", alpha=0.5,
               label=f"correctness majority baseline ({chance_correct:.2f})")
    ax.axhline(chance_cutoff, color="#ff7f0e", linestyle=":", alpha=0.5,
               label=f"cutoff chance ({chance_cutoff:.2f})")
    ax.set_xlabel("Layer index (0 = embeddings, ..., 28 = last transformer block)")
    ax.set_ylabel("5-fold CV accuracy (band = ±1 std across folds)")
    ax.set_title("Per-layer linear probe on last-prompt-token hidden state\n"
                 "(StandardScaler + PCA(16) + LogReg)")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.0, 1.05)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)

    print(f"\n=== Per-layer probe ===")
    print(f"  Best layer for correctness: {acc_correct.argmax()} (acc={acc_correct.max():.3f} "
          f"+/- {std_correct[acc_correct.argmax()]:.3f}, baseline={chance_correct:.3f})")
    print(f"  Best layer for cutoff:      {acc_cutoff.argmax()} (acc={acc_cutoff.max():.3f} "
          f"+/- {std_cutoff[acc_cutoff.argmax()]:.3f}, baseline={chance_cutoff:.3f})")


def plot_correct_within_obscure_probe(responses, out_path):
    obs = [r for r in responses if r.get("category") == "obscure"]
    n_correct = sum(1 for r in obs if r["correct"])
    n_wrong = len(obs) - n_correct
    if n_correct < 5 or n_wrong < 5:
        print(f"\n=== Correct-within-obscure probe: SKIPPED "
              f"(n_correct={n_correct}, n_wrong={n_wrong}; need >=5 of each) ===")
        return

    accs, stds, n_total = per_layer_probe(responses, "correct_within_obscure")
    chance = max(n_correct, n_wrong) / len(obs)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    layers = np.arange(len(accs))
    ax.plot(layers, accs, marker="D", color="#bc8f00",
            label=f"predict correctness within OBSCURE pre-cutoff (n={n_total}: "
                  f"{n_correct} correct, {n_wrong} wrong)")
    ax.fill_between(layers, accs - stds, accs + stds, color="#bc8f00", alpha=0.15)
    ax.axhline(chance, color="#bc8f00", linestyle=":", alpha=0.5,
               label=f"obscure-cell majority baseline ({chance:.2f})")
    ax.set_xlabel("Layer index")
    ax.set_ylabel("5-fold CV accuracy (band = +/-1 std across folds)")
    ax.set_title("Per-layer probe: predicting correctness on OBSCURE pre-cutoff items only\n"
                 "(removes both cutoff and popularity from the disconfound)")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.0, 1.05)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)

    print(f"\n=== Correct-within-obscure probe ===")
    print(f"  Best layer: {accs.argmax()} (acc={accs.max():.3f} "
          f"+/- {stds[accs.argmax()]:.3f}, baseline={chance:.3f})")


def plot_correct_within_pre_probe(responses, out_path):
    pre = [r for r in responses if r["cutoff_class"] == "pre"]
    n_correct = sum(1 for r in pre if r["correct"])
    n_wrong = len(pre) - n_correct
    if n_correct < 5 or n_wrong < 5:
        print(f"\n=== Correct-within-pre probe: SKIPPED "
              f"(n_correct={n_correct}, n_wrong={n_wrong}; need >=5 of each) ===")
        return

    accs, stds, n_total = per_layer_probe(responses, "correct_within_pre")
    chance = max(n_correct, n_wrong) / len(pre)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    layers = np.arange(len(accs))
    ax.plot(layers, accs, marker="o", color="#17becf",
            label=f"predict correctness within pre-cutoff items (n={n_total}: "
                  f"{n_correct} correct, {n_wrong} wrong)")
    ax.fill_between(layers, accs - stds, accs + stds, color="#17becf", alpha=0.15)
    ax.axhline(chance, color="#17becf", linestyle=":", alpha=0.5,
               label=f"pre-cutoff majority baseline ({chance:.2f})")
    ax.set_xlabel("Layer index")
    ax.set_ylabel("5-fold CV accuracy (band = +/-1 std across folds)")
    ax.set_title("Per-layer probe: predicting model correctness on pre-cutoff items only\n"
                 "(removes the cutoff/correctness confound)")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.0, 1.05)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)

    print(f"\n=== Correct-within-pre probe ===")
    print(f"  Best layer: {accs.argmax()} (acc={accs.max():.3f} "
          f"+/- {stds[accs.argmax()]:.3f}, baseline={chance:.3f})")


def refusal_metrics_at_peak(responses, peak_layer: int):
    """Class-imbalance-aware metrics for the refusal_vs_wrong probe at one layer."""
    sub = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
    X = np.stack([r["last_prompt_hidden"][peak_layer] for r in sub])

    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=min(16, len(sub) - 1))),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

    y_pred = cross_val_predict(pipe, X, y, cv=cv, method="predict")
    y_proba = cross_val_predict(pipe, X, y, cv=cv, method="predict_proba")[:, 1]

    cm = confusion_matrix(y, y_pred, labels=[0, 1])  # rows: true; cols: pred
    tn, fp, fn, tp = cm.ravel()
    acc = (tp + tn) / len(y)
    bal_acc = balanced_accuracy_score(y, y_pred)
    recall_refusal = recall_score(y, y_pred, pos_label=1) if y.sum() else 0.0
    recall_wrong = recall_score(y, y_pred, pos_label=0)
    auc = roc_auc_score(y, y_proba)

    print(f"\n=== Refusal-vs-wrong metrics at peak layer {peak_layer} ===")
    print(f"  n = {len(y)} ({(y == 1).sum()} refusals, {(y == 0).sum()} wrong)")
    print(f"  Confusion matrix [rows=true, cols=pred, classes (0=wrong, 1=refusal)]:")
    print(f"    [[TN={tn:3d}  FP={fp:3d}]")
    print(f"     [FN={fn:3d}  TP={tp:3d}]]")
    print(f"  Accuracy:                 {acc:.3f}")
    print(f"  Balanced accuracy:        {bal_acc:.3f}")
    print(f"  Recall on refusals (TPR): {recall_refusal:.3f}  ({tp}/{tp + fn})")
    print(f"  Recall on wrong:          {recall_wrong:.3f}  ({tn}/{tn + fp})")
    print(f"  ROC AUC:                  {auc:.3f}")
    return {
        "peak_layer": peak_layer, "n": int(len(y)),
        "n_refusal": int((y == 1).sum()), "n_wrong": int((y == 0).sum()),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "accuracy": float(acc), "balanced_accuracy": float(bal_acc),
        "recall_refusal": float(recall_refusal), "recall_wrong": float(recall_wrong),
        "auc": float(auc),
    }


def plot_refusal_vs_wrong_probe(responses, out_path):
    subset = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
    n_refusal = sum(1 for r in subset if r["judge_label"] == "refusal")
    n_wrong = len(subset) - n_refusal
    if n_refusal < 5 or n_wrong < 5:
        print(f"\n=== Refusal-vs-wrong probe: SKIPPED "
              f"(n_refusal={n_refusal}, n_wrong={n_wrong}; need >=5 of each) ===")
        return

    accs, stds, n_total = per_layer_probe(responses, "refusal_vs_wrong")
    chance = max(n_refusal, n_wrong) / len(subset)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    layers = np.arange(len(accs))
    ax.plot(layers, accs, marker="o", color="#9467bd",
            label=f"predict refusal-vs-wrong (n={n_total}: {n_refusal} refusal, {n_wrong} wrong)")
    ax.fill_between(layers, accs - stds, accs + stds, color="#9467bd", alpha=0.15)
    ax.axhline(chance, color="#9467bd", linestyle=":", alpha=0.5,
               label=f"majority baseline ({chance:.2f})")
    ax.set_xlabel("Layer index")
    ax.set_ylabel("5-fold CV accuracy (band = ±1 std across folds)")
    ax.set_title("Per-layer probe: does the model already 'know' whether it will refuse\n"
                 "vs. confidently confabulate?")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.0, 1.05)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)

    print(f"\n=== Refusal-vs-wrong probe ===")
    print(f"  Best layer: {accs.argmax()} (acc={accs.max():.3f} "
          f"+/- {stds[accs.argmax()]:.3f}, baseline={chance:.3f})")


def layers_within_sigma(accs, stds, n_sigma=1.0):
    """Return all layer indices whose accuracy is within n_sigma fold-std of the peak."""
    peak_idx = int(accs.argmax())
    peak_acc = float(accs[peak_idx])
    peak_std = float(stds[peak_idx])
    band = [int(i) for i, a in enumerate(accs) if a >= peak_acc - n_sigma * peak_std]
    return {"peak_layer": peak_idx, "peak_acc": peak_acc, "peak_std": peak_std,
            "within_1sigma_layers": band,
            "within_1sigma_range": [min(band), max(band)] if band else [peak_idx, peak_idx]}


_YEAR_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
_CAP_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")


def prompt_features(r):
    """Prompt-only features: nothing from the model's hidden state."""
    q = r["question"]
    years = _YEAR_RE.findall(q)
    return {
        "q_char_len": len(q),
        "q_word_len": len(q.split()),
        "has_year": int(bool(years)),
        "year_value": int(years[0]) if years else 2000,
        "n_capwords": len(_CAP_RE.findall(q)),
        "n_digits": sum(c.isdigit() for c in q),
        "n_commas": q.count(","),
        "ends_questionmark": int(q.strip().endswith("?")),
        "domain": r["domain"],
        "category": r.get("category", "unknown"),
    }


def prompt_feature_matrix(responses, include_category=True, include_domain=True):
    feats = [prompt_features(r) for r in responses]
    domains = sorted({f["domain"] for f in feats})
    cats = sorted({f["category"] for f in feats})
    numeric_keys = ["q_char_len", "q_word_len", "has_year", "year_value",
                    "n_capwords", "n_digits", "n_commas", "ends_questionmark"]
    rows = []
    for f in feats:
        row = [f[k] for k in numeric_keys]
        if include_domain:
            row += [1 if f["domain"] == d else 0 for d in domains]
        if include_category:
            row += [1 if f["category"] == c else 0 for c in cats]
        rows.append(row)
    return np.array(rows, dtype=float)


def tfidf_baseline_for_target(responses, target):
    """5-fold CV accuracy of a TF-IDF + LR baseline on the raw question text.

    Strictly text-only: no metadata, no engineered features, no annotator labels.
    This is the strongest "what could a generic text classifier learn from the
    question text alone" baseline. If the hidden-state probe still beats this,
    it carries information beyond what is recoverable from the prompt by any
    bag-of-tokens classifier.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    if target == "correct":
        sub = list(responses)
        y = np.array([1 if r["correct"] else 0 for r in sub])
    elif target == "cutoff":
        sub = list(responses)
        y = np.array([1 if r["cutoff_class"] == "post" else 0 for r in sub])
    elif target == "refusal_vs_wrong":
        sub = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
        y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
    elif target == "refusal_vs_wrong_within_post":
        sub = [r for r in responses
               if r["judge_label"] in ("refusal", "wrong") and r["cutoff_class"] == "post"]
        y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
    elif target == "correct_within_pre":
        sub = [r for r in responses if r["cutoff_class"] == "pre"]
        y = np.array([1 if r["correct"] else 0 for r in sub])
    elif target == "correct_within_obscure":
        sub = [r for r in responses if r.get("category") == "obscure"]
        y = np.array([1 if r["correct"] else 0 for r in sub])
    else:
        raise ValueError(target)
    texts = [r["question"] for r in sub]
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95,
                                    sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    scores = cross_val_score(pipe, texts, y, cv=cv, scoring="accuracy")
    return {"n": int(len(y)), "n_pos": int(y.sum()),
            "mean_acc": float(scores.mean()),
            "std_acc": float(scores.std())}


def prompt_baseline_for_target(responses, target, include_category=True, include_domain=True):
    """5-fold CV accuracy of a logistic regression on prompt-only features for `target`."""
    if target == "correct":
        sub = list(responses)
        y = np.array([1 if r["correct"] else 0 for r in sub])
    elif target == "cutoff":
        sub = list(responses)
        y = np.array([1 if r["cutoff_class"] == "post" else 0 for r in sub])
    elif target == "refusal_vs_wrong":
        sub = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
        y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
    elif target == "refusal_vs_wrong_within_post":
        sub = [r for r in responses
               if r["judge_label"] in ("refusal", "wrong") and r["cutoff_class"] == "post"]
        y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
    elif target == "correct_within_pre":
        sub = [r for r in responses if r["cutoff_class"] == "pre"]
        y = np.array([1 if r["correct"] else 0 for r in sub])
    elif target == "correct_within_obscure":
        sub = [r for r in responses if r.get("category") == "obscure"]
        y = np.array([1 if r["correct"] else 0 for r in sub])
    else:
        raise ValueError(target)
    X = prompt_feature_matrix(sub, include_category=include_category,
                                include_domain=include_domain)
    pipe = Pipeline([("scale", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=2000, C=1.0))])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
    return {"n": int(len(y)), "n_pos": int(y.sum()),
            "mean_acc": float(scores.mean()),
            "std_acc": float(scores.std())}


def build_summary(responses):
    """Assemble a single authoritative dict consumed by the paper."""
    set_seeds()
    n = len(responses)
    s = {"n": n}

    # judge / cutoff / category distributions
    judge = defaultdict(int)
    cutoff = defaultdict(int)
    cat = defaultdict(int)
    cutoff_x_judge = defaultdict(int)
    for r in responses:
        judge[r["judge_label"]] += 1
        cutoff[r["cutoff_class"]] += 1
        cat[r.get("category", "?")] += 1
        cutoff_x_judge[(r["cutoff_class"], r["judge_label"])] += 1
    s["judge_counts"] = dict(judge)
    s["cutoff_counts"] = dict(cutoff)
    s["category_counts"] = dict(cat)
    s["cutoff_x_judge"] = {f"{k[0]}__{k[1]}": v for k, v in cutoff_x_judge.items()}

    # correctness x category (with mean logprob)
    by_cat = defaultdict(list)
    for r in responses:
        if r.get("category"):
            by_cat[r["category"]].append(r)
    cat_table = {}
    for c, items in by_cat.items():
        nc = sum(1 for r in items if r["correct"])
        lp = statistics.mean(r["mean_logprob"] for r in items)
        cat_table[c] = {"n": len(items), "correct": nc,
                        "accuracy": nc / len(items), "mean_logprob": lp}
    s["by_category"] = cat_table

    # cutoff-class accuracies
    s["by_cutoff"] = {}
    for cls in ["pre", "post"]:
        items = [r for r in responses if r["cutoff_class"] == cls]
        nc = sum(1 for r in items if r["correct"])
        s["by_cutoff"][cls] = {"n": len(items), "correct": nc,
                               "accuracy": nc / len(items) if items else 0.0}

    # domain x cutoff
    by_d = defaultdict(list)
    by_dc = defaultdict(list)
    for r in responses:
        by_d[r["domain"]].append(r)
        by_dc[(r["domain"], r["cutoff_class"])].append(r)
    s["by_domain"] = {}
    for d, items in by_d.items():
        nc = sum(1 for r in items if r["correct"])
        s["by_domain"][d] = {"n": len(items), "correct": nc,
                             "accuracy": nc / len(items)}
    s["by_domain_x_cutoff"] = {}
    for (d, cls), items in by_dc.items():
        nc = sum(1 for r in items if r["correct"])
        s["by_domain_x_cutoff"][f"{d}__{cls}"] = {
            "n": len(items), "correct": nc,
            "accuracy": nc / len(items) if items else 0.0}

    # per-layer probes
    s["probes"] = {}
    targets = ["correct", "cutoff", "refusal_vs_wrong", "refusal_vs_wrong_within_post",
               "correct_within_pre", "correct_within_obscure"]
    for t in targets:
        accs, stds, ntotal = per_layer_probe(responses, t)
        # majority baseline
        if t == "correct":
            ys = [1 if r["correct"] else 0 for r in responses]
        elif t == "cutoff":
            ys = [1 if r["cutoff_class"] == "post" else 0 for r in responses]
        elif t == "refusal_vs_wrong":
            sub = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
            ys = [1 if r["judge_label"] == "refusal" else 0 for r in sub]
        elif t == "refusal_vs_wrong_within_post":
            sub = [r for r in responses
                   if r["judge_label"] in ("refusal", "wrong") and r["cutoff_class"] == "post"]
            ys = [1 if r["judge_label"] == "refusal" else 0 for r in sub]
        elif t == "correct_within_pre":
            sub = [r for r in responses if r["cutoff_class"] == "pre"]
            ys = [1 if r["correct"] else 0 for r in sub]
        elif t == "correct_within_obscure":
            sub = [r for r in responses if r.get("category") == "obscure"]
            ys = [1 if r["correct"] else 0 for r in sub]
        n_pos = int(sum(ys)); n_neg = len(ys) - n_pos
        baseline = max(n_pos, n_neg) / len(ys) if ys else 0.0
        band = layers_within_sigma(accs, stds, n_sigma=1.0)
        s["probes"][t] = {
            "n": int(ntotal), "n_pos": n_pos, "n_neg": n_neg,
            "baseline": float(baseline),
            "per_layer_acc": [float(a) for a in accs],
            "per_layer_std": [float(s) for s in stds],
            **band,
            "margin_pp": (band["peak_acc"] - baseline) * 100,
        }
        # prompt-feature baselines: nested handcrafted feature sets + a strict
        # TF-IDF-on-question-text baseline.
        # tfidf is the strongest "what could a bag-of-tokens classifier learn".
        # text-only is hand-crafted features without annotator labels.
        # +domain adds the question's intrinsic field.
        # +domain+cat is the loosest (uses the annotator's difficulty label).
        s["probes"][t]["prompt_feature_baselines"] = {}
        try:
            s["probes"][t]["prompt_feature_baselines"]["tfidf"] = \
                tfidf_baseline_for_target(responses, t)
        except Exception as e:
            s["probes"][t]["prompt_feature_baselines"]["tfidf"] = {"error": str(e)}
        for tag, kwargs in [
            ("text_only", dict(include_category=False, include_domain=False)),
            ("text_plus_domain", dict(include_category=False, include_domain=True)),
            ("text_plus_domain_plus_cat", dict(include_category=True, include_domain=True)),
        ]:
            try:
                pf = prompt_baseline_for_target(responses, t, **kwargs)
                s["probes"][t]["prompt_feature_baselines"][tag] = pf
            except Exception as e:
                s["probes"][t]["prompt_feature_baselines"][tag] = {"error": str(e)}

    # refusal-vs-wrong class-imbalance metrics at peak
    rvw = s["probes"]["refusal_vs_wrong"]
    s["refusal_metrics_at_peak"] = refusal_metrics_at_peak(responses, int(rvw["peak_layer"]))

    # confident confabulation / refusal lists
    wrong_sorted = sorted([r for r in responses if r["judge_label"] == "wrong"],
                          key=lambda r: -r["mean_logprob"])[:5]
    refusal_sorted = sorted([r for r in responses if r["judge_label"] == "refusal"],
                            key=lambda r: -r["mean_logprob"])[:5]
    s["top_confabulations"] = [{"id": r["question_id"], "category": r.get("category"),
                                 "gold": r["expected_answer"],
                                 "answer_head": r["answer_text"][:140],
                                 "mean_logprob": r["mean_logprob"]}
                                for r in wrong_sorted]
    s["top_refusals"] = [{"id": r["question_id"], "category": r.get("category"),
                           "answer_head": r["answer_text"][:140],
                           "mean_logprob": r["mean_logprob"]}
                          for r in refusal_sorted]
    return s


def main():
    set_seeds()
    FIGURES_DIR.mkdir(exist_ok=True)
    responses = load_all()
    print(f"Loaded {len(responses)} responses")

    print_summary(responses)

    plot_logprob_histogram(responses, FIGURES_DIR / "01_logprob_histogram.png")
    plot_calibration_scatter(responses, FIGURES_DIR / "02_calibration_scatter.png")

    num_layers = responses[0]["last_prompt_hidden"].shape[0]
    plot_pca_layer(responses, num_layers // 2, FIGURES_DIR / f"03_pca_layer_{num_layers // 2}.png")
    plot_pca_layer(responses, num_layers - 1, FIGURES_DIR / f"04_pca_layer_{num_layers - 1}.png")

    plot_per_layer_probe(responses, FIGURES_DIR / "05_per_layer_probe.png")
    plot_refusal_vs_wrong_probe(responses, FIGURES_DIR / "06_refusal_vs_wrong_probe.png")
    plot_correct_within_pre_probe(responses, FIGURES_DIR / "07_correct_within_pre_probe.png")
    plot_correct_within_obscure_probe(responses, FIGURES_DIR / "11_correct_within_obscure_probe.png")

    summary = build_summary(responses)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_PATH, "w") as fp:
        json.dump(summary, fp, indent=2)
    print(f"\nWrote {SUMMARY_PATH}")

    print(f"\nFigures saved to {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
