"""Negative money forms and byte-preserved payment corrections, not a CK3 model."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from tools.validate_mod import gold_errors, validate
from tools.verify_telemetry import gameplay_digest

ROOT=Path(__file__).resolve().parents[1]


class GoldEffectTests(unittest.TestCase):
    def test_negative_scalar_debits_rejected(self):
        for effect in ('add_gold','remove_short_term_gold'):
            for amount in ('-25','-50','-0.5'):
                with self.subTest(effect=effect,amount=amount):
                    self.assertTrue(gold_errors(f'owned = {{ {effect} = {amount} }}'))

    def test_calculated_negative_additions_rejected(self):
        for value in ('scope:rw_service_price','scope:rw_cc_price','25','25.5','0.5'):
            with self.subTest(value=value):
                self.assertTrue(gold_errors(f'add_gold = {{ value = {value} multiply = -1 }}'))
        self.assertTrue(gold_errors('add_gold = { value = -25 }'))

    def test_positive_native_pair_and_unknown_expressions_allowed(self):
        self.assertEqual([],gold_errors('''
            scope:payer = { remove_short_term_gold = scope:price }
            scope:payee = { add_gold = scope:price }
            add_gold = 25
            remove_short_term_gold = 50
            add_gold = { value = variable_price max = 50 }
        '''))

    def test_not_an_arithmetic_evaluator(self):
        # Do not label a double negation or an arbitrary expression as a known debit.
        self.assertEqual([],gold_errors('add_gold = { value = -25 multiply = -1 }'))
        self.assertEqual([],gold_errors('add_gold = { value = 50 subtract = 75 }'))
        self.assertEqual([],gold_errors('add_gold = named_value_of_unknown_sign'))

    def test_zero_is_not_negative(self):
        self.assertEqual([],gold_errors('add_gold = -0 remove_short_term_gold = -0.0 add_gold = { value = 0 multiply = -1 }'))

    def test_comments_and_strings_are_not_operations(self):
        self.assertEqual([],gold_errors('''# add_gold = -25
            debug_log = "add_gold = -50"
            text = "remove_short_term_gold = -25"
        '''))

    def test_multiline_locations(self):
        out=gold_errors('owned = {\n # note\n add_gold = -25\n add_gold = {\n value = scope:price\n multiply = -1\n }\n}')
        self.assertEqual(2,len(out))
        self.assertTrue(out[0].startswith('line 3:'))
        self.assertTrue(out[1].startswith('line 4:'))

    def test_validator_rejects_regression_in_real_mod_layout(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(ROOT/'mod',root/'mod')
            target=root/'mod/real_westeros/common/scripted_effects/rw_bad_gold_fixture.txt'
            target.write_text('rw_bad_gold_fixture = { add_gold = -25 }\n')
            self.assertTrue(any('negative add_gold' in s for s in validate(root)))
            target.write_text('rw_bad_gold_fixture = { remove_short_term_gold = 25 }\n')
            self.assertEqual([],validate(root))

    def test_all_eleven_corrections_inverse_preserve_every_other_byte(self):
        data=json.loads((ROOT/'docs/GOLD_DEBIT_SOURCE_RECEIPT.json').read_text())
        self.assertEqual(11,len(data['corrections']))
        self.assertEqual(11,len({x['path'] for x in data['corrections']}))
        for row in data['corrections']:
            with self.subTest(path=row['path']):
                raw=(ROOT/row['path']).read_bytes();text=raw.decode()
                self.assertEqual(row['after_sha256'],hashlib.sha256(raw).hexdigest())
                self.assertEqual(1,text.count(row['after']))
                restored=text.replace(row['after'],row['before'],1)
                self.assertEqual(row['before_sha256'],hashlib.sha256(restored.encode()).hexdigest())
                self.assertEqual([],gold_errors(text))
                self.assertTrue(gold_errors(restored))

    def test_telemetry_baseline_changes_only_for_the_approved_debit(self):
        data=json.loads((ROOT/'docs/TELEMETRY_HOOKS.json').read_text())
        update=data['gameplay_updates'][-1]
        path=ROOT/update['file'];text=path.read_text()
        old=text.replace('remove_short_term_gold = scope:rw_ba_price',
                         'add_gold = { value = scope:rw_ba_price multiply = -1 }',1)
        self.assertEqual(update['before_sha256'],gameplay_digest(old))
        self.assertEqual(update['after_sha256'],gameplay_digest(text))
        self.assertEqual(data['gameplay_sha256'][update['file']],gameplay_digest(text))
        self.assertNotEqual(update['after_sha256'],gameplay_digest(text+'\nadd_gold = 25'))


if __name__ == '__main__':unittest.main()
