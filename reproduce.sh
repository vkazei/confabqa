#!/usr/bin/env bash
# ConfabQA reproduction entry point.
#
#   ./reproduce.sh figures   Regenerate the numeric paper figures from the
#                            committed result artifacts (JSON). Minutes, CPU-only,
#                            no model downloads.
#   ./reproduce.sh arxiv     Build + test-compile the arXiv source package
#                            (TeX-Live-shipped fonts; produces arxiv_upload.tar.gz).
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
  "$PY" -m plots.figure_bootstrap_forest          # 14-cell forest plot  <- bootstrap_*.json
  "$PY" -m plots.figure_merge_per_layer_probes    # per-layer probe curves <- data/qwen3_1_7b_summary.json
  "$PY" -m plots.figure_sae_features              # SAE feature card <- figures/sae_decompose_refusal.json
  echo "== Done. Rebuilt PNGs are in figures/ =="
  exit 0
fi

if [[ "$MODE" == "arxiv" ]]; then
  echo "== Building the arXiv source package (TeX-Live fonts only, no macOS fonts) =="
  rm -rf arxiv_pkg && mkdir -p arxiv_pkg
  pandoc -s paper_confabqa.md -o arxiv_pkg/paper_confabqa.tex \
    --pdf-engine=xelatex \
    -V documentclass=article -V fontsize=10pt -V papersize=letter \
    -V geometry:textwidth=5.5in -V geometry:textheight=9in -V geometry:centering \
    --include-in-header=neurips_header_arxiv.tex
  "$PY" arxiv_package.py
  (cd arxiv_pkg \
    && xelatex -interaction=nonstopmode paper_confabqa.tex >/dev/null \
    && xelatex -interaction=nonstopmode paper_confabqa.tex >/dev/null \
    && rm -f paper_confabqa.aux paper_confabqa.log paper_confabqa.out \
    && tar czf ../arxiv_upload.tar.gz paper_confabqa.tex figures/)
  echo "== arxiv_upload.tar.gz ready; test-compiled PDF at arxiv_pkg/paper_confabqa.pdf =="
  exit 0
fi

if [[ "$MODE" != "full" ]]; then
  echo "usage: ./reproduce.sh [figures|arxiv|full]" >&2; exit 1
fi

echo "== FULL PIPELINE (this takes days; see README hardware notes) =="
"$PY" 01_question_set.py

for M in "Qwen/Qwen3-1.7B" "unsloth/gemma-2-2b-it" "unsloth/Llama-3.2-3B-Instruct"; do
  MODEL_ID="$M" "$PY" 02_evaluate.py
done
MODEL_ID=Qwen/Qwen3-1.7B "$PY" 04_regrade.py

"$PY" -m external.popqa_prepare
"$PY" -m external.triviaqa_prepare
MODEL_ID=Qwen/Qwen3-1.7B "$PY" -m external.popqa_evaluate
MODEL_ID=Qwen/Qwen3-1.7B "$PY" -m external.triviaqa_evaluate
# Repeat evaluate for Qwen3-4B / Llama-3.2-3B; judge via external.popqa_judge_only
# (separate process, avoids subject+judge co-load OOM on 16 GB).

"$PY" -m analysis.bootstrap_h_adds
"$PY" -m analysis.bootstrap_llama_external
"$PY" -m analysis.bootstrap_qwen3_4b
"$PY" -m analysis.refusal_channel_test
"$PY" -m analysis.cross_dataset_transfer

"$PY" -m saes.sae_test_reconstruction
"$PY" -m saes.sae_decompose_refusal
"$PY" -m saes.sae_causal_ablation

"$PY" -m plots.figure_bootstrap_forest
"$PY" -m plots.figure_merge_per_layer_probes
"$PY" -m plots.figure_sae_features
"$PY" -m plots.figure_atlas_merged
"$PY" -m plots.figure_embeddings_merged
"$PY" -m plots.figure_confidence_merged

pandoc paper_confabqa.md -o paper_confabqa.pdf \
  --pdf-engine=xelatex \
  -V documentclass=article -V fontsize=10pt -V papersize=letter \
  -V geometry:textwidth=5.5in -V geometry:textheight=9in -V geometry:centering \
  -V CJKmainfont="Heiti SC" \
  --include-in-header=neurips_header.tex
echo "== Full pipeline complete =="
