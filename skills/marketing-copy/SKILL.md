---
name: marketing-copy
description: Write or rewrite JENGAI website, landing page, or collateral copy grounded in approved-messaging.md, headline-bank.md, feature-value-mapping.md, identity marketing, and pre-publish voice rules.
---

# JENGAI Copywriting & Messaging Engine (`/marketing copy`)

Analyzes existing JENGAI copy or drafts new website/landing/collateral copy strictly grounded in `gtm-brain`. Every line complies with Renata's 2026-08-31 positioning lock and passes `<MKT_ROOT>/scripts/validate_copy.py`.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `gtm-knowledge/messaging-and-value-proposition.md`
2. `marketing/outputs/messaging/approved-messaging.md`
3. `marketing/outputs/messaging/headline-bank.md`
4. `gtm-knowledge/feature-value-mapping.md` (note unshipped `Bid Version History` and coined product names)
5. `gtm-knowledge/icp.md`
6. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` and `gtm-knowledge/gtm-specific-voice.md`

## Copy Principles for JENGAI

- **Positioning lock:** Always position JENGAI as a **pricing and operations platform for commercial specialty contractors**. Never describe JENGAI as an estimating or takeoff tool. When referencing estimation speed, use the approved always-on junior estimator analogy or Bonitz's exact proof ("40% faster takeoff turnaround via Automated Plan Analysis (APA)").
- **Identity marketing ("buy this" → "be this"):** Write to who the contractor becomes once JENGAI is running — an owner who sees slow seasons coming months ahead, a sales team back in front of customers instead of buried in spreadsheets, an estimating team focused on the right jobs.
- **Buyer personas:** Tailor to Owner/President, Head of Estimation, and Head of Sales in commercial flooring, stone, and tile (\$4M+ revenue, self-performing takeoffs). Do not draft Project Manager value props (outside product scope per `approved-messaging.md`).
- **Hard claim bans:** Never claim JENGAI "eliminates errors," "50% faster pricing," "100% accuracy guarantee," per-bid win-probability scoring, "catches hidden risks," or "protects institutional knowledge." Never invent customer counts.
- **CTA discipline:** Default CTA is `"Book a demo"` (or `"Schedule a discovery call"` for `/starnet`-style pages). Keep headlines from `headline-bank.md` distinct from CTA buttons.

## Execution Process

1. **If given a URL:** Fetch the live page and extract title, meta description, H1, subhead, section headers, body copy, CTAs, and proof points. Run `validate_copy.py` on existing copy to surface positioning drift or banned claims.
2. **If given a brief:** Confirm target page type (homepage, `/starnet` or trade vertical page, product/feature section, `/demo`, or collateral), primary persona, and primary message pillar.
3. **Draft / Rewrite:**
   - Score existing copy 0–100 (Positioning & ICP clarity, Claim governance, Pillar/identity strength, Voice compliance, CTA clarity).
   - Provide **Before / After / Why** rewrites for headline, subhead, primary CTA, body section, and meta description.
   - Provide a **curated headline swipe set** pulled from or aligned with `headline-bank.md` (sentence case per `visual-brand-guide.md`, JENGAI in full caps).
4. **Mandatory Validation:** Save to `COPY-SUGGESTIONS.md` and run:
   ```bash
   python3 <MKT_ROOT>/scripts/validate_copy.py COPY-SUGGESTIONS.md --public --register external
   ```
   Complete `pre-publish-checklist.md` (including cutting ~20% bloat while keeping complete sentences and 1- or 3-item lists).
