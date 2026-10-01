# YouTube AI Production Rules — Creative & Auto-Humanization Standard

> **LUẬT TỐI CAO (HARD CONSTRAINTS):**
> Áp dụng cho MỌI kênh YouTube trong dự án `video-atlas` (Papercut Business, Pixel Rewind, và các kênh tương lai).
> Định hướng tư duy sáng tạo nội dung AI không trùng lặp + Luồng tự động hóa "Chất người" 100%.
> Tất cả các file trong `.agents/rules/` là **Always-On Rules** được nạp 100% vào Context ở MỌI lượt hội thoại.

---

## 1. Triết Lý Cốt Lõi: Tự Động Hóa "Chất Người" (Full Auto-Humanization)

YouTube KHÔNG cấm AI, nhưng họ tiêu diệt sự lặp lại vô cảm (Generic and Repetitive Content). Để hệ thống tự động hóa 100% mà vẫn được duyệt kiếm tiền và thu hút khán giả Mỹ:

- **70% Macro Structure (Khung vĩ mô - AI đảm nhận):** Tra cứu dữ liệu, lập dàn ý thô, xây dựng cấu trúc kịch bản `beats.json`.
- **30% Auto-Humanization Pipeline (Chất người tự động - AI Agent tự xử lý):**
  1.  **AI Persona (Nhân cách kênh):** Mọi kịch bản phải phát biểu qua Nhân cách AI cụ thể của kênh đó (xem định nghĩa trong Skill kênh). Không dùng giọng "bách khoa toàn thư" tẻ nhạt.
  2.  **Reddit Research Pipeline (Reddit MCP):** Tự động cào góc nhìn, câu chuyện, tranh luận thực tế của người thật trên các Subreddit ngách để chèn vào kịch bản (không copy-paste nguyên xi).
  3.  **Imperfection Pass (Checklist Phá Hoàn Hảo):** Tự động ngắt nhịp câu theo chuẩn **Staccato** (3 câu ngắn dồn dập -> 1 câu giải thích êm ái), chèn câu cảm thán cụt, loại bỏ 100% từ nối máy móc (_Furthermore, Additionally, Moreover, In conclusion_).

---

## 2. Chiến Lược "Nhân Bánh & Vỏ Bánh" (Edutainment Strategy)

- **Nhân Bánh (Core Value):** Dữ liệu thô, kiến thức ngầm về kinh tế, lịch sử, công nghệ, thương hiệu.
- **Vỏ Bánh (Entertainment Packaging):** Hình thức thể hiện riêng của từng kênh (Vox Paper Collage cho _Papercut Business_, Pixel Art CRT cho _Pixel Rewind_).
- **Tỷ lệ:** 80% Thời lượng cho sự Giải trí/Visual/Trải nghiệm -> 20% Lồng ghép Giá trị học thuật.

---

## 3. Quy Tắc Thumbnail & Chiến Lược First Frame Cho YouTube Shorts

- **Long-form (16:9):** Chạy `thumbnail.py` để tạo file `thumbnail.png` 16:9. Chữ 3-5 từ, font nét cứng, màu vàng/trắng tương phản cực mạnh với nền đậm. Phủ lớp nhiễu hạt (**Film Grain Filter**) hoặc **CRT Scanlines**.
- **Shorts (9:16):** **BỎ QUA BƯỚC TẠO THUMBNAIL (`thumbnail.py`)**. YouTube Shorts tự động chọn **Frame 0 (Shot 1a)** làm thumbnail hiển thị trên Shorts Feed. Tuân thủ Quy tắc 12 (Công thức 3 Lớp cho Frame 0: Visual Anchor 9:16 + Bold Headline Text Card `"title_en"` + Kinetic Subtitle at t=0.00s) để tối đa hóa tỷ lệ dừng xem 3 giây đầu.
- **Nói KHÔNG với Misleading:** Không dùng ảnh biểu cảm cường điệu "há hốc mồm/Sốc" kiểu Kids, không treo đầu dê bán thịt chó.

---

## 4. Quy Trình Kiểm Soát Sản Xuất Nghiêm Ngặt (2-Gate User Approval)

