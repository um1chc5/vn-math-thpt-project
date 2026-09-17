# Setup

Install two stacks: **TeX (XeLaTeX + latexmk)** and **Python 3.10+**.

| OS | Guide |
|----|--------|
| Linux (Debian/Ubuntu) | [linux.md](linux.md) |
| Windows | [windows.md](windows.md) |
| macOS | [macos.md](macos.md) |

Then in the project root:

```bash
python3 -m pip install -r requirements.txt
```

Check:

```bash
xelatex --version
latexmk -v
python3 --version
```

PDF output is always **XeLaTeX → PDF**. Python/Jinja only fills a `.tex` file first. See [how it works](../how-it-works.md).
