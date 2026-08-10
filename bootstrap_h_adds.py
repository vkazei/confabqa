"""Bootstrap 95% CIs on h_adds (probe vs strongest prompt baseline) for every
(dataset, model, target) balanced cell.

Method: for each cell, run K=30 random balanced subsamples (N correct + N wrong,
without replacement within each subsample, but different subsamples sample
different items). For each subsample: refit probe (StandardScaler -> PCA(16) ->
LR, 5-fold CV at every layer, peak), refit 4 prompt baselines, compute
`h_adds = probe_peak_acc - strongest_baseline_acc`.

Report:
  - mean, median, std across K subsamples
  - percentile-based 95% CI: 2.5th / 97.5th percentile of the K h_adds values
  - "CI excludes 0?" flag
  - per-subsample h_adds list (for further analysis)

This is a proper sampling-distribution estimate of h_adds (under the assumption
that the underlying pool of items is representative). It's not a true
non-parametric bootstrap of the items themselves (that would require
refitting K * 11 * 29 layers * 5 folds models -- too slow). Instead it's a
"resampling-of-balanced-subsamples" bootstrap, which captures the same noise
sources for the same effective compute.

Writes:
  figures/bootstrap_h_adds.json  (all K subsample results per cell)
  figures/bootstrap_h_adds.md    (summary table with CIs)
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

_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location("analyze", _HERE / "03_analyze.py")
_AN = importlib.util.module_from_spec(_SPEC)
sys.modules["analyze"] = _AN
_SPEC.loader.exec_module(_AN)
from analyze import prompt_features, prompt_feature_matrix  # noqa: E402

K = 30                  # number of bootstrap subsamples per cell
MAX_PER_CLASS = 400
OUT_JSON = Path("figures") / "bootstrap_h_adds.json"
OUT_MD = Path("figures") / "bootstrap_h_adds.md"


def load_v13(model_subdir):
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


def load_triviaqa_pool():
    seen = {}
    for seed_dir in ["triviaqa_sample", "triviaqa_sample_seed1", "triviaqa_sample_seed2"]:
        resp_dir = Path(f"data/{seed_dir}/responses/qwen3_1_7b")
        act_dir = Path(f"data/{seed_dir}/activations/qwen3_1_7b")
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


def subset_for_target(responses, target):
    if target == "correct":
        return list(responses)
    if target == "correct_within_pre":
        return [r for r in responses if r["cutoff_class"] == "pre"]
    if target == "correct_within_obscure":
        return [r for r in responses if r.get("category") == "obscure"]
    raise ValueError(target)


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

    h_vals = []
    probe_vals = []
    base_vals = []
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

    # v1.3
    for model_subdir in ["qwen3_1_7b", "gemma_2_2b", "llama_3_2_3b"]:
        print(f"\n=== v1.3 / {model_subdir} ===")
        responses = load_v13(model_subdir)
        for target in ["correct", "correct_within_pre", "correct_within_obscure"]:
            sub = subset_for_target(responses, target)
            key = f"v13_{model_subdir}_{target}"
            results[key] = bootstrap_cell(sub, key)

    # PopQA Qwen3
    print(f"\n=== PopQA / qwen3_1_7b ===")
    pool = load_popqa_pool()
    print(f"  loaded {len(pool)} unique PopQA items")
    results["popqa_qwen3_1_7b_full"] = bootstrap_cell(pool, "popqa_qwen3_1_7b_full")

    # TriviaQA Qwen3
    print(f"\n=== TriviaQA / qwen3_1_7b ===")
    pool = load_triviaqa_pool()
    print(f"  loaded {len(pool)} unique TriviaQA items")
    results["triviaqa_qwen3_1_7b_full"] = bootstrap_cell(pool, "triviaqa_qwen3_1_7b_full")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\nWrote {OUT_JSON}")

    # Markdown
    md = []
    md.append(f"# Bootstrap 95% CIs on h_adds (probe − strongest prompt baseline)\n\n")
    md.append(f"Method: K={K} balanced 50/50 subsamples per cell. Each subsample: "
              "refit probe (StandardScaler→PCA(16)→LR, 5-fold CV, peak across 29 "
              "layers) and 4 prompt baselines on identical folds. 95% CI = percentile-"
              "based on the K h_adds values.\n\n")
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
    n_excludes = sum(1 for r in results.values() if r.get("ci_excludes_zero"))
    n_total = sum(1 for r in results.values() if "skipped" not in r)
    md.append(f"\n**{n_excludes}/{n_total}** cells have a 95% CI that excludes 0 — i.e., the\n")
    md.append("hidden-state-over-strongest-prompt-baseline margin is statistically\n")
    md.append("distinguishable from zero at the conventional bar.\n")

    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
