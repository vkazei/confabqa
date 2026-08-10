"""Phase 2 steps 5-6: the null test + popularity split on TriviaQA, reusing
03_analyze.py's probe pipeline and baseline definitions verbatim.

Computes:
  (a) THE NULL TEST: hidden-state correctness probe peak accuracy vs the
      strongest prompt-feature baseline on the full TriviaQA sample.
      Question: does the +small-margin-within-noise pattern reproduce on
      external data?
  (b) THE POPULARITY QUESTION: split at the median o_pop into low-/high-
      popularity halves; report the correctness probe's margin over its
      prompt baseline SEPARATELY in each half. Sharper question: does the
      hidden state add MORE in the low-popularity half, where the prompt
      is less informative?
  (c) REFUSAL PROBE: only run if >= 30 refusals exist on TriviaQA. TriviaQA is
      mostly answerable static facts so refusals are expected to be rare.

This script does NOT modify the paper's pipeline files. It imports the
existing baseline definitions (prompt_features, prompt_feature_matrix,
tfidf_baseline_for_target, prompt_baseline_for_target, per_layer_probe)
from 03_analyze.py by importlib.

Writes figures/{model_subdir}/triviaqa_generalization.md with:
  - stratum / popularity-bin counts
  - judge spot-check pointer
  - the null-test result on external data
  - the popularity-split margins
  - explicit 'what transferred / what could not be tested here' paragraph.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from config import MODEL_SUBDIR

_HERE = Path(__file__).parent

def _paths_for_suffix(suffix: str):
    return {
        "responses": Path(f"data/triviaqa_sample{suffix}/responses") / MODEL_SUBDIR,
        "activations": Path(f"data/triviaqa_sample{suffix}/activations") / MODEL_SUBDIR,
        "spotcheck": Path("figures") / MODEL_SUBDIR / f"triviaqa{suffix}_judge_spotcheck.md",
        "out_md": Path("figures") / MODEL_SUBDIR / f"triviaqa{suffix}_generalization.md",
        "out_json": Path("figures") / MODEL_SUBDIR / f"triviaqa{suffix}_generalization.json",
    }


# Module-level defaults (overwritten in main() once --suffix is parsed)
_PATHS = _paths_for_suffix("")
TRIVIAQA_RESPONSES_DIR = _PATHS["responses"]
TRIVIAQA_ACTIVATIONS_DIR = _PATHS["activations"]
SPOTCHECK_PATH = _PATHS["spotcheck"]
OUT_MD = _PATHS["out_md"]
OUT_JSON = _PATHS["out_json"]


def load_triviaqa_responses():
    """Load TriviaQA responses + activations into the same dict shape that
    03_analyze.py's load_all() returns, so existing functions Just Work."""
    out = []
    for f in sorted(TRIVIAQA_RESPONSES_DIR.glob("*.json")):
        with open(f) as fp:
            r = json.load(fp)
        act_path = TRIVIAQA_ACTIVATIONS_DIR / f"{r['question_id']}.pt"
        if not act_path.exists():
            continue
        act = torch.load(act_path, weights_only=False)
        r["last_prompt_hidden"] = act["last_prompt_hidden"].numpy()
        r["first_gen_hidden"] = (act["first_gen_hidden"].numpy()
                                  if act["first_gen_hidden"] is not None else None)
        if "judge_label" not in r:
            r["judge_label"] = "correct" if r.get("correct") else "wrong"
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# Probe pipeline -- identical hyperparameters to 03_analyze.py
# ---------------------------------------------------------------------------
def per_layer_correctness_probe(responses):
    """Same StandardScaler -> PCA(16) -> LR -> 5-fold CV as 03_analyze.py."""
    y = np.array([1 if r["correct"] else 0 for r in responses])
    n_layers = responses[0]["last_prompt_hidden"].shape[0]
    accs = np.zeros(n_layers); stds = np.zeros(n_layers)
    for layer in range(n_layers):
        X = np.stack([r["last_prompt_hidden"][layer] for r in responses])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=min(16, len(responses) - 1))),
            ("clf", LogisticRegression(max_iter=2000, C=1.0)),
        ])
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
        accs[layer] = scores.mean(); stds[layer] = scores.std()
    return accs, stds


