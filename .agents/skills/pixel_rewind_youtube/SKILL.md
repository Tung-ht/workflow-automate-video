---
name: pixel-rewind-youtube
description: >
  Chiến lược xây dựng kênh YouTube "Pixel Rewind" nhắm khán giả Mỹ (US) bằng AI
  phong cách Pixel Art / CRT / Retro Computing. Kích hoạt skill này BẤT CỨ KHI NÀO user yêu cầu:
  viết kịch bản (beats.json), chọn chủ đề cho video, làm thumbnail, tạo Outro,
  đăng video, hoặc bất kỳ công việc nào liên quan đến kênh "Pixel Rewind",
  series "Boot Sequence", hoặc chiến lược YouTube nói chung.
  Triggers: "pixel rewind", "boot sequence", "youtube strategy",
  "viết kịch bản", "beats.json", "thumbnail", "outro", "series",
  "video short", "video ngang", "long-form", "retro tech", "gaming history".
---

# Pixel Rewind — YouTube Channel Playbook

Cẩm nang toàn diện để xây dựng kênh YouTube **"Pixel Rewind"** nhắm tới khán giả
Mỹ (US), sản xuất tự động bằng AI phong cách 16-bit pixel art, CRT scanlines, và retro arcade aesthetic.

---

## 📌 Phân Định Scope & Kiến Trúc Skill

