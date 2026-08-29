"""Small-cell statistics repair: item bootstrap, permutation null, labels.

Three referee-requested reruns, CPU only:

A. Item-level bootstrap (B=400) at the summary-declared fixed layer for
   the five smallest disconfounded cells: resample items with
   replacement, refit probe (scaler -> PCA16 -> logreg, 5-fold CV) and
   a TF-IDF question-text baseline, report the percentile CI of the
   margin. Complements (not replaces) the K=30 subsample protocol.

B. Label-permutation null (B=100) of the peak-over-all-layers margin
   for the two all-items correctness cells, calibrating the
   max-over-layers selection bias the bootstrap cannot see.

C. External-dataset label sensitivity: PopQA/TriviaQA margins for Qwen
   and Llama under the generation-time substring labels vs the
   three-way judge labels, same pipeline.

Writes figures/small_cell_stats.json.
Run from the repo root: python -m analysis.small_cell_stats
"""
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA = Path("data")
B_BOOT = 400
B_PERM = 100


def probe_pipe():
    return make_pipeline(StandardScaler(), PCA(n_components=16),
                         LogisticRegression(max_iter=2000, C=1.0))


def tfidf_pipe():
    return make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2),
                         LogisticRegression(max_iter=2000, C=1.0))


def cv(pipe, X, y, seed=0):
    return float(cross_val_score(
        pipe, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=seed)).mean())


def load_cell(resp_dir, act_dir):
    items = []
    for f in sorted(Path(resp_dir).glob("*.json")):
        r = json.loads(f.read_text())
        a = torch.load(Path(act_dir) / f"{f.stem}.pt", map_location="cpu",
                       weights_only=False)
        r["H"] = a["last_prompt_hidden"].float().numpy()
        items.append(r)
    return items


def margin_at_layer(items, layer, y, seed=0):
    X = np.stack([r["H"][layer] for r in items])
    texts = [r["question"] for r in items]
    return cv(probe_pipe(), X, y, seed) - cv(tfidf_pipe(), texts, y, seed)


def peak_margin(items, y, seed=0):
    L = items[0]["H"].shape[0]
    texts = [r["question"] for r in items]
    base = cv(tfidf_pipe(), texts, y, seed)
    best = max(cv(probe_pipe(),
                  np.stack([r["H"][l] for r in items]), y, seed)
               for l in range(L))
    return best - base


def main():
    out = {}

    # ---------- A. item-level bootstrap ----------
    cells = [
        ("llama_within_pre", "llama_3_2_3b", 13,
         lambda r: r["cutoff_class"] == "pre"),
        ("llama_within_obscure", "llama_3_2_3b", 13,
         lambda r: r["category"] == "obscure"),
        ("llama_all", "llama_3_2_3b", 13, lambda r: True),
        ("qwen_within_obscure", "qwen3_1_7b", 7,
         lambda r: r["category"] == "obscure"),
        ("gemma_within_pre", "gemma_2_2b", 13,
         lambda r: r["cutoff_class"] == "pre"),
    ]
    out["item_bootstrap"] = {}
    for name, sub, layer, filt in cells:
        items = [r for r in load_cell(DATA / "responses" / sub,
                                      DATA / "activations" / sub) if filt(r)]
        y = np.array([1 if r["judge_label"] == "correct" else 0 for r in items])
        point = margin_at_layer(items, layer, y)
        rng = np.random.default_rng(0)
        boots = []
        for b in range(B_BOOT):
            idx = rng.integers(0, len(items), len(items))
            yi = y[idx]
            if yi.sum() < 8 or (1 - yi).sum() < 8:
                continue
            boots.append(margin_at_layer([items[i] for i in idx], layer, yi,
                                         seed=b % 5))
        lo, hi = np.percentile(boots, [2.5, 97.5])
        out["item_bootstrap"][name] = {
            "n": len(items), "n_pos": int(y.sum()), "layer": layer,
            "point_margin": round(point, 4), "B": len(boots),
            "ci95": [round(float(lo), 4), round(float(hi), 4)]}
        print(name, out["item_bootstrap"][name], flush=True)

    # ---------- B. permutation null of peak-over-layers ----------
    out["permutation_null"] = {}
    for name, sub in [("llama_all_correct", "llama_3_2_3b"),
                      ("qwen_all_correct", "qwen3_1_7b")]:
        items = load_cell(DATA / "responses" / sub, DATA / "activations" / sub)
        y = np.array([1 if r["judge_label"] == "correct" else 0 for r in items])
        obs = peak_margin(items, y)
        rng = np.random.default_rng(0)
        null = [peak_margin(items, rng.permutation(y), seed=b % 5)
                for b in range(B_PERM)]
        out["permutation_null"][name] = {
            "observed_margin": round(obs, 4),
            "null_mean": round(float(np.mean(null)), 4),
            "null_p95": round(float(np.percentile(null, 95)), 4),
            "p_value": round(float(np.mean([v >= obs for v in null])), 4),
            "B": B_PERM}
        print(name, out["permutation_null"][name], flush=True)

    # ---------- C. external label sensitivity ----------
    out["external_label_sensitivity"] = {}
    for ds in ("popqa_sample", "triviaqa_sample"):
        for sub in ("qwen3_1_7b", "llama_3_2_3b"):
            items = load_cell(DATA / ds / "responses" / sub,
                              DATA / ds / "activations" / sub)
            res = {}
            for lab_name, lab_fn in [
                ("substring", lambda r: bool(r["correct"])),
                ("judge", lambda r: r["judge_label"] == "correct")]:
                y = np.array([1 if lab_fn(r) else 0 for r in items])
                res[lab_name] = {
                    "n": len(items), "n_pos": int(y.sum()),
                    "peak_margin": round(peak_margin(items, y), 4)}
            out["external_label_sensitivity"][f"{ds}/{sub}"] = res
            print(ds, sub, res, flush=True)

    Path("figures/small_cell_stats.json").write_text(json.dumps(out, indent=1))
    print("Wrote figures/small_cell_stats.json")


if __name__ == "__main__":
    main()
