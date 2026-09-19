# ConfabQA paper: build with XeLaTeX (fontspec + unicode-math require it;
# pdflatex/lualatex will not work). Lets a bare `latexmk` in tex/ do the
# right thing, and runs bibtex when the paper cites refs.bib.
$pdf_mode  = 5;   # 5 = xelatex
$xelatex   = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$bibtex_use = 2;
