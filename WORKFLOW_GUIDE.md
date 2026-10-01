# 📘 Cẩm Nang Hướng Dẫn Vận Hành AI Workflow (`WORKFLOW_GUIDE.md`)

Tài liệu này hướng dẫn **Chủ Kênh** cách vận hành trọn bộ hệ thống AI Workflow để sản xuất video tự động từ A-Z.

---

## 🏗️ 1. Cấu Trúc Hệ Thống Workflow

Hệ thống được thiết kế theo mô hình **2-Tier Skill Architecture** kết hợp với **Always-On Rules**:

```
video-atlas/
├── scripts/                             # ⚙️ SHARED ENGINE (keyframes, clips, audio, assemble, metadata...)
├── assets/                              # 🎨 LOGO & SCANLINE ASSETS
├── .agents/
│   ├── rules/                           # 📌 RULES DÙNG CHUNG (AI TỰ NẠP 100%)
│   │   ├── channel-identities.md        # Bảng tham số 3 kênh (voice_id, watermark, outro CTA, schedule)
│   │   └── video-production.md          # 17 Quy tắc sản xuất cứng & kịch bản kỹ thuật
│   └── skills/                          # 🛠️ SKILLS THEO NHIỆM VỤ (KÍCH HOẠT THEO CẦU)
│       ├── youtube_trend_scout/         # Skill đào ý tưởng xu hướng & phân tích đối thủ YouTube Faceless
│       ├── channel_factory/             # Skill "nhà máy" tạo kênh mới + Banner (2560x1440) & Avatar (800x800)
│       ├── human_scriptwriter/          # Skill viết kịch bản chống rập khuôn AI (Staccato, Imperfection pass)
│       ├── reddit_research/             # Skill cào insight thực tế từ Reddit qua Reddit MCP
│       ├── youtube_seo_writer/          # Skill xuất gói Metadata chuẩn SEO YouTube, TikTok & Reels
│       ├── papercut_business_youtube/   # Skill chiến lược kênh Papercut Business
│       ├── vox_papercut_director/       # Skill đạo diễn hình ảnh Vox Paper Collage
│       ├── pixel_rewind_youtube/        # Skill chiến lược kênh Pixel Rewind
│       ├── pixel_retro_director/        # Skill đạo diễn hình ảnh Pixel Art & CRT
│       ├── pulp_hypotheses_youtube/     # Skill chiến lược kênh Pulp Hypotheses
│       └── pulp_comic_director/         # Skill đạo diễn hình ảnh Retro Pulp Comic 80s
└── out/                                 # 📂 THƯ MỤC CHỨA SẢN PHẨM VIDEO XUẤT RA
```

---

## ⚡ 2. Quy Trình 7 Bước Sản Xuất Video Từ A-Z

### 📍 Bước 1: Yêu cầu AI tạo video (Prompting)
Bạn chỉ cần đưa ra chủ đề và kênh mong muốn.

* **Ví dụ mẫu:**
  ```text
  Làm video short 45s cho kênh Pixel Rewind về chủ đề "How a janitor at Nintendo invented the Game Boy"
  ```
  ```text
  Làm video long-form 3 phút cho kênh Pulp Hypotheses về chủ đề "What if cavemen had assault rifles?"
  ```

### 📍 Bước 2: Duyệt Kịch Bản (Approval Gate 1)
AI Agent sẽ tự động chạy `reddit_research` + `human_scriptwriter` và trình cho bạn **bảng kịch bản 5 cột** (`Shot ID`, `Thời lượng`, `Narration EN`, `Dịch Tiếng Việt`, `Visual`).

* **Hành động của bạn:**
  * Nếu OK $\rightarrow$ Bỏ phím gõ: **"Approve"** hoặc **"OK sản xuất đi"**.
  * Nếu muốn sửa $\rightarrow$ Báo AI: *"Sửa shot 3 narration ngắn lại"*.

### 📍 Bước 3: Tạo Ảnh Keyframes
Khi bạn Approve Gate 1, AI Agent sẽ gọi `keyframes.py` để tạo bộ ảnh chìa khóa 9:16 hoặc 16:9 + ảnh Thumbnail.

