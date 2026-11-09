"""
ui.py - DealAnchor Interactive Web Dashboard
Visualizes multi-meeting memory stream, side-by-side proposal comparison,
continuous meeting retention, and win/loss pattern reflection.
"""

import streamlit as st
from seed_deals import INITIAL_DEALS
from memory import DealAnchorMemory
from agent import draft_proposal_without_memory, draft_proposal_with_hindsight

st.set_page_config(
    page_title="DealAnchor | B2B Client Memory Co-Pilot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .deal-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #F59E0B;
        margin-bottom: 0px;
    }
    .deal-sub {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 25px;
    }
    .timeline-card {
        background-color: #1E293B;
        border-left: 4px solid #F59E0B;
        padding: 14px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .generic-pitch {
        background-color: #18181B;
        border-left: 4px solid #EF4444;
        padding: 16px;
        border-radius: 6px;
    }
    .hindsight-pitch {
        background-color: #0F172A;
        border-left: 4px solid #10B981;
        padding: 16px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

if "memory_manager" not in st.session_state:
    mm = DealAnchorMemory()
    mm.seed_initial_deals(INITIAL_DEALS)
    st.session_state.memory_manager = mm

mm: DealAnchorMemory = st.session_state.memory_manager

with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/handshake.png", width=64)
    st.markdown("### **DealAnchor Engine**")
    st.caption("Client Relationship Intelligence Powered by Hindsight")
    
    st.divider()
    selected_deal_name = st.selectbox(
        "Select Active Client:",
        [d["client_name"] for d in INITIAL_DEALS]
    )
    
    current_deal = next(d for d in INITIAL_DEALS if d["client_name"] == selected_deal_name)
    
    st.markdown(f"**Industry:** `{current_deal['industry']}`")
    st.markdown(f"**Target Value:** `{current_deal['deal_value']}`")
    st.markdown(f"**Stakeholder:** `{current_deal['key_stakeholder']}`")
    
    st.divider()
    if st.button("🔄 Reset & Re-Seed Client Memory", use_container_width=True):
        mm.seed_initial_deals(INITIAL_DEALS)
        st.success("Re-seeded client memories!")
        st.rerun()

st.markdown('<div class="deal-header">💼 DealAnchor Co-Pilot</div>', unsafe_allow_html=True)
st.markdown('<div class="deal-sub">Persistent memory for client negotiations & high-value sales — powered by <b>Vectorize Hindsight</b>.</div>', unsafe_allow_html=True)

tab_triage, tab_timeline, tab_add, tab_reflect = st.tabs([
    "🎯 Generate Proposal / Follow-up",
    "📅 Multi-Meeting Memory Stream",
    "📝 Retain New Meeting Notes",
    "📈 Win/Loss Pattern Reflection"
])

with tab_triage:
    st.markdown(f"#### Generating Follow-up Proposal for **{selected_deal_name}**")
    st.caption("See what happens when an AI forgets past meetings vs. when it remembers every client constraint.")
    
    if st.button("⚡ Generate Closing Proposal Comparison", type="primary"):
        c_base, c_mem = st.columns(2)
        
        with c_base:
            st.markdown("### ❌ Generic AI (Without Memory)")
            st.caption("Stateless chatbot — has zero memory of prior calls")
            base = draft_proposal_without_memory(selected_deal_name, "")
            st.markdown(f'<div class="generic-pitch">{base["proposal"]}</div>', unsafe_allow_html=True)
            
        with c_mem:
            st.markdown("### ✅ DealAnchor (With Hindsight Memory)")
            st.caption("Recalls every constraint, budget ceiling & competitor objection")
            hindsight_res = draft_proposal_with_hindsight(selected_deal_name, mm)
            st.markdown(f'<div class="hindsight-pitch">{hindsight_res["proposal"]}</div>', unsafe_allow_html=True)

with tab_timeline:
    st.markdown(f"#### 📅 Historical Meeting Stream: **{selected_deal_name}**")
    for m in current_deal["meeting_history"]:
        st.markdown(f"""
        <div class="timeline-card">
            <b>Meeting #{m['meeting_number']} ({m['date']})</b><br>
            <i>{m['summary']}</i><br><br>
            📌 <b>Constraints Identified:</b> {m.get('constraints_identified', 'None')}<br>
            ⚠️ <b>Objections / Competitors:</b> {m.get('objections_raised', 'None')}
        </div>
        """, unsafe_allow_html=True)

with tab_add:
    st.markdown("#### 📝 Record Takeaways from Today's Meeting")
    with st.form("new_meeting_form"):
        f_client = st.text_input("Client Name:", value=selected_deal_name)
        f_summary = st.text_area("Discussion Summary:", placeholder="What was discussed in today's call?")
        f_constraints = st.text_input("Specific Preferences / Budget Constraints:", placeholder="e.g. Max budget $20k, must support iOS")
        f_objections = st.text_input("Competitor Mentions or Pushbacks:", placeholder="e.g. Looking at competitor X, worried about setup time")
        
        sub = st.form_submit_button("💾 Save into Hindsight Memory", type="primary")
        if sub and f_summary:
            mm.retain_meeting_note(
                deal_id="DEAL-CUSTOM",
                client_name=f_client,
                meeting_summary=f_summary,
                constraints=f_constraints,
                objections=f_objections
            )
            st.success(f"✅ Retained meeting takeaways for {f_client} in Hindsight!")
            st.rerun()

with tab_reflect:
    st.markdown("#### 📈 Hindsight Deal Reflection: Cross-Client Intelligence")
    st.caption("Analyzes recurring objections and deal-breakers across all clients.")
    if st.button("🔍 Reflect on Deal Patterns", type="primary"):
        with st.spinner("Analyzing deal patterns across Hindsight memory bank..."):
            res = mm.reflect_on_win_loss_patterns()
            st.info(res)

