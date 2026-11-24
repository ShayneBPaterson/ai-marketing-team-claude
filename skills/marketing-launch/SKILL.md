---
name: marketing-launch
description: Generate a JENGAI feature release or marketing campaign launch playbook (customer comms, Constant Contact release pair, LinkedIn announcement, website updates, sales handoff, and CS coordination).
---

# JENGAI Feature Release & Campaign Launch Playbook (`/marketing launch`)

Generates a tactical launch playbook tailored to how JENGAI actually launches new product capabilities (e.g., Data Privatization release) or demand campaigns (e.g., Q3/Q4 Sales-Support series, Owner AI Workshops). Explicitly excludes Product Hunt, consumer waitlists, and fake early-bird countdowns.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `core-brain/company/product-overview.md` and `gtm-knowledge/feature-value-mapping.md` (verify whether the capability is shipped vs. upcoming!)
2. `marketing/outputs/messaging/approved-messaging.md` and `gtm-knowledge/messaging-and-value-proposition.md`
3. `marketing/knowledge/channels-and-cadence.md` and `marketing/status.md`
4. `marketing/knowledge/visual-brand-guide.md` and `marketing/knowledge/website-tracking-and-embed-snippets.md`
5. `marketing/campaigns/2026-09-24-data-privatization-release-email/` (reference pattern for product releases)

## Pre-Launch Product-Truth Gate (Mandatory)

Per `approved-messaging.md` (*Where product truth comes from*):
- Never announce a capability as shipped unless confirmed in `product-state.md` or explicitly confirmed by Engineering/Product (for example, `Bid Version History` and per-bid win-probability scoring remain unshipped/unconfirmed unless updated).
- Confirm whether the feature is gated per Account (`AccountId` settings) so customer comms set accurate expectations.

## Playbook Structure (`<MKT_ROOT>/templates/campaign-launch-checklist.md`)

1. **Launch Brief & Positioning Alignment:** Target persona (Owner, Head of Estimation, Head of Sales), message pillar, positioning lock check, and approval owners (Renata for marketing, Shayne for sales handoff).
2. **4-Week Timeline (T-3 weeks → Launch Week → T+2 weeks):**
   - **T-3 to T-2 (Foundation):** Lock feature naming with Product, draft positioning + FAQs, build Constant Contact Email 1 (Coming soon) & Email 2 (Live) using `<MKT_ROOT>/templates/email-product-release.md` + `<MKT_ROOT>/templates/email-constant-contact.mjml`, prep website updates (`jengai-com/public-website`).
   - **T-1 (Enablement & QA):** Brief Sales (Shayne, Zhai, Aica) with 1-page talk track + objection responses; brief CS/onboarding; test GA4 (`G-EJJJHWZFQQ`), HubSpot forms, and Calendly links; run `validate_copy.py --public` on all assets.
   - **Launch Week:** Send Customer/Prospect Constant Contact announcement (after Renata CMO approval), publish weekly LinkedIn post (company, Renata CMO/Founder, or Shayne founder voice), publish website update / short walkthrough video, notify team via **Microsoft Teams**.
   - **T+1 to T+2 (Follow-through):** Review HubSpot/Constant Contact opens, clicks, and demo requests; capture early customer quotes for future case studies; run brief internal retrospective.
3. **Ready-to-Edit Assets:** Draft Email 1 (Coming soon), Draft Email 2 (Live), Draft LinkedIn post, and Sales 1-paragraph briefing note.

Save to `LAUNCH-PLAYBOOK.md` and run `python3 <MKT_ROOT>/scripts/validate_copy.py LAUNCH-PLAYBOOK.md --register internal` (plus `--public` on the customer-facing email/LinkedIn drafts).
