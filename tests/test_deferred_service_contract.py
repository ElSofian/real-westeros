"""Lexical contract/graph checks only. No CK3 state transition is simulated."""
from pathlib import Path
import re
import unittest
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def block(text, name):
    clean, _ = clean_script(text)
    match = re.search(r'\b' + re.escape(name) + r'\s*=\s*\{', clean)
    if not match:
        return ''
    start = clean.index('{', match.start())
    depth = 1
    for end in range(start + 1, len(clean)):
        depth += (clean[end] == '{') - (clean[end] == '}')
        if depth == 0:
            return clean[start + 1:end]
    raise ValueError('unclosed fixture')


def obligation_errors(effects, triggers):
    errors = []
    acceptance = block(effects, 'rw_service_accept_promise_effect')
    if re.search(r'\b(add_gold|add_prestige|rw_service_settle_effect)\s*=', acceptance):
        errors.append('acceptance performs service/payment')
    if 'change_variable = { name = rw_service_revision add = 1 }' not in acceptance:
        errors.append('acceptance leaves negotiation revision live')
    if 'rw_service_snapshot_effect = yes' not in acceptance:
        errors.append('scheduled callbacks lack new snapshot')
    fulfillment = block(effects, 'rw_service_fulfill_promise_effect')
    if 'rw_service_obligation_fulfillable_trigger = yes' not in fulfillment:
        errors.append('unguarded fulfillment')
    consume, payment = fulfillment.find('rw_service_clear_effect = yes'), fulfillment.find('add_gold')
    if consume < 0 or payment < 0 or consume > payment:
        errors.append('fulfillment before consumption')
    timeout = block(effects, 'rw_service_timeout_effect')
    if 'rw_service_obligation_owner_matches_trigger = yes' not in timeout:
        errors.append('stale timeout can clear a new contract')
    if 'NOT = { has_character_flag = rw_service_deadline }' not in timeout:
        errors.append('premature timeout')
    if 'rw_service_affordable_trigger = yes' not in timeout:
        errors.append('timeout blames provider for unfunded service')
    if 'rw_service_cancel_promise_effect = yes' not in timeout:
        errors.append('unavailable party has no neutral cancellation')
    receipt = block(triggers, 'rw_service_breach_receipt_trigger')
    if 'var:rw_service_last_serial = scope:rw_service_serial' not in receipt:
        errors.append('reaction not bound to receipt')
    if 'NOT = { var:rw_service_reacted_serial = scope:rw_service_serial }' not in receipt:
        errors.append('reaction can replay')
    return errors