def per_layer_refusal_probe(responses):
    sub = [r for r in responses if r["judge_label"] in ("refusal", "wrong")]
    if len(sub) < 20 or sum(1 for r in sub if r["judge_label"] == "refusal") < 5:
        return None, None, sub
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
    n_layers = sub[0]["last_prompt_hidden"].shape[0]
    accs = np.zeros(n_layers); stds = np.zeros(n_layers)
    for layer in range(n_layers):
        X = np.stack([r["last_prompt_hidden"][layer] for r in sub])
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=min(16, len(sub) - 1))),
            ("clf", LogisticRegression(max_iter=2000, C=1.0)),
        ])
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
        accs[layer] = scores.mean(); stds[layer] = scores.std()
    return accs, stds, sub


# ---------------------------------------------------------------------------
# Prompt-feature baselines on TriviaQA -- import the exact definitions from
# 03_analyze.py and run them on the y vector from `correct`.
# ---------------------------------------------------------------------------
import re as _re
_YEAR_RE = _re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
_CAP_RE = _re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b")


def prompt_features(r):
    """Exactly 03_analyze.prompt_features (8 numeric + domain + category)."""
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


def tfidf_baseline(sub, y):
    texts = [r["question"] for r in sub]
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95,
                                  sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    return float(cross_val_score(pipe, texts, y, cv=cv, scoring="accuracy").mean())


def engineered_baseline(sub, y, include_category=True, include_domain=True):
    X = prompt_feature_matrix(sub, include_category=include_category,
                                include_domain=include_domain)
    pipe = Pipeline([("scale", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=2000, C=1.0))])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    return float(cross_val_score(pipe, X, y, cv=cv, scoring="accuracy").mean())


def all_baselines(sub, y):
    """Return dict of four baselines + the strongest's name/value."""
    out = {
        "majority": max((y == 1).mean(), (y == 0).mean()),
        "tfidf": tfidf_baseline(sub, y),
        "text_only": engineered_baseline(sub, y, include_domain=False, include_category=False),
        "text_plus_domain": engineered_baseline(sub, y, include_domain=True, include_category=False),
        "text_plus_domain_plus_cat": engineered_baseline(sub, y, include_domain=True, include_category=True),
    }
    strongest_name = max(("tfidf", "text_only", "text_plus_domain", "text_plus_domain_plus_cat"),
                         key=lambda k: out[k])
    out["strongest_name"] = strongest_name
    out["strongest_value"] = out[strongest_name]
    return out


def correctness_probe_peak(responses):
    """5-fold CV correctness probe; return (peak_layer, peak_acc, peak_std,
    full per-layer curve)."""
    accs, stds = per_layer_correctness_probe(responses)
    peak = int(accs.argmax())
    return {
        "peak_layer": peak,
        "peak_acc": float(accs[peak]),
        "peak_std": float(stds[peak]),
        "per_layer_acc": [float(a) for a in accs],
        "per_layer_std": [float(s) for s in stds],
    }


