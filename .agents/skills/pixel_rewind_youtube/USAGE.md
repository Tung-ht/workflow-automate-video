# 📖 Hướng Dẫn Sử Dụng — Pixel Rewind Combo Skill

Tài liệu này hướng dẫn bạn cách prompt AI Agent để tạo video Pixel Rewind **từ con số 0** —
từ chọn chủ đề, viết kịch bản, đến xuất file `final_crt.mp4`.

> **Ai đọc file này?** Bạn — chủ kênh. Đây KHÔNG phải file cho Agent đọc (Agent đọc `SKILL.md`).
> File này dạy bạn **nói gì** với Agent để nó chạy đúng pipeline.

---

## ⚡ Khởi động nhanh (Quick Start)

### Cách nhanh nhất — 1 câu prompt duy nhất:

```
Tạo video pixel rewind short 45s về "How a janitor at Nintendo invented the Game Boy"
```

Agent sẽ tự động:
1. Nghiên cứu Reddit → tìm Easter Egg facts
2. Viết `beats.json` → hiện cho bạn duyệt
3. Tạo ảnh pixel art → tạo video motion → thu âm giọng đọc + nhạc nền
4. Ghép video + CRT overlay → xuất `final_crt.mp4` + `thumbnail.png`

**Bạn chỉ cần duyệt 1 lần** (ở bước beats.json) rồi ngồi chờ.

---

## 🎯 Các mẫu prompt theo tình huống

### Tình huống 1: Tạo video Short (45 giây) — Phổ biến nhất

```
Tạo video pixel rewind short 45s về "The $3 billion typo that killed Sega"
```

Hoặc chi tiết hơn:

```
Tạo video pixel rewind short 45s:
- Chủ đề: "Why your microwave still runs on 1970s code"
- Theme: crt-arcade
- Ngôn ngữ: English
```

---

### Tình huống 2: Tạo video Long-form (3-5 phút)

```
Tạo video pixel rewind long-form 3 phút về "The intern who wrote Tetris — and never saw a penny"
```

Hoặc chỉ định theme cụ thể:

```
Tạo video pixel rewind long-form 5 phút:
- Chủ đề: "How dial-up internet actually worked"
- Theme: terminal-green
- Arc: how_it_works
```

---

### Tình huống 3: Tạo combo Short + Long-form cùng chủ đề

Đây là flow **khuyến nghị** — tạo Long-form trước, rút Short sau:

```
Tạo combo pixel rewind cho chủ đề "Atari buried millions of cartridges in a desert. We found them."
- Long-form: 3 phút, theme vhs-rewind
- Short: 45s, rút từ góc gây sốc nhất của Long-form
```

Agent sẽ:
1. Viết beats.json Long-form trước → bạn duyệt
2. Sản xuất Long-form → `final_crt.mp4`
3. Rút 1 góc mạnh nhất → viết beats.json Short (tái sử dụng keyframe) → bạn duyệt
4. Sản xuất Short → `final_crt.mp4`

---

### Tình huống 4: Chỉ viết kịch bản (beats.json), chưa sản xuất

```
Viết beats.json pixel rewind short 45s cho chủ đề "Why the GameBoy was intentionally ugly"
- Chỉ viết kịch bản, chưa sản xuất video
```

Agent sẽ:
1. Nghiên cứu Reddit
2. Viết beats.json hoàn chỉnh
3. Hiện cho bạn duyệt, KHÔNG chạy pipeline production

→ Bạn có thể sửa kịch bản thoải mái trước khi nói: **"OK, sản xuất đi"**

---

### Tình huống 5: Đã có beats.json, chỉ cần sản xuất

```
Sản xuất video pixel retro từ beats.json tại out/gameboy/beats.json
```

Agent sẽ bỏ qua bước viết kịch bản, chạy thẳng pipeline:
keyframes → clips → audio → draft → assemble → CRT overlay

---

### Tình huống 6: Chỉ muốn xem bản nháp (Draft — $0)

```
Tạo draft pixel rewind cho "The teenager who saved Nintendo"
- Chỉ tạo đến draft, KHÔNG tạo video motion (tiết kiệm tiền)
```

Agent sẽ:
1. Viết beats.json
2. Tạo ảnh pixel art (keyframes) — ~$0.04/shot
3. Thu âm giọng đọc + nhạc
4. Ghép ảnh tĩnh + audio = `draft.mp4` (ffmpeg, $0)

→ Bạn xem draft kiểm tra nhịp điệu, timing. OK thì nói: **"Sản xuất full đi"** — Agent chạy tiếp từ bước video motion.

---

### Tình huống 7: Gợi ý chủ đề

```
Gợi ý 10 chủ đề pixel rewind hay nhất cho tuần này
```

Hoặc cụ thể hơn:

