#!/usr/bin/env python3
"""
Assembly stage (ffmpeg): multi-shot clips + per-beat narration + music -> final.mp4

Model: beats -> shots. Each shot is one short clip (its own cut). Narration and
captions are per BEAT and span all the beat's shots, so the voice stays aligned
while the visuals cut. BGM is ducked under the narration. Captions + watermark
are Pillow PNGs composited with `overlay` (this ffmpeg has no libass/drawtext).

Usage: python3 assemble.py <project_dir>   (default: out/tang-30s)
"""
import json
import os
import subprocess
import sys

import text_overlay

FPS, TAIL = 24, 0.5
WATERMARK = ""
RES = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080)}


def ff(args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def probe_dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    try:
        return float(out.strip())
    except ValueError:
        return 0.0


def shots_of(beat):
    if beat.get("shots"):
        for s in beat["shots"]:
            yield s
    else:
        yield beat


import re

def split_narration_into_chunks(text, target_min=3, target_max=8):
    raw_parts = [s.strip() for s in re.split(r'(?<=[.!?,;:—–])\s+', text) if s.strip()]
    chunks = []
    current_words = []
    for part in raw_parts:
        words = part.split()
        if len(current_words) + len(words) <= target_max:
            current_words.extend(words)
        else:
            if current_words:
                chunks.append(" ".join(current_words))
                current_words = []
            if len(words) <= target_max:
                current_words = list(words)
            else:
                for i in range(0, len(words), target_max):
                    sub = words[i:i+target_max]
                    if len(sub) < target_min and chunks:
                        prev = chunks[-1].split()
                        if len(prev) + len(sub) <= target_max + 3:
                            chunks[-1] = " ".join(prev + sub)
                        else:
                            chunks.append(" ".join(sub))
                    else:
                        chunks.append(" ".join(sub))
                current_words = []
    if current_words:
        if len(current_words) < target_min and chunks:
            prev = chunks[-1].split()
            if len(prev) + len(current_words) <= target_max + 3:
                chunks[-1] = " ".join(prev + current_words)
            else:
                chunks.append(" ".join(current_words))
        else:
            chunks.append(" ".join(current_words))
    return chunks

def run(project_dir):
    with open(os.path.join(project_dir, "beats.json"), encoding="utf-8") as f:
        doc = json.load(f)
    beats = doc["beats"]
    W, H = RES.get(doc.get("aspect", "16:9"), (1920, 1080))
    wm_text = doc.get("watermark", WATERMARK)
    mix = doc.get("mix", {})                      # per-project audio balance (optional)
    music_vol = float(mix.get("music", 0.6))      # BGM level (was a fixed 0.9 — lowered so VO leads)
    voice_vol = float(mix.get("voice", 1.25))     # narration boost before the duck + final mix
    cap_style = doc.get("caption_style", "white") # from beats.json — each skill sets its own (vox→paper, pixel→white)
    tmp = os.path.join(project_dir, "_seg")
    os.makedirs(tmp, exist_ok=True)

    # ---- flatten shots into timed segments; track each beat's span ----
    segs = []          # {clip, dur}
    beat_spans = []    # {start, dur, beat}
    t = 0.0
    for beat in beats:
        beat_start = t
        shot_list = list(shots_of(beat))
        # ensure the beat covers its narration (extend last shot if needed)
        durs = [float(s.get("dur", 10)) for s in shot_list]
        need = float(beat.get("narration_dur", sum(durs))) + TAIL
        if sum(durs) < need:
            durs[-1] += need - sum(durs)
        for s, d in zip(shot_list, durs):
            clip_p = s.get("clip_path")
            # Auto-fallback: if clip_path is missing or doesn't exist on disk, check for keyframe_path
            if not clip_p or not os.path.exists(clip_p):
                kf_p = s.get("keyframe_path")
                if not kf_p or not os.path.exists(kf_p):
                    # check if keyframe file exists in keyframes/
                    bid = beat["id"]
                    sid = s.get("id", "")
                    cand = os.path.join(project_dir, "keyframes", f"kf_{bid}{sid}.jpg")
                    if os.path.exists(cand):
                        kf_p = cand
                if kf_p and os.path.exists(kf_p):
                    auto_clip = os.path.join(project_dir, "clips", f"clip_{beat['id']}{s.get('id','')}.mp4")
                    os.makedirs(os.path.dirname(auto_clip), exist_ok=True)
                    cam_m = s.get("camera_move") or s.get("camera") or s.get("motion", "push_in")
                    print(f"[assemble] Auto-generating 24 FPS static clip for {beat['id']}{s.get('id','')} from keyframe ({cam_m})...")
                    frames = max(int(d * FPS), 1)
                    if cam_m in ("static", "static_still", "none", "locked"):
                        vf = (
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                            f"boxblur=26:2,eq=brightness=-0.05[bg];"
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps={FPS}[v]"
                        )
                    elif cam_m in ("pull_out", "zoom_out"):
                        z = "if(eq(on,1),1.08,max(zoom-0.0005,1.0))"
                        vf = (
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                            f"boxblur=26:2,eq=brightness=-0.05[bg];"
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,scale={W*2}:{H*2},"
                            f"zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}[v]"
                        )
                    elif cam_m in ("pan_left", "pan_right", "pan"):
                        x_expr = "max(x-1,0)" if cam_m == "pan_left" else "min(x+1,iw-iw/zoom)"
                        vf = (
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                            f"boxblur=26:2,eq=brightness=-0.05[bg];"
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,scale={W*2}:{H*2},"
                            f"zoompan=z='1.06':d={frames}:x='if(eq(on,1),iw*0.05,{x_expr})':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}[v]"
                        )
                    else:
                        z = "min(zoom+0.0006,1.08)"
                        vf = (
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                            f"boxblur=26:2,eq=brightness=-0.05[bg];"
                            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,scale={W*2}:{H*2},"
                            f"zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}[v]"
                        )
                    ff(["-loop", "1", "-i", kf_p, "-filter_complex", vf, "-map", "[v]", "-t", f"{d}",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", auto_clip])
                    clip_p = auto_clip
                    s["clip_path"] = auto_clip
            segs.append({"clip": clip_p, "dur": round(d, 2)})
            t += d
        beat_spans.append({"start": beat_start, "dur": round(t - beat_start, 2), "beat": beat})
    total = round(t, 2)

    # ---- 1) normalise each shot to a silent segment of exactly its dur ----
    print(f"[assemble] Step 1/4: Normalizing {len(segs)} shot segments to 24 FPS HD...", flush=True)
    seg_files = []
    for i, s in enumerate(segs):
        out = os.path.join(tmp, f"seg_{i:02d}.mp4")
        if not s.get("clip") or not os.path.exists(s["clip"]):
            raise FileNotFoundError(f"Clip file not found: {s.get('clip')}")
        cd = probe_dur(s["clip"])
        factor = s["dur"] / cd if cd > 0 else 1.0
        pre = f"setpts={factor:.4f}*PTS," if factor > 1.02 else ""
        fc = (f"[0:v]{pre}split[s0][s1];"
              f"[s0]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"boxblur=26:2,eq=brightness=-0.05[bg];"
              f"[s1]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps={FPS},"
              f"tpad=stop_mode=clone:stop_duration=1[v]")
        print(f"  - seg {i+1}/{len(segs)} ({s['dur']}s): {os.path.basename(s['clip'])}", flush=True)
        ff(["-i", s["clip"], "-an", "-filter_complex", fc, "-map", "[v]", "-t", f"{s['dur']}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", out])
        seg_files.append(out)

    # ---- 2) concat all shot segments (video only) ----
    print("[assemble] Step 2/4: Concatenating silent video segments...", flush=True)
    listf = os.path.join(tmp, "list.txt")
    with open(listf, "w", encoding="utf-8") as f:
        for s in seg_files:
            f.write(f"file '{os.path.abspath(s)}'\n")
    body = os.path.join(tmp, "body_silent.mp4")
    ff(["-f", "concat", "-safe", "0", "-i", listf, "-c", "copy", body])

    # ---- 3) captions (per short phrase chunk) + watermark PNGs ----
    print("[assemble] Step 3/4: Generating subtitle phrase overlays & watermark...", flush=True)
    captions_on = bool(doc.get("captions", True))
    cap_items = []  # list of {path, start, end}
    if captions_on:
        for bs in beat_spans:
            beat = bs["beat"]
            b_start = bs["start"]
            b_dur = bs["dur"]
            chunks = split_narration_into_chunks(beat["narration"], target_min=3, target_max=8)
            total_words = sum(len(c.split()) for c in chunks)
            if total_words == 0:
                continue
            
            acc = None
            if cap_style == "paper":
                kf = next((s["keyframe_path"] for s in (beat.get("shots") or [beat])
                           if s.get("keyframe_path") and os.path.exists(s["keyframe_path"])), None)
                acc = text_overlay.accent_color(kf) if kf else None
            
            curr_t = b_start + 0.1
            for j, c_text in enumerate(chunks):
                c_words = len(c_text.split())
                c_dur = round((c_words / total_words) * (b_dur - 0.2), 2)
                if c_dur < 1.0:
                    c_dur = 1.0
                c_end = round(curr_t + c_dur, 2)
                if c_end > b_start + b_dur:
                    c_end = b_start + b_dur
                
                p = os.path.join(tmp, f"cap_{beat['id']}_{j+1}.png")
                text_overlay.render_caption(c_text, p, W, H, accent=acc, style=cap_style)
                cap_items.append({"path": p, "start": curr_t, "end": c_end})
                curr_t = c_end

    wm_img_path = doc.get("watermark_image")
    if wm_img_path and not os.path.isabs(wm_img_path):
        candidates = [
            os.path.join(project_dir, wm_img_path),
            os.path.abspath(wm_img_path),
            os.path.join(os.path.dirname(__file__), "..", wm_img_path),
            os.path.join(os.path.dirname(__file__), "..", "..", "..", wm_img_path),
        ]
        for c in candidates:
            if os.path.exists(c):
                wm_img_path = c
                break
    wm_png = text_overlay.render_watermark(wm_text, os.path.join(tmp, "wm.png"), W, H, wm_image=wm_img_path, style=cap_style)

    # ---- 4A) Render Video Pass: Overlay captions + watermark (+ CRT) onto silent video ----
    print(f"[assemble] Step 4A/4: Applying {len(cap_items)} caption overlays & watermark to video...", flush=True)
    
    crt_post = doc.get("crt_post", False)
    crt_overlay_path = None
    if crt_post:
        crt_overlay_path = os.path.join(os.path.dirname(__file__), "..",
                                         "assets", f"crt_scanline_{W}x{H}.png")
        if not os.path.exists(crt_overlay_path):
            from PIL import Image
            spacing = 3
            opacity = 90
            img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            px = img.load()
            for y in range(H):
                if y % spacing == 0:
                    for x in range(W):
                        px[x, y] = (0, 0, 0, opacity)
            os.makedirs(os.path.dirname(crt_overlay_path), exist_ok=True)
            img.save(crt_overlay_path)
            print(f"[crt] generated scanline overlay: {crt_overlay_path}", flush=True)

    v_inputs = ["-i", body]
    v_chain = []
    prev_node = "[0:v]"
    next_input_idx = 1

    # Use Concat Demuxer stream for captions if any exist (dramatically faster & low RAM)
    if cap_items:
        blank_png = os.path.join(tmp, "blank.png")
        if not os.path.exists(blank_png):
            from PIL import Image
            img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            img.save(blank_png)

        concat_txt_path = os.path.join(tmp, "concat_captions.txt")
        cap_items_sorted = sorted(cap_items, key=lambda x: x["start"])
        t_curr = 0.0
        with open(concat_txt_path, "w", encoding="utf-8") as f:
            for ci in cap_items_sorted:
                s, e = ci["start"], ci["end"]
                if s > t_curr:
                    gap = s - t_curr
                    f.write(f"file '{os.path.abspath(blank_png)}'\nduration {gap:.4f}\n")
                dur = e - s
                if dur > 0:
                    f.write(f"file '{os.path.abspath(ci['path'])}'\nduration {dur:.4f}\n")
                t_curr = e
            if total > t_curr:
                gap = total - t_curr
                f.write(f"file '{os.path.abspath(blank_png)}'\nduration {gap:.4f}\n")
            f.write(f"file '{os.path.abspath(blank_png)}'\n")

        v_inputs += ["-f", "concat", "-safe", "0", "-i", concat_txt_path]
        cap_node = "[v_cap]"
        v_chain.append(f"{prev_node}[{next_input_idx}:v]overlay=0:0{cap_node}")
        prev_node = cap_node
        next_input_idx += 1

    # Watermark
    v_inputs += ["-loop", "1", "-i", wm_png]
    wm_node = "[v_wm]" if crt_post else "[v]"
    v_chain.append(f"{prev_node}[{next_input_idx}:v]overlay=0:0{wm_node}")
    prev_node = wm_node
    next_input_idx += 1

    # CRT filter post-processing
    if crt_post:
        v_inputs += ["-loop", "1", "-i", crt_overlay_path]
        v_chain.append(f"{prev_node}[{next_input_idx}:v]overlay=0:0,eq=saturation=1.1:contrast=1.08:brightness=-0.01[v]")

    v_filt = ";".join(v_chain)
    video_tagged = os.path.join(tmp, "video_tagged.mp4")
    ff([*v_inputs, "-filter_complex", v_filt, "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", f"{total}", video_tagged])

    # ---- 4B) Render Audio Pass & Multiplex: Mix per-beat narration + duck BGM + copy tagged video ----
    nb = len(beat_spans)
    print(f"[assemble] Step 4B/4: Mixing audio tracks ({nb} voice + BGM) & multiplexing final MP4...", flush=True)
    a_inputs = ["-i", video_tagged]
    for bs in beat_spans:
        a_inputs += ["-i", bs["beat"]["narration_audio"]]
    bgm_idx = nb + 1
    a_inputs += ["-i", doc["bgm_path"]]

    a_chain = []
    nlabels = []
    for i, bs in enumerate(beat_spans):
        ms = int(bs["start"] * 1000)
        a_chain.append(f"[{i+1}:a]adelay={ms}:all=1[n{i}]")
        nlabels.append(f"[n{i}]")
    a_chain.append(f"{''.join(nlabels)}amix=inputs={nb}:normalize=0:duration=longest,volume={voice_vol},apad,atrim=0:{total}[narrmix]")
    a_chain.append("[narrmix]asplit=2[narrA][narrB]")
    a_chain.append(f"[{bgm_idx}:a]atrim=0:{total},volume={music_vol},afade=t=out:st={max(total-2,0):.2f}:d=2[bgt]")
    a_chain.append("[bgt][narrA]sidechaincompress=threshold=0.04:ratio=4:attack=50:release=800[bgd]")
    a_chain.append(f"[narrB][bgd]amix=inputs=2:normalize=0:duration=longest,volume=1.4,atrim=0:{total}[a]")
    a_filt = ";".join(a_chain)

    final = os.path.join(project_dir, "final.mp4")
    ff([*a_inputs, "-filter_complex", a_filt, "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-t", f"{total}", final])
    crt_note = " +CRT" if crt_post else ""
    print(f"FINAL: {final} (~{total}s, {len(segs)} shots{crt_note})", flush=True)


if __name__ == "__main__":
    proj = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "out", "tang-30s")
    run(os.path.abspath(proj))
