---
name: marketing-report
description: Compile all completed JENGAI marketing audits into a unified internal leadership report in Markdown for Renata and Shayne, using consistent filenames, unified 0-100 scoring, and zero fabricated revenue numbers.
---

# JENGAI Internal Marketing Report (`/marketing report`)

Compiles available JENGAI audit artifacts into a single executive Markdown report written for **Renata (CMO)** and **Shayne (Founder & Sales)** in `gtm-specific-voice.md`'s **Internal reports & audits** register.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md`
2. `gtm-knowledge/gtm-specific-voice.md` (Internal reports & audits section)
3. `marketing/status.md`

## Canonical Input Filenames (Fixed Cross-Skill Alignment)

Check the working directory for these exact artifacts produced by the `marketing-*` skills:
- `MARKETING-AUDIT.md` (from `/marketing audit`)
- `SEO-AUDIT.md` (from `/marketing seo`)
- `LANDING-CRO.md` (from `/marketing landing`)
- `BRAND-AUDIT.md` (from `/marketing brand`)
- `COMPETITOR-REPORT.md` (from `/marketing competitors`)
- `FUNNEL-ANALYSIS.md` (from `/marketing funnel`)
- `COPY-SUGGESTIONS.md` (from `/marketing copy`)
- `SOCIAL-CALENDAR.md` (from `/marketing social`)
- `EMAIL-SEQUENCES.md` (from `/marketing emails`)
- `AD-CAMPAIGNS.md` (from `/marketing ads`, if a test was explicitly commissioned)

If no prior audit exists, recommend running `/marketing audit https://www.jengai.com` first.

## Unified Scoring Rubric (Matches `marketing-audit` 100%)

| Category | Weight | Source |
| --- | --- | --- |
| Content & Messaging | 25% | `marketing-content` / `COPY-SUGGESTIONS.md` |
| Conversion Optimization | 20% | `marketing-conversion` / `LANDING-CRO.md` / `FUNNEL-ANALYSIS.md` |
| SEO & Technical Foundations | 20% | `marketing-technical` / `SEO-AUDIT.md` |
| Competitive Positioning | 15% | `marketing-competitive` / `COMPETITOR-REPORT.md` |
| Brand & Trust | 10% | `marketing-strategy` / `BRAND-AUDIT.md` |
| Growth & Strategy | 10% | `marketing-strategy` / `marketing/status.md` |

## Reporting Rules

- **No agency sales pitch tone.** Write as an accountable internal JENGAI team member ("we", "our") reporting plainly to leadership.
- **No fabricated revenue projections.** Only include pipeline/revenue sizing when backed by live figures from `core-brain/skills/salesforce-data/` or `hubspot-data/`. Otherwise state what data is missing.
- **Formatting:** Sentence case headings, US dates (`MM/DD/YYYY`) in tables, full numbers (no `\$19.1M` abbreviations), JENGAI in full caps, "in reality" instead of "in practice", lists of 1 or 3 items where practical.

## Output: `MARKETING-REPORT.md`

Include: Executive summary, Unified 6-category scorecard, Top 3 priority actions, Category deep-dives, Competitive snapshot (internal only), SEO & tracking snapshot, Prioritized action plan (This week / This month / This quarter), and Live data gaps to close.

Run `python3 <MKT_ROOT>/scripts/validate_copy.py MARKETING-REPORT.md --register internal`. Offer `/marketing report-pdf` (writing directly to SharePoint) if a formatted PDF is needed.
