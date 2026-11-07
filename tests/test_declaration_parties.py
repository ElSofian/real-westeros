"""Inspect native-callback party snapshots without simulating CK3 scopes."""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_g1_royal_response import block

ROOT = builder.TEMPLATES
EFFECTS = ROOT/'common/scripted_effects/rw_declaration_law_effects.txt'
STORIES = ROOT/'common/story_cycles/rw_declaration_law.txt'


def party_errors(effects, stories):
    errors = []

    def need(source, tokens, label):
        if any(token not in source for token in tokens):
            errors.append(label)

    capture = block(effects, 'rw_dl_capture_effect')
    need(capture, ('name = rw_dl_party_schema value = 1',
                  'limit = { exists = scope:claimant }',
                  'name = rw_dl_claimant value = scope:claimant',
                  'name = rw_dl_claimant_state value = flag:missing',
                  'name = rw_dl_defender_liege value = scope:rw_dl_target.liege',
                  'rw_dl_capture_targets_effect = yes'), 'missing or inferred party')
    if capture.index('rw_dl_capture_targets_effect = yes') < capture.index('name = rw_dl_serial value ='):
        errors.append('title capture precedes parent identity')
    definition = effects[effects.index('\nrw_dl_capture_targets_effect = {'):]
    worker = block(definition, 'rw_dl_capture_targets_effect')
    need(worker, ('rw_dl_callback_context_trigger = yes', 'exists = scope:rw_dl_record',
                  'story_type = story_rw_declaration_law', 'story_owner = scope:rw_dl_actor',
                  'var:rw_dl_schema = 1', 'var:rw_dl_party_schema = 1', 'var:rw_dl_serial > 0',
                  'var:rw_dl_attacker = scope:rw_dl_actor', 'var:rw_dl_defender = scope:defender',
                  'var:rw_dl_war = scope:rw_dl_war',
                  'var:rw_dl_phase = flag:claim_cb_on_declaration_prefix',
                  'var:rw_dl_seen_on = current_date',
                  'NOT = { has_variable = rw_dl_targets_started }'), 'late/foreign/replayed parent')
    need(worker, ('scope:rw_dl_war = {', 'casus_belli = {', 'every_target_title = {', 'save_scope_as = rw_dt_title',
                  'name = rw_dl_target_count value = 0', 'name = rw_dl_target_records value = 0',
                  'name = rw_dl_targets_state value = flag:unavailable',
                  'name = rw_dl_targets_state value = flag:partial',
                  'var:rw_dl_target_count > 0',
                  'var:rw_dl_target_records = var:rw_dl_target_count',
                  'name = rw_dl_targets_state value = flag:all_titles_recorded'), 'partial list treated as complete')
    if worker.index('name = rw_dl_targets_started value = flag:yes') > worker.index('every_target_title = {'):
        errors.append('list observed before consumption')
    for counter in ('rw_dl_target_count', 'rw_dl_target_records'):
        initializer = 'name = '+counter+' value = 0'
        increment = 'name = '+counter+' add = 1'
        if worker.index(initializer) > worker.index(increment):
            errors.append('counter increment before initialization')
    for alias in ('rw_dt_holder', 'rw_dt_liege', 'rw_dt_authority'):
        if 'clear_saved_scope = '+alias not in worker or worker.index('clear_saved_scope = '+alias) > worker.index('holder = {'):
            errors.append('stale title-party alias')
    need(worker, ('var:rw_dt_parent = scope:rw_dl_record',
                  'var:rw_dt_parent_serial = scope:rw_dl_record.var:rw_dl_serial',
                  'var:rw_dt_war = scope:rw_dl_war', 'var:rw_dt_title = scope:rw_dt_title',
                  'clear_saved_scope = rw_dt_record', 'exists = scope:rw_dt_record',
                  'story_type = story_rw_declaration_target', 'story_owner = scope:rw_dl_actor',
                  'NOT = { has_variable = rw_dt_schema }',
                  'name = rw_dt_title value = scope:rw_dt_title',
                  'name = rw_dt_holder_state value = flag:missing',
                  'name = rw_dt_holder value = scope:rw_dt_holder',
                  'name = rw_dt_holder_liege value = scope:rw_dt_liege',
                  'name = rw_dt_holder_authority value = scope:rw_dt_authority'), 'ambiguous title record')
    child = block(stories, 'story_rw_declaration_target')
    need(child, ('on_owner_death = { end_story = yes }', 'days = 30',
                 'exists = var:rw_dt_parent', 'story_type = story_rw_declaration_law',
                 'story_owner = scope:rw_dt_check.story_owner', 'var:rw_dl_schema = 1',
                 'var:rw_dl_serial = scope:rw_dt_check.var:rw_dt_parent_serial',
                 'var:rw_dl_war = scope:rw_dt_check.var:rw_dt_war',
                 'effect = { end_story = yes }'), 'orphan/foreign parent retention')
    if re.search(r'\b(add_to_list|remove_from_list|start_war|end_war|change_title_holder|add_gold|add_opinion|run_interaction|make_story_owner)\s*=',
                 clean_script(effects+stories)[0]):
        errors.append('native state or input list changed')
    return errors


