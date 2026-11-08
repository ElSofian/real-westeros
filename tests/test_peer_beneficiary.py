"""Exact public claimant source contracts, without simulating CK3 decisions."""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_peer_war_ai import VALUES, ACTION_DIGEST, EVENT
from test_promise_ai_policy import action_digest

CONTEXT = 'common/scripted_triggers/rw_peer_beneficiary_triggers.txt'
CLAIMANT = 'scope:rw_uw_record.var:rw_dl_link.var:rw_dl_claimant'
FACTOR = 'rw_ai_uw_beneficiary_favor_factor'
IDENTITY_TOKENS = (
    'OR = { rw_uw_issuer_turn_trigger = yes rw_uw_answer_turn_trigger = yes }',
    'exists = var:rw_dl_link', 'has_variable = rw_dl_link_serial',
    'rw_dl_match_response_trigger = yes', 'var:rw_dl_serial > 0',
    'var:rw_dl_serial = prev.var:rw_dl_link_serial', 'var:rw_dl_party_schema = 1',
    'var:rw_dl_claimant_state = flag:known', 'exists = var:rw_dl_claimant',
    'var:rw_dl_claimant = { is_alive = yes }',
    'NOT = { var:rw_dl_claimant = scope:rw_uw_attacker }',
)
DIRECTIONS = {
    'ignore_weight': 'multiply', 'censure_weight': 'divide',
    'resolution_factor': 'divide', 'acknowledge_weight': 'divide',
    'refuse_weight': 'multiply',
}


def beneficiary_errors(values, context):
    errors = []
    guard = block(context, 'rw_ai_uw_beneficiary_context_trigger')
    if any(token not in guard for token in IDENTITY_TOKENS):
        errors.append('unbound beneficiary context')
    parent = block(guard, 'var:rw_dl_link')
    if any(token not in parent for token in IDENTITY_TOKENS[3:]):
        errors.append('wrong claimant provenance')
    factor = block(values, FACTOR)
    conditional = block(factor, 'if')
    if (not factor.strip().startswith('value = 1') or
            'rw_ai_uw_beneficiary_context_trigger = yes' not in block(conditional, 'limit') or
            factor.count(CLAIMANT) != conditional.count(CLAIMANT) or
            'min = 0.5' not in factor or 'max = 2' not in factor):
        errors.append('missing neutral guarded factor')
    for token in ('this = '+CLAIMANT, 'multiply = 1.5', 'else = {',
                  'target = '+CLAIMANT+' value >= 25',
                  'target = '+CLAIMANT+' value <= -25',
                  'is_close_family_of = '+CLAIMANT, 'is_allied_to = '+CLAIMANT,
                  'multiply = 1.25', 'multiply = 0.75'):
        if token not in conditional:
            errors.append('wrong own beneficiary affinity')
            break
    for name, operation in DIRECTIONS.items():
        if block(values, 'rw_ai_uw_'+name).count(operation+' = '+FACTOR) != 1:
            errors.append('wrong direction '+name)
    executable = clean_script(factor+context)[0]
    if re.search(r'\b(set_variable|change_variable|save_\w+|create_story|trigger_event|run_interaction|add_opinion|random\w*|any_\w+|every_\w+)\s*=', executable):
        errors.append('beneficiary policy writes or scans')
    if any(scope != 'rw_uw_record' for scope in re.findall(r'\bscope:(\w+)', factor)):
        errors.append('inferred or foreign claimant')
    if re.search(r'\b(?:has_trait\s*=|ai_\w+\b)', factor):
        errors.append('borrowed beneficiary personality')
    return errors


class PeerBeneficiaryTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.context = (builder.TEMPLATES/CONTEXT).read_text(encoding='utf-8-sig')

    def test_actual_policy_is_delivered_and_wired(self):
        self.assertEqual([], beneficiary_errors(self.values, self.context))
        self.assertIn(CONTEXT, builder.FILES)
        for name in ('demand_weight', 'native_weight'):
            self.assertIn('multiply = rw_ai_uw_resolution_factor', block(self.values, 'rw_ai_uw_'+name))

    def test_missing_foreign_stale_legacy_dead_and_own_claim_guards(self):
        for token in IDENTITY_TOKENS:
            with self.subTest(guard=token):
                self.assertTrue(beneficiary_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_unavailable_context_keeps_neutral_affinity(self):
        for token in ('value = 1', 'rw_ai_uw_beneficiary_context_trigger = yes', 'min = 0.5', 'max = 2'):
            factor = block(self.values, FACTOR)
            changed = factor.replace(token, 'always = yes', 1)
            self.assertTrue(beneficiary_errors(self.values.replace(factor, changed), self.context))

    def test_counterpart_and_opinion_direction_mutations_fail(self):
        for old, new in ((CLAIMANT, 'scope:rw_uw_attacker'),
                         ('value >= 25', 'value <= 25'), ('value <= -25', 'value >= -25')):
            self.assertTrue(beneficiary_errors(self.values.replace(old, new), self.context))

    def test_stop_and_refusal_directions_remain_opposed(self):
        for name, operation in DIRECTIONS.items():
            body = block(self.values, 'rw_ai_uw_'+name)
            changed = body.replace(operation+' = '+FACTOR, 'add = '+FACTOR)
            self.assertTrue(beneficiary_errors(self.values.replace(body, changed), self.context))

    def test_read_only_and_no_other_personality(self):
        changed = self.context+'\nbad = { set_variable = {} }'
        self.assertIn('beneficiary policy writes or scans', beneficiary_errors(self.values, changed))
        factor = block(self.values, FACTOR)
        changed = factor+'\nvalue = ai_honor'
        self.assertIn('borrowed beneficiary personality',
                      beneficiary_errors(self.values.replace(factor, changed), self.context))

    def test_event_action_graph_is_preserved(self):
        event = (builder.TEMPLATES/EVENT).read_text(encoding='utf-8-sig')
        self.assertEqual(ACTION_DIGEST, action_digest(event))
