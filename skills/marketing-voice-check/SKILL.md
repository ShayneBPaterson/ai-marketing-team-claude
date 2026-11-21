---
name: marketing-voice-check
description: Run JENGAI's mandatory pre-publish voice, positioning, proof-point, and compliance gate on any draft file or pasted copy using scripts/validate_copy.py and pre-publish-checklist.md.
---

# JENGAI Pre-Publish Voice & Claim Gate (`/marketing voice-check`)

Turns JENGAI's voice rules, pre-publish checklist, positioning lock, and proof-point governance into an executable quality gate. Run this automatically at the end of every drafting skill, or manually on any document via `/marketing voice-check <file>`.

## Mandatory Pre-Flight Reads

Resolve `<GTM_BRAIN>` via `context/gtm-brain-map.md` and read:
1. `core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md`
2. `core-brain/how-we-work/ai-conventions/pre-publish-checklist.md`
3. `gtm-knowledge/gtm-specific-voice.md`
4. `gtm-knowledge/messaging-and-value-proposition.md`
5. `marketing/outputs/messaging/approved-messaging.md`

## Execution Process

### Step 1: Run Deterministic Copy Linter
Determine the register (`external`, `founder`, `internal`, or `outreach`) and whether the draft is customer-facing (`--public`), then run:

```bash
python3 scripts/validate_copy.py <path-to-file> --public --register <register>
```

(Omit `--public` only for internal leadership reports or internal competitive analyses.)

### Step 2: Run Structural & Editorial Checks (Beyond Regex)
Inspect the draft manually against every remaining rule in `pre-publish-checklist.md` and `gtm-specific-voice.md`:
- **Complete sentences:** Every sentence has a stated subject and verb (no clipped fragments, including in headings/cards/UI copy).
- **Explicit connections:** Uses "so," "but," "because," or "which means" instead of letting dashes imply the link.
- **Structure hygiene:**
  - Lists contain **1 item or 3 items — never 2**.
  - No stacked one-line opening paragraphs; no stacked closing imperatives.
  - No repeated emphasis phrase or three-in-a-row "X, not Y" headings.
  - Flowed prose (no mid-sentence line breaks).
  - Acronyms spelled out on first use (e.g., Automated Plan Analysis (APA), General Contractor (GC), Invitation to Bid (ITB)).
- **Register-specific checks:**
  - *External marketing copy:* Trusted industry peer tone; identity marketing ("buy this" → "be this").
  - *Founder voice:* CEO-to-CEO, specific storytelling, humble confidence.
  - *Internal reports:* Plain language, "in reality" instead of "in practice", no fabricated revenue projections.
  - *Outreach:* `"Dear [First Name],"`, no contractions, self-intro paragraph, association check (skip company description for Starnet/FUSE/Commercial USA members), hyphenated role attribution (`"our CMO - Renata"`), accurate conversation attribution, closing line before signature.
- **Read-out-loud test:** Flag any sentence that sounds written by software instead of spoken by a knowledgeable colleague.

### Step 3: Output Pass/Fail Compliance Report + Line-by-Line Fixes

```markdown
# JENGAI Voice & Claim Gate: <filename>
- **Register:** external / founder / internal / outreach
- **Audience:** Public / Internal
- **Status:** PASS / FAIL

## Automated Linter Output (`validate_copy.py`)
- Errors: X
- Warnings: Y
[Exact line numbers and rules]

## Editorial Checklist Findings
| Check | Status | Line / quote | Concrete rewrite |
| --- | --- | --- | --- |

## Sign-Off
- Ready for Renata / Shayne approval: YES / NO (list blocking fixes)
```
