---
name: channel-factory
description: >
  Skill "nhà máy" tạo bộ kênh YouTube mới + video style director mới từ đầu.
  Kích hoạt BẤT CỨ KHI NÀO user muốn: tạo kênh YouTube mới, thêm kênh mới
  vào hệ thống, tạo phong cách hình ảnh mới, hoặc mở rộng hệ thống multi-channel.
  Triggers: "tạo kênh mới", "kênh youtube mới", "new channel", "thêm kênh",
  "phong cách mới", "new video style", "mở rộng hệ thống", "channel factory".
---

# Channel Factory — Tạo Kênh YouTube & Video Style Director Mới

Skill này hướng dẫn AI Agent tạo **trọn bộ 2 files Skill** cho một kênh YouTube mới:
1. **Channel Skill** (chiến lược kênh) — theo bộ khung `papercut_business_youtube`
2. **Director Skill** (đạo diễn hình ảnh) — theo bộ khung `vox_papercut_director`, `pixel_retro_director`, hoặc `pulp_comic_director`

Đồng thời cập nhật `channel-identities.md` để hệ thống nhận diện kênh mới.

---

## Quy Trình Tạo Kênh Mới (7 Bước)

### Bước 1: Thu Thập Thông Tin Kênh (Phỏng Vấn User)

AI Agent PHẢI hỏi user **tất cả** các thông tin sau trước khi tạo bất kỳ file nào.
Nếu user chưa cung cấp đủ, hỏi tiếp — KHÔNG tự đoán.

#### 1A. Thông tin cốt lõi (BẮT BUỘC)

| # | Câu hỏi | Ví dụ |
|---|---------|-------|
| 1 | **Tên kênh?** | "Neon Pulse" |
| 2 | **Micro-niche?** (Ngách cụ thể, không phải chủ đề rộng) | "Câu chuyện đen tối đằng sau ngành công nghiệp giải trí Mỹ" |
| 3 | **Series chính?** (Tên series xuyên suốt) | "Behind the Curtain" |
| 4 | **Khán giả mục tiêu?** (Quốc gia, độ tuổi, sở thích) | "Người Mỹ 20-40, thích true crime & pop culture" |
| 5 | **Ngôn ngữ nội dung?** | "100% Tiếng Anh Mỹ" |
| 6 | **Phong cách hình ảnh?** (Mô tả visual style mong muốn) | "Neon noir — ánh đèn neon, bóng tối, film grain, typography đậm" |
| 7 | **Giọng đọc AI Voice?** (`voice_id` từ xAI TTS — xem `references/voices.md`) | "ember" (giọng nữ trầm bí ẩn) |
| 8 | **Lịch đăng video?** (Ví dụ: Thứ 2 & Thứ 5, hoặc Thứ 3 & Thứ 6) | "2 video / tuần (ví dụ: Thứ 2 & Thứ 5)" |

#### 1B. Thông tin bổ sung (hỏi thêm nếu cần)

| # | Câu hỏi | Mặc định nếu không trả lời |
|---|---------|---------------------------|
| 9 | **Caption style?** (`paper`, `white`, hoặc custom) | `white` |
| 10 | **Hiệu ứng post-processing đặc biệt?** (CRT scanlines, film grain, glitch...) | Không |
| 11 | **Persona narration?** (Tuổi, giới, tính cách, giọng viết) | AI đề xuất dựa trên niche |
| 12 | **Subreddits mục tiêu?** (Cho topic discovery & research) | AI đề xuất dựa trên niche |
| 13 | **Câu Outro CTA Short?** | AI đề xuấ```markdown
## Đề xuất nhận diện kênh: [TÊN KÊNH]

| Tham số | Giá trị |
|---------|---------|
| Tên kênh | ... |
| Micro-niche | ... |
| Series | ... |
| Lịch đăng video | ... (ví dụ: Thứ 2 & Thứ 5) |
| voice_id | ... |
| caption_style | ... |
| watermark | ... |
| watermark_image | assets/[tên_kênh]_watermark.png |
| Post-processing | ... |
| Avatar Prompt | ... |
| Banner Safe Zone Text | [TÊN KÊNH] - [TAGLINE] - NEW EPISODES [DAYS] |

### Outro CTA (BẤT BIẾN sau khi duyệt)
- **Short:** "..."
- **Long-form:** "..."
- **Hình ảnh Outro:** ...

### Persona
| Thuộc tính | Giá trị |
|---|---|
| Tuổi | ... |
| Giới | ... |
| Tính cách | ... |
| Giọng viết | ... |
```

