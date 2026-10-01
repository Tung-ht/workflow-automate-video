# 📖 Hướng Dẫn Sử Dụng — Papercut Business Video Factory

> Tài liệu này hướng dẫn bạn cách dùng 2 skill `papercut_business_youtube` +
> `vox_papercut_director` kết hợp với Reddit MCP để tạo video từ A-Z.

---

## 🔧 Thiết Lập Ban Đầu (Chỉ Cần Làm 1 Lần)

### Bước 0: Kiểm tra Prerequisites

```powershell
# Kiểm tra ffmpeg
ffmpeg -version

# Kiểm tra Python + Pillow
python3 -c "import PIL; print('OK')"

# Kiểm tra API key (Atlas Cloud)
echo $env:ATLASCLOUD_API_KEY
```

Nếu thiếu:

- **ffmpeg:** Tải từ https://ffmpeg.org/download.html → thêm vào PATH
- **Pillow:** `pip install Pillow`
- **Atlas Cloud API Key:** Đăng ký tại https://www.atlascloud.ai/console/api-keys → set biến môi trường:
  ```powershell
  $env:ATLASCLOUD_API_KEY = "your_key_here"
  ```

### Bước 1: Khởi Động Chrome Cho Reddit MCP

> ⚠️ **Quan trọng:** Nên dùng Chrome Profile riêng (không login ngân hàng/email).

Mở Window+R, paste lệnh:

```
# Mở Chrome với cổng CDP 9222
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir=C:\Users\Admin\chrome-cdp https://www.reddit.com
```

Sau khi Chrome mở:

1. Vào **reddit.com**
2. **Đăng nhập** tài khoản Reddit của bạn
3. **Để tab Reddit mở** (không đóng) — MCP cần tab này để hoạt động

### Bước 2: Khởi Động Antigravity

Mở Antigravity mới (hoặc restart nếu đang chạy). MCP server `reddit` sẽ tự động kết nối tới Chrome.

**Kiểm tra kết nối:**
Gõ vào Antigravity:

```
kiểm tra kết nối reddit mcp, gọi tool reddit_ensure_session
```

Nếu thành công sẽ thấy: `Logged in as u/<tên_reddit_của_bạn>`

### Bước 3: Khởi Động Flowkit

Vào thư mục flowkit_repo và khởi động flowkit:

```
cd flowkit_repo
python -m agent.main
```

---

## 🎬 Tạo Video — Prompt Mẫu Theo Từng Bước

### Quy Trình Tổng Quan

```
[Ý TƯỞNG] → [NGHIÊN CỨU REDDIT] → [VIẾT KỊCH BẢN] → [DUYỆT] → [SẢN XUẤT]

Skill dùng:     papercut_business_youtube                    vox_director
Bước:      1. Chọn đề tài ──→ 2. Reddit research ──→ 3. beats.json ──→ 4. Duyệt
           ──→ 5. Style bakeoff ──→ 6. Keyframes ──→ 7. Motion ──→ 8. Audio
           ──→ 9. Draft ──→ 10. Assemble + Thumbnail ──→ 🎉 final.mp4
```

---

### 🟢 CÁCH 1: Prompt Đơn Giản Nhất (Agent Tự Làm Mọi Thứ)

Chỉ cần gõ **1 câu**, agent sẽ tự chạy cả pipeline:

#### Cho Video Short (45s):

```
Làm video short 45s về "Costco Hot Dog $1.50" cho kênh Papercut Business.
Nghiên cứu Reddit trước rồi viết kịch bản.
```

#### Cho Video Long-form (3-5 phút):

```
Làm video dài 3-5 phút về "Tại sao máy tính TI-84 giá $100+ suốt 30 năm"
cho kênh Papercut Business. Cần thumbnail.
```

> Agent sẽ tự động:
>
> 1. Kích hoạt skill `papercut_business_youtube`
> 2. Search Reddit → thu thập perspectives
> 3. Viết kịch bản bằng "Papercut Persona" (giọng Mỹ tự nhiên)
> 4. Chạy Imperfection Pass
> 5. **Dừng lại hỏi bạn duyệt kịch bản** ← bạn duyệt ở đây
> 6. Sau khi duyệt → chuyển sang `vox_director` sản xuất

---

### 🟡 CÁCH 2: Prompt Từng Bước (Kiểm Soát Tối Đa)

Dùng cách này khi bạn muốn can thiệp sâu vào từng giai đoạn:

#### Bước 1 — Chọn Chủ Đề

```
Gợi ý 5 chủ đề video cho series "Everyday Monopolies" của kênh Papercut Business.
Ưu tiên chủ đề gây tò mò cao, có data thú vị, phù hợp khán giả Mỹ 25-55 tuổi.
```

#### Bước 2 — Nghiên Cứu Reddit

