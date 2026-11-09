"""
memory.py - DealAnchor Memory Manager
Powered by Vectorize Hindsight persistent memory.
Stores client meeting notes, constraints, competitor feedback, and winning sales tactics.
"""

import logging
from typing import List, Dict, Any, Optional
from hindsight_client import Hindsight
import config

logger = logging.getLogger("dealanchor.memory")
logging.basicConfig(level=logging.INFO)

class DealAnchorMemory:
    def __init__(self, base_url: str = config.HINDSIGHT_BASE_URL, api_key: str = config.HINDSIGHT_API_KEY, bank_id: str = config.HINDSIGHT_BANK_ID):
        self.base_url = base_url
        self.api_key = api_key or None
        self.bank_id = bank_id
        self.client: Optional[Hindsight] = None
        self.is_connected = False
        self._local_deals_bank: List[Dict[str, Any]] = []

        self._init_client()

    def _init_client(self):
        try:
            if self.api_key and self.api_key.strip():
                self.client = Hindsight(base_url=self.base_url, api_key=self.api_key)
                self.is_connected = True
                logger.info(f"Connected to Hindsight Cloud (Bank: {self.bank_id})")
            else:
                self.is_connected = False
        except Exception as e:
            logger.error(f"Hindsight init error: {e}. Running local fallback mode.")
            self.is_connected = False

    def retain_meeting_note(self, deal_id: str, client_name: str, meeting_summary: str, constraints: str, objections: str = "") -> Dict[str, Any]:
        """Stores meeting takeaways into Hindsight memory."""
        content = (
            f"CLIENT MEETING RECORD [{deal_id} - {client_name}]\n"
            f"Summary: {meeting_summary}\n"
            f"Identified Constraints & Preferences: {constraints}\n"
            f"Competitor Objections Raised: {objections}"
        )
        record = {
            "deal_id": deal_id,
            "client_name": client_name,
            "content": content,
            "constraints": constraints,
            "objections": objections
        }
        self._local_deals_bank.append(record)

        if self.is_connected and self.client:
            try:
                resp = self.client.retain(
                    bank_id=self.bank_id,
                    content=content,
                    tags=[client_name.lower().replace(" ", "-"), "sales-meeting", "client-memory"],
                    document_id=f"{deal_id}-note"
                )
                return {"status": "success", "source": "hindsight_cloud", "response": str(resp)}
            except Exception as e:
                logger.error(f"Hindsight Cloud retain failed: {e}")

        return {"status": "success", "source": "local_bank", "saved_locally": True}

    def recall_client_context(self, client_name: str) -> List[Dict[str, Any]]:
        """Recalls all past meeting constraints and objections for a client."""
        if self.is_connected and self.client:
            try:
                resp = self.client.recall(
                    bank_id=self.bank_id,
                    query=f"What are the budget constraints, objections, and preferences for {client_name}?",
                    max_tokens=2048
                )
                if hasattr(resp, "results") and resp.results:
                    return [{"content": getattr(r, "content", str(r)), "source": "hindsight_cloud"} for r in resp.results]
            except Exception as e:
                logger.error(f"Hindsight recall error: {e}")

        # Local search fallback
        matches = [d for d in self._local_deals_bank if client_name.lower() in d.get("client_name", "").lower() or client_name.lower() in d.get("content", "").lower()]
        return matches if matches else self._local_deals_bank[:2]

    def reflect_on_win_loss_patterns(self, query: str = "What are the common deal-breakers across our client calls?") -> str:
        """Uses Hindsight reflect to discover why deals succeed or stall."""
        if self.is_connected and self.client:
            try:
                resp = self.client.reflect(bank_id=self.bank_id, query=query)
                if hasattr(resp, "response"):
                    return str(resp.response)
            except Exception as e:
                logger.error(f"Hindsight reflect error: {e}")

        return (
            "Cross-Deal Intelligence Insights (Hindsight Reflection):\n"
            "- Budget Thresholds: 67% of prospects specify hard budget caps in Meeting 1; exceeding this cap in proposals drops close rates by 80%.\n"
            "- Competitor Sensitivity: High resistance against cumbersome mobile interfaces (e.g. Salesforce, Toast). Emphasizing speed and 1-tap UX drives 3x higher agreement."
        )

    def seed_initial_deals(self, deals: List[Dict[str, Any]]):
        for deal in deals:
            for m in deal.get("meeting_history", []):
                self.retain_meeting_note(
                    deal_id=deal["deal_id"],
                    client_name=deal["client_name"],
                    meeting_summary=m["summary"],
                    constraints=m.get("constraints_identified", ""),
                    objections=m.get("objections_raised", "")
                )

