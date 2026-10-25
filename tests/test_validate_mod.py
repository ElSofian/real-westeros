"""Positive and negative fixtures for the structural validator."""

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate_mod import brace_errors, validate  # noqa: E402

META = 'name="Real Westeros"\nversion="0.1.0"\nsupported_version="1.19.*"\n'


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        mod = self.root / 'mod' / 'real_westeros'
        for folder in (
            'common/character_interactions', 'common/scripted_triggers',
            'common/scripted_effects', 'common/on_action',
            'events', 'localization/english',
        ):
            (mod / folder).mkdir(parents=True)
        (self.root / 'mod' / 'real_westeros.mod').write_text(META + 'path="mod/real_westeros"\n', encoding='utf-8')
        (mod / 'descriptor.mod').write_text(META, encoding='utf-8')
        self.mod = mod

    def test_valid_scaffold(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_folder(self):
        (self.mod / 'events').rmdir()
        self.assertTrue(any('missing directory' in e for e in validate(self.root)))

    def test_wrong_path(self):
        (self.root / 'mod' / 'real_westeros.mod').write_text(META + 'path="C:/personal"\n')
        self.assertTrue(any('expected relative path' in e for e in validate(self.root)))

    def test_metadata_mismatch(self):
        (self.mod / 'descriptor.mod').write_text(META.replace('0.1.0', '0.2.0'))
        self.assertTrue(any('version differs' in e for e in validate(self.root)))

    def test_duplicate_descriptor_key(self):
        (self.mod / 'descriptor.mod').write_text(META + 'version="0.2.0"\n')
        self.assertTrue(any('duplicate descriptor key' in e for e in validate(self.root)))

    def test_unbalanced_braces(self):
        (self.mod / 'events' / 'example.txt').write_text('event = {\n')
        self.assertTrue(any('unclosed brace' in e for e in validate(self.root)))

    def test_comments_and_strings_not_counted(self):
        self.assertEqual(brace_errors('a = { # }\n x = "{ } # \\" "\n}\n'), [])

    def test_invalid_utf8(self):
        (self.mod / 'events' / 'bad.txt').write_bytes(b'\xff\xfe')
        self.assertTrue(any('invalid UTF-8' in e for e in validate(self.root)))

    def test_duplicate_top_level_trigger(self):
        folder = self.mod / 'common' / 'scripted_triggers'
        (folder / 'a.txt').write_text('rw_test = { always = yes }\n')
        (folder / 'b.txt').write_text('rw_test = { always = no }\n')
        self.assertTrue(any('duplicate top-level' in e for e in validate(self.root)))

    def test_nested_repeated_keys_are_valid(self):
        (self.mod / 'common' / 'scripted_effects' / 'x.txt').write_text('rw_x = { add_gold = 1\n add_gold = 2\n}\n')
        self.assertEqual(validate(self.root), [])

    def test_localization_duplicates(self):
        path = self.mod / 'localization' / 'english' / 'rw_l_english.yml'
        path.write_text('l_english:\n rw_key:0 "One"\n rw_key:0 "Two"\n', encoding='utf-8-sig')
        self.assertTrue(any('duplicate rw_key' in e for e in validate(self.root)))

    def test_archive_forbidden(self):
        (self.mod / 'game.zip').write_bytes(b'fake')
        self.assertTrue(any('forbidden archive' in e for e in validate(self.root)))


if __name__ == '__main__':
    unittest.main()
