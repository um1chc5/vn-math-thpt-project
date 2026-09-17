#!/usr/bin/env python3
"""Sinh đề thi Toán THPT từ ngân hàng câu hỏi (chương trình GDPT 2018)."""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import subprocess
import sys
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

MUC_DO_ORDER = ("nhan_biet", "thong_hieu", "van_dung", "van_dung_cao")

CHUONG_CATALOG: dict[str, dict[str, str]] = {
    "10": {
        "menh-de-tap-hop": "Mệnh đề và tập hợp",
        "ham-so-bac-hai": "Hàm số bậc hai",
        "he-thuc-luong": "Hệ thức lượng trong tam giác",
        "vecto": "Vectơ",
        "thong-ke-xac-suat": "Thống kê và xác suất",
        "phuong-phap-toa-do": "Phương pháp tọa độ trong mặt phẳng",
    },
    "11": {
        "ham-so-luong-giac": "Hàm số lượng giác",
        "day-so-cap-so": "Dãy số. Cấp số cộng và cấp số nhân",
        "gioi-han-ham-lien-tuc": "Giới hạn và hàm số liên tục",
        "dao-ham": "Đạo hàm",
        "quan-he-vuong-goc": "Quan hệ vuông góc trong không gian",
        "to-hop-xac-suat": "Tổ hợp và xác suất",
    },
    "12": {
        "ung-dung-dao-ham": "Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số",
        "ham-so-mu-logarit": "Hàm số mũ và hàm số lôgarit",
        "nguyen-ham-tich-phan": "Nguyên hàm và tích phân",
        "so-phuc": "Số phức",
        "khoi-da-dien": "Khối đa diện",
        "mat-non-mat-tru-mat-cau": "Mặt nón, mặt trụ, mặt cầu",
        "phuong-phap-toa-do-khong-gian": "Phương pháp tọa độ trong không gian",
    },
}

MUC_DO_LABELS = {
    "nhan_biet": "Nhận biết",
    "thong_hieu": "Thông hiểu",
    "van_dung": "Vận dụng",
    "van_dung_cao": "Vận dụng cao",
}


def project_root() -> Path:
    # src/scripts/generate_exam.py → repo root
    return Path(__file__).resolve().parent.parent.parent


def src_dir(root: Path | None = None) -> Path:
    return (root or project_root()) / "src"


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip()


def _norm(s: str) -> str:
    return _nfc(s).casefold()


def _chuong_identity(lop: str, source_stem: str, chuong_name: str) -> set[str]:
    identity = {_norm(source_stem), _norm(chuong_name)}
    catalog = CHUONG_CATALOG.get(str(lop), {})
    if source_stem in catalog:
        identity.add(_norm(catalog[source_stem]))
        identity.add(_norm(source_stem))
    for slug, name in catalog.items():
        if _norm(name) == _norm(chuong_name) or _norm(slug) == _norm(source_stem):
            identity.add(_norm(slug))
            identity.add(_norm(name))
    return identity


def _matches_chuong(lop: str, source_stem: str, chuong_name: str, filters: list[str]) -> bool:
    identity = _chuong_identity(lop, source_stem, chuong_name)
    return any(_norm(f) in identity for f in filters)


def load_questions(
    bank_dir: Path,
    lop: str,
    chuong_filters: list[str] | None = None,
) -> list[dict]:
    lop_dir = bank_dir / f"lop{lop}"
    if not lop_dir.is_dir():
        raise FileNotFoundError(f"Không tìm thấy ngân hàng lớp {lop}: {lop_dir}")

    questions: list[dict] = []
    for path in sorted(lop_dir.glob("*.jsonl")):
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSONL lỗi tại {path.name}:{lineno}: {exc}") from exc
            item["_source"] = path.stem
            if chuong_filters and not _matches_chuong(
                str(item.get("lop", lop)),
                path.stem,
                str(item.get("chuong", "")),
                chuong_filters,
            ):
                continue
            questions.append(item)
    return questions


def filter_muc_do(questions: list[dict], muc_do: list[str] | None) -> list[dict]:
    if not muc_do:
        return list(questions)
    allowed = {_norm(m) for m in muc_do}
    return [q for q in questions if _norm(str(q.get("muc_do", ""))) in allowed]


