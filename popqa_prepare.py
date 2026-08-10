"""Phase 2 step 1: pull PopQA, stratified sample N=800 by o_pop (object Wikipedia
pageviews), map to the paper's schema, persist as a NEW dataset under
data/popqa_sample/.

Caveats this script encodes (also reported in the output md):
  - PopQA is templated from Wikidata triples, so it doesn't fully escape the
    surface-form concern. Its value is (a) independent construction, (b) a
    continuous popularity variable (Wikipedia pageviews), (c) a different
    distribution from the v1.3 set.
  - PopQA has no knowledge-cutoff structure -- mostly static factual triples.
    The cutoff disconfound does NOT apply. Every item is marked
    cutoff_class='external'.
  - PopQA items are mostly answerable, so refusals are expected to be rare in
    the model output. The popqa_analyze.py step will only run the refusal probe
    if >=30 refusals appear.

Stratification: bin o_pop into 5 percentile bins (0-20, 20-40, 40-60, 60-80,
80-100) and sample evenly within each bin (160 per bin = 800 total).
random.Random(0) for reproducibility.

Writes:
  data/popqa_sample/questions_popqa_n800.json
  data/popqa_sample/popqa_sample_metadata.json   (stratification spec, seed,
                                                   per-bin n, schema mapping)
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from datasets import load_dataset

N = 800
N_BINS = 5
SEED = 0
# OUT paths now built inside main() from --seed / --suffix args.


def parse_aliases(blob):
    """possible_answers is stored as a JSON-encoded list string."""
    if not blob:
        return []
    if isinstance(blob, list):
        return [str(x) for x in blob]
    if isinstance(blob, str):
        try:
            arr = json.loads(blob)
            if isinstance(arr, list):
                return [str(x) for x in arr]
        except json.JSONDecodeError:
            pass
        # Fallback: comma-split
        return [s.strip() for s in blob.strip("[]").split(",") if s.strip()]
    return []


def percentile_bin(value, edges):
    for i, e in enumerate(edges):
        if value <= e:
            return i
    return len(edges)


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=SEED,
                   help="RNG seed for the stratified sample (default 0)")
    p.add_argument("--suffix", type=str, default="",
                   help="Suffix on data/popqa_sample{suffix}/ paths")
    args = p.parse_args()
    seed = args.seed
    out_dir = Path(f"data/popqa_sample{args.suffix}")
    questions_path = out_dir / "questions_popqa_n800.json"
    meta_path = out_dir / "popqa_sample_metadata.json"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("Loading PopQA test split...")
    ds = load_dataset("akariasai/PopQA", split="test")
    n_total = len(ds)
    print(f"  total PopQA items: {n_total}")

    # Build o_pop percentile edges. Sort once.
    o_pops = sorted(int(r["o_pop"]) for r in ds)
    quintile_edges = [o_pops[int(n_total * q / N_BINS) - 1]
                      for q in range(1, N_BINS + 1)]
    print(f"  o_pop quintile edges: {quintile_edges}")

    # Group by bin
    by_bin = {i: [] for i in range(N_BINS)}
    for idx in range(n_total):
        r = ds[idx]
        b = percentile_bin(int(r["o_pop"]), quintile_edges)
        if b >= N_BINS:
            b = N_BINS - 1
        by_bin[b].append(idx)

    print("  bin sizes (full PopQA):")
    for i in range(N_BINS):
        edges_desc = (f"<= {quintile_edges[i]}" if i == 0
                      else f"({quintile_edges[i-1]}, {quintile_edges[i]}]")
        print(f"    bin {i} {edges_desc}: n = {len(by_bin[i])}")

    # Sample evenly per bin
    per_bin = N // N_BINS
    rng = random.Random(seed)
    sampled_idxs = []
    for i in range(N_BINS):
        pool = by_bin[i][:]
        rng.shuffle(pool)
        sampled_idxs.extend(pool[:per_bin])
    rng.shuffle(sampled_idxs)
    print(f"  sampled {len(sampled_idxs)} items ({per_bin} per bin x {N_BINS} bins)")

    # Build questions in the paper's schema
    questions = []
    for sidx, idx in enumerate(sampled_idxs):
        r = ds[idx]
        aliases = parse_aliases(r.get("possible_answers"))
        # The first element of possible_answers usually equals obj; keep the rest
        # as acceptable_alternatives (drop duplicate of gold).
        gold = str(r["obj"])
        alts = [a for a in aliases if a and a != gold]
        bin_i = percentile_bin(int(r["o_pop"]), quintile_edges)
        if bin_i >= N_BINS:
            bin_i = N_BINS - 1
        q = {
            "id": f"popqa_{sidx:04d}",
            "question": r["question"],
            "answer": gold,
            "acceptable_alternatives": alts,
            "cutoff_class": "external",
            "category": "popqa",
            "domain": f"popqa_{r['prop']}",
            "answer_date": "wikidata",
            "provenance": r.get("o_uri", ""),
            "validation_status": "popqa_external",
            # PopQA-specific bookkeeping (preserved):
            "popqa_id": int(r["id"]),
            "popqa_subj": r["subj"],
            "popqa_prop": r["prop"],
            "popqa_obj": gold,
            "popqa_s_pop": int(r["s_pop"]),
            "popqa_o_pop": int(r["o_pop"]),
            "popqa_o_pop_bin": bin_i,
        }
        questions.append(q)

    with open(questions_path, "w") as fp:
        json.dump(questions, fp, indent=2, ensure_ascii=False)
    print(f"\nWrote {questions_path}  ({len(questions)} items)")

    # Metadata
    bin_counts = {i: sum(1 for q in questions if q["popqa_o_pop_bin"] == i)
                  for i in range(N_BINS)}
    o_pop_in_sample = [q["popqa_o_pop"] for q in questions]
    meta = {
        "dataset": "akariasai/PopQA test split",
        "n_total_in_popqa": n_total,
        "n_sampled": len(questions),
        "stratification": {
            "variable": "o_pop (object Wikipedia pageviews)",
            "n_bins": N_BINS,
            "edge_strategy": "quintiles over full PopQA o_pop distribution",
            "quintile_edges_o_pop": quintile_edges,
            "per_bin_target": per_bin,
            "per_bin_actual": bin_counts,
        },
        "rng_seed": seed,
        "sample_o_pop_summary": {
            "min": min(o_pop_in_sample),
            "max": max(o_pop_in_sample),
            "median": sorted(o_pop_in_sample)[len(o_pop_in_sample) // 2],
        },
        "schema_mapping": {
            "question": "PopQA.question (Wikidata-templated)",
            "answer": "PopQA.obj",
            "acceptable_alternatives": "PopQA.possible_answers \\ {answer}",
            "cutoff_class": "literal string 'external' (PopQA has no cutoff structure)",
            "category": "literal string 'popqa'",
            "domain": "'popqa_' + PopQA.prop (relation name)",
            "popqa_o_pop": "preserved for popularity-split analysis",
            "popqa_o_pop_bin": "0-4 quintile bin",
        },
        "caveats": [
            "PopQA is templated from Wikidata, so it does not fully escape the "
            "surface-form concern in Phase 1. Value: independent construction + "
            "real continuous popularity signal + different distribution.",
            "PopQA has no cutoff structure (mostly static facts); the "
            "cutoff/correctness disconfound does NOT apply. Every item is "
            "marked cutoff_class='external'.",
            "PopQA questions are mostly answerable, so refusals are expected to "
            "be rare. The refusal-vs-wrong probe will only be run on the PopQA "
            "sample if at least 30 refusals appear.",
        ],
    }
    with open(meta_path, "w") as fp:
        json.dump(meta, fp, indent=2, ensure_ascii=False)
    print(f"Wrote {meta_path}")

    # Print quick distribution check
    print("\nSample o_pop distribution by bin:")
    for i in range(N_BINS):
        items = [q for q in questions if q["popqa_o_pop_bin"] == i]
        if items:
            mn = min(q["popqa_o_pop"] for q in items)
            mx = max(q["popqa_o_pop"] for q in items)
            print(f"  bin {i}: n={len(items):3d}  o_pop in [{mn}, {mx}]")


if __name__ == "__main__":
    main()
