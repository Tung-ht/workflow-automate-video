#!/usr/bin/env python3
import os
import glob
import subprocess
import json

out_dir = os.path.abspath("out")
subdirs = [d for d in os.listdir(out_dir) if os.path.isdir(os.path.join(out_dir, d))]

print(f"Found {len(subdirs)} project directories in {out_dir}")

for d in sorted(subdirs):
    proj_path = os.path.join(out_dir, d)
    beats_path = os.path.join(proj_path, "beats.json")
    if os.path.exists(beats_path):
        print(f"\n--- Updating SEO for: {d} ---")
        try:
            subprocess.run(["python", "scripts/metadata.py", f"out/{d}"], check=True)
        except Exception as e:
            print(f"Error updating {d}: {e}")
    else:
        # If no beats.json, check if there's an existing youtube_seo.md to clean manually
        seo_files = glob.glob(os.path.join(proj_path, "*youtube_seo.md"))
        for sf in seo_files:
            print(f"\n--- Cleaning standalone SEO file: {sf} ---")
            with open(sf, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Remove AI disclosure block
            import re
            content_cleaned = re.sub(r'━━━━━━━━━━━━━━━━━━━━━━━━━━━━\s*\n🤖 AI CONTENT DISCLOSURE[^\n]*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\s*\n[^\n]+\n', '', content)
            content_cleaned = re.sub(r'🤖 AI CONTENT DISCLOSURE[^\n]*\n[^\n]+\n', '', content_cleaned)
            
            with open(sf, "w", encoding="utf-8") as f:
                f.write(content_cleaned)
            print(f"Cleaned: {sf}")

print("\n✅ All SEO files have been updated successfully!")
