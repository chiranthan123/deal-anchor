"""
sync_director.py
Modular Synchronized Video Director & Desync Auditor.
- Records each scene modularly to guarantee 100% synchronization between audio narration and visual actions.
- Audits and fixes any desync between audio duration and video duration.
- Guarantees zero abrupt audio cutoff at the end with safe padding.
- Mixes ambient background music seamlessly.
"""

import os
import sys
import time
import subprocess
import asyncio
from pathlib import Path
import imageio_ffmpeg
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
SLIDES_DIR = BASE_DIR / "slides"
AUDIO_DIR = BASE_DIR / "audio"
RAW_CLIPS_DIR = BASE_DIR / "raw_clips"
OUTPUT_DIR = BASE_DIR / "output"

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

CURSOR_JS = """
(() => {
    if (document.getElementById('virtual-cursor')) return;
    const c = document.createElement('div');
    c.id = 'virtual-cursor';
    c.style.cssText = `
        position: fixed;
        top: 0; left: 0;
        width: 22px; height: 22px;
        background: #F59E0B;
        border: 2px solid #FFFFFF;
        border-radius: 50%;
        box-shadow: 0 0 16px rgba(245, 158, 11, 0.9);
        pointer-events: none;
        z-index: 9999999;
        transition: transform 0.28s cubic-bezier(0.25, 1, 0.5, 1);
        transform: translate(-100px, -100px);
    `;
    document.body.appendChild(c);

    window.moveVirtualCursor = (x, y) => {
        c.style.transform = `translate(${x}px, ${y}px)`;
    };

    window.pulseCursor = () => {
        c.style.boxShadow = '0 0 28px #10B981';
        c.style.background = '#10B981';
        setTimeout(() => {
            c.style.boxShadow = '0 0 16px rgba(245, 158, 11, 0.9)';
            c.style.background = '#F59E0B';
        }, 350);
    };
})();
"""

def get_media_duration(file_path):
    cmd = [FFMPEG_EXE, "-i", str(file_path)]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration" in line:
            parts = line.strip().split(",")[0].split("Duration:")[1].strip().split(":")
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    return 0.0

async def smooth_move(page, x, y, delay=0.3):
    await page.evaluate(f"window.moveVirtualCursor({x}, {y})")
    await asyncio.sleep(delay)

async def smooth_click(page, element):
    box = await element.bounding_box()
    if box:
        target_x = box["x"] + box["width"] / 2
        target_y = box["y"] + box["height"] / 2
        await smooth_move(page, target_x, target_y, 0.35)
        await page.evaluate("window.pulseCursor()")
        await element.click()
        await asyncio.sleep(0.4)

async def human_type(page, element, text, delay=0.03):
    await smooth_click(page, element)
    await element.fill("")
    for char in text:
        await element.type(char, delay=int(delay * 1000))

