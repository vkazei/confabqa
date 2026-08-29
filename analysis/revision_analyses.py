"""Revision analyses: pre-norm probe refit, DR-label sensitivity, SAE residual.

Three referee-requested checks, no generation needed:

A. Pre-norm probe refit. Fit the standard pipeline (StandardScaler ->
   PCA(16) -> LogReg) on the true post-block-27 residuals instead of the
   cached normed states; report CV accuracy in both representations,
   the cosine between the two recovered directions, cosines to the SAE
   2191 decoder and optimized directions, and held-out first-token flip
   curves for the native-space direction (bf16 final-norm+head).

B. DR-label sensitivity. Refit refusal_vs_wrong (layer 28) and correct
   (layer 18) probes and a TF-IDF question-text baseline on the same
   folds under the Qwen-judge labels and under the DR regrade labels;
   report accuracies and probe-minus-baseline margins for both.

C. SAE-residual probe. Probe h - Dec(Enc(h)) on the pre-norm states for
   refusal_vs_wrong and correct_vs_wrong; a coverage check that the
   dictionary's missing ~50% variance does not hide class signal.

Writes figures/qwen3_1_7b/revision_analyses.json.
Run from the repo root: python -m analysis.revision_analyses
"""
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import analysis.make_probe_direction_atlas as atlas
from analysis.cache_prenorm_states import load_prenorm
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, MODEL_ID, set_seeds

DR_PATH = Path("data/gemini_regrade/qwen3_1_7b_dr_labels.jsonl")
EVAL_BUDGETS = (50, 100, 200, 350, 500, 750, 1500)


def cv_acc(X, y, seed=0):
    pipe = make_pipeline(StandardScaler(), PCA(n_components=16),
                         LogisticRegression(max_iter=2000, C=1.0))
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    return float(cross_val_score(pipe, X, y, cv=cv).mean())


def tfidf_acc(texts, y, seed=0):
    pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2),
                         LogisticRegression(max_iter=2000, C=1.0))
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    return float(cross_val_score(pipe, texts, y, cv=cv).mean())


