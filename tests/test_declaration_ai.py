"""Native boolean preference contracts, not AI wars or a CK3 score simulator."""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_peer_war_ai import GUARD_FILE, GUARD_DIGEST, guard_digest

VALUES = 'common/script_values/rw_declaration_ai_values.txt'
CONTEXT = 'common/scripted_triggers/rw_declaration_ai_triggers.txt'
SHARED = 'common/script_values/rw_external_war_ai_values.txt'


def declaration_policy_errors(values, context, choices, shared):
    errors = []

    def need(text, tokens, label):
        if any(token not in text for token in tokens):
            errors.append(label)

    need(block(context, 'rw_ai_wd_context_trigger'),
         ('exists = scope:actor', 'exists = scope:recipient', 'this = scope:actor',
          'rw_uw_applicable_ban_trigger = yes', 'NOT = { always = scope:hook }'), 'invalid declaration frame')
    preference = block(choices, 'rw_uw_ai_default_defiance_trigger')
    need(preference, ('rw_uw_applicable_ban_trigger = yes', 'NOT = { always = scope:hook }',
                      'is_ai = yes', 'rw_ai_wd_motivation_value >= rw_ai_wd_caution_value'),
         'shared gate or AI comparison missing')
    actor = block(preference, 'scope:actor')
    need(actor, ('is_ai = yes', 'rw_ai_wd_motivation_value >= rw_ai_wd_caution_value'), 'wrong preference decider')
    motivation = block(values, 'rw_ai_wd_motivation_value')
    conditional = block(motivation, 'if')
    need(conditional, ('rw_ai_wd_context_trigger = yes', 'add = 50',
                       'add = rw_ai_wd_boldness_value', 'subtract = rw_ai_wd_honor_value',
                       'add = rw_ai_wd_energy_value', 'subtract = rw_ai_wd_compassion_value',
                       'target = scope:actor.liege value <= -25',
                       'target = scope:actor.liege value >= 25',
                       'target = scope:recipient value <= -25', 'add = rw_ai_wd_grievance_value',
                       'min = 0', 'max = 100'), 'motivation context missing')
    if not motivation.strip().startswith('value = 0'):
        errors.append('unknown context gains motivation')
    burden = block(values, 'rw_ai_wd_burden_value')
    need(burden, ('rw_ai_wd_context_trigger = yes', 'gold < 0', 'gold < 50', 'gold < 150',
                  'else_if =', 'is_at_war = yes', 'rw_ai_existing_commitment_trigger = yes',
                  'stress_level >= 2', 'health < 3'), 'own burden missing')
    caution = block(values, 'rw_ai_wd_caution_value')
    if not caution.strip().startswith('value = 1000'):
        errors.append('unknown context has reachable threshold')
    need(block(caution, 'if'), ('rw_ai_wd_context_trigger = yes', 'subtract = 1000', 'add = 60',
                               'add = rw_ai_wd_practical_risk_value',
                               'has_realm_law_flag = vassal_all_wars_banned',
                               'has_dread_level_towards = { target = scope:actor.liege level = 2 }',
                               'has_dread_level_towards = { target = scope:actor.liege level = 1 }',
                               'is_close_family_of = scope:actor.liege', 'is_allied_to = scope:actor.liege',
                               'is_close_family_of = scope:recipient', 'is_allied_to = scope:recipient',
                               'has_usable_hook = scope:actor.liege'), 'political caution missing')
    for name, factor, scale in (('boldness', 'resolve', 50), ('honor', 'honor', 40),
                                ('energy', 'initiative', 20), ('compassion', 'compassion', 20),
                                ('grievance', 'grievance', 20)):
        need(block(values, 'rw_ai_wd_'+name+'_value'),
             ('value = rw_ai_xw_'+factor+'_factor', 'subtract = 1', 'multiply = '+str(scale)),
             'wrong own personality component '+name)
        if 'scope:' in block(shared, 'rw_ai_xw_'+factor+'_factor'):
            errors.append('shared axis reads foreign frame')
    need(block(values, 'rw_ai_wd_practical_risk_value'),
         ('value = rw_ai_wd_burden_value', 'multiply = rw_ai_xw_rationality_factor'), 'risk rationality missing')
    if guard_digest(choices) != GUARD_DIGEST:
        errors.append('nonpreference guard changed')
    executable = clean_script(values+context+preference)[0]
    if re.search(r'\b(set_variable|change_variable|create_story|trigger_event|run_interaction|start_war|end_war|add_gold|use_hook|save_scope_as|save_temporary_scope_as|save_scope_value_as|random|random_list|chance|every_\w+|any_\w+)\s*=', executable):
        errors.append('preference writes rolls or scans')
    if any(name not in ('actor', 'recipient', 'hook') for name in re.findall(r'\bscope:(\w+)', executable)):
        errors.append('inferred native candidate identity')
    definitions = set(re.findall(r'^\s*(rw_\w+)\s*=\s*\{', clean_script(values+shared)[0], re.MULTILINE))
    refs = set(re.findall(r'\b(?:value|add|subtract|multiply|divide)\s*=\s*(rw_\w+)', clean_script(values)[0]))
    if refs - definitions:
        errors.append('unresolved score component')
    return errors


class DeclarationAiTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')
        self.context = (builder.TEMPLATES/CONTEXT).read_text(encoding='utf-8-sig')
        self.choices = (builder.TEMPLATES/GUARD_FILE).read_text(encoding='utf-8-sig')
        self.shared = (builder.TEMPLATES/SHARED).read_text(encoding='utf-8-sig')

    def test_actual_policy_and_unchanged_native_option(self):
        self.assertEqual([], declaration_policy_errors(self.values, self.context, self.choices, self.shared))
        self.assertEqual(1, builder.OPTION.count('starts_enabled = { rw_uw_ai_default_defiance_trigger = yes }'))
        for name in (VALUES, CONTEXT, SHARED): self.assertIn(name, builder.FILES)

    def test_foreign_missing_or_hook_selected_frame_is_detected(self):
        for token in ('this = scope:actor', 'exists = scope:recipient', 'rw_uw_applicable_ban_trigger = yes',
                      'NOT = { always = scope:hook }'):
            with self.subTest(guard=token):
                changed = self.context.replace(token, 'always = yes')
                self.assertIn('invalid declaration frame', declaration_policy_errors(
                    self.values, changed, self.choices, self.shared))

    def test_unknown_candidate_cannot_receive_a_true_default(self):
        for before, after, error in (('value = 1000', 'value = 0', 'unknown context has reachable threshold'),
                                     ('rw_ai_wd_motivation_value = {\n    value = 0',
                                      'rw_ai_wd_motivation_value = {\n    value = 50', 'unknown context gains motivation')):
            with self.subTest(guard=before):
                self.assertIn(error, declaration_policy_errors(self.values.replace(before, after), self.context, self.choices, self.shared))

    def test_both_shared_permission_and_actor_ai_comparison_are_required(self):
        for token in ('is_ai = yes', 'rw_ai_wd_motivation_value >= rw_ai_wd_caution_value'):
            with self.subTest(guard=token):
                self.assertIn('shared gate or AI comparison missing', declaration_policy_errors(
                    self.values, self.context, self.choices.replace(token, 'always = yes'), self.shared))

    def test_personality_directions_and_rational_risk_are_preserved(self):
        for token in ('subtract = rw_ai_wd_honor_value', 'add = rw_ai_wd_boldness_value',
                      'subtract = rw_ai_wd_compassion_value', 'multiply = rw_ai_xw_rationality_factor'):
            with self.subTest(component=token):
                self.assertTrue(declaration_policy_errors(self.values.replace(token, 'add = 0'), self.context, self.choices, self.shared))

    def test_resources_fear_known_relations_and_hook_alternative_are_present(self):
        for token in ('gold < 0', 'is_at_war = yes', 'health < 3', 'stress_level >= 2',
                      'has_usable_hook = scope:actor.liege',
                      'has_dread_level_towards = { target = scope:actor.liege level = 2 }'):
            with self.subTest(input=token):
                self.assertTrue(declaration_policy_errors(self.values.replace(token, 'always = yes'), self.context, self.choices, self.shared))

    def test_preference_is_deterministic_read_only_and_does_not_invent_cb_parties(self):
        for operation in ('random_list = {}', 'set_variable = {}', 'start_war = {}', 'any_character = {}'):
            with self.subTest(operation=operation):
                self.assertIn('preference writes rolls or scans', declaration_policy_errors(
                    self.values+'\nbad = { '+operation+' }', self.context, self.choices, self.shared))
        changed = self.values.replace('scope:recipient', 'scope:claimant')
        self.assertIn('inferred native candidate identity', declaration_policy_errors(changed, self.context, self.choices, self.shared))

    def test_nonpreference_war_and_permission_guards_cannot_change(self):
        changed = self.choices.replace('war_declarer_needs_hook_on_liege = yes', 'always = yes')
        self.assertIn('nonpreference guard changed', declaration_policy_errors(
            self.values, self.context, changed, self.shared))
