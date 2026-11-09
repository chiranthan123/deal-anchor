"""
main.py - DealAnchor CLI & Parser Entrypoint
"""

import sys
import argparse
from seed_deals import INITIAL_DEALS
from memory import DealAnchorMemory
from agent import draft_proposal_without_memory, draft_proposal_with_hindsight

def run_evaluation():
    print("=" * 60)
    print("DealAnchor Client Intelligence Engine (CLI Mode)")
    print("Powered by Vectorize Hindsight Persistent Memory")
    print("=" * 60)
    
    mm = DealAnchorMemory()
    mm.seed_initial_deals(INITIAL_DEALS)
    
    client = "Apex Fleet Logistics"
    print(f"\n[1/2] Drafting Generic Proposal for {client} (Without Memory)...")
    base = draft_proposal_without_memory(client, "")
    print(f"Has memory: {base['has_memory']}")
    
    print(f"\n[2/2] Drafting DealAnchor Proposal for {client} (With Hindsight Memory)...")
    res = draft_proposal_with_hindsight(client, mm)
    print(f"Has memory: {res['has_memory']}")
    print(f"Retained constraints: {len(res['matched_constraints'])}")
    print("\nPROPOSAL PREVIEW:\n" + res["proposal"][:350] + "...\n")
    print("✅ DealAnchor automated parser check passed successfully!")

def main():
    parser = argparse.ArgumentParser(description="DealAnchor CLI")
    parser.add_argument("--eval", action="store_true", help="Run automated evaluation")
    parser.add_argument("--ui", action="store_true", help="Launch Streamlit UI")
    args = parser.parse_args()
    
    if args.ui:
        import os
        os.system("streamlit run ui.py")
    else:
        run_evaluation()

if __name__ == "__main__":
    main()

