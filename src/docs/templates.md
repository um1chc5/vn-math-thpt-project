# Template layers

Keep `exam.cls` and `math-macros.sty` at `src/templates/` (XeLaTeX finds them via `TEXINPUTS`).

| Layer | Path | Job |
|-------|------|-----|
| Page / header | `src/templates/exam.cls` | School header, `\question`, answer-key toggle, fonts |
| Math shortcuts | `src/templates/math-macros.sty` | `\vect`, `\comb`, intervals, … |
| Paper (whole đề) | `src/templates/papers/*.tex.j2` | Title block + which sections exist |
| Item (one question) | `src/templates/items/*.tex.j2` | Tự luận / trắc nghiệm / đúng-sai / trả lời ngắn. TN 4 đáp án: lưới 2×2 mặc định (`\choicegrid`) |
| Legacy wrapper | `src/templates/exam.tex.j2` | Same as simple paper; tests and old calls |

Add a new **paper** when the exam *shape* changes (THPT QG 3 phần vs one list).  
Add a new **item** when the *question UI* changes (MCQ vs short answer).  
Do not fork `exam.cls` for that — only if the header/page geometry itself changes (e.g. two-column).

Onboarding **Khác** may paste LaTeX into these layers; keep 4-choice answers as a 2×2 grid unless they ask otherwise.

## Agent-authored LaTeX and helper scripts

Complex questions may include TikZ geometry, variation tables, custom tables, or external images directly in `question_latex`. Prefer storing that LaTeX with the question so it can be reused.

Create a helper under `src/scripts/` only when the operation is repeatable (for example, generating a family of diagrams or importing many questions). For a one-off question, write the LaTeX directly instead of adding a one-use script.

After PDF review, fix the owning source and regenerate:

- question content or diagram → question bank;
- paper/item appearance → templates;
- exam composition → exam-type config or generator.
