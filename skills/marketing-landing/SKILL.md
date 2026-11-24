---
name: marketing-landing
description: Audit or brief a JENGAI landing page (/, /starnet, /demo, trade vertical, or workshop page) for B2B CRO, Design System v2 compliance, approved messaging, and HubSpot/GA4/Calendly tracking.
---

# JENGAI Landing Page CRO & Tracking Audit (`/marketing landing <url>`)

Audits live JENGAI landing pages or produces build-ready page briefs for `jengai-com/public-website` (`/`, `/starnet`, `/demo`, trade verticals, and Owner AI Workshop pages).

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `marketing/knowledge/website-tracking-and-embed-snippets.md`
2. `marketing/knowledge/visual-brand-guide.md`
3. `marketing/outputs/messaging/approved-messaging.md` and `gtm-knowledge/messaging-and-value-proposition.md`
4. `gtm-knowledge/icp.md` and `gtm-knowledge/feature-value-mapping.md`

## Execution Process

### Step 1: Automated Page & Stack Check
Run `python3 <MKT_ROOT>/scripts/analyze_page.py <url>` and inspect live HTML/copy.

### Step 2: Run the 7-Point JENGAI B2B CRO Audit (0–100)
1. **Hero Clarity & Positioning Lock (25 pts):** Communicates within 5 seconds that JENGAI is a pricing and operations platform for commercial finish-trade subcontractors; single H1; primary CTA (`"Book a demo"` or `"Schedule a discovery call"`) above the fold; zero retired estimating/takeoff tool wording.
2. **ICP & Trade Relevance (15 pts):** Speaks directly to Owners, Heads of Estimation, and Heads of Sales in commercial flooring, stone, and tile (\$4M+, FUSE/Starnet/Commercial USA).
3. **Approved Proof Placement (20 pts):** Surfaces verified proof from the 5 approved customers (Bonitz, Pro-United, Silver Slate, Transylvania, Axis) and \$15,000+ error-cost claim near decision points; zero banned/on-hold claims.
4. **Form & Calendly Handoff (15 pts):**
   - Form posts cleanly to HubSpot Forms API (`https://api.hsforms.com/submissions/v3/integration/submit/51915935/<form ID>`) with `hubspotutk` cookie and matching HubSpot field names (unmatched fields are silently dropped).
   - Required processing consent + optional Marketing Information subscription (`3442066946`).
   - Post-submit pre-filled Calendly iframe (confirm current Sales/Marketing routing — `website-tracking-and-embed-snippets.md` lists `renata-jengai/jengai-discovery-call` and `1hour`) with `hide_gdpr_banner=1`, `embed_type=Inline`, `embed_domain=www.jengai.com`.
5. **Tracking & Attribution Completeness (10 pts):** GA4 (`G-EJJJHWZFQQ`), HubSpot (`51915935`), plus check whether GA4 form-submission event and `calendly_booking` message listener are installed (flag if still open).
6. **Objection Handling (10 pts):** Addresses top subcontractor concerns (works with MeasureSquare MS8 / BuildingConnected; does not replace estimators; no fake urgency/scarcity).
7. **Design System v2 & Visual Hygiene (5 pts):** `#020133` deep navy, `#000180` primary pill buttons, `#d0ffa3` lime spark only (never background), Inter font, sentence case, full-caps `JENGAI`, responsive layout, lazy-loaded below-fold images.

### Step 3: Output & Validation
Write `LANDING-CRO.md` (Internal Reports register) with score breakdown, exact before/after copy fixes, exact HubSpot/GA4/Calendly snippet diffs, and 3 B2B test hypotheses (no fabricated dollar lift). Run `python3 <MKT_ROOT>/scripts/validate_copy.py LANDING-CRO.md --register internal`.
