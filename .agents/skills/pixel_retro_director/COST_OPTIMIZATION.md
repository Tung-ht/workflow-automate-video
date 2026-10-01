# Bảng tính & Hướng dẫn Tối ưu chi phí (Cost Optimization) - Pixel Retro Director

Workflow tạo video pixel retro / phong cách CRT sử dụng chung cấu trúc script và pipeline với `vox-director`, đồng thời sử dụng hoàn toàn cùng các model AI. Do đó, **cấu trúc chi phí hoàn toàn giống hệt với vox-director**.

Tài liệu này giải thích các phương pháp tối ưu chi phí đã được áp dụng và cung cấp bảng dự toán chi phí chi tiết.

## 1. Bảng Dự Toán Chi Phí (Chuẩn 1 Cảnh / Beat dài 6-7s)

Bảng dưới đây ước lượng chi phí cho các mức độ dài video phổ biến.
*Giả định:*
- **Ảnh (Keyframe Pixel Art):** `google/nano-banana-2/text-to-image-developer` ($0.04 / ảnh)
- **Video Motion:** `kwaivgi/kling-video-o3-pro/image-to-video` ($0.095 / giây video sinh ra). AI sinh video đoạn 7s tiêu tốn ~ $0.665/cảnh.
- **Audio (Âm thanh):** Nhạc nền chiptune/retro (~$0.11) và Lời đọc TTS (~$0.02 - $0.05).
- **Post-processing (CRT/VHS):** $0 (chạy local qua `ffmpeg`).

| Thời lượng Video | Số lượng Cảnh (Shots) | Chi phí tạo Ảnh | Chi phí tạo Video | Chi phí Âm thanh | **TỔNG CHI PHÍ (Ước tính)** |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **15 giây** (Short/Reel) | 3 cảnh | $0.12 | ~ $2.00 | $0.13 | **~ $2.25** |
| **30 giây** (Standard Ad) | 4-5 cảnh | $0.20 | ~ $3.33 | $0.14 | **~ $3.67** |
| **60 giây** (Full Ad) | 8-10 cảnh | $0.40 | ~ $6.65 | $0.16 | **~ $7.21** |
| **3 phút** (Explainer) | 24-27 cảnh | $1.08 | ~ $17.95 | $0.30 | **~ $19.33** |

*(Lưu ý: Nếu không sử dụng phương pháp tối ưu bên dưới, chi phí có thể đắt gấp 2 hoặc 3 lần bảng này).*

---

## 2. Phân tích các bước Tối ưu đã áp dụng (Kế thừa từ vox-director)

### A. Sử dụng model ảnh bản Developer (Giảm 50% tiền ảnh)
- **Thay đổi:** Sử dụng `nano-banana-2-developer` ($0.04) thay vì bản thường.
- **Giải thích:** Model developer tạo art pixel và chữ (nếu có) tốt tương đương bản thường nhưng rẻ hơn 50%.

### B. Thay đổi nhịp điệu: 1 Cảnh kéo dài 6-7s (Giảm ~40-50% tiền video)
- **Thay đổi:** Gom câu thành 1 cảnh dài 6-7s cho mỗi nhịp.
- **Giải thích:** Chi phí API Video tính theo giây. Ít cảnh hơn nhưng thời lượng mỗi cảnh vừa đủ (không quá dài) giúp tối ưu giá. Đối với Pixel Art, sử dụng `element_motion` mang tính retro (nhấp nháy, text typing, scanline scroll) giúp giữ được sự hấp dẫn trên cảnh tĩnh.

### C. Sử dụng Kling thay cho Gemini (Giảm ~27% tiền video)
- **Thay đổi:** Dùng `kling-video-o3-pro`.
- **Giải thích:** Kling có giá rẻ hơn ($0.095/s) so với Gemini Omni Flash ($0.13/s) và cực kỳ xuất sắc trong việc duy trì cấu trúc **2D flat grid** của Pixel Art. Tránh trường hợp AI cố biến hình ảnh thành 3D.

### D. Render bản nháp (Draft Mode) với chi phí $0 (Chống lãng phí 100%)
- **Thay đổi:** Sử dụng `draft.py`.
- **Giải thích:** Tương tự vox-director, `draft.py` kết hợp ảnh tĩnh pixel art với Audio thành video thô `draft.mp4` bằng `ffmpeg` hoàn toàn **miễn phí**. Giúp kiểm tra timing và nhịp điệu trước khi gọi API Video tốn tiền.

### E. CRT Effects hoàn toàn miễn phí
- **Thay đổi:** Xử lý hiệu ứng bằng `ffmpeg` local thay vì prompt AI.
- **Giải thích:** Hiệu ứng như CRT scanline, VHS tracking hay Phosphor glow được thực hiện qua lệnh `ffmpeg` ở bước Assemble cuối cùng. Điều này mang lại chất lượng chính xác mà **không tốn thêm đồng nào** cho chi phí API video.
