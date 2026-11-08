"""Exact native participation as a bounded signal, without CK3 simulation."""
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
     'baseline': '15a1f2c5311e72d17d520da65a6b9d4b5f82574dff6c1795862f3239556fdc1a'},
    {'family': 'xw', 'values': EXTERNAL, 'war': 'scope:rw_xw_record.var:rw_xw_war',
     'baseline': '70e8abd1f23da0ad4fe4c15658075c614e404208455c47520a8ce61070cfe7ba'},
)


def strip_support_extension(values):
    """Share the exact removal with older independent profile invariants."""
    clean = clean_script(values)[0]
    for case in CASES:
        name = 'rw_ai_'+case['family']+'_committed_support_factor'
        if re.search(r'^\s*'+name+r'\s*=\s*\{', clean, re.MULTILINE):
            start, _, end = builder.bounds(clean, name)
            clean = clean[:start]+clean[end:]
            clean = re.sub(r'\b(?:multiply|divide)\s*=\s*'+name+r'\b', '', clean)
    return clean


def previous_profile_digest(values):
    return hashlib.sha256(' '.join(strip_support_extension(values).split()).encode()).hexdigest()


def support_errors(sources):
    errors = []
    for case in CASES:
        family = case['family']
        name = 'rw_ai_'+family+'_committed_support_factor'
        values = sources[case['values']]
        factor = block(values, name)
        conditional = block(factor, 'if')
        if (not factor.strip().startswith('value = 1') or
                ' '.join(block(conditional, 'limit').split()) != 'rw_'+family+'_answer_turn_trigger = yes' or
                'min = 0.8' not in factor or 'max = 1.25' not in factor):
            errors.append('invalid neutral support frame '+family)
        for side in ('attacker', 'defender'):
            marker = 'any_war_'+side
            iterator = block(conditional, marker)
            if any(token not in iterator for token in (
                    'is_alive = yes', 'NOT = { this = scope:rw_'+family+'_'+side+' }',
                    'current_military_strength > 0')):
                errors.append('unbound secondary '+side+' '+family)
            if conditional.count(marker+' = {') != 1:
                errors.append('repeated side query '+family)
        # Each camp must be queried from this family's exact original native war.
        war_blocks = [block(conditional[m.start():], case['war'])
                      for m in re.finditer(re.escape(case['war'])+r'\s*=\s*\{', conditional)]
        if (len(war_blocks) != 2 or 'any_war_attacker = {' not in war_blocks[0] or
                'any_war_defender = {' not in war_blocks[1]):
            errors.append('wrong support war '+family)
        branches = [block(conditional[m.start():], 'if')
                    for m in re.finditer(r'\bif\s*=\s*\{', conditional)]
        if (len(branches) != 2 or 'any_war_attacker = {' not in branches[0] or
                'multiply = 1.25' not in branches[0] or
                'any_war_defender = {' not in branches[1] or 'divide = 1.25' not in branches[1]):
            errors.append('support camps reverse confidence '+family)
        if (conditional.count('multiply = 1.25') != 1 or conditional.count('divide = 1.25') != 1):
            errors.append('wrong symmetric support increments '+family)
        for suffix, operation in (('acknowledge_weight', 'divide'), ('refuse_weight', 'multiply')):
            if block(values, 'rw_ai_'+family+'_'+suffix).count(operation+' = '+name) != 1:
                errors.append('wrong support reply direction '+family)
        if values.count('multiply = '+name) != 1 or values.count('divide = '+name) != 1:
            errors.append('support escapes attacker reply '+family)
        if previous_profile_digest(values) != case['baseline']:
            errors.append('prior numeric profile changed '+family)
        executable = clean_script(factor)[0]
        if re.search(r'\b(set_variable|change_variable|create_story|trigger_event|run_interaction|start_war|add_gold|save_\w+|random\w*|every_\w+)\s*=', executable):
            errors.append('support writes or global work '+family)
        if set(re.findall(r'\b(any_\w+)\s*=', executable)) - {'any_war_attacker', 'any_war_defender'}:
            errors.append('potential or unrelated support counted '+family)
        if any(not scope.startswith('rw_'+family+'_') for scope in re.findall(r'\bscope:(\w+)', executable)):
            errors.append('foreign support frame '+family)
    return errors