class DeclarationPartyTests(unittest.TestCase):
    def setUp(self):
        self.effects = EFFECTS.read_text(encoding='utf-8-sig')
        self.stories = STORIES.read_text(encoding='utf-8-sig')

    def test_actual_snapshot_source_and_parent_lifetime(self):
        self.assertEqual([], party_errors(self.effects, self.stories))

    def test_missing_claimant_cannot_be_substituted_by_attacker(self):
        changed = self.effects.replace('name = rw_dl_claimant value = scope:claimant',
                                       'name = rw_dl_claimant value = scope:rw_dl_actor')
        self.assertIn('missing or inferred party', party_errors(changed, self.stories))

    def test_foreign_legacy_late_and_replayed_parent_rejected(self):
        for token in ('var:rw_dl_party_schema = 1', 'var:rw_dl_war = scope:rw_dl_war',
                      'var:rw_dl_seen_on = current_date',
                      'NOT = { has_variable = rw_dl_targets_started }'):
            with self.subTest(guard=token):
                self.assertIn('late/foreign/replayed parent',
                              party_errors(self.effects.replace(token, 'always = yes'), self.stories))

    def test_missing_holder_cannot_reuse_previous_title_party(self):
        for alias in ('rw_dt_holder', 'rw_dt_liege', 'rw_dt_authority'):
            with self.subTest(alias=alias):
                self.assertIn('stale title-party alias', party_errors(
                    self.effects.replace('clear_saved_scope = '+alias, ''), self.stories))

    def test_partial_title_capture_cannot_claim_complete(self):
        changed = self.effects.replace('var:rw_dl_target_records = var:rw_dl_target_count',
                                       'var:rw_dl_target_records > 0')
        self.assertIn('partial list treated as complete', party_errors(changed, self.stories))

    def test_target_counters_start_before_the_first_increment(self):
        for counter in ('rw_dl_target_count', 'rw_dl_target_records'):
            initializer = 'set_variable = { name = '+counter+' value = 0 }'
            increment = 'change_variable = { name = '+counter+' add = 1 }'
            changed = self.effects.replace(initializer, '').replace(increment, increment+' '+initializer)
            with self.subTest(counter=counter):
                self.assertIn('counter increment before initialization', party_errors(changed, self.stories))

    def test_child_requires_exact_parent_owner_serial_and_war(self):
        for token in ('story_owner = scope:rw_dt_check.story_owner',
                      'var:rw_dl_serial = scope:rw_dt_check.var:rw_dt_parent_serial',
                      'var:rw_dl_war = scope:rw_dt_check.var:rw_dt_war'):
            with self.subTest(guard=token):
                self.assertIn('orphan/foreign parent retention', party_errors(
                    self.effects, self.stories.replace(token, 'always = yes')))

    def test_no_target_cap_random_selection_native_mutation_or_new_response(self):
        definition = self.effects[self.effects.index('\nrw_dl_capture_targets_effect = {'):]
        worker = block(definition, 'rw_dl_capture_targets_effect')
        for operation in ('random_in_list', 'ordered_in_list', 'max =', 'trigger_event',
                          'every_living_character', 'every_ruler'):
            self.assertNotIn(operation, worker)
        changed = self.effects+'\n synthetic_bad_effect = { add_to_list = target_titles }'
        self.assertIn('native state or input list changed', party_errors(changed, self.stories))
