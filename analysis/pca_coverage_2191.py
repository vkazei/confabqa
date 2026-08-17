"""How much of SAE feature 2191 the probe's PCA subspace can see.

The probe pipeline's reachable gradient directions in raw hidden-state
space are span{v_k / sigma} for the top-k standardized principal
components (Section 2.3), so the projection of W_dec_hat[2191] onto
that subspace is a ceiling on the alignment any pipeline probe can
have with the feature. Computes the coverage curve over k.

Writes figures/qwen3_1_7b/pca_coverage_2191.json.
Run from the repo root: python -m analysis.pca_coverage_2191
"""
import json

import numpy as np
from sae_lens import SAE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import analysis.make_probe_direction_atlas as atlas
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, set_seeds

KS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 549]


def main():
    set_seeds()
    items = atlas.load_subset({"refusal", "wrong"})
    H = np.stack([r["h"] for r in items])
    scaler = StandardScaler().fit(H)
    pca = PCA(n_components=min(H.shape)).fit(scaler.transform(H))
    V, sigma = pca.components_, scaler.scale_

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    d = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID]
    d = d / np.linalg.norm(d)

    def coverage(k):
        E = V[:k] / sigma
        c, *_ = np.linalg.lstsq(E.T, d, rcond=None)
        return float(np.linalg.norm(E.T @ c))

    curve = {str(k): round(coverage(k), 4) for k in KS}
    out = {"feature": SAE_FEATURE_ID, "n_items": int(H.shape[0]),
           "max_achievable_cos_by_k": curve,
           "observed_probe_cos": 0.161}
    out_path = FIGURES_DIR / "pca_coverage_2191.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(curve, indent=1))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
