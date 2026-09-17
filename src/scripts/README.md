# Scripts

Clean-code **ideas** — folder tree follows what the teacher actually needs, not a fixed layout.

## Principles

1. **Content stays in the bank** — one-off TikZ / tables / LaTeX → `question-bank/`. Add a script only if the same operation will run again.
2. **Grow by role, when crowded** — if `src/scripts/` is still a few files, a flat layout is fine. Split when a second tool of the same kind appears.
3. **Tests mirror scripts** — same role name under `src/tests/` when you do split.
4. **Stable project root** — use `_paths.py` (or walk up to `requirements.txt` + `src/configs/`). Do not hardcode `Path.parents[N]`.

## Predicted cases (create only when needed)

| When the teacher / agent needs… | Likely home |
|---------------------------------|-------------|
| Sinh đề → `.tex` / PDF | `generate/` (or keep `generate_exam.py` at top while alone) |
| Import đề ngoài (MyLT, Word, scan) → JSONL | `ingest/` |
| Batch figures / TikZ families | `diagrams/` |
| Shared path / IO helpers | `_paths.py`, later `lib/` |
| One-shot experiment | chat / local scratch — do **not** commit unless reused |

Exam packs (`question-bank/thpt/…`) and loại-đề YAML are **not** scripts; they are config + bank layout chosen in onboarding.

## Agent note

Do not invent empty folders “for later”. Prefer the smallest path that matches an existing case above. Details for CLI live in skills / `AGENTS.md`; this file is the structure policy only.
