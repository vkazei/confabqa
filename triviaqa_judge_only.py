"""Generalized judge-only pass for any subject model's TriviaQA responses.

Loads only the Qwen3-1.7B judge (subject model already ran separately,
responses written to disk). Avoids the OOM trap of co-loading large subject +
judge models on a 16GB unified-memory M1 Pro.

Usage:
  venv/bin/python triviaqa_judge_only.py --subdir qwen3_8b
  venv/bin/python triviaqa_judge_only.py --subdir qwen3_8b --sample-suffix _seed1

Skips items that already have judge_label set.
"""
from __future__ import annotations

import argparse
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

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))
from judge import judge  # noqa: E402
from config import get_device  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdir", required=True, help="Subject-model subdir under data/triviaqa_sample*/responses/")
    parser.add_argument("--sample-suffix", default="", help='e.g. "_seed1"')
    args = parser.parse_args()

    resp_dir = Path(f"data/triviaqa_sample{args.sample_suffix}/responses/{args.subdir}")
    if not resp_dir.exists():
        sys.exit(f"Responses dir not found: {resp_dir}")

    device = get_device()
    print(f"Device: {device}")
    print(f"Responses: {resp_dir}")
    print(f"Loading judge model {JUDGE_MODEL_ID}...")
    tok = AutoTokenizer.from_pretrained(JUDGE_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        JUDGE_MODEL_ID, dtype=torch.bfloat16, device_map=device)
    model.eval()
    print("  loaded.")

    files = sorted(resp_dir.glob("*.json"))
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

    # Final tally
    all_labels = Counter()
    for f in files:
        r = json.load(open(f))
        if r.get("judge_label"):
            all_labels[r["judge_label"]] += 1
    total = sum(all_labels.values())
    print(f"\n=== Judge summary ({resp_dir.name}) ===")
    print(f"  judged: {total}/{len(files)}")
    for lbl in ("correct", "refusal", "wrong"):
        n = all_labels[lbl]
        print(f"    {lbl}: {n} ({n/max(total,1)*100:.1f}%)")


if __name__ == "__main__":
    main()
