#!/usr/bin/env python3
import os
import glob
import json
import subprocess

proj_dir = os.path.abspath("out/blackprint-sr71-fuel-leak-short")
clips_dir = os.path.join(proj_dir, "clips")
kf_dir = os.path.join(proj_dir, "keyframes")
beats_path = os.path.join(proj_dir, "beats.json")

# Map patterns to target clip names
pattern_map = {
    "*blueprint*stealth*": "clip_1a.mp4",
    "*CAD*schematic*cutaway*": "clip_2a.mp4",
    "*Thermal*airflow*": "clip_3a.mp4",
    "*Mechanical*cutaway*": "clip_4a.mp4",
    "*Smoke*rising*": "clip_5a.mp4",
    "*Military*radar*": "clip_6a.mp4",
}

for pattern, target_name in pattern_map.items():
    matches = glob.glob(os.path.join(clips_dir, pattern))
    if matches:
        src = matches[0]
        dst = os.path.join(clips_dir, target_name)
        if src != dst:
            if os.path.exists(dst):
                os.remove(dst)
            os.rename(src, dst)
            print(f"Renamed: {os.path.basename(src)} -> {target_name}")

# Check clip_7a.mp4 (Outro)
dst_7a = os.path.join(clips_dir, "clip_7a.mp4")
if not os.path.exists(dst_7a):
    kf_7a = os.path.join(kf_dir, "kf_7a.jpg")
    if os.path.exists(kf_7a):
        print("Generating static Outro clip_7a.mp4 from kf_7a.jpg (8.0s)...")
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", kf_7a,
            "-t", "8.0", "-r", "24",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            dst_7a
        ], check=True)
        print("Generated clip_7a.mp4 successfully.")

# Update beats.json clip_path
with open(beats_path, "r", encoding="utf-8") as f:
    doc = json.load(f)

for beat in doc["beats"]:
    b_id = beat["id"]
    for shot in beat["shots"]:
        s_id = shot.get("id", "a")
        key = f"{b_id}{s_id}"
        clip_file = os.path.join(clips_dir, f"clip_{key}.mp4")
        if os.path.exists(clip_file):
            shot["clip_path"] = clip_file
            print(f"Linked [{key}] -> {clip_file}")

with open(beats_path, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

print("\nSuccessfully updated beats.json with all clip paths!")
