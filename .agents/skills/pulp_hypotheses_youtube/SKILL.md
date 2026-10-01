---
name: pulp-hypotheses-youtube
description: >
  Chiến lược nội dung, kịch bản và phát triển kênh YouTube "Pulp Hypotheses" — chuyên chủ đề
  giả định phi lý nhưng thú vị (Absurd & Mind-Bending What-If Scenarios) bằng phong cách Truyện Tranh Cổ Điển (Retro Pulp Comic Style).
  Triggers: "pulp hypotheses", "absurd timelines", "what if comic", "tạo video pulp hypotheses", "giả định phi lý", "nếu người tiền sử có súng", "retro comic video".
---

# Pulp Hypotheses — YouTube Channel Playbook

## 📌 Phân Định Scope & Kiến Trúc Skill
> ⚠️ THAM CHIẾU QUY TẮC BẮT BUỘC:
> - `.agents/rules/video-production.md` — 12 quy tắc production bắt buộc
> - `.agents/rules/channel-identities.md` — Tham số nhận diện kênh + Outro CTA bất biến
> - Kỹ thuật đạo diễn hình ảnh: xem skill `pulp_comic_director` (`pulp-comic-director`)
> - Viết kịch bản tự nhiên giống người: xem skill `human-scriptwriter` (`human_scriptwriter`)
> - Nghiên cứu Reddit: xem skill `reddit-research` (`reddit_research`)

---

## 1. Thông tin Kênh (Channel Identity)

| Thuộc tính | Giá trị |
|---|---|
| **Tên kênh** | `Pulp Hypotheses` |
| **Micro-Niche** | Absurd & Mind-Bending "What If" History, Science & Civilization Scenarios |
| **Series chính** | *"Absurd Timelines"* (Dòng thời gian phi lý) |
| **Khán giả mục tiêu** | Nam/Nữ Mỹ (18–35 tuổi), mê Sci-Fi, Alternate History, Pop Culture, Comic Books, Thought Experiments |
| **Phong cách hình ảnh** | Retro Pulp Comic Style (80s-90s Multi-Panel Comic Book Page Layout, Traditional 2D Superhero Cel Animation, heavy ink outlines, CMYK halftone dots, pop-art colors) |
| **Ngôn ngữ** | `English (United States)` |
| **Giọng đọc AI Voice** | xAI TTS — Giọng nam kịch tính, năng lượng, vintage comic narrator (`leo`) |
| **Caption Style** | `yellow_comic` (Chữ vàng viền đen nét đậm) |

---

## 2. Chiến lược Phễu: Shorts → Long-form

### 2.1. Thứ Tự SẢN XUẤT
1. **Sản xuất Long-form trước (3–5 phút):** Phân tích đầy đủ 3-4 giai đoạn tác động dây chuyền của kịch bản giả định (Domino effect: Ngắn hạn → Trung hạn → Dài hạn).
2. **Sản xuất Short sau (tối đa 45 giây):** Rút trích 1 nút thắt bất ngờ nhất / phi lý nhất từ Long-form để tạo Short.

### 2.2. Mối Quan Hệ Nội Dung (Bổ sung, KHÔNG lặp)
- **Short:** Tập trung vào câu hỏi gây ngỡ ngàng (The Hook) + 2 domino effect nhanh + cliffhanger bất ngờ.
- **Long-form:** Mở rộng chiều sâu lịch sử, khoa học thực tế đằng sau logic giả định, và kết luận "What if" có chiều sâu.

### 2.3. Thứ Tự ĐĂNG VIDEO
1. Đăng **Long-form trước** (8:00 AM EST).
2. Đăng **Short sau 4–24h** và cài đặt **Related Video** trỏ trực tiếp về Long-form.

---

## 3. Dấu Ấn Thương Hiệu (Brand Identity)

### 3.1. Watermark Logo
- **Prompt sinh logo watermark:**
  `"A retro 80s pulp comic book logo badge of the text 'Pulp Hypotheses', bold heavy black ink superhero typography with vibrant yellow fill, red drop shadow, subtle halftone dot texture, isolated on pure white background, high-resolution graphic asset."`
- **Asset path:** `assets/pulp_hypotheses_watermark.png`

