"""
tests/test_deal_anchor.py
Unit tests verifying DealAnchor memory retention, recall, and agent comparison.
"""

import pytest
from seed_deals import INITIAL_DEALS
from memory import DealAnchorMemory
from agent import draft_proposal_without_memory, draft_proposal_with_hindsight

@pytest.fixture
def memory_manager():
    mm = DealAnchorMemory(bank_id="test-deal-bank")
    mm.seed_initial_deals(INITIAL_DEALS)
    return mm

def test_initial_deals_seeding(memory_manager):
    assert len(memory_manager._local_deals_bank) >= 6

def test_recall_client_context(memory_manager):
    recalled = memory_manager.recall_client_context("Apex")
    assert len(recalled) > 0
    assert any("Marcus" in r.get("content", "") or "Apex" in r.get("client_name", "") for r in recalled)

def test_retain_new_meeting(memory_manager):
    res = memory_manager.retain_meeting_note(
        deal_id="DEAL-TEST",
        client_name="Test Enterprise",
        meeting_summary="Discussed custom SLA requirements",
        constraints="Requires 99.99% uptime guarantee"
    )
    assert res is not None
    recalled = memory_manager.recall_client_context("Test Enterprise")
    assert any("SLA" in r.get("content", "") for r in recalled)

def test_proposal_comparison(memory_manager):
    base = draft_proposal_without_memory("Apex Fleet Logistics", "")
    assert base["has_memory"] is False

    anchored = draft_proposal_with_hindsight("Apex Fleet Logistics", memory_manager)
    assert anchored["has_memory"] is True
    assert "$14,400" in anchored["proposal"] or "Salesforce" in anchored["proposal"]

