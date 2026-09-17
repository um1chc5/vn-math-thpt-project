#!/usr/bin/env python3
"""Extract MyLT THPT 2025 sample into JSONL + figure TeX files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _paths import src_dir  # noqa: E402

SRC = Path("/home/um1chc/Downloads/MD 0105 - THPT 2025.tex")
PACK = src_dir() / "question-bank" / "thpt" / "md0105"
BANK = PACK
FIG = PACK / "figures"
OUT = PACK / "questions.jsonl"
FIG_INPUT_PREFIX = "thpt/md0105/figures"

PART_I_END = 12
PART_II_END = 16


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*?$", "", text, flags=re.M)


def split_ex_blocks(text: str) -> list[str]:
    return re.findall(r"\\begin\{ex\}.*?\\end\{ex\}", text, flags=re.S)


def parse_choice_braces(body: str, cmd: str) -> tuple[str, list[str]]:
    """Return (stem_before_cmd, list of brace groups after \\cmd)."""
    m = re.search(rf"\\{cmd}\b", body)
    if not m:
        return body.strip(), []
    stem = body[: m.start()].strip()
    rest = body[m.end() :]
    groups: list[str] = []
    i = 0
    while i < len(rest):
        while i < len(rest) and rest[i].isspace():
            i += 1
        if i >= len(rest) or rest[i] != "{":
            break
        depth = 0
        j = i
        while j < len(rest):
            if rest[j] == "{" and (j == 0 or rest[j - 1] != "\\"):
                depth += 1
            elif rest[j] == "}" and (j == 0 or rest[j - 1] != "\\"):
                depth -= 1
                if depth == 0:
                    groups.append(rest[i + 1 : j].strip())
                    i = j + 1
                    break
            j += 1
        else:
            break
    return stem, groups


def parse_immini(body: str) -> tuple[str, str | None]:
    m = re.search(r"\\immini\s*\{", body)
    if not m:
        return body.strip(), None
    # parse two top-level brace groups after \immini
    rest = body[m.end() - 1 :]  # starts at '{'
    groups: list[str] = []
    i = 0
    while i < len(rest) and len(groups) < 2:
        while i < len(rest) and rest[i].isspace():
            i += 1
        if i >= len(rest) or rest[i] != "{":
            break
        depth = 0
        j = i
        while j < len(rest):
            ch = rest[j]
            if ch == "{" and (j == 0 or rest[j - 1] != "\\"):
                depth += 1
            elif ch == "}" and (j == 0 or rest[j - 1] != "\\"):
                depth -= 1
                if depth == 0:
                    groups.append(rest[i + 1 : j])
                    i = j + 1
                    break
            j += 1
        else:
            break
    if len(groups) != 2:
        return body.strip(), None
    return groups[0].strip(), groups[1].strip()


def guess_chuong(stem: str, kieu: str) -> str:
    s = stem.lower()
    rules = [
        ("tích phân", "Nguyên hàm và tích phân"),
        ("nguyên hàm", "Nguyên hàm và tích phân"),
        ("log", "Hàm số mũ và hàm số lôgarit"),
        ("tứ phân vị", "Các số đặc trưng của mẫu số liệu ghép nhóm"),
        ("tần số", "Các số đặc trưng của mẫu số liệu ghép nhóm"),
        ("oxyz", "Hình học Oxyz"),
        ("o x y z", "Hình học Oxyz"),
        ("vectơ pháp tuyến", "Hình học Oxyz"),
        ("chỉ phương", "Hình học Oxyz"),
        ("lăng trụ", "Vectơ trong không gian"),
        ("hình hộp", "Vectơ trong không gian"),
        ("hình chóp", "Quan hệ vuông góc"),
        ("tiệm cận", "Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số"),
        ("cấp số cộng", "Dãy số. Cấp số cộng và cấp số nhân"),
        ("sin x", "Hàm số lượng giác"),
        ("xác suất", "Xác suất có điều kiện"),
        ("tin nhắn", "Xác suất có điều kiện"),
        ("nồng độ", "Hàm số mũ và hàm số lôgarit"),
        ("đạo hàm", "Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số"),
        ("doanh thu", "Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số"),
        ("mật thư", "Tổ hợp và xác suất"),
        ("quyển sách", "Tổ hợp và xác suất"),
        ("thực đơn", "Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số"),
        ("chân đế", "Mặt nón, mặt trụ, mặt cầu"),
    ]
    for key, name in rules:
        if key in s:
            return name
    if kieu == "tra-loi-ngan":
        return "Tổng hợp luyện TN THPT"
    return "Tổng hợp luyện TN THPT"


def main() -> None:
    raw = strip_comments(SRC.read_text(encoding="utf-8"))
    # Keep only exam body before answer key page
    body = raw.split("\\label{mylt}")[0]
    blocks = split_ex_blocks(body)
    if len(blocks) < 22:
        raise SystemExit(f"Expected >=22 ex blocks, got {len(blocks)}")

    FIG.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for idx, block in enumerate(blocks[:22], start=1):
        inner = re.sub(r"^\\begin\{ex\}", "", block, count=1).strip()
        inner = re.sub(r"\\end\{ex\}\s*$", "", inner).strip()
        inner = re.sub(r"^%Câu[^\n]*\n?", "", inner).strip()

        if idx <= PART_I_END:
            kieu = "trac-nghiem"
        elif idx <= PART_II_END:
            kieu = "dung-sai"
        else:
            kieu = "tra-loi-ngan"

        fig = None
        stem_body = inner
        if "\\immini" in inner:
            stem_body, fig = parse_immini(inner)

        qid = f"12-MD0105-{idx:02d}"
        chuong = guess_chuong(stem_body, kieu)

        if fig:
            fig_path = FIG / f"{qid}.tex"
            fig_path.write_text(fig.strip() + "\n", encoding="utf-8")

        if kieu == "trac-nghiem":
            stem, choices = parse_choice_braces(stem_body, "choice")
            if fig:
                stem = (
                    stem
                    + "\n\n\\begin{center}\\input{"
                    + f"{FIG_INPUT_PREFIX}/{qid}.tex"
                    + "}\\end{center}"
                )
            row = {
                "id": qid,
                "lop": "12",
                "chuong": chuong,
                "muc_do": "nhan_biet" if idx <= 8 else "thong_hieu",
                "dang_bai": "tn-thpt-2025",
                "kieu_cau": kieu,
                "choices": choices,
                "question_latex": stem,
                "answer_latex": "",
                "loi_giai_latex": "",
                "tag": ["md0105", "thpt-2025"],
            }
        elif kieu == "dung-sai":
            stem, statements = parse_choice_braces(stem_body, "choiceTF")
            row = {
                "id": qid,
                "lop": "12",
                "chuong": chuong,
                "muc_do": "van_dung",
                "dang_bai": "dung-sai-thpt-2025",
                "kieu_cau": kieu,
                "statements": statements,
                "question_latex": stem,
                "answer_latex": "",
                "loi_giai_latex": "",
                "tag": ["md0105", "thpt-2025"],
            }
        else:
            stem = stem_body.strip()
            if fig:
                stem = (
                    stem
                    + "\n\n\\begin{center}\\input{"
                    + f"{FIG_INPUT_PREFIX}/{qid}.tex"
                    + "}\\end{center}"
                )
            row = {
                "id": qid,
                "lop": "12",
                "chuong": chuong,
                "muc_do": "van_dung_cao",
                "dang_bai": "tra-loi-ngan-thpt-2025",
                "kieu_cau": kieu,
                "question_latex": stem,
                "answer_latex": "",
                "loi_giai_latex": "",
                "tag": ["md0105", "thpt-2025"],
            }
        rows.append(row)

    OUT.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} questions -> {OUT}")
    print(f"Figures -> {FIG}")


if __name__ == "__main__":
    main()
