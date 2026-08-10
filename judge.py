import re

import torch

JUDGE_SYSTEM = """You grade a model's answer to a factual question.

You MUST decide between three labels:
- CORRECT: the answer contains the gold answer (or an acceptable alternative). Extra text is fine.
- REFUSAL: the answer does NOT contain the gold answer AND the model declines, says it lacks information, says the event hasn't happened, or anchors to a knowledge cutoff. The model is NOT asserting a specific competing fact.
- WRONG: the answer does NOT contain the gold answer AND the model confidently asserts a specific competing fact (a different name, date, entity, etc.).

Decision rule:
1. Does the answer contain the gold answer or an acceptable alternative? -> CORRECT.
2. Otherwise, does the model assert a specific competing fact (a name, entity, number)? -> WRONG.
3. Otherwise (the model declined, hedged, said it doesn't know, or said the event hasn't happened) -> REFUSAL.

Examples:

Q: Who won the 2024 election?
Gold: Donald Trump
Answer: "Donald Trump won the 2024 presidential election."
Label: CORRECT

Q: Who won the 2024 election?
Gold: Donald Trump
Answer: "Joe Biden won re-election in 2024."
Label: WRONG

Q: Who won the 2024 election?
Gold: Donald Trump
Answer: "As of my knowledge cutoff in early 2024, the election has not yet taken place, so I cannot say who won."
Label: REFUSAL

Q: Who directed Anora?
Gold: Sean Baker
Answer: "I don't have information about a film called Anora."
Label: REFUSAL

Q: What is the chemical symbol for gold?
Gold: Au
Answer: "Australia is a country in the southern hemisphere."
Label: WRONG

Respond with exactly one line: `Label: CORRECT`, `Label: REFUSAL`, or `Label: WRONG`."""

JUDGE_TEMPLATE = """Q: {question}
Gold: {expected}
Acceptable alternatives: {alternatives}

Answer to grade:
\"\"\"
{answer}
\"\"\"

Apply the decision rule. Output exactly one line."""

LABEL_RE = re.compile(r"Label:\s*(CORRECT|REFUSAL|WRONG)", re.IGNORECASE)


def _build_prompt(question, expected, alternatives, answer_text):
    alt_str = ", ".join(repr(a) for a in (alternatives or [])) or "(none)"
    return JUDGE_TEMPLATE.format(
        question=question,
        expected=expected,
        alternatives=alt_str,
        answer=answer_text.strip() or "(empty)",
    )


def judge(model, tokenizer, device, question, expected, alternatives, answer_text,
          max_new_tokens: int = 32) -> dict:
    messages = [
        {"role": "system", "content": JUDGE_SYSTEM},
        {"role": "user", "content": _build_prompt(question, expected, alternatives, answer_text)},
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    inputs = tokenizer(text, return_tensors="pt").to(device)
    input_len = inputs["input_ids"].shape[1]

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
    raw = tokenizer.decode(output_ids[0, input_len:], skip_special_tokens=True).strip()

    m = LABEL_RE.search(raw)
    if m:
        label = m.group(1).lower()
        return {"label": label, "raw": raw}

    # Fallback: look for bare keywords on the first line.
    first_line = raw.splitlines()[0].upper() if raw else ""
    for candidate in ("CORRECT", "REFUSAL", "WRONG"):
        if candidate in first_line:
            return {"label": candidate.lower(), "raw": raw}

    return {"label": "wrong", "raw": raw, "parse_error": True}
