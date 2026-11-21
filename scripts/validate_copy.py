#!/usr/bin/env python3
"""
JENGAI Copy Validator — Automated pre-publish linter for JENGAI marketing drafts.

Enforces deterministic rules from:
- core-brain/how-we-work/ai-conventions/jengai-voice-and-communication-rules.md
- core-brain/how-we-work/ai-conventions/pre-publish-checklist.md
- gtm-knowledge/gtm-specific-voice.md
- gtm-knowledge/messaging-and-value-proposition.md
- marketing/outputs/messaging/approved-messaging.md
- marketing/campaigns/2026-08-content-calendar-hook-rework/findings-2026-08-01-growth-story-sourcing.md
"""

import argparse
import json
import re
import sys
from pathlib import Path


BANNED_NEVER_WORDS = [
    (r"\bthe one\b", 'Never use crutch phrase "the one" — name the specific thing instead.'),
    (r"\bhonestly\b", 'Never use "honestly" — sincerity-signaling filler.'),
    (r"\btruly\b", 'Never use "truly" — sincerity-signaling filler.'),
]

BANNED_AI_WORDS = [
    "delve", "tapestry", "multifaceted", "nuanced", "resonate", "resonates", "resonating",
    "embark", "journey", "foster", "illuminate", "paramount", "pivotal", "robust",
    "seamless", "seamlessly", "holistic", "cutting-edge", "revolutionary", "revolutionize",
    "revolutionizing", "testament", "meticulous", "intricate", "comprehensive",
    "furthermore", "moreover", "in addition", "additionally", "in essence",
    "in conclusion", "in summary",
]

BANNED_CORPORATE_WORDS = [
    (r"\bunpack\b", 'Avoid corporate buzzword "unpack".'),
    (r"\bdeep dive\b", 'Avoid corporate buzzword "deep dive".'),
    (r"\bpivot\b", 'Avoid corporate buzzword "pivot".'),
    (r"\bleverag(?:e|es|ed|ing)\b", 'Avoid "leverage" as a verb — use plain language.'),
    (r"\butiliz(?:e|es|ed|ing)\b", 'Avoid "utilize" — use "use".'),
    (r"\baligned\b", 'Avoid corporate buzzword "aligned".'),
    (r"\bgame[- ]changer\b", 'Avoid buzzword "game changer".'),
    (r"\bsomething shifted\b", 'Avoid cliché "something shifted".'),
    (r"\bstreamlin(?:e|es|ed|ing)\b", 'Avoid SaaS-hype word "streamline" (gtm-specific-voice.md).'),
    (r"\boptimiz(?:e|es|ed|ing)\b", 'Avoid SaaS-hype word "optimize" in external copy (gtm-specific-voice.md).'),
    (r"\bai-driven\b", 'Avoid AI-hype phrase "AI-driven" (gtm-specific-voice.md).'),
    (r"\bml-driven\b", 'Avoid AI-hype phrase "ML-driven" (gtm-specific-voice.md).'),
]

BANNED_THROAT_CLEARING = [
    r"\bhere['’]s the thing\b",
    r"\blet me explain\b",
    r"\bthe truth is\b",
    r"\bat the end of the day\b",
    r"\blet that sink in\b",
    r"\band that brings me to\b",
    r"\bsound familiar\b",
    r"\bmore than ever\b",
    r"\bit['’]s safe to say\b",
]

RETIRED_POSITIONING_PATTERNS = [
    (
        r"\bcrm[- ]estimation suite\b",
        'Retired positioning: "CRM-Estimation Suite". Use "pricing and operations platform for commercial specialty contractors".',
    ),
    (
        r"\bai crm,\s*estimation,\s*and pricing suite\b",
        'Retired positioning (cancelled 2026-08-31): use "pricing and operations platform for commercial specialty contractors".',
    ),
    (
        r"\b(?:is|as)\s+an?\s+(?:ai\s+)?(?:estimating|estimation|takeoff)\s+(?:tool|software|platform)\b",
        'Positioning violation (2026-08-31): JENGAI is a pricing and operations platform, NOT an estimating or takeoff tool.',
    ),
    (
        r"\bai estimating\s*(?:&|and)\s*bidding software\b",
        'Positioning violation (2026-08-31): JENGAI is a pricing and operations platform, NOT estimating software.',
    ),
    (
        r"\btransforms the estimating and bidding process\b",
        'Retired wording (2026-08-31): replace with current pricing and operations platform positioning.',
    ),
    (
        r"\bai-powered workflow automation\b",
        'Retired wording (messaging-and-value-proposition.md): do not describe JENGAI as "AI-powered workflow automation".',
    ),
]

