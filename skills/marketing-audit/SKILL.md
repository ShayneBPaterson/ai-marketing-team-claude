---
name: marketing-audit
description: Run a full 5-subagent parallel marketing audit of jengai.com or a JENGAI landing page, scored 0-100 across 6 weighted dimensions and grounded in gtm-brain.
---

# JENGAI Full Marketing Audit (`/marketing audit <url>`)

Launches JENGAI's 5 parallel audit subagents (`marketing-content`, `marketing-conversion`, `marketing-competitive`, `marketing-technical`, `marketing-strategy`), aggregates their 0–100 scores, and produces an internal leadership audit at `MARKETING-AUDIT.md`.

## Mandatory Pre-Flight

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md`. Confirm the target URL (default: `https://www.jengai.com`, or specific pages like `/starnet`, `/demo`). Do not run generic e-commerce/creator business-type detection — JENGAI is a B2B vertical SaaS pricing and operations platform for commercial finish-trade subcontractors.

## Phase 1: Discovery
1. Run `python3 <MKT_ROOT>/scripts/analyze_page.py <url> --sitemap --max-pages 15` to collect technical, heading, schema, CTA, and JENGAI tracking stack data.
2. Fetch key pages (homepage, `/starnet`, `/demo`, success stories, product pages) so all 5 subagents analyze live copy.
3. Check if existing reports exist in the working directory (`COMPETITOR-REPORT.md`, `SEO-AUDIT.md`, `LANDING-CRO.md`, `BRAND-VOICE-AUDIT.md`) to cross-reference.

## Phase 2: Parallel Subagent Execution
Launch all 5 subagents in `agents/` simultaneously:
1. **`marketing-content`** → Content & Messaging (25% weight, 0–100)
2. **`marketing-conversion`** → Conversion Optimization (20% weight, 0–100)
3. **`marketing-technical`** → SEO & Technical Foundations (20% weight, 0–100)
4. **`marketing-competitive`** → Competitive Positioning (15% weight, 0–100)
5. **`marketing-strategy`** → Brand & Trust (10% weight, 0–100) + Growth & Strategy (10% weight, 0–100)

## Phase 3: Unified Scoring & Synthesis

```
Overall Score =
  (Content & Messaging * 0.25) +
  (Conversion Optimization * 0.20) +
  (SEO & Technical Foundations * 0.20) +
  (Competitive Positioning * 0.15) +
  (Brand & Trust * 0.10) +
  (Growth & Strategy * 0.10)
```

| Score Range | Grade | Meaning |
| --- | --- | --- |
| 85–100 | A | Strong — minor optimizations only |
| 70–84 | B | Good — clear, focused improvements available |
| 55–69 | C | Average — notable gaps affecting pipeline or clarity |
| 40–54 | D | Below average — priority rework needed |
| 0–39 | F | Critical — fundamental positioning, tracking, or SEO issues |

## No-Fabrication Rule
- **Never invent monthly traffic, conversion rates, or `\$XX,XXX/mo` revenue lift.**
- If the operator supplies GA4 / HubSpot / Salesforce baselines (or invokes `salesforce-data` / `hubspot-data`), show transparent sensitivity math grounded in those real numbers. Otherwise prioritize fixes by effort and funnel bottleneck without fake dollar projections.

## Output: `MARKETING-AUDIT.md`
Write in `gtm-specific-voice.md`'s **Internal reports & audits** register (complete sentences, plain words, "in reality" instead of "in practice", JENGAI full caps, US dates `MM/DD/YYYY` in tables). Include:
1. Executive summary (score, top 3 strengths, top 3 fixes)
2. Unified 6-category score breakdown table
3. Prioritized action plan: Quick wins (this week), Medium-term (this month), Strategic (this quarter)
4. Detailed findings from all 5 subagents
5. Open data requests (GA4, HubSpot, Salesforce, PageSpeed Insights)

Run `python3 <MKT_ROOT>/scripts/validate_copy.py MARKETING-AUDIT.md --register internal` before finishing. Suggest `/marketing report-pdf` (rendered to SharePoint) if Renata or Shayne want a formatted PDF copy.