```
Nghiên cứu Reddit về chủ đề "Costco Hot Dog $1.50".
Tìm trên r/Costco, r/todayilearned, r/Economics, r/Anticonsumption.
Lọc ra 5 bình luận có insight mạnh nhất (trải nghiệm cá nhân, góc nhìn trái chiều,
câu nói sắc sảo).
```

#### Bước 3 — Viết Kịch Bản

```
Viết beats.json cho video short 45s về Costco Hot Dog.
Dùng Papercut Persona (giọng anh Mỹ 32-38t, tò mò, hơi bức xúc).
Chèn Reddit insights đã nghiên cứu vào.
Chạy Imperfection Pass.
Aspect ratio: 9:16.
```

#### Bước 4 — Duyệt Kịch Bản

Agent sẽ xuất kịch bản cho bạn. Bạn đọc và:

```
# Nếu OK:
OK, duyệt kịch bản. Tiến hành sản xuất.

# Nếu muốn sửa:
Sửa shot 3: thêm chi tiết về con số $1.50 từ năm 1985.
Bỏ câu "Furthermore" ở shot 5, thay bằng "Here's the kicker."
```

#### Bước 5 — Chọn Style (Bakeoff)

```
Chạy style bakeoff cho project costco-hotdog.
Thử các theme: american-retro, newsprint-editorial, atomic-age.
```

Agent sẽ tạo 3 ảnh mẫu để bạn chọn style ưng nhất.

#### Bước 6 → 10 — Sản Xuất (Tự Động)

```
Sản xuất video từ beats.json đã duyệt.
Chạy lần lượt: keyframes → clips → audio → draft → assemble.
```

Hoặc chạy từng bước nếu muốn kiểm tra:

```
# Chỉ tạo keyframes (ảnh collage):
Chạy keyframes cho project costco-hotdog

# Xem draft trước khi tốn tiền motion:
Chạy draft mode cho project costco-hotdog

# OK rồi, chạy motion + audio + ghép:
Chạy clips, audio, assemble cho project costco-hotdog

# Tạo thumbnail (chỉ cho long-form):
Chạy thumbnail cho project costco-hotdog
```

---

## 📋 Bảng Tham Chiếu Nhanh — Prompt Theo Tình Huống

| Bạn muốn...           | Prompt                                                                    |
| --------------------- | ------------------------------------------------------------------------- |
| **Ý tưởng mới**       | `Gợi ý 5 chủ đề video Everyday Monopolies`                                |
| **Nghiên cứu đề tài** | `Nghiên cứu Reddit về [chủ đề]`                                           |
| **Video Short nhanh** | `Làm video short 45s về [chủ đề] cho Papercut Business`                   |
| **Video Long-form**   | `Làm video dài 3-5 phút về [chủ đề] cho Papercut Business, cần thumbnail` |
| **Chỉ viết kịch bản** | `Viết beats.json cho [chủ đề], chưa cần sản xuất`                         |
| **Sửa kịch bản**      | `Sửa shot X: [nội dung sửa]`                                              |
| **Xem draft 0đ**      | `Chạy draft mode cho project [tên]`                                       |
| **Sản xuất full**     | `Sản xuất video từ beats.json đã duyệt`                                   |
| **Chỉ thumbnail**     | `Tạo thumbnail cho project [tên]`                                         |
| **Tạo logo kênh**     | `Tạo watermark logo PNG "Papercut Business" phong cách Vox`               |

---

## 📁 Cấu Trúc Output

Sau khi hoàn thành, tất cả file nằm trong `out/<tên-project>/`:

```
out/costco-hotdog/
├── beats.json              ← Kịch bản (nguồn sự thật duy nhất)
├── keyframes/              ← Ảnh collage cho từng shot
│   ├── kf_1a.jpg
│   ├── kf_2a.jpg
│   └── ...
├── clips/                  ← Video motion cho từng shot
│   ├── clip_1a.mp4
│   └── ...
├── audio/
│   ├── vo_1.mp3            ← Voice-over từng beat
│   └── music.mp3           ← Nhạc nền instrumental
├── draft.mp4               ← Bản nháp (keyframes + voice, không motion)
├── final.mp4               ← 🎉 VIDEO HOÀN CHỈNH
└── thumbnail.png           ← Thumbnail (chỉ long-form)
```

---

## ⚡ Mẹo Quan Trọng

### Tiết kiệm tiền:

1. **LUÔN chạy Draft trước** (`draft.py`) — nghe voice-over, kiểm tra pacing. Nếu không ưng → sửa beats.json → chạy draft lại. Chỉ chạy `clips.py` (tốn tiền) khi draft đã hoàn hảo.
2. **Dùng 1 shot/beat** thay vì 2 → giảm 50% chi phí motion.
3. **Tái sử dụng keyframe** giữa Short và Long-form cùng chủ đề.

