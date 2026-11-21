# JENGAI AI Marketing Team

JENGAI's internal AI marketing suite for Claude Code and Codex, built for **Renata Doralieva-Paterson (Founder & CMO)** and **Berwyn San Juan (Marketing Associate)**, and anchored directly to `jengai-corp/gtm-brain` as the single source of truth.

## Guardrails Built Into Every Skill

- **Positioning lock (2026-08-31):** JENGAI is a **pricing and operations platform for commercial specialty contractors**. JENGAI is **not** an estimating or takeoff tool.
- **ICP lock:** Owners and Presidents (influenced by Heads of Estimation and Sales) at US and Canada commercial finish-trade subcontractors (stone, tile, flooring) with **\$4M+ annual revenue** who self-perform takeoffs, concentrated in **FUSE Alliance, Starnet Worldwide, and Commercial USA**.
- **Strict proof-point governance:** Only the five approved customer stories in `approved-messaging.md` (Bonitz, Pro-United Inc., Silver Slate Group, Transylvania Flooring Professionals, Axis Interior Systems) plus the standing \$15,000+ error-cost claim. Every customer-facing draft passes `scripts/validate_copy.py`.
- **Draft-only approval gate:** Nothing posts, sends, or publishes automatically. All outbound drafts await explicit Renata or Shayne approval (notified via Microsoft Teams).
- **No binaries in git and no external hosting:** PDFs and visual deliverables write directly to SharePoint (`AI_Marketing_Outputs/...`) via `core-brain/scripts/sharepoint_path.py` with a `.sharepoint.md` breadcrumb in the repo. Never publish to `claude.ai`.
- **Sales boundary:** Subscription proposals (`sales/skills/sales-proposal/`), live sales call scripts, and deal-closing outreach stay with Sales (Shayne, Zhai, Aica).

---

## Commands (`marketing-*`)

### Core Weekly Operations & JENGAI Campaigns

| Command | Skill | Purpose |
|---|---|---|
| `/marketing weekly-cadence [week]` | `marketing-weekly-cadence` | Draft the week's 1 LinkedIn post + 1 Constant Contact nurture email from the active quarterly calendar |
| `/marketing case-study <customer>` | `marketing-case-study` | Convert a customer story or transcript into a web page (`Review` schema), sales 1-pager, LinkedIn post, and nurture email |
| `/marketing event <event>` | `marketing-event` | Build Starnet, FUSE Alliance, or Commercial USA event kits (pre-show, onsite MJML, `/starnet`-style landing brief, post-show) |
| `/marketing workshop <topic>` | `marketing-workshop` | Build Owner AI Workshop or customer webinar packages |
| `/marketing voice-check <file>` | `marketing-voice-check` | Run deterministic copy linter (`scripts/validate_copy.py`) + `pre-publish-checklist.md` |

### Audits, Content, Intelligence & Reporting

| Command | Skill | Purpose |
|---|---|---|
| `/marketing audit <url>` | `marketing-audit` | Full 5-subagent parallel audit (`marketing-content`, `marketing-conversion`, `marketing-competitive`, `marketing-technical`, `marketing-strategy`) |
| `/marketing quick <url>` | `marketing` | 60-second page snapshot (under 30 lines) |
| `/marketing copy <url/brief>` | `marketing-copy` | Write or rewrite copy grounded in `approved-messaging.md`, `headline-bank.md`, and identity marketing |
| `/marketing emails <campaign>` | `marketing-emails` | Draft Constant Contact nurture, product release, event, or case-study sequences (+ Design System v2 MJML) |
| `/marketing social [quarter]` | `marketing-social` | Scaffold weekly LinkedIn calendars and draft founder-voice or brand-voice posts (1/week cadence) |
| `/marketing seo <url>` | `marketing-seo` | Multi-page sitemap SEO audit, LCP/INP/CLS check, JSON-LD schema, and PR-ready `public-website` fixes |
| `/marketing landing <url>` | `marketing-landing` | Landing page CRO + Design System v2 + GA4/HubSpot/Calendly tracking verification |
| `/marketing competitors <url>` | `marketing-competitors` | Compliance-checked competitor profile (1–5 threat rating, 0–100 matrix score, evidence ledger, `gtm-brain` propagation checklist) |
| `/marketing funnel [scope]` | `marketing-funnel` | Audit or complete JENGAI's TOFU → HubSpot → Calendly → Salesforce funnel |
| `/marketing brand <url/file>` | `marketing-brand` | Voice and Design System v2 compliance audit |
| `/marketing launch <feature>` | `marketing-launch` | Feature release or campaign launch playbook (verified against `product-state.md`) |
| `/marketing report` | `marketing-report` | Internal Markdown leadership report for Renata and Shayne |
| `/marketing report-pdf` | `marketing-report-pdf` | JENGAI-branded PDF report written straight to SharePoint `AI_Marketing_Outputs/` |
| `/marketing ads <test>` | `marketing-ads` | *(Parked / test-only — requires explicit Renata approval)* LinkedIn ABM + exact/phrase Google Search tests |

