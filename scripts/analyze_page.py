#!/usr/bin/env python3
"""
JENGAI Marketing Page Analyzer — Utility script for JENGAI marketing-* skills.

Analyzes one or more webpages for SEO elements, heading hierarchy, image alt/lazy-load,
schema markup, CTAs, forms, JENGAI web stack (GA4, HubSpot, Calendly), and optional
Google PageSpeed Insights Core Web Vitals (LCP, INP, CLS).
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urlparse


JENGAI_GA4_ID = "G-EJJJHWZFQQ"
JENGAI_HUBSPOT_PORTAL = "51915935"
JENGAI_CALENDLY_HOST = "calendly.com"


class MarketingPageParser(HTMLParser):
    """Parse HTML and extract marketing, SEO, tracking, and conversion elements."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.meta_keywords = ""
        self.og_tags = {}
        self.headings = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}
        self.links = []
        self.images = []
        self.forms = []
        self.buttons = []
        self.scripts = []
        self.iframes = []
        self.schema_data = []
        self.ctas = []
        self.social_links = []
        self.tracking_scripts = []
        self.jengai_stack = {
            "ga4_measurement_id_present": False,
            "hubspot_portal_present": False,
            "calendly_embed_present": False,
            "calendly_booking_ga4_listener": False,
            "hubspot_forms_api_present": False,
        }

        self._in_title = False
        self._in_heading = None
        self._in_button = False
        self._in_a = False
        self._in_script = False
        self._in_style = False
        self._in_form = False
        self._script_type = ""
        self._current_text = ""
        self._current_form = {}
        self._form_fields = []
        self._text_content = []
        self._has_viewport = False
        self._canonical = ""
        self._robots_meta = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "title":
            self._in_title = True
            self._current_text = ""
        elif tag == "style":
            self._in_style = True
        elif tag == "meta":
            name = (attrs_dict.get("name") or "").lower()
            prop = (attrs_dict.get("property") or "").lower()
            content = attrs_dict.get("content") or ""
            if name == "description":
                self.meta_description = content
            elif name == "keywords":
                self.meta_keywords = content
            elif name == "viewport":
                self._has_viewport = True
            elif name == "robots":
                self._robots_meta = content
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
        elif tag == "link":
            rel = (attrs_dict.get("rel") or "").lower()
            if "canonical" in rel:
                self._canonical = attrs_dict.get("href") or ""
        elif tag in self.headings:
            self._in_heading = tag
            self._current_text = ""
        elif tag == "a":
            self._in_a = True
            self._current_text = ""
            href = attrs_dict.get("href") or ""
            self.links.append({"href": href, "text": ""})
            for platform in (
                "twitter.com", "x.com", "facebook.com", "linkedin.com",
                "instagram.com", "youtube.com", "tiktok.com", "github.com",
            ):
                if platform in href.lower():
                    self.social_links.append({"platform": platform.split(".")[0], "url": href})
            if JENGAI_CALENDLY_HOST in href.lower():
                self.jengai_stack["calendly_embed_present"] = True
        elif tag == "iframe":
            src = attrs_dict.get("src") or ""
            self.iframes.append(src)
            if JENGAI_CALENDLY_HOST in src.lower():
                self.jengai_stack["calendly_embed_present"] = True
        elif tag == "div":
            data_url = (attrs_dict.get("data-url") or "").lower()
            if JENGAI_CALENDLY_HOST in data_url:
                self.jengai_stack["calendly_embed_present"] = True
            if attrs_dict.get("data-portal-id") == JENGAI_HUBSPOT_PORTAL:
                self.jengai_stack["hubspot_portal_present"] = True
        elif tag == "img":
            self.images.append({
                "src": attrs_dict.get("src") or "",
                "alt": attrs_dict.get("alt") or "",
                "has_alt": "alt" in attrs_dict,
                "loading": (attrs_dict.get("loading") or "").lower(),
            })
        elif tag == "button":
            self._in_button = True
            self._current_text = ""
        elif tag == "form":
            self._in_form = True
            self._current_form = {
                "action": attrs_dict.get("action") or "",
                "method": (attrs_dict.get("method") or "GET").upper(),
            }
            self._form_fields = []
        elif tag in ("input", "select", "textarea") and self._in_form:
            self._form_fields.append({
                "tag": tag,
                "type": attrs_dict.get("type", "text"),
                "name": attrs_dict.get("name") or "",
                "placeholder": attrs_dict.get("placeholder") or "",
                "required": "required" in attrs_dict,
            })
        elif tag == "script":
            self._in_script = True
            self._script_type = (attrs_dict.get("type") or "").lower()
            self._current_text = ""
            src = attrs_dict.get("src") or ""
            if src:
                self.scripts.append(src)
                src_lower = src.lower()
                if JENGAI_GA4_ID.lower() in src_lower:
                    self.jengai_stack["ga4_measurement_id_present"] = True
                if JENGAI_HUBSPOT_PORTAL in src_lower:
                    self.jengai_stack["hubspot_portal_present"] = True
                if JENGAI_CALENDLY_HOST in src_lower:
                    self.jengai_stack["calendly_embed_present"] = True
                indicators = {
                    "gtag": "Google Analytics 4 (gtag)",
                    "googletagmanager": "Google Tag Manager",
                    "hs-scripts": "HubSpot Tracking",
                    "hsforms": "HubSpot Forms",
                    "hubspot": "HubSpot",
                    "snap.licdn": "LinkedIn Insight Tag",
                    "fbevents": "Meta Pixel",
                    "clarity": "Microsoft Clarity",
                    "hotjar": "Hotjar",
                    "calendly": "Calendly",
                }
                for needle, label in indicators.items():
                    if needle in src_lower:
                        self.tracking_scripts.append(label)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.title = self._current_text.strip()
        elif tag == "style":
            self._in_style = False
        elif tag in self.headings and self._in_heading == tag:
            text = " ".join(self._current_text.split())
            if text:
                self.headings[tag].append(text)
            self._in_heading = None
        elif tag == "a" and self._in_a:
            self._in_a = False
            text = " ".join(self._current_text.split())
            if self.links:
                self.links[-1]["text"] = text
            cta_words = (
                "book a demo", "request demo", "schedule", "discovery call",
                "get started", "contact us", "see pricing", "learn more",
                "watch demo", "sign up", "register", "download",
            )
            text_lower = text.lower()
            for cta in cta_words:
                if cta in text_lower:
                    self.ctas.append({"text": text, "href": self.links[-1]["href"], "type": "link"})
                    break
        elif tag == "button" and self._in_button:
            self._in_button = False
            text = " ".join(self._current_text.split())
            if text:
                self.buttons.append(text)
                self.ctas.append({"text": text, "type": "button"})
        elif tag == "form" and self._in_form:
            self._in_form = False
            self._current_form["fields"] = self._form_fields
            self._current_form["field_count"] = len(self._form_fields)
            self.forms.append(self._current_form)
        elif tag == "script" and self._in_script:
            self._in_script = False
            body = self._current_text
            if JENGAI_GA4_ID in body:
                self.jengai_stack["ga4_measurement_id_present"] = True
            if JENGAI_HUBSPOT_PORTAL in body:
                self.jengai_stack["hubspot_portal_present"] = True
            if "api.hsforms.com/submissions/v3" in body:
                self.jengai_stack["hubspot_forms_api_present"] = True
            if "calendly.event_scheduled" in body or "calendly_booking" in body:
                self.jengai_stack["calendly_booking_ga4_listener"] = True
            if "gtag" in body or "dataLayer" in body:
                self.tracking_scripts.append("Google Analytics/GTM (inline)")
            if self._script_type == "application/ld+json":
                try:
                    parsed = json.loads(body)
                    if isinstance(parsed, list):
                        self.schema_data.extend(parsed)
                    elif isinstance(parsed, dict):
                        if "@graph" in parsed and isinstance(parsed["@graph"], list):
                            self.schema_data.extend(parsed["@graph"])
                        else:
                            self.schema_data.append(parsed)
                except (json.JSONDecodeError, ValueError):
                    pass

    def handle_data(self, data):
        if self._in_title or self._in_heading or self._in_a or self._in_button or self._in_script:
            self._current_text += data
        if not self._in_script and not self._in_style and not self._in_title:
            stripped = data.strip()
            if stripped:
                self._text_content.append(stripped)

    def get_full_text(self):
        return " ".join(self._text_content)

    def get_results(self):
        images_without_alt = sum(
            1 for img in self.images if not img.get("has_alt") or not img.get("alt").strip()
        )
        images_with_lazy = sum(1 for img in self.images if img.get("loading") == "lazy")

        heading_issues = []
        if not self.headings["h1"]:
            heading_issues.append("Missing H1 tag")
        elif len(self.headings["h1"]) > 1:
            heading_issues.append(f"Multiple H1 tags ({len(self.headings['h1'])})")
        if self.headings["h3"] and not self.headings["h2"]:
            heading_issues.append("H3 used without H2 (skipped level)")

        tracking = sorted(set(self.tracking_scripts))
        word_count = len(self.get_full_text().split())
        schema_types = [s.get("@type", "Unknown") for s in self.schema_data if isinstance(s, dict)]

        return {
            "seo": {
                "title": self.title,
                "title_length": len(self.title),
                "title_ok": 30 <= len(self.title) <= 60,
                "meta_description": self.meta_description,
                "meta_description_length": len(self.meta_description),
                "meta_description_ok": 120 <= len(self.meta_description) <= 160,
                "canonical": self._canonical,
                "robots_meta": self._robots_meta,
                "has_viewport": self._has_viewport,
                "og_tags": self.og_tags,
                "headings": {k: v for k, v in self.headings.items() if v},
                "heading_issues": heading_issues,
                "images_total": len(self.images),
                "images_without_alt": images_without_alt,
                "images_with_lazy_loading": images_with_lazy,
            },
            "content": {
                "word_count": word_count,
                "headings_count": sum(len(v) for v in self.headings.values()),
                "h1": self.headings["h1"],
                "h2": self.headings["h2"],
            },
            "conversion": {
                "ctas": self.ctas[:25],
                "cta_count": len(self.ctas),
                "forms": self.forms,
                "form_count": len(self.forms),
                "buttons": self.buttons[:25],
            },
            "trust": {
                "social_links": self.social_links,
                "social_link_count": len(self.social_links),
            },
            "tracking": {
                "tools_detected": tracking,
                "tools_count": len(tracking),
                "jengai_stack": self.jengai_stack,
                "schema_types": schema_types,
                "schema_count": len(schema_types),
            },
            "technical": {
                "total_links": len(self.links),
                "internal_links": 0,
                "external_links": 0,
                "scripts_count": len(self.scripts),
                "iframes_count": len(self.iframes),
            },
        }


