"""
generate_elevenlabs_audio.py
Generates studio-grade AI narration using ElevenLabs API (Adam voice).
Precisely pronounces Chiranthan and Macrosoftware.
"""

import os
import requests

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
API_KEY = "sk_e07683ebeb1c0e9f2b41fa63eb087538d92d72ea706e428e"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # ElevenLabs Adam - deep, authoritative, natural

URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

SCRIPTS = {
    "part1_intro.mp3": (
        "Hi everyone, I am Chiranthan from team Macrosoftware. "
        "Today, I am proud to present DealAnchor, an autonomous B2B client and deal memory co-pilot built using Vectorize Hindsight."
    ),
    "part2_problem.mp3": (
        "In enterprise B2B sales, closing high-value deals takes weeks across multiple discovery meetings. "
        "Clients share critical boundary conditions: firm budget limits, negative experiences with competitors, and specific operational constraints. "
        "Standard AI chatbots suffer from goldfish memory. They treat every meeting like Day 1. "
        "When an account executive asks a generic AI to draft a contract proposal, "
        "it ignores past conversations and pitches inflated pricing that the buyer already rejected."
    ),
    "part3_demo_proposal.mp3": (
        "Let's look at DealAnchor in action. On the dashboard, we track active enterprise accounts like Apex Fleet Logistics. "
        "In Meeting 1, their VP of Operations stated a hard annual budget ceiling of fifteen thousand dollars, "
        "emphasizing that their forty-five truck drivers need a dead-simple, one-tap mobile interface. "
        "In Meeting 2, they noted that competitor Salesforce had an intolerable six-second mobile lag. "
        "Watch what happens when we click Generate Closing Proposal Comparison. "
        "On the left, generic stateless AI fails completely: it quotes thirty-two thousand dollars, more than double their budget, "
        "and pushes complex dashboards drivers hate. "
        "On the right, DealAnchor recalls every past meeting constraint from Hindsight. "
        "It locks the price at fourteen thousand four hundred dollars flat, under their ceiling, "
        "highlights sub-second mobile confirmation, and directly counters Salesforce's mobile slowness."
    ),
    "part4_demo_tabs.mp3": (
        "Now, let's explore the rest of the application. "
        "In the Multi-Meeting Memory Stream tab, we can inspect Hindsight's full chronological timeline of customer requirements and competitor objections. "
        "Next, in the Retain New Meeting Notes tab, our agent continuously learns. "
        "Watch as we enter notes from today's call: confirming the pilot kickoff for next Monday with quarterly billing. "
        "When we click Save into Hindsight Memory, the agent immediately commits this to persistent storage. "
        "Finally, in the Win-Loss Reflection tab, we trigger Hindsight's reflect capability. "
        "Instead of guessing, Hindsight audits patterns across our entire pipeline, "
        "revealing that exceeding initial meeting budgets causes an eighty percent drop in deal closing rates."
    ),
    "part5_architecture_outro.mp3": (
        "Under the hood, DealAnchor is powered by the Hindsight memory triad: "
        "Retaining meeting notes, Recalling contextual constraints, and Reflecting on systemic pipeline patterns. "
        "From team Macrosoftware, DealAnchor turns stateless chatbots into trusted enterprise partners. "
        "The codebase is fully open source on GitHub. Thank you for watching."
    )
}

def generate_audio():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    print("Generating ultra-realistic ElevenLabs voiceover tracks...")
    for filename, text in SCRIPTS.items():
        payload = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.85
            }
        }
        res = requests.post(URL, headers=HEADERS, json=payload)
        if res.status_code == 200:
            out_file = os.path.join(AUDIO_DIR, filename)
            with open(out_file, "wb") as f:
                f.write(res.content)
            print(f"✅ Generated {filename} ({len(res.content)} bytes)")
        else:
            print(f"❌ Error generating {filename}:", res.status_code, res.text)
            raise RuntimeError(f"ElevenLabs TTS failed for {filename}")

if __name__ == "__main__":
    generate_audio()
