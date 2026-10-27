"""Build safety and structural fixtures only; CK3 behavior is not exercised."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build_g1_probe import build, helper_block, HELPER, GUARD, REPO
from validate_mod import brace_errors

SYNTHETIC = '''# unrelated { brace in comment
unrelated = { text = "}" }
war_declarer_needs_hook_on_liege = {
 scope:actor = {
  liege != scope:recipient
  OR = {
   has_character_flag = vassal_internal_wars_banned
   has_character_flag = vassal_all_wars_banned
  }
  NOT = { has_character_flag = vassal_contract_war_override }
 }
}
'''


class BuildProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.agot = self.root / 'agot'
        self.source = self.agot / 'common/scripted_triggers/00_war_and_peace_triggers.txt'
        self.source.parent.mkdir(parents=True)
        self.source.write_text(SYNTHETIC, encoding='utf-8-sig')
        (self.agot / 'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="1.19.0.6"\n')
        self.out = self.root / 'private'

    def test_build_preserves_source_and_original_body(self):
        before = self.source.read_bytes()
        build(self.agot, self.out)
        patched = (self.out / 'rw_g1_probe/common/scripted_triggers/zz_rw_g1_probe.txt').read_text(encoding='utf-8-sig')
        head, body = helper_block(SYNTHETIC)
        self.assertEqual(head + GUARD + body + '\n', patched)
        self.assertEqual(before, self.source.read_bytes())
        self.assertNotIn('unrelated', patched)
        self.assertEqual([], brace_errors(patched))
        self.assertEqual(1, len(list((self.out / 'rw_g1_probe').rglob('*.txt'))))
        self.assertNotIn(str(self.agot), (self.out / 'receipt.json').read_text())

    def test_existing_output_rejected(self):
        self.out.mkdir()
        with self.assertRaises(ValueError): build(self.agot, self.out)

    def test_installed_source_output_rejected(self):
        with self.assertRaises(ValueError): build(self.agot, self.agot / 'probe')

    def test_repo_output_rejected(self):
        with self.assertRaises(ValueError): build(self.agot, REPO / 'private-probe')

    def test_changed_version_rejected(self):
        (self.agot / 'descriptor.mod').write_text('version="9.9"\nsupported_version="1.19.0.6"')
        with self.assertRaises(ValueError): build(self.agot, self.out)
        self.assertFalse(self.out.exists())

    def test_duplicate_definition_rejected(self):
        with self.assertRaises(ValueError): helper_block(SYNTHETIC + '\n' + HELPER + ' = {}')

    def test_malformed_source_rejected(self):
        with self.assertRaises(ValueError): helper_block(SYNTHETIC + '}')

    def test_unknown_layout_rejected(self):
        self.source.write_text(HELPER + ' = { always = yes }')
        with self.assertRaises(ValueError): build(self.agot, self.out)
        self.assertFalse(self.out.exists())
