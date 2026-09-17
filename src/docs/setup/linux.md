# Linux setup (Debian / Ubuntu / Mint)

## TeX Live

This set is **enough** for this project (a bit more than the strict minimum):

```bash
sudo apt update
sudo apt install texlive texlive-latex-extra texlive-fonts-extra \
  texlive-science texlive-xetex texlive-lang-other texlive-pictures \
  latexmk
```

Also keep a Unicode font with Vietnamese diacritics (usually already present):

```bash
sudo apt install fonts-liberation fonts-dejavu
```

| Package | Why |
|---------|-----|
| `texlive-xetex` | **Required.** `xelatex` + `fontspec` (Vietnamese text). |
| `texlive-latex-extra` | **Required.** `enumitem`, `mathtools`, `geometry`, … |
| `latexmk` | **Required.** Script calls this to build PDF. |
| `texlive` | Base classes (`article`, `amsmath`, `xcolor`, …). |
| `texlive-fonts-extra` | Extra TeX fonts. Optional here; we prefer system fonts. |
| `texlive-science` | Extra math packages. Optional until a question uses them. |
| `texlive-lang-other` | Vietnamese hyphenation (babel/polyglossia). Optional; `fontspec` already renders diacritics. |
| `texlive-pictures` | TikZ/PGF. Optional until diagrams go into the bank. |

Strict minimum if disk is tight:

```bash
sudo apt install texlive-xetex texlive-latex-extra latexmk fonts-liberation
```

Do **not** use `pdflatex` for this project. Vietnamese in `exam.cls` needs XeLaTeX.

## Python

```bash
sudo apt install python3 python3-pip python3-venv
cd vn-math-thpt-project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Verify

```bash
which xelatex latexmk
fc-list :lang=vi | head
python3 src/scripts/generate_exam.py --help
```
