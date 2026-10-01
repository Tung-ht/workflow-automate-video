#!/usr/bin/env python3
"""
Clip stage: animate each SHOT's keyframe into a short clip (Gemini Omni Flash
image-to-video), using the shot's own duration and a punchy collage
motion-graphic prompt (5-axis + the shot's specific move). More, shorter shots
= more cuts = less "one static frame for 10s".

Usage: python3 clips.py <project_dir>   (default: out/tang-30s)
"""
import json
import os
import sys

from provider import get_provider, run_jobs
from styles import resolve_theme, resolve_video_aspect

VIDEO_MODEL = "vidu/q3-turbo/image-to-video"


def shots_of(beat):
    if beat.get("shots"):
        for s in beat["shots"]:
            yield s, f"{beat['id']}{s.get('id','')}"
    else:
        yield beat, f"{beat['id']}"


# Camera-move vocab. The first group is flat-collage-SAFE (default). The "bold" group can warp
# the flat art / smear text (verified) — they're AVAILABLE, not banned: use with constraints
# "loose" and expect to re-roll. Any string not in the dict passes through verbatim too.
CAMERA_VOCAB = {
    "static":   "a locked-off static camera (no camera move)",
    "push_in":  "one very slow smooth push-in (uniform scale-up, Ken-Burns)",
    "pull_out": "one slow smooth pull-out (uniform scale-down) revealing the full scene",
    "pan":      "one slow horizontal pan across the frame (flat translate, no perspective shift)",
    "tilt":     "one slow vertical tilt (flat translate, no perspective shift)",
    "parallax": "a gentle multi-layer parallax drift (paper layers moving at slightly different "
                "speeds), the camera otherwise steady",
    # bold / experimental (pair with constraints="loose", re-roll):
    "orbit":     "a slow 3D orbit / camera arc around the scene",
    "dolly_zoom": "a dolly-zoom (vertigo) — push in while the background pulls back",
    "roll":      "a slow camera roll / canted rotation",
    "whip":      "a fast whip-pan sweep that settles",
}

AMPLITUDE = {
    "calm":   "subtle, restrained amplitude",
    "punchy": "lively, energetic amplitude with clear, bold movement",
    "max":    "high-energy amplitude — elements burst, scatter and fly boldly",
}

# Neutral fallback when a shot doesn't specify element_motion. Prefer per-shot AI-authored
# element_motion that fits the scene — do NOT force a flying element into every shot.
DEFAULT_ELEMENT = ("several cut-out elements move naturally with the scene — they bob, tilt, "
                   "slide, drift and scatter; halftone dots pulse")