class DeferredContractTests(unittest.TestCase):
    def setUp(self):
        self.e = (MOD / 'common/scripted_effects/rw_obligation_effects.txt').read_text()
        self.t = (MOD / 'common/scripted_triggers/rw_service_triggers.txt').read_text()

    def test_contract(self):
        self.assertEqual([], obligation_errors(self.e, self.t))

    def test_prepayment_mutation(self):
        changed = self.e.replace('rw_service_accept_promise_effect = {', 'rw_service_accept_promise_effect = { add_gold = 50')
        self.assertIn('acceptance performs service/payment', obligation_errors(changed, self.t))

    def test_obsolete_acceptance_mutation(self):
        changed = self.e.replace('change_variable = { name = rw_service_revision add = 1 }', '')
        self.assertIn('acceptance leaves negotiation revision live', obligation_errors(changed, self.t))

    def test_unconditional_fulfillment_mutation(self):
        changed = self.e.replace('rw_service_obligation_fulfillable_trigger = yes', 'always = yes')
        self.assertIn('unguarded fulfillment', obligation_errors(changed, self.t))

    def test_consumption_removed(self):
        self.assertIn('fulfillment before consumption', obligation_errors(self.e.replace('rw_service_clear_effect = yes', ''), self.t))

    def test_stale_timeout_mutation(self):
        changed = self.e.replace('rw_service_obligation_owner_matches_trigger = yes', 'always = yes')
        self.assertIn('stale timeout can clear a new contract', obligation_errors(changed, self.t))

    def test_early_timeout_mutation(self):
        changed = self.e.replace('NOT = { has_character_flag = rw_service_deadline }', 'always = yes')
        self.assertIn('premature timeout', obligation_errors(changed, self.t))

    def test_unfunded_default_mutation(self):
        self.assertIn('timeout blames provider for unfunded service', obligation_errors(self.e.replace('rw_service_affordable_trigger = yes', 'always = yes'), self.t))

    def test_repeated_reaction_mutation(self):
        t = self.t.replace('NOT = { var:rw_service_reacted_serial = scope:rw_service_serial }', 'always = yes')
        self.assertIn('reaction can replay', obligation_errors(self.e, t))

    def test_forgiveness_has_no_penalty(self):
        forgive = block(self.e, 'rw_service_forgive_breach_effect')
        self.assertNotRegex(forgive, r'\b(add_opinion|add_gold|add_prestige)\s*=')
        resent = block(self.e, 'rw_service_resent_breach_effect')
        self.assertLess(resent.index('rw_service_reacted_serial'), resent.index('add_opinion'))

    def test_shared_ai_decision_and_expiry_schedule(self):
        events = (MOD / 'events/rw_obligation_events.txt').read_text()
        for option in ('fulfill', 'break', 'wait'):
            self.assertIn('name = rw_obligations.' + option, events)
        self.assertEqual(1, self.e.count('id = rw_obligations.0002 days = 31'))
        self.assertIn('rw_service_wait_promise_effect = yes', events)
        fulfillment = block(self.t, 'rw_service_obligation_fulfillable_trigger')
        self.assertIn('rw_service_affordable_trigger = yes', fulfillment)

    def test_orphan_cleanup_only_uses_exact_owner_identity(self):
        owner = block(self.t, 'rw_service_obligation_owner_matches_trigger')
        self.assertIn('var:rw_service_serial = scope:rw_service_serial', owner)
        self.assertIn('var:rw_service_revision = scope:rw_service_revision', owner)
        self.assertIn('has_character_flag = rw_service_obligation', owner)
        self.assertNotIn('exists = scope:rw_service_client', owner)
        cancel = block(self.e, 'rw_service_cancel_promise_effect')
        self.assertIn('rw_service_obligation_owner_matches_trigger = yes', cancel)
        self.assertNotRegex(cancel, r'\b(add_opinion|add_gold|add_prestige)\s*=')

    def test_translations_cover_promises(self):
        events = (MOD / 'events/rw_obligation_events.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', events))
        keys.update(('rw_review_endorsement_promise_interaction',
                     'rw_review_endorsement_promise_interaction_desc', 'rw_broken_service_opinion'))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_obligations_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set()
            for translation in (MOD / f'localization/{lang}').glob('*.yml'):
                actual.update(re.findall(r'^\s+([\w.]+):0', translation.read_text(encoding='utf-8-sig'), re.M))
            self.assertTrue(keys <= actual, keys - actual)

    def test_custom_effect_trigger_and_event_references_resolve(self):
        files = [p.read_text(encoding='utf-8-sig') for p in MOD.rglob('*.txt')]
        texts = [clean_script(text)[0] for text in files]
        definitions = set()
        references = set()
        for text in texts:
            definitions.update(re.findall(r'(?m)^\s*(rw_[\w.]+)\s*=\s*\{', text))
            references.update(re.findall(r'\b(rw_\w+(?:_effect|_trigger))\s*=', text))
        self.assertEqual(set(), references - definitions)
        events = set(re.findall(r'(?m)^(rw_[\w]+\.\d+)\s*=\s*\{', '\n'.join(texts)))
        event_refs = set(re.findall(r'\bid\s*=\s*(rw_\w+\.\d+)', '\n'.join(texts)))
        self.assertEqual(set(), event_refs - events)
