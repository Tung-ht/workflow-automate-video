# Bảng tính & Hướng dẫn Tối ưu chi phí (Cost Optimization)

Workflow tạo video cắt dán phong cách Vox sử dụng các API AI chất lượng cao. Nếu không kiểm soát tốt, chi phí tạo video có thể tăng rất nhanh. Tài liệu này giải thích các phương pháp tối ưu chi phí đã được áp dụng vào mã nguồn của Skill và cung cấp bảng dự toán chi phí chi tiết.

## 1. Bảng Dự Toán Chi Phí (Chuẩn 1 Cảnh / Beat dài 6-7s)

Bảng dưới đây ước lượng chi phí cho các mức độ dài video phổ biến. 
*Giả định:*
- **Ảnh (Keyframe):** `google/nano-banana-2/text-to-image-developer` ($0.04 / ảnh)
- **Video Motion:** `kwaivgi/kling-video-o3-pro/image-to-video` ($0.095 / giây video sinh ra). AI thường sinh video thành các đoạn tròn 5s hoặc 10s. Ta giả định tạo đoạn 7s (tiêu tốn ~ $0.665/cảnh).
- **Audio (Âm thanh):** Nhạc nền (~$0.11) và Lời đọc TTS (~$0.02 - $0.05).

| Thời lượng Video | Số lượng Cảnh (Shots) | Chi phí tạo Ảnh | Chi phí tạo Video | Chi phí Âm thanh | **TỔNG CHI PHÍ (Ước tính)** |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **15 giây** (Short/Reel) | 3 cảnh | $0.12 | ~ $2.00 | $0.13 | **~ $2.25** |
| **30 giây** (Standard Ad) | 4-5 cảnh | $0.20 | ~ $3.33 | $0.14 | **~ $3.67** |
| **60 giây** (Full Ad) | 8-10 cảnh | $0.40 | ~ $6.65 | $0.16 | **~ $7.21** |
| **3 phút** (Explainer) | 24-27 cảnh | $1.08 | ~ $17.95 | $0.30 | **~ $19.33** |

*(Lưu ý: Nếu không sử dụng phương pháp tối ưu bên dưới, chi phí có thể đắt gấp 2 hoặc 3 lần bảng này).*

---

## 2. Phân tích các bước Tối ưu đã áp dụng

### A. Sử dụng model ảnh bản Developer (Giảm 50% tiền ảnh)
- **Thay đổi:** Đổi từ `nano-banana-2` thường ($0.08) sang bản `-developer` ($0.04).
- **Giải thích:** Model developer có chất lượng và khả năng render text tiếng Việt / Anh y hệt bản thường nhưng được trợ giá cho nhà phát triển.

### B. Thay đổi nhịp điệu: 1 Cảnh kéo dài 6-7s (Giảm ~40-50% tiền video)
- **Thay đổi:** Trước đây, Skill hướng dẫn cắt 2 cảnh cho mỗi câu nói 10s (mỗi cảnh 4-5s). Hiện tại, Skill gộp thành **1 cảnh duy nhất kéo dài 6-7s** cho mỗi nhịp.
- **Giải thích:** Chi phí API Video tính theo giây. Việc có ít cảnh hơn nhưng kéo dài thêm một chút giúp giảm đáng kể số lần gọi API và tổng số giây cần render. Để cảnh 6-7s không bị nhàm chán, AI được hướng dẫn viết prompt `element_motion` thật phong phú (nhiều chi tiết chuyển động cùng lúc).

### C. Sử dụng Kling thay cho Gemini (Giảm ~27% tiền video)
- **Thay đổi:** Sử dụng `kwaivgi/kling-video-o3-pro/image-to-video` làm model sinh chuyển động mặc định.
- **Giải thích:** Gemini Omni Flash có giá khá cao ($0.13/giây). Kling O3 Pro có giá thấp hơn ($0.095/giây) nhưng lại giữ được độ phẳng (flat 2D) của giấy cắt dán rất tốt và đặc biệt là không bị chặn (block) khi video có hình ảnh người thật/logo thương hiệu nổi tiếng.

### D. Render bản nháp (Draft Mode) với chi phí $0 (Chống lãng phí 100%)
- **Thay đổi:** Bổ sung script `draft.py`.
- **Giải thích:** Sai lầm tốn kém nhất là tạo ra video xịn xong mới nhận ra nhịp điệu quá nhanh hoặc lời đọc (VO) không khớp, dẫn đến phải bỏ video đó đi và tạo lại từ đầu. 
`draft.py` giải quyết vấn đề này bằng cách dùng `ffmpeg` ghép các tấm ảnh tĩnh (0.04$) cùng với Audio để tạo thành một video thô `draft.mp4` hoàn toàn **miễn phí**. Bạn chỉ bấm chạy API Video đắt đỏ sau khi đã xem và hài lòng với bản nháp này.
