"""Can the dormant apology register be activated? Push feature 14034.

Feature 14034's decoder logit-lens points at `Sorry`/`Oops` openers,
but the feature never fires on ConfabQA (0% hit rate): the paper calls
it a dormant refusal register. This script tests whether it is
causally available: add alpha * W_dec_hat[14034] at the Section 6.2
intervention point on the same 30 originally-wrong items as the other
causal runs, generate, and record (a) whether the first token lands in
the Sorry/Oops family, (b) the three-way judge label.

Writes figures/qwen3_1_7b/sae_apology_feature_test.json.
Run from the repo root: python -m analysis.sae_apology_feature_test
"""
import json

import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.make_causal_intervention import generate_with_intervention
from confabqa.constants import SAE_RELEASE, SAE_LAYER
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from judge import judge as run_judge

APOLOGY_FEATURE = 14034
ALPHAS = [750.0, 1500.0]
APOLOGY_OPENERS = ("Sorry", " Sorry", "sorry", " sorry", "Oops", " Oops")


def main():
    set_seeds()
    art = json.load(open(FIGURES_DIR / "13_intervention_results.json"))
    items = art["wrong_subset"]

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    d_f = sae.W_dec.detach().cpu().numpy()[APOLOGY_FEATURE]
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
            apology = text.startswith(APOLOGY_OPENERS)
            rows.append({"id": r["id"], "alpha": alpha,
                         "apology_opener": bool(apology),
                         "judge_label": verdict["label"],
                         "text_head": text[:120]})
            print(f"a={alpha:+.0f} {r['id']} apology={apology} "
                  f"-> {verdict['label']} | {text[:60]!r}", flush=True)

    summary = {}
    for alpha in ALPHAS:
        sub = [x for x in rows if x["alpha"] == alpha]
        n = len(sub)
        summary[str(alpha)] = {
            "apology_opener_rate": sum(x["apology_opener"] for x in sub) / n,
            **{lab: sum(x["judge_label"] == lab for x in sub) / n
               for lab in ("correct", "refusal", "wrong")}}

    out = {"feature": APOLOGY_FEATURE, "alphas": ALPHAS, "n": len(items),
           "apology_openers": list(APOLOGY_OPENERS),
           "summary": summary, "rows": rows}
    out_path = FIGURES_DIR / "sae_apology_feature_test.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
