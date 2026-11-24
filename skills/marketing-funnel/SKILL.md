---
name: marketing-funnel
description: Audit or design JENGAI's end-to-end B2B funnel (TOFU LinkedIn/Email/Events -> jengai.com -> HubSpot Form -> Calendly Discovery -> Sandler Discovery -> Salesforce Opportunity), reconciling gtm-knowledge placeholders.
---

# JENGAI Funnel & Buyer Journey Analysis (`/marketing funnel`)

Maps, audits, and helps complete JENGAI's B2B funnel from top-of-funnel (TOFU) awareness through booked discovery call and Sales handoff. Directly supports filling the two currently unbuilt canonical files in `gtm-brain`: `gtm-knowledge/funnel-stages-and-journey-maps.md` and `gtm-knowledge/lead-definitions-and-qualification-criteria.md`.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `gtm-knowledge/funnel-stages-and-journey-maps.md`
2. `gtm-knowledge/lead-definitions-and-qualification-criteria.md`
3. `gtm-knowledge/icp.md` and `gtm-knowledge/pricing.md`
4. `marketing/knowledge/channels-and-cadence.md`
5. `marketing/knowledge/website-tracking-and-embed-snippets.md`

## JENGAI's Real Funnel Architecture (No E-Commerce or PLG Free Trials)

```
TOFU Channels (LinkedIn 1/wk · Constant Contact 1/wk · Starnet/FUSE/Commercial USA Events · Owner AI Workshops · Organic Search)
   │
   ▼
Website Entry (jengai.com · /starnet · /demo · /success-stories · Workshop Registration)
   │   [Tracked: GA4 G-EJJJHWZFQQ + HubSpot 51915935 + hubspotutk]
   ▼
Lead Capture (HubSpot Forms API: /starnet or /demo form — contact + bids/mo, takeoff/pricing/ERP stack)
   │   [Open gap: GA4 form_submit event not yet wired]
   ▼
Discovery Scheduling (Pre-filled Calendly — verify current Sales/Marketing routing; website-tracking-and-embed-snippets.md lists renata-jengai/jengai-discovery-call 30m and 1hour 45m)
   │   [Open gap: GA4 calendly_booking event not yet wired]
   ▼
Sales Qualification & Close (Sales-owned: Prospecting -> Discovery [Sandler Pain/Budget/Decision] -> Demo -> Proposal -> Negotiation -> Closed Won/Lost)
```

## Execution Process

1. **Pull Live Data When Available:** Prompt to invoke `core-brain/skills/hubspot-data/` (form fills, landing page conversions) and `core-brain/skills/salesforce-data/` (opportunity stages, win rates, cycle length). **Never invent conversion rates or monthly dollar revenue lift** when live data is absent.
2. **Stage-by-Stage Buyer Journey Audit:** For every stage (Unaware → Aware → Engaged/MQL → Booked Discovery → SQL/Demo → Proposal), document:
   - What the finish-trade Owner / Head of Estimation / Head of Sales is thinking
   - Primary objection or friction point
   - Exact JENGAI asset or approved proof point that moves them forward
   - Measurement source (GA4, HubSpot, Calendly, Salesforce) and tracking gaps
3. **Reconcile Stage & Lead Definitions:** Where helpful, draft concrete updates for:
   - Mapping Salesforce's 16 `StageName` values onto Sales's 6 deal stages
   - Explicit MQL criteria (ICP fit: \$4M+, commercial finish-trade sub, self-performs takeoff + engagement signal) vs. SQL criteria (Sandler Pain + Budget + Decision confirmed)
4. **Prioritized Bottleneck Fixes:** Rank by impact and effort (Quick wins this week, Medium-term this month, Strategic this quarter).

Save to `FUNNEL-ANALYSIS.md` (Internal Reports register) and run `python3 <MKT_ROOT>/scripts/validate_copy.py FUNNEL-ANALYSIS.md --register internal`.
