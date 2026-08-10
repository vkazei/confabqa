"""Phase 2 steps 3-4: generate + grade the PopQA sample with Qwen3-1.7B
(or whichever MODEL_ID is set), reusing the existing pipeline functions
verbatim.

This script does NOT modify 02_evaluate.py, 03_analyze.py, judge.py, or any
existing data. It imports `evaluate_question` and `grade` from 02_evaluate.py,
and `judge` from judge.py, and writes its output to data/popqa_sample/...
(NEW directories), keyed by the model subdir to support cross-model runs
later if you choose.

Pipeline preserved exactly:
  - Same greedy decoding (do_sample=False, max_new_tokens=64,
    enable_thinking=False).
  - Same last-prompt-token hidden-state pickoff at every layer.
  - Same judge prompt (judge.py JUDGE_SYSTEM + JUDGE_TEMPLATE) with PopQA
    gold + aliases plugged in.

Caveats reported in output:
  - The judge has been calibrated on v1.0/v1.3 (Cohen kappa = 0.892 / 1.0
    against Claude); it has NOT been independently validated on PopQA's
    distribution. popqa_evaluate writes a 20-item spot-check pack to
    figures/.../popqa_judge_spotcheck.md so the user can eyeball it.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import random
import sys
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Import 02_evaluate.py (filename starts with a digit -> use importlib).
_HERE = Path(__file__).parent
_SPEC = importlib.util.spec_from_file_location("evaluate", _HERE / "02_evaluate.py")
_EV = importlib.util.module_from_spec(_SPEC)
sys.modules["evaluate"] = _EV
_SPEC.loader.exec_module(_EV)

from evaluate import evaluate_question, grade  # type: ignore
from judge import judge  # noqa: E402
from config import MODEL_ID, MODEL_SUBDIR, get_device, set_seeds  # noqa: E402

def _paths_for_suffix(suffix: str):
    base = Path(f"data/popqa_sample{suffix}")
    return {
        "questions": base / "questions_popqa_n800.json",
        "responses": base / "responses" / MODEL_SUBDIR,
        "activations": base / "activations" / MODEL_SUBDIR,
        "spotcheck": Path("figures") / MODEL_SUBDIR / f"popqa{suffix}_judge_spotcheck.md",
    }

os.environ.setdefault("PYTORCH_MPS_HIGH_WATERMARK_RATIO", "0.0")

JUDGE_MODEL_ID = "Qwen/Qwen3-1.7B"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                        help="Run only first N items (default: all 800)")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip items already evaluated")
    parser.add_argument("--skip-judge", action="store_true",
                        help="Skip the judge pass (run generation only)")
    parser.add_argument("--suffix", type=str, default="",
                        help="Suffix on data/popqa_sample{suffix}/ paths")
    args = parser.parse_args()

    set_seeds()
    device = get_device()
    paths = _paths_for_suffix(args.suffix)
    QUESTIONS_PATH = paths["questions"]
    RESPONSES_DIR = paths["responses"]
    ACTIVATIONS_DIR = paths["activations"]
    SPOTCHECK_PATH = paths["spotcheck"]
    print(f"Device: {device}")
    print(f"Subject model: {MODEL_ID}  (subdir: {MODEL_SUBDIR})")
    print(f"Judge model:   {JUDGE_MODEL_ID}")
    print(f"Suffix:        {args.suffix!r}")
    print(f"Questions:     {QUESTIONS_PATH}")
    print(f"Responses:     {RESPONSES_DIR}")

    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVATIONS_DIR.mkdir(parents=True, exist_ok=True)
    SPOTCHECK_PATH.parent.mkdir(parents=True, exist_ok=True)

    questions = json.load(open(QUESTIONS_PATH))
    if args.limit:
        questions = questions[: args.limit]
    print(f"Items to process: {len(questions)}")

    # ---- Load subject model ----
    print(f"\nLoading subject model {MODEL_ID}...")
    t_load = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, dtype=torch.bfloat16, device_map=device,
    )
    model.eval()
    print(f"  loaded in {time.perf_counter() - t_load:.1f}s "
          f"({model.num_parameters():,} params, "
          f"{model.config.num_hidden_layers} layers)")

    # ---- Phase 1 of evaluate: generation + hidden states ----
    n_done = 0
    n_correct = 0
    failed = []
    t_overall = time.perf_counter()
    for i, q in enumerate(questions, 1):
        qid = q["id"]
        response_path = RESPONSES_DIR / f"{qid}.json"
        if args.skip_existing and response_path.exists():
            print(f"[{i}/{len(questions)}] {qid}: SKIP (cached)")
            continue
        try:
            result = evaluate_question(model, tokenizer, device, q["question"])
        except Exception as e:
            print(f"[{i}/{len(questions)}] {qid}: ERROR {e}")
            failed.append(qid)
            continue
        is_correct = grade(result["answer_text"], q["answer"],
                           q.get("acceptable_alternatives", []))
        if is_correct:
            n_correct += 1
        n_done += 1
        torch.save(
            {"question_id": qid,
             "last_prompt_hidden": result.pop("_last_prompt_hidden"),
             "first_gen_hidden": result.pop("_first_gen_hidden")},
            ACTIVATIONS_DIR / f"{qid}.pt",
        )
        response = {
            "question_id": qid,
            "question": q["question"],
            "expected_answer": q["answer"],
            "acceptable_alternatives": q.get("acceptable_alternatives", []),
            "cutoff_class": q["cutoff_class"],
            "category": q.get("category"),
            "domain": q["domain"],
            "answer_date": q.get("answer_date"),
            "provenance": q.get("provenance"),
            "validation_status": q.get("validation_status"),
            "popqa_id": q.get("popqa_id"),
            "popqa_subj": q.get("popqa_subj"),
            "popqa_prop": q.get("popqa_prop"),
            "popqa_obj": q.get("popqa_obj"),
            "popqa_s_pop": q.get("popqa_s_pop"),
            "popqa_o_pop": q.get("popqa_o_pop"),
            "popqa_o_pop_bin": q.get("popqa_o_pop_bin"),
            "correct": is_correct,
            **result,
        }
        with open(response_path, "w") as fp:
            json.dump(response, fp, indent=2, ensure_ascii=False)
        mark = "OK" if is_correct else "X"
        elapsed = time.perf_counter() - t_overall
        rate = n_done / elapsed if elapsed > 0 else 0
        eta = (len(questions) - i) / rate / 60 if rate > 0 else 0
        print(f"[{i}/{len(questions)}] {qid} [{mark}] "
              f"o_pop={q['popqa_o_pop']:>7}  lp={result['mean_logprob']:+.3f}  "
              f"{result['answer_text'][:80]!r}  (rate {rate:.2f}/s, eta {eta:.1f} min)")

    elapsed = time.perf_counter() - t_overall
    print(f"\n=== Generation summary ===")
    print(f"  evaluated: {n_done}/{len(questions)}")
    print(f"  substring-correct: {n_correct}/{n_done}  ({n_correct/max(n_done,1)*100:.1f}%)")
    print(f"  generation time: {elapsed/60:.1f} min ({elapsed/max(n_done,1):.1f}s/item)")
    if failed:
        print(f"  FAILED ({len(failed)}): {', '.join(failed[:10])}{'...' if len(failed) > 10 else ''}")

    if args.skip_judge:
        print("Skipping judge pass (--skip-judge).")
        return

    # ---- Phase 2 of evaluate: judge re-grade ----
    print(f"\nLoading judge model {JUDGE_MODEL_ID}...")
    if JUDGE_MODEL_ID == MODEL_ID:
        judge_tok = tokenizer
        judge_model = model
        print("  judge = subject (same model)")
    else:
        judge_tok = AutoTokenizer.from_pretrained(JUDGE_MODEL_ID)
        judge_model = AutoModelForCausalLM.from_pretrained(
            JUDGE_MODEL_ID, dtype=torch.bfloat16, device_map=device,
        )
        judge_model.eval()
        print("  judge loaded.")

    from collections import Counter
    labels = Counter()
    t_judge = time.perf_counter()
    n_judged = 0
    for i, q in enumerate(questions, 1):
        qid = q["id"]
        response_path = RESPONSES_DIR / f"{qid}.json"
        if not response_path.exists():
            continue
        r = json.load(open(response_path))
        if "judge_label" in r and not args.skip_existing:
            pass  # re-grade always for first run
        j = judge(judge_model, judge_tok, device, q["question"], q["answer"],
                  q.get("acceptable_alternatives", []), r["answer_text"])
        r["judge_label"] = j["label"]
        r["judge_raw"] = j.get("raw", "")
        if j.get("parse_error"):
            r["judge_parse_error"] = True
        with open(response_path, "w") as fp:
            json.dump(r, fp, indent=2, ensure_ascii=False)
        labels[j["label"]] += 1
        n_judged += 1
        if i % 50 == 0:
            elapsed = time.perf_counter() - t_judge
            rate = n_judged / elapsed if elapsed > 0 else 0
            eta = (len(questions) - i) / rate / 60 if rate > 0 else 0
            print(f"  [{i}/{len(questions)}] labels so far: {dict(labels)}  "
                  f"(eta {eta:.1f} min)")
    elapsed = time.perf_counter() - t_judge
    print(f"\n=== Judge summary ===")
    print(f"  judged: {n_judged}/{len(questions)}")
    for lbl in ("correct", "refusal", "wrong"):
        n = labels[lbl]
        print(f"    {lbl}: {n} ({n/max(n_judged,1)*100:.1f}%)")
    print(f"  judge time: {elapsed/60:.1f} min")

    # ---- Spot-check pack ----
    rng = random.Random(7)
    response_files = sorted(RESPONSES_DIR.glob("*.json"))
    sample = rng.sample(response_files, min(20, len(response_files)))
    md = ["# PopQA judge spot-check (20 random items)\n\n"]
    md.append(f"Judge: {JUDGE_MODEL_ID} self-judge (same model as v1.3 paper).\n")
    md.append(f"Caveat: judge has NOT been independently validated on the PopQA distribution. ")
    md.append(f"Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). ")
    md.append(f"PopQA = Wikidata triples, different distribution.\n\n")
    for f in sample:
        r = json.load(open(f))
        md.append(f"---\n\n**{r['question_id']}**  (o_pop = {r.get('popqa_o_pop')}, "
                  f"judge: `{r['judge_label']}`, substring-correct: {r['correct']})\n\n")
        md.append(f"- Q: {r['question']}\n")
        md.append(f"- Gold: `{r['expected_answer']}`  ")
        alts = r.get('acceptable_alternatives', [])
        if alts:
            md.append(f"(aliases: {', '.join(f'`{a}`' for a in alts[:6])})")
        md.append("\n")
        md.append(f"- Model: {r['answer_text'][:300]!r}\n\n")
    SPOTCHECK_PATH.write_text("".join(md))
    print(f"\nSpot-check pack written: {SPOTCHECK_PATH}")


if __name__ == "__main__":
    main()
