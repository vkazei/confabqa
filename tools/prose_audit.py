"""Prose-only audit: check that an edit to the paper source changed wording and
nothing else.

For every file it compares the working tree against a git base and reports any
difference in the multiset of
  numbers, citation keys, labels and references, units (%, pp, \\times, \\circ,
  \\ldots), math segments, headings, and \\input / \\includegraphics targets.
LaTeX comments are ignored and whitespace inside math is normalized, so
re-wrapping a paragraph passes while a dropped digit, a renamed label, or a
"pp" turned into "%" fails. It also lists em-dashes, which the paper does not use.

Run from the repo root:
  python -m tools.prose_audit                  # working tree vs HEAD
  python -m tools.prose_audit --base cfe5c0e   # working tree vs a fixed base
  python -m tools.prose_audit tex/sections/06_probe_to_tokens.tex

Exit status is 1 if any file differs. Standard library only.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_FILES = ["tex/paper_confabqa.tex", *sorted(
    str(p.relative_to(REPO)) for p in (REPO / "tex" / "sections").glob("*.tex"))]

COMMENT = re.compile(r"(?<!\\)%.*")
MATH = re.compile(
    r"\\\((.*?)\\\)|\\\[(.*?)\\\]"
    r"|\\begin\{(equation|align|gather|multline)\*?\}(.*?)\\end\{\3\*?\}",
    re.DOTALL)
CITE = re.compile(r"\\[cC]ite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")


def strip_comments(text):
    return "\n".join(COMMENT.sub("", line) for line in text.split("\n"))


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def extract(text):
    text = strip_comments(text)
    cites = Counter()
    for m in CITE.finditer(text):
        cites.update(k.strip() for k in m.group(1).split(",") if k.strip())
    return {
        "numbers": Counter(re.findall(r"\d(?:[\d.,]*\d)?", text)),
        "cite keys": cites,
        "labels/refs": Counter(
            f"\\{cmd}{{{arg}}}" for cmd, arg in re.findall(
                r"\\(label|ref|eqref|autoref|pageref|[cC]ref)\{([^}]*)\}", text)),
        "units": Counter(re.findall(r"\\%|\bpp\b|\\times|\\circ|\\ldots", text)),
        "math": Counter(squash(m.group(0)) for m in MATH.finditer(text)),
        "headings": Counter(
            squash(m.group(0)) for m in re.finditer(
                r"\\(?:sub)*section\*?\{(?:[^{}]|\{[^{}]*\})*\}", text)),
        "includes": Counter(re.findall(
            r"\\(?:input|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}", text)),
    }


def git_show(base, path):
    r = subprocess.run(["git", "show", f"{base}:{path}"], cwd=REPO,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def fmt(counter):
    return "  ".join(f"[{k}]" + (f" x{n}" if n > 1 else "")
                     for k, n in sorted(counter.items()))


def em_dashes(text):
    hits = []
    for i, line in enumerate(text.split("\n"), 1):
        body = COMMENT.sub("", line)
        if "\u2014" in body or re.search(r"(?<!-)---(?!-)", body):
            hits.append(i)
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*", default=DEFAULT_FILES,
                    help="paths relative to the repo root (default: the paper source)")
    ap.add_argument("--base", default="HEAD", help="git ref to compare against")
    args = ap.parse_args()

    failed = 0
    for path in args.files:
        new_path = REPO / path
        if not new_path.exists():
            print(f"FAIL  {path}: missing from the working tree")
            failed += 1
            continue
        new_text = new_path.read_text()
        old_text = git_show(args.base, path)
        if old_text is None:
            print(f"FAIL  {path}: not present at {args.base}")
            failed += 1
            continue

        old, new = extract(old_text), extract(new_text)
        diffs = [(cat, old[cat] - new[cat], new[cat] - old[cat])
                 for cat in old if old[cat] != new[cat]]
        dashes = em_dashes(new_text)
        if not diffs:
            state = "same" if old_text == new_text else "PASS"
            n_num, n_math = sum(new["numbers"].values()), sum(new["math"].values())
            print(f"{state:5} {path}  ({n_num} numbers, {n_math} math segments)")
        else:
            failed += 1
            print(f"FAIL  {path}")
            for cat, removed, added in diffs:
                if removed:
                    print(f"        {cat} removed: {fmt(removed)}")
                if added:
                    print(f"        {cat} added:   {fmt(added)}")
        if dashes:
            print(f"        note: em-dash on line(s) {', '.join(map(str, dashes))}")

    print(f"\n{'FAIL' if failed else 'PASS'}: {len(args.files) - failed}/"
          f"{len(args.files)} files prose-only against {args.base}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