BANNED_AND_ONHOLD_CLAIMS = [
    (
        r"\beliminat(?:e|es|ed|ing)\s+(?:all\s+)?(?:estimation\s+|estimating\s+)?(?:errors|mistakes)\b",
        'Banned claim: never say JENGAI "eliminates" errors — only that it reduces the risk of one.',
    ),
    (
        r"\b50%\s+faster\s+pricing\b",
        'Banned claim: "50% faster pricing" has no verified source in gtm-brain.',
    ),
    (
        r"\b100%\s+accuracy(?:\s+guarantee)?\b",
        'On-hold claim (2026-08-27): "100% accuracy" / guarantee is under review — do not use.',
    ),
    (
        r"\b40%\s+faster\s+estimation\b",
        'Inaccurate proof point: Bonitz result is "40% faster takeoff turnaround (via APA)", not "40% faster estimation".',
    ),
    (
        r"\brank(?:s|ing)?\s+(?:incoming\s+)?bids?\s+by\s+(?:margin|win[- ]probability)\b",
        'On-hold claim (2026-08-27): per-bid win-probability scoring is not confirmed in product-state.md.',
    ),
    (
        r"\bwin[- ]probability\s+scor(?:e|ing)\b",
        'On-hold claim (2026-08-27): per-bid win-probability scoring is not supported today — do not claim.',
    ),
    (
        r"\bcatch(?:es|ing)?\s+hidden\s+risks\b",
        'On-hold claim (2026-08-27): "catch hidden risks" has no backing capability in product-state.md.',
    ),
    (
        r"\bprotect(?:s|ing)?\s+institutional\s+knowledge\b",
        'On-hold claim (2026-08-27): "protect institutional knowledge" is withheld pending product decision.',
    ),
    (
        r"\b(?:25%\s+win[- ]rate|2\.3x\s+more\s+bids)\b",
        'Cancelled BuildingConnected stat (2026-07-29): unverifiable benchmark — do not cite.',
    ),
    (
        r"\btransylvania\b.{0,60}\b(?<!30[-–])40%\s+(?:more\s+bids|increase\s+in\s+bids)\b",
        'Inaccurate proof point: Transylvania Flooring result is "30-40% increase in bids sent", never a flat "40%".',
    ),
    (
        r"\b(?:\$10m\+|10\s*million\+)\b.{0,40}\b(?:icp|floor|qualif|revenue)\b",
        'Outdated ICP floor: lowered from $10M+ to $4M+ in Q2 2026 (gtm-knowledge/icp.md).',
    ),
    (
        r"\b37\s+customers\b|\$518\.8k\b",
        'Stale figure (2026-07-06): never quote hardcoded customer count or ARR — verify live via salesforce-data.',
    ),
]

PUBLIC_ONLY_COMPETITOR_BANS = [
    (r"\bSTACK\b", 'Public compliance rule: STACK is a monitored direct competitor — never name publicly without explicit approval.'),
    (r"\bBobyard\b", 'Public compliance rule: Bobyard is a monitored direct competitor — never name publicly without explicit approval.'),
    (r"\bKreo\b", 'Public compliance rule: Kreo is a tracked competitor/partner — do not name in public marketing content without approval.'),
    (r"\bTogal(?:\.AI)?\b", 'Public compliance rule: Togal.AI is a monitored direct competitor — never name publicly without explicit approval.'),
    (r"\b1build\b|\bHandoff\b", 'Public compliance rule: 1build/Handoff is a monitored direct competitor — never name publicly without explicit approval.'),
    (r"\bMeasureSquare\s+CRM\b", 'Public compliance rule: do not name MeasureSquare CRM in public content without explicit approval.'),
    (r"\bGarmon\s*(?:&|and)\s*Company\b", 'Compliance exclusion: Garmon & Company is a live at-risk account — never cite publicly.'),
]

