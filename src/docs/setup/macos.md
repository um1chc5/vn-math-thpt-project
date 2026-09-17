# macOS setup

## TeX — MacTeX (recommended)

Install **MacTeX** from https://tug.org/mactex/ (or `brew install --cask mactex`).

That one installer covers XeLaTeX, latexmk, AMS fonts, and extra packages. Size is large (~4 GB) but you will not chase collections by hand.

```bash
xelatex --version
latexmk -v
```

Times New Roman / Arial are already on macOS; `exam.cls` will use them.

## TeX — BasicTeX (smaller)

If you prefer a small install:

```bash
brew install --cask basictex
eval "$(/usr/libexec/path_helper)"
sudo tlmgr update --self
sudo tlmgr install latexmk xetex fontspec geometry enumitem mathtools \
  xcolor setspace tools amscls amsmath collection-fontsrecommended
```

If a compile error names a missing `.sty`, install that package with `sudo tlmgr install <name>`.

## Python

```bash
# 3.10+ ; Apple Python or python.org / brew are all fine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 src/scripts/generate/generate_exam.py --help
```

## PATH note

After MacTeX, open a **new** terminal so `/Library/TeX/texbin` is on `PATH`. If `xelatex` is still “not found”:

```bash
export PATH="/Library/TeX/texbin:$PATH"
```
