# 💼 DealAnchor — B2B Client & Deal Memory Co-Pilot

> **HackwithHyderabad 3.0 Project Submission**  
> **Theme:** AI Agents That Learn Using Hindsight (Persistent Memory Architecture)  
> **Target Problem:** High-value deals lost because sales teams & account managers forget nuanced client constraints across multi-week sales cycles.

---

## 📌 Executive Summary

Closing major B2B contracts takes weeks across multiple calls. Along the way, clients share crucial constraints: budget limits, competitor comparisons, and specific feature pet peeves. 

Standard AI chatbots suffer from **"goldfish memory"**—they treat every conversation in isolation, drafting generic sales pitches that ask questions the client already answered or recommend things the client already rejected.

**DealAnchor** solves this using **Vectorize Hindsight** as an intelligent, long-term memory layer for customer relationships:
* **Meeting 1 (3 weeks ago):** Client says: *"We have a hard budget cap of $15,000/year and our truck drivers need a dead-simple 1-tap mobile experience."*
* **Meeting 2 (2 weeks ago):** Client says: *"We're also looking at Salesforce, but their mobile app has a 6-second lag that our drivers hated."*
* **Meeting 3 (Today):** When generating a proposal:
  * **Generic AI (No Memory):** Pitch asks for $32,000/year and proposes complex dashboards.
  * **DealAnchor (With Hindsight):** Recalls the $15k budget cap, prices the deal at $14,400 flat, highlights sub-second mobile delivery confirmation, and directly contrasts against Salesforce's mobile lag.

---

## 🚀 Quick Start

```bash
# Launch interactive Streamlit dashboard
streamlit run ui.py
```
*(Or double-click `run_demo.bat`)*

