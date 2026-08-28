"""The optimized refusal direction: recovery by direct optimization.

Third recovery method beside the probe (discriminative) and the class-
mean difference: treat the intervention vector itself as the only
trainable parameter and maximize first-token refusal-opener probability
on true pre-norm states (post-block-27 residuals, the Section 6.2
intervention point). The first-token distribution is differentiable
through just the final RMSNorm and LM head, so the optimization runs
on the cached pre-norm states with no full-model backprop.

Objective: v on the sphere ||v|| = BUDGET, maximizing mean
log P(opener set) of softmax(LMHead(RMSNorm(h + v))) over a train half
of the 402 wrong states; all evaluations on the held-out half, with
first-token argmax computed in bfloat16 to match the paper's runtime.

Writes figures/qwen3_1_7b/optimized_refusal_direction.json.
Run from the repo root: python -m analysis.optimize_refusal_direction
"""
import json

import numpy as np
import torch
from sae_lens import SAE
from transformers import AutoModelForCausalLM, AutoTokenizer

import analysis.make_probe_direction_atlas as atlas
from analysis.cache_prenorm_states import load_prenorm
from confabqa.constants import SAE_RELEASE, SAE_LAYER, SAE_FEATURE_ID
from config import FIGURES_DIR, MODEL_ID, get_device, set_seeds
from saes.sae_causal_ablation import REFUSAL_OPENER_STRS

BUDGET = 200.0
STEPS = 200
LR = 0.03
EVAL_BUDGETS = (50, 100, 200, 350, 500, 750, 1500)


def main():
    set_seeds()
    items, H = load_prenorm({"refusal", "wrong"})
    labs = np.array([r["judge_label"] for r in items])
    H_wrong = H[labs == "wrong"]
    rng = np.random.default_rng(0)
    perm = rng.permutation(len(H_wrong))
    tr, te = perm[: len(perm) // 2], perm[len(perm) // 2:]

    d = atlas.recover_direction(atlas.load_subset({"refusal", "wrong"}),
                                "refusal")
    u_full = d["direction_raw"] / np.linalg.norm(d["direction_raw"])
    u_wp = np.load(
        "figures/qwen3_1_7b/12_probe_direction_refusal_vs_wrong_within_post.npy")
    u_wp = u_wp / np.linalg.norm(u_wp)
    dm = H[labs == "refusal"].mean(0) - H_wrong.mean(0)
    u_dm = dm / np.linalg.norm(dm)
    sae = SAE.from_pretrained(release=SAE_RELEASE,
                              sae_id=f"layer{SAE_LAYER}", device="cpu")
    u_2191 = sae.W_dec.detach().cpu().numpy()[SAE_FEATURE_ID]
    u_2191 = u_2191 / np.linalg.norm(u_2191)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    # CPU: the workload is only RMSNorm + LM-head matmuls, and sustained
    # backprop through the 152k-vocab head triggers MPS command-buffer
    # failures (GPU error recovery) on this hardware.
    device = torch.device("cpu")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float32).to(device)
    model.eval()
    # only the final RMSNorm and the (tied) LM head are used past this
    # point, here and in logit_lens_top_tokens; free the blocks
    model.model.layers = torch.nn.ModuleList()
    import gc
    gc.collect()
    norm, head = model.model.norm, model.lm_head.weight

    opener_ids = set()
    for s in REFUSAL_OPENER_STRS:
        for tid in tokenizer(s, add_special_tokens=False).input_ids:
            opener_ids.add(int(tid))
    op_t = torch.tensor(sorted(opener_ids), device=device)

    Htr = torch.tensor(H_wrong[tr], dtype=torch.float32, device=device)
    Hte = torch.tensor(H_wrong[te], dtype=torch.float32, device=device)

    torch.manual_seed(0)
    raw = torch.randn(2048, device=device)
    raw = (raw / raw.norm()).clone().requires_grad_(True)
    opt = torch.optim.Adam([raw], lr=LR)
    for step in range(STEPS):
        u = raw / raw.norm()  # normalize inside the graph: optimize on the sphere
        z = norm(Htr + BUDGET * u)
        lg = z @ head.T
        loss = -(torch.logsumexp(lg[:, op_t], -1)
                 - torch.logsumexp(lg, -1)).mean()
        opt.zero_grad(); loss.backward(); opt.step()
        if step % 50 == 0:
            with torch.no_grad():
                fl = float(torch.isin(lg.argmax(-1), op_t).float().mean())
            print(f"step {step:3d} train -logP(opener) {loss.item():.4f} "
                  f"train flip {fl:.0%}", flush=True)
    with torch.no_grad():
        u_star = (raw / raw.norm()).cpu().numpy()
    assert np.isfinite(u_star).all()

    def flip(u, b):
        with torch.no_grad():
            hb = (Hte + b * torch.tensor(u, dtype=torch.float32,
                                         device=device)).to(torch.bfloat16)
            am = (norm(hb).float() @ head.T).argmax(-1)
            return round(float(torch.isin(am, op_t).float().mean()), 4)

    dirs = {"optimized": u_star, "probe_full": u_full,
            "probe_within_post": u_wp, "sae_2191": u_2191,
            "diff_means_prenorm": u_dm}
    flips = {n: {str(b): flip(u, b) for b in EVAL_BUDGETS}
             for n, u in dirs.items()}

    from saes.sae_decompose_refusal import logit_lens_top_tokens
    top, bot = logit_lens_top_tokens(u_star.astype(np.float32),
                                     model, tokenizer)
    out = {
        "geometry": "pre-norm post-block-27 residual",
        "budget": BUDGET, "steps": STEPS,
        "n_train": int(len(tr)), "n_test": int(len(te)),
        "cosines": {
            "optimized_vs_probe_full": round(float(u_star @ u_full), 4),
            "optimized_vs_probe_within_post": round(float(u_star @ u_wp), 4),
            "optimized_vs_2191": round(float(u_star @ u_2191), 4),
            "optimized_vs_diff_means": round(float(u_star @ u_dm), 4),
            "probe_full_vs_within_post": round(float(u_full @ u_wp), 4),
            "probe_within_post_vs_2191": round(float(u_wp @ u_2191), 4),
        },
        "heldout_flip_rates": flips,
        "optimized_lens_top": [[t, round(s, 2)] for _, t, s in top[:15]],
        "optimized_lens_bottom": [[t, round(s, 2)] for _, t, s in bot[:8]],
    }
    out_path = FIGURES_DIR / "optimized_refusal_direction.json"
    with open(out_path, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({"cosines": out["cosines"]}, indent=1))
    print("flip curves (held-out 201 wrong states):")
    print("budget:     " + "  ".join(f"{b:>5d}" for b in EVAL_BUDGETS))
    for n in dirs:
        print(f"{n:20s} " + "  ".join(
            f"{flips[n][str(b)]:5.0%}" for b in EVAL_BUDGETS))
    print("lens top:", [t for t, _ in out["optimized_lens_top"][:8]])
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
