"""Current client, historical capacity and voluntary repair source contracts."""

import hashlib
import json
from pathlib import Path
import re
import unittest

from test_deferred_service_contract import block
from test_gold_effects import restore_later_updates
from test_political_ai import option
from test_promise_ai_policy import action_digest
from tools.validate_mod import clean_script
from tools.audit_trait_context import client_markdown, read_traits


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT/'mod/real_westeros'
CHOICES = (
    ('gold_client_resent', 'gold_breach', 60, 'rw_obligation_events.txt', 'rw_obligations.resent'),
    ('gold_client_forgive', 'gold_breach', 40, 'rw_obligation_events.txt', 'rw_obligations.forgive'),
    ('gold_client_refer', 'gold_breach', 20, 'rw_obligation_events.txt', 'rw_cases.refer'),
    ('favor_client_resent', 'favor_renunciation', 30, 'rw_favor_service_events.txt', 'rw_favor_renunciation.resent'),
    ('favor_client_note', 'favor_renunciation', 40, 'rw_favor_service_events.txt', 'rw_favor_renunciation.note'),
    ('client_repair_accept', 'repair_response', 50, 'rw_case_events.txt', 'rw_repair.accept'),
    ('client_repair_reject', 'repair_response', 50, 'rw_case_events.txt', 'rw_repair.reject'),
)


