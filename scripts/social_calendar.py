#!/usr/bin/env python3
"""
JENGAI Weekly Content Calendar Scaffolder — Utility script for marketing-social
and marketing-weekly-cadence.

Generates JENGAI's standing cadence:
- 1 LinkedIn post + 1 Constant Contact nurture email per week (never daily flooding)
- Monthly rotation across JENGAI's three message pillars:
  1. Protect margins (Estimation speed & accuracy)
  2. Sell more (Sales capacity)
  3. Pipeline visibility
- Tags each week with one of Shayne's three emotional hook buttons:
  Find work | Win more work | Make more money
- Anchors known trade events (Starnet, FUSE, Commercial USA) and compliance fields.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta


PILLARS = [
    {
        "id": "protect-margins",
        "name": "Protect margins (Estimation speed and accuracy)",
        "default_proof": "Bonitz (40% faster takeoff turnaround via APA); Pro-United Inc. (1 estimation error in 3 years); $15,000+ average error cost",
        "default_button": "Make more money",
    },
    {
        "id": "sell-more",
        "name": "Sell more (Sales capacity)",
        "default_proof": "Transylvania Flooring Professionals (30-40% increase in bids sent); Silver Slate Group (revenue tripled)",
        "default_button": "Win more work",
    },
    {
        "id": "pipeline-visibility",
        "name": "Pipeline visibility",
        "default_proof": "Silver Slate Group (net profit margin well above industry standard); Axis Interior Systems (moved off Excel, centralized project data)",
        "default_button": "Find work",
    },
]

EMOTIONAL_BUTTONS = ["Find work", "Win more work", "Make more money"]
FRAMEWORKS = ["Problem -> Solution -> Proof", "Before / After", "Named Growth Story -> JENGAI Bridge"]
VOICES = ["JENGAI company voice", "Renata CMO/Founder voice", "Shayne founder voice"]


def next_monday(start: date) -> date:
    offset = (7 - start.weekday()) % 7
    return start + timedelta(days=offset)


def generate_weekly_calendar(
    start_date_str: str | None = None,
    weeks: int = 12,
    events: dict[int, str] | None = None,
) -> dict:
    start = date.fromisoformat(start_date_str) if start_date_str else next_monday(date.today())
    event_map = events or {}
    rows = []

    for idx in range(weeks):
        week_start = start + timedelta(days=idx * 7)
        # Rotate pillar roughly once per 4-week month
        pillar = PILLARS[(idx // 4) % len(PILLARS)]
        button = EMOTIONAL_BUTTONS[idx % len(EMOTIONAL_BUTTONS)]
        framework = FRAMEWORKS[idx % len(FRAMEWORKS)]
        voice = VOICES[idx % len(VOICES)]
        approval = (
            "DRAFT — awaiting Renata approval (+ Shayne sign-off for Shayne founder voice)"
            if voice == "Shayne founder voice"
            else "DRAFT — awaiting Renata approval"
        )

        rows.append({
            "week": idx + 1,
            "week_of": week_start.isoformat(),
            "linkedin_publish_window": "Tue-Thu 8:00-11:00 AM ET",
            "email_platform": "Constant Contact",
            "pillar_id": pillar["id"],
            "pillar_name": pillar["name"],
            "emotional_button": button,
            "framework": framework,
            "voice": voice,
            "approved_proof_anchor": pillar["default_proof"],
            "default_cta": "Book a demo (soften for cold LinkedIn)",
            "event_anchor": event_map.get(idx + 1),
            "source_provenance": "[Fill: internal-pattern-only OR public-citation with verified URL — never name direct competitors]",
            "approval_status": approval,
        })

    return {
        "brand": "JENGAI",
        "cadence": "1 LinkedIn post + 1 Constant Contact nurture email per week",
        "approval_gate": "Draft only — no auto-publish or auto-send",
        "start_week": start.isoformat(),
        "weeks": weeks,
        "calendar": rows,
    }


def render_markdown(cal: dict) -> str:
    lines = [
        f"# JENGAI Weekly Content Calendar ({cal['start_week']}, {cal['weeks']} weeks)",
        "",
        f"- **Cadence:** {cal['cadence']}",
        f"- **Approval gate:** {cal['approval_gate']}",
        "- **Positioning lock:** JENGAI is a pricing and operations platform for commercial specialty contractors — never an estimating or takeoff tool.",
        "- **Compliance:** All claims must come from `marketing/outputs/messaging/approved-messaging.md`. Never name direct competitors publicly.",
        "",
        "| Week | Week of | Pillar | Emotional button | Voice | Framework | Event anchor | Source provenance | Status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in cal["calendar"]:
        ev = r["event_anchor"] or "—"
        lines.append(
            f"| {r['week']} | {r['week_of']} | {r['pillar_name']} | {r['emotional_button']} | "
            f"{r['voice']} | {r['framework']} | {ev} | {r['source_provenance']} | {r['approval_status']} |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Scaffold a JENGAI weekly LinkedIn + Constant Contact calendar.")
    parser.add_argument("--start", default=None, help="Start Monday in YYYY-MM-DD format (default: next Monday).")
    parser.add_argument("--weeks", type=int, default=12, help="Number of weeks (default: 12).")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format (default: json).")
    parser.add_argument("--event", action="append", default=[], help="Event anchor as WEEK:NAME (e.g. 4:Starnet Fall Meeting).")
    args = parser.parse_args()

    events = {}
    for item in args.event:
        if ":" in item:
            wk, name = item.split(":", 1)
            if wk.strip().isdigit():
                events[int(wk.strip())] = name.strip()

    cal = generate_weekly_calendar(args.start, args.weeks, events)
    if args.format == "markdown":
        print(render_markdown(cal))
    else:
        print(json.dumps(cal, indent=2))


if __name__ == "__main__":
    main()
