"""Cross-dataset transfer of the correctness probe (Qwen3-1.7B).

Open question raised in the abstract: does a correctness probe trained on
ConfabQA-784 generalize to PopQA / TriviaQA, or is the hidden-state correctness
signal dataset-specific?

Protocol:
  1. For each (train_dataset, test_dataset) pair:
     - Load Qwen3-1.7B last-prompt-token hidden states at a fixed layer.
     - Use judge_label == "correct" as the target on both datasets.
     - Fit pipeline (StandardScaler -> PCA(16) -> LR, C=1.0) on TRAIN only.
     - Predict on TEST. Report accuracy + majority-class baseline.
  2. Report a 3x3 matrix of cross-dataset accuracies.
  3. Compare against:
     - Majority baseline on each test set
     - Within-dataset 5-fold CV accuracy (diagonal of the matrix is "no transfer")
     - Prompt-feature classifier trained on TRAIN applied to TEST (controls for
       "just learning question-text patterns")

Run at layers 14, 18, 22, 28 to see whether transfer is layer-dependent.

Outputs:
  figures/cross_dataset_transfer.{json,md}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import argparse

LAYERS = [14, 18, 22, 28]  # will be overridden if MODEL has different layer count


def load_confabqa(model_subdir):
    resp = Path(f"data/responses/{model_subdir}")
    act = Path(f"data/activations/{model_subdir}")
    out = []
    for f in sorted(resp.glob("*.json")):
        r = json.load(open(f))
        if "judge_label" not in r:
            continue
        a = torch.load(act / f"{r['question_id']}.pt", weights_only=False)
        r["h"] = a["last_prompt_hidden"].numpy()
        r["y"] = 1 if r["judge_label"] == "correct" else 0
        out.append(r)
    return out


def load_external(name, model_subdir):
    """name in {'popqa', 'triviaqa'}. Pools all three seeds, dedupes by qid."""
    qid_field = "popqa_id" if name == "popqa" else "triviaqa_qid"
    seen = {}
    for suffix in ["", "_seed1", "_seed2"]:
        resp = Path(f"data/{name}_sample{suffix}/responses/{model_subdir}")
        act = Path(f"data/{name}_sample{suffix}/activations/{model_subdir}")
        if not resp.exists():
            continue
        for f in sorted(resp.glob("*.json")):
            r = json.load(open(f))
            qid = r.get(qid_field)
            if qid is None or qid in seen or "judge_label" not in r:
                continue
            a = torch.load(act / f"{r['question_id']}.pt", weights_only=False)
            r["h"] = a["last_prompt_hidden"].numpy()
            r["y"] = 1 if r["judge_label"] == "correct" else 0
            seen[qid] = r
    return list(seen.values())


def stack_layer(items, layer):
    X = np.stack([r["h"][layer] for r in items])
    y = np.array([r["y"] for r in items])
    return X, y


def majority(y):
    return float(max((y == 1).mean(), (y == 0).mean()))


def within_dataset_cv(items, layer):
    X, y = stack_layer(items, layer)
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=min(16, len(items) - 1))),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    return float(cross_val_score(pipe, X, y, cv=cv, scoring="accuracy").mean())


def cross_dataset(train_items, test_items, layer):
    X_train, y_train = stack_layer(train_items, layer)
    X_test, y_test = stack_layer(test_items, layer)
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=min(16, len(train_items) - 1))),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    pipe.fit(X_train, y_train)
    return float(pipe.score(X_test, y_test))


def prompt_baseline_cross(train_items, test_items):
    """TF-IDF on question text trained on TRAIN, predicted on TEST."""
    X_train_text = [r["question"] for r in train_items]
    y_train = np.array([r["y"] for r in train_items])
    X_test_text = [r["question"] for r in test_items]
    y_test = np.array([r["y"] for r in test_items])
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    pipe.fit(X_train_text, y_train)
    return float(pipe.score(X_test_text, y_test))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3_1_7b",
                        help="MODEL_SUBDIR under data/activations/ "
                             "(e.g. qwen3_1_7b, llama_3_2_3b)")
    parser.add_argument("--layers", type=int, nargs="+", default=None,
                        help="Layers to test; default per-model")
    args = parser.parse_args()
    model = args.model
    out_json = Path(f"figures/cross_dataset_transfer_{model}.json")
    out_md = Path(f"figures/cross_dataset_transfer_{model}.md")

    print(f"Loading datasets ({model} hidden states)...")
    confabqa = load_confabqa(model)
    popqa = load_external("popqa", model)
    triviaqa = load_external("triviaqa", model)
    datasets = {"ConfabQA-784": confabqa, "PopQA": popqa, "TriviaQA": triviaqa}
    for name, items in datasets.items():
        n = len(items)
        pos = sum(1 for r in items if r["y"] == 1) if items else 0
        print(f"  {name}: n={n}, correct={pos} ({pos/max(n,1)*100:.1f}%)")

    # Determine n_layers from data
    n_layers = confabqa[0]["h"].shape[0] if confabqa else (popqa[0]["h"].shape[0] if popqa else triviaqa[0]["h"].shape[0])
    if args.layers:
        layers = args.layers
    else:
        # Pick 4 layers spanning early-mid-late based on model depth
        layers = sorted({n_layers // 4, n_layers // 2,
                          int(n_layers * 0.75), n_layers - 1})
    print(f"  n_layers={n_layers}, sweeping layers {layers}")

    results = {"model": model, "layers": layers, "datasets": {}, "transfer": {}, "baselines": {}}

    # Per-dataset metadata
    for name, items in datasets.items():
        y = np.array([r["y"] for r in items])
        results["datasets"][name] = {
            "n": len(items), "n_correct": int(y.sum()),
            "majority_baseline": majority(y),
        }

    for layer in layers:
        print(f"\n=== layer {layer} ===")
        # Within-dataset CV (diagonal)
        within = {}
        for name, items in datasets.items():
            acc = within_dataset_cv(items, layer)
            within[name] = acc
            print(f"  WITHIN {name:>12s}: 5-fold CV acc = {acc*100:.2f}% (majority {majority(np.array([r['y'] for r in items]))*100:.2f}%)")

        # Cross-dataset transfer
        cross_matrix = {}
        for tr_name, tr_items in datasets.items():
            cross_matrix[tr_name] = {}
            for te_name, te_items in datasets.items():
                if tr_name == te_name:
                    cross_matrix[tr_name][te_name] = within[tr_name]
                else:
                    acc = cross_dataset(tr_items, te_items, layer)
                    cross_matrix[tr_name][te_name] = acc
                    print(f"  TRANSFER {tr_name:>12s} -> {te_name:<12s}: acc = {acc*100:.2f}% (majority {majority(np.array([r['y'] for r in te_items]))*100:.2f}%)")

        results["transfer"][f"layer{layer}"] = cross_matrix

    # Prompt-feature baseline cross-dataset (layer-independent — uses question text)
    print(f"\n=== prompt-feature baseline (TF-IDF, layer-independent) ===")
    prompt_cross = {}
    for tr_name, tr_items in datasets.items():
        prompt_cross[tr_name] = {}
        for te_name, te_items in datasets.items():
            if tr_name == te_name:
                # Within-dataset 5-fold for the baseline too
                texts = [r["question"] for r in tr_items]
                y = np.array([r["y"] for r in tr_items])
                pipe = Pipeline([
                    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True)),
                    ("clf", LogisticRegression(max_iter=2000, C=1.0)),
                ])
                cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
                acc = float(cross_val_score(pipe, texts, y, cv=cv, scoring="accuracy").mean())
            else:
                acc = prompt_baseline_cross(tr_items, te_items)
            prompt_cross[tr_name][te_name] = acc
            print(f"  PROMPT-BL {tr_name:>12s} -> {te_name:<12s}: acc = {acc*100:.2f}%")
    results["baselines"]["prompt_feature_cross"] = prompt_cross

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\nWrote {out_json}")

    # Markdown report
    md = []
    md.append(f"# Cross-dataset transfer of the correctness probe ({model})\n\n")
    md.append(f"Train a {model} correctness probe on dataset A, apply (without refit) to dataset B.\n")
    md.append("Target = `judge_label == \"correct\"`. Pipeline: StandardScaler -> PCA(16) -> LR(C=1.0).\n\n")

    md.append("## Dataset sizes\n\n")
    md.append("| dataset | n | correct | %correct | majority baseline |\n|---|--:|--:|--:|--:|\n")
    for name, d in results["datasets"].items():
        md.append(f"| {name} | {d['n']} | {d['n_correct']} | {d['n_correct']/d['n']*100:.1f}% | {d['majority_baseline']*100:.2f}% |\n")
    md.append("\n")

    md.append("## Probe transfer matrix\n\n")
    md.append("Rows: train dataset. Columns: test dataset. Values: accuracy %.\n")
    md.append("Diagonal: within-dataset 5-fold CV (probe trained and evaluated on the same set).\n")
    md.append("Off-diagonal: train on row, test on column, no refit.\n\n")

    for layer in layers:
        md.append(f"### Layer {layer}\n\n")
        m = results["transfer"][f"layer{layer}"]
        md.append("| train \\ test | ConfabQA-784 | PopQA | TriviaQA |\n|---|--:|--:|--:|\n")
        for tr in ["ConfabQA-784", "PopQA", "TriviaQA"]:
            row = [f"{m[tr][te]*100:.2f}" for te in ["ConfabQA-784", "PopQA", "TriviaQA"]]
            md.append(f"| {tr} | {row[0]} | {row[1]} | {row[2]} |\n")
        md.append("\n")

    md.append("## Prompt-feature baseline transfer (TF-IDF on question text)\n\n")
    md.append("Control: same train/test split but the classifier sees only question text, no hidden state.\n\n")
    pc = results["baselines"]["prompt_feature_cross"]
    md.append("| train \\ test | ConfabQA-784 | PopQA | TriviaQA |\n|---|--:|--:|--:|\n")
    for tr in ["ConfabQA-784", "PopQA", "TriviaQA"]:
        row = [f"{pc[tr][te]*100:.2f}" for te in ["ConfabQA-784", "PopQA", "TriviaQA"]]
        md.append(f"| {tr} | {row[0]} | {row[1]} | {row[2]} |\n")
    md.append("\n")

    md.append("## Reading the matrix\n\n")
    md.append("- **Diagonal > off-diagonal**: probe overfits to dataset-specific features (signal is dataset-specific).\n")
    md.append("- **Diagonal ≈ off-diagonal**: probe captures a dataset-agnostic correctness signal.\n")
    md.append("- **Off-diagonal ≈ majority baseline**: transfer fails entirely; the probe's within-dataset accuracy was item-specific noise.\n")
    md.append("- **Off-diagonal > prompt-feature transfer**: hidden-state probe extracts something beyond question-text patterns even cross-dataset.\n")

    out_md.write_text("".join(md))
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
