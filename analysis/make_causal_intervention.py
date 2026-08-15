"""Causal intervention: add/subtract scaled refusal direction at layer-28
(last prompt token) during prefill, sweep alpha, measure refusal-rate shift.

The probe-direction analysis (Section 6.6) recovered a direction in
2048-d hidden-state space whose LM-head projection is the refusal opening
vocabulary. That's evidence the *correlation* between the direction and
refusal is strong. This script tests whether the direction is also *causal*:
if we push the model's pre-commitment hidden state along the direction, does
its actual generated output switch from confabulation to refusal?

Protocol:
  - Subset: 30 wrong post-cutoff items + 30 refusal items (stratified by domain).
  - Direction: the saved layer-28 refusal-vs-wrong-within-post direction (most
    discriminative, since all refusals are post-cutoff).
  - Intervention: forward hook on model.model.layers[-1] that adds alpha * dir
    to h[:, -1, :] during prefill only (sequence length > 1). Generation steps
    pass through unmodified.
  - Sweep: alpha in {-15, -10, -5, -2, 0, +2, +5, +10, +15}.
  - For each (item, alpha): generate 64 tokens greedily; re-judge with the
    same three-way judge (judge.py); record the new label.
  - Output: figures/13_intervention_refusal_rate.{png,json} summarizing the
    refusal rate as a function of alpha for each starting subset.

If the direction is causal, refusal rate on the originally-wrong items should
increase monotonically with alpha, and refusal rate on the originally-refusal
items should decrease with -alpha.
"""
from __future__ import annotations

import argparse
import json
import time
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import (FIGURES_DIR, MODEL_ID, RESPONSES_DIR, SUMMARY_PATH,
                    get_device, set_seeds)
from judge import judge as run_judge

ALPHAS = [-15.0, -10.0, -5.0, -2.0, 0.0, 2.0, 5.0, 10.0, 15.0]
N_PER_GROUP = 30

# Load refusal_vs_wrong peak layer from summary if it exists, else default to 28 (which corresponds to index 27)
INTERVENTION_LAYER = 27
if SUMMARY_PATH.exists():
    try:
        with open(SUMMARY_PATH) as f:
            _summary = json.load(f)
        INTERVENTION_LAYER = _summary["probes"]["refusal_vs_wrong"]["peak_layer"] - 1
    except Exception:
        pass
DIRECTION_NPY = FIGURES_DIR / "12_probe_direction_refusal_vs_wrong_within_post.npy"
OUT_JSON = FIGURES_DIR / "13_intervention_results.json"
OUT_PNG = FIGURES_DIR / "13_intervention_refusal_rate.png"


