"""Assemble the arXiv source package.

Run by `./reproduce.sh arxiv` after pandoc has written arxiv_pkg/paper_confabqa.tex:
prepends the xelatex engine hint and copies every asset the .tex references
(\includegraphics PNGs and \input TikZ files) into arxiv_pkg/.
"""
import re
import shutil
from pathlib import Path

TEX = Path("arxiv_pkg/paper_confabqa.tex")

t = TEX.read_text()
if not t.startswith("% !TEX"):
    TEX.write_text("% !TEX program = xelatex\n" + t)

assets = set(re.findall(r"\{(figures/[^}]+?\.(?:png|pdf|jpe?g))\}", t))
assets |= {f + ".tex" for f in re.findall(r"\\input\{(figures/[^}]+?)\}", t)}
assets = {f.replace("\\_", "_") for f in assets}
for f in sorted(assets):
    src = Path(f)
    dst = Path("arxiv_pkg") / src
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)
    print(f"packed {src}")
