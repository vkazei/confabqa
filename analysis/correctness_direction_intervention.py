"""One-shot intervention along the layer-18 correctness direction.

Causal companion to analysis/correctness_direction_lens.py: recovers the
correct-vs-rest probe direction at the correctness-probe peak layer
(18), unit-normalizes it, and adds alpha * w_unit to the last prompt
token's hidden state during prefill (forward hook on
model.model.layers[17], the block whose output is the layer-18 hidden
state), exactly the Section 6.2 protocol but for the correctness
direction. Subsets: 30 originally-correct + 30 originally-wrong items,
stratified by domain. Each generation is re-judged by the three-way
judge.py (same-model judge).

Writes figures/qwen3_1_7b/correctness_direction_intervention.{json,md}.
Run from the repo root:
    python -m analysis.correctness_direction_intervention
"""
import json
import random
from collections import defaultdict

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import analysis.make_probe_direction_atlas as atlas
from analysis.make_causal_intervention import generate_with_intervention
import analysis.make_causal_intervention as mci
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from judge import judge as run_judge

CORRECTNESS_LAYER = 18
ALPHAS = [-3000.0, -1500.0, -500.0, 0.0, 500.0, 1500.0, 3000.0]
N_PER_GROUP = 30


def pick_subset(items, label, n, rng):
    by_domain = defaultdict(list)
    for r in items:
        if r["judge_label"] == label:
            by_domain[r["domain"]].append(r)
    for v in by_domain.values():
        v.sort(key=lambda r: r["question_id"])
        rng.shuffle(v)
    picked, i = [], 0
    domains = sorted(by_domain)
    while len(picked) < n and any(by_domain.values()):
        d = domains[i % len(domains)]
        if by_domain[d]:
            picked.append(by_domain[d].pop())
        i += 1
    return picked[:n]


def main():
    set_seeds()
    atlas.PROBE_LAYER = CORRECTNESS_LAYER
    mci.INTERVENTION_LAYER = CORRECTNESS_LAYER - 1  # block 17 outputs layer-18 h
    items = atlas.load_subset({"correct", "refusal", "wrong"})
    d = atlas.recover_direction(items, "correct")
    w = d["direction_raw"]
    w_unit = w / np.linalg.norm(w)

    rng = random.Random(0)
    subsets = {
        "originally_correct": pick_subset(items, "correct", N_PER_GROUP, rng),
        "originally_wrong": pick_subset(items, "wrong", N_PER_GROUP, rng),
    }

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    device = get_device()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16).to(device)
    model.eval()
    direction_t = torch.tensor(w_unit, dtype=model.dtype, device=device)

    # resume from a previous partial run
    rows_path = FIGURES_DIR / "correctness_direction_intervention_rows.jsonl"
    results = []
    done = set()
    if rows_path.exists():
        for line in rows_path.open():
            row = json.loads(line)
            results.append(row)
            done.add((row["id"], row["alpha"]))
        print(f"resuming: {len(results)} rows already done")
    rows_f = rows_path.open("a")
    for subset_name, subset in subsets.items():
        for r in subset:
            for alpha in ALPHAS:
                if (r["question_id"], alpha) in done:
                    continue
                text = generate_with_intervention(
                    model, tokenizer, device, r["question"], direction_t, alpha)
                verdict = run_judge(model, tokenizer, device, r["question"],
                                    r["expected_answer"],
                                    r.get("acceptable_alternatives") or [], text)
                row = {
                    "subset": subset_name, "id": r["question_id"],
                    "alpha": alpha, "text_head": text[:120],
                    "judge_label": verdict["label"],
                }
                results.append(row)
                rows_f.write(json.dumps(row, ensure_ascii=False) + "\n")
                rows_f.flush()
                print(f"{subset_name} {r['question_id']} a={alpha:+.0f} "
                      f"-> {verdict['label']}", flush=True)

    # aggregate
    agg = defaultdict(lambda: defaultdict(int))
    for row in results:
        agg[(row["subset"], row["alpha"])][row["judge_label"]] += 1
    summary = {}
    for (subset_name, alpha), counts in sorted(agg.items()):
        n = sum(counts.values())
        summary.setdefault(subset_name, {})[str(alpha)] = {
            lab: counts.get(lab, 0) / n for lab in ("correct", "refusal", "wrong")}

    out = {
        "layer": CORRECTNESS_LAYER,
        "direction": "correct-vs-rest probe, unit-normalized",
        "alphas": ALPHAS, "n_per_group": N_PER_GROUP,
        "summary": summary, "rows": results,
    }
    out_json = FIGURES_DIR / "correctness_direction_intervention.json"
    with open(out_json, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"Wrote {out_json}")

    lines = ["# Correctness-direction intervention (layer 18)\n"]
    for subset_name, per_alpha in summary.items():
        lines.append(f"\n## {subset_name}\n")
        lines.append("| alpha | correct | refusal | wrong |")
        lines.append("|--:|--:|--:|--:|")
        for a in ALPHAS:
            c = per_alpha[str(a)]
            lines.append(f"| {a:+.0f} | {c['correct']:.0%} | "
                         f"{c['refusal']:.0%} | {c['wrong']:.0%} |")
    out_md = FIGURES_DIR / "correctness_direction_intervention.md"
    out_md.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
