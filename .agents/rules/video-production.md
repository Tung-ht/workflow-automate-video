# Video Production Rules — Hard Constraints & Execution Discipline

> **LUẬT TỐI CAO (HARD CONSTRAINTS):**
> Các quy tắc dưới đây áp dụng cho MỌI video của MỌI kênh YouTube trong hệ thống `video-atlas`.
> Tất cả các file trong `.agents/rules/` là **Always-On Rules** được nạp 100% vào Context ở MỌI lượt hội thoại.
> AI Agent PHẢI tự ngắt nhịp và đối chiếu lại 10 Quy tắc này trước khi thực thi bất kỳ bước sản xuất nào. KHÔNG ĐƯỢC vi phạm.

1. **Provider:** Mặc định `flowkit`. KHÔNG dùng `atlas_cloud` cho image/video gen khi chưa được user approve (tốn tiền API thật).
2. **Short Duration & Clips (53 - 58s, Max 60s):**
   - **Số lượng shots:** **7-8 shots tổng** (6-7 shots nội dung + 1 shot Outro CTA 8s cố định).
   - **Tối ưu nhịp điệu (Tránh kéo dãn/đơ hình):** Do clip Google Flow dài cố định 8.0s, thoại của mỗi shot nội dung chỉ nên dài **6.5 - 7.5 giây** (~15-18 từ/shot). Khi thoại <= 7.5s, `assemble.py` sẽ cắt gọn gàng mà **KHÔNG BAO GIỜ bị freeze/kéo dãn đơ hình**.
   - **Word Budget tổng:** **130 - 145 từ MAX** (Nội dung chính ~110-125 từ + Outro CTA 19 từ).
   - **Thời lượng `final.mp4`:** **53 - 58 giây** (trần tối đa 60.0s để đảm bảo 100% nằm trong luồng Shorts feed YouTube).
3. **Keyframe Short mới 100%:** Tạo mới ở tỷ lệ 9:16, KHÔNG crop/reuse từ Long-form 16:9.
4. **Reddit Research riêng cho Short:** Bắt buộc dùng Reddit MCP tìm hook/góc nhìn/chi tiết gây sốc khác cho Short. KHÔNG chỉ dùng lại thông tin từ Long-form.
5. **Ngôn ngữ:** 100% tiếng Anh Mỹ (narration, caption, keyframe text). KHÔNG chèn ngôn ngữ khác.
6. **Duyệt kịch bản (Approval Gate 1):** PHẢI trình kịch bản `beats.json` dưới dạng bảng Markdown dễ đọc gồm 5 cột (`Shot ID`, `Thời lượng (s)`, `Narration (Tiếng Anh Mỹ)`, `Dịch Tiếng Việt`, `Mô tả Visual`) để user review nhanh và chính xác → hỏi user _"Kịch bản beats.json đã sẵn sàng. Bạn muốn sửa gì không hay Approve để chạy production?"_ → CHỜ USER APPROVE → mới tiến hành chạy keyframes.
7. **Thứ tự Sản xuất & Đăng:** Sản xuất Long-form TRƯỚC → Short SAU. Đăng Long-form TRƯỚC (8-10am EST) → Short SAU 4-24h.
8. **QUY TẮC BẮT BUỘC YÊU CẦU URL PROJECT GOOGLE FLOW KHI TẠO VIDEO (GEN MỚI, GEN LẠI, HOẶC GEN BỔ SUNG) & REVIEW KEYFRAME (QUY TẮC CỨNG):**
   - **BẤT KỲ KHI NÀO** người dùng yêu cầu tạo video (dù là **gen mới từ đầu**, **gen lại clip bị lỗi/chưa ưng ý**, hoặc **gen bổ sung thêm clip**), AI Agent **BẮT BUỘC PHẢI XÁC NHẬN / YÊU CẦU ĐƯỜNG LINK URL CỦA PROJECT GOOGLE FLOW ĐANG MỞ** (ví dụ: `https://labs.google/fx/vi/tools/flow/project/<project_id>`) trước khi thực hiện bất kỳ lệnh submit video nào.
   - **Tại Gate 2 (sau khi chạy `keyframes.py`):** AI Agent **BẮT BUỘC LẬP TỨC TẠM DỪNG** (phanh tiến trình) $\rightarrow$ Thông báo user: _"Đã gen xong keyframes & thumbnail. Mời bạn kiểm tra, xóa watermark (nếu có) trong thư mục keyframes/, và **đồng thời cung cấp đường link URL của Project Google Flow bạn đang mở** (ví dụ: `https://labs.google/fx/vi/tools/flow/project/<project_id>`) để hệ thống tạo video chính xác vào project đó!"_
   - **TUYỆT ĐỐI KHÔNG** tự ý chạy `clips.py` hoặc submit bất kỳ request video nào khi chưa có URL Project Google Flow xác nhận từ user.
   - Khi nhận được Project URL từ user, AI Agent cấu hình Project ID làm Active Project trong FlowKit trước khi submit video.
   - **Cơ chế Video Generation (Fire-and-Forget, KHÔNG Auto-Download, KHÔNG Auto-Retry):** Script `clips.py` gửi request tạo clip theo từng đợt (batch 3 clip/lần) lên FlowKit và kết thúc ngay. Video sẽ hiện trực tiếp trên màn hình Canvas Google Flow để user tải về thủ công và đặt vào `clips/` (hoặc đặt tên `clip_1a.mp4`, `clip_2a.mp4`...), sau đó chạy `assemble.py`. (Lưu ý: Tính năng sinh Keyframe `keyframes.py` vẫn giữ nguyên 100% cơ chế tự động tạo và tải về máy).
