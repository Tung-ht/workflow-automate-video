---
name: pixel-retro-director
description: >
  Turn ONE topic into a finished retro pixel-art / CRT-style explainer video, end to end.
  Fork of vox-director: same pipeline scripts, different visual DNA — pixel art keyframes,
  CRT scanlines, phosphor glow, VHS effects instead of paper collage.
  Uses Google Flow (via FlowKit) for visuals and the Atlas Cloud API for audio + local ffmpeg.
  Triggers: "pixel video", "retro video", "CRT style", "pixel art explainer",
  "8-bit video", "retro gaming video", "arcade style video".
---

# Pixel Retro Director

Turn a one-line topic into a finished **retro pixel-art / CRT-style explainer video**: a nostalgic, arcade-inspired explainer where each beat is a pixel-art scene that comes alive, with voice-over, music, captions, and CRT post-processing. Runs on **Google Flow (via FlowKit) for images/videos**, **one Atlas Cloud API key for audio**, + local **ffmpeg**.

## The core idea (read this first)

The pixel-retro look and the retro motion are **two different steps**:

1. **The look is born in the IMAGE step.** Each beat is a finished pixel-art scene made by text-to-image. All the retro DNA (pixel grid, limited palette, CRT glow, scanlines) lives in that image.
2. **The motion is added after.** AI video model animates the scene with retro-appropriate motion.
3. **CRT overlay is added in post.** Scanlines, phosphor glow, vignette, and optional VHS tracking are applied by ffmpeg during assembly — this is what sells the "old screen" illusion.

## Prerequisites (check, don't skip)

