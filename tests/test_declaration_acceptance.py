"""Source contracts for exact post-native acceptance metadata; no CK3 model."""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_g1_native_choice import FIXTURE
from test_g1_royal_response import block

ROOT = builder.TEMPLATES


def acceptance_errors(triggers, effects):
    errors = []

    def need(source, tokens, label):
        if any(token not in source for token in tokens):
            errors.append(label)

    match = block(triggers, 'rw_dl_acceptance_match_trigger')
    need(match, ('story_type = story_rw_declaration_law', 'story_owner = scope:actor',
                 'var:rw_dl_schema = 1', 'var:rw_dl_party_schema = 1', 'var:rw_dl_serial > 0',
                 'has_variable = rw_dl_retained',
                 'var:rw_dl_phase = flag:claim_cb_on_declaration_prefix',
                 'var:rw_dl_seen_on = current_date',
                 'var:rw_dl_attacker = scope:actor', 'var:rw_dl_defender = scope:recipient',
                 'var:rw_dl_issuer = scope:actor.liege',
                 'exists = var:rw_dl_authority', 'holder = scope:actor.liege',
                 'exists = var:rw_dl_war', 'using_cb = claim_cb',
                 'primary_attacker = scope:actor', 'primary_defender = scope:recipient',
                 'any_character_war = { this = scope:rw_da_check.var:rw_dl_war }'),
         'foreign/legacy/stale/inactive receipt')
    if 'rw_dl_accepted_on' in match or 'rw_dl_acceptance_ready' in match:
        errors.append('processed receipt hidden from ambiguity check')
    bind = block(effects, 'rw_dl_bind_acceptance_effect')
    need(bind, ('exists = scope:actor', 'exists = scope:recipient', 'this = scope:actor',
                'exists = liege', 'liege = { is_alive = yes is_landed = yes }',
                'count >= 2',
                'primary_attacker = scope:actor', 'primary_defender = scope:recipient',
                'any_owned_story = { rw_dl_acceptance_match_trigger = yes }',
                'count >= 2 rw_dl_acceptance_match_trigger = yes',
                'clear_saved_scope = rw_da_record', 'exists = scope:rw_da_record',
                'has_variable = rw_dl_acceptance_ready', 'remove_variable = rw_dl_acceptance_ready',
                'NOT = { has_variable = rw_dl_accepted_on }',
                'name = rw_dl_accepted_on value = current_date',
                'name = rw_dl_acceptance_schema value = 1',
                'name = rw_dl_accepted_actor value = scope:actor',
                'name = rw_dl_accepted_recipient value = scope:recipient'), 'ambiguous/replayed acceptance')
    recheck = ('exists = scope:rw_da_record scope:rw_da_record = { '
               'rw_dl_acceptance_match_trigger = yes '
               'has_variable = rw_dl_acceptance_ready '
               'NOT = { has_variable = rw_dl_accepted_on } }')
    if recheck not in ' '.join(bind.split()):
        errors.append('missing final revalidation')
    if bind.index('name = rw_dl_accepted_on value = current_date') > bind.index('name = rw_dl_accepted_actor value ='):
        errors.append('acceptance consumed after metadata')
    if bind.index('remove_variable = rw_dl_acceptance_ready') > bind.index('name = rw_dl_accepted_on value ='):
        errors.append('acceptance consumed after metadata')
    if 'using_cb' in bind:
        errors.append('other-CB pair ambiguity ignored')
    if re.search(r'\b(start_war|end_war|run_interaction|create_story|add_gold|use_hook|add_opinion|trigger_event|change_title_holder)\s*=',
                 clean_script(bind)[0]):
        errors.append('acceptance performs native or new political action')
    for operation in ('rw_dl_capture_effect', 'rw_dl_capture_targets_effect',
                      'has_realm_law_flag', 'rw_dl_native_permission_trigger'):
        if operation in bind+match:
            errors.append('late law or party reconstruction')
    if 'days =' in bind or 'name = rw_dl_retained' in bind:
        errors.append('acceptance extends snapshot lifetime')
    if re.search(r'save_(?:temporary_)?scope_as\s*=\s*(actor|recipient|attacker|defender|target|war)\b', bind+match):
        errors.append('native identity overwritten')
    return errors


class DeclarationAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.triggers = (ROOT/'common/scripted_triggers/rw_declaration_law_triggers.txt').read_text(encoding='utf-8-sig')
        self.effects = (ROOT/'common/scripted_effects/rw_declaration_law_effects.txt').read_text(encoding='utf-8-sig')

    def test_actual_acceptance_source_contract(self):
        self.assertEqual([], acceptance_errors(self.triggers, self.effects))

    def test_foreign_legacy_stale_and_changed_authority_are_detected(self):
        for token in ('story_owner = scope:actor', 'var:rw_dl_party_schema = 1',
                      'var:rw_dl_seen_on = current_date', 'var:rw_dl_attacker = scope:actor',
                      'var:rw_dl_defender = scope:recipient', 'holder = scope:actor.liege',
                      'primary_defender = scope:recipient'):
            with self.subTest(guard=token):
                self.assertIn('foreign/legacy/stale/inactive receipt', acceptance_errors(
                    self.triggers.replace(token, 'always = yes'), self.effects))

    def test_ambiguous_wars_receipts_and_replay_are_detected(self):
        for token in ('count >= 2', 'has_variable = rw_dl_acceptance_ready',
                      'NOT = { has_variable = rw_dl_accepted_on }',
                      'count >= 2 rw_dl_acceptance_match_trigger = yes'):
            with self.subTest(guard=token):
                self.assertIn('ambiguous/replayed acceptance', acceptance_errors(
                    self.triggers, self.effects.replace(token, 'always = yes')))
        changed = self.triggers.replace('rw_dl_acceptance_match_trigger = {',
            'rw_dl_acceptance_match_trigger = { NOT = { has_variable = rw_dl_accepted_on }')
        self.assertIn('processed receipt hidden from ambiguity check', acceptance_errors(changed, self.effects))
        changed = self.effects.replace('count >= 2\n                    primary_attacker',
                                       'count >= 2 using_cb = claim_cb\n                    primary_attacker')
        self.assertIn('other-CB pair ambiguity ignored', acceptance_errors(self.triggers, changed))

    def test_selected_flags_keep_distinct_ordinary_defy_hook_and_ambiguous_branches(self):
        expected = '''
            set_variable = { name = rw_dl_accepted_choice value = flag:ordinary }
            if = {
                limit = { always = scope:rw_uw_defy }
                set_variable = { name = rw_dl_accepted_choice value = flag:defy_selected }
                if = {
                    limit = { always = scope:hook }
                    set_variable = { name = rw_dl_accepted_choice value = flag:ambiguous }
                }
            }
            else_if = {
                limit = { always = scope:hook }
                set_variable = { name = rw_dl_accepted_choice value = flag:hook_selected }
            }
        '''
        self.assertIn(' '.join(expected.split()), ' '.join(clean_script(self.effects)[0].split()))

    def test_tail_hook_runs_after_native_body_before_existing_response_and_inverts(self):
        original, patched = builder.patch_native(FIXTURE.encode())
        tail = builder.ACCEPT.encode()
        self.assertEqual(1, patched.count(tail))
        self.assertGreater(patched.index(tail), patched.index(b'preserved_native_callback = yes'))
        self.assertLess(tail.index(b'rw_dl_bind_acceptance_effect'), tail.index(b'rw_uw_notice_effect'))
        restored = patched
        for addition in (builder.GUARD, builder.OPTION, builder.ACCEPT):
            restored = restored.replace(addition.encode(), b'', 1)
        self.assertEqual(original, restored)

    def test_no_late_capture_native_effect_or_retention_extension(self):
        for operation, error in (
            ('rw_dl_capture_effect = yes', 'late law or party reconstruction'),
            ('run_interaction = {}', 'acceptance performs native or new political action'),
            ('set_variable = { name = rw_dl_retained value = flag:yes days = 365 }',
             'acceptance extends snapshot lifetime'),
            ('save_scope_as = actor', 'native identity overwritten'),
        ):
            changed = self.effects.replace('rw_dl_bind_acceptance_effect = {',
                                           'rw_dl_bind_acceptance_effect = { '+operation)
            with self.subTest(operation=operation):
                self.assertIn(error, acceptance_errors(self.triggers, changed))
