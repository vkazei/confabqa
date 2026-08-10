"""TriviaQA 50/50 class-balanced subsample test.

The seed-0/1/2 runs had ~38% correct rate, so the strongest prompt baseline
hovers near majority (~62%) and the probe's '+5 pp' is partly attributable
to "always predict wrong" being a strong default. This script tests
whether the probe's margin survives when class balance is enforced:
sample 400 correct + 400 wrong items from the pool of all unique items
across seeds 0/1/2, refit probe + baselines.

If h_adds stays ~+5 pp on the balanced subsample, the signal is genuine
"hidden state predicts correctness." If h_adds shrinks toward 0, the
seed-0/1/2 signal was partly class-imbalance prediction.

No new generation -- reuses cached activations from the three seed dirs.
"""
from __future__ import annotations

import importlib.util
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import MODEL_SUBDIR

# Import prompt_features / prompt_feature_matrix from 03_analyze.py
_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location("analyze", _HERE / "03_analyze.py")
_AN = importlib.util.module_from_spec(_SPEC)
sys.modules["analyze"] = _AN
_SPEC.loader.exec_module(_AN)
from analyze import prompt_features, prompt_feature_matrix  # noqa: E402

SEED_DIRS = ["triviaqa_sample", "triviaqa_sample_seed1", "triviaqa_sample_seed2"]
SUBSAMPLES = [0, 1, 2, 3, 4]  # 5 balanced subsample seeds
N_PER_CLASS = 400
OUT_MD = Path("figures") / MODEL_SUBDIR / "triviaqa_rebalance_50_50.md"
OUT_JSON = Path("figures") / MODEL_SUBDIR / "triviaqa_rebalance_50_50.json"


def load_pool():
    """Pool unique items across three seeds, keyed by triviaqa_qid."""
    by_qid = {}
    for seed_dir in SEED_DIRS:
        resp_dir = Path("data") / seed_dir / "responses" / MODEL_SUBDIR
        act_dir = Path("data") / seed_dir / "activations" / MODEL_SUBDIR
        if not resp_dir.exists():
            print(f"  skipping missing dir: {resp_dir}")
            continue
        n = 0
        for f in sorted(resp_dir.glob("*.json")):
            r = json.load(open(f))
            qid = r.get("triviaqa_qid")
            if qid is None or qid in by_qid:
                continue
            act_path = act_dir / f"{r['question_id']}.pt"
            if not act_path.exists():
                continue
            act = torch.load(act_path, weights_only=False)
            r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
            by_qid[qid] = r
            n += 1
        print(f"  {seed_dir}: added {n} unique items, pool size now {len(by_qid)}")
    return list(by_qid.values())


def correctness_probe_peak(items, y):
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


