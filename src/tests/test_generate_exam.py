"""Tests for exam generation: bank loading, ma trận tỉ lệ, and TeX rendering."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import generate_exam as ge  # noqa: E402


def _q(**kwargs) -> dict:
    base = {
        "id": "10-TEST-001",
        "lop": "10",
        "chuong": "Hàm số bậc hai",
        "muc_do": "nhan_biet",
        "dang_bai": "tìm đỉnh parabol",
        "question_latex": "Câu hỏi $x^2$.",
        "answer_latex": "$S = (1; -4)$.",
        "loi_giai_latex": "Lời giải mẫu.",
    }
    base.update(kwargs)
    return base


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


@pytest.fixture
def bank(tmp_path: Path) -> Path:
    _write_jsonl(
        tmp_path / "lop10" / "ham-so-bac-hai.jsonl",
        [
            _q(id="10-HS2-001", muc_do="nhan_biet", dang_bai="đỉnh"),
            _q(id="10-HS2-002", muc_do="thong_hieu", dang_bai="trục đối xứng"),
            _q(id="10-HS2-003", muc_do="van_dung", dang_bai="bất phương trình"),
            _q(id="10-HS2-004", muc_do="van_dung_cao", dang_bai="cực trị hình học"),
        ],
    )
    _write_jsonl(
        tmp_path / "lop10" / "vecto.jsonl",
        [
            _q(
                id="10-VT-001",
                chuong="Vectơ",
                muc_do="nhan_biet",
                dang_bai="tổng vectơ",
                question_latex="Câu vectơ.",
            ),
            _q(
                id="10-VT-002",
                chuong="Vectơ",
                muc_do="thong_hieu",
                dang_bai="tích vô hướng",
            ),
        ],
    )
    _write_jsonl(
        tmp_path / "lop11" / "dao-ham.jsonl",
        [
            _q(id="11-DH-001", lop="11", chuong="Đạo hàm", muc_do="nhan_biet"),
        ],
    )
    return tmp_path


def test_load_questions_filters_by_lop(bank: Path) -> None:
    qs = ge.load_questions(bank, "10")
    assert {q["id"] for q in qs} == {
        "10-HS2-001",
        "10-HS2-002",
        "10-HS2-003",
        "10-HS2-004",
        "10-VT-001",
        "10-VT-002",
    }


def test_load_questions_filters_by_chuong_slug(bank: Path) -> None:
    qs = ge.load_questions(bank, "10", chuong_filters=["vecto"])
    assert {q["id"] for q in qs} == {"10-VT-001", "10-VT-002"}


def test_load_questions_filters_by_vietnamese_chapter_name(bank: Path) -> None:
    qs = ge.load_questions(bank, "10", chuong_filters=["Hàm số bậc hai"])
    assert {q["id"] for q in qs} == {
        "10-HS2-001",
        "10-HS2-002",
        "10-HS2-003",
        "10-HS2-004",
    }


def test_filter_muc_do() -> None:
    qs = [
        _q(id="a", muc_do="nhan_biet"),
        _q(id="b", muc_do="van_dung"),
        _q(id="c", muc_do="thong_hieu"),
    ]
    out = ge.filter_muc_do(qs, ["nhan_biet", "thong_hieu"])
    assert [q["id"] for q in out] == ["a", "c"]


def test_parse_ty_le_typical_matrix() -> None:
    assert ge.parse_ty_le("40:30:20:10") == (40, 30, 20, 10)


def test_parse_ty_le_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        ge.parse_ty_le("40:30:20")
    with pytest.raises(ValueError):
        ge.parse_ty_le("0:0:0:0")


def test_allocate_counts_largest_remainder() -> None:
    counts = ge.allocate_counts(10, (40, 30, 20, 10))
    assert counts == {
        "nhan_biet": 4,
        "thong_hieu": 3,
        "van_dung": 2,
        "van_dung_cao": 1,
    }
    assert sum(counts.values()) == 10


def test_select_questions_respects_ty_le_and_seed(bank: Path) -> None:
    qs = ge.load_questions(bank, "10", chuong_filters=["ham-so-bac-hai"])
    selected = ge.select_questions(qs, so_cau=4, seed=42, ty_le=(1, 1, 1, 1))
    assert [q["muc_do"] for q in selected] == list(ge.MUC_DO_ORDER)
    again = ge.select_questions(qs, so_cau=4, seed=42, ty_le=(1, 1, 1, 1))
    assert [q["id"] for q in again] == [q["id"] for q in selected]


def test_select_questions_seed_is_reproducible(bank: Path) -> None:
    qs = ge.load_questions(bank, "10")
    a = [q["id"] for q in ge.select_questions(qs, so_cau=3, seed=7)]
    b = [q["id"] for q in ge.select_questions(qs, so_cau=3, seed=7)]
    c = [q["id"] for q in ge.select_questions(qs, so_cau=3, seed=8)]
    assert a == b
    assert a != c


def test_select_questions_raises_when_bank_too_small(bank: Path) -> None:
    qs = ge.load_questions(bank, "10", chuong_filters=["vecto"])
    with pytest.raises(ValueError, match="Không đủ câu"):
        ge.select_questions(qs, so_cau=10)


def test_render_exam_tex_de_thi_omits_answers(tmp_path: Path) -> None:
    templates = tmp_path / "templates"
    templates.mkdir()
    # Point renderer at real project templates via copy of exam.tex.j2
    src = Path(__file__).resolve().parents[1] / "templates" / "exam.tex.j2"
    templates.joinpath("exam.tex.j2").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    tex = ge.render_exam_tex(
        [_q(question_latex="Tìm đỉnh parabol.", answer_latex="BÍ MẬT", loi_giai_latex="CHE GIẤU")],
        templates,
        meta={
            "school": "TRƯỜNG THPT ABC",
            "department": "SỞ GD\\&ĐT HÀ NỘI",
            "examtitle": "ĐỀ KIỂM TRA GIỮA KỲ I",
            "subject": "Toán",
            "grade": "10",
            "duration": "90 phút",
            "examdate": "17/09/2026",
            "answerkey": False,
        },
        show_answers=False,
        show_solutions=False,
    )
    assert r"\documentclass{exam}" in tex
    assert "Tìm đỉnh parabol." in tex
    assert "BÍ MẬT" not in tex
    assert "CHE GIẤU" not in tex
    assert r"\answerkeyfalse" in tex
    assert "TRƯỜNG THPT ABC" in tex


def test_render_exam_tex_dap_an_includes_solution(tmp_path: Path) -> None:
    templates = tmp_path / "templates"
    templates.mkdir()
    src = Path(__file__).resolve().parents[1] / "templates" / "exam.tex.j2"
    templates.joinpath("exam.tex.j2").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    tex = ge.render_exam_tex(
        [_q(answer_latex="ĐÁP ÁN X", loi_giai_latex="LỜI GIẢI Y")],
        templates,
        meta={
            "school": "TRƯỜNG THPT ABC",
            "department": "SỞ GD\\&ĐT HÀ NỘI",
            "examtitle": "ĐÁP ÁN",
            "subject": "Toán",
            "grade": "10",
            "duration": "90 phút",
            "examdate": "17/09/2026",
            "answerkey": True,
        },
        show_answers=True,
        show_solutions=True,
    )
    assert "ĐÁP ÁN X" in tex
    assert "LỜI GIẢI Y" in tex
    assert r"\answerkeytrue" in tex


def test_output_dir_for_nests_by_class_and_exam_type(tmp_path: Path) -> None:
    p = ge.output_dir_for(tmp_path, "12", "giua-ki", "de-a", when=date(2026, 9, 17))
    assert p == tmp_path / "src" / "output" / "lop12" / "giua-ki" / "2026-09-17-de-a"


def test_load_exam_type_reads_yaml(tmp_path: Path) -> None:
    folder = tmp_path / "src" / "configs" / "exam-types"
    folder.mkdir(parents=True)
    folder.joinpath("giua-ki.yaml").write_text(
        "id: giua-ki\nso_cau: 10\nty_le: '40:30:20:10'\npaper: papers/exam.tex.j2\n",
        encoding="utf-8",
    )
    profile = ge.load_exam_type(tmp_path, "giua-ki")
    assert profile["so_cau"] == 10
    assert profile["ty_le"] == "40:30:20:10"
    assert "papers/" in profile["paper"]


def test_load_exam_type_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        ge.load_exam_type(tmp_path, "giua-ki")


def test_prepare_questions_sets_item_style() -> None:
    rows = ge.prepare_questions(
        [_q(kieu_cau="trac_nghiem"), _q()],
        item_style="tu-luan",
    )
    assert rows[0]["_item"] == "trac-nghiem"
    assert rows[1]["_item"] == "tu-luan"
