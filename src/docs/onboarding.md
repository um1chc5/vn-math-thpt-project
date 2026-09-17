# Onboarding — chọn cách làm việc

Repo này **chưa khóa** loại đề hay cây ngân hàng. Lần chat đầu, agent chạy menu dưới rồi **mới** tạo file YAML / folder. Thầy/cô chọn ý tưởng nào vừa dùng; không phải chọn hết.

Nếu `src/configs/profile.yaml` có `completed: true` thì bỏ qua bước này (trừ khi họ nói “làm lại onboarding”).

**Khác:** mọi câu đều có lựa chọn này. Họ có thể (1) mô tả bằng lời, hoặc (2) dán snippet LaTeX. Agent không bịa thêm loại đề / folder / header ngoài những gì họ đưa.

- Header / trang → ghi vào `src/templates/exam.cls` (và paper `.tex.j2` nếu cần)
- Hình dạng cả đề (1 list vs 3 phần) → `src/templates/papers/`
- Giao diện một câu → `src/templates/items/`

Trắc nghiệm 4 lựa chọn: **lưới 2×2 (A B / C D) mặc định**.

## 1. Bạn dạy ở đâu?

| | Vai trò | Thường cần |
|--|---------|------------|
| A | Giáo viên trường | Header Sở/trường/lớp, ma trận tổ chuyên môn, kiểm tra 15 phút → cuối kỳ, có khi luyện TN THPT |
| B | Gia sư / dạy thêm | Header tên GV hoặc tối giản, phiếu theo buổi, theo học sinh, không bắt buộc ma trận Sở |
| C | Cả hai | Hai bộ header hoặc một header đổi theo lần ra đề |
| D | Khác | Mô tả (trung tâm, online, soạn thuê, …) hoặc dán header LaTeX |

## 2. Loại sản phẩm (ý tưởng)

Không có file YAML sẵn. Chỉ tạo file cho loại **họ nói sẽ dùng**.

| Ý tưởng | Ai hay dùng | Gợi ý khi hỏi thêm |
|---------|-------------|-------------------|
| Kiểm tra 15 phút / 1 tiết | Trường | 1 bài vừa dạy? |
| Giữa kỳ / cuối kỳ | Trường | Danh sách chương do họ đưa, đừng đoán |
| Luyện tốt nghiệp THPT | Trường + gia sư | Có thể dùng cấu trúc chuẩn hiện hành hoặc tùy chỉnh như mọi loại đề khác |
| Phiếu bài tập theo buổi | Gia sư | Thời lượng buổi, sĩ số |
| Đề theo chuyên đề | Cả hai | Không theo lịch tuần của trường |
| Đề theo học sinh | Gia sư | Tên HS chỉ để đặt folder, không in trừ khi họ muốn |
| Khác | — | Đặt tên (`--loai-de` = slug) **hoặc** dán paper LaTeX / YAML loại đề |

Mỗi loại khi đã chọn → một file `src/configs/exam-types/<slug>.yaml` (số câu, thời gian, tỉ lệ nếu có). Template YAML tối thiểu:

```yaml
id: giua-ki          # slug, trùng tên file
label: Kiểm tra giữa kỳ
so_cau: 10
ty_le: "40:30:20:10" # bỏ nếu không dùng ma trận 4 bậc
thoi_gian: "90 phút"
tieu_de: "ĐỀ KIỂM TRA GIỮA KỲ"
paper: papers/exam.tex.j2
```

Nếu loại đề có cơ cấu mặc định, thêm `sections`:

```yaml
sections:
  - kieu_cau: trac-nghiem
    so_cau: 6
  - kieu_cau: tu-luan
    so_cau: 4
```

`sections` là mặc định có thể override theo từng lần sinh. Nếu generator hiện tại chưa đọc cấu hình này, agent phải điều chỉnh luồng sinh đề hoặc bổ sung hỗ trợ tái sử dụng; không được âm thầm bỏ qua cơ cấu.

## 3. Cây ngân hàng (ý tưởng)

Folder `src/question-bank/` để trống cho đến khi chọn.

| | Cách chia | Ví dụ path |
|--|-----------|------------|
| A | Theo chương GDPT 2018 | `lop12/ung-dung-dao-ham.jsonl` |
| B | Theo chuyên đề tự đặt | `chuyen-de/dao-ham-ham-hop.jsonl` |
| C | Theo học sinh / lớp dạy thêm | `gia-su/hs-minh/dao-ham.jsonl` |
| D | Ít file, lọc metadata | `bank.jsonl` (mọi câu, lọc `lop`/`chuong`/`tag`) |
| E | Hỗn hợp | Trường dùng A, gia sư thêm C |
| F | Khác | Mô tả cây folder **hoặc** dán path/schema họ muốn |

