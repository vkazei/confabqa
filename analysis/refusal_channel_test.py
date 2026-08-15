"""Test whether Llama's large h_adds is mostly a refusal-readout.

Two tests, both K=30 balanced bootstraps:

  TEST A — drop refusals, refit:
    Filter to items where judge_label in {"correct", "wrong"}, balance
    correct vs wrong 50/50, refit probe + baselines, report h_adds.
    Prediction: if h_adds collapses for Llama, the original headline was
    largely refusal-readout. If it survives, it's genuine factual self-
    knowledge.

  TEST B — probe refusal directly:
    Target = (judge_label == "refusal"). Balance 50/50, refit probe +
    baselines, report:
      - probe peak accuracy (absolute)
      - h_adds (probe peak - strongest prompt baseline)
    Prediction: if Llama's probe scores high and Qwen's is near majority,
    refusal is the readable signal.

Cells tested (only the four cross-model external-dataset cells where the
contrast is largest):
  - PopQA × Qwen3-1.7B, PopQA × Llama-3.2-3B
  - TriviaQA × Qwen3-1.7B, TriviaQA × Llama-3.2-3B

Writes:
  figures/refusal_channel_test.json
  figures/refusal_channel_test.md
"""
from __future__ import annotations

import json
import random
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

from confabqa.constants import BOOTSTRAP_K as K, MAX_PER_CLASS
OUT_JSON = Path("figures") / "refusal_channel_test.json"
OUT_MD = Path("figures") / "refusal_channel_test.md"


def load_pool(dataset, model_subdir):
    if dataset == "popqa":
        suffixes = ["", "_seed1", "_seed2"]
        base = "popqa_sample"
        qid_field = "popqa_id"
    elif dataset == "triviaqa":
        suffixes = ["", "_seed1", "_seed2"]
        base = "triviaqa_sample"
        qid_field = "triviaqa_qid"
    else:
        raise ValueError(dataset)
    seen = {}
    for suffix in suffixes:
        resp_dir = Path(f"data/{base}{suffix}/responses/{model_subdir}")
        act_dir = Path(f"data/{base}{suffix}/activations/{model_subdir}")
        if not resp_dir.exists():
            continue
        for f in sorted(resp_dir.glob("*.json")):
            r = json.load(open(f))
            qid = r.get(qid_field)
            if qid is None or qid in seen:
                continue
            if "judge_label" not in r:
                continue
            act_path = act_dir / f"{r['question_id']}.pt"
            if not act_path.exists():
                continue
            act = torch.load(act_path, weights_only=False)
            r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
            seen[qid] = r
    return list(seen.values())


def probe_peak(items, y):
    n_layers = items[0]["last_prompt_hidden"].shape[0]
    accs = np.zeros(n_layers)
    for layer in range(n_layers):
        X = np.stack([r["last_prompt_hidden"][layer] for r in items])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=min(16, len(items) - 1))),
            ("clf", LogisticRegression(max_iter=2000, C=1.0)),
        ])
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        accs[layer] = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy").mean()
    peak = int(accs.argmax())
    return float(accs[peak]), peak


def all_baselines(items, y):
    texts = [r["question"] for r in items]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    out = {}
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, C=1.0))])
    out["tfidf"] = float(cross_val_score(pipe, texts, y, cv=cv, scoring="accuracy").mean())
    for tag, kw in [("text_only", dict(include_category=False, include_domain=False)),
                    ("text_plus_domain", dict(include_category=False, include_domain=True)),
                    ("text_plus_domain_plus_cat", dict(include_category=True, include_domain=True))]:
        X = prompt_feature_matrix(items, **kw)
        pipe = Pipeline([("scale", StandardScaler()),
                         ("clf", LogisticRegression(max_iter=2000, C=1.0))])
        out[tag] = float(cross_val_score(pipe, X, y, cv=cv, scoring="accuracy").mean())
    return max(out.values())


