"""Generic 50/50 class-balanced rebalance test across all datasets.

For each (dataset, model, target) combination, samples N_per_class items
from each class (whichever class is smaller, capped at MAX_PER_CLASS),
refits probe + 4 prompt baselines, averages across 5 subsample seeds.

Covers:
  - v1.3 paper data: Qwen3-1.7B, Gemma 2 2B, Llama 3.2 3B
    targets: correct, correct_within_pre, correct_within_obscure
  - PopQA: pool across seed=0/1/2, full sample (Qwen3 only -- PopQA
    cross-model not run)
  - TriviaQA balanced result already in figures/qwen3_1_7b/triviaqa_rebalance_50_50.json
    (re-summarized here for comparison)

Writes figures/rebalance_all_datasets.md
"""
from __future__ import annotations

import importlib.util
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

# Import prompt_features / prompt_feature_matrix from 03_analyze.py
_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location("analyze", _HERE / "03_analyze.py")
_AN = importlib.util.module_from_spec(_SPEC)
sys.modules["analyze"] = _AN
_SPEC.loader.exec_module(_AN)
from analyze import prompt_features, prompt_feature_matrix  # noqa: E402

SUBSAMPLE_SEEDS = [0, 1, 2, 3, 4]
MAX_PER_CLASS = 400   # cap (avoids huge runs); use min(MAX, min_class)
OUT_MD = Path("figures") / "rebalance_all_datasets.md"
OUT_JSON = Path("figures") / "rebalance_all_datasets.json"


def load_v13_responses(model_subdir):
    resp_dir = Path("data/responses") / model_subdir
    act_dir = Path("data/activations") / model_subdir
    out = []
    for f in sorted(resp_dir.glob("*.json")):
        r = json.load(open(f))
        act = torch.load(act_dir / f"{r['question_id']}.pt", weights_only=False)
        r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
        out.append(r)
    return out


def load_popqa_pool():
    """Pool unique items from popqa_sample, _seed1, _seed2, keyed by popqa_id."""
    seen = {}
    for suffix in ["", "_seed1", "_seed2"]:
        resp_dir = Path(f"data/popqa_sample{suffix}/responses/qwen3_1_7b")
        act_dir = Path(f"data/popqa_sample{suffix}/activations/qwen3_1_7b")
        if not resp_dir.exists():
            continue
        for f in sorted(resp_dir.glob("*.json")):
            r = json.load(open(f))
            qid = r.get("popqa_id")
            if qid is None or qid in seen:
                continue
            act_path = act_dir / f"{r['question_id']}.pt"
            if not act_path.exists():
                continue
            act = torch.load(act_path, weights_only=False)
            r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
            seen[qid] = r
    return list(seen.values())


def subset_for_target(responses, target):
    if target == "correct" or target == "popqa_correct":
        return list(responses)
    if target == "correct_within_pre":
        return [r for r in responses if r["cutoff_class"] == "pre"]
    if target == "correct_within_obscure":
        return [r for r in responses if r.get("category") == "obscure"]
    raise ValueError(target)


def probe_peak(items, y):
    n_layers = items[0]["last_prompt_hidden"].shape[0]
    accs = np.zeros(n_layers); stds = np.zeros(n_layers)
    for layer in range(n_layers):
        X = np.stack([r["last_prompt_hidden"][layer] for r in items])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=min(16, len(items) - 1))),
            ("clf", LogisticRegression(max_iter=2000, C=1.0)),
        ])
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        s = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
        accs[layer] = s.mean(); stds[layer] = s.std()
    peak = int(accs.argmax())
    return float(accs[peak]), float(stds[peak]), peak


def all_baselines(items, y):
    texts = [r["question"] for r in items]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    out = {"majority": float(max((y == 1).mean(), (y == 0).mean()))}
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
    strongest_name = max(("tfidf", "text_only", "text_plus_domain", "text_plus_domain_plus_cat"),
                         key=lambda k: out[k])
    out["strongest_name"] = strongest_name
    out["strongest_value"] = out[strongest_name]
    return out


def rebalance_test(items, label):
    """For a set of items with correctness labels, run 50/50 balanced
    subsamples and report mean ± std of h_adds."""
    correct = [r for r in items if r["correct"]]
    wrong = [r for r in items if not r["correct"]]
    n_per_class = min(len(correct), len(wrong), MAX_PER_CLASS)
    if n_per_class < 20:
        return {"label": label, "skipped": f"min-class size {n_per_class} < 20"}
    print(f"  pool: {len(correct)} correct, {len(wrong)} wrong -> sampling "
          f"{n_per_class}+{n_per_class}")
    results = []
    for ss in SUBSAMPLE_SEEDS:
        rng = random.Random(ss)
        c_sub = rng.sample(correct, n_per_class)
        w_sub = rng.sample(wrong, n_per_class)
        sample = c_sub + w_sub
        rng.shuffle(sample)
        y = np.array([1 if r["correct"] else 0 for r in sample])
        p_acc, p_std, peak = probe_peak(sample, y)
        bl = all_baselines(sample, y)
        h = (p_acc - bl["strongest_value"]) * 100
        results.append({
            "sub_seed": ss, "probe_acc": p_acc, "probe_std": p_std, "peak_layer": peak,
            "strongest_name": bl["strongest_name"], "strongest_value": bl["strongest_value"],
            "h_adds_pp": h, "tfidf": bl["tfidf"], "majority": bl["majority"],
        })
        print(f"    sub_seed={ss}: probe L{peak}={p_acc*100:.2f}% strongest="
              f"{bl['strongest_name']}={bl['strongest_value']*100:.2f}% h_adds={h:+.2f} pp")
    h_vals = [r["h_adds_pp"] for r in results]
    mean_h = statistics.mean(h_vals)
    std_h = statistics.stdev(h_vals) if len(h_vals) > 1 else 0
    print(f"  -> {label}: h_adds = {mean_h:+.2f} ± {std_h:.2f} pp "
          f"(n_per_class={n_per_class}, {len(results)} subsamples)")
    return {
        "label": label, "n_per_class": n_per_class,
        "n_subsamples": len(results),
        "subsamples": results,
        "mean_h_adds_pp": mean_h, "std_h_adds_pp": std_h,
    }


