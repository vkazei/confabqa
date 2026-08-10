from pathlib import Path

import torch

import os

MODEL_ID = os.environ.get("MODEL_ID", "Qwen/Qwen3-1.7B")


def get_model_subdir(model_id: str = None) -> str:
    if model_id is None:
        model_id = MODEL_ID
    name = model_id.split("/")[-1].lower()
    name = name.replace("-it", "").replace("-instruct", "").replace(".", "_").replace("-", "_")
    return name


MODEL_SUBDIR = get_model_subdir()

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
QUESTIONS_V0_PATH = DATA_DIR / "questions_v0.json"
QUESTIONS_V1_PATH = DATA_DIR / "questions_v1.json"
QUESTIONS_PATH = QUESTIONS_V0_PATH  # back-compat alias for any external callers
RESPONSES_DIR = DATA_DIR / "responses" / MODEL_SUBDIR
ACTIVATIONS_DIR = DATA_DIR / "activations" / MODEL_SUBDIR
FIGURES_DIR = PROJECT_DIR / "figures" / MODEL_SUBDIR
SUMMARY_PATH = DATA_DIR / f"{MODEL_SUBDIR}_summary.json"


def get_questions_path():
    """Return v1 if generated, else v0."""
    return QUESTIONS_V1_PATH if QUESTIONS_V1_PATH.exists() else QUESTIONS_V0_PATH

SEED = 0


def get_device():
    if os.environ.get("FORCE_CPU") == "1":
        return torch.device("cpu")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def set_seeds(seed: int = SEED):
    import random
    import numpy as np
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.backends.mps.is_available():
        torch.mps.manual_seed(seed)