---

## Architecture

```text
ai-marketing-team-claude/
├── CLAUDE.md                        # Repo-level rules pointing to gtm-brain
├── context/gtm-brain-map.md         # Canonical router to gtm-brain & core-brain files
├── skills/                          # 19 skills (marketing + 18 marketing-* skills)
├── agents/                          # 10 agents (5 execution + 5 parallel audit subagents)
│   ├── marketing-cmo.md             # Weekly LinkedIn + Constant Contact cadence producer
│   ├── marketing-proof.md           # Customer case study & proof kit producer
│   ├── marketing-campaigns.md       # Events (Starnet/FUSE/Commercial USA), workshops & releases
│   ├── marketing-intel.md           # Compliance-checked competitor & growth-story scout
│   ├── marketing-editor.md          # Independent pre-publish voice, claim & visual gate
│   ├── marketing-content.md         # Audit: Content & Messaging (25%)
│   ├── marketing-conversion.md      # Audit: Conversion Optimization & Tracking (20%)
│   ├── marketing-technical.md       # Audit: Technical SEO & Web Stack (20%)
│   ├── marketing-competitive.md     # Audit: Competitive Positioning (15%)
│   └── marketing-strategy.md        # Audit: Brand & Trust (10%) + Growth & Strategy (10%)
├── scripts/
│   ├── validate_copy.py             # Deterministic JENGAI voice, positioning & claim linter
│   ├── analyze_page.py              # Sitemap-aware SEO, JENGAI stack & PageSpeed analyzer
│   ├── competitor_scanner.py        # robots.txt + compliance-registry competitor scanner
│   ├── social_calendar.py           # JENGAI weekly LinkedIn + Constant Contact scaffolder
│   ├── generate_pdf_report.py       # Design System v2 PDF generator with SharePoint routing
│   └── install-skills.mjs           # Cross-platform symlink installer + gtm-brain sync
├── templates/                       # 7 JENGAI-native markdown & MJML templates
├── tests/                           # Stdlib unittest suite (scripts + repo integrity)
└── archive/                         # Superseded pre-refactor outputs
```

---

## Installation (macOS, Linux & Windows)

### Option 1 (Recommended): Sync into `gtm-brain`
Drop the skills and subagents directly into `gtm-brain/marketing/` so Renata and Berwyn receive updates automatically through `core-brain/scripts/brain-skills.mjs`:

```bash
node scripts/install-skills.mjs sync-gtm-brain ../jengai-corp/gtm-brain --dry-run
node scripts/install-skills.mjs sync-gtm-brain ../jengai-corp/gtm-brain
cd ../jengai-corp/gtm-brain && node core-brain/scripts/brain-skills.mjs install
```

### Option 2: Install Directly From This Repo
Links skills into `~/.agents/skills/` → `~/.claude/skills/` and `~/.codex/skills/`, plus subagents into `~/.claude/agents/`:

```bash
export JENGAI_GTM_BRAIN=/path/to/gtm-brain
node scripts/install-skills.mjs install
```

Optional dependency for PDF generation:

```bash
pip install -r requirements.txt
```

## Verification

Run the automated test suite anytime after editing skills, scripts, or templates:

```bash
python3 -m unittest discover -s tests -v
```
