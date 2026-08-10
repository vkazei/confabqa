"""Sweep over SAE layers to find best base->instruct transfer.

For each candidate layer, load the SAE, encode/decode v1.3 hidden states,
report explained variance + L0. Pick the layer with the best EV that still
overlaps with the refusal-vs-wrong probe peak band (Section 6.4: layers 20-28).
"""
import json
from pathlib import Path
import numpy as np
import torch
from sae_lens import SAE

SAE_RELEASE = "qwen-scope-3-1.7b-base-w32k-l50"
LAYERS = [10, 14, 18, 20, 22, 24, 26, 27]
RESPONSES_DIR = Path("data/responses/qwen3_1_7b")
ACTIVATIONS_DIR = Path("data/activations/qwen3_1_7b")


def load_sample(layer, n=200):
    out = []
    for f in sorted(RESPONSES_DIR.glob("*.json"))[:n]:
        r = json.load(open(f))
        act_path = ACTIVATIONS_DIR / f"{r['question_id']}.pt"
        if not act_path.exists():
            continue
        act = torch.load(act_path, weights_only=False)
        out.append(act["last_prompt_hidden"][layer].numpy())
    return np.stack(out)


def main():
    print(f"{'layer':>6} {'EV mean':>8} {'EV med':>8} {'cos mean':>9} {'L0':>5}")
    for layer in LAYERS:
        try:
            sae = SAE.from_pretrained(release=SAE_RELEASE, sae_id=f"layer{layer}", device="cpu")
        except Exception as e:
            print(f"{layer:>6} skipped: {e}")
            continue
        X = torch.from_numpy(load_sample(layer)).float()
        with torch.no_grad():
            feats = sae.encode(X)
            recon = sae.decode(feats)
        mse = ((X - recon) ** 2).mean(dim=1)
        var = X.var(dim=1, unbiased=False)
        ev = 1 - mse / (var + 1e-9)
        cos = torch.nn.functional.cosine_similarity(X, recon, dim=1)
        l0 = (feats > 0).float().sum(dim=1).mean().item()
        print(f"{layer:>6} {ev.mean().item():>8.3f} {ev.median().item():>8.3f} {cos.mean().item():>9.3f} {l0:>5.1f}")


if __name__ == "__main__":
    main()
