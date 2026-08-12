#!/usr/bin/env bash
# ConfabQA reproduction entry point.
#
#   ./reproduce.sh figures   Regenerate the numeric paper figures from the
#                            committed result artifacts (JSON). Minutes, CPU-only,
#                            no model downloads.
#   ./reproduce.sh full      The complete pipeline: generation -> judging ->
#                            probing -> bootstraps -> SAE -> figures.
#                            ~3 days wall-clock on an M1 Pro 16 GB; needs the
#                            subject models from HF Hub.
#
# Figures that require the gitignored multi-GB activation caches (the atlas,
# embeddings, confidence-scatter, and PCA-robustness plots) are shipped as
# committed PNGs and are only rebuilt by the `full` path.
set -euo pipefail
PY="${PYTHON:-python3}"
MODE="${1:-figures}"

if [[ "$MODE" == "figures" ]]; then
  echo "== Rebuilding numeric figures from committed artifacts =="
  "$PY" figure_bootstrap_forest.py          # 14-cell forest plot  <- bootstrap_*.json
  "$PY" figure_merge_per_layer_probes.py    # per-layer probe curves <- data/qwen3_1_7b_summary.json
  "$PY" figure_sae_features.py              # SAE feature card <- figures/sae_decompose_refusal.json
  echo "== Done. Rebuilt PNGs are in figures/ =="
  exit 0
fi

if [[ "$MODE" != "full" ]]; then
  echo "usage: ./reproduce.sh [figures|full]" >&2; exit 1
fi

echo "== FULL PIPELINE (this takes days; see README hardware notes) =="
"$PY" 01_question_set.py

for M in "Qwen/Qwen3-1.7B" "unsloth/gemma-2-2b-it" "unsloth/Llama-3.2-3B-Instruct"; do
  MODEL_ID="$M" "$PY" 02_evaluate.py
done
MODEL_ID=Qwen/Qwen3-1.7B "$PY" 04_regrade.py

"$PY" popqa_prepare.py
"$PY" triviaqa_prepare.py
MODEL_ID=Qwen/Qwen3-1.7B "$PY" popqa_evaluate.py
MODEL_ID=Qwen/Qwen3-1.7B "$PY" triviaqa_evaluate.py
# Repeat evaluate for Qwen3-4B / Llama-3.2-3B; judge via popqa_judge_only.py
# (separate process, avoids subject+judge co-load OOM on 16 GB).

"$PY" bootstrap_h_adds.py
"$PY" bootstrap_llama_external.py
"$PY" bootstrap_qwen3_4b.py
"$PY" refusal_channel_test.py
"$PY" cross_dataset_transfer.py

"$PY" sae_test_reconstruction.py
"$PY" sae_decompose_refusal.py
"$PY" sae_causal_ablation.py

"$PY" figure_bootstrap_forest.py
"$PY" figure_merge_per_layer_probes.py
"$PY" figure_sae_features.py
"$PY" figure_atlas_merged.py
"$PY" figure_embeddings_merged.py
"$PY" figure_confidence_merged.py

pandoc paper_confabqa.md -o paper_confabqa.pdf \
  --pdf-engine=xelatex \
  -V documentclass=article -V fontsize=10pt -V papersize=letter \
  -V geometry:textwidth=5.5in -V geometry:textheight=9in -V geometry:centering \
  -V CJKmainfont="Heiti SC" \
  --include-in-header=neurips_header.tex
echo "== Full pipeline complete =="
