"""Gemma 2 2B: sub-norm dose sweep plus random-direction controls.

The recorded Gemma sweep ran at 6-25x its residual scale (326 at the
layer-19 hook), a regime where magnitude artifacts are live. This
script completes the dose ladder downward, with controls: the real
refusal direction and two norm-matched random directions at
alpha in {-300, -100, +100, +300} (0.31x and 0.92x), wrong and refusal
subsets, same generate-and-judge protocol.

Run with: MODEL_ID=unsloth/gemma-2-2b-it python -m analysis.gemma_subnorm_sweep
Writes figures/gemma_2_2b/17_intervention_gemma_subnorm.json.
"""
import json
import time
from collections import defaultdict

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.make_causal_intervention import (DIRECTION_NPY,
                                               generate_with_intervention,
                                               pick_subset)
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from judge import judge as run_judge

ALPHAS = [-300.0, -100.0, 100.0, 300.0]
OUT_JSON = FIGURES_DIR / "17_intervention_gemma_subnorm.json"
JUDGE_MODEL_ID = "Qwen/Qwen3-1.7B"
OPENER_PREFIXES = ("As", "as", "I ", "I'", "Unfortunately", "Sorry")


def main():
    assert "gemma" in MODEL_ID.lower(), "run with MODEL_ID=unsloth/gemma-2-2b-it"
    set_seeds()
    device = get_device()

    w = np.load(DIRECTION_NPY)
    dirs = {"refusal_dir": w / np.linalg.norm(w)}
    for seed in (1, 2):
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(w.shape[0])
        dirs[f"random_{seed}"] = v / np.linalg.norm(v)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.bfloat16,
                                                 device_map=device)
    model.eval()
    judge_tok = AutoTokenizer.from_pretrained(JUDGE_MODEL_ID)
    judge_model = AutoModelForCausalLM.from_pretrained(
        JUDGE_MODEL_ID, dtype=torch.bfloat16, device_map=device)
    judge_model.eval()

    wrong_sub, refusal_sub = pick_subset()
    subsets = {"wrong_subset": wrong_sub, "refusal_subset": refusal_sub}

    results = {"alphas": ALPHAS, "directions": {}}
    if OUT_JSON.exists():
        results = json.loads(OUT_JSON.read_text())

    n_total = len(dirs) * 60 * len(ALPHAS)
    n_done = 0
    for dname, u in dirs.items():
        dres = results["directions"].setdefault(dname, {})
        direction_t = torch.tensor(u, dtype=torch.float32, device=device)
        for sname, subset in subsets.items():
            sres = dres.setdefault(sname, {})
            for r in subset:
                qid = r["question_id"]
                per_item = sres.setdefault(
                    qid, {"original_label": r["judge_label"], "by_alpha": {}})
                for alpha in ALPHAS:
                    if str(alpha) in per_item["by_alpha"]:
                        n_done += 1
                        continue
                    t0 = time.perf_counter()
                    ans = generate_with_intervention(
                        model, tokenizer, device, r["question"], direction_t,
                        alpha=alpha, mode="prefill_only")
                    j = run_judge(judge_model, judge_tok, device,
                                  r["question"], r["expected_answer"],
                                  r.get("acceptable_alternatives", []), ans)
                    per_item["by_alpha"][str(alpha)] = {
                        "answer": ans[:200], "judge_label": j["label"],
                        "opener_start": ans.lstrip().startswith(OPENER_PREFIXES)}
                    n_done += 1
                    print(f"[{n_done}/{n_total}] {dname} {sname} {qid} "
                          f"a={alpha:+.0f}: {j['label']:<8s} "
                          f"({time.perf_counter()-t0:.0f}s)", flush=True)
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
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
