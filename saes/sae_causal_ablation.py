"""Causal test: is SAE feature 2191 sufficient to induce refusal-opener generation?

Hypothesis: Feature 2191's decoder direction is the canonical refusal-opener
direction in Qwen3-1.7B residual stream at layer 28 (after block 27). If we
add alpha * W_dec[2191] to a wrong item's last-prompt-token hidden state,
P(first generated token in {refusal openers}) should rise monotonically
with alpha until saturation.

Protocol mirrors Section 6.7's probe-direction intervention but substitutes
the SAE feature's decoder vector for the recovered probe direction:

  h'[last_prompt_token] = h[last_prompt_token] + alpha * W_dec[2191] / ||W_dec[2191]||

The hook fires on model.model.norm's forward pre-call (input is the
post-block-27 residual stream).

For each (item, alpha) we compute the next-token distribution and report:
  - P(any token in REFUSAL_OPENERS) — primary metric
  - argmax token + its probability
  - P(refusal openers) - P(refusal openers at alpha=0) — gain over baseline

Outputs:
  figures/sae_causal_ablation.json
  figures/sae_causal_ablation.md
  figures/sae_causal_ablation.png  (dose-response curve)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

from confabqa.constants import (SAE_RELEASE, SAE_LAYER,
                                SAE_HF_LAYER as HF_LAYER)
SAE_ID = f"layer{SAE_LAYER}"
MODEL_ID = "Qwen/Qwen3-1.7B"
RESPONSES_DIR = Path("data/responses/qwen3_1_7b")
ACTIVATIONS_DIR = Path("data/activations/qwen3_1_7b")

from confabqa.constants import SAE_FEATURE_ID as FEATURE_ID
N_ITEMS = 30
# Alphas matched to Section 6.7 effective magnitude.
# Section 6.7 used alpha in +/-[2000] with recovered probe direction
# (||direction||=0.374), giving effective magnitude ~748. Decoder vectors are
# unit-normalized, so a comparable scan is alpha in [0, 1000].
ALPHAS = [0.0, 16.0, 64.0, 200.0, 400.0, 750.0, 1500.0, 3000.0]

# Tokens we count as refusal openers; based on §6.6 logit lens and feature 2191's top tokens
REFUSAL_OPENER_STRS = [" as", " As", "As", "as", " there", "作为", "作为一个", "作為", "\tas", "-as"]


def load_items(judge_label, n):
    """Load n items with the given judge label, with their hidden states at HF_LAYER."""
    out = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        r = json.load(open(f))
        if r.get("judge_label") != judge_label:
            continue
        out.append(r)
        if len(out) >= n:
            break
    return out


def run_intervention(model, tokenizer, sae, items, alpha):
    """Forward each item with alpha * W_dec[FEATURE_ID] added to last prompt token
    at the layer-28 residual stream. Return list of (qid, refusal_opener_prob, argmax_token, argmax_prob).
    """
    W_dec = sae.W_dec[FEATURE_ID].detach().cpu().to(model.dtype)
    W_dec_unit = W_dec / W_dec.norm()

    # Look up refusal-opener token ids
    opener_ids = set()
    for s in REFUSAL_OPENER_STRS:
        for tid in tokenizer(s, add_special_tokens=False).input_ids:
            opener_ids.add(int(tid))
    opener_ids = sorted(opener_ids)

    results = []
    device = next(model.parameters()).device
    handle = None
    # Pre-hook on final norm: modifies its INPUT (post-block-27 residual)
    def pre_hook(module, inputs):
        # inputs is a tuple; first element is hidden_states (B, T, d)
        h = inputs[0]
        h_mod = h.clone()
        # Add alpha * unit direction to last token only
        h_mod[:, -1, :] = h_mod[:, -1, :] + alpha * W_dec_unit.to(h.device)
        return (h_mod,) + tuple(inputs[1:])

    try:
        handle = model.model.norm.register_forward_pre_hook(pre_hook)
        for r in items:
            qid = r["question_id"]
            q = r["question"]
            # Apply Qwen3 chat template (matching 02_evaluate.py)
            messages = [{"role": "user", "content": q}]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                                                    add_generation_prompt=True,
                                                    enable_thinking=False)
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            with torch.no_grad():
                out = model(**inputs, output_hidden_states=False)
            logits = out.logits[0, -1, :].float().cpu().numpy()
            probs = np.exp(logits - logits.max())
            probs /= probs.sum()
            opener_prob = float(probs[opener_ids].sum())
            argmax_id = int(np.argmax(probs))
            argmax_str = tokenizer.decode([argmax_id])
            argmax_prob = float(probs[argmax_id])
            results.append({
                "qid": qid, "judge_label_orig": r["judge_label"],
                "opener_prob": opener_prob,
                "argmax_token_id": argmax_id, "argmax_token_str": argmax_str,
                "argmax_prob": argmax_prob,
            })
    finally:
        if handle is not None:
            handle.remove()
    return results, opener_ids


def main():
    print(f"Loading SAE {SAE_RELEASE} / {SAE_ID}...")
    sae = SAE.from_pretrained(release=SAE_RELEASE, sae_id=SAE_ID, device="cpu")

    print(f"Loading Qwen3-1.7B model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.bfloat16, device_map="cpu")
    model.eval()

    print(f"Loading items: {N_ITEMS} wrong + {N_ITEMS} refusal...")
    wrong_items = load_items("wrong", N_ITEMS)
    refusal_items = load_items("refusal", N_ITEMS)
    print(f"  wrong: {len(wrong_items)}; refusal: {len(refusal_items)}")

    all_results = {"wrong": {}, "refusal": {}}
    opener_ids = None
    for subset, items in [("wrong", wrong_items), ("refusal", refusal_items)]:
        print(f"\n=== {subset} subset (n={len(items)}) ===")
        for alpha in ALPHAS:
            print(f"  alpha={alpha:>6.1f} ...", end="", flush=True)
            results, opener_ids = run_intervention(model, tokenizer, sae, items, alpha)
            ops = [r["opener_prob"] for r in results]
            mean_p = float(np.mean(ops))
            argmax_in_opener = sum(1 for r in results if r["argmax_token_id"] in opener_ids)
            print(f"  P(opener)={mean_p:.3f}, argmax-in-opener={argmax_in_opener}/{len(results)}")
            all_results[subset][alpha] = {
                "items": results,
                "mean_opener_prob": mean_p,
                "argmax_in_opener_count": argmax_in_opener,
            }

    output = {
        "metadata": {
            "model": MODEL_ID, "sae_release": SAE_RELEASE, "sae_id": SAE_ID,
            "feature_id": FEATURE_ID, "alphas": ALPHAS,
            "n_items_per_subset": N_ITEMS,
            "opener_token_ids": opener_ids,
            "opener_token_strs": REFUSAL_OPENER_STRS,
        },
        "results": all_results,
    }
    out_json = Path("figures/sae_causal_ablation.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w") as fp:
        json.dump(output, fp, indent=2, ensure_ascii=False)
    print(f"\nWrote {out_json}")

    # Dose-response figure
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=140)
    for subset, color, marker in [("wrong", "#1f77b4", "o"), ("refusal", "#d62728", "s")]:
        ys = [all_results[subset][a]["mean_opener_prob"] for a in ALPHAS]
        ax.plot(ALPHAS, ys, marker=marker, color=color, label=f"{subset} items (n={N_ITEMS})", lw=2)
    ax.set_xscale("symlog", linthresh=1.0)
    ax.set_xlabel(r"$\alpha$  (units of $\hat W_{\rm dec}[2191]$ added to last-prompt-token h)", fontsize=10)
    ax.set_ylabel(r"$P($next token $\in$ refusal openers$)$", fontsize=10)
    ax.set_title(f"Causal intervention via SAE feature 2191\n"
                 f"Adding $\\alpha \\cdot \\hat W_{{dec}}[2191]$ at HF layer {HF_LAYER} "
                 f"induces refusal-opener generation", fontsize=11)
    ax.grid(alpha=0.3); ax.legend(loc="upper left")
    plt.tight_layout()
    out_png = Path("figures/sae_causal_ablation.png")
    plt.savefig(out_png, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out_png}")

    # Markdown summary
    md = []
    md.append("# Causal intervention via SAE feature 2191\n\n")
    md.append(f"**Hypothesis:** Feature 2191's decoder direction is the canonical refusal-opener\n")
    md.append(f"direction in Qwen3-1.7B at HF layer {HF_LAYER}. Adding $\\alpha \\cdot \\hat W_{{dec}}[2191]$ to\n")
    md.append(f"the last-prompt-token hidden state should induce refusal-opener generation.\n\n")
    md.append(f"**Items:** {N_ITEMS} wrong + {N_ITEMS} refusal (baseline from v1.3, judge_label-labeled).\n")
    md.append(f"**Opener token set:** {', '.join(repr(s) for s in REFUSAL_OPENER_STRS)} (decoded to {len(opener_ids)} unique token IDs).\n\n")
    md.append("## Dose-response\n\n")
    md.append("| alpha | wrong P(opener) | wrong argmax-in-opener | refusal P(opener) | refusal argmax-in-opener |\n")
    md.append("|--:|--:|--:|--:|--:|\n")
    for a in ALPHAS:
        ws = all_results["wrong"][a]
        rs = all_results["refusal"][a]
        md.append(f"| {a:.1f} | {ws['mean_opener_prob']:.3f} | "
                  f"{ws['argmax_in_opener_count']}/{N_ITEMS} | "
                  f"{rs['mean_opener_prob']:.3f} | "
                  f"{rs['argmax_in_opener_count']}/{N_ITEMS} |\n")
    md.append("\n![dose-response](sae_causal_ablation.png)\n")

    out_md = Path("figures/sae_causal_ablation.md")
    out_md.write_text("".join(md))
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
