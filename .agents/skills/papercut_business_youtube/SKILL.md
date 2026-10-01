---
name: papercut-business-youtube
description: >
  Chiến lược xây dựng kênh YouTube "Papercut Business" nhắm khán giả Mỹ (US) bằng AI
  phong cách Vox cắt dán giấy. Kích hoạt skill này BẤT CỨ KHI NÀO user yêu cầu:
  viết kịch bản (beats.json), chọn chủ đề cho video, làm thumbnail, tạo Outro,
  đăng video, hoặc bất kỳ công việc nào liên quan đến kênh "Papercut Business",
  series "Everyday Monopolies", hoặc chiến lược YouTube nói chung.
  Triggers: "papercut business", "everyday monopolies", "youtube strategy",
  "viết kịch bản", "beats.json", "thumbnail", "outro", "series",
  "video short", "video ngang", "long-form", "tìm chủ đề", "gợi ý video",
  "topic discovery", "có gì hot", "chủ đề mới".
---

# Papercut Business — YouTube Channel Playbook

Cẩm nang toàn diện để xây dựng kênh YouTube **"Papercut Business"** nhắm tới khán giả
Mỹ (US), sản xuất tự động bằng AI phong cách Vox cắt dán giấy (Paper Collage).

---

## 📌 Phân Định Scope & Kiến Trúc Skill

