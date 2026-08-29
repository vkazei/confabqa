"""Steering-matrix parity: SAE-2191 and optimized directions, judged.

Table 4's judged steering matrix was measured with the probe direction
only. This script reruns the same protocol (one-shot prefill push,
greedy 64-token generation, three-way judge) for the other two
candidate refusal directions on the same three 30-item subsets and
doses, so all three directions can be compared at the judge level.

Requires figures/qwen3_1_7b/optimized_refusal_direction.npy
(python -m analysis.optimize_refusal_direction saves it).

Writes figures/qwen3_1_7b/15_intervention_three_directions.json.
Run from the repo root: python -m analysis.intervene_three_directions
"""
import json
import time
from collections import defaultdict

import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.make_causal_intervention import (generate_with_intervention,
                                               pick_subset)
from analysis.intervene_correct_subset import (OPENER_PREFIXES,
                                               pick_correct_subset)
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from judge import judge as run_judge

ALPHAS = [-2000.0, -500.0, 500.0, 1500.0, 3000.0]  # alpha=0 is in 13_/14_
OUT_JSON = FIGURES_DIR / "15_intervention_three_directions.json"


def main():
    set_seeds()
    device = get_device()

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    u_2191 = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID]
    u_2191 = u_2191 / np.linalg.norm(u_2191)
    del sae
    u_opt = np.load(FIGURES_DIR / "optimized_refusal_direction.npy")
    u_opt = u_opt / np.linalg.norm(u_opt)
    directions = {"sae_2191": u_2191, "optimized": u_opt}

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.bfloat16,
                                                 device_map=device)
    model.eval()

    wrong_sub, refusal_sub = pick_subset()
    correct_sub = pick_correct_subset()
    subsets = {"wrong_subset": wrong_sub, "refusal_subset": refusal_sub,
               "correct_subset": correct_sub}

    results = {"alphas": ALPHAS, "directions": {}}
    if OUT_JSON.exists():  # resume across restarts
        results = json.loads(OUT_JSON.read_text())

    n_total = len(directions) * sum(len(s) for s in subsets.values()) * len(ALPHAS)
    n_done = 0
    t_overall = time.perf_counter()
    for dname, u in directions.items():
        dres = results["directions"].setdefault(dname, {})
        direction_t = torch.tensor(u, dtype=torch.float32, device=device)
        for sname, subset in subsets.items():
            sres = dres.setdefault(sname, {})
            for r in subset:
                qid = r["question_id"]
                if qid in sres and len(sres[qid]["by_alpha"]) == len(ALPHAS):
                    n_done += len(ALPHAS)
                    continue
                per_item = sres.setdefault(
                    qid, {"domain": r["domain"], "question": r["question"],
                          "original_label": r["judge_label"], "by_alpha": {}})
                for alpha in ALPHAS:
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
                        "answer": ans, "judge_label": j["label"],
                        "opener_start": ans.lstrip().startswith(OPENER_PREFIXES)}
                    n_done += 1
                    dt = time.perf_counter() - t0
                    print(f"[{n_done}/{n_total}] {dname} {sname} {qid} "
                          f"a={alpha:+.0f}: {j['label']:<8s} ({dt:.0f}s, "
                          f"eta {(n_total - n_done) * dt / 3600:.1f}h)",
                          flush=True)
                with open(OUT_JSON, "w") as f:
                    json.dump(results, f, ensure_ascii=False, indent=1)

    summary = {}
    for dname, dres in results["directions"].items():
        summary[dname] = {}
        for sname, sres in dres.items():
            per_alpha = {}
            for alpha in ALPHAS:
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
    print(f"Total {(time.perf_counter() - t_overall) / 3600:.1f}h; "
          f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
