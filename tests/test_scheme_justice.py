"""Read-only legal-state source contracts; no CK3 execution or legal simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def assessment_errors(t, v, journal):
    errors = []
    access = block(t, 'rw_scheme_justice_view_trigger')
    for guard in ('rw_scheme_evidence_view_trigger = yes',
                  'var:rw_evidence_kind = flag:participant_exposed',
                  'exists = var:rw_evidence_participant'):
        if guard not in access:
            errors.append('private observation identity bypass')
    living = block(t, 'rw_scheme_justice_living_trigger')
    for guard in ('rw_scheme_justice_view_trigger = yes', 'is_alive = yes',
                  'NOT = { this = scope:rw_scheme_observer }'):
        if guard not in living:
            errors.append('dead or wrong participant assessed')
    for suffix in ('own_custody', 'other_custody', 'free', 'reason', 'no_reason'):
        if 'rw_scheme_justice_living_trigger = yes' not in block(t, f'rw_scheme_justice_{suffix}_trigger'):
            errors.append('stale legal branch')
    reason = block(t, 'rw_scheme_justice_reason_trigger')
    predicate = 'has_imprisonment_reason = scope:rw_scheme_evidence_record.var:rw_evidence_participant'
    if predicate not in reason or 'scope:rw_scheme_evidence_record.var:rw_evidence_participant = {' in reason:
        errors.append('reason read in wrong direction')
    if f'NOT = {{ {predicate} }}' not in block(t, 'rw_scheme_justice_no_reason_trigger'):
        errors.append('missing native reason invented')
    if 'NOT = { is_imprisoned_by = scope:rw_scheme_observer }' not in block(t, 'rw_scheme_justice_other_custody_trigger'):
        errors.append('custody conflated')
    # Only navigation and descriptive predicates are permitted, not state changes.
    scripts = clean_script(t + v)[0]
    if re.search(r'\b(set_variable|remove_variable|add_character_flag|add_gold|add_opinion|imprison|death|consume_imprisonment_reasons|consume_all_criminal_reasons_effect|rightfully_imprison_character_effect|imprison_character_effect|trigger_event|save_scope_as)\s*=', scripts):
        errors.append('assessment changes state or applies penalty')
    if journal.count('limit = { rw_scheme_justice_view_trigger = yes }') != 1:
        errors.append('journal execution guard bypass')
    return errors


class SchemeJusticeTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_scheme_justice_triggers.txt').read_text()
        self.v = (MOD / 'events/rw_scheme_justice_events.txt').read_text()
        self.j = (MOD / 'events/rw_scheme_evidence_events.txt').read_text()

    def test_read_only_contract(self):
        self.assertEqual([], assessment_errors(self.t, self.v, self.j))

    def test_generic_or_foreign_observation_mutations(self):
        for guard in ('rw_scheme_evidence_view_trigger = yes',
                      'var:rw_evidence_kind = flag:participant_exposed',
                      'exists = var:rw_evidence_participant'):
            with self.subTest(guard=guard):
                self.assertIn('private observation identity bypass', assessment_errors(self.t.replace(guard, 'always = yes', 1), self.v, self.j))

    def test_dead_wrong_or_stale_subject_mutations(self):
        for guard in ('is_alive = yes', 'NOT = { this = scope:rw_scheme_observer }'):
            self.assertIn('dead or wrong participant assessed', assessment_errors(self.t.replace(guard, 'always = yes'), self.v, self.j))
        self.assertIn('stale legal branch', assessment_errors(self.t.replace('rw_scheme_justice_living_trigger = yes', 'always = yes', 1), self.v, self.j))

    def test_reason_direction_and_custody_mutations(self):
        self.assertIn('reason read in wrong direction', assessment_errors(self.t.replace('has_imprisonment_reason = scope:rw_scheme_evidence_record.var:rw_evidence_participant', 'has_imprisonment_reason = scope:rw_scheme_observer', 1), self.v, self.j))
        self.assertIn('custody conflated', assessment_errors(self.t.replace('NOT = { is_imprisoned_by = scope:rw_scheme_observer }', 'always = yes'), self.v, self.j))

    def test_no_punishment_consumption_or_cached_judgment(self):
        for effect in ('imprison', 'rightfully_imprison_character_effect', 'consume_imprisonment_reasons', 'set_variable'):
            with self.subTest(effect=effect):
                self.assertIn('assessment changes state or applies penalty', assessment_errors(self.t, self.v + f'\n{effect} = yes', self.j))
        self.assertNotIn('rw_scheme_response_state', self.t + self.v)
        self.assertNotRegex(self.t + self.v, r'\b(scheme_owner|scheme_target_character|every_living_character|every_owned_story)\b')

    def test_navigation_revalidates_and_has_no_ai_schedule(self):
        self.assertIn('journal execution guard bypass', assessment_errors(self.t, self.v, self.j.replace('limit = { rw_scheme_justice_view_trigger = yes }', 'limit = { always = yes }')))
        self.assertIn('rw_scheme_justice.0001', self.j)
        self.assertNotRegex(self.v, r'\b(days|months|years|immediate|after)\s*=')
        self.assertEqual(1, self.v.count('option = {'))

    def test_original_reader_keeps_owner_type_serial_retention_guards(self):
        original = (MOD / 'common/scripted_triggers/rw_scheme_evidence_triggers.txt').read_text()
        reader = block(original, 'rw_scheme_evidence_reader_trigger')
        for guard in ('story_type = story_rw_scheme_evidence', 'story_owner = $READER$', 'var:rw_evidence_schema = 1', 'has_variable = rw_evidence_retained'):
            self.assertIn(guard, reader)
        view = block(original, 'rw_scheme_evidence_view_trigger')
        for guard in ('this = scope:rw_scheme_observer', 'var:rw_evidence_serial = scope:rw_scheme_evidence_serial'):
            self.assertIn(guard, view)

    def test_localization_references_and_no_hidden_names(self):
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_scheme_justice\.[\w.]+)', self.v + self.j))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_scheme_justice_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', text, re.M)))
            self.assertNotIn('[', text)
