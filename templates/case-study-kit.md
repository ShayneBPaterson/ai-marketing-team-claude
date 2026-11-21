# JENGAI Customer Case Study Kit — [Customer Name]

- **Status:** DRAFT — [VERIFIED IN approved-messaging.md / PENDING CUSTOMER SIGN-OFF]
- **Trade & location:** [Flooring / Stone / Tile] · [City, State]
- **Association:** [Starnet Worldwide / FUSE Alliance / Commercial USA / Independent]
- **Primary pillar:** [Protect margins / Sell more / Pipeline visibility]
- **Interviewee:** [Full Name, Title]

---

## 1. Evidence Ledger (Verbatim Source Facts Only)

| Fact / Metric | Exact wording | Source & date | Customer sign-off |
| --- | --- | --- | --- |
| Before state | [quote or note] | [source] | Verified / Pending |
| Workflow change | [quote or note] | [source] | Verified / Pending |
| Quantified outcome | [exact number or range] | [source] | Verified / Pending |

---

## 2. Standalone Web Page Copy (`jengai.com/success-stories/<slug>`)

- **Title tag (50–60 chars):** [Customer Name] Case Study | JENGAI
- **Meta description (140–160 chars):** [Specific verified result + trade + Book a demo CTA]
- **H1:** [Specific outcome headline — sentence case, JENGAI full caps]

### The challenge
[Complete sentences describing the contractor's pre-JENGAI bottleneck.]

### How [Customer Name] uses JENGAI
[Plain workflow explanation — never describe JENGAI as an estimating or takeoff tool.]

### The results
- [Verified metric 1]
- [Verified metric 2]
- [Verified metric 3]

> "[Exact attributed customer quote]" — [Full Name], [Title], [Customer Name]

- **Internal links:** Link to `/demo` and relevant solution pages.
- **Primary CTA:** Book a demo (`https://www.jengai.com/demo`).

---

## 3. JSON-LD Structured Data (`Review` + `Article`)

```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "SoftwareApplication",
    "name": "JENGAI",
    "applicationCategory": "BusinessApplication"
  },
  "author": {
    "@type": "Person",
    "name": "[Full Name]",
    "jobTitle": "[Title]"
  },
  "reviewBody": "[Exact attributed customer quote]",
  "publisher": {
    "@type": "Organization",
    "name": "JENGAI"
  }
}
```

---

## 4. Sales 1-Pager Source & SharePoint Export Note

- Style against `marketing/knowledge/visual-brand-guide.md` (`#020133`, `#000180`, `#d0ffa3` spark only, Inter).
- When exporting to PDF, write straight to `AI_Marketing_Outputs/case-studies/<slug>.pdf` and drop a `.sharepoint.md` stub in the repo. Never commit the PDF to git.

---

## 5. Distribution Cuts (1 LinkedIn Post + 1 Constant Contact Email)

### LinkedIn Post (Founder or Company Voice)
```text
[Ready-to-approve LinkedIn post linking to https://www.jengai.com/success-stories/<slug>]
```

### Constant Contact Nurture Email
- **Subject:** [Concrete outcome hook]
- **Preview text:** [Supporting detail]
```text
[150-220 word story-driven email with Book a demo CTA]
```

---

## 6. Proposed `approved-messaging.md` Proof Entry

*(Merge only after customer confirmation and Renata sign-off.)*

```markdown
- **[Customer Name]** ([Location, trade, association]) — [exact verified result]. — [Full Name, Title].
```
