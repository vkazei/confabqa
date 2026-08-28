"""Which SAE features fire for wrong responses? (pre-norm geometry)

Mirror of Section 6.3's view C, which asked what fires for refusals.
Three contrasts over all 784 ConfabQA layer-28 states, each ranking
features by the standardized activation differential (diff-z, same
formula as the decompose script):

  (a) wrong vs correct, all items;
  (b) wrong vs correct, pre-cutoff items only (the disconfounded
      version: recency cues cannot masquerade as confabulation
      detectors);
  (c) wrong vs refusal (the negative tail of view C).

For the top features of each contrast, records diff-z, per-class hit
rates, top decoder logit-lens tokens, and the three max-activating
prompts.

Writes figures/qwen3_1_7b/sae_wrong_features.json.
Run from the repo root: python -m saes.sae_wrong_features
"""
import json

import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.cache_prenorm_states import load_prenorm
from saes.sae_decompose_refusal import logit_lens_top_tokens
from confabqa.constants import SAE_RELEASE, SAE_LAYER
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds

TOP_N = 8


def diff_z(acts, mask_a, mask_b):
    mu_a, mu_b = acts[mask_a].mean(0), acts[mask_b].mean(0)
    var = (acts[mask_a].var(0) * mask_a.sum() +
           acts[mask_b].var(0) * mask_b.sum()) / (mask_a.sum() + mask_b.sum())
    return (mu_a - mu_b) / (np.sqrt(var) + 1e-9)


def main():
    set_seeds()
    items, H = load_prenorm({"correct", "refusal", "wrong"})
    labs = np.array([r["judge_label"] for r in items])
    pre = np.array([r["cutoff_class"] == "pre" for r in items])

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    with torch.no_grad():
        A = sae.encode(torch.from_numpy(H).float()).numpy()
    W_dec = sae.W_dec.detach().cpu().numpy()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32).to(get_device())
    model.eval()

    contrasts = {
        "wrong_vs_correct": (labs == "wrong", labs == "correct"),
        "wrong_vs_correct_within_pre": (
            (labs == "wrong") & pre, (labs == "correct") & pre),
        "wrong_vs_refusal": (labs == "wrong", labs == "refusal"),
    }
    out = {"n_items": len(items), "contrasts": {}}
    for name, (ma, mb) in contrasts.items():
        z = diff_z(A, ma, mb)
        rank = np.argsort(z)[::-1][:TOP_N]
        feats = []
        for fid in rank:
            fid = int(fid)
            top_tok, _ = logit_lens_top_tokens(W_dec[fid], model, tokenizer)
            act_order = np.argsort(A[:, fid])[::-1][:3]
            feats.append({
                "fid": fid,
                "diff_z": round(float(z[fid]), 3),
                "hit_rate": {lab: round(float((A[labs == lab, fid] > 0).mean()), 3)
                             for lab in ("correct", "refusal", "wrong")},
                "lens_top_tokens": [tok for _, tok, _ in top_tok[:6]],
                "max_activating": [
                    {"id": items[i]["question_id"],
                     "label": items[i]["judge_label"],
                     "q": items[i]["question"][:90]}
                    for i in act_order],
            })
        out["contrasts"][name] = {
            "n_a": int(ma.sum()), "n_b": int(mb.sum()), "top_features": feats}

    out_path = FIGURES_DIR / "sae_wrong_features.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for name, c in out["contrasts"].items():
        print(f"== {name} (n={c['n_a']} vs {c['n_b']})")
        for ft in c["top_features"][:5]:
            print(f"  f{ft['fid']:>6} z={ft['diff_z']:+.2f} "
                  f"hit c/r/w={ft['hit_rate']['correct']:.2f}/"
                  f"{ft['hit_rate']['refusal']:.2f}/{ft['hit_rate']['wrong']:.2f} "
                  f"tokens={ft['lens_top_tokens'][:4]}")
            for m in ft["max_activating"][:2]:
                print(f"      [{m['label']:7s}] {m['q'][:70]}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
