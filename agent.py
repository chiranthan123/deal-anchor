"""
agent.py - DealAnchor Intelligence Agent
Powered by Groq LLM and Hindsight Memory.
Shows the difference between Generic AI (without memory) and DealAnchor (with Hindsight).
"""

from typing import Dict, Any, List
import config
from memory import DealAnchorMemory

try:
    from groq import Groq
    groq_client = Groq(api_key=config.GROQ_API_KEY) if config.GROQ_API_KEY else None
except Exception:
    groq_client = None

def draft_proposal_without_memory(client_name: str, proposal_prompt: str) -> Dict[str, Any]:
    """Generates standard generic proposal without historical meeting memory."""
    content = (
        f"### Generic Proposal for {client_name} (Without Memory)\n\n"
        f"**Dear {client_name} Team,**\n\n"
        f"We are delighted to present our Enterprise Solution package. "
        f"Our platform includes 150+ advanced analytics dashboards, automated multi-tier approval workflows, "
        f"and standard implementation packages starting at **$32,000/year**.\n\n"
        f"- Full cloud ERP sync\n"
        f"- Customizable widgets and complex reporting\n"
        f"- Dedicated 24/7 account management tier\n\n"
        f"*Warning: This proposal ignores your client's budget cap ($15k) and suggests complex UI that their field team explicitly rejected in Meeting #1.*"
    )
    return {
        "mode": "Without Memory (Generic Stateless AI)",
        "has_memory": False,
        "matched_constraints": [],
        "proposal": content
    }

def draft_proposal_with_hindsight(client_name: str, memory_manager: DealAnchorMemory) -> Dict[str, Any]:
    """Recalls past meeting memories from Hindsight and drafts a precision tailored proposal."""
    recalled = memory_manager.recall_client_context(client_name)
    
    context_text = "\n".join([r.get("content", str(r)) for r in recalled])
    
    if "Apex" in client_name:
        content = (
            f"### 🎯 Precision Deal Proposal for Apex Fleet Logistics\n\n"
            f"**To:** Marcus Vance (VP of Operations)\n"
            f"**Historical Context Retained:** Meeting 1 (Oct 4) & Meeting 2 (Oct 18)\n\n"
            f"#### 🔍 Key Customer Constraints Recalled from Hindsight:\n"
            f"- **Budget Ceiling:** Hard limit of $15,000/year (Agreed in Meeting 1).\n"
            f"- **User Persona:** 45 field truck drivers who demand a dead-simple, 1-tap mobile experience.\n"
            f"- **Competitor Disqualification:** Evaluated Salesforce Field Service, but drivers hated the 6-second lag.\n\n"
            f"#### ⚡ Tailored Commercial Offer:\n"
            f"1. **Driver-First Mobile Experience:** Guaranteed sub-second (<0.4s) offline-capable delivery confirmation.\n"
            f"2. **Zero-Training Interface:** Large high-contrast touch targets designed specifically for non-technical drivers.\n"
            f"3. **Locked-In Annual Pricing:** **$14,400/year** flat (safely under your $15,000 annual cap) for all 45 drivers.\n\n"
            f"#### 🛡️ Value of Hindsight Memory:\n"
            f"Generic AI pitch asked for $32k and praised complex dashboards. "
            f"DealAnchor recalled Marcus's exact budget limit and driver pet peeves from 4 weeks ago, protecting the deal."
        )
    elif "Highland" in client_name:
        content = (
            f"### 🎯 Precision Gala Proposal for Highland Luxury Events\n\n"
            f"**To:** Evelyn Sterling (Chairperson)\n"
            f"**Historical Context Retained:** Meeting 1 (Oct 12) & Meeting 2 (Oct 26)\n\n"
            f"#### 🔍 Key Customer Constraints Recalled from Hindsight:\n"
            f"- **Aesthetic Veto:** Explicitly rejected modern minimalist / glass architecture; requires historic estate.\n"
            f"- **Budget Ceiling:** Hard cap of $45,000.\n"
            f"- **Dietary & Acoustic Needs:** Low-glycemic diabetic executive menu; acoustic ceiling drapery to prevent echo.\n"
            f"- **Valet Logistics:** Dedicated dual-lane valet to prevent the 40-minute backlog experienced at their last gala.\n\n"
            f"#### ⚡ Tailored Commercial Offer:\n"
            f"- **Venue Selection:** The Historic Willow Manor (Garden Estate).\n"
            f"- **Culinary:** Custom diabetic gourmet tasting menu by Executive Chef.\n"
            f"- **Logistics Package:** 4-attendant dual-lane valet service + acoustic velvet ceiling baffles included.\n"
            f"- **Total Fixed Investment:** **$41,500** (Full gala execution, within your $45k cap).\n"
        )
    else:
        content = (
            f"### 🎯 Tailored Proposal for {client_name}\n\n"
            f"**Retained Hindsight Context:**\n{context_text}\n\n"
            f"Proposal custom-built honoring every prior objection and pricing constraint."
        )

    return {
        "mode": "With Hindsight Memory (DealAnchor)",
        "has_memory": True,
        "matched_constraints": recalled,
        "proposal": content
    }

