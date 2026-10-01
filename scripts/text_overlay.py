#!/usr/bin/env python3
"""
Text overlays via Pillow -> transparent PNG (this ffmpeg has no libass/drawtext,
so captions/watermark are rendered as images and composited with `overlay`).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_BOLD = [
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]
FONT_REG = [
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]

CAPTION_STYLES = ("white", "paper")


def _font(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def accent_color(image_path, default=(214, 64, 42)):
    """Sample a vibrant color from a keyframe so the caption keyline travels with
    each film's palette (Mexican -> pink/teal, Tang -> vermilion...). Fallback default.
    Only the `paper` caption style uses this."""
    try:
        im = Image.open(image_path).convert("RGB").resize((80, 80)).quantize(colors=24).convert("RGB")
    except Exception:
        return default
    best, best_score = None, -1.0
    for count, (r, g, b) in (im.getcolors(80 * 80) or []):
        mx, mn = max(r, g, b), min(r, g, b)
        if mx == 0:
            continue
        sat, val = (mx - mn) / mx, mx / 255.0
        if sat < 0.45 or val < 0.35 or val > 0.92:   # skip washed-out / too dark / too light
            continue
        score = sat * val * (count ** 0.3)
        if score > best_score:
            best, best_score = (r, g, b), score
    return best or default


def render_caption(text, out_path, W=1920, H=1080, margin_v=None, accent=None, style="white"):
    """Bottom-centered caption. `style` picks the look (default 'white'):
      white – plain white letters + dark edge + soft shadow, NO band. The clean,
              legible subtitle look from the original Tang film. Never gaudy.
      paper – cream cut-out paper letters + ink edge + soft shadow + optional per-beat
              colored keyline (the collage-styled look; `accent` is used ONLY here).
    Size is small (like the original captions) so it never occludes the collage."""
    if style not in CAPTION_STYLES:
        style = "white"
    size = int(min(W, H) * 0.045)
    if margin_v is None:
        margin_v = int(H * 0.06)
    fnt = _font(FONT_BOLD, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d0 = ImageDraw.Draw(img)
    lines = _wrap(d0, text, fnt, int(W * 0.8))
    lh = int(size * 1.3)
    y0 = H - margin_v - lh * len(lines)
    # (x, y, text, width) per line
    pos = [(round((W - d0.textlength(ln, font=fnt)) / 2), y0 + i * lh, ln,
            d0.textlength(ln, font=fnt)) for i, ln in enumerate(lines)]

    if style == "paper":
        _draw_paper(img, pos, fnt, size, accent)
    else:
        _draw_white(img, pos, fnt, size)
    img.save(out_path)
    return out_path


def _draw_white(img, pos, fnt, size):
    """Clean white subtitle: white fill, dark keyline for legibility, soft shadow."""
    ow = max(2, round(size * 0.08))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for x, y, t, _ in pos:
        sd.text((x + 2, y + 3), t, font=fnt, fill=(0, 0, 0, 175),
                stroke_width=ow, stroke_fill=(0, 0, 0, 175))
    blended = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(4)))
    img.paste(blended, (0, 0))
    d = ImageDraw.Draw(img)
    for x, y, t, _ in pos:
        d.text((x, y), t, font=fnt, fill=(255, 255, 255, 255),
               stroke_width=ow, stroke_fill=(26, 20, 16, 235))


def _draw_paper(img, pos, fnt, size, accent):
    """Cream cut-out paper letters + ink edge + soft shadow + optional colored keyline."""
    W, H = img.size
    ow = max(3, round(size * 0.13))                       # ink edge
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))          # soft shadow halo
    sd = ImageDraw.Draw(sh)
    for x, y, t, _ in pos:
        sd.text((x + 3, y + 4), t, font=fnt, fill=(8, 6, 3, 190),
                stroke_width=ow, stroke_fill=(8, 6, 3, 190))
    blended = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(5)))
    img.paste(blended, (0, 0))
    d = ImageDraw.Draw(img)
    if accent:                                            # per-beat colored keyline
        a = tuple(accent[:3]) + (255,)
        kw = max(4, round(size * 0.14))
        for x, y, t, _ in pos:
            d.text((x, y), t, font=fnt, fill=a, stroke_width=ow + kw, stroke_fill=a)
    for x, y, t, _ in pos:                                # cream cut-out letters + ink edge
        d.text((x, y), t, font=fnt, fill=(252, 246, 232, 255),
               stroke_width=ow, stroke_fill=(32, 22, 18, 255))


def render_title(text, out_path, W=1080, H=1920, sub=None):
    """Big centered title (dark on transparent) for the ending assembly card."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = int(min(W, H) * 0.075)
    fnt = _font(FONT_BOLD, size)
    lines = _wrap(d, text, fnt, int(W * 0.86))
    lh = int(size * 1.2)
    y = int(H * 0.1)
    for ln in lines:
        w = d.textlength(ln, font=fnt)
        d.text(((W - w) / 2, y), ln, font=fnt, fill=(40, 30, 24, 255),
               stroke_width=2, stroke_fill=(255, 255, 255, 180))
        y += lh
    if sub:
        sf = _font(FONT_REG, int(size * 0.4))
        sw = d.textlength(sub, font=sf)
        d.text(((W - sw) / 2, y + 6), sub, font=sf, fill=(150, 40, 30, 255))
    img.save(out_path)
    return out_path


