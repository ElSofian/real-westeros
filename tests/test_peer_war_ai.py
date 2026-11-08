"""Peer-response source policies and invariants, not a CK3 decision simulation."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_political_ai import option
from test_promise_ai_policy import action_digest

VALUES = 'common/script_values/rw_peer_war_ai_values.txt'
SHARED = 'common/script_values/rw_external_war_ai_values.txt'
EVENT = 'events/rw_unlawful_war_response_events.txt'
ACTION_DIGEST = '4ba2a17572959d677e3f0ec13ef46b8f28b752280e0e3f64eaccfd098cad8db0'
GUARD_FILE = 'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt'
GUARD_DIGEST = 'fae47d2941fa3999b0ea65aa5f12f05390e84771a5aa138f69cfc793060c9db9'
UNCHANGED = {
    'common/scripted_effects/rw_unlawful_war_response_effects.txt': '287f689916c744cc99f5ff7d12c0a619f1a8c515abeb79760d9e41f2ff72860e',
    'common/scripted_effects/rw_unlawful_war_intervention_effects.txt': '9de13bfe4d6e6d22463906d0440b8f5c50d87823d2027ed5fe69c59bc2cd6329',
    'common/story_cycles/rw_unlawful_war_responses.txt': '756a3ce435b83660d6bd9a1568ac732645d570fd8aae45b7a1c8b2c3b3390e4c',
    SHARED: '2de4a200314de8c600f330d72054853584c4608a6614c68b9384db06326a4fe6',
}
BINDINGS = (
    ('rw_uw.ignore', 'rw_ai_uw_ignore_weight', 'rw_uw_issuer_turn_trigger', 20),
    ('rw_uw.censure', 'rw_ai_uw_censure_weight', 'rw_uw_issuer_turn_trigger', 20),
    ('rw_uw.demand', 'rw_ai_uw_demand_weight', 'rw_uw_issuer_turn_trigger', 30),
    ('rw_uw.native_intervene', 'rw_ai_uw_native_weight', 'rw_uw_can_queue_native_trigger', 20),
    ('rw_uw.acknowledge', 'rw_ai_uw_acknowledge_weight', 'rw_uw_answer_turn_trigger', 30),
    ('rw_uw.refuse', 'rw_ai_uw_refuse_weight', 'rw_uw_answer_turn_trigger', 15),
)
SHARED_FACTORS = {'rw_ai_xw_'+name+'_factor' for name in (
    'resolve', 'caution', 'honor', 'compassion', 'grievance', 'initiative', 'social',
    'rationality', 'workload')}


def guard_digest(text):
    """Keep every byte outside the deliberately separate AI initial preference."""
    start, _, end = builder.bounds(text, 'rw_uw_ai_default_defiance_trigger')
    return hashlib.sha256((text[:start]+text[end:]).encode('utf-8')).hexdigest()


def peer_policy_errors(values, shared, event):
    errors = []
    for choice, name, guard, base in BINDINGS:
        body = block(values, name)
        conditional = block(body, 'if')
        if not body.strip().startswith('value = 0') or any(token not in conditional for token in (guard+' = yes', 'add = '+str(base))):
            errors.append('unguarded '+name)
        if any(token not in conditional for token in ('min = 1', 'max = 300')):
            errors.append('unbounded '+name)
        expected = 'base = 0 modifier = { add = '+name+' always = yes }'
        if ' '.join(block(option(event, choice), 'ai_chance').split()) != expected:
            errors.append('unwired '+name)
    clean = clean_script(values)[0]
    definitions = set(re.findall(r'^\s*(rw_\w+)\s*=\s*\{', clean+clean_script(shared)[0], re.MULTILINE))
    references = set(re.findall(r'\b(?:multiply|divide)\s*=\s*(rw_\w+)', clean))
    if references - definitions:
        errors.append('unresolved factor')
    used_shared = {name for name in references if name.startswith('rw_ai_xw_')}
    if used_shared != SHARED_FACTORS:
        errors.append('wrong shared factor set')
    for name in used_shared:
        if 'scope:' in block(shared, name):
            errors.append('shared factor borrows foreign frame')
    if any(not name.startswith('rw_uw_') for name in re.findall(r'\bscope:(\w+)', clean)):
        errors.append('foreign event frame')
    for factor, counterpart in (('attacker_favor', 'attacker'), ('defender_concern', 'defender'), ('issuer_favor', 'issuer')):
        body = block(values, 'rw_ai_uw_'+factor+'_factor')
        for token in ('target = scope:rw_uw_'+counterpart+' value >= 25',
                      'target = scope:rw_uw_'+counterpart+' value <= -25',
                      'is_close_family_of = scope:rw_uw_'+counterpart,
                      'is_allied_to = scope:rw_uw_'+counterpart, 'min = 0.5', 'max = 2'):
            if token not in body:
                errors.append('wrong relationship '+factor)
                break
    position = block(values, 'rw_ai_uw_refusal_position_factor')
    if any(token not in position for token in ('scope:rw_uw_war', 'attacker_war_score >= 25',
                                               'attacker_war_score <= -25',
                                               'multiply = rw_ai_xw_rationality_factor',
                                               'divide = rw_ai_xw_rationality_factor')):
        errors.append('wrong peer war position')
    if re.search(r'\b(set_variable|change_variable|create_story|trigger_event|run_interaction|add_opinion|add_gold|save_scope_as|save_temporary_scope_as|save_scope_value_as)\s*=', clean):
        errors.append('policy mutates gameplay')
    if 'has_trait' in clean or 'is_ai' in clean:
        errors.append('trait gate or actor-specific permission')
    return errors


class PeerWarAiTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.shared = (builder.TEMPLATES/SHARED).read_text(encoding='utf-8-sig')
        self.event = (builder.TEMPLATES/EVENT).read_text(encoding='utf-8-sig')

    def test_actual_six_weights_and_matching_shared_delivery(self):
        self.assertEqual([], peer_policy_errors(self.values, self.shared, self.event))
        for name in (VALUES, SHARED, EVENT):
            self.assertIn(name, builder.FILES)
        self.assertTrue((builder.TEMPLATES/VALUES).read_bytes().startswith(b'\xef\xbb\xbf'))

    def test_stale_missing_and_wrong_turn_contexts_cannot_gain_weight(self):
        for _, name, guard, _ in BINDINGS:
            with self.subTest(weight=name):
                original = block(self.values, name)
                changed = original.replace(guard+' = yes', 'always = yes')
                self.assertIn('unguarded '+name,
                              peer_policy_errors(self.values.replace(original, changed), self.shared, self.event))

    def test_public_relationships_use_their_own_peer_counterparts(self):
        for counterpart in ('attacker', 'defender', 'issuer'):
            with self.subTest(party=counterpart):
                changed = self.values.replace('scope:rw_uw_'+counterpart, 'scope:rw_uw_record')
                self.assertTrue(peer_policy_errors(changed, self.shared, self.event))

    def test_foreign_saved_frames_are_rejected(self):
        changed = self.values.replace('scope:rw_uw_attacker', 'scope:rw_xw_attacker')
        self.assertIn('foreign event frame', peer_policy_errors(changed, self.shared, self.event))
        changed = self.values.replace('rw_ai_xw_caution_factor', 'rw_ai_xw_concern_factor')
        self.assertIn('shared factor borrows foreign frame', peer_policy_errors(changed, self.shared, self.event))

    def test_same_war_position_and_opposite_reply_directions_are_required(self):
        changed = self.values.replace('attacker_war_score <= -25', 'attacker_war_score >= -25')
        self.assertIn('wrong peer war position', peer_policy_errors(changed, self.shared, self.event))
        self.assertIn('divide = rw_ai_uw_refusal_position_factor', block(self.values, 'rw_ai_uw_acknowledge_weight'))
        self.assertIn('multiply = rw_ai_uw_refusal_position_factor', block(self.values, 'rw_ai_uw_refuse_weight'))

    def test_old_flat_wiring_and_missing_numeric_factors_are_detected(self):
        changed = self.event.replace('add = rw_ai_uw_native_weight', 'add = 20')
        self.assertIn('unwired rw_ai_uw_native_weight', peer_policy_errors(self.values, self.shared, changed))
        changed = self.values.replace('multiply = rw_ai_uw_resolution_factor', 'multiply = rw_ai_missing_factor')
        self.assertIn('unresolved factor', peer_policy_errors(changed, self.shared, self.event))

    def test_only_ai_weights_change_in_the_original_event(self):
        self.assertEqual(ACTION_DIGEST, action_digest(self.event))
        self.assertEqual(GUARD_DIGEST, guard_digest((builder.TEMPLATES/GUARD_FILE).read_text(encoding='utf-8-sig')))
        for name, expected in UNCHANGED.items():
            with self.subTest(source=name):
                self.assertEqual(expected, hashlib.sha256((builder.TEMPLATES/name).read_bytes()).hexdigest())

    def test_read_only_preferences_and_liquidity_restricted_to_native_attempt(self):
        changed = self.values+'\nbad = { set_variable = {} }'
        self.assertIn('policy mutates gameplay', peer_policy_errors(changed, self.shared, self.event))
        for _, name, _, _ in BINDINGS:
            if name != 'rw_ai_uw_native_weight':
                self.assertNotIn('gold', block(self.values, name))
        self.assertIn('gold < 50', block(self.values, 'rw_ai_uw_native_weight'))
