---
name: generating-exam
description: Use when the teacher wants a đề thi, phiếu bài tập, đáp án, or mixed-difficulty exam after onboarding (or when they name a loại đề).
---

# Generating an exam

If `src/configs/profile.yaml` is not `completed: true`, run `onboarding-teacher` first.

`--loai-de` must be a file that **exists** in `src/configs/exam-types/`. If they name a new type, write the YAML (see onboarding §2) then generate.

```bash
python3 src/scripts/generate_exam.py \
  --lop 12 \
  --loai-de <slug> \
  --mode ca-hai \
  --output-name de-a \
  --seed 42
```

Chat can override `--so-cau`, `--ty-le`, `--thoi-gian`, `--tieu-de`, `--chuong`.

Any exam type may mix `trac-nghiem`, `dung-sai`, `tra-loi-ngan`, and `tu-luan`. Read its saved default composition when present. If `profile.yaml` has `composition_mode: moi-lan`, or no default exists, ask for counts per format before generating. Never infer composition from names such as `thpt-qg`, `phieu-buoi`, or `giua-ki`.

If the current generator cannot enforce the requested composition, explain that briefly and add reusable config/generator support or assemble the requested paper directly. Do not silently approximate the mix.

Output: `src/output/…`. If the bank is empty or too small, tell the teacher and ask whether to add questions, reduce the requested count, or have the agent draft the missing questions. Do not silently invent a full đề.

After the teacher reviews the PDF, apply accepted fixes to their owning source (question bank, config, or template) and regenerate. Treat generated `.tex` as output, not the durable source.

The agent may write rich LaTeX directly for complex questions. Add a helper script only for a repeatable operation, not for one-off exam content.
