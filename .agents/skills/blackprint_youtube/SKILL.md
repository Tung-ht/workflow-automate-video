---
name: blackprint-youtube
description: >
  Chiến lược xây dựng kênh YouTube "Blackprint" nhắm khán giả toàn cầu (Global English)
  bằng AI phong cách Bản vẽ 3D X-Ray Hắc Ám (Blueprint Noir). Kích hoạt BẤT CỨ KHI NÀO
  user yêu cầu: viết kịch bản (beats.json), chọn chủ đề, làm thumbnail, tạo Outro,
  hoặc bất kỳ công việc nào liên quan đến kênh "Blackprint", series "Deconstructed",
  hoặc chiến lược kênh giải phẫu kỹ thuật / siêu công trình / vũ khí / kỳ quan.
  Triggers: "blackprint", "blueprint noir", "deconstructed", "bản vẽ 3d", "giải phẫu vũ khí",
  "siêu công trình", "kỳ quan cổ đại", "tạo video blackprint", "bản vẽ kỹ thuật".
---

# Blackprint — YouTube Channel Playbook

Cẩm nang toàn diện để xây dựng kênh YouTube **"Blackprint"** nhắm tới khán giả toàn cầu
(Global English), sản xuất tự động bằng AI phong cách Bản vẽ 3D X-Ray Hắc Ám (Blueprint Noir).

---

## 📌 Phân Định Scope & Kiến Trúc Skill

