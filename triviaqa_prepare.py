"""Phase 2 follow-up: pull TriviaQA (closed-book, unfiltered.nocontext) and
sample N=800 for an external generalization check. Mirrors popqa_prepare.py
in structure; differences are dataset-specific.

TriviaQA was the primary dataset behind Kadavath et al. (2022) "Language
Models (Mostly) Know What They Know" P(IK) calibration experiments. Closed-
book QA matches the open-ended generation shape of the v1 paper (no MC).

Caveats:
  - TriviaQA has no continuous popularity axis like PopQA. Sampling is a
    simple uniform random sample (random.Random(0)).
  - TriviaQA has no cutoff structure (mostly trivia from <=2017 sources).
    cutoff_class is set to "external".
  - The aliases set in TriviaQA covers many surface forms but is not
    exhaustive; substring grading + the same-model judge may both produce
    some false-negative correctness errors. Spot-check pack written for
    inspection.

Writes:
  data/triviaqa_sample/questions_triviaqa_n800.json
  data/triviaqa_sample/triviaqa_sample_metadata.json
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from datasets import load_dataset

N = 800
SEED = 0


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=SEED,
                   help="RNG seed for the random sample (default 0)")
    p.add_argument("--suffix", type=str, default="",
                   help="Suffix appended to the output dir name, e.g. '_seed1'")
    args = p.parse_args()
    seed = args.seed
    out_dir = Path(f"data/triviaqa_sample{args.suffix}")
    questions_path = out_dir / "questions_triviaqa_n800.json"
    meta_path = out_dir / "triviaqa_sample_metadata.json"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Loading TriviaQA (mandarjoshi/trivia_qa, unfiltered.nocontext, validation)...")
    ds = load_dataset("mandarjoshi/trivia_qa", "unfiltered.nocontext",
                      split="validation")
    n_total = len(ds)
    print(f"  total TriviaQA validation items: {n_total}")

    rng = random.Random(seed)
    idxs = list(range(n_total))
    rng.shuffle(idxs)
    sampled = idxs[:N]
    print(f"  sampled {len(sampled)} items (random.Random({seed}))")

    questions = []
    answer_len_dist = {"short": 0, "medium": 0, "long": 0}
    for sidx, idx in enumerate(sampled):
        r = ds[idx]
        gold = r["answer"]["value"]
        # Dedup aliases against the canonical answer string (preserve order).
        aliases = list(dict.fromkeys(r["answer"].get("aliases", [])))
        alts = [a for a in aliases if a and a != gold]
        # Crude answer-length proxy (no popularity axis here)
        word_len = len(gold.split())
        if word_len == 1:
            answer_len_dist["short"] += 1
        elif word_len <= 3:
            answer_len_dist["medium"] += 1
        else:
            answer_len_dist["long"] += 1
        q = {
            "id": f"triviaqa_{sidx:04d}",
            "question": r["question"],
            "answer": gold,
            "acceptable_alternatives": alts,
            "cutoff_class": "external",
            "category": "triviaqa",
            "domain": "triviaqa",
            "answer_date": "trivia_qa_validation",
            "provenance": r.get("question_source", ""),
            "validation_status": "triviaqa_external",
            # TriviaQA-specific bookkeeping
            "triviaqa_qid": r["question_id"],
            "triviaqa_n_aliases": len(aliases),
            "triviaqa_answer_word_len": word_len,
            "triviaqa_answer_type": r["answer"].get("type", ""),
        }
        questions.append(q)

    with open(questions_path, "w") as fp:
        json.dump(questions, fp, indent=2, ensure_ascii=False)
    print(f"\nWrote {questions_path}  ({len(questions)} items)")

    meta = {
        "dataset": "mandarjoshi/trivia_qa (unfiltered.nocontext, validation split)",
        "n_total_in_split": n_total,
        "n_sampled": len(questions),
        "rng_seed": seed,
        "sampling": "uniform random over the validation split",
        "answer_length_distribution_in_sample": answer_len_dist,
        "schema_mapping": {
            "question": "TriviaQA.question",
            "answer": "TriviaQA.answer.value",
            "acceptable_alternatives": "TriviaQA.answer.aliases \\ {answer}",
            "cutoff_class": "literal string 'external'",
            "category": "literal string 'triviaqa'",
            "domain": "literal string 'triviaqa'",
        },
        "caveats": [
            "No continuous popularity axis (unlike PopQA's o_pop pageviews).",
            "No cutoff structure -- TriviaQA is static trivia from pre-2017 sources.",
            "TriviaQA aliases cover many surface forms but are not exhaustive; "
            "substring + same-model-judge may produce some false-negative "
            "correctness errors. A 20-item spot-check pack is written for "
            "manual inspection (figures/{model}/triviaqa_judge_spotcheck.md).",
            "Kadavath et al. (2022) leaned heavily on TriviaQA for their P(IK) "
            "calibration probe; running our hidden-state probe + prompt-feature "
            "baselines on the same benchmark is the most directly comparable "
            "head-to-head replication.",
        ],
    }
    with open(meta_path, "w") as fp:
        json.dump(meta, fp, indent=2, ensure_ascii=False)
    print(f"Wrote {meta_path}")
    print(f"\nAnswer-length distribution in sample: {answer_len_dist}")


if __name__ == "__main__":
    main()