> ⛔ **CHỜ USER APPROVE** trước khi tạo files. Sau khi Outro CTA được duyệt, nó trở thành BẤT BIẾN — không được sửa trong các video sau.

---

### Bước 3: Tạo Channel Skill (Chiến Lược Kênh)

Tạo file: `.agents/skills/[tên_kênh_snake_case]_youtube/SKILL.md`

**Bộ khung BẮT BUỘC** (10 sections — giống `papercut_business_youtube` và `pixel_rewind_youtube`):

```
---
name: [tên-kênh]-youtube
description: >
  [Mô tả skill — kích hoạt khi nào]
  Triggers: "[tên kênh]", "[tên series]", ...
---

# [Tên Kênh] — YouTube Channel Playbook

## 📌 Phân Định Scope & Kiến Trúc Skill
> ⚠️ THAM CHIẾU QUY TẮC BẮT BUỘC:
> - .agents/rules/video-production.md — 12 quy tắc production
> - .agents/rules/channel-identities.md — Tham số kênh + Outro CTA bất biến
> - Kỹ thuật pipeline: xem skill [tên director skill]
> - Viết kịch bản giống người: xem skill `human-scriptwriter` (`human_scriptwriter`)
> - Nghiên cứu Reddit: xem skill `reddit-research` (`reddit_research`)

## 1. Thông tin Kênh (Channel Identity)
   → Bảng: tên, ngách, series, khán giả, phong cách, ngôn ngữ, voice, lịch đăng video (Upload Schedule)

## 2. Chiến lược Phễu: Shorts → Long-form
   ### 2.1. Thứ Tự SẢN XUẤT
   ### 2.2. Mối Quan Hệ Nội Dung (Bổ sung, KHÔNG lặp)
   ### 2.3. Thứ Tự ĐĂNG VIDEO (Theo đúng lịch đăng của kênh)

## 3. Dấu Ấn Thương Hiệu (Brand Identity)
   ### 3.1. Watermark Logo (prompt tạo logo + asset path)
   ### 3.2. Signature Outro (tham chiếu channel-identities.md)
   ### 3.3. Quy Chuẩn Tạo Channel Banner & Avatar (YouTube Header)
      - Avatar: 800x800 px prompt
      - Banner Canvas: 2560x1440 px prompt (Aspect Ratio 16:9)
      - Banner Safe Zone (1546x423 px trung tâm): Tên Kênh + Tagline + Lịch Đăng Video

## 4. Nguyên tắc Viết Kịch Bản — Quy tắc 70/30
   ### 4.1. YPP restrictions
   ### 4.2. 5 quy tắc scripting (①-⑤, customize cho niche)

## 5. Chiến lược Thumbnail
   ### 5.1. Long-form (Poster 16:9 2K qua provider.py + đè chữ 3-5 từ + film grain / CRT scanline filter)
   ### 5.2. Shorts — Chiến Lược First Frame Thumbnail (Frame 0 Optimization)

## 6. Hướng dẫn Sản Xuất
   ### Mẹo tối ưu chi phí
   ### Cấu trúc kịch bản mẫu (Short)

## 7. Cài đặt Kênh YouTube (Checklist bao gồm Avatar & Banner Assets)
```mbnail.py`. Áp dụng công thức 3 Lớp cho Shot 1a:
      - **Lớp 1 (Visual Anchor + Embedded Headline)**: `keyframe_prompt` của Shot 1a (`kf_1a.jpg`) BẮT BUỘC chèn chỉ thị chữ Headline trực tiếp cho AI Image model (ví dụ: `"...Include a torn-paper banner with a big bold cut-out English headline '[TITLE_EN]'"`) để ảnh `kf_1a.jpg` sinh ra ĐÃ CÓ SẴN chữ Headline khổng lồ đập vào mắt người xem.
      - **Lớp 2 (Bold Headline Text Card)**: Beat 1 chứa `"title_en"` 3-5 từ in hoa giật gân và Shot 1a set `"title": true`.
      - **Lớp 3 (Kinetic Subtitle at 0.00s)**: Thoại cất lên ngay milisecond 0.00, `assemble.py` render phụ đề kinetic dán nổi đè lên Frame 0.

## 6. Hướng dẫn Sản Xuất
   ### Mẹo tối ưu chi phí
   ### Cấu trúc kịch bản mẫu (Short)

## 7. Cài đặt Kênh YouTube (Checklist)

## 8. Tham khảo Kinh nghiệm / Ý tưởng Chủ đề

## 9. Tự Động Hóa "Chất Người" — Human Voice Automation
   ### 9.1. Persona (customize hoàn toàn cho kênh mới)
   ### 9.2. Reddit Research Pipeline (channel-specific config only — tham chiếu `reddit_research/SKILL.md`)
   ### 9.3. Imperfection Injection (customize cho niche)
   ### 9.4. Pipeline Tổng Hợp

## 10. Topic Discovery Engine
   ### 10.1. Subreddit Mục Tiêu (tiered — riêng cho niche mới)
   ### 10.2. Quy Trình Quét
   ### 10.3. Bộ Lọc 5 Tiêu Chí (customize cho niche)
   ### 10.4. Virality Scoring
   ### 10.5. Danh sách Đã Làm
   ### 10.6. Output Bảng Xếp Hạng
```

