import argparse
import json
import os
import time
from collections import Counter

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import MODEL_ID, RESPONSES_DIR, get_device, set_seeds
from judge import judge

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"


def iter_responses(ids=None, limit=None):
    paths = sorted(RESPONSES_DIR.glob("*.json"))
    if ids is not None:
        wanted = set(ids)
        paths = [p for p in paths if p.stem in wanted]
    if limit is not None:
        paths = paths[:limit]
    return paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Only re-grade first N responses")
    parser.add_argument("--ids", type=str, default=None,
                        help="Comma-separated question IDs to re-grade")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print decisions without overwriting response JSONs")
    parser.add_argument("--force", action="store_true",
                        help="Force re-grading of responses that already have judge_label")
    args = parser.parse_args()

    set_seeds()
    ids = [s.strip() for s in args.ids.split(",")] if args.ids else None
    paths = iter_responses(ids=ids, limit=args.limit)
    if not paths:
        print("No responses to re-grade.")
        return

    device = get_device()
    print(f"Device: {device}")
    JUDGE_MODEL_ID = "Qwen/Qwen3-1.7B"
    print(f"Loading judge model {JUDGE_MODEL_ID}...")
    t_load = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(JUDGE_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        JUDGE_MODEL_ID,
        dtype=torch.bfloat16,
        device_map=device,
    )
    model.eval()
    print(f"Judge model loaded in {time.perf_counter() - t_load:.1f}s")
    print(f"Re-grading {len(paths)} responses{' (dry run)' if args.dry_run else ''}\n")

    label_counts = Counter()
    flips = {"true_to_false": [], "false_to_true": [], "unchanged": 0}
    parse_errors = []

    for i, path in enumerate(paths, 1):
        with open(path) as f:
            r = json.load(f)

        if "judge_label" in r and not args.force:
            label = r["judge_label"]
            new_correct = r["correct"]
            old_correct = bool(r.get("correct", False))
            label_counts[label] += 1
            flips["unchanged"] += 1
            if r.get("judge_parse_error"):
                parse_errors.append(r["question_id"])
            if i % 100 == 0 or i == len(paths):
                print(f"[{i}/{len(paths)}] {r['question_id']:14s} (skipped - already graded)")
            continue

        result = judge(
            model, tokenizer, device,
            question=r["question"],
            expected=r["expected_answer"],
            alternatives=r.get("acceptable_alternatives", []),
            answer_text=r["answer_text"],
            max_new_tokens=16,
        )
        label = result["label"]
        label_counts[label] += 1
        new_correct = (label == "correct")
        old_correct = bool(r.get("correct", False))
        if new_correct != old_correct:
            if old_correct and not new_correct:
                flips["true_to_false"].append(r["question_id"])
            else:
                flips["false_to_true"].append(r["question_id"])
        else:
            flips["unchanged"] += 1
        if result.get("parse_error"):
            parse_errors.append(r["question_id"])

        flip_mark = " " if new_correct == old_correct else "*"
        print(f"[{i}/{len(paths)}] {r['question_id']:14s} "
              f"old={'T' if old_correct else 'F'} new={label:7s} {flip_mark} "
              f"| {r['answer_text'][:70].replace(chr(10), ' ')}")

        if not args.dry_run:
            r["judge_label"] = label
            r["judge_raw"] = result["raw"]
            if "parse_error" in result:
                r["judge_parse_error"] = True
            elif "judge_parse_error" in r:
                del r["judge_parse_error"]
            r["correct"] = new_correct
            with open(path, "w") as f:
                json.dump(r, f, indent=2, ensure_ascii=False)

    print("\n=== Summary ===")
    print(f"Labels: " + ", ".join(f"{k}={v}" for k, v in sorted(label_counts.items())))
    print(f"Unchanged correctness: {flips['unchanged']}")
    print(f"Flipped True -> False: {len(flips['true_to_false'])} "
          f"{flips['true_to_false'] if flips['true_to_false'] else ''}")
    print(f"Flipped False -> True: {len(flips['false_to_true'])} "
          f"{flips['false_to_true'] if flips['false_to_true'] else ''}")
    if parse_errors:
        print(f"Parse errors ({len(parse_errors)}): {parse_errors}")


if __name__ == "__main__":
    main()
