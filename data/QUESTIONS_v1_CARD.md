# ConfabQA — Dataset Card

## Motivation

The v0 question set (50 items, 5 domains × pre/post cutoff) suffered from a structural confound: every post-cutoff item was also something the subject model could not answer, so a probe trained to predict "model will be correct" was indistinguishable from a probe trained to predict "this question is post-cutoff." The two probes peaked at nearly the same network depth with nearly the same accuracy, and there was no way to argue, from data alone, that the probe was reading model-knowledge rather than training-data-recency.

ConfabQA breaks the confound by introducing a third category: pre-cutoff items the subject model is *expected to get wrong* despite the answer existing in its training data. These come from obscure subfields, mid-card historical figures, and runners-up — facts that exist on the public record but that small models compress lossily. If the correctness probe can predict "model will be wrong" on these items, then it is reading model-knowledge, not cutoff.

## Composition

- **Size:** 784 items (4 domains). Sports was dropped from the main analysis
  after an earlier iteration produced 0/26 correct across all sports categories; see paper
  Appendix D. Current cell counts (4 domains × 3 categories):
  | domain | well_known | obscure | post_cutoff |
  |--------|-----------:|--------:|------------:|
  | science | 42 | 45 | 119 |
  | history | 33 | 37 | 127 |
  | culture | 34 | 34 | 121 |
  | cinema | 34 | 37 | 121 |
  | **total** | **143** | **153** | **488** |

- **Schema (per item):**
  - `id` — `{dom3}_{cat2}_{nn}` (e.g. `sci_wk_01`, `sci_ob_01`, `sci_pc_01`)
  - `question` — natural-language prompt
  - `answer` — single canonical gold answer string
  - `acceptable_alternatives` — list of alternate phrasings the judge should accept
  - `cutoff_class` — `"pre"` or `"post"` (derived; `post_cutoff` category maps to `"post"`)
  - `category` — `"well_known"`, `"obscure"`, or `"post_cutoff"`
  - `domain` — one of `science`, `sports`, `history`, `culture`, `cinema`
  - `answer_date` — ISO date of when the fact became true (or `"timeless"`)
  - `source_file` — path to the source-template file the item was generated from
  - `provenance` — authoritative URL for the gold answer
  - `validation_status` — `"unverified"`, `"verified"`, `"corrected"`, `"flagged"`
  - `validation_notes` — populated by the validation step

## Collection process

1. **Source templates.** 15 JSON files at `data/sources/{domain}/{topic}.json`, each declaring a single question template and three keyed lists of substitutable rows (one list per category). Source files include human-readable selection criteria for the `well_known` vs `obscure` boundary in their `_documentation` header.
2. **Generation.** `python 01_question_set.py` walks every source file, substitutes each row into its template, assigns a stable ID, derives `cutoff_class` from `category`, and writes `data/questions_v1.json`. Order within each (domain, category) is shuffled deterministically with the project-wide random seed.
3. **External LLM validation.** `python 01_question_set.py --emit-validation-prompt` writes `data/questions_v1_validation_prompt.md` — a self-contained prompt designed to be pasted into a high-capability LLM with web access (Gemini Deep Research, Claude with web search, GPT with browsing). The prompt asks the LLM to mark each item as `verified`, `corrected`, `flagged`, or `rejected`, with citations, and to return a single JSON array.
4. **Applying corrections.** `python 01_question_set.py --apply-validation results.json` merges the LLM's verdicts back into `questions_v1.json`: gold answers are overwritten for `corrected` items (old gold preserved in `validation_notes`), `flagged` items keep their gold but are skipped by default in evaluation, `rejected` items are removed.

The validation step is not optional. A wrong gold answer silently corrupts the correctness label that becomes the probe target — and the same-model judge in `04_regrade.py` cannot catch it, since it is gold-anchored.

## Selection criteria per category

Boundaries are deliberately subjective and documented per source file. Common heuristics:

- **well_known:** the fact appears in standard textbooks or popular media for that domain; recognizable to a college-educated generalist.
- **obscure:** the fact is on the public record (Wikipedia or equivalent) but is not commonly cited; typically requires domain familiarity to recall. Examples: Nobel laureates from specific instrumentation subfields (1970s-90s), mid-card sports champions outside dynastic franchises, Best Picture winners from less-canonized decades, runners-up.
- **post_cutoff:** the answer became true after September 2024, the conservative knowledge-cutoff window for Qwen3-1.7B used in the v0 experiments. The subject model cannot have seen these facts during pretraining.

The obscure/well_known boundary is the most subjective and the most worth revisiting per-domain. The dataset card documents the heuristics used; the source-file `_documentation` blocks document them per topic.

## Intended use

This is a calibration-probing benchmark, not a general factual QA benchmark. It is designed to support experiments asking:

- *Do the model's internal activations encode whether it will produce a correct answer?*
- *Does that encoding emerge at a particular network depth?*
- *Is the encoding distinct from a "this question is about knowledge I don't have" signal (post_cutoff)?*

The 5-domain stratification controls for per-domain biases; the 3-category stratification is the central experimental lever. Treating accuracy on this set as a general capability metric would be misleading — the set is deliberately weighted toward the model's failure modes.

## Distribution

Lives in the project repository. Versioned by filename (`questions_v0.json`, `questions_v1.json`). The generator script, source files, validation prompt, and validation results JSON together form a reproducible artifact: running the same script against the same source files with the same applied validation produces the same question set. To cite a specific snapshot, reference the repository commit hash.

## Maintenance

- The source files (`data/sources/{domain}/*.json`) are the editable surface. Add rows for under-populated cells, correct gold errors found during use, or extend with new topics. Re-run `01_question_set.py` to regenerate.
- The `--apply-validation` flow preserves a corrections audit trail in `validation_notes`, so any change to a gold answer is recoverable.
- Major schema changes bump the version (`questions_v2.json`); downstream scripts already prefer the highest version present.

## Known limitations

- **Anglophone skew.** Best Picture winners, Super Bowls, Booker Prize, UK PMs, US presidents — the well_known and obscure buckets are weighted toward English-language source material and Anglo-American institutions.
- **Subjective boundary.** Whether a 1970s Best Picture is "well_known" or "obscure" depends on the rater's cultural reference frame.
- **Same-model judge in downstream pipeline.** `04_regrade.py` uses the subject model (Qwen3-1.7B) to judge its own outputs against this gold. The judge has a measured ~4% error rate on the v0 set (`report.md`). The validation pipeline above addresses gold-side errors; it does not address judge-side errors.
- **Post-cutoff scarcity.** Cleanly factual post-cutoff items (single canonical answer, sourced authoritatively) are harder to find at scale than pre-cutoff ones. The cell is under-populated for this reason.
- **Single-snapshot validation.** "Verified by Deep Research" is a snapshot in time. A 2026 re-validation pass may surface drift in citations or in the underlying facts (e.g. successor records, retracted papers).

## Versioning

| version | size | notes |
|--------:|-----:|-------|
| v0 | 50 | hand-curated; no `category` field; substring grader |
| ConfabQA (v1.3) | 784 | source-templated 4×3 (domain × category) design; external-LLM validation pipeline; carries `provenance` and `validation_status`. The dataset used throughout the paper (paper §4). |