**Nguyên tắc viết nội dung:**
- §1-§3: Copy khung từ `papercut_business_youtube`, thay đổi **mọi chi tiết** cho kênh mới
- §4: Giữ nguyên YPP rules + 5 quy tắc scripting, nhưng customize ví dụ và từ lóng cho niche mới
- §5: Giữ khung, thay đổi style thumbnail cho phù hợp phong cách hình ảnh mới
- §9: **Viết mới Persona (9.1) và Imperfection (9.3)**. Section 9.2 chỉ khai báo **channel-specific config** (subreddits, insight types, injection points) — quy trình đầy đủ nằm trong shared skill `reddit_research/SKILL.md`
- §10: **Viết mới hoàn toàn** — Subreddit tiers khác, tiêu chí lọc khác

> ⚠️ **KHÔNG copy-paste nội dung từ kênh cũ.** Chỉ copy BỘ KHUNG (headings + cấu trúc). Mọi nội dung chi tiết phải được viết mới cho niche của kênh mới.

---

### Bước 4: Tạo Director Skill (Đạo Diễn Hình Ảnh)

Tạo file: `.agents/skills/[tên_style_snake_case]_director/SKILL.md`

**Chọn base template:**
- Nếu phong cách mới gần với **paper collage** → fork từ `vox_papercut_director`
- Nếu phong cách mới gần với **pixel art / retro** → fork từ `pixel_retro_director`
- Nếu phong cách mới gần với **comic / pop-art** → fork từ `pulp_comic_director`
- Nếu phong cách hoàn toàn mới → tạo hybrid hoặc từ đầu theo bộ khung dưới

**Bộ khung BẮT BUỘC** (giống `vox_director` và `pixel_retro_director`):

```
---
name: [tên-style]-director
description: >
  [Mô tả phong cách hình ảnh + khi nào kích hoạt]
  Triggers: ...
---

# [Tên Style] Director

## The core idea (read this first)
   → 2 bước: look sinh ra trong IMAGE, motion thêm sau
   → Mô tả DNA hình ảnh riêng của style mới

## Prerequisites (check, don't skip)
   > ⚠️ THAM CHIẾU QUY TẮC BẮT BUỘC:
   > - .agents/rules/video-production.md
   > - .agents/rules/channel-identities.md
   > - Pipeline cơ sở: xem skill vox-director

## Standard workflow (topic → film)
   ### 1. Topic → beat map
   ### 2. Pick Visual Style ([Style] Themes)
      → Định nghĩa 4-6 theme presets riêng cho style mới
      → Mỗi preset: palette, typography, texture, mood, motion default
   ### 3. Keyframes (The [Style] Look)
      → 5-part prompt structure riêng cho style mới
      → Ví dụ prompt cụ thể
   ### 4. Motion ([Style]-Appropriate)
      → Từ vựng motion phù hợp style
      → Camera moves nào an toàn, nào rủi ro
   ### 5. Voice + Music
      → Thể loại nhạc nền phù hợp
   ### 6. Draft Mode
   ### 7. Assemble (+ post-processing nếu có)
      → Hiệu ứng đặc biệt (nếu có): scanlines, grain, glitch...
   ### 8. Thumbnail
   ### Cadence
   ### Verify

## beats.json schema ([Style] adaptations)
   → Thêm fields riêng nếu cần (như crt_post cho pixel_retro)

## Model selection (always verify IDs live)
   → Bảng model mặc định + lý do chọn
```

**Nguyên tắc viết nội dung:**
- Core idea: Mô tả DNA hình ảnh mới (như paper collage cho Vox, pixel art cho Pixel Retro)
- Theme presets: Tạo 4-6 presets PHÙ HỢP phong cách mới (VD: neon-noir, cyberpunk-glow, dark-cinema...)
- Prompt structure: Viết mới 5-part prompt cho style mới (medium/era/palette/type/finish)
- Motion: Từ vựng motion phù hợp (VD: neon → "neon flicker, light sweep"; pixel → "pixel scatter")
- Post-processing: Mô tả pipeline ffmpeg nếu có hiệu ứng đặc biệt