```
Gợi ý 5 chủ đề pixel rewind về lịch sử console wars thập niên 90
```

Agent sẽ dùng Reddit MCP để tìm trending topics + easter eggs, rồi gợi ý danh sách chủ đề
với hook sẵn.

---

## 🎨 Chọn Theme (Visual Style)

Khi prompt, bạn có thể chỉ định 1 trong 6 theme. Nếu không chỉ định, Agent mặc định dùng `crt-arcade`.

| Theme | Khi nào dùng | Ví dụ chủ đề |
|---|---|---|
| **`crt-arcade`** (mặc định) | Arcade, console wars, classic games | "How Pac-Man conquered the world" |
| **`gameboy-green`** | Handheld gaming, Game Boy history | "Why the GameBoy was intentionally ugly" |
| **`vhs-rewind`** | 90s tech, home computing, early internet | "The rise and fall of AOL" |
| **`terminal-green`** | Hacker stories, programming, OS wars | "How Linux was born in a dorm room" |
| **`snes-16bit`** | SNES/Genesis era, RPG history | "The secret team behind Final Fantasy" |
| **`commodore-beige`** | Early PC, hobbyist computing | "The bedroom coders who built an empire" |

**Cách chỉ định trong prompt:**
```
Tạo video pixel rewind short 45s về "How Linux was born" — dùng theme terminal-green
```

---

## 🔀 Chọn Narrative Arc (Cách kể chuyện)

| Arc | Khi nào dùng | Ví dụ |
|---|---|---|
| **`timeline`** (mặc định) | Lịch sử tech theo thời gian | "The evolution of the gamepad" |
| **`man_in_hole`** | Rise → Fall → Rise lại | "Nokia: from rubber boots to smartphones to... rubber boots" |
| **`how_it_works`** | Giải thích kỹ thuật | "How dial-up internet actually worked" |

**Cách chỉ định:**
```
Tạo video pixel rewind 3 phút về "The rise and fall of BlackBerry" — arc: man_in_hole, theme: vhs-rewind
```

---

## 💰 Chi phí ước tính

| Loại video | Số shots | Chi phí |
|---|---|---|
| Draft (ảnh tĩnh + audio) | 6-7 | **~$0.40** |
| Short 45s (full production) | 6-7 | **~$5** |
| Long-form 3 phút | 24-27 | **~$19** |
| Combo (Long + Short cùng chủ đề) | 30-34 | **~$21** (tiết kiệm nhờ tái sử dụng keyframe) |

> **Mẹo:** Luôn chạy Draft trước khi sản xuất full. Draft chỉ tốn ~$0.40 mà giúp bạn
> kiểm tra pacing, timing, nội dung narration. Sửa kịch bản ở bước draft rẻ hơn 50x
> so với sản xuất full rồi mới phát hiện lỗi.

---

## 🔄 Flow đầy đủ từ A-Z (Step by step)

Dưới đây là quy trình hoàn chỉnh để tạo 1 video, bao gồm cả những lúc bạn cần can thiệp:

### Bước 1: Chọn chủ đề
```
Gợi ý 5 chủ đề pixel rewind về lịch sử Nintendo
```
→ Agent trả về danh sách. Bạn chọn 1.

### Bước 2: Viết kịch bản
```
Viết beats.json pixel rewind short 45s cho chủ đề "How a janitor invented the Game Boy"
```
→ Agent nghiên cứu Reddit, viết beats.json, hiện cho bạn.

### Bước 3: Duyệt kịch bản ← **BẠN CAN THIỆP Ở ĐÂY**
Đọc beats.json. Bạn có thể:
- **"OK, sản xuất đi"** → Agent chạy tiếp
- **"Sửa shot 3 — thêm chi tiết về..."** → Agent sửa, hiện lại
- **"Hook chưa đủ shock, viết lại shot 1"** → Agent viết lại

### Bước 4: Chạy Draft (khuyến nghị)
```
Tạo draft trước
```
→ Agent tạo ảnh pixel art + audio → ghép draft.mp4 ($0.40)
→ Bạn xem draft. Nếu OK:

### Bước 5: Sản xuất full
```
OK, sản xuất full đi
```
→ Agent chạy video motion → assemble → CRT overlay → `final_crt.mp4`

### Bước 6: Kiểm tra
→ Agent tự verify: pixel art không bị mushed, scanlines không quá đậm, text đọc được.
→ Nếu có shot nào bị lỗi, Agent auto retry.

### Bước 7: Tạo Thumbnail
```
Tạo thumbnail
```
→ Agent tạo `thumbnail.png` theo prompt trong beats.json

### Bước 8 (Nếu muốn combo): Tạo Short đi kèm
```
Rút short 45s từ video long-form này
```
→ Agent phân tích đâu là fact gây sốc nhất → viết beats.json Short → sản xuất