### Chất lượng kịch bản:

4. **Đừng skip bước Reddit research** — đây là thứ tạo ra "dấu vân tay tác giả" giúp video không bị YouTube xếp vào "generic AI content".
5. **Đọc kịch bản thành tiếng** trước khi duyệt — nếu câu nào không đọc được trong 1 hơi thở → quá dài → bảo agent cắt.

### Kỹ thuật:

6. **Chrome CDP phải luôn mở** khi dùng Reddit MCP. Nếu gặp lỗi "No Reddit tab found" → kiểm tra tab Reddit còn mở không.
7. **Mỗi lần restart Antigravity** → MCP server được load lại. Không cần restart Chrome.
8. **Voice ID cố định:** Kênh dùng `leo` (xAI TTS) — không đổi voice giữa các video.

---

## 🔴 Troubleshooting

| Lỗi                                | Nguyên nhân                                | Cách sửa                                              |
| ---------------------------------- | ------------------------------------------ | ----------------------------------------------------- |
| `No Reddit tab found in Chrome`    | Chrome chưa mở hoặc chưa có tab reddit.com | Mở Chrome CDP + vào reddit.com                        |
| `CDP call timed out after 30s`     | Chrome bị treo hoặc Reddit tab bị crash    | Refresh tab Reddit trong Chrome                       |
| `Could not get modhash`            | Chưa đăng nhập Reddit                      | Login Reddit trong Chrome                             |
| `ATLASCLOUD_API_KEY not set`       | Thiếu API key                              | Set `$env:ATLASCLOUD_API_KEY`                         |
| Keyframe trông không giống collage | Prompt yếu                                 | Bảo agent đọc `references/prompt-guide.md` và re-roll |
| Video motion bị biến dạng text     | Camera move quá mạnh                       | Đổi `constraints` sang `strict`, tránh `orbit`/`roll` |
| Thumbnail quá "AI smooth"          | Film grain chưa đủ mạnh                    | Chạy lại `thumbnail.py --force`                       |

---

## 📅 Chiến Lược Sản Xuất & Đăng Video Cho 1 Chủ Đề

### Thứ tự sản xuất: Long-form TRƯỚC, Short SAU

Long-form chứa toàn bộ nghiên cứu → bạn biết rõ đâu là hook mạnh nhất → rút ra làm Short.

```
Bước 1: Nghiên cứu Reddit
Bước 2: Viết beats.json LONG-FORM (3-5 phút) → duyệt
Bước 3: Sản xuất Long-form → final_long.mp4 + thumbnail.png
Bước 4: Từ Long-form, RÚT 1 góc mạnh nhất → viết beats.json SHORT (45s)
Bước 5: Sản xuất Short (tái sử dụng keyframe → tiết kiệm ~30%)
```

### Thứ tự đăng YouTube: Long-form TRƯỚC, Short sau 4-24h

| Bước | Khi nào                   | Làm gì                                                      |
| ---- | ------------------------- | ----------------------------------------------------------- |
| 1    | Ngày N, sáng (8-10am EST) | Đăng **Long-form**                                          |
| 2    | Ngày N chiều/tối hoặc N+1 | Đăng **Short**                                              |
| 3    | Ngay sau đăng Short       | YouTube Studio → Short → **Related Video** → chọn Long-form |

> ⚠️ **KHÔNG đăng Short trước Long-form.** Khi Short viral mà chưa có Long-form,
> người xem tò mò bấm vào kênh → không có gì xem → rời đi vĩnh viễn.

### Prompt mẫu cho cả cặp video:

```
# Bước 1: Làm Long-form trước
Làm video dài 3-5 phút về "Costco Hot Dog $1.50" cho Papercut Business.
Nghiên cứu Reddit trước. Cần thumbnail.

# Bước 2: Sau khi Long-form xong, làm Short
Làm video short 45s về cùng chủ đề Costco Hot Dog.
Rút 1 góc nhìn gây sốc nhất từ video dài vừa làm.
Tái sử dụng keyframe từ project long-form nếu phù hợp.
```

---

## 🚀 Quick Start — Tạo Video Đầu Tiên Trong 5 Phút

**Bước 1:** Mở PowerShell, chạy:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**Bước 2:** Trong Chrome → vào reddit.com → đăng nhập

**Bước 3:** Mở Antigravity, gõ:

```
Làm video short 45s về "Costco bán hot dog $1.50 suốt 40 năm"
cho kênh Papercut Business. Nghiên cứu Reddit trước.
```

**Bước 4:** Đợi agent nghiên cứu + viết kịch bản → **duyệt kịch bản**

**Bước 5:** Gõ `OK, duyệt. Sản xuất đi.` → Agent tự chạy hết pipeline

**Bước 6:** Nhận `out/<project>/final.mp4` 🎉
