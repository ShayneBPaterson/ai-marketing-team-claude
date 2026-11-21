# JENGAI GTM Brain — Canonical Source Map

All `marketing-*` skills, subagents, and scripts treat `jengai-corp/gtm-brain` (and its `core-brain` submodule) as the single source of truth. Do not duplicate volatile company facts, customer counts, pricing, or competitor profiles into this repository.

## Locating `gtm-brain` (machine-agnostic)

Resolve `<GTM_BRAIN>` in this order on macOS, Linux, and Windows:

1. **Inside `gtm-brain`:** If the current working directory (or a parent directory) contains `gtm-knowledge/` and `core-brain/`, use that directory as `<GTM_BRAIN>`.
2. **Environment variable:** If `JENGAI_GTM_BRAIN` is set and points to a valid clone, use `$JENGAI_GTM_BRAIN`.
3. **Sibling checkout:** Check `../jengai-corp/gtm-brain` and `../gtm-brain` relative to this repository root.
4. **Unavailable:** If `<GTM_BRAIN>` cannot be reached on the current machine, stop before writing customer-facing claims and tell the operator to set `JENGAI_GTM_BRAIN` or clone `gtm-brain` with `--recurse-submodules`.

## Authoritative File Index

| Domain | Canonical Path (relative to `<GTM_BRAIN>`) | What It Governs |
|---|---|---|
| Company overview | `core-brain/company/overview.md` | High-level company context and stage (follow `messaging-and-value-proposition.md` for current positioning) |
| Product capabilities | `core-brain/company/product-overview.md` | Verified product modules and platform architecture |
| Users and workflows | `core-brain/company/users-and-workflows.md` | Product personas (Estimator, Business owner, Account admin, Global admin) and canonical bid / Automated Plan Analysis (APA) flows |
| Trade glossary | `core-brain/company/glossary.md` | Finish-trade and internal JENGAI terms |
| Company voice rules | `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` | Baseline writing rules, banned AI/corporate words, formatting, sentence rules |
| Pre-publish checklist | `core-brain/how-we-work/ai-conventions/pre-publish-checklist.md` | Line-by-line scan required before shipping any written work |
| GTM-specific voice | `gtm-knowledge/gtm-specific-voice.md` | Register rules for external marketing copy, founder voice (Shayne), internal reports, and outreach |
| Positioning and proof | `gtm-knowledge/messaging-and-value-proposition.md` | Short-form positioning lock (2026-08-31), 5 approved customer proof points, and banned/on-hold claims |
| Approved messaging | `marketing/outputs/messaging/approved-messaging.md` | Full copy source of truth, message pillars, team cards, competitive objections, and product-truth rules |
| Headline bank | `marketing/outputs/messaging/headline-bank.md` | Approved short headlines for backdrops, social posts, and ads (not CTA copy) |
| Feature-to-value map | `gtm-knowledge/feature-value-mapping.md` | Feature → persona → pain → value proposition table (observe unshipped and coined-name flags) |
| ICP | `gtm-knowledge/icp.md` | Single ICP definition (\$4M+ revenue floor, US/Canada, finish trades, FUSE/Starnet/Commercial USA, self-performs takeoff) |
| Pricing | `gtm-knowledge/pricing.md` | Current location + user pricing model (\$800/loc Starter, +\$300 Expert, \$75/\$100 seats, setup and onboarding) |
| Funnel and leads | `gtm-knowledge/funnel-stages-and-journey-maps.md` and `gtm-knowledge/lead-definitions-and-qualification-criteria.md` | Current placeholders mapping sales stages, Salesforce `StageName` values, and MQL/SQL criteria |
| Channels and cadence | `marketing/knowledge/channels-and-cadence.md` | Standing weekly cadence (1 LinkedIn post + 1 Constant Contact email), events, parked channels (paid ads, cold email, direct mail) |
| Positioning and pillars | `marketing/knowledge/positioning-and-pillars.md` | Three message pillars and monthly rotation model |
| Visual brand guide | `marketing/knowledge/visual-brand-guide.md` | Design System v2 tokens (`#000180`, `#020133`, `#d0ffa3` spark only, Inter, sentence case, `MM/DD/YYYY` dates, full numbers) |
| Website tracking | `marketing/knowledge/website-tracking-and-embed-snippets.md` | `jengai-com/public-website` tracking: GA4 (`G-EJJJHWZFQQ`), HubSpot (`51915935`), form IDs (`/starnet`, `/demo`), Calendly links, open tracking gaps |
| Competitor index | `marketing/knowledge/competitors/README.md`, `threat-assessment-matrix.md`, `all-known-competitors.md`, `top-10-funded-competitors.md` | Tracked competitor profiles, 1–5 threat rating, 0–100 matrix score, Tier H/M/L |
| Top 5 competitors | `marketing/outputs/competitive/top-five-competitors.md` | Call-ready summary for Bobyard, MeasureSquare, Kreo, Togal.AI, and 1build/Handoff |
| Collection compliance | `marketing/market-intelligence/settings.md` | Approved, owner-override, and excluded web sources; attribution rules; Azure crawler mirror rules |
| Marketing status | `marketing/status.md` | Active campaigns, current quarterly calendar filename, open blockers, and pending approvals |
| Content calendars | `marketing/outputs/campaigns/content-calendar-q3-q4-2026.md` (check `marketing/status.md` for active quarter) | Weekly LinkedIn and Constant Contact schedule and hook rework status |
| Growth-story hooks | `marketing/campaigns/2026-08-content-calendar-hook-rework/findings-2026-08-01-growth-story-sourcing.md` | Shayne's 3 emotional buttons (find work, win more work, make more money) and compliance flags |
| Case studies | `marketing/projects/2026-09-customer-case-studies/` and `marketing/knowledge/website-success-stories/` | Customer story templates, texts, and published success stories |
| Events | `marketing/events/2026/` | Starnet Fall Meeting, Starnet Tech Summit, AHSG Commercial USA Summit plans |
| Workshops | `marketing/campaigns/2026-08-owner-ai-workshops/` | Owner AI Workshops campaign plans and materials |
| Generated binary rules | `core-brain/how-we-work/ai-conventions/generated-binary-rules.md` | Mandatory SharePoint output routing (`AI_Marketing_Outputs/...`) and external-hosting ban |
| Skills convention | `core-brain/how-we-work/ai-conventions/skills-convention.md` | Skill placement, naming prefixes, machine-agnostic rules, and `brain-skills.mjs` installer |

