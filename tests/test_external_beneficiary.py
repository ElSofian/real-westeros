"""Read-only external claimant contracts, not a CK3 decision simulation."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_external_war_ai import VALUES, ACTION_DIGESTS
from test_promise_ai_policy import action_digest

CONTEXT = 'common/scripted_triggers/rw_external_beneficiary_triggers.txt'
CLAIMANT = 'scope:rw_xw_record.var:rw_xw_source.var:rw_dl_claimant'
FACTOR = 'rw_ai_xw_beneficiary_favor_factor'
BASELINE_PROFILE_DIGEST = 'e7f8eacb1c78ad2b6121994cc74971e1ca92ac5df4729ab9539861ff3bf2b9c4'
TURNS = ('rw_xw_turn_trigger = yes', 'rw_xw_answer_turn_trigger = yes', 'rw_xm_turn_trigger = yes')
PARENT = (
    'story_type = story_rw_declaration_law', 'story_owner = scope:rw_xw_attacker',
    'var:rw_dl_schema = 1', 'var:rw_dl_serial > 0',
    'var:rw_dl_serial = prev.var:rw_xw_source_serial', 'var:rw_dl_party_schema = 1',
    'var:rw_dl_phase = flag:claim_cb_on_declaration_prefix', 'has_variable = rw_dl_retained',
    'var:rw_dl_war = scope:rw_xw_record.var:rw_xw_war',
    'var:rw_dl_attacker = scope:rw_xw_attacker', 'var:rw_dl_defender = scope:rw_xw_defender',
    'var:rw_dl_claimant_state = flag:known', 'exists = var:rw_dl_claimant',
    'var:rw_dl_claimant = { is_alive = yes }',
    'NOT = { var:rw_dl_claimant = scope:rw_xw_attacker }',
)
IDENTITY_TOKENS = (*TURNS, 'exists = var:rw_xw_source', 'has_variable = rw_xw_source_serial', *PARENT)
DIRECTIONS = {
    'rw_ai_xw_ignore_weight': 'multiply', 'rw_ai_xw_disapprove_weight': 'divide',
    'rw_ai_xw_resolution_factor': 'divide', 'rw_ai_xw_acknowledge_weight': 'divide',
    'rw_ai_xw_refuse_weight': 'multiply', 'rw_ai_xm_accept_weight': 'divide',
    'rw_ai_xm_decline_weight': 'multiply',
}


def baseline_profile_digest(values):
    """Remove only this addition to retain the entire prior numeric policy."""
    clean = clean_script(values)[0]
    start, _, end = builder.bounds(clean, FACTOR)
    clean = clean[:start]+clean[end:]
    clean = re.sub(r'\b(?:multiply|divide)\s*=\s*'+FACTOR+r'\b', '', clean)
    return hashlib.sha256(' '.join(clean.split()).encode()).hexdigest()


def beneficiary_errors(values, context):
    errors = []
    guard = block(context, 'rw_ai_xw_beneficiary_context_trigger')
    if any(token not in block(guard, 'OR') for token in TURNS):
        errors.append('wrong external decider turns')
    record = block(guard, 'scope:rw_xw_record')
    if any(token not in record for token in IDENTITY_TOKENS[len(TURNS):]):
        errors.append('unbound external beneficiary')
    if any(token not in block(record, 'var:rw_xw_source') for token in PARENT):
        errors.append('wrong original claimant provenance')
    factor = block(values, FACTOR)
    conditional = block(factor, 'if')
    if (not factor.strip().startswith('value = 1') or
            'rw_ai_xw_beneficiary_context_trigger = yes' not in block(conditional, 'limit') or
            factor.count(CLAIMANT) != conditional.count(CLAIMANT) or
            'min = 0.5' not in factor or 'max = 2' not in factor):
        errors.append('missing neutral guarded affinity')
    for token in ('this = '+CLAIMANT, 'multiply = 1.5', 'else = {',
                  'target = '+CLAIMANT+' value >= 25', 'target = '+CLAIMANT+' value <= -25',
                  'is_close_family_of = '+CLAIMANT, 'is_allied_to = '+CLAIMANT,
                  'multiply = 1.25', 'multiply = 0.75'):
        if token not in conditional:
            errors.append('wrong own claimant relationship')
            break
    for name, operation in DIRECTIONS.items():
        if block(values, name).count(operation+' = '+FACTOR) != 1:
            errors.append('wrong direction '+name)
    if baseline_profile_digest(values) != BASELINE_PROFILE_DIGEST:
        errors.append('prior numeric policy changed')
    executable = clean_script(factor+context)[0]
    if re.search(r'\b(set_variable|change_variable|save_\w+|create_story|trigger_event|run_interaction|add_opinion|random\w*|any_\w+|every_\w+)\s*=', executable):
        errors.append('claimant policy writes or scans')
    if any(scope != 'rw_xw_record' for scope in re.findall(r'\bscope:(\w+)', factor)):
        errors.append('foreign or inferred claimant')
    if re.search(r'\b(?:has_trait\s*=|ai_\w+\b)', factor):
        errors.append('borrowed claimant personality')
    return errors


class ExternalBeneficiaryTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.context = (builder.TEMPLATES/CONTEXT).read_text(encoding='utf-8-sig')

    def test_actual_policy_and_matching_delivery(self):
        self.assertEqual([], beneficiary_errors(self.values, self.context))
        self.assertIn(CONTEXT, builder.FILES)
        for name in ('demand', 'native'):
            self.assertIn('multiply = rw_ai_xw_resolution_factor', block(self.values, 'rw_ai_xw_'+name+'_weight'))
        self.assertIn('multiply = rw_ai_xw_resolution_factor', block(self.values, 'rw_ai_xm_request_weight'))

    def test_issuer_attacker_mediator_turns_stay_separate(self):
        for token in TURNS:
            with self.subTest(turn=token):
                self.assertTrue(beneficiary_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_foreign_missing_dead_legacy_and_mismatched_parent_mutations(self):
        for token in IDENTITY_TOKENS[len(TURNS):]:
            with self.subTest(guard=token):
                self.assertTrue(beneficiary_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_neutrality_and_claimant_identity_are_guarded(self):
        for token in ('value = 1', 'rw_ai_xw_beneficiary_context_trigger = yes', 'min = 0.5', 'max = 2'):
            factor = block(self.values, FACTOR)
            changed = factor.replace(token, 'always = yes', 1)
            self.assertTrue(beneficiary_errors(self.values.replace(factor, changed), self.context))
        self.assertTrue(beneficiary_errors(self.values.replace(CLAIMANT, 'scope:rw_xw_attacker'), self.context))

    def test_all_seven_preference_directions_and_relationship_thresholds(self):
        for name, operation in DIRECTIONS.items():
            body = block(self.values, name)
            changed = body.replace(operation+' = '+FACTOR, 'add = '+FACTOR)
            self.assertTrue(beneficiary_errors(self.values.replace(body, changed), self.context))
        for token in ('value >= 25', 'value <= -25'):
            self.assertTrue(beneficiary_errors(self.values.replace(token, 'value = 0'), self.context))

    def test_entire_prior_profile_and_shared_peer_declaration_factors_preserved(self):
        self.assertEqual(BASELINE_PROFILE_DIGEST, baseline_profile_digest(self.values))
        changed = self.values.replace('value = ai_honor', 'value = ai_greed')
        self.assertIn('prior numeric policy changed', beneficiary_errors(changed, self.context))
        existing = block(self.values, 'rw_ai_xm_existing_weight')
        self.assertNotIn(FACTOR, existing)
        self.assertIn('rw_xw_other_native_attempt_trigger = yes', existing)

    def test_no_writes_scans_or_beneficiary_personality(self):
        changed = self.context+'\nbad = { set_variable = {} }'
        self.assertIn('claimant policy writes or scans', beneficiary_errors(self.values, changed))
        factor = block(self.values, FACTOR)
        changed = self.values.replace(factor, factor+'\nvalue = ai_honor')
        self.assertIn('borrowed claimant personality', beneficiary_errors(changed, self.context))

    def test_both_event_action_graphs_preserved(self):
        for name, expected in ACTION_DIGESTS.items():
            self.assertEqual(expected, action_digest((builder.TEMPLATES/name).read_text(encoding='utf-8-sig')))