> ⚠️ **THAM CHIẾU QUY TẮC BẮT BUỘC (HARD CONSTRAINTS):**
> Mọi bước trong Skill này PHẢI tuân thủ nghiêm ngặt:
> - [`.agents/rules/video-production.md`](file:///d:/video-atlas/.agents/rules/video-production.md) — 12 quy tắc production (Provider flowkit, Gates, Duration, Anti-hallucination, Google Flow Safety)
> - [`.agents/rules/channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md) — Tham số kênh (voice, caption, watermark, CRT) + Outro CTA bất biến
> - Pipeline cơ sở: xem skill `vox-director` (`vox_papercut_director`)

- `command -v ffmpeg ffprobe` — required for assembly (`brew install ffmpeg` on macOS).
- `python3 -c "import PIL"` — Pillow, for captions/watermark overlays.
- `echo "${ATLASCLOUD_API_KEY:+set}"` — cần cho audio (TTS + Music). Nếu thiếu → hỏi user set
  (get one at https://www.atlascloud.ai/console/api-keys).

## Script Location

All execution scripts are located in the shared workspace directory: `scripts/`
Run all commands from the workspace root. The visual difference comes from the PROMPTS this skill teaches you to write.
For CRT post-processing, this skill adds ONE new ffmpeg command chain in the assemble step.

## Standard workflow (topic → film)

### 1. Topic → beat map
Same process as vox-director. Read `references/beat-layer.md` from vox-director for narrative arcs.
Pick arc: `timeline` for tech history, `man_in_hole` for rise-fall-rise stories, `how_it_works` for technical explanations.
Beat count: same as vox-director (45s = 6-7 shots at 6-7s each).
First approval gate: show user the beat map.

### 2. Pick Visual Style (Pixel Themes)
Instead of vox-director's collage themes, use PIXEL THEME PRESETS:

**THEME PRESETS:**

#### `crt-arcade` (DEFAULT for most topics)
The definitive retro arcade look.
- **Palette:** Dark background, neon cyan/magenta/amber accents, phosphor green highlights
- **Texture:** CRT phosphor dot grid, scanline interference, warm amber color cast
- **Typography:** Blocky pixel font, ALL CAPS, score-counter style numbers
- **Mood:** Dark arcade room, cabinet glow, quarter-slot nostalgia
- **Best for:** Arcade history, console wars, classic game stories

#### `gameboy-green`
The iconic 4-shade green palette.
- **Palette:** 4 shades of olive/lime green ONLY (#0f380f, #306230, #8bac0f, #9bbc0f)
- **Texture:** Dot-matrix grid, no anti-aliasing, sharp pixel edges
- **Typography:** Minimal, Game Boy system font style
- **Mood:** Intimate, handheld, personal, nostalgic warmth
- **Best for:** Handheld gaming, Game Boy history, portable tech, indie games

#### `vhs-rewind`
Warm analog decay — the home video era.
- **Palette:** Warm desaturated tones, VHS color bleed (slight RGB misalignment)
- **Texture:** VHS tracking lines, tape degradation noise, soft horizontal smear
- **Typography:** VHS timestamp font (white, bottom-right), channel number overlay
- **Mood:** Living room in 1993, recording Saturday morning cartoons
- **Best for:** 90s tech, home computing, early internet, VHS-era pop culture

#### `terminal-green`
Command-line hacker aesthetic.
- **Palette:** Pure black background, bright green (#00ff00) text/elements ONLY
- **Texture:** CRT curvature, phosphor bloom on bright elements, screen flicker
- **Typography:** Monospace terminal font, blinking cursor
- **Mood:** Late-night coding, early Unix, hacker culture, the birth of the internet
- **Best for:** Programming history, hacker stories, OS wars, early internet

#### `snes-16bit`
The golden age of 16-bit — rich, colorful, detailed.
- **Palette:** Full 16-bit color range, vibrant but not modern-bright, slightly warm
- **Texture:** 16-bit pixel art with visible but refined pixel grid, dithering gradients
- **Typography:** RPG dialogue box style, bordered text windows
- **Mood:** Epic adventure, golden era of gaming, peak creativity
- **Best for:** SNES/Genesis era, RPG history, 16-bit golden age, game design stories

#### `commodore-beige`
The home computer revolution — beige plastic and floppy disks.
- **Palette:** Beige (#c8b89c), brown, muted blue, Commodore PETSCII colors
- **Texture:** Floppy disk label aesthetic, dot-matrix printer output, thermal paper
- **Typography:** PETSCII / C64 font, blocky, uppercase-dominant
- **Mood:** Garage computing, bedroom coders, the personal computer revolution
- **Best for:** Early PC history, Commodore/Apple II/IBM era, hobbyist computing

### 3. Keyframes (The Pixel Look)
`python3 scripts/keyframes.py out/<project>`

Same script as vox-director. The PIXEL LOOK comes from how you write the image prompts.

**IMAGE PROMPT DNA — THE 5-PART PIXEL PROMPT:**

```
[PIXEL STYLE + RESOLUTION] + [SUBJECT performing ACTION] + [ENVIRONMENT with PERIOD DETAILS] + [LIGHTING + COLOR PALETTE from theme] + [COMPOSITION + FRAME ELEMENTS]
```

**Part 1 — PIXEL STYLE (always first):**
Always start with one of these depending on theme:
- `"Detailed 16-bit pixel art illustration,"` (crt-arcade, snes-16bit)
- `"4-color Game Boy pixel art in olive green palette,"` (gameboy-green)
- `"Warm VHS-captured scene with analog noise,"` (vhs-rewind)
- `"Green phosphor terminal screen display,"` (terminal-green)
- `"8-bit Commodore 64 pixel art,"` (commodore-beige)

**Part 2 — SUBJECT + ACTION (same rules as vox-director):**
- Describe ACTION, not appearance
- Never describe character details if using refs
- Use specific verbs: "soldering", "typing furiously", "presenting to boardroom"

**Part 3 — ENVIRONMENT with PERIOD DETAILS:**
This is where pixel-retro shines. Add era-specific props:
- 1970s: wood-paneled basement, oscilloscope, wire-wrap boards, reel-to-reel tape
- 1980s: arcade cabinets, neon signs, cassette tapes, CRT monitors with green text
- 1990s: beige PC towers, floppy disks, dial-up modems, Netscape browser, pizza boxes
- 2000s: iPod silhouettes, flip phones, chunky laptops, AIM chat windows

**Part 4 — LIGHTING + PALETTE:**
- crt-arcade: "dark room lit by arcade cabinet glow, neon cyan and magenta reflections"
- gameboy-green: "rendered in exactly 4 shades of olive green, dot-matrix texture"
- vhs-rewind: "warm desaturated VHS color palette, slight color bleed on edges"
- terminal-green: "bright green on pure black, phosphor glow bloom around text"
- snes-16bit: "vibrant 16-bit color palette, warm golden lighting, dithered gradients"

**Part 5 — COMPOSITION + FRAME ELEMENTS:**
- Add CRT/screen frame elements: "visible CRT screen curvature", "scanline overlay", "pixel grid visible at edges"
- Score/HUD elements: "score counter in top-right", "health bar", "lives remaining icons"
- Period UI: "DOS command prompt border", "Windows 3.1 window frame", "Macintosh dialog box"

**FULL EXAMPLE PROMPT (crt-arcade theme):**
```
Detailed 16-bit pixel art illustration, a determined young engineer soldering circuit boards alone in a cluttered garage workshop, oscilloscope glowing on workbench beside scattered blueprints and empty coffee cups, dark room lit by a single desk lamp and the amber glow of a CRT monitor displaying scrolling green code, neon cyan accent lighting from a vintage neon 'OPEN' sign in the window, warm amber and cool cyan color palette, wide shot with the engineer small against towering shelves of electronic components, CRT scanline texture overlay, retro arcade aesthetic
```

**BAD vs GOOD prompts:**
| BAD | GOOD | WHY |
|-----|------|-----|
| "pixel art of a computer" | "Detailed 16-bit pixel art of a beige IBM PC on a cluttered desk, green phosphor monitor displaying BASIC code, stack of 5.25-inch floppy disks, 1983 suburban bedroom" | Vague → specific era + details |
| "retro game scene" | "SNES-style 16-bit pixel art RPG scene, hero character standing at crossroads sign in autumn forest, golden dithered light through pixel trees, dialogue box at bottom reading 'WHICH WAY?'" | Generic → specific game-era aesthetic |
| "a guy with a computer" | "Terminal-green style, silhouette of a hacker hunched over keyboard, green code cascading down CRT screen, dark room, phosphor bloom around bright text, coffee cup steaming" | No style → full theme + mood |

### 4. Motion (Pixel-Appropriate)
`python3 scripts/clips.py out/<project>`

Same script as vox-director. Uses `kwaivgi/kling-video-o3-pro/image-to-video` (cheaper, handles pixel art well).

**PIXEL MOTION VOCABULARY:**

**camera_move** — same pool as vox-director, but frequency guidance:
- `static` — MORE frequent than collage (pixel art looks best with minimal camera). Use on 30-40% of shots.
- `push_in` — slow zoom into detail. Great for "revealing" a hidden element.
- `parallax` — layers shifting. EXCELLENT for pixel art (simulates parallax scrolling from games).
- `pan` — horizontal sweep. Good for showing wide pixel landscapes.
- `pull_out` — reveal the full scene from a detail.
- AVOID: `orbit`, `dolly_zoom`, `roll` — these warp pixel grids and look terrible.

**element_motion** — PIXEL-SPECIFIC:
DO NOT write generic motion. Write motion that reinforces the retro aesthetic:
- Scanline scroll (scanlines moving vertically across screen)
- Pixel shimmer (individual pixels flickering like a CRT)
- Score counter ticking up rapidly
- Text cursor blinking
- Loading bar filling
- Progress dots appearing one by one
- Floppy disk inserting into drive, LED blinking
- CRT static burst (brief snow then clear)
- Health bar depleting or filling
- Sprite animation (character idle animation — subtle bobbing)
- Screen transition (horizontal wipe, like a game scene change)
- "Power on" sequence (black → static → image stabilizes)

**motion_style:** Default `calm` for pixel art. Pixel art + `max` motion = the pixel grid warps into mush. Use `punchy` sparingly on 1-2 dramatic beats.

**constraints:** Default `strict`. Pixel art must stay FLAT and 2D. `loose` will make AI try to "3D-ify" the pixels — almost always terrible.

### 5. Voice + Music
`python3 scripts/audio.py out/<project>`

**Voice:** xAI TTS, voice_id `kai` (young, energetic male). Consistent across all Pixel Rewind videos.

**Music Prompt Templates (for minimax/music-2.6):**

Pick based on theme and mood:
- **Adventure/Discovery:** "chiptune 8-bit retro gaming soundtrack, adventurous and uplifting, synthesizer arpeggios, melodic lead over driving bass, reminiscent of NES era exploration music, 120 BPM"
- **Mystery/Investigation:** "lo-fi chiptune ambient, mysterious synthesizer pads, sparse 8-bit percussion, dark retro computing atmosphere, slow tempo, tense undercurrent"
- **Epic/Dramatic:** "16-bit SNES RPG boss battle music, dramatic orchestral chiptune, building intensity, heroic brass synth melody, fast-paced drums, 140 BPM"
- **Nostalgia/Warmth:** "warm analog synthesizer melody, gentle chiptune arpeggios, soft 8-bit percussion, nostalgic and bittersweet, VHS-era background music, 90 BPM"
- **Tech/Hacker:** "dark synthwave, pulsing bass, glitchy digital percussion, cyberpunk retro computing atmosphere, Blade Runner meets War Games"

### 6. Draft Mode
`python3 scripts/draft.py out/<project>`
Identical to vox-director. Review pacing before spending money on video motion.

### 7. Assemble + CRT Post-Processing (Integrated)
`python3 scripts/assemble.py out/<project>`

CRT post-processing is **integrated directly into `assemble.py`** via one `beats.json` field.
No separate ffmpeg command or `final_crt.mp4` file needed — `final.mp4` is the single deliverable.

**beats.json CRT field:**
```json
"crt_post": true       // enables CRT scanline overlay + phosphor EQ
```

**How it works internally:**
1. `assemble.py` checks `crt_post` in beats.json.
2. If `true`, loads (or auto-generates) a transparent PNG scanline overlay (`assets/crt_scanline_{W}x{H}.png`).
3. The scanline PNG is composited over the video as an additional ffmpeg overlay input.
4. Phosphor EQ is applied: `eq=saturation=1.1:contrast=1.08:brightness=-0.01`.

> **Note:** `vignette` was tested and removed — ffmpeg's vignette filter is too aggressive
> for dark retro content (it blacks out edges even at `angle=PI/3`). Scanlines + EQ alone
> are sufficient to sell the CRT look without destroying the image.

**Usage by channel:**
| Channel | `crt_post` | Notes |
|---|---|---|
| Pixel Rewind (Long-form + Short) | `true` | Retro CRT aesthetic |
| Papercut Business | omit or `false` | Paper collage style, no CRT |

**Scanline overlay specs:**
- Spacing: 1 dark line every 3 pixels
- Opacity: 90/255 (~35%) — visible texture without destroying content
- Auto-generated per resolution if not found in `assets/`

### 8. Thumbnail (YouTube Long-form ONLY — SKIP cho Shorts)
`python3 scripts/thumbnail.py out/<project>`

- **Long-form 16:9:** Tạo poster pixel art 16:9 qua `provider.py`, đè chữ tiêu đề + film grain / CRT filter $\rightarrow$ `thumbnail.png`.
- **Shorts 9:16:** **BỎ QUA BƯỚC NÀY**. Script `thumbnail.py` tự động SKIP khi `aspect: "9:16"`. Tuân thủ **Mục 2 trong [`channel-identities.md`](file:///d:/video-atlas/.agents/rules/channel-identities.md)** (Công thức 3 Lớp cho Frame 0) để tạo thumbnail 9:16 đập ngay vào mắt từ giây 0.00.

Thumbnail prompt pattern:
```
"Dramatic [theme] pixel art illustration of [ICONIC OBJECT glowing/prominent], [environment details], [lighting], bold retro pixel typography, 16:9 composition"
```

### Cadence:
Same as vox-director:
- Shots: 6-7 seconds each
- 1 shot per beat
- 45s Short = 6-7 shots
- 3 min = ~24-27 shots
- 5 min = ~40-45 shots

### Cost:
Identical to vox-director (same models, same optimization):
- Image: $0.04/shot (nano-banana-2 developer)
- Video: ~$0.665/shot (Kling O3 Pro, 7s)
- Audio: ~$0.13-0.16 total
- **3 min video: ~$19**
- **45s Short: ~$5**

### Verify:
Same as vox-director:
```bash
ffmpeg -ss <t> -i final_crt.mp4 -vf "scale=640:-1,format=yuvj420p" -frames:v 1 f.jpg
```
Check that:
1. Pixel art is clearly visible and NOT mushed by motion
2. CRT scanlines are subtle (not obscuring content)
3. Text/titles are readable through the CRT overlay
4. Color palette matches the chosen theme

## beats.json schema (Pixel Retro adaptations)

```json
{
  "project": "my-retro-film", "topic": "...", "language": "en",
  "aspect": "16:9",                       // 16:9 | 9:16 | 1:1 | 3:4
  "style": "pixel-art",
  "provider": "flowkit",                  // ⛔ MẶC ĐỊNH flowkit — KHÔNG được đổi sang atlas_cloud nếu chưa có sự cho phép của user
  "theme": "crt-arcade",                  // THEME_PRESET — the LOOK layer
  "arc": "timeline",                      // narrative arc (beat-layer.md) — the STORY skeleton
  "video_model": "kwaivgi/kling-video-o3-pro/image-to-video",
  "image_model": "google/nano-banana-2/text-to-image-developer",
  "image_resolution": "1k",
  "video_resolution": "720p",
  "motion_style": "calm",                 // amplitude: calm for pixel art to avoid mushing
  "constraints": "strict",                // strict = keep it flat 2D
  "voice": {"voice_id": "kai", "language": "en", "speed": 1.0}, // young, energetic male
  "music": "chiptune 8-bit retro gaming soundtrack, 120 BPM",
  "mix": {"music": 0.3, "voice": 1.5},
  "caption_style": "white",               // set by channel skill: "white" (pixel/retro) | "paper" (Vox collage)
  "captions": true,
  "watermark": "Pixel Rewind",              // set by channel skill — text watermark góc phải dưới (cũng che logo Veo)
  "watermark_image": "assets/pixel_rewind_watermark.png", // set by channel skill — Logo PNG góc trái trên (branding)
  "beats": [
    {
      "id": 1, "title_cn": "", "title_en": "THE BEGINNING",
      "bg": "dark amber glow", "feel": "nostalgic, electric", "hook": "curiosity",
      "narration": "Before the internet, there was the arcade...",
      "shots": [
        {"id": "a", "dur": 6, "title": true,  "shot_size": "WIDE", "camera_move": "static",
         "scene": "Detailed 16-bit pixel art of a dark arcade room glowing with cabinet screens...",
         "element_motion": "screens flicker, score counter ticks up rapidly, scanlines scroll"}
      ]
    }
  ]
}
```

## Model selection (always verify IDs live)

Same backend approach as vox-director, utilizing `provider.py`.

| Job | Model | Note |
|---|---|---|
| Keyframe / pixel art | `google/nano-banana-2/text-to-image-developer` | default; $0.04 |
| Animate (default) | `kwaivgi/kling-video-o3-pro/image-to-video` | default; maintains 2D grid stability well |
| Narration | `xai/tts-v1` | `voice_id: kai` for energetic male |
| Music | `minimax/music-2.6` | `is_instrumental: true` |
