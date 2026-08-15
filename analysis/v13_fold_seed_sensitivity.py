"""v1.3 fold-seed sensitivity check for Qwen3-1.7B, Gemma 2 2B, Llama 3.2 3B.

The v1.3 paper data is fixed (n=784); we can't resample it the way we did
TriviaQA. But we CAN refit the probe + prompt baselines with different
CV `random_state` values to estimate how much of the reported
'h_adds_vs_strongest' margin is sensitive to a particular fold split.

This script:
  - For each model in {qwen3_1_7b, gemma_2_2b, llama_3_2_3b}:
    - For each target in {correct, correct_within_pre, correct_within_obscure}:
      - For each fold_seed in {0, 1, 2, 3, 4}:
        - Refit probe + all four prompt baselines
        - Record probe peak acc, strongest baseline, h_adds
    - Report mean +- std of h_adds across fold seeds

Writes figures/v13_fold_seed_sensitivity.md
"""
from __future__ import annotations

import json
import statistics
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

from confabqa.analysis import prompt_features, prompt_feature_matrix

MODELS = ["qwen3_1_7b", "gemma_2_2b", "llama_3_2_3b"]
TARGETS = ["correct", "correct_within_pre", "correct_within_obscure"]
FOLD_SEEDS = [0, 1, 2, 3, 4]
OUT_MD = Path("figures") / "v13_fold_seed_sensitivity.md"


def load_responses(model_subdir):
    resp_dir = Path("data/responses") / model_subdir
    act_dir = Path("data/activations") / model_subdir
    out = []
    for f in sorted(resp_dir.glob("*.json")):
        r = json.load(open(f))
        act = torch.load(act_dir / f"{r['question_id']}.pt", weights_only=False)
        r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
        out.append(r)
    return out


def subset_and_y(responses, target):
    if target == "correct":
        sub = list(responses)
    elif target == "correct_within_pre":
        sub = [r for r in responses if r["cutoff_class"] == "pre"]
    elif target == "correct_within_obscure":
        sub = [r for r in responses if r.get("category") == "obscure"]
    y = np.array([1 if r["correct"] else 0 for r in sub])
    return sub, y


def probe_peak_at_seed(sub, y, fold_seed):
    n_layers = sub[0]["last_prompt_hidden"].shape[0]
    accs = np.zeros(n_layers); stds = np.zeros(n_layers)
    for layer in range(n_layers):
        X = np.stack([r["last_prompt_hidden"][layer] for r in sub])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=min(16, len(sub) - 1))),
            ("clf", LogisticRegression(max_iter=2000, C=1.0)),
        ])
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=fold_seed)
        s = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
        accs[layer] = s.mean(); stds[layer] = s.std()
    peak = int(accs.argmax())
    return float(accs[peak]), float(stds[peak]), peak


def baselines_at_seed(sub, y, fold_seed):
    texts = [r["question"] for r in sub]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=fold_seed)
    out = {"majority": float(max((y == 1).mean(), (y == 0).mean()))}
    # TF-IDF
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, C=1.0))])
    out["tfidf"] = float(cross_val_score(pipe, texts, y, cv=cv, scoring="accuracy").mean())
    # Engineered (3 variants)
    for tag, kw in [("text_only", dict(include_category=False, include_domain=False)),
                    ("text_plus_domain", dict(include_category=False, include_domain=True)),
                    ("text_plus_domain_plus_cat", dict(include_category=True, include_domain=True))]:
        X = prompt_feature_matrix(sub, **kw)
        pipe = Pipeline([("scale", StandardScaler()),
                         ("clf", LogisticRegression(max_iter=2000, C=1.0))])
        out[tag] = float(cross_val_score(pipe, X, y, cv=cv, scoring="accuracy").mean())
    strongest_name = max(("tfidf", "text_only", "text_plus_domain", "text_plus_domain_plus_cat"),
                         key=lambda k: out[k])
    out["strongest_name"] = strongest_name
    out["strongest_value"] = out[strongest_name]
    return out