> ⚠️ **THAM CHIẾU QUY TẮC BẮT BUỘC (HARD CONSTRAINTS):**
> Mọi bước trong Skill này PHẢI tuân thủ nghiêm ngặt:
> - [`.agents/rules/video-production.md`](file:///d:/video-atlas/.agents/rules/video-production.md) — 12 quy tắc production (Provider flowkit, Gates, Duration, Anti-hallucination, Google Flow Safety)
> - [`.agents/rules/channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md) — Tham số kênh (voice, caption, watermark, CRT) + Outro CTA bất biến
> - Kỹ thuật pipeline: xem skill `vox-director` (`vox_papercut_director`) hoặc `pixel-retro-director`
> - Viết kịch bản giống người: xem skill `human-scriptwriter` (`human_scriptwriter`) — Anti-AI-slop, sensory injection, imperfection pass
> - Nghiên cứu Reddit: xem skill `reddit-research` (`reddit_research`) — Quy trình 5 bước đào insight người thật

Để tránh ôm đồm và chồng chéo trách nhiệm giữa các Skill:

* **`pixel_rewind_youtube` (Skill này):** Chịu trách nhiệm 100% về **Chiến lược Nội dung & Thương hiệu Kênh**.
  - Định hướng ngách nội dung (Retro Tech Origin Stories & Gaming History), series "Boot Sequence" (Khởi động — mỗi tập là origin story của 1 sản phẩm tech/game huyền thoại).
  - Chiến lược Phễu (Shorts 45s → Long-form), chọn chủ đề gây tò mò cho khán giả Mỹ (gamers, tech nostalgics).
  - Quy tắc viết kịch bản giữ chân người xem (Easter Egg Trick, Nostalgia Bait, The "One Person" Hook, Present-day Payoff, Staccato pacing).
  - Quy định nhận diện thương hiệu (Outro Voice CTA cố định, Watermark Logo Asset prompt, Thumbnail style).
  - **Sản phẩm đầu ra của Skill này:** File kịch bản `beats.json` chuẩn chiến lược + Ý tưởng thiết kế Logo/Thumbnail.

* **`pixel-retro-director` (`pixel_retro_director`):** Chịu trách nhiệm 100% về **Đạo diễn Kỹ thuật & Pipeline Sản xuất**.
  - Chuyển `beats.json` thành tài nguyên video hoàn chỉnh.
  - Sử dụng pixel art image prompts thay vì paper collage.
  - Xử lý hậu kỳ (CRT/scanline overlays, phosphor glow, VHS tracking).
  - Hướng dẫn và cung cấp các script công cụ (giống core pipeline của vox-director).
  - Gọi API tới các AI models để sinh ảnh, tạo chuyển động video, thu âm giọng đọc xAI TTS, ghép nhạc nền.
  - Sử dụng ffmpeg để chồng lớp watermark logo PNG, chèn phụ đề, và xuất file `final.mp4`.





## 1. Thông tin Kênh (Channel Identity)

| Thuộc tính | Giá trị |
|---|---|
| **Tên kênh** | Pixel Rewind |
| **Ngách (Micro-niche)** | "The untold stories behind the tech and games that shaped us" — Retro Tech Origin Stories & Gaming History |
| **Series chính** | "Boot Sequence" (Khởi động — mỗi tập là origin story của 1 sản phẩm tech/game huyền thoại) |
| **Khán giả mục tiêu** | Americans 20-40, gamers, tech nostalgics, những người lớn lên với Nintendo/Sega/early PC |
| **Phong cách hình ảnh** | 16-bit pixel art, CRT scanlines, phosphor glow, VHS tracking, retro arcade aesthetic |
| **Ngôn ngữ** | 100% Tiếng Anh (US) |
| **Giọng AI Voice** | xAI TTS, young energetic male voice (voice_id `kai`), giữ nguyên xuyên suốt tất cả video |

---

## 2. Chiến lược Phễu: Shorts → Long-form

Chiến lược cốt lõi: dùng **YouTube Shorts (45 giây)** làm "cái móc" (hook) kéo traffic
về cho **Video ngang (Long-form 3-5 phút)**.

### 2.1. Thứ Tự SẢN XUẤT: Long-form TRƯỚC, Short SAU

Long-form là "bộ não" — chứa toàn bộ nghiên cứu, data, narrative arc đầy đủ.
Short chỉ là "cái móc câu" rút ra từ Long-form.

**Quy trình sản xuất cho 1 chủ đề:**
1. **Nghiên cứu** Reddit cho chủ đề (dùng Reddit MCP) → viết Long-form.
2. **Viết `beats.json` LONG-FORM** (3-5 phút, ~40-45 shots) → duyệt kịch bản.
3. **Sản xuất Long-form** → `final.mp4` + `thumbnail.png`.
4. **Nghiên cứu Reddit LẦN 2** cho góc nhìn Short — tìm câu hỏi/tranh cãi/sự thật gây sốc mà cộng đồng đang bàn luận nhiều nhất. Short cần hook khác Long-form, nên cần research riêng.
5. **Viết `beats.json` SHORT** (53-58s tổng, 7-8 shots) — góc nhìn mới, keyframe mới 9:16.
6. **Sản xuất Short** → `final.mp4` riêng.



**Lý do:** Nếu làm Short trước, bạn chưa biết đâu là insight hay nhất, twist mạnh nhất
→ dễ chọn nhầm hook. Khi viết xong Long-form, bạn đã biết rõ **đâu là sự thật gây sốc
nhất** → biến nó thành Short.

### 2.2. Mối Quan Hệ Nội Dung: Bổ Sung, KHÔNG Lặp Lại

**TUYỆT ĐỐI KHÔNG** cắt 45s từ video dài rồi đăng lên Shorts. YouTube detect được nội
dung tái chế và dìm cả hai video.

**Nguyên tắc: Short = "Câu hỏi", Long-form = "Câu trả lời"**

| | Short (45s) | Long-form (3-5 phút) |
|---|---|---|
| **Vai trò** | Gây tò mò, đặt câu hỏi, bỏ lửng | Giải đáp thỏa mãn, full story |
| **Nội dung** | 1 sự thật gây sốc + "WHY?" bỏ lửng | Full story: How + Why + So What? |
| **Kết thúc** | **Cliffhanger** — không giải thích hết | **Satisfying** — người xem hiểu toàn bộ |
| **Keyframe** | **Keyframe MỚI 100%, định dạng 9:16** | Bộ keyframe đầy đủ 16:9 |
| **Script** | Viết MỚI, góc nhìn khác, KHÔNG tóm tắt | Script gốc đầy đủ |



Ví dụ Game Boy:
- **Short:** Chỉ nói về thiết kế — "The Game Boy was intentionally ugly. It looked like a brick. It had no backlight. Meanwhile Sega had a color screen. But that ugly design is exactly why it destroyed Sega..." → kết: "Want to know how a maintenance man pulled this off? Subscribe to Pixel Rewind..."
- **Long-form:** Đi sâu vào TOÀN BỘ — Gunpei Yokoi → Lateral Thinking with Withered Technology → bài toán pin và độ bền → sự thất bại của Game Gear → kết luận rộng hơn về thiết kế hiện đại.

### 2.3. Thứ Tự ĐĂNG VIDEO: Long-form TRƯỚC, Short sau 4-24 giờ

| Bước | Thời gian | Hành động | Lý do |
|---|---|---|---|
| **1** | Ngày N, sáng (8-10am EST) | **Đăng Long-form** | YouTube cần 2-4 giờ index + đề xuất ban đầu |
| **2** | Ngày N chiều/tối hoặc N+1 | **Đăng Short** | Shorts algorithm push mạnh trong 1-2 giờ đầu |
| **3** | Ngay sau khi đăng Short | **Gắn Related Video** | YouTube Studio → Short → Related Video → chọn Long-form |

**Tại sao KHÔNG đăng Short trước?** Khi Short viral → hàng ngàn người tò mò → bấm vào
kênh → **KHÔNG CÓ Long-form để xem** → họ rời đi vĩnh viễn. Cơ hội mất trắng.

**Tại sao KHÔNG đăng cùng lúc?** Đăng cùng lúc chia đôi engagement ban đầu. YouTube
đánh giá video trong 1-2 giờ đầu. Cả hai nhận nửa engagement → cả hai bị xếp "trung bình".

---

## 3. Dấu Ấn Thương Hiệu (Brand Identity & Consistency)

Để kênh trông chuyên nghiệp và tạo dấu ấn nhận diện ngay lập tức, tất cả video
(cả Shorts lẫn Long-form) PHẢI tuân thủ các quy tắc nhận diện thương hiệu sau:

### 3.1. Hybrid Watermark Logo "Pixel Rewind" (Chiến lược Logo Đỉnh Cao & Đồng Nhất)

Để đạt được **vừa thẩm mỹ retro cao cấp vừa đồng nhất 100% về vị trí và tỷ lệ**, kênh sử dụng **Giải Pháp Hybrid**:

1. **Phong cách & Prompt tạo Logo PNG Asset (Tạo 1 lần duy nhất):**
   Skill này quy định prompt chuẩn để tạo ảnh logo độc bản:
   > *"A pixel art logo of the text 'Pixel Rewind', 8-bit retro gaming typography, CRT phosphor glow effect, isolated on pure black background, high-resolution graphic asset."*

   *Cơ chế gọi tool:* Agent sử dụng bộ công cụ phát request để tạo ảnh, sau đó xử lý tách nền (giữ lại hiệu ứng glow) và lưu ảnh PNG trong suốt thu được vào **`assets/pixel_rewind_watermark.png`**.

2. **Tham số truyền vào beats.json:**
   Khi tạo kịch bản `beats.json`, AI Agent truyền 2 tham số watermark này:
   ```json
   "watermark": "Pixel Rewind",
   "watermark_image": "assets/pixel_rewind_watermark.png"
   ```

3. **Cách vận hành & Quy tắc đè Veo Logo:**
   - Skill `pixel_rewind_youtube` chịu trách nhiệm quy định phong cách logo, prompt tạo logo và truyền tham số `"watermark_image"` vào `beats.json`.
   - **Text Watermark góc phải dưới (`"watermark"`):** BẮT BUỘC dùng đồng nhất `caption_style` với phụ đề (`"white"`). Được `text_overlay.py` tự động căn chỉnh tọa độ và kích thước riêng cho từng định dạng (16:9 Long-form & 9:16 Short) kèm viền nét stroke và bóng đổ, đảm bảo **100% CHE HOÀN TOÀN LOGO VEO (Google Flow logo)** ở góc phải dưới mà không bị lệch hay lộ viền.
   - Skill `pixel-retro-director` (kỹ thuật pipeline) sẽ đọc tham số `"watermark_image"` và `"watermark"` để gọi ffmpeg ghép đè theo đúng quy tắc này.

### 3.2. Signature Outro — Frame Cuối Cùng (BẮT BUỘC trên mọi video)

Mọi video trong series "Boot Sequence" PHẢI kết thúc bằng một shot Outro thống
nhất. Đây là "chữ ký" của kênh — khán giả xem nhiều video sẽ nghe đi nghe lại câu
này và tự động liên kết nó với thương hiệu "Pixel Rewind".

**Voice-over CTA:** Tham chiếu câu Outro CTA bất biến tại [`.agents/rules/channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md). KHÔNG ĐƯỢC THAY ĐỔI BẤT KỲ TỪ NÀO.

**Hình ảnh Outro — tĩnh, bất biến (IMMUTABLE):**

Hình ảnh Outro luôn theo cấu trúc sau, camera LUÔN TĨNH:
- Pixel art animation của một màn hình CRT monitor powering on.
- Tiêu đề **"Boot Sequence"** xuất hiện bằng chữ màu xanh lá cây dạ quang (green phosphor text).
- Xung quanh là các retro gaming sprites nhỏ trang trí.

### 3.3. Nhất quán xuyên suốt — Bảng tóm tắt

| Yếu tố | Shorts (45s) | Long-form (3-5 phút) | Ghi chú |
|---|---|---|---|
| **Watermark logo** | ✅ "Pixel Rewind" | ✅ "Pixel Rewind" | Cùng font, cùng vị trí, cùng opacity |
| **Voice CTA (Outro)** | Câu Short cố định | Câu Long-form cố định | KHÔNG ĐƯỢC sửa bất kỳ từ nào |
| **Voice ID** | `kai` (xAI TTS) | `kai` (xAI TTS) | Cùng giọng xuyên suốt |
| **Hình ảnh Outro** | CRT Boot Sequence | CRT Boot Sequence | Không đổi |
| **Camera Outro** | Static | Static | Không bao giờ zoom/pan |
| **Phong cách hình ảnh** | 16-bit pixel art + CRT | 16-bit pixel art + CRT | Đồng nhất toàn bộ kênh |

### 3.4. Quy Chuẩn Tạo Channel Banner & Avatar (YouTube Header)

Khi khởi tạo nhận diện kênh "Pixel Rewind" hoặc người dùng yêu cầu làm bộ Banner/Avatar:

1. **Avatar Kênh (Square 1:1, 800x800 px):**
   - **Prompt:** `"8-bit pixel art avatar of a retro arcade cabinet glowing with CRT phosphor light, green neon typography 'PR', centered on dark background, high resolution graphic asset."`
   - **File xuất:** `assets/pixel_rewind_avatar.png`

2. **Channel Banner Kênh (Cover Header 16:9, 2560x1440 px):**
   - **Kích thước chuẩn:** `2560 x 1440 px` (Full Canvas TV Display).
   - **Vùng an toàn (Desktop & Mobile Safe Zone):** `1546 x 423 px` nằm chính giữa trung tâm.
   - **Prompt Lớp Nền Canvas (2560x1440):** `"Detailed 16-bit pixel art banner of a wide retro arcade room with glowing arcade cabinets, CRT scanlines overlay, neon cyan and magenta lighting, wide 16:9 composition."`
   - **Lớp Chữ Vùng An Toàn (Safe Zone 1546x423):** 
     - **Tên Kênh Khổng Lồ:** "PIXEL REWIND" (Font chữ pixel 8-bit dạ quang xanh lá/neon).
     - **Tagline Khẩu Hiệu:** "RETRO TECH & GAMING HISTORY"
     - **Lịch Đăng Video:** "NEW EPISODES MON & THU" (Thứ 2 & Thứ 5 hàng tuần)
   - **File xuất:** `assets/pixel_rewind_banner.png`


---

## 4. Nguyên tắc Viết Kịch Bản — Quy tắc 70/30 & Scripting Rules

> Quy tắc viết kịch bản cơ bản (anti-AI-slop, staccato, sensory injection, imperfection pass): xem skill `human-scriptwriter`. Phần dưới chỉ chứa các quy tắc RIÊNG cho kênh Pixel Rewind.

### 4.1. Ba nhóm nội dung YouTube hạn chế trong YPP (phải tránh):
1. **Generic and Repetitive:** Nội dung rập khuôn.
2. **Off-putting or Distressing:** Câu view tiêu cực.
3. **AI Personas trong lĩnh vực nhạy cảm:** Giọng văn máy móc, tẻ nhạt.

### 4.2. Năm quy tắc khi viết kịch bản (beats.json):

**① Easter Egg Trick (Thay thế Reddit Trick của Papercut):**
Mọi kịch bản phải chứa ít nhất 1 sự thật cực kỳ ít người biết (obscure fact) mà chỉ fan cứng mới nhận ra — một chi tiết ẩn, một developer easter egg, một bản prototype bị hủy.
- Nguồn: Reddit (r/retrogaming, r/gaming, r/todayilearned, r/technology, r/NintendoSwitch, r/pcgaming), gaming wikis, các bài phỏng vấn lưu trữ.

**② Nostalgia Bait (Mồi nhử Hoài niệm có chủ đích):**
Liên hệ trực tiếp đến các trải nghiệm chung của người Mỹ lớn lên thập niên 80-90:
- Thổi bụi băng game (blowing into cartridges).
- Đợi tiếng tít tít của dial-up internet.
- Lần đầu nhìn thấy đồ họa 3D.
- Tiếng màn hình CRT bật lên.
- Mùi sách hướng dẫn game mới mua.
- Xin bố mẹ tiền xu (quarters) ra khu arcade.

**③ The "One Person" Hook (Cú Zoom Cá Nhân):**
Mỗi câu chuyện PHẢI focus vào MỘT con người cụ thể (kỹ sư, nhà thiết kế, thực tập sinh) — người đã đưa ra quyết định sống còn.
- KHÔNG: "Nintendo decided to make a portable console..."
- CÓ: "Gunpei Yokoi, a maintenance man at a playing card company, was bored on a train..."

**④ Present-day Payoff (Cú chốt hiện tại):**
Luôn kết thúc bằng việc liên kết công nghệ cũ đó với hiện tại.
- "And that chip they designed in 1985? It's still inside your microwave."
- "That failed console? Its controller layout became the standard you're using right now."

**⑤ Staccato Pacing, Anti-AI-slop & Imperfection:** Xem chi tiết trong skill `human-scriptwriter` §2 (Blacklist), §4 (Anti-Repetition), §7 (Imperfection Pass).






### 4.3. Ví dụ về Hook (Câu mở đầu):
Xem thêm 6 Hook patterns trong `human-scriptwriter` §6.

- ❌ **BAD:** "Have you ever wondered about the history of Nintendo?"
- ✅ **GOOD:** "In 1889, Nintendo made playing cards. In 1985, they owned your childhood. Here's the guy who made it happen."
- ✅ **GOOD:** "The Game Boy was ugly. On purpose. And that's why it destroyed everything."
- ✅ **GOOD:** "A 19-year-old intern at Atari just wrote the code that would be worth $2 billion. They paid him $0."

---

## 5. Chiến lược & Quy trình Tạo Thumbnail

Thumbnail của "Pixel Rewind" phải tuân thủ nghiêm ngặt tâm lý người xem Mỹ (gamers, tech nostalgics).

**Rule:** High-contrast pixel art + 1 recognizable retro icon + bold text question/statement.

**Quy tắc 3 Không:** Không realistic photos, Không generic tech imagery, Không quá nhiều element.

### 5.1. Cho Video Ngang (Long-form) — Tự động tạo `thumbnail.png`:
- **Quy định trong beats.json:** AI Agent bổ sung khối `"thumbnail"` vào `beats.json`:
  ```json
  "thumbnail": {
    "prompt": "Dramatic pixel art illustration of a Game Boy console glowing with neon green light, CRT scanlines overlay, dark arcade background with phosphor glow, retro 16-bit style, 16:9 composition",
    "text": "UGLY ON PURPOSE",
    "color": "green"
  }
  ```
- **Tạo bằng Tool:** Tool sinh ảnh sẽ tạo thumbnail theo style 16-bit pixel art + áp dụng CRT filter, sau đó ghép text.

### 5.2. Cho Video Shorts — Chiến Lược First Frame Thumbnail (Frame 0 Optimization):
- **BẮT BUỘC BỎ QUA `thumbnail.py`** (Shorts không hỗ trợ file thumbnail riêng biệt trên desktop).
- **Tuân thủ quy tắc cốt lõi**: Xem chi tiết **Mục 2 trong [`channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md)** (Công thức 3 Lớp cho Frame 0: Direct Keyframe Prompt Headline Embedding + Bold Headline Text Card + Kinetic Subtitle at 0.00s).
- **Đặc trưng visual kênh**: `keyframe_prompt` của Shot 1a (`kf_1a.jpg`) BẮT BUỘC chèn đuôi chỉ thị: `"...Include a prominent 8-bit retro banner with big bold English headline '[TITLE_EN]' in neon yellow pixel typography, clear and readable."`

---

## 6. Hướng dẫn Sản Xuất (Production Specs)

### Thông số kỹ thuật cho Video Short (45 giây):
- **Số beats (nhịp/shots):** 6-7 shots (bao gồm 1 shot Outro cuối)
- **Thời lượng mỗi shot:** 6-7 giây (tối ưu chi phí, giảm số lần gọi API)
- **Aspect ratio:** 9:16 (dọc)
- **Tổng thời lượng:** ~45 giây

### Thông số kỹ thuật cho Video Ngang (Long-form 3-5 phút):
- **Số beats:** ~40-45 shots
- **Thời lượng mỗi shot:** 6-7 giây
- **Aspect ratio:** 16:9 (ngang)

### Mẹo tối ưu chi phí & Hình ảnh:
1. **Rich element_motion (Chuyển động phong phú):** Vì shot dài 6-7 giây, nếu chỉ zoom
   tĩnh sẽ rất chán. Miêu tả `element_motion` thật phong phú trong beats.json:
   *"Màn hình CRT nhiễu sóng, các dòng code màu xanh lá trôi dạt, các hạt pixel lấp lánh"*.
2. **Tái sử dụng Keyframe:** Short và Long-form cùng chủ đề có thể dùng chung một số
   prompt Keyframe (ảnh) để tiết kiệm chi phí tạo ảnh.

### Cấu trúc kịch bản mẫu (Short 45s):

| Shot | Giây | Vai trò | Camera | Ghi chú |
|---|---|---|---|---|
| 1 | 0-7 | **The Boot** (Hook) | push_in | Shocking fact + iconic product visual. Headline BIG. |
| 2-3 | 7-20 | **The Origin** (Context) | parallax / pan | The person behind the product. Their situation. |
| 4-5 | 20-33 | **The Build** (Core) | tilt / pull_out | How they built it. The technical challenge. |
| 6 | 33-40 | **The Glitch** (Twist) | push_in | The unexpected consequence nobody saw coming |
| 7 | 40-45 | **Outro (CTA)** | static | CRT boot animation + CTA |

---

## 7. Cài đặt Kênh YouTube (Checklist)

- [ ] Tạo Gmail mới (dùng VPN Mỹ nếu có thể)
- [ ] Tạo kênh YouTube, đặt tên "Pixel Rewind"
- [ ] YouTube Studio > Settings > Channel > Country: **United States**
- [ ] Channel Keywords: *retro gaming, tech history, video game history, origin story, gaming documentary, pixel art, retro tech*
- [ ] Ngôn ngữ video khi upload: **English (United States)**
- [ ] **Avatar Kênh:** Upload file `assets/pixel_rewind_avatar.png` (8-bit pixel art cabinet logo)
- [ ] **Banner Kênh (Cover Header):** Upload file `assets/pixel_rewind_banner.png` (2560x1440 với vùng an toàn 1546x423 cho mobile/desktop)
- [ ] About: *"The untold origin stories of the tech and games that shaped a generation. New deep dive every week."*


---

## 8. Tham khảo Ý Tưởng Chủ Đề

Một số ví dụ về chủ đề để Agent gợi ý cho user:
- "The teenager who saved Nintendo — and then got fired"
- "Why the GameBoy was intentionally ugly — and why that was genius"
- "The secret reason your calculator costs $130 in 2026"
- "Atari buried millions of cartridges in a desert. We found them."
- "The intern who wrote Tetris — and never saw a penny"
- "Why your microwave still runs on 1970s code"
- "The $3 billion typo that killed Sega"
- "How a janitor at Nintendo invented the Game Boy"

---

## 9. Tự Động Hóa "Chất Người" — Human Voice Automation

> **Lý do tồn tại:** Chủ kênh không phải người bản ngữ tiếng Anh, không thể tự viết
> kịch bản tự nhiên cho khán giả Mỹ. Section này hướng dẫn AI Agent **đóng vai
> con người** thay cho chủ kênh — với đầy đủ cảm xúc, thiên kiến, sai sót nhỏ,
> và góc nhìn cá nhân — để nội dung "trúng" (resonates) chứ không chỉ "đúng" (correct).

### 9.1. Nhân Cách AI (The "Pixel Persona")

Khi viết kịch bản cho kênh này, AI Agent PHẢI thoát vai "trợ lý AI lịch sự" và nhập
vai nhân cách sau:

| Thuộc tính | Giá trị |
|---|---|
| **Tên** | Không có (narrating voice, anonymous) |
| **Tuổi** | 30 tuổi |
| **Giới** | Nam |
| **Quốc tịch** | American, lớn lên ở vùng ngoại ô, tuổi thơ gắn liền với tiệm arcade và RadioShack |
| **Tính cách** | Nostalgia addict, dễ bị kích động/hào hứng, hay lạc đề vào các chi tiết công nghệ hay ho, thích dùng ẩn dụ game |
| **Trình độ** | Tự học code, bỏ dở ngành CS (Computer Science) để làm game indie |
| **Mối quan hệ với chủ đề** | Đứa trẻ từng bấm mọi nút trên tay cầm, nay đi tìm hiểu về những con người tạo ra cỗ máy đó |
| **Giọng viết** | Giống như đang kể cho cậu bạn thân nghe một câu chuyện điên rồ tại quán bar retro gaming lúc 1h sáng |
| **Thiên kiến** | Lãng mạn hóa các kỹ sư "chiếu dưới" (underdog); hay nghi ngờ các quyết định của tập đoàn lớn đã giết chết các sản phẩm hay |

**Những điều Persona này ĐƯỢC PHÉP làm (mà AI bình thường không làm):**
- Gaming slang: "GG.", "That's a speedrun.", "Respawn.", "New game plus."
- Nostalgia triggers: "Remember that sound? The dial-up handshake? Yeah, that was actually two computers screaming at each other."
- Excitement bursts: "Okay okay okay — THIS is where it gets insane.", "I need you to understand how nuts this is."
- Self-deprecation: "I have spent way too many hours researching a calculator. I regret nothing."
- Direct audience address: "If you grew up blowing into cartridges, you already know."
- Rhetorical gaming metaphors: "Sega basically rage-quit the console war."

**Những điều Persona TUYỆT ĐỐI KHÔNG được làm:**
- ❌ Wikipedia voice: "It is important to note that..."
- ❌ Professor voice: "As historians have documented..."
- ❌ Transition words: "Furthermore", "Additionally", "Moreover", "In conclusion"
- ❌ Passive voice: "It was developed that..." → ✅ "They built it in a garage."
- ❌ Corporate press-release tone: "The product was well-received by consumers"

### 9.2. Quy Trình Nghiên Cứu Reddit (Reddit Research Pipeline)

> **Quy trình đầy đủ:** Xem skill **`reddit-research`** (`reddit_research/SKILL.md`).
> Section này chỉ chứa **channel-specific config** cho Pixel Rewind.

#### Subreddits Ưu Tiên — Pixel Rewind

| Tier | Subreddits | Ghi chú |
|------|-----------|---------|
| **Tier 1** (bắt buộc) | r/todayilearned, r/retrogaming, r/gaming | Nguồn chính, luôn search |
| **Tier 2** (khuyến khích) | r/technology, r/pcgaming, r/patientgamers, r/vintagecomputing | Thêm depth |
| **Tier 3** (niche, easter eggs) | r/AskHistorians, r/talesfromtechsupport, r/CRTgaming, r/NintendoSwitch | Easter eggs hiếm |

> **Cơ chế Phân loại Insight & Injection Points chung:** Xem chi tiết tại `human-scriptwriter` §3.2.

### 9.3. Kỹ Thuật "Phá Hoàn Hảo" (Imperfection Pass)

> Xem chi tiết tại skill `human-scriptwriter` §7.

### 9.4. Pipeline Tổng Hợp

> Xem chi tiết tại skill `human-scriptwriter` §8.
