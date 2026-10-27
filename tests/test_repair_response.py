"""Adversarial source checks for voluntary repair consent, not engine execution."""
from pathlib import Path
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def response_errors(triggers, effects, case_effects):
    errors = []
    gate = block(triggers, 'rw_repair_client_turn_trigger')
    for required in ('rw_case_matches_trigger = yes', 'rw_case_jurisdiction_trigger = yes',
                     'this = scope:rw_service_client', 'var:rw_case_stage = flag:closed',
                     'var:rw_case_result = flag:repaired', 'var:rw_case_gesture = flag:offered',
                     'has_variable = rw_case_gesture_pending', 'rw_case_disclosed_trigger = yes'):
        if required not in gate:
            errors.append('wrong, expired or replayed response permitted')
    offer = block(case_effects, 'rw_case_apologise_effect')
    if 'scope:rw_service_client = {' in offer:
        errors.append('client opinion changes without consent')
    if 'name = rw_case_gesture_pending value = flag:yes days = 30' not in offer:
        errors.append('response deadline absent')
    if offer.find('name = rw_case_gesture value = flag:offered') > offer.find('rw_case_close_effect'):
        errors.append('response initialized after notification')
    for name in ('accept', 'reject'):
        effect = block(effects, f'rw_repair_{name}_effect')
        if 'limit = { rw_repair_client_turn_trigger = yes }' not in effect:
            errors.append('effect bypasses consent gate')
        if 'remove_variable = rw_case_gesture_pending' not in effect:
            errors.append('response remains replayable')
    accept = block(effects, 'rw_repair_accept_effect')
    if not 0 <= accept.find('name = rw_case_gesture value = flag:accepted') < accept.find('add_opinion'):
        errors.append('benefit before consumption')
    if 'add_opinion' in block(effects, 'rw_repair_reject_effect'):
        errors.append('refusal changes opinion')
    if 'set_variable = { name = rw_case_evidence' in effects:
        errors.append('response rewrites evidence')
    return errors


class RepairResponseTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_repair_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_repair_effects.txt').read_text()
        self.c = (MOD / 'common/scripted_effects/rw_case_effects.txt').read_text()

    def errors(self, t=None, e=None, c=None):
        return response_errors(self.t if t is None else t, self.e if e is None else e,
                               self.c if c is None else c)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_wrong_actor_stale_record_deadline_and_replay_mutations(self):
        for guard in ('this = scope:rw_service_client', 'rw_case_matches_trigger = yes',
                      'rw_case_jurisdiction_trigger = yes', 'has_variable = rw_case_gesture_pending',
                      'var:rw_case_gesture = flag:offered', 'var:rw_case_stage = flag:closed',
                      'var:rw_case_result = flag:repaired', 'rw_case_disclosed_trigger = yes'):
            with self.subTest(guard=guard):
                self.assertIn('wrong, expired or replayed response permitted',
                              self.errors(t=self.t.replace(guard, 'always = yes', 1)))

    def test_automatic_consent_mutation(self):
        c = self.c.replace('add_prestige = -25', 'add_prestige = -25\nscope:rw_service_client = { add_opinion = yes }')
        self.assertIn('client opinion changes without consent', self.errors(c=c))

    def test_direct_effect_bypass_mutation(self):
        self.assertIn('effect bypasses consent gate', self.errors(e=self.e.replace('limit = { rw_repair_client_turn_trigger = yes }', 'limit = { always = yes }')))

    def test_repeat_response_mutation(self):
        self.assertIn('response remains replayable', self.errors(e=self.e.replace('remove_variable = rw_case_gesture_pending', '')))

    def test_reward_before_consumption_mutation(self):
        e = self.e.replace('name = rw_case_gesture value = flag:accepted', 'name = rw_case_gesture value = flag:offered')
        self.assertIn('benefit before consumption', self.errors(e=e))

    def test_refusal_and_silence_have_no_economic_or_native_effect(self):
        reject = block(self.e, 'rw_repair_reject_effect')
        self.assertNotRegex(clean_script(reject)[0], r'\b(add_opinion|add_prestige|add_gold)\s*=')
        self.assertNotRegex(clean_script(self.e)[0], r'\b(add_gold|add_prestige|death|imprison|add_secret|add_hook|rw_case_close_effect)\s*=')
        self.assertNotIn('rw_case_pending value', self.e)
        self.assertNotIn('rw_case_retained value', self.e)
        self.assertNotIn('rw_service_last_outcome', self.e)

    def test_evidence_rewrite_mutation(self):
        self.assertIn('response rewrites evidence', self.errors(e=self.e + '\nset_variable = { name = rw_case_evidence value = flag:admitted }'))

    def test_record_view_readonly_and_role_guarded(self):
        events = (MOD / 'events/rw_case_events.txt').read_text()
        view = block(events, 'rw_cases.0007')
        self.assertIn('rw_repair_can_read_trigger = yes', view)
        self.assertNotRegex(view, r'\brw_\w+_effect\s*=')
        reader = block(self.t, 'rw_repair_can_read_trigger')
        self.assertIn('this = scope:rw_case_reader', reader)
        self.assertIn('rw_case_reader_allowed_trigger = { READER = scope:rw_case_reader }', reader)
        self.assertIn('has_variable = rw_case_gesture', reader)

    def test_ai_and_player_share_both_choices(self):
        events = (MOD / 'events/rw_case_events.txt').read_text()
        notice = block(events, 'rw_cases.0003')
        self.assertNotIn('is_ai', notice)
        self.assertIn('name = rw_repair.accept', notice)
        self.assertIn('name = rw_repair.reject', notice)
        self.assertEqual(2, notice.count('trigger = { rw_repair_client_turn_trigger = yes }'))
        self.assertIn('NOT = { rw_repair_client_turn_trigger = yes }', notice)
        self.assertIn('opinion = { target = scope:rw_service_provider', notice)
