# Windows setup

Use **MiKTeX** (smaller, installs packages on demand) or **TeX Live**.

## Option A — MiKTeX (recommended)

1. Install from https://miktex.org/download
2. During setup: enable **install missing packages on the fly**.
3. Open **MiKTeX Console → Updates → Check for updates**.
4. Confirm these tools exist (Win + R → `cmd`):

```bat
xelatex --version
latexmk -v
```

If `latexmk` is missing: MiKTeX Console → Packages → search `latexmk` → install.

XeLaTeX uses **Times New Roman** on Windows (`exam.cls` looks for it first). No extra font install.

## Option B — TeX Live

1. Install from https://tug.org/texlive/windows.html
2. Keep the default scheme, or at least collections that include XeTeX, latex-extra, and latexmk.
3. Tick **add TeX Live to PATH**.
4. Open a **new** terminal and run the same version checks as above.

Full TeX Live is several GB; MiKTeX is usually enough for this repo.

## Python

1. Install Python 3.10+ from https://www.python.org/downloads/
2. Tick **Add python.exe to PATH**.
3. In PowerShell, from the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\scripts\generate_exam.py --help
```

If execution policy blocks the venv:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Editor

Install the **LaTeX Workshop** VS Code/Cursor extension. This repo already has `.vscode/settings.json` (latexmk + XeLaTeX, build on save).
