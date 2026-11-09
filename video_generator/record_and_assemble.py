"""
record_and_assemble.py
Automated End-to-End Screen Director & Video Producer.
1. Starts the DealAnchor Streamlit application.
2. Automates Playwright Chromium with visible mouse movements & clicks.
3. Records slides, live UI proposal generation, and memory tabs in 1080p.
4. Muxes with neural AI voiceover into final MP4: deal_anchor_demo_1080p.mp4.
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

# Timings in seconds derived from neural voiceover tracks
TIMINGS = {
    "slide1": 11.0,
    "slide2": 31.5,
    "demo_proposal": 59.0,
    "demo_tabs": 15.5,
    "slide3_arch": 8.0,
    "slide4_outro": 7.5
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
        }, 400);
    };
})();
"""

async def smooth_move_and_click(page, element):
    box = await element.bounding_box()
    if box:
        target_x = box["x"] + box["width"] / 2
        target_y = box["y"] + box["height"] / 2
        await page.evaluate(f"window.moveVirtualCursor({target_x}, {target_y})")
        await asyncio.sleep(0.4)
        await page.evaluate("window.pulseCursor()")
        await element.click()
        await asyncio.sleep(0.5)

async def run_recording():
    RAW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Start Streamlit in background on port 8503
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

    # Wait for Streamlit to start
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

            # SCENE 1: Slide 1 (Intro)
            print("Recording Scene 1: Intro Slide...")
            slide1_url = f"file:///{SLIDES_DIR / 'slide1_intro.html'}"
            await page.goto(slide1_url)
            await asyncio.sleep(TIMINGS["slide1"])

            # SCENE 2: Slide 2 (The Problem)
            print("Recording Scene 2: The Problem...")
            slide2_url = f"file:///{SLIDES_DIR / 'slide2_problem.html'}"
            await page.goto(slide2_url)
            await asyncio.sleep(TIMINGS["slide2"])

            # SCENE 3: Live Application Demo (Proposal Generation)
            print("Recording Scene 3: Live UI Proposal Generation...")
            await page.goto("http://localhost:8503")
            await page.wait_for_load_state("networkidle")
            await page.evaluate(CURSOR_JS)
            await asyncio.sleep(2)

            # Move virtual cursor to title
            await page.evaluate("window.moveVirtualCursor(600, 160)")
            await asyncio.sleep(1)

            # Find and click "Generate Closing Proposal Comparison" button
            buttons = await page.query_selector_all("button")
            gen_btn = None
            for b in buttons:
                txt = await b.inner_text()
                if "Generate Closing Proposal" in txt:
                    gen_btn = b
                    break

            if gen_btn:
                print("Clicking Generate Closing Proposal Comparison button...")
                await smooth_move_and_click(page, gen_btn)
                await asyncio.sleep(1.5)

            # Smoothly scroll down to showcase the comparison
            print("Scrolling to highlight Generic AI vs DealAnchor...")
            await page.evaluate("window.moveVirtualCursor(500, 500)")
            for scroll_y in range(100, 650, 50):
                await page.evaluate(f"window.scrollTo({{ top: {scroll_y}, behavior: 'smooth' }});")
                await page.evaluate(f"window.moveVirtualCursor(500, {300 + scroll_y//3})")
                await asyncio.sleep(0.15)

            # Pause to let the voiceover explain the proposal contrast
            await asyncio.sleep(45)

            # SCENE 4: Memory Tabs & Systemic Reflection
            print("Recording Scene 4: Memory Stream & Reflection...")
            tabs = await page.query_selector_all("button[data-baseweb='tab']")
            if len(tabs) >= 4:
                # Tab 2: Multi-Meeting Memory Stream
                await smooth_move_and_click(page, tabs[1])
                await asyncio.sleep(5)

                # Tab 4: Win/Loss Pattern Reflection
                await smooth_move_and_click(page, tabs[3])
                await asyncio.sleep(1)

                # Click reflect button
                reflect_btns = await page.query_selector_all("button")
                for rb in reflect_btns:
                    t = await rb.inner_text()
                    if "Reflect on Deal Patterns" in t:
                        await smooth_move_and_click(page, rb)
                        break
                await asyncio.sleep(7)

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

    # 4. Find the recorded WebM file
    video_files = list(RAW_CLIPS_DIR.glob("*.webm"))
    if not video_files:
        print("[ERROR] No recorded video file found in raw_clips!")
        return
    raw_video = video_files[-1]
    print(f"Raw screen recording captured: {raw_video.name}")

    # 5. Merge all voiceover tracks with FFmpeg
    print("Concatenating audio tracks...")
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

    full_audio = BASE_DIR / "full_voiceover.mp3"
    subprocess.run([
        FFMPEG_EXE, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy", str(full_audio)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 6. Final Video Assembly: Mux Video + Audio into 1080p MP4
    final_output = OUTPUT_DIR / "deal_anchor_demo_1080p.mp4"
    print(f"Muxing and rendering final video: {final_output} ...")
    subprocess.run([
        FFMPEG_EXE, "-y",
        "-i", str(raw_video),
        "-i", str(full_audio),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_output)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if final_output.exists():
        size_mb = final_output.stat().st_size / (1024 * 1024)
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Professional Demo Video Created!")
        print(f"File Path: {final_output}")
        print(f"File Size: {size_mb:.2f} MB")
        print("Format: 1920x1080 Full HD with Neural AI Voiceover")
        print("=" * 60)
    else:
        print("[ERROR] Final video rendering failed.")

if __name__ == "__main__":
    asyncio.run(run_recording())
