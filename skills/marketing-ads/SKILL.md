---
name: marketing-ads
description: DORMANT / TEST-ONLY skill (paid ads are currently parked per channels-and-cadence.md). When explicitly greenlit by Renata, designs small-budget B2B LinkedIn ABM and high-intent Google Search experiments for JENGAI.
---

# JENGAI Paid Acquisition Test Playbook (`/marketing ads`) — DORMANT / TEST-ONLY

> **Status: PARKED BY DEFAULT (`marketing/knowledge/channels-and-cadence.md`).**
> Paid advertising is currently parked for JENGAI. **Do not recommend launching paid ads proactively, and never spend or finalize a campaign without explicit approval from Renata (CMO).** Use this skill only when Renata or Shayne explicitly commissions a bounded test experiment.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` via `context/gtm-brain-map.md` and read:
1. `marketing/knowledge/channels-and-cadence.md`
2. `gtm-knowledge/icp.md` and `gtm-knowledge/pricing.md`
3. `marketing/outputs/messaging/approved-messaging.md` and `marketing/outputs/messaging/headline-bank.md`
4. `marketing/knowledge/website-tracking-and-embed-snippets.md` (note: GA4 form-submit and `calendly_booking` events MUST be wired before spending ad dollars!)
5. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` and `gtm-knowledge/gtm-specific-voice.md`

## Pre-Spend Tracking Prerequisite (Hard Gate)

Before any test launches, confirm on the destination landing page:
- GA4 (`G-EJJJHWZFQQ`) and HubSpot (`51915935`) are active.
- GA4 form-submission event and `calendly_booking` listener are live and marked as Key Events.
- Dedicated destination URL (`/starnet`, `/demo`, or vertical landing page) matches the ad message 1:1.

## Only Two Approved Experiment Channels (No TikTok, No Meta B2C, No E-Commerce)

### Channel 1: LinkedIn Account-Based Marketing (ABM)
- **Audience:** Matched company list from FUSE Alliance (`fuse-alliance-members.csv`), Starnet (`starnet-accounts.md`), and Commercial USA (~500 target commercial finish-trade subcontractors, \$4M+ revenue) layered by job title: Owner, President, Principal, Chief Estimator, Head of Estimation, VP of Preconstruction, Head of Sales.
- **Formats:** Single-image Sponsored Content (Design System v2 tokens: `#020133`, `#000180`, `#d0ffa3` spark only, Inter) or Document Ads (PDF carousel built from approved case studies — Bonitz, Pro-United, Silver Slate, Transylvania, Axis).
- **Hook discipline:** Lead with Shayne's 3 emotional buttons (Find work, Win more work, Make more money) and approved proof points. Default CTA: `"Book a demo"` or `"Register for Owner AI Workshop"`.

### Channel 2: Google Search (Exact & Phrase Match Only)
- **Match types:** **Exact match `[keyword]` and Phrase match `"keyword"` only** (never deprecated broad match modified; avoid broad match in a ~500-company niche).
- **Keyword themes:** Commercial flooring bid management software, commercial specialty contractor proposal software, commercial subcontractor bid pipeline CRM, finish schedule analysis software.
- **Strict negative keyword list:** Exclude `free`, `residential`, `DIY`, `homeowner`, `handyman`, `general contractor`, `GC`, `jobs`, `salary`, `careers`, `template free`, `Excel download`, `roofing`, `plumbing`, `HVAC`, `electrical`.
- **Responsive Search Ads:** Up to 15 headlines (≤30 chars) and 4 descriptions (≤90 chars), all strictly honoring the 2026-08-31 positioning lock (pricing and operations platform, NOT estimating/takeoff tool).

## Output & Validation

Save to `AD-CAMPAIGNS.md` clearly stamped `STATUS: TEST PROPOSAL — PARKED CHANNEL, REQUIRES RENATA APPROVAL + GA4 CONVERSION TRACKING PREREQUISITE`. Do not fabricate ROAS or CPA projections without historical JENGAI ad data. Run:
```bash
python3 scripts/validate_copy.py AD-CAMPAIGNS.md --public --register external
```
