"""Logit-lens projection of the layer-18 correctness direction.

Companion to analysis/make_probe_direction_atlas.py (which projects the
layer-28 refusal-vs-wrong direction): recovers the correct-vs-rest probe
direction on all 784 ConfabQA items at the correctness-probe peak layer
and pushes it through the model's final RMSNorm and tied LM head.

Writes figures/correctness_direction_lens.json with the top/bottom-20
tokens by logit-lens score. Reads the cached activations; needs the
subject model from HF Hub. Run from the repo root:
    python -m analysis.correctness_direction_lens
"""
import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import analysis.make_probe_direction_atlas as atlas
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds

CORRECTNESS_LAYER = 18  # correctness-probe peak layer (paper Table 5)


def main():
    set_seeds()
    atlas.PROBE_LAYER = CORRECTNESS_LAYER
    items = atlas.load_subset({"correct", "refusal", "wrong"})
    d = atlas.recover_direction(items, "correct")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32).to(get_device())
    model.eval()
    top, bot, _ = atlas.project_through_lm_head(d["direction_raw"], model, tokenizer)

    out = {
        "layer": CORRECTNESS_LAYER,
        "target": "correct (vs refusal+wrong)",
        "n_items": len(items),
        "pipeline": "StandardScaler -> PCA(16) -> LogisticRegression, full fit",
        "top_tokens": [[t, round(float(s), 2)] for t, s in top[:20]],
        "bottom_tokens": [[t, round(float(s), 2)] for t, s in bot[:20]],
    }
    out_path = FIGURES_DIR / "correctness_direction_lens.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