class CommittedWarSupportTests(unittest.TestCase):
    def setUp(self):
        self.sources = {case['values']: (builder.TEMPLATES/case['values']).read_text(encoding='utf-8-sig')
                        for case in CASES}

    def test_both_actual_policies_and_existing_attested_delivery(self):
        self.assertEqual([], support_errors(self.sources))
        for case in CASES:
            self.assertIn(case['values'], builder.FILES)

    def test_missing_stale_wrong_turn_frame_stays_neutral(self):
        for case in CASES:
            changed = dict(self.sources)
            changed[case['values']] = changed[case['values']].replace('rw_'+case['family']+'_answer_turn_trigger = yes', 'always = yes')
            self.assertTrue(support_errors(changed))

    def test_dead_empty_and_primary_participants_cannot_supply_this_signal(self):
        for case in CASES:
            family = case['family']
            body = block(self.sources[case['values']], 'rw_ai_'+family+'_committed_support_factor')
            for token in ('is_alive = yes', 'current_military_strength > 0',
                          'NOT = { this = scope:rw_'+family+'_attacker }',
                          'NOT = { this = scope:rw_'+family+'_defender }'):
                with self.subTest(family=family, guard=token):
                    changed = dict(self.sources)
                    changed[case['values']] = changed[case['values']].replace(body, body.replace(token, 'always = yes', 1))
                    self.assertTrue(support_errors(changed))

    def test_both_camps_use_the_exact_same_war(self):
        for case in CASES:
            changed = dict(self.sources)
            body = block(changed[case['values']], 'rw_ai_'+case['family']+'_committed_support_factor')
            changed[case['values']] = changed[case['values']].replace(body, body.replace(case['war'], 'scope:foreign_war', 1))
            self.assertTrue(support_errors(changed))

    def test_neutral_default_symmetric_factors_and_opposed_reply_directions(self):
        for case in CASES:
            name = 'rw_ai_'+case['family']+'_committed_support_factor'
            body = block(self.sources[case['values']], name)
            for old, new in (('value = 1', 'value = 0'), ('divide = 1.25', 'multiply = 1.25'), ('min = 0.8', 'min = 0')):
                changed = dict(self.sources)
                changed[case['values']] = changed[case['values']].replace(body, body.replace(old, new, 1))
                self.assertTrue(support_errors(changed))
            changed = dict(self.sources)
            changed[case['values']] = changed[case['values']].replace('divide = '+name, 'multiply = '+name)
            self.assertTrue(support_errors(changed))

    def test_potential_allies_and_global_scans_are_rejected(self):
        for case in CASES:
            changed = dict(self.sources)
            body = block(changed[case['values']], 'rw_ai_'+case['family']+'_committed_support_factor')
            changed[case['values']] = changed[case['values']].replace(body, body.replace('any_war_attacker = {', 'any_ally = {'))
            self.assertTrue(support_errors(changed))

    def test_support_reads_cannot_change_state(self):
        for case in CASES:
            changed = dict(self.sources)
            body = block(changed[case['values']], 'rw_ai_'+case['family']+'_committed_support_factor')
            changed[case['values']] = changed[case['values']].replace(body, body+'\nset_variable = {}')
            self.assertTrue(support_errors(changed))

    def test_entire_prior_profiles_legacy_inputs_and_action_graphs_preserved(self):
        for case in CASES:
            self.assertEqual(case['baseline'], previous_profile_digest(self.sources[case['values']]))
            self.assertEqual(case['baseline'], previous_profile_digest(strip_support_extension(self.sources[case['values']])))
        for name, expected in {EVENT: ACTION_DIGEST, **ACTION_DIGESTS}.items():
            self.assertEqual(expected, action_digest((builder.TEMPLATES/name).read_text(encoding='utf-8-sig')))
