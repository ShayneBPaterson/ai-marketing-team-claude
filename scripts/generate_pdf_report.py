#!/usr/bin/env python3
"""
JENGAI Marketing Report PDF Generator — Branded with JENGAI Design System v2.

Enforces:
- Visual brand guide tokens (#020133 deep header, #000180 primary blue,
  #d0ffa3 lime accent spark only — never background, #18181f ink, #67697f muted,
  #edeef1 hairline borders, sentence case headings, US MM/DD/YYYY dates).
- Generated binary rules (core-brain/how-we-work/ai-conventions/generated-binary-rules.md):
  When --sharepoint is supplied, writes the PDF directly to AI_Marketing_Outputs/...
  and writes a tracked <basename>.sharepoint.md stub next to the source path.

Requires: reportlab (pip install reportlab)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from reportlab.graphics.shapes import Circle, Drawing, Line, Rect, String
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# JENGAI Design System v2 semantic palette
if REPORTLAB_AVAILABLE:
    COLORS = {
        "header_deep": HexColor("#020133"),   # surface/header
        "primary": HexColor("#000180"),       # brand/primary
        "blue_600": HexColor("#1718b9"),      # chart primary
        "lime_spark": HexColor("#d0ffa3"),    # brand/success accent (spark only, never full bg)
        "success": HexColor("#3b9719"),       # lime/800 readable status
        "warning": HexColor("#fe8201"),       # status/warning
        "danger": HexColor("#fb281c"),        # status/error
        "light_bg": HexColor("#f8f8f9"),      # neutral/100
        "text": HexColor("#18181f"),          # text/strong
        "text_muted": HexColor("#67697f"),    # text/muted
        "border": HexColor("#edeef1"),        # input/border hairline
        "white": white,
    }


def score_color(score: float):
    if score >= 80:
        return COLORS["success"]
    if score >= 60:
        return COLORS["blue_600"]
    if score >= 40:
        return COLORS["warning"]
    return COLORS["danger"]


def build_competitor_table_rows(data: dict) -> list[list[str]]:
    """Build competitor comparison rows using target_comparison fields (fixes repeated brand_name bug)."""
    brand = data.get("brand_name", "JENGAI")
    competitors = (data.get("competitors") or [])[:3]
    target_comp = data.get("target_comparison") or {}

    header = ["Dimension", brand] + [c.get("name", f"Competitor {i + 1}") for i, c in enumerate(competitors)]
    rows = [header]
    dimensions = [
        ("Positioning", "positioning"),
        ("Pricing", "pricing"),
        ("Social proof", "social_proof"),
        ("Content", "content"),
    ]
    for label, key in dimensions:
        row = [label, str(target_comp.get(key, "—"))]
        for comp in competitors:
            row.append(str(comp.get(key, "—")))
        rows.append(row)
    return rows


def resolve_sharepoint_marketing_dir() -> Path | None:
    """Locate core-brain/scripts/sharepoint_path.py and resolve AI_Marketing_Outputs."""
    candidates = []
    env_brain = os.environ.get("JENGAI_GTM_BRAIN")
    if env_brain:
        candidates.append(Path(env_brain) / "core-brain" / "scripts")
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidates.append(parent / "core-brain" / "scripts")
        candidates.append(parent / "jengai-corp" / "gtm-brain" / "core-brain" / "scripts")
        candidates.append(parent / "gtm-brain" / "core-brain" / "scripts")

    for script_dir in candidates:
        if (script_dir / "sharepoint_path.py").is_file():
            sys.path.insert(0, str(script_dir))
            try:
                import sharepoint_path  # type: ignore
                return sharepoint_path.outputs_dir("marketing", init=True)
            except Exception:
                return None
    return None


def draw_score_gauge(score: float, size: int = 96):
    d = Drawing(size + 24, size + 24)
    cx = size / 2 + 12
    cy = size / 2 + 12
    d.add(Circle(cx, cy, size / 2, fillColor=COLORS["light_bg"], strokeColor=COLORS["border"], strokeWidth=2))
    d.add(Circle(cx, cy, size / 2 - 7, fillColor=score_color(score), strokeColor=None))
    d.add(Circle(cx, cy, size / 2 - 17, fillColor=COLORS["white"], strokeColor=None))
    d.add(String(cx, cy - 7, str(int(round(score))), fontSize=22, fillColor=COLORS["header_deep"], textAnchor="middle", fontName="Helvetica-Bold"))
    return d


def create_bar_chart(categories: list[str], scores: list[float], width: int = 470, height: int = 185):
    d = Drawing(width, height)
    bar_h = 18
    gap = 10
    label_w = 170
    max_bar_w = width - label_w - 45
    start_y = height - 24

    for i, (cat, sc) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_h + gap)
        d.add(String(0, y + 5, cat[:26], fontSize=9, fillColor=COLORS["text"], fontName="Helvetica"))
        d.add(Rect(label_w, y, max_bar_w, bar_h, fillColor=COLORS["light_bg"], strokeColor=None))
        bar_w = max(0, min(100, sc)) / 100.0 * max_bar_w
        d.add(Rect(label_w, y, bar_w, bar_h, fillColor=score_color(sc), strokeColor=None))
        d.add(String(label_w + max_bar_w + 10, y + 5, f"{int(round(sc))}/100", fontSize=9, fillColor=COLORS["text"], fontName="Helvetica-Bold"))
    return d


def generate_report(data: dict, output_path: str | Path) -> Path:
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError("reportlab is required. Install with: pip install reportlab")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(out),
        pagesize=letter,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("JTitle", parent=styles["Title"], fontSize=24, textColor=COLORS["header_deep"], spaceAfter=6, fontName="Helvetica-Bold", alignment=0)
    subtitle_style = ParagraphStyle("JSub", parent=styles["Normal"], fontSize=11, textColor=COLORS["text_muted"], spaceAfter=6, fontName="Helvetica")
    h1_style = ParagraphStyle("JH1", parent=styles["Heading1"], fontSize=16, textColor=COLORS["header_deep"], spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold")
    h2_style = ParagraphStyle("JH2", parent=styles["Heading2"], fontSize=12, textColor=COLORS["primary"], spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold")
    body_style = ParagraphStyle("JBody", parent=styles["Normal"], fontSize=10, textColor=COLORS["text"], spaceAfter=6, fontName="Helvetica", leading=14)

    elements = []

    # Cover header band (JENGAI deep navy + lime spark line)
    band = Drawing(516, 52)
    band.add(Rect(0, 4, 516, 48, fillColor=COLORS["header_deep"], strokeColor=None))
    band.add(Rect(0, 0, 516, 4, fillColor=COLORS["lime_spark"], strokeColor=None))
    band.add(String(16, 22, "JENGAI", fontSize=18, fillColor=COLORS["white"], fontName="Helvetica-Bold"))
    band.add(String(500, 24, "Internal marketing report", fontSize=9, fillColor=COLORS["lime_spark"], fontName="Helvetica", textAnchor="end"))
    elements.append(band)
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("Marketing audit report", title_style))
    url = data.get("url", "https://www.jengai.com")
    date_str = data.get("date", datetime.now().strftime("%m/%d/%Y"))
    elements.append(Paragraph(f"Target: {url}", subtitle_style))
    elements.append(Paragraph(f"Report date: {date_str}", subtitle_style))
    elements.append(Spacer(1, 0.25 * inch))

    overall_score = float(data.get("overall_score", 0))
    elements.append(draw_score_gauge(overall_score))
    elements.append(Spacer(1, 0.15 * inch))

    grade = "A" if overall_score >= 85 else "B" if overall_score >= 70 else "C" if overall_score >= 55 else "D" if overall_score >= 40 else "F"
    elements.append(Paragraph(f"Overall marketing score: {int(round(overall_score))}/100 (Grade {grade})", h1_style))
    elements.append(Paragraph(data.get("executive_summary", "Executive summary pending audit data."), body_style))
    elements.append(PageBreak())

    # Score breakdown
    elements.append(Paragraph("Score breakdown", h1_style))
    categories = data.get("categories") or {}
    cat_names = list(categories.keys())
    cat_scores = [float(categories[c].get("score", 0)) for c in cat_names]
    if cat_names:
        elements.append(create_bar_chart(cat_names, cat_scores))
        elements.append(Spacer(1, 0.2 * inch))
        rows = [["Category", "Score", "Weight", "Status"]]
        for c, sc in zip(cat_names, cat_scores):
            status = "Strong" if sc >= 75 else "Needs work" if sc >= 50 else "Critical"
            rows.append([c, f"{int(round(sc))}/100", str(categories[c].get("weight", "—")), status])
        tbl = Table(rows, colWidths=[210, 80, 70, 110])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_deep"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["light_bg"]]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(tbl)
    elements.append(PageBreak())

    # Findings
    elements.append(Paragraph("Key findings", h1_style))
    findings = data.get("findings") or []
    if findings:
        f_rows = [["Severity", "Finding"]]
        for f in findings:
            f_rows.append([f.get("severity", "Medium"), Paragraph(str(f.get("finding", "")), body_style)])
        f_tbl = Table(f_rows, colWidths=[80, 420])
        cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_deep"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
        sev_map = {"Critical": COLORS["danger"], "High": COLORS["warning"], "Medium": COLORS["blue_600"], "Low": COLORS["text_muted"]}
        for idx, f in enumerate(findings, 1):
            cmds.append(("TEXTCOLOR", (0, idx), (0, idx), sev_map.get(f.get("severity", "Medium"), COLORS["text"])))
            cmds.append(("FONTNAME", (0, idx), (0, idx), "Helvetica-Bold"))
        f_tbl.setStyle(TableStyle(cmds))
        elements.append(f_tbl)

    # Action plan
    elements.append(Spacer(1, 0.25 * inch))
    elements.append(Paragraph("Prioritized action plan", h1_style))
    for heading, key in (
        ("Quick wins (this week)", "quick_wins"),
        ("Medium-term (this month)", "medium_term"),
        ("Strategic (this quarter)", "strategic"),
    ):
        items = data.get(key) or []
        if items:
            elements.append(Paragraph(heading, h2_style))
            for i, item in enumerate(items, 1):
                elements.append(Paragraph(f"{i}. {item}", body_style))

    # Competitor landscape
    if data.get("competitors"):
        elements.append(PageBreak())
        elements.append(Paragraph("Competitive landscape", h1_style))
        comp_rows = build_competitor_table_rows(data)
        col_w = 500 / len(comp_rows[0])
        wrapped = [[Paragraph(cell, body_style) if r_i > 0 else cell for cell in row] for r_i, row in enumerate(comp_rows)]
        c_tbl = Table(wrapped, colWidths=[col_w] * len(comp_rows[0]))
        c_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_deep"]),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["light_bg"]]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elements.append(c_tbl)

    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph("Generated by JENGAI AI Marketing Team — internal draft, not for external distribution without approval.", ParagraphStyle("JFooter", parent=body_style, fontSize=8, textColor=COLORS["text_muted"])))

    doc.build(elements)
    return out


def main():
    parser = argparse.ArgumentParser(description="Generate a JENGAI-branded marketing PDF report.")
    parser.add_argument("input_json", help="Path to structured audit JSON input.")
    parser.add_argument("output_pdf", nargs="?", default=None, help="Output PDF path (use /tmp or SharePoint; never inside a git repo).")
    parser.add_argument("--sharepoint-rel", default=None, help="Relative path inside AI_Marketing_Outputs (writes directly to SharePoint).")
    parser.add_argument("--stub-path", default=None, help="Optional repo path to write a <basename>.sharepoint.md breadcrumb stub.")
    args = parser.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))

    if args.sharepoint_rel:
        sp_root = resolve_sharepoint_marketing_dir()
        if not sp_root:
            print("Error: Could not resolve SharePoint AI_Marketing_Outputs folder. Ensure gtm-brain/core-brain is present and SharePoint is synced.", file=sys.stderr)
            sys.exit(2)
        target = sp_root / args.sharepoint_rel
        generate_report(data, target)
        if args.stub_path:
            stub = Path(args.stub_path)
            stub.parent.mkdir(parents=True, exist_ok=True)
            stub.write_text(f"SharePoint: AI_Marketing_Outputs/{args.sharepoint_rel}\n", encoding="utf-8")
        print(f"Report written to SharePoint: {target}")
        return

    if not args.output_pdf:
        print("Error: Provide either --sharepoint-rel or an explicit output_pdf path (outside git repos).", file=sys.stderr)
        sys.exit(2)

    out = generate_report(data, args.output_pdf)
    print(f"Report generated: {out}")


if __name__ == "__main__":
    main()