PUBLIC_ONLY_WARNINGS = [
    (
        r"\bPlanHub\b",
        'Review required: PlanHub citation policy is still open (findings-2026-08-01-growth-story-sourcing.md). Confirm with Renata/Shayne before publishing.',
    ),
    (
        r"\b(?:Procore|Salesforce|Gong|Snowflake)\b",
        'ICP-proof check: avoid citing generic B2B SaaS case studies as proof (finish-trade or construction-tech proof only; ignore if naming an integration).',
    ),
    (
        r"\b60\+\s+(?:specialty\s+)?contractors\b",
        'Unverified count: "60+" is in headline-bank.md as Renata\'s call but not yet verified in approved-messaging.md — verify via salesforce-data.',
    ),
    (
        r"\bBid\s+Version\s+History\b",
        'Unshipped feature (feature-value-mapping.md): do not present Bid Version History as currently shipped until release is confirmed.',
    ),
]

GENERAL_WARNINGS = [
    (
        r"\b(?:real|actual|actually|really|genuine|genuinely)\b",
        'Filler check: keep "real/actual/actually/really/genuine/genuinely" only when removing it changes the claim.',
    ),
    (
        r"\b(?:swept|drifted|closed the loop|propagated|defer to)\b",
        'Internal jargon check (jengai-voice-and-communication-rules.md): prefer plain words (synced, out of sync, confirmed, applied, refer to).',
    ),
    (
        r"\bin practice\b",
        'GTM style check: prefer "in reality" over "in practice" (gtm-specific-voice.md).',
    ),
    (
        r"\b(?:what if you could|are you tired of|ready to transform)\b",
        'Rhetorical/engagement-bait check: make a direct statement instead of asking bait questions.',
    ),
]

URL_OR_EMAIL_RE = re.compile(
    r"https?://\S+|\b[\w.+-]+@[\w-]+\.[\w.-]+\b|`[^`]+`|<code[^>]*>.*?</code>|\([^\)]*jengai[^\)]*\)",
    re.IGNORECASE,
)
WRONG_JENGAI_CASE_RE = re.compile(r"\b(?!JENGAI\b)[Jj][Ee][Nn][Gg][Aa][Ii]\b")

OUTREACH_CONTRACTION_RE = re.compile(
    r"\b(?:don't|doesn't|didn't|won't|wouldn't|can't|couldn't|shouldn't|isn't|aren't|wasn't|weren't|"
    r"haven't|hasn't|hadn't|we're|you're|they're|it's|that's|there's|here's|we've|you've|i've|"
    r"i'm|i'll|we'll|you'll|i'd|we'd|you'd)\b",
    re.IGNORECASE,
)


def strip_fenced_code(lines):
    """Yield (line_number, line_text) skipping fenced code blocks."""
    in_fence = False
    for idx, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield idx, line


