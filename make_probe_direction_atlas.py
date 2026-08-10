"""Recover the layer-28 refusal-vs-wrong probe direction in original 2048-d
hidden-state space, project it through the LM head (logit-lens style), and
report the top/bottom tokens along it.

This is the literal "atlas": a single direction in token space corresponding
to the model's refusal-vs-confabulation distinction at its deepest layer.

Pipeline:
  1. Load all 549 refusal+wrong items, stack their layer-28 hidden states.
  2. Fit the same StandardScaler -> PCA(16) -> LogReg pipeline as the
     headline probe (on the full subset, no CV; we want the direction, not
     a fold-mean accuracy).
  3. Recover the direction in raw 2048-d space:
        w_pca = LR.coef_[0]              (16,)
        w_std = V.T @ w_pca              (2048,)  via PCA inverse
        w_raw = w_std / scaler.scale_    (2048,)  undo the per-feature std
     Sign convention: refusal end is positive.
  4. Project through the LM head:
        logits = (Norm(w_raw) @ W_U.T)    (V,)
     Following the logit-lens convention, approximate the final RMSNorm by
     L2-normalizing the direction; this preserves token-direction angles.
  5. Report top-K and bottom-K tokens along this direction.

Also produces a sanity-check second analysis on the
refusal_vs_wrong_within_post subset (n=393, where the cutoff covariate is
held out by construction), and writes a figure showing the histogram of
projected scores per judge label.
"""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import (ACTIVATIONS_DIR, FIGURES_DIR, MODEL_ID, RESPONSES_DIR,
                    SUMMARY_PATH, get_device, set_seeds)

# Load refusal_vs_wrong peak layer from summary if it exists, else default to 28
PROBE_LAYER = 28
if SUMMARY_PATH.exists():
    try:
        with open(SUMMARY_PATH) as f:
            _summary = json.load(f)
        PROBE_LAYER = _summary["probes"]["refusal_vs_wrong"]["peak_layer"]
    except Exception:
        pass

PCA_N = 16
TOP_K = 30


def load_subset(judge_filter, cutoff_filter=None):
    items = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        with open(f) as fp:
            r = json.load(fp)
        if r.get("judge_label") not in judge_filter:
            continue
        if cutoff_filter is not None and r["cutoff_class"] != cutoff_filter:
            continue
        act = torch.load(ACTIVATIONS_DIR / f"{r['question_id']}.pt", weights_only=False)
        r["h"] = act["last_prompt_hidden"][PROBE_LAYER].numpy()
        items.append(r)
    return items


def recover_direction(items, target_label):
    """Returns (direction_raw_2048, signed_scores_per_item, pca_obj, scaler_obj, lr_obj)."""
    X = np.stack([r["h"] for r in items])  # (n, 2048)
    y = np.array([1 if r["judge_label"] == target_label else 0 for r in items])

    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    pca = PCA(n_components=PCA_N).fit(Xs)
    Xp = pca.transform(Xs)  # (n, 16)
    lr = LogisticRegression(max_iter=2000, C=1.0).fit(Xp, y)

    w_pca = lr.coef_[0]                       # (16,)
    w_std = pca.components_.T @ w_pca         # (2048,) direction in standardized space
    # Convert back to raw hidden-state space: a unit change along this direction
    # in raw space corresponds to w_std / scaler.scale_ in standardized space.
    # The direction in raw space that increases the standardized projection by
    # one unit per raw-unit is w_std / scaler.scale_ (componentwise).
    w_raw = w_std / scaler.scale_

    # Signed scores per item (in standardized PCA space; same as Xp @ w_pca / |w_pca|).
    scores = Xp @ w_pca
    # Sign convention: positive = refusal pole
    if scores[y == 1].mean() < scores[y == 0].mean():
        w_pca = -w_pca; w_std = -w_std; w_raw = -w_raw; scores = -scores

    return {
        "direction_raw": w_raw,
        "direction_std": w_std,
        "direction_pca": w_pca,
        "scores": scores,
        "labels": y,
        "scaler": scaler,
        "pca": pca,
        "lr": lr,
    }


def project_through_lm_head(direction_raw, model, tokenizer, top_k=TOP_K):
    """Apply the final RMSNorm + LM head to `direction_raw` and return top/bottom tokens.

    Following the logit-lens convention, we treat the direction as a hidden
    state and pass it through the model's final RMSNorm and tied LM head.
    """
    with torch.no_grad():
        # We need: final norm and lm_head.
        device = next(model.parameters()).device
        h = torch.tensor(direction_raw, dtype=model.dtype, device=device).unsqueeze(0)  # (1, d)
        # Qwen3 has model.model.norm (RMSNorm) then model.lm_head.
        h_norm = model.model.norm(h)
        logits = model.lm_head(h_norm).squeeze(0).cpu().float().numpy()  # (V,)

    top_idx = np.argsort(-logits)[:top_k]
    bot_idx = np.argsort(logits)[:top_k]
    top_tokens = [(tokenizer.decode([int(i)]), float(logits[i])) for i in top_idx]
    bot_tokens = [(tokenizer.decode([int(i)]), float(logits[i])) for i in bot_idx]
    return top_tokens, bot_tokens, logits


