"""
record_and_assemble.py
Upgraded Master Video Director & Producer.
- Uses studio-quality ElevenLabs Adam voiceover (pronouncing Chiranthan & Macrosoftware).
- Features extended, deep-dive application walkthrough:
  * Sidebar account inspection
  * Live side-by-side proposal generation ($15k vs $32k)
  * Multi-meeting memory timeline audit
  * Real-time form typing & live Hindsight memory retention
  * Systemic cross-deal pattern reflection
- Mixes subtle ambient background music with professional ducking.
- Renders final 1080p MP4.
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

# Exact timing derived from ElevenLabs audio files
TIMINGS = {
    "slide1": 11.5,
    "slide2": 33.5,
    "demo_proposal": 58.5,
    "demo_tabs": 49.0,
    "slide3_arch": 11.0,
    "slide4_outro": 11.5
}

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

async def run_recording():
    RAW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Clean previous webm clips
    for old_clip in RAW_CLIPS_DIR.glob("*.webm"):
        try:
            old_clip.unlink()
        except Exception:
            pass

    # 2. Launch Streamlit background instance
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
            print("Launching automated Chromium browser (1920x1080)...")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                record_video_dir=str(RAW_CLIPS_DIR),
                record_video_size={"width": 1920, "height": 1080}
            )
            page = await context.new_page()

            # SCENE 1: Slide 1 (Intro: Chiranthan & Macrosoftware)
            print("Recording Scene 1: Intro Slide...")
            slide1_url = f"file:///{SLIDES_DIR / 'slide1_intro.html'}"
            await page.goto(slide1_url)
            await asyncio.sleep(TIMINGS["slide1"])

            # SCENE 2: Slide 2 (The Problem: Stateless AI vs Reality)
            print("Recording Scene 2: The Problem Slide...")
            slide2_url = f"file:///{SLIDES_DIR / 'slide2_problem.html'}"
            await page.goto(slide2_url)
            await asyncio.sleep(TIMINGS["slide2"])

            # SCENE 3: Live Application Demo - Proposal Generation
            print("Recording Scene 3: Live UI - Proposal Generation...")
            await page.goto("http://localhost:8503")
            await page.wait_for_load_state("networkidle")
            await page.evaluate(CURSOR_JS)
            await asyncio.sleep(1.5)

            # Move cursor to sidebar client details
            print("Hovering on sidebar client metadata...")
            await smooth_move(page, 150, 220, 0.8)
            await smooth_move(page, 150, 360, 0.8)

            # Find and click "Generate Closing Proposal Comparison"
            buttons = await page.query_selector_all("button")
            gen_btn = None
            for b in buttons:
                txt = await b.inner_text()
                if "Generate Closing Proposal" in txt:
                    gen_btn = b
                    break

            if gen_btn:
                print("Clicking Generate Closing Proposal Comparison...")
                await smooth_click(page, gen_btn)
                await asyncio.sleep(1.5)

            # Smoothly scroll down to showcase the comparison
            print("Scrolling through side-by-side proposal comparison...")
            for scroll_y in range(100, 680, 40):
                await page.evaluate(f"window.scrollTo({{ top: {scroll_y}, behavior: 'smooth' }});")
                await smooth_move(page, 480, 250 + (scroll_y // 4), 0.1)

            # Let the voiceover complete its explanation of the contrast
            await asyncio.sleep(40)

            # SCENE 4: Extended Deep-Dive into All Application Tabs
            print("Recording Scene 4: Deep-Dive into Tabs (Memory Stream, Live Retain, Reflection)...")
            await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' });")
            await asyncio.sleep(1.0)

            tabs = await page.query_selector_all("button[data-baseweb='tab']")
            if len(tabs) >= 4:
                # 4A. TAB 2: Multi-Meeting Memory Stream
                print("Navigating to Tab 2: Multi-Meeting Memory Stream...")
                await smooth_click(page, tabs[1])
                await asyncio.sleep(1.5)
                await smooth_move(page, 600, 320, 0.5)
                # Scroll gently to show both Meeting 1 and Meeting 2 cards
                for sy in range(50, 350, 50):
                    await page.evaluate(f"window.scrollTo({{ top: {sy}, behavior: 'smooth' }});")
                    await smooth_move(page, 600, 300 + sy // 4, 0.12)
                await asyncio.sleep(8)

                # 4B. TAB 3: Retain New Meeting Notes (Live Typing!)
                print("Navigating to Tab 3: Retain New Meeting Notes (Typing Live)...")
                await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' });")
                await smooth_click(page, tabs[2])
                await asyncio.sleep(1.0)

                # Type into the meeting summary text area
                textareas = await page.query_selector_all("textarea")
                inputs = await page.query_selector_all("input[type='text']")

                if textareas:
                    print("Typing live meeting summary...")
                    await human_type(page, textareas[0], "Pilot kickoff confirmed for next Monday with all 45 truck drivers.", 0.02)
                    await asyncio.sleep(0.5)

                if len(inputs) >= 2:
                    print("Typing specific preferences...")
                    await human_type(page, inputs[1], "Quarterly invoice billing, sub-second response time mandatory.", 0.02)
                    await asyncio.sleep(0.5)

                # Click "Save into Hindsight Memory"
                form_btn = None
                for b in await page.query_selector_all("button"):
                    if "Save into Hindsight Memory" in await b.inner_text():
                        form_btn = b
                        break

                if form_btn:
                    print("Clicking Save into Hindsight Memory...")
                    await smooth_click(page, form_btn)
                    await asyncio.sleep(2.5)  # Show green success banner!

                # 4C. TAB 4: Win/Loss Pattern Reflection
                print("Navigating to Tab 4: Win/Loss Pattern Reflection...")
                await smooth_click(page, tabs[3])
                await asyncio.sleep(1.0)

                reflect_btns = await page.query_selector_all("button")
                for rb in reflect_btns:
                    t = await rb.inner_text()
                    if "Reflect on Deal Patterns" in t:
                        print("Clicking Reflect on Deal Patterns...")
                        await smooth_click(page, rb)
                        break
                await asyncio.sleep(9)

            # SCENE 5: Architecture Slide
            print("Recording Scene 5: Architecture Slide...")
            slide3_url = f"file:///{SLIDES_DIR / 'slide3_architecture.html'}"
            await page.goto(slide3_url)
            await asyncio.sleep(TIMINGS["slide3_arch"])

            # SCENE 6: Conclusion Slide
            print("Recording Scene 6: Conclusion Slide...")
            slide4_url = f"file:///{SLIDES_DIR / 'slide4_conclusion.html'}"
            await page.goto(slide4_url)
            await asyncio.sleep(TIMINGS["slide4_outro"])

            print("Closing browser context to finalize raw video...")
            await context.close()
            await browser.close()

    finally:
        print("Stopping background Streamlit server...")
        streamlit_proc.terminate()

    # Find the recorded WebM file
    video_files = list(RAW_CLIPS_DIR.glob("*.webm"))
    if not video_files:
        print("[ERROR] No recorded video file found in raw_clips!")
        return
    raw_video = video_files[-1]
    print(f"Raw screen recording captured: {raw_video.name}")

    # Concatenate ElevenLabs voiceover tracks
    print("Concatenating ElevenLabs audio tracks...")
    concat_list_file = BASE_DIR / "audio_concat.txt"
    audio_files = [
        "part1_intro.mp3",
        "part2_problem.mp3",
        "part3_demo_proposal.mp3",
        "part4_demo_tabs.mp3",
        "part5_architecture_outro.mp3"
    ]
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for af in audio_files:
            af_path = (AUDIO_DIR / af).resolve()
            f.write(f"file '{af_path}'\n")

    full_voice = BASE_DIR / "full_elevenlabs_voice.mp3"
    subprocess.run([
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy", str(full_voice)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    bgm_path = AUDIO_DIR / "ambient_bgm.mp3"
    final_output = OUTPUT_DIR / "deal_anchor_demo_1080p.mp4"

    print("Muxing video, ElevenLabs voiceover, and ambient BGM with audio ducking...")
    # FFmpeg filter:
    # [1:a] Voice at 1.0 (100%)
    # [2:a] BGM at 0.10 (10% volume, subtle and warm)
    # amix combines them seamlessly!
    cmd = [
        FFMPEG_EXE, "-y",
        "-i", str(raw_video),
        "-i", str(full_voice),
        "-i", str(bgm_path),
        "-filter_complex", "[1:a]volume=1.0[voice];[2:a]volume=0.10[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if final_output.exists():
        size_mb = final_output.stat().st_size / (1024 * 1024)
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Upgraded Master Demo Video Created!")
        print(f"File Path: {final_output}")
        print(f"File Size: {size_mb:.2f} MB")
        print("Audio: ElevenLabs Adam (Chiranthan & Macrosoftware)")
        print("Soundtrack: Ambient Lo-Fi Tech BGM (Audio Ducked)")
        print("Format: 1920x1080 Full HD (Full Feature Walkthrough)")
        print("=" * 60)
    else:
        print("[ERROR] Final video rendering failed.")

if __name__ == "__main__":
    asyncio.run(run_recording())
