"""Exact title facts and bounded protector preferences, without CK3 simulation."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_external_war_ai import VALUES, ACTION_DIGESTS
from test_promise_ai_policy import action_digest
from test_external_title_stakes import strip_title_extension

CONTEXT = 'common/scripted_triggers/rw_protected_title_stakes_triggers.txt'
FACTOR = 'rw_ai_xw_protected_title_factor'
FACT_GUARD = 'rw_ai_xw_protected_title_fact_trigger = yes'
BASELINE_DIGEST = '5add46b0fa9a17d35b34933cbee84471ed9cb025f2726026db71f6d83dcb2ce7'
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
FACT_TOKENS = (
    'story_type = story_rw_declaration_target', 'story_owner = scope:rw_xw_attacker',
    'var:rw_dt_schema = 1', 'exists = var:rw_dt_parent', 'has_variable = rw_dt_parent_serial',
    'exists = var:rw_dt_war', 'has_variable = rw_dt_seen_on',
    'var:rw_dt_parent = scope:rw_xw_record.var:rw_xw_source',
    'var:rw_dt_parent_serial = scope:rw_xw_record.var:rw_xw_source_serial',
    'var:rw_dt_war = scope:rw_xw_record.var:rw_xw_war',
    'var:rw_dt_seen_on = scope:rw_xw_record.var:rw_xw_source.var:rw_dl_seen_on',
    'var:rw_dt_holder_state = flag:known', 'exists = var:rw_dt_title',
    'exists = var:rw_dt_holder', 'exists = var:rw_dt_holder_liege',
    'exists = var:rw_dt_holder_authority', 'var:rw_dt_holder_liege = scope:rw_xw_ruler',
    'var:rw_dt_holder_authority = scope:rw_xw_record.var:rw_xw_authority',
    'var:rw_dt_holder = { is_alive = yes liege = scope:rw_xw_ruler }',
    'var:rw_dt_title = { holder = prev.var:rw_dt_holder }',
    'var:rw_dt_holder_authority = { holder = scope:rw_xw_ruler }',
)
CONTEXT_TOKENS = (
    'rw_xw_turn_trigger = yes', 'var:rw_xw_role = flag:target_liege',
    'exists = var:rw_xw_source', 'has_variable = rw_xw_source_serial', *PARENT_TOKENS,
)


def previous_profile_digest(values):
    clean = strip_title_extension(values)
    start, _, end = builder.bounds(clean, FACTOR)
    clean = clean[:start]+clean[end:]
    clean = re.sub(r'\bmultiply\s*=\s*'+FACTOR+r'\b', '', clean)
    return hashlib.sha256(' '.join(clean.split()).encode()).hexdigest()


def stakes_errors(values, context):
    errors = []
    guard = block(context, 'rw_ai_xw_title_context_trigger')
    if any(token not in guard for token in CONTEXT_TOKENS):
        errors.append('invalid protector context')
    if any(token not in block(guard, 'var:rw_xw_source') for token in PARENT_TOKENS):
        errors.append('incomplete original title capture')
    fact = block(context, 'rw_ai_xw_protected_title_fact_trigger')
    if any(token not in fact for token in FACT_TOKENS):
        errors.append('foreign or changed title fact')
    factor = block(values, FACTOR)
    conditional = block(factor, 'if')
    if (not factor.strip().startswith('value = 1') or
            'rw_ai_xw_title_context_trigger = yes' not in block(conditional, 'limit') or
            'min = 1' not in factor or 'max = 1.7' not in factor):
        errors.append('missing neutral bounded stakes')
    searches = [block(conditional[m.start():], 'any_owned_story')
                for m in re.finditer(r'\bany_owned_story\s*=', conditional)]
    if (len(searches) != 6 or any(FACT_GUARD not in search for search in searches) or
            conditional.count('scope:rw_xw_attacker = {') != 6):
        errors.append('unbound title search')
    for search, tier in zip(searches[:4], ('empire', 'kingdom', 'duchy', 'county')):
        if 'var:rw_dt_title = { tier >= tier_'+tier+' }' not in search:
            errors.append('wrong target title rank')
    if conditional.count('else_if = {') != 3:
        errors.append('title ranks can stack')
    if (len(searches) == 6 and
            ('exists = var:rw_dt_holder.primary_title' not in searches[4] or
             'var:rw_dt_title = { this = prev.var:rw_dt_holder.primary_title }' not in searches[4] or
             'count >= 2' not in searches[5])):
        errors.append('wrong primary or multiple-title signal')
    if re.findall(r'\badd\s*=\s*([\d.]+)', conditional) != ['0.4', '0.3', '0.2', '0.1', '0.2', '0.1']:
        errors.append('wrong stakes increments')
    concern = block(values, 'rw_ai_xw_concern_factor')
    if ('multiply = '+FACTOR not in block(concern, 'else') or
            values.count('multiply = '+FACTOR) != 1):
        errors.append('stakes escape protector concern')
    if previous_profile_digest(values) != BASELINE_DIGEST:
        errors.append('prior numeric profile changed')
    executable = clean_script(factor+context)[0]
    if re.search(r'\b(set_variable|change_variable|save_\w+|create_story|trigger_event|run_interaction|add_opinion|random\w*|every_\w+)\s*=', executable):
        errors.append('stakes write or global work')
    if set(re.findall(r'\b(any_\w+)\s*=', executable)) - {'any_owned_story'}:
        errors.append('stakes write or global work')
    if set(re.findall(r'\bscope:(\w+)', executable)) - {'rw_xw_attacker', 'rw_xw_defender', 'rw_xw_record', 'rw_xw_ruler'}:
        errors.append('foreign stakes frame')
    return errors


class ProtectedTitleStakesTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.context = (builder.TEMPLATES/CONTEXT).read_text(encoding='utf-8-sig')

    def test_actual_policy_and_matching_delivery(self):
        self.assertEqual([], stakes_errors(self.values, self.context))
        self.assertIn(CONTEXT, builder.FILES)

    def test_stale_foreign_legacy_and_partial_parent_guards(self):
        for token in CONTEXT_TOKENS:
            with self.subTest(guard=token):
                self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_each_target_retains_its_actual_owner_war_holder_and_protector(self):
        for token in FACT_TOKENS:
            with self.subTest(guard=token):
                self.assertTrue(stakes_errors(self.values, self.context.replace(token, 'always = yes')))

    def test_all_searches_are_guarded_and_ranks_do_not_stack(self):
        self.assertTrue(stakes_errors(self.values.replace(FACT_GUARD, 'always = yes', 1), self.context))
        self.assertTrue(stakes_errors(self.values.replace('else_if = {', 'if = {', 1), self.context))
        self.assertTrue(stakes_errors(self.values.replace('tier >= tier_duchy', 'tier >= tier_county'), self.context))

    def test_primary_title_belongs_to_actual_holder_and_multi_signal_needs_two(self):
        for old, new in (('prev.var:rw_dt_holder.primary_title', 'scope:rw_xw_defender.primary_title'),
                         ('count >= 2', 'count >= 1')):
            self.assertTrue(stakes_errors(self.values.replace(old, new), self.context))

    def test_neutral_bounds_and_existing_profile_are_preserved(self):
        for token in ('value = 1', 'rw_ai_xw_title_context_trigger = yes', 'max = 1.7'):
            factor = block(self.values, FACTOR)
            self.assertTrue(stakes_errors(self.values.replace(factor, factor.replace(token, 'always = yes', 1)), self.context))
        self.assertEqual(BASELINE_DIGEST, previous_profile_digest(self.values))
        self.assertTrue(stakes_errors(self.values.replace('value = ai_honor', 'value = ai_greed'), self.context))

    def test_read_only_local_work_and_no_weight_outside_protector_concern(self):
        self.assertTrue(stakes_errors(self.values, self.context+'\nbad = { set_variable = {} }'))
        self.assertTrue(stakes_errors(self.values.replace('any_owned_story = {', 'any_living_character = {', 1), self.context))
        changed = self.values.replace('multiply = '+FACTOR, 'divide = '+FACTOR)
        self.assertTrue(stakes_errors(changed, self.context))

    def test_both_event_action_graphs_are_preserved(self):
        for name, expected in ACTION_DIGESTS.items():
            self.assertEqual(expected, action_digest((builder.TEMPLATES/name).read_text(encoding='utf-8-sig')))
