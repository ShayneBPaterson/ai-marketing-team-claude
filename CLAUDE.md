# CLAUDE.md — JENGAI AI Marketing Team

This repository holds the source skills (`marketing-*`), subagents (`marketing-*`), templates, and utility scripts for JENGAI's AI marketing team. It operates directly against `jengai-corp/gtm-brain` as the single source of truth and syncs cleanly into `gtm-brain/marketing/` (`skills/`, `agents/`, `scripts/`, `templates/`, and `context/`) as the canonical operating home for Marketing.

## Ownership and scope

- **Owner:** Renata Doralieva-Paterson, Founder and Chief Marketing Officer (CMO), with Berwyn San Juan (Marketing Associate) reporting to her.
- **Scope:** Top-of-funnel (TOFU) demand generation, brand consistency, website optimization, weekly LinkedIn and Constant Contact content, trade show and association campaigns, Owner AI Workshops, competitive intelligence, and sales-support collateral.
- **Boundary with Sales:** Shayne Paterson owns Sales directly (with Zhai and Aica reporting to him). Subscription pricing proposals (`sales/skills/sales-proposal/`), sales call scripts (`sales/outputs/sales-scripts/`), and deal-closing outreach stay in Sales.

## Single source of truth

Never invent company metrics, customer counts, pricing, proof points, or product claims. Before running any `marketing-*` skill or subagent, resolve `gtm-brain` using [context/gtm-brain-map.md](context/gtm-brain-map.md) and read the authoritative files listed there:

- Positioning and proof points: `gtm-knowledge/messaging-and-value-proposition.md` and `marketing/outputs/messaging/approved-messaging.md`
- Ideal customer profile (ICP): `gtm-knowledge/icp.md`
- Pricing: `gtm-knowledge/pricing.md`
- Voice and pre-publish gate: `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md`, `core-brain/how-we-work/ai-conventions/pre-publish-checklist.md`, and `gtm-knowledge/gtm-specific-voice.md`
- Visual identity: `marketing/knowledge/visual-brand-guide.md`
- Competitive intelligence and collection rules: `marketing/knowledge/competitors/README.md`, `marketing/outputs/competitive/top-five-competitors.md`, and `marketing/market-intelligence/settings.md`
- Tracking and embeds: `marketing/knowledge/website-tracking-and-embed-snippets.md`

## Non-negotiable operating rules

1. **Draft only, always.** No skill or agent may auto-publish, auto-send, or auto-post. Every customer-facing artifact is a draft awaiting explicit approval from **Renata** (CMO). **Shayne** sign-off is additionally required for Shayne founder-voice posts, Sales handoff collateral, and open compliance decisions (such as PlanHub citations).
2. **Positioning lock.** JENGAI is a **pricing and operations platform for commercial specialty contractors**. JENGAI is **not** an estimating or takeoff tool.
3. **Strict proof points.** Only cite the five approved customer proof points in `approved-messaging.md` (Bonitz, Pro-United Inc., Silver Slate Group, Transylvania Flooring Professionals, Axis Interior Systems) plus the standing \$15,000+ error-cost claim. Never freelance stats, flatten ranges, claim JENGAI "eliminates" errors, or hardcode customer counts or ARR without checking `core-brain/skills/salesforce-data/`.
4. **Mandatory copy validation.** Run `python3 <MKT_ROOT>/scripts/validate_copy.py <file>` (use `python` on Windows; add `--public` for customer-facing content) and complete `pre-publish-checklist.md` before finishing any drafting task.
5. **No binaries in git and no external hosting.** Never write PDF, DOCX, XLSX, PPTX, or image deliverables into any git repository. Render binaries directly to SharePoint (`AI_Marketing_Outputs/...`) via `core-brain/scripts/sharepoint-path.mjs marketing` or `sharepoint_path.py` and leave a tracked markdown source or `<basename>.sharepoint.md` pointer in the repo. Never publish work products to `claude.ai` or external hosts.
6. **Cross-platform and machine-agnostic.** Keep all paths relative to `<GTM_BRAIN>` or `<MKT_ROOT>` (resolved via `context/gtm-brain-map.md` or `JENGAI_GTM_BRAIN`). Never hardcode user home directories, `/tmp/`, or OS-specific absolute paths in skills or scripts.
7. **JENGAI is always full caps.** Never write `Jengai` or `jengai` in copy, headlines, or reports.