def render_watermark(text, out_path, W=1920, H=1080, wm_image=None, style="white"):
    """Renders watermark overlay PNG. Two layers:
      1. Logo PNG at top-left (branding) — if watermark_image is set
      2. Text watermark at bottom-right (always) — MUST 100% cover Veo/AI model logo

    The bottom-right text is styled matching `style` (white/paper) and positioned
    to fully cover the Veo logo embedded by Google Flow at the bottom right corner
    in both 16:9 (long) and 9:16 (short) videos.
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    is_vertical = H > W

    # ---- Layer 1: Logo PNG at top-left (branding) ----
    if wm_image and os.path.exists(wm_image):
        try:
            wm_asset = Image.open(wm_image).convert("RGBA")
            target_w = int(W * 0.11) if is_vertical else int(W * 0.075)
            aspect = wm_asset.height / wm_asset.width
            target_h = int(target_w * aspect)
            
            # Limit height so it stays within top bar margin (max 6% of H)
            max_h = int(H * 0.06)
            if target_h > max_h:
                target_h = max_h
                target_w = int(target_h / aspect)

            wm_resized = wm_asset.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Apply subtle transparency (85% opacity) for elegant broadcast feel
            r, g, b, a = wm_resized.split()
            a = a.point(lambda p: int(p * 0.85))
            wm_resized = Image.merge("RGBA", (r, g, b, a))

            # Tight top-left corner placement (2% W, 2.5% H) so it never touches headlines
            pad_x, pad_y = int(W * 0.02), int(H * 0.025)
            img.paste(wm_resized, (pad_x, pad_y), wm_resized)
        except Exception as e:
            print(f"Warning: Failed to load custom watermark image ({wm_image}): {e}. Text-only fallback.")

    # ---- Layer 2: Text watermark at bottom-right (MUST fully cover Veo logo) ----
    if text:
        d = ImageDraw.Draw(img)
        # Sized to cover the Veo logo reliably (3.8% of min dimension for 9:16 vertical, 3.2% for 16:9)
        size = int(min(W, H) * 0.038) if is_vertical else int(min(W, H) * 0.032)
        fnt = _font(FONT_BOLD, size)
        tw = d.textlength(text, font=fnt)
        
        # Position right up against the bottom-right corner:
        # In 9:16 vertical, pad_y is based on min(W,H) to keep text down at bottom corner (covering Veo at y~1850-1910)
        pad_x = int(W * 0.015) if is_vertical else int(W * 0.012)
        pad_y = int(min(W, H) * 0.012) if is_vertical else int(H * 0.02)

        x = W - tw - pad_x
        y = H - size - pad_y
        ow = max(3, round(size * 0.14))

        # Soft text shadow / dark outline to obscure any underlying Veo text bleed
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        sd.text((x + 2, y + 2), text, font=fnt, fill=(0, 0, 0, 240),
                stroke_width=ow + 2, stroke_fill=(0, 0, 0, 240))
        blended = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(3)))
        img.paste(blended, (0, 0))

        d0 = ImageDraw.Draw(img)
        if style == "paper":
            d0.text((x, y), text, font=fnt, fill=(252, 246, 232, 255),
                    stroke_width=ow, stroke_fill=(32, 22, 18, 240))
        else:
            # White style: clean white text + dark edge + soft shadow
            ow_w = max(2, round(size * 0.08))
            d0.text((x, y), text, font=fnt, fill=(255, 255, 255, 255),
                    stroke_width=ow_w, stroke_fill=(26, 20, 16, 240))

    img.save(out_path)
    return out_path

