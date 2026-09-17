---
name: generating-exam
description: Use when the teacher wants a đề thi, phiếu bài tập, đáp án, or mixed-difficulty exam after onboarding (or when they name a loại đề).
---

# Generating an exam

If `src/configs/profile.yaml` is not `completed: true`, run `onboarding-teacher` first.

`--loai-de` must be a file that **exists** in `src/configs/exam-types/`. If they name a new type, write the YAML (see onboarding §2) then generate.

```bash
python3 src/scripts/generate/generate_exam.py \
  --lop 12 \
  --loai-de <slug> \
  --mode ca-hai \
  --output-name de-a \
  --seed 42
```

Chat can override `--so-cau`, `--ty-le`, `--thoi-gian`, `--tieu-de`, `--chuong`.

Output: `src/output/…`. If the bank is empty or too small, say so and ingest questions — do not invent a full đề from nothing.
