#!/usr/bin/env python3
"""
Generate a high-CTR YouTube thumbnail (1920x1080 16:9) for Vox-style projects.
Reads `thumbnail` config from `out/<project>/beats.json`.

Features & Fault Tolerance:
1. Idempotency: Skips if `thumbnail.png` already exists (use --force to override).
2. Auto-Regenerate: If `thumbnail.png` is missing, generates or regenerates it.
3. Fallback: If AI image generation API fails, falls back to using Beat 1's keyframe (kf_1a.jpg).
4. Text & Noise Overlay: High-contrast 3-5 word headline + film grain filter to defeat AI smoothness.
"""
import os
import sys
import json
import random
import glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from provider import get_provider, run_jobs

FONT_BOLD = [
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

def _get_font(size):
    for p in FONT_BOLD:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def add_film_grain(img, intensity=12):
    """Add subtle random noise/grain to eliminate AI smooth 'Uncanny Valley' feel."""
    img = img.convert("RGBA")
    noise = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pixels = noise.load()
    w, h = img.size
    for x in range(0, w, 2):
        for y in range(0, h, 2):
            val = random.randint(0, intensity)
            alpha = random.randint(10, 40)
            color = (val, val, val, alpha) if random.random() > 0.5 else (255, 255, 255, alpha // 2)
            pixels[x, y] = color
            if x + 1 < w: pixels[x + 1, y] = color
            if y + 1 < h: pixels[x, y + 1] = color
            if x + 1 < w and y + 1 < h: pixels[x + 1, y + 1] = color
    return Image.alpha_composite(img, noise)

def render_thumbnail_text(base_img, text, color="yellow"):
    """Overlay 3-5 words in high-contrast bold typography with ink edge and shadow."""
    img = base_img.convert("RGBA")
    w, h = img.size
    draw = ImageDraw.Draw(img)
    
    text = text.upper()
    words = text.split()
    if len(words) > 6:
        text = " ".join(words[:5])
        
    font_size = int(h * 0.12)
    fnt = _get_font(font_size)
    
    text_w = draw.textlength(text, font=fnt)
    if text_w > w * 0.85:
        font_size = int(font_size * (w * 0.85 / text_w))
        fnt = _get_font(font_size)
        text_w = draw.textlength(text, font=fnt)
        
    x = int((w - text_w) / 2)
    y = int(h * 0.72)
    
    fill_col = (255, 220, 0, 255) if color == "yellow" else (255, 255, 255, 255)
    stroke_col = (10, 10, 10, 255)
    stroke_w = max(4, int(font_size * 0.12))
    
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.text((x + 6, y + 8), text, font=fnt, fill=(0, 0, 0, 220), stroke_width=stroke_w, stroke_fill=(0, 0, 0, 220))
    blended = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(6)))
    
    d = ImageDraw.Draw(blended)
    d.text((x, y), text, font=fnt, fill=fill_col, stroke_width=stroke_w, stroke_fill=stroke_col)
    
    return blended

def fit_to_aspect(img, target_w=1920, target_h=1080):
    """Crop and resize any image to exact target canvas (e.g. 16:9 or 9:16)."""
    img = img.convert("RGB")
    w, h = img.size
    target_aspect = target_w / target_h
    img_aspect = w / h
    
    if img_aspect > target_aspect:
        new_w = int(h * target_aspect)
        offset = (w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, h))
    else:
        new_h = int(w / target_aspect)
        offset = (h - new_h) // 2
        img = img.crop((0, offset, w, offset + new_h))
        
    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

def find_fallback_keyframe(project_dir):
    """Find any available keyframe image in project directory as fallback."""
    kf_dir = os.path.join(project_dir, "keyframes")
    patterns = [
        os.path.join(kf_dir, "kf_11a.jpg"),
        os.path.join(kf_dir, "kf_1a.jpg"),
        os.path.join(kf_dir, "kf_1.jpg"),
        os.path.join(kf_dir, "*.jpg"),
        os.path.join(kf_dir, "*.png"),
    ]
    for pat in patterns:
        matches = glob.glob(pat)
        if matches and os.path.exists(matches[0]):
            return matches[0]
    return None

