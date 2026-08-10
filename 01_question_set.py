"""Generate, emit-validation-prompt-for, and apply-validation-to the v1 question set.

Three modes (mutually exclusive):
  python 01_question_set.py                                # MODE 1: generate
  python 01_question_set.py --emit-validation-prompt       # MODE 2: prompt for external LLM
  python 01_question_set.py --apply-validation results.json  # MODE 3: merge results back

Schema (per item):
  id, question, answer, acceptable_alternatives, cutoff_class, category, domain,
  answer_date, source_file, provenance, validation_status, validation_notes
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

from config import DATA_DIR, SEED

SOURCES_DIR = DATA_DIR / "sources"
QUESTIONS_V1_PATH = DATA_DIR / "questions_v1.json"
VALIDATION_PROMPT_PATH = DATA_DIR / "questions_v1_validation_prompt.md"

DOMAINS = ["science", "history", "culture", "cinema"]  # sports dropped from main analysis (see paper appendix)
CATEGORIES = ["well_known", "obscure", "post_cutoff"]
CAT_TO_CODE = {"well_known": "wk", "obscure": "ob", "post_cutoff": "pc"}
DOM_TO_CODE = {"science": "sci", "sports": "spo", "history": "his",
               "culture": "cul", "cinema": "cin"}


def _format_template(template: str, row: dict) -> str:
    try:
        return template.format(**row)
    except KeyError as e:
        raise ValueError(f"Template {template!r} references missing field {e} in row {row!r}")


def _load_sources(domain: str) -> list[dict]:
    domain_dir = SOURCES_DIR / domain
    files = sorted(domain_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No source files in {domain_dir}")
    return [(p, json.loads(p.read_text())) for p in files]


def _build_questions_for_domain(domain: str) -> dict[str, list[dict]]:
    """Returns {category: [item, ...]} for one domain."""
    by_category = {c: [] for c in CATEGORIES}
    for source_path, source in _load_sources(domain):
        template = source["template"]
        answer_field = source["answer_field"]
        for category in CATEGORIES:
            rows = source.get(category, [])
            for row in rows:
                answer = row[answer_field]
                alts = row.get("alternatives", [])
                question_text = _format_template(template, row)
                cutoff_class = "post" if category == "post_cutoff" else "pre"
                item = {
                    "question": question_text,
                    "answer": answer,
                    "acceptable_alternatives": alts,
                    "cutoff_class": cutoff_class,
                    "category": category,
                    "domain": domain,
                    "answer_date": row.get("answer_date"),
                    "source_file": str(source_path.relative_to(DATA_DIR.parent)),
                    "provenance": row.get("provenance"),
                    "validation_status": "unverified",
                    "validation_notes": None,
                }
                by_category[category].append(item)
    return by_category


def generate(force: bool = False) -> list[dict]:
    if QUESTIONS_V1_PATH.exists() and not force:
        sys.exit(f"{QUESTIONS_V1_PATH} already exists; pass --force to overwrite.")

    rng = random.Random(SEED)
    all_items = []
    counts = defaultdict(int)
    for domain in DOMAINS:
        by_cat = _build_questions_for_domain(domain)
        for category in CATEGORIES:
            items = by_cat[category]
            rng.shuffle(items)
            dom_code = DOM_TO_CODE[domain]
            cat_code = CAT_TO_CODE[category]
            for i, item in enumerate(items, 1):
                item["id"] = f"{dom_code}_{cat_code}_{i:02d}"
                all_items.append(item)
            counts[(domain, category)] = len(items)

    print("=== Generation summary ===")
    print(f"  {'domain':10s} {'well_known':>10s} {'obscure':>10s} {'post_cutoff':>12s}")
    for d in DOMAINS:
        line = f"  {d:10s}"
        for c in CATEGORIES:
            n = counts[(d, c)]
            line += f" {n:>10d}" if c != "post_cutoff" else f" {n:>12d}"
        print(line)
    total = sum(counts.values())
    print(f"  TOTAL: {total} items")

    short = [(d, c, counts[(d, c)]) for d in DOMAINS for c in CATEGORIES if counts[(d, c)] < 10]
    if short:
        print("\nWARNING: under-populated cells (target = 10):")
        for d, c, n in short:
            print(f"  {d}/{c}: {n}")

    QUESTIONS_V1_PATH.write_text(json.dumps(all_items, indent=2, ensure_ascii=False))
    print(f"\nWrote {QUESTIONS_V1_PATH} ({len(all_items)} items)")
    return all_items


def emit_validation_prompt() -> None:
    if not QUESTIONS_V1_PATH.exists():
        sys.exit(f"Run generation first: {QUESTIONS_V1_PATH} not found.")
    items = json.loads(QUESTIONS_V1_PATH.read_text())

    lines = []
    lines.append("# Validation pass — Confabulation Atlas v1 question set\n")
    lines.append(
        "You are validating gold answers for a small LLM-calibration benchmark. The benchmark probes "
        "whether a model's hidden states encode whether it is about to answer correctly versus "
        "confabulate. A wrong gold answer in this set silently corrupts both the probe target and "
        "the same-model judge that downstream code uses. Be rigorous; cite authoritative sources.\n"
    )

    lines.append("## Task\n")
    lines.append(
        "For each numbered item below, decide one of four statuses for its gold answer:\n\n"
        "- `verified` — the gold answer is correct. Provide one authoritative citation URL.\n"
        "- `corrected` — the gold answer is wrong. Provide the correct answer, acceptable phrasing "
        "variants, an authoritative citation URL, and a one-sentence explanation of the original error.\n"
        "- `flagged` — the question is ambiguous, has multiple defensible answers depending on "
        "interpretation, or the source-of-truth is disputed. Keep the gold but note the concern.\n"
        "- `rejected` — the question is ill-posed or cannot have a single objective correct answer. "
        "Recommend dropping it.\n"
    )

    lines.append("## Required output format\n")
    lines.append(
        "Return **only** a single JSON array, no prose before or after, no markdown fences. "
        "Each element has this shape:\n\n"
        "```json\n"
        "[\n"
        '  {"id": "sci_wk_01", "status": "verified", "citation": "https://example.org/...", "notes": null,\n'
        '   "corrected_answer": null, "corrected_alternatives": null},\n'
        '  {"id": "sci_wk_02", "status": "corrected", "citation": "https://example.org/...",\n'
        '   "corrected_answer": "the actually-correct answer string",\n'
        '   "corrected_alternatives": ["alt1", "alt2"],\n'
        '   "notes": "Original gold said X; the authoritative source confirms Y."},\n'
        '  {"id": "sci_wk_03", "status": "flagged", "citation": "https://example.org/...",\n'
        '   "corrected_answer": null, "corrected_alternatives": null,\n'
        '   "notes": "Both X and Y are commonly cited as the answer; the source-of-truth depends on interpretation."},\n'
        '  {"id": "sci_wk_04", "status": "rejected", "citation": null,\n'
        '   "corrected_answer": null, "corrected_alternatives": null,\n'
        '   "notes": "The question presupposes a fact that is not established; recommend dropping."}\n'
        "]\n"
        "```\n\n"
        "Include every item in the input below. Do not omit any IDs. Do not include items not present below.\n"
    )

    lines.append(f"## Items to validate ({len(items)} total)\n")
    for item in items:
        alts = item.get("acceptable_alternatives") or []
        alts_str = ", ".join(repr(a) for a in alts) if alts else "(none)"
        provenance = item.get("provenance") or "(none on file)"
        lines.append(
            f"### {item['id']}\n"
            f"- **Question:** {item['question']}\n"
            f"- **Gold answer:** {item['answer']!r}\n"
            f"- **Acceptable alternatives:** {alts_str}\n"
            f"- **Domain / category:** {item['domain']} / {item['category']}\n"
            f"- **Answer date (claimed):** {item.get('answer_date') or '(unknown)'}\n"
            f"- **Provenance (claimed):** {provenance}\n"
        )

    lines.append("\n---\n\n")
    lines.append(
        "Now return the JSON array. Remember: no prose, no fences, just the array.\n"
    )

    VALIDATION_PROMPT_PATH.write_text("\n".join(lines))
    print(f"Wrote {VALIDATION_PROMPT_PATH} ({len(items)} items)")


def apply_validation(results_path: Path) -> None:
    if not QUESTIONS_V1_PATH.exists():
        sys.exit(f"Run generation first: {QUESTIONS_V1_PATH} not found.")
    items = json.loads(QUESTIONS_V1_PATH.read_text())
    by_id = {it["id"]: it for it in items}

    results = json.loads(Path(results_path).read_text())
    if not isinstance(results, list):
        sys.exit("validation results must be a JSON array")

    status_counts = Counter()
    corrected_diffs = []
    rejected_ids = []
    unknown_ids = []

    for entry in results:
        qid = entry.get("id")
        status = entry.get("status")
        if qid not in by_id:
            unknown_ids.append(qid)
            continue
        item = by_id[qid]
        notes = entry.get("notes")
        citation = entry.get("citation")
        status_counts[status] += 1

        if status == "verified":
            item["validation_status"] = "verified"
            if citation:
                item["provenance"] = citation
            item["validation_notes"] = notes
        elif status == "corrected":
            old_answer = item["answer"]
            corrected_answer = entry.get("corrected_answer")
            if not corrected_answer:
                print(f"WARNING: {qid} marked corrected but no corrected_answer provided; skipping")
                continue
            item["answer"] = corrected_answer
            item["acceptable_alternatives"] = entry.get("corrected_alternatives") or []
            item["validation_status"] = "corrected"
            item["validation_notes"] = f"Original gold: {old_answer!r}. " + (notes or "")
            if citation:
                item["provenance"] = citation
            corrected_diffs.append((qid, old_answer, corrected_answer))
        elif status == "flagged":
            item["validation_status"] = "flagged"
            item["validation_notes"] = notes
        elif status == "rejected":
            rejected_ids.append(qid)
        else:
            print(f"WARNING: {qid} has unknown status {status!r}; skipping")

    final_items = [it for it in items if it["id"] not in rejected_ids]
    QUESTIONS_V1_PATH.write_text(json.dumps(final_items, indent=2, ensure_ascii=False))

    print("=== Validation summary ===")
    for s, n in sorted(status_counts.items()):
        print(f"  {s}: {n}")
    if corrected_diffs:
        print(f"\nCorrected ({len(corrected_diffs)}):")
        for qid, old, new in corrected_diffs:
            print(f"  {qid}: {old!r} -> {new!r}")
    if rejected_ids:
        print(f"\nRejected and removed ({len(rejected_ids)}): {rejected_ids}")
    if unknown_ids:
        print(f"\nWARNING: validation results referenced unknown IDs: {unknown_ids}")
    missing_in_results = set(by_id) - {e.get("id") for e in results}
    if missing_in_results:
        print(f"\nWARNING: {len(missing_in_results)} questions had no entry in results: "
              f"{sorted(missing_in_results)[:5]}{'...' if len(missing_in_results) > 5 else ''}")
    print(f"\nWrote {QUESTIONS_V1_PATH} ({len(final_items)} items, "
          f"was {len(items)}, removed {len(items) - len(final_items)})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--emit-validation-prompt", action="store_true",
                       help="MODE 2: write the validation prompt for an external LLM.")
    group.add_argument("--apply-validation", type=str, metavar="RESULTS_JSON",
                       help="MODE 3: merge validation results back into questions_v1.json.")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite questions_v1.json on generation.")
    args = parser.parse_args()

    if args.emit_validation_prompt:
        emit_validation_prompt()
    elif args.apply_validation:
        apply_validation(Path(args.apply_validation))
    else:
        generate(force=args.force)


if __name__ == "__main__":
    main()
