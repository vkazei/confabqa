"""Prefix-forcing control for the Section 6.2 intervention.

Question: is the refusal-direction intervention causally equivalent to
simply forcing the generation to open with the refusal opener? On the
same 30 originally-wrong items the Section 6.2 sweep used (read from
figures/qwen3_1_7b/13_intervention_results.json), generate with the
literal first token "As" appended to the assistant prefix and NO
hidden-state perturbation, then re-judge with the three-way judge.
Compare the judge-refusal rate against the intervention's rate at
alpha = +1500/+3000 (30%), where the first-token opener rate is
97-100%.

Writes figures/qwen3_1_7b/prefix_forcing_control.json.
Run from the repo root: python -m analysis.prefix_forcing_control
"""
import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from judge import judge as run_judge

FORCED_PREFIX = "As"
MAX_NEW = 63  # one token is already forced


def main():
    set_seeds()
    art = json.load(open(FIGURES_DIR / "13_intervention_results.json"))
    items = art["wrong_subset"]

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    device = get_device()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16).to(device)
    model.eval()

    rows = []
    for r in items:
        messages = [{"role": "user", "content": r["question"]}]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
            enable_thinking=False) + FORCED_PREFIX
        inputs = tokenizer(text, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=MAX_NEW,
                                 do_sample=False)
        gen = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:],
                               skip_special_tokens=True)
        answer = FORCED_PREFIX + gen
        verdict = run_judge(model, tokenizer, device, r["question"],
                            r["expected"], r.get("alternatives") or [], answer)
        rows.append({"id": r["id"], "judge_label": verdict["label"],
                     "text_head": answer[:120]})
        print(f"{r['id']} -> {verdict['label']} | {answer[:70]!r}", flush=True)

    n = len(rows)
    counts = {}
    for row in rows:
        counts[row["judge_label"]] = counts.get(row["judge_label"], 0) + 1
    out = {
        "forced_prefix": FORCED_PREFIX,
        "n": n,
        "rates": {k: v / n for k, v in sorted(counts.items())},
        "intervention_reference": {
            "judge_refusal_rate_alpha_1500": 0.30,
            "judge_refusal_rate_alpha_3000": 0.30,
            "first_token_opener_rate_alpha_1500": 0.97,
        },
        "rows": rows,
    }
    out_path = FIGURES_DIR / "prefix_forcing_control.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["rates"], indent=1))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
