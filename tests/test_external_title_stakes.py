"""External title interests with role isolation, without CK3 simulation."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_external_war_ai import VALUES, ACTION_DIGESTS
from test_promise_ai_policy import action_digest

CONTEXT = 'common/scripted_triggers/rw_external_title_stakes_triggers.txt'
FACTOR = 'rw_ai_xw_external_title_factor'
GOAL = 'rw_ai_xw_claim_goal_factor'
FACT_GUARD = 'rw_ai_xw_external_title_fact_trigger = yes'
BASELINE_DIGEST = 'fbe4f05ae161071f6a5cfa273a6c16dd322ae4976c74f44f2068dd9fb79a3819'
TURNS = (
    'rw_xw_turn_trigger = yes', 'var:rw_xw_role = flag:declaring_liege',
    'rw_xw_answer_turn_trigger = yes', 'rw_xm_turn_trigger = yes',
)
PARENT_TOKENS = (
    'story_type = story_rw_declaration_law', 'story_owner = scope:rw_xw_attacker',
    'var:rw_dl_schema = 1', 'var:rw_dl_serial > 0',
    'var:rw_dl_serial = prev.var:rw_xw_source_serial', 'var:rw_dl_party_schema = 1',
    'var:rw_dl_phase = flag:claim_cb_on_declaration_prefix', 'has_variable = rw_dl_retained',
    'has_variable = rw_dl_seen_on', 'var:rw_dl_war = scope:rw_xw_record.var:rw_xw_war',
    'var:rw_dl_attacker = scope:rw_xw_attacker', 'var:rw_dl_defender = scope:rw_xw_defender',
    'var:rw_dl_targets_state = flag:all_titles_recorded', 'var:rw_dl_target_count > 0',
    'var:rw_dl_target_records = var:rw_dl_target_count',
)
CONTEXT_TOKENS = (*TURNS, 'exists = var:rw_xw_source', 'has_variable = rw_xw_source_serial', *PARENT_TOKENS)
FACT_TOKENS = (
    'story_type = story_rw_declaration_target', 'story_owner = scope:rw_xw_attacker',
    'var:rw_dt_schema = 1', 'exists = var:rw_dt_parent', 'has_variable = rw_dt_parent_serial',
    'exists = var:rw_dt_war', 'has_variable = rw_dt_seen_on',
    'var:rw_dt_parent = scope:rw_xw_record.var:rw_xw_source',
    'var:rw_dt_parent_serial = scope:rw_xw_record.var:rw_xw_source_serial',
    'var:rw_dt_war = scope:rw_xw_record.var:rw_xw_war',
    'var:rw_dt_seen_on = scope:rw_xw_record.var:rw_xw_source.var:rw_dl_seen_on',
    'var:rw_dt_holder_state = flag:known', 'exists = var:rw_dt_title',
    'exists = var:rw_dt_holder', 'var:rw_dt_holder = { is_alive = yes }',
    'var:rw_dt_title = { holder = prev.var:rw_dt_holder }',
    'var:rw_dt_holder = scope:rw_xw_defender', 'exists = var:rw_dt_holder_liege',
    'exists = var:rw_dt_holder_authority', 'liege = prev.var:rw_dt_holder_liege',
    'is_vassal_or_below_of = scope:rw_xw_defender',
    'var:rw_dt_holder_authority = { holder = prev.var:rw_dt_holder_liege }',
)
CLAIMANT_TOKENS = (
    'rw_xw_answer_turn_trigger = yes', 'rw_ai_xw_external_title_context_trigger = yes',
    'var:rw_dl_claimant_state = flag:known', 'exists = var:rw_dl_claimant',
    'var:rw_dl_claimant = { is_alive = yes }',
)


def strip_title_extension(values):
    """Share the exact removal with older invariants, including legacy inputs."""
    clean = clean_script(values)[0]
    for name in (FACTOR, GOAL):
        if re.search(r'^\s*'+name+r'\s*=\s*\{', clean, re.MULTILINE):
            start, _, end = builder.bounds(clean, name)
            clean = clean[:start]+clean[end:]
            clean = re.sub(r'\b(?:multiply|divide)\s*=\s*'+name+r'\b', '', clean)
    return clean


def previous_profile_digest(values):
    return hashlib.sha256(' '.join(strip_title_extension(values).split()).encode()).hexdigest()


def stakes_errors(values, context):
    errors = []
    guard = block(context, 'rw_ai_xw_external_title_context_trigger')
    turns = block(guard, 'OR')
    if (any(token not in guard for token in CONTEXT_TOKENS) or
            any(token not in block(turns, 'AND') for token in TURNS[:2])):
        errors.append('wrong external decider turns')
    if any(token not in block(guard, 'var:rw_xw_source') for token in PARENT_TOKENS):
        errors.append('invalid complete original source')
    fact = block(context, 'rw_ai_xw_external_title_fact_trigger')
    if any(token not in fact for token in FACT_TOKENS):
        errors.append('foreign or changed target fact')
    sides = block(fact, 'OR')
    nested = block(sides, 'AND')
    if ('var:rw_dt_holder = scope:rw_xw_defender' not in sides or
            any(token not in nested for token in FACT_TOKENS[-5:])):
        errors.append('independent or nested holder confused')
    claimant = block(context, 'rw_ai_xw_claim_goal_context_trigger')
    if (any(token not in claimant for token in CLAIMANT_TOKENS) or
            'scope:rw_xw_record.var:rw_xw_source = {' not in claimant or 'NOT =' in claimant):
        errors.append('original claimant missing or own claim excluded')
    factor = block(values, FACTOR)
    conditional = block(factor, 'if')
    if (not factor.strip().startswith('value = 1') or
            'rw_ai_xw_external_title_context_trigger = yes' not in block(conditional, 'limit') or
            'min = 1' not in factor or 'max = 1.7' not in factor):
        errors.append('missing neutral bounded magnitude')
    searches = [block(conditional[m.start():], 'any_owned_story')
                for m in re.finditer(r'\bany_owned_story\s*=', conditional)]
    if (len(searches) != 6 or any(FACT_GUARD not in search for search in searches) or
            conditional.count('scope:rw_xw_attacker = {') != 6):
        errors.append('unbound title search')
    for search, tier in zip(searches[:4], ('empire', 'kingdom', 'duchy', 'county')):
        if 'var:rw_dt_title = { tier >= tier_'+tier+' }' not in search:
            errors.append('wrong target title rank')
    if (conditional.count('else_if = {') != 3 or
            re.findall(r'\badd\s*=\s*([\d.]+)', conditional) != ['0.4', '0.3', '0.2', '0.1', '0.2', '0.1']):
        errors.append('ranks stack or increments differ')
    if (len(searches) == 6 and
            ('exists = var:rw_dt_holder.primary_title' not in searches[4] or
             'var:rw_dt_title = { this = prev.var:rw_dt_holder.primary_title }' not in searches[4] or
             'count >= 2' not in searches[5])):
        errors.append('wrong primary or multiple-title signal')
    goal = block(values, GOAL)
    if (not goal.strip().startswith('value = 1') or
            'rw_ai_xw_claim_goal_context_trigger = yes' not in block(block(goal, 'if'), 'limit') or
            'multiply = '+FACTOR not in block(goal, 'if') or
            'min = 1' not in goal or 'max = 1.7' not in goal):
        errors.append('unguarded claim goal')
    concern = block(values, 'rw_ai_xw_concern_factor')
    if ('multiply = '+FACTOR not in block(concern, 'if') or
            FACTOR in block(concern, 'else')):
        errors.append('protector reader overwritten')
    for name, operation, target in (
            ('rw_ai_xm_accept_weight', 'multiply', FACTOR),
            ('rw_ai_xm_decline_weight', 'divide', FACTOR),
            ('rw_ai_xw_acknowledge_weight', 'divide', GOAL),
            ('rw_ai_xw_refuse_weight', 'multiply', GOAL)):
        if block(values, name).count(operation+' = '+target) != 1:
            errors.append('wrong external title direction '+name)
    if FACTOR in block(values, 'rw_ai_xm_existing_weight') or GOAL in block(values, 'rw_ai_xm_existing_weight'):
        errors.append('existing attempt becomes preference')
    if previous_profile_digest(values) != BASELINE_DIGEST:
        errors.append('prior external profile changed')
    executable = clean_script(factor+goal+context)[0]
    if re.search(r'\b(set_variable|change_variable|save_\w+|create_story|trigger_event|run_interaction|add_opinion|random\w*|every_\w+)\s*=', executable):
        errors.append('title policy writes or global work')
    if set(re.findall(r'\b(any_\w+)\s*=', executable)) - {'any_owned_story'}:
        errors.append('title policy writes or global work')
    if any(not name.startswith(('rw_xw_', 'rw_xm_')) for name in re.findall(r'\bscope:(\w+)', executable)):
        errors.append('foreign title frame')
    return errors


class ExternalTitleStakesTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.context = (builder.TEMPLATES/CONTEXT).read_text(encoding='utf-8-sig')

    def test_actual_policy_and_matching_delivery(self):
        self.assertEqual([], stakes_errors(self.values, self.context))
        self.assertIn(CONTEXT, builder.FILES)

    def test_own_turns_complete_capture_and_exact_parent(self):
        for token in CONTEXT_TOKENS:
            with self.subTest(guard=token):
                self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_actual_primary_defender_and_nested_holder_paths(self):
        for token in FACT_TOKENS:
            with self.subTest(guard=token):
                self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_claim_goal_requires_original_living_claimant_including_own(self):
        for token in CLAIMANT_TOKENS:
            self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))
        self.assertTrue(stakes_errors(self.values, self.context.replace('exists = var:rw_dl_claimant', 'NOT = { var:rw_dl_claimant = scope:rw_xw_attacker }')))

    def test_local_searches_ranks_primary_holder_and_multiple_targets(self):
        for old, new in ((FACT_GUARD, 'always = yes'), ('else_if = {', 'if = {'),
                         ('prev.var:rw_dt_holder.primary_title', 'scope:rw_xw_defender.primary_title'),
                         ('count >= 2', 'count >= 1')):
            self.assertTrue(stakes_errors(self.values.replace(old, new, 1), self.context))

    def test_bounds_neutrality_and_opposite_mediation_reply_directions(self):
        for name in (FACTOR, GOAL):
            body = block(self.values, name)
            self.assertTrue(stakes_errors(self.values.replace(body, body.replace('value = 1', 'value = 0', 1)), self.context))
        for name, operation, target in (('rw_ai_xm_decline_weight', 'divide', FACTOR),
                                        ('rw_ai_xw_acknowledge_weight', 'divide', GOAL)):
            body = block(self.values, name)
            changed = body.replace(operation+' = '+target, 'multiply = '+target)
            self.assertTrue(stakes_errors(self.values.replace(body, changed), self.context))

    def test_read_only_work_and_no_foreign_frame(self):
        self.assertTrue(stakes_errors(self.values, self.context+'\nbad = { set_variable = {} }'))
        body = block(self.values, FACTOR)
        self.assertTrue(stakes_errors(self.values.replace(body, body.replace('any_owned_story = {', 'any_living_character = {', 1)), self.context))
        self.assertTrue(stakes_errors(self.values, self.context.replace('scope:rw_xw_defender', 'scope:rw_uw_defender')))

    def test_preserve_prior_profile_old_inputs_and_both_event_action_graphs(self):
        self.assertEqual(BASELINE_DIGEST, previous_profile_digest(self.values))
        self.assertEqual(BASELINE_DIGEST, previous_profile_digest(strip_title_extension(self.values)))
        self.assertTrue(stakes_errors(self.values.replace('value = ai_honor', 'value = ai_greed'), self.context))
        for name, expected in ACTION_DIGESTS.items():
            self.assertEqual(expected, action_digest((builder.TEMPLATES/name).read_text(encoding='utf-8-sig')))