def collage_prompt(camera, element_motion=None, feel=None, palette=None, amplitude="punchy",
                   has_title=True, constraints="strict", anchor_freeze=None, style="collage"):
    """Collage / Pixel motion prompt. `constraints`: 'strict' = defect guards on (flat-2D, one-way,
    no-morph) for text-heavy explainers; 'loose' = let the model explore (3D/bold moves), keep
    only the essentials. Text is hard-protected ONLY when the shot has a headline (has_title).
    `anchor_freeze`: C-roll only — a FREEZE sentence protecting the photographic anchor
    sticker (face or product+label); croll_keyframes.py writes it into beats.json. Without it
    the video stage may re-letter a label or re-time a face (both observed in validation)."""
    cam = CAMERA_VOCAB.get(camera, camera)
    element = element_motion or DEFAULT_ELEMENT
    feel = feel or "tactile, editorial, a page from a scrapbook"
    palette = palette or "the still's existing palette, high contrast"
    amp = AMPLITUDE.get(amplitude, AMPLITUDE["punchy"])
    text_lock = ("Keep the HEADLINE TEXT sharp, legible and stable — do not warp or wobble the "
                 "lettering. " if has_title else "")
    if anchor_freeze:
        text_lock = f"{anchor_freeze} " + text_lock

    if style in ("pixel-art", "crt-arcade", "pixel", "retro", "vhs-rewind", "terminal-green"):
        guard = (text_lock + "Keep the retro pixel art style, pixel grid, and clean retro textures intact. "
                 "Stay flat 2D — no 3D rotation, no perspective distortion. ONE continuous move. "
                 "Animate the motion only; do not melt or blur the pixel graphic.")
        return (
            "Animate this 16-bit pixel art scene into a subtle, retro-appropriate motion graphic.\n"
            f"CAMERA (one move only): {cam}.\n"
            f"ELEMENT MOTION (rich — this is the energy, {amp}): {element}.\n"
            "AESTHETIC: keep the 16-bit pixel grid, scanlines, and retro computing aesthetic.\n"
            f"FEEL: {feel}.\nCOLOR: {palette}.\n"
            f"CONSTRAINTS: {guard}"
        )

    if constraints == "loose":
        guard = (text_lock + "Keep the paper-collage look (printed cut-outs, not photoreal); "
                 "avoid a subject melting into shapeless goo. Otherwise explore freely.")
    else:  # strict — defect guards for clean, text-heavy explainers
        guard = (text_lock + "STRICT 2D CONSTRAINTS: ABSOLUTELY NO ZOOM-IN, NO PUSH-IN, NO 3D CAMERA PUSH. "
                 "Camera must remain strictly flat 2D parallel to the comic poster. "
                 "ONE continuous move that does not loop, retract or reset. Rigid paper — no morph/melt. Animate the motion only; don't re-render the picture.")
        if "wave" in str(element_motion).lower() or "ripple" in str(element_motion).lower():
            guard += " Include a subtle tactile paper wave wobble ripple effect, as if someone is holding the edge of the printed comic paper page and gently shaking it to create paper wave ripples."

    return (
        "Animate this still into a mixed-media paper-collage MOTION GRAPHIC, printed cut-outs, "
        "not photoreal.\n"
        f"CAMERA (one move only): {cam}.\n"
        f"ELEMENT MOTION (rich — this is the energy, {amp}): {element}. Elements move as paper "
        "cut-outs (slide, flap, hinge, pop, scatter, fly).\n"
        "AESTHETIC: keep the torn-paper, tape, halftone, newsprint and paper-stencil textures "
        "and the bold flat background.\n"
        f"FEEL: {feel}.\nCOLOR: {palette}.\n"
        f"CONSTRAINTS: {guard}"
    )


def painterly_prompt(motion):
    return (f"Animate this artistic scene with subtle, tasteful motion: {motion}. "
            f"STRICTLY NO ZOOM-IN. Keep the original visual style, textures, and details intact and stable. "
            f"Gentle, cinematic, no morphing, no new objects.")



