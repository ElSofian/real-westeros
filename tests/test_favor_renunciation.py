"""Adversarial source contracts for personal renunciation response, not CK3 proof."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/real_westeros'


def response_errors(t, e, fd):
    errors = []
    view = block(t, 'rw_fr_view_trigger')
    for guard in ('rw_fv_view_trigger = yes', 'rw_fd_deferred_trigger = yes',
                  'var:rw_fv_state = flag:provider_renounced', 'var:rw_fr_schema = 1',
                  'var:rw_fr_serial = scope:rw_fv_serial', 'var:rw_fr_revision = scope:rw_fv_revision',
                  'var:rw_fr_term = scope:rw_fv_term', 'has_variable = rw_fr_finished_on',
                  'var:rw_fr_finished_on = var:rw_fv_finished_on', 'has_variable = rw_fr_responded_on'):
        if guard not in view:
            errors.append('foreign stale or incomplete receipt')
    respond = block(t, 'rw_fr_can_respond_trigger')
    for guard in ('rw_fr_view_trigger = yes', 'this = scope:rw_fv_client', 'is_alive = yes',
                  'var:rw_fr_state = flag:pending', 'has_variable = rw_fr_window'):
        if guard not in respond:
            errors.append('wrong actor replay or expired response')
    begin = block(e, 'rw_fr_begin_effect')
    for guard in ('rw_fv_view_trigger = yes', 'rw_fd_deferred_trigger = yes', 'this = scope:rw_fv_provider',
                  'exists = scope:rw_fr_fresh_renunciation',
                  'scope:rw_fr_fresh_renunciation = scope:rw_fv_provider',
                  'var:rw_fv_state = flag:provider_renounced',
                  'NOT = { AND = { has_variable = rw_fr_serial var:rw_fr_serial = scope:rw_fv_serial } }'):
        if guard not in begin:
            errors.append('legacy backfill or repeated response window')
    for name, value in (('serial', 'scope:rw_fv_serial'), ('revision', 'scope:rw_fv_revision'),
                        ('term', 'scope:rw_fv_term'), ('finished_on', 'var:rw_fv_finished_on')):
        if f'name = rw_fr_{name} value = {value}' not in begin:
            errors.append('unbound response receipt')
    if 'name = rw_fr_window value = flag:yes days = 30' not in begin:
        errors.append('response deadline changed')
    renounce = block(fd, 'rw_fd_renounce_effect')
    parts = [renounce.find(x) for x in ('limit = { rw_fd_can_renounce_trigger = yes }',
        'rw_fd_finish_effect = { RESULT = provider_renounced }',
        'save_scope_as = rw_fr_fresh_renunciation', 'rw_fr_begin_effect = yes',
        'clear_saved_scope = rw_fr_fresh_renunciation', 'rw_fv_notify_effect = yes')]
    if min(parts) < 0 or parts != sorted(parts):
        errors.append('fresh evidence before terminal consumption or notice')
    for action, result in (('resent', 'resented'), ('note', 'noted')):
        b = block(e, f'rw_fr_{action}_effect')
        for guard in ('limit = { rw_fr_can_respond_trigger = yes }', 'remove_variable = rw_fr_window',
                      f'name = rw_fr_state value = flag:{result}', 'name = rw_fr_responded_on value = current_date'):
            if guard not in b:
                errors.append('response not guarded or consumed')
        if action == 'resent':
            if 'NOT = { has_opinion_modifier = { target = scope:rw_fv_provider modifier = rw_favor_renounced_opinion } }' not in b:
                errors.append('rancour stacked or renewed')
            if not 0 <= b.find('remove_variable = rw_fr_window') < b.find('add_opinion =') < b.find('rw_fr_notify_provider_effect = yes'):
                errors.append('opinion before consumption or private notice')
        elif re.search(r'\b(add_opinion|remove_opinion)\s*=', b):
            errors.append('neutral response changes opinions')
    code = clean_script(e)[0]
    if re.search(r'\b(add_hook|remove_hook|add_gold|add_prestige|imprison|add_secret|add_claim|run_interaction|every_living_character|create_story|change_title_holder)\s*=', code):
        errors.append('personal reaction alters native state or scans world')
    return errors


class FavorRenunciationTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_favor_renunciation_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_favor_renunciation_effects.txt').read_text()
        self.fd = (MOD/'common/scripted_effects/rw_deferred_favor_effects.txt').read_text()
        self.ev = (MOD/'events/rw_favor_service_events.txt').read_text()

    def errors(self, t=None, e=None, fd=None):
        return response_errors(self.t if t is None else t, self.e if e is None else e, self.fd if fd is None else fd)

    def test_source_contract(self):
        self.assertEqual([], self.errors())

    def test_full_private_mode_and_original_ticket_required(self):
        for guard in ('rw_fv_view_trigger = yes', 'rw_fd_deferred_trigger = yes',
                      'var:rw_fv_state = flag:provider_renounced', 'var:rw_fr_serial = scope:rw_fv_serial',
                      'var:rw_fr_revision = scope:rw_fv_revision', 'var:rw_fr_term = scope:rw_fv_term',
                      'var:rw_fr_finished_on = var:rw_fv_finished_on'):
            self.assertIn('foreign stale or incomplete receipt', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_only_original_living_client_and_unspent_fixed_window(self):
        for guard in ('this = scope:rw_fv_client', 'is_alive = yes', 'var:rw_fr_state = flag:pending', 'has_variable = rw_fr_window'):
            self.assertIn('wrong actor replay or expired response', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertIn('is_alive = yes', block((MOD/'common/scripted_triggers/rw_favor_service_triggers.txt').read_text(), 'rw_fv_view_trigger'))

    def test_legacy_receipt_cannot_backfill_or_renew(self):
        for guard in ('this = scope:rw_fv_provider', 'exists = scope:rw_fr_fresh_renunciation',
                      'scope:rw_fr_fresh_renunciation = scope:rw_fv_provider',
                      'NOT = { AND = { has_variable = rw_fr_serial var:rw_fr_serial = scope:rw_fv_serial } }'):
            self.assertIn('legacy backfill or repeated response window', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertIn('unbound response receipt', self.errors(e=self.e.replace('name = rw_fr_revision value = scope:rw_fv_revision', 'removed')))

    def test_terminal_renunciation_precedes_fresh_window_and_both_notices(self):
        for guard in ('rw_fd_finish_effect = { RESULT = provider_renounced }', 'save_scope_as = rw_fr_fresh_renunciation',
                      'clear_saved_scope = rw_fr_fresh_renunciation'):
            self.assertIn('fresh evidence before terminal consumption or notice', self.errors(fd=self.fd.replace(guard, '')))
        self.assertEqual(1, self.fd.count('rw_fr_begin_effect = yes'))
        for path in ('rw_fd_timeout_effect', 'rw_fd_withdraw_effect', 'rw_fd_perform_effect', 'rw_fd_accept_effect'):
            self.assertNotIn('rw_fr_', block(self.fd, path))

    def test_review_leave_and_notifications_never_renew_response_window(self):
        self.assertEqual(1, len(re.findall(r'name\s*=\s*rw_fr_window\b', self.e)))
        fv = (MOD/'common/scripted_effects/rw_favor_service_effects.txt').read_text()
        self.assertNotIn('rw_fr_begin_effect', fv + self.ev)
        self.assertIn('response deadline changed', self.errors(e=self.e.replace('days = 30', 'days = 365')))
        self.assertNotRegex(self.e, r'\b(?:days|months|years)\s*=\s*1\b')

    def test_each_choice_consumes_before_opinion_and_notice(self):
        for guard in ('limit = { rw_fr_can_respond_trigger = yes }', 'remove_variable = rw_fr_window',
                      'name = rw_fr_responded_on value = current_date'):
            self.assertIn('response not guarded or consumed', self.errors(e=self.e.replace(guard, 'removed')))
        self.assertIn('opinion before consumption or private notice', self.errors(e=self.e.replace('add_opinion = {', 'removed = {')))

    def test_pair_opinion_cannot_stack_or_refresh_between_new_promises(self):
        guard = 'NOT = { has_opinion_modifier = { target = scope:rw_fv_provider modifier = rw_favor_renounced_opinion } }'
        self.assertIn('rancour stacked or renewed', self.errors(e=self.e.replace(guard, 'always = yes')))
        op = (MOD/'common/opinion_modifiers/rw_favor_renunciation_opinions.txt').read_text()
        self.assertRegex(op, r'opinion\s*=\s*-15\b')
        self.assertRegex(op, r'years\s*=\s*2\b')
        self.assertEqual(1, len(re.findall(r'\badd_opinion\s*=', self.e)))

    def test_neutral_choice_does_not_forgive_other_affairs(self):
        self.assertIn('neutral response changes opinions', self.errors(e=self.e.replace('rw_fr_note_effect = {', 'rw_fr_note_effect = { remove_opinion = {}')))
        self.assertNotRegex(self.e, r'\b(remove_opinion|remove_character_flag)\s*=')

    def test_only_private_original_provider_notice_and_no_reminders(self):
        b = block(self.e, 'rw_fr_notify_provider_effect')
        self.assertIn('scope:rw_fv_provider =', b)
        self.assertIn('id = rw_favor_service.0001', b)
        self.assertNotIn('scope:rw_fv_client', b)
        self.assertEqual(1, self.e.count('trigger_event ='))
        self.assertNotIn('rw_fr_', block(self.fd, 'rw_fd_timeout_effect'))

    def test_native_state_ai_and_player_execution_unchanged(self):
        for cmd in ('add_hook', 'add_gold', 'imprison', 'run_interaction', 'every_living_character'):
            self.assertIn('personal reaction alters native state or scans world', self.errors(e=self.e+'\n'+cmd+' = {}'))
        self.assertNotRegex(clean_script(self.t+self.e+self.ev)[0], r'\bis_ai\s*=')
        for action in ('resent', 'note'):
            self.assertIn('trigger = { rw_fr_can_respond_trigger = yes }', self.ev)
            self.assertIn('rw_fr_'+action+'_effect = yes', self.ev)
        self.assertIn('has_trait = vengeful', self.ev)
        self.assertIn('has_trait = forgiving', self.ev)

    def test_localized_choices_and_distinct_silence_status(self):
        keys = set(re.findall(r'(?:name|desc)\s*=\s*(rw_favor_renunciation\.[\w.]+)', self.ev))
        keys.add('rw_favor_renounced_opinion')
        self.assertIn('rw_favor_renunciation.expired', keys)
        for lang in ('english', 'french'):
            p = MOD/f'localization/{lang}/rw_favor_renunciation_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertTrue(keys <= actual, keys - actual)
