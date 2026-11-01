"""Source contracts for voluntary responses to role observations; no engine run."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT/'mod/real_westeros'


def response_errors(t, e, mr):
    errors = []
    def need(body, fragments, message):
        if any(x not in body for x in fragments): errors.append(message)
    need(block(t, 'rw_mb_view_trigger'), ('rw_mr_view_trigger = yes',
        'var:rw_mr_state = flag:war_observed', 'var:rw_mb_schema = 1', 'var:rw_mb_serial = scope:rw_mr_serial',
        'has_variable = rw_mb_observed_on', 'var:rw_mb_observed_on = var:rw_mr_observed_on',
        'OR = { var:rw_mb_statement = flag:unanswered var:rw_mb_statement = flag:acknowledged var:rw_mb_statement = flag:contested }',
        'has_variable = rw_mb_requested_on', 'has_variable = rw_mb_answered_on', 'has_variable = rw_mb_reacted_on'),
        'foreign incomplete or old observation response')
    need(block(t, 'rw_mb_live_trigger'), ('rw_mb_view_trigger = yes',
        'scope:rw_mr_provider = { is_alive = yes }', 'scope:rw_mr_beneficiary = { is_alive = yes }',
        'var:rw_mb_state = flag:pending', 'has_variable = rw_mb_window'), 'expired terminal or dead-party action')
    need(block(t, 'rw_mb_can_react_trigger'), ('rw_mb_live_trigger = yes', 'this = scope:rw_mr_beneficiary'),
        'wrong personal reactor')
    need(block(t, 'rw_mb_can_request_trigger'), ('rw_mb_can_react_trigger = yes',
        'NOT = { has_variable = rw_mb_requested_on }', 'var:rw_mb_statement = flag:unanswered'), 'repeated or wrong request')
    need(block(t, 'rw_mb_can_answer_trigger'), ('rw_mb_live_trigger = yes', 'this = scope:rw_mr_provider',
        'has_variable = rw_mb_requested_on', 'var:rw_mb_statement = flag:unanswered'), 'unsolicited replayed or wrong reply')
    begin = block(e, 'rw_mb_begin_effect')
    need(begin, ('rw_mr_view_trigger = yes', 'this = scope:rw_mr_provider',
        'exists = scope:rw_mb_fresh_observation', 'scope:rw_mb_fresh_observation = scope:rw_mr_record',
        'var:rw_mr_state = flag:war_observed', 'NOT = { has_variable = rw_mb_schema }',
        'name = rw_mb_serial value = scope:rw_mr_serial', 'name = rw_mb_observed_on value = var:rw_mr_observed_on',
        'name = rw_mb_statement value = flag:unanswered', 'name = rw_mb_state value = flag:pending',
        'name = rw_mb_window value = flag:yes days = 30'), 'legacy backfill renewed window or invented statement')
    obs = block(mr, 'rw_mr_observe_effect')
    points = [obs.find(x) for x in ('name = rw_mr_state value = flag:war_observed',
        'save_scope_as = rw_mb_fresh_observation', 'rw_mb_begin_effect = yes',
        'clear_saved_scope = rw_mb_fresh_observation', 'rw_mr_notify_effect = yes')]
    if min(points) < 0 or points != sorted(points): errors.append('response before fresh fact or after notice')
    request = block(e, 'rw_mb_request_effect')
    need(request, ('limit = { rw_mb_can_request_trigger = yes }',
        'name = rw_mb_requested_on value = current_date', 'scope:rw_mr_provider = { trigger_event'), 'unguarded request')
    answer = block(e, 'rw_mb_answer_effect')
    need(answer, ('rw_mb_can_answer_trigger = yes',
        'OR = { scope:rw_mb_answer = flag:acknowledged scope:rw_mb_answer = flag:contested }',
        'name = rw_mb_statement value = scope:rw_mb_answer', 'name = rw_mb_answered_on value = current_date',
        'scope:rw_mr_beneficiary = { trigger_event'), 'unguarded or fabricated reply')
    if not 0 <= answer.find('name = rw_mb_statement') < answer.find('trigger_event'):
        errors.append('unguarded or fabricated reply')
    for name, state in (('resent', 'resented'), ('note', 'noted')):
        b = block(e, 'rw_mb_'+name+'_effect')
        need(b, ('limit = { rw_mb_can_react_trigger = yes }', 'remove_variable = rw_mb_window',
            'name = rw_mb_state value = flag:'+state, 'name = rw_mb_reacted_on value = current_date'),
            'replayed or unconsumed reaction')
        if name == 'resent':
            need(b, ('NOT = { has_opinion_modifier = { target = scope:rw_mr_provider modifier = rw_restraint_resented_opinion } }',),
                'opinion stacked refreshed or wrong target')
            if not 0 <= b.find('remove_variable = rw_mb_window') < b.find('add_opinion =') < b.find('trigger_event'):
                errors.append('opinion or notice before consumption')
        elif re.search(r'\b(add_opinion|remove_opinion)\s*=', clean_script(b)[0]):
            errors.append('neutral choice changes other grievances')
    code = clean_script(e)[0]
    if re.search(r'\bname\s*=\s*rw_mr_|\b(add_gold|add_prestige|add_hook|remove_hook|add_secret|add_claim|imprison|declare_war|end_war|run_interaction|change_title_holder|every_living_character)\s*=', code):
        errors.append('role facts or native state changed')
    return errors


class RestraintResponseTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_restraint_response_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_restraint_response_effects.txt').read_text()
        self.mr = (MOD/'common/scripted_effects/rw_military_restraint_effects.txt').read_text()
        self.ev = (MOD/'events/rw_military_restraint_events.txt').read_text()

    def errors(self, t=None, e=None, mr=None):
        return response_errors(self.t if t is None else t, self.e if e is None else e, self.mr if mr is None else mr)

    def test_source_contract(self): self.assertEqual([], self.errors())

    def test_exact_private_story_identity_schema_serial_and_observed_date(self):
        for g in ('rw_mr_view_trigger = yes', 'var:rw_mb_serial = scope:rw_mr_serial',
                  'var:rw_mb_observed_on = var:rw_mr_observed_on', 'var:rw_mr_state = flag:war_observed'):
            self.assertIn('foreign incomplete or old observation response', self.errors(t=self.t.replace(g, 'always = yes')))

    def test_fresh_same_call_token_and_no_legacy_backfill(self):
        for g in ('exists = scope:rw_mb_fresh_observation', 'scope:rw_mb_fresh_observation = scope:rw_mr_record',
                  'this = scope:rw_mr_provider', 'NOT = { has_variable = rw_mb_schema }'):
            self.assertIn('legacy backfill renewed window or invented statement', self.errors(e=self.e.replace(g, 'always = yes')))
        self.assertEqual(1, self.mr.count('rw_mb_begin_effect = yes'))
        for path in ('rw_mr_read_effect', 'rw_mr_accept_effect', 'rw_mr_renounce_effect', 'rw_mr_release_effect'):
            self.assertNotIn('rw_mb_begin_effect', block(self.mr, path))

    def test_observation_consumed_before_window_and_token_cleared_before_notice(self):
        for g in ('save_scope_as = rw_mb_fresh_observation', 'clear_saved_scope = rw_mb_fresh_observation',
                  'name = rw_mr_state value = flag:war_observed'):
            self.assertIn('response before fresh fact or after notice', self.errors(mr=self.mr.replace(g, 'removed')))
        self.assertNotIn('trigger_event', block(self.e, 'rw_mb_begin_effect'))

    def test_only_original_living_parties_and_pending_window_can_act(self):
        for g in ('scope:rw_mr_provider = { is_alive = yes }', 'scope:rw_mr_beneficiary = { is_alive = yes }',
                  'var:rw_mb_state = flag:pending', 'has_variable = rw_mb_window'):
            self.assertIn('expired terminal or dead-party action', self.errors(t=self.t.replace(g, 'always = yes')))
        self.assertIn('wrong personal reactor', self.errors(t=self.t.replace('this = scope:rw_mr_beneficiary', 'always = yes')))

    def test_single_optional_request_never_implies_admission(self):
        for g in ('rw_mb_can_react_trigger = yes', 'NOT = { has_variable = rw_mb_requested_on }'):
            self.assertIn('repeated or wrong request', self.errors(t=self.t.replace(g, 'always = yes')))
        b = block(self.e, 'rw_mb_request_effect')
        self.assertNotIn('name = rw_mb_statement', b)
        self.assertNotIn('add_opinion', b)
        self.assertLess(b.index('name = rw_mb_requested_on'), b.index('trigger_event'))

    def test_only_requested_original_promisor_can_answer_once(self):
        for g in ('this = scope:rw_mr_provider', 'has_variable = rw_mb_requested_on', 'var:rw_mb_statement = flag:unanswered'):
            self.assertIn('unsolicited replayed or wrong reply', self.errors(t=self.t.replace(g, 'always = yes')))
        self.assertIn('unguarded or fabricated reply', self.errors(e=self.e.replace('rw_mb_can_answer_trigger = yes', 'always = yes')))

    def test_reply_is_explicit_enum_and_preserves_fact(self):
        g = 'OR = { scope:rw_mb_answer = flag:acknowledged scope:rw_mb_answer = flag:contested }'
        self.assertIn('unguarded or fabricated reply', self.errors(e=self.e.replace(g, 'always = yes')))
        b = block(self.e, 'rw_mb_answer_effect')
        self.assertNotRegex(b, r'\b(add_opinion|remove_opinion|add_gold)\s*=|name\s*=\s*rw_mr_')
        for g in ('ANSWER = acknowledged', 'ANSWER = contested'): self.assertIn(g, self.ev)

    def test_response_needs_no_reply_or_verdict_and_keeps_other_disputes(self):
        b = block(self.t, 'rw_mb_can_react_trigger')
        self.assertNotIn('rw_mb_statement', b)
        self.assertNotIn('rw_mb_requested_on', b)
        self.assertNotRegex(self.e, r'\bremove_opinion\s*=')
        self.assertIn('neutral choice changes other grievances', self.errors(e=self.e.replace('rw_mb_note_effect = {', 'rw_mb_note_effect = { remove_opinion = {}')))

    def test_both_reactions_consumed_before_optional_opinion_and_notice(self):
        for g in ('limit = { rw_mb_can_react_trigger = yes }', 'remove_variable = rw_mb_window',
                  'name = rw_mb_reacted_on value = current_date'):
            self.assertIn('replayed or unconsumed reaction', self.errors(e=self.e.replace(g, 'removed')))
        self.assertIn('opinion or notice before consumption', self.errors(e=self.e.replace('add_opinion =', 'removed =')))

    def test_existing_pair_grievance_never_stacks_or_refreshes(self):
        g = 'NOT = { has_opinion_modifier = { target = scope:rw_mr_provider modifier = rw_restraint_resented_opinion } }'
        self.assertIn('opinion stacked refreshed or wrong target', self.errors(e=self.e.replace(g, 'always = yes')))
        op = (MOD/'common/opinion_modifiers/rw_restraint_response_opinions.txt').read_text()
        self.assertRegex(op, r'opinion\s*=\s*-15\b')
        self.assertRegex(op, r'years\s*=\s*2\b')
        self.assertEqual(1, len(re.findall(r'\badd_opinion\s*=', self.e)))

    def test_original_thirty_day_window_never_renews_and_silence_stays_unanswered(self):
        self.assertEqual(1, len(re.findall(r'name\s*=\s*rw_mb_window\b', self.e)))
        self.assertIn('legacy backfill renewed window or invented statement', self.errors(e=self.e.replace('days = 30', 'days = 365')))
        for name in ('rw_mb_request_effect', 'rw_mb_answer_effect', 'rw_mb_resent_effect', 'rw_mb_note_effect'):
            self.assertNotRegex(block(self.e, name), r'\b(?:days|months|years)\s*=')
        self.assertIn('name = rw_mb_statement value = flag:unanswered', block(self.e, 'rw_mb_begin_effect'))
        self.assertIn('desc = rw_restraint_response.expired', self.ev)

    def test_private_bounded_notices_no_timer_global_poll_or_legal_war_effect(self):
        self.assertEqual(4, self.e.count('trigger_event ='))
        self.assertNotIn('scope:rw_case_mediator', self.e+self.ev)
        self.assertNotRegex(self.e, r'\b(?:days|months|years)\s*=\s*(?:1|7|90)\b')
        for cmd in ('declare_war = {}', 'imprison = {}', 'add_secret = {}', 'add_gold = {}'):
            self.assertIn('role facts or native state changed', self.errors(e=self.e+'\n'+cmd))
        self.assertIn('role facts or native state changed', self.errors(e=self.e+'\nset_variable = { name = rw_mr_state value = flag:fulfilled }'))

    def test_ai_and_player_share_request_reply_reaction_guards(self):
        self.assertNotRegex(clean_script(self.t+self.e+self.ev)[0], r'\bis_ai\s*=')
        for name in ('request', 'answer', 'react'):
            self.assertIn('rw_mb_can_'+name+'_trigger = yes', self.ev)
        for trait in ('just', 'honest', 'deceitful', 'vengeful', 'forgiving'):
            self.assertIn('has_trait = '+trait, self.ev)
        self.assertIn('var:rw_mb_statement = flag:acknowledged', self.ev)

    def test_localized_status_choices_and_statement_fact_distinction(self):
        keys = set(re.findall(r'(?:name|desc)\s*=\s*(rw_restraint_response\.[\w.]+)', self.ev))
        keys.add('rw_restraint_resented_opinion')
        for lang in ('english', 'french'):
            p=MOD/f'localization/{lang}/rw_restraint_response_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertTrue(keys<=actual,keys-actual)
