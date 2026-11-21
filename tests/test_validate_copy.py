"""Unit tests for scripts/validate_copy.py."""

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_copy  # noqa: E402


class ValidateCopyTests(unittest.TestCase):
    def test_clean_jengai_copy_passes(self):
        text = (
            "JENGAI is a pricing and operations platform for commercial specialty contractors.\n"
            "Bonitz achieved 40% faster takeoff turnaround via Automated Plan Analysis (APA).\n"
            "Transylvania Flooring Professionals saw a 30-40% increase in bids sent.\n"
            "Visit https://www.jengai.com/success-stories to see customer stories.\n"
        )
        res = validate_copy.validate_text(text, public=True, register="external")
        self.assertTrue(res["passed"], res["errors"])
        self.assertEqual(res["error_count"], 0)

    def test_catches_lowercase_jengai_but_ignores_urls(self):
        text = "Jengai helps contractors at https://www.jengai.com and sales@jengai.com.\n"
        res = validate_copy.validate_text(text)
        self.assertFalse(res["passed"])
        casing_errors = [e for e in res["errors"] if e["rule"] == "brand-casing"]
        self.assertEqual(len(casing_errors), 1)
        self.assertEqual(casing_errors[0]["match"], "Jengai")

    def test_catches_retired_positioning_and_banned_claims(self):
        text = (
            "JENGAI is an AI estimating tool that eliminates errors with 50% faster pricing "
            "and a 100% accuracy guarantee. It ranks incoming bids by win-probability scoring "
            "and delivers 40% faster estimation for our 37 customers.\n"
        )
        res = validate_copy.validate_text(text, public=True)
        self.assertFalse(res["passed"])
        rules = {e["rule"] for e in res["errors"]}
        self.assertIn("positioning-lock", rules)
        self.assertIn("claim-governance", rules)
        self.assertGreaterEqual(res["error_count"], 6)

    def test_catches_ai_and_corporate_words(self):
        text = "Honestly, JENGAI will seamlessly leverage cutting-edge workflows. Here's the thing: delve in.\n"
        res = validate_copy.validate_text(text)
        self.assertFalse(res["passed"])
        matches = {e["match"].lower() for e in res["errors"]}
        self.assertTrue({"honestly", "seamlessly", "leverage", "cutting-edge", "delve"}.issubset(matches))

    def test_public_mode_blocks_competitors_and_warns_planhub(self):
        text = "Unlike STACK and Bobyard, contractors using PlanHub saw faster bids.\n"
        res = validate_copy.validate_text(text, public=True)
        self.assertFalse(res["passed"])
        err_matches = {e["match"] for e in res["errors"]}
        self.assertIn("STACK", err_matches)
        self.assertIn("Bobyard", err_matches)
        warn_matches = {w["match"] for w in res["warnings"]}
        self.assertIn("PlanHub", warn_matches)

    def test_outreach_register_rejects_contractions(self):
        text = "Dear Michael,\nWe're reaching out because you don't want missed follow-ups.\n"
        res = validate_copy.validate_text(text, register="outreach")
        self.assertFalse(res["passed"])
        rules = [e["rule"] for e in res["errors"]]
        self.assertIn("outreach-no-contractions", rules)

    def test_legacy_seo_audit_triggers_expected_violations(self):
        legacy = ROOT / "archive" / "2026-08-19-legacy-seo-audit.md"
        self.assertTrue(legacy.is_file())
        res = validate_copy.validate_text(legacy.read_text(encoding="utf-8"), public=False)
        self.assertFalse(res["passed"])
        rules = {e["rule"] for e in res["errors"]}
        self.assertIn("positioning-lock", rules)
        self.assertIn("claim-governance", rules)


if __name__ == "__main__":
    unittest.main()
