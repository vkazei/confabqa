import argparse
import json
import os
import time

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from pathlib import Path

from config import (
    ACTIVATIONS_DIR,
    MODEL_ID,
    RESPONSES_DIR,
    get_device,
    get_questions_path,
    set_seeds,
)

MAX_NEW_TOKENS = 64

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"


def load_questions(path: Path, include_flagged: bool = False):
    with open(path) as f:
        data = json.load(f)
    items = [q for q in data if not q["id"].startswith("_")]
    if not include_flagged:
        items = [q for q in items if q.get("validation_status") != "flagged"]
    return items


def grade(answer_text: str, expected: str, alternatives, window: int = 200) -> bool:
    # Check only the first `window` characters so a wrong primary answer that
    # later mentions the correct name in passing (e.g. "Biden won; Trump lost")
    # doesn't get scored as correct.
    head = answer_text[:window].lower()
    if expected and expected.lower() in head:
        return True
    for alt in alternatives or []:
        if alt and alt.lower() in head:
            return True
    return False


def evaluate_question(model, tokenizer, device, question_text):
    messages = [{"role": "user", "content": question_text}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    inputs = tokenizer(text, return_tensors="pt").to(device)
    input_len = inputs["input_ids"].shape[1]

    t_start = time.perf_counter()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            return_dict_in_generate=True,
            output_hidden_states=True,
            output_scores=True,
        )
    t_total = time.perf_counter() - t_start

    new_tokens = outputs.sequences[0, input_len:]
    num_new = new_tokens.shape[0]
    answer_text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    token_logprobs = []
    entropies = []
    first_token_top5 = []
    for t, score in enumerate(outputs.scores):
        logits = score[0].float()
        logprobs = F.log_softmax(logits, dim=-1)
        chosen_id = new_tokens[t].item()
        token_logprobs.append(logprobs[chosen_id].item())
        probs = logprobs.exp()
        ent = -(probs * logprobs).sum().item()
        entropies.append(ent)
        if t == 0:
            topk = torch.topk(logprobs, k=5)
            first_token_top5 = [
                {"token": tokenizer.decode([tid.item()]), "logprob": lp.item()}
                for tid, lp in zip(topk.indices, topk.values)
            ]

    mean_logprob = sum(token_logprobs) / len(token_logprobs) if token_logprobs else 0.0
    mean_entropy = sum(entropies) / len(entropies) if entropies else 0.0
    min_logprob = min(token_logprobs) if token_logprobs else 0.0

    prefill_hiddens = outputs.hidden_states[0]
    last_prompt_per_layer = torch.stack(
        [layer_h[0, -1, :].detach().cpu().float() for layer_h in prefill_hiddens],
        dim=0,
    )
    if len(outputs.hidden_states) > 1:
        first_gen_hiddens = outputs.hidden_states[1]
        first_gen_per_layer = torch.stack(
            [layer_h[0, -1, :].detach().cpu().float() for layer_h in first_gen_hiddens],
            dim=0,
        )
    else:
        first_gen_per_layer = None

    return {
        "answer_text": answer_text,
        "input_tokens": input_len,
        "new_tokens": num_new,
        "generation_time_s": t_total,
        "tokens_per_sec": num_new / t_total if t_total > 0 else 0,
        "token_logprobs": token_logprobs,
        "token_entropies": entropies,
        "mean_logprob": mean_logprob,
        "min_logprob": min_logprob,
        "mean_entropy": mean_entropy,
        "first_token_top5": first_token_top5,
        "_last_prompt_hidden": last_prompt_per_layer,
        "_first_gen_hidden": first_gen_per_layer,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Run only first N questions")
    parser.add_argument("--skip-existing", action="store_true", help="Skip questions already evaluated")
    parser.add_argument("--questions", type=str, default=None,
                        help="Explicit path to question JSON (default: prefer v1 if present, else v0)")
    parser.add_argument("--include-flagged", action="store_true",
                        help="Include items with validation_status=flagged (default: skip them)")
    args = parser.parse_args()

    set_seeds()
    device = get_device()
    print(f"Device: {device}")

    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVATIONS_DIR.mkdir(parents=True, exist_ok=True)

    questions_path = Path(args.questions) if args.questions else get_questions_path()
    print(f"Questions: {questions_path}")
    questions = load_questions(questions_path, include_flagged=args.include_flagged)
    if args.limit:
        questions = questions[: args.limit]
    print(f"Evaluating {len(questions)} questions")

    print(f"Loading {MODEL_ID}...")
    t_load = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        dtype=torch.bfloat16,
        device_map=device,
    )
    model.eval()
    print(f"Model loaded in {time.perf_counter() - t_load:.1f}s "
          f"({model.num_parameters():,} params, {model.config.num_hidden_layers} layers)")

    n_correct = 0
    n_total = 0
    failed_ids = []
    t_overall = time.perf_counter()
    for i, q in enumerate(questions, 1):
        qid = q["id"]
        response_path = RESPONSES_DIR / f"{qid}.json"
        if args.skip_existing and response_path.exists():
            print(f"[{i}/{len(questions)}] {qid}: SKIP (already evaluated)")
            continue

        print(f"[{i}/{len(questions)}] {qid} ({q['cutoff_class']}/{q['domain']}): {q['question'][:55]}")
        try:
            result = evaluate_question(model, tokenizer, device, q["question"])
        except Exception as e:
            print(f"  ERROR: {e}")
            failed_ids.append(qid)
            continue

        is_correct = grade(result["answer_text"], q["answer"], q.get("acceptable_alternatives", []))
        n_total += 1
        if is_correct:
            n_correct += 1

        torch.save(
            {
                "question_id": qid,
                "last_prompt_hidden": result.pop("_last_prompt_hidden"),
                "first_gen_hidden": result.pop("_first_gen_hidden"),
            },
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
            "correct": is_correct,
            **result,
        }
        with open(response_path, "w") as f:
            json.dump(response, f, indent=2, ensure_ascii=False)

        mark = "OK" if is_correct else "X"
        print(f"  [{mark}] {result['answer_text'][:80]}")
        print(f"      mean_logprob={result['mean_logprob']:.3f} "
              f"mean_entropy={result['mean_entropy']:.2f} "
              f"tok/s={result['tokens_per_sec']:.1f}")

    elapsed = time.perf_counter() - t_overall
    acc = n_correct / n_total if n_total else 0.0
    print(f"\n=== Summary ===")
    print(f"Evaluated: {n_total}/{len(questions)}")
    print(f"Correct: {n_correct}/{n_total} ({acc:.1%})")
    print(f"Total time: {elapsed:.1f}s ({elapsed/n_total:.1f}s/q)" if n_total else f"Total time: {elapsed:.1f}s")
    if failed_ids:
        print(f"FAILED ({len(failed_ids)}): {', '.join(failed_ids)}")


if __name__ == "__main__":
    main()
