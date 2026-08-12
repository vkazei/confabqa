"""ConfabQA benchmark sanity checks (pure JSON, no torch needed)."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = json.loads((ROOT / "data" / "questions_v1.json").read_text())


def test_size():
    assert len(QUESTIONS) == 784


def test_unique_ids():
    ids = [q["id"] for q in QUESTIONS]
    assert len(set(ids)) == 784


def test_schema():
    required = {"question", "answer", "acceptable_alternatives", "cutoff_class",
                "category", "domain", "provenance", "validation_status", "id"}
    for q in QUESTIONS:
        assert required <= set(q), f"missing keys on {q.get('id')}"


def test_category_counts():
    c = Counter(q["category"] for q in QUESTIONS)
    assert c["well_known"] == 143
    assert c["obscure"] == 153
    assert c["post_cutoff"] == 488


def test_cutoff_consistency():
    for q in QUESTIONS:
        expected = "post" if q["category"] == "post_cutoff" else "pre"
        assert q["cutoff_class"] == expected, q["id"]


def test_domains():
    c = Counter(q["domain"] for q in QUESTIONS)
    assert set(c) == {"science", "history", "culture", "cinema"}
    assert c["science"] == 206 and c["history"] == 197
    assert c["culture"] == 189 and c["cinema"] == 192
