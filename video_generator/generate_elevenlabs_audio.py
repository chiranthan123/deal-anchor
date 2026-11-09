"""
generate_elevenlabs_audio.py
Generates 6 modular audio tracks using ElevenLabs.
Tries the requested voice (Mark: UgBBYS2sOqTuMpoF3BR0), with automatic fallback
to Chris (iP95p4xoKVk53GoZ742B - Natural Conversational) if the free tier restricts library voices.
"""

import os
import requests
import json

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
API_KEY = "sk_e07683ebeb1c0e9f2b41fa63eb087538d92d72ea706e428e"

PRIMARY_VOICE_ID = "UgBBYS2sOqTuMpoF3BR0"   # Mark (Requested)
FALLBACK_VOICE_ID = "iP95p4xoKVk53GoZ742B"  # Chris (Natural Conversational American Male)

HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

SCENES = {
    "scene1_intro.mp3": (
        "Hi everyone, I am Chiranthan from team Macrosoftware. "
        "Today, I am proud to present DealAnchor, an autonomous B2B client and deal memory co-pilot built using Vectorize Hindsight."
    ),
    "scene2_problem.mp3": (
        "In enterprise B2B sales, closing high-value deals takes weeks across multiple discovery meetings. "
        "Clients share critical boundary conditions: firm budget limits, negative experiences with competitors, and specific operational constraints. "
        "Standard AI chatbots suffer from goldfish memory. They treat every meeting like Day 1. "
        "When an account executive asks a generic AI to draft a contract proposal, "
        "it ignores past conversations and pitches inflated pricing that the buyer already rejected."
    ),
    "scene3_demo_proposal.mp3": (
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
    "scene4_demo_tabs.mp3": (
        "Now, let's explore the rest of the application. "
        "In the Multi-Meeting Memory Stream tab, we can inspect Hindsight's full chronological timeline of customer requirements and competitor objections. "
        "Next, in the Retain New Meeting Notes tab, our agent continuously learns. "
        "Watch as we enter notes from today's call: confirming the pilot kickoff for next Monday with quarterly billing. "
        "When we click Save into Hindsight Memory, the agent immediately commits this to persistent storage. "
        "Finally, in the Win-Loss Reflection tab, we trigger Hindsight's reflect capability. "
        "Instead of guessing, Hindsight audits patterns across our entire pipeline, "
        "revealing that exceeding initial meeting budgets causes an eighty percent drop in deal closing rates."
    ),
    "scene5_architecture.mp3": (
        "Under the hood, DealAnchor is powered by the Hindsight cognitive memory triad: "
        "Retaining atomic meeting notes, Recalling contextual constraints before drafting, "
        "and Reflecting on systemic pipeline patterns across all customer interactions."
    ),
    "scene6_conclusion.mp3": (
        "From team Macrosoftware, DealAnchor turns stateless chatbots into trusted enterprise partners. "
        "The codebase is fully open source on GitHub. Thank you for watching."
    )
}

def generate_voice(text, filename, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.85
        }
    }
    return requests.post(url, headers=HEADERS, json=payload)

def generate_all_scenes():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    # Test primary voice
    test_res = generate_voice("Test", "test.mp3", PRIMARY_VOICE_ID)
    if test_res.status_code == 200:
        active_voice = PRIMARY_VOICE_ID
        voice_name = "Mark (UgBBYS2sOqTuMpoF3BR0)"
    else:
        active_voice = FALLBACK_VOICE_ID
        voice_name = "Chris (iP95p4xoKVk53GoZ742B - Conversational)"
        print(f"[NOTE] Primary voice returned {test_res.status_code} ({test_res.text[:80]}). Using natural voice: {voice_name}")

    print(f"Generating 6 scenes using ElevenLabs Voice: {voice_name}...")
    for filename, text in SCENES.items():
        res = generate_voice(text, filename, active_voice)
        if res.status_code == 200:
            out_path = os.path.join(AUDIO_DIR, filename)
            with open(out_path, "wb") as f:
                f.write(res.content)
            print(f"✅ Generated {filename} ({len(res.content)} bytes)")
        else:
            raise RuntimeError(f"ElevenLabs TTS failed for {filename}: {res.status_code} {res.text}")

if __name__ == "__main__":
    generate_all_scenes()
