---
name: pulp-comic-director
description: >
  Đạo diễn hình ảnh phong cách Truyện Tranh Cổ Điển (Retro Pulp Comic Style 80s-90s US Comic).
  Đặc điểm thị giác: nét mực đen đậm (heavy ink outlines), đổ bóng vệt chấm bi (CMYK halftone dots),
  màu sắc pop-art rực rỡ, góc quay kịch tính (dramatic superhero / sci-fi action pose).
  Triggers: "pulp comic style", "pulp comic director", "retro comic style", "truyện tranh cổ điển", "phong cách comic 80s", "heavy ink halftone".
---

# Retro Pulp Comic Director — Đạo Diễn Hình Ảnh Truyện Tranh Cổ Điển

## The Core Idea (Read This First)

Phong cách **Retro Pulp Comic** lấy cảm hứng từ các bộ truyện tranh Mỹ Sci-Fi và Siêu anh hùng thập niên 80-90 (Golden & Bronze Age Comics). 

### DNA Thị Giác Cốt Lõi:
1. **Multi-Panel Comic Page Layout:** Bố cục rõ ràng là một trang sách / trang bìa truyện tranh cổ điển (Vintage 80s Comic Book Page) với các ô panel truyện hình chữ nhật có viền đen dày (*thick black grid borders*).
2. **2D Traditional Superhero Cel Animation:** Phong cách hoạt hình 2D truyền thống kiểu phim hoạt hình siêu anh hùng thập niên 80 (Marvel/DC 80s animated series cel aesthetic).
3. **Heavy Black Ink Outlines:** Nét vẽ bằng mực đen đậm cứng cáp, nét cọ đánh bóng thủ công.
4. **CMYK Halftone Dots & Newsprint Texture:** Đổ bóng hạt chấm bi in báo CMYK cổ điển và vân nhám giấy báo ngả vàng.
5. **Comic Sound Badges & Speech Balloons:** Các ô thoại bong bóng (*speech balloons*) và biểu tượng chữ tiếng động kịch tính (*BAM!*, *KABOOM!*, *POW!*, *WHAT IF?!*).

---

## Prerequisites (Check, Don't Skip)

> ⚠️ THAM CHIẾU QUY TẮC BẮT BUỘC:
> - `.agents/rules/video-production.md` — 12 quy tắc production bắt buộc
> - `.agents/rules/channel-identities.md` — Tham số nhận diện kênh `Pulp Hypotheses`
> - Skill chiến lược kênh: xem `pulp_hypotheses_youtube` (`pulp-hypotheses-youtube`)

---

## Standard Workflow (Topic → Comic Film)

### 1. Pick Theme Presets (Pulp Comic Themes)

Chọn 1 trong 5 bộ Theme Preset phù hợp nhất với bối cảnh của beat:

| Theme Preset | Palette Dominant | Bối cảnh phù hợp | Element đặc trưng |
|---|---|---|---|
| **`pulp-sci-fi`** | Cyan neon, Magenta, Electric Yellow, Deep Navy | Vũ trụ, công nghệ tương lai, đĩa bay, vũ khí laser | Plasma ray glow, starfield halftone, retro spacesuits |
| **`prehistoric-pulp`** | Ochre vàng, Đỏ đất gạch, Xanh rừng thẫm, Mực đen | Thời tiền sử, khủng long, người hang động | Volcanic smoke halftone, wooden club vs high-tech contrast |
| **`vintage-hero`** | Đỏ cờ, Vàng chanh, Xanh Coban, Nét mực đậm | Góc quay siêu anh hùng, khoảnh khắc hành động kịch tính | Explosive action burst halftone background, low angle |
| **`alternate-noir`** | Amber thẫm, Crimson, Mực đen high-contrast | Bí mật phòng thí nghiệm, âm mưu, thám tử | Venetian blind shadow dots, smoking beaker, moody ink |
| **`absurd-apocalypse`** | Burnt Orange, Toxic Lime Green, Mực đen | Tận thế phi lý, thành phố sụp đổ, thảm họa | Ruined skyline halftone, Dutch tilt perspective, rubble |

---

### 2. Keyframes — The 5-Part Pulp Comic Prompt Formula

Mọi prompt sinh ảnh keyframe (qua FlowKit hoặc `provider.py`) BẮT BUỘC tuân thủ công thức 5 phần:

```
[1. Medium & Multi-Panel Layout] + [2. 2D Cel & Ink Style] + [3. Halftone & Newsprint Texture] + [4. Pop-Art Palette] + [5. Subject, Speech Balloons & Sound Badges]
```

