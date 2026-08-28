"""SAE decomposition of the refusal direction, in the SAE's own geometry.

Supersedes the activation statistics of sae_decompose_refusal.py, which
fed the cached final NORMED state (HF hidden-states index 28) to a
dictionary whose declared hook is blocks.27.hook_resid_post with
normalize_activations='none'. This script uses the true post-block-27
residuals (analysis/cache_prenorm_states.py).

Views:
  B) decoder alignment W_dec . w_refusal (geometry, unchanged);
  C) standardized activation differential refusal-vs-wrong on pre-norm
     codes;
  A') direct encoding of the refusal direction placed at the typical
      state magnitude (encode(||h||_bar * w_hat)); the original view A
      encoded the raw 0.37-norm direction, which is bias-dominated for
      a scale-sensitive encoder.

Also records, for a shortlist of ensemble features: hit rates by label,
mean activations, decoder-lens top tokens, and top max-activating
prompts; plus base->instruct reconstruction quality at the declared
hook (per-item EV and cosine, the D.2 numbers).

Writes figures/sae_decompose_prenorm.json.
Run from the repo root: python -m saes.sae_decompose_prenorm
"""
import json

import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

from analysis.cache_prenorm_states import load_prenorm
import analysis.make_probe_direction_atlas as atlas
from saes.sae_decompose_refusal import logit_lens_top_tokens
from confabqa.constants import SAE_RELEASE, SAE_LAYER
from config import MODEL_ID, get_device, set_seeds
from pathlib import Path

TOP_K = 20
SHORTLIST = [2191, 14034, 17077, 4314, 14361, 16612, 8875, 27369,
             18937, 21750]


def main():
    set_seeds()
    items, H = load_prenorm({"refusal", "wrong"})
    labs = np.array([r["judge_label"] for r in items])
    ref, wrg = labs == "refusal", labs == "wrong"

    # the probe direction (recovered from the states the probes read)
    d = atlas.recover_direction(atlas.load_subset({"refusal", "wrong"}),
                                "refusal")
    w = d["direction_raw"]
    w_hat = w / np.linalg.norm(w)

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    W_dec = sae.W_dec.detach().cpu().numpy()
    with torch.no_grad():
        A = sae.encode(torch.from_numpy(H).float()).numpy()
        R = sae.decode(torch.from_numpy(A)).numpy()

    # D.2 numbers: per-item EV and cosine at the declared hook
    mse = ((H - R) ** 2).mean(1)
    var = H.var(1)
    ev_item = 1 - mse / (var + 1e-9)
    cos_item = (H * R).sum(1) / (np.linalg.norm(H, axis=1)
                                 * np.linalg.norm(R, axis=1) + 1e-9)

    # View C
    mu_r, mu_w = A[ref].mean(0), A[wrg].mean(0)
    var_p = (A[ref].var(0) * ref.sum() + A[wrg].var(0) * wrg.sum()) / len(labs)
    diff_z = (mu_r - mu_w) / (np.sqrt(var_p) + 1e-9)
    C_rank = np.argsort(diff_z)[::-1][:TOP_K]

    # View B (unchanged geometry)
    align = W_dec @ w
    B_rank = np.argsort(align)[::-1][:TOP_K]

    # View A': encode the direction at typical state magnitude
    scale = float(np.linalg.norm(H, axis=1).mean())
    with torch.no_grad():
        a_dir = sae.encode(torch.from_numpy(
            (scale * w_hat)[None].astype(np.float32))).numpy()[0]
    A_rank = np.argsort(a_dir)[::-1][:TOP_K]

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32).to(get_device())
    model.eval()

    feats = {}
    for fid in sorted(set(SHORTLIST) | set(map(int, C_rank[:8]))):
        top_tok, _ = logit_lens_top_tokens(W_dec[fid].astype(np.float32),
                                           model, tokenizer)
        order = np.argsort(A[:, fid])[::-1][:5]
        feats[str(fid)] = {
            "diff_z": round(float(diff_z[fid]), 3),
            "rank_C": int((diff_z > diff_z[fid]).sum()) + 1,
            "decoder_alignment": round(float(align[fid]), 4),
            "hit_rate_refusal": round(float((A[ref, fid] > 0).mean()), 4),
            "hit_rate_wrong": round(float((A[wrg, fid] > 0).mean()), 4),
            "mean_act_refusal": round(float(A[ref, fid].mean()), 2),
            "lens_top": [t for _, t, _ in top_tok[:8]],
            "max_activating": [
                {"id": items[i]["question_id"],
                 "label": items[i]["judge_label"],
                 "act": round(float(A[i, fid]), 1),
                 "q": items[i]["question"][:90]} for i in order],
        }

    out = {
        "geometry": "post-block-27 residual (blocks.27.hook_resid_post), "
                    "normalize_activations=none",
        "n_refusal": int(ref.sum()), "n_wrong": int(wrg.sum()),
        "reconstruction": {
            "ev_per_item_mean": round(float(ev_item.mean()), 4),
            "ev_per_item_median": round(float(np.median(ev_item)), 4),
            "cos_mean": round(float(cos_item.mean()), 4),
        },
        "state_norm_mean": round(scale, 1),
        "view_C_top": [int(f) for f in C_rank],
        "view_B_top": [int(f) for f in B_rank],
        "view_Aprime_top": [int(f) for f in A_rank],
        "features": feats,
    }
    out_path = Path("figures") / "sae_decompose_prenorm.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["reconstruction"], indent=1))
    print("C top8:", out["view_C_top"][:8])
    print("B top8:", out["view_B_top"][:8])
    print("A' top8:", out["view_Aprime_top"][:8])
    for fid in ("2191", "14034", "17077", "4314"):
        ft = feats[fid]
        print(f"f{fid}: z={ft['diff_z']} hit {ft['hit_rate_refusal']:.0%}/"
              f"{ft['hit_rate_wrong']:.0%} lens={ft['lens_top'][:4]}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
