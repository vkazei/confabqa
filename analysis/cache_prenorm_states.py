"""Cache the true pre-norm layer-28 residual states.

HF's output_hidden_states stores the *post-final-norm* state as its
last entry, so the cached activations' index 28 is the normed state,
not the post-block-27 residual that the Section 6.2/6.3.1 intervention
hooks (and Qwen-Scope's training) operate on. This script recomputes
one prefill per ConfabQA item with a forward hook on block 27 and
saves the last-prompt-token PRE-norm state.

Output: data/activations/qwen3_1_7b_prenorm/{id}.npy (float32, 2048).
Resumable; gitignored like the other activation caches.
Run from the repo root: python -m analysis.cache_prenorm_states
"""
import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import MODEL_ID, RESPONSES_DIR, get_device, set_seeds

OUT_DIR = Path("data/activations/qwen3_1_7b_prenorm")


def main():
    set_seeds()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        r = json.loads(f.read_text())
        if not (OUT_DIR / f"{r['question_id']}.npy").exists():
            items.append((r["question_id"], r["question"]))
    print(f"to cache: {len(items)}")
    if not items:
        return

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    device = get_device()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16).to(device)
    model.eval()

    grabbed = {}

    def hook(module, inputs, output):
        h = output[0] if isinstance(output, tuple) else output
        grabbed["h"] = h[0, -1].float().cpu().numpy()

    handle = model.model.layers[27].register_forward_hook(hook)
    for n, (qid, question) in enumerate(items, 1):
        text = tokenizer.apply_chat_template(
            [{"role": "user", "content": question}], tokenize=False,
            add_generation_prompt=True, enable_thinking=False)
        ids = tokenizer(text, return_tensors="pt").to(device)
        with torch.no_grad():
            model.model(**ids)
        np.save(OUT_DIR / f"{qid}.npy", grabbed["h"])
        if n % 100 == 0:
            print(f"{n}/{len(items)}", flush=True)
    handle.remove()
    print("done")


if __name__ == "__main__":
    main()


def load_prenorm(judge_filter=None):
    """Load cached pre-norm states as (items, H) aligned lists.

    items are the response dicts (with judge_label, question, ...);
    H is (n, 2048) float32 of post-block-27 residuals.
    """
    items, H = [], []
    for f in sorted(RESPONSES_DIR.glob("*.json")):
        r = json.loads(f.read_text())
        if judge_filter and r["judge_label"] not in judge_filter:
            continue
        p = OUT_DIR / f"{r['question_id']}.npy"
        if not p.exists():
            raise FileNotFoundError(
                f"{p} missing; run python -m analysis.cache_prenorm_states")
        items.append(r)
        H.append(np.load(p))
    return items, np.stack(H)
