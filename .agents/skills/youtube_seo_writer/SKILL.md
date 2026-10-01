---
name: youtube-seo-writer
description: >
  Chuyên gia tối ưu hóa Metadata chuẩn YouTube SEO, TikTok & Instagram Reels.
  Kích hoạt BẤT CỨ KHI NÀO user hoặc pipeline cần: tạo tiêu đề (titles), mô tả (description),
  tags, hashtags, pinned comment, AI disclosure, hoặc tối ưu SEO cho video Shorts & Long-form.
  Triggers: "seo", "metadata", "tiêu đề", "description", "tags", "hashtags",
  "youtube seo", "tiktok caption", "metadata.py", "xuất metadata".
---

# YouTube & Multi-Platform SEO Writer — Cẩm Nang Metadata Chuẩn 2026

Skill này hướng dẫn AI Agent đóng vai một **Chuyên Gia YouTube SEO & Viral Copywriter**, chịu trách nhiệm tạo trọn bộ tài nguyên **Metadata Package** (`youtube_seo.md`) cho mọi video Shorts và Long-form trước khi đăng lên YouTube, TikTok và Instagram Reels.

---

## 📌 Phân Định Kiến Trúc: Rule vs Skill

* **`rules/youtube-ai-production.md` (Rule):** Chỉ giữ lệnh ràng buộc cứng — *"Mọi video sau khi render xong BẮT BUỘC phải chạy `metadata.py` để tạo `youtube_seo.md`"*.
* **`youtube-seo-writer` (Skill này):** Nơi chứa toàn bộ **tri thức chiều sâu**, công thức đặt tiêu đề, cấu trúc Mô tả 3 Zone, chiến lược Hashtag/Tag, chính sách AI Disclosure 2026 và cách vận hành script `metadata.py`.

---

## 1. Công Thức Đặt Tiêu Đề (Title Optimization Engine)

Tiêu đề là yếu tố quyết định **70% tỷ lệ nhấp (CTR)**. 

### ⛔ QUY TẮC CẤM CỨNG (Title Anti-Pattern Guards):
1. **CẤM DÙNG TIÊU ĐỀ BEAT INTRO/SETUP:** Tuyệt đối KHÔNG lấy tiêu đề của Beat 1 (như *"The Classified File"*, *"The Thought Experiment"*, *"Intro"*, *"Prologue"*) ghép vào template để làm tiêu đề video (VD: ❌ *"The Classified File — The Untold Story"*). Khán giả lướt qua sẽ không hiểu video nói về cái gì và bỏ qua ngay lập tức!
2. **CẤM CẮT BỎ HOOK CHÍNH:** Khi topic có dạng `"CONCEPT — HOOK QUESTION"` (như *"The Silurian Paradox — What If Dinosaurs Had An Industrial Revolution?"*), KHÔNG ĐƯỢC vứt bỏ phần câu hỏi hook phía sau. Phần câu hỏi hook chính là mồi câu CTR đắt giá nhất.
3. **CẤM RẬP KHUÔN TEMPLATE RỖNG:** Không gắn máy móc đuôi *"The Hidden Truth"* hay *"The Untold Story"* vào từ khóa cụt lủn nếu không tạo ra câu có nghĩa.
4. **CẤM DÙNG "WHAT IF" TRÊN KÊNH PULP HYPOTHESES:** Kênh `Pulp Hypotheses` **CẤM TUYỆT ĐỐI** dùng cụm từ *"What If"* trong tiêu đề video. Mọi tiêu đề Pulp Hypotheses **BẮT BUỘC là câu hỏi trực diện** (`Did ...?`, `Could ...?`, `Were ...?`, `Why Did ...?`).

### ✅ Quy tắc kỹ thuật bắt buộc:
1. **Quy tắc Trực Diện Chủ Đề (Direct Topic Hook Principle):** Tiêu đề BẮT BUỘC phải chứa **Chủ Thể Cốt Lõi (Core Subject)** + **Hành Động / Giả Định Gây Sốc** (VD: *Dinosaurs*, *Industrial Revolution*, *Silurian Paradox*, *Nintendo*, *Game Boy*).
2. **Quy tắc Truncation trên Mobile (< 50-55 ký tự):** Giao diện ứng dụng YouTube trên điện thoại cắt xén tiêu đề sau 55 ký tự. Từ khóa chính và từ gây tò mò (Hook) **BẮT BUỘC nằm ở 5 từ đầu tiên**.
3. **Loại bỏ thẻ rác (`[4K]`, `[HD]`):** Tuyệt đối KHÔNG chèn thẻ `[4K]` ở cuối tiêu đề vì làm tăng độ dài tiêu đề, gây lỗi cắt xén trên mobile và làm tiêu đề trông thiếu tinh tế. YouTube đã tự động hiển thị nhãn 4K trên trình phát khi video đạt chuẩn.
4. **Hậu tố định dạng:**
   * Video Shorts (9:16): BẮT BUỘC kết thúc bằng `#Shorts`.
   * Video Long-form (16:9): Giữ tiêu đề sạch hoặc chỉ thêm thương hiệu ngắn `| [Tên Kênh]` (tổng độ dài < 60 ký tự).
5. **Power Words (Từ tạo cảm xúc mạnh):** `SHOCKING`, `SECRET`, `IMPOSSIBLE`, `DEADLY`, `WHY`, `DID`, `COULD`, `THE TRUTH`.

### 3 Công thức Tiêu đề chuẩn SEO & CTR (Long-form & Shorts):

