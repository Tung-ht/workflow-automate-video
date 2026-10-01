---
name: reddit-research
description: >
  Skill nghiên cứu Reddit cho content pipeline. Quy trình 5 bước: Post Discovery →
  Comment Mining → Insight Classification → Transform & Inject → Fallback.
  Kích hoạt BẤT CỨ KHI NÀO cần tìm insight "người thật" từ Reddit cho kịch bản video,
  bài viết, hoặc bất kỳ nội dung nào cần tiếng nói cộng đồng.
  Triggers: "reddit research", "tìm reddit", "comment mining", "insight người thật",
  "reddit MCP", "nghiên cứu reddit", "reddit pipeline".
---

# Reddit Research Pipeline — Shared Skill

> **Mục đích:** Tìm và khai thác insight "người thật" từ Reddit để bổ sung vào kịch bản video.
> Đây là quy trình chung cho TẤT CẢ kênh YouTube trong hệ thống.
> Mỗi kênh sẽ có **channel-specific config** riêng (subreddits, insight types, injection points)
> được khai báo trong skill của kênh đó (section 9.2).

---

## 1. Yêu Cầu Kỹ Thuật & Hướng Dẫn Khởi Động (BẮT BUỘC KHI START)

- **Tool:** MCP Server `reddit` (reddit-unofficial-api via Chrome DevTools Protocol)
- **Không cần API key** — tất cả tools (search, comments, user analysis) đều hoạt động qua Chrome session

### ⚠️ QUY TRÌNH KHỞI ĐỘNG (START):
Trước khi thực hiện nghiên cứu, **phải bật CMD lên và chạy lệnh sau** để mở Chrome và Reddit trên máy:

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir=C:\Users\Admin\chrome-cdp https://www.reddit.com
```

> **Chi tiết tham số:**
> - `--remote-debugging-port=9222`: Mở cổng remote debugging cho MCP kết nối qua Chrome DevTools Protocol.
> - `--remote-allow-origins=*`: Cho phép kết nối WebSocket từ MCP server.
> - `--user-data-dir=C:\Users\Admin\chrome-cdp`: Lưu profile và phiên đăng nhập Reddit riêng biệt.
> - `https://www.reddit.com`: Tự động mở sẵn trang Reddit.

**Các bước kiểm tra khi start:**
1. Bật CMD và thực thi lệnh mở Chrome trên.
2. Đảm bảo cửa sổ Chrome đã mở, trang Reddit đã tải và đã đăng nhập.
3. Gọi tool `reddit_ensure_session` để xác nhận MCP đã kết nối thành công trước khi chuyển sang Bước 1.

---

## 2. Quy Trình 5 Bước

### Bước 1: Tìm Post (Post Discovery)

Dùng tool `reddit_search` với các tham số:

| Tham số | Mô tả | Ví dụ |
|---------|--------|-------|
| `query` | Từ khóa chủ đề | `"Tetris Pajitnov Soviet"` |
| `subreddit` | Tìm **TỪNG subreddit riêng biệt** — KHÔNG gộp | `"todayilearned"` |
| `sort` | `"relevance"` (đúng chủ đề) hoặc `"top"` (bài nổi nhất) | `"relevance"` |
| `limit` | Số posts trả về | `5` hoặc `10` |

> **LƯU Ý:** Tìm mỗi subreddit bằng 1 lệnh `reddit_search` riêng biệt.
> Chạy song song nhiều search cùng lúc để tiết kiệm thời gian.

**Từ kết quả JSON, lọc posts quan trọng:**
- `score > 1000` — posts đã được cộng đồng "verify" bằng upvotes
- Ghi lại `permalink` (URL) và `num_comments` để dùng ở Bước 2
- Ưu tiên posts có `num_comments > 100` — nhiều comments = nhiều perspectives

**Danh sách subreddits:** Xem channel-specific config trong skill của từng kênh (section 9.2).

---

### Bước 2: Đào Comment (Comment Mining) — MỎ VÀNG ⭐

