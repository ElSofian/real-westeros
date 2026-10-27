"""Story storage, access and retention contracts; no engine/persistence simulation."""
from pathlib import Path
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def record_errors(triggers, effects, story, archive):
    errors = []
    identity = block(triggers, 'rw_case_matches_trigger')
    if 'exists = scope:rw_case_record' not in identity or 'story_type = story_rw_political_case' not in identity:
        errors.append('missing typed record identity')
    if 'story_owner = scope:rw_service_provider' not in identity:
        errors.append('record owner not checked')
    opening = block(effects, 'rw_case_open_effect')
    if 'create_story = { type = story_rw_political_case save_scope_as = rw_case_record }' not in opening:
        errors.append('not creating independent record')
    if 'has_character_flag = rw_case_pending' in triggers:
        errors.append('provider-global pending lock remains')
    closing = block(effects, 'rw_case_close_effect')
    if 'scope:rw_case_record = {\n            remove_variable = rw_case_pending' not in closing:
        errors.append('closure not scoped to selected record')
    if 'name = rw_case_retained value = flag:yes days = 1825' not in closing:
        errors.append('closed history retention missing')
    if 'NOT = { has_variable = rw_case_retained }' not in story or 'var:rw_case_stage = flag:closed' not in story:
        errors.append('cleanup can delete active/retained records')
    if 'make_story_owner' in clean_script(story)[0]:
        errors.append('personal guilt inherited')
    reader = block(triggers, 'rw_case_reader_allowed_trigger')
    for comparison in ('story_owner = $READER$', 'var:rw_case_client = $READER$',
                       'var:rw_case_mediator = $READER$'):
        if comparison not in reader:
            errors.append('reader role missing')
    if 'every_owned_story' not in archive or 'limit = { rw_case_reader_allowed_trigger = { READER = scope:rw_case_reader } }' not in archive:
        errors.append('archive not filtered by known records')
    if 'random_owned_story' in archive:
        errors.append('history randomly truncated')
    return errors


class CaseRecordsTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_case_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_case_effects.txt').read_text()
        self.s = (MOD / 'common/story_cycles/rw_political_cases.txt').read_text()
        self.a = (MOD / 'common/scripted_effects/rw_case_archive_effects.txt').read_text()

    def errors(self, t=None, e=None, s=None, a=None):
        return record_errors(self.t if t is None else t, self.e if e is None else e,
                             self.s if s is None else s, self.a if a is None else a)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_untyped_record_mutation(self):
        self.assertIn('missing typed record identity', self.errors(t=self.t.replace('story_type = story_rw_political_case', 'always = yes')))

    def test_wrong_owner_mutation(self):
        self.assertIn('record owner not checked', self.errors(t=self.t.replace('story_owner = scope:rw_service_provider', 'always = yes')))

    def test_single_slot_regression(self):
        self.assertIn('not creating independent record', self.errors(e=self.e.replace('create_story = { type = story_rw_political_case save_scope_as = rw_case_record }', 'save_scope_as = rw_case_record')))

    def test_global_lock_regression(self):
        self.assertIn('provider-global pending lock remains', self.errors(t=self.t + '\nhas_character_flag = rw_case_pending'))

    def test_retained_record_deleted_mutation(self):
        self.assertIn('cleanup can delete active/retained records', self.errors(s=self.s.replace('NOT = { has_variable = rw_case_retained }', 'always = yes')))

    def test_unfiltered_archive_mutation(self):
        self.assertIn('archive not filtered by known records', self.errors(a=self.a.replace('limit = { rw_case_reader_allowed_trigger = { READER = scope:rw_case_reader } }', 'limit = { always = yes }')))

    def test_random_history_regression(self):
        self.assertIn('history randomly truncated', self.errors(a=self.a.replace('every_owned_story', 'random_owned_story')))

    def test_heir_transfer_mutation(self):
        self.assertIn('personal guilt inherited', self.errors(s=self.s + '\nmake_story_owner = player_heir'))

    def test_archive_does_not_settle_or_sanction(self):
        clean, _ = clean_script(self.a)
        self.assertNotRegex(clean, r'\b(add_gold|add_prestige|add_opinion|set_variable|end_story)\s*=')
        event = block((MOD / 'events/rw_case_events.txt').read_text(), 'rw_cases.0006')
        self.assertNotRegex(event, r'\brw_\w+_effect\s*=')

    def test_unique_story_definition_and_passive_lifecycle(self):
        all_scripts = '\n'.join(clean_script(p.read_text(encoding='utf-8-sig'))[0] for p in MOD.rglob('*.txt'))
        import re
        self.assertEqual(1, len(re.findall(r'(?m)^story_rw_political_case\s*=\s*\{', all_scripts)))
        self.assertIn('on_owner_death = { end_story = yes }', self.s)
        self.assertNotRegex(clean_script(self.s)[0], r'\b(add_opinion|add_prestige|add_gold|change_title_holder)\s*=')
        self.assertIn('days = 60', self.s)
        self.assertIn('NOT = { has_variable = rw_case_pending }', self.s)
        self.assertIn('NOT = { var:rw_case_stage = flag:closed }', self.s)

    def test_notices_read_result_from_own_record(self):
        events = (MOD / 'events/rw_case_events.txt').read_text()
        self.assertNotIn('scope:rw_service_provider = { var:rw_case_result', events)
        self.assertIn('scope:rw_case_record = { var:rw_case_result', events)
