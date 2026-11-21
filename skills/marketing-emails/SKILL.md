---
name: marketing-emails
description: Draft JENGAI Constant Contact nurture emails, product release announcements, case-study email series, and event emails in JENGAI voice and Design System v2 MJML. Draft only.
---

# JENGAI Email Marketing Engine (`/marketing emails`)

Drafts JENGAI marketing emails built for **Constant Contact** (company standard) and aligned to JENGAI's Design System v2 visual email standard.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` via `context/gtm-brain-map.md` and read:
1. `marketing/outputs/messaging/approved-messaging.md` and `gtm-knowledge/messaging-and-value-proposition.md`
2. `marketing/knowledge/channels-and-cadence.md`
3. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` and `gtm-knowledge/gtm-specific-voice.md`
4. `marketing/knowledge/visual-brand-guide.md` (`In email` section)

## Supported JENGAI Email Types (No E-Commerce / Cart Abandonment)

| Sequence Type | Platform & Register | Use Case |
|---|---|---|
| **Weekly Nurture** | Constant Contact · External copy or Shayne founder voice | 1 email/week paired to the quarterly content calendar (finish-trade inbox is saturated — lead with numbers/stories hitting Find work, Win more work, or Make more money) |
| **Product Release** | Constant Contact · External copy | 2-email pair modeled on `2026-09-24-data-privatization-release-email` (Email 1: Coming soon; Email 2: Now live + walkthrough) |
| **Case Study Series** | Constant Contact · External copy | Multi-touch proof series modeled on `2026-09-28-case-study-email-series` featuring Bonitz, Pro-United, Silver Slate, Transylvania, or Axis |
| **Event Broadcast** | Constant Contact · External copy | Pre-show invite, onsite welcome, and post-show follow-up for Starnet, FUSE, and Commercial USA |
| **Workshop / Webinar** | Constant Contact · External copy | Owner AI Workshop invites, reminders, and replay delivery |

> **Sales boundary:** Cold BD outreach, proposal-sending emails, and deal resurrection sequences belong to Sales (Shayne, Zhai, Aica). If explicitly asked to draft a 1:1 rep email, switch strictly to `gtm-specific-voice.md`'s **Outreach & cold copy** register (`Dear [First Name],`, no contractions, association membership check, hyphenated role attribution, closing line before signature, never list product features in a resurrection email).

## JENGAI Visual Email Standard (MJML)

When HTML/MJML is requested, use `templates/email-constant-contact.mjml`:
- **Header:** Solid `#020133` band, left-aligned inverse `JENGAI` wordmark.
- **Primary CTA:** Single `#000180` pill button (`border-radius: 48px`), white label, default `"Book a demo"`.
- **Accent:** Lime `#d0ffa3` only as a small spark (dot or thin divider) — **never a background**.
- **Typography:** Inter, sentence case headings in `#020133`, body copy `#18181f`, muted footer `#67697f`.
- **Compliance:** Include physical address placeholder and Constant Contact unsubscribe token.

## Execution & Validation

1. Draft complete subject line (sentence case, concrete hook), preview text, body copy (1 email = 1 job, 1 primary CTA, complete sentences, lists of 1 or 3), and Constant Contact segmentation notes (e.g., Starnet vs. FUSE vs. Commercial USA vs. general commercial subs).
2. Save to `EMAIL-SEQUENCES.md` (and `.mjml` when requested).
3. Run:
   ```bash
   python3 scripts/validate_copy.py EMAIL-SEQUENCES.md --public --register external
   ```
   Mark clearly as `DRAFT — AWAITING RENATA/SHAYNE APPROVAL`.