### 3.2. Signature Outro (Tham chiếu `channel-identities.md`)
- **Short CTA:** *"That's just one absurd timeline. Subscribe to Pulp Hypotheses for more mind-bending What-If files!"*
- **Long-form CTA (Alternate History):** *"History is written by the victors, but rewritten in our comic vault. Subscribe to Pulp Hypotheses for more absurd timelines!"*
- **Long-form CTA (Sci-Fi / Science / Civilization):** *"Reality is bound by laws, but rewritten in our comic vault. Subscribe to Pulp Hypotheses for more absurd timelines!"*
- **Hình ảnh Outro:** Vintage 80s comic cover frame + yellow speech bubble *"TO BE CONTINUED... SUBSCRIBE!"*. Camera LUÔN TĨNH.

---

## 4. Nguyên tắc Viết Kịch Bản — Quy tắc 70/30 & Absurd Logic

### 4.1. YPP Restrictions
- Không cổ xúy bạo lực vô căn cứ, không dùng từ ngữ vi phạm chính sách monetization của YouTube.
- Mọi tình huống vũ khí hay chiến tranh giả định đều phải đóng khung trong "Lịch sử giả định / Thí nghiệm tư duy" (Thought Experiment).

### 4.2. 5 Quy Tắc Scripting Cho Pulp Hypotheses
1. **Rule ① — The Counter-Intuitive Hook:** Mở đầu bằng một tiền đề trái khoáy, gây giật mình ngay giây thứ nhất. *(VD: "If cavemen had AK-47s, mammoths wouldn't be extinct... they'd be domesticated combat mounts.")*
2. **Rule ② — Domino Chain Logic:** Diễn biến theo quy luật phản ứng dây chuyền 3 bước:
   - *Tác động 1 (Instant Shock):* Điều gì xảy ra ngay lập tức?
   - *Tác động 2 (Societal Shift):* Xã hội / văn minh thay đổi ra sao?
   - *Tác động 3 (Absurd Conclusion):* Kết quả kỳ lạ mà không ai ngờ tới.
3. **Rule ③ — Grounded Science in Absurdity:** Dù tiền đề phi lý, lập luận giải thích phải DỰA TRÊN khoa học, tâm lý học và lịch sử thật *(70% Absurd premise + 30% Real historical science)*.
4. **Rule ④ — Cinematic Comic Pacing:** Nhịp thoại dồn dập như từng panel truyện tranh lật qua. Dùng các từ nối kịch tính (*"But then...", "Plot twist...", "Here is where physics gets mad..."*).
5. **Rule ⑤ — Hard Cut Cliffhanger:** Ngừng lại ở đỉnh điểm tò mò trước khi đọc Outro CTA cố định.

---

## 5. Chiến lược Thumbnail & Tiêu Đề

### 5.1. Long-form Thumbnail (16:9 Comic Cover Poster)
- Sinh poster qua `provider.py` (Flux/Ideogram) phong cách **Bìa truyện tranh Mỹ thập niên 80**.
- Đèn chiếu kịch tính, nét mực đen đậm, vệt chấm bi halftone.
- Đè tiêu đề giật gân 3-5 từ chữ vàng viền đen đậm (*"CAVEMEN WITH GUNS!"*, *"ROME HAD ELECTRICITY?!"*).

### 5.2. Shorts — First Frame Optimization (Frame 0)
- Áp dụng công thức 3 lớp tại Shot 1a:
  - **Lớp 1 (Visual Anchor):** Prompt `kf_1a.jpg` chèn chỉ thị comic headline: `"...Include a dramatic retro comic book headline banner with big bold English text '[TITLE_EN]' in heavy black ink superhero typography, yellow fill with thick black outlines, crisp and readable."`
  - **Lớp 2 (Bold Headline Text Card):** Beat 1 set `"title_en"` và Shot 1a set `"title": true`.
  - **Lớp 3 (Kinetic Subtitles at 0.00s):** Phụ đề viền đen chữ vàng hiển thị ngay milisecond 0.00.

### 5.3. Chiến Lược Tiêu Đề YouTube (CẤM 'What If' — 100% Bắt Buộc Là Câu Hỏi Trực Diện)
- ⛔ **CẤM TUYỆT ĐỐI dùng cụm từ "What If":** Không dùng "What If" trong tiêu đề vì gây nhàm chán, rập khuôn và giảm CTR.
- ✅ **BẮT BUỘC đặt tiêu đề dưới dạng CÂU HỎI TRỰC DIỆN (Direct Question Hook):**
  * Sử dụng các trợ từ nghi vấn kích thích trí tò mò cực độ: `Did ...?`, `Could ...?`, `Were ...?`, `Why Did ...?`.
  * **Ví dụ chuyển đổi chuẩn:**
    - ❌ *What If Dinosaurs Had An Industrial Revolution?* $\rightarrow$ ✅ **`Did Dinosaurs Have An Industrial Revolution?`**
    - ❌ *What If China Colonized America in 1421?* $\rightarrow$ ✅ **`Did China Colonize America In 1421?`**
    - ❌ *What If America and Vietnam Were Best Friends in 1945?* $\rightarrow$ ✅ **`Were America and Vietnam Best Friends in 1945?`**
    - ❌ *What If Humans Had Floating Health Bars?* $\rightarrow$ ✅ **`Could Humans Survive With Floating Health Bars?`**

