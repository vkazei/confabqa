"""Compare TriviaQA seed=0 and seed=1 runs side by side.

Reads the two generalization JSONs produced by triviaqa_analyze.py (with
suffixes '' and '_seed1') and prints + writes a comparison report.

Question being answered: is the seed=0 pattern (TF-IDF below majority,
probe +5pp at ~2σ over the strongest prompt baseline) a stable property of
TriviaQA-on-Qwen3-1.7B, or is it sample-specific?
"""
from __future__ import annotations

import json
from pathlib import Path

from config import MODEL_SUBDIR

FIG_DIR = Path("figures") / MODEL_SUBDIR
OUT_MD = FIG_DIR / "triviaqa_seed_comparison.md"


def load(suffix):
    p = FIG_DIR / f"triviaqa{suffix}_generalization.json"
    if not p.exists():
        raise SystemExit(f"Missing: {p}. Run triviaqa_analyze.py --suffix {suffix!r} first.")
    return json.load(open(p))


def row(label, a, b):
    return f"| {label} | {a} | {b} |"


def fmt_pct(x):
    return f"{x*100:.2f}%"


def main():
    s0 = load("")
    s1 = load("_seed1")

    a_null = s0["null_test_full"]
    b_null = s1["null_test_full"]
    a_bl = a_null["baselines"]
    b_bl = b_null["baselines"]

    lines = []
    lines.append("# TriviaQA seed=0 vs seed=1 comparison\n")
    lines.append(
        f"Same pipeline, same model ({MODEL_SUBDIR}), same hyperparameters; "
        "the only difference is `random.Random(seed)` for the 800-item sample "
        "from `mandarjoshi/trivia_qa unfiltered.nocontext` (validation split, "
        "n=11313 total). Overlap between samples is small (~7%).\n\n"
    )
    lines.append("## Sample composition\n\n")
    lines.append("| metric | seed=0 | seed=1 |\n|---|--:|--:|\n")
    lines.append(row("n", s0["n_total"], s1["n_total"]) + "\n")
    j0, j1 = s0["judge_label_distribution"], s1["judge_label_distribution"]
    lines.append(row("correct", j0.get("correct", 0), j1.get("correct", 0)) + "\n")
    lines.append(row("refusal", j0.get("refusal", 0), j1.get("refusal", 0)) + "\n")
    lines.append(row("wrong",   j0.get("wrong", 0),   j1.get("wrong", 0)) + "\n")

    lines.append("\n## Full-sample null test\n\n")
    lines.append("| metric | seed=0 | seed=1 |\n|---|--:|--:|\n")
    lines.append(row("majority baseline", fmt_pct(a_bl["majority"]), fmt_pct(b_bl["majority"])) + "\n")
    lines.append(row("TF-IDF", fmt_pct(a_bl["tfidf"]), fmt_pct(b_bl["tfidf"])) + "\n")
    lines.append(row("**TF-IDF − majority**",
                     f"{(a_bl['tfidf']-a_bl['majority'])*100:+.2f} pp",
                     f"{(b_bl['tfidf']-b_bl['majority'])*100:+.2f} pp") + "\n")
    lines.append(row("text-only", fmt_pct(a_bl["text_only"]), fmt_pct(b_bl["text_only"])) + "\n")
    lines.append(row("+domain", fmt_pct(a_bl["text_plus_domain"]),
                     fmt_pct(b_bl["text_plus_domain"])) + "\n")
    lines.append(row("+category", fmt_pct(a_bl["text_plus_domain_plus_cat"]),
                     fmt_pct(b_bl["text_plus_domain_plus_cat"])) + "\n")
    lines.append(row("strongest baseline (name)",
                     f"`{a_bl['strongest_name']}` ({fmt_pct(a_bl['strongest_value'])})",
                     f"`{b_bl['strongest_name']}` ({fmt_pct(b_bl['strongest_value'])})") + "\n")
    lines.append(row("hidden-state probe peak",
                     f"{fmt_pct(a_null['probe']['peak_acc'])} (L{a_null['probe']['peak_layer']})",
                     f"{fmt_pct(b_null['probe']['peak_acc'])} (L{b_null['probe']['peak_layer']})") + "\n")
    lines.append(row("probe std at peak",
                     f"{a_null['probe']['peak_std']*100:.2f} pp",
                     f"{b_null['probe']['peak_std']*100:.2f} pp") + "\n")
    lines.append(row("**h adds vs strongest**",
                     f"**{a_null['h_adds_vs_strongest_pp']:+.2f} pp**",
                     f"**{b_null['h_adds_vs_strongest_pp']:+.2f} pp**") + "\n")
    lines.append(row("within per-fold std?",
                     "yes" if a_null["within_per_fold_std"] else "NO",
                     "yes" if b_null["within_per_fold_std"] else "NO") + "\n")

    lines.append("\n## Read of the comparison\n\n")
    tfidf_drop_0 = (a_bl["tfidf"] - a_bl["majority"]) * 100
    tfidf_drop_1 = (b_bl["tfidf"] - b_bl["majority"]) * 100
    h_0 = a_null["h_adds_vs_strongest_pp"]
    h_1 = b_null["h_adds_vs_strongest_pp"]

    if tfidf_drop_0 < 0 and tfidf_drop_1 < 0:
        lines.append(f"- TF-IDF below majority on BOTH seeds ({tfidf_drop_0:+.2f} pp / "
                     f"{tfidf_drop_1:+.2f} pp). The pattern reproduces -- prompt-bigram\n")
        lines.append("  features carry no predictive signal about correctness on TriviaQA\n")
        lines.append("  for this model.\n")
    elif tfidf_drop_0 < 0 or tfidf_drop_1 < 0:
        lines.append(f"- TF-IDF below majority on one seed but not the other "
                     f"({tfidf_drop_0:+.2f} vs {tfidf_drop_1:+.2f} pp). The seed=0\n")
        lines.append("  result was at least partly sample-specific; the TF-IDF baseline\n")
        lines.append("  hovers right around majority on TriviaQA but isn't reliably below it.\n")
    else:
        lines.append(f"- TF-IDF beats majority on both seeds ({tfidf_drop_0:+.2f} / "
                     f"{tfidf_drop_1:+.2f} pp). The seed=0 below-majority TF-IDF was\n")
        lines.append("  sample-specific.\n")

    if abs(h_0 - h_1) <= 1.5:
        lines.append(f"- Hidden-state margin over strongest baseline: {h_0:+.2f} pp (seed=0) vs "
                     f"{h_1:+.2f} pp (seed=1). Difference ({h_0 - h_1:+.2f} pp) is small\n")
        lines.append("  -- the margin reproduces.\n")
    else:
        lines.append(f"- Hidden-state margin over strongest baseline differs noticeably: "
                     f"{h_0:+.2f} pp (seed=0) vs {h_1:+.2f} pp (seed=1).\n")
        lines.append(f"  Difference of {h_0 - h_1:+.2f} pp suggests the +5pp / 2σ result is\n")
        lines.append("  partly sample-noise.\n")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("".join(lines))
    print("".join(lines))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