### 📍 Bước 4: Kiểm Tra & Xóa Watermark (Approval Gate 2 — BẮT BUỘC TẠM DỪNG)
Ngay sau khi sinh xong ảnh keyframes, AI Agent sẽ **tự động phanh dừng tiến trình** và báo cho bạn.

* **Hành động của bạn:**
  * Mở thư mục `out/<project>/keyframes/` ra kiểm tra ảnh.
  * Nếu ảnh có watermark hoặc logo dư thừa $\rightarrow$ Xóa/sửa ảnh.
  * Khi xong, báo AI: **"Đã kiểm tra keyframes, tiếp tục gen clips đi"**.

### 📍 Bước 5: Tạo Video Clips & Audio
AI Agent sẽ tự động gọi `clips.py` (sinh chuyển động qua Google Flow / Kling) + `audio.py` (thu âm giọng đọc xAI TTS chuẩn -14 LUFS + ghép nhạc nền BGM ducking).

### 📍 Bước 6: Ghép Thành Video Hoàn Chỉnh (`assemble.py`)
AI Agent ghép video + khớp phụ đề Kinetic + ghép Watermark nhận diện kênh + chèn hiệu ứng đặc biệt (CRT scanlines nếu là Pixel Rewind).
* **Kết quả:** File video chuẩn `out/<project>/final.mp4` (hoặc `final_crt.mp4`).

### 📍 Bước 7: Xuất Gói SEO Metadata Package (`metadata.py`)
AI Agent tự động gọi `metadata.py` để xuất gói `out/<project>/youtube_seo.md`.
* **Kết quả:** 3 Lựa chọn Tiêu đề, Mô tả 3 Zone, Tags ẩn, Hashtags, Pinned Comment và TikTok Caption hiển thị trực tiếp trên màn hình!

---

## 🏭 3. Hướng Dẫn Mở Rộng Kênh Mới Qua `channel-factory`

Khi bạn muốn mở thêm một kênh YouTube hoàn toàn mới (ví dụ: Kênh True Crime hoặc Kênh Sci-Fi):

1. **Gõ câu lệnh:**
   ```text
   Tạo cho tôi một kênh YouTube mới phong cách [tên phong cách] về ngách [tên ngách]
   ```
2. **AI Agent sẽ phỏng vấn bạn 8 câu hỏi cốt lõi:**
   - Tên kênh, Micro-niche, Series chính, Khán giả mục tiêu, Phong cách hình ảnh, Voice ID, Lịch đăng video.
3. **AI Agent sẽ tự động sinh trọn bộ:**
   - Strategy Skill mới (`.agents/skills/[tên_kênh]_youtube/SKILL.md`)
   - Director Skill mới (`.agents/skills/[tên_style]_director/SKILL.md`)
   - Cập nhật `.agents/rules/channel-identities.md`
   - Tạo trọn bộ ảnh **Logo Watermark**, **Avatar (800x800)** và **Channel Banner (2560x1440 với Safe Zone 1546x423)** tại `assets/`.

---

## 🛠️ 4. Bảng Tra Cứu Lệnh Nhanh (Cheat Sheet)

| Bạn muốn... | Câu Prompt mẫu |
|---|---|
| **Làm video Short 45s** | `Tạo video short 45s kênh [Tên Kênh] về "[Chủ đề]"` |
| **Làm video Ngang 3-5 phút** | `Tạo video long-form 3 phút kênh [Tên Kênh] về "[Chủ đề]"` |
| **Làm Combo Short + Long** | `Tạo combo short và long-form kênh [Tên Kênh] về "[Chủ đề]"` |
| **Chạy bản nháp ($0.40)** | `Tạo draft trước cho chủ đề "[Chủ đề]"` |
| **Tạo Banner & Avatar kênh** | `Tạo bộ nhận diện Banner và Avatar cho kênh [Tên Kênh]` |
| **Xuất lại SEO Metadata** | `Tạo lại metadata cho thư mục out/[tên_dự_án]` |
