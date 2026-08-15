"""Bootstrap 95% CIs on h_adds for Llama-3.2-3B-Instruct on PopQA + TriviaQA.

Mirrors bootstrap_h_adds.py exactly (K=30 balanced subsamples, same probe
pipeline and prompt baselines) but for the two new cells produced by the
Llama generalization runs:
  - popqa_llama_3_2_3b_full
  - triviaqa_llama_3_2_3b_full

Writes:
  figures/bootstrap_llama_external.json
  figures/bootstrap_llama_external.md

Reusing the same K=30 and percentile-based 95% CI makes results directly
comparable to bootstrap_h_adds.md.
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
MODEL_SUBDIR = "llama_3_2_3b"
OUT_JSON = Path("figures") / "bootstrap_llama_external.json"
OUT_MD = Path("figures") / "bootstrap_llama_external.md"


def load_popqa_pool():
    seen = {}
    for suffix in ["", "_seed1", "_seed2"]:
        resp_dir = Path(f"data/popqa_sample{suffix}/responses/{MODEL_SUBDIR}")
        act_dir = Path(f"data/popqa_sample{suffix}/activations/{MODEL_SUBDIR}")
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


def load_triviaqa_pool():
    seen = {}
    for seed_dir in ["triviaqa_sample", "triviaqa_sample_seed1", "triviaqa_sample_seed2"]:
        resp_dir = Path(f"data/{seed_dir}/responses/{MODEL_SUBDIR}")
        act_dir = Path(f"data/{seed_dir}/activations/{MODEL_SUBDIR}")
        if not resp_dir.exists():
            continue
        for f in sorted(resp_dir.glob("*.json")):
            r = json.load(open(f))
            qid = r.get("triviaqa_qid")
            if qid is None or qid in seen:
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


def bootstrap_cell(items, label):
    correct = [r for r in items if r["correct"]]
    wrong = [r for r in items if not r["correct"]]
    n_per_class = min(len(correct), len(wrong), MAX_PER_CLASS)
    if n_per_class < 20:
        print(f"  [{label}] SKIP min-class={n_per_class}")
        return {"label": label, "skipped": f"min-class={n_per_class} < 20"}
    print(f"  [{label}] pool: {len(correct)} correct + {len(wrong)} wrong, "
          f"sampling {n_per_class}+{n_per_class}, K={K}")

    h_vals, probe_vals, base_vals = [], [], []
    for k in range(K):
        rng = random.Random(k)
        c_sub = rng.sample(correct, n_per_class)
        w_sub = rng.sample(wrong, n_per_class)
        sample = c_sub + w_sub
        rng.shuffle(sample)
        y = np.array([1 if r["correct"] else 0 for r in sample])
        p_acc, _ = probe_peak(sample, y)
        b_acc = all_baselines(sample, y)
        h = (p_acc - b_acc) * 100
        h_vals.append(h)
        probe_vals.append(p_acc * 100)
        base_vals.append(b_acc * 100)
        if (k + 1) % 5 == 0 or k == K - 1:
            print(f"    k={k+1}/{K}: h_adds running mean = {statistics.mean(h_vals):+.2f} pp")

    mean_h = statistics.mean(h_vals)
    median_h = statistics.median(h_vals)
    std_h = statistics.stdev(h_vals) if len(h_vals) > 1 else 0
    h_sorted = sorted(h_vals)
    ci_low = h_sorted[int(0.025 * K)]
    ci_high = h_sorted[int(0.975 * K)]
    ci_excludes_zero = ci_low > 0 or ci_high < 0
    print(f"  -> {label}: h_adds = {mean_h:+.2f} ± {std_h:.2f} pp  "
          f"95% CI [{ci_low:+.2f}, {ci_high:+.2f}]  "
          f"{'EXCLUDES 0' if ci_excludes_zero else 'includes 0'}")
    return {
        "label": label, "n_per_class": n_per_class, "K": K,
        "h_adds_pp": h_vals, "probe_pct": probe_vals, "baseline_pct": base_vals,
        "mean": mean_h, "median": median_h, "std": std_h,
        "ci_95_low": ci_low, "ci_95_high": ci_high,
        "ci_excludes_zero": ci_excludes_zero,
    }


def main():
    results = {}

    print(f"\n=== PopQA / {MODEL_SUBDIR} ===")
    pool = load_popqa_pool()
    print(f"  loaded {len(pool)} unique PopQA items")
    if pool:
        results[f"popqa_{MODEL_SUBDIR}_full"] = bootstrap_cell(pool, f"popqa_{MODEL_SUBDIR}_full")
    else:
        print("  no items found — skipping")

    print(f"\n=== TriviaQA / {MODEL_SUBDIR} ===")
    pool = load_triviaqa_pool()
    print(f"  loaded {len(pool)} unique TriviaQA items")
    if pool:
        results[f"triviaqa_{MODEL_SUBDIR}_full"] = bootstrap_cell(pool, f"triviaqa_{MODEL_SUBDIR}_full")
    else:
        print("  no items found — skipping")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\nWrote {OUT_JSON}")

    md = []
    md.append(f"# Bootstrap 95% CIs on h_adds — Llama-3.2-3B on external datasets\n\n")
    md.append(f"Method: K={K} balanced 50/50 subsamples per cell. Same pipeline as "
              "`bootstrap_h_adds.md`. 95% CI = percentile-based.\n\n")
    md.append("| cell | n/class | mean h_adds | median | std | 95% CI | excludes 0? |\n")
    md.append("|---|--:|--:|--:|--:|---|:--:|\n")
    for k, r in results.items():
        if "skipped" in r:
            md.append(f"| `{k}` | — | (skipped: {r['skipped']}) | | | | |\n")
            continue
        flag = "**yes**" if r["ci_excludes_zero"] else "no"
        md.append(f"| `{k}` | {r['n_per_class']} | "
                  f"**{r['mean']:+.2f} pp** | {r['median']:+.2f} | {r['std']:.2f} | "
                  f"[{r['ci_95_low']:+.2f}, {r['ci_95_high']:+.2f}] | {flag} |\n")
    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
