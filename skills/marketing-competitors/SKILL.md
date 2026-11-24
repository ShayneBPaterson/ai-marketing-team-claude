---
name: marketing-competitors
description: Research and profile a competitor using JENGAI's threat-scoring model (1-5 material threat, 0-100 matrix score, Tier H/M/L), robots.txt/terms compliance checks, and gtm-brain propagation checklist.
---

# JENGAI Competitive Intelligence (`/marketing competitors <company/url>`)

Maintains JENGAI's canonical competitor tracker in `gtm-brain/marketing/knowledge/competitors/` and enforces JENGAI's market-intelligence compliance rules.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `gtm-knowledge/competitive-intelligence.md`
2. `marketing/knowledge/competitors/README.md` and `threat-assessment-matrix.md`
3. `marketing/outputs/competitive/top-five-competitors.md`
4. `marketing/market-intelligence/settings.md` and `marketing/market-intelligence/runbook.md`
5. `marketing/outputs/messaging/approved-messaging.md` (Competitive context section)

## Compliance Rules (Non-Negotiable)

- **Always run a compliance check first:** Check `robots.txt`, site terms, and `marketing/market-intelligence/*/sources.json`. Never scrape domains marked `excluded` (ENR, Construction Dive, JBKnowledge; check Procore/Bobyard/PlanHub override notes).
- **Evidence ledger required:** Record exact URLs, access dates (`YYYY-MM-DD`), and separate confirmed facts from inferences. Never guess funding or ARR when public databases conflict — state the conflict explicitly.
- **No public competitor naming by default:** Competitor profiles and analyses are **internal intelligence**. Never reproduce competitor content or name direct competitors in public JENGAI copy without Renata/Shayne sign-off.
- **Keep known nuances intact:**
  - MeasureSquare takeoff (MS8) is a partner tool JENGAI works with; **only MeasureSquare CRM** competes (and fits multi-location firms poorly).
  - BuildingConnected Bid Board Pro is a real bid-tracking threat (confirmed churn signal); never cite cancelled 25% / 8 hrs / 2.3x stats.
  - Contractor Foreman ships a real generic sales CRM (do not claim "no sales pipeline").

## Execution Workflow

1. **Run compliance-aware scanner:**
   ```bash
   python3 <MKT_ROOT>/scripts/competitor_scanner.py --url <competitor-url> --output json
   ```
   (Respect `blocked_by_compliance` or `blocked_by_robots` outputs — never silently bypass.)
2. **Research via web search & review sites (G2, Capterra, Reddit, vendor docs):**
   - Primary paying buyer (GC vs. specialty sub; residential vs. commercial; finish trades vs. MEP/general)
   - Transaction side (outbound GC bid-leveling vs. inbound sub ITB intake → pricing → proposal → CRM)
   - Pricing tiers, disclosed funding/ownership, integrations, recent shipped releases, top user praise/complaints
3. **Score the Competitor on JENGAI's Model:**
   - **Material Threat Rating (1–5):** `1/5` wrong buyer/trade, `2/5` adjacent watch, `3/5` partial overlap, `4/5` strong direct overlap, `5/5` head-on finish-trade rival.
   - **Threat Matrix Score (0–100) & Tier (`H` / `M` / `L`):** Consistent with `marketing/knowledge/competitors/threat-assessment-matrix.md`.
4. **Produce Two Artifacts** using `<MKT_ROOT>/templates/competitor-profile.md`:
   - Compact profile (`COMPETITOR-PROFILE-<slug>.md` — ready for `marketing/knowledge/competitors/<slug>.md`)
   - Full dated analysis + source ledger (`COMPETITOR-REPORT.md` — ready for `marketing/outputs/competitive/analyses/<slug>-competitive-analysis-YYYY-MM-DD.md`)
5. **Include `gtm-brain` Propagation Checklist:** Remind the operator which tracker files to update (`README.md`, `threat-assessment-matrix.md`, `all-known-competitors.md`, `top-10-funded-competitors.md`, and `market-intelligence/*/sources.json` + Azure crawler pack if monitored).

Run `python3 <MKT_ROOT>/scripts/validate_copy.py COMPETITOR-REPORT.md --register internal`.
