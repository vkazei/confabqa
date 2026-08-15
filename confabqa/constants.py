"""Shared experiment constants (single source of truth).

Values are verbatim from the scripts that produced the paper's artifacts;
changing any of them invalidates the committed results.
"""
# --- SAE experiments (Qwen3-1.7B only) ---
SAE_RELEASE = "qwen-scope-3-1.7b-base-w32k-l50"
SAE_HF_LAYER = 28   # index into HF hidden_states (embedding = 0)
SAE_LAYER = 27      # Qwen-Scope layer id: post-block-27 residual stream
SAE_FEATURE_ID = 2191  # canonical refusal-opener feature (selection: paper §5.9)

# --- balanced-subsample bootstrap (paper §7.1) ---
BOOTSTRAP_K = 30
MAX_PER_CLASS = 400
