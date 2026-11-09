"""
seed_deals.py
Realistic client deal cycles with multi-meeting conversation history,
objections, competitor benchmarks, and specific customer requirements.
"""

INITIAL_DEALS = [
    {
        "deal_id": "DEAL-001",
        "client_name": "Apex Fleet Logistics",
        "industry": "Supply Chain & Transportation",
        "deal_value": "$15,000/year",
        "key_stakeholder": "Marcus Vance (VP of Operations)",
        "meeting_history": [
            {
                "meeting_number": 1,
                "date": "2026-10-04",
                "summary": "Discovery Call: 45 field truck drivers. Marcus emphasized that drivers are non-technical and push back against complicated software.",
                "constraints_identified": "Strict annual budget limit of $15,000. Needs offline sync capability in remote delivery zones."
            },
            {
                "meeting_number": 2,
                "date": "2026-10-18",
                "summary": "Technical Evaluation: Marcus revealed they are actively comparing us against Salesforce Field Service.",
                "objections_raised": "Salesforce app took 6 seconds to log a drop-off during their pilot test, causing driver complaints. Drivers need a 1-tap confirmation."
            }
        ],
        "winning_tactics": "Highlight sub-second 1-tap delivery logging, offline-first sync, and guaranteed locked pricing at $14,400/yr (under their $15k ceiling). Directly counter Salesforce mobile latency."
    },
    {
        "deal_id": "DEAL-002",
        "client_name": "Highland Luxury Gala",
        "industry": "Corporate Events & Hospitality",
        "deal_value": "$42,000",
        "key_stakeholder": "Evelyn Sterling (Chairperson)",
        "meeting_history": [
            {
                "meeting_number": 1,
                "date": "2026-10-12",
                "summary": "Concept Planning: 150 executive guests. Evelyn strictly hates modern minimalist glass architecture; insists on historic garden estates.",
                "constraints_identified": "Hard budget cap of $45,000. Board Chairman requires strictly low-glycemic / diabetic culinary menu."
            },
            {
                "meeting_number": 2,
                "date": "2026-10-26",
                "summary": "Venue Review: Evelyn raised serious concerns regarding valet logistics and acoustic echo during the keynote address.",
                "objections_raised": "Previous gala had a 40-minute valet queue. Insists on dedicated dual-lane valet and acoustic draped ceilings."
            }
        ],
        "winning_tactics": "Recommend the Historic Willow Manor with acoustic ceiling baffles. Include custom diabetic gourmet tasting menu and 4-attendant valet service at $41,500 total."
    },
    {
        "deal_id": "DEAL-003",
        "client_name": "Bloom Specialty Roasters",
        "industry": "Retail & Specialty Food",
        "deal_value": "$800/month",
        "key_stakeholder": "David Kim (Founder & CEO)",
        "meeting_history": [
            {
                "meeting_number": 1,
                "date": "2026-10-20",
                "summary": "Initial Chat: 8 cafe locations experiencing 18% bean spoilage due to irregular FIFO stock rotation by morning shift baristas.",
                "constraints_identified": "Monthly budget maximum $1,000/mo. Cannot require more than 15 seconds of barista time per shift."
            },
            {
                "meeting_number": 2,
                "date": "2026-11-01",
                "summary": "Competitor Comparison: Tested Toast POS inventory add-on, but baristas found the 5-screen nested dropdowns too tedious during rush hours.",
                "objections_raised": "Won't buy any software that slows down espresso checkout queues."
            }
        ],
        "winning_tactics": "Showcase barcode camera scan with 2-second batch stock confirmation. Price at $750/month with zero-hardware setup."
    }
]

