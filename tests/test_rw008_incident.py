"""Static integration fixtures only: no CK3 effects or event scopes execute here."""
from pathlib import Path
import shutil
import tempfile
import unittest
from tools.validate_mod import validate

ROOT = Path(__file__).resolve().parents[1]


class IncidentStructureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / 'mod', self.root / 'mod')

    def test_integrated_mod_passes(self):
        self.assertEqual([], validate(self.root))

    def test_broken_event_rejected(self):
        event = self.root / 'mod/real_westeros/events/rw_reconciliation_events.txt'
        event.write_text(event.read_text() + '\n}', encoding='utf-8')
        self.assertTrue(any('unexpected closing brace' in e for e in validate(self.root)))

    def test_colliding_trigger_rejected(self):
        target = self.root / 'mod/real_westeros/common/scripted_triggers/collision.txt'
        target.write_text('rw_can_petition_trigger = { always = yes }\n')
        self.assertTrue(any('duplicate top-level rw_can_petition_trigger' in e for e in validate(self.root)))

    def test_colliding_translation_rejected(self):
        target = self.root / 'mod/real_westeros/localization/english/collision_l_english.yml'
        target.write_text('l_english:\n rw_reconciliation.0001.accept:0 "collision"\n', encoding='utf-8-sig')
        self.assertTrue(any('duplicate rw_reconciliation.0001.accept' in e for e in validate(self.root)))

    def test_translations_cover_display_keys(self):
        import re
        keys = {
            'rw_seek_reconciliation_interaction',
            'rw_seek_reconciliation_interaction_desc',
            'rw_reconciliation_accepted_opinion',
            'rw_reconciliation_refused_opinion',
        }
        event = (ROOT / 'mod/real_westeros/events/rw_reconciliation_events.txt').read_text()
        keys.update(re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', event))
        for language in ('english', 'french'):
            text = (ROOT / f'mod/real_westeros/localization/{language}/rw_reconciliation_l_{language}.yml').read_text(encoding='utf-8-sig')
            actual = set(re.findall(r'^\s+([\w.]+):0', text, re.M))
            self.assertEqual(keys, actual)


if __name__ == '__main__':
    unittest.main()
