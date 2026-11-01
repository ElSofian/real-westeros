"""Static wiring/mutation checks; no Python simulation of the service or engine."""
from pathlib import Path
import re
import unittest
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def contract_errors(triggers, effects):
    triggers, effects = (clean_script(s)[0] for s in (triggers, effects))
    errors = []
    for key in ('serial', 'revision', 'price', 'mode'):
        if f'var:rw_service_{key} = scope:rw_service_{key}' not in triggers:
            errors.append(f'missing {key} identity')
    if 'var:rw_service_target = scope:rw_service_client' not in triggers:
        errors.append('missing client identity')
    if 'remove_variable = rw_service_serial' in effects:
        errors.append('serial reset')
    if 'limit = { rw_service_can_offer_trigger = yes }' not in effects:
        errors.append('missing initiation revalidation')
    if 'gold >= scope:rw_service_price' not in triggers:
        errors.append('missing affordability')
    settlement = effects[effects.index('rw_service_settle_effect = {'):]
    if 'rw_service_affordable_trigger = yes' not in settlement:
        errors.append('missing settlement revalidation')
    consume = settlement.find('rw_service_clear_effect = yes')
    if consume < 0 or consume > settlement.find('add_gold'):
        errors.append('settlement occurs before consume')
    if effects.count('add_character_flag = { flag = rw_service_pending days = 30 }') != 1:
        errors.append('quote reset extends expiry')
    return errors


class ServiceContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (ROOT / 'common/scripted_triggers/rw_service_triggers.txt').read_text()
        self.e = (ROOT / 'common/scripted_effects/rw_service_effects.txt').read_text()

    def test_contract(self):
        self.assertEqual([], contract_errors(self.t, self.e))

    def test_stale_quote_mutation(self):
        changed = self.t.replace('var:rw_service_revision = scope:rw_service_revision', 'always = yes')
        self.assertIn('missing revision identity', contract_errors(changed, self.e))

    def test_payment_mode_mutation(self):
        changed = self.t.replace('var:rw_service_mode = scope:rw_service_mode', 'always = yes')
        self.assertIn('missing mode identity', contract_errors(changed, self.e))

    def test_old_contract_mutation(self):
        self.assertIn('serial reset', contract_errors(self.t, self.e + '\nremove_variable = rw_service_serial'))

    def test_wrong_client_mutation(self):
        changed = self.t.replace('var:rw_service_target = scope:rw_service_client', 'always = yes')
        self.assertIn('missing client identity', contract_errors(changed, self.e))

    def test_unfunded_settlement_mutation(self):
        self.assertIn('missing settlement revalidation', contract_errors(self.t, self.e.replace('rw_service_affordable_trigger = yes', 'always = yes')))

    def test_consumption_removed(self):
        e = self.e.replace('rw_service_clear_effect = yes', '')
        self.assertIn('settlement occurs before consume', contract_errors(self.t, e))

    def test_consumption_after_payment(self):
        e = self.e.replace('        rw_service_clear_effect = yes', '')
        e = e.replace('        scope:rw_service_client = { add_prestige = 50 }',
                      '        scope:rw_service_client = { add_prestige = 50 }\n        rw_service_clear_effect = yes')
        self.assertIn('settlement occurs before consume', contract_errors(self.t, e))

    def test_quote_cannot_extend_deadline(self):
        self.assertIn('quote reset extends expiry', contract_errors(self.t, self.e + '\nadd_character_flag = { flag = rw_service_pending days = 30 }'))

    def test_translations_cover_event_options(self):
        events = (ROOT / 'events/rw_service_events.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', events))
        keys.update(('rw_offer_endorsement_interaction', 'rw_offer_endorsement_interaction_desc',
                     'rw_offer_deferred_endorsement_interaction', 'rw_offer_deferred_endorsement_interaction_desc'))
        for lang in ('english','french'):
            p = ROOT / f'localization/{lang}/rw_services_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            shared_keys = set()
            for stem in ('rw_delivery', 'rw_remembered_support'):
                shared_path = ROOT / f'localization/{lang}/{stem}_l_{lang}.yml'
                self.assertTrue(shared_path.read_bytes().startswith(b'\xef\xbb\xbf'))
                shared = shared_path.read_text(encoding='utf-8-sig')
                shared_keys.update(re.findall(r'^\s+([\w.]+):0', shared, re.M))
            self.assertEqual(keys, actual | (shared_keys & keys))