> **NGUYÊN TẮC CỐT LÕI:**
> Insight "người thật" nằm trong **COMMENTS**, không phải trong title hay selftext.
> Title chỉ là fact kiểu Wikipedia.
> Comments mới là nơi người ta kể chuyện đời thực, tranh cãi, chia sẻ kỷ niệm cá nhân.
> **Đây là bước quan trọng nhất** — skip bước này = mất 80% giá trị của Reddit research.

Dùng tool `reddit_get_comments`:

| Tham số | Mô tả | Ví dụ |
|---------|--------|-------|
| `url` | URL **đầy đủ** của post | `"https://www.reddit.com/r/todayilearned/comments/ar21og/..."` |
| `sort` | Cách sắp xếp comments | `"top"` (khuyến nghị) |

> **CHÚ Ý:** Tham số bắt buộc là `url` (không phải `post_id`).
> URL lấy từ `permalink` ở Bước 1, thêm prefix `https://www.reddit.com`.

**Bộ lọc chất lượng (áp dụng trên kết quả JSON):**

| Điều kiện | Lý do |
|-----------|-------|
| `score > 100` | Insight đã được nhiều người đồng thuận |
| `depth <= 1` | Comments gốc (depth 0) và reply trực tiếp (depth 1) — tránh side-discussion |
| Ưu tiên `score > 500` | Insight được **hàng trăm người** validate |

**Lệnh PowerShell lọc nhanh từ file JSON output:**
```powershell
$json = Get-Content "<output_file_path>" -Raw | ConvertFrom-Json
$json | Where-Object { $_.score -gt 100 -and $_.depth -le 1 } |
  Select-Object score, author, @{N='body_short';E={$_.body.Substring(0,[Math]::Min($_.body.Length,300))}} |
  Sort-Object score -Descending | Format-Table -Wrap
```

> **MẸO:** Kết quả MCP thường lưu vào file lớn. Dùng lệnh trên để lọc nhanh
> thay vì đọc toàn bộ file JSON thủ công.

---

### Bước 3: Phân Loại Insight (Insight Classification)

Từ comments đã lọc, phân loại vào các nhóm giá trị. Dưới đây là **5 nhóm phổ biến nhất**
(mỗi kênh có thể tùy chỉnh tên nhóm — xem channel-specific config):

| Nhóm | Mô tả | Ví dụ | Vị trí chèn |
|------|--------|-------|-------------|
| **Personal Anecdote** | Người thật kể trải nghiệm cá nhân | *"I met him in person. He is a really nice guy."* (2,221↑) | Humanize nhân vật chính |
| **Obscure Claim** | Tuyên bố hiếm, khó verify, gây tò mò | *"A professor claimed the idea was stolen from his doctoral thesis"* (446↑) | Easter Egg Trick |
| **Counterintuitive Fact** | Góc nhìn/số liệu trái trực giác | *"Everyone knows Tetris but nobody can tell you who made it"* (1,102↑) | Hook / Opening |
| **Nostalgia / Emotion** | Kỷ niệm cá nhân hoặc phản ứng cảm xúc mạnh | *"Tetris B theme was the best and I listened to it for hours"* (254↑) | Nostalgia triggers |
| **Contrarian View** | Góc nhìn phản biện, tranh cãi | *"It wasn't really 'stolen' — IP didn't exist in the Soviet system"* | Nuance / Depth |

**MỤC TIÊU tối thiểu:** Mỗi kịch bản phải chèn ít nhất **3 Reddit insights** từ ít nhất **2 nhóm khác nhau**.

---

### Bước 4: Biến Đổi và Chèn (Transform & Inject)

#### Quy tắc biến đổi:
1. **Hấp thụ tinh thần** của comment Reddit — KHÔNG copy nguyên văn
2. **Viết lại hoàn toàn** bằng giọng Persona của kênh (xem skill kênh, section 9.1)
3. Giữ lại **cốt lõi insight** nhưng thay đổi cấu trúc câu, từ ngữ, nhịp điệu
4. **KHÔNG bao giờ** trích dẫn username Reddit hoặc nói "theo một người trên Reddit"

