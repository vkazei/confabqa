"""Phase 1: descriptive inspection of the prompt-feature baselines.

For each of three correctness targets (correct, correct_within_pre,
correct_within_obscure), refit the four baselines defined in 03_analyze.py
on the SAME cached responses and report what the classifier is keying on:

  (a) TF-IDF baseline: top-30 positive and top-30 negative LR coefficients
      with their token strings, plus a heuristic tag per token
      (YEAR/DATE, TEMPLATE-STRUCTURAL, ENTITY-NAME, CONTENT-WORD, TOKENIZER-ARTIFACT).

  (b) Engineered baselines: standardized coefficient magnitudes per named
      feature (has_year, year_value, char_length, word_count, capwords,
      digits, commas, ends_q, each domain dummy, each category dummy).

This script is descriptive only. It does NOT modify the existing pipeline
files or any cached data; it reuses the function definitions from
03_analyze.py by import. Writes figures/baseline_inspection.md and prints
the obscure-cell verdict + token tables to stdout.

The four baseline pipelines mirror 03_analyze.py exactly:
  TF-IDF: TfidfVectorizer(ngram_range=(1,2), min_df=2, max_df=0.95,
          sublinear_tf=True) + LogisticRegression(max_iter=2000, C=1.0).
  Engineered: StandardScaler + LogisticRegression(max_iter=2000, C=1.0)
          on the prompt_feature_matrix output (8 numeric features +
          optional domain/category one-hot dummies).
The classifiers are refit on the FULL subset (no held-out fold) to
extract coefficients; the CV accuracy column at the top of each section
matches the 5-fold CV-mean reported in data/qwen3_1_7b_summary.json.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Import 03_analyze.py as a module (its filename starts with a digit).
_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location("analyze", _HERE / "03_analyze.py")
_AN = importlib.util.module_from_spec(_SPEC)
sys.modules["analyze"] = _AN
_SPEC.loader.exec_module(_AN)

# Pull in the exact feature definitions from the paper's pipeline:
from analyze import load_all, prompt_features, prompt_feature_matrix  # type: ignore
from config import FIGURES_DIR

TARGETS = ["correct", "correct_within_pre", "correct_within_obscure"]
OUT_MD = FIGURES_DIR / "baseline_inspection.md"

# ---------------------------------------------------------------------------
# Target subsetting (matches 03_analyze.py exactly)
# ---------------------------------------------------------------------------
def subset_and_y(responses, target):
    if target == "correct":
        sub = list(responses)
    elif target == "correct_within_pre":
        sub = [r for r in responses if r["cutoff_class"] == "pre"]
    elif target == "correct_within_obscure":
        sub = [r for r in responses if r.get("category") == "obscure"]
    else:
        raise ValueError(target)
    y = np.array([1 if r["correct"] else 0 for r in sub])
    return sub, y


# ---------------------------------------------------------------------------
# Heuristic tagger for TF-IDF tokens
# ---------------------------------------------------------------------------
_YEAR_RE = re.compile(r"^(1[89]\d{2}|20\d{2})$")          # 4-digit year
_YEAR_NGRAM_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")  # year inside an n-gram

# Template-structural phrasing used in the source files: "former X", "deputy Y",
# "runner-up at Z", "first to do W", "won the Nobel Prize in...", etc.
_TEMPLATE_WORDS = {
    "former", "deputy", "runner", "runnerup", "first", "second", "third",
    "latest", "most", "recent", "previous", "prior", "earliest", "the",
    "won", "winner", "winning", "wins", "prize", "award", "awarded",
    "released", "release", "directed", "director", "starred", "starring",
    "writer", "wrote", "authored", "published", "novel", "album", "film",
    "movie", "song", "single", "track", "ceremony", "edition", "event",
    "year", "month", "january", "february", "march", "april", "may",
    "june", "july", "august", "september", "october", "november", "december",
    "spring", "summer", "fall", "autumn", "winter",
    "succeeded", "succeed", "became", "elected", "appointed", "confirmed",
    "sworn", "inaugurated", "resigned", "stepped",
    "no", "not", "did", "didn't", "didnt", "after", "before", "during",
}

# Code/tokenizer artifacts a TF-IDF on chat-template-stripped text shouldn't
# produce often, but flag obvious ones if they show up.
_ARTIFACT_RE = re.compile(r"^[\W_]+$|^[a-z]{1,2}$|^_+\w*|<\|.*\|>")

# A small content-word stoplist (we don't tag stopwords as CONTENT-WORD).
_STOPWORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "has", "have",
    "in", "is", "it", "its", "of", "on", "or", "that", "the", "to", "was",
    "were", "which", "who", "with", "what", "where", "when", "how", "why",
    "this", "these", "those", "their", "his", "her", "he", "she", "they",
    "i", "you", "we", "us", "him", "them", "do", "does", "did", "but",
    "if", "then", "so", "than", "such", "also", "very", "into", "out",
    "up", "down", "over", "under", "above", "below",
}


def tag_token(tok: str) -> str:
    """Tag a TF-IDF token (unigram or bigram) heuristically."""
    parts = tok.split()
    # YEAR / DATE: any 4-digit year token
    if any(_YEAR_NGRAM_RE.search(p) for p in parts):
        return "YEAR/DATE"
    # TOKENIZER-ARTIFACT: pure punctuation or single-letter/short fragments
    if all(_ARTIFACT_RE.match(p) for p in parts):
        return "TOKENIZER-ARTIFACT"
    lower_parts = [p.lower().strip(".,!?;:'\"()[]{}") for p in parts]
    # TEMPLATE-STRUCTURAL: any template-vocabulary word present
    if any(p in _TEMPLATE_WORDS for p in lower_parts):
        return "TEMPLATE-STRUCTURAL"
    # ENTITY-NAME: starts with a capital letter, not in stopwords
    if all(p and p[0].isupper() and p.lower() not in _STOPWORDS for p in parts if p):
        return "ENTITY-NAME"
    # CONTENT-WORD: lowercase or mixed-case word that is not a stopword
    nonstop = [p for p in lower_parts if p and p not in _STOPWORDS]
    if nonstop:
        return "CONTENT-WORD"
    return "TOKENIZER-ARTIFACT"


# ---------------------------------------------------------------------------
# TF-IDF inspection: refit on the full subset, extract top coefficients
# ---------------------------------------------------------------------------
def inspect_tfidf(sub, y, target, top_k=30):
    texts = [r["question"] for r in sub]
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.95,
                                  sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=2000, C=1.0)),
    ])
    # 5-fold CV acc for the header (matches the paper).
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    cv_acc = cross_val_score(pipe, texts, y, cv=cv, scoring="accuracy").mean()
    # Fit on the full subset to extract coefficients.
    pipe.fit(texts, y)
    vocab = pipe.named_steps["tfidf"].get_feature_names_out()
    coef = pipe.named_steps["clf"].coef_[0]
    order_pos = np.argsort(-coef)[:top_k]
    order_neg = np.argsort(coef)[:top_k]
    top_pos = [(vocab[i], float(coef[i]), tag_token(vocab[i])) for i in order_pos]
    top_neg = [(vocab[i], float(coef[i]), tag_token(vocab[i])) for i in order_neg]
    return {
        "target": target, "n": len(y), "n_pos": int(y.sum()),
        "cv_acc": float(cv_acc),
        "n_features": int(len(vocab)),
        "top_positive": top_pos, "top_negative": top_neg,
    }


# ---------------------------------------------------------------------------
# Engineered inspection: refit each variant on the full subset, report
# standardized coefficient magnitudes per named feature.
# ---------------------------------------------------------------------------
NUMERIC_KEYS = ["q_char_len", "q_word_len", "has_year", "year_value",
                "n_capwords", "n_digits", "n_commas", "ends_questionmark"]


def feature_names(sub, include_domain, include_category):
    feats = [prompt_features(r) for r in sub]
    domains = sorted({f["domain"] for f in feats})
    cats = sorted({f["category"] for f in feats})
    names = list(NUMERIC_KEYS)
    if include_domain:
        names += [f"domain={d}" for d in domains]
    if include_category:
        names += [f"category={c}" for c in cats]
    return names


def inspect_engineered(sub, y, target, include_domain, include_category, tag):
    X = prompt_feature_matrix(sub, include_category=include_category,
                                include_domain=include_domain)
    names = feature_names(sub, include_domain, include_category)
    pipe = Pipeline([("scale", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=2000, C=1.0))])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    cv_acc = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy").mean()
    pipe.fit(X, y)
    coef = pipe.named_steps["clf"].coef_[0]
    pairs = sorted(zip(names, coef.tolist()), key=lambda kv: -abs(kv[1]))
    return {
        "target": target, "tag": tag, "n": len(y), "n_pos": int(y.sum()),
        "cv_acc": float(cv_acc),
        "coef_by_magnitude": [(n, float(c)) for n, c in pairs],
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------
def fmt_tfidf_table(result, side="positive"):
    rows = result["top_positive"] if side == "positive" else result["top_negative"]
    sign = "+" if side == "positive" else "-"
    lines = [f"| rank | token | coef | tag |", f"|--:|---|--:|---|"]
    for i, (tok, c, tag) in enumerate(rows, start=1):
        # escape pipes inside tokens
        safe = tok.replace("|", "\\|").replace("`", "\\`")
        lines.append(f"| {i} | `{safe}` | {sign if side=='positive' else ''}{c:+.3f} | {tag} |"
                     .replace(f"{sign}+", "+").replace(f"{sign}-", "-"))
    return "\n".join(lines)


def fmt_engineered_table(result):
    lines = [f"| feature | coef (standardized) | |coef| |", f"|---|--:|--:|"]
    for name, c in result["coef_by_magnitude"]:
        lines.append(f"| `{name}` | {c:+.4f} | {abs(c):.4f} |")
    return "\n".join(lines)


def render_markdown(tfidf_results, eng_results):
    out = []
    out.append("# Baseline inspection: what the prompt-feature classifiers key on\n")
    out.append("Phase 1 descriptive analysis. The four baselines below are refit on\n")
    out.append("the same cached `data/responses/qwen3_1_7b/` items as the paper,\n")
    out.append("using the same Pipeline definitions taken verbatim from\n")
    out.append("`03_analyze.py`. 5-fold CV accuracy column matches the paper's\n")
    out.append("`data/qwen3_1_7b_summary.json` numbers. Coefficients are extracted\n")
    out.append("from a single refit on the full subset (no held-out fold).\n\n")
    out.append("**Heuristic tag legend:**\n")
    out.append("- `YEAR/DATE` — 4-digit year token (e.g. `1978`, `in 2024`).\n")
    out.append("- `TEMPLATE-STRUCTURAL` — phrasing baked into the question template\n")
    out.append("  (e.g. `former`, `deputy`, `runner-up`, `first`, `latest`, month\n")
    out.append("  names, `won`, `released`, `directed`, `who`).\n")
    out.append("- `ENTITY-NAME` — capitalized word(s) that aren't in the structural\n")
    out.append("  vocabulary (proper nouns).\n")
    out.append("- `CONTENT-WORD` — lowercase content word not in stopwords/template\n")
    out.append("  vocabulary (e.g. `protein`, `album`).\n")
    out.append("- `TOKENIZER-ARTIFACT` — punctuation, single letters, or pure\n")
    out.append("  symbols.\n\n")
    out.append("Tag classification is heuristic and the raw token list is shown so\n")
    out.append("the reader can re-judge any borderline call.\n\n")

    for tfres in tfidf_results:
        t = tfres["target"]
        out.append(f"---\n\n## Target: `{t}`\n\n")
        out.append(f"n={tfres['n']} ({tfres['n_pos']} positive); "
                   f"TF-IDF vocabulary size={tfres['n_features']}; "
                   f"TF-IDF 5-fold CV acc = {tfres['cv_acc']:.4f}\n\n")

        # Tag summary (positive coefficients)
        tag_counts_pos = {}
        for _, _, tag in tfres["top_positive"]:
            tag_counts_pos[tag] = tag_counts_pos.get(tag, 0) + 1
        tag_counts_neg = {}
        for _, _, tag in tfres["top_negative"]:
            tag_counts_neg[tag] = tag_counts_neg.get(tag, 0) + 1
        out.append(f"**Tag distribution in top 30 positive tokens:** ")
        out.append(", ".join(f"{k}={v}" for k, v in sorted(tag_counts_pos.items(),
                                                            key=lambda kv: -kv[1])))
        out.append("\n\n")
        out.append(f"**Tag distribution in top 30 negative tokens:** ")
        out.append(", ".join(f"{k}={v}" for k, v in sorted(tag_counts_neg.items(),
                                                            key=lambda kv: -kv[1])))
        out.append("\n\n")

        out.append("### Top 30 positive (predict CORRECT)\n\n")
        out.append(fmt_tfidf_table(tfres, "positive") + "\n\n")
        out.append("### Top 30 negative (predict WRONG)\n\n")
        out.append(fmt_tfidf_table(tfres, "negative") + "\n\n")

        # Engineered for this target
        out.append("### Engineered baselines (standardized coefficient magnitudes)\n\n")
        for engres in eng_results:
            if engres["target"] != t:
                continue
            out.append(f"**`{engres['tag']}` baseline** "
                       f"(n={engres['n']}; CV acc = {engres['cv_acc']:.4f})\n\n")
            out.append(fmt_engineered_table(engres) + "\n\n")

    return "".join(out)


def verdict_obscure(tfidf_results):
    """Plain-English verdict on `correct_within_obscure` specifically."""
    obs = next(r for r in tfidf_results if r["target"] == "correct_within_obscure")
    pos = obs["top_positive"]
    neg = obs["top_negative"]
    all_tokens = pos + neg
    tag_counts = {}
    for _, _, tag in all_tokens:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    total = len(all_tokens)
    pct = {k: v / total for k, v in tag_counts.items()}
    artifact_share = (pct.get("YEAR/DATE", 0) +
                       pct.get("TEMPLATE-STRUCTURAL", 0) +
                       pct.get("TOKENIZER-ARTIFACT", 0))
    content_share = (pct.get("CONTENT-WORD", 0) + pct.get("ENTITY-NAME", 0))
    if artifact_share > 0.5:
        verdict = (
            "VERDICT: the TF-IDF baseline on `correct_within_obscure` is "
            "primarily riding CONSTRUCTION ARTIFACTS (year/date tokens, "
            "template-structural phrasing, tokenizer fragments). The current "
            "framing 'prompt encodes the answer' should be softened to 'prompt "
            "encodes ANSWERABILITY, partly via construction artifacts': the "
            "baseline wins not because the prompt text contains the answer, but "
            "because the question's surface form leaks how hard the question is "
            "to answer."
        )
    elif content_share > 0.5:
        verdict = (
            "VERDICT: the TF-IDF baseline on `correct_within_obscure` is "
            "primarily keying on CONTENT WORDS / ENTITY NAMES rather than "
            "construction artifacts. The surface signal looks semantically "
            "meaningful, so the existing framing 'prompt encodes the answer' "
            "is defensible -- the baseline is recovering something about the "
            "specific facts in the question, not template noise."
        )
    else:
        verdict = (
            "VERDICT: mixed signal. The top TF-IDF tokens on "
            "`correct_within_obscure` are split between construction artifacts "
            f"({artifact_share:.0%}) and content words ({content_share:.0%}); "
            "neither dominates the top 60 tokens. The framing decision is a "
            "judgment call -- the safer move is the softer phrasing."
        )
    return verdict, tag_counts, pct


def main():
    print("Loading cached responses (qwen3_1_7b)...")
    responses = load_all()
    print(f"  loaded {len(responses)} responses\n")

    tfidf_results = []
    eng_results = []

    for target in TARGETS:
        sub, y = subset_and_y(responses, target)
        print(f"== {target}: n={len(sub)} ({int(y.sum())} positive) ==")
        # TF-IDF
        tf = inspect_tfidf(sub, y, target)
        tfidf_results.append(tf)
        print(f"   TF-IDF: CV acc = {tf['cv_acc']:.4f}, vocab = {tf['n_features']}")
        # Engineered (3 variants)
        for tag, kw in [
            ("text_only", dict(include_domain=False, include_category=False)),
            ("text_plus_domain", dict(include_domain=True, include_category=False)),
            ("text_plus_domain_plus_cat", dict(include_domain=True, include_category=True)),
        ]:
            eng = inspect_engineered(sub, y, target, tag=tag, **kw)
            eng_results.append(eng)
            print(f"   {tag}: CV acc = {eng['cv_acc']:.4f}")
        print()

    md = render_markdown(tfidf_results, eng_results)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_MD, "w") as fp:
        fp.write(md)
    print(f"Wrote {OUT_MD}")

    verdict, tag_counts, pct = verdict_obscure(tfidf_results)
    # Also append the verdict to the md
    with open(OUT_MD, "a") as fp:
        fp.write("---\n\n## Verdict: `correct_within_obscure`\n\n")
        fp.write("**Tag distribution across top 60 tokens (pos + neg) for the obscure cell:**\n\n")
        fp.write("| tag | count | share |\n|---|--:|--:|\n")
        for k, v in sorted(tag_counts.items(), key=lambda kv: -kv[1]):
            fp.write(f"| {k} | {v} | {pct[k]:.1%} |\n")
        fp.write(f"\n{verdict}\n")

    # ---- Stdout: print obscure-cell tables + verdict for the reviewer pause ----
    print("\n" + "=" * 72)
    print(" PHASE 1 PAUSE -- correct_within_obscure: top tokens + verdict")
    print("=" * 72)
    obs = next(r for r in tfidf_results if r["target"] == "correct_within_obscure")
    print(f"\nn={obs['n']}, positive={obs['n_pos']}, "
          f"TF-IDF CV acc = {obs['cv_acc']:.4f}, vocab = {obs['n_features']}\n")
    print("Top 30 POSITIVE tokens (predict CORRECT on obscure pre-cutoff items):")
    print(f"  {'rank':>4}  {'coef':>8}  {'tag':<24}  token")
    for i, (tok, c, tag) in enumerate(obs["top_positive"], start=1):
        print(f"  {i:>4}  {c:+8.3f}  {tag:<24}  {tok!r}")
    print("\nTop 30 NEGATIVE tokens (predict WRONG on obscure pre-cutoff items):")
    print(f"  {'rank':>4}  {'coef':>8}  {'tag':<24}  token")
    for i, (tok, c, tag) in enumerate(obs["top_negative"], start=1):
        print(f"  {i:>4}  {c:+8.3f}  {tag:<24}  {tok!r}")
    print("\nTag distribution across top 60 tokens (pos + neg) for the obscure cell:")
    for k, v in sorted(tag_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<22} {v:>3}  ({pct[k]:.1%})")
    print("\n" + verdict)
    print("\nFull report: " + str(OUT_MD))
    print("\nPAUSED. Awaiting review before starting Phase 2 (PopQA generalization).")


if __name__ == "__main__":
    main()