| Công thức | Kênh Áp Dụng | Cấu trúc | Mục đích | Ví dụ Thực Tế |
|---|---|---|---|---|
| **Option 1 (Direct Question Hook)** | **Pulp Hypotheses** | `Did / Could / Were [CHỦ THỂ] [HÀNH ĐỘNG]?` | Đẩy tối đa CTR, loại bỏ hoàn toàn "What If" | `Did Dinosaurs Have An Industrial Revolution? 🦖⚙️` |
| **Option 2 (Concept & Mystery Question)** | **Pulp Hypotheses** | `[TÊN NGHỊCH LÝ / BÍ ẨN]: [CÂU HỎI TRỰC DIỆN]` | Tạo chiều sâu học thuật + bí ẩn | `The Silurian Paradox: Did Dinosaurs Have Factories?` |
| **Option 3 (Documentary / Economics)** | **Papercut / Pixel** | `[TỪ KHÓA CHÍNH] — The Untold Story / Scandal` | Đón đầu lượng tìm kiếm và đề xuất lâu dài | `The $130 Texas Instruments TI-84 Monopoly` |

---

## 2. Cấu Trúc Mô Tả 3 Zone (Description Architecture)

Mô tả YouTube có 3 vùng với mục đích thuật toán khác nhau:

```
[ZONE 1: Above the fold (150 ký tự đầu — trước nút "Show More")]
- Tiêu đề chính lặp lại
- Lời kêu gọi hành động (Subscribe & Bật chuông) + Lịch phát sóng kênh
- Tóm tắt 1 câu chứa Primary Keyword

[ZONE 2: Nội dung chính & Chapters (150 - 2,500 ký tự)]
- Tóm tắt câu chuyện kịch bản (Story Summary 3-5 câu giàu từ khóa tự nhiên)
- ⏱️ TIMESTAMPS (Chapters tự động — BẮT BUỘC bắt đầu từ 00:00)
- Mật độ từ khóa tự nhiên: 2-3% (viết cho người đọc, không nhồi nhét)

[ZONE 3: Kêu gọi hành động & Footer (2,000 - 5,000 ký tự)]
- 📢 Lời kêu gọi Subscribe & Link kênh (Outro CTA)
- #HASHTAGS (5 đến 8 Hashtags chuẩn)
- © Thông tin bản quyền & thương hiệu

> 💡 **LƯU Ý QUAN TRỌNG VỀ AI DISCLOSURE (CHÍNH SÁCH YOUTUBE 2026):**
> - **KHÔNG viết khối chữ "AI CONTENT DISCLOSURE" vào phần mô tả văn bản** vì gây lãng phí dung lượng SEO và kích hoạt định kiến tiêu cực của người xem.
> - Khai báo AI theo chính sách YouTube được thực hiện **trực tiếp qua tùy chọn Checkbox "Altered content" (Nội dung chỉnh sửa/tổng hợp) trong YouTube Studio** khi tải video lên. YouTube sẽ tự động gắn nhãn UI chuẩn nếu cần. Animation/CAD kỹ thuật thậm chí được YouTube miễn trừ yêu cầu dán nhãn vì không phải deepfake người thật gây hiểu lầm.
```

---

## 3. Chiến Lược Hashtags (Giới Hạn Tối Đa 5 - 8 Hashtags)

> ⛔ **CẢNH BÁO THUẬT TOÁN YOUTUBE:** Nếu mô tả chứa **trên 15 hashtags**, thuật toán YouTube sẽ **PHẠT VÀ BỎ QUA TOÀN BỘ HASHTAGS** trên video đó.

### Công thức phân bổ Hashtags chuẩn (5-8 tags):
1. **Tier 1 (Brand & Niche - 3 Hashtags):** Hiển thị trên tiêu đề video.
   * Ví dụ: `#PulpHypotheses #WhatIf #AlternateHistory`
2. **Tier 2 (Topic Specific - 3-5 Hashtags):** Nằm ở footer mô tả.
   * Ví dụ: `#PulpComic #AbsurdHistory #HistoryMemes`

---

## 4. Bộ Từ Khóa Ẩn (Tags Engine ≤ 480 Ký Tự)

Thẻ Tags ẩn giúp YouTube phân loại chủ đề cho các kênh mới và xử lý tìm kiếm gõ sai.

### Công thức xếp tầng Tags:
1. **Brand Tag:** Tên kênh (`Pulp Hypotheses`, `Pixel Rewind`, `Papercut Business`).
2. **Exact Match Phrases:** Tiêu đề và cụm từ chính (`what if cavemen had guns`).
3. **Broad Niche Terms:** Từ khóa ngách rộng (`alternate history`, `history memes`, `weird history`).
4. **Long-tail & Misspellings:** Từ khóa dài + từ gõ sai phổ biến (`pulp hypothesis`, `caveman ak47`).

---

## 5. Tự Động Hóa Qua Script `scripts/metadata.py`

Gói Metadata được tự động sinh ra bằng cách gọi script:

```bash
python3 scripts/metadata.py out/<project> --channel "[Tên Kênh]"
```

### File kết quả xuất ra: `out/<project>/youtube_seo.md` chứa:
- 📌 3 Lựa chọn Tiêu đề
- 📝 Mô tả 3 Zone đầy đủ
- 🏷️ Bộ Tags ẩn (chuẩn < 480 chars)
- #️⃣ Bộ Hashtags (5-8 tags)
- 📌 Pinned Comment (Bình luận ghim đầu tiên)
- 📱 TikTok & Instagram Reels Caption Package