9. **Outro CTA BẮT BUỘC:** Mọi video (Short & Long-form) PHẢI có beat/frame Outro CTA ở cuối. Tra câu CTA chính xác theo kênh trong `channel-identities.md`. KHÔNG được bỏ qua, rút ngắn, hoặc thay đổi nội dung CTA.
10. **Tỷ lệ Thoại & Shot trong Beat:** Clip Google Flow dài cố định chuẩn **8 giây**. Nếu thoại Beat ≤ 12s, gán 1 shot (8s). Nếu thoại Beat **> 12s** (như 14-18s), **BẮT BUỘC** chia Beat đó thành 2-3 Shots (ví dụ `1a` [8s] và `1b` [8s]) hoặc tách làm 2 Beats ngắn hơn để tránh đơ/lag hình.
11. **Google Flow Safety & Prompt Rules (Tránh bị từ chối / mất credit / lỗi vi phạm người nổi tiếng):**
    - **PHÂN BẬC TỰ DO NỘI DUNG (Content Policy Distinction)**:
      - **Narrative / Kịch bản thoại (`narration`)**: **ĐƯỢC PHÉP 100% TỰ DO**. Bạn có thể viết, nhắc đến, hay gọi tên bất kỳ ai (người thật, nhân vật lịch sử, Alexey Pajitnov, Henk Rogers, Steve Jobs...) cũng như bất kỳ chủ đề hay sự kiện nào. Không có bất kỳ hạn chế nào cho phần kịch bản/thoại giọng đọc TTS!
      - **Visual Prompts (Ảnh Keyframe & Video Prompt)**: **BẮT BUỘC tuân thủ bộ lọc của Google Flow** để không bị từ chối sinh video.
    - **QUY TẮC TẠO HÌNH VISUAL PROMPT (Keyframes & Video Clips)**:
      - `video_prompt` tuyệt đối KHÔNG được để trống (`""`).
      - KHÔNG dùng tên thương hiệu / nhãn hiệu thương mại (Nintendo, PlayStation, iPhone, Game Boy...) trong `scene` hoặc `video_prompt`. Thay bằng tên chung ("modern handheld gaming console", "retro 16-bit gaming system").
      - KHÔNG dùng tên người thật (Alexey Pajitnov, Henk Rogers, Steve Jobs...) hoặc khuôn mặt giống hệt người nổi tiếng ngoài đời trong `scene`, `keyframe_prompt`, `video_prompt` để tránh kích hoạt bộ lọc *"câu lệnh này có thể vi phạm chính sách về việc tạo video về người nổi tiếng"*.
      - **ĐƯỢC PHÉP**: Mô tả nhân vật bằng các danh từ chung hư cấu sinh động (`"a 16-bit pixel art computer programmer with a beard"`, `"a charismatic tech entrepreneur in a business suit"`). AI sẽ tự tạo ra nhân vật sinh động, có biểu cảm mà 100% qua mặt bộ lọc Google Flow.
    - Tránh từ khóa bạo lực, vũ khí, nhân vật bản quyền trong Visual Prompt → kích hoạt Safety Filter khiến request bị huỷ.