#### Cấu Trúc Chi Tiết:
1. **Medium & Multi-Panel Layout:** `"Vintage 1980s American pulp comic book page layout, multi-panel comic strip with thick black grid borders,"`
2. **2D Cel & Ink Style:** `"traditional 2D hand-drawn cel animation aesthetic, heavy black ink outlines, bold graphic brush shading,"`
3. **Halftone & Newsprint Texture:** `"classic CMYK halftone dot pattern shading, aged newsprint paper texture,"`
4. **Pop-Art Palette:** `"vibrant 80s pop-art color palette, saturated primary yellow, red and cyan colors, high contrast,"`
5. **Subject & Comic Badges:** `"[Mô tả hành động nhân vật], speech balloons with English text, explosive sound effect badges (BAM!, KABOOM!), dramatic retro comic stance."`

> ⚠️ **QUY TẮC CẤM TỪ KHÓA SUPERHERO CHO CHỦ ĐỀ LỊCH SỬ / XÃ HỘI (SUPERHERO PROMPT GUARD):**
> - Đối với các video lịch sử giả định, xã hội, khoa học (không phải nhân vật siêu anh hùng thực sự), **TUYỆT ĐỐI KHÔNG** dùng cụm từ `"superhero comic book illustration"`, `"superhero typography"`, hoặc `"superhero action stance"` trong `keyframe_prompt`.
> - Việc dùng từ khóa "superhero" sẽ khiến AI image generator ảo tưởng vẽ thêm trang phục / nhân vật siêu nhân không liên quan vào bối cảnh lịch sử.
> - Thay bằng: `"retro 1980s American pulp comic book illustration"`, `"bold graphic comic typography"`, `"dramatic retro comic stance"`.
> - Ngoại lệ: Chỉ dùng từ khóa superhero ở Frame Outro bìa truyện hoặc phân cảnh timeline shift.

> ⚠️ **QUY TẮC VỊ TRÍ Ô CHỮ / BONG BÓNG THOẠI (NO BOTTOM TEXT / TOP PLACEMENT RULE):**
> - Mọi ô thoại (speech balloons), ô chữ tiêu đề (headline text banners) BẮT BUỘC chỉ thị vị trí nằm ở **NỬA TRÊN CỦA KHUNG HÌNH** (`"speech balloon positioned near the top edge of the comic panel"` / `"placed at the top area"`).
> - ⛔ **CẤM TUYỆT ĐỐI đặt ô chữ ở góc dưới bên phải hoặc chính giữa đáy ảnh (`bottom-right` / `bottom-center`)**, vì đây là khu vực bị đè/trùng vị trí Logo Watermark của Google Flow, Watermark Kênh và Phụ đề Kinetic.

> ⚠️ **QUY TẮC MÔ TẢ CỜ VIỆT NAM CHÍNH XÁC (VIETNAMESE FLAG ACCURACY):**
> - Khi vẽ Cờ Việt Nam trong prompt, BẮT BUỘC mô tả chi tiết: `"the official flag of Vietnam, a solid bright crimson-red flag with a single centered golden-yellow five-pointed star"`.
> - Tuyệt đối không viết ngắn gọn `"Vietnamese flag"` để tránh AI vẽ nhầm nhiều sao hoặc hoa văn sai lệch.

---


### 3. Motion Vocabulary (Comic Page Flip & Panel-to-Panel Guided View)

Quy tắc chuyển động camera & chuyển cảnh cốt lõi cho phong cách Truyện Tranh Cổ Điển:

