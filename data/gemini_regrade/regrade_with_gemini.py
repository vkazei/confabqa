"""Regrade ConfabQA-784 Qwen3-1.7B responses with Gemini.

Reads:
  data/gemini_regrade/judge_prompt.txt       (system prompt + per-item template)
  data/gemini_regrade/qwen3_1_7b_items.jsonl (784 items)

Writes:
  data/gemini_regrade/qwen3_1_7b_gemini_labels.jsonl
    one line per item: {id, gemini_label, gemini_raw}

Requires: GEMINI_API_KEY env var, `google-generativeai` package.

Resumes automatically: skips items already in the output file. Safe to ^C and rerun.
"""
import json
import os
import pathlib
import re
import sys
import time

import google.generativeai as genai

MODEL = "gemini-3.1-pro-preview"

ROOT = pathlib.Path("data/gemini_regrade")
PROMPT_PATH = ROOT / "judge_prompt.txt"
ITEMS_PATH = ROOT / "qwen3_1_7b_items.jsonl"
OUT_PATH = ROOT / "qwen3_1_7b_gemini_labels.jsonl"

LABEL_RE = re.compile(r"Label:\s*(CORRECT|REFUSAL|WRONG)", re.IGNORECASE)


def build_user_prompt(template_body, item):
    alts = ", ".join(repr(a) for a in (item.get("alternatives") or [])) or "(none)"
    return template_body.format(
        question=item["question"],
        expected=item["gold"],
        alternatives=alts,
        answer=(item["answer"] or "(empty)").strip(),
    )


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("Set GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    full_prompt = PROMPT_PATH.read_text()
    # Split judge_prompt.txt into the system rules + the per-item template.
    template_marker = "Per-item template:"
    system_text, template_text = full_prompt.split(template_marker, 1)
    template_body = template_text.strip()

    model = genai.GenerativeModel(MODEL, system_instruction=system_text.strip())

    done_ids = set()
    if OUT_PATH.exists():
        for line in OUT_PATH.open():
            done_ids.add(json.loads(line)["id"])
    print(f"Already graded: {len(done_ids)}")

    items = [json.loads(line) for line in ITEMS_PATH.open()]
    todo = [it for it in items if it["id"] not in done_ids]
    print(f"To grade: {len(todo)}")

    with OUT_PATH.open("a") as f:
        for i, item in enumerate(todo, 1):
            user_msg = build_user_prompt(template_body, item)
            try:
                resp = model.generate_content(user_msg)
                raw = (resp.text or "").strip()
            except Exception as e:
                raw = f"ERROR: {e}"
            m = LABEL_RE.search(raw)
            label = m.group(1).lower() if m else "unparsed"
            out = {"id": item["id"], "gemini_label": label, "gemini_raw": raw}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
            f.flush()
            if i % 25 == 0:
                print(f"  [{i}/{len(todo)}] last id={item['id']} label={label}")
            # Gemini 3.1 Pro Preview is tightly rate-limited; back off on 429s.
            if "ERROR: 429" in raw:
                time.sleep(30)
            else:
                time.sleep(2.0)

    print(f"Done. Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