12. **CHIẾN LƯỢC FIRST FRAME THUMBNAIL CHO YOUTUBE SHORTS (FRAME 0 OPTIMIZATION)**:
    - **Quy tắc cốt lõi**: Mọi video Short BẮT BUỘC tuân thủ **Mục 2 trong [`channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md)** (Công thức 3 Lớp cho Frame 0: Lớp 1 Direct Keyframe Prompt Headline Embedding + Lớp 2 Headline Text Card + Lớp 3 Kinetic Subtitle at 0.00s).
    - **Thực thi khi sinh Keyframe 1a**: Ngay từ bước `keyframes.py`, `keyframe_prompt` của Shot 1a (`kf_1a.jpg`) BẮT BUỘC chèn chỉ thị chữ Headline trực tiếp vào prompt tạo ảnh AI để bức ảnh sinh ra ĐÃ CÓ sẵn chữ Headline khổng lồ đập vào mắt người xem.
    - **Cấm màn hình đen khởi đầu**: Shot 1a tuyệt đối KHÔNG bắt đầu bằng màn hình đen, fade-in từ màu đen hay khoảng dừng 0.5s ở đầu.
    - **Checklist Gate 2**: Ở Gate 2, Agent & User kiểm tra `kf_1a.jpg` đảm bảo Headline hiển thị đập vào mắt trước khi duyệt sinh clip.
13. **QUY TẮC CẤM ZOOM-IN VÀ TÙY CHỌN SÓNG GIẤY VỚI THỂ LOẠI COMIC / TRUYỆN TRANH (`pulp-comic` / `Pulp Hypotheses`):**
    - ⛔ **CẤM TUYỆT ĐỐI CAMERA ZOOM-IN (`zoom_in`, `push_in`, `quick_zoom`):** Đối với video thể loại comic / truyện tranh cổ điển, tuyệt đối KHÔNG dùng hiệu ứng phóng to / zoom dồn camera vào hình. Camera mặc định khi không chỉ định BẮT BUỘC là `"static"`, tuyệt đối KHÔNG mặc định `"push_in"`.
    - 💡 **TÙY CHỌN HIỆU ỨNG SÓNG GIẤY (PAPER WAVE RIPPLE EFFECT):** Không bắt buộc cho mọi shot. Chỉ sử dụng khi phù hợp với cảnh (ví dụ các phân cảnh lật trang, nhịp comic tactile): `"Include a subtle tactile paper wave wobble ripple effect, as if someone is holding the edge of the printed comic paper page and gently shaking it to create paper wave ripples."`
    - ✅ **CHỈ SỬ DỤNG CHUYỂN ĐỘNG 2D TRUYỆN TRANH CHUẨN:** Gán rõ trong `beats.json` và `video_prompt`: `camera: "static"` (camera tĩnh cố định), `camera: "pan"` (trượt ngang/dọc qua ô truyện 2D), hoặc `camera: "page_turn"` (lật trang truyện 3D). Mọi `video_prompt` cho thể loại comic BẮT BUỘC chèn thêm ràng buộc cứng: `"flat 2D comic strip — camera static or flat pan, no zoom in, no 3D push in"`.
14. **QUY TẮC VỊ TRÍ Ô CHỮ / BONG BÓNG THOẠI (NO BOTTOM TEXT / TOP PLACEMENT RULE):**
    - Mọi ô thoại (speech balloons), ô chữ tiêu đề (headline text banners) BẮT BUỘC chỉ thị vị trí nằm ở **NỬA TRÊN CỦA KHUNG HÌNH** (`"positioned near the top edge of the frame"` / `"placed in the upper half of the comic panel"`).
    - ⛔ **CẤM TUYỆT ĐỐI đặt ô chữ ở góc dưới bên phải hoặc chính giữa đáy ảnh (`bottom-right` / `bottom-center`)**, vì đây là khu vực bị che/đè bởi Logo Watermark của Google Flow, Watermark Kênh và Phụ đề Kinetic.
15. **QUY TẮC MÔ TẢ CỜ VIỆT NAM CHÍNH XÁC (VIETNAMESE FLAG ACCURACY):**
    - Khi vẽ Cờ Việt Nam trong `keyframe_prompt`, BẮT BUỘC mô tả chi tiết: `"the official flag of Vietnam, a solid bright crimson-red flag with a single centered golden-yellow five-pointed star"`.
    - Tuyệt đối không viết ngắn gọn `"Vietnamese flag"` để tránh AI vẽ nhầm số lượng sao hoặc họa tiết sai lệch.
16. **QUY TẮC CHUẨN ÂM THANH YOUTUBE (-14 LUFS NORMALIZATION & DUCKING):**
    - Giọng đọc TTS BẮT BUỘC rõ ràng, nổi bật. Nhạc nền (BGM) set âm lượng thấp hơn thoại từ **-18dB đến -22dB** (kỹ thuật Ducking) để giọng đọc không bị chìm.
    - Tổng thể âm lượng audio xuất ra đạt chuẩn **-14 LUFS** (YouTube Integrated Loudness Standard) để không bị thuật toán YouTube tự động giảm âm lượng video.
17. **QUY TẮC VIẾT CHỮ CHO AI TTS ĐỌC (TTS PHONETIC & PRONUNCIATION RULE):**
    - Trong phần kịch bản thoại (`narration`), viết các số năm bằng chữ (ví dụ: `nineteen eighty-five` thay vì `1985`, `nineteen forty-five` thay vì `1945`).
    - Viết rõ các tên gọi dễ đọc cho AI TTS (ví dụ: `Nintendo`, `Game Boy`, `PlayStation`) để tránh giọng AI đọc sai phiên âm hoặc đọc từng chữ cái rời rạc.





