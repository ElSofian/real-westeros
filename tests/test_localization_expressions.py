"""Narrow expression/markup regressions; not a localization renderer or CK3 model."""
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from tools.validate_mod import localization_value_errors, validate

ROOT=Path(__file__).resolve().parents[1]


class LocalizationExpressionTests(unittest.TestCase):
    def test_saved_scopes_and_numeric_functions_allowed(self):
        self.assertEqual([],localization_value_errors(
            "[rw_person.GetShortUIName] [rw_title.GetName] [SCOPE.GetValue('serial')|0]"))

    def test_script_prefix_is_rejected_in_a_datafunction(self):
        for value in ('[scope:rw_person.GetName]', '[ scope:rw_person.GetName]',
                      'Person: [scope:rw_person.GetShortUIName].'):
            with self.subTest(value=value):
                self.assertTrue(any('scope:' in e for e in localization_value_errors(value)))

    def test_plain_scope_text_is_not_a_datafunction(self):
        self.assertEqual([],localization_value_errors('Reference scope:rw_person in prose.'))

    def test_hash_number_marker_requires_escape(self):
        expression="[SCOPE.GetValue('serial')|0]"
        for count in (1,3,5):
            with self.subTest(count=count):
                self.assertTrue(any('unescaped #' in e for e in localization_value_errors('#'*count+expression)))
        for count in (2,4,6):
            with self.subTest(count=count):
                self.assertEqual([],localization_value_errors('#'*count+expression))

    def test_valid_markup_and_dynamic_tooltip_are_preserved(self):
        for value in ('#P [rw_person.GetName]#!', '#weak Text#!',
                      '#tooltip:[GetPlayer.GetTooltipTag] Text#!', '##[rw_title.GetName]'):
            with self.subTest(value=value):self.assertEqual([],localization_value_errors(value))

    def test_validator_catches_bad_values_with_file_and_line(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(ROOT/'mod',root/'mod')
            p=root/'mod/real_westeros/localization/english/rw_expression_fixture_l_english.yml'
            for value,problem in (('[scope:rw_person.GetName]','scope:'),
                                  ("#[SCOPE.GetValue('serial')|0]",'unescaped #')):
                with self.subTest(value=value):
                    p.write_text('l_english:\n rw_expression_fixture:0 "'+value+'"\n',encoding='utf-8-sig')
                    self.assertTrue(any('rw_expression_fixture_l_english.yml:2:' in e and problem in e for e in validate(root)))

    def test_validator_ignores_comments_outside_escaped_quoted_value(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(ROOT/'mod',root/'mod')
            p=root/'mod/real_westeros/localization/english/rw_expression_fixture_l_english.yml'
            p.write_text('l_english:\n # [scope:comment.GetName] #[ignored]\n'
                         ' rw_expression_fixture:0 "He said \\"yes\\" to [rw_person.GetName]." # [scope:comment.GetName]\n',encoding='utf-8-sig')
            self.assertEqual([],validate(root))
            # The expression after escaped quotes is still inspected.
            p.write_text(p.read_text(encoding='utf-8-sig').replace('[rw_person.GetName]', '[scope:rw_person.GetName]'),encoding='utf-8-sig')
            self.assertTrue(any('scope:' in e for e in validate(root)))

    def test_corrected_parties_keep_their_saved_scope_names_in_both_languages(self):
        cases={'rw_allegation_settlement':('rw_service_provider','rw_service_client'),
               'rw_military_restraint':('rw_mr_provider','rw_mr_beneficiary'),
               'rw_unlawful_war_choice':('rw_uw_attacker','rw_uw_defender','rw_uw_issuer')}
        for lang in ('english','french'):
            for stem,scopes in cases.items():
                with self.subTest(lang=lang,stem=stem):
                    raw=(ROOT/f'mod/real_westeros/localization/{lang}/{stem}_l_{lang}.yml').read_bytes()
                    self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
                    value=raw.decode('utf-8-sig');self.assertNotIn('[scope:',value)
                    for scope in scopes:self.assertRegex(value,r'\['+scope+r'\.(?:GetShortUIName|GetTitledFirstName)\]')

    def test_observation_numbers_keep_their_values_and_format(self):
        p=ROOT/'mod/real_westeros/localization/english/rw_revocation_intents_l_english.yml'
        value=p.read_text(encoding='utf-8-sig')
        self.assertIn("##[SCOPE.GetValue('rw_scheme_evidence_serial')|0]",value)
        self.assertEqual(2,value.count("##[SCOPE.GetValue('rw_ri_basis_serial')|0]"))
        self.assertEqual(3,len(re.findall(r'(?<!#)##\[SCOPE',value)))


if __name__ == '__main__':unittest.main()
