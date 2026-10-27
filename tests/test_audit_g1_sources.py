"""Synthetic positive/negative fixtures for the private G1 source locator."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit_g1_sources import REFERENCES, SourceReference, audit, main, marker_line_numbers  # noqa: E402


class G1SourceAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ck3 = self.root / "private_ck3"
        self.agot = self.root / "private_agot"
        self.reference = SourceReference(
            "CK3", "common/character_interactions/00_war.txt",
            ("declare_war_interaction", "has_any_display_cb_on"),
        )
        self.path = self.ck3 / self.reference.relative_path
        self.path.parent.mkdir(parents=True)

    def test_located_but_unverified(self):
        self.path.write_text(
            "declare_war_interaction = {\n"
            "  has_any_display_cb_on = scope:recipient\n}\n",
            encoding="utf-8",
        )
        result = audit(self.ck3, self.agot, (self.reference,))
        self.assertEqual(result[0]["status"], "LOCATED_UNVERIFIED")
        self.assertEqual(result[0]["markers"]["declare_war_interaction"], [1])
        self.assertEqual(result[0]["markers"]["has_any_display_cb_on"], [2])

    def test_observed_target_identifiers_not_newer_index(self):
        # Original synthetic fixtures: identifiers only, no installed source copied.
        for ref in REFERENCES:
            path = (self.ck3 if ref.source == 'CK3' else self.agot) / ref.relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            if 'character_interactions' in ref.relative_path:
                text = ('declare_war_interaction = {\n'
                        ' can_attack_in_hierarchy = scope:recipient\n'
                        ' has_any_display_cb_on = scope:recipient\n'
                        ' war_declarer_needs_hook_on_liege = no\n}\n')
            elif ref.relative_path.endswith('00_war_and_peace_triggers.txt'):
                text = 'war_declarer_needs_hook_on_liege = { always = no }\n'
            else:
                text = 'synthetic_reference = { always = yes }\n'
            path.write_text(text, encoding='utf-8')
        results = audit(self.ck3, self.agot)
        self.assertTrue(all(r['status'] == 'LOCATED_UNVERIFIED' for r in results))
        # A newer-version identifier cannot silently substitute for the observed gate.
        helper = self.agot / 'common/scripted_triggers/00_war_and_peace_triggers.txt'
        helper.write_text('allows_declaring_war_against_target_trigger = { always = yes }\n')
        changed = audit(self.ck3, self.agot)
        self.assertTrue(any(r['status'] == 'REVIEW_MARKERS' for r in changed))

    def test_missing_source_is_not_success(self):
        result = audit(self.ck3, self.agot, (self.reference,))
        self.assertEqual(result[0]["status"], "MISSING")

    def test_missing_marker_requires_review(self):
        self.path.write_text("declare_war_interaction = { }\n", encoding="utf-8")
        result = audit(self.ck3, self.agot, (self.reference,))
        self.assertEqual(result[0]["status"], "REVIEW_MARKERS")

    def test_comments_and_strings_do_not_count(self):
        text = (
            "# declare_war_interaction = { }\n"
            "message = \"has_any_display_cb_on\"\n"
            "not_declare_war_interaction = { }\n"
        )
        found = marker_line_numbers(text, self.reference.markers)
        self.assertEqual(found, {
            "declare_war_interaction": [],
            "has_any_display_cb_on": [],
        })

    def test_empty_source_requires_review(self):
        self.path.write_text(" \n", encoding="utf-8")
        self.assertEqual(
            audit(self.ck3, self.agot, (self.reference,))[0]["status"], "EMPTY"
        )

    def test_invalid_utf8_requires_review(self):
        self.path.write_bytes(b"\xff")
        self.assertEqual(
            audit(self.ck3, self.agot, (self.reference,))[0]["status"], "UNREADABLE"
        )

    def test_cli_failure_without_private_sources(self):
        from contextlib import redirect_stdout
        from io import StringIO
        output = StringIO()
        with redirect_stdout(output):
            code = main(["--ck3-root", str(self.ck3),
                         "--agot-root", str(self.agot)])
        self.assertEqual(code, 1)
        self.assertIn("MISSING:", output.getvalue())
        self.assertNotIn(str(self.root), output.getvalue())

    def test_no_source_content_or_absolute_paths_in_findings(self):
        self.path.write_text(
            "declare_war_interaction = {\n"
            "  has_any_display_cb_on = scope:recipient\n}\n",
            encoding="utf-8",
        )
        result = str(audit(self.ck3, self.agot, (self.reference,)))
        self.assertNotIn(str(self.root), result)
        self.assertNotIn("scope:recipient", result)


if __name__ == "__main__":
    unittest.main()
