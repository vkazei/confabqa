"""Decoder-space neighbors of the Section 6.3 ensemble features.

For each ensemble feature: nearest dictionary neighbors under raw
decoder cosine and under the dual-code similarity d_f^T G^{-1} d_g
(G = W_dec^T W_dec), with lens labels; and the ConfabQA hit rates of
feature 2191's "as-family" (its nearest decoder neighbors), computed
on the pre-norm residuals, as a feature-splitting check.

Writes figures/qwen3_1_7b/sae_feature_neighbors.json.
Run from the repo root: python -m saes.sae_feature_neighbors
"""
import json

import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.cache_prenorm_states import load_prenorm
from saes.sae_decompose_refusal import logit_lens_top_tokens
from confabqa.constants import SAE_RELEASE, SAE_LAYER
from config import FIGURES_DIR, MODEL_ID, set_seeds

FEATURES = [2191, 14034, 17077, 4314]
TOP_N = 6


def main():
    set_seeds()
    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    W = sae.W_dec.detach().cpu().numpy().astype(np.float64)
    G = W.T @ W
    Ginv = np.linalg.inv(G + 1e-8 * np.eye(W.shape[1]))
    Wg = W @ Ginv
    dual_self = np.einsum("fd,fd->f", Wg, W)

    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    # lens labels only need the final norm and the (tied) LM head;
    # load light and free the blocks to keep the footprint small
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16).to(torch.device("cpu"))
    model.eval()
    model.model.layers = torch.nn.ModuleList()

    def label(g):
        top, _ = logit_lens_top_tokens(W[g].astype(np.float32), model, tok)
        return [t for _, t, _ in top[:3]]

    out = {"features": {}}
    for f in FEATURES:
        raw = W @ W[f]
        dual = Wg @ W[f] / np.sqrt(dual_self * dual_self[f])
        def nb(s):
            top = [g for g in np.argsort(s)[::-1] if g != f][:TOP_N]
            return [{"fid": int(g), "sim": round(float(s[g]), 3),
                     "lens": label(int(g))} for g in top]
        out["features"][str(f)] = {"raw_cos": nb(raw), "dual_cos": nb(dual)}

    items, H = load_prenorm({"refusal", "wrong"})
    labs = np.array([r["judge_label"] for r in items])
    with torch.no_grad():
        A = sae.encode(torch.from_numpy(H).float()).numpy()
    family = [2191] + [n["fid"] for n in out["features"]["2191"]["raw_cos"][:4]]
    ref, wrg = labs == "refusal", labs == "wrong"
    out["as_family_hit_rates"] = {
        str(f): {"refusal": round(float((A[ref, f] > 0).mean()), 4),
                 "wrong": round(float((A[wrg, f] > 0).mean()), 4)}
        for f in family}
    out["as_family_union"] = {
        "refusal": round(float((A[ref][:, family] > 0).any(1).mean()), 4),
        "wrong": round(float((A[wrg][:, family] > 0).any(1).mean()), 4)}

    out_path = FIGURES_DIR / "sae_feature_neighbors.json"
    with open(out_path, "w") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
