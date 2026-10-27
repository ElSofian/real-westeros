"""Mutation checks for script safety wiring; no CK3 gameplay is simulated."""
from pathlib import Path
import unittest
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def contract_errors(triggers, effects, events):
    triggers, effects, events = (clean_script(s)[0] for s in (triggers, effects, events))
    errors = []
    if 'var:rw_petition_revision = scope:rw_petition_revision' not in triggers:
        errors.append('event revision identity missing')
    if 'var:rw_petition_target = scope:rw_petition_recipient' not in triggers:
        errors.append('recipient identity missing')
    if 'remove_variable = rw_petition_revision' in effects:
        errors.append('revision reset permits old-event collision')
    if 'limit = { rw_petition_parties_valid_trigger = yes }' not in effects:
        errors.append('execution eligibility missing')
    if 'limit = { rw_petition_matches_trigger = yes }' not in effects:
        errors.append('cleanup identity missing')
    if 'rw_clear_petition_effect = yes' not in events:
        errors.append('dismissal cleanup missing')
    return errors


class LifecycleContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (ROOT / 'common/scripted_triggers/rw_reconciliation_triggers.txt').read_text()
        self.e = (ROOT / 'common/scripted_effects/rw_reconciliation_effects.txt').read_text()
        self.v = (ROOT / 'events/rw_reconciliation_events.txt').read_text()

    def test_contract(self):
        self.assertEqual([], contract_errors(self.t, self.e, self.v))

    def test_old_response_revision_guard_removed(self):
        t = self.t.replace('var:rw_petition_revision = scope:rw_petition_revision', 'always = yes')
        self.assertIn('event revision identity missing', contract_errors(t, self.e, self.v))

    def test_wrong_recipient_guard_removed(self):
        t = self.t.replace('var:rw_petition_target = scope:rw_petition_recipient', 'always = yes')
        self.assertIn('recipient identity missing', contract_errors(t, self.e, self.v))

    def test_revision_reset_rejected(self):
        self.assertIn('revision reset permits old-event collision', contract_errors(self.t, self.e + '\nremove_variable = rw_petition_revision', self.v))

    def test_execution_revalidation_removed(self):
        e = self.e.replace('limit = { rw_petition_parties_valid_trigger = yes }', 'limit = { always = yes }')
        self.assertIn('execution eligibility missing', contract_errors(self.t, e, self.v))

    def test_old_dismissal_cleanup_guard_removed(self):
        e = self.e.replace('limit = { rw_petition_matches_trigger = yes }', 'limit = { always = yes }')
        self.assertIn('cleanup identity missing', contract_errors(self.t, e, self.v))
