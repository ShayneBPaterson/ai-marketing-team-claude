# SEO Content Audit
## https://www.jengai.com
### Date: 2026-08-19

---

## SEO Health Score: 48/100

Solid technical foundation (robots.txt, sitemap, canonical, HTTPS, viewport) undercut by on-page fundamentals: no H1, a meta description less than half the usable length, 38% of images missing alt text, and a title tag chasing a compound keyword almost nobody searches for.

---

## On-Page SEO Checklist

### Title Tag
- Status: **Needs Work**
- Current: `"AI CRM-Estimation Suite for Commercial Subcontractors | JENGAI"` (62 characters)
- Recommended: `"AI Estimating & Bidding Software for Subcontractors | JENGAI"` (60 characters)
- Issues:
  - 2 characters over the 60-char display limit — will clip on some SERP layouts
  - "CRM-Estimation Suite" is an invented compound term with ~zero search volume; nobody types "CRM-estimation" into Google
  - Splits keyword equity across three concepts (CRM + estimation + suite) instead of targeting one term people actually search

### Meta Description
- Status: **Fail**
- Current: `"Turn Estimation & Bidding into your Competitive advantage with the power of AI"` (79 characters)
- Recommended: `"JENGAI helps commercial subcontractors estimate 40% faster and win more bids with AI-powered pre-construction software. Request a demo today."` (~148 characters)
- Issues:
  - Uses less than half of the available 150–160 character SERP real estate — leaving free ad space unclaimed
  - No explicit call to action
  - No concrete proof point (the homepage itself has a "40% Faster Estimation" stat sitting unused)

### Heading Hierarchy
- Status: **Fail**
- **No H1 tag found anywhere on the page.** This is the single highest-impact fix on the site — Google uses the H1 as one of the strongest on-page relevance signals, and this page has none.
- H2s and H3s are present but structurally messy:
  - "LOVED BY INDUSTRY LEADERS" appears as an **H2 twice** (duplicate heading)
  - A cookie-consent string, `"We value your privacy"`, is marked up as an **H3** — this is UI chrome, not content, and dilutes the heading outline search engines parse
  - The real value proposition — `"Turn Estimation & Bidding Into Your Competitive Advantage with the power of AI"` — is buried as an H3 instead of the H1
- Fix: promote the hero headline to a single H1, remove the duplicate H2, and strip non-content strings (cookie banner, privacy text) out of the heading hierarchy entirely.

### Image Optimization
- Status: **Fail**
- 63 images on the page, **24 (38%) missing alt text** entirely
- 0 images using lazy loading — every image loads on initial page fetch, which drags down Largest Contentful Paint (LCP) and total page weight on a homepage with this many images
- Recommendation: add descriptive alt text to all 24 images (partner/client logos should use `alt="[Company] logo"`; case study photos should describe the context), and lazy-load everything below the fold

### Internal Linking
- Status: **Pass**
- 47 internal links / 74 total links — healthy ratio, no signs of orphaned navigation
- Footer nav is organized into Solutions / Company / Resources clusters, which is good topical grouping
- Opportunity: the "Insights from the field" blog teaser links out to only a few articles — once more blog content exists, add more contextual in-body links from blog posts back to the estimation/bidding/CRM product pages

### URL Structure
- Status: **Pass**
- Root domain (`jengai.com`), HTTPS, self-referencing canonical to `https://www.jengai.com/` — clean

---

## Content Quality (E-E-A-T)

| Dimension | Score | Evidence |
|---|---|---|
| Experience | Present | Named client case studies with specific, credible results ("Axis," "SSG," "Transylvania Flooring Professionals") and concrete numbers (40% faster estimation, 50% faster pricing, 100% accuracy, "triples its business") — this is genuinely strong proof-of-experience content, just under-leveraged (buried in H3s, not surfaced as standalone case-study pages with schema) |
| Expertise | Weak | Homepage has no visible author bylines or credentialed team info. A blog ("Insights from the field") is referenced, which is where expertise signals should live — worth auditing separately once blog URLs are known |
| Authoritativeness | Weak | Partner/client logos exist ("LOVED BY INDUSTRY LEADERS") but no visible awards, press mentions, or industry certifications on the homepage. Client logos are good social proof but weaker than named backlinks or third-party coverage |
| Trustworthiness | Present | HTTPS enabled, cookie-consent flow present, social profiles live (Facebook, X/Twitter, LinkedIn, Instagram, YouTube — 5 platforms, good signal). Footer has Company/Resources sections, but no privacy policy or terms link was captured in this scan — verify those exist and are linked from the footer |

---