1.  **Gate 1 (Duyệt kịch bản):** Agent chạy Auto-Humanization Pipeline -> Trình bảng kịch bản `beats.json` 5 cột (`Shot ID`, `Thời lượng`, `Narration EN`, `Dịch Tiếng Việt`, `Visual`) -> Hỏi user: _"Kịch bản beats.json đã được hoàn thiện. Bạn có muốn sửa gì không hay Approve để chạy production?"_ -> CHỜ USER APPROVE.
2.  **Chạy Keyframes:** Khi user Approve Gate 1 -> Agent chạy `keyframes.py` để tạo bộ ảnh keyframes + thumbnail (Tự động tải về máy).
3.  **Gate 2 (Thực thi Quy tắc 8 - Tạm dừng xóa Watermark & Yêu cầu URL Project Google Flow):** Ngay khi `keyframes.py` chạy xong -> Agent **LẬP TỨC TẠM DỪNG** -> Báo user: _"Đã gen xong keyframes & thumbnail. Mời bạn kiểm tra, xóa watermark (nếu có) trong thư mục keyframes/, và **đồng thời gửi kèm đường link URL Project Google Flow bạn đang mở** để hệ thống tạo video đúng nơi!"_ -> **CHỜ USER GỬI LINK PROJECT & XÁC NHẬN** (Áp dụng cho MỌI trường hợp tạo video: gen mới, gen lại, hoặc gen bổ sung) -> Cấu hình Project ID vào FlowKit -> Mới chạy `clips.py`.
4.  **Chạy Clips & Assembly & Metadata (Fire-and-Forget Video Generation):** Khi User xác nhận hoàn tất Gate 2 kèm Project URL -> Agent chạy `clips.py` (cơ chế Fire-and-Forget, chia batch 3 clip/lần, **KHÔNG auto-download, KHÔNG auto-retry**) -> Video render trực tiếp trên web Google Flow để user tải về `clips/` -> Chạy `audio.py` -> `assemble.py` để xuất video `final.mp4`. Ngay sau khi xuất video xong, Agent BẮT BUỘC chạy `python3 scripts/metadata.py out/<project>` để tạo gói tài nguyên **YouTube SEO Metadata Package** (Lưu file `out/<project>/youtube_seo.md` và in trực tiếp ra terminal).

---

## 5. Quy Tắc Tỷ Lệ Thoại & Shot Trong Beat (`beats.json`)

Mỗi clip AI generated (Google Flow) có thời lượng cố định chuẩn là **8 giây** (không thể điều chỉnh khi khởi tạo).

- **Lời thoại Beat ≤ 12 giây:** Cho phép gán **1 shot** (8s). Việc `assemble.py` kéo dãn/freeze nhẹ khung hình vài giây là chấp nhận được.
- **Lời thoại Beat > 12 giây (ví dụ 14 - 18s):** **BẮT BUỘC** phải chia Beat đó thành **2 hoặc 3 shots** riêng biệt (ví dụ Shot `1a` [8s] và Shot `1b` [8s]), hoặc tách làm 2 Beats ngắn hơn.

---

## 6. Quy Tắc Xuất Gói YouTube & TikTok SEO Metadata Package (`youtube_seo.md`)

Mọi video sau khi render hoàn tất BẮT BUỘC phải chạy `python3 scripts/metadata.py out/<project>` để tạo gói tài nguyên `youtube_seo.md`:
1. **Title Options (3 lựa chọn Tiêu đề chuẩn SEO & CTR)**:
   - Giữ từ khóa chính trong **5 từ đầu tiên** (< 55 ký tự để tránh bị cắt chữ trên giao diện di động).
   - Video Shorts BẮT BUỘC gắn đuôi `#Shorts`.
2. **Description 3 Zone (Chuẩn SEO YouTube)**: 
   - *Zone 1 (Above the fold)*: 150 ký tự đầu tiên chứa Hook + CTA + Keyword.
   - *Zone 2 (Body & Timestamps)*: Tóm tắt kịch bản + Timestamps (Chapters) phân đoạn tự động.
   - *Zone 3 (Compliance & Footer)*: Lời kêu gọi hành động (Subscribe & Link) + Lịch phát sóng + Hashtags (Giới hạn tối đa **5 đến 8 Hashtags**, tuyệt đối không quá 15 hashtags để không bị phạt bỏ qua hashtags). Khai báo AI được thực hiện trực tiếp trên checkbox YouTube Studio khi upload.
3. **Tags (Từ khóa ẩn ≤ 480 chars)**: Phân tách bằng dấu phẩy, gồm Tên kênh + Tiêu đề exact match + Từ khóa tìm kiếm + Từ viết sai phổ biến.
4. **Pinned Comment (Bình luận ghim)**: Câu hỏi mở câu tương tác + Link dẫn tới video liên quan (Related Video).
5. **TikTok & Instagram Reels Caption Package**: Đoạn caption ngắn 150 ký tự kèm 4-5 hashtags chuyên biệt cho TikTok/Reels.


