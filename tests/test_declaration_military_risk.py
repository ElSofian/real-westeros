"""Guarded numeric inputs and source invariants, without simulating CK3."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_declaration_ai import VALUES

RISK = 'rw_ai_wd_military_risk_value'
COMPONENTS = (
    ('rw_ai_wd_target_force_risk_value', 'scope:recipient.current_military_strength',
     'scope:recipient.current_military_strength',
     'scope:recipient = { current_military_strength > 0 }', 20),
    ('rw_ai_wd_liege_force_risk_value', 'scope:actor.liege.current_military_strength',
     'scope:actor.liege.current_military_strength',
     'scope:actor.liege = { current_military_strength > 0 }', 15),
    ('rw_ai_wd_depletion_risk_value', 'scope:actor.max_military_strength',
     'max_military_strength', 'max_military_strength > 0', 10),
)
BASELINE_DIGEST = '97a183cca6ee847df9294c5981a4ba3ba98c758b0af40eb02419376d91aeacde'


def previous_profile_digest(values):
    clean = clean_script(values)[0]
    for name in (*(component[0] for component in COMPONENTS), RISK):
        start, _, end = builder.bounds(clean, name)
        clean = clean[:start]+clean[end:]
    clean = re.sub(r'\badd\s*=\s*'+RISK+r'\b', '', clean)
    return hashlib.sha256(' '.join(clean.split()).encode()).hexdigest()


def military_errors(values):
    errors = []
    for name, counterpart, denominator, positive, scale in COMPONENTS:
        body = block(values, name)
        outer = block(body, 'if')
        if (not body.strip().startswith('value = 0') or
                ' '.join(block(outer, 'limit').split()) != 'rw_ai_wd_context_trigger = yes'):
            errors.append('unguarded candidate '+name)
        numeric = block(outer, 'if')
        limit = block(numeric, 'limit')
        if any(token not in limit for token in ('current_military_strength >= 0',
                                                'current_military_strength < '+counterpart, positive)):
            errors.append('invalid zero or negative denominator '+name)
        expected = 'value = current_military_strength divide = '+denominator
        if (' '.join(block(numeric, 'subtract').split()) != expected or
                'add = 1' not in numeric or 'multiply = '+str(scale) not in numeric):
            errors.append('wrong deficit direction '+name)
        if 'min = 0' not in body or 'max = '+str(scale) not in body:
            errors.append('unbounded deficit '+name)
    aggregate = block(values, RISK)
    conditional = block(aggregate, 'if')
    if (not aggregate.strip().startswith('value = 0') or
            ' '.join(block(conditional, 'limit').split()) != 'rw_ai_wd_context_trigger = yes' or
            any(conditional.count('add = '+component[0]) != 1 for component in COMPONENTS) or
            'multiply = rw_ai_xw_rationality_factor' not in conditional or
            'min = 0' not in aggregate or 'max = 67.5' not in aggregate):
        errors.append('wrong bounded own rationality aggregate')
    caution = block(values, 'rw_ai_wd_caution_value')
    if ('add = '+RISK not in block(caution, 'if') or
            values.count('add = '+RISK) != 1):
        errors.append('military risk not confined to caution')
    if previous_profile_digest(values) != BASELINE_DIGEST:
        errors.append('prior declaration profile changed')
    executable = clean_script(values)[0]
    if re.search(r'\b(set_variable|change_variable|create_story|trigger_event|run_interaction|start_war|end_war|add_gold|use_hook|save_\w+|random\w*|every_\w+|any_\w+)\s*=', executable):
        errors.append('military policy writes rolls or scans')
    if set(re.findall(r'\bscope:(\w+)', executable)) - {'actor', 'recipient'}:
        errors.append('foreign military frame')
    return errors


class DeclarationMilitaryRiskTests(unittest.TestCase):
    def setUp(self):
        self.values = (builder.TEMPLATES/VALUES).read_text(encoding='utf-8-sig')

    def test_actual_policy_and_existing_attested_delivery(self):
        self.assertEqual([], military_errors(self.values))
        self.assertIn(VALUES, builder.FILES)

    def test_invalid_candidate_is_rejected_before_metric_access(self):
        for name, *_ in COMPONENTS:
            body = block(self.values, name)
            changed = body.replace('rw_ai_wd_context_trigger = yes', 'always = yes')
            self.assertIn('unguarded candidate '+name, military_errors(self.values.replace(body, changed)))

    def test_zero_negative_and_equal_strength_guards_are_required(self):
        for name, counterpart, _, positive, _ in COMPONENTS:
            for token in ('current_military_strength >= 0',
                          'current_military_strength < '+counterpart, positive):
                with self.subTest(component=name, guard=token):
                    body = block(self.values, name)
                    changed = body.replace(token, 'always = yes')
                    self.assertIn('invalid zero or negative denominator '+name,
                                  military_errors(self.values.replace(body, changed)))

    def test_target_liege_and_own_maximum_are_distinct_denominators(self):
        for name, _, denominator, _, _ in COMPONENTS:
            body = block(self.values, name)
            changed = body.replace('divide = '+denominator, 'divide = current_military_strength')
            self.assertIn('wrong deficit direction '+name, military_errors(self.values.replace(body, changed)))

    def test_neutral_defaults_nonnegative_bounds_and_direction(self):
        for name, *_ in COMPONENTS:
            body = block(self.values, name)
            for old, new in (('value = 0', 'value = 1'), ('min = 0', 'min = -10'),
                             ('subtract = {', 'add = {')):
                self.assertTrue(military_errors(self.values.replace(body, body.replace(old, new, 1))))

    def test_rationality_and_caution_only_wiring(self):
        body = block(self.values, RISK)
        for token in ('rw_ai_wd_context_trigger = yes', 'multiply = rw_ai_xw_rationality_factor', 'max = 67.5'):
            self.assertTrue(military_errors(self.values.replace(body, body.replace(token, 'add = 0'))))
        self.assertIn('military risk not confined to caution',
                      military_errors(self.values.replace('add = '+RISK, 'subtract = '+RISK)))

    def test_no_assumed_allied_armies_writes_or_foreign_scopes(self):
        self.assertTrue(military_errors(self.values+'\nbad = { every_ally = {} }'))
        self.assertTrue(military_errors(self.values+'\nbad = { start_war = {} }'))
        self.assertIn('foreign military frame', military_errors(self.values.replace('scope:recipient', 'scope:claimant')))

    def test_entire_previous_declaration_profile_is_preserved(self):
        self.assertEqual(BASELINE_DIGEST, previous_profile_digest(self.values))
        self.assertIn('prior declaration profile changed', military_errors(self.values.replace('add = 60', 'add = 6')))