> ⚠️ **THAM CHIẾU QUY TẮC BẮT BUỘC (HARD CONSTRAINTS):**
> Mọi bước trong Skill này PHẢI tuân thủ nghiêm ngặt:
> - [`.agents/rules/video-production.md`](file:///d:/video-atlas/.agents/rules/video-production.md) — 17 quy tắc production bắt buộc
> - [`.agents/rules/channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md) — Tham số kênh (voice `leo`, caption `white`, watermark) + Outro CTA bất biến
> - Kỹ thuật pipeline hình ảnh: xem skill `blueprint-noir-director` (`blueprint_noir_director`)
> - Viết kịch bản giống người: xem skill `human-scriptwriter` (`human_scriptwriter`) — Anti-AI-slop, sensory injection, imperfection pass
> - Nghiên cứu Reddit: xem skill `reddit-research` (`reddit_research`) — Quy trình 5 bước đào insight người thật

* **`blackprint-youtube` (Skill này):** Chiến lược Nội dung & Thương hiệu Kênh (ngách, phễu, persona, Reddit research, topic discovery, thumbnail).
* **`blueprint-noir-director`:** Đạo diễn Kỹ thuật & Pipeline Hình ảnh (3D isometric prompts, color presets, CAD overlays, motion integrity, ffmpeg assembly).

---

## 1. Thông tin Kênh (Channel Identity)

| Thuộc tính | Giá trị |
|---|---|
| **Tên kênh** | `Blackprint` |
| **Ngách (Micro-niche)** | Universal 3D X-Ray Schematics & Megastructures (Công trình, Cỗ máy, Vũ khí, Kỳ quan Cổ đại đến Tương lai) |
| **Series chính** | *"Deconstructed"* (Giải Phẫu 3D) |
| **Khán giả mục tiêu** | Khán giả toàn cầu (16–50 tuổi, mê kỹ thuật, vũ khí, lịch sử, kỳ quan, sci-fi, cơ khí) |
| **Phong cách hình ảnh** | **Blueprint Noir** (Deep Slate Navy `#0B192C` + Cyan Wireframe `#00F0FF` + Neon Yellow `#FFDE59`) |
| **Ngôn ngữ** | `English (United States)` — 100% Tiếng Anh toàn cầu |
| **Giọng AI Voice** | xAI TTS, giọng nam trầm ấm tài liệu điện ảnh (`leo`) |
| **Lịch đăng video** | 2 video / tuần (Thứ 3 & Thứ 6 hàng tuần — Tue & Fri) |

---

## 2. Chiến Lược Phễu & Định Dạng Video (Shorts 70s → Long-Form 10 Phút)

### 2.1. Không Giới Hạn Chi Phí — Ưu Tiên Chất Lượng & Chi Tiết Tuyệt Đối
* **Không giới hạn số lượng frame, shot hay sub-clips:** Kênh không chạy theo việc cắt giảm chi phí. Mọi chi tiết kỹ thuật cần thiết để giải thích cặn kẽ công trình đều phải được tạo đầy đủ.
* **Thời lượng linh hoạt mở rộng:**
  * **Video Long-form:** Độ dài có thể lên đến **tối đa 10 phút** (tùy thuộc vào độ phức tạp của công trình/cỗ máy, từ 40 đến 80+ shots chi tiết).
  * **Video Shorts:** Độ dài mở rộng lên đến **tối đa 70 giây** (cho phép truyền tải trọn vẹn 1 cơ chế kỹ thuật hoàn chỉnh mà không bị vội).

### 2.2. Cấu Trúc Hybrid: Kết Hợp Ảnh Tĩnh Độ Nét Cao & Video Chuyển Động Hợp Lý
* **Video final là sự kết hợp nhịp nhàng giữa Ảnh tĩnh (Static Schematics) và Video Clips ngắn:**
  * **Ảnh tĩnh chất lượng cao (Static Shots):** Dành cho các bản vẽ tổng thể phức tạp, các sơ đồ cấu trúc đa tầng. Script `assemble.py` sẽ áp dụng hiệu ứng camera trượt nhẹ (pan/zoom tinh tế) và lớp chữ vector overlay sắc nét để người xem chiêm ngưỡng toàn bộ bản vẽ mà không bị biến dạng hình học.
  * **Video Clips động (Dynamic Google Flow Clips):** Dành riêng cho các phân đoạn cần mô phỏng **luồng chuyển động vật lý thực tế** (dòng nước chảy qua van, pít-tông trích khí di chuyển, thanh nhiên liệu hạ vào lõi phản ứng, tia quét radar).

### 2.3. Thứ Tự Sản Xuất & Đăng Video
1. **Nghiên cứu kỹ thuật:** Quét Reddit (`r/EngineeringPorn`, `r/MachinePorn`, `r/ThingsCutInHalfPorn`, `r/MilitaryPorn`, `r/CatastrophicFailure`) thu thập sơ đồ kỹ thuật và số liệu vật lý chính xác.
2. **Viết `beats.json` Long-form (5–10 phút):** Mổ xẻ từng lớp từ ngoài vào trong.
3. **Sản xuất Long-form** $\rightarrow$ `final.mp4` + `thumbnail.png`.
4. **Viết `beats.json` Short (55–70s):** Rút trích 1 cơ chế giật gân nhất làm Short 9:16.
5. **Sáng ngày N đăng Long-form, Chiều/Tối đăng Short kèm Related Video.**

---

## 3. Dấu Ấn Thương Hiệu (Brand Identity & Consistency)

### 3.1. Watermark Logo "Blackprint"
* **Prompt sinh logo PNG asset:**
  `"A glowing neon architectural CAD badge sticker logo of the text 'Blackprint', sleek technical typography, electric cyan and gold wireframe vector accents, deep charcoal slate background, high-resolution graphic asset, isolated center on pure black background."`
* **Asset path:** `assets/blackprint_watermark.png`
* **Tham số trong beats.json:**
  ```json
  "watermark": "Blackprint",
  "watermark_image": "assets/blackprint_watermark.png"
  ```

### 3.2. Signature Outro — Frame Cuối Cùng (BẤT BIẾN)
* **Shorts CTA:** *"Every machine has a secret. Subscribe to Blackprint to unlock the next 3D file."*
* **Long-form CTA:** *"From ancient ruins to forbidden megaprojects, human ambition is written in the blueprints. Subscribe to Blackprint for the next deconstruction."*
* **Hình ảnh Outro:** Bản vẽ Blueprint Noir tĩnh + Dòng chữ phát sáng *"TO BE CONTINUED... SUBSCRIBE TO BLACKPRINT"*. Camera LUÔN TĨNH.

### 3.3. Avatar & Banner Kênh YouTube
* **Avatar (1:1, 800x800 px):**
  - *Prompt:* `"Minimalist glowing technical vector avatar of an isometric 3D wireframe cube intersecting a gear, electric cyan and neon yellow outlines, dark navy slate background, crisp CAD precision, centered."`
  - *File xuất:* `assets/blackprint_avatar.png`
* **Channel Banner (16:9, 2560x1440 px):**
  - *Prompt Canvas (2560x1440):* `"Epic wide 16:9 technical blueprint banner featuring layered 3D isometric wireframes of a nuclear submarine, a rocket engine, and an ancient pyramid cutaway, glowing electric cyan and amber telemetry on dark navy slate background, cinematic noir lighting."`
  - *Safe Zone Text (1546x423 px trung tâm):*
    - **Tên kênh:** "BLACKPRINT" (Font chữ kỹ thuật khối dày / Heavy Industrial Tech Sans).
    - **Tagline:** "UNIVERSAL 3D SCHEMATICS & MEGASTRUCTURES"
    - **Lịch đăng:** "NEW EPISODES TUE & FRI"
  - *File xuất:* `assets/blackprint_banner.png`

---

## 4. Nguyên Tắc Kịch Bản & Độ Chính Xác Kỹ Thuật

### 4.1. Phân Bổ Nội Dung 30 / 70
* **30% Chủ đề Mồi (Proven Giants):** Chernobyl, Tàu ngầm hạt nhân, B-2 Stealth, Kim tự tháp, Titanic $\rightarrow$ Đón đầu hàng triệu lượt tìm kiếm và ăn đề xuất từ đối thủ.
* **70% Chủ đề Độc Lạ Chưa Từng Thấy (Untapped Secrets):** Project Iceworm, Project Pluto, Bê tông La Mã tự vá, Tàu hỏa hạt nhân Xô Viết, Pháo hơi nước Archimedes $\rightarrow$ Tạo bản sắc độc quyền không kênh nào có.

### 4.2. 5 Quy Tắc Scripting Đòi Hỏi Độ Chính Xác Cao
1. **Rule ① — The Micro-Mechanism Hook:** Mở đầu bằng một cơ chế vật lý có thật, chính xác đến từng chi tiết *(e.g. "A nuclear submarine doesn't carry oxygen tanks from land. It continuously generates air by splitting purified seawater using 2,000-volt electrolysis cells.")*.
2. **Rule ② — Layer-by-Layer Deconstruction:** Bóc tách chính xác vị trí các khoang theo sơ đồ thực tế (vỏ kép chịu áp lực $\rightarrow$ khoang chỉ huy $\rightarrow$ lò phản ứng $\rightarrow$ tuabin hơi nước).
3. **Rule ③ — Concrete Metric Anchors:** Luôn neo chặt thông số kỹ thuật thực tế *(12,000 PSI, Mach 3.2, 2,000°C, 36,000 km, 18,000 tấn)*.
4. **Rule ④ — The Fatal Flaw / Engineering Truth:** Phân tích chính xác nguyên nhân kỹ thuật gốc rễ của sự cố hoặc lý do dự án bị hủy bỏ.
5. **Rule ⑤ — Hard Cut Cliffhanger (Shorts) & Deep Masterclass Conclusion (Long-form).**

---

## 5. Chiến Lược Thumbnail

### 5.1. Long-form Thumbnail (16:9 Blueprint Poster)
* **Quy định trong beats.json:**
  ```json
  "thumbnail": {
    "prompt": "A striking 3D isometric cutaway poster of [SUBJECT] in Blueprint Noir style, deep navy background with glowing electric cyan wireframes, dramatic neon yellow arrows pointing to secret internal chamber, high contrast technical annotations, cinematic lighting, 16:9 composition",
    "text": "WHAT'S INSIDE?",
    "color": "yellow"
  }
  ```
* **Script tạo:** `python3 scripts/thumbnail.py out/<project>`.

### 5.2. Shorts — Chiến Lược First Frame Thumbnail (Frame 0)
* **Chỉ thị bắt buộc tại Shot 1a (`kf_1a.jpg`):**
  `"...Include a prominent technical CAD title banner with big bold English headline '[TITLE_EN]' in crisp electric-cyan and neon-yellow typography, highly visible and legible against the dark blueprint grid."`

---

## 6. Hướng Dẫn Kịch Bản & Cấu Trúc Khung Hình

### Cấu Trúc Kịch Bản Long-Form Mẫu (8–10 phút, ~50–70 shots):
* **Phần 1 (0:00 – 1:30):** Bí ẩn không gian & Bối cảnh kỹ thuật (Hook + Macro Isometric View).
* **Phần 2 (1:30 – 4:00):** Giải phẫu từng khoang/chi tiết lớp ngoài (Static & Pan Shots).
* **Phần 3 (4:00 – 7:00):** Trái tim cỗ máy: Lõi năng lượng / Động cơ / Cơ chế vận hành (Dynamic Google Flow Motion Clips).
* **Phần 4 (7:00 – 9:00):** Giới hạn vật lý, Điểm yếu chết người hoặc Thảm họa kỹ thuật.
* **Phần 5 (9:00 – 10:00):** Kết luận tham vọng nhân loại + Signature Outro CTA.

---

## 7. Cài Đặt Kênh YouTube (Checklist)

- [ ] Tên kênh: **Blackprint**
- [ ] Country: **United States** (hoặc Global English)
- [ ] Category: **Science & Technology** hoặc **Education**
- [ ] Description: *"Deconstructing history's deadliest weapons, impossible megaprojects, and lost ancient machines in 3D. New schematics unlocked every week."*
- [ ] Channel Keywords: *3d animation, how it works, blueprints, engineering breakdown, nuclear submarine, classified weapons, ancient technology, megastructures, deconstructed*
- [ ] Avatar & Banner: Phong cách Blueprint Noir đồng nhất

---

## 8. Tự Động Hóa "Chất Người" — Persona & Nghiên Cứu

* **Persona:** *The Chief Blueprint Architect* — 38 tuổi, am tường cơ khí, vật lý và lịch sử quân sự. Lối dẫn chuyện đanh thép, nghiêm túc, đam mê bóc tách sự thật đằng sau những bản vẽ phức tạp.
* **Subreddits ưu tiên:** `r/ThingsCutInHalfPorn`, `r/EngineeringPorn`, `r/MachinePorn`, `r/MilitaryPorn`, `r/HistoryPorn`, `r/CatastrophicFailure`, `r/IsaacArthur`, `r/AskScience`.
