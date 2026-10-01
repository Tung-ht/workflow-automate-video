# Channel Identities & Brand Standards

Khi sản xuất video, AI PHẢI tra bảng này để áp dụng đúng tham số cho kênh được yêu cầu.

## 1. Bảng Tham Số Nhận Diện Kênh

| Tham số | Papercut Business | Pixel Rewind | Pulp Hypotheses | Blackprint |
|---------|-------------------|--------------|-----------------|------------|
| `voice_id` | `leo` | `leo` | `leo` | `leo` |
| `caption_style` | `paper` | `white` | `yellow_comic` | `white` |
| `upload_schedule` | Thứ 4 & Thứ 7 (Wed & Sat) | Thứ 2 & Thứ 5 (Mon & Thu) | Thứ 3 & Thứ 6 (Tue & Fri) | Thứ 3 & Thứ 6 (Tue & Fri) |
| `watermark` | `Papercut Business` | `Pixel Rewind` | `Pulp Hypotheses` | `Blackprint` |
| `watermark_image` | `assets/papercut_business_watermark.png` | `assets/pixel_rewind_watermark.png` | `assets/pulp_hypotheses_watermark.png` | `assets/blackprint_watermark.png` |
| `crt_post` | ❌ KHÔNG dùng | `true` (bắt buộc) | ❌ KHÔNG dùng | ❌ KHÔNG dùng |
| `avatar_prompt` | `Minimalist torn-paper collage avatar of a globe and gold coin, bold wood-type typography 'PB', high contrast flat color, isolated center` | `8-bit pixel art avatar of a retro arcade cabinet glowing with CRT phosphor light, green neon typography 'PR', centered` | `Retro 1980s pulp comic avatar of a scientist in comic superhero pose with glowing eyes, halftone dots, heavy black ink lines, centered` | `Minimalist glowing technical vector avatar of an isometric 3D wireframe cube intersecting a gear, electric cyan and neon yellow outlines, dark navy slate background, crisp CAD precision, centered` |
| `banner_safe_zone_text` | `PAPERCUT BUSINESS - Everyday Monopolies - New Episodes Wed & Sat` | `PIXEL REWIND - Retro Tech & Gaming History - New Episodes Mon & Thu` | `PULP HYPOTHESES - Mind-Bending What-If Files - New Episodes Tue & Fri` | `BLACKPRINT - Universal 3D Schematics & Megastructures - New Episodes Tue & Fri` |

---

## 1.5. Quy Chuẩn Tạo Channel Banner & Avatar (YouTube Channel Branding)

Khi thiết lập kênh hoặc người dùng yêu cầu làm bộ nhận diện kênh (Channel Branding):

### Kích thước Banner Chuẩn YouTube:
- **Full Canvas (TV Display):** `2560 x 1440 px` (Aspect Ratio 16:9).
- **Vùng An Toàn (Desktop & Mobile Safe Zone):** `1546 x 423 px` (nằm chính giữa trung tâm ảnh).

### Quy tắc ghép Banner:
1. **Lớp Nền (Background Canvas 2560x1440):** Dùng AI sinh ảnh theo phong cách đặc trưng của kênh (Paper Collage / Pixel Art CRT / Pulp Comic / Blueprint Noir) mở rộng toàn màn hình.
2. **Lớp Trung Tâm (Safe Zone 1546x423):** Đặt Tên Kênh khổng lồ, Tagline thương hiệu và Lịch đăng video (`New Episode Every Week`) nằm trọn trong vùng an toàn trung tâm.

---

## 2. Chiến Lược First Frame Thumbnail Cho YouTube Shorts (Frame 0 Optimization)

YouTube Shorts trên máy tính KHÔNG hỗ trợ upload file thumbnail riêng biệt. Thuật toán Shorts Feed tự động lấy **Frame 0 (Giây 0.00 / Shot 1a)** làm thumbnail hiển thị duy nhất trên Shorts Feed, danh sách tìm kiếm và trang kênh.