def run(project_dir, force=False):
    beats_path = os.path.join(project_dir, "beats.json")
    if not os.path.exists(beats_path):
        print(f"Error: {beats_path} not found.")
        sys.exit(1)
        
    out_path = os.path.join(project_dir, "thumbnail.png")
    
    with open(beats_path, "r", encoding="utf-8") as f:
        doc = json.load(f)
        
    aspect_ratio = doc.get("aspect", "16:9")
    
    # Shorts Check: YouTube Shorts uses Frame 0 (Shot 1a) as thumbnail. Skip thumbnail.py for 9:16 projects unless force=True.
    if aspect_ratio == "9:16" and not force:
        print(f"[thumbnail] Project '{doc.get('project')}' is a Short (9:16). YouTube Shorts uses Frame 0 (Shot 1a) as thumbnail. SKIPPING thumbnail generation.")
        return None
        
    thumb_cfg = doc.get("thumbnail") or {}
    topic = doc.get("topic", "Explainer")
    theme = doc.get("theme", "american-retro")
    target_w, target_h = (1080, 1920) if aspect_ratio == "9:16" else (1920, 1080)
    
    custom_prompt = thumb_cfg.get("prompt")
    if not custom_prompt:
        custom_prompt = (
            f"A high-contrast editorial paper collage poster thumbnail about {topic}, "
            f"bold newsprint typography, vintage torn paper edges, Scotch tape, halftone texture, "
            f"striking central photographic cut-out object, {theme} aesthetic, {aspect_ratio} composition"
        )
        
    text = thumb_cfg.get("text") or doc.get("beats", [{}])[0].get("title_en") or "MUST WATCH"
    color = thumb_cfg.get("color", "yellow")
    
    base_img = None
    raw_img_path = os.path.join(project_dir, "thumbnail_raw.jpg")
    
    # 2. Try Generating Base Poster via AI Provider API
    print(f"[thumbnail] Generating base {aspect_ratio} thumbnail poster for '{doc.get('project')}'...")
    prov_name = doc.get("provider", "flowkit")
    img_model = doc.get("image_model", "google/nano-banana-2/text-to-image-developer")
    
    try:
        prov = get_provider(prov_name)
        def submit_job():
            return prov.submit_image(img_model, custom_prompt, aspect=aspect_ratio, resolution="2k")
            
        def on_done(key, url):
            if url:
                prov.download(url, raw_img_path)
                
        run_jobs(prov, {"thumb": submit_job}, on_done=on_done, poll_s=3, deadline_s=180, max_retries=2)
        
        if os.path.exists(raw_img_path):
            base_img = fit_to_aspect(Image.open(raw_img_path), target_w, target_h)
            doc["thumbnail_raw_path"] = raw_img_path
    except Exception as e:
        print(f"[thumbnail] Warning: Base image AI generation failed ({e}). Attempting fallback...")

    # 3. Fallback Mechanism: Use existing keyframe image if API generation failed
    if base_img is None:
        fallback_path = find_fallback_keyframe(project_dir)
        if fallback_path:
            print(f"[thumbnail] FALLBACK SUCCESS: Using keyframe '{fallback_path}' as base thumbnail.")
            raw = Image.open(fallback_path)
            base_img = fit_to_aspect(raw, target_w, target_h)
        else:
            print("[thumbnail] Error: Could not generate base image and no keyframe fallback found.")
            sys.exit(1)

    # 4. Render Typography Overlay + Film Grain Noise Filter
    print(f"[thumbnail] Applying high-contrast text overlay ('{text}') & film grain filter...")
    text_img = render_thumbnail_text(base_img, text, color=color)
    final_thumb = add_film_grain(text_img, intensity=16)
    
    final_thumb.save(out_path)
    
    # Update beats.json state
    doc["thumbnail_path"] = out_path
    try:
        with open(beats_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
        
    print(f"SUCCESS: Thumbnail created at {out_path}")
    return out_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/thumbnail.py out/<project> [--force]")
        sys.exit(1)
        
    proj_dir = sys.argv[1]
    is_force = "--force" in sys.argv or "-f" in sys.argv
    run(os.path.abspath(proj_dir), force=is_force)
