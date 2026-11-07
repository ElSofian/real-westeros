"""Synthetic originals only. Native source is neither required nor distributed."""

from pathlib import Path
import tempfile
import unittest

from tools.audit_trait_context import inventory, literal_script_values, markdown, read_traits


class TraitContextAuditTests(unittest.TestCase):
    def test_comments_strings_constants_and_combined_axes(self):
        text = '''@word = 35
        # fake = { ai_honor = -100 }
        example = {
            desc = "braces { } and # comments are quoted"
            personality = yes
            ai_honor = @word
            ai_greed = -20
            martial = 2
        }'''
        row, = read_traits(text, 'CK3', 'common/traits/example.txt')
        self.assertEqual('example', row['id'])
        self.assertEqual({'ai_honor': 35, 'ai_greed': -20}, row['direct_axes'])
        self.assertEqual({'martial': 2}, row['direct_personal_fields'])
        self.assertEqual('native_axes_input', row['promise_input_status'])
        self.assertEqual('pending', row['context_review'])
        self.assertTrue(row['personality_trait'])

    def test_absent_and_explicit_zero_are_not_claimed_fully_reviewed(self):
        for text in ('example = { ai_honor = 0 }', 'example = { prowess = 8 }'):
            row, = read_traits(text, 'CK3', 'common/traits/example.txt')
            self.assertEqual('zero_direct_axis_input', row['promise_input_status'])
            self.assertEqual('pending', row['context_review'])

    def test_nested_track_and_symbolic_values_stay_unresolved(self):
        for text in (
            'example = { track = { modifier = { ai_honor = 20 } } }',
            'example = { ai_honor = native_script_value }',
            'example = { ai_greed = @missing }',
            'example = { ai_honor = 10 ai_honor = 20 }',
        ):
            row, = read_traits(text, 'AGOT', 'common/traits/example.txt')
            self.assertEqual('conditional_or_unresolved', row['promise_input_status'])

    def test_malformed_input_fails_instead_of_inventing_zero(self):
        for text in ('example = { ai_honor = 10', 'example = yes', 'example { }'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                read_traits(text, 'CK3', 'common/traits/example.txt')

    def test_overlay_replaces_whole_file_and_retains_other_files(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            ck3, agot = base/'ck3', base/'agot'
            for root in (ck3, agot):
                (root/'common/traits').mkdir(parents=True)
            (ck3/'common/traits/00_traits.txt').write_text('old = { ai_honor = 99 }')
            (ck3/'common/traits/extra.txt').write_text('retained = { ai_energy = 10 }')
            (agot/'common/traits/00_traits.txt').write_text('replacement = { ai_honor = -5 }')
            report = inventory(ck3, agot)
            self.assertEqual(['replacement', 'retained'], [row['id'] for row in report['traits']])
            self.assertEqual(['common/traits/00_traits.txt'], report['replaced_files'])
            self.assertEqual(2, sum(report['summary'].values()))
            self.assertNotIn(str(base), str(report))
            self.assertNotIn('old', markdown(report))
            (agot/'common/traits/duplicate.txt').write_text('retained = { ai_greed = 5 }')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                inventory(ck3, agot)

    def test_missing_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'Missing or empty'):
                inventory(Path(directory), Path(directory))

    def test_only_literal_script_values_resolve_and_same_file_overlay_applies(self):
        with tempfile.TemporaryDirectory() as directory:
            ck3, agot = Path(directory)/'ck3', Path(directory)/'agot'
            for root in (ck3, agot):
                (root/'common/script_values').mkdir(parents=True)
            (ck3/'common/script_values/values.txt').write_text('native_value = 80')
            (agot/'common/script_values/values.txt').write_text(
                'native_value = 20\nexpression = @[native_value * 2]\n'
                'scripted = { value = 20 add = 10 }')
            values, _ = literal_script_values(ck3, agot)
            self.assertEqual({'native_value': '20'}, values)
            row, = read_traits('example = { ai_honor = native_value }', 'AGOT', 'traits.txt', values)
            self.assertEqual(20, row['direct_axes']['ai_honor'])
            (agot/'common/script_values/duplicate.txt').write_text('native_value = 50')
            values, _ = literal_script_values(ck3, agot)
            self.assertNotIn('native_value', values)

    def test_french_names_and_trait_identifiers_remain_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            ck3, agot = Path(directory)/'ck3', Path(directory)/'agot'
            for root in (ck3, agot):
                (root/'common/traits').mkdir(parents=True)
                (root/'localization/french').mkdir(parents=True)
            (ck3/'common/traits/base.txt').write_text('child = { ai_honor = 15 }')
            (agot/'common/traits/extra.txt').write_text('adult = { category = personality }')
            (ck3/'localization/french/traits_l_french.yml').write_text(
                'l_french:\n trait_child:0 "Curieux"\n trait_adult:0 "Curieux"', encoding='utf-8')
            report = inventory(ck3, agot)
            self.assertEqual({'adult', 'child'}, {row['id'] for row in report['traits']})
            self.assertEqual({'Curieux'}, {row['label_fr'] for row in report['traits']})
            self.assertIn('| Curieux | `adult`', markdown(report))


if __name__ == '__main__':
    unittest.main()
