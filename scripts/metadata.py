#!/usr/bin/env python3
"""
metadata.py — High-Performance Multi-Platform SEO Metadata Generator (YouTube & TikTok)
Clean Markdown Formatting + Smart Timestamps from beats.json
Usage: python3 metadata.py out/<project> [--channel <channel_name>]
"""

import sys
import os
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def generate_seo_metadata(project_dir, channel_name=None):
    beats_path = os.path.join(project_dir, "beats.json")
    if not os.path.exists(beats_path):
        print(f"❌ Error: beats.json not found in {project_dir}")
        sys.exit(1)

    beats_data = load_json(beats_path)
    
    project_id = beats_data.get("project", os.path.basename(project_dir))
    topic = beats_data.get("topic", "Explainer Video")
    aspect = beats_data.get("aspect", "16:9")
    is_short = (aspect == "9:16")
    channel = channel_name or beats_data.get("watermark", "YouTube Channel")
    
    beats = beats_data.get("beats", [])

    # Extract clean topic title & first beat title
    topic_clean = re.sub(r'\(.*?\)', '', topic).split("—")[0].strip()
    
    first_title_en = ""
    for beat in beats:
        if beat.get("title_en"):
            first_title_en = beat.get("title_en").strip()
            break
    if not first_title_en:
        first_title_en = topic_clean

    # Determine Niche Defaults & Schedule
    if "Pixel" in channel or "pixel" in topic.lower() or "gaming" in topic.lower():
        channel_niche = "Retro Tech & Gaming History"
        schedule_text = "Every Monday & Thursday"
        schedule_days = "Mon & Thu"
        hashtags_list = ["#PixelRewind", "#RetroGaming", "#TechHistory", "#PixelArt", "#GamingDocumentary", "#Nostalgia"]
        base_tags = ["pixel rewind", "retro gaming", "tech history", "video game history", "pixel art", "crt gaming", "nintendo history", "arcade history", "gaming documentary", "boot sequence"]
        outro_cta = "Subscribe to Pixel Rewind for more retro tech deep dives!"
        comment_q = "Which retro console or tech product brought back the most nostalgia for you?"
    elif "Pulp" in channel or "comic" in topic.lower():
        channel_niche = "Absurd Alternate History & Thought Experiments"
        schedule_text = "Every Tuesday & Friday"
        schedule_days = "Tue & Fri"
        hashtags_list = ["#PulpHypotheses", "#ThoughtExperiment", "#AlternateHistory", "#PulpComic", "#AbsurdHistory", "#HistoryMemes"]
        base_tags = ["pulp hypotheses", "thought experiment", "alternate history", "pulp comic", "absurd history", "history memes", "time glitch", "weird history", "hypothetical scenario", "comic book art"]
        outro_cta = "Subscribe to Pulp Hypotheses for more mind-bending timeline files!"
        comment_q = "How do YOU think human history would have changed if this scenario actually happened?"
    elif "Blackprint" in channel or "blueprint" in topic.lower() or "blackprint" in project_id.lower():
        channel_niche = "3D Blueprint Noir & Engineering Deconstructed"
        schedule_text = "Every Tuesday & Friday"
        schedule_days = "Tue & Fri"
        hashtags_list = ["#Blackprint", "#BlueprintNoir", "#Engineering", "#Deconstructed", "#HowItWorks", "#3DAnimation", "#MilitaryTech"]
        base_tags = ["blackprint", "blueprint noir", "3d animation", "how it works", "blueprints", "engineering breakdown", "deconstructed", "megastructures", "cad cutaway", "mechanical engineering"]
        outro_cta = "Every machine has a secret. Subscribe to Blackprint to unlock the next 3D file."
        comment_q = "What impossible machine or mega-structure should we deconstruct next in 3D?"
    else:
        channel_niche = "Everyday Monopolies & Hidden Economics"
        schedule_text = "Every Wednesday & Saturday"
        schedule_days = "Wed & Sat"
        hashtags_list = ["#PapercutBusiness", "#Economics", "#VoxStyle", "#Monopoly", "#HiddenEconomics", "#BusinessDocumentary"]
        base_tags = ["papercut business", "everyday monopolies", "hidden economics", "vox style explainer", "business documentary", "corporate secrets", "money", "economics explained", "monopoly"]
        outro_cta = "Subscribe to Papercut Business for more hidden economic deep dives!"
        comment_q = "Did this business strategy surprise you? What other company should we investigate next?"

    # Clean and normalize title text
    def normalize_title(text):
        text = text.strip()
        if text.isupper():
            words = text.split()
            acronyms = {"US", "USA", "UK", "USSR", "AI", "CRT", "NASA", "TI", "OSS", "UN", "WW2", "WWI", "PFAS", "PETM"}
            cleaned = []
            for w in words:
                clean_w = re.sub(r'[^\w]', '', w)
                if clean_w in acronyms:
                    cleaned.append(w)
                else:
                    cleaned.append(w.capitalize())
            return " ".join(cleaned)
        return text

    # Smart Topic Extraction (Never use generic intro beat titles!)
    GENERIC_INTRO_TITLES = {
        "THE CLASSIFIED FILE", "THE THOUGHT EXPERIMENT", "THE HOOK", "INTRO", "INTRODUCTION",
        "DISCLAIMER", "PROLOGUE", "THE SETUP", "FILE", "VAULT", "DISCLAIMER INTRO",
        "A QUICK THOUGHT EXPERIMENT", "BEFORE WE START"
    }

    # Split topic by em-dash or spaced hyphen or colon (preserve hyphenated words like TI-84)
    topic_no_paren = re.sub(r'\(.*?\)', '', topic).strip()
    topic_parts = [p.strip() for p in re.split(r'\s*[—–]\s*|\s+-\s+|:\s+', topic_no_paren) if p.strip()]

    # Identify question part vs named concept part
    hook_question = ""
    named_concept = ""
    for p in topic_parts:
        p_norm = normalize_title(p)
        if re.search(r'^(what if|why|how|did|could)\b', p.strip(), flags=re.IGNORECASE):
            hook_question = p_norm.rstrip("?!.") + "?"
        else:
            if not named_concept:
                named_concept = p_norm.rstrip("?!.")

    # Fallback to thumbnail text or full topic if parts are sparse
    thumb_text = normalize_title(beats_data.get("thumbnail", {}).get("text", "")).rstrip("?!.")
    clean_full_topic = normalize_title(topic_parts[0])

    # Find the most meaningful visual/story hook from beats
    best_story_beat = ""
    for b in beats:
        bt = b.get("title_en", "").strip().upper()
        if bt and bt not in GENERIC_INTRO_TITLES:
            best_story_beat = normalize_title(b.get("title_en")).rstrip("?!.")
            break

    # Determine core subject
    primary_hook = hook_question or clean_full_topic
    concept_title = named_concept or thumb_text or clean_full_topic

    # Helper to transform any statement/what-if into a natural direct question (NO "What If" on Pulp Hypotheses!)
    def convert_to_pulp_question(text):
        t = text.strip().rstrip("?!.")
        core = re.sub(r'^(what\s+if\s+|what\s+happens\s+if\s+)', '', t, flags=re.IGNORECASE).strip()
        core = re.sub(r'\(.*?\)', '', core).strip()
        
        # Already a question word
        if re.match(r'^(did|could|were|was|why|how|is|are|can|would|should)\b', core, flags=re.IGNORECASE):
            return core[0].upper() + core[1:] + "?"
            
        # "were" -> "Were ...?"
        if re.search(r'\bwere\b', core, flags=re.IGNORECASE):
            tr = re.sub(r'^(.*?)\s+were\s+(.*)$', r'Were \1 \2?', core, flags=re.IGNORECASE)
            if tr != core: return tr
            
        # "had" -> "Did ... Have ...?"
        if re.search(r'\bhad\b', core, flags=re.IGNORECASE):
            tr = re.sub(r'^(.*?)\s+had\s+(.*)$', r'Did \1 Have \2?', core, flags=re.IGNORECASE)
            if tr != core: return tr

        # Verbs ending with "ed" -> "Did ... [Verb] ...?"
        past_match = re.search(r'^(.*?)\s+([a-zA-Z]+ed)\s+(.*)$', core, flags=re.IGNORECASE)
        if past_match:
            subj = past_match.group(1).strip()
            verb_ed = past_match.group(2).strip()
            rest = past_match.group(3).strip()
            if verb_ed.lower().endswith("colonized"):
                verb_base = "Colonize"
            elif verb_ed.lower().endswith("created"):
                verb_base = "Create"
            elif verb_ed.lower().endswith("discovered"):
                verb_base = "Discover"
            elif verb_ed.lower().endswith("invented"):
                verb_base = "Invent"
            elif verb_ed.lower().endswith("ruled"):
                verb_base = "Rule"
            elif verb_ed.lower().endswith("died"):
                verb_base = "Die"
            elif verb_ed.lower().endswith("ied"):
                verb_base = verb_ed[:-3].capitalize() + "y"
            elif verb_ed.lower().endswith("e"):
                verb_base = verb_ed[:-1].capitalize()
            else:
                verb_base = verb_ed[:-2].capitalize() if len(verb_ed) > 4 else verb_ed.capitalize()
            return f"Did {subj} {verb_base} {rest}?"

        # "woke up with" -> "Could Humans Have ..."
        if "woke up" in core.lower() or "health bar" in core.lower():
            return "Could Humans Survive With Floating Health Bars?"

        # Fallback to "Could ..."
        return f"Could {core}?"

    # Title Formulas Engine by Channel & Format
    if "Pulp" in channel:
        # PULP HYPOTHESES: Strict BAN on "What If" — All titles MUST be direct questions!
        pulp_q = convert_to_pulp_question(hook_question or clean_full_topic)
        pulp_q_short = re.sub(r'an industrial revolution', 'Factories', pulp_q.rstrip('?'), flags=re.IGNORECASE)
        
        if is_short:
            title_v1 = f"{pulp_q} 😱 #Shorts"
            title_v2 = f"Did {thumb_text or concept_title} Actually Happen? #Shorts"
            title_v3 = f"Could {concept_title} Be True? #Shorts"
        else:
            title_v1 = f"{pulp_q}"
            if named_concept and named_concept.lower() not in pulp_q.lower():
                if len(f"{named_concept}: {pulp_q}") <= 60:
                    title_v2 = f"{named_concept}: {pulp_q}"
                elif len(f"{named_concept}: {pulp_q_short}?") <= 60:
                    title_v2 = f"{named_concept}: {pulp_q_short}?"
                else:
                    title_v2 = f"{named_concept}: Did It Actually Happen?"
            else:
                title_v2 = f"Why Did {concept_title} Disappear?"
            title_v3 = f"{named_concept or concept_title}: The Hidden Truth" if named_concept else f"Could {concept_title} Actually Happen?"
            
    elif is_short:
        # Other Channels Shorts Formulas
        if hook_question:
            title_v1 = f"{hook_question} 😱 #Shorts"
            title_v2 = f"{concept_title}: The Hidden Truth #Shorts" if concept_title != hook_question.rstrip('?') else f"The Secret Behind {thumb_text or concept_title} #Shorts"
            title_v3 = f"Did {thumb_text or concept_title} Actually Happen? #Shorts"
        elif "Papercut" in channel:
            title_v1 = f"The {concept_title} Scandal 😱 #Shorts" if "monopoly" in concept_title.lower() or "scam" in concept_title.lower() else f"The Truth About {concept_title} #Shorts"
            title_v2 = f"Why {concept_title} Is Banned #Shorts" if "ban" in topic.lower() else f"How {concept_title} Works #Shorts"
            title_v3 = f"The Secret Behind {thumb_text or concept_title} #Shorts"
        elif "Pixel" in channel:
            title_v1 = f"The Shocking Truth About {concept_title} #Shorts"
            title_v2 = f"Why {concept_title} Failed #Shorts" if "fail" in topic.lower() or "disaster" in topic.lower() else f"The Secret Behind {concept_title} #Shorts"
            title_v3 = f"{thumb_text or concept_title} #Shorts"
        else:
            title_v1 = f"{primary_hook} 😱 #Shorts"
            title_v2 = f"The Truth About {concept_title} #Shorts"
            title_v3 = f"What If {thumb_text or concept_title}? #Shorts"
    else:
        # Other Channels Long-form Formulas
        if "Papercut" in channel:
            title_v1 = f"{clean_full_topic}"
            title_v2 = f"The Hidden Economics of {clean_full_topic}" if len(f"The Hidden Economics of {clean_full_topic}") <= 60 else f"Why {clean_full_topic} Exists"
            title_v3 = f"{clean_full_topic} — The Untold Story"
        elif "Pixel" in channel:
            title_v1 = f"{clean_full_topic}"
            title_v2 = f"{clean_full_topic} — The Untold Story"
            title_v3 = f"The Secret History of {thumb_text or clean_full_topic}"
        elif hook_question:
            title_v1 = f"{hook_question}"
            title_v2 = f"The Science of {thumb_text or best_story_beat}"
            title_v3 = f"{thumb_text or best_story_beat} — The Untold Story"
        else:
            title_v1 = f"What If {concept_title}?"
            title_v2 = f"{concept_title} — The Untold Story"
            title_v3 = f"The Hidden Truth of {concept_title} | {channel}"

    # Final safety clamp on title length without breaking words
    def clamp_title(t, max_len=60):
        t = re.sub(r'\bthe\s+the\b', 'The', t, flags=re.IGNORECASE)
        t = re.sub(r'\?+', '?', t)
        t = re.sub(r'\s*\?\s*😱', ' 😱', t)
        if len(t) <= max_len:
            return t
        has_shorts = "#Shorts" in t
        t_clean = t.replace(" #Shorts", "").strip()
        truncated = t_clean[:max_len - (8 if has_shorts else 0)].rsplit(' ', 1)[0].rstrip(" —–:-?,")
        if '?' in t and not truncated.endswith('?'):
            truncated += '?'
        if has_shorts:
            truncated += " #Shorts"
        return truncated

    title_v1 = clamp_title(title_v1, 60)
    title_v2 = clamp_title(title_v2, 60)
    title_v3 = clamp_title(title_v3, 60)

    # Calculate Timestamps from beats.json
    timestamps = []
    narration_lines = []
    current_time = 0.0

    for idx, beat in enumerate(beats):
        narration = beat.get("narration", "").strip()
        if narration:
            narration_lines.append(narration)

        beat_dur = beat.get("dur", 0)
        if not beat_dur:
            shots = beat.get("shots", [])
            beat_dur = sum([s.get("dur", 6) for s in shots]) if shots else 7

        beat_title = beat.get("title_en", "").strip()
        
        # Only add timestamps if it's Long-Form (not Short) and duration is valid
        if not is_short:
            if idx == 0:
                timestamps.append(f"00:00 — Intro: {beat_title if beat_title else first_title_en}")
            elif beat_title and (current_time - (float(timestamps[-1].split("—")[0].strip().replace(":", ".")) * 60 if ":" in timestamps[-1] else 0)) >= 15:
                # Ensure chapter length is at least 15-20s apart for YouTube chapters requirement
                timestamps.append(f"{format_time(current_time)} — {beat_title}")

        current_time += beat_dur

    full_summary = " ".join(narration_lines[:4]) if narration_lines else topic

    # Build Tags (Exact Match + Broad Match ≤ 480 chars)
    all_tags = list(base_tags)
    topic_keywords = [w.lower() for w in re.findall(r'\w+', topic_clean) if len(w) > 3]
    all_tags.extend(topic_keywords)
    all_tags.append(topic_clean.lower())
    
    seen = set()
    unique_tags = []
    for tag in all_tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)
            
    tags_string = ", ".join(unique_tags)
    if len(tags_string) > 480:
        tags_string = tags_string[:475].rsplit(',', 1)[0]

    # Format Timestamps Section (Only for Long-Form 16:9 >= 2 mins)
    timestamps_section = ""
    if not is_short and len(timestamps) >= 3:
        timestamps_section = "\n⏱️ CHAPTER TIMESTAMPS:\n" + "\n".join(timestamps) + "\n"
    elif not is_short:
        # Fallback if beats didn't have enough distinct titles
        timestamps_section = f"\n⏱️ CHAPTER TIMESTAMPS:\n00:00 — Intro: {first_title_en}\n01:00 — The Main Discovery\n02:30 — The Payoff & Impact\n"

    # Description Zone 1, 2, 3
    description_content = f"""{title_v1}

Like & Subscribe to {channel} for new episodes {schedule_text}! 🔔
Turn on notifications so you never miss an upload.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 STORY SUMMARY & CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{full_summary}{timestamps_section}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📢 CONNECT & SUBSCRIBE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{outro_cta}

{" ".join(hashtags_list[:8])}

© 2026 {channel} — All rights reserved."""

    # TikTok & Instagram Reels Caption Package
    tiktok_caption = f"""{title_v1} 🤯

{full_summary[:140]}...

What do you think? Comment below! 👇
{" ".join(hashtags_list[:5])} #fyp #viral #education"""

    # Pinned Comment Package
    pinned_comment = f"""👇 {comment_q.upper()}
Leave your thoughts below! We reply to top comments! 💬

🔗 Related Deep Dive Video: Check out the full episode on our channel tab!
Don't forget to Subscribe to {channel} (New episodes {schedule_days})! 🚀"""

    # Clean GitHub Markdown Formatting for youtube_seo.md
    markdown_output = f"""# 🎬 YouTube & Multi-Platform SEO Package — {channel}

> **Project:** `{project_id}`  
> **Format:** `{"Shorts (9:16)" if is_short else "Long-Form (16:9)"}`  
> **Schedule:** `{schedule_text}`  

---

## 📌 YouTube Title Options

1. **`{title_v1}`** ({len(title_v1)} chars) — *(Recommended for High CTR)*
2. **`{title_v2}`** ({len(title_v2)} chars) — *(Search Intent)*
3. **`{title_v3}`** ({len(title_v3)} chars) — *(Evergreen Documentary)*

---

## 📝 YouTube Description

```text
{description_content.strip()}
```

---

## 🏷️ YouTube Tags (Copy & paste into Studio Tags box)

```text
{tags_string}
```

---

## #️⃣ YouTube Hashtags

```text
{" ".join(hashtags_list[:8])}
```

---

## 📌 YouTube Pinned Comment

```text
{pinned_comment}
```

---

## 📱 TikTok & Instagram Reels Caption

```text
{tiktok_caption}
```
"""

    # Save to out/<project>/youtube_seo.md
    out_seo_path = os.path.join(project_dir, "youtube_seo.md")
    with open(out_seo_path, "w", encoding="utf-8") as f:
        f.write(markdown_output)

    print(markdown_output)
    print(f"✅ Saved clean Markdown metadata package to: {out_seo_path}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 metadata.py out/<project> [--channel <channel_name>]")
        sys.exit(1)
        
    project_directory = sys.argv[1]
    ch_name = None
    if len(sys.argv) >= 4 and sys.argv[2] == "--channel":
        ch_name = sys.argv[3]
        
    generate_seo_metadata(project_directory, ch_name)
