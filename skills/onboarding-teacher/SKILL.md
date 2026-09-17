---
name: onboarding-teacher
description: Use when the teacher is new to this repo, profile.yaml completed is not true, exam-types or question-bank are empty, or they mention gia sư, dạy thêm, giáo viên trường, onboarding, chọn cách làm việc, or “làm lại cấu trúc”.
---

# Onboarding teacher

Read [src/docs/onboarding.md](../../src/docs/onboarding.md). Run that menu in Vietnamese. Do not assume they are a school teacher.

Skip if `src/configs/profile.yaml` has `completed: true`, unless they ask to redo.

Do **not** create 15-phut / giua-ki / thpt-qg YAML or `lop10/` folders unless they chose those options.

Every menu item has **Khác**: they may describe in words **or** paste LaTeX. Map paste to the right layer (`exam.cls` header/page, `papers/` exam shape, `items/` one-question UI). Do not invent the rest.

Four-choice MCQ is a **2×2 grid** by default (`\choicegrid` / `fourchoices` in `exam.cls`).

After they choose question formats, ask how to compose them for **all** product types: a default composition for selected exam types, decide on each generation, or Khác. Ask counts per format only for exam types with a requested default. Do not special-case graduation exams.

Do not ask the teacher to choose JSONL versus `.tex`, skills, or scripts.

After choices: write `profile.yaml` (including `composition_mode`), header yaml, only the exam-type files they named, and empty bank folders that match the layout. Store any default composition with its exam-type config; do not infer it from the exam-type name. Apply any Khác LaTeX they pasted.

Summarize in chat, then mention once that they may send text, images, or LaTeX; geometry, variation tables, and long solutions are supported and the agent will choose suitable storage.
