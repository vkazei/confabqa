# ConfabQA paper: build with pdfLaTeX (arXiv's default engine). Lets a bare
# `latexmk` in tex/ do the right thing, and runs bibtex when the paper cites refs.bib.
$pdf_mode  = 1;   # 1 = pdflatex
$pdflatex  = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$bibtex_use = 2;
@default_files = ('paper_confabqa.tex');   # not preamble.tex or sections/