def main():
    all_results = {}
    for model_subdir in MODELS:
        print(f"\n=== {model_subdir} ===")
        responses = load_responses(model_subdir)
        print(f"  loaded {len(responses)} responses")
        all_results[model_subdir] = {}
        for target in TARGETS:
            sub, y = subset_and_y(responses, target)
            if len(set(y)) < 2 or min((y == 0).sum(), (y == 1).sum()) < 5:
                continue
            print(f"\n  [{target}] n={len(sub)} (pos={int(y.sum())})")
            per_seed = []
            for fs in FOLD_SEEDS:
                probe_acc, probe_std, peak = probe_peak_at_seed(sub, y, fs)
                bl = baselines_at_seed(sub, y, fs)
                h_adds = (probe_acc - bl["strongest_value"]) * 100
                per_seed.append({
                    "fold_seed": fs,
                    "probe_peak_acc": probe_acc, "probe_peak_std": probe_std,
                    "probe_peak_layer": peak,
                    "strongest_baseline_name": bl["strongest_name"],
                    "strongest_baseline_value": bl["strongest_value"],
                    "h_adds_pp": h_adds,
                    "tfidf": bl["tfidf"], "text_only": bl["text_only"],
                    "+dom": bl["text_plus_domain"], "+cat": bl["text_plus_domain_plus_cat"],
                    "majority": bl["majority"],
                })
                print(f"    fold_seed={fs}: probe L{peak} {probe_acc*100:.2f}% "
                      f"+/- {probe_std*100:.2f} pp, strongest={bl['strongest_name']}={bl['strongest_value']*100:.2f}%, "
                      f"h_adds={h_adds:+.2f} pp")
            all_results[model_subdir][target] = per_seed
            h_vals = [r["h_adds_pp"] for r in per_seed]
            mean = statistics.mean(h_vals); std = statistics.stdev(h_vals) if len(h_vals) > 1 else 0
            print(f"    -> h_adds across fold seeds: {mean:+.2f} +/- {std:.2f} pp")

    # Markdown report
    lines = []
    lines.append("# v1.3 fold-seed sensitivity (Qwen3-1.7B / Gemma 2 2B / Llama 3.2 3B)\n\n")
    lines.append("Fixed v1.3 paper data (n=784); only `random_state` of the 5-fold CV "
                 "split varies. Tests how much of the reported `h_adds_vs_strongest` "
                 "margin is sensitive to a particular fold split, holding the dataset "
                 "and pipeline constant.\n\n")
    for model_subdir, per_target in all_results.items():
        lines.append(f"## {model_subdir}\n\n")
        for target, per_seed in per_target.items():
            h_vals = [r["h_adds_pp"] for r in per_seed]
            mean = statistics.mean(h_vals)
            std = statistics.stdev(h_vals) if len(h_vals) > 1 else 0
            within_band = abs(mean) <= statistics.mean(r["probe_peak_std"] * 100 for r in per_seed)
            lines.append(f"### `{target}` (n={int(per_seed[0]['probe_peak_acc']*0+0)+1 if False else ''})\n\n")
            lines.append("| fold_seed | probe peak | strongest baseline | **h adds** |\n")
            lines.append("|--:|--:|--:|--:|\n")
            for r in per_seed:
                lines.append(f"| {r['fold_seed']} | "
                             f"{r['probe_peak_acc']*100:.2f}% (L{r['probe_peak_layer']}, "
                             f"+/- {r['probe_peak_std']*100:.2f}) | "
                             f"`{r['strongest_baseline_name']}` "
                             f"{r['strongest_baseline_value']*100:.2f}% | "
                             f"**{r['h_adds_pp']:+.2f} pp** |\n")
            lines.append(f"\n**h_adds across 5 fold seeds: `{mean:+.2f} ± {std:.2f} pp`** "
                         f"(within fold std band? {'yes' if within_band else 'NO'})\n\n")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("".join(lines))
    print(f"\nWrote {OUT_MD}")

    # Also save JSON
    json_path = OUT_MD.with_suffix(".json")
    with open(json_path, "w") as fp:
        json.dump(all_results, fp, indent=2)
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
