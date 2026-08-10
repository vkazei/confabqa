"""Bootstrap h_adds CIs for Qwen3-4B on PopQA (scaling data point).

Same K=30 protocol as bootstrap_llama_external.py. Single-seed pool
(n=800 unique). Writes:
  figures/bootstrap_qwen3_4b.json
  figures/bootstrap_qwen3_4b.md
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
from analyze import prompt_feature_matrix  # noqa: E402

K = 30
MAX_PER_CLASS = 400
MODEL_SUBDIR = "qwen3_4b"
RESP_DIR = Path(f"data/popqa_sample/responses/{MODEL_SUBDIR}")
ACT_DIR = Path(f"data/popqa_sample/activations/{MODEL_SUBDIR}")
OUT_JSON = Path("figures") / "bootstrap_qwen3_4b.json"
OUT_MD = Path("figures") / "bootstrap_qwen3_4b.md"


def load_pool():
    out = []
    for f in sorted(RESP_DIR.glob("*.json")):
        r = json.load(open(f))
        if "judge_label" not in r:
            continue
        act_path = ACT_DIR / f"{r['question_id']}.pt"
        if not act_path.exists():
            continue
        act = torch.load(act_path, weights_only=False)
        r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
        out.append(r)
    return out


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
        if (k + 1) % 10 == 0 or k == K - 1:
            print(f"    k={k+1}/{K}: h_adds running mean = {statistics.mean(h_vals):+.2f} pp")
    mean_h = statistics.mean(h_vals)
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
        "mean": mean_h, "std": std_h,
        "ci_95_low": ci_low, "ci_95_high": ci_high,
        "ci_excludes_zero": ci_excludes_zero,
    }


def main():
    print(f"=== PopQA / {MODEL_SUBDIR} ===")
    pool = load_pool()
    print(f"  loaded {len(pool)} items")
    cell = bootstrap_cell(pool, f"popqa_{MODEL_SUBDIR}_full")
    results = {f"popqa_{MODEL_SUBDIR}_full": cell}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(results, fp, indent=2)
    print(f"\nWrote {OUT_JSON}")
    md = [f"# Bootstrap h_adds — Qwen3-4B on PopQA\n\n",
          f"K={K} balanced 50/50 subsamples; same protocol as bootstrap_h_adds.md.\n\n",
          "| cell | n/class | mean h_adds | 95% CI | excl 0? |\n",
          "|---|--:|--:|---|:--:|\n"]
    for k, r in results.items():
        if "skipped" in r:
            md.append(f"| `{k}` | — | (skipped) | | |\n")
            continue
        flag = "**yes**" if r["ci_excludes_zero"] else "no"
        md.append(f"| `{k}` | {r['n_per_class']} | **{r['mean']:+.2f}** | "
                  f"[{r['ci_95_low']:+.2f}, {r['ci_95_high']:+.2f}] | {flag} |\n")
    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