def _ssl_context(insecure: bool) -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_url(url: str, *, insecure: bool = False, timeout: int = 15) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; JENGAIMarketingAudit/2.0; +https://www.jengai.com)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context(insecure)) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def fetch_robots_txt(url: str, *, insecure: bool = False) -> dict:
    parsed = urlparse(url)
    content = fetch_url(f"{parsed.scheme}://{parsed.netloc}/robots.txt", insecure=insecure)
    if content:
        return {
            "exists": True,
            "has_sitemap_reference": "sitemap:" in content.lower(),
            "content_preview": content[:500],
        }
    return {"exists": False}


def fetch_sitemap(url: str, *, insecure: bool = False) -> dict:
    parsed = urlparse(url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    content = fetch_url(sitemap_url, insecure=insecure)
    if not content:
        return {"exists": False, "url_count": 0, "urls": []}
    urls = []
    try:
        root = ET.fromstring(content)
        for elem in root.iter():
            if elem.tag.endswith("loc") and elem.text:
                urls.append(elem.text.strip())
    except ET.ParseError:
        urls = re.findall(r"<loc>(.*?)</loc>", content, re.IGNORECASE)
    return {"exists": True, "url_count": len(urls), "urls": urls}


def fetch_pagespeed_cwv(url: str, api_key: str, *, strategy: str = "mobile", insecure: bool = False) -> dict | None:
    qs = urllib.parse.urlencode({"url": url, "strategy": strategy, "key": api_key, "category": "performance"})
    endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?{qs}"
    raw = fetch_url(endpoint, insecure=insecure, timeout=45)
    if not raw:
        return None
    try:
        data = json.loads(raw)
        audits = data.get("lighthouseResult", {}).get("audits", {})
        perf_score = data.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score")
        field = data.get("loadingExperience", {}).get("metrics", {})
        return {
            "strategy": strategy,
            "performance_score": round(perf_score * 100) if isinstance(perf_score, (int, float)) else None,
            "lab": {
                "lcp": audits.get("largest-contentful-paint", {}).get("displayValue"),
                "cls": audits.get("cumulative-layout-shift", {}).get("displayValue"),
                "tbt": audits.get("total-blocking-time", {}).get("displayValue"),
                "fcp": audits.get("first-contentful-paint", {}).get("displayValue"),
            },
            "field_crux": {
                "lcp_ms": field.get("LARGEST_CONTENTFUL_PAINT_MS", {}).get("percentile"),
                "inp_ms": field.get("INTERACTION_TO_NEXT_PAINT", {}).get("percentile"),
                "cls": field.get("CUMULATIVE_LAYOUT_SHIFT_SCORE", {}).get("percentile"),
            },
        }
    except (json.JSONDecodeError, AttributeError):
        return None


def analyze_html(html: str, url: str) -> dict:
    """Pure HTML analysis helper (unit-testable without network access)."""
    parser = MarketingPageParser()
    parser.feed(html)
    page_results = parser.get_results()

    domain = urlparse(url).netloc
    internal = 0
    external = 0
    for link in parser.links:
        href = link.get("href", "")
        if href.startswith("/") or (domain and domain in href):
            internal += 1
        elif href.startswith("http"):
            external += 1
    page_results["technical"]["internal_links"] = internal
    page_results["technical"]["external_links"] = external

    # 0-100 scoring aligned with marketing-audit
    seo = page_results["seo"]
    seo_score = 100
    if not seo["title"]:
        seo_score -= 25
    elif not seo["title_ok"]:
        seo_score -= 10
    if not seo["meta_description"]:
        seo_score -= 20
    elif not seo["meta_description_ok"]:
        seo_score -= 10
    if not seo["headings"].get("h1"):
        seo_score -= 20
    if seo["heading_issues"]:
        seo_score -= 10
    if seo["images_total"] > 0 and seo["images_without_alt"] > 0:
        seo_score -= min(15, round(15 * (seo["images_without_alt"] / seo["images_total"])))
    if not seo["has_viewport"]:
        seo_score -= 10
    seo_score = max(0, seo_score)

    conv = page_results["conversion"]
    cta_score = 20 if conv["cta_count"] == 0 else (70 if conv["cta_count"] < 4 else 85)
    if any("demo" in c.get("text", "").lower() or "discovery" in c.get("text", "").lower() for c in conv["ctas"]):
        cta_score = min(100, cta_score + 15)

    tracking = page_results["tracking"]
    track_score = min(100, 30 + tracking["tools_count"] * 20 + (15 if tracking["schema_count"] > 0 else 0))

    page_results["scores_100"] = {
        "seo_technical": seo_score,
        "cta_presence": cta_score,
        "tracking_and_schema": track_score,
    }
    return page_results


def analyze(url: str, *, insecure: bool = False, crawl_sitemap: bool = False, max_pages: int = 10, psi_key: str | None = None) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    html = fetch_url(url, insecure=insecure)
    if not html:
        return {"url": url, "date": date.today().isoformat(), "status": "error", "message": "Could not fetch page"}

    page_results = analyze_html(html, url)
    page_results["robots"] = fetch_robots_txt(url, insecure=insecure)
    sitemap = fetch_sitemap(url, insecure=insecure)
    page_results["sitemap"] = {"exists": sitemap["exists"], "url_count": sitemap["url_count"]}

    result = {
        "url": url,
        "date": date.today().isoformat(),
        "status": "success",
        "analysis": page_results,
    }

    if psi_key:
        result["core_web_vitals"] = fetch_pagespeed_cwv(url, psi_key, insecure=insecure)

    if crawl_sitemap and sitemap.get("urls"):
        pages_summary = []
        for page_url in sitemap["urls"][:max_pages]:
            sub_html = fetch_url(page_url, insecure=insecure)
            if not sub_html:
                pages_summary.append({"url": page_url, "status": "error"})
                continue
            sub = analyze_html(sub_html, page_url)
            pages_summary.append({
                "url": page_url,
                "status": "success",
                "title": sub["seo"]["title"],
                "title_ok": sub["seo"]["title_ok"],
                "meta_ok": sub["seo"]["meta_description_ok"],
                "h1_count": len(sub["content"]["h1"]),
                "images_without_alt": sub["seo"]["images_without_alt"],
                "schema_types": sub["tracking"]["schema_types"],
                "seo_technical_score": sub["scores_100"]["seo_technical"],
            })
        result["sitemap_crawl"] = pages_summary

    return result


def main():
    parser = argparse.ArgumentParser(description="Analyze webpages for JENGAI SEO, CRO, and tracking audits.")
    parser.add_argument("url", help="Target URL to analyze (e.g., https://www.jengai.com).")
    parser.add_argument("--sitemap", action="store_true", help="Also crawl URLs from /sitemap.xml.")
    parser.add_argument("--max-pages", type=int, default=10, help="Max sitemap pages to crawl (default: 10).")
    parser.add_argument("--psi-key", default=None, help="Optional Google PageSpeed Insights API key for LCP/INP/CLS.")
    parser.add_argument("--insecure", action="store_true", help="Skip SSL certificate verification (fallback only).")
    parser.add_argument("--output", default=None, help="Optional file path to write JSON output.")
    args = parser.parse_args()

    res = analyze(
        args.url,
        insecure=args.insecure,
        crawl_sitemap=args.sitemap,
        max_pages=args.max_pages,
        psi_key=args.psi_key,
    )
    rendered = json.dumps(res, indent=2, default=str)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
