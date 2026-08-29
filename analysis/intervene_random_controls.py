"""Norm-matched random-direction and shuffled-probe steering controls.

The steering claims of Sections 6.2/6.3.1 lack a direction-specificity
control at matched dose. This script pushes the same items with (i)
three norm-matched random unit directions and (ii) a shuffled-label
probe direction (logistic fit on the pre-norm states with permuted
labels), using the identical one-shot protocol and judge:

  wrong subset  x alpha in {-2000, -500, +500, +1500, +3000}
  refusal subset x alpha in {-2000, -500}   (de-refusal artifact check)

Writes figures/qwen3_1_7b/16_intervention_random_controls.json.
Run from the repo root: python -m analysis.intervene_random_controls
"""
import json
import time
from collections import defaultdict

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.cache_prenorm_states import load_prenorm
from analysis.make_causal_intervention import (generate_with_intervention,
                                               pick_subset)
from analysis.intervene_correct_subset import OPENER_PREFIXES
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from judge import judge as run_judge

SWEEP = {"wrong_subset": [-2000.0, -500.0, 500.0, 1500.0, 3000.0],
         "refusal_subset": [-2000.0, -500.0]}
OUT_JSON = FIGURES_DIR / "16_intervention_random_controls.json"


def build_directions():
    dirs = {}
    for seed in (1, 2, 3):
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(2048)
        dirs[f"random_{seed}"] = v / np.linalg.norm(v)
    items, H = load_prenorm({"refusal", "wrong"})
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in items])
    rng = np.random.default_rng(0)
    y_shuf = rng.permutation(y)
    clf = LogisticRegression(max_iter=2000, class_weight="balanced")
    clf.fit(H, y_shuf)
    w = clf.coef_[0]
    dirs["shuffled_probe"] = w / np.linalg.norm(w)
    return dirs


def main():
    set_seeds()
    device = get_device()
    directions = build_directions()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.bfloat16,
                                                 device_map=device)
    model.eval()

    wrong_sub, refusal_sub = pick_subset()
    subsets = {"wrong_subset": wrong_sub, "refusal_subset": refusal_sub}

    results = {"sweep": {k: list(v) for k, v in SWEEP.items()},
               "directions": {}}
    if OUT_JSON.exists():
        results = json.loads(OUT_JSON.read_text())

    n_total = sum(len(subsets[s]) * len(a) for s, a in SWEEP.items()) * len(directions)
    n_done = 0
    for dname, u in directions.items():
        dres = results["directions"].setdefault(dname, {})
        direction_t = torch.tensor(u, dtype=torch.float32, device=device)
        for sname, alphas in SWEEP.items():
            sres = dres.setdefault(sname, {})
            for r in subsets[sname]:
                qid = r["question_id"]
                per_item = sres.setdefault(
                    qid, {"original_label": r["judge_label"], "by_alpha": {}})
                for alpha in alphas:
                    if str(alpha) in per_item["by_alpha"]:
                        n_done += 1
                        continue
                    t0 = time.perf_counter()
                    ans = generate_with_intervention(
                        model, tokenizer, device, r["question"], direction_t,
                        alpha=alpha, mode="prefill_only")
                    j = run_judge(model, tokenizer, device, r["question"],
                                  r["expected_answer"],
                                  r.get("acceptable_alternatives", []), ans)
                    per_item["by_alpha"][str(alpha)] = {
                        "answer": ans[:200], "judge_label": j["label"],
                        "opener_start": ans.lstrip().startswith(OPENER_PREFIXES)}
                    n_done += 1
                    dt = time.perf_counter() - t0
                    print(f"[{n_done}/{n_total}] {dname} {sname} {qid} "
                          f"a={alpha:+.0f}: {j['label']:<8s} ({dt:.0f}s)",
                          flush=True)
                with open(OUT_JSON, "w") as f:
                    json.dump(results, f, ensure_ascii=False, indent=1)

    summary = {}
    for dname, dres in results["directions"].items():
        summary[dname] = {}
        for sname, sres in dres.items():
            per_alpha = {}
            for alpha in SWEEP[sname]:
                cnt = defaultdict(int)
                op = 0
                for it in sres.values():
                    c = it["by_alpha"][str(alpha)]
                    cnt[c["judge_label"]] += 1
                    op += c["opener_start"]
                n = len(sres)
                per_alpha[str(alpha)] = {
                    "n": n,
                    **{k: cnt[k] for k in ("correct", "wrong", "refusal")},
                    "opener_rate": round(op / n, 4)}
            summary[dname][sname] = per_alpha
    results["summary"] = summary
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1))
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
