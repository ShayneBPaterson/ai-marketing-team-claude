"""Unit tests for analyze_page, competitor_scanner, social_calendar, and generate_pdf_report."""

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_page  # noqa: E402
import competitor_scanner  # noqa: E402
import generate_pdf_report  # noqa: E402
import social_calendar  # noqa: E402


class AnalyzePageTests(unittest.TestCase):
    def test_excludes_script_and_style_from_word_count_and_detects_jengai_stack(self):
        html = """
        <html>
          <head>
            <title>Pricing and Operations Platform for Commercial Subcontractors | JENGAI</title>
            <meta name="description" content="JENGAI helps commercial finish-trade subcontractors sell more while protecting margins. Book a demo today to see how teams protect estimator hours.">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>.hero { color: #000180; font-family: Inter; }</style>
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-EJJJHWZFQQ"></script>
            <script id="hs-script-loader" src="//js.hs-scripts.com/51915935.js"></script>
            <script type="application/ld+json">{"@type": "SoftwareApplication", "name": "JENGAI"}</script>
          </head>
          <body>
            <h1>Pipeline management, reinvented.</h1>
            <p>Sell more while protecting your margins.</p>
            <a href="/demo">Book a demo</a>
            <iframe src="https://calendly.com/renata-jengai/jengai-discovery-call"></iframe>
            <script>console.log("this script text should not inflate word count one two three four five");</script>
          </body>
        </html>
        """
        res = analyze_page.analyze_html(html, "https://www.jengai.com/")
        self.assertEqual(res["content"]["h1"], ["Pipeline management, reinvented."])
        self.assertLess(res["content"]["word_count"], 20)
        stack = res["tracking"]["jengai_stack"]
        self.assertTrue(stack["ga4_measurement_id_present"])
        self.assertTrue(stack["hubspot_portal_present"])
        self.assertTrue(stack["calendly_embed_present"])
        self.assertFalse(stack["calendly_booking_ga4_listener"])
        self.assertIn("SoftwareApplication", res["tracking"]["schema_types"])


class CompetitorScannerTests(unittest.TestCase):
    def test_blocks_excluded_domains_by_default(self):
        res = competitor_scanner.scan_competitor("https://www.enr.com/articles/123", registry={"enr.com": {"status": "excluded"}})
        self.assertEqual(res["status"], "blocked_by_compliance")

    def test_parses_competitor_signals(self):
        html = """
        <html><head><title>Example Sub Tool</title></head>
        <body>
          <h1>Bid management for commercial flooring and tile</h1>
          <h2>Integrates with BuildingConnected and MeasureSquare</h2>
          <p>Starts at $299 /month with a free trial.</p>
          <a href="/demo">Book a demo</a>
        </body></html>
        """
        data = competitor_scanner.parse_competitor_html(html)
        self.assertIn("flooring", data["finish_trade_signals"])
        self.assertIn("tile", data["finish_trade_signals"])
        self.assertIn("BuildingConnected", data["integrations_mentioned"])
        self.assertIn("MeasureSquare", data["integrations_mentioned"])
        self.assertTrue(data["pricing"]["has_pricing_info"])


class SocialCalendarTests(unittest.TestCase):
    def test_generates_weekly_jengai_cadence(self):
        cal = social_calendar.generate_weekly_calendar("2026-11-23", weeks=8, events={3: "Starnet Fall Meeting"})
        self.assertEqual(cal["brand"], "JENGAI")
        self.assertEqual(len(cal["calendar"]), 8)
        self.assertEqual(cal["calendar"][2]["event_anchor"], "Starnet Fall Meeting")
        self.assertEqual(cal["calendar"][0]["pillar_id"], "protect-margins")
        self.assertEqual(cal["calendar"][4]["pillar_id"], "sell-more")
        md = social_calendar.render_markdown(cal)
        self.assertIn("1 LinkedIn post + 1 Constant Contact nurture email per week", md)
        self.assertIn("Starnet Fall Meeting", md)


class PdfReportTests(unittest.TestCase):
    def test_competitor_table_uses_target_comparison_not_brand_name_bug(self):
        data = {
            "brand_name": "JENGAI",
            "target_comparison": {
                "positioning": "Pricing and operations platform for finish trades",
                "pricing": "$800/loc Starter + seats",
                "social_proof": "Bonitz, Pro-United, Silver Slate",
                "content": "Weekly LinkedIn + Constant Contact",
            },
            "competitors": [
                {"name": "MeasureSquare CRM", "positioning": "Bundled takeoff + CRM", "pricing": "Tiered", "social_proof": "Install base", "content": "Product tutorials"},
            ],
        }
        rows = generate_pdf_report.build_competitor_table_rows(data)
        self.assertEqual(rows[0], ["Dimension", "JENGAI", "MeasureSquare CRM"])
        self.assertEqual(rows[1][1], "Pricing and operations platform for finish trades")
        self.assertNotEqual(rows[1][1], "JENGAI")


if __name__ == "__main__":
    unittest.main()