def bootstrap_cell(pos_items, neg_items, label):
    n_per_class = min(len(pos_items), len(neg_items), MAX_PER_CLASS)
    if n_per_class < 20:
        print(f"  [{label}] SKIP min-class={n_per_class}")
        return {"label": label, "skipped": f"min-class={n_per_class} < 20",
                "n_pos": len(pos_items), "n_neg": len(neg_items)}
    print(f"  [{label}] pool: {len(pos_items)} pos + {len(neg_items)} neg, "
          f"sampling {n_per_class}+{n_per_class}, K={K}")

    h_vals, probe_vals, base_vals = [], [], []
    for k in range(K):
        rng = random.Random(k)
        p_sub = rng.sample(pos_items, n_per_class)
        n_sub = rng.sample(neg_items, n_per_class)
        sample = p_sub + n_sub
        y = np.array([1] * n_per_class + [0] * n_per_class)
        idx = list(range(len(sample))); rng.shuffle(idx)
        sample = [sample[i] for i in idx]
        y = y[idx]
        p_acc, _ = probe_peak(sample, y)
        b_acc = all_baselines(sample, y)
        h = (p_acc - b_acc) * 100
        h_vals.append(h)
        probe_vals.append(p_acc * 100)
        base_vals.append(b_acc * 100)
        if (k + 1) % 10 == 0 or k == K - 1:
            print(f"    k={k+1}/{K}: probe {statistics.mean(probe_vals):.2f}%, "
                  f"baseline {statistics.mean(base_vals):.2f}%, "
                  f"h_adds {statistics.mean(h_vals):+.2f} pp")

    mean_h = statistics.mean(h_vals)
    std_h = statistics.stdev(h_vals) if len(h_vals) > 1 else 0
    h_sorted = sorted(h_vals)
    ci_low = h_sorted[int(0.025 * K)]
    ci_high = h_sorted[int(0.975 * K)]
    ci_excludes_zero = ci_low > 0 or ci_high < 0
    mean_probe = statistics.mean(probe_vals)
    mean_base = statistics.mean(base_vals)
    print(f"  -> {label}: probe {mean_probe:.2f}%, baseline {mean_base:.2f}%, "
          f"h_adds {mean_h:+.2f} ± {std_h:.2f} pp  "
          f"95% CI [{ci_low:+.2f}, {ci_high:+.2f}]  "
          f"{'EXCLUDES 0' if ci_excludes_zero else 'includes 0'}")
    return {
        "label": label, "n_per_class": n_per_class, "K": K,
        "h_adds_pp": h_vals, "probe_pct": probe_vals, "baseline_pct": base_vals,
        "mean_h": mean_h, "std_h": std_h,
        "mean_probe": mean_probe, "mean_baseline": mean_base,
        "ci_95_low": ci_low, "ci_95_high": ci_high,
        "ci_excludes_zero": ci_excludes_zero,
    }


