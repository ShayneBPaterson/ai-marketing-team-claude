---
name: marketing-social
description: Plan and draft JENGAI's LinkedIn content (1 post/week cadence in Shayne's founder voice or JENGAI company voice) and quarterly calendar scaffolds grounded in gtm-brain.
---

# JENGAI Social Media & LinkedIn Engine (`/marketing social`)

Plans quarterly weekly calendars and drafts JENGAI's **LinkedIn** content (primary B2B channel). Explicitly rejects daily multi-platform creator schedules, TikTok trends, and Twitter-thread bro-marketing hooks.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` via `context/gtm-brain-map.md` and read:
1. `marketing/status.md` (check active quarterly calendar and hook-rework status)
2. `marketing/knowledge/channels-and-cadence.md` and `marketing/knowledge/positioning-and-pillars.md`
3. `marketing/outputs/messaging/approved-messaging.md` and `marketing/outputs/messaging/headline-bank.md`
4. `marketing/campaigns/2026-08-content-calendar-hook-rework/findings-2026-08-01-growth-story-sourcing.md`
5. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` and `gtm-knowledge/gtm-specific-voice.md`

## JENGAI Social Operating Rules

- **Standing cadence:** **1 LinkedIn post per week** (paired with 1 Constant Contact nurture email). Best publish window: **Tue–Thu, 8:00–11:00 AM ET**.
- **Two voices only:**
  - **Shayne founder voice:** CEO-to-CEO, technical yet plain-spoken, concrete customer storytelling, humble confidence, short connected paragraphs.
  - **JENGAI company voice:** Trusted finish-trade peer, identity marketing ("buy this" → "be this"), zero AI hype.
- **Hook rules:** Lead with a specific number or named growth story hitting one of the three emotional buttons (**Find work**, **Win more work**, **Make more money**). Never open with engagement-bait rhetorical questions (`"Sound familiar?"`, `"What if you could..."`, `"Unpopular opinion 🧵"`, `"POV:"`) or stacked one-line hype paragraphs.
- **CTA discipline:** Soften the CTA for cold LinkedIn audiences (link to `jengai.com/success-stories`, invite a DM/comment, or "Book a demo" on proof posts).
- **Source & compliance rule:** Every post using external inspiration must carry a `Source provenance` line:
  - *Internal-pattern-only:* Inspired by monitored competitors (never name STACK, Bobyard, MeasureSquare CRM, Kreo, Togal.AI, or 1build/Handoff publicly).
  - *Public-citation:* Verified trade press, associations (NTCA, FCICA, Natural Stone Institute, FUSE, Starnet), or non-competitor adjacent-trade SaaS (ServiceTitan, Knowify, Housecall Pro) — exact figures, no rounding. Flag PlanHub for Renata/Shayne review; never cite Garmon & Company.

## Execution Modes

### Mode A: Scaffold a Quarterly Calendar
Run:
```bash
python3 scripts/social_calendar.py --start YYYY-MM-DD --weeks 12 --format markdown --event "4:Starnet Fall Meeting"
```
Fill in concrete hooks, proof anchors, and source-provenance lines for each week and save to `SOCIAL-CALENDAR.md`.

### Mode B: Draft LinkedIn Posts (Single or Monthly Batch)
For each post, output:
- Target week, pillar, emotional button, voice (Founder vs. Company), framework (`Problem → Solution → Proof`, `Before / After`, or `Named Growth Story → JENGAI Bridge`)
- Full ready-to-paste LinkedIn post (120–250 words, complete sentences, zero banned words)
- 3 relevant finish-trade hashtags max (e.g., `#CommercialFlooring #SpecialtyContractors #Preconstruction`)
- Visual/asset note aligned to `visual-brand-guide.md` (`#020133`, `#000180`, `#d0ffa3` spark only)
- Source provenance line

### Validation
Run `python3 scripts/validate_copy.py SOCIAL-CALENDAR.md --public --register external` (or `--register founder`) and complete `pre-publish-checklist.md`. Mark all posts `DRAFT — AWAITING APPROVAL`.