> ⚠️ **THAM CHIẾU QUY TẮC BẮT BUỘC (HARD CONSTRAINTS):**
> Mọi bước trong Skill này PHẢI tuân thủ nghiêm ngặt:
> - [`.agents/rules/video-production.md`](file:///d:/video-atlas/.agents/rules/video-production.md) — 12 quy tắc production (Provider flowkit, Gates, Duration, Anti-hallucination, Google Flow Safety)
> - [`.agents/rules/channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md) — Tham số kênh (voice, caption, watermark, CRT) + Outro CTA bất biến
> - Kỹ thuật pipeline: xem skill `vox-director` (`vox_papercut_director`)
> - Viết kịch bản giống người: xem skill `human-scriptwriter` (`human_scriptwriter`) — Anti-AI-slop, sensory injection, imperfection pass
> - Nghiên cứu Reddit: xem skill `reddit-research` (`reddit_research`) — Quy trình 5 bước đào insight người thật

* **`papercut-business-youtube` (Skill này):** Chiến lược Nội dung & Thương hiệu Kênh (ngách, phễu, scriptwriting persona, Reddit pipeline, topic discovery, thumbnail).
* **`vox-director`:** Đạo diễn Kỹ thuật & Pipeline Sản xuất (scripts, API calls, ffmpeg assembly).

## 1. Thông tin Kênh (Channel Identity)

| Thuộc tính | Giá trị |
|---|---|
| **Tên kênh** | Papercut Business |
| **Ngách (Micro-niche)** | Hidden Business & Pop Culture Economics — Kinh tế học ngầm & Bí mật các thương hiệu đại chúng Mỹ |
| **Series chính** | "Everyday Monopolies" (Những đế chế độc quyền quanh ta) |
| **Khán giả mục tiêu** | Người Mỹ trưởng thành (25-55+ tuổi), thích xem explainer/mini-documentary |
| **Phong cách hình ảnh** | Vox-style Paper Collage (cắt dán giấy, báo cũ, vintage, halftone) |
| **Ngôn ngữ** | 100% Tiếng Anh (US) |
| **Giọng AI Voice** | xAI TTS, giọng nam trầm ấm tài liệu (ví dụ `leo`), giữ nguyên xuyên suốt tất cả video |

---

## 2. Chiến lược Phễu: Shorts → Long-form

Chiến lược cốt lõi: dùng **YouTube Shorts (45 giây)** làm "cái móc" (hook) kéo traffic
về cho **Video ngang (Long-form 3-5 phút)**.

### 2.1. Thứ Tự SẢN XUẤT: Long-form TRƯỚC, Short SAU

Long-form là "bộ não" — chứa toàn bộ nghiên cứu, data, narrative arc đầy đủ.
Short chỉ là "cái móc câu" rút ra từ Long-form.

**Quy trình sản xuất cho 1 chủ đề:**
1. **Nghiên cứu** Reddit cho chủ đề (dùng Reddit MCP) → viết Long-form.
2. **Viết `beats.json` LONG-FORM** (3-5 phút, ~40 shots) → duyệt kịch bản.
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



Ví dụ Costco Hot Dog:
- **Short:** Chỉ nói về CON SỐ — "$1.50 since 1985, they lose money, CEO threatened
  to kill anyone who raises the price" → kết: "But WHY would a company WANT to lose
  money? Subscribe to Papercut Business..."
- **Long-form:** Đi sâu vào TOÀN BỘ — loss leader → membership psychology → rotisserie
  chicken cùng chiến thuật → so sánh IKEA meatball → kết luận rộng hơn.

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

### 3.1. Hybrid Watermark Logo "Papercut Business" (Chiến lược Logo Đỉnh Cao & Đồng Nhất)

Để đạt được **vừa thẩm mỹ cắt dán Vox cao cấp vừa đồng nhất 100% về vị trí và tỷ lệ**, kênh sử dụng **Giải Pháp Hybrid**:

1. **Phong cách & Prompt tạo Logo PNG Asset (Tạo 1 lần duy nhất):**
   Skill này quy định prompt chuẩn Vox để tạo ảnh logo độc bản:
   > *"A papercut collage sticker logo of the text 'Papercut Business', bold newsprint vintage typography, raw torn paper edges, a piece of translucent Scotch tape at the top corner, subtle halftone dot texture, isolated on pure white background, high-resolution graphic asset."*

   *Cơ chế gọi tool:* Agent sử dụng bộ công cụ phát request (`scripts/provider.py` hoặc FlowKit từ skill `vox-director`) để gửi prompt trên lên `google/nano-banana-2/text-to-image-developer`, sau đó xử lý tách nền (hoặc dùng `remove-background` của `vox-director`) và lưu ảnh PNG trong suốt thu được vào **`assets/papercut_business_watermark.png`**.

2. **Tham số truyền vào beats.json:**
   Khi tạo kịch bản `beats.json`, AI Agent truyền 2 tham số watermark này:
   ```json
   "watermark": "Papercut Business",
   "watermark_image": "assets/papercut_business_watermark.png"
   ```

3. **Cách vận hành & Quy tắc đè Veo Logo:**
   - Skill `papercut_business_youtube` chịu trách nhiệm quy định phong cách logo, prompt tạo logo và truyền tham số `"watermark_image"` vào `beats.json`.
   - **Text Watermark góc phải dưới (`"watermark"`):** BẮT BUỘC dùng đồng nhất `caption_style` với phụ đề (`"paper"`). Được `text_overlay.py` tự động căn chỉnh tọa độ và kích thước riêng cho từng định dạng (16:9 Long-form & 9:16 Short) kèm viền nét stroke và bóng đổ, đảm bảo **100% CHE HOÀN TOÀN LOGO VEO (Google Flow logo)** ở góc phải dưới mà không bị lệch hay lộ viền.
   - Skill `vox-director` (kỹ thuật pipeline) sẽ đọc tham số `"watermark_image"` và `"watermark"` để gọi ffmpeg ghép đè theo đúng quy tắc này.

### 3.2. Signature Outro — Frame Cuối Cùng (BẮT BUỘC trên mọi video)

Mọi video trong series "Everyday Monopolies" PHẢI kết thúc bằng một shot Outro thống
nhất. Đây là "chữ ký" của kênh — khán giả xem nhiều video sẽ nghe đi nghe lại câu
này và tự động liên kết nó với thương hiệu "Papercut Business".

### 3.3. Quy Chuẩn Tạo Channel Banner & Avatar (YouTube Header)

Khi khởi tạo nhận diện kênh "Papercut Business" hoặc người dùng yêu cầu làm bộ Banner/Avatar:

1. **Avatar Kênh (Square 1:1, 800x800 px):**
   - **Prompt:** `"Minimalist torn-paper collage avatar of a globe and gold coin, bold wood-type typography 'PB', raw torn edges, Scotch tape texture, high contrast flat color, isolated center."`
   - **File xuất:** `assets/papercut_business_avatar.png`

2. **Channel Banner Kênh (Cover Header 16:9, 2560x1440 px):**
   - **Kích thước chuẩn:** `2560 x 1440 px` (Full Canvas TV Display).
   - **Vùng an toàn (Desktop & Mobile Safe Zone):** `1546 x 423 px` nằm chính giữa trung tâm.
   - **Prompt Lớp Nền Canvas (2560x1440):** `"Vintage newsprint paper collage banner with torn edges, halftone dots, subtle financial chart graphics, Vox editorial paper style, wide 16:9 composition."`
   - **Lớp Chữ Vùng An Toàn (Safe Zone 1546x423):** 
     - **Tên Kênh Khổng Lồ:** "PAPERCUT BUSINESS" (Font chữ wood-type thủ công / torn paper cut-outs).
     - **Tagline Khẩu Hiệu:** "EVERYDAY MONOPOLIES & HIDDEN ECONOMICS"
     - **Lịch Đăng Video:** "NEW EPISODES WED & SAT" (Thứ 4 & Thứ 7 hàng tuần)
   - **File xuất:** `assets/papercut_business_banner.png`

---

## 4. Nguyên tắc Viết Kịch Bản

> Quy tắc viết kịch bản cơ bản (anti-AI-slop, staccato, sensory injection, imperfection pass): xem skill `human-scriptwriter`. Phần dưới chỉ chứa các quy tắc RIÊNG cho kênh Papercut Business.

### 4.1. Ba nhóm nội dung YouTube hạn chế trong YPP (phải tránh):
1. **Generic and Repetitive**
2. **Off-putting or Distressing**
3. **AI Personas trong lĩnh vực nhạy cảm**

### 4.2. Các quy tắc khi viết kịch bản (beats.json):

**① Dấu vân tay tác giả (The "Reddit Trick"):**
- Mọi kịch bản phải chứa một góc nhìn độc bản.
- Mang câu hỏi đó lên Reddit tìm những bình luận sắc sảo đời thực, chắt lọc rồi bắt AI chèn mượt mà vào kịch bản.

**② Hạ Thẩm Quyền Trần Thuật (Lowering Authority):**
- Đổi giọng thành người tiêu dùng tò mò: ✅ "I always wondered why Costco...", ✅ "Turns out, we've been tricked...".

**③ Hook (Câu Mồi) do người viết:**
- Ví dụ tốt: "Costco loses millions on hot dogs every year. And they absolutely love it."
- Xem đầy đủ 6 Hook patterns trong `human-scriptwriter` §6.

**④⑤ Staccato Pacing & Imperfection:** Xem chi tiết trong skill `human-scriptwriter` §2 (Blacklist), §4 (Anti-Repetition), §7 (Imperfection Pass).

---

## 5. Chiến lược & Quy trình Tạo Thumbnail

Thumbnail của "Papercut Business" phải tuân thủ nghiêm ngặt tâm lý người xem Mỹ trưởng thành (25-55+ tuổi): họ chán ngấy sự lòe loẹt giả tạo.

**Quy tắc 3 Không:** Không màu mè rực rỡ, Không mặt cường điệu há hốc mồm, Không clickbait lấp lửng.

### 5.1. Cho Video Ngang (Long-form) — Tự động tạo `thumbnail.png`:
- **Quy định trong beats.json:** AI Agent bổ sung khối `"thumbnail"` vào `beats.json`:
  ```json
  "thumbnail": {
    "prompt": "A high-contrast editorial paper collage poster thumbnail about Costco hot dog, bold newsprint typography, vintage torn paper edges, Scotch tape, halftone texture, striking central photographic cut-out object, american-retro aesthetic, 16:9 composition",
    "text": "THE $1.50 SECRET",
    "color": "yellow"
  }
  ```
- **Tạo bằng Tool:** Chạy script `python3 scripts/thumbnail.py out/<project>`.
  - Script sẽ tạo ảnh gốc 16:9 2K Vox poster bằng AI Model (`google/nano-banana-2/text-to-image-developer` hoặc FlowKit).
  - Tự động đè chữ tiêu đề 3-5 từ màu vàng/trắng tương phản siêu mạnh.
  - Tự động thêm hiệu ứng **nhiễu hạt nhiễu tạp (film grain filter)** để triệt tiêu sự trơn mượt AI (Uncanny Valley), giúp thumbnail trông như báo in thật.
  - Xuất file kết quả tại **`out/<project>/thumbnail.png`**.

### 5.2. Cho Video Shorts — Chiến Lược First Frame Thumbnail (Frame 0 Optimization):
- **BẮT BUỘC BỎ QUA `thumbnail.py`** (Shorts không hỗ trợ file thumbnail riêng biệt trên desktop).
- **Tuân thủ quy tắc cốt lõi**: Xem chi tiết **Mục 2 trong [`channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md)** (Công thức 3 Lớp cho Frame 0: Direct Keyframe Prompt Headline Embedding + Bold Headline Text Card + Kinetic Subtitle at 0.00s).
- **Đặc trưng visual kênh**: `keyframe_prompt` của Shot 1a (`kf_1a.jpg`) BẮT BUỘC chèn đuôi chỉ thị: `"...Include a torn-paper banner with a big bold cut-out English headline '[TITLE_EN]' in bold wood-type / heavy slab, all-caps. Keep the headline crisp and legible."`

---

## 6. Hướng dẫn Sản Xuất (Tối ưu Ngân sách Vox-Director)


### Mẹo tối ưu chi phí:
1. **Rich element_motion (Chuyển động phong phú):** Vì shot dài 6-7 giây, nếu chỉ zoom
   tĩnh sẽ rất chán. Miêu tả `element_motion` thật phong phú trong beats.json:
   *"Bảng mạch điện tử lóe sáng, các con số trôi nổi lơ lửng, tờ đô la giấy bay ngang
   qua màn hình, halftone nhấp nháy"*.
2. **Tái sử dụng Keyframe:** Short và Long-form cùng chủ đề có thể dùng chung một số
   prompt Keyframe (ảnh) để tiết kiệm chi phí tạo ảnh.
3. **Luôn dùng Draft Mode:** Chạy `python3 scripts/draft.py` trước để nghe thử pacing
   (nhịp đọc) của Voice-over. Chỉ chi tiền cho motion (clips.py) khi đã ưng ý hoàn toàn.

### Cấu trúc kịch bản mẫu (Short 45s):

| Shot | Giây | Vai trò | Camera | Ghi chú |
|---|---|---|---|---|
| 1 | 0-7 | **The Hook** (Câu mồi) | push_in | Sự thật gây sốc. Headline TO. Chuyển động mạnh ở 2s đầu |
| 2-3 | 7-20 | **The Context** (Bối cảnh) | parallax / pan | Thiết lập logic, cung cấp thông tin nền |
| 4-5 | 20-33 | **The Meat** (Nội dung chính) | tilt / pull_out | Giải thích cốt lõi vấn đề |
| 6 | 33-40 | **The Twist** (Bí mật) | push_in | Thông tin bất ngờ 99% không biết |
| 7 | 40-45 | **Outro (CTA)** | static | Logo series + CTA cố định (xem mục 3) |

---

## 7. Cài đặt Kênh YouTube (Checklist)

- [ ] Tạo Gmail mới (dùng VPN Mỹ nếu có thể)
- [ ] Tạo kênh YouTube, đặt tên "Papercut Business"
- [ ] YouTube Studio > Settings > Channel > Country: **United States**
- [ ] Channel Keywords: *business secrets, mini documentary, economics, video essay,
  company history, everyday monopolies*
- [ ] Ngôn ngữ video khi upload: **English (United States)**
- [ ] Avatar & Banner: Phong cách cắt dán giấy (Collage), nhất quán với video
- [ ] About: *"Bite-sized documentaries unraveling the hidden economics of everyday
  life. New video every week."*

---

## 8. Tham khảo Kinh nghiệm Thực chiến

File `youtube-real-experience.txt` trong workspace chứa kinh nghiệm thực tế từ một
YouTuber thành công. Các bài học then chốt đã được tích hợp vào skill này:

- **"Phép thử 10 phút":** Nếu người khác cầm đúng công cụ, đúng chủ đề, ra video
  y chang bạn trong 10 phút → video đó vô giá trị dù không dùng AI.
- **Garbage In, Garbage Out:** Prompt chỉ là cái "Xẻng". Insight (ý tưởng cốt lõi) mới
  là mỏ vàng. Siêu Prompt không cứu nổi nội dung dở.
- **Ngách trong Ngách (Micro-niche):** Đừng làm "Kinh doanh" (chủ đề). Hãy làm
  "Bí mật độc quyền của những thương hiệu Mỹ quen thuộc" (micro-niche). Ít đối thủ,
  khán giả trung thành vì thấy bản thân trong đó.
- **Uncanny Valley trong kịch bản:** Kịch bản AI quá hoàn hảo = vô hồn = buồn ngủ.
  Khán giả thèm khát sự thô ráp. Cảm xúc sinh ra từ sự bất toàn.

---

## 9. Tự Động Hóa "Chất Người" — Human Voice Automation

> **Lý do tồn tại:** Chủ kênh không phải người bản ngữ tiếng Anh, không thể tự viết
> kịch bản tự nhiên cho khán giả Mỹ. Section này hướng dẫn AI Agent **đóng vai
> con người** thay cho chủ kênh — với đầy đủ cảm xúc, thiên kiến, sai sót nhỏ,
> và góc nhìn cá nhân — để nội dung "trúng" (resonates) chứ không chỉ "đúng" (correct).

### 9.1. Nhân Cách AI (The "Papercut Persona")

Khi viết kịch bản cho kênh này, AI Agent PHẢI thoát vai "trợ lý AI lịch sự" và nhập
vai nhân cách sau:

| Thuộc tính | Giá trị |
|---|---|
| **Tên** | Không có (narrating voice, anonymous) |
| **Tuổi** | 32-38 tuổi |
| **Giới** | Nam |
| **Quốc tịch** | Mỹ, lớn lên ở vùng ngoại ô (suburbs) |
| **Tính cách** | Tò mở, hơi hoài nghi, hay bức xúc nhẹ về bất công giá cả |
| **Trình độ** | College-educated nhưng KHÔNG phải chuyên gia kinh tế |
| **Mối quan hệ với chủ đề** | Người tiêu dùng bình thường bỗng phát hiện "trò lừa" |
| **Giọng viết** | Như đang kể chuyện cho bạn bè trong quán bar, không phải đọc báo cáo |
| **Thiên kiến** | Thiên về phía người tiêu dùng, nghi ngờ tập đoàn lớn |

**Những điều Persona này ĐƯỢC PHÉP làm (mà AI bình thường không làm):**
- Dùng từ lóng Mỹ: "That's nuts.", "No way.", "Wild, right?", "Dude.", "Legit."
- Thể hiện bức xúc: "And they charge HOW MUCH for that?", "This is borderline criminal."
- Có ý kiến cá nhân: "Honestly? I respect the hustle." / "I kinda hate that this works."
- Thỉnh thoảng tự mâu thuẫn nhẹ: "I mean, I still buy their stuff. So who's the real clown here?"
- Dùng câu cảm thán ngắn cụt: "Insane.", "Just... wow.", "Think about that."
- Đặt câu hỏi tu từ như đang nói chuyện: "But here's the weird part — why would they WANT to lose money?"

**Những điều Persona TUYỆT ĐỐI KHÔNG được làm:**
- ❌ Nói giọng Wikipedia: "It is important to note that..."
- ❌ Nói giọng professor: "As economists have observed..."
- ❌ Dùng transition words máy móc: "Furthermore", "Additionally", "In conclusion"
- ❌ Dùng passive voice quá nhiều: "It was determined that..." → ✅ "They figured out..."
- ❌ Nói quá cân bằng: "On one hand... on the other hand..." → ✅ Chọn 1 phe rồi thách thức nó

### 9.2. Quy Trình Nghiên Cứu Reddit (Reddit Research Pipeline)

> **Quy trình đầy đủ:** Xem skill **`reddit-research`** (`reddit_research/SKILL.md`).
> Section này chỉ chứa **channel-specific config** cho Papercut Business.

#### Subreddits Ưu Tiên — Papercut Business

| Tier | Subreddits | Ghi chú |
|------|-----------|---------|
| **Tier 1** (bắt buộc) | r/todayilearned, r/PersonalFinance, r/Economics, r/explainlikeimfive | Nguồn chính, luôn search |
| **Tier 2** (khuyến khích) | r/Anticonsumption, r/business, r/investing, r/dataisbeautiful | Thêm depth |
| **Tier 3** (niche — insider stories) | Subreddits chuyên ngành theo chủ đề: r/Costco, r/starbucks, r/walmart, r/fastfood, v.v. | Insider stories |

#### Phân Loại Insight — Papercut Business

| Nhóm | Mô tả | Ví dụ | Dùng ở đâu |
|------|--------|-------|------------|
| **Insider Story** | Nhân viên/người trong cuộc kể chuyện | *"I worked there 3 years. The rotisserie chicken is the same deal."* | Context / "người trong cuộc" |
| **Obscure Claim** | Tuyên bố hiếm, khó verify, gây tò mò | *"The CEO literally threatened to kill someone over the hot dog price"* | Easter Egg Trick |
| **Counterintuitive Stat** | Số liệu trái trực giác | *"They lose $40M/year on hot dogs but make $4B from memberships"* | Hook / Opening |
| **Emotional Reaction** | Phản ứng cảm xúc mạnh | *"This genuinely pisses me off"* / *"Genius move tbh"* | Twist / Shift tone |
| **Contrarian View** | Góc nhìn phản biện, tranh cãi | *"Actually it's not a loss leader, it's a membership retention tool"* | Nuance / Depth |

#### Injection Points — Papercut Business

| Format | Injection Point | Loại insight phù hợp |
|--------|----------------|---------------------|
| **Short (7 shots)** | Shot 1 (Hook) | Counterintuitive Stat / Shocking fact |
| | Shot 2-3 (Context) | Insider Story / "người trong cuộc" |
| | Shot 4-5 (Meat) | Logic/phản biện từ thread tranh luận |
| | Shot 6 (Twist) | Obscure Claim từ niche subreddit |
| **Long-form (20+ beats)** | Beat 1 (Hook) | Counterintuitive Stat / Shocking stat |
| | Beat 4-6 (Core Story) | Insider Story / Emotional Reaction |
| | Beat 15-17 (Escalation) | Contrarian View / Nuance |
| | Beat 20-21 (Payoff) | Obscure Claim (Easter Egg) + Self-aware humor |

#### Ví dụ Transform — Papercut Business

Kỹ thuật chuyển đổi Reddit → narration: xem `human-scriptwriter` §3.2.


### 9.3. Kỹ Thuật "Phá Hoàn Hảo" (Imperfection Injection)

> Imperfection Pass checklist: xem `human-scriptwriter` §7.


### 9.4. Pipeline Tổng Hợp — Thay Thế Con Người Trong Quy Tắc 70/30

> Quy trình tích hợp: xem `human-scriptwriter` §8.


### 9.5. Ví Dụ: Agent Tự Nghiên Cứu Chủ Đề Mới

Khi chủ kênh nói: **"Làm video về Costco Hot Dog"**, Agent thực hiện:

```
1. [RESEARCH] Dùng Reddit MCP search "Costco hot dog" trên r/Costco, r/todayilearned, r/Economics, r/Anticonsumption
2. [HARVEST] Chọn 5 bình luận có insight/cảm xúc mạnh nhất
3. [TRANSFORM] Viết lại bằng giọng Persona (32 tuổi, suburbs, tò mò, hơi bức xúc)
4. [DRAFT] Viết beats.json theo cấu trúc Short 45s (Section 6)
5. [INJECT] Chèn Reddit insights vào đúng vị trí (Hook/Context/Meat/Twist)
6. [IMPERFECTION] Chạy Imperfection Pass
7. [REVIEW] Xuất kịch bản cho chủ kênh duyệt
8. [PRODUCE] Sau khi duyệt → chuyển beats.json sang vox-director để sản xuất
```

---

## 10. Tự Động Tìm Chủ Đề Mới Từ Reddit (Topic Discovery Engine)

> **Khi nào kích hoạt:** Chủ kênh nói: "Tìm chủ đề mới", "Gợi ý video tiếp theo",
> "Có gì hot trên Reddit không?", hoặc bất kỳ yêu cầu brainstorm chủ đề nào.

### 10.1. Subreddit Mục Tiêu — "Mỏ Vàng" Chủ Đề

Agent quét các subreddit sau để tìm chủ đề phù hợp với ngách "Hidden Business &
Pop Culture Economics":

| Tier | Subreddits | Tại sao |
|---|---|---|
| **Tier 1 — Trực tiếp** | `todayilearned`, `Damnthatsinteresting`, `interestingasfuck`, `explainlikeimfive` | Nơi sự thật gây sốc viral. Post 10K+ upvotes = chủ đề đã được validate |
| **Tier 2 — Kinh tế/Business** | `Economics`, `Anticonsumption`, `LateStageCapitalism`, `PersonalFinance`, `Frugal` | Góc nhìn bức xúc về giá cả, độc quyền, chiến thuật doanh nghiệp |
| **Tier 3 — Brand cụ thể** | `Costco`, `walmart`, `Starbucks`, `McDonalds`, `Target`, `IKEA`, `apple` | Trải nghiệm người tiêu dùng thật, drama nội bộ, tin rò rỉ |
| **Tier 4 — Pop Culture** | `NoStupidQuestions`, `OutOfTheLoop`, `YouShouldKnow`, `AskReddit` | Câu hỏi triệu view kiểu "Why is X so expensive?" |

### 10.2. Quy Trình Quét Tự Động (Auto-Scan Pipeline)

```
Bước 1: [SCAN]     Quét Tier 1-4, sort "top", time "month" hoặc "week"
Bước 2: [FILTER]   Lọc theo tiêu chí ngách (xem 10.3)
Bước 3: [SCORE]    Chấm điểm virality (xem 10.4)
Bước 4: [DEEP]     Đào sâu top 5 → đọc comments tìm góc nhìn độc
Bước 5: [PRESENT]  Xuất bảng xếp hạng cho chủ kênh chọn
```

**Lệnh quét chi tiết:**

```
# Tier 1 — Sự thật gây sốc
Tool: reddit_search
→ query: "company secretly" OR "you're paying for" OR "reason why" OR "monopoly"
   OR "loss leader" OR "planned obsolescence" OR "price fixing"
→ subreddit: (để trống = search toàn Reddit)
→ sort: "top" | time: "month" | limit: 25

# Tier 2 — Kinh tế
Tool: reddit_get_subreddit
→ subreddit: "Anticonsumption" | type: "top" | time: "week" | limit: 15
→ subreddit: "todayilearned" | type: "top" | time: "week" | limit: 15

# Tier 4 — Câu hỏi triệu view
Tool: reddit_search
→ query: "why is * so expensive" OR "why does * cost" OR "how does * make money"
→ sort: "top" | time: "month" | limit: 20
```

### 10.3. Bộ Lọc Chủ Đề — 5 Tiêu Chí Phải Đạt

Mỗi chủ đề tiềm năng PHẢI đạt **ít nhất 4/5** tiêu chí:

| # | Tiêu chí | Ví dụ ĐẠT | Ví dụ TRƯỢT |
|---|---|---|---|
| ① | **Quen thuộc với người Mỹ** — thương hiệu/sản phẩm mà 80%+ người Mỹ biết | Costco, TI-84, Starbucks | Mì Hảo Hảo, Vinamilk |
| ② | **Có "bí mật" ẩn sau** — sự thật mà đa số không biết | "Costco lỗ tiền trên mỗi hot dog" | "Costco bán hot dog" (ai cũng biết, không có twist) |
| ③ | **Gây cảm xúc** — bức xúc, ngạc nhiên, hoặc khâm phục | "TI-84 giá $120 suốt 30 năm vì Texas Instruments lobbied trường học" | "Lịch sử máy tính bỏ túi" (nhàm) |
| ④ | **Có data/con số cụ thể** — để làm Hook mạnh | "$1.50 since 1985", "90% market share" | "Costco có chiến lược hay" (mơ hồ) |
| ⑤ | **Phù hợp phong cách Vox Collage** — có thể minh họa bằng cắt dán giấy | Hóa đơn, sản phẩm, logo, biểu đồ | Thuật toán trừu tượng, code |

### 10.4. Chấm Điểm Virality (1-10)

Agent tự chấm mỗi chủ đề theo công thức:

```
VIRALITY = (Reddit_Engagement × 0.3) + (Hook_Strength × 0.3)
         + (Emotion_Trigger × 0.2) + (Visual_Potential × 0.2)
```

| Yếu tố | Cách chấm |
|---|---|
| **Reddit_Engagement** | Upvotes post gốc: <1K = 3đ, 1-5K = 5đ, 5-20K = 7đ, 20K+ = 9đ; Số comments tranh luận sôi nổi +1đ |
| **Hook_Strength** | Có thể viết câu Hook ≤15 từ gây sốc không? Có = 8-10đ, Phải giải thích dài = 4-6đ |
| **Emotion_Trigger** | Gây bức xúc (giá cả bất công) = 9đ, Gây ngạc nhiên (sự thật lạ) = 7đ, Chỉ thú vị = 5đ |
| **Visual_Potential** | Có sản phẩm/logo iconic để cắt dán = 9đ, Chỉ có khái niệm trừu tượng = 4đ |

### 10.5. Danh Sách "Đã Làm" — Tránh Trùng Lặp

Agent PHẢI kiểm tra thư mục `out/` trước khi đề xuất. Nếu đã có project folder
cho chủ đề đó → đánh dấu "ĐÃ LÀM" và không đề xuất lại.

```
Tool: Kiểm tra thư mục out/
→ Liệt kê tất cả project folders
→ So sánh với chủ đề đề xuất
→ Loại bỏ trùng lặp
```

### 10.6. Output: Bảng Xếp Hạng Chủ Đề

Agent xuất kết quả dạng bảng để chủ kênh dễ chọn:

```markdown
| # | Chủ đề | Virality | Hook mẫu | Nguồn Reddit |
|---|--------|---------|----------|--------------|
| 1 | TI-84 Calculator Monopoly | 9.2/10 | "This $120 calculator hasn't changed since 1994. Here's why it never will." | r/todayilearned (47K upvotes) |
| 2 | Why Movie Popcorn Costs $9 | 8.7/10 | "Movie theaters make 85% profit on popcorn. The movie? They barely break even." | r/explainlikeimfive (31K) |
| 3 | IKEA's Meatball Strategy | 8.1/10 | "IKEA sells 2 billion meatballs a year. They're not a furniture company." | r/Damnthatsinteresting (22K) |
| 4 | Printer Ink: Liquid Gold | 7.8/10 | "Printer ink costs more per ounce than human blood. And HP made sure of it." | r/Anticonsumption (18K) |
| 5 | Why Gas Prices End in 9/10 | 7.3/10 | "That extra 9/10 of a cent? It's been legal since 1933." | r/NoStupidQuestions (12K) |
```

Chủ kênh chọn 1 chủ đề → Agent tự động chuyển sang quy trình sản xuất (Section 9.5).

### 10.7. Prompt Mẫu Cho Chủ Kênh

```
# Tìm chủ đề mới — full scan
Tìm 5 chủ đề video mới cho Papercut Business. Quét Reddit, chấm điểm virality.

# Tìm chủ đề theo hướng cụ thể
Tìm chủ đề về ngành fast food cho Papercut Business. Quét Reddit.

# Tìm chủ đề trending tuần này
Có gì hot trên Reddit tuần này phù hợp kênh Papercut Business không?

# Tìm + làm luôn
Tìm chủ đề mới và làm video cho chủ đề hay nhất.
```
