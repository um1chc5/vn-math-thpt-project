# Question JSONL (gợi ý)

Cây folder **không cố định** — chọn ở [onboarding.md](onboarding.md) §3. File có thể là `lop12/….jsonl`, `chuyen-de/….jsonl`, hoặc một `bank.jsonl`.

Một dòng = một object. Field gợi ý (thêm/bớt sau onboarding):

| Field | Gợi ý |
|-------|--------|
| `id` | Unique |
| `lop` | `10` \| `11` \| `12` nếu còn chia khối |
| `chuong` / `chuyen_de` / `tag` | Tùy layout đã chọn |
| `muc_do` | Theo scheme onboarding (§4), không bắt buộc 4 bậc nhà trường |
| `dang_bai` | Dạng trong chuyên đề, vd. `tính đạo hàm hàm hợp` |
| `kieu_cau` | `tu-luan` \| `trac-nghiem` \| `dung-sai` \| `tra-loi-ngan` nếu dùng |
| `choices` | List đáp án TN |
| `question_latex` | Đề |
| `answer_latex` | Đáp án |
| `loi_giai_latex` | Lời giải (tách khỏi đáp án) |

```json
{"id": "10-HS2-001", "lop": "10", "chuong": "Hàm số bậc hai", "muc_do": "nhan_biet", "dang_bai": "tìm đỉnh parabol", "question_latex": "Cho hàm số $y = x^2 - 2x - 3$. Tìm tọa độ đỉnh của parabol $(P)$.", "answer_latex": "$(1; -4)$", "loi_giai_latex": "Đỉnh $I\\left(-\\dfrac{b}{2a}; -\\dfrac{\\Delta}{4a}\\right) = (1; -4)$."}
```

Một dòng trong file. Backslash LaTeX phải `\\` vì đây là JSON.

Nếu layout là theo chương GDPT 2018, slug `--chuong` thường gặp: `menh-de-tap-hop`, `ham-so-bac-hai`, `he-thuc-luong`, `vecto`, `thong-ke-xac-suat`, `phuong-phap-toa-do` (10); `ham-so-luong-giac`, `day-so-cap-so`, `gioi-han-ham-lien-tuc`, `dao-ham`, `quan-he-vuong-goc`, `to-hop-xac-suat` (11); `ung-dung-dao-ham`, `ham-so-mu-logarit`, `nguyen-ham-tich-phan`, `so-phuc`, `khoi-da-dien`, `mat-non-mat-tru-mat-cau`, `phuong-phap-toa-do-khong-gian` (12).

Macros: `src/templates/math-macros.sty` (`\vect`, `\comb`, `\degree`, …).
