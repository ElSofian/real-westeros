"""Own-army observation anchors and source contracts, without CK3 simulation."""
import hashlib
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_deferred_service_contract import block
from test_peer_war_ai import VALUES as PEER, EVENT, ACTION_DIGEST
from test_external_war_ai import VALUES as EXTERNAL, ACTION_DIGESTS
from test_promise_ai_policy import action_digest

CASES = (
    {'family': 'uw', 'values': PEER, 'war': 'scope:rw_uw_war',
     'baseline': '087f07abdd5b39165c32fc91d7fda11d311d0a99c52d2bf90f5741423496bca7'},
    {'family': 'xw', 'values': EXTERNAL, 'war': 'scope:rw_xw_record.var:rw_xw_war',
     'baseline': '2173a5460b61d179940cf84cc6e967fbdbf88287730eac39d03a3df90b7fda52'},
)


def strip_observed_extension(values):
    clean = clean_script(values)[0]
    for case in CASES:
        name = 'rw_ai_'+case['family']+'_observed_reinforcement_factor'
        if re.search(r'^\s*'+name+r'\s*=\s*\{', clean, re.MULTILINE):
            start, _, end = builder.bounds(clean, name)
            clean = clean[:start]+clean[end:]
            clean = re.sub(r'\b(?:multiply|divide)\s*=\s*'+name+r'\b', '', clean)
    return clean


def previous_profile_digest(values):
    return hashlib.sha256(' '.join(strip_observed_extension(values).split()).encode()).hexdigest()


def observation_errors(sources):
    errors = []
    for case in CASES:
        family = case['family']
        actor = 'scope:rw_'+family+'_attacker'
        name = 'rw_ai_'+family+'_observed_reinforcement_factor'
        values = sources[case['values']]
        factor = block(values, name)
        outer = block(factor, 'if')
        if (not factor.strip().startswith('value = 1') or
                ' '.join(block(outer, 'limit').split()) != 'rw_'+family+'_answer_turn_trigger = yes' or
                'min = 1' not in factor or 'max = 1.1' not in factor):
            errors.append('invalid neutral observation frame '+family)
        condition = block(block(outer, 'if'), 'limit')
        unique = block(condition, actor)
        expected = 'NOT = { any_character_war = { NOT = { this = '+case['war']+' } } }'
        if ' '.join(unique.split()) != expected:
            errors.append('ambiguous army conflict '+family)
        war = block(condition, case['war'])
        supporter = block(war, 'any_war_attacker')
        if any(token not in supporter for token in ('is_alive = yes', 'NOT = { this = '+actor+' }')):
            errors.append('wrong secondary participant '+family)
        army = block(supporter, 'any_army')
        supporter_header = army.split('location = {', 1)[0]
        if any(token not in supporter_header for token in ('army_owner = prev', 'army_size > 0',
                                               'NOT = { is_raid_army = yes }', 'exists = location')):
            errors.append('unbound supporter army '+family)
        location = block(army, 'location')
        own = block(location, 'any_army_in_location')
        if any(token not in own for token in ('army_owner = '+actor, 'army_size > 0',
                                              'NOT = { is_raid_army = yes }')):
            errors.append('missing own army observation anchor '+family)
        if 'multiply = 1.1' not in block(outer, 'if'):
            errors.append('missing bounded observed signal '+family)
        for suffix, operation in (('acknowledge_weight', 'divide'), ('refuse_weight', 'multiply')):
            if block(values, 'rw_ai_'+family+'_'+suffix).count(operation+' = '+name) != 1:
                errors.append('wrong observed reply direction '+family)
        if values.count('multiply = '+name) != 1 or values.count('divide = '+name) != 1:
            errors.append('observation escapes own reply '+family)
        if previous_profile_digest(values) != case['baseline']:
            errors.append('prior profile changed '+family)
        executable = clean_script(factor)[0]
        if re.search(r'\b(set_variable|change_variable|create_story|trigger_event|run_interaction|start_war|add_gold|save_\w+|random\w*|every_\w+)\s*=', executable):
            errors.append('observation writes or global work '+family)
        allowed = {'any_character_war', 'any_war_attacker', 'any_army', 'any_army_in_location'}
        if set(re.findall(r'\b(any_\w+)\s*=', executable)) - allowed:
            errors.append('unrelated or enemy observation '+family)
        if any(not scope.startswith('rw_'+family+'_') for scope in re.findall(r'\bscope:(\w+)', executable)):
            errors.append('foreign observation frame '+family)
    return errors