def run(project_dir, only=None):
    bpath = os.path.join(project_dir, "beats.json")
    with open(bpath, encoding="utf-8") as f:
        doc = json.load(f)
    aspect = doc.get("aspect", "16:9")
    style = doc.get("style", "collage")
    _theme = resolve_theme(doc.get("theme")) or {}
    motion_style = doc.get("motion_style") or _theme.get("motion_style", "punchy")  # calm|punchy|max
    constraints = doc.get("constraints", "strict")   # strict = defect guards on | loose = explore
    model = doc.get("video_model", VIDEO_MODEL)   # Seedance for real people; Omni otherwise
    vid_res = doc.get("video_resolution", "720p")  # 720p default; Seedance also 480p/1080p (Omni is 720p-only)
    clip_dir = os.path.join(project_dir, "clips")
    os.makedirs(clip_dir, exist_ok=True)

    # Aspect routing: prefer the project's own target aspect; only fall back to an
    # approximation when this model has no matching enum value, and never apply that
    # approximation without a human confirming it first (see styles.resolve_video_aspect).
    resolved_aspect, aspect_exact = resolve_video_aspect(aspect, model)
    if not aspect_exact:
        if not doc.get("aspect_approx_confirmed"):
            print(f"ASPECT MISMATCH: project aspect \"{aspect}\" has no exact match on "
                  f"{model}; nearest supported is \"{resolved_aspect}\". This changes the "
                  f"output framing — confirm with the user before generating, then set "
                  f"\"aspect_approx_confirmed\": true in beats.json to proceed (or pick a "
                  f"different video_model / aspect).")
            return
        print(f"[aspect] using confirmed approximation \"{resolved_aspect}\" for project "
              f"aspect \"{aspect}\" on {model}")
    if resolved_aspect:
        aspect = resolved_aspect   # every shot below shares this one resolved aspect

    prov = get_provider(doc.get("provider"))
    specs, by_key = {}, {}
    for beat in doc["beats"]:
        for shot, key in shots_of(beat):
            if only and key not in only:
                continue
            # Protection: Never resubmit if clip file already exists on disk or in shot dict
            dest_clip = os.path.join(clip_dir, f"clip_{key}.mp4")
            if os.path.exists(dest_clip) and os.path.getsize(dest_clip) > 1000:
                shot["clip_path"] = dest_clip
                print(f"[{key}] clip file already exists on disk ({dest_clip}) -> skip")
                continue
            if shot.get("clip_path") and os.path.exists(shot["clip_path"]):
                print(f"[{key}] clip already exists -> skip")
                continue
            if shot.get("clip_url"):
                print(f"[{key}] clip_url exists but file missing, redownloading...")
                dest = os.path.join(clip_dir, f"clip_{key}.mp4")
                try:
                    prov.download(shot["clip_url"], dest)
                    shot["clip_path"] = dest
                    with open(bpath, "w", encoding="utf-8") as f:
                        json.dump(doc, f, ensure_ascii=False, indent=2)
                    print(f"[{key}] redownloaded -> {dest}")
                except Exception as e:
                    print(f"[{key}] redownload failed: {e}")
                continue
            # Check for static shot: if marked as static, render locally with FFmpeg (no video model needed)
            is_static_shot = (
                shot.get("motion_type") in ("static", "static_pan", "static_zoom", "static_still") or
                shot.get("static") is True or
                shot.get("motion") in ("static_hold", "static_still")
            )
            if is_static_shot:
                kf_file = shot.get("keyframe_path") or os.path.join(project_dir, "keyframes", f"kf_{key}.jpg")
                if kf_file and os.path.exists(kf_file):
                    dur = float(shot.get("dur", 6.5))
                    W, H = (1920, 1080) if aspect == "16:9" else ((1080, 1920) if aspect == "9:16" else (1080, 1080))
                    cam_m = shot.get("camera_move") or shot.get("camera") or shot.get("motion", "push_in")
                    dest_clip = os.path.join(clip_dir, f"clip_{key}.mp4")
                    try:
                        frames = max(int(dur * 24), 1)
                        if cam_m in ("static", "static_still", "none", "locked"):
                            vf = (
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                                f"boxblur=26:2,eq=brightness=-0.05[bg];"
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=24[v]"
                            )
                        elif cam_m in ("pull_out", "zoom_out"):
                            z = "if(eq(on,1),1.08,max(zoom-0.0005,1.0))"
                            vf = (
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                                f"boxblur=26:2,eq=brightness=-0.05[bg];"
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,scale={W*2}:{H*2},"
                                f"zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=24[v]"
                            )
                        elif cam_m in ("pan_left", "pan_right", "pan"):
                            x_expr = "max(x-1,0)" if cam_m == "pan_left" else "min(x+1,iw-iw/zoom)"
                            vf = (
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                                f"boxblur=26:2,eq=brightness=-0.05[bg];"
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,scale={W*2}:{H*2},"
                                f"zoompan=z='1.06':d={frames}:x='if(eq(on,1),iw*0.05,{x_expr})':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=24[v]"
                            )
                        else:
                            z = "min(zoom+0.0006,1.08)"
                            vf = (
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                                f"boxblur=26:2,eq=brightness=-0.05[bg];"
                                f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
                                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,scale={W*2}:{H*2},"
                                f"zoompan=z='{z}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=24[v]"
                            )
                        import subprocess
                        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", kf_file,
                                        "-filter_complex", vf, "-map", "[v]", "-t", f"{dur}",
                                        "-c:v", "libx264", "-pix_fmt", "yuv420p", dest_clip], check=True)
                        shot["clip_path"] = dest_clip
                        print(f"[{key}] rendered static local clip -> {dest_clip} ({dur}s, local 24fps {cam_m})")
                        with open(bpath, "w", encoding="utf-8") as f:
                            json.dump(doc, f, ensure_ascii=False, indent=2)
                        continue
                    except Exception as e:
                        print(f"[{key}] local static render failed: {e}, falling back to cloud model...")

            if doc.get("provider") == "flowkit" and shot.get("keyframe_path") and os.path.exists(shot["keyframe_path"]):
                url = shot["keyframe_path"]
            else:
                url = shot.get("keyframe_url")
                if (not url or "flow-content.google" in url) and shot.get("keyframe_path") and os.path.exists(shot["keyframe_path"]):
                    print(f"[{key}] uploading/refreshing keyframe -> {shot['keyframe_path']}")
                    url = prov.upload(shot["keyframe_path"])
                    shot["keyframe_url"] = url
                    print(f"[{key}] keyframe uploaded -> {url}")
            if not url:
                print(f"[{key}] no keyframe — provide keyframe_path or run keyframes.py")
                continue
            # new schema: camera_move (token) + element_motion (rich). Back-compat: old `motion`.
            camera = shot.get("camera_move") or shot.get("motion", "static")
            element = shot.get("element_motion")
            if shot.get("video_prompt"):
                prompt = shot["video_prompt"]
            elif style in ("collage", "pulp-comic", "pulp-comic-director", "pixel-art", "crt-arcade", "pixel", "retro", "vhs-rewind", "terminal-green", "blueprint-noir", "blueprint-noir-director"):
                prompt = collage_prompt(camera, element_motion=element, feel=beat.get("feel"),
                                        palette=beat.get("bg"), amplitude=motion_style,
                                        anchor_freeze=doc.get("anchor_freeze"),
                                        has_title=shot.get("title", True), constraints=constraints,
                                        style=style)
            else:
                prompt = painterly_prompt(shot.get("motion", camera))
            dur = int(shot.get("dur", 10))
            if "seedance" in model:                 # ratio (not aspect_ratio); real-person OK
                params = dict(image=url, duration=dur, ratio=aspect,
                              resolution=vid_res, generate_audio=False)
            elif "kling-video-o3-pro/reference-to-video" in model:  # has an aspect_ratio enum
                params = dict(image=url, duration=dur, aspect_ratio=aspect, sound=False)
            elif "kling" in model:                   # image-to-video / video-edit: follows input; allows real people
                params = dict(image=url, duration=dur, aspect_ratio=aspect, sound=False)
            elif "vidu" in model:
                params = dict(image=url, duration=dur, aspect_ratio=aspect, resolution="1080p-sr")
            else:                                    # gemini omni flash
                params = dict(image=url, duration=dur, aspect_ratio=aspect, resolution=vid_res)
            specs[key] = (lambda m=model, p=prompt, pr=params: prov.submit_video(m, p, **pr))
            by_key[key] = shot
            mname = model.split('/')[1] if '/' in model else model
            print(f"[{key}] queued ({dur}s, {mname})")

    initial_pids = {k: v.get("clip_pid") for k, v in by_key.items() if v.get("clip_pid")}

    def on_submit(key, pid):
        shot = by_key[key]
        shot["clip_pid"] = pid
        try:
            with open(bpath, "w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def on_success(key, url):
        if not url: return
        dest = os.path.join(clip_dir, f"clip_{key}.mp4")
        try:
            prov.download(url, dest)
            shot = by_key[key]
            shot["clip_url"] = url
            shot["clip_path"] = dest
            print(f"[{key}] saved {dest}")
            with open(bpath, "w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[{key}] error downloading/saving: {e}")

    if doc.get("provider") == "flowkit":
        print(f"\n[flowkit] Submitting {len(specs)} clip(s) to FlowKit in batches of 3 (fire-and-forget, no polling/retries)...")
        keys = list(specs.keys())
        for i in range(0, len(keys), 3):
            batch = keys[i:i+3]
            for k in batch:
                pid = specs[k]()
                on_submit(k, pid)
                print(f"[{k}] submitted -> {pid}")
            if i + 3 < len(keys):
                import time
                time.sleep(12)
        print(f"\n[flowkit] All {len(specs)} clip(s) submitted directly to Google Flow! Open your active project to download.")
        print("updated", bpath)
        return

    done = run_jobs(prov, specs, initial_pids=initial_pids, on_submit=on_submit, on_done=on_success, poll_s=5, stall_s=1800, max_retries=2, deadline_s=7200)
    print("updated", bpath)


if __name__ == "__main__":
    proj = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "out", "tang-30s")
    only = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    run(os.path.abspath(proj), only=only)
