"""Static political-case wiring and adversarial source mutations, not CK3 execution."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def case_errors(triggers, effects):
    errors = []
    opening = block(triggers, 'rw_case_can_open_trigger')
    if 'rw_service_breach_receipt_trigger = yes' not in opening:
        errors.append('unsupported allegation can open case')
    if 'has_variable = rw_service_last_reason' not in opening:
        errors.append('reason provenance missing')
    if 'top_liege = scope:rw_service_client.top_liege' not in opening:
        errors.append('no common overlord required')
    jurisdiction = block(triggers, 'rw_case_jurisdiction_trigger')
    if jurisdiction.count('top_liege = scope:rw_case_mediator') != 2:
        errors.append('current authority not checked for both parties')
    for party in ('provider', 'client'):
        if f'NOT = {{ this = scope:rw_service_{party} }}' not in jurisdiction:
            errors.append('party can judge own case')
    identity = block(triggers, 'rw_case_matches_trigger')
    for comparison in ('var:rw_case_serial = scope:rw_case_serial',
                       'var:rw_case_client = scope:rw_service_client',
                       'var:rw_case_mediator = scope:rw_case_mediator',
                       'var:rw_case_reason = scope:rw_case_reason'):
        if comparison not in identity:
            errors.append('case identity missing')
    for turn in ('ruler', 'provider'):
        gate = block(triggers, f'rw_case_{turn}_turn_trigger')
        if 'rw_case_jurisdiction_trigger = yes' not in gate or 'rw_case_matches_trigger = yes' not in gate:
            errors.append('decision can bypass identity/authority')
    apology = block(effects, 'rw_case_apologise_effect')
    if 'prestige >= 25' not in apology:
        errors.append('unfunded apology allowed')
    consume = apology.find('rw_case_close_effect')
    if consume < 0 or consume > apology.find('add_prestige'):
        errors.append('apology charges before consumption')
    close = block(effects, 'rw_case_close_effect')
    if 'NOT = { var:rw_case_stage = flag:closed }' not in close:
        errors.append('closure can replay')
    if 'NOT = { has_variable = rw_case_pending }' not in block(effects, 'rw_case_expire_effect'):
        errors.append('early expiry allowed')
    if 'rw_service_last_outcome' in clean_script(effects)[0]:
        errors.append('mediation rewrites underlying breach')
    return errors


class CaseContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_case_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_case_effects.txt').read_text()

    def test_contract(self):
        self.assertEqual([], case_errors(self.t, self.e))

    def test_unsupported_accusation_mutation(self):
        t = self.t.replace('rw_service_breach_receipt_trigger = yes', 'always = yes')
        self.assertIn('unsupported allegation can open case', case_errors(t, self.e))

    def test_lost_authority_mutation(self):
        t = self.t.replace('top_liege = scope:rw_case_mediator', 'always = yes', 1)
        self.assertIn('current authority not checked for both parties', case_errors(t, self.e))

    def test_self_judging_mutation(self):
        t = self.t.replace('NOT = { this = scope:rw_service_client }', '')
        self.assertIn('party can judge own case', case_errors(t, self.e))

    def test_stale_case_mutation(self):
        t = self.t.replace('var:rw_case_serial = scope:rw_case_serial', 'always = yes')
        self.assertIn('case identity missing', case_errors(t, self.e))

    def test_wrong_client_mutation(self):
        t = self.t.replace('var:rw_case_client = scope:rw_service_client', 'always = yes')
        self.assertIn('case identity missing', case_errors(t, self.e))

    def test_unfunded_apology_mutation(self):
        self.assertIn('unfunded apology allowed', case_errors(self.t, self.e.replace('prestige >= 25', 'always = yes')))

    def test_replayed_closure_mutation(self):
        e = self.e.replace('NOT = { var:rw_case_stage = flag:closed }', 'always = yes')
        self.assertIn('closure can replay', case_errors(self.t, e))

    def test_underlying_fact_mutation(self):
        self.assertIn('mediation rewrites underlying breach', case_errors(self.t, self.e + '\nrw_service_last_outcome = flag:fulfilled'))

    def test_early_expiry_mutation(self):
        self.assertIn('early expiry allowed', case_errors(self.t, self.e.replace('NOT = { has_variable = rw_case_pending }', 'always = yes')))

    def test_decline_and_refusal_are_not_automatic_penalties(self):
        for name in ('rw_case_decline_effect', 'rw_case_refuse_repair_effect',
                     'rw_case_expire_effect', 'rw_case_lost_jurisdiction_effect'):
            self.assertNotRegex(block(self.e, name), r'\b(add_opinion|add_prestige|add_gold)\s*=')
        self.assertNotRegex(clean_script(self.e)[0], r'\b(death|imprison|revoke_title|add_claim|add_hook|add_secret)\s*=')

    def test_disclosure_consumes_response_before_delivery(self):
        opening = block(self.e, 'rw_case_open_effect')
        self.assertLess(opening.index('rw_service_reacted_serial'), opening.index('id = rw_cases.0001'))
        self.assertEqual(1, self.e.count('set_variable = { name = rw_case_pending value = flag:yes days = 30 }'))
        self.assertEqual(1, self.e.count('id = rw_cases.0004 days = 31'))

    def test_ruler_ai_uses_context_and_keeps_all_choices(self):
        text = (MOD / 'events/rw_case_events.txt').read_text()
        ruler = block(text, 'rw_cases.0001')
        self.assertIn('is_at_war = yes', ruler)
        self.assertIn('opinion = { target = scope:rw_service_provider', ruler)
        for choice in ('decline', 'admonish', 'invite_repair'):
            self.assertIn('name = rw_cases.' + choice, ruler)

    def test_only_actual_callbacks_generate_reason(self):
        e = (MOD / 'common/scripted_effects/rw_obligation_effects.txt').read_text()
        explicit = block(e, 'rw_service_break_promise_effect')
        deadline = block(e, 'rw_service_timeout_effect')
        self.assertIn('name = rw_service_breach_reason value = flag:refusal', explicit)
        self.assertIn('name = rw_service_breach_reason value = flag:deadline', deadline)
        self.assertNotIn('rw_service_last_reason', block(e, 'rw_service_cancel_promise_effect'))

    def test_display_keys_exist_in_both_languages(self):
        events = (MOD / 'events/rw_case_events.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', events))
        keys.update(('rw_cases.refer', 'rw_case_admonished_opinion', 'rw_case_apology_opinion',
                     'rw_review_political_cases_interaction', 'rw_review_political_cases_interaction_desc'))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_cases_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertEqual(keys, actual)
