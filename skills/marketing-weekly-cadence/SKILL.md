---
name: marketing-weekly-cadence
description: Draft JENGAI's standing weekly marketing cadence (1 LinkedIn post and 1 Constant Contact nurture email) from the active quarterly content calendar, approved messaging, and voice rules. Draft only; awaits Renata (CMO) approval.
---

# JENGAI Weekly Cadence Drafting (`/marketing weekly-cadence`)

Operationalizes JENGAI's standing weekly marketing cadence (`marketing/CLAUDE.md` and `marketing/agents/marketing-cmo.md`): **1 LinkedIn post + 1 Constant Contact nurture email per week**, built so Renata (CMO) can review and approve in under 30 minutes.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `marketing/status.md` (confirm which quarterly calendar file is active and check open content flags)
2. Active quarterly calendar (e.g., `marketing/outputs/campaigns/content-calendar-q3-q4-2026.md`)
3. `marketing/outputs/messaging/approved-messaging.md` and `gtm-knowledge/messaging-and-value-proposition.md`
4. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` and `gtm-knowledge/gtm-specific-voice.md`
5. `marketing/campaigns/2026-08-content-calendar-hook-rework/findings-2026-08-01-growth-story-sourcing.md`
6. `marketing/knowledge/visual-brand-guide.md` (In email section, if drafting MJML)

## Non-Negotiable Constraints

- **Draft only, always.** Never post, publish, or send. Approval by **Renata (CMO)** is the default release gate (**Shayne** sign-off additionally required for Shayne founder-voice posts and open compliance calls).
- **Strict cadence:** Produce 1 LinkedIn post + 1 Constant Contact nurture email per requested week. Never propose daily posting schedules or multi-platform flooding.
- **Positioning lock:** JENGAI is a pricing and operations platform for commercial specialty contractors — never an estimating or takeoff tool.
- **Approved proof only:** Cite only Bonitz (40% faster takeoff turnaround via APA), Pro-United Inc. (1 estimation error in 3 years), Silver Slate Group (revenue tripled; net profit margin well above industry standard), Transylvania Flooring Professionals (30–40% increase in bids sent), Axis Interior Systems (moved off Excel; improved accuracy, centralized project data), and the \$15,000+ error-cost claim.
- **Hook-first standard:** Open with a concrete number or named non-competitor growth story hitting one of the three emotional buttons: **Find work**, **Win more work**, or **Make more money**.
- **Public compliance:** Never name direct monitored competitors (STACK, Bobyard, MeasureSquare CRM, Kreo, Togal.AI, 1build/Handoff) or Garmon & Company. Flag any PlanHub reference explicitly for Renata/Shayne review.
- **Link check (`2026-11-21` audit):** `https://www.jengai.com/success-stories` returned HTTP 404 in the 2026-11-21 site audit. Verify it is live before linking it; until restored, use `https://www.jengai.com/demo` or a verified live customer story URL.

## Execution Workflow

1. **Locate the target calendar row** (or accept raw founder/CMO material such as a video transcript, customer win, or event theme).
2. **Select voice register:**
   - **JENGAI company voice** (trusted finish-trade peer, identity marketing: "buy this" → "be this"),
   - **Renata CMO/Founder voice** (co-founder and finish-trade peer perspective, plain language, customer-story focus), or
   - **Shayne founder voice** (CEO-to-CEO, specific storytelling, short connected paragraphs, humble confidence — requires Shayne sign-off).
3. **Draft the LinkedIn post:**
   - Structure: Hook (number or named story) → Problem → Solution → Proof → Soft CTA ("Book a demo" at `https://www.jengai.com/demo` or a verified live customer story link).
   - Best publish window: Tue–Thu 8:00–11:00 AM ET.
4. **Draft the Constant Contact nurture email:**
   - Subject line (normal sentence case, concrete hook, under 55 chars) + preview text.
   - Body: 150–250 words, flowed paragraphs, Problem → Solution → Proof or Before/After, single primary CTA ("Book a demo" → `https://www.jengai.com/demo` or `/starnet`).
   - Optionally generate branded MJML from `<MKT_ROOT>/templates/email-constant-contact.mjml` (`#020133` header band, `#000180` pill CTA, `#d0ffa3` spark only, Inter font).
5. **Run mandatory validation** (use `python` on Windows if `python3` is not installed):
   ```bash
   python3 <MKT_ROOT>/scripts/validate_copy.py <draft-file> --public --register external
   ```
   Complete `pre-publish-checklist.md` line by line and fix every error before returning.

## Output

Save using `<MKT_ROOT>/templates/weekly-cadence-pack.md` as `WEEKLY-CADENCE-YYYY-MM-DD.md` (or inside `marketing/outputs/campaigns/email-drafts/` when working inside `gtm-brain`). Mark clearly: `STATUS: DRAFT — AWAITING RENATA (CMO) APPROVAL` (plus Shayne sign-off when using Shayne founder voice; notify via Microsoft Teams).
