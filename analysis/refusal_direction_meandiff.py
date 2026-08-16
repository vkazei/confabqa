"""Difference-in-means recovery of the refusal direction, vs the probe.

The probe direction of Section 6.1 is recovered through
StandardScaler -> PCA(16) -> LogisticRegression. The simplest
alternative is the class-mean difference used for safety-refusal
directions (Arditi et al. 2024): mean(refusal states) - mean(wrong
states) at the same layer (28). This script compares the two (cosine
in raw hidden-state space), also evaluates the *plain* mean of refusal
states as a control, and pushes all three vectors through the same
RMSNorm + tied-LM-head logit lens.

Writes figures/qwen3_1_7b/refusal_direction_meandiff.json.
Run from the repo root:
    python -m analysis.refusal_direction_meandiff
"""
import json

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import analysis.make_probe_direction_atlas as atlas
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds


def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main():
    set_seeds()
    items = atlas.load_subset({"refusal", "wrong"})
    d = atlas.recover_direction(items, "refusal")
    w_probe = d["direction_raw"]

    H_ref = np.stack([r["h"] for r in items if r["judge_label"] == "refusal"])
    H_wrong = np.stack([r["h"] for r in items if r["judge_label"] == "wrong"])
    mean_ref = H_ref.mean(axis=0)
    diff_means = mean_ref - H_wrong.mean(axis=0)
    # within post-cutoff: controls the topic difference (all refusals are
    # post-cutoff, so the full-subset diff also absorbs recency content)
    H_wrong_post = np.stack([r["h"] for r in items
                             if r["judge_label"] == "wrong"
                             and r["cutoff_class"] == "post"])
    diff_means_post = mean_ref - H_wrong_post.mean(axis=0)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32).to(get_device())
    model.eval()

    out = {
        "layer": int(atlas.PROBE_LAYER),
        "n_refusal": int(H_ref.shape[0]),
        "n_wrong": int(H_wrong.shape[0]),
        "n_wrong_post": int(H_wrong_post.shape[0]),
        "cosine": {
            "probe_vs_diff_means": cos(w_probe, diff_means),
            "probe_vs_diff_means_within_post": cos(w_probe, diff_means_post),
            "probe_vs_plain_refusal_mean": cos(w_probe, mean_ref),
            "diff_means_vs_plain_refusal_mean": cos(diff_means, mean_ref),
        },
        "lens": {},
    }
    for name, vec in [("probe", w_probe), ("diff_means", diff_means),
                      ("diff_means_within_post", diff_means_post),
                      ("plain_refusal_mean", mean_ref)]:
        top, bot, _ = atlas.project_through_lm_head(vec, model, tokenizer)
        out["lens"][name] = {
            "top": [[t, round(float(s), 2)] for t, s in top[:15]],
            "bottom": [[t, round(float(s), 2)] for t, s in bot[:10]],
        }
    top_probe = {t for t, _ in out["lens"]["probe"]["top"][:10]}
    top_dm = {t for t, _ in out["lens"]["diff_means"]["top"][:10]}
    out["top10_overlap_probe_vs_diff_means"] = len(top_probe & top_dm)

    out_path = FIGURES_DIR / "refusal_direction_meandiff.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "lens"}, indent=1))
    for name in out["lens"]:
        print(name, "top8:", [t for t, _ in out["lens"][name]["top"][:8]])
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