def run_null_test(label, responses):
    """Full pipeline: probe + all four baselines + 'h adds vs strongest'."""
    y = np.array([1 if r["correct"] else 0 for r in responses])
    n_pos = int(y.sum())
    n_neg = int(len(y) - n_pos)
    print(f"  [{label}] n={len(responses)} ({n_pos} correct, {n_neg} wrong)")
    if n_pos < 10 or n_neg < 10:
        return {"label": label, "n": len(responses), "n_pos": n_pos, "n_neg": n_neg,
                "skipped": "fewer than 10 of each class"}
    probe = correctness_probe_peak(responses)
    bl = all_baselines(responses, y)
    margin_pp = (probe["peak_acc"] - bl["strongest_value"]) * 100
    print(f"  [{label}] probe peak L{probe['peak_layer']} = {probe['peak_acc']:.4f} +- {probe['peak_std']:.4f}")
    print(f"  [{label}] baselines: tfidf={bl['tfidf']:.4f}, text={bl['text_only']:.4f}, "
          f"+dom={bl['text_plus_domain']:.4f}, +cat={bl['text_plus_domain_plus_cat']:.4f} "
          f"(majority={bl['majority']:.4f})")
    print(f"  [{label}] strongest baseline = {bl['strongest_name']} = {bl['strongest_value']:.4f}")
    print(f"  [{label}] h adds vs strongest = {margin_pp:+.2f} pp  "
          f"(probe std at peak = {probe['peak_std']*100:.2f} pp)")
    return {
        "label": label, "n": len(responses), "n_pos": n_pos, "n_neg": n_neg,
        "probe": probe, "baselines": bl,
        "h_adds_vs_strongest_pp": margin_pp,
        "within_per_fold_std": abs(margin_pp) <= probe["peak_std"] * 100,
    }


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--suffix", type=str, default="",
                   help="Suffix on data/triviaqa_sample{suffix}/ paths")
    args = p.parse_args()
    global _PATHS, TRIVIAQA_RESPONSES_DIR, TRIVIAQA_ACTIVATIONS_DIR
    global SPOTCHECK_PATH, OUT_MD, OUT_JSON
    _PATHS = _paths_for_suffix(args.suffix)
    TRIVIAQA_RESPONSES_DIR = _PATHS["responses"]
    TRIVIAQA_ACTIVATIONS_DIR = _PATHS["activations"]
    SPOTCHECK_PATH = _PATHS["spotcheck"]
    OUT_MD = _PATHS["out_md"]
    OUT_JSON = _PATHS["out_json"]

    print(f"Loading TriviaQA responses from {TRIVIAQA_RESPONSES_DIR}...")
    responses = load_triviaqa_responses()
    print(f"  loaded {len(responses)} responses\n")
    if not responses:
        print("ERROR: no responses found. Run triviaqa_evaluate.py first.")
        return

    # ---- Distribution check ----
    from collections import Counter
    judge_dist = Counter(r["judge_label"] for r in responses)
    print(f"Judge label distribution: {dict(judge_dist)}")
    # Answer-word-length distribution (TriviaQA has no popularity axis)
    alen_dist = Counter(r.get("triviaqa_answer_word_len") for r in responses)
    print(f"Answer word-length distribution: {dict(sorted(alen_dist.items()))}")
    correct_by_alen = Counter()
    n_by_alen = Counter()
    for r in responses:
        a = r.get("triviaqa_answer_word_len")
        n_by_alen[a] += 1
        if r["correct"]:
            correct_by_alen[a] += 1
    print(f"Per-answer-length correctness:")
    for a in sorted(n_by_alen):
        if n_by_alen[a]:
            print(f"  word_len={a}: {correct_by_alen[a]}/{n_by_alen[a]} = "
                  f"{correct_by_alen[a]/n_by_alen[a]*100:.1f}%")

    # ---- Null test on full sample ----
    print("\n=== NULL TEST (full TriviaQA sample) ===")
    null_full = run_null_test("full", responses)

    # ---- Answer-length split (TriviaQA's nearest analogue to PopQA's popularity axis) ----
    # Shorter answers (1 word) tend to be common entities / well-known facts;
    # longer multi-word answers tend to be more obscure. Not a perfect proxy
    # for popularity but it's the only honest continuous-ish axis available
    # in TriviaQA without joining external data. The median split below.
    print("\n=== ANSWER-LENGTH SPLIT (TriviaQA has no popularity axis) ===")
    alens = sorted(r["triviaqa_answer_word_len"] for r in responses)
    median_alen = alens[len(alens) // 2]
    print(f"  median answer word-length in sample = {median_alen}")
    short_ans = [r for r in responses if r["triviaqa_answer_word_len"] <= median_alen]
    long_ans = [r for r in responses if r["triviaqa_answer_word_len"] > median_alen]
    null_low = run_null_test("short_answer", short_ans) if short_ans else {"label": "short_answer", "skipped": "empty"}
    null_high = run_null_test("long_answer", long_ans) if long_ans else {"label": "long_answer", "skipped": "empty"}

    # ---- Refusal probe (only if >=30 refusals) ----
    n_refusal = judge_dist.get("refusal", 0)
    print(f"\n=== REFUSAL PROBE ===")
    print(f"  refusal count on TriviaQA: {n_refusal}")
    refusal_result = None
    if n_refusal >= 30:
        print("  >= 30 refusals -- running refusal-vs-wrong probe")
        accs, stds, sub = per_layer_refusal_probe(responses)
        peak = int(accs.argmax())
        y_sub = np.array([1 if r["judge_label"] == "refusal" else 0 for r in sub])
        bl = all_baselines(sub, y_sub)
        margin = (accs[peak] - bl["strongest_value"]) * 100
        refusal_result = {
            "n": len(sub),
            "n_refusal": int(y_sub.sum()),
            "n_wrong": int((y_sub == 0).sum()),
            "peak_layer": peak,
            "peak_acc": float(accs[peak]),
            "peak_std": float(stds[peak]),
            "baselines": bl,
            "h_adds_vs_strongest_pp": float(margin),
        }
        print(f"  peak L{peak} acc = {accs[peak]:.4f} +- {stds[peak]:.4f}")
        print(f"  strongest baseline = {bl['strongest_name']} = {bl['strongest_value']:.4f}")
        print(f"  h adds vs strongest = {margin:+.2f} pp")
    else:
        print(f"  < 30 refusals -- refusal probe declared UNDERPOWERED on TriviaQA; skipped.")

    # ---- Render markdown ----
    summary = {
        "n_total": len(responses),
        "judge_label_distribution": dict(judge_dist),
        "answer_word_length_distribution": dict(sorted(alen_dist.items())),
        "per_answer_length_correctness": {a: correct_by_alen[a] / n_by_alen[a]
                                          for a in n_by_alen if n_by_alen[a]},
        "null_test_full": null_full,
        "null_test_short_answer": null_low,
        "null_test_long_answer": null_high,
        "median_answer_word_len": median_alen,
        "refusal_probe": refusal_result,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(summary, fp, indent=2, ensure_ascii=False)
    print(f"\nWrote {OUT_JSON}")

    # Markdown
    md = []
    md.append(f"# TriviaQA generalization check ({MODEL_SUBDIR})\n\n")
    md.append("Phase 2 follow-up to the PopQA replication. Sample: 800 TriviaQA\n")
    md.append("`unfiltered.nocontext` validation items, uniform random with\n")
    md.append("`random.Random(0)`. TriviaQA was the primary closed-book QA dataset\n")
    md.append("Kadavath et al.\\ (2022) leaned on for their P(IK) calibration probe,\n")
    md.append("so this is the most directly comparable head-to-head replication of\n")
    md.append("the null. Pipeline: identical to the v1 paper (greedy decoding,\n")
    md.append("`enable_thinking=False`, last-prompt-token hidden-state pickoff at\n")
    md.append("every layer, `StandardScaler -> PCA(16) -> LogReg` probe with 5-fold\n")
    md.append("CV, same prompt-feature baselines).\n\n")
    md.append("## Sample composition\n\n")
    md.append(f"- n total: {len(responses)}\n")
    md.append(f"- judge labels: {dict(judge_dist)}\n")
    md.append(f"- median answer word-length: {median_alen}\n")
    md.append("- per-answer-length correctness (top 6 most-common lengths):\n\n")
    md.append("| answer word-length | n | correct | accuracy |\n|--:|--:|--:|--:|\n")
    top_lens = sorted(n_by_alen, key=lambda a: -n_by_alen[a])[:6]
    for a in sorted(top_lens):
        md.append(f"| {a} | {n_by_alen[a]} | {correct_by_alen[a]} | "
                  f"{correct_by_alen[a]/n_by_alen[a]*100:.1f}% |\n")
    md.append("\n")

    md.append(f"Judge spot-check: see `{SPOTCHECK_PATH.name}`. **Caveat:** the\n")
    md.append("judge has been calibrated on the v1.0/v1.3 question set (Cohen\n")
    md.append("$\\kappa = 0.892$ on v1.0, Claude $\\kappa = 1.0$ on v1.3), NOT on\n")
    md.append("the TriviaQA distribution. TriviaQA's aliases cover many but not\n")
    md.append("all surface forms; judge errors are unmeasured here and may shift\n")
    md.append("the correctness count by a few pp.\n\n")

    md.append("## (a) The null test on external data\n\n")
    md.append("Hidden-state correctness probe vs. the strongest prompt-feature\n")
    md.append("baseline (max of TF-IDF, engineered text-only, +domain, +category):\n\n")
    md.append("| split | n | probe peak (layer) | strongest baseline | h adds (pp) | within per-fold std? |\n")
    md.append("|---|--:|--:|--:|--:|--:|\n")
    for r in (null_full, null_low, null_high):
        if r.get("skipped"):
            md.append(f"| {r['label']} | {r['n']} | (skipped: {r['skipped']}) | | | |\n")
            continue
        md.append(f"| {r['label']} | {r['n']} | "
                  f"{r['probe']['peak_acc']*100:.2f}% (L{r['probe']['peak_layer']}) | "
                  f"{r['baselines']['strongest_value']*100:.2f}% "
                  f"(`{r['baselines']['strongest_name']}`) | "
                  f"{r['h_adds_vs_strongest_pp']:+.2f} | "
                  f"{'yes' if r['within_per_fold_std'] else 'NO'} |\n")
    md.append("\n")

    md.append("**Full baseline table (TriviaQA full sample, correctness target):**\n\n")
    bl = null_full["baselines"]
    md.append("| metric | value |\n|---|--:|\n")
    md.append(f"| majority baseline | {bl['majority']*100:.2f}% |\n")
    md.append(f"| TF-IDF baseline | {bl['tfidf']*100:.2f}% |\n")
    md.append(f"| engineered text-only | {bl['text_only']*100:.2f}% |\n")
    md.append(f"| +domain | {bl['text_plus_domain']*100:.2f}% |\n")
    md.append(f"| +domain+category | {bl['text_plus_domain_plus_cat']*100:.2f}% |\n")
    md.append(f"| **hidden-state probe peak** | **{null_full['probe']['peak_acc']*100:.2f}%** "
              f"(L{null_full['probe']['peak_layer']}, $\\pm$ {null_full['probe']['peak_std']*100:.2f} pp) |\n")
    md.append(f"| h adds vs strongest | **{null_full['h_adds_vs_strongest_pp']:+.2f} pp** |\n\n")

    md.append("## (b) Answer-length split (TriviaQA's nearest analogue to PopQA's popularity axis)\n\n")
    md.append("TriviaQA has no continuous popularity axis. The nearest available\n")
    md.append("proxy is answer word-length: 1-word answers tend to be common\n")
    md.append("entities (e.g. `Hitler`, `Beethoven`); multi-word answers tend to\n")
    md.append("be more obscure (e.g. specific book titles, niche figures). Not as\n")
    md.append("clean as Wikipedia pageviews, but it's the only continuous-ish\n")
    md.append("axis the dataset provides without a Wikidata join.\n\n")
    if null_low.get("skipped") or null_high.get("skipped"):
        md.append("Skipped (insufficient items in one half).\n\n")
    else:
        delta = (null_low["h_adds_vs_strongest_pp"]
                  - null_high["h_adds_vs_strongest_pp"])
        md.append(f"- short-answer half (word-length $\\le$ {median_alen}): "
                  f"h adds = {null_low['h_adds_vs_strongest_pp']:+.2f} pp\n")
        md.append(f"- long-answer half (word-length $>$ {median_alen}): "
                  f"h adds = {null_high['h_adds_vs_strongest_pp']:+.2f} pp\n")
        md.append(f"- short minus long: {delta:+.2f} pp\n\n")

    md.append("## (c) Refusal probe\n\n")
    if refusal_result is None:
        md.append(f"Refusal count on TriviaQA = **{n_refusal}** (< 30).\n\n")
        md.append("Per the protocol caveat: TriviaQA items are mostly answerable static\n")
        md.append("facts, so refusals are expected to be rare. The refusal-vs-wrong\n")
        md.append("probe is declared **UNDERPOWERED on TriviaQA and skipped**, rather\n")
        md.append("than reporting a noisy number from a tiny positive class.\n\n")
    else:
        md.append(f"Refusal count = {n_refusal} ($\\ge 30$), probe run.\n\n")
        md.append(f"- subset n = {refusal_result['n']} "
                  f"({refusal_result['n_refusal']} refusal, {refusal_result['n_wrong']} wrong)\n")
        md.append(f"- probe peak L{refusal_result['peak_layer']} = "
                  f"{refusal_result['peak_acc']*100:.2f}% $\\pm$ "
                  f"{refusal_result['peak_std']*100:.2f} pp\n")
        md.append(f"- strongest baseline = `{refusal_result['baselines']['strongest_name']}` = "
                  f"{refusal_result['baselines']['strongest_value']*100:.2f}%\n")
        md.append(f"- h adds vs strongest = {refusal_result['h_adds_vs_strongest_pp']:+.2f} pp\n\n")

    md.append("## What transferred / what could not be tested here\n\n")
    md.append("- **Cutoff disconfound: N/A.** TriviaQA is static trivia; the\n")
    md.append("  within-pre/within-obscure disconfound tests from the main paper\n")
    md.append("  cannot be re-run. The full TriviaQA sample is the closest\n")
    md.append("  analogue to the v1 paper's all-items `correct` target.\n")
    md.append("- **Surface-form concern: PARTIAL.** TriviaQA is human-written\n")
    md.append("  trivia, so the question-construction phrasing is less templated\n")
    md.append("  than PopQA's Wikidata-derived prompts, but the questions still\n")
    md.append("  have systematic phrasing patterns (\"Who wrote X\", \"Who played\n")
    md.append("  Y\", etc.) that a TF-IDF baseline can pick up. The point of\n")
    md.append("  running on TriviaQA specifically is that it's the dataset\n")
    md.append("  Kadavath et al.\\ (2022) leaned on for their P(IK) probe -- so\n")
    md.append("  the head-to-head is on the original claim's home turf.\n")
    if refusal_result is None:
        md.append("- **Refusal probe: NOT TESTED.** TriviaQA items are mostly\n")
        md.append("  answerable, refusals are rare; the refusal-vs-wrong probe is\n")
        md.append("  underpowered on this data. The v1 paper's refusal positive\n")
        md.append("  result is neither corroborated nor challenged here.\n")
    md.append("- **Judge calibration on TriviaQA: UNVALIDATED.** The same-model\n")
    md.append("  judge has been calibrated on v1.0/v1.3 but not on TriviaQA. Spot-\n")
    md.append("  check pack provided for visual inspection only.\n")

    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")
    print("\nPHASE 2 COMPLETE. Awaiting your review.")


if __name__ == "__main__":
    main()
