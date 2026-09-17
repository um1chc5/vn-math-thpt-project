# How the pipeline works

Jinja does **not** generate HTML in this project. It generates **LaTeX**. XeLaTeX builds the PDF.

```
src/question-bank/*.jsonl
        │  Python selects questions (lớp, chương, mức độ, tỉ lệ / loại đề YAML)
        ▼
src/templates/papers/*.tex.j2 + src/templates/items/*.tex.j2
        │  Jinja fills header + question loop
        ▼
src/output/lop12/giua-ki/2026-09-17-de-a/*.tex
        │  latexmk -xelatex
        ▼
same folder → PDF
```

The bank entry can contain rich LaTeX, not only plain text: TikZ drawings, variation tables, tabular data, and references to image assets. The agent may author or repair those snippets before running the same pipeline.

`src/output/` is generated output. If review finds a problem, update the bank, config, or template and regenerate so the correction remains reusable.

## Why Jinja at all?

`exam.cls` cannot loop over a JSON question bank. Something has to turn “12 random questions + school name + đáp án on/off” into a `.tex` file.

Jinja is that step: a **text** template engine. Web apps use it for HTML; we use the same engine for LaTeX because:

- `\begin{question} … \end{question}` is repeated with `{% for q in questions %}`
- đề vs đáp án is `{% if show_answers %}` — no duplicated Python string soup
- teachers can edit `src/templates/papers/` and `src/templates/items/` without touching `src/scripts/generate_exam.py`

It is **not** a web renderer. Nothing is served in a browser.

## Why not write `.tex` from Python f-strings?

You can, but `{` `}` in LaTeX fights with Python format strings, and conditionals get messy. Jinja keeps the template looking like LaTeX.

## Compile without Python

If a `.tex` already sits in `src/output/`:

```bash
cd vn-math-thpt-project
export TEXINPUTS="$(pwd)/src/templates//:"
latexmk -xelatex -outdir=src/output/lop12/giua-ki/2026-09-17-de-a \
  src/output/lop12/giua-ki/2026-09-17-de-a/de-a.tex
```

`--no-compile` on the generator writes `.tex` only, then you run `latexmk` yourself.
