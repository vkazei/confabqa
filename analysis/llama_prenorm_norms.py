"""Measure Llama-3.2-3B pre-norm state norms at its intervention hook.

The cross-model scale table quoted the cached final-normed-state norm
for Llama (90, sigma 0.3); the intervention hooks layers[27], whose
output is the post-block-27 residual. This script measures that
residual's last-prompt-token norm over all 784 ConfabQA questions with
Llama's own chat template.

Uses a seeded 150-question sample (SE of the mean well under 1%);
appends incrementally to a jsonl so interrupted runs resume.

Writes figures/llama_3_2_3b/prenorm_norms.json.
Run from the repo root: python -m analysis.llama_prenorm_norms
"""
import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import RESPONSES_DIR, get_device, set_seeds

MODEL_ID_LLAMA = "unsloth/Llama-3.2-3B-Instruct"
HOOK_LAYER = 27
OUT = Path("figures/llama_3_2_3b/prenorm_norms.json")
PARTIAL = Path("figures/llama_3_2_3b/prenorm_norms_partial.jsonl")
N_SAMPLE = 150


def main():
    set_seeds()
    device = get_device()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID_LLAMA)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID_LLAMA, dtype=torch.bfloat16, device_map=device)
    model.eval()

    grabbed = {}

    def hook(module, inputs, output):
        h = output[0] if isinstance(output, tuple) else output
        grabbed["n"] = float(h[0, -1].float().norm())

    handle = model.model.layers[HOOK_LAYER].register_forward_hook(hook)
    files = sorted(RESPONSES_DIR.glob("*.json"))
    rng = np.random.default_rng(0)
    files = [files[i] for i in rng.permutation(len(files))[:N_SAMPLE]]
    done = {}
    if PARTIAL.exists():
        for line in PARTIAL.read_text().splitlines():
            r = json.loads(line)
            done[r["id"]] = r["norm"]
    norms = list(done.values())
    for i, f in enumerate(files, 1):
        if f.stem in done:
            continue
        q = json.loads(f.read_text())["question"]
        text = tokenizer.apply_chat_template(
            [{"role": "user", "content": q}], tokenize=False,
            add_generation_prompt=True)
        ids = tokenizer(text, return_tensors="pt").to(device)
        with torch.no_grad():
            model.model(**ids)
        norms.append(grabbed["n"])
        with open(PARTIAL, "a") as fp:
            fp.write(json.dumps({"id": f.stem, "norm": grabbed["n"]}) + "\n")
        if i % 25 == 0:
            print(f"{i}/{len(files)}", flush=True)
    handle.remove()

    ns = np.array(norms)
    out = {"model": MODEL_ID_LLAMA, "hook": f"layers[{HOOK_LAYER}] output",
           "n": len(ns), "norm_mean": round(float(ns.mean()), 1),
           "norm_std": round(float(ns.std()), 1),
           "p5": round(float(np.percentile(ns, 5)), 1),
           "p95": round(float(np.percentile(ns, 95)), 1)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps(out))


if __name__ == "__main__":
    main()
