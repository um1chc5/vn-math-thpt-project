# Agent instructions (Cursor, Claude, Gemini, …)

Teacher works **in chat**. They look at the **PDF** (sometimes the `.tex`). Do not assume they can use a terminal.

**First session:** if `src/configs/profile.yaml` is not `completed: true`, run [src/docs/onboarding.md](src/docs/onboarding.md) (skill `onboarding-teacher`). They may be giáo viên trường, gia sư, or both — do not assume. Do not invent loại đề or bank folders they did not pick.

Read details only when needed:

- Onboarding menu: [src/docs/onboarding.md](src/docs/onboarding.md)
- Setup: [src/docs/setup/README.md](src/docs/setup/README.md)
- Pipeline: [src/docs/how-it-works.md](src/docs/how-it-works.md)
- Bank JSONL: [src/docs/question-bank.md](src/docs/question-bank.md)
- Exam-type folder (starts empty): [src/configs/exam-types/README.md](src/configs/exam-types/README.md)
- Template layers: [src/docs/templates.md](src/docs/templates.md)
- Chat after onboarding: [src/docs/chat-workflow.md](src/docs/chat-workflow.md)

Skills: [onboarding-teacher](skills/onboarding-teacher/SKILL.md), [checking-setup](skills/checking-setup/SKILL.md), [ingesting-question](skills/ingesting-question/SKILL.md), [generating-exam](skills/generating-exam/SKILL.md)

## Language

Speak Vietnamese with the teacher unless they write English. Keep questions short.

## Never dump a command and walk away

If TeX/Python is missing: **ask permission**, then run the install (`src/docs/setup/`). Same for `pip install -r requirements.txt` and `src/scripts/generate_exam.py`.

After a đề is built, reply with the **PDF path**. Show LaTeX only if they ask or compile failed.

## Output

Default: `src/output/…` (nesting follows onboarding / `--loai-de`). Do not hardcode 15-phut/giua-ki/thpt-qg.

## Do not invent coverage

Never pull every chapter of a grade unless they listed those chapters.
