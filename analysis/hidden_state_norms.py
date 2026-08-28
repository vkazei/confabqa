"""Distribution of the layer-28 last-prompt-token hidden-state RMS.

Supports the Section 6.1 magnitude discussion: rms(h) = ||h||/sqrt(d)
per item, overall and per judge label, across all 784 ConfabQA items.

Writes figures/qwen3_1_7b/hidden_state_norms.json.
Run from the repo root: python -m analysis.hidden_state_norms
"""
import json

import numpy as np
from scipy import stats as st

import analysis.make_probe_direction_atlas as atlas
from config import FIGURES_DIR, set_seeds


def describe(r):
    return {
        "n": int(len(r)),
        "mean": round(float(r.mean()), 4),
        "std": round(float(r.std()), 4),
        "cv": round(float(r.std() / r.mean()), 4),
        "skew": round(float(st.skew(r)), 3),
        "excess_kurtosis": round(float(st.kurtosis(r)), 3),
        "percentiles": {str(q): round(float(np.percentile(r, q)), 3)
                        for q in (0, 5, 25, 50, 75, 95, 100)},
    }


def main():
    set_seeds()
    from analysis.cache_prenorm_states import load_prenorm
    items = atlas.load_subset({"correct", "refusal", "wrong"})
    H_post = np.stack([r["h"] for r in items])
    labs = np.array([r["judge_label"] for r in items])
    items_pre, H_pre = load_prenorm({"correct", "refusal", "wrong"})
    labs_pre = np.array([r["judge_label"] for r in items_pre])

    def block(H, lab_arr):
        rms = np.linalg.norm(H, axis=1) / np.sqrt(H.shape[1])
        return {
            "rms_overall": describe(rms),
            "rms_by_label": {lab: describe(rms[lab_arr == lab])
                             for lab in ("correct", "refusal", "wrong")},
            "norm_mean": round(float(np.linalg.norm(H, axis=1).mean()), 2),
        }

    out = {
        "d": int(H_post.shape[1]),
        "final_normed_state_hf_index_28": block(H_post, labs),
        "prenorm_residual_post_block_27": block(H_pre, labs_pre),
    }
    out_path = FIGURES_DIR / "hidden_state_norms.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"overall": out["rms_overall"]["mean"],
                      "by_label": {k: v["mean"]
                                   for k, v in out["rms_by_label"].items()}}))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