def main():
    set_seeds()
    out = {}

    # ---------- A. pre-norm probe refit ----------
    items_pn, H_pn = load_prenorm({"refusal", "wrong"})
    y_pn = np.array([1 if r["judge_label"] == "refusal" else 0
                     for r in items_pn])
    for r, h in zip(items_pn, H_pn):
        r["h"] = h
    d_pn = atlas.recover_direction(items_pn, "refusal")
    w_pn = d_pn["direction_raw"]
    w_pn_hat = w_pn / np.linalg.norm(w_pn)

    items_nm = atlas.load_subset({"refusal", "wrong"})
    H_nm = np.stack([r["h"] for r in items_nm])
    y_nm = np.array([1 if r["judge_label"] == "refusal" else 0
                     for r in items_nm])
    d_nm = atlas.recover_direction(items_nm, "refusal")
    w_nm_hat = d_nm["direction_raw"] / np.linalg.norm(d_nm["direction_raw"])

    w_wp = np.load(
        "figures/qwen3_1_7b/12_probe_direction_refusal_vs_wrong_within_post.npy")
    w_wp_hat = w_wp / np.linalg.norm(w_wp)

    from sae_lens import SAE
    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    u_2191 = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID]
    u_2191 = u_2191 / np.linalg.norm(u_2191)
    u_opt = np.load(FIGURES_DIR / "optimized_refusal_direction.npy")

    out["prenorm_refit"] = {
        "cv_acc_prenorm": round(cv_acc(H_pn, y_pn), 4),
        "cv_acc_normed": round(cv_acc(H_nm, y_nm), 4),
        "cos_prenorm_vs_normed_full": round(float(w_pn_hat @ w_nm_hat), 4),
        "cos_prenorm_vs_within_post": round(float(w_pn_hat @ w_wp_hat), 4),
        "cos_prenorm_vs_2191": round(float(w_pn_hat @ u_2191), 4),
        "cos_prenorm_vs_optimized": round(float(w_pn_hat @ u_opt), 4),
    }

    # held-out flip curves for the native direction (same split as Table 5)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32).to(torch.device("cpu"))
    model.eval()
    model.model.layers = torch.nn.ModuleList()
    norm, head = model.model.norm, model.lm_head.weight
    from saes.sae_causal_ablation import REFUSAL_OPENER_STRS
    op_ids = set()
    for s in REFUSAL_OPENER_STRS:
        for tid in tokenizer(s, add_special_tokens=False).input_ids:
            op_ids.add(int(tid))
    op_t = torch.tensor(sorted(op_ids))
    H_wrong = H_pn[y_pn == 0]
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(H_wrong))
    te = perm[len(perm) // 2:]
    Hte = torch.tensor(H_wrong[te], dtype=torch.float32)

    def flip(u, b):
        with torch.no_grad():
            hb = (Hte + b * torch.tensor(u, dtype=torch.float32)).to(torch.bfloat16)
            am = (norm(hb).float() @ head.T).argmax(-1)
            return round(float(torch.isin(am, op_t).float().mean()), 4)

    out["prenorm_refit"]["heldout_flips_prenorm_dir"] = {
        str(b): flip(w_pn_hat, b) for b in EVAL_BUDGETS}
    out["prenorm_refit"]["heldout_flips_within_post_dir"] = {
        str(b): flip(w_wp_hat, b) for b in EVAL_BUDGETS}
    del model

    # ---------- B. DR-label sensitivity ----------
    dr = {}
    for line in open(DR_PATH):
        r = json.loads(line)
        dr[r["id"]] = r["dr_label"]

    def probe_vs_baseline(judge_filter, target, layer, label_source):
        old_layer = atlas.PROBE_LAYER
        atlas.PROBE_LAYER = layer
        items = atlas.load_subset({"refusal", "wrong", "correct"})
        atlas.PROBE_LAYER = old_layer
        rows = []
        for r in items:
            lab = r["judge_label"] if label_source == "judge" else dr[r["question_id"]]
            if lab in judge_filter:
                rows.append((r["h"], r["question"], 1 if lab == target else 0))
        X = np.stack([h for h, _, _ in rows])
        texts = [q for _, q, _ in rows]
        y = np.array([t for _, _, t in rows])
        return {"n": int(len(y)), "n_pos": int(y.sum()),
                "probe_acc": round(cv_acc(X, y), 4),
                "tfidf_acc": round(tfidf_acc(texts, y), 4)}

    out["dr_sensitivity"] = {}
    for name, (filt, target, layer) in {
        "refusal_vs_wrong_L28": ({"refusal", "wrong"}, "refusal", 28),
        "correct_all_L18": ({"correct", "wrong", "refusal"}, "correct", 18),
    }.items():
        out["dr_sensitivity"][name] = {
            src: probe_vs_baseline(filt, target, layer, src)
            for src in ("judge", "dr")}

    # ---------- C. SAE-residual probe ----------
    items_all, H_all = load_prenorm({"refusal", "wrong", "correct"})
    labs = np.array([r["judge_label"] for r in items_all])
    with torch.no_grad():
        A = sae.encode(torch.from_numpy(H_all).float())
        R = sae.decode(A).numpy()
    resid = H_all - R
    m_rw = np.isin(labs, ["refusal", "wrong"])
    m_cw = np.isin(labs, ["correct", "wrong"])
    out["sae_residual_probe"] = {
        "refusal_vs_wrong": {
            "resid_acc": round(cv_acc(resid[m_rw], (labs[m_rw] == "refusal").astype(int)), 4),
            "full_acc": round(cv_acc(H_all[m_rw], (labs[m_rw] == "refusal").astype(int)), 4)},
        "correct_vs_wrong": {
            "resid_acc": round(cv_acc(resid[m_cw], (labs[m_cw] == "correct").astype(int)), 4),
            "full_acc": round(cv_acc(H_all[m_cw], (labs[m_cw] == "correct").astype(int)), 4)},
    }

    out_path = FIGURES_DIR / "revision_analyses.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
