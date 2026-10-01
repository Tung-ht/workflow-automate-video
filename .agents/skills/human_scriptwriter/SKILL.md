---
name: human-scriptwriter
description: >
  Skill chuyên viết và tinh chỉnh kịch bản video (beats.json narration) sao cho
  giống con người viết nhất, tẩy sạch dấu vết AI. Kích hoạt BẤT CỨ KHI NÀO:
  viết kịch bản, sửa narration, review chất lượng script, "polish" kịch bản,
  hoặc khi cần đảm bảo nội dung vượt qua "phép thử 10 phút" của YouTube.
  Triggers: "viết kịch bản", "sửa narration", "polish script", "review script",
  "chất người", "human voice", "tẩy AI", "anti-slop", "imperfection pass",
  "sensory", "ký ức giác quan", "scriptwriter".
---

# Human Scriptwriter — Viết Kịch Bản Không Dấu Vết AI

Skill này chứa **toàn bộ kiến thức và kỹ thuật** để viết narration cho video YouTube
sao cho khán giả KHÔNG nhận ra kịch bản do AI viết. Áp dụng cho MỌI kênh, MỌI niche.

> ⚠️ **THAM CHIẾU QUY TẮC BẮT BUỘC (HARD CONSTRAINTS):**
> Skill này hoạt động CÙNG VỚI channel skill (chiến lược kênh) và director skill (pipeline kỹ thuật):
> - [`.agents/rules/video-production.md`](file:///d:/video-atlas/.agents/rules/video-production.md) — 12 quy tắc production
> - [`.agents/rules/channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md) — Tham số kênh + CTA
> - Channel skill cung cấp: Persona, niche, subreddits mục tiêu
> - Skill này cung cấp: **Kỹ thuật viết giống người, anti-AI-slop, sensory injection**

---

## 1. Triết Lý Cốt Lõi

**"Phép thử 10 phút"** (từ kinh nghiệm thực chiến YouTube):
> Nếu một người khác cầm đúng công cụ đó, đúng chủ đề đó, họ có ra được video
> y chang bạn trong 10 phút không? Nếu CÓ → video vô giá trị dù không dùng AI.

AI viết kịch bản **đúng** (correct) nhưng không **trúng** (resonates). Con người
xem video không cần sự chính xác hoàn hảo — họ cần cảm thấy: *"Ủa, sao ông này
biết đúng cái tôi đang nghĩ?"*

Sự khác biệt nằm ở **3 tầng:**
1. **Ký ức giác quan** — AI không có thân xác, không biết mùi, không biết đau
2. **Thiên kiến cá nhân** — AI cố gắng cân bằng; con người chọn phe
3. **Sự bất toàn** — AI viết câu hoàn hảo; con người hụt hơi, vấp, bức xúc

---

## 2. Danh Sách Đen — AI Slop Phải Tẩy (Blacklist)

### 2.1. Từ/Cụm từ CẤM CỨNG (Hard Ban)

Những từ/cụm từ dưới đây là **dấu vân tay của AI**. Nếu xuất hiện trong narration,
khán giả trưởng thành Mỹ nhận ra ngay = mất trust = thoát video.

**Transition words công nghiệp:**
- ❌ "Furthermore" / "Additionally" / "Moreover" / "In addition"
- ❌ "It is worth noting that..." / "It is important to note..."
- ❌ "In conclusion" / "To summarize"
- ❌ "This highlights" / "This underscores" / "This demonstrates"
- ❌ "Interestingly" / "Remarkably" / "Significantly" / "Notably"

**Cụm chuyển cảnh rập khuôn (AI Structural Patterns):**
- ❌ "To understand X, we have to go back to Y" ← DẤU VẾT NGUY HIỂM NHẤT — nếu dùng cho 3 video liên tiếp, khán giả phát hiện ngay cùng 1 bot viết
- ❌ "But here's where it gets interesting..."
- ❌ "And that's not all..."
- ❌ "Let's dive in" / "Let's break it down"
- ❌ "How did they pull this off?"
- ❌ "The answer might surprise you"

**Từ cảm thán — DÙNG CÓ CHỪNG MỰC (tối đa 2 lần/video, không lặp cùng 1 câu):**
- ⚠️ "Crazy, right?" / "Wild, right?" — OK nhưng không dùng quá 1 lần/video
- ⚠️ "Nonsense." / "Wait a minute." / "Let that sink in." — OK nếu đặt đúng ngữ cảnh
- ❌ "Mind-blowing" / "Game-changer" / "Revolutionary" — CẤM (khoa trương rỗng)

**Từ khoa trương rỗng:**
- ❌ "Delve" / "Delving into"
- ❌ "Testament to" / "A testament"
- ❌ "Revolutionize" / "Groundbreaking"
- ❌ "Paradigm shift" / "Landscape"
- ❌ "Tapestry" / "Myriad" / "Plethora"
- ❌ "Nuanced" / "Multifaceted"

### 2.2. Cấu Trúc Câu Phải Tránh

**Passive voice quá nhiều:**
- ❌ "It was determined that..." → ✅ "They figured out..."
- ❌ "The decision was made to..." → ✅ "They decided to..."
- ❌ "It has been observed that..." → ✅ "People noticed..."

**Câu ghép quá dài (compound-complex):**
- ❌ Câu > 25 từ mà không ngắt → đọc TTS sẽ thành 1 cục dài monotone
- ✅ Tách thành: 3 câu ngắn dồn dập → 1 câu dài giải thích (công thức Staccato)

**Giọng bách khoa / giáo sư:**
- ❌ "As economists have observed..." → ✅ "Turns out..."
- ❌ "According to industry analysts..." → ✅ "The numbers tell a different story."
- ❌ "Studies have shown that..." → ✅ "Here's the data:"

---

## 3. Kỹ Thuật "Ký Ức Giác Quan" (Sensory Memory Injection)

Đây là thứ AI **không thể tự tạo** vì AI không có thân xác. Nhưng AI CÓ THỂ
**mô phỏng** bằng cách hỏi đúng câu hỏi và nghiên cứu Reddit/forums.

### 3.1. Quy Tắc "5 Giác Quan" — Hỏi Trước Khi Viết

Với MỖI chủ đề video, trước khi viết narration, Agent PHẢI tự hỏi:

| Giác quan | Câu hỏi | Ví dụ (TI-84) |
|-----------|---------|---------------|
| **Thị giác** | Khán giả NHÌN THẤY gì khi tiếp xúc với sản phẩm/chủ đề này? | Màn hình LCD mờ mịt, pixel thô, ký tự nhảy múa |
| **Thính giác** | Họ NGHE gì? | Tiếng bấm phím bíp bíp trong giờ kiểm tra yên ắng |
| **Xúc giác** | Họ CẢM THẤY gì khi chạm vào? | Vỏ nhựa ọp ẹp, phím cứng ngắc, nặng túi quần |
| **Khứu giác** | Có MÙI nào liên quan không? | Mùi nhựa mới khi mở hộp đầu năm học |
| **Cảm xúc** | Họ cảm thấy gì về mặt TÂM LÝ? | Ức chế vì bắt buộc mua, rồi lén chơi game Block Dude |

### 3.2. Nguồn Khai Thác Ký Ức Giác Quan

**Reddit là mỏ vàng giác quan:**
```
Tool: reddit_search
→ query: "TI-84 remember" OR "TI-84 nostalgia" OR "TI-84 high school"
→ sort: "top" | time: "all"

Tool: reddit_get_comments (cho post có nhiều anecdotes)
→ Tìm comment bắt đầu bằng: "I remember...", "My teacher used to...",
  "The worst part was...", "Am I the only one who..."
```

**Mẫu chuyển đổi Reddit → Narration:**

| Reddit gốc (KHÔNG copy) | Ký ức giác quan rút ra | Chèn vào narration |
|---|---|---|
| "My teacher walked around pressing 2nd+MEM+7+1+2 on everyone's calculator before SAT" | Xúc giác + thính giác: thầy giáo đi từng bàn, tiếng bíp xóa bộ nhớ | "Before every SAT, your teacher walked desk to desk, punching in the factory reset code. Bip. Bip. Bip. Three years of saved programs—gone." |
| "I spent more time playing Block Dude than doing actual math" | Cảm xúc: lén lút, hồi hộp sợ bị bắt | "Half the class was secretly playing Block Dude while pretending to graph parabolas." |

### 3.3. Quy Tắc Chèn Giác Quan

- **Chèn ít nhất 2 chi tiết giác quan** vào mỗi kịch bản (Short hoặc Long)
- **Vị trí tốt nhất:** Hook (Beat 1) hoặc Context (Beat 2-3) — giúp khán giả "nhập vai" ngay
- **KHÔNG chèn vào mỗi beat** — quá nhiều sẽ bị sến. 2-3 chỗ trong toàn bộ video là đủ
- **Ưu tiên chi tiết CỤ THỂ** hơn mô tả chung: ✅ "phím 2nd+MEM+7+1+2" > ❌ "nút bấm trên máy tính"

---

## 4. Kỹ Thuật Đa Dạng Hóa Cấu Trúc (Anti-Repetition)

### 4.1. Ngân Hàng Câu Chuyển Cảnh Lùi Thời Gian

Thay vì luôn dùng "To understand X, we have to go back to Y", AI PHẢI luân phiên
dùng các mẫu khác nhau cho MỖI video:

| # | Mẫu chuyển cảnh | Khi nào dùng |
|---|-----------------|--------------|
| 1 | "Long before [hiện tại], [chủ thể] wasn't even [ngành hiện tại]." | Khi chủ thể có nguồn gốc bất ngờ |
| 2 | "Rewind to [năm]. [Bối cảnh giác quan ngắn gọn]." | Khi cần thiết lập atmosphere |
| 3 | "[Năm]. [Tên người]. [Hành động ngắn]." — Mở thẳng, không transition | Khi muốn nhịp nhanh, cinematic |
| 4 | "The story starts with a guy who [hành động bất ngờ]." | Khi có nhân vật thú vị |
| 5 | "None of this would exist without [chi tiết bất ngờ]." | Khi muốn nhấn mạnh causality |
| 6 | "Picture this: [mô tả cảnh giác quan]. That was [năm]." | Khi muốn immersive |
| 7 | "[Sự thật shock]. And it all traces back to [năm/sự kiện]." | Khi muốn giữ tension |
| 8 | Không dùng câu chuyển cảnh — nhảy thẳng vào timeline mới | Khi nhịp phim đã nhanh |

**QUY TẮC:** Trong cùng 1 batch sản xuất (VD: 3 video cùng tuần), KHÔNG ĐƯỢC dùng
cùng 1 mẫu chuyển cảnh cho 2 video. Đánh dấu mẫu đã dùng.

### 4.2. Ngân Hàng Câu Cảm Thán Thay Thế

Thay vì "Crazy, right?" / "Wild." / "Let that sink in.", dùng:

| # | Câu thay thế | Tone |
|---|-------------|------|
| 1 | "I mean... come on." | Bức xúc nhẹ |
| 2 | "Read that again." | Nhấn mạnh lặng lẽ |
| 3 | "[Im lặng 0.5s]. Yeah." | Resigned acceptance |
| 4 | "And nobody blinked." | Châm biếm xã hội |
| 5 | "That's not a bug. That's the business model." | Cynical twist |
| 6 | "You paid for that, by the way." | Trực tiếp vào túi tiền |
| 7 | "So... who's really paying for this?" | Câu hỏi tu từ mở |
| 8 | "[Dừng]. Think about that for a second." | Pause + reflect |

**QUY TẮC:** Tối đa **2 câu cảm thán** trong 1 Short, **4 câu** trong 1 Long-form.
Không dùng cùng 1 câu 2 lần trong 1 video.

---

## 5. Kỹ Thuật "Chọn Phe" (Opinion Injection)

AI có xu hướng viết cân bằng "on one hand... on the other hand". Con người KHÔNG
nói như vậy — họ có thiên kiến, họ chọn phe, họ thay đổi ý giữa chừng.

### 5.1. Spectrum Thiên Kiến (chọn 1 cho mỗi video)

| Vị trí | Giọng | Ví dụ |
|--------|-------|-------|
| **Bất bình nhẹ** | "Tôi hiểu logic kinh doanh, nhưng vẫn thấy sai sai" | "I get why they do it. Doesn't mean I have to like it." |
| **Khâm phục miễn cưỡng** | "Ghét thì ghét nhưng phải phục" | "Honestly? I kinda respect the hustle. Even if it screws us." |
| **Tự mâu thuẫn** | "Tôi biết nó sai nhưng tôi vẫn mua" | "I hate this. But I'm still a member. So who's the real clown here?" |
| **Châm biếm lạnh** | "Nói sự thật bằng giọng bình thản" | "They found a way to charge $130 for a $15 chip. And we call that innovation." |

### 5.2. Quy Tắc Opinion

- Mỗi video PHẢI có **ít nhất 1 câu opinion** — không phải fact thuần
- Opinion nên xuất hiện ở **Twist beat** (Beat 5-6 trong Short) hoặc **kết luận**
- KHÔNG đưa opinion ở Beat 1 (Hook) — Hook cần là sự thật gây sốc, không phải ý kiến
- Cho phép **tự mâu thuẫn nhẹ** — "I hate this. But... I get it." → tạo depth

---

## 6. Kỹ Thuật Viết Hook (Câu Mở Đầu)

### 6.1. CẤM CỨNG — Hook Patterns Phải Tránh

- ❌ "Have you ever wondered..."
- ❌ "In today's video..."
- ❌ "Welcome back to..."
- ❌ "What if I told you..."
- ❌ "Did you know that..."
- ❌ "[Số liệu]. That's right."

### 6.2. Hook Patterns Hiệu Quả

| # | Pattern | Ví dụ |
|---|---------|-------|
| 1 | **Sự thật + Hành động bất ngờ** | "Costco loses money on every single hot dog. And they absolutely love it." |
| 2 | **Con số + Contradiction** | "$130 for a calculator with $15 worth of parts. Every year. For 30 years." |
| 3 | **Bạn là nạn nhân (trực tiếp)** | "If you went to high school in America, you got scammed." |
| 4 | **Cảnh giác quan** | "Pull into an Interstate rest stop at midnight. Fluorescent lights buzzing. A vending machine from 1998." |
| 5 | **Tuyên bố gây tranh cãi** | "The most overpriced product in America isn't healthcare. It's your kid's math class." |
| 6 | **Mini-story 1 câu** | "In 1995, Nintendo shipped a console that gave kids headaches. On purpose." |

**QUY TẮC:** Hook PHẢI gây được 1 trong 3 phản ứng: 😡 bức xúc, 😲 bất ngờ, 🤔 tò mò.
Nếu không gây được phản ứng nào → viết lại.

---

## 7. Imperfection Pass — Checklist Cuối Cùng

Sau khi kịch bản đã viết xong, Agent chạy **Imperfection Pass** — lượt rà cuối
để phá hoàn hảo và thêm chất người.

### Checklist (áp dụng cho MỖI kịch bản):

**Phá hoàn hảo:**
- [ ] ≥ 2 câu ngắn cụt có cảm xúc (nhưng KHÔNG nằm trong Blacklist §2)
- [ ] ≥ 1 chỗ tự mâu thuẫn nhẹ ("I hate this. But... I get it.")
- [ ] ≥ 1 câu hỏi tu từ tự nhiên (không giống quiz show)
- [ ] ≥ 1 từ lóng đời thường phù hợp persona (nhưng không gượng gạo)

**Anti-AI:**
- [ ] 0 từ/cụm từ trong Blacklist §2.1
- [ ] 0 cấu trúc câu trong danh sách tránh §2.2
- [ ] Câu chuyển cảnh lùi thời gian KHÁC video trước (kiểm tra §4.1)
- [ ] Không trùng câu cảm thán với video trước

**Giác quan:**
- [ ] ≥ 2 chi tiết giác quan cụ thể (từ Reddit research)
- [ ] Chi tiết giác quan nằm ở Hook hoặc Context (không rải khắp nơi)

**Nhịp điệu:**
- [ ] Không có câu > 25 từ nào không ngắt
- [ ] Có ít nhất 1 chuỗi staccato (3 câu ngắn liên tiếp)
- [ ] Mọi câu đọc thành tiếng được trong 1 hơi thở

**Kiểm tra chéo (Cross-Video Check):**
- [ ] Nếu đang sản xuất batch (nhiều video cùng lúc): không trùng mẫu chuyển cảnh
- [ ] Không trùng câu cảm thán giữa các video trong batch
- [ ] Hook pattern khác video trước trong cùng batch

---

## 8. Quy Trình Tích Hợp Với Channel Skill

Skill này KHÔNG hoạt động độc lập. Quy trình kết hợp:

```
Channel Skill (papercut/pixel_rewind/kênh_mới)
    ↓ cung cấp: Persona, niche, subreddits, CTA
    ↓
Human Scriptwriter (skill này)
    ↓ áp dụng: Anti-slop, sensory injection, imperfection pass
    ↓
Director Skill (vox_director/pixel_retro/style_mới)
    ↓ thực thi: beats.json → production pipeline
    ↓
final.mp4
```

**Khi viết beats.json:**
1. Channel Skill xác định: chủ đề, persona, arc, CTA
2. **Human Scriptwriter kiểm soát: narration text** (mọi narration trong beats.json)
3. Director Skill kiểm soát: scene, element_motion, camera_move, kỹ thuật

**Agent PHẢI đọc skill này TRƯỚC khi viết bất kỳ narration nào** — không phải sau.

---

## 9. Ví Dụ Thực Tế: Before vs After

### Ví dụ 1: TI-84 Monopoly (Short)

**BEFORE (AI 7.5/10):**
> "A $130 calculator with $15 parts. Yet every American student is forced to buy one.
> Here's why. The TI-84 runs on a Z80 chip from 1976. The screen is worse than a
> Gameboy. Crazy, right?"

**AFTER (Human 9/10):**
> "If you went to high school in America, you got scammed out of a hundred and thirty
> bucks for a calculator powered by a chip older than Star Wars. The screen? Worse
> than an original Game Boy. And your math teacher made it mandatory."

**Gì đã thay đổi:**
- ❌ "Crazy, right?" → Xóa (Blacklist)
- ❌ "Here's why" → Xóa (cliché)
- ✅ "you got scammed" → Opinion injection (bạn là nạn nhân)
- ✅ "older than Star Wars" → Pop culture anchor (1977 vs 1976 chip)
- ✅ "your math teacher made it mandatory" → Ký ức giác quan (ai cũng nhớ thầy/cô toán)

### Ví dụ 2: Rest Stop (Long-form Hook)

**BEFORE:**
> "You're driving down an American Interstate, low on gas and starving. You pull
> into a rest stop. And what do you get? A toilet, a picnic table, and a vending machine."

**AFTER:**
> "Pull into an Interstate rest stop at midnight. Fluorescent lights humming.
> A vending machine from 1998 spitting out lukewarm coffee. One toilet. One picnic
> table bolted to concrete. That's it. Two hundred feet down the road? A Buc-ee's
> the size of a Walmart, with seventy gas pumps and fresh-smoked brisket."

**Gì đã thay đổi:**
- ✅ "at midnight" → Time anchor tạo atmosphere
- ✅ "Fluorescent lights humming" → Thính giác
- ✅ "from 1998" → Cụ thể hóa
- ✅ "lukewarm coffee" → Xúc giác + vị giác
- ✅ "bolted to concrete" → Xúc giác, cảm giác buồn tẻ
- ✅ "seventy gas pumps and fresh-smoked brisket" → Tương phản giác quan cực mạnh
