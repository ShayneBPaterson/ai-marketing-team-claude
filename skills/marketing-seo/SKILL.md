---
name: marketing-seo
description: Perform a multi-page SEO audit of jengai.com (sitemap crawl, Core Web Vitals LCP/INP/CLS, JSON-LD schema, and finish-trade keyword clusters) aligned to JENGAI's pricing and operations positioning.
---

# JENGAI SEO Content & Technical Audit (`/marketing seo <url>`)

Audits `jengai.com` (`jengai-com/public-website`) across on-page SEO, sitemap health, Core Web Vitals (**LCP, INP, CLS** — never deprecated FID), structured data, and commercial finish-trade keyword strategy.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` and `<MKT_ROOT>` (`<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root) via `<MKT_ROOT>/context/gtm-brain-map.md` and read:
1. `gtm-knowledge/messaging-and-value-proposition.md` and `marketing/outputs/messaging/approved-messaging.md`
2. `gtm-knowledge/icp.md`
3. `marketing/knowledge/website-tracking-and-embed-snippets.md`
4. `marketing/knowledge/website-success-stories/README.md`

## Positioning Guardrail for SEO (Critical)

- **Never recommend primary titles, H1s, or positioning statements that categorize JENGAI as an estimating or takeoff tool** (e.g., do not recommend `"AI Estimating & Bidding Software"` as JENGAI's category definition — Renata's 2026-08-31 decision retired that framing).
- **Target real commercial finish-trade search demand cleanly:**
  - Core platform cluster: commercial subcontractor pricing and operations software, commercial flooring bid management software, specialty contractor bid pipeline CRM, commercial subcontractor proposal software.
  - Trade-vertical cluster: commercial flooring bid management, commercial tile and stone bid software, finish-trade pre-construction operations.
  - Problem/workflow cluster: automated finish schedule analysis, BuildingConnected bid workflow for subcontractors, multi-GC proposal generator for subcontractors.
- **Note search volume honesty:** Never invent search volume numbers. Classify potential qualitatively (High/Medium/Low) and flag Google Search Console / Ahrefs lookup as required before committing to a multi-month content build.

## Execution Process

### Step 1: Run Automated Multi-Page Crawl
```bash
python3 <MKT_ROOT>/scripts/analyze_page.py https://www.jengai.com --sitemap --max-pages 20
```
If `PSI_API_KEY` is configured, append `--psi-key "$PSI_API_KEY"` for real LCP, INP, and CLS metrics.

### Step 2: Audit 6 SEO Areas
1. **On-page checklist (homepage + key interior pages):** Title tag (50–60 chars, positioning-compliant), meta description (140–160 chars, approved proof + CTA), single clean H1, clean H2–H3 hierarchy (zero UI-chrome headings like cookie banners), image alt text and below-fold `loading="lazy"`.
2. **Sitemap & internal linking:** Compare `sitemap.xml` URLs against homepage links; map "Insights from the field" blog posts and standalone customer success stories (`jengai.com/success-stories/...`) back to product/demo pages.
3. **Core Web Vitals:** Report real PSI metrics if captured, else mark `Not measured — run PageSpeed Insights` and flag likely LCP/CLS risks (unlazy-loaded images, heavy scripts). Benchmarks: LCP < 2.5s, **INP < 200ms**, CLS < 0.1.
4. **JSON-LD Structured Data:** Check and provide copy-pasteable JSON-LD for `Organization`, `SoftwareApplication`, `Review` (for approved customer stories), `BreadcrumbList`, and `Article`.
5. **JENGAI Tracking Stack Check:** Verify GA4 (`G-EJJJHWZFQQ`), HubSpot (`51915935`), and note open GA4 event gaps from `website-tracking-and-embed-snippets.md`.
6. **PR-Ready Fixes for `jengai-com/public-website`:** Group recommendations into Critical (this week), High (this month), and Medium (this quarter) with exact HTML/meta/JSON-LD snippets ready to apply.

### Step 3: Validate & Save
Save to `SEO-AUDIT.md` (in Internal Reports register) and run:
```bash
python3 <MKT_ROOT>/scripts/validate_copy.py SEO-AUDIT.md --register internal
```
Ensure zero positioning violations or unapproved stats appear in recommended meta descriptions or titles.