#### Ví dụ biến đổi:

| Reddit gốc (KHÔNG dùng) | Viết lại bằng Persona (DÙNG) |
|---|---|
| *"I met him in person. He is a really nice guy."* (comment Reddit) | *"People who've met Pajitnov say the same thing: the guy's just... nice. No ego. No bitterness."* (narration) |
| *"Everyone knows Tetris but nobody can tell you who made it"* (comment Reddit) | *"Everyone knows Tetris. Ask anyone on the street to name the guy who made it. Silence."* (narration) |
| *"The hot dog is a loss leader"* (comment Reddit) | *"You walk in for a buck-fifty hot dog. You leave with a TV you didn't know you needed."* (narration) |

#### Injection Points:
Mỗi kênh có bảng injection points riêng cho Short và Long-form — xem channel-specific config (section 9.2 trong skill kênh).

**Framework chung:**

| Format | Vị trí | Loại insight |
|--------|--------|-------------|
| **Short** | Shot 1 (Hook) | Counterintuitive Fact / Shocking stat |
| | Shot 2-3 (Origin/Context) | Personal Anecdote / Insider Story |
| | Shot 6 (Twist) | Obscure Claim / Easter Egg |
| **Long-form** | Beat 1 (Hook) | Counterintuitive Fact |
| | Beat 5-6 (Core Story) | Personal Anecdote / Nostalgia |
| | Beat 17-19 (Emotional Valley) | Contrarian View / Empathy |
| | Beat 20-21 (Payoff) | Obscure Claim + Self-aware humor |

---

### Bước 5: Fallback khi Reddit MCP không khả dụng

Nếu `reddit_ensure_session` lỗi (Chrome chưa mở, MCP server down):

**Bước 5a — Thử khắc phục:**
Bật CMD lên và chạy lại lệnh sau, đợi 8-10 giây rồi gọi lại `reddit_ensure_session`:
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir=C:\Users\Admin\chrome-cdp https://www.reddit.com
```

**Bước 5b — Fallback sang Web Search:**
Nếu vẫn lỗi, dùng `search_web` với query chứa keyword `"reddit"`:
- Ví dụ: `"Tetris Pajitnov Soviet reddit"` → Google trả về summary các thread Reddit phổ biến
- Web search cho **facts** ổn, nhưng **KHÔNG thể thay thế** comment mining (Bước 2)

**Bước 5c — Ghi chú:**
Nếu dùng fallback, ghi rõ trong artifact review:
> *"Reddit MCP unavailable — used web search fallback. Comment mining pending."*

**Bước 5d — Bổ sung sau:**
Khi Reddit MCP khả dụng lại, quay lại chạy Bước 2 (Comment Mining) vì insight "người thật"
từ top comments là thứ tạo ra sự khác biệt giữa video "đúng" và video **"trúng"**.

---

## 3. Checklist Nghiên Cứu Reddit

- [ ] Đã bật CMD chạy lệnh mở Chrome (`--remote-debugging-port=9222`, user data dir `C:\Users\Admin\chrome-cdp`) và load Reddit
- [ ] Đã gọi `reddit_ensure_session` thành công
- [ ] Đã search ít nhất **3 subreddits** từ Tier 1 của kênh
- [ ] Đã đào comments từ ít nhất **2 posts** có `score > 1000`
- [ ] Đã lọc và chọn ít nhất **3 insights** từ ít nhất **2 nhóm** khác nhau
- [ ] Mỗi insight đã được **viết lại** bằng Persona — không còn nguyên văn Reddit
- [ ] Đã chèn insights vào đúng **injection points** theo format (Short/Long-form)
- [ ] Artifact review có bảng tóm tắt **Reddit insights đã dùng** (source, score, nhóm, beat)
