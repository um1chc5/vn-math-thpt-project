# Onboarding — chọn cách làm việc

Repo này **chưa khóa** loại đề hay cây ngân hàng. Lần chat đầu, agent chạy menu dưới rồi **mới** tạo file YAML / folder. Thầy/cô chọn ý tưởng nào vừa dùng; không phải chọn hết.

Nếu `src/configs/profile.yaml` có `completed: true` thì bỏ qua bước này (trừ khi họ nói “làm lại onboarding”).

## 1. Bạn dạy ở đâu?

| | Vai trò | Thường cần |
|--|---------|------------|
| A | Giáo viên trường | Header Sở/trường/lớp, ma trận tổ chuyên môn, kiểm tra 15 phút → cuối kỳ, có khi luyện TN THPT |
| B | Gia sư / dạy thêm | Header tên GV hoặc tối giản, phiếu theo buổi, theo học sinh, không bắt buộc ma trận Sở |
| C | Cả hai | Hai bộ header hoặc một header đổi theo lần ra đề |
| D | Khác | Ghi chú (trung tâm, online, soạn thuê, …) |

## 2. Loại sản phẩm (ý tưởng)

Không có file YAML sẵn. Chỉ tạo file cho loại **họ nói sẽ dùng**.

| Ý tưởng | Ai hay dùng | Gợi ý khi hỏi thêm |
|---------|-------------|-------------------|
| Kiểm tra 15 phút / 1 tiết | Trường | 1 bài vừa dạy? |
| Giữa kỳ / cuối kỳ | Trường | Danh sách chương do họ đưa, đừng đoán |
| Luyện tốt nghiệp THPT | Trường + gia sư | Hỏi ma trận năm nay (số câu từng phần) |
| Phiếu bài tập theo buổi | Gia sư | Thời lượng buổi, sĩ số |
| Đề theo chuyên đề | Cả hai | Không theo lịch tuần của trường |
| Đề theo học sinh | Gia sư | Tên HS chỉ để đặt folder, không in trừ khi họ muốn |
| Khác | — | Họ đặt tên (`--loai-de` = slug họ chọn) |

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

## 3. Cây ngân hàng (ý tưởng)

Folder `src/question-bank/` để trống cho đến khi chọn.

| | Cách chia | Ví dụ path |
|--|-----------|------------|
| A | Theo chương GDPT 2018 | `lop12/ung-dung-dao-ham.jsonl` |
| B | Theo chuyên đề tự đặt | `chuyen-de/dao-ham-ham-hop.jsonl` |
| C | Theo học sinh / lớp dạy thêm | `gia-su/hs-minh/dao-ham.jsonl` |
| D | Ít file, lọc metadata | `bank.jsonl` (mọi câu, lọc `lop`/`chuong`/`tag`) |
| E | Hỗn hợp | Trường dùng A, gia sư thêm C |

Schema một dòng JSON (gợi ý, thêm field nếu họ cần): xem [question-bank.md](question-bank.md).

## 4. Mức độ

| | Scheme | Khi nào |
|--|--------|---------|
| A | `nhan_biet` / `thong_hieu` / `van_dung` / `van_dung_cao` | Đề trường, ma trận |
| B | dễ / trung bình / khó | Gia sư, phiếu luyện |
| C | Không gắn mức độ | Ngân hàng nhỏ |
| D | Nhãn riêng | Họ liệt kê |

## 5. Header trang đề

| | Style | Config |
|--|--------|--------|
| A | Sở + trường + lớp | `school.yaml`: `so_gd`, `truong` |
| B | Gia sư (tên GV, môn, buổi) | `school.yaml` hoặc `tutor.yaml`: `ho_ten_gv`, không cần Sở |
| C | Tối giản (chỉ môn + thời gian) | Để trống tên trường |

## 6. Dạng câu đang soạn

Tự luận · trắc nghiệm · đúng/sai · trả lời ngắn. Chỉ bật item template nào họ dùng (`src/templates/items/`).

---

## Agent: sau khi họ chọn

1. Ghi `src/configs/profile.yaml` (`completed: true` + các lựa chọn).
2. Ghi header vào `school.yaml` / `tutor.yaml`.
3. Tạo **chỉ** YAML loại đề họ chọn; đừng seed 15-phut/giua-ki/thpt-qg nếu họ không xin.
4. Tạo cây folder ngân hàng đúng layout đã chọn (vẫn để trống file nếu chưa có câu).
5. Tóm tắt lại cho họ bằng tiếng Việt, một khối ngắn: vai trò, loại đề, chỗ để câu hỏi, chỗ ra PDF.
