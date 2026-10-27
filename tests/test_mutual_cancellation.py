"""Adversarial source checks for mutual release; these do not execute CK3."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def cancellation_errors(t, e, service):
    errors = []
    live = block(t, 'rw_cancel_obligation_live_trigger')
    for guard in ('rw_service_obligation_live_trigger = yes', 'rw_service_deferred_trigger = yes',
                  'has_character_flag = rw_service_deadline'):
        if guard not in live:
            errors.append('completed, broken or overdue promise can be released')
    pair = block(t, 'rw_cancel_parties_trigger')
    for role in ('proposer', 'responder'):
        for party in ('provider', 'client'):
            if f'scope:rw_cancel_{role} = scope:rw_service_{party}' not in pair:
                errors.append('unrelated party can consent')
    response = block(t, 'rw_cancel_responder_turn_trigger')
    if 'rw_cancel_request_matches_trigger = yes' not in response or 'this = scope:rw_cancel_responder' not in response:
        errors.append('response actor not checked')
    identity = block(t, 'rw_cancel_request_matches_trigger')
    for guard in ('rw_cancel_obligation_live_trigger = yes', 'rw_cancel_parties_trigger = yes',
                  'has_character_flag = rw_cancel_pending',
                  'var:rw_cancel_serial = scope:rw_cancel_serial',
                  'var:rw_cancel_proposer = scope:rw_cancel_proposer',
                  'var:rw_cancel_responder = scope:rw_cancel_responder'):
        if guard not in identity:
            errors.append('stale or expired request can settle')
    for action in ('accept', 'reject'):
        if 'limit = { rw_cancel_responder_turn_trigger = yes }' not in block(e, f'rw_cancel_{action}_effect'):
            errors.append('direct response bypass')
    accept = block(e, 'rw_cancel_accept_effect')
    if not 0 <= accept.find('rw_service_clear_effect = yes') < accept.find('id = rw_cancellations.0002'):
        errors.append('release is not consumed before notice')
    if 'rw_service_last_outcome value = flag:mutually_released' not in accept:
        errors.append('mutual release misclassified')
    propose = block(e, 'rw_cancel_propose_effect')
    if 'rw_cancel_can_propose_trigger = yes' not in propose:
        errors.append('proposer execution bypass')
    if 'change_variable = { name = rw_cancel_serial add = 1 }' not in propose:
        errors.append('proposal identity reused')
    if re.search(r'\b(?:add_gold|add_prestige|add_opinion|rw_service_clear_effect|rw_service_record_breach_effect)\s*=', propose):
        errors.append('proposal unilaterally changes obligation or wealth')
    if 'rw_service_revision' in e or 'flag = rw_service_deadline' in e or 'flag = rw_service_not_due' in e:
        errors.append('proposal rewrites obligation identity or dates')
    clear = block(service, 'rw_service_clear_effect')
    if 'remove_character_flag = rw_cancel_pending' not in clear:
        errors.append('terminal outcome leaves request pending')
    if 'remove_variable = rw_cancel_serial' in clear:
        errors.append('request serial reset')
    return errors


class MutualCancellationTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_cancellation_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_cancellation_effects.txt').read_text()
        self.s = (MOD / 'common/scripted_effects/rw_service_effects.txt').read_text()
        self.v = (MOD / 'events/rw_cancellation_events.txt').read_text()

    def errors(self, t=None, e=None, s=None):
        return cancellation_errors(self.t if t is None else t, self.e if e is None else e,
                                   self.s if s is None else s)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_terminated_or_overdue_promise_mutations(self):
        for guard in ('rw_service_obligation_live_trigger = yes', 'rw_service_deferred_trigger = yes', 'has_character_flag = rw_service_deadline'):
            with self.subTest(guard=guard):
                self.assertIn('completed, broken or overdue promise can be released', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_wrong_actor_and_unrelated_parties_mutations(self):
        self.assertIn('response actor not checked', self.errors(t=self.t.replace('this = scope:rw_cancel_responder', 'always = yes')))
        self.assertIn('unrelated party can consent', self.errors(t=self.t.replace('scope:rw_cancel_proposer = scope:rw_service_client', 'always = yes')))

    def test_request_identity_expiry_and_cross_request_mutations(self):
        for guard in ('has_character_flag = rw_cancel_pending', 'var:rw_cancel_serial = scope:rw_cancel_serial',
                      'var:rw_cancel_proposer = scope:rw_cancel_proposer', 'var:rw_cancel_responder = scope:rw_cancel_responder'):
            with self.subTest(guard=guard):
                self.assertIn('stale or expired request can settle', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_direct_effect_bypass_mutation(self):
        self.assertIn('direct response bypass', self.errors(e=self.e.replace('limit = { rw_cancel_responder_turn_trigger = yes }', 'limit = { always = yes }')))

    def test_proposal_cannot_unilaterally_release_or_pay(self):
        for injected in ('rw_service_clear_effect = yes', 'add_gold = 50', 'rw_service_record_breach_effect = yes'):
            with self.subTest(injected=injected):
                e = self.e.replace('rw_cancel_propose_effect = {', 'rw_cancel_propose_effect = { ' + injected)
                self.assertIn('proposal unilaterally changes obligation or wealth', self.errors(e=e))

    def test_terminal_consumption_and_serial_reuse_mutations(self):
        self.assertIn('release is not consumed before notice', self.errors(e=self.e.replace('rw_service_clear_effect = yes', '')))
        self.assertIn('terminal outcome leaves request pending', self.errors(s=self.s.replace('remove_character_flag = rw_cancel_pending', '')))
        self.assertIn('request serial reset', self.errors(s=self.s.replace('remove_character_flag = rw_cancel_pending', 'remove_character_flag = rw_cancel_pending\nremove_variable = rw_cancel_serial')))
        self.assertIn('proposal identity reused', self.errors(e=self.e.replace('change_variable = { name = rw_cancel_serial add = 1 }', '')))

    def test_obligation_revision_and_deadline_not_extended(self):
        for injected in ('change_variable = { name = rw_service_revision add = 1 }', 'add_character_flag = { flag = rw_service_deadline days = 30 }'):
            with self.subTest(injected=injected):
                self.assertIn('proposal rewrites obligation identity or dates', self.errors(e=self.e + '\n' + injected))
        self.assertEqual(1, self.e.count('flag = rw_cancel_pending days = 7'))
        self.assertEqual(1, self.e.count('flag = rw_cancel_cooldown days = 7'))

    def test_no_effect_on_refusal_silence_or_native_systems(self):
        reject = block(self.e, 'rw_cancel_reject_effect')
        self.assertNotRegex(reject, r'\b(?:add_opinion|add_gold|add_prestige|rw_service_clear_effect|rw_service_record_receipt_effect)\s*=')
        self.assertNotRegex(clean_script(self.e)[0], r'\b(?:add_gold|add_prestige|add_opinion|death|imprison|add_secret|add_hook|change_title_holder)\s*=')
        ignore = self.v[self.v.index('name = rw_cancellations.ignore'):self.v.index('name = rw_cancellations.lapsed')]
        self.assertNotRegex(clean_script(ignore)[0], r'\brw_\w+_effect\s*=')
        self.assertIn('flag:mutually_released', block(self.e, 'rw_cancel_accept_effect'))

    def test_shared_ai_opportunities_and_provider_revisit(self):
        acceptance = (MOD / 'common/scripted_effects/rw_obligation_effects.txt').read_text()
        self.assertIn('id = rw_cancellations.0003', block(acceptance, 'rw_service_accept_promise_effect'))
        provider = block((MOD / 'events/rw_obligation_events.txt').read_text(), 'rw_obligations.0001')
        choice = provider[provider.index('name = rw_cancellations.propose'):provider.index('name = rw_obligations.wait')]
        self.assertIn('rw_service_wait_promise_effect = yes', choice)
        self.assertIn('ai_chance', choice)
        self.assertNotIn('is_ai', self.v + self.e + self.t)
        for choice in ('accept', 'reject', 'ignore'):
            self.assertIn('name = rw_cancellations.' + choice, self.v)

    def test_execution_and_both_interaction_directions_revalidate(self):
        prepare = block(self.e, 'rw_cancel_prepare_effect')
        self.assertIn('rw_cancel_interaction_allowed_trigger = { PROVIDER = $PROVIDER$ CLIENT = $CLIENT$ }', prepare)
        self.assertIn('rw_service_snapshot_effect = yes', prepare)
        self.assertIn('rw_cancel_can_propose_trigger = yes', block(self.e, 'rw_cancel_propose_effect'))
        interactions = (MOD / 'common/character_interactions/rw_cancellation_interactions.txt').read_text()
        for mapping in ('PROVIDER = scope:actor CLIENT = scope:recipient', 'PROVIDER = scope:recipient CLIENT = scope:actor'):
            self.assertIn(mapping, interactions)
        self.assertEqual(2, interactions.count('on_accept = { rw_cancel_prepare_effect'))
        # War and poverty do not make consenting to a neutral release impossible.
        self.assertNotRegex(self.t, r'\b(?:gold|is_at_war|rw_service_affordable_trigger)\s*=')

    def test_receipt_notices_are_identity_bound_and_readonly(self):
        receipt = block(self.t, 'rw_cancel_release_receipt_trigger')
        for comparison in ('var:rw_service_last_serial = scope:rw_service_serial', 'var:rw_service_last_client = scope:rw_service_client',
                           'var:rw_service_last_outcome = flag:mutually_released', 'var:rw_service_last_cancel_serial = scope:rw_cancel_serial'):
            self.assertIn(comparison, receipt)
        self.assertNotRegex(block(self.v, 'rw_cancellations.0002'), r'\brw_\w+_effect\s*=')

    def test_localization_covers_new_display_keys(self):
        interactions = (MOD / 'common/character_interactions/rw_cancellation_interactions.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', self.v + interactions))
        keys.update(('rw_request_release_endorsement_interaction', 'rw_offer_release_endorsement_interaction'))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_cancellations_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertEqual(keys, actual)
