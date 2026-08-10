"""Regression tests for the judge.

Loads the model once at module level (slow), then runs each case as a fast
generate call. Run with: `pytest test_judge.py -v -s`.
"""
import pytest
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import MODEL_ID, get_device, set_seeds
from judge import judge


@pytest.fixture(scope="module")
def model_bundle():
    set_seeds()
    device = get_device()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, dtype=torch.float32, device_map=device,
    )
    model.eval()
    return model, tokenizer, device


CASES = [
    pytest.param(
        "Who wrote 'One Hundred Years of Solitude'?",
        "Gabriel García Márquez", ["Garcia Marquez", "Marquez"],
        "Gabriel García Márquez wrote it in 1967.",
        "correct",
        id="clean_correct",
    ),
    pytest.param(
        "What is the chemical symbol for gold?",
        "Au", ["au"],
        "Australia is a country in the southern hemisphere.",
        "wrong",
        id="substring_trap",
    ),
    pytest.param(
        "Who was the MVP of Super Bowl LIX?",
        "Jalen Hurts", [],
        "As of my knowledge cutoff in early 2024, Super Bowl LIX has not been played yet, so there is no MVP.",
        "refusal",
        id="confident_refusal",
    ),
    pytest.param(
        "Who was the MVP of Super Bowl LIX?",
        "Jalen Hurts", [],
        "The MVP of Super Bowl LIX was Patrick Mahomes of the Kansas City Chiefs.",
        "wrong",
        id="confident_wrong",
    ),
    pytest.param(
        "What is the speed of light in a vacuum, in meters per second?",
        "299792458", ["approximately 300,000,000", "3 x 10^8"],
        "About 300 million meters per second.",
        "correct",
        id="paraphrase",
    ),
    pytest.param(
        "Who won the 2024 NASA mission to Europa?",
        "Europa Clipper", [],
        "JUICE (Jupiter Icy Moon Explorer) is the NASA mission to Europa launched in 2024.",
        "wrong",
        id="confident_wrong_specific_entity",
    ),
]


@pytest.mark.parametrize("question,expected,alternatives,answer,want_label", CASES)
def test_judge_label(model_bundle, question, expected, alternatives, answer, want_label):
    model, tokenizer, device = model_bundle
    result = judge(model, tokenizer, device, question, expected, alternatives, answer)
    assert result["label"] == want_label, (
        f"\n  Question: {question}"
        f"\n  Answer:   {answer}"
        f"\n  Expected label: {want_label}"
        f"\n  Got label:      {result['label']}"
        f"\n  Judge raw:      {result['raw']!r}"
    )