def main():
    # Load TriviaQA balanced result (already computed)
    tqa_json = Path("figures/qwen3_1_7b/triviaqa_rebalance_50_50.json")
    tqa_balanced = json.load(open(tqa_json))["summary"] if tqa_json.exists() else None

    results = {}

    # v1.3 paper data
    for model_subdir in ["qwen3_1_7b", "gemma_2_2b", "llama_3_2_3b"]:
        print(f"\n=== v1.3 / {model_subdir} ===")
        responses = load_v13_responses(model_subdir)
        print(f"  loaded {len(responses)} responses")
        for target in ["correct", "correct_within_pre", "correct_within_obscure"]:
            sub = subset_for_target(responses, target)
            label = f"v13_{model_subdir}_{target}"
            print(f"\n  -- {target} (n={len(sub)}) --")
            results[label] = rebalance_test(sub, label)

    # PopQA pool across 3 seeds
    print(f"\n=== PopQA (pool seed 0/1/2) ===")
    popqa_pool = load_popqa_pool()
    print(f"  loaded {len(popqa_pool)} unique PopQA items")
    results["popqa_qwen3_1_7b_full"] = rebalance_test(popqa_pool, "popqa_qwen3_1_7b_full")

    # TriviaQA balanced (re-summarize)
    if tqa_balanced:
        results["triviaqa_qwen3_1_7b_full"] = {
            "label": "triviaqa_qwen3_1_7b_full",
            "n_per_class": 400,
            "n_subsamples": 5,
            "mean_h_adds_pp": tqa_balanced["mean_h_adds_pp"],
            "std_h_adds_pp": tqa_balanced["std_h_adds_pp"],
            "note": "from existing triviaqa_rebalance_50_50.json",
        }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\nWrote {OUT_JSON}")

    # Markdown
    md = []
    md.append("# Cross-dataset 50/50 class-balanced rebalance test\n\n")
    md.append("For each (dataset, model, target), sample N correct + N wrong items "
              "(N = min of class size and 400), refit probe + 4 prompt baselines "
              "with the standard 5-fold CV pipeline, repeat across 5 subsample seeds. "
              "Reports `h_adds vs strongest prompt baseline` as mean ± std across "
              "subsamples.\n\n")
    md.append("## Summary\n\n")
    md.append("| dataset/target | n per class | n subsamples | mean h_adds | std |\n")
    md.append("|---|--:|--:|--:|--:|\n")
    for k, r in results.items():
        if "skipped" in r:
            md.append(f"| {k} | -- | -- | (skipped: {r['skipped']}) | |\n")
            continue
        md.append(f"| `{k}` | {r['n_per_class']} | {r['n_subsamples']} | "
                  f"**{r['mean_h_adds_pp']:+.2f} pp** | {r['std_h_adds_pp']:.2f} |\n")

    md.append("\n## Comparison to unbalanced (single-seed paper) numbers\n\n")
    unbalanced_map = {
        "v13_qwen3_1_7b_correct": (2.42, "paper §6.5, single fold seed"),
        "v13_qwen3_1_7b_correct_within_pre": (3.04, "paper §6.5"),
        "v13_qwen3_1_7b_correct_within_obscure": (-2.56, "paper §6.5 — the 'cleanest refutation'"),
        "v13_gemma_2_2b_correct": (1.66, "paper §6.10"),
        "v13_gemma_2_2b_correct_within_pre": (3.73, ""),
        "v13_gemma_2_2b_correct_within_obscure": (1.98, ""),
        "v13_llama_3_2_3b_correct": (2.42, "paper §6.10"),
        "v13_llama_3_2_3b_correct_within_pre": (4.75, ""),
        "v13_llama_3_2_3b_correct_within_obscure": (6.54, ""),
        "popqa_qwen3_1_7b_full": (0.50, "PopQA seed=0"),
        "triviaqa_qwen3_1_7b_full": (4.54, "TriviaQA 3-seed mean"),
    }
    md.append("| dataset/target | unbalanced single-seed | balanced 50/50 (mean±std) | delta |\n")
    md.append("|---|--:|--:|--:|\n")
    for k, (unb, note) in unbalanced_map.items():
        if k not in results or "skipped" in results[k]:
            continue
        r = results[k]
        delta = r["mean_h_adds_pp"] - unb
        md.append(f"| `{k}` | {unb:+.2f} pp{' ' + note if note else ''} | "
                  f"**{r['mean_h_adds_pp']:+.2f} ± {r['std_h_adds_pp']:.2f} pp** | "
                  f"{delta:+.2f} pp |\n")

    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
