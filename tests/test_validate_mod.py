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

    def test_owned_calls_resolve_across_files_and_forward_definitions(self):
        (self.mod / 'events/rw_caller.txt').write_text(
            'rw_fixture.0001 = { trigger = { rw_fixture_trigger = yes } '
            'immediate = { rw_fixture_effect = { AMOUNT = 2 } } }')
        (self.mod / 'common/scripted_effects/rw_fixture.txt').write_text(
            'rw_fixture_effect = { if = { limit = { rw_fixture_trigger = yes } '
            'add_prestige = $AMOUNT$ } }')
        (self.mod / 'common/scripted_triggers/rw_fixture.txt').write_text(
            'rw_fixture_trigger = { always = yes }')
        self.assertEqual([], validate(self.root))

    def test_missing_owned_effect_or_trigger_reports_source_and_line(self):
        for kind in ('effect', 'trigger'):
            with self.subTest(kind=kind):
                (self.mod / 'events/rw_caller.txt').write_text(
                    'rw_fixture.0001 = {\n rw_missing_' + kind + ' = yes\n}')
                self.assertEqual([
                    f'mod/real_westeros/events/rw_caller.txt:2: undefined owned {kind} rw_missing_{kind}'
                ], validate(self.root))

    def test_wrong_definition_namespace_does_not_resolve_owned_call(self):
        (self.mod / 'common/scripted_effects/rw_wrong.txt').write_text(
            'rw_missing_trigger = { always = yes }')
        self.assertTrue(any('undefined owned trigger rw_missing_trigger' in error
                            for error in validate(self.root)))

    def test_comments_strings_scopes_and_native_calls_are_not_owned_calls(self):
        (self.mod / 'events/rw_caller.txt').write_text(
            '# rw_comment_effect = yes\n'
            'rw_fixture.0001 = { desc = "rw_string_trigger = yes" '
            'immediate = { native_effect = yes scope:rw_saved_effect = { native_effect = yes } '
            'var:rw_saved_trigger = yes rw_$PREFIX$_effect = yes } }')
        self.assertEqual([], validate(self.root))

    def test_commented_definition_cannot_satisfy_owned_call(self):
        (self.mod / 'common/scripted_effects/rw_wrong.txt').write_text(
            '# rw_missing_effect = { always = yes }\n')
        (self.mod / 'events/rw_caller.txt').write_text(
            'rw_fixture.0001 = { immediate = { rw_missing_effect = yes } }')
        self.assertTrue(any('undefined owned effect rw_missing_effect' in error
                            for error in validate(self.root)))

    def memory_fixture(self, english=True, french=True, perspectives_only=False):
        folder = self.mod / 'common/character_memory_types'
        folder.mkdir()
        (folder / 'rw_memory_fixture.txt').write_text('rw_memory_fixture = { duration = { years = 5 } }\n')
        key = 'rw_memory_fixture.first' if perspectives_only else 'rw_memory_fixture'
        for lang, present in (('english', english), ('french', french)):
            directory = self.mod / 'localization' / lang
            directory.mkdir(parents=True, exist_ok=True)
            text = 'l_' + lang + ':\n'
            if present:
                text += ' ' + key + ':0 "A public memory"\n'
            (directory / ('rw_memory_fixture_l_' + lang + '.yml')).write_text(text, encoding='utf-8-sig')

    def test_memory_type_label_exists_in_both_supported_languages(self):
        self.memory_fixture()
        self.assertEqual([], validate(self.root))

    def test_memory_type_label_missing_from_one_language_is_rejected(self):
        self.memory_fixture(french=False)
        problems = validate(self.root)
        self.assertTrue(any('missing french localization for memory type rw_memory_fixture' in e for e in problems))
        self.assertFalse(any('missing english localization for memory type' in e for e in problems))

    def test_perspective_text_does_not_replace_memory_type_label(self):
        self.memory_fixture(perspectives_only=True)
        problems = validate(self.root)
        self.assertTrue(any('missing english localization for memory type rw_memory_fixture' in e for e in problems))
        self.assertTrue(any('missing french localization for memory type rw_memory_fixture' in e for e in problems))

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

    def test_duplicate_script_value_is_rejected(self):
        folder = self.mod / 'common' / 'script_values'
        folder.mkdir()
        (folder / 'a.txt').write_text('rw_weight = { value = 1 }\n')
        (folder / 'b.txt').write_text('rw_weight = { value = 2 }\n')
        self.assertTrue(any('duplicate top-level rw_weight' in e for e in validate(self.root)))

    def test_duplicate_native_memory_type_is_rejected(self):
        folder = self.mod / 'common' / 'character_memory_types'
        folder.mkdir()
        (folder / 'a.txt').write_text('rw_memory = { duration = { years = 5 } }\n')
        (folder / 'b.txt').write_text('rw_memory = { duration = { years = 1 } }\n')
        self.assertTrue(any('duplicate top-level rw_memory' in e for e in validate(self.root)))

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