def main():
    print("Loading pool from 3 seed dirs...")
    pool = load_pool()
    correct_pool = [r for r in pool if r["correct"]]
    wrong_pool = [r for r in pool if not r["correct"]]
    print(f"\nPool size: {len(pool)} unique items")
    print(f"  correct: {len(correct_pool)}")
    print(f"  wrong:   {len(wrong_pool)}")

    if len(correct_pool) < N_PER_CLASS or len(wrong_pool) < N_PER_CLASS:
        n_per_class = min(len(correct_pool), len(wrong_pool))
        print(f"\n*Insufficient items for {N_PER_CLASS}+{N_PER_CLASS}; using {n_per_class}+{n_per_class}*")
    else:
        n_per_class = N_PER_CLASS

    results = []
    for sub_seed in SUBSAMPLES:
        rng = random.Random(sub_seed)
        c_sample = rng.sample(correct_pool, n_per_class)
        w_sample = rng.sample(wrong_pool, n_per_class)
        sample = c_sample + w_sample
        rng.shuffle(sample)
        y = np.array([1 if r["correct"] else 0 for r in sample])

        print(f"\n=== subsample seed={sub_seed} (n={len(sample)}, "
              f"{int(y.sum())} correct, {int((y==0).sum())} wrong) ===")
        probe_acc, probe_std, peak = correctness_probe_peak(sample, y)
        bl = all_baselines(sample, y)
        h_adds = (probe_acc - bl["strongest_value"]) * 100
        print(f"  probe peak L{peak} = {probe_acc*100:.2f}% +/- {probe_std*100:.2f} pp")
        print(f"  baselines: tfidf={bl['tfidf']*100:.2f}%, text={bl['text_only']*100:.2f}%, "
              f"+dom={bl['text_plus_domain']*100:.2f}%, +cat={bl['text_plus_domain_plus_cat']*100:.2f}% "
              f"(majority={bl['majority']*100:.2f}%)")
        print(f"  strongest = {bl['strongest_name']} = {bl['strongest_value']*100:.2f}%")
        print(f"  h adds vs strongest = {h_adds:+.2f} pp  (probe std at peak = {probe_std*100:.2f} pp)")
        results.append({
            "sub_seed": sub_seed,
            "n": len(sample),
            "probe_peak_acc": probe_acc, "probe_peak_std": probe_std,
            "probe_peak_layer": peak,
            "majority": bl["majority"], "tfidf": bl["tfidf"],
            "text_only": bl["text_only"],
            "text_plus_domain": bl["text_plus_domain"],
            "text_plus_domain_plus_cat": bl["text_plus_domain_plus_cat"],
            "strongest_name": bl["strongest_name"],
            "strongest_value": bl["strongest_value"],
            "h_adds_pp": h_adds,
        })

    # Summary
    h_vals = [r["h_adds_pp"] for r in results]
    probe_vals = [r["probe_peak_acc"] * 100 for r in results]
    baseline_vals = [r["strongest_value"] * 100 for r in results]
    mean_h = statistics.mean(h_vals); std_h = statistics.stdev(h_vals) if len(h_vals) > 1 else 0
    print(f"\n=== SUMMARY ({len(results)} balanced subsamples) ===")
    print(f"  probe peak: {statistics.mean(probe_vals):.2f}% +/- "
          f"{statistics.stdev(probe_vals) if len(probe_vals)>1 else 0:.2f} pp")
    print(f"  strongest baseline: {statistics.mean(baseline_vals):.2f}% +/- "
          f"{statistics.stdev(baseline_vals) if len(baseline_vals)>1 else 0:.2f} pp")
    print(f"  h adds vs strongest: {mean_h:+.2f} +/- {std_h:.2f} pp")

    # Comparison to unbalanced TriviaQA
    print("\nCompared to unbalanced TriviaQA (3 sample seeds at 38% correct rate):")
    print("  unbalanced h adds: +4.54 +/- 1.25 pp (seed=0/1/2 mean)")
    print(f"  balanced h adds:   {mean_h:+.2f} +/- {std_h:.2f} pp")

    summary = {
        "n_per_class": n_per_class,
        "n_subsamples": len(results),
        "subsample_results": results,
        "summary": {
            "mean_h_adds_pp": mean_h,
            "std_h_adds_pp": std_h,
            "mean_probe_acc": statistics.mean(probe_vals),
            "mean_strongest_baseline": statistics.mean(baseline_vals),
        },
        "comparison_to_unbalanced": {
            "unbalanced_3seed_h_adds_pp": 4.54,
            "unbalanced_3seed_std_pp": 1.25,
            "delta": mean_h - 4.54,
            "interpretation": (
                "Balanced > unbalanced -> signal is genuine and stronger when "
                "class imbalance is removed" if mean_h > 4.54 + std_h
                else ("Balanced ~ unbalanced -> +5 pp is mostly genuine signal, "
                      "not class-imbalance prediction" if abs(mean_h - 4.54) < max(std_h, 1.5)
                      else "Balanced << unbalanced -> unbalanced +5 pp was partly "
                           "class-imbalance prediction; rebalancing removes most of it")
            ),
        },
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(summary, fp, indent=2)
    print(f"\nWrote {OUT_JSON}")

    # Markdown
    md = []
    md.append("# TriviaQA 50/50 class-balanced subsample test\n\n")
    md.append(f"Pool: {len(pool)} unique TriviaQA items across seed=0/1/2 "
              f"(deduped by `triviaqa_qid`); {len(correct_pool)} judged correct, "
              f"{len(wrong_pool)} judged wrong.\n\n")
    md.append(f"Method: sample {n_per_class} correct + {n_per_class} wrong = "
              f"{2*n_per_class} balanced items, refit probe + 4 prompt baselines on the "
              "subsample. Repeated across 5 subsample seeds for variance.\n\n")
    md.append("## Per-subsample results\n\n")
    md.append("| sub_seed | probe peak | strongest baseline | **h adds** |\n")
    md.append("|--:|--:|--:|--:|\n")
    for r in results:
        md.append(f"| {r['sub_seed']} | "
                  f"{r['probe_peak_acc']*100:.2f}% (L{r['probe_peak_layer']}, "
                  f"+/-{r['probe_peak_std']*100:.2f}) | "
                  f"`{r['strongest_name']}` {r['strongest_value']*100:.2f}% | "
                  f"**{r['h_adds_pp']:+.2f} pp** |\n")
    md.append(f"\n**Mean across 5 balanced subsamples: `{mean_h:+.2f} ± {std_h:.2f} pp`**\n\n")
    md.append("## Comparison to unbalanced TriviaQA\n\n")
    md.append("| | unbalanced (38% correct, 3 sample seeds) | balanced 50/50 (5 subsample seeds) |\n")
    md.append("|---|--:|--:|\n")
    md.append(f"| **h adds vs strongest prompt baseline** | +4.54 ± 1.25 pp | "
              f"**{mean_h:+.2f} ± {std_h:.2f} pp** |\n")
    md.append(f"\n**Read:** {summary['comparison_to_unbalanced']['interpretation']}\n")

    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
