"""Judge-label refusal rate under the feature-2191 intervention.

The Section 6.3.1 dose-response read next-token distributions only.
This script closes the loop for the strict criterion: generate full
continuations with alpha * W_dec_hat[2191] added at the Section 6.2
intervention point, on the SAME 30 originally-wrong items as the probe
intervention and the prefix-forcing control (read from
figures/qwen3_1_7b/13_intervention_results.json), and re-judge with the
three-way judge. Comparable numbers: probe direction 30% judge-refusals
at alpha=+1500; literal "As" forcing 37%.

Writes figures/qwen3_1_7b/sae_feature_refusal_rate.json.
Run from the repo root: python -m analysis.sae_feature_refusal_rate
"""
import json

import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

import analysis.make_causal_intervention as mci
from analysis.make_causal_intervention import generate_with_intervention
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from judge import judge as run_judge

ALPHAS = [750.0, 1500.0]


def main():
    set_seeds()
    art = json.load(open(FIGURES_DIR / "13_intervention_results.json"))
    items = art["wrong_subset"]

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    d_f = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID]
    d_f = d_f / np.linalg.norm(d_f)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    device = get_device()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16).to(device)
    model.eval()
    direction_t = torch.tensor(d_f, dtype=model.dtype, device=device)

    rows = []
    for alpha in ALPHAS:
        for r in items:
            text = generate_with_intervention(
                model, tokenizer, device, r["question"], direction_t, alpha)
            verdict = run_judge(model, tokenizer, device, r["question"],
                                r["expected"], r.get("alternatives") or [],
                                text)
            rows.append({"id": r["id"], "alpha": alpha,
                         "judge_label": verdict["label"],
                         "text_head": text[:120]})
            print(f"a={alpha:+.0f} {r['id']} -> {verdict['label']}",
                  flush=True)

    summary = {}
    for alpha in ALPHAS:
        sub = [x for x in rows if x["alpha"] == alpha]
        n = len(sub)
        summary[str(alpha)] = {
            lab: sum(x["judge_label"] == lab for x in sub) / n
            for lab in ("correct", "refusal", "wrong")}

    out = {"feature": SAE_FEATURE_ID, "alphas": ALPHAS, "n": len(items),
           "summary": summary,
           "reference": {"probe_alpha_1500_judge_refusal": 0.30,
                         "prefix_forcing_As_judge_refusal": 0.367},
           "rows": rows}
    out_path = FIGURES_DIR / "sae_feature_refusal_rate.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