def validate_text(text, *, public=False, register="external"):
    """Validate text against JENGAI voice, positioning, and proof-point rules."""
    errors = []
    warnings = []
    lines = text.splitlines()

    for line_no, raw_line in strip_fenced_code(lines):
        if line_no <= 10 and (raw_line.strip() == "---" or re.match(r"^[a-z_-]+:\s", raw_line)):
            continue

        prose = URL_OR_EMAIL_RE.sub(" ", raw_line)

        for m in WRONG_JENGAI_CASE_RE.finditer(prose):
            errors.append({
                "line": line_no,
                "rule": "brand-casing",
                "match": m.group(0),
                "message": f'JENGAI must always be full caps (found "{m.group(0)}").',
            })

        for pattern, msg in BANNED_NEVER_WORDS:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                errors.append({"line": line_no, "rule": "banned-word", "match": m.group(0), "message": msg})

        for word in BANNED_AI_WORDS:
            for m in re.finditer(rf"\b{re.escape(word)}\b", prose, re.IGNORECASE):
                errors.append({
                    "line": line_no,
                    "rule": "ai-vocabulary",
                    "match": m.group(0),
                    "message": f'Avoid AI-generated vocabulary "{m.group(0)}" (jengai-voice-and-communication-rules.md).',
                })

        for pattern, msg in BANNED_CORPORATE_WORDS:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                if register == "internal" and "optimiz" in pattern:
                    warnings.append({"line": line_no, "rule": "corporate-buzzword", "match": m.group(0), "message": msg})
                else:
                    errors.append({"line": line_no, "rule": "corporate-buzzword", "match": m.group(0), "message": msg})

        for pattern in BANNED_THROAT_CLEARING:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                errors.append({
                    "line": line_no,
                    "rule": "throat-clearing",
                    "match": m.group(0),
                    "message": f'Cut throat-clearing phrase "{m.group(0)}" (jengai-voice-and-communication-rules.md).',
                })

        for pattern, msg in RETIRED_POSITIONING_PATTERNS:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                errors.append({"line": line_no, "rule": "positioning-lock", "match": m.group(0), "message": msg})

        for pattern, msg in BANNED_AND_ONHOLD_CLAIMS:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                errors.append({"line": line_no, "rule": "claim-governance", "match": m.group(0), "message": msg})

        if public:
            for pattern, msg in PUBLIC_ONLY_COMPETITOR_BANS:
                for m in re.finditer(pattern, prose):
                    errors.append({"line": line_no, "rule": "public-compliance", "match": m.group(0), "message": msg})
            for pattern, msg in PUBLIC_ONLY_WARNINGS:
                for m in re.finditer(pattern, prose, re.IGNORECASE):
                    warnings.append({"line": line_no, "rule": "public-review", "match": m.group(0), "message": msg})

        if register == "outreach":
            for m in OUTREACH_CONTRACTION_RE.finditer(prose):
                errors.append({
                    "line": line_no,
                    "rule": "outreach-no-contractions",
                    "match": m.group(0),
                    "message": f'No contractions in outreach register (found "{m.group(0)}" — gtm-specific-voice.md).',
                })

        for pattern, msg in GENERAL_WARNINGS:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                warnings.append({"line": line_no, "rule": "style-warning", "match": m.group(0), "message": msg})

    return {
        "passed": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate JENGAI marketing copy against voice, positioning, and proof-point rules."
    )
    parser.add_argument("files", nargs="+", help="Path(s) to markdown, HTML, or MJML files to validate.")
    parser.add_argument(
        "--public",
        action="store_true",
        help="Apply public-facing compliance checks (blocks direct competitor names and flags PlanHub/generic SaaS proof).",
    )
    parser.add_argument(
        "--register",
        choices=["external", "founder", "internal", "outreach"],
        default="external",
        help="Writing register from gtm-specific-voice.md (default: external).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Output machine-readable JSON.",
    )
    args = parser.parse_args()

    overall_ok = True
    report = []

    for file_arg in args.files:
        path = Path(file_arg)
        if not path.is_file():
            overall_ok = False
            report.append({"file": str(path), "error": "File not found", "passed": False})
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        res = validate_text(text, public=args.public, register=args.register)
        res["file"] = str(path)
        report.append(res)
        if not res["passed"]:
            overall_ok = False

    if args.as_json:
        print(json.dumps({"passed": overall_ok, "results": report}, indent=2))
    else:
        for item in report:
            if "error" in item:
                print(f"[FAIL] {item['file']}: {item['error']}")
                continue
            status = "PASS" if item["passed"] else "FAIL"
            print(f"[{status}] {item['file']} — {item['error_count']} error(s), {item['warning_count']} warning(s)")
            for err in item["errors"]:
                print(f"  ERROR   L{err['line']} [{err['rule']}]: {err['message']}")
            for warn in item["warnings"]:
                print(f"  WARN    L{warn['line']} [{warn['rule']}]: {warn['message']}")

    sys.exit(0 if overall_ok else 1)


if __name__ == "__main__":
    main()