class ClientResponseAITests(unittest.TestCase):
    def setUp(self):
        self.values = (MOD/'common/script_values/rw_client_response_ai_values.txt').read_text(encoding='utf-8-sig')
        self.triggers = (MOD/'common/scripted_triggers/rw_client_response_ai_triggers.txt').read_text(encoding='utf-8-sig')

    def test_existing_choices_consume_zero_default_guarded_profiles(self):
        for name, family, base, filename, option_name in CHOICES:
            with self.subTest(name=name):
                weight = block(self.values, 'rw_ai_'+name+'_weight')
                self.assertTrue(weight.strip().startswith('value = 0'))
                self.assertIn('limit = { rw_ai_'+family+'_context_trigger = yes }', weight)
                self.assertIn('add = '+str(base), weight)
                event = (MOD/'events'/filename).read_text(encoding='utf-8-sig')
                self.assertIn('add = rw_ai_'+name+'_weight', block(option(event, option_name), 'ai_chance'))
        self.assertIn('limit = { rw_case_can_open_trigger = yes }', block(self.values, 'rw_ai_gold_client_refer_weight'))

    def test_full_original_client_context_precedes_existing_receipt_or_case_validation(self):
        for family, fields, client, guard in (
            ('gold_breach', ('rw_service_provider','rw_service_client','rw_service_serial'), 'rw_service_client', 'rw_service_breach_receipt_trigger'),
            ('favor_renunciation', ('rw_fv_provider','rw_fv_client','rw_fv_serial','rw_fv_revision','rw_fv_term','rw_fv_mode'), 'rw_fv_client', 'rw_fr_can_respond_trigger'),
            ('repair_response', ('rw_service_provider','rw_service_client','rw_case_record','rw_case_mediator','rw_case_serial','rw_case_reason','rw_case_kind'), 'rw_service_client', 'rw_repair_client_turn_trigger'),
        ):
            body = block(self.triggers, 'rw_ai_'+family+'_context_trigger')
            for field in fields:
                self.assertIn('exists = scope:'+field, block(body, 'limit'))
            self.assertIn('this = scope:'+client, body)
            self.assertLess(body.index('exists = scope:'+fields[-1]), body.index(guard+' = yes'))
            self.assertIn('trigger_else = { always = no }', body)
            changed = body.replace('this = scope:'+client, 'this = scope:foreign_party')
            self.assertNotIn('this = scope:'+client, changed)

    def test_gold_capacity_is_captured_before_cleanup_and_reset_for_new_receipts(self):
        effects = (MOD/'common/scripted_effects/rw_obligation_effects.txt').read_text(encoding='utf-8-sig')
        receipt = block(effects, 'rw_service_record_breach_effect')
        self.assertLess(receipt.index('rw_service_record_receipt_effect = yes'), receipt.index('name = rw_service_last_performance_capacity'))
        self.assertLess(receipt.index('name = rw_service_last_performance_capacity'), receipt.index('rw_service_clear_effect = yes'))
        for fragment in ('scope:rw_service_provider = { rw_service_party_eligible_trigger = yes }',
                         'scope:rw_service_client = { rw_service_party_eligible_trigger = yes }',
                         'rw_service_affordable_trigger = yes', 'value = flag:available', 'value = flag:unavailable'):
            self.assertIn(fragment, receipt)
        self.assertNotIn('rw_service_obligation_fulfillable_trigger', receipt)
        terms = (MOD/'common/scripted_effects/rw_case_terms_effects.txt').read_text(encoding='utf-8-sig')
        self.assertIn('remove_variable = rw_service_last_performance_capacity', block(terms, 'rw_service_clear_receipt_terms_effect'))

    def test_favor_early_or_expired_renunciation_does_not_invent_capacity(self):
        effects = (MOD/'common/scripted_effects/rw_deferred_favor_effects.txt').read_text(encoding='utf-8-sig')
        body = block(effects, 'rw_fd_renounce_effect')
        self.assertLess(body.index('name = rw_fr_capacity value = flag:unknown'), body.index('rw_fd_due_trigger = yes'))
        self.assertLess(body.index('rw_fd_due_trigger = yes'), body.index('value = flag:unavailable'))
        self.assertLess(body.index('rw_fd_can_perform_trigger = yes'), body.index('value = flag:available'))
        self.assertLess(body.index('value = flag:available'), body.index('rw_fd_finish_effect'))

    def test_unknown_capacity_is_neutral_and_later_resources_are_not_read(self):
        for family, provider, field in (('gold','rw_service_provider','rw_service_last_performance_capacity'),
                                         ('favor','rw_fv_provider','rw_fr_capacity')):
            body = block(self.values, 'rw_ai_'+family+'_response_accountability_factor')
            self.assertTrue(body.strip().startswith('value = 1'))
            self.assertLess(body.index('has_variable = '+field), body.index('var:'+field+' = flag:unavailable'))
            self.assertIn('multiply = 0.5', body)
            self.assertIn('multiply = 1.25', body)
            for forbidden in ('gold', 'is_at_war', 'rw_fd_can_perform_trigger', 'rw_service_affordable_trigger'):
                self.assertNotRegex(body, r'\b'+forbidden+r'\s*[=<>]')
        body = block(self.values, 'rw_ai_gold_response_accountability_factor')
        self.assertLess(body.index('has_variable = rw_service_last_reason'), body.index('var:rw_service_last_reason = flag:refusal'))

    def test_justice_uses_known_capacity_and_repair_uses_its_own_case(self):
        refer = block(self.values, 'rw_ai_gold_client_refer_weight')
        self.assertLess(refer.index('flag:available'), refer.index('multiply = rw_ai_client_fair_process_factor'))
        self.assertIn('value < 0', refer)
        for name in ('accept', 'reject'):
            body = block(self.values, 'rw_ai_client_repair_'+name+'_weight')
            self.assertNotIn('rw_service_last_', body)
            self.assertNotIn('accountability', body)
            self.assertIn('target = scope:rw_service_provider', body)

    def test_personality_axes_are_read_only_current_character_inputs(self):
        for name, axis, divisor, lower, upper in (
            ('resentment','ai_vengefulness',200,.25,2), ('forgiveness','ai_vengefulness',200,.25,2),
            ('compassion','ai_compassion',400,.5,1.5), ('fair_process','ai_honor',200,.5,1.5),
        ):
            body = block(self.values, 'rw_ai_client_'+name+'_factor')
            for fragment in ('value = '+axis, 'divide = '+str(divisor), 'min = '+str(lower), 'max = '+str(upper)):
                self.assertIn(fragment, body)
            self.assertNotIn('scope:', body)
        for forbidden in ('set_variable', 'add_gold', 'add_opinion', 'trigger_event', 'is_ai =', 'has_trait', 'has_secret', 'global_var', 'every_'):
            self.assertNotIn(forbidden, clean_script(self.values)[0])

    def test_event_action_graphs_preserve_rights_costs_consent_and_fallbacks(self):
        for filename, digest in (
            ('rw_obligation_events.txt','3e937926b1425d3141b471efb5a8ea27f39c6bcd1fbbb195221fd4e9ee025ea5'),
            ('rw_favor_service_events.txt','a0f079aa0e9ab8700a00add3c2248e17948dc81f809b84f027ca315664f91cc3'),
            ('rw_case_events.txt','b60bb412b15f5ae002fc0958f25773159fbb72143df413a04df7506dd61ec343'),
        ):
            self.assertEqual(digest, action_digest((MOD/'events'/filename).read_text(encoding='utf-8-sig')))

    def test_capacity_metadata_reverses_exactly_without_weakening_payment_proofs(self):
        updates = [row for row in json.loads((ROOT/'docs/GOLD_DEBIT_SOURCE_RECEIPT.json').read_text())['subsequent_updates']
                   if row.get('reason') == 'RW-010 client breach capacity snapshot']
        self.assertEqual(2, len(updates))
        for row in updates:
            raw = (ROOT/row['path']).read_bytes()
            restored = restore_later_updates(raw, row['path'], updates)
            self.assertEqual(row['before_sha256'], hashlib.sha256(restored).hexdigest())
            with self.assertRaises(ValueError):
                restore_later_updates(raw+b'\n', row['path'], updates)
        raw = (MOD/'common/scripted_effects/rw_case_terms_effects.txt').read_bytes()
        line = b'    remove_variable = rw_service_last_performance_capacity\n'
        self.assertEqual(1, raw.count(line))
        self.assertEqual('fcd8e9693a98f58c68d030890e191f14f583b00d3691e1c44865e5d55b0d51a5', hashlib.sha256(raw.replace(line,b'',1)).hexdigest())

    def test_isolated_arithmetic_retains_alternatives_and_capacity_mitigation(self):
        # Arithmetic examples only, not CK3 decisions or probabilities.
        for revenge in (-200, 0, 200):
            harsh = min(2, max(.25, 1+revenge/200))
            gentle = min(2, max(.25, 1-revenge/200))
            self.assertGreater(harsh, 0)
            self.assertGreater(gentle, 0)
            self.assertGreater(harsh*1.25, harsh*.5)
            self.assertLess(gentle/1.25, gentle/.5)

    def test_client_trait_directions_are_separate_from_provider_preferences(self):
        row, = read_traits('example = { category = personality ai_vengefulness = 200 ai_compassion = -20 }', 'CK3', 'traits.txt')
        result = row['client_response_axis_review']
        self.assertEqual('nondecreasing', result['resent'])
        self.assertEqual('nonincreasing', result['forgive_or_note'])
        self.assertEqual('zero_direct', result['refer_known_available'])
        self.assertEqual('pending', row['context_review'])
        row, = read_traits('example = { ai_honor = 20 }', 'CK3', 'traits.txt')
        self.assertEqual('nondecreasing', row['client_response_axis_review']['refer_known_available'])
        self.assertEqual('zero_direct', row['client_response_axis_review']['resent'])

    def test_client_report_keeps_historical_and_case_scope_explicit(self):
        row, = read_traits('example = { category = personality ai_honor = 20 }', 'CK3', 'traits.txt')
        text = client_markdown({'traits': [row]})
        self.assertIn('`example`', text)
        self.assertIn('capacité attestée', text)
        self.assertIn('sans réutiliser un reçu plus récent', text)
        self.assertIn('Validation moteur en attente', text)


if __name__ == '__main__':
    unittest.main()
