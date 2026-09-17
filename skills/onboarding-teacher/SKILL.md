---
name: onboarding-teacher
description: Use when the teacher is new to this repo, profile.yaml completed is not true, exam-types or question-bank are empty, or they mention gia sư, dạy thêm, giáo viên trường, onboarding, chọn cách làm việc, or “làm lại cấu trúc”.
---

# Onboarding teacher

Read [src/docs/onboarding.md](../../src/docs/onboarding.md). Run that menu in Vietnamese. Do not assume they are a school teacher.

Skip if `src/configs/profile.yaml` has `completed: true`, unless they ask to redo.

Do **not** create 15-phut / giua-ki / thpt-qg YAML or `lop10/` folders unless they chose those options.

After choices: write `profile.yaml`, header yaml, only the exam-type files they named, empty bank folders that match the layout. Summarize in chat.
