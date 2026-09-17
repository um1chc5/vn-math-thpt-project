---
name: checking-setup
description: Use when xelatex, latexmk, Python, or pip deps are missing; when compile fails with font/command-not-found; or when a teacher asks to cài TeX / cài đặt / setup this exam project.
---

# Checking setup

Teacher may not know the terminal. You run installs after a clear yes.

## Steps

1. Check: `xelatex --version`, `latexmk -v`, `python3 --version`, `python3 -c "import jinja2, yaml"`.
2. If anything is missing, **ask permission** in Vietnamese, name the command, mention `sudo` if needed.
3. OS guide: [docs/setup/README.md](../../../src/docs/setup/README.md)
4. Then: `python3 -m pip install -r requirements.txt` from `vn-math-thpt-project/`.
5. Confirm with the same version checks. Do not generate a đề until XeLaTeX exists (or teacher chose `--no-compile`).

Never paste a long apt/brew block and stop. Either they said no, or you ran it.
