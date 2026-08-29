"""Causal intervention on originally-CORRECT items: the missing cell.

Section 6.2 pushes wrong items toward refusal and refusal items toward
attempt; this script completes the matrix by pushing 30 originally
correct items along the same direction with the same doses. Questions
answered: (i) can the model be made to refuse what it knows (positive
doses), and (ii) does suppressing refusal-ness damage retrieval and
create confabulation from knowledge (negative doses)?

Protocol identical to analysis/make_causal_intervention.py (one-shot
prefill hook at the post-block-27 residual, greedy 64-token generation,
three-way judge), reusing its hook and generation code.

Writes figures/qwen3_1_7b/14_intervention_correct_subset.json.
Run from the repo root: python -m analysis.intervene_correct_subset
"""
import json
import time
from collections import defaultdict

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.make_causal_intervention import (DIRECTION_NPY,
                                               generate_with_intervention)
from config import FIGURES_DIR, MODEL_ID, RESPONSES_DIR, get_device, set_seeds
from judge import judge as run_judge
from saes.sae_causal_ablation import REFUSAL_OPENER_STRS

ALPHAS = [-2000.0, -500.0, 0.0, 500.0, 1500.0, 3000.0]
N_ITEMS = 30
OUT_JSON = FIGURES_DIR / "14_intervention_correct_subset.json"
OPENER_PREFIXES = tuple(sorted({s.strip() for s in REFUSAL_OPENER_STRS
                                if s.strip()}))


def pick_correct_subset(n_total=N_ITEMS):
    """Domain-stratified sample of originally-correct items."""
    rng = np.random.RandomState(0)
    by_dom = defaultdict(list)
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        r = json.load(open(f))
        if r["judge_label"] == "correct":
            by_dom[r["domain"]].append(r)
    domains = sorted(by_dom)
    per = max(1, n_total // len(domains))
    picked = []
    for d in domains:
        items = list(by_dom[d])
        rng.shuffle(items)
        picked.extend(items[:per])
    rest = [r for d in domains for r in by_dom[d] if r not in picked]
    rng.shuffle(rest)
    return (picked[:n_total] + rest[:max(0, n_total - len(picked))])[:n_total]


def main():
    set_seeds()
    device = get_device()
    direction = np.load(DIRECTION_NPY)
    direction_t = torch.tensor(direction, dtype=torch.float32, device=device)
    direction_t = direction_t / direction_t.norm()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.bfloat16,
                                                 device_map=device)
    model.eval()

    subset = pick_correct_subset()
    print(f"Subset: {len(subset)} originally-correct items")

    results = {"alphas": ALPHAS, "correct_subset": []}
    n_total, n_done = len(subset) * len(ALPHAS), 0
    t_overall = time.perf_counter()
    for r in subset:
        per_item = {"id": r["question_id"], "domain": r["domain"],
                    "question": r["question"],
                    "expected": r["expected_answer"],
                    "alternatives": r.get("acceptable_alternatives", []),
                    "original_label": r["judge_label"],
                    "original_answer": r["answer_text"],
                    "by_alpha": {}}
        for alpha in ALPHAS:
            t0 = time.perf_counter()
            ans = generate_with_intervention(
                model, tokenizer, device, r["question"], direction_t,
                alpha=alpha, mode="prefill_only")
            j = run_judge(model, tokenizer, device, r["question"],
                          r["expected_answer"],
                          r.get("acceptable_alternatives", []), ans)
            per_item["by_alpha"][str(alpha)] = {
                "answer": ans, "judge_label": j["label"],
                "opener_start": ans.lstrip().startswith(OPENER_PREFIXES)}
            n_done += 1
            dt = time.perf_counter() - t0
            print(f"  [{n_done}/{n_total}] {r['question_id']} "
                  f"alpha={alpha:+.0f}: {j['label']:<8s} "
                  f"({dt:.1f}s, eta {(n_total - n_done) * dt / 60:.0f} min)",
                  flush=True)
        results["correct_subset"].append(per_item)
        with open(OUT_JSON, "w") as f:  # resumable-ish: persist per item
            json.dump(results, f, ensure_ascii=False, indent=1)

    summary = {"alphas": ALPHAS, "by_alpha": {}}
    for alpha in ALPHAS:
        cnt = defaultdict(int)
        op = 0
        for it in results["correct_subset"]:
            c = it["by_alpha"][str(alpha)]
            cnt[c["judge_label"]] += 1
            op += c["opener_start"]
        n = len(results["correct_subset"])
        summary["by_alpha"][str(alpha)] = {
            "n": n, **{k: cnt[k] for k in ("correct", "wrong", "refusal")},
            "refusal_rate": round(cnt["refusal"] / n, 4),
            "correct_rate": round(cnt["correct"] / n, 4),
            "opener_rate": round(op / n, 4)}
    results["summary"] = summary
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1))
    print(f"Total {(time.perf_counter() - t_overall) / 60:.1f} min; "
          f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
