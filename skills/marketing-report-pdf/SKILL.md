---
name: marketing-report-pdf
description: Generate a JENGAI Design System v2 branded PDF marketing report via generate_pdf_report.py, writing the PDF directly to SharePoint AI_Marketing_Outputs/ with a repo .sharepoint.md stub per generated-binary-rules.md.
---

# JENGAI Branded PDF Report Generator (`/marketing report-pdf`)

Compiles available `marketing-*` audit artifacts into a structured JSON payload and renders a **JENGAI Design System v2** PDF using `<MKT_ROOT>/scripts/generate_pdf_report.py` (resolve `<MKT_ROOT>` via `<MKT_ROOT>/context/gtm-brain-map.md`: `<GTM_BRAIN>/marketing` inside `gtm-brain`, else repo root).

## Mandatory Binary & Hosting Rules (`generated-binary-rules.md`)

1. **NEVER save a PDF inside a git repository** (not even temporarily "to move later").
2. **Write directly to SharePoint** using `--sharepoint-rel <relative-path>` (which invokes `core-brain/scripts/sharepoint_path.py` → `AI_Marketing_Outputs/<relative-path>`), and pass `--stub-path <repo-path>/<basename>.sharepoint.md` to leave the required one-line repo breadcrumb.
3. If SharePoint is not synced on the current machine, pass `--temp-fallback` so `generate_pdf_report.py` writes to the OS temp directory (`/tmp` on macOS/Linux, `%TEMP%` on Windows) and informs the operator to upload it to `AI_Marketing_Outputs/`.
4. **Never publish the report to `claude.ai` or any external host.**

## Execution Steps

### Step 1: Collect Audit Data
Read existing files from the unified filenames (`MARKETING-AUDIT.md`, `SEO-AUDIT.md`, `LANDING-CRO.md`, `BRAND-AUDIT.md`, `COMPETITOR-REPORT.md`, `FUNNEL-ANALYSIS.md`).

### Step 2: Assemble JSON in the OS Temp Directory (`<TEMP_DIR>/jengai_report_data.json`)
Write the scratch JSON outside any git repo using the OS temp directory (resolve cross-platform via `python -c "import tempfile; print(tempfile.gettempdir())"` — `$TMPDIR` on macOS, `/tmp` on Linux, `%TEMP%` on Windows). Ensure every field matches the exact schema expected by `<MKT_ROOT>/scripts/generate_pdf_report.py`, including `target_comparison` (for the competitor comparison table) and US date format (`MM/DD/YYYY`):

```json
{
  "url": "https://www.jengai.com",
  "date": "11/20/2026",
  "brand_name": "JENGAI",
  "overall_score": 72,
  "executive_summary": "Concise 2-4 sentence summary in JENGAI internal-report voice. No fabricated revenue dollars.",
  "categories": {
    "Content & Messaging": {"score": 70, "weight": "25%"},
    "Conversion Optimization": {"score": 68, "weight": "20%"},
    "SEO & Technical Foundations": {"score": 62, "weight": "20%"},
    "Competitive Positioning": {"score": 78, "weight": "15%"},
    "Brand & Trust": {"score": 80, "weight": "10%"},
    "Growth & Strategy": {"score": 76, "weight": "10%"}
  },
  "findings": [
    {"severity": "Critical", "finding": "Specific verified finding with evidence"}
  ],
  "quick_wins": ["Concrete action 1", "Concrete action 2", "Concrete action 3"],
  "medium_term": ["Concrete action 1", "Concrete action 2", "Concrete action 3"],
  "strategic": ["Concrete action 1", "Concrete action 2", "Concrete action 3"],
  "target_comparison": {
    "positioning": "Pricing and operations platform for commercial specialty contractors",
    "pricing": "$800/location Starter + seats + setup/onboarding",
    "social_proof": "Bonitz, Pro-United Inc., Silver Slate Group, Transylvania Flooring, Axis Interior Systems",
    "content": "Weekly LinkedIn + Constant Contact nurture + Owner AI Workshops"
  },
  "competitors": [
    {
      "name": "MeasureSquare CRM",
      "positioning": "Takeoff-bundled flooring CRM",
      "pricing": "Tiered SaaS",
      "social_proof": "Large MS8 takeoff install base",
      "content": "Product tutorials and trade demos"
    }
  ]
}
```

### Step 3: Validate Copy & Render PDF
Use `python3` on macOS/Linux or `python` (or `py -3`) on Windows:
1. Validate the JSON text strings with `python3 <MKT_ROOT>/scripts/validate_copy.py <TEMP_DIR>/jengai_report_data.json --register internal`.
2. Ensure `reportlab` is installed (`python3 -c "import reportlab"`).
3. Render straight to SharePoint:
   ```bash
   python3 <MKT_ROOT>/scripts/generate_pdf_report.py <TEMP_DIR>/jengai_report_data.json \
     --sharepoint-rel "audits/2026-11-20-jengai-marketing-report.pdf" \
     --stub-path "outputs/audits/2026-11-20-jengai-marketing-report.pdf.sharepoint.md" \
     --temp-fallback
   ```
4. Clean up `<TEMP_DIR>/jengai_report_data.json`.