def pick_subset(n_per_group=N_PER_GROUP):
    """Stratified subset: n_per_group wrong post-cutoff + n_per_group refusals."""
    rng = np.random.RandomState(0)
    wrong_post = []
    refusal_all = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        r = json.load(open(f))
        if r["cutoff_class"] != "post":
            continue
        if r["judge_label"] == "wrong":
            wrong_post.append(r)
        elif r["judge_label"] == "refusal":
            refusal_all.append(r)
    by_dom_w = defaultdict(list)
    by_dom_r = defaultdict(list)
    for r in wrong_post:
        by_dom_w[r["domain"]].append(r)
    for r in refusal_all:
        by_dom_r[r["domain"]].append(r)

    def stratified(grouped, n_total):
        # try to allocate roughly evenly
        domains = sorted(grouped.keys())
        per = max(1, n_total // len(domains))
        picked = []
        for d in domains:
            items = list(grouped[d])
            rng.shuffle(items)
            picked.extend(items[:per])
        # fill remainder
        rest = [r for d in domains for r in grouped[d] if r not in picked]
        rng.shuffle(rest)
        return picked[:n_total] + rest[:max(0, n_total - len(picked))]

    wrong_sub = stratified(by_dom_w, n_per_group)[:n_per_group]
    refusal_sub = stratified(by_dom_r, n_per_group)[:n_per_group]
    return wrong_sub, refusal_sub


def make_hook(direction_t, alpha, mode="prefill_only"):
    """Forward hook on the last transformer block.

    mode:
      - "prefill_only": modify h[:, -1, :] only during prefill (sequence length > 1).
      - "throughout": modify h[:, -1, :] on every forward pass (prefill + every gen step).
    """
    nudge = alpha * direction_t  # (d,)

    def hook(module, input, output):
        if isinstance(output, tuple):
            h = output[0]
            rest = output[1:]
        else:
            h = output
            rest = None
        if mode == "prefill_only" and h.shape[1] == 1:
            return output  # generation step in prefill_only mode: passthrough
        h_mod = h.clone()
        h_mod[:, -1, :] = h_mod[:, -1, :] + nudge.to(h.dtype)
        if rest is not None:
            return (h_mod,) + rest
        return h_mod

    return hook


def generate_with_intervention(model, tokenizer, device, question, direction_t,
                                 alpha, mode="prefill_only", max_new_tokens=64):
    messages = [{"role": "user", "content": question}]
    text = tokenizer.apply_chat_template(messages, tokenize=False,
                                          add_generation_prompt=True,
                                          enable_thinking=False)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    input_len = inputs["input_ids"].shape[1]

    handle = model.model.layers[INTERVENTION_LAYER].register_forward_hook(
        make_hook(direction_t, alpha, mode=mode))
    try:
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=max_new_tokens,
                                  do_sample=False)
    finally:
        handle.remove()
    return tokenizer.decode(out[0, input_len:], skip_special_tokens=True).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alphas", type=float, nargs="*", default=ALPHAS)
    parser.add_argument("--n", type=int, default=N_PER_GROUP)
    parser.add_argument("--mode", choices=["prefill_only", "throughout"],
                        default="prefill_only")
    parser.add_argument("--verbose", action="store_true",
                        help="Print first 80 chars of each answer")
    args = parser.parse_args()

    set_seeds()
    device = get_device()

    direction = np.load(DIRECTION_NPY)
    print(f"Loaded direction: shape={direction.shape} norm={np.linalg.norm(direction):.3f}")

    print(f"Loading subject model {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.bfloat16,
                                                   device_map=device)
    model.eval()
    print(f"  loaded; device={device}, dtype={next(model.parameters()).dtype}")

    JUDGE_MODEL_ID = "Qwen/Qwen3-1.7B"
    if MODEL_ID == JUDGE_MODEL_ID:
        judge_tokenizer, judge_model = tokenizer, model
        print(f"Using subject model as judge (Qwen3-1.7B is the standard judge).")
    else:
        print(f"Loading separate judge model {JUDGE_MODEL_ID}...")
        judge_tokenizer = AutoTokenizer.from_pretrained(JUDGE_MODEL_ID)
        judge_model = AutoModelForCausalLM.from_pretrained(
            JUDGE_MODEL_ID, dtype=torch.bfloat16, device_map=device)
        judge_model.eval()
        print(f"  judge loaded.")

    direction_t = torch.tensor(direction, dtype=torch.float32, device=device)
    # Normalize the direction so alpha has comparable scale across runs:
    # alpha = nudge in units of the direction's L2 norm in raw 2048-d space.
    # NB: we report alpha in these normalized units.
    direction_t = direction_t / direction_t.norm()

    wrong_sub, refusal_sub = pick_subset(n_per_group=args.n)
    print(f"Subset: {len(wrong_sub)} wrong-post-cutoff items, "
          f"{len(refusal_sub)} refusal items")

    results = {"alphas": list(args.alphas), "wrong_subset": [],
               "refusal_subset": []}

    t_overall = time.perf_counter()
    n_done = 0
    n_total = (len(wrong_sub) + len(refusal_sub)) * len(args.alphas)

    for subset_name, subset in [("wrong_subset", wrong_sub),
                                  ("refusal_subset", refusal_sub)]:
        for r in subset:
            per_item = {"id": r["question_id"], "domain": r["domain"],
                        "question": r["question"],
                        "expected": r["expected_answer"],
                        "alternatives": r.get("acceptable_alternatives", []),
                        "original_label": r["judge_label"],
                        "original_answer": r["answer_text"],
                        "by_alpha": {}}
            for alpha in args.alphas:
                t0 = time.perf_counter()
                ans = generate_with_intervention(
                    model, tokenizer, device, r["question"], direction_t,
                    alpha=alpha, mode=args.mode)
                j = run_judge(judge_model, judge_tokenizer, device, r["question"],
                              r["expected_answer"],
                              r.get("acceptable_alternatives", []), ans)
                per_item["by_alpha"][str(alpha)] = {
                    "answer": ans, "judge_label": j["label"],
                    "judge_raw": j.get("raw", "")[:200]}
                n_done += 1
                dt = time.perf_counter() - t0
                eta = (n_total - n_done) * dt
                line = (f"  [{n_done}/{n_total}] {r['question_id']} alpha={alpha:+.1f}: "
                        f"{j['label']:<8s} ({dt:.1f}s/step, eta {eta/60:.1f} min)")
                if args.verbose:
                    line += f"\n    ANS: {ans[:80]!r}"
                print(line)
            results[subset_name].append(per_item)

    elapsed = time.perf_counter() - t_overall
    print(f"\nTotal: {elapsed/60:.1f} min ({elapsed/n_total:.1f}s/step)")

    # Aggregate: refusal rate per alpha per starting subset
    summary = {"alphas": list(args.alphas), "by_subset": {}}
    for subset_name in ("wrong_subset", "refusal_subset"):
        n = len(results[subset_name])
        per_alpha = {}
        for alpha in args.alphas:
            akey = str(alpha)
            cnt = defaultdict(int)
            for item in results[subset_name]:
                cnt[item["by_alpha"][akey]["judge_label"]] += 1
            per_alpha[akey] = {
                "n": n,
                "refusal": cnt["refusal"], "wrong": cnt["wrong"],
                "correct": cnt["correct"],
                "refusal_rate": cnt["refusal"] / n if n else 0.0,
                "correct_rate": cnt["correct"] / n if n else 0.0,
            }
        summary["by_subset"][subset_name] = per_alpha

    results["summary"] = summary
    with open(OUT_JSON, "w") as fp:
        json.dump(results, fp, indent=2, ensure_ascii=False)
    print(f"Wrote {OUT_JSON}")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
    for ax, subset_name, title in [
        (axes[0], "wrong_subset",
         f"Originally WRONG (post-cutoff, n={len(results['wrong_subset'])})"),
        (axes[1], "refusal_subset",
         f"Originally REFUSAL (n={len(results['refusal_subset'])})"),
    ]:
        alphas = [float(a) for a in args.alphas]
        rates_ref = [summary["by_subset"][subset_name][str(a)]["refusal_rate"]
                     for a in args.alphas]
        rates_cor = [summary["by_subset"][subset_name][str(a)]["correct_rate"]
                     for a in args.alphas]
        ax.plot(alphas, rates_ref, marker="o", color="#1f77b4",
                label="refusal rate")
        ax.plot(alphas, rates_cor, marker="s", color="#2ca02c",
                label="correct rate")
        ax.axvline(0.0, color="#888", linestyle=":", alpha=0.6,
                   label="no intervention")
        ax.set_xlabel(r"$\alpha$ (units of refusal-direction L2 norm)")
        ax.set_title(title, fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.05, 1.05)
        ax.legend(loc="best", fontsize=9)
    axes[0].set_ylabel("rate over subset")
    fig.suptitle("Causal intervention: layer-28 refusal direction "
                  f"(prefill-only, last prompt token)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT_PNG, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