def plot_score_histogram(scores, labels, label_names, out_path, title):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bins = np.linspace(scores.min() - 0.1, scores.max() + 0.1, 35)
    for lbl_val, lbl_name, color in zip([0, 1], label_names, ["#d62728", "#1f77b4"]):
        mask = labels == lbl_val
        ax.hist(scores[mask], bins=bins, alpha=0.7, color=color,
                label=f"{lbl_name} (n={mask.sum()})", edgecolor="white", linewidth=0.4)
    ax.set_xlabel(f"signed projection onto layer-{PROBE_LAYER} probe direction "
                  "(positive = refusal pole)")
    ax.set_ylabel("count")
    ax.set_title(title)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def main():
    set_seeds()
    FIGURES_DIR.mkdir(exist_ok=True)
    print(f"Loading model {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    device = get_device()
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float32).to(device)
    model.eval()
    print(f"  loaded; device={device}")

    out_md = []
    out_md.append("# Probe-direction atlas: layer-28 refusal-vs-wrong\n")
    out_md.append("Generated by `make_probe_direction_atlas.py`. ")
    out_md.append(f"Probe direction recovered from the layer-{PROBE_LAYER} hidden state, ")
    out_md.append("projected through the model's final RMSNorm and (tied) LM head ")
    out_md.append("to a vocabulary score vector. Top tokens score highest along the ")
    out_md.append("refusal pole of the probe; bottom tokens score highest along the ")
    out_md.append("opposite (wrong-confabulation) pole.\n\n")

    summary_payload = {}

    for tag, judge_filter, cutoff_filter, target_label, title in [
        ("refusal_vs_wrong_full",
         {"refusal", "wrong"}, None, "refusal",
         f"Layer-{PROBE_LAYER} refusal-vs-wrong probe (full subset, n=549)"),
        ("refusal_vs_wrong_within_post",
         {"refusal", "wrong"}, "post", "refusal",
         f"Layer-{PROBE_LAYER} refusal-vs-wrong probe (post-cutoff only, n=393)"),
    ]:
        items = load_subset(judge_filter, cutoff_filter)
        n_pos = sum(1 for r in items if r["judge_label"] == target_label)
        n_neg = len(items) - n_pos
        print(f"\n=== {tag} ===  n={len(items)} ({n_pos} refusal, {n_neg} wrong)")
        d = recover_direction(items, target_label)

        top, bot, _ = project_through_lm_head(d["direction_raw"], model, tokenizer)

        out_md.append(f"## {tag}\n\n")
        out_md.append(f"- subset: n={len(items)} ({n_pos} {target_label}, {n_neg} wrong)\n")
        out_md.append(f"- training direction: PCA({PCA_N}) -> LogReg on standardized layer-{PROBE_LAYER} hidden state\n")
        out_md.append(f"- sign convention: positive = {target_label} pole\n\n")
        out_md.append(f"### Top {TOP_K} tokens (refusal pole)\n\n")
        out_md.append("| rank | token | logit |\n|--:|---|--:|\n")
        for i, (tok, lg) in enumerate(top, start=1):
            esc = repr(tok)
            out_md.append(f"| {i} | {esc} | {lg:+.3f} |\n")
        out_md.append(f"\n### Bottom {TOP_K} tokens (wrong / confabulation pole)\n\n")
        out_md.append("| rank | token | logit |\n|--:|---|--:|\n")
        for i, (tok, lg) in enumerate(bot, start=1):
            esc = repr(tok)
            out_md.append(f"| {i} | {esc} | {lg:+.3f} |\n")
        out_md.append("\n")

        # score histogram
        fig_path = FIGURES_DIR / f"12_probe_score_hist_{tag}.png"
        plot_score_histogram(d["scores"], d["labels"],
                              label_names=[f"wrong (n={n_neg})", f"{target_label} (n={n_pos})"],
                              out_path=fig_path, title=title)
        print(f"  wrote {fig_path}")

        # save direction
        np.save(FIGURES_DIR / f"12_probe_direction_{tag}.npy", d["direction_raw"])
        summary_payload[tag] = {
            "n": len(items), "n_refusal": n_pos, "n_wrong": n_neg,
            "top_tokens": [(t, float(l)) for t, l in top],
            "bottom_tokens": [(t, float(l)) for t, l in bot],
            "direction_norm_raw": float(np.linalg.norm(d["direction_raw"])),
            "direction_norm_std": float(np.linalg.norm(d["direction_std"])),
        }

    out_md_path = FIGURES_DIR / "12_probe_direction_atlas.md"
    with open(out_md_path, "w") as fp:
        fp.write("".join(out_md))
    print(f"\nWrote {out_md_path}")

    out_json_path = FIGURES_DIR / "12_probe_direction_atlas.json"
    with open(out_json_path, "w") as fp:
        json.dump(summary_payload, fp, indent=2)
    print(f"Wrote {out_json_path}")


if __name__ == "__main__":
    main()