---

### Bước 5: Cập Nhật `channel-identities.md`

Thêm cột mới vào bảng trong `.agents/rules/channel-identities.md`:

```markdown
| Tham số | Papercut Business | Pixel Rewind | [Kênh Mới] |
|---------|-------------------|--------------|------------|
| `voice_id` | `leo` | `leo` | `[voice_id mới]` |
| `caption_style` | `paper` | `white` | `[style mới]` |
| `watermark` | `Papercut Business` | `Pixel Rewind` | `[Tên kênh]` |
| `watermark_image` | `assets/...` | `assets/...` | `assets/[kênh mới]_watermark.png` |
| `crt_post` | ❌ | `true` | `[true/false]` |
| `[field mới nếu có]` | ... | ... | ... |
```

Thêm section Outro CTA cho kênh mới:

```markdown
### [Tên Kênh Mới]
- **Short:** "[câu CTA đã được user duyệt]"
- **Long-form:** "[câu CTA đã được user duyệt]"
- **Hình ảnh Outro:** [mô tả visual]
```

---

### Bước 6: Tạo Bộ Tài Nguyên Nhận Diện Kênh (Logo Watermark, Avatar & Banner)

1. **Logo Watermark (PNG Tách Nền):**
   - Dùng prompt từ §3.1 của Channel Skill mới để gen logo qua `scripts/provider.py` hoặc FlowKit.
   - Tách nền (`remove-background`) và lưu vào `assets/[tên_kênh]_watermark.png`.

2. **Avatar Kênh (Square 1:1, 800x800 px):**
   - Dùng prompt từ §3.3 của Channel Skill mới để gen avatar theo visual style của kênh.
   - Lưu vào `assets/[tên_kênh]_avatar.png`.

3. **Channel Banner Kênh (Cover Header 16:9, 2560x1440 px):**
   - Gen ảnh nền Canvas 2560x1440 mở rộng theo visual style của kênh.
   - Ghép chữ Vùng An Toàn (Safe Zone 1546x423 px trung tâm): Tên Kênh + Tagline + Lịch Đăng Video (`upload_schedule`).
   - Lưu vào `assets/[tên_kênh]_banner.png`.

---

### Bước 7: Verify & Test

Sau khi tạo xong tất cả files:

1. **Kiểm tra cấu trúc:**
   ```
   .agents/
   ├── rules/
   │   ├── video-production.md      (đã có — không sửa)
   │   └── channel-identities.md    (đã cập nhật — thêm cột + CTA)
   └── skills/
       ├── [kênh_mới]_youtube/
       │   └── SKILL.md              (MỚI — channel strategy)
       └── [style_mới]_director/
           └── SKILL.md              (MỚI — visual director)
   ```

2. **Test bằng prompt thử:**
   - _"Làm Short cho kênh [Tên Kênh Mới] về [chủ đề]"_
   - Kiểm tra: AI có dùng đúng voice_id, caption_style, CTA, persona không?
   - Kiểm tra: AI có tham chiếu đúng rules không?

3. **Checklist trước khi hoàn tất:**
   - [ ] Channel Skill có đủ 10 sections?
   - [ ] Director Skill có đủ các sections (workflow, themes, prompts, schema)?
   - [ ] `channel-identities.md` đã có kênh mới?
   - [ ] Bộ nhận diện kênh: Logo watermark (`assets/[kênh]_watermark.png`), Avatar (`assets/[kênh]_avatar.png`) và Channel Banner (`assets/[kênh]_banner.png`) đã tạo đủ?
   - [ ] Outro CTA đã được user duyệt và lock?
   - [ ] Không có nội dung nào copy-paste từ kênh cũ?

---

## Lưu Ý Quan Trọng

> ⛔ **KHÔNG tạo kênh mới khi chưa có đủ thông tin từ Bước 1.** Hỏi cho đủ rồi mới tạo.

> ⚠️ **Mỗi kênh mới = 2 files Skill + cập nhật 1 file Rule.** Không cần tạo thêm rule file riêng.

> 💡 **Nguyên tắc "Source of Truth":** Quy tắc chung nằm ở `rules/`. Kênh-specific nằm ở channel skill. Style-specific nằm ở director skill. KHÔNG lặp lại nội dung giữa các nơi.