## Keyword Analysis
- **Primary keyword target (inferred from title):** "AI CRM-estimation suite" — this is a made-up compound phrase, not a real search term
- **Recommended primary keyword:** something in the actual search-demand cluster subcontractors use, e.g. *"construction estimating software"*, *"subcontractor bidding software"*, or *"pre-construction software for subcontractors"* — pick based on real keyword-volume data, but the current title targets none of them
- **Search intent:** Homepage is commercial-investigation / navigational (branded product page) — content matches that intent structurally (demo CTA, feature highlights, social proof), the problem is purely which keyword the title/meta/H1 are built around
- **Keyword placement today:** not present in H1 (no H1 exists), not in meta description, only loosely present in title
- **Secondary keyword candidates to work into subheadings and body copy:**
  - "estimation software for commercial subcontractors"
  - "AI bid management"
  - "construction pre-construction software"
  - "flooring/stone/tile estimating software" (JENGAI's actual named verticals — high relevance, likely low competition)
  - "estimation accuracy software"

---

## Technical SEO

| Check | Status | Notes |
|---|---|---|
| robots.txt | Pass | Exists, references sitemap. Notably includes AI-content-signal directives (`Content-Signal`) — an emerging standard for controlling AI crawler/training access, worth confirming this is configured intentionally |
| XML sitemap | Pass | Exists, 61 URLs indexed |
| Canonical tag | Pass | Self-referencing, correctly pointed at `https://www.jengai.com/` |
| Viewport meta | Pass | Present — page declares mobile-responsive intent |
| Schema markup | Needs Work | Only `WebPage` schema detected. No `Organization`, `SoftwareApplication`/`Product`, `Review`/`AggregateRating`, `FAQPage`, or `BreadcrumbList` — given the case-study content already on the page, `Review` schema is a quick, high-value win |
| Core Web Vitals | Not measured | This audit's script doesn't capture LCP/CLS/INP directly — recommend running PageSpeed Insights or Lighthouse on `jengai.com` as a follow-up. Given 63 unoptimized/non-lazy images, LCP is the most likely metric at risk |
| Tracking | Pass | Google Analytics (gtag) + Google Tag Manager both detected — measurement stack is in place |

---

## Content Gap Analysis

| Missing Topic | Search Volume Potential | Competition | Content Type Needed | Priority |
|---|---|---|---|---|
| "[Trade] estimating software" (stone/tile/flooring specifically) | Medium | Low | Landing page per vertical | 1 |
| "JENGAI vs [competitor]" comparison content | Medium | Medium | Comparison page | 2 |
| Individual case study pages (Axis, SSG, Transylvania Flooring) as standalone URLs | Low-Med | Low | Case study page w/ Review schema | 2 |
| "How AI estimating works" / methodology explainer | Medium | Medium | Guide/blog post | 3 |
| Pricing/ROI calculator content | Low-Med | Low | Interactive page or guide | 3 |

---

## Featured Snippet Opportunities
- The stat block ("40% Faster Estimation," "50% Faster Pricing," "100% Accuracy") is snippet-ready but currently sits in unstructured H3s with no supporting paragraph — reformat as: H2/H3 question ("How much faster is estimation with JENGAI?") → 40-60 word answer paragraph citing the case study
- Case studies ("How This New Hampshire Based Company Eliminated Estimation Mistakes") are natural fits for list-snippet or table-snippet formatting once they're their own indexable pages

---

## Schema Markup

| Schema Type | Applicable To | Status |
|---|---|---|
| Organization | Homepage | Missing |
| SoftwareApplication / Product | Homepage / product pages | Missing |
| Review / AggregateRating | Case study sections | Missing — highest-value gap given existing content |
| FAQPage | If FAQ content exists elsewhere | Missing/N/A — verify |
| BreadcrumbList | Interior pages | Missing |
| WebSite / SearchAction | Homepage | Missing |

---

## Internal Linking Opportunities
- No orphan pages detected from this crawl, but sitemap (61 URLs) vs. homepage internal links (47) suggests some interior pages aren't linked directly from the homepage — worth a full site crawl to confirm
- Once case studies get standalone URLs, link to them from the homepage proof section, from the blog, and from relevant product pages
- Blog → product page links: ensure every blog post links back to the relevant estimation/bidding feature page (cluster-to-pillar linking)

---

## Core Web Vitals
Not directly measured by this audit — flagged as a follow-up. Given 63 total images and zero lazy loading detected, LCP is the metric most likely to be underperforming. Recommend running Lighthouse/PageSpeed Insights before prioritizing a broader performance pass.

---

## Content Strategy Recommendations
1. **Publishing cadence:** Given "Insights from the field" already exists as a blog category, 2-4 posts/month targeting the vertical-specific keywords (stone, tile, flooring estimating) is a low-competition opportunity
2. **Content types:** Convert existing case studies into standalone, schema-marked pages before writing new content — this is reusing proof that already exists rather than creating from scratch
3. **Keyword targeting:** Prioritize the named trade verticals (flooring, tile, stone) over generic "construction software" terms — lower volume, but far lower competition and higher buyer intent
4. **Content update:** Homepage copy/heading structure should be fixed before new content is built on top of it — an H1-less homepage undermines topical authority signals for everything else on the domain
5. **Distribution:** 5 active social profiles exist — confirm case study and blog content is actually being pushed through them once produced

---

## Prioritized Recommendations

### Critical (Fix Immediately)
1. **Add an H1 tag** to the homepage using the actual value proposition, targeting a real search term — no-cost, highest-leverage fix on the page
2. **Rewrite the meta description** to use the full 150-160 character allowance with a concrete stat and a CTA — currently wasting free SERP real estate
3. **Add alt text to the 24 images missing it** — accessibility and image-search win, near-zero effort

### High Priority (This Month)
1. Rework the title tag off "CRM-Estimation Suite" onto a real, search-demand keyword
2. Remove the duplicate H2 and the cookie-banner text currently marked up as an H3
3. Add `Review`/`AggregateRating` schema to the existing case-study content
4. Enable lazy loading on below-fold images to protect LCP

### Medium Priority (This Quarter)
1. Convert the three case studies (Axis, SSG, Transylvania Flooring) into standalone, indexable pages
2. Add `Organization` and `SoftwareApplication` schema
3. Build vertical-specific landing pages (stone/tile/flooring estimating software)
4. Run a full Lighthouse/PageSpeed audit to quantify Core Web Vitals

### Low Priority (When Resources Allow)
1. Build comparison content ("JENGAI vs. [competitor]")
2. Add FAQ content + `FAQPage` schema if there's demand for it
3. Full-site internal link audit to confirm no orphaned pages among the 61 sitemap URLs

---

*Automated data collected via `scripts/analyze_page.py`. Core Web Vitals and full-site crawl were not part of this pass — recommended as a fast follow-up.*
