# vn-math-thpt-project

Sinh đề Toán THPT → XeLaTeX PDF. Teachers work in **chat**; agents follow [AGENTS.md](AGENTS.md).

**Start here:** [src/docs/onboarding.md](src/docs/onboarding.md) — chọn vai trò (giáo viên trường / gia sư / cả hai), loại đề, cây ngân hàng. `exam-types/` và `question-bank/` bắt đầu **trống**.

Jinja fills `.tex`; it does not make HTML. [src/docs/how-it-works.md](src/docs/how-it-works.md)

## Setup

[src/docs/setup/](src/docs/setup/README.md). Or tell the agent: “cài giúp TeX”.

```bash
python3 -m pip install -r requirements.txt
```

## Chat

Lần đầu: “Mình là giáo viên trường / gia sư, …” — agent chạy onboarding.  
Sau đó: “Ra đề …” — PDF trong `src/output/`.

## CLI (after onboarding created a loại đề)

```bash
python3 src/scripts/generate_exam.py \
  --lop 12 \
  --loai-de <slug-da-tao> \
  --mode ca-hai \
  --output-name de-a
```

`--mode`: `de-thi` | `dap-an` | `ca-hai`

## Layout

```
src/docs/            guides + onboarding
src/configs/         profile.yaml, school.yaml, exam-types/ (empty until chosen)
src/question-bank/   empty until onboarding
src/templates/       exam.cls, papers, items
src/scripts/
src/tests/
src/output/
```
