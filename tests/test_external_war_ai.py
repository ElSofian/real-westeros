"""Effective source wiring and negative contracts, not simulated CK3 choices."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_political_ai import option
from test_promise_ai_policy import action_digest

VALUES = 'common/script_values/rw_external_war_ai_values.txt'
RESPONSE = 'events/rw_external_war_response_events.txt'
MEDIATION = 'events/rw_external_war_mediation_events.txt'
BINDINGS = (
    (RESPONSE, 'rw_xw.ignore', 'rw_ai_xw_ignore_weight', 'rw_xw_turn_trigger', 30),
    (RESPONSE, 'rw_xw.disapprove', 'rw_ai_xw_disapprove_weight', 'rw_xw_turn_trigger', 30),
    (RESPONSE, 'rw_xw.demand', 'rw_ai_xw_demand_weight', 'rw_xw_turn_trigger', 25),
    (RESPONSE, 'rw_xw.native_intervene', 'rw_ai_xw_native_weight', 'rw_xw_can_queue_native_trigger', 20),
    (RESPONSE, 'rw_xm.request', 'rw_ai_xm_request_weight', 'rw_xm_can_request_trigger', 25),
    (RESPONSE, 'rw_xw.acknowledge', 'rw_ai_xw_acknowledge_weight', 'rw_xw_answer_turn_trigger', 30),
    (RESPONSE, 'rw_xw.refuse', 'rw_ai_xw_refuse_weight', 'rw_xw_answer_turn_trigger', 20),
    (MEDIATION, 'rw_xm.accept', 'rw_ai_xm_accept_weight', 'rw_xm_can_accept_trigger', 30),
    (MEDIATION, 'rw_xm.decline', 'rw_ai_xm_decline_weight', 'rw_xm_turn_trigger', 25),
    (MEDIATION, 'rw_xm.note_existing', 'rw_ai_xm_existing_weight', 'rw_xm_turn_trigger', 100),
)
ACTION_DIGESTS = {
    RESPONSE: 'ebe39c24edf1ca939fb58ee1268e2076a1c19a05704b7681eecf8697b2786c5b',
    MEDIATION: '342b2c7ae440cf83516ba3eb93fbd74fd307496479f66cd1f9d3915ffa5ca7fe',
}
UNCHANGED = {
    'common/scripted_effects/rw_external_war_intervention_effects.txt': '7398b6162273edb1051d2e6e624ca98a5524e7e6908eb5fa4ecd6ef2be67b1c7',
    'common/scripted_effects/rw_external_war_mediation_effects.txt': '3497619872c765119c72902481b6c9df406d23b0326c46047d849398636acd75',
    'common/scripted_effects/rw_external_war_response_effects.txt': '8b09f035557399529dfc679d281f737fc8b1783f93d043abfd32f6c3bf80d7b1',
    'common/scripted_triggers/rw_external_war_intervention_triggers.txt': '22db9a19ea2dcf7cb28b4c8c2ae2c527ef0ecc1cebaea523cdf60151e57dd4c7',
    'common/scripted_triggers/rw_external_war_mediation_triggers.txt': '24f9df8293f093ba367fe226698c26f8566df09ce59fdaf82269b9c75542c47d',
    'common/scripted_triggers/rw_external_war_response_triggers.txt': '1960ed62bf9f7873c928fb9a32a0cf585530385c517e7bb539e36086e9af6ae3',
    'common/story_cycles/rw_external_war_responses.txt': '9a138b1fdb4526e372095535543dd9cbd943b853de1a6e079257fbf524956b5d',
}
AXES = {'resolve': 'boldness', 'caution': 'boldness', 'honor': 'honor',
        'compassion': 'compassion', 'grievance': 'vengefulness',
        'initiative': 'energy', 'social': 'sociability', 'rationality': 'rationality'}


def policy_errors(values, events):
    errors = []
    definitions = set(re.findall(r'^\s*(rw_\w+)\s*=\s*\{', clean_script(values)[0], re.MULTILINE))
    references = set(re.findall(r'\b(?:multiply|divide)\s*=\s*(rw_\w+)', clean_script(values)[0]))
    if references - definitions:
        errors.append('unresolved personality factor')
    for file, choice, weight, guard, base in BINDINGS:
        body = block(values, weight)
        conditional = block(body, 'if')
        if not body.strip().startswith('value = 0') or any(token not in conditional for token in (guard+' = yes', 'add = '+str(base))):
            errors.append('unguarded '+weight)
        if weight != 'rw_ai_xm_existing_weight' and any(token not in conditional for token in ('min = 1', 'max = 300')):
            errors.append('unbounded '+weight)
        selected = option(events[file], choice)
        expected = 'base = 0 modifier = { add = '+weight+' always = yes }'
        if ' '.join(block(selected, 'ai_chance').split()) != expected:
            errors.append('unwired '+weight)
    for name, axis in AXES.items():
        factor = block(values, 'rw_ai_xw_'+name+'_factor')
        if any(token not in factor for token in ('value = ai_'+axis, 'divide = 200', 'add = 1', 'min = 0.5', 'max = 1.5')) or 'scope:' in factor:
            errors.append('foreign or unbounded axis '+name)
    if 'multiply = -1' not in block(values, 'rw_ai_xw_caution_factor'):
        errors.append('caution direction inverted')
    workload = block(values, 'rw_ai_xw_workload_factor')
    if any(token not in workload for token in ('is_at_war = yes', 'stress_level >= 2', 'health < 3',
                                               'rw_ai_existing_commitment_trigger = yes', 'min = 0.25', 'max = 1')):
        errors.append('own workload context missing')
    concern = block(values, 'rw_ai_xw_concern_factor')
    if any(token not in concern for token in ('var:rw_xw_role = flag:declaring_liege',
                                              'target = scope:rw_xw_defender',
                                              'target = scope:rw_xw_record.var:rw_xw_target.var:rw_dt_holder',
                                              'is_close_family_of', 'is_allied_to')):
        errors.append('beneficiary roles conflated')
    for factor, counterpart in (('attacker', 'rw_xw_attacker'), ('requester', 'rw_xw_ruler')):
        body = block(values, 'rw_ai_xw_'+factor+'_favor_factor')
        if any(token not in body for token in ('target = scope:'+counterpart+' value >= 25',
                                               'target = scope:'+counterpart+' value <= -25',
                                               'is_close_family_of = scope:'+counterpart,
                                               'is_allied_to = scope:'+counterpart)):
            errors.append('wrong own relationship '+factor)
    position = block(values, 'rw_ai_xw_refusal_position_factor')
    if any(token not in position for token in ('scope:rw_xw_record.var:rw_xw_war',
                                               'attacker_war_score >= 25', 'attacker_war_score <= -25',
                                               'multiply = rw_ai_xw_rationality_factor',
                                               'divide = rw_ai_xw_rationality_factor')):
        errors.append('wrong attacker war position')
    existing = block(values, 'rw_ai_xm_existing_weight')
    if 'rw_xw_other_native_attempt_trigger = yes' not in existing:
        errors.append('existing attempt fabricated')
    if re.search(r'\b(set_variable|change_variable|create_story|trigger_event|run_interaction|add_opinion|add_gold|save_scope_as|save_temporary_scope_as|save_scope_value_as)\s*=', clean_script(values)[0]):
        errors.append('AI profile mutates gameplay')
    if 'has_trait' in values or 'is_ai' in values:
        errors.append('trait gate or actor-specific permission')
    return errors


class ExternalWarAiTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.events = {file: (builder.TEMPLATES/file).read_text(encoding='utf-8-sig') for file in ACTION_DIGESTS}

    def test_actual_policy_and_ten_effective_weights(self):
        self.assertEqual([], policy_errors(self.values, self.events))
        self.assertEqual(10, len(BINDINGS))
        self.assertIn(VALUES, builder.FILES)
        self.assertIn('common/scripted_triggers/rw_political_ai_triggers.txt', builder.FILES)
        self.assertTrue((builder.TEMPLATES/VALUES).read_bytes().startswith(b'\xef\xbb\xbf'))

    def test_missing_stale_or_ineligible_frames_cannot_gain_weight(self):
        for _, _, weight, guard, _ in BINDINGS:
            with self.subTest(weight=weight):
                original = block(self.values, weight)
                changed = original.replace(guard+' = yes', 'always = yes', 1)
                self.assertIn('unguarded '+weight, policy_errors(self.values.replace(original, changed), self.events))

    def test_each_axis_uses_current_decider_with_positive_bounds(self):
        for name, axis in AXES.items():
            with self.subTest(axis=axis, factor=name):
                original = block(self.values, 'rw_ai_xw_'+name+'_factor')
                changed = original.replace('value = ai_'+axis, 'value = scope:rw_xw_attacker.ai_'+axis)
                self.assertIn('foreign or unbounded axis '+name,
                              policy_errors(self.values.replace(original, changed), self.events))

    def test_liege_and_protector_consider_their_correct_public_counterpart(self):
        changed = self.values.replace('target = scope:rw_xw_record.var:rw_xw_target.var:rw_dt_holder',
                                      'target = scope:rw_xw_attacker')
        self.assertIn('beneficiary roles conflated', policy_errors(changed, self.events))
        self.assertIn('multiply = rw_ai_xm_requester_favor_factor', block(self.values, 'rw_ai_xm_accept_weight'))
        self.assertIn('divide = rw_ai_xw_attacker_favor_factor', block(self.values, 'rw_ai_xm_accept_weight'))

    def test_workload_position_and_pending_attempt_evidence_are_required(self):
        for token, error in (('stress_level >= 2', 'own workload context missing'),
                             ('attacker_war_score <= -25', 'wrong attacker war position'),
                             ('rw_xw_other_native_attempt_trigger = yes', 'existing attempt fabricated')):
            with self.subTest(guard=token):
                self.assertIn(error, policy_errors(self.values.replace(token, 'always = yes'), self.events))

    def test_profile_is_read_only_and_old_flat_weight_cannot_survive(self):
        changed = self.values+'\nbad = { set_variable = {} }'
        self.assertIn('AI profile mutates gameplay', policy_errors(changed, self.events))
        changed = self.values.replace('multiply = rw_ai_xw_social_factor', 'multiply = rw_ai_missing_factor')
        self.assertIn('unresolved personality factor', policy_errors(changed, self.events))
        events = dict(self.events)
        events[MEDIATION] = events[MEDIATION].replace('add = rw_ai_xm_accept_weight', 'add = 30')
        self.assertIn('unwired rw_ai_xm_accept_weight', policy_errors(self.values, events))

    def test_all_actions_guards_effects_windows_and_native_dispatch_are_unchanged(self):
        for file, expected in ACTION_DIGESTS.items():
            with self.subTest(event=file):
                self.assertEqual(expected, action_digest(self.events[file]))
        for file, expected in UNCHANGED.items():
            with self.subTest(source=file):
                self.assertEqual(expected, hashlib.sha256((builder.TEMPLATES/file).read_bytes()).hexdigest())

    def test_free_messages_do_not_read_liquidity_as_a_payment(self):
        for name in ('ignore', 'disapprove', 'demand', 'acknowledge', 'refuse'):
            self.assertNotIn('gold', block(self.values, 'rw_ai_xw_'+name+'_weight'))
        self.assertIn('gold < 50', block(self.values, 'rw_ai_xw_native_weight'))
        self.assertIn('gold < 50', block(self.values, 'rw_ai_xm_accept_weight'))
