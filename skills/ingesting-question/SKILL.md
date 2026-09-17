---
name: ingesting-question
description: Use when the teacher adds or fixes questions via chat, photo, PDF/Word paste, SGK scan, or typed LaTeX; or mentions ngân hàng, jsonl, muc_do, dang_bai, lời giải.
---

# Ingesting a question

## Hint what they can send

- Ảnh đề / SGK / vở (bạn đọc và gõ LaTeX)
- Văn bản copy từ Word
- Câu đã gõ (kể cả không có `$...$`)
- Đáp án + lời giải nếu có; nếu không, soạn lời giải rồi hỏi họ duyệt

Always capture: `lop`, `chuong`, `muc_do`, `dang_bai`. Guess `muc_do` from the 4 official tiers, then confirm.

## Write

Write JSONL under the bank layout from onboarding (`src/question-bank/…`). Schema: [docs/question-bank.md](../../src/docs/question-bank.md).

Optional: `kieu_cau` = `tu-luan` | `trac-nghiem` | `dung-sai` | `tra-loi-ngan`. MCQ may include `choices`.

`question_latex` may include TikZ, variation tables, tabular data, or `\includegraphics`. The agent may author these directly. Keep related image assets with the selected bank layout.

Use authentic THPT Vietnamese, not translated English. Escape LaTeX backslashes in JSON.

Show the teacher the stem + đáp án in chat before appending when the source was a photo (OCR can lie) or the agent supplied substantive missing content. After PDF review, save accepted corrections back to this bank entry.
