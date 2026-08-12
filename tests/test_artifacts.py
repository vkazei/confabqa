"""Committed result artifacts: 14 bootstrap cells, CI sanity, judge-label counts."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"


def _cells(name):
    return json.loads((FIG / name).read_text())


def test_bootstrap_has_14_cells_total():
    n = sum(len(_cells(f)) for f in
            ["bootstrap_h_adds.json", "bootstrap_llama_external.json",
             "bootstrap_qwen3_4b.json"])
    assert n == 14


def test_bootstrap_cell_fields_and_ci_order():
    for f in ["bootstrap_h_adds.json", "bootstrap_llama_external.json",
              "bootstrap_qwen3_4b.json"]:
        for key, cell in _cells(f).items():
            assert cell["K"] == 30, key
            assert cell["ci_95_low"] <= cell["mean"] <= cell["ci_95_high"], key
            assert cell["ci_excludes_zero"] == (
                cell["ci_95_low"] > 0 or cell["ci_95_high"] < 0), key


def test_headline_llama_cells():
    ext = _cells("bootstrap_llama_external.json")
    assert abs(ext["popqa_llama_3_2_3b_full"]["mean"] - 24.94) < 0.01
    assert abs(ext["triviaqa_llama_3_2_3b_full"]["mean"] - 21.25) < 0.01


def test_transfer_matrices_exist_for_three_models():
    for m in ["qwen3_1_7b", "gemma_2_2b", "llama_3_2_3b"]:
        j = json.loads((FIG / f"cross_dataset_transfer_{m}.json").read_text())
        assert "transfer" in j and "datasets" in j


def test_judge_label_distribution():
    items = [json.loads(l) for l in
             (ROOT / "data/gemini_regrade/qwen3_1_7b_items.jsonl").read_text().splitlines()]
    c = Counter(i["qwen_judge_label"] for i in items)
    assert (c["correct"], c["refusal"], c["wrong"]) == (235, 147, 402)
