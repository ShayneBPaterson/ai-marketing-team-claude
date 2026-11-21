"""Repository integrity tests for JENGAI AI Marketing Team skills, agents, and templates."""

import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_copy  # noqa: E402

EXPECTED_SKILLS = {
    "marketing",
    "marketing-ads",
    "marketing-audit",
    "marketing-brand",
    "marketing-case-study",
    "marketing-competitors",
    "marketing-copy",
    "marketing-emails",
    "marketing-event",
    "marketing-funnel",
    "marketing-landing",
    "marketing-launch",
    "marketing-report",
    "marketing-report-pdf",
    "marketing-seo",
    "marketing-social",
    "marketing-voice-check",
    "marketing-weekly-cadence",
    "marketing-workshop",
}

EXPECTED_AGENTS = {
    # 5 Execution agents
    "marketing-campaigns.md",
    "marketing-cmo.md",
    "marketing-editor.md",
    "marketing-intel.md",
    "marketing-proof.md",
    # 5 Parallel audit subagents
    "marketing-competitive.md",
    "marketing-content.md",
    "marketing-conversion.md",
    "marketing-strategy.md",
    "marketing-technical.md",
}


class RepoIntegrityTests(unittest.TestCase):
    def test_expected_skills_and_frontmatter(self):
        skills_dir = ROOT / "skills"
        found = {p.name for p in skills_dir.iterdir() if p.is_dir()}
        self.assertEqual(found, EXPECTED_SKILLS)

        for name in sorted(found):
            skill_md = skills_dir / name / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing {skill_md}")
            text = skill_md.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), f"{skill_md} missing YAML frontmatter")
            fm_end = text.find("\n---\n", 4)
            self.assertGreater(fm_end, 4, f"{skill_md} unclosed YAML frontmatter")
            fm = text[4:fm_end]
            self.assertRegex(fm, rf"(?m)^name:\s*{re.escape(name)}\s*$")
            self.assertRegex(fm, r"(?m)^description:\s*.+$")
            self.assertNotIn("/Users/", text, f"Hardcoded macOS user path in {skill_md}")
            self.assertNotRegex(text, r"/market\s+[a-z]", f"Legacy /market command reference in {skill_md}")

    def test_expected_agents_and_frontmatter(self):
        agents_dir = ROOT / "agents"
        found = {p.name for p in agents_dir.iterdir() if p.is_file() and p.suffix == ".md"}
        self.assertEqual(found, EXPECTED_AGENTS)

        for fname in sorted(found):
            agent_md = agents_dir / fname
            text = agent_md.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), f"{agent_md} missing YAML frontmatter")
            fm_end = text.find("\n---\n", 4)
            self.assertGreater(fm_end, 4, f"{agent_md} unclosed YAML frontmatter")
            fm = text[4:fm_end]
            expected_name = fname[:-3]
            self.assertRegex(fm, rf"(?m)^name:\s*{re.escape(expected_name)}\s*$")
            self.assertRegex(fm, r"(?m)^description:\s*.+$")
            self.assertRegex(fm, r"(?m)^tools:\s*.+$")
            self.assertNotIn("/Users/", text, f"Hardcoded macOS user path in {agent_md}")

    def test_templates_pass_jengai_copy_validator(self):
        templates_dir = ROOT / "templates"
        files = sorted(templates_dir.iterdir())
        self.assertEqual(len(files), 7)
        for tpl in files:
            text = tpl.read_text(encoding="utf-8")
            # competitor-profile.md is internal; all others checked in public mode too
            is_public = tpl.name != "competitor-profile.md"
            res = validate_copy.validate_text(text, public=is_public, register="external")
            self.assertTrue(res["passed"], f"Template {tpl.name} failed validation: {res['errors']}")

    def test_no_binaries_added_outside_legacy_banner(self):
        banned_exts = {".pdf", ".docx", ".xlsx", ".pptx"}
        for path in ROOT.rglob("*"):
            if ".git" in path.parts:
                continue
            self.assertNotIn(path.suffix.lower(), banned_exts, f"Binary deliverable found in repo: {path}")


if __name__ == "__main__":
    unittest.main()
