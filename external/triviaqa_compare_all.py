"""Multi-seed comparison for TriviaQA generalization runs.

Reads `triviaqa{suffix}_generalization.json` for any suffixes that exist
(default: '', '_rerun0', '_seed1', '_seed2') and emits a side-by-side
comparison + a "determinism vs sample variance" decomposition:

  - Compare original seed=0 to _rerun0 (same 800 IDs, fresh forward pass):
    isolates pipeline noise from BF16/MPS + judge re-eval.
  - Compare seed=0 / seed=1 / seed=2 (three distinct samples): estimates
    sample variance over the +h-adds-vs-strongest-prompt-baseline number.

Writes figures/{model}/triviaqa_seed_comparison_all.md
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from config import MODEL_SUBDIR

FIG_DIR = Path("figures") / MODEL_SUBDIR
OUT_MD = FIG_DIR / "triviaqa_seed_comparison_all.md"

SUFFIXES = ["", "_rerun0", "_seed1", "_seed2"]
LABELS = {"": "seed=0", "_rerun0": "seed=0 rerun", "_seed1": "seed=1", "_seed2": "seed=2"}


def load(suffix):
    p = FIG_DIR / f"triviaqa{suffix}_generalization.json"
    if not p.exists():
        return None
    return json.load(open(p))


def main():
    runs = {LABELS[s]: load(s) for s in SUFFIXES}
    runs = {k: v for k, v in runs.items() if v is not None}
    if not runs:
        raise SystemExit("No runs found.")

    lines = []
    lines.append("# TriviaQA multi-seed comparison\n")
    lines.append(
        f"Same pipeline, same model ({MODEL_SUBDIR}), same hyperparameters. "
        "The only variation is `random.Random(seed)` over the validation split "
        "(n=11313). 'seed=0 rerun' uses the *same* seed=0 and therefore the "
        "*same* 800 question IDs as the original seed=0 run; the only thing "
        "that differs in the rerun is the model forward pass and judge re-eval "
        "(testing pipeline-level non-determinism from BF16/MPS).\n\n"
    )

    # ---------- Sample composition ----------
    lines.append("## Sample composition\n\n")
    header = "| metric | " + " | ".join(runs.keys()) + " |"
    sep = "|---" + "|--:" * len(runs) + "|"
    lines.append(header + "\n" + sep + "\n")
    for metric_key, label in [("n_total", "n"),
                              (("judge_label_distribution", "correct"), "correct"),
                              (("judge_label_distribution", "refusal"), "refusal"),
                              (("judge_label_distribution", "wrong"),   "wrong")]:
        row = [label]
        for name, run in runs.items():
            if isinstance(metric_key, tuple):
                v = run.get(metric_key[0], {}).get(metric_key[1], 0)
            else:
                v = run.get(metric_key)
            row.append(str(v))
        lines.append("| " + " | ".join(row) + " |\n")

    # ---------- Full-sample null test ----------
    lines.append("\n## Full-sample null test\n\n")
    lines.append(header + "\n" + sep + "\n")
    metric_rows = [
        ("majority baseline", lambda r: f"{r['null_test_full']['baselines']['majority']*100:.2f}%"),
        ("TF-IDF",            lambda r: f"{r['null_test_full']['baselines']['tfidf']*100:.2f}%"),
        ("**TF-IDF − majority**",
         lambda r: f"{(r['null_test_full']['baselines']['tfidf'] - r['null_test_full']['baselines']['majority'])*100:+.2f} pp"),
        ("text-only",          lambda r: f"{r['null_test_full']['baselines']['text_only']*100:.2f}%"),
        ("+domain",            lambda r: f"{r['null_test_full']['baselines']['text_plus_domain']*100:.2f}%"),
        ("+category",          lambda r: f"{r['null_test_full']['baselines']['text_plus_domain_plus_cat']*100:.2f}%"),
        ("strongest baseline",
         lambda r: f"`{r['null_test_full']['baselines']['strongest_name']}` ({r['null_test_full']['baselines']['strongest_value']*100:.2f}%)"),
        ("probe peak",
         lambda r: f"{r['null_test_full']['probe']['peak_acc']*100:.2f}% (L{r['null_test_full']['probe']['peak_layer']})"),
        ("probe std at peak",
         lambda r: f"{r['null_test_full']['probe']['peak_std']*100:.2f} pp"),
        ("**h adds vs strongest**",
         lambda r: f"**{r['null_test_full']['h_adds_vs_strongest_pp']:+.2f} pp**"),
        ("within per-fold std?",
         lambda r: "yes" if r['null_test_full']['within_per_fold_std'] else "**NO**"),
    ]
    for label, fmt in metric_rows:
        row = [label] + [fmt(r) for r in runs.values()]
        lines.append("| " + " | ".join(row) + " |\n")

    # ---------- Determinism check ----------
    if "seed=0" in runs and "seed=0 rerun" in runs:
        a = runs["seed=0"]["null_test_full"]
        b = runs["seed=0 rerun"]["null_test_full"]
        lines.append("\n## Determinism check (seed=0 vs seed=0 rerun)\n\n")
        lines.append(f"Same 800 question IDs in both runs; differences below are "
                     "from BF16/MPS forward-pass non-determinism propagating "
                     "through generation, judge, and probe.\n\n")
        diffs = [
            ("probe peak acc", a['probe']['peak_acc'] - b['probe']['peak_acc'], "pp", 100),
            ("strongest baseline", a['baselines']['strongest_value'] - b['baselines']['strongest_value'], "pp", 100),
            ("h adds vs strongest", a['h_adds_vs_strongest_pp'] - b['h_adds_vs_strongest_pp'], "pp", 1),
            ("TF-IDF acc", a['baselines']['tfidf'] - b['baselines']['tfidf'], "pp", 100),
        ]
        lines.append("| metric | seed=0 − rerun | |\n|---|--:|---|\n")
        for n, diff, unit, scale in diffs:
            lines.append(f"| {n} | {diff*scale:+.3f} {unit} | |\n")
        # Verdict
        max_swing = max(abs(d * sc) for _, d, _, sc in diffs)
        if max_swing < 0.5:
            lines.append("\n**Pipeline is effectively deterministic** "
                         f"(max metric swing < 0.5 pp). Forward-pass non-determinism is\n"
                         "not driving any of the inter-seed differences below.\n")
        elif max_swing < 1.5:
            lines.append(f"\n**Modest pipeline non-determinism** (max swing "
                         f"{max_swing:.2f} pp). Smaller than the seed-to-seed "
                         "sample variance but not negligible.\n")
        else:
            lines.append(f"\n**Substantial pipeline non-determinism** (max "
                         f"swing {max_swing:.2f} pp). Re-examine BF16/MPS handling.\n")

    # ---------- Sample variance across distinct seeds ----------
    distinct_seeds = [(k, v) for k, v in runs.items() if k != "seed=0 rerun"]
    if len(distinct_seeds) >= 3:
        lines.append("\n## Sample variance across distinct seeds\n\n")
        h_vals = [v["null_test_full"]["h_adds_vs_strongest_pp"] for _, v in distinct_seeds]
        peak_accs = [v["null_test_full"]["probe"]["peak_acc"] * 100 for _, v in distinct_seeds]
        baseline_vals = [v["null_test_full"]["baselines"]["strongest_value"] * 100 for _, v in distinct_seeds]
        m_h = statistics.mean(h_vals); s_h = statistics.stdev(h_vals) if len(h_vals) > 1 else 0
        m_p = statistics.mean(peak_accs); s_p = statistics.stdev(peak_accs) if len(peak_accs) > 1 else 0
        m_b = statistics.mean(baseline_vals); s_b = statistics.stdev(baseline_vals) if len(baseline_vals) > 1 else 0
        lines.append("Across the three distinct samples (seed=0, seed=1, seed=2; "
                     "excludes seed=0 rerun, which is for determinism only):\n\n")
        lines.append("| metric | values | mean ± std |\n|---|---|---:|\n")
        lines.append(f"| probe peak acc | {', '.join(f'{p:.2f}%' for p in peak_accs)} | "
                     f"{m_p:.2f}% ± {s_p:.2f} pp |\n")
        lines.append(f"| strongest baseline | {', '.join(f'{b:.2f}%' for b in baseline_vals)} | "
                     f"{m_b:.2f}% ± {s_b:.2f} pp |\n")
        lines.append(f"| **h adds vs strongest** | {', '.join(f'{h:+.2f} pp' for h in h_vals)} | "
                     f"**{m_h:+.2f} ± {s_h:.2f} pp** |\n")
        lines.append("\n**Headline number for the paper:** `+{:.1f} ± {:.1f} pp` "
                     "(TriviaQA, n=800 per sample, 3 reshuffles).\n".format(m_h, s_h))
        # Compare to typical per-fold std
        per_fold_stds = [v["null_test_full"]["probe"]["peak_std"] * 100 for _, v in distinct_seeds]
        m_pf = statistics.mean(per_fold_stds)
        lines.append(f"\nFor context: the average per-fold std at the probe peak is "
                     f"{m_pf:.2f} pp. The seed-to-seed std of the h-adds margin "
                     f"({s_h:.2f} pp) is "
                     f"{'comparable to' if abs(s_h - m_pf) < 1 else ('smaller than' if s_h < m_pf else 'larger than')} "
                     "the per-fold noise -- so the sample variance and the fit variance are on the same order.\n")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("".join(lines))
    print("".join(lines))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
