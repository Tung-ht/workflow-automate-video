# Models & Gotchas

Everything here was learned the hard way while building this pipeline. Read it before
debugging — most failures are already solved below.

## Model selection (verify IDs live first)

`GET https://api.atlascloud.ai/api/v1/models` (no auth) → keep only `display_console: true`.
Model schemas live at `https://static.atlascloud.ai/model/schema/<id-with-slashes-as-dashes>.json`
under `components.schemas.Input`.

| Job | Model | Price | Why |
|---|---|---|---|
| Keyframe / collage poster | `google/nano-banana-2/text-to-image-developer` | ~$0.04 | best CN+EN text rendering; layered look (developer tier saves 50%) |
| Animate (default) | `kwaivgi/kling-video-o3-pro/image-to-video` | ~$0.095/s | keeps on-screen text stable, handles celebrities/logos |
| Animate (alternative) | `google/gemini-omni-flash/image-to-video` | ~$0.13/s | keeps on-screen text stable, layered/parallax motion |
| Element cut-out (advanced) | `youchuan/v8.1/remove-background` | ~$0.086 | `image`=URL, submit via `generateImage` |
| Narration | `xai/tts-v1` | ~$0.015 | clean multilingual TTS; `voice_id`, `language`, `speed` |
| Music | `minimax/music-2.6` | ~$0.11 | `is_instrumental: true`; returns ~2min, trim in mix |
| SFX (whoosh, ambience) | `bytedance/seed-audio-1.0` | ~$0.015 | describe the sound in the `text` field |

### Content blocks (architecture-level, verified)
Feeding a recognizable **real celebrity + brand logos** into a video model:
- `gemini-omni-flash` (both image-to-video AND reference-to-video) → **blocked**:
  "The prompt is blocked due to prohibited contents". Removing the name from the prompt,
  converting PNG→JPG, or using a face-less silhouette does NOT help — it's the image content.
- `bytedance/seedance-2.0` → **blocked**: "Content suspected of infringing digital rights"
  (only an abstract silhouette passed).
- `kwaivgi/kling-video-o3-pro` → **allows it.** Use Kling for real people.
- The **local keyframe engine never hits this** (no video model in the loop) — the other way
  through for real-person content.

### Voice: seed-audio needs a pinned speaker (then it's beat-stable)
`bytedance/seed-audio-1.0` is a general *audio-scene* model, not a plain TTS. Given bare
narration with no pinned voice it adds pauses/SFX and produced wildly inconsistent lengths
(same 3 lines: 22s / 14s / 12s vs xai-tts's clean 8.6 / 10.2 / 9.0s). **But pinned, it is
beat-alignable** — validated 2026-07-17 with the voice-clone template in `audio.py`
(pinned **Speaker A** @audio1 + "clean dry studio vocal only — no background music, no
sound effects, no room noise or reverb"): 62 words rendered in 19.3s, verbatim, one natural
0.5s pause. The earlier "rhythm doesn't match the beats" failures were the bare-narration
usage, not the model. Default to `xai/tts-v1` for narration; reach for seed-audio for
voice cloning (`voice.clone_ref` → `references` payload), Chinese-specific voices, or SFX
like transition whooshes — and always derive final timing from the ACTUAL audio (ASR word
timestamps), never from the script.

## API gotchas (Atlas, behind a proxy)

1. **Every request MUST send a real `User-Agent` header** — default Python `urllib` UA is
   blocked by the WAF → 403 Forbidden. (`scripts/atlas_cloud.py` sets one.)
2. **Download generated assets with curl, not urllib** — the OSS host behind the local proxy
   kills `urlretrieve` with `RemoteDisconnected`.
3. **Audio/TTS/music/video all submit via `POST /api/v1/model/generateVideo`**, image &
   background-removal via `/generateImage`; poll `/model/prediction/{id}`.
   (A playbook noted a `/generateAudio` endpoint — go by what the live schema/API accepts.)
4. **A failed generation makes the prediction GET return HTTP 500** (not a clean
   `status:failed`) — treat a persistent 500 on poll as a failure, and read `message` for the
   reason.
5. POST generation calls are **not** retried (they create billable tasks); GET polls are.

## ffmpeg gotchas (this machine's build)

The local ffmpeg is minimal: **no libass, no drawtext** (no libfreetype). So:
- **Captions & watermark → render PNGs with Pillow and composite via `overlay`**
  (`scripts/text_overlay.py`). Size text by `min(W,H)` so it works in 16:9 and 9:16.
- **Off-aspect clips** (e.g. a 3:4 card in a 9:16 frame): use a blurred-cover background +
  fitted sharp foreground via `overlay`, not black bars.
- **Slow, don't freeze**: if a clip is shorter than its narration-driven segment, stretch it
  with `setpts` to fill instead of `tpad` freezing the last frame.
- **`blend` needs both inputs in the same pixel format** — convert both to `gbrp` before a
  `screen` blend (confetti overlay) or the whole frame turns magenta.
- **`sidechaincompress` output length follows its sidechain** — `apad` the narration track to
  the full duration, or `-shortest` will cut a music-only ending (e.g. a scrapbook outro).
- **Whip transitions**: `xfade` slides between shots; recompute each beat's start time
  (each transition overlaps by the transition duration) so narration/captions stay in sync.
- **Verify by extracting frames** — you can't read an mp4's content. `mjpeg` refuses
  full-range YUV, so add `format=yuvj420p` when grabbing jpgs.

## Cost

A ~30s standard film relies on Video API costs ($0.095/s for Kling) which is the largest expense. By using `draft.py` to preview before rendering, utilizing the developer tier for images ($0.04), and pacing at 1 shot per beat (fewer API calls), the overall cost is minimized and avoids wasted budget on rejected clips.
