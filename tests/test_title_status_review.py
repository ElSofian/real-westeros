"""Static original-script checks; no CK3 title transfer or noble-status simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'
PERSON = 'scope:rw_scheme_evidence_record.var:rw_evidence_participant'


def review_errors(t, v, parent):
    errors = []
    if 'rw_sentencing_current_prisoner_trigger = yes' not in block(t, 'rw_title_status_view_trigger'):
        errors.append('private current custody bypass')
    for key in ('revoke_reason', 'no_revoke_reason', 'knight', 'stripped_knight', 'landed_knight_contract', 'can_open_revocation', 'can_open_release'):
        if 'rw_title_status_view_trigger = yes' not in block(t, f'rw_title_status_{key}_trigger'):
            errors.append('unguarded branch')
    reason = block(t, 'rw_title_status_revoke_reason_trigger')
    no_reason = block(t, 'rw_title_status_no_revoke_reason_trigger')
    if f'has_revoke_title_reason = {PERSON}' not in reason or f'NOT = {{ has_revoke_title_reason = {PERSON} }}' not in no_reason:
        errors.append('revocation grounds confused or reversed')
    knight = block(t, 'rw_title_status_knight_trigger')
    if f'{PERSON} = {{ is_agot_knight_trigger = yes }}' not in knight:
        errors.append('native recognition replaced by guessed status')
    stripped = block(t, 'rw_title_status_stripped_knight_trigger')
    if f'{PERSON} = {{ has_trait = stripped_knight }}' not in stripped:
        errors.append('wrong stripped knight')
    contract = block(t, 'rw_title_status_landed_knight_contract_trigger')
    if 'exists = liege' not in contract or 'vassal_contract_has_flag = has_landed_knight_contract' not in contract or f'{PERSON} = {{' not in contract:
        errors.append('contract context conflated with nobility')
    gate = block(t, 'rw_title_status_can_open_revocation_trigger')
    for guard in ('is_ai = no', 'is_landed = yes', 'liege = scope:rw_scheme_observer'):
        if guard not in gate:
            errors.append('wrong revocation subject or UI')
    native = nested_block(gate, 'is_character_interaction_valid')
    if 'interaction = revoke_title_interaction' not in native or f'recipient = {PERSON}' not in native:
        errors.append('wrong native revocation query')
    if 'rw_sentencing_can_open_release_trigger = yes' not in block(t, 'rw_title_status_can_open_release_trigger'):
        errors.append('release eligibility copied or bypassed')
    for action, interaction in (('revocation', 'revoke_title_interaction'), ('release', 'release_from_prison_interaction')):
        if v.count(f'trigger = {{ rw_title_status_can_open_{action}_trigger = yes }}') != 1 or v.count(f'limit = {{ rw_title_status_can_open_{action}_trigger = yes }}') != 1:
            errors.append('stale click not revalidated')
        option = v.split(f'name = rw_title_status.review_{action}', 1)[-1].split('ai_chance', 1)[0]
        window = nested_block(option, 'open_interaction_window')
        for field in (f'interaction = {interaction}', 'actor = root', f'recipient = {PERSON}'):
            if field not in window:
                errors.append('wrong native handoff')
        if re.search(r'\b(target|secondary_recipient|send_option|flag)\s*=', window):
            errors.append('punishment term preselected')
    if parent.count('limit = { rw_title_status_view_trigger = yes }') != 1 or parent.count('trigger_event = { id = rw_title_status.0001 }') != 1:
        errors.append('unguarded parent navigation')
    code = clean_script(t + v)[0]
    if re.search(r'\b(run_interaction|send_interaction|change_title_holder|change_liege|create_title_and_vassal_change|destroy_title|vassal_contract_set_obligation_level|add_trait|remove_trait|add_to_global_variable_list|change_house_relation_effect|add_opinion|add_gold|set_variable|remove_variable|add_character_flag|trigger_event|agot_strip_lordship_as_punishment_effect|agot_strip_knighthood_as_punishment_effect)\s*=', code):
        errors.append('navigation applies or caches a sanction')
    return errors


class TitleStatusReviewTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_title_status_triggers.txt').read_text()
        self.v = (MOD / 'events/rw_title_status_events.txt').read_text()
        self.p = (MOD / 'events/rw_sentencing_events.txt').read_text()

    def errors(self, t=None, v=None, parent=None):
        return review_errors(self.t if t is None else t, self.v if v is None else v, self.p if parent is None else parent)

    def test_current_review_contract(self):
        self.assertEqual([], self.errors())

    def test_private_foreign_stale_custody_mutations(self):
        self.assertIn('private current custody bypass', self.errors(t=self.t.replace('rw_sentencing_current_prisoner_trigger = yes', 'always = yes')))
        self.assertIn('unguarded branch', self.errors(t=self.t.replace('rw_title_status_view_trigger = yes', 'always = yes')))

    def test_arrest_execution_not_promoted_to_revocation(self):
        for substitute in ('has_execute_reason', 'has_imprisonment_reason'):
            self.assertIn('revocation grounds confused or reversed', self.errors(t=self.t.replace('has_revoke_title_reason', substitute)))
        self.assertIn('revocation grounds confused or reversed', self.errors(t=self.t.replace(f'has_revoke_title_reason = {PERSON}', 'has_revoke_title_reason = scope:rw_scheme_observer')))
        self.assertNotIn('has_revoke_title_reason', block(self.t, 'rw_title_status_can_open_revocation_trigger'))

    def test_native_knight_and_stripped_status_stay_separate(self):
        self.assertIn('native recognition replaced by guessed status', self.errors(t=self.t.replace('is_agot_knight_trigger = yes', 'has_trait = knight')))
        self.assertIn('wrong stripped knight', self.errors(t=self.t.replace('has_trait = stripped_knight', 'has_trait = knight')))
        self.assertIn('rw_title_status.knight', self.v)
        self.assertIn('rw_title_status.stripped_knight', self.v)

    def test_contract_context_and_direct_vassal_mutations(self):
        self.assertIn('contract context conflated with nobility', self.errors(t=self.t.replace('exists = liege', 'always = yes')))
        self.assertIn('contract context conflated with nobility', self.errors(t=self.t.replace('has_landed_knight_contract', 'vassal_contract_cannot_revoke_titles')))
        for guard in ('liege = scope:rw_scheme_observer', 'is_landed = yes', 'is_ai = no'):
            self.assertIn('wrong revocation subject or UI', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_exact_native_query_and_release_delegation(self):
        self.assertIn('wrong native revocation query', self.errors(t=self.t.replace('interaction = revoke_title_interaction', 'interaction = retract_vassal_interaction')))
        self.assertIn('release eligibility copied or bypassed', self.errors(t=self.t.replace('rw_sentencing_can_open_release_trigger = yes', 'always = yes')))

    def test_each_window_click_revalidates(self):
        for action in ('revocation', 'release'):
            self.assertIn('stale click not revalidated', self.errors(v=self.v.replace(f'limit = {{ rw_title_status_can_open_{action}_trigger = yes }}', 'limit = { always = yes }')))

    def test_actor_recipient_and_term_preselection_mutations(self):
        for old, new in (('actor = root', 'actor = scope:rw_scheme_participant'),
                         (f'recipient = {PERSON}', 'recipient = root'),
                         ('interaction = revoke_title_interaction', 'interaction = grant_titles_interaction')):
            self.assertIn('wrong native handoff', self.errors(v=self.v.replace(old, new)))
        self.assertIn('punishment term preselected', self.errors(v=self.v.replace('interaction = revoke_title_interaction', 'interaction = revoke_title_interaction target = title:d_dummy')))

    def test_no_forced_transfer_status_or_completed_cache(self):
        for effect in ('run_interaction', 'destroy_title', 'change_title_holder', 'vassal_contract_set_obligation_level', 'add_trait', 'agot_strip_lordship_as_punishment_effect', 'set_variable'):
            self.assertIn('navigation applies or caches a sanction', self.errors(v=self.v + f'\n{effect} = yes'))

    def test_parent_navigation_and_portrait_are_private(self):
        self.assertIn('unguarded parent navigation', self.errors(parent=self.p.replace('limit = { rw_title_status_view_trigger = yes }', 'limit = { always = yes }')))
        portrait = nested_block(self.v, 'right_portrait')
        self.assertIn('trigger = { rw_title_status_view_trigger = yes }', portrait)
        self.assertIn(f'character = {PERSON}', portrait)

    def test_no_family_ban_scheduler_or_native_overrides(self):
        code = clean_script(self.t + self.v)[0]
        self.assertNotRegex(code, r'\b(every_house_member|every_dynasty_member|every_held_title|every_living_character|days|years|on_actions|immediate|after)\s*=')
        self.assertNotIn('rw_scheme_response_state', code)
        self.assertNotIn('rw_service_', code)
        self.assertEqual(2, self.v.count('open_interaction_window = {'))

    def test_localization_and_known_subject_only(self):
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_title_status\.[\w.]+)', self.v + self.p))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_title_status_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', text, re.M)))
            self.assertNotIn('[', text)
