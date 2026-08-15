"""SAE feature decomposition of the Qwen3-1.7B refusal direction.

For Anthropic-Interp-team consumption. Takes the layer-28 refusal-vs-wrong
probe direction recovered in `make_probe_direction_atlas.py` and decomposes
it into a sparse mix of Qwen-Scope SAE features. Reports for each top
feature:

  - decoder direction's logit-lens projection (top output tokens)
  - top max-activating prompts from v1.3 (interpretable example pool)
  - empirical activation differential between refusal and wrong items
  - direct encoding weight (what fraction of the refusal direction the
    feature accounts for under the SAE's own sparse code)

Three orthogonal views are reported:
  A) Direct encoding: SAE.encode(refusal_direction) -> sparse decomposition.
     The SAE's own answer to "what features compose this direction".
  B) Decoder alignment: SAE.W_dec @ refusal_direction -> linear alignment
     per feature. Useful as a sanity check on (A) without the encoder
     nonlinearity.
  C) Empirical activation differential: for each feature, the mean activation
     on refusal items minus wrong items, normalized by pooled std. This is
     a "what features actually fire on real refusals" measure, independent
     of the probe direction.

The SAE is qwen-scope-3-1.7b-base-w32k-l50, trained on Qwen3-1.7B-Base. Our
subject model is Qwen3-1.7B-Instruct. Reconstruction quality on Instruct
activations at layer 27 (=HF idx 28, our probe peak) is EV=0.82, cos=0.90 —
acceptable transfer (`sae_layer_sweep.py`).

Outputs:
  figures/sae_decompose_refusal.{json,md}
  figures/sae_decompose_refusal_top_features.png  (heatmap of top features
    by activation across refusal / wrong items)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch
from sae_lens import SAE
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from transformers import AutoModelForCausalLM, AutoTokenizer

from confabqa.constants import (SAE_RELEASE, SAE_LAYER,
                                SAE_HF_LAYER as HF_LAYER)
SAE_ID = f"layer{SAE_LAYER}"
MODEL_ID = "Qwen/Qwen3-1.7B"
RESPONSES_DIR = Path("data/responses/qwen3_1_7b")
ACTIVATIONS_DIR = Path("data/activations/qwen3_1_7b")

PCA_N = 16
TOP_K_FEATURES = 20
TOP_K_TOKENS = 12
TOP_K_PROMPTS = 5

OUT_JSON = Path("figures") / "sae_decompose_refusal.json"
OUT_MD = Path("figures") / "sae_decompose_refusal.md"
OUT_PNG = Path("figures") / "sae_decompose_refusal_top_features.png"


def load_refusal_vs_wrong():
    items = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        r = json.load(open(f))
        if r.get("judge_label") not in ("refusal", "wrong"):
            continue
        act = torch.load(ACTIVATIONS_DIR / f"{r['question_id']}.pt", weights_only=False)
        r["h"] = act["last_prompt_hidden"][HF_LAYER].numpy()
        items.append(r)
    return items


def recover_direction(items):
    X = np.stack([r["h"] for r in items])
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in items])
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    pca = PCA(n_components=PCA_N).fit(Xs)
    Xp = pca.transform(Xs)
    lr = LogisticRegression(max_iter=2000, C=1.0).fit(Xp, y)
    w_pca = lr.coef_[0]
    w_std = pca.components_.T @ w_pca
    w_raw = w_std / scaler.scale_
    scores = Xp @ w_pca
    if scores[y == 1].mean() < scores[y == 0].mean():
        w_pca, w_std, w_raw, scores = -w_pca, -w_std, -w_raw, -scores
    return w_raw, scores, y


def logit_lens_top_tokens(direction, model, tokenizer, k=TOP_K_TOKENS):
    """Project a direction through final RMSNorm + LM head, return top/bottom token strings."""
    device = next(model.parameters()).device
    h = torch.tensor(direction, dtype=model.dtype, device=device).unsqueeze(0)
    with torch.no_grad():
        # Approximate final RMSNorm by L2-normalization (preserves token-direction angles)
        h_norm = h / (h.norm(dim=-1, keepdim=True) + 1e-9) * np.sqrt(h.shape[-1])
        h_norm = model.model.norm(h_norm)
        logits = (h_norm @ model.lm_head.weight.T.to(model.dtype)).squeeze(0).float().cpu().numpy()
    order = np.argsort(logits)
    top = order[::-1][:k]
    bot = order[:k]
    return ([(int(t), tokenizer.decode([int(t)]), float(logits[t])) for t in top],
            [(int(t), tokenizer.decode([int(t)]), float(logits[t])) for t in bot])


def main():
    print("Loading SAE...")
    sae = SAE.from_pretrained(release=SAE_RELEASE, sae_id=SAE_ID, device="cpu")
    print(f"  d_in={sae.cfg.d_in}, d_sae={sae.cfg.d_sae}")

    print("Loading refusal+wrong items...")
    items = load_refusal_vs_wrong()
    print(f"  n={len(items)} ({sum(1 for r in items if r['judge_label']=='refusal')} refusal, "
          f"{sum(1 for r in items if r['judge_label']=='wrong')} wrong)")

    print("Recovering refusal direction...")
    refusal_dir, _, y = recover_direction(items)
    print(f"  direction L2-norm: {np.linalg.norm(refusal_dir):.4f}")

    # ============= View A: direct encoding =============
    print("\nView A: direct encoding of refusal direction through SAE")
    rd_t = torch.from_numpy(refusal_dir).float().unsqueeze(0)
    with torch.no_grad():
        feats_dir = sae.encode(rd_t).squeeze(0).numpy()
    nonzero = np.where(feats_dir > 0)[0]
    print(f"  active features in direct encoding: {len(nonzero)} / {sae.cfg.d_sae}")
    # Rank by direct encoding magnitude
    A_rank = np.argsort(feats_dir)[::-1][:TOP_K_FEATURES]

    # ============= View B: decoder alignment =============
    print("\nView B: decoder alignment with refusal direction")
    W_dec = sae.W_dec.detach().cpu().numpy()  # (d_sae, d_in)
    decoder_align = W_dec @ refusal_dir  # (d_sae,)
    # Norm normalized: feature i contributes (decoder_align[i]) per unit feature activation
    B_rank = np.argsort(decoder_align)[::-1][:TOP_K_FEATURES]

    # ============= View C: empirical activation differential =============
    print("\nView C: empirical activation differential on v1.3 items")
    X = torch.from_numpy(np.stack([r["h"] for r in items])).float()
    with torch.no_grad():
        feats_all = sae.encode(X).numpy()   # (n, d_sae)
    is_refusal = y == 1
    mu_r = feats_all[is_refusal].mean(axis=0)
    mu_w = feats_all[~is_refusal].mean(axis=0)
    pooled_std = feats_all.std(axis=0) + 1e-9
    diff_z = (mu_r - mu_w) / pooled_std
    hit_r = (feats_all[is_refusal] > 0).mean(axis=0)
    hit_w = (feats_all[~is_refusal] > 0).mean(axis=0)
    C_rank = np.argsort(diff_z)[::-1][:TOP_K_FEATURES]

    # ============= Union of top features for characterization =============
    union_top = sorted(set(A_rank.tolist()) | set(B_rank.tolist()) | set(C_rank.tolist()))
    print(f"\nUnion of top features across views A, B, C: {len(union_top)}")

    # ============= Logit-lens of each top feature's decoder =============
    print("\nLoading Qwen3 model for logit lens...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.bfloat16, device_map="cpu")
    model.eval()
    print("  loaded")

    feature_records = {}
    for i, fid in enumerate(union_top):
        if (i + 1) % 5 == 0:
            print(f"  characterized {i+1}/{len(union_top)} features")
        dec_dir = W_dec[fid]
        top_tok, bot_tok = logit_lens_top_tokens(dec_dir, model, tokenizer)
        # Top-K prompts by feature activation
        top_prompt_idx = np.argsort(feats_all[:, fid])[::-1][:TOP_K_PROMPTS]
        top_prompts = []
        for idx in top_prompt_idx:
            top_prompts.append({
                "qid": items[idx]["question_id"],
                "question": items[idx]["question"][:120],
                "judge_label": items[idx]["judge_label"],
                "activation": float(feats_all[idx, fid]),
            })
        feature_records[int(fid)] = {
            "fid": int(fid),
            "direct_encoding": float(feats_dir[fid]),
            "decoder_alignment": float(decoder_align[fid]),
            "diff_z": float(diff_z[fid]),
            "mean_activation_refusal": float(mu_r[fid]),
            "mean_activation_wrong": float(mu_w[fid]),
            "hit_rate_refusal": float(hit_r[fid]),
            "hit_rate_wrong": float(hit_w[fid]),
            "top_tokens": [t[1] for t in top_tok],
            "bottom_tokens": [t[1] for t in bot_tok],
            "top_prompts": top_prompts,
        }

    # ============= Baseline: refusal direction's own logit lens =============
    print("\nBaseline: refusal direction logit lens (Section 6.6)")
    rd_top, rd_bot = logit_lens_top_tokens(refusal_dir, model, tokenizer)
    print(f"  top tokens: {[t[1] for t in rd_top[:10]]}")
    print(f"  bot tokens: {[t[1] for t in rd_bot[:10]]}")

    # ============= Save outputs =============
    output = {
        "metadata": {
            "model": MODEL_ID,
            "sae_release": SAE_RELEASE,
            "sae_id": SAE_ID,
            "hf_layer": HF_LAYER,
            "n_items": len(items),
            "n_refusal": int(is_refusal.sum()),
            "n_wrong": int((~is_refusal).sum()),
            "pca_n": PCA_N,
            "d_in": int(sae.cfg.d_in),
            "d_sae": int(sae.cfg.d_sae),
        },
        "refusal_direction_logit_lens": {
            "top_tokens": [(t[1], t[2]) for t in rd_top],
            "bottom_tokens": [(t[1], t[2]) for t in rd_bot],
        },
        "view_a_direct_encoding_top": [int(f) for f in A_rank.tolist()],
        "view_b_decoder_alignment_top": [int(f) for f in B_rank.tolist()],
        "view_c_activation_diff_top": [int(f) for f in C_rank.tolist()],
        "features": feature_records,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as fp:
        json.dump(output, fp, indent=2, ensure_ascii=False)
    print(f"\nWrote {OUT_JSON}")

    # ============= Markdown report =============
    md = []
    md.append("# SAE feature decomposition of the Qwen3-1.7B refusal direction\n\n")
    md.append(f"- **Model:** {MODEL_ID} (Instruct)\n")
    md.append(f"- **SAE:** {SAE_RELEASE} (trained on Qwen3-1.7B-Base; transfer EV=0.82 at this layer)\n")
    md.append(f"- **Layer:** HF index {HF_LAYER} (= SAE layer{SAE_LAYER}; refusal-vs-wrong probe peak)\n")
    md.append(f"- **d_in={sae.cfg.d_in}, d_sae={sae.cfg.d_sae}**\n")
    md.append(f"- **n items:** {len(items)} ({int(is_refusal.sum())} refusal + {int((~is_refusal).sum())} wrong)\n\n")

    md.append("## Baseline: refusal direction's own logit lens (replicates Section 6.6)\n\n")
    md.append(f"- **Top tokens (push toward refusal):** {', '.join(repr(t[1]) for t in rd_top[:12])}\n")
    md.append(f"- **Bottom tokens (push away from refusal):** {', '.join(repr(t[1]) for t in rd_bot[:12])}\n\n")

    md.append("## Three views of which SAE features compose the refusal direction\n\n")
    md.append("- **View A (direct encoding):** SAE.encode(refusal_direction) — the SAE's own sparse decomposition.\n")
    md.append("- **View B (decoder alignment):** W_dec @ refusal_direction — linear alignment per feature.\n")
    md.append("- **View C (activation differential):** standardized mean-activation gap between refusal and wrong items.\n\n")
    md.append("Convergent features (appearing in multiple top-K lists) are the most robust.\n\n")

    md.append("### Top features (union of views A, B, C top-" + str(TOP_K_FEATURES) + ")\n\n")
    md.append("| fid | view A rank | view B rank | view C rank | diff_z | hit% refusal | hit% wrong | top tokens (decoder logit-lens) |\n")
    md.append("|--:|---:|---:|---:|--:|--:|--:|---|\n")
    A_set = list(A_rank); B_set = list(B_rank); C_set = list(C_rank)
    rows = []
    for fid in union_top:
        ar = (A_set.index(fid) + 1) if fid in A_set else None
        br = (B_set.index(fid) + 1) if fid in B_set else None
        cr = (C_set.index(fid) + 1) if fid in C_set else None
        rows.append((fid, ar, br, cr))
    # Sort: features appearing in most views first, then by best rank
    rows.sort(key=lambda r: (-sum(x is not None for x in r[1:]), min(x for x in r[1:] if x is not None)))
    for fid, ar, br, cr in rows:
        r = feature_records[fid]
        a_str = str(ar) if ar else "—"
        b_str = str(br) if br else "—"
        c_str = str(cr) if cr else "—"
        tok_str = ", ".join(repr(t) for t in r["top_tokens"][:8])
        md.append(f"| {fid} | {a_str} | {b_str} | {c_str} | "
                  f"{r['diff_z']:+.2f} | {r['hit_rate_refusal']*100:.0f} | {r['hit_rate_wrong']*100:.0f} | "
                  f"{tok_str} |\n")

    md.append("\n### Per-feature detail (sorted by view-C rank)\n\n")
    rows_c = [(fid, C_set.index(fid)) for fid in union_top if fid in C_set]
    rows_c.sort(key=lambda x: x[1])
    for fid, cr in rows_c[:15]:
        r = feature_records[fid]
        md.append(f"#### Feature {fid}\n")
        md.append(f"- **Activation differential:** refusal mean {r['mean_activation_refusal']:.3f} vs wrong {r['mean_activation_wrong']:.3f} "
                  f"(z={r['diff_z']:+.2f}); hit rate {r['hit_rate_refusal']*100:.1f}% refusal vs {r['hit_rate_wrong']*100:.1f}% wrong\n")
        md.append(f"- **Decoder logit-lens top tokens:** {', '.join(repr(t) for t in r['top_tokens'])}\n")
        md.append(f"- **Top {TOP_K_PROMPTS} max-activating prompts:**\n")
        for p in r["top_prompts"]:
            md.append(f"  - `[{p['judge_label']}]` (act={p['activation']:.2f}) {p['qid']}: {p['question']!r}\n")
        md.append("\n")

    OUT_MD.write_text("".join(md))
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
