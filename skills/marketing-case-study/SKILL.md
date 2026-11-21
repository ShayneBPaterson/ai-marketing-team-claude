---
name: marketing-case-study
description: Turn a JENGAI customer interview transcript, notes, or existing customer win into a complete proof kit — standalone jengai.com case study page with Review JSON-LD schema, sales 1-pager, LinkedIn post, nurture email, and approved-messaging.md update diff.
---

# JENGAI Case Study & Customer Proof Kit (`/marketing case-study`)

Directly powers JENGAI's proof-led campaigns ("Proof in Their Words", `marketing/projects/2026-09-customer-case-studies/`, and the video-interview-to-content pipeline). Converts raw customer material into verified multi-channel assets without inventing a single metric.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` via `context/gtm-brain-map.md` and read:
1. `marketing/outputs/messaging/approved-messaging.md` and `gtm-knowledge/messaging-and-value-proposition.md`
2. `marketing/projects/2026-09-customer-case-studies/case-study-structure.md`
3. `marketing/knowledge/website-success-stories/README.md`
4. `marketing/knowledge/visual-brand-guide.md`
5. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md` and `generated-binary-rules.md`

## Non-Negotiable Proof Rules

- **Zero invented or extrapolated numbers.** Every figure, quote, title, and company name must trace verbatim to the provided transcript/notes or `approved-messaging.md`.
- **Customer approval gate for new claims:** Any new metric or quote extracted from a raw call or video must be tagged `[PENDING CUSTOMER CONFIRMATION — DO NOT PUBLISH UNTIL SIGNED OFF AND ADDED TO approved-messaging.md]`.
- **Never claim JENGAI "eliminates" errors** — frame as reducing estimation-error risk or quote the customer's exact attributed words with context.
- **No binaries in git:** If rendering a PDF 1-pager, write the PDF straight to SharePoint (`AI_Marketing_Outputs/...`) and drop a `.sharepoint.md` breadcrumb in the repo.

## Execution Workflow

1. **Extract Evidence Ledger:** List every concrete fact from the source (company, city/state, trade, alliance membership like Starnet/FUSE/Commercial USA, interviewee name and title, before state, workflow change, verified quantified outcomes, verbatim quotes with timestamps if from video).
2. **Map to JENGAI Pillars:** Link the story to the primary pillar (Protect margins, Sell more, or Pipeline visibility) and emotional button (Find work, Win more work, or Make more money).
3. **Generate the 5-Asset Kit** using `templates/case-study-kit.md`:
   - **Asset 1: Standalone `jengai.com/success-stories/<slug>` web page copy** (H1, 50–60 char title, 140–160 char meta description, Challenge → Approach → Results, verified pull-quotes, internal links to product pages, "Book a demo" CTA).
   - **Asset 2: Valid JSON-LD `Review` + `Article` schema snippet** ready for `jengai-com/public-website`.
   - **Asset 3: Sales-support 1-pager source** (markdown/HTML structured to `visual-brand-guide.md`; PDF export only via SharePoint).
   - **Asset 4: Distribution pair** — 1 LinkedIn post (Shayne founder voice or JENGAI brand voice) + 1 Constant Contact nurture email referencing the standalone URL.
   - **Asset 5: Proposed `approved-messaging.md` proof-point entry** (ready to merge once customer and Renata sign off).
4. **Validate:** Run `python3 scripts/validate_copy.py <output-file> --public --register external` and check `pre-publish-checklist.md`.

## Output

Save to `CASE-STUDY-<customer-slug>-YYYY-MM-DD.md` (or inside the active `marketing/projects/` folder when running in `gtm-brain`).