## Shared Skills to Invoke (Do Not Duplicate)

When a marketing task requires live data or system access, invoke these canonical `core-brain` or `gtm-brain` skills rather than guessing:

- **`core-brain/skills/salesforce-data/`** — Live customer count, ARR, opportunity stages, churn signals, and association membership lookups (Starnet, FUSE, Commercial USA).
- **`core-brain/skills/hubspot-data/`** — Form submissions, marketing contacts, and landing page conversion counts.
- **`core-brain/skills/jengai-design-system/`** — Token and component checks for HTML emails, landing pages, and decks.
- **`core-brain/skills/courier/`** *(macOS only)* — Drafting Microsoft 365 emails or checking calendar/Teams threads (draft only; never auto-send).
- **`core-brain/skills/planner/`** — Tracking marketing action items and campaign tasks.
- **`marketing/skills/tub-students-customer-research-analyst-v1/`** — Voice-of-customer research from public forums (always pass output through `marketing-voice-check`).
- **`marketing/skills/tub-students-design-dna-extractor-v1/`** — Extracting design patterns from reference sites (always map onto `visual-brand-guide.md`).
- **`marketing/skills/tub-students-sales-call-analyzer-v1/`** — Extracting buyer objections and exact customer language from call transcripts.

## Open Decisions to Respect Until Resolved in `gtm-brain`

- **On-hold product claims (`approved-messaging.md`):** Do not claim per-bid win-probability/margin triage, "catch hidden risks," "protect institutional knowledge," "100% accuracy guarantee," or shipped "Bid Version History."
- **MeasureSquare wording (`marketing/status.md` 2026-11-03):** MeasureSquare takeoff (MS8) is a partner tool JENGAI works with; only MeasureSquare CRM competes (and fits multi-location contractors poorly).
- **PlanHub citations (`findings-2026-08-01-growth-story-sourcing.md`):** Flag any public citation of PlanHub case studies for Renata/Shayne review until resolved.
- **Unconfirmed customer count (`headline-bank.md`):** Do not publish "60+" or stale "37 customers" without verifying live via `salesforce-data`.