---

## 🛠️ Các prompt điều chỉnh trong quá trình sản xuất

### Sửa kịch bản sau khi đã viết:
```
Sửa shot 2 — narration quá dài, cắt ngắn lại
```

```
Thêm 1 easter egg fact vào shot 4 — tôi muốn mention việc Nintendo từng bán taxi
```

```
Hook chưa đủ mạnh — viết lại shot 1 theo kiểu "A 19-year-old intern..."
```

### Đổi theme giữa chừng:
```
Đổi theme sang gameboy-green — chủ đề này phù hợp hơn
```

### Chỉ sản xuất lại 1 shot bị lỗi:
```
Shot 4 bị mush pixel art — tạo lại clip cho shot 4 với motion_style calm hơn
```

### Tạo thumbnail riêng:
```
Tạo thumbnail pixel rewind với text "UGLY ON PURPOSE" — Game Boy trên nền đen, glow xanh
```

---

## ⚠️ Những lưu ý quan trọng

### 1. Luôn duyệt beats.json trước khi sản xuất
Đây là bước rẻ nhất ($0) — sửa ở đây tiết kiệm hàng chục đô so với sửa sau production.

### 2. Dùng Draft Mode cho video đầu tiên
Chạy draft ($0.40) trước khi full production ($5-19). Kiểm tra pacing, timing, narration.

### 3. Long-form trước, Short sau
Khi làm combo, luôn làm Long-form trước. Short rút từ insight mạnh nhất của Long-form.

### 4. Đăng Long-form trước Short 4-24 giờ
Khi đăng YouTube: Long-form sáng → Short chiều/tối. Không đăng cùng lúc.

### 5. KHÔNG sửa câu Outro CTA
Hai câu CTA là bất biến — chữ ký âm thanh của kênh. Không sửa dù 1 từ.

### 6. Kiểm tra API key trước khi bắt đầu
```
Kiểm tra ATLASCLOUD_API_KEY đã set chưa
```

---

## 📋 Bảng tham chiếu nhanh (Cheat Sheet)

| Bạn muốn... | Prompt |
|---|---|
| Video short 45s | `Tạo video pixel rewind short 45s về "[chủ đề]"` |
| Video dài 3 phút | `Tạo video pixel rewind long-form 3 phút về "[chủ đề]"` |
| Combo Short + Long | `Tạo combo pixel rewind cho "[chủ đề]"` |
| Chỉ kịch bản | `Viết beats.json pixel rewind cho "[chủ đề]"` |
| Chỉ draft | `Tạo draft pixel rewind cho "[chủ đề]"` |
| Gợi ý chủ đề | `Gợi ý 10 chủ đề pixel rewind` |
| Chọn theme | Thêm `— theme: terminal-green` vào cuối prompt |
| Chọn arc | Thêm `— arc: man_in_hole` vào cuối prompt |
| Sản xuất từ beats.json có sẵn | `Sản xuất video pixel retro từ out/[project]/beats.json` |
| Tạo thumbnail | `Tạo thumbnail pixel rewind với text "[TEXT]"` |
| Kiểm tra chi phí | `Ước tính chi phí video pixel rewind [thời lượng]` |

---

## 📂 Cấu trúc thư mục output

Sau khi sản xuất xong, bạn sẽ thấy:

```
out/<project>/
├── beats.json              # Kịch bản
├── keyframes/
│   ├── kf_1.png            # Ảnh pixel art cho mỗi shot
│   ├── kf_2.png
│   └── ...
├── clips/
│   ├── clip_1.mp4          # Video motion cho mỗi shot
│   ├── clip_2.mp4
│   └── ...
├── audio/
│   ├── narr_1.mp3          # Giọng đọc cho mỗi shot
│   ├── narr_2.mp3
│   ├── music.mp3           # Nhạc nền chiptune
│   └── ...
├── draft.mp4               # Bản nháp (ảnh tĩnh + audio)
├── final.mp4               # Video hoàn chỉnh (chưa CRT)
├── final_crt.mp4           # ✅ VIDEO CUỐI CÙNG (có CRT overlay)
└── thumbnail.png           # Thumbnail cho YouTube
```

---

*File này thuộc bộ skill `pixel_rewind_youtube`. Xem thêm:*
- *[SKILL.md](SKILL.md) — Chiến lược kênh (cho Agent đọc)*
- *[../pixel_retro_director/SKILL.md](../pixel_retro_director/SKILL.md) — Pipeline kỹ thuật (cho Agent đọc)*
- *[../pixel_retro_director/COST_OPTIMIZATION.md](../pixel_retro_director/COST_OPTIMIZATION.md) — Bảng chi phí chi tiết*
