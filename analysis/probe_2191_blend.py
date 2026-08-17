"""Does blending the probe direction with feature 2191 improve the split?

Feature 2191's decoder direction lies mostly outside the probe
pipeline's 16-PC subspace (Appendix/6.3 coverage: max cos 0.37), so a
blend w(lambda) = normalize((1-lambda) * w_probe_hat + lambda * d_2191_hat)
can reach directions no pipeline probe can. 5-fold stratified CV on the
n=549 refusal+wrong subset: the probe is re-recovered on each training
fold, blends are evaluated on the held-out fold by ROC AUC of the raw
projection h . w(lambda). Also fits a two-feature logistic stack
[h . w_probe, h . d_2191] per fold as the adaptive-blend reference.

Writes figures/qwen3_1_7b/probe_2191_blend.json.
Run from the repo root: python -m analysis.probe_2191_blend
"""
import json

import numpy as np
from sae_lens import SAE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

import analysis.make_probe_direction_atlas as atlas
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, set_seeds

LAMBDAS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def main():
    set_seeds()
    items = atlas.load_subset({"refusal", "wrong"})
    H = np.stack([r["h"] for r in items])
    y = np.array([1 if r["judge_label"] == "refusal" else 0 for r in items])

    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    d_f = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID]
    d_f = d_f / np.linalg.norm(d_f)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    auc_per_lambda = {lam: [] for lam in LAMBDAS}
    auc_stack, auc_2191_only = [], []

    class _Sub(list):
        pass

    for tr, te in skf.split(H, y):
        train_items = [items[i] for i in tr]
        d = atlas.recover_direction(train_items, "refusal")
        w = d["direction_raw"]
        w_hat = w / np.linalg.norm(w)
        for lam in LAMBDAS:
            v = (1 - lam) * w_hat + lam * d_f
            v = v / np.linalg.norm(v)
            auc_per_lambda[lam].append(
                roc_auc_score(y[te], H[te] @ v))
        # adaptive two-feature stack
        Ztr = np.stack([H[tr] @ w_hat, H[tr] @ d_f], axis=1)
        Zte = np.stack([H[te] @ w_hat, H[te] @ d_f], axis=1)
        lr = LogisticRegression(max_iter=2000, C=1.0).fit(Ztr, y[tr])
        auc_stack.append(roc_auc_score(y[te], lr.decision_function(Zte)))
        auc_2191_only.append(roc_auc_score(y[te], H[te] @ d_f))

    out = {
        "n": int(len(y)), "folds": 5,
        "auc_by_lambda": {str(lam): {
            "mean": round(float(np.mean(v)), 4),
            "std": round(float(np.std(v)), 4)}
            for lam, v in auc_per_lambda.items()},
        "auc_two_feature_stack": {
            "mean": round(float(np.mean(auc_stack)), 4),
            "std": round(float(np.std(auc_stack)), 4)},
        "auc_2191_projection_only": {
            "mean": round(float(np.mean(auc_2191_only)), 4),
            "std": round(float(np.std(auc_2191_only)), 4)},
    }
    out_path = FIGURES_DIR / "probe_2191_blend.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    for lam in LAMBDAS:
        m = out["auc_by_lambda"][str(lam)]
        print(f"lambda={lam:.1f}  AUC = {m['mean']:.4f} +- {m['std']:.4f}")
    print("stack:", out["auc_two_feature_stack"],
          "| 2191 only:", out["auc_2191_projection_only"])
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