---

## 6. Hướng dẫn Sản Xuất

### Cấu trúc Kịch bản Short Mẫu (45s):
- `0 - 7s` **The Absurd Hook:** Tiền đề giả định gây sốc + Headline comic to.
- `7 - 20s` **Domino 1 (The Immediate Chaos):** Tác động tức thì của giả định.
- `20 - 33s` **Domino 2 (The World Altered):** Sự biến đổi của nền văn minh.
- `33 - 40s` **The Mind-Bending Twist:** Sự thật lịch sử / khoa học bất ngờ đằng sau.
- `40 - 45s` **Outro CTA Cố Định:** Đọc đúng câu Short Outro Signature + Hình Outro comic tĩnh.

---

## 7. Cài đặt Kênh YouTube (Checklist)

- **Channel Name:** `Pulp Hypotheses`
- **Country:** `United States`
- **Language:** `English (United States)`
- **Category:** `Entertainment` hoặc `Education`
- **Description:** *"Mind-bending what-if scenarios and absurd history unravelled in classic retro pulp comic style. New hypothetical timeline every week."*
- **Keywords:** `what if, absurd history, alternate history, retro comic, pulp comic, thought experiment, animated explainer, mind bending`

---

## 8. Tham khảo Ý tưởng Chủ đề (Idea Bank)

1. *"What if cavemen had assault rifles?"* (Người tiền sử có súng)
2. *"What if the asteroid missed the dinosaurs by 5 minutes?"* (Thiên thạch trượt Trái Đất)
3. *"What if the Roman Empire discovered electricity in 100 AD?"* (Đế chế La Mã có điện)
4. *"What if humans hibernated through winter like bears?"* (Con người ngủ đông)
5. *"What if gravity was 20% weaker on Mondays?"* (Trọng lực giảm vào thứ Hai)
6. *"What if the ocean was made of liquid caffeine?"* (Đại dương toàn nước tăng lực/caffeine)

---

## 9. Tự Động Hóa "Chất Người" — Human Voice Automation

### 9.1. Persona Narration
- **Tên Persona:** *Captain Hypo* — Một nhà du hành thời gian kiêm tác giả truyện tranh pulp thập niên 80. Táo bạo, châm biếm nhẹ nhàng, yêu thích những giả định điên rồ nhưng giải thích bằng thái độ cực kỳ nghiêm túc.
- **Giọng viết:** Dùng các cụm từ cửa miệng: *"Picture this...", "Now, before you call me crazy...", "Here's where human nature ruins everything..."*

### 9.2. Imperfection Injection
- Chèn cảm xúc ngạc nhiên, tiếng tặc lưỡi nhẹ hoặc ngắt nhịp tự nhiên trong narration để xóa dấu vết robot TTS.
- Tránh liệt kê danh sách khô khan (`1, 2, 3`), chuyển thành mạch kể chuyện nối tiếp (*"And just when you thought it settled..."*).

---

## 10. Topic Discovery Engine

### 10.1. Subreddits Mục Tiêu
- `r/WhatIf`
- `r/AlternateHistory`
- `r/AskReddit` (lọc các post "What if...")
- `r/Showerthoughts`
- `r/absurdist`
- `r/comicbooks`

### 10.2. Bộ Lọc 5 Tiêu Chí Chọn Topic
1. **High Visual Potential:** Tình huống dễ tưởng tượng ra khung hình truyện tranh kịch tính (action pose/sci-fi visual).
2. **Instant Curiosity:** Tiêu đề đọc lên người xem phải tò mò ngay lập tức.
3. **Domino Potential:** Có đủ chất liệu để suy luận phản ứng dây chuyền 3-4 bước.
4. **Debate Trigger:** Kích thích khán giả comment tranh luận dưới video.
5. **Brand Safe:** Phù hợp chính sách YouTube Monetization (YPP).
