---
name: blueprint-noir-director
description: >
  Đạo diễn hình ảnh phong cách Bản Vẽ 3D X-Ray Hắc Ám (Blueprint Noir).
  Đặc trưng thị giác: Phối cảnh 3D Isometric cắt lớp (Cutaway X-Ray), nền than chì/navy
  kỹ thuật (`#0B192C`), đường nét vector khung xương phát sáng (Electric Cyan `#00F0FF`,
  Neon Yellow `#FFDE59`, Antique Gold `#D4AF37`), bóng nhiệt con người (thermal heatmap),
  và giao diện dữ liệu radar/HUD quân sự.
  Triggers: "blueprint noir", "blueprint director", "bản vẽ 3d", "phong cách blueprint noir",
  "3d cutaway", "x-ray schematics", "cad wireframe".
---

# Blueprint Noir Director — 3D X-Ray Schematics Visual Guide

Cẩm nang đạo diễn hình ảnh cho phong cách **"Blueprint Noir" (Bản vẽ 3D X-Ray Hắc Ám)**
chuyên mổ xẻ siêu công trình, vũ khí, cỗ máy và kỳ quan cổ đại trên Google Flow (FlowKit)
kết hợp cùng xAI TTS và Local FFmpeg Assembly.

---

## 1. The Core Idea & Triết Lý Kỹ Thuật

> ⚠️ **TIÊU CHUẨN KỸ THUẬT NGHIÊM NGẶT CỦA BLACKPRINT:**
> Đây là kênh mô tả **Kiến trúc & Bản vẽ kỹ thuật thực tế**. Tuyệt đối không làm hình ảnh qua loa,
> chắp vá hay thiếu chính xác như các video AI trôi nổi. Mọi bản vẽ phải bám sát cấu trúc cơ khí
> và logic vật lý thực tế của công trình/cỗ máy.

### 1.1. Cấu Trúc Hybrid: Kết Hợp Ảnh Tĩnh Độ Nét Cao & Video Clips Động
* **Video Final KHÔNG bắt buộc tất cả các frame đều phải là video chuyển động:**
  * **Shot Ảnh Tĩnh (Static Schematic Shots):** Chiếm ~40–60% thời lượng. Áp dụng cho các bản vẽ tổng thể phức tạp, sơ đồ mặt cắt đa tầng. Script `assemble.py` áp dụng camera pan/zoom trượt nhẹ nhàng và lớp chữ vector overlay cực kỳ sắc nét.
  * **Shot Video Clips (Dynamic Motion Clips):** Chiếm ~40–60% thời lượng. Áp dụng khi cần mô phỏng **luồng chuyển động vật lý thực tế** (dòng áp suất khí, pít-tông trích khí, âu tàu nâng nước, dòng chảy thủy ngân, tia laser quét).

### 1.2. Quy Tắc Chuyển Động Google Flow: Tuyệt Đối Không Chuyển Động Vô Lý
* Khi gửi chỉ thị sinh video sang **Google Flow (FlowKit)**, chuyển động PHẢI tuyệt đối tuân thủ vật lý thực tế:
  * ✅ **ĐƯỢC PHÉP:** Camera đẩy chậm tuyến tính (`push_in`), quét ngang ổn định (`pan_left`), quét tia laser radar (`light sweep`), dòng hạt năng lượng chạy dọc theo đường ống dẫn (`conduit flow`).
  * ⛔ **CẤM TUYỆT ĐỐI:** Chuyển động biến dạng hình học (morphing), xoay 360 độ làm méo khung xương, vật thể tự uốn lượn vô lý, ảo giác dị tật. Nếu shot nào có nguy cơ bị méo hình học, **BẮT BUỘC giữ nguyên dạng Shot Ảnh Tĩnh**.

---

## 2. Prerequisites (Kiểm Tra Trước Khi Chạy)

