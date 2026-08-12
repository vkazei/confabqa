"""Judge prompt/parser logic (imports judge.py, which needs torch installed)."""
import judge


def test_label_regex_variants():
    for raw, want in [
        ("Label: CORRECT", "CORRECT"),
        ("label: refusal", "REFUSAL"),
        ("noise before\nLabel: WRONG trailing", "WRONG"),
    ]:
        m = judge.LABEL_RE.search(raw)
        assert m and m.group(1).upper() == want


def test_label_regex_rejects_garbage():
    assert judge.LABEL_RE.search("The answer is correct.") is None


def test_build_prompt_contains_fields():
    p = judge._build_prompt("Q?", "Gold", ["Alt1"], "Answer text")
    assert "Q?" in p and "Gold" in p and "'Alt1'" in p and "Answer text" in p


def test_build_prompt_no_alternatives():
    p = judge._build_prompt("Q?", "Gold", [], "A")
    assert "(none)" in p


def test_build_prompt_empty_answer():
    p = judge._build_prompt("Q?", "Gold", None, "   ")
    assert "(empty)" in p
