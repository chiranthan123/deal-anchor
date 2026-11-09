"""
generate_audio.py
Generates studio-quality neural AI voiceover using edge-tts.
"""

import asyncio
import edge_tts
import os

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio")
VOICE = "en-US-ChristopherNeural"  # Professional, authoritative, natural tech narrator

SCRIPTS = {
    "part1_intro.mp3": (
        "Hi everyone, I'm Chirantha. Today I'm demonstrating DealAnchor, an autonomous B2B client and deal memory co-pilot powered by Vectorize Hindsight."
    ),
    "part2_problem.mp3": (
        "In enterprise sales, closing high-value contracts takes weeks across multiple discovery calls. "
        "Along the way, clients share crucial boundary conditions: hard budget limits, negative experiences with competitors, and specific user preferences. "
        "Standard AI chatbots suffer from goldfish memory. When an account executive asks a generic AI to draft a proposal, "
        "it ignores prior conversations and quotes inflated enterprise tiers that the buyer explicitly rejected weeks ago."
    ),
    "part3_demo_proposal.mp3": (
        "Let's look at DealAnchor in action. Here we have a client called Apex Fleet Logistics. "
        "In Meeting 1, their VP of Operations stated a hard annual budget cap of fifteen thousand dollars, "
        "noting that their forty-five truck drivers need a dead-simple, one-tap mobile experience. "
        "In Meeting 2, they noted that Salesforce's mobile app had an intolerable six-second lag. "
        "Now, watch what happens when we generate a closing proposal comparison. "
        "On the left, notice how a generic stateless AI responds: it quotes thirty-two thousand dollars a year, "
        "more than double the customer's budget, and pushes complex dashboards that field drivers hate. "
        "On the right, DealAnchor uses Hindsight to recall Meeting 1 and Meeting 2 notes from weeks ago. "
        "It locks the price at fourteen thousand four hundred dollars flat, honoring their budget ceiling, "
        "emphasizes sub-second mobile confirmation, and directly addresses Salesforce's mobile slowness."
    ),
    "part4_demo_tabs.mp3": (
        "In the dashboard, we can inspect Hindsight's multi-meeting memory stream, "
        "retain new meeting takeaways after calls, and even run systemic reflections across fifty deals "
        "to discover recurring deal-breakers and improve sales win rates across our entire pipeline."
    ),
    "part5_architecture_outro.mp3": (
        "DealAnchor transforms stateless AI into an indispensable enterprise partner "
        "using Vectorize Hindsight's retain, recall, and reflect memory loop. "
        "The project is completely open source on GitHub. Thank you for watching."
    )
}

async def generate_all():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    print("Generating neural voiceover tracks with edge-tts...")
    for filename, text in SCRIPTS.items():
        out_path = os.path.join(AUDIO_DIR, filename)
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(out_path)
        print(f"Generated: {filename} ({len(text)} chars)")
    print("All voiceover tracks generated successfully!")

if __name__ == "__main__":
    asyncio.run(generate_all())
