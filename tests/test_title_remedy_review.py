"""Adversarial source checks for exact-role native navigation, not title simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def review_errors(t, e, v, parent):
    errors = []
    entry = block(t, 'rw_title_remedy_can_review_trigger')
    for guard in ('rw_house_view_trigger = yes', 'is_ai = no',
                  'var:rw_house_state = flag:restored', 'has_variable = rw_house_retained'):
        if guard not in entry:
            errors.append('unrestored or stale record')
    roles = nested_block(entry, 'OR')
    if 'rw_house_current_ruler_trigger = yes' not in roles or 'rw_house_current_head_trigger = yes' not in roles:
        errors.append('reader confused with current role')
    authority = nested_block(entry, 'scope:rw_house_authority')
    if 'exists = holder' not in authority or 'holder = { rw_house_sovereign_trigger = yes }' not in authority:
        errors.append('unqualified authority')
    head = nested_block(entry, 'scope:rw_house_target')
    for guard in ('exists = house_head', 'is_alive = yes', 'is_adult = yes',
                  'is_imprisoned = no', 'house = scope:rw_house_target',
                  'NOT = { this = scope:rw_house_authority.holder }'):
        if guard not in head:
            errors.append('wrong or unavailable house head')
    view = block(t, 'rw_title_remedy_view_trigger')
    for guard in ('rw_title_remedy_can_review_trigger = yes',
                  'exists = scope:rw_title_remedy_ruler', 'exists = scope:rw_title_remedy_head',
                  'scope:rw_house_authority = { holder = scope:rw_title_remedy_ruler }',
                  'scope:rw_house_target = { house_head = scope:rw_title_remedy_head }'):
        if guard not in view:
            errors.append('recipient changed under old panel')
    gate = block(t, 'rw_title_remedy_can_open_grant_trigger')
    for guard in ('rw_title_remedy_view_trigger = yes', 'rw_house_current_ruler_trigger = yes',
                  'this = scope:rw_title_remedy_ruler'):
        if guard not in gate:
            errors.append('nonruler can grant')
    query = nested_block(gate, 'is_character_interaction_valid')
    if query.strip() != 'interaction = grant_titles_interaction\n        recipient = scope:rw_title_remedy_head':
        errors.append('native eligibility bypass or wrong recipient')
    if 'limit = { rw_title_remedy_can_review_trigger = yes }' not in e:
        errors.append('unguarded review dispatch')
    for alias in ('scope:rw_house_authority.holder = { save_scope_as = rw_title_remedy_ruler }',
                  'scope:rw_house_target.house_head = { save_scope_as = rw_title_remedy_head }'):
        if alias not in e or e.find(alias) > e.find('trigger_event'):
            errors.append('recipient not captured before dispatch')
    if e.count('trigger_event = { id = rw_title_remedies.0001 }') != 1:
        errors.append('wrong review dispatch')
    if 'trigger = { rw_title_remedy_can_review_trigger = yes }' not in parent or parent.count('rw_title_remedy_open_review_effect = yes') != 1:
        errors.append('unguarded archive navigation')
    if v.count('trigger = { rw_title_remedy_can_open_grant_trigger = yes }') != 1 or v.count('limit = { rw_title_remedy_can_open_grant_trigger = yes }') != 1:
        errors.append('stale native click')
    window = nested_block(v, 'open_interaction_window')
    for field in ('interaction = grant_titles_interaction', 'actor = root', 'recipient = scope:rw_title_remedy_head'):
        if field not in window:
            errors.append('wrong native handoff')
    if re.search(r'\b(target|secondary_recipient|send_option|flag|execute_threshold)\s*=', window):
        errors.append('native title or terms preselected')
    portrait = nested_block(v, 'right_portrait')
    if 'trigger = { rw_title_remedy_view_trigger = yes }' not in portrait or 'character = scope:rw_title_remedy_head' not in portrait:
        errors.append('stale portrait')
    if 'trigger = { rw_title_remedy_view_trigger = yes }' not in v.split('right_portrait')[0]:
        errors.append('stale description')
    code = clean_script(t + e + v)[0]
    forbidden = ('run_interaction', 'send_interaction', 'change_title_holder',
                 'change_title_holder_include_vassals', 'create_title_and_vassal_change',
                 'resolve_title_and_vassal_change', 'change_liege', 'destroy_title',
                 'set_variable', 'remove_variable', 'add_character_flag', 'add_opinion',
                 'add_gold', 'add_prestige', 'add_trait', 'remove_trait',
                 'add_to_global_variable_list', 'every_house_member', 'days', 'years', 'on_actions')
    if re.search(r'\b(' + '|'.join(forbidden) + r')\s*=', code):
        errors.append('navigation mutates state or schedules work')
    return errors


class TitleRemedyReviewTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_title_remedy_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_title_remedy_effects.txt').read_text()
        self.v = (MOD / 'events/rw_title_remedy_events.txt').read_text()
        self.p = (MOD / 'events/rw_house_affair_events.txt').read_text()

    def errors(self, t=None, e=None, v=None, p=None):
        return review_errors(self.t if t is None else t, self.e if e is None else e,
                             self.v if v is None else v, self.p if p is None else p)

    def test_review_contract(self):
        self.assertEqual([], self.errors())

    def test_old_or_unrestored_record_mutations(self):
        for guard in ('rw_house_view_trigger = yes', 'is_ai = no',
                      'var:rw_house_state = flag:restored', 'has_variable = rw_house_retained'):
            self.assertIn('unrestored or stale record', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_reader_is_not_authority_or_head(self):
        for guard in ('rw_house_current_ruler_trigger = yes', 'rw_house_current_head_trigger = yes'):
            self.assertIn('reader confused with current role', self.errors(t=self.t.replace(guard, 'always = yes', 1)))
        self.assertIn('unqualified authority', self.errors(t=self.t.replace('holder = { rw_house_sovereign_trigger = yes }', 'always = yes')))

    def test_dead_imprisoned_other_house_or_self_head(self):
        for guard in ('exists = house_head', 'is_alive = yes', 'is_adult = yes',
                      'is_imprisoned = no', 'house = scope:rw_house_target',
                      'NOT = { this = scope:rw_house_authority.holder }'):
            self.assertIn('wrong or unavailable house head', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_successors_cannot_inherit_old_panel_consent(self):
        for guard in ('exists = scope:rw_title_remedy_ruler', 'exists = scope:rw_title_remedy_head',
                      'scope:rw_house_authority = { holder = scope:rw_title_remedy_ruler }',
                      'scope:rw_house_target = { house_head = scope:rw_title_remedy_head }'):
            self.assertIn('recipient changed under old panel', self.errors(t=self.t.replace(guard, 'always = yes')))
        for alias in ('rw_title_remedy_ruler', 'rw_title_remedy_head'):
            self.assertIn('recipient not captured before dispatch', self.errors(e=self.e.replace('save_scope_as = '+alias, 'save_scope_as = wrong_person')))

    def test_head_cannot_open_rulers_grant_window(self):
        for guard in ('rw_house_current_ruler_trigger = yes', 'this = scope:rw_title_remedy_ruler'):
            self.assertIn('nonruler can grant', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_native_validity_and_direction_are_not_guessed(self):
        for old, new in (('is_character_interaction_valid', 'custom_tooltip'),
                         ('interaction = grant_titles_interaction', 'interaction = revoke_title_interaction'),
                         ('recipient = scope:rw_title_remedy_head', 'recipient = root')):
            self.assertIn('native eligibility bypass or wrong recipient', self.errors(t=self.t.replace(old, new)))

    def test_public_dispatch_and_click_revalidate(self):
        self.assertIn('unguarded review dispatch', self.errors(e=self.e.replace('limit = { rw_title_remedy_can_review_trigger = yes }', 'limit = { always = yes }')))
        self.assertIn('unguarded archive navigation', self.errors(p=self.p.replace('trigger = { rw_title_remedy_can_review_trigger = yes }', 'trigger = { always = yes }')))
        self.assertIn('stale native click', self.errors(v=self.v.replace('limit = { rw_title_remedy_can_open_grant_trigger = yes }', 'limit = { always = yes }')))

    def test_window_cannot_send_select_or_swap_parties(self):
        for old, new in (('actor = root', 'actor = scope:rw_title_remedy_head'),
                         ('recipient = scope:rw_title_remedy_head', 'recipient = root')):
            self.assertIn('wrong native handoff', self.errors(v=self.v.replace(old, new)))
        self.assertIn('native title or terms preselected', self.errors(v=self.v.replace('actor = root', 'actor = root target = title:c_dummy')))
        for effect in ('run_interaction', 'change_title_holder', 'add_gold', 'set_variable', 'days'):
            self.assertIn('navigation mutates state or schedules work', self.errors(v=self.v + '\n'+effect+' = yes'))

    def test_stale_panel_does_not_disclose_new_recipient(self):
        self.assertIn('stale portrait', self.errors(v=self.v.replace('character = scope:rw_title_remedy_head', 'character = scope:rw_house_target.house_head')))
        self.assertIn('stale description', self.errors(v=self.v.replace('trigger = { rw_title_remedy_view_trigger = yes }', 'trigger = { always = yes }', 1)))

    def test_complete_bilingual_terms_and_no_new_ai_gameplay(self):
        keys = set(re.findall(r'(?:name|title|desc)\s*=\s*(rw_title_remedies\.[\w.]+)', self.v+self.p))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_title_remedies_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text = p.read_text(encoding='utf-8-sig')
            for key in keys:
                self.assertRegex(text, r'(?m)^ '+re.escape(key)+r':0 ')
            for ref in ('rw_title_remedy_head', 'rw_title_remedy_ruler', 'rw_house_target', 'rw_house_authority'):
                self.assertIn('['+ref+'.', text)
        self.assertEqual(1, self.v.count('open_interaction_window = {'))
        self.assertNotIn('rw_house_restore_effect', self.e+self.v)
        self.assertNotIn('rw_house_terms_settle_effect', self.e+self.v)
