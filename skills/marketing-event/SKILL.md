---
name: marketing-event
description: Build an end-to-end JENGAI trade show or buying-association event campaign kit for Starnet, FUSE Alliance, or Commercial USA (pre-show emails, onsite welcome MJML, booth headlines, /starnet-style landing brief, and post-show follow-up).
---

# JENGAI Trade Show & Association Event Kit (`/marketing event`)

Built for JENGAI's highest-converting live channel: **Starnet Spring/Fall Meetings, Starnet Tech Summit, FUSE Alliance, and AHSG Commercial USA**. Mirrors existing patterns in `marketing/events/2026/` and `marketing/campaigns/2026-09-14-ahsg-commercial-usa-email-campaign/`.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `gtm-knowledge/icp.md` and `gtm-knowledge/gtm-specific-voice.md` (especially the **Association membership check**, **Travel/event framing**, and **People references** rules)
2. `marketing/outputs/messaging/approved-messaging.md` and `marketing/outputs/messaging/headline-bank.md`
3. `marketing/knowledge/website-tracking-and-embed-snippets.md` (`/starnet` HubSpot form + pre-filled Calendly pattern)
4. `marketing/knowledge/visual-brand-guide.md`
5. Relevant existing event files in `marketing/events/2026/` (if present) and `marketing/memories/starnet-accounts.md` / `marketing/knowledge/fuse-alliance-members.csv` (only when targeting specific accounts)

## Critical Event & Voice Rules

- **Verify event dates:** Never invent conference dates or booth numbers — confirm from `marketing/events/2026/` or ask the operator.
- **Association check (`gtm-specific-voice.md`):** If emailing Starnet, FUSE, or Commercial USA members, **omit the full JENGAI company-description paragraph** on first touch because network membership already provides context. Include it only for non-association prospects.
- **Travel framing:** Say *"traveling to [city] for [Conference]"*, never *"doing a road trip"*.
- **Meeting routing (post-2026-11-09 Sales split):** Check who is attending and taking discovery/floor meetings before publishing. `website-tracking-and-embed-snippets.md` currently lists `renata-jengai/jengai-discovery-call`, while Sales moved to Shayne on 2026-11-09 — confirm with Renata and Shayne whether bookings for this event should route to Renata or Sales.
- **Direct outreach emails use Outreach register:** `"Dear [First Name],"`, no contractions, hyphenated role attribution (`"our CMO - Renata"`), closing line before signature.
- **Constant Contact broadcast emails** use External Marketing Copy register + Design System v2 MJML (`#020133` header band, `#000180` pill CTA, `#d0ffa3` spark only).

## Deliverables Generated (`<MKT_ROOT>/templates/email-event-series.md`)

1. **Event Brief & Positioning Angle:** Selected pillar, approved proof points (prioritize alliance-matched proof like Axis Interior Systems for Starnet), and approved headlines from `headline-bank.md` for booth/backdrop/signage.
2. **Pre-Show Email Sequence (Constant Contact broadcast + optional 1:1 invite):**
   - Email 1 (10–14 days before): Booth/meeting invite with the confirmed discovery-call Calendly link (verify current Sales/Marketing routing in `website-tracking-and-embed-snippets.md`).
   - Email 2 (2–3 days before): Short logistics + booth number reminder.
3. **Onsite Welcome Email (Branded MJML):** Ready for Constant Contact (`<MKT_ROOT>/templates/email-constant-contact.mjml`).
4. **Dedicated Event Landing Page Brief:** Follows the `/starnet` pattern in `website-tracking-and-embed-snippets.md` (GA4 `G-EJJJHWZFQQ`, HubSpot portal `51915935`, form fields aligned to HubSpot company properties, pre-filled Calendly iframe, reminder to attach GA4 `calendly_booking` listener).
5. **Post-Show Follow-Up Sequence (2–3 touches):** Day +2 thank-you + recap; Day +7 proof-led value follow-up; Day +14 soft close.
6. **LinkedIn Event Support:** 1 pre-event or post-event LinkedIn post fitting the standing weekly cadence.

## Validation

Run `python3 <MKT_ROOT>/scripts/validate_copy.py <output-file> --public --register external` (and `--register outreach` for 1:1 rep notes) and confirm every claim against `approved-messaging.md`. Save as `EVENT-CAMPAIGN-<slug>-YYYY-MM-DD.md` (draft only).
