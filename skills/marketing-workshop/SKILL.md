---
name: marketing-workshop
description: Build a campaign package for JENGAI's Owner AI Workshops or customer webinars (landing page brief, Constant Contact promo/reminder/replay emails, LinkedIn promo post, and post-workshop demo handoff).
---

# JENGAI Owner AI Workshops & Webinar Campaign (`/marketing workshop`)

Supports JENGAI's active owner-focused education campaigns (`marketing/campaigns/2026-08-owner-ai-workshops/` — e.g., *Before You Sign* subcontract review, *Get the Business Out of Your Head* SOP drafting, and customer webinars).

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` via `context/gtm-brain-map.md` and read:
1. `marketing/campaigns/2026-08-owner-ai-workshops/readme.md` and current workshop plan files
2. `marketing/outputs/messaging/approved-messaging.md` and `gtm-knowledge/icp.md`
3. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` and `gtm-knowledge/gtm-specific-voice.md`
4. `marketing/knowledge/website-tracking-and-embed-snippets.md` and `marketing/knowledge/visual-brand-guide.md`

## Workshop-Specific Guardrails

- **Do not compete with JENGAI's pre-award workflow:** Owner AI Workshops solve high-value adjacent owner problems (subcontract review, SOPs, admin drafting) to earn trust and qualified demand — keep the workshop genuinely useful without turning the session into a disguised product pitch.
- **Explicit disclaimers where required:** For contract-review workshops (*Before You Sign*), always include a clear "not legal advice" disclaimer.
- **No external hosting of JENGAI internal docs:** Any downloadable attendee pack goes through approved JENGAI delivery channels; never publish internal company docs to `claude.ai`.
- **Natural bridge to demo:** Use post-workshop follow-up (not hard-sell during the lesson) to bridge attendees to a JENGAI discovery call (`https://calendly.com/renata-jengai/jengai-discovery-call`) using the "this will not be a pitch" framing when appropriate.

## Campaign Package Deliverables

1. **Workshop Positioning & Registration Page Brief:**
   - Audience: Owners and Presidents of \$4M+ commercial flooring, stone, and tile subcontractors.
   - Outcome-focused headline, 3 concrete takeaways (lists of 1 or 3 — never 2), speaker bio, exact date/time in US format (`MM/DD/YYYY`, 12-hour AM/PM ET), HubSpot registration form spec (portal `51915935`) + GA4 tracking (`G-EJJJHWZFQQ`).
2. **Constant Contact Email Sequence (Copy + MJML option):**
   - Invite 1 (14 days out): Practical owner pain + concrete takeaway.
   - Invite 2 (5 days out): Specific example of what attendees walk away with.
   - Reminder (24 hours + 1 hour before): Join link + prep note.
   - Replay + Resource Delivery (Day +1): Recording/resources + soft bridge to JENGAI discovery call.
3. **LinkedIn Promo Post (fits weekly cadence):** Founder or company voice, zero hype, concrete takeaway.
4. **Post-Workshop Sales Handoff Notes:** What signals qualify an attendee for Sales follow-up (per `gtm-knowledge/icp.md` and `lead-definitions-and-qualification-criteria.md`).

## Validation

Run `python3 scripts/validate_copy.py <output-file> --public --register external` and verify against `pre-publish-checklist.md`. Save as `WORKSHOP-CAMPAIGN-<slug>-YYYY-MM-DD.md` (draft only).
