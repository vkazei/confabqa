"""Sanity-check: can the Qwen-scope SAE (trained on Qwen3-1.7B-Base) reconstruct
hidden states from Qwen3-1.7B-Instruct cleanly?

If the explained-variance / reconstruction loss is poor, we either pivot to
a closer model or train a small SAE from scratch.

Test: load v1.3 last-prompt-token hidden states at layer 24 (mid-late, where
both the refusal probe shows signal and base->instruct SAE transfer is more
robust than at the very last layer). Encode/decode through the SAE; report:
  - reconstruction MSE relative to per-feature variance
  - cosine similarity between original and reconstructed vectors
  - explained variance (1 - MSE/Var)
  - sparsity stats (mean L0, max activation)

Acceptance threshold: explained variance >= 0.75 on instruct-model
activations. If lower, the base->instruct shift is dominating and we need a
different SAE.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch
from sae_lens import SAE

LAYER = 24
SAE_RELEASE = "qwen-scope-3-1.7b-base-w32k-l50"
SAE_ID = f"layer{LAYER}"
RESPONSES_DIR = Path("data/responses/qwen3_1_7b")
ACTIVATIONS_DIR = Path("data/activations/qwen3_1_7b")


def load_sample_activations(n=200):
    out = []
    files = sorted(RESPONSES_DIR.glob("*.json"))[:n]
    for f in files:
        r = json.load(open(f))
        act_path = ACTIVATIONS_DIR / f"{r['question_id']}.pt"
        if not act_path.exists():
            continue
        act = torch.load(act_path, weights_only=False)
        # last_prompt_hidden: (n_layers, d)
        h = act["last_prompt_hidden"][LAYER].numpy()
        out.append(h)
    return np.stack(out)


def main():
    print(f"Loading SAE: {SAE_RELEASE} / {SAE_ID}")
    sae, cfg_dict, sparsity = SAE.from_pretrained(
        release=SAE_RELEASE,
        sae_id=SAE_ID,
        device="cpu",
    )
    print(f"  loaded. d_in={sae.cfg.d_in}, d_sae={sae.cfg.d_sae}, "
          f"normalize={sae.cfg.normalize_activations}")

    print(f"\nLoading sample v1.3 activations at layer {LAYER}...")
    X = load_sample_activations(n=200)
    print(f"  shape: {X.shape}, dtype={X.dtype}")
    print(f"  per-vector mean norm: {np.linalg.norm(X, axis=1).mean():.2f}")
    print(f"  per-feature variance: mean={X.var(axis=0).mean():.4f}")

    X_t = torch.from_numpy(X).float()
    with torch.no_grad():
        features = sae.encode(X_t)
        recon = sae.decode(features)

    # Reconstruction quality
    mse = ((X_t - recon) ** 2).mean(dim=1)
    var = X_t.var(dim=1, unbiased=False)
    ev_per_item = 1 - mse / (var + 1e-9)
    cos = torch.nn.functional.cosine_similarity(X_t, recon, dim=1)

    print(f"\n=== reconstruction quality ===")
    print(f"  explained variance: mean={ev_per_item.mean().item():.4f}, "
          f"median={ev_per_item.median().item():.4f}, "
          f"min={ev_per_item.min().item():.4f}, max={ev_per_item.max().item():.4f}")
    print(f"  cosine similarity:  mean={cos.mean().item():.4f}, "
          f"median={cos.median().item():.4f}, "
          f"min={cos.min().item():.4f}")

    # Sparsity
    active = (features > 0).float().sum(dim=1)
    print(f"\n=== sparsity ===")
    print(f"  L0 (active features per item): mean={active.mean().item():.1f}, "
          f"median={active.median().item():.1f}, "
          f"max={active.max().item():.0f}, min={active.min().item():.0f}")
    max_act = features.max(dim=1).values
    print(f"  max activation per item: mean={max_act.mean().item():.3f}, "
          f"median={max_act.median().item():.3f}")

    # Verdict
    ev_mean = ev_per_item.mean().item()
    cos_mean = cos.mean().item()
    print(f"\n=== verdict ===")
    if ev_mean >= 0.75:
        print(f"  PASS: explained variance {ev_mean:.2f} >= 0.75 threshold")
        print(f"  Base->Instruct SAE transfer is acceptable. Proceed to feature attribution.")
    elif ev_mean >= 0.5:
        print(f"  MARGINAL: explained variance {ev_mean:.2f} in [0.5, 0.75)")
        print(f"  Transfer is partial. Try a different layer or accept a noisier decomposition.")
    else:
        print(f"  FAIL: explained variance {ev_mean:.2f} < 0.5")
        print(f"  Base->Instruct shift dominates. Pivot to gemma-scope on Gemma 2 2B or train custom.")


if __name__ == "__main__":
    main()