def parse_ty_le(text: str) -> tuple[int, int, int, int]:
    parts = [p.strip() for p in text.split(":")]
    if len(parts) != 4:
        raise ValueError('Tỉ lệ phải có dạng "NB:TH:VD:VDC", ví dụ "40:30:20:10".')
    try:
        vals = tuple(int(p) for p in parts)
    except ValueError as exc:
        raise ValueError("Tỉ lệ ma trận phải là bốn số nguyên.") from exc
    if any(v < 0 for v in vals) or sum(vals) == 0:
        raise ValueError("Tỉ lệ ma trận phải gồm số không âm và tổng > 0.")
    return vals  # type: ignore[return-value]


def allocate_counts(n: int, ratios: tuple[int, int, int, int]) -> dict[str, int]:
    total = sum(ratios)
    raw = [n * r / total for r in ratios]
    floors = [math.floor(x) for x in raw]
    remainder = n - sum(floors)
    order = sorted(
        range(4),
        key=lambda i: (raw[i] - floors[i], -i),
        reverse=True,
    )
    for i in range(remainder):
        floors[order[i]] += 1
    return dict(zip(MUC_DO_ORDER, floors))


def select_questions(
    questions: list[dict],
    so_cau: int,
    seed: int | None = None,
    ty_le: tuple[int, int, int, int] | None = None,
    muc_do_filter: list[str] | None = None,
) -> list[dict]:
    pool = filter_muc_do(questions, muc_do_filter)
    if so_cau < 1:
        raise ValueError("--so-cau phải là số nguyên dương.")
    if so_cau > len(pool):
        raise ValueError(f"Không đủ câu hỏi trong ngân hàng (cần {so_cau}, có {len(pool)}).")

    rng = random.Random(seed)

    if ty_le is None:
        picked = rng.sample(pool, so_cau)
        return picked

    counts = allocate_counts(so_cau, ty_le)
    by_md: dict[str, list[dict]] = defaultdict(list)
    for q in pool:
        by_md[str(q.get("muc_do", ""))].append(q)
    for bucket in by_md.values():
        rng.shuffle(bucket)

    selected: list[dict] = []
    leftover: list[dict] = []
    shortfall = 0
    for md in MUC_DO_ORDER:
        need = counts[md]
        bucket = by_md.get(md, [])
        take = min(need, len(bucket))
        selected.extend(bucket[:take])
        leftover.extend(bucket[take:])
        shortfall += need - take

    extra_md = [md for md in by_md if md not in MUC_DO_ORDER]
    for md in extra_md:
        leftover.extend(by_md[md])

    rng.shuffle(leftover)
    if shortfall > 0:
        if len(leftover) < shortfall:
            raise ValueError(
                f"Không đủ câu hỏi trong ngân hàng (cần {so_cau}, "
                f"sau khi phân bổ ma trận còn thiếu {shortfall - len(leftover)})."
            )
        selected.extend(leftover[:shortfall])

    selected.sort(key=lambda q: MUC_DO_ORDER.index(q["muc_do"]) if q.get("muc_do") in MUC_DO_ORDER else 99)
    return selected


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("Cần PyYAML. Chạy: pip install -r requirements.txt")
    if not path.is_file():
        raise FileNotFoundError(f"Không thấy file cấu hình: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_school(root: Path) -> dict:
    path = src_dir(root) / "configs" / "school.yaml"
    return load_yaml(path) if path.is_file() else {}


def load_tutor(root: Path) -> dict:
    path = src_dir(root) / "configs" / "tutor.yaml"
    return load_yaml(path) if path.is_file() else {}


def _nonempty(*vals: object, default: str = "") -> str:
    for v in vals:
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return default


def load_exam_type(root: Path, loai_de: str) -> dict:
    path = src_dir(root) / "configs" / "exam-types" / f"{loai_de}.yaml"
    return load_yaml(path)


def topic_label(questions: list[dict]) -> str:
    names: list[str] = []
    seen: set[str] = set()
    for q in questions:
        name = _nfc(str(q.get("chuong") or q.get("chuyen_de") or ""))
        key = _norm(name)
        if name and key not in seen:
            seen.add(key)
            names.append(name)
    return "; ".join(names)


def output_dir_for(
    root: Path,
    lop: str,
    loai_de: str | None,
    output_name: str,
    when: date | None = None,
) -> Path:
    day = (when or date.today()).strftime("%Y-%m-%d")
    kind = loai_de or "khac"
    return src_dir(root) / "output" / f"lop{lop}" / kind / f"{day}-{output_name}"


def _normalize_item_style(value: str | None, fallback: str = "tu-luan") -> str:
    raw = (value or fallback).strip().replace("_", "-")
    allowed = {"tu-luan", "trac-nghiem", "dung-sai", "tra-loi-ngan"}
    return raw if raw in allowed else fallback


def prepare_questions(questions: list[dict], item_style: str = "tu-luan") -> list[dict]:
    prepared = []
    for q in questions:
        row = dict(q)
        row["_item"] = _normalize_item_style(row.get("kieu_cau"), item_style)
        prepared.append(row)
    return prepared


def resolve_paper_template(template_dir: Path, paper: str | None) -> str:
    if paper:
        return paper
    if (template_dir / "papers" / "exam.tex.j2").is_file():
        return "papers/exam.tex.j2"
    return "exam.tex.j2"


def render_exam_tex(
    questions: list[dict],
    template_dir: Path,
    meta: dict,
    show_answers: bool,
    show_solutions: bool,
) -> str:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    item_style = _normalize_item_style(meta.get("item_style"))
    prepared = prepare_questions(questions, item_style)
    template_name = resolve_paper_template(template_dir, meta.get("paper"))
    if template_name.endswith("thpt-qg.tex.j2"):
        order = {"trac-nghiem": 0, "dung-sai": 1, "tra-loi-ngan": 2, "tu-luan": 3}
        prepared.sort(key=lambda q: order.get(q["_item"], 9))
    template = env.get_template(template_name)
    return template.render(
        questions=prepared,
        show_answers=show_answers,
        show_solutions=show_solutions,
        item_style=item_style,
        **{k: v for k, v in meta.items() if k not in {"paper", "item_style"}},
    )


def compile_tex(tex_path: Path, templates_dir: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    texinputs = str(templates_dir.resolve()) + "//:" + env.get("TEXINPUTS", "")
    env["TEXINPUTS"] = texinputs
    cmd = [
        "latexmk",
        "-xelatex",
        "-interaction=nonstopmode",
        "-file-line-error",
        f"-outdir={out_dir}",
        str(tex_path),
    ]
    try:
        subprocess.run(cmd, check=True, env=env, cwd=str(out_dir))
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "Không tìm thấy latexmk. Cài TeX Live / MacTeX rồi chạy lại, "
            f"hoặc biên dịch thủ công file {tex_path}."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"latexmk thất bại (mã {exc.returncode}). Xem log trong {out_dir}.") from exc

    pdf = out_dir / f"{tex_path.stem}.pdf"
    if not pdf.is_file():
        raise RuntimeError(f"Không thấy PDF sau khi biên dịch: {pdf}")
    return pdf


def _escape_meta(text: str) -> str:
    return text.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%")


def _today() -> str:
    return date.today().strftime("%d/%m/%Y")


def write_and_maybe_compile(
    questions: list[dict],
    root: Path,
    output_name: str,
    meta: dict,
    show_answers: bool,
    show_solutions: bool,
    do_compile: bool,
    out_dir: Path | None = None,
) -> Path:
    dest = out_dir if out_dir is not None else src_dir(root) / "output"
    dest.mkdir(parents=True, exist_ok=True)
    tex_path = dest / f"{output_name}.tex"
    tex = render_exam_tex(
        questions,
        src_dir(root) / "templates",
        meta,
        show_answers=show_answers,
        show_solutions=show_solutions,
    )
    tex_path.write_text(tex, encoding="utf-8")
    if do_compile:
        compile_tex(tex_path, src_dir(root) / "templates", dest)
    return tex_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sinh đề thi Toán THPT (GDPT 2018) từ ngân hàng JSONL."
    )
    parser.add_argument("--lop", required=True, choices=["10", "11", "12"], help="Khối lớp")
    parser.add_argument(
        "--chuong",
        nargs="+",
        default=None,
        help="Slug hoặc tên chương (có thể chọn nhiều). Mặc định: mọi chương của lớp.",
    )
    parser.add_argument(
        "--muc-do",
        nargs="+",
        dest="muc_do",
        choices=list(MUC_DO_ORDER),
        default=None,
        help="Lọc mức độ: nhan_biet thong_hieu van_dung van_dung_cao",
    )
    parser.add_argument(
        "--so-cau",
        type=int,
        default=None,
        dest="so_cau",
        help="Số câu. Bỏ trống nếu --loai-de đã có so_cau.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Seed để tái lập đề")
    parser.add_argument("--output-name", dest="output_name", default="de-thi", help="Tên file trong thư mục output")
    parser.add_argument(
        "--loai-de",
        dest="loai_de",
        default=None,
        help="Profile YAML trong src/configs/exam-types/ (slug do onboarding tạo)",
    )
    parser.add_argument(
        "--mode",
        choices=["de-thi", "dap-an", "ca-hai"],
        default="de-thi",
        help="de-thi | dap-an | ca-hai",
    )
    parser.add_argument(
        "--ty-le",
        dest="ty_le",
        default=None,
        help='Ma trận đề NB:TH:VD:VDC, ví dụ "40:30:20:10"',
    )
    parser.add_argument("--truong", default=None)
    parser.add_argument("--so-gd", dest="so_gd", default=None)
    parser.add_argument("--tieu-de", dest="tieu_de", default=None)
    parser.add_argument("--thoi-gian", dest="thoi_gian", default=None)
    parser.add_argument("--ngay", default=None, help="Ngày ghi trên đề (mặc định: hôm nay)")
    parser.add_argument("--mon", default=None)
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Chỉ sinh file .tex, không chạy latexmk",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = project_root()
    bank_dir = src_dir(root) / "question-bank"
    school = load_school(root)
    tutor = load_tutor(root)
    profile: dict = load_exam_type(root, args.loai_de) if args.loai_de else {}

    so_cau = args.so_cau if args.so_cau is not None else profile.get("so_cau")
    if not so_cau:
        raise ValueError("Cần --so-cau, hoặc --loai-de có trường so_cau.")

    ty_le_text = args.ty_le or profile.get("ty_le")
    ty_le = parse_ty_le(str(ty_le_text)) if ty_le_text else None
    tieu_de = args.tieu_de or profile.get("tieu_de") or "ĐỀ KIỂM TRA"
    thoi_gian = args.thoi_gian or profile.get("thoi_gian") or "90 phút"
    truong = _nonempty(args.truong, school.get("truong"))
    teacher = _nonempty(tutor.get("ho_ten_gv"), school.get("ho_ten_gv"))
    so_gd = _nonempty(args.so_gd, school.get("so_gd"))
    mon = _nonempty(args.mon, school.get("mon"), tutor.get("mon"), default="Toán")

    questions = load_questions(bank_dir, args.lop, args.chuong)
    selected = select_questions(
        questions,
        so_cau=int(so_cau),
        seed=args.seed,
        ty_le=ty_le,
        muc_do_filter=args.muc_do,
    )

    out_dir = output_dir_for(root, args.lop, args.loai_de, args.output_name)
    meta_base = {
        "school": _escape_meta(str(truong)),
        "department": _escape_meta(str(so_gd)),
        "teacher": _escape_meta(str(teacher)),
        "topic": _escape_meta(topic_label(selected)),
        "subject": _escape_meta(str(mon)),
        "grade": args.lop,
        "duration": _escape_meta(str(thoi_gian)),
        "examdate": _escape_meta(args.ngay or _today()),
        "paper": profile.get("paper"),
        "item_style": profile.get("item_style", "tu-luan"),
    }

    jobs: list[tuple[str, str, bool, bool]] = []
    if args.mode in {"de-thi", "ca-hai"}:
        jobs.append((args.output_name, tieu_de, False, False))
    if args.mode in {"dap-an", "ca-hai"}:
        name = args.output_name if args.mode == "dap-an" else f"{args.output_name}-dap-an"
        jobs.append((name, f"ĐÁP ÁN — {tieu_de}", True, True))

    do_compile = not args.no_compile
    written: list[Path] = []
    for name, title, show_ans, show_sol in jobs:
        meta = {
            **meta_base,
            "examtitle": _escape_meta(title),
            "answerkey": show_ans,
        }
        written.append(
            write_and_maybe_compile(
                selected,
                root,
                name,
                meta,
                show_answers=show_ans,
                show_solutions=show_sol,
                do_compile=do_compile,
                out_dir=out_dir,
            )
        )

    print(f"Thư mục: {out_dir}")
    for path in written:
        print(f"Đã ghi {path}")
        pdf = path.with_suffix(".pdf")
        if pdf.is_file():
            print(f"PDF: {pdf}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
