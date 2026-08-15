"""Judge-only pass for Qwen3-4B PopQA responses.

The popqa_evaluate.py pipeline loads subject + judge models simultaneously,
which thrashes on a 16GB M1 Pro when subject = Qwen3-4B (~8GB) + judge =
Qwen3-1.7B (~3.4GB). This script skips that: subject responses are already
on disk, so we only load Qwen3-1.7B as judge and grade them.

Skips items that already have judge_label set (resume support).
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ.setdefault("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.0")

JUDGE_MODEL_ID = "Qwen/Qwen3-1.7B"
RESPONSES_DIR = Path("data/popqa_sample/responses/qwen3_4b")

# Import judge.py
_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE.parent))  # repo root: judge.py, config.py
from judge import judge  # noqa: E402
from config import get_device  # noqa: E402


def main():
    device = get_device()
    print(f"Device: {device}")
    print(f"Loading judge model {JUDGE_MODEL_ID}...")
    tok = AutoTokenizer.from_pretrained(JUDGE_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(JUDGE_MODEL_ID, dtype=torch.bfloat16, device_map=device)
    model.eval()
    print("  loaded.")

    files = sorted(RESPONSES_DIR.glob("*.json"))
    print(f"Found {len(files)} responses")

    todo = []
    skipped = 0
    for f in files:
        r = json.load(open(f))
        if r.get("judge_label"):
            skipped += 1
            continue
        todo.append((f, r))
    print(f"  already judged: {skipped}; to judge: {len(todo)}")

    labels = Counter()
    t0 = time.perf_counter()
    for i, (f, r) in enumerate(todo, 1):
        q = r["question"]
        gold = r["expected_answer"]
        alts = r.get("acceptable_alternatives", [])
        j = judge(model, tok, device, q, gold, alts, r["answer_text"])
        r["judge_label"] = j["label"]
        r["judge_raw"] = j.get("raw", "")
        if j.get("parse_error"):
            r["judge_parse_error"] = True
        with open(f, "w") as fp:
            json.dump(r, fp, indent=2, ensure_ascii=False)
        labels[j["label"]] += 1
        if i % 25 == 0 or i == len(todo):
            elapsed = time.perf_counter() - t0
            rate = i / elapsed if elapsed > 0 else 0
            eta = (len(todo) - i) / rate / 60 if rate > 0 else 0
            print(f"  [{i}/{len(todo)}] labels: {dict(labels)}  rate={rate:.2f}/s  eta {eta:.1f}m")

    # Final tally over all files
    all_labels = Counter()
    for f in files:
        r = json.load(open(f))
        if r.get("judge_label"):
            all_labels[r["judge_label"]] += 1
    total = sum(all_labels.values())
    print(f"\n=== Judge summary ===")
    print(f"  judged: {total}/{len(files)}")
    for lbl in ("correct", "refusal", "wrong"):
        n = all_labels[lbl]
        print(f"    {lbl}: {n} ({n/max(total,1)*100:.1f}%)")


if __name__ == "__main__":
    main()