- ⛔ **CẤM TUYỆT ĐỐI CAMERA ZOOM-IN (`zoom_in`, `quick_zoom`, `push_in`):** Không dùng các hiệu ứng phóng to/zoom dồn camera vào hình. Mọi `video_prompt` cho thể loại Comic BẮT BUỘC chèn thêm câu lệnh bảo vệ 2D: `"flat 2D comic strip — camera static or flat pan, no zoom in, no 3D push in"`.
- ✅ **2 HIỆU ỨNG CHUYỂN ĐỘNG CHỦ ĐẠO MONG MUỐN:**

  1. **Hiệu Ứng Lật Trang Truyện (`page_turn` / `flip_page` / `page_curl`):**
     - **Ứng dụng:** Chuyển cảnh giữa các Beat lớn hoặc chuyển sang phân đoạn câu chuyện mới.
     - **Cơ chế:** Mô phỏng tờ báo/trang sách truyện tranh 3D lật từ phải sang trái hoặc từ trái sang phải, mở ra một trang truyện mới với chất liệu giấy nhám báo cũ.
     - **Video Prompt chỉ thị:** `"3D vintage 1980s comic book page turning smoothly from right to left, paper page flip transition revealing a new comic book page."`

  2. **Hiệu Ứng Di Chuyển Tầm Nhìn Giữa Các Khung Tranh (`panel_to_panel_pan` / `panel_hop` / `guided_view`):**
     - **Ứng dụng:** Di chuyển nhịp lướt giữa các ô truyện trong cùng một trang multi-panel.
     - **Cơ chế:** Tầm nhìn camera di chuyển trượt chính xác từ **Khung Tranh 1 ➔ Khung Tranh 2 ➔ Khung Tranh 3** cắt qua đường rãnh viền đen (*thick black grid gutter border*), giống hiệu ứng đọc truyện tranh số (Guided View Comic Reader).
     - **Video Prompt chỉ thị:** `"Camera smoothly moves across the thick black grid border from comic panel A to adjacent comic panel B, digital comic reader guided view camera pan across comic strip frames."`

  3. **Hoạt Hình 2D Cel Trong Khung Tranh (`in_panel_2d_cel_animation`):**
     - **Cơ chế:** Tầm nhìn camera giữ nguyên ô truyện hoặc di chuyển theo rãnh khung, để nhân vật cử động hoạt hình 2D cel (vung tay, bắn laser, khói bốc, ô thoại nhấp nháy).

  4. **Hiệu Ứng Sóng Giấy Lắc Nẹp Trang Truyện (`paper_wave_ripple`):**
     - **Ứng dụng:** Tạo cảm giác mặt trang giấy truyện tranh in thực tế đang được rung lắc nhẹ ở mép giấy.
     - **Cơ chế:** Lớp hiệu ứng gợn sóng rung rinh bề mặt giấy 2D.
     - **Video Prompt chỉ thị:** `"STRICT 2D CONSTRAINTS: ABSOLUTELY NO ZOOM-IN, NO PUSH-IN. Include a subtle tactile paper wave wobble ripple effect, as if someone is holding the edge of the printed comic paper page and gently shaking it to create paper wave ripples."`

---

### 4. Voice & Music Direction

- **Voice ID:** `leo` (Giọng nam kịch tính, tài liệu cổ điển, Tiếng Anh Mỹ).
- **Nhạc nền (Music Prompt):**
  - Minimax prompt: `"80s synthwave action soundtrack, driving bassline, dramatic brass stabs, retro superhero movie theme, energetic, high tension."`

---

### 5. Post-Processing & Halftone Assembly

Script `assemble.py` bọc hiệu ứng và render phụ đề:
- **Caption Style:** `yellow_comic` (Chữ vàng viền đen dày nét to đậm).
- **Watermark:** Dán logo `assets/pulp_hypotheses_watermark.png` ở góc trên cùng.
- **Outro:** Trích xuất đúng câu CTA bất biến từ `channel-identities.md`.

---

## beats.json Schema (Pulp Comic Adaptation)

Mỗi beat trong `beats.json` cho kênh `Pulp Hypotheses` tuân theo schema tiêu chuẩn, bổ sung field `theme_preset`:

```json
{
  "beat_id": 1,
  "narration": "What if cavemen didn't fight with stone axes... but with fully automatic assault rifles?",
  "narration_vn": "Chuyện gì sẽ xảy ra nếu người tiền sử không đánh nhau bằng rìu đá... mà bằng súng trường tấn công?",
  "theme_preset": "prehistoric-pulp",
  "shots": [
    {
      "shot_id": "1a",
      "duration": 4.5,
      "title": true,
      "title_en": "CAVEMEN WITH GUNS?!",
      "keyframe_prompt": "Vintage 1980s American pulp comic book illustration... Include a dramatic retro comic book headline banner with big bold English text 'CAVEMEN WITH GUNS?!' in heavy black ink superhero typography, yellow fill with thick black outlines...",
      "motion": "page_turn",
      "camera": "pan_right"
    }
  ]
}
```

---

## Verify & Quality Control

Trước khi xuất bản video phong cách Pulp Comic, kiểm tra 4 tiêu chí:
1. [ ] Ảnh keyframe sinh ra có **nét mực đen đậm** và **hạt halftone dot** rõ rệt?
2. [ ] Phối màu có rực rỡ chuẩn **pop-art vintage 80s**?
3. [ ] Shot 1a đã nhúng chữ tiêu đề comic nét to giật gân làm Frame 0 Thumbnail?
4. [ ] Outro có đọc đúng câu CTA bất biến và dùng hình Outro tĩnh?
