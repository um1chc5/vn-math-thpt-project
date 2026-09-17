# Output

Default: generated đề stay local (gitignored).

Each đề folder layout after compile:

- `*.tex`, `*.pdf` — same level (what teachers open)
- `others/` — latexmk junk (`.aux`, `.log`, `.fls`, `.xdv`, …)

**Examples** under `lop12/` (`.tex` + `.pdf` only) may be committed on the test/demo branch. `others/` stays ignored.

Regenerate anytime with the exam CLI; overwrite these snapshots when the sample should change.
