---
name: marketing-brand
description: Audit any JENGAI webpage, draft, email, or visual asset for strict compliance with JENGAI's documented voice rules, positioning lock, approved messaging, and Design System v2 visual brand guide.
---

# JENGAI Brand & Visual Compliance Audit (`/marketing brand <url/file>`)

Instead of trying to guess an unknown brand's personality, this skill audits any JENGAI webpage, document, deck, or email against JENGAI's **established** voice and visual standards in `gtm-brain`.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` via `context/gtm-brain-map.md` and read:
1. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md`
2. `core-brain/how-we-work/ai-conventions/pre-publish-checklist.md`
3. `gtm-knowledge/gtm-specific-voice.md`
4. `marketing/outputs/messaging/approved-messaging.md` and `marketing/outputs/messaging/headline-bank.md`
5. `marketing/knowledge/visual-brand-guide.md` (and `core-brain/skills/jengai-design-system/` for UI/HTML reviews)

## Audit Dimensions (Scored 0–100)

1. **Positioning & Claim Integrity (30 pts):** Pricing and operations platform (never estimating/takeoff tool); only 5 approved customers + \$15,000+ claim; zero on-hold or banned claims; JENGAI always full caps.
2. **Voice & Register Alignment (30 pts):** Runs `python3 scripts/validate_copy.py <target> --public` + checks complete sentences, explicit connections, 1- or 3-item lists, zero AI/corporate words, identity marketing ("buy this" → "be this"), and correct register (External vs. Founder vs. Internal vs. Outreach).
3. **Visual Design System v2 Compliance (25 pts):**
   - Core palette: `#020133` deep header, `#000180` primary action, `#d0ffa3` lime as spark/accent **only** (never full background), `#18181f` ink, `#67697f` muted text, `#edeef1` borders.
   - Typography: **Inter**, **sentence case everywhere** (no Title Case in headings or table columns), proper hierarchy.
   - Wordmark integrity: whole, unstretched, approved variants, ≥64px width, cap-height clear space.
   - Email rules (if email): solid `#020133` header band, one `#000180` pill CTA, `#d0ffa3` spark only.
4. **Format Conventions (15 pts):** US dates `MM/DD/YYYY` in UI/tables (`YYYY-MM-DD` in filenames), 12-hour AM/PM time, full numbers (`\$19,177,098` — never `\$19.1M`), acronyms spelled out on first use.

## Output: `BRAND-AUDIT.md`

Produce a clear internal compliance report with:
- Overall Brand Compliance Score (0–100)
- `validate_copy.py` findings
- Exact visual/CSS token mismatches (if HTML/URL/email)
- Line-by-line Before/After fixes
- Sign-off checklist for Renata / Berwyn

Run `python3 scripts/validate_copy.py BRAND-AUDIT.md --register internal`.
