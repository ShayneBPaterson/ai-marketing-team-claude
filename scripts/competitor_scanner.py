#!/usr/bin/env python3
"""
JENGAI Competitor Scanner — Compliance-aware utility for marketing-competitors.

Supports both `--url <url>` flags and positional URLs, checks robots.txt and
gtm-brain/marketing/market-intelligence/*/sources.json exclusions before fetching,
and outputs data aligned with JENGAI's competitor profile schema.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
import urllib.robotparser
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


USER_AGENT = "JENGAIMarketIntel/2.0"

# Hard-coded fallback exclusions matching gtm-brain/marketing/market-intelligence/settings.md
DEFAULT_EXCLUDED_DOMAINS = {
    "enr.com",
    "constructiondive.com",
    "jbknowledge.com",
}


def find_gtm_brain() -> Path | None:
    env_path = os.environ.get("JENGAI_GTM_BRAIN")
    if env_path:
        p = Path(env_path)
        if (p / "gtm-knowledge").is_dir():
            return p
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "gtm-knowledge").is_dir() and (parent / "marketing").is_dir():
            return parent
        for sibling in (parent / "jengai-corp" / "gtm-brain", parent / "gtm-brain"):
            if (sibling / "gtm-knowledge").is_dir() and (sibling / "marketing").is_dir():
                return sibling
    return None


def load_compliance_registry(gtm_brain: Path | None = None) -> dict[str, dict]:
    """Load compliance status by domain from market-intelligence/*/sources.json."""
    registry: dict[str, dict] = {
        d: {"status": "excluded", "source": "default-exclusion"} for d in DEFAULT_EXCLUDED_DOMAINS
    }
    root = gtm_brain or find_gtm_brain()
    if not root:
        return registry

    for pipeline in ("threat-monitoring", "content-opportunities"):
        src_file = root / "marketing" / "market-intelligence" / pipeline / "sources.json"
        if not src_file.is_file():
            continue
        try:
            entries = json.loads(src_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(entries, list):
            continue
        for entry in entries:
            status = (entry.get("status") or "").lower()
            decision = entry.get("compliance_decision") or ""
            for src_url in entry.get("sources") or []:
                dom = urlparse(src_url).netloc.lower().replace("www.", "")
                if dom:
                    registry[dom] = {
                        "status": status,
                        "company": entry.get("name"),
                        "pipeline": pipeline,
                        "compliance_decision": decision,
                    }
    return registry


class CompetitorPageParser(HTMLParser):
    """Parse competitor page HTML for positioning, pricing, trade focus, and integrations."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.og_title = ""
        self.og_description = ""
        self.h1_tags = []
        self.h2_tags = []
        self.pricing_indicators = []
        self.social_links = []
        self.ctas = []
        self.testimonial_count = 0
        self.logo_count = 0

        self._in_title = False
        self._in_h1 = False
        self._in_h2 = False
        self._in_a = False
        self._in_button = False
        self._in_script = False
        self._in_style = False
        self._current_text = ""
        self._all_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self._in_title = True
            self._current_text = ""
        elif tag == "script":
            self._in_script = True
        elif tag == "style":
            self._in_style = True
        elif tag == "meta":
            name = (attrs_dict.get("name") or "").lower()
            prop = (attrs_dict.get("property") or "").lower()
            content = attrs_dict.get("content") or ""
            if name == "description":
                self.meta_description = content
            elif prop == "og:title":
                self.og_title = content
            elif prop == "og:description":
                self.og_description = content
        elif tag == "h1":
            self._in_h1 = True
            self._current_text = ""
        elif tag == "h2":
            self._in_h2 = True
            self._current_text = ""
        elif tag == "a":
            self._in_a = True
            self._current_text = ""
            href = attrs_dict.get("href") or ""
            for domain, name in {
                "linkedin.com": "LinkedIn",
                "youtube.com": "YouTube",
                "twitter.com": "Twitter/X",
                "x.com": "Twitter/X",
                "facebook.com": "Facebook",
                "instagram.com": "Instagram",
            }.items():
                if domain in href.lower():
                    self.social_links.append({"platform": name, "url": href})
        elif tag == "button":
            self._in_button = True
            self._current_text = ""
        elif tag == "img":
            alt = (attrs_dict.get("alt") or "").lower()
            src = (attrs_dict.get("src") or "").lower()
            if any(w in alt or w in src for w in ("logo", "client", "partner", "customer")):
                self.logo_count += 1

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self._in_title = False
            self.title = " ".join(self._current_text.split())
        elif tag == "script":
            self._in_script = False
        elif tag == "style":
            self._in_style = False
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            text = " ".join(self._current_text.split())
            if text:
                self.h1_tags.append(text)
        elif tag == "h2" and self._in_h2:
            self._in_h2 = False
            text = " ".join(self._current_text.split())
            if text:
                self.h2_tags.append(text)
        elif tag == "a" and self._in_a:
            self._in_a = False
            text = " ".join(self._current_text.split())
            if any(w in text.lower() for w in ("demo", "trial", "pricing", "start", "book", "contact")):
                self.ctas.append(text)
        elif tag == "button" and self._in_button:
            self._in_button = False
            text = " ".join(self._current_text.split())
            if text:
                self.ctas.append(text)

    def handle_data(self, data):
        if self._in_script or self._in_style:
            return
        if self._in_title or self._in_h1 or self._in_h2 or self._in_a or self._in_button:
            self._current_text += data
        stripped = data.strip()
        if not stripped:
            return
        self._all_text.append(stripped)
        lower = stripped.lower()
        for pat in (r"\$\d+", r"/month", r"/mo\b", r"/year", r"per user", r"free trial", r"enterprise"):
            if re.search(pat, lower):
                self.pricing_indicators.append(stripped[:140])
                break
        if any(w in lower for w in ("testimonial", "case study", "customer story", "success story")):
            self.testimonial_count += 1

    def get_results(self):
        full_text = " ".join(self._all_text)
        full_lower = full_text.lower()
        finish_trades = [t for t in ("flooring", "tile", "stone", "carpet", "terrazzo", "finishes") if t in full_lower]
        integrations = [
            name for name in (
                "BuildingConnected", "PlanSwift", "MeasureSquare", "Bluebeam",
                "Salesforce", "Zoho", "Procore", "QuickBooks", "Revit", "Spec-ID", "PlanHub",
            )
            if name.lower() in full_lower
        ]
        capabilities = [
            cap for cap in (
                "takeoff", "estimating", "bid board", "bid management", "crm",
                "proposal", "plan analysis", "ai", "job costing", "scheduling",
            )
            if cap in full_lower
        ]
        return {
            "positioning": {
                "headline": self.h1_tags[0] if self.h1_tags else self.title,
                "title": self.title,
                "meta_description": self.meta_description,
                "og_description": self.og_description,
                "key_sections": self.h2_tags[:12],
            },
            "finish_trade_signals": finish_trades,
            "integrations_mentioned": integrations,
            "capability_signals": capabilities,
            "pricing": {
                "has_pricing_info": bool(self.pricing_indicators),
                "pricing_mentions": sorted(set(self.pricing_indicators))[:10],
            },
            "trust": {
                "social_platforms": sorted({s["platform"] for s in self.social_links}),
                "estimated_logo_count": self.logo_count,
                "has_testimonials": self.testimonial_count > 0,
            },
            "ctas": sorted(set(self.ctas))[:12],
            "content": {"word_count": len(full_text.split()), "sections": len(self.h2_tags)},
        }


def parse_competitor_html(html: str) -> dict:
    """Pure HTML parsing helper (unit-testable without network access)."""
    parser = CompetitorPageParser()
    parser.feed(html)
    return parser.get_results()


def check_robots_allowed(url: str, *, insecure: bool = False) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(robots_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            lines = resp.read().decode("utf-8", errors="replace").splitlines()
        rp.parse(lines)
        return rp.can_fetch(USER_AGENT, url)
    except (urllib.error.URLError, TimeoutError, OSError):
        return True


def fetch_page(url: str, *, insecure: bool = False) -> str | None:
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def scan_competitor(
    url: str,
    *,
    registry: dict[str, dict] | None = None,
    allow_excluded: bool = False,
    skip_robots: bool = False,
    insecure: bool = False,
) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")
    reg = registry if registry is not None else load_compliance_registry()

    compliance = reg.get(domain, {"status": "not_reviewed"})
    if compliance.get("status") == "excluded" and not allow_excluded:
        return {
            "url": url,
            "domain": domain,
            "last_verified": date.today().isoformat(),
            "status": "blocked_by_compliance",
            "compliance": compliance,
            "message": "Domain is marked excluded in market-intelligence compliance registry. Do not scrape.",
        }

    if not skip_robots and not check_robots_allowed(url, insecure=insecure):
        return {
            "url": url,
            "domain": domain,
            "last_verified": date.today().isoformat(),
            "status": "blocked_by_robots",
            "compliance": compliance,
            "message": "robots.txt disallows automated access. Record compliance review before proceeding.",
        }

    html = fetch_page(url, insecure=insecure)
    if not html:
        return {
            "url": url,
            "domain": domain,
            "last_verified": date.today().isoformat(),
            "status": "error",
            "compliance": compliance,
            "message": "Could not fetch page",
        }

    result = {
        "url": url,
        "domain": domain,
        "last_verified": date.today().isoformat(),
        "status": "success",
        "compliance": compliance,
        "data": parse_competitor_html(html),
        "pricing_page": {"found": False},
    }

    for suffix in ("/pricing", "/plans", "/price"):
        pricing_url = f"{parsed.scheme}://{parsed.netloc}{suffix}"
        if not skip_robots and not check_robots_allowed(pricing_url, insecure=insecure):
            continue
        p_html = fetch_page(pricing_url, insecure=insecure)
        if p_html and len(p_html) > 1000:
            p_data = parse_competitor_html(p_html)
            result["pricing_page"] = {
                "url": pricing_url,
                "found": True,
                "pricing_mentions": p_data["pricing"]["pricing_mentions"],
                "sections": p_data["positioning"]["key_sections"],
            }
            break

    return result


def main():
    parser = argparse.ArgumentParser(description="Compliance-aware competitor website scanner for JENGAI.")
    parser.add_argument("urls", nargs="*", help="One or more competitor URLs.")
    parser.add_argument("--url", action="append", dest="flag_urls", default=[], help="Competitor URL (repeatable).")
    parser.add_argument("--output", choices=["json", "summary"], default="json", help="Output format (default: json).")
    parser.add_argument("--allow-excluded", action="store_true", help="Override excluded domain block (owner approval only).")
    parser.add_argument("--skip-robots", action="store_true", help="Skip robots.txt check (owner override only).")
    parser.add_argument("--insecure", action="store_true", help="Skip SSL verification (fallback only).")
    args = parser.parse_args()

    all_urls = [*args.flag_urls, *args.urls]
    if not all_urls:
        parser.print_help()
        sys.exit(0)

    registry = load_compliance_registry()
    results = [
        scan_competitor(
            u,
            registry=registry,
            allow_excluded=args.allow_excluded,
            skip_robots=args.skip_robots,
            insecure=args.insecure,
        )
        for u in all_urls
    ]

    payload = results[0] if len(results) == 1 else {"competitors": results}
    if args.output == "summary":
        for item in results:
            print(f"- {item['domain']}: {item['status']} (compliance: {item.get('compliance', {}).get('status')})")
    else:
        print(json.dumps(payload, indent=2, default=str))


if __name__ == "__main__":
    main()