Schema một dòng JSON (gợi ý, thêm field nếu họ cần): xem [question-bank.md](question-bank.md).

## 4. Mức độ

| | Scheme | Khi nào |
|--|--------|---------|
| A | `nhan_biet` / `thong_hieu` / `van_dung` / `van_dung_cao` | Đề trường, ma trận |
| B | dễ / trung bình / khó | Gia sư, phiếu luyện |
| C | Không gắn mức độ | Ngân hàng nhỏ |
| D | Khác | Họ liệt kê nhãn **hoặc** dán field `muc_do` mẫu |

## 5. Header trang đề

Mặc định (gia sư / phiếu): tên bài + môn/lớp + chuyên đề + thời gian; tên GV chữ nhỏ dưới dòng Lớp. Sở/trường chỉ in nếu họ chọn A.

| | Style | Config |
|--|--------|--------|
| A | Sở + trường + lớp | `school.yaml`: `so_gd`, `truong` |
| B | Gia sư (tên GV, môn, buổi) | `tutor.yaml` / `school.yaml`: `ho_ten_gv` |
| C | Tối giản (chỉ môn + thời gian) | Để trống tên trường |
| D | Khác | Mô tả các dòng header **hoặc** dán LaTeX `\makeheader` / snippet `exam.cls` |

## 6. Dạng câu đang soạn

Tự luận · trắc nghiệm · đúng/sai · trả lời ngắn. Chỉ bật item template nào họ dùng (`src/templates/items/`).

| | Dạng |
|--|------|
| A | Trắc nghiệm 4 lựa chọn (lưới **2×2** mặc định) |
| B | Đúng / sai |
| C | Trả lời ngắn |
| D | Tự luận |
| E | Khác — mô tả layout hoặc dán item LaTeX (`items/*.tex.j2`) |

Sau khi chọn các dạng câu, hỏi **một lần** về cách phối cho mọi loại sản phẩm:

| | Cách phối dạng câu |
|--|--------------------|
| A | Có cấu trúc mặc định cho một hoặc nhiều loại đề |
| B | Quyết định mỗi lần sinh đề |
| C | Khác — mô tả quy tắc riêng |

Chỉ hỏi số câu từng dạng cho những loại đề mà họ muốn có cấu trúc mặc định. Nếu chọn B, để agent hỏi cơ cấu khi sinh từng đề. Không mặc định rằng chỉ đề tốt nghiệp THPT mới được trộn nhiều dạng câu.

---

## Agent: sau khi họ chọn

1. Ghi `src/configs/profile.yaml` (`completed: true` + các lựa chọn; `notes` nếu Khác).
2. Ghi header vào `school.yaml` / `tutor.yaml`. Nếu họ dán LaTeX header → cập nhật `exam.cls` (đừng bịa Sở/trường).
3. Tạo **chỉ** YAML loại đề họ chọn; đừng seed 15-phut/giua-ki/thpt-qg nếu họ không xin. Paper LaTeX Khác → file trong `papers/`.
4. Tạo cây folder ngân hàng đúng layout đã chọn (vẫn để trống file nếu chưa có câu).
5. Item Khác → chỉ sửa/thêm file trong `items/`. TN 4 đáp án giữ lưới 2×2 trừ khi họ xin khác.
6. Ghi cách phối dạng câu vào `profile.yaml` (`composition_mode`). Nếu có cấu trúc mặc định, ghi vào config của đúng loại đề; không hardcode theo tên loại đề.
7. Không hỏi giáo viên chọn JSONL / `.tex` / skill / script. Agent tự chọn cách lưu và chỉ bàn về script khi có thao tác lặp lại.
8. Tóm tắt lại cho họ bằng tiếng Việt, một khối ngắn: vai trò, loại đề, cách phối dạng câu, chỗ để câu hỏi, chỗ ra PDF. Kết thúc bằng một câu:

   > Thầy/cô có thể gửi câu hỏi bằng văn bản, ảnh hoặc LaTeX. Hình học, bảng biến thiên và lời giải dài đều được hỗ trợ; agent sẽ tự chọn cách lưu phù hợp.