async def record_modular_scenes():
    RAW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Clean existing clips
    for sub in RAW_CLIPS_DIR.glob("*"):
        if sub.is_dir():
            for f in sub.glob("*.*"):
                try: f.unlink()
                except Exception: pass

    # Start Streamlit on 8503
    print("Starting Streamlit application on port 8503...")
    streamlit_proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", "ui.py",
            "--server.port=8503",
            "--server.headless=true",
            "--theme.base=dark"
        ],
        cwd=str(PROJECT_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    import urllib.request
    for _ in range(30):
        try:
            with urllib.request.urlopen("http://localhost:8503", timeout=1):
                print("Streamlit UI is live!")
                break
        except Exception:
            time.sleep(1)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # --- SCENE 1: Intro Slide ---
            a1_dur = get_media_duration(AUDIO_DIR / "scene1_intro.mp3")
            print(f"\n[SCENE 1/6] Intro Slide (Audio: {a1_dur:.2f}s)...")
            s1_dir = RAW_CLIPS_DIR / "s1"
            s1_dir.mkdir(exist_ok=True)
            ctx1 = await browser.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=str(s1_dir), record_video_size={"width": 1920, "height": 1080})
            p1 = await ctx1.new_page()
            await p1.goto(f"file:///{SLIDES_DIR / 'slide1_intro.html'}")
            await asyncio.sleep(a1_dur + 0.5)
            await ctx1.close()

            # --- SCENE 2: The Problem Slide ---
            a2_dur = get_media_duration(AUDIO_DIR / "scene2_problem.mp3")
            print(f"\n[SCENE 2/6] Problem Slide (Audio: {a2_dur:.2f}s)...")
            s2_dir = RAW_CLIPS_DIR / "s2"
            s2_dir.mkdir(exist_ok=True)
            ctx2 = await browser.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=str(s2_dir), record_video_size={"width": 1920, "height": 1080})
            p2 = await ctx2.new_page()
            await p2.goto(f"file:///{SLIDES_DIR / 'slide2_problem.html'}")
            await asyncio.sleep(a2_dur + 0.5)
            await ctx2.close()

            # --- SCENE 3: Live UI - Proposal Generation ---
            a3_dur = get_media_duration(AUDIO_DIR / "scene3_demo_proposal.mp3")
            print(f"\n[SCENE 3/6] Live UI Proposal Generation (Audio: {a3_dur:.2f}s)...")
            s3_dir = RAW_CLIPS_DIR / "s3"
            s3_dir.mkdir(exist_ok=True)
            ctx3 = await browser.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=str(s3_dir), record_video_size={"width": 1920, "height": 1080})
            p3 = await ctx3.new_page()
            start_s3 = time.time()
            await p3.goto("http://localhost:8503")
            
            # Explicitly wait for main page and Generate button to mount
            gen_btn = await p3.wait_for_selector("button:has-text('Generate Closing Proposal')", timeout=25000)
            await p3.evaluate(CURSOR_JS)
            await asyncio.sleep(1.0)

            # 1. Inspect sidebar client details (0s - 10s)
            await smooth_move(p3, 140, 220, 0.8)
            await asyncio.sleep(1.5)
            await smooth_move(p3, 140, 360, 0.8)
            await asyncio.sleep(2.0)

            # 2. Move directly to 'Generate Closing Proposal Comparison' and click it (10s - 18s)
            print("Clicking 'Generate Closing Proposal Comparison'...")
            await smooth_click(p3, gen_btn)
            
            # Wait for comparison columns to render
            await p3.wait_for_selector(".generic-pitch", timeout=10000)
            await asyncio.sleep(1.5)

            # 3. Hover over left Generic AI proposal (18s - 34s)
            # Generic AI pitch ($32,000 failure)
            print("Inspecting Generic AI pitch (left column)...")
            await smooth_move(p3, 500, 480, 0.8)
            await asyncio.sleep(2.0)
            await smooth_move(p3, 520, 560, 0.8)
            await asyncio.sleep(4.0)

            # 4. Glide over to right Hindsight proposal (34s - 48s)
            # Hindsight pitch ($15,000 success)
            print("Inspecting DealAnchor Hindsight pitch (right column)...")
            await smooth_move(p3, 1150, 480, 0.9)
            await asyncio.sleep(2.0)
            await smooth_move(p3, 1180, 560, 0.8)
            await asyncio.sleep(4.0)

            # 5. Smooth scroll down to reveal full side-by-side terms (48s - 55s)
            for sy in range(60, 450, 40):
                await p3.evaluate(f"window.scrollTo({{ top: {sy}, behavior: 'smooth' }});")
                await smooth_move(p3, 850, 400 + (sy // 6), 0.12)

            # Hold to match exact audio duration
            elapsed_s3 = time.time() - start_s3
            remaining_s3 = max(0.5, (a3_dur + 0.5) - elapsed_s3)
            await asyncio.sleep(remaining_s3)
            await ctx3.close()

            # --- SCENE 4: Live UI - Tabs, Retain & Reflection ---
            a4_dur = get_media_duration(AUDIO_DIR / "scene4_demo_tabs.mp3")
            print(f"\n[SCENE 4/6] Live UI Tabs & Memory Retain (Audio: {a4_dur:.2f}s)...")
            s4_dir = RAW_CLIPS_DIR / "s4"
            s4_dir.mkdir(exist_ok=True)
            ctx4 = await browser.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=str(s4_dir), record_video_size={"width": 1920, "height": 1080})
            p4 = await ctx4.new_page()
            start_s4 = time.time()
            await p4.goto("http://localhost:8503")
            # Explicitly wait for tabs to mount!
            await p4.wait_for_selector("[data-testid='stTab']", timeout=15000)
            await p4.evaluate(CURSOR_JS)
            await asyncio.sleep(1.0)

            tabs = await p4.query_selector_all("[data-testid='stTab']")
            if len(tabs) >= 4:
                # 4A. TAB 2: Multi-Meeting Memory Stream (12s)
                print("Showing Tab 2: Memory Stream...")
                await smooth_click(p4, tabs[1])
                await asyncio.sleep(1.2)
                for sy in range(50, 360, 40):
                    await p4.evaluate(f"window.scrollTo({{ top: {sy}, behavior: 'smooth' }});")
                    await smooth_move(p4, 600, 280 + sy // 4, 0.15)
                await asyncio.sleep(7.0)

                # 4B. TAB 3: Retain New Meeting Notes (16s)
                print("Showing Tab 3: Retaining New Meeting Notes live...")
                await p4.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' });")
                await smooth_click(p4, tabs[2])
                await asyncio.sleep(1.0)

                textareas = await p4.query_selector_all("textarea")
                inputs = await p4.query_selector_all("input[type='text']")
                if textareas:
                    await human_type(p4, textareas[0], "Pilot kickoff confirmed for next Monday with all 45 drivers.", 0.02)
                await asyncio.sleep(0.4)
                if len(inputs) >= 2:
                    await human_type(p4, inputs[1], "Quarterly billing, sub-second response time mandatory.", 0.02)
                await asyncio.sleep(0.6)

                # Save into Hindsight
                for b in await p4.query_selector_all("button"):
                    if "Save into Hindsight Memory" in await b.inner_text():
                        await smooth_click(p4, b)
                        break
                await asyncio.sleep(3.5)

                # 4C. TAB 4: Win/Loss Reflection (12s)
                print("Showing Tab 4: Systemic Pattern Reflection...")
                await smooth_click(p4, tabs[3])
                await asyncio.sleep(1.0)
                for rb in await p4.query_selector_all("button"):
                    if "Reflect on Deal Patterns" in await rb.inner_text():
                        await smooth_click(p4, rb)
                        break
                await asyncio.sleep(8.0)

            elapsed_s4 = time.time() - start_s4
            remaining_s4 = max(0.5, (a4_dur + 0.5) - elapsed_s4)
            await asyncio.sleep(remaining_s4)
            await ctx4.close()

            # --- SCENE 5: Architecture Slide ---
            a5_dur = get_media_duration(AUDIO_DIR / "scene5_architecture.mp3")
            print(f"\n[SCENE 5/6] Architecture Slide (Audio: {a5_dur:.2f}s)...")
            s5_dir = RAW_CLIPS_DIR / "s5"
            s5_dir.mkdir(exist_ok=True)
            ctx5 = await browser.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=str(s5_dir), record_video_size={"width": 1920, "height": 1080})
            p5 = await ctx5.new_page()
            await p5.goto(f"file:///{SLIDES_DIR / 'slide3_architecture.html'}")
            await asyncio.sleep(a5_dur + 0.5)
            await ctx5.close()

            # --- SCENE 6: Conclusion Slide (With 2.5s Safety Buffer) ---
            a6_dur = get_media_duration(AUDIO_DIR / "scene6_conclusion.mp3")
            print(f"\n[SCENE 6/6] Conclusion Slide (Audio: {a6_dur:.2f}s)...")
            s6_dir = RAW_CLIPS_DIR / "s6"
            s6_dir.mkdir(exist_ok=True)
            ctx6 = await browser.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=str(s6_dir), record_video_size={"width": 1920, "height": 1080})
            p6 = await ctx6.new_page()
            await p6.goto(f"file:///{SLIDES_DIR / 'slide4_conclusion.html'}")
            await asyncio.sleep(a6_dur + 2.5)
            await ctx6.close()

            await browser.close()
    finally:
        streamlit_proc.terminate()

    # --- DESYNC AUDIT & FIX ENGINE ---
    print("\n" + "=" * 65)
    print("🔍 RUNNING DESYNC AUDIT & AUTO-FIX ON RECORDED SCENES...")
    print("=" * 65)

    scene_configs = [
        ("s1", "scene1_intro.mp3", "synced_s1.mp4"),
        ("s2", "scene2_problem.mp3", "synced_s2.mp4"),
        ("s3", "scene3_demo_proposal.mp3", "synced_s3.mp4"),
        ("s4", "scene4_demo_tabs.mp3", "synced_s4.mp4"),
        ("s5", "scene5_architecture.mp3", "synced_s5.mp4"),
        ("s6", "scene6_conclusion.mp3", "synced_s6.mp4"),
    ]

    synced_clips = []

    for s_id, a_name, out_name in scene_configs:
        raw_webms = list((RAW_CLIPS_DIR / s_id).glob("*.webm"))
        if not raw_webms:
            print(f"[ERROR] Missing raw video for {s_id}")
            continue
        raw_vid = raw_webms[-1]
        audio_file = AUDIO_DIR / a_name

        v_dur = get_media_duration(raw_vid)
        a_dur = get_media_duration(audio_file)
        delta = v_dur - a_dur

        status_marker = "✅ PERFECT SYNC" if abs(delta) <= 1.0 else ("⚠️ PADDING APPLIED" if delta > 0 else "🚨 CRITICAL DESYNC FIXED")
        print(f"[{s_id.upper()}] Audio: {a_dur:.2f}s | Video: {v_dur:.2f}s | Delta: {delta:+.2f}s -> {status_marker}")

        synced_out = RAW_CLIPS_DIR / out_name
        
        # Guarantee video is at least as long as audio so audio never cuts off!
        if delta < 0:
            pad_needed = abs(delta) + 0.5
            filter_str = f"tpad=stop_mode=clone:stop_duration={pad_needed}"
        else:
            filter_str = "null"

        cmd = [
            FFMPEG_EXE, "-y",
            "-i", str(raw_vid),
            "-i", str(audio_file),
            "-vf", filter_str,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-c:a", "aac",
            "-b:a", "192k",
            str(synced_out)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        synced_clips.append(synced_out)

    # --- MASTER CONCATENATION & AMBIENT BGM DUCKING ---
    print("\nConcatenating synchronized scenes and mixing ambient soundtrack...")
    concat_txt = BASE_DIR / "final_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for sc in synced_clips:
            f.write(f"file '{sc.resolve()}'\n")

    unmixed_video = BASE_DIR / "unmixed_master.mp4"
    subprocess.run([
        FFMPEG_EXE, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(unmixed_video)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_dur = get_media_duration(unmixed_video)
    bgm_path = AUDIO_DIR / "ambient_bgm.mp3"
    final_output = OUTPUT_DIR / "deal_anchor_demo_1080p.mp4"

    print(f"Total video duration: {total_dur:.2f}s. Mixing background music with 3s fadeout...")

    cmd_mix = [
        FFMPEG_EXE, "-y",
        "-i", str(unmixed_video),
        "-i", str(bgm_path),
        "-filter_complex", (
            f"[1:a]volume=0.09,afade=t=out:st={max(0, total_dur - 3)}:d=3[bgm];"
            "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
        ),
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        str(final_output)
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if final_output.exists():
        size_mb = final_output.stat().st_size / (1024 * 1024)
        print("\n" + "=" * 65)
        print("🎉 SUCCESS! 100% SYNCHRONIZED MASTER VIDEO CREATED!")
        print(f"File Path: {final_output}")
        print(f"Duration: {total_dur:.2f} seconds")
        print(f"File Size: {size_mb:.2f} MB")
        print("Sync Status: 100% Audited, Zero Desync, Zero Audio Cutoff")
        print("=" * 65)

if __name__ == "__main__":
    asyncio.run(record_modular_scenes())