> ⚠️ **THAM CHIẾU QUY TẮC BẮT BUỘC:**
> - [`.agents/rules/video-production.md`](file:///d:/video-atlas/.agents/rules/video-production.md) — 17 quy tắc kỹ thuật
> - [`.agents/rules/channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md) — Tham số kênh `Blackprint`
> - Kỹ thuật pipeline ffmpeg cơ sở: tham chiếu `scripts/assemble.py` và `scripts/text_overlay.py`

---

## 3. Theme Presets (4 Phong Cách Biến Thể)

Mỗi kịch bản `beats.json` chọn 1 theme preset chính tùy thuộc vào kỷ nguyên và đối tượng:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  THE 4 BLUEPRINT NOIR THEME PRESETS                                                    │
├──────────────────────────┬─────────────────────────────────────────────────────────────┤
│ 1. classified_cyber_cad  │ Navy Slate (#0B192C) + Electric Cyan (#00F0FF) + Neon Yellow│
│                          │ ➔ Dành cho: Tàu ngầm hạt nhân, B-2 Stealth, CERN, tên lửa.  │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 2. antique_da_vinci_noir │ Charcoal Slate (#12161A) + Gold/Brass (#D4AF37) + Chalk White│
│                          │ ➔ Dành cho: Kim tự tháp, Cẩu Archimedes, Nỏ Tam Quốc, DaVinci│
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 3. reactor_thermal_xray  │ Carbon Black (#080A0E) + Radioactive Emerald + Amber Pulse  │
│                          │ ➔ Dành cho: Chernobyl, Lò phản ứng hạt nhân, Thảm họa nhiệt │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 4. subterranean_bunker   │ Granite Grey (#1A1E24) + Hazard Yellow + Laser Scan Red     │
│                          │ ➔ Dành cho: Cheyenne NORAD, Hầm ngầm Paris, Kho vàng Fort Knox│
└──────────────────────────┴─────────────────────────────────────────────────────────────┘
```

---

## 4. Cấu Trúc Prompt 5 Phần Cho Keyframes (5-Part Formula)

Mọi prompt tạo ảnh cho Blueprint Noir BẮT BUỘC mô tả chi tiết từng cụm chi tiết cơ khí/kiến trúc thực tế:

```text
[1. MEDIUM & PERSPECTIVE] + [2. SUBJECT & AUTHENTIC REAL-WORLD CUTAWAY] + [3. PALETTE & WIREFRAME] + [4. TELEMETRY & HEATMAP] + [5. NOIR LIGHTING & FINISH]
```

### Ví dụ Prompt Mẫu:

#### Ví dụ 1: Tàu ngầm hạt nhân lớp Ohio (Classified Cyber CAD)
```text
"A high-precision 3D architectural and mechanical isometric cutaway diagram of a modern nuclear ballistic submarine in Blueprint Noir style. 
Deep navy-blue blueprint paper background with subtle coordinate grids, measurement scales, and technical CAD annotations. 
The central hull reveals authentic real-world slice-through X-ray internal cross-sections showing the pressurized nuclear reactor chamber, 24 vertical Trident missile launch tubes, main control room, steam turbines, and crew quarters. 
Crisp electric cyan and chalk-white technical wireframe outlines, accented with glowing neon-yellow highlight zones on coolant pipelines. 
Tiny glowing thermal heatmap orange silhouettes of crew members working in compartments to establish scale. 
Cinematic dark noir lighting, high contrast, clean vector precision, high resolution architectural drawing."
```

#### Ví dụ 2: Lăng Mộ Tần Thủy Hoàng (Antique Da Vinci Noir)
```text
"A striking 3D archaeological isometric cutaway diagram of Emperor Qin's underground imperial tomb in Antique Blueprint Noir style. 
Dark weathered charcoal slate background with faint ancient parchment grid lines and gold drafting callouts. 
The subterranean cross-section reveals multi-tiered tomb chambers with glowing molten gold rivers of liquid mercury flowing through miniature copper landscapes and mechanical bronze crossbow trigger mechanisms. 
Intricate brass-gold and chalk-white architectural linework, accented with warm glowing amber lanterns and historical annotations. 
Cinematic atmospheric noir lighting, deep shadows, fine technical engraving aesthetic, high resolution."
```

---

## 5. Từ Vựng Chuyển Động Google Flow & Độ Chính Xác Vật Lý

Khi tạo video clip từ Keyframe qua Google Flow (FlowKit):

### ✅ Chuyển Động Chính Xác Với Thực Tế (Khuyên Dùng):
* `push_in`: Đẩy chậm tuyến tính vào buồng máy / khoang bí mật trung tâm (tạo cảm giác khám phá sâu mà không làm méo góc nhìn).
* `pan_left` / `pan_right`: Quét ngang qua các khoang máy từ đuôi tàu lên mũi tàu dọc theo trục thẳng.
* `tilt_down`: Quét thẳng đứng từ mặt đất xuống sâu dưới hầm ngầm.
* `light_sweep`: Tia laser radar quét phẳng ngang qua bề mặt bản vẽ kỹ thuật.
* `element_motion`: Dòng chảy phát sáng di chuyển bên trong các đường ống dẫn (`glowing coolant fluid flowing steadily through primary pipes`).

### ⛔ Chuyển Động Bị Cấm Tuyệt Đối:
* ❌ Xoay vòng tròn 360 độ (gây méo mó góc phối cảnh CAD).
* ❌ Đột ngột biến đổi hình dạng vật thể (morphing).
* ❌ Các chi tiết cơ khí bị uốn cong hoặc trôi nổi vô lý.

---

## 6. Voice & Âm Nhạc (Audio Design)

* **Voice TTS:** Giọng nam xAI `leo` (trầm, chậm rãi, uy quyền, mang âm hưởng phim tài liệu điều tra cao cấp).
* **Music Genre:** *Dark Ambient Synthwave / Minimalist Cinematic Electronic* (nhịp bass dồn dập, tiếng tích tắc đồng hồ cơ khí, âm thanh tần số thấp tạo cảm giác bí mật quân sự).

---

## 7. Schema `beats.json` Dành Cho Blueprint Noir

### 💡 Quy Định Trường `motion_type` (Hybrid Static / Dynamic):
* `"motion_type": "static"` (hoặc `"static_pan"`, `"static_zoom"`, `"static_still"`):
  * **Hành vi:** Script `clips.py` và `assemble.py` sẽ **tự động render clip tĩnh 24 FPS trực tiếp trên máy bằng FFmpeg** từ ảnh Keyframe, KHÔNG gửi lên Google Flow.
  * **Ưu điểm:** Giữ nguyên 100% độ sắc nét sắc lẹm của bản vẽ CAD gốc, áp dụng hiệu ứng camera trượt nhẹ (Ken Burns / Pan / Zoom), tốc độ xử lý 0.5s/shot, 0% rủi ro lỗi hình học.
* `"motion_type": "dynamic"`:
  * **Hành vi:** Gửi request lên **Google Flow (FlowKit)** để sinh hoạt ảnh mô phỏng luồng chuyển động vật lý thực tế (dòng nước, pít-tông, tia laser quét).

```json
{
  "project": "project-name",
  "aspect_ratio": "16:9",
  "theme": "classified_cyber_cad",
  "caption_style": "white",
  "watermark": "Blackprint",
  "watermark_image": "assets/blackprint_watermark.png",
  "beats": [
    {
      "id": "beat_1",
      "shot": "1a",
      "duration": 6.5,
      "title_en": "THE SECRET ATOM",
      "camera": "push_in",
      "motion_type": "dynamic", 
      "keyframe_prompt": "A high-precision 3D isometric cutaway of...",
      "narration": "Inside this 18,000-ton steel giant lies a secret machine...",
      "element_motion": "Electric cyan wireframe glows, glowing energy pulse traveling steadily through coolant conduits"
    },
    {
      "id": "beat_2",
      "shot": "2",
      "duration": 7.0,
      "camera": "pan_left",
      "motion_type": "static",
      "keyframe_prompt": "A detailed full-length architectural cross-section schematic of...",
      "narration": "From the forward sonar dome to the dual-hull reactor compartment...",
      "element_motion": "Static schematic with subtle linear camera slide and vector HUD overlay"
    }
  ]
}
```

---

## 8. Model Selection (Lựa Chọn AI Model Tối Ưu)

| Loại Tác Vụ | Model Ưu Tiên | Lý Do |
|---|---|---|
| **Text-to-Image (Keyframes)** | `google/nano-banana-2/text-to-image-developer` hoặc `Flux.1 Pro` | Khả năng render chi tiết hình học, chữ CAD và ánh sáng neon đỉnh cao nhất. |
| **Image-to-Video (Motion)** | `Google FlowKit` / `Veo 2` | Duy trì 100% tính toàn vẹn hình học (Zero geometry warping) khi camera push_in. |
| **Voice TTS** | `xAI TTS` (`leo`) | Độ trầm ấm, nhịp ngắt tự nhiên chuẩn phát thanh viên Mỹ. |