class ObservedReinforcementTests(unittest.TestCase):
    def setUp(self):
        self.sources = {case['values']: (builder.TEMPLATES/case['values']).read_text(encoding='utf-8-sig')
                        for case in CASES}

    def test_both_actual_policies_and_attested_delivery(self):
        self.assertEqual([], observation_errors(self.sources))
        for case in CASES:
            self.assertIn(case['values'], builder.FILES)

    def test_own_turn_and_single_exact_war_are_required(self):
        for case in CASES:
            family = case['family']
            for token in ('rw_'+family+'_answer_turn_trigger = yes', 'NOT = { this = '+case['war']+' }'):
                changed = dict(self.sources)
                values = changed[case['values']]
                factor = block(values, 'rw_ai_'+family+'_observed_reinforcement_factor')
                changed[case['values']] = values.replace(factor, factor.replace(token, 'always = yes', 1))
                self.assertTrue(observation_errors(changed))

    def test_dead_primary_and_foreign_participants_are_rejected(self):
        for case in CASES:
            values = self.sources[case['values']]
            factor = block(values, 'rw_ai_'+case['family']+'_observed_reinforcement_factor')
            for token in ('is_alive = yes', 'NOT = { this = scope:rw_'+case['family']+'_attacker }'):
                changed = dict(self.sources)
                changed[case['values']] = values.replace(factor, factor.replace(token, 'always = yes', 1))
                self.assertTrue(observation_errors(changed))
            changed = dict(self.sources)
            changed[case['values']] = values.replace(factor, factor.replace('any_war_attacker', 'any_ally'))
            self.assertTrue(observation_errors(changed))

    def test_supporter_army_needs_exact_owner_positive_size_and_location(self):
        for case in CASES:
            values = self.sources[case['values']]
            factor = block(values, 'rw_ai_'+case['family']+'_observed_reinforcement_factor')
            for token in ('army_owner = prev', 'army_size > 0', 'NOT = { is_raid_army = yes }', 'exists = location'):
                changed = dict(self.sources)
                changed[case['values']] = values.replace(factor, factor.replace(token, 'always = yes', 1))
                self.assertTrue(observation_errors(changed))

    def test_same_province_needs_own_positive_nonraiding_army(self):
        for case in CASES:
            values = self.sources[case['values']]
            factor = block(values, 'rw_ai_'+case['family']+'_observed_reinforcement_factor')
            own = block(factor, 'any_army_in_location')
            for token in ('army_owner = scope:rw_'+case['family']+'_attacker', 'army_size > 0', 'NOT = { is_raid_army = yes }'):
                changed = dict(self.sources)
                replacement = factor.replace(own, own.replace(token, 'always = yes', 1), 1)
                changed[case['values']] = values.replace(factor, replacement, 1)
                self.assertTrue(observation_errors(changed))

    def test_neutral_bounds_and_opposite_reply_directions(self):
        for case in CASES:
            values = self.sources[case['values']]
            name = 'rw_ai_'+case['family']+'_observed_reinforcement_factor'
            factor = block(values, name)
            for token in ('value = 1', 'min = 1', 'max = 1.1'):
                changed = dict(self.sources)
                changed[case['values']] = values.replace(factor, factor.replace(token, 'always = yes', 1))
                self.assertTrue(observation_errors(changed))
            changed = dict(self.sources)
            changed[case['values']] = values.replace('divide = '+name, 'multiply = '+name)
            self.assertTrue(observation_errors(changed))

    def test_enemy_or_foreign_scopes_and_writes_are_rejected(self):
        for case in CASES:
            values = self.sources[case['values']]
            factor = block(values, 'rw_ai_'+case['family']+'_observed_reinforcement_factor')
            for old, new in (('any_war_attacker', 'any_war_defender'),
                             ('multiply = 1.1', 'set_variable = {}'),
                             (case['war'], 'scope:foreign_war')):
                changed = dict(self.sources)
                changed[case['values']] = values.replace(factor, factor.replace(old, new, 1))
                self.assertTrue(observation_errors(changed))

    def test_prior_profiles_legacy_inputs_and_action_graphs_are_preserved(self):
        for case in CASES:
            self.assertEqual(case['baseline'], previous_profile_digest(self.sources[case['values']]))
            self.assertEqual(case['baseline'], previous_profile_digest(strip_observed_extension(self.sources[case['values']])))
        for name, expected in {EVENT: ACTION_DIGEST, **ACTION_DIGESTS}.items():
            self.assertEqual(expected, action_digest((builder.TEMPLATES/name).read_text(encoding='utf-8-sig')))