def main():
    cells = [
        ("popqa", "qwen3_1_7b"),
        ("popqa", "llama_3_2_3b"),
        ("triviaqa", "qwen3_1_7b"),
        ("triviaqa", "llama_3_2_3b"),
    ]
    results = {"test_a_drop_refusals": {}, "test_b_refusal_probe": {}}

    for dataset, model in cells:
        print(f"\n=== {dataset} × {model} ===")
        pool = load_pool(dataset, model)
        print(f"  loaded {len(pool)} items with judge labels")
        labels = {}
        for r in pool:
            labels[r["judge_label"]] = labels.get(r["judge_label"], 0) + 1
        print(f"  judge label counts: {labels}")

        # TEST A: drop refusals, probe correct vs wrong
        non_refusals = [r for r in pool if r["judge_label"] in ("correct", "wrong")]
        correct = [r for r in non_refusals if r["judge_label"] == "correct"]
        wrong = [r for r in non_refusals if r["judge_label"] == "wrong"]
        label_a = f"{dataset}_{model}_drop_refusals"
        print(f"\n  TEST A ({label_a}): "
              f"after dropping refusals -> {len(correct)} correct, {len(wrong)} wrong")
        results["test_a_drop_refusals"][label_a] = bootstrap_cell(correct, wrong, label_a)

        # TEST B: probe refusal vs not-refusal
        refusals = [r for r in pool if r["judge_label"] == "refusal"]
        not_refusals = [r for r in pool if r["judge_label"] != "refusal"]
        label_b = f"{dataset}_{model}_refusal_vs_rest"
        print(f"\n  TEST B ({label_b}): "
              f"{len(refusals)} refusals vs {len(not_refusals)} not-refusals")
        results["test_b_refusal_probe"][label_b] = bootstrap_cell(refusals, not_refusals, label_b)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\nWrote {OUT_JSON}")

    md = []
    md.append("# Refusal-channel test: is Llama's huge h_adds mostly a refusal-readout?\n\n")
    md.append(f"K={K} balanced 50/50 bootstrap subsamples per cell. Same probe + "
              "baseline pipeline as `bootstrap_h_adds.md`.\n\n")

    md.append("## Test A — drop refusals, probe correct vs wrong\n\n")
    md.append("If Llama's headline +25 pp was mostly refusal-readout, this collapses.\n")
    md.append("For reference, the unfiltered numbers are: Qwen-PopQA +4.35, "
              "Llama-PopQA **+24.94**, Qwen-TriviaQA +9.57, Llama-TriviaQA **+21.25**.\n\n")
    md.append("| cell | n/class | probe acc | baseline | h_adds | 95% CI |\n")
    md.append("|---|--:|--:|--:|--:|---|\n")
    for k, r in results["test_a_drop_refusals"].items():
        if "skipped" in r:
            md.append(f"| `{k}` | — | (skipped: {r['skipped']}, "
                      f"pos={r['n_pos']}, neg={r['n_neg']}) | | | |\n")
            continue
        md.append(f"| `{k}` | {r['n_per_class']} | {r['mean_probe']:.2f}% | "
                  f"{r['mean_baseline']:.2f}% | **{r['mean_h']:+.2f} pp** | "
                  f"[{r['ci_95_low']:+.2f}, {r['ci_95_high']:+.2f}] |\n")

    md.append("\n## Test B — probe refusal directly\n\n")
    md.append("Target = judge_label == 'refusal'. Probe absolute accuracy is the "
              "interesting number here — if Llama's probe scores high and the "
              "baselines stay near 50% (majority of a 50/50 sample), refusal is "
              "the readable signal in the hidden state.\n\n")
    md.append("| cell | n/class | probe acc | baseline | h_adds | 95% CI |\n")
    md.append("|---|--:|--:|--:|--:|---|\n")
    for k, r in results["test_b_refusal_probe"].items():
        if "skipped" in r:
            md.append(f"| `{k}` | — | (skipped: {r['skipped']}, "
                      f"pos={r['n_pos']}, neg={r['n_neg']}) | | | |\n")
            continue
        md.append(f"| `{k}` | {r['n_per_class']} | {r['mean_probe']:.2f}% | "
                  f"{r['mean_baseline']:.2f}% | **{r['mean_h']:+.2f} pp** | "
                  f"[{r['ci_95_low']:+.2f}, {r['ci_95_high']:+.2f}] |\n")

    md.append("\n## Interpretation cheat-sheet\n\n")
    md.append("- **Test A h_adds collapses for Llama** → headline is mostly refusal channel.\n")
    md.append("- **Test A h_adds holds for Llama** → genuine factual self-knowledge contributes.\n")
    md.append("- **Test B Llama probe ≫ Qwen probe** → Llama has a clean abstention "
              "representation Qwen lacks (or has in a non-linearly-decodable form).\n")
    md.append("- **Test B baselines near 50%** → refusal is not predictable from question text "
              "alone, so probe gain is a real readout of the model's internal state, not a "
              "question-difficulty leak.\n")

    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
