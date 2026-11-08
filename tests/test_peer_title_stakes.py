"""Peer title context and opposite response directions, without CK3 simulation."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_peer_war_ai import VALUES, EVENT, ACTION_DIGEST
from test_promise_ai_policy import action_digest
from test_committed_war_support import strip_support_extension

CONTEXT = 'common/scripted_triggers/rw_peer_title_stakes_triggers.txt'
FACTOR = 'rw_ai_uw_title_stakes_factor'
CONTESTED = 'rw_ai_uw_contested_stakes_factor'
FACT_GUARD = 'rw_ai_uw_title_fact_trigger = yes'
BASELINE_DIGEST = '66d422346c32fe89c2c61cf133b09d19ca401148205047bfe3c88cc2a9fb0bf5'
PARENT_TOKENS = (
    'rw_dl_match_response_trigger = yes', 'var:rw_dl_serial > 0',
    'var:rw_dl_serial = prev.var:rw_dl_link_serial', 'var:rw_dl_party_schema = 1',
    'has_variable = rw_dl_seen_on', 'var:rw_dl_targets_state = flag:all_titles_recorded',
    'var:rw_dl_target_count > 0', 'var:rw_dl_target_records = var:rw_dl_target_count',
)
CONTEXT_TOKENS = (
    'OR = { rw_uw_issuer_turn_trigger = yes rw_uw_answer_turn_trigger = yes }',
    'exists = var:rw_dl_link', 'has_variable = rw_dl_link_serial', *PARENT_TOKENS,
)
FACT_TOKENS = (
    'story_type = story_rw_declaration_target', 'story_owner = scope:rw_uw_attacker',
    'var:rw_dt_schema = 1', 'exists = var:rw_dt_parent', 'has_variable = rw_dt_parent_serial',
    'exists = var:rw_dt_war', 'has_variable = rw_dt_seen_on',
    'var:rw_dt_parent = scope:rw_uw_record.var:rw_dl_link',
    'var:rw_dt_parent_serial = scope:rw_uw_record.var:rw_dl_link_serial',
    'var:rw_dt_war = scope:rw_uw_war',
    'var:rw_dt_seen_on = scope:rw_uw_record.var:rw_dl_link.var:rw_dl_seen_on',
    'var:rw_dt_holder_state = flag:known', 'exists = var:rw_dt_title',
    'exists = var:rw_dt_holder', 'exists = var:rw_dt_holder_liege',
    'exists = var:rw_dt_holder_authority', 'is_alive = yes',
    'liege = prev.var:rw_dt_holder_liege', 'this = scope:rw_uw_defender',
    'is_vassal_or_below_of = scope:rw_uw_defender',
    'var:rw_dt_title = { holder = prev.var:rw_dt_holder }',
    'var:rw_dt_holder_authority = { holder = prev.var:rw_dt_holder_liege }',
)
CLAIMANT_TOKENS = (
    'rw_uw_answer_turn_trigger = yes', 'rw_ai_uw_title_context_trigger = yes',
    'var:rw_dl_claimant_state = flag:known', 'exists = var:rw_dl_claimant',
    'var:rw_dl_claimant = { is_alive = yes }',
)


def previous_profile_digest(values):
    clean = strip_support_extension(values)
    for name in (FACTOR, CONTESTED):
        start, _, end = builder.bounds(clean, name)
        clean = clean[:start]+clean[end:]
        clean = re.sub(r'\b(?:multiply|divide)\s*=\s*'+name+r'\b', '', clean)
    return hashlib.sha256(' '.join(clean.split()).encode()).hexdigest()


def stakes_errors(values, context):
    errors = []
    guard = block(context, 'rw_ai_uw_title_context_trigger')
    if (any(token not in guard for token in CONTEXT_TOKENS) or
            any(token not in block(guard, 'var:rw_dl_link') for token in PARENT_TOKENS)):
        errors.append('invalid peer title context')
    fact = block(context, 'rw_ai_uw_title_fact_trigger')
    if any(token not in fact for token in FACT_TOKENS):
        errors.append('foreign or changed defender-side title')
    holder = block(fact, 'var:rw_dt_holder')
    if ('this = scope:rw_uw_defender' not in block(holder, 'OR') or
            'is_vassal_or_below_of = scope:rw_uw_defender' not in block(holder, 'OR')):
        errors.append('nested holder is not defender-side')
    claimant = block(context, 'rw_ai_uw_contested_stakes_context_trigger')
    if (any(token not in claimant for token in CLAIMANT_TOKENS) or
            'scope:rw_uw_record.var:rw_dl_link = {' not in claimant or
            'NOT =' in claimant):
        errors.append('missing original claimant or own claim excluded')
    factor = block(values, FACTOR)
    conditional = block(factor, 'if')
    if (not factor.strip().startswith('value = 1') or
            'rw_ai_uw_title_context_trigger = yes' not in block(conditional, 'limit') or
            'min = 1' not in factor or 'max = 1.7' not in factor):
        errors.append('missing neutral bounded title stakes')
    searches = [block(conditional[m.start():], 'any_owned_story')
                for m in re.finditer(r'\bany_owned_story\s*=', conditional)]
    if (len(searches) != 6 or any(FACT_GUARD not in search for search in searches) or
            conditional.count('scope:rw_uw_attacker = {') != 6):
        errors.append('unbound peer title search')
    for search, tier in zip(searches[:4], ('empire', 'kingdom', 'duchy', 'county')):
        if 'var:rw_dt_title = { tier >= tier_'+tier+' }' not in search:
            errors.append('wrong target rank')
    if (conditional.count('else_if = {') != 3 or
            re.findall(r'\badd\s*=\s*([\d.]+)', conditional) != ['0.4', '0.3', '0.2', '0.1', '0.2', '0.1']):
        errors.append('ranks stack or coefficients differ')
    if (len(searches) == 6 and
            ('exists = var:rw_dt_holder.primary_title' not in searches[4] or
             'var:rw_dt_title = { this = prev.var:rw_dt_holder.primary_title }' not in searches[4] or
             'count >= 2' not in searches[5])):
        errors.append('wrong primary or multiple-title signal')
    contested = block(values, CONTESTED)
    if (not contested.strip().startswith('value = 1') or
            'rw_ai_uw_contested_stakes_context_trigger = yes' not in block(block(contested, 'if'), 'limit') or
            'multiply = '+FACTOR not in block(contested, 'if') or
            'min = 1' not in contested or 'max = 1.7' not in contested):
        errors.append('unguarded claimant attachment')
    for name, operation, target in (
            ('rw_ai_uw_defender_concern_factor', 'multiply', FACTOR),
            ('rw_ai_uw_acknowledge_weight', 'divide', CONTESTED),
            ('rw_ai_uw_refuse_weight', 'multiply', CONTESTED)):
        if block(values, name).count(operation+' = '+target) != 1:
            errors.append('wrong stakes direction '+name)
    if previous_profile_digest(values) != BASELINE_DIGEST:
        errors.append('prior peer numeric policy changed')
    executable = clean_script(factor+contested+context)[0]
    if re.search(r'\b(set_variable|change_variable|save_\w+|create_story|trigger_event|run_interaction|add_opinion|random\w*|every_\w+)\s*=', executable):
        errors.append('stakes write or global work')
    if set(re.findall(r'\b(any_\w+)\s*=', executable)) - {'any_owned_story'}:
        errors.append('stakes write or global work')
    if any(not name.startswith('rw_uw_') for name in re.findall(r'\bscope:(\w+)', executable)):
        errors.append('foreign stakes frame')
    return errors


class PeerTitleStakesTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.context = (builder.TEMPLATES/CONTEXT).read_text(encoding='utf-8-sig')

    def test_actual_policy_and_matching_delivery(self):
        self.assertEqual([], stakes_errors(self.values, self.context))
        self.assertIn(CONTEXT, builder.FILES)

    def test_legacy_partial_foreign_and_expired_parent_guards(self):
        for token in CONTEXT_TOKENS:
            with self.subTest(guard=token):
                self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_actual_holder_and_nested_defender_side_are_required(self):
        for token in FACT_TOKENS:
            with self.subTest(guard=token):
                self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_claim_goal_needs_original_living_claimant_including_own_claim(self):
        for token in CLAIMANT_TOKENS:
            self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))
        changed = self.context.replace('exists = var:rw_dl_claimant', 'NOT = { var:rw_dl_claimant = scope:rw_uw_attacker }')
        self.assertTrue(stakes_errors(self.values, changed))

    def test_all_local_searches_rank_exclusivity_and_primary_holder(self):
        for old, new in ((FACT_GUARD, 'always = yes'), ('else_if = {', 'if = {'),
                         ('prev.var:rw_dt_holder.primary_title', 'scope:rw_uw_defender.primary_title'),
                         ('count >= 2', 'count >= 1')):
            self.assertTrue(stakes_errors(self.values.replace(old, new, 1), self.context))

    def test_neutrality_bounds_and_opposite_response_directions(self):
        for name in (FACTOR, CONTESTED):
            body = block(self.values, name)
            self.assertTrue(stakes_errors(self.values.replace(body, body.replace('value = 1', 'value = 0', 1)), self.context))
        self.assertTrue(stakes_errors(self.values.replace('divide = '+CONTESTED, 'multiply = '+CONTESTED), self.context))

    def test_no_writes_global_scans_or_foreign_event_scopes(self):
        self.assertTrue(stakes_errors(self.values, self.context+'\nbad = { set_variable = {} }'))
        self.assertTrue(stakes_errors(self.values.replace('any_owned_story = {', 'any_living_character = {', 1), self.context))
        self.assertTrue(stakes_errors(self.values, self.context.replace('scope:rw_uw_defender', 'scope:rw_xw_defender')))

    def test_prior_policy_and_action_graph_are_preserved(self):
        self.assertEqual(BASELINE_DIGEST, previous_profile_digest(self.values))
        self.assertTrue(stakes_errors(self.values.replace('add = 20', 'add = 200', 1), self.context))
        self.assertEqual(ACTION_DIGEST, action_digest((builder.TEMPLATES/EVENT).read_text(encoding='utf-8-sig')))
