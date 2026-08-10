"""Post-hoc analysis of the causal-intervention sweep.

Reads figures/13_intervention_results.json (produced by make_causal_intervention.py)
and computes, per (subset, alpha):

  1. Final judge-label refusal rate (the strict, header-line measure).
  2. First-token flip rate: fraction of items whose generated answer opens with
     one of the refusal-opener tokens (' as', 'As', ' there', ' There', '作为',
     '作为一个', '作為'). Catches cases where intervention nudges the first token
     to a refusal opener even if the autoregressive continuation pulls back to
     content.
  3. Sample answer text per alpha for one representative item, so the reader
     can see the qualitative shift.

Writes:
  figures/13_intervention_results_postanalysis.json
  figures/13_intervention_first_token_flip.png
"""
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from config import FIGURES_DIR

RES = FIGURES_DIR / "13_intervention_results.json"
# Refusal openers across all subject models we ran the intervention on.
# Derived from the top-15 tokens of each model's recovered refusal direction
# (figures/{model}/12_probe_direction_atlas.json):
#   - Qwen3-1.7B:  " as", "As", " As", " there", "作为", "作為"
#   - Gemma 2 2B:  " Regret"/"Regret"/"Regrettably", "Formal" announcements,
#                  " Alas", " Neither"/"neither", " no", "Không" (Vietnamese)
#   - Llama 3.2 3B: " I" (don't/cannot/can't), " Given", " As", " After"
# Also include common English refusal pragmatics seen in actual outputs.
REFUSAL_OPENERS = [
    # Qwen3 vocabulary
    r"^\s*as\b", r"^\s*As\b",
    r"^\s*There\b", r"^\s*there\b",
    r"^\s*作为", r"^\s*作為",
    # Gemma vocabulary
    r"^\s*Regret", r"^\s*regret",
    r"^\s*Formal\b",
    r"^\s*Alas\b",
    r"^\s*Neither\b", r"^\s*neither\b",
    r"^\s*Không\b",
    # Llama vocabulary
    r"^\s*I\b",
    r"^\s*Given\b",
    # Generic English refusals
    r"^\s*No\b", r"^\s*no\b",
    r"^\s*Unfortunately\b",
    r"^\s*Sorry\b",
    r"^\s*I'm not\b", r"^\s*I do not\b", r"^\s*I don't\b", r"^\s*I cannot\b",
    r"^\s*While\b",
]
OPENER_RE = re.compile("|".join(REFUSAL_OPENERS))


def is_refusal_opener(text):
    return bool(OPENER_RE.match(text or ""))


def main():
    if not RES.exists():
        print(f"Missing {RES}; run make_causal_intervention.py first.")
        return
    res = json.load(open(RES))
    alphas = res["alphas"]
    by_sub = {}
    for subset_name in ("wrong_subset", "refusal_subset"):
        items = res[subset_name]
        n = len(items)
        per_alpha = {}
        for alpha in alphas:
            akey = str(alpha)
            label_counts = {"correct": 0, "refusal": 0, "wrong": 0}
            opener_flips = 0
            for item in items:
                lbl = item["by_alpha"][akey]["judge_label"]
                ans = item["by_alpha"][akey]["answer"]
                label_counts[lbl] += 1
                if is_refusal_opener(ans):
                    opener_flips += 1
            per_alpha[akey] = {
                "n": n,
                "refusal_rate": label_counts["refusal"] / n,
                "correct_rate": label_counts["correct"] / n,
                "wrong_rate": label_counts["wrong"] / n,
                "first_token_refusal_opener_rate": opener_flips / n,
            }
        by_sub[subset_name] = per_alpha

    out = {"alphas": alphas, "by_subset": by_sub}
    out_path = FIGURES_DIR / "13_intervention_results_postanalysis.json"
    with open(out_path, "w") as fp:
        json.dump(out, fp, indent=2)
    print(f"Wrote {out_path}")

    # print table
    for subset_name, sub in by_sub.items():
        print(f"\n=== {subset_name} ===")
        print(f"  alpha    refusal%   correct%   wrong%   first-token-refusal-opener%")
        for alpha in alphas:
            akey = str(alpha)
            p = sub[akey]
            print(f"  {alpha:+7.1f}  {p['refusal_rate']*100:7.1f}   "
                  f"{p['correct_rate']*100:7.1f}   {p['wrong_rate']*100:7.1f}   "
                  f"{p['first_token_refusal_opener_rate']*100:7.1f}")

    # sample answers for one representative item per subset
    print("\n=== Sample answer text per alpha (first item in each subset) ===")
    for subset_name in ("wrong_subset", "refusal_subset"):
        items = res[subset_name]
        if not items:
            continue
        item = items[0]
        print(f"\n{subset_name}  id={item['id']}  Q: {item['question']}")
        print(f"  expected: {item['expected']}")
        for alpha in alphas:
            akey = str(alpha)
            ans = item["by_alpha"][akey]["answer"]
            lbl = item["by_alpha"][akey]["judge_label"]
            print(f"  alpha={alpha:+7.1f}  [{lbl:<7s}]  {ans[:140]!r}")

    # plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for ax, subset_name, title in [
        (axes[0], "wrong_subset",
         f"Originally WRONG (post-cutoff, n={by_sub['wrong_subset'][str(alphas[0])]['n']})"),
        (axes[1], "refusal_subset",
         f"Originally REFUSAL (n={by_sub['refusal_subset'][str(alphas[0])]['n']})"),
    ]:
        xs = alphas
        rates_ref = [by_sub[subset_name][str(a)]["refusal_rate"] for a in xs]
        rates_opener = [by_sub[subset_name][str(a)]["first_token_refusal_opener_rate"] for a in xs]
        rates_cor = [by_sub[subset_name][str(a)]["correct_rate"] for a in xs]
        ax.plot(xs, rates_opener, marker="o", color="#1f77b4",
                label="first-token = refusal opener", linewidth=2)
        ax.plot(xs, rates_ref, marker="s", color="#9467bd",
                label="judge says REFUSAL", linewidth=2, linestyle="--")
        ax.plot(xs, rates_cor, marker="^", color="#2ca02c",
                label="judge says CORRECT", linewidth=1.5, alpha=0.7)
        ax.axvline(0.0, color="#888", linestyle=":", alpha=0.6,
                   label="no intervention")
        ax.set_xlabel(r"$\alpha$ (units of refusal-direction L2 norm)")
        ax.set_title(title, fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        ax.legend(loc="best", fontsize=9)
    axes[0].set_ylabel("rate over subset")
    fig.suptitle(
        "Causal intervention: refusal direction at layer 28, prefill-only "
        "(last prompt token)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    out_png = FIGURES_DIR / "13_intervention_first_token_flip.png"
    fig.savefig(out_png, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out_png}")


if __name__ == "__main__":
    main()