### Công Thức 3 Lớp Cho Frame 0 (Shot 1a):
1. **Lớp 1 (Visual Anchor + Embedded Headline)**: Shot 1a (`kf_1a.jpg`) BẮT BUỘC chèn chỉ thị vẽ chữ tiêu đề trực tiếp vào `keyframe_prompt` khi tạo ảnh AI. Ngay khi `keyframes.py` sinh ảnh 1a, hình ảnh ĐÃ CÓ sẵn chữ Headline khổng lồ nét cứng đập vào mắt người xem:
   - **Papercut Business (Paper Collage)**: `"...Include a torn-paper banner with a big bold cut-out English headline '[TITLE_EN]' in bold wood-type / heavy slab, all-caps. Keep the headline crisp and legible."`
   - **Pixel Rewind (Pixel Art)**: `"...Include a prominent 8-bit retro banner with big bold English headline '[TITLE_EN]' in neon yellow pixel typography, clear and readable."`
   - **Pulp Hypotheses (Retro Comic)**: `"...Include a dramatic retro comic book headline banner with big bold English text '[TITLE_EN]' in heavy black ink superhero typography, yellow fill with thick black outlines, crisp and readable."`
   - **Blackprint (Blueprint Noir)**: `"...Include a prominent technical CAD title banner with big bold English headline '[TITLE_EN]' in crisp electric-cyan and neon-yellow typography, highly visible and legible against the dark blueprint grid."`
2. **Lớp 2 (Bold Headline Text Card in Assembly)**: Beat 1 BẮT BUỘC chứa `"title_en"` (3-5 từ in hoa giật gân/bức xúc/trái trực giác) và Shot 1a set `"title": true`. Script `assemble.py` bọc thêm lớp thẻ chữ nét cứng tăng cường khả năng đọc.
3. **Lớp 3 (Kinetic Subtitle at t=0.00s)**: Thoại cất lên ngay milisecond 0.00 (không trễ 0.5s pause ở đầu audio). Script `assemble.py` render phụ đề kinetic dán nổi đè lên Frame 0.

> ⛔ **CẤM CỨNG MÀN HÌNH ĐEN / FADE-IN KHỞI ĐẦU**: Shot 1a tuyệt đối không fade-in từ màu đen hay để khoảng trống 0.5s ở đầu.

---

## 3. Outro CTA — BẤT BIẾN, KHÔNG ĐƯỢC SỬA BẤT KỲ TỪ NÀO

### Papercut Business
- **Short:** "This is just the surface of corporate secrets. Subscribe to Papercut Business for the full deep dive into everyday monopolies."
- **Long-form:** "This is just one example of the hidden economics shaping our lives. Subscribe to Papercut Business for more deep dives."
- **Hình ảnh Outro:** Collage + chữ "Everyday Monopolies" newsprint. Camera LUÔN TĨNH (static).

### Pixel Rewind
- **Short:** "That's just one level of tech history. Subscribe to Pixel Rewind for the full playthrough."
- **Long-form:** "Every piece of tech has a story. And most of them are wilder than you think. Subscribe to Pixel Rewind for more."
- **Hình ảnh Outro:** CRT monitor powering on + "Boot Sequence" green phosphor text. Camera LUÔN TĨNH (static).

### Pulp Hypotheses
- **Short:** "That's just one absurd timeline. Subscribe to Pulp Hypotheses for more mind-bending What-If files!"
- **Long-form (Alternate History topics):** "History is written by the victors, but rewritten in our comic vault. Subscribe to Pulp Hypotheses for more absurd timelines!"
- **Long-form (Sci-Fi / Science / Civilization topics):** "Reality is bound by laws, but rewritten in our comic vault. Subscribe to Pulp Hypotheses for more absurd timelines!"
- **Hình ảnh Outro:** Vintage 80s comic cover frame + yellow speech bubble "TO BE CONTINUED... SUBSCRIBE!". Camera LUÔN TĨNH (static).

### Blackprint
- **Short:** "Every machine has a secret. Subscribe to Blackprint to unlock the next 3D file."
- **Long-form:** "From ancient ruins to forbidden megaprojects, human ambition is written in the blueprints. Subscribe to Blackprint for the next deconstruction."
- **Hình ảnh Outro:** Bản vẽ Blueprint Noir tĩnh + Dòng chữ phát sáng "TO BE CONTINUED... SUBSCRIBE TO BLACKPRINT". Camera LUÔN TĨNH (static).

