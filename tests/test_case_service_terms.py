"""Adversarial source checks for historical promise terms; no CK3 simulation."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'
FIELDS = ('revision', 'price', 'delivery_days', 'mode', 'service', 'recorded_on')


def terms_errors(obligation, effects, triggers, case):
    errors = []
    receipt = block(obligation, 'rw_service_record_receipt_effect')
    clear = receipt.find('rw_service_clear_receipt_terms_effect = yes')
    first_write = receipt.find('name = rw_service_last_serial')
    if not 0 <= clear < first_write:
        errors.append('previous receipt certificate survives replacement')
    for guard in ('rw_service_obligation_matches_trigger = yes',
                  'rw_service_deferred_trigger = yes', 'exists = scope:rw_service_delivery_days',
                  'has_variable = rw_service_delivery_days',
                  'var:rw_service_delivery_days = scope:rw_service_delivery_days'):
        if guard not in receipt:
            errors.append('uncertain legacy terms certified')
    stamp = receipt.find('name = rw_service_last_terms_schema value = 1')
    for field in ('revision', 'mode', 'service', 'recorded_on'):
        if not 0 <= receipt.find('name = rw_service_last_' + field) < stamp:
            errors.append('incomplete receipt certified')
    reset = block(effects, 'rw_service_clear_receipt_terms_effect')
    for field in ('terms_schema', 'revision', 'mode', 'service', 'recorded_on'):
        if 'remove_variable = rw_service_last_' + field not in reset:
            errors.append('stale receipt metadata survives reset')
    if 'rw_service_clear_receipt_terms_effect = yes' not in block(obligation, 'rw_service_cancel_promise_effect'):
        errors.append('neutral cancellation inherits prior terms')
    capture = block(effects, 'rw_case_capture_service_terms_effect')
    for guard in ('rw_case_can_open_trigger = yes', 'story_type = story_rw_political_case',
                  'story_owner = scope:rw_service_provider', 'var:rw_case_kind = flag:service',
                  'var:rw_case_serial = scope:rw_service_serial',
                  'var:rw_case_client = scope:rw_service_client',
                  'NOT = { has_variable = rw_case_terms_schema }',
                  'rw_service_receipt_terms_trigger = yes',
                  'var:rw_service_last_serial = scope:rw_service_serial',
                  'var:rw_service_last_client = scope:rw_service_client'):
        if guard not in capture:
            errors.append('foreign or repeated receipt copied')
    stamp = capture.find('name = rw_case_terms_schema value = 1')
    for field in FIELDS:
        target = 'kind' if field == 'service' else field
        assignment = f'name = rw_case_service_{target} value = scope:rw_service_provider.var:rw_service_last_{field}'
        if not 0 <= capture.find(assignment) < stamp:
            errors.append('case copies live or incomplete terms')
    opening = block(case, 'rw_case_open_effect')
    if not 0 <= opening.find('clear_saved_scope = rw_case_record') < opening.find('create_story'):
        errors.append('nonfresh case overwritten')
    for guard in ('story_type = story_rw_political_case', 'story_owner = scope:rw_service_provider',
                  'NOT = { has_variable = rw_case_serial }'):
        if guard not in opening:
            errors.append('nonfresh case overwritten')
    copied = opening.find('rw_case_capture_service_terms_effect = yes')
    consumed = opening.find('name = rw_service_reacted_serial')
    notice = opening.find('id = rw_cases.0001')
    if not 0 <= copied < consumed < notice:
        errors.append('terms captured after consumption or disclosure')
    reader = block(triggers, 'rw_case_can_read_service_terms_trigger')
    for guard in ('rw_case_matches_trigger = yes', 'is_alive = yes', 'var:rw_case_kind = flag:service',
                  'rw_case_reader_allowed_trigger = { READER = root }'):
        if guard not in reader:
            errors.append('unrelated reader sees clauses')
    code = clean_script(effects)[0]
    if re.search(r'\b(add_gold|add_prestige|add_opinion|trigger_event|end_story|create_story|add_character_flag)\s*=', code):
        errors.append('term copying changes gameplay')
    if re.search(r'\bname\s*=\s*rw_(?:service_(?!last_)|case_(?:pending|stage|result|retained))', code):
        errors.append('term copying changes original clocks or outcome')
    return errors


class CaseServiceTermsTests(unittest.TestCase):
    def setUp(self):
        self.o = (MOD/'common/scripted_effects/rw_obligation_effects.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_case_terms_effects.txt').read_text()
        self.t = (MOD/'common/scripted_triggers/rw_case_terms_triggers.txt').read_text()
        self.c = (MOD/'common/scripted_effects/rw_case_effects.txt').read_text()
        self.v = (MOD/'events/rw_case_terms_events.txt').read_text()

    def errors(self, o=None, e=None, t=None, c=None):
        return terms_errors(self.o if o is None else o, self.e if e is None else e,
                            self.t if t is None else t, self.c if c is None else c)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_replacing_receipt_invalidates_old_certificate_first(self):
        self.assertIn('previous receipt certificate survives replacement',
                      self.errors(o=self.o.replace('rw_service_clear_receipt_terms_effect = yes', '')))
        receipt = block(self.o, 'rw_service_record_receipt_effect')
        self.assertIn('name = rw_service_last_price value = scope:rw_service_price', receipt)
        for name in ('rw_service_fulfill_promise_effect', 'rw_service_record_breach_effect'):
            b = block(self.o, name)
            self.assertLess(b.index('rw_service_record_receipt_effect = yes'), b.index('rw_service_clear_effect = yes'))
        cancel = (MOD/'common/scripted_effects/rw_cancellation_effects.txt').read_text()
        b = block(cancel, 'rw_cancel_accept_effect')
        self.assertLess(b.index('rw_service_record_receipt_effect = yes'), b.index('rw_service_clear_effect = yes'))

    def test_unknown_legacy_terms_cannot_receive_current_certificate(self):
        for guard in ('rw_service_obligation_matches_trigger = yes', 'rw_service_deferred_trigger = yes',
                      'exists = scope:rw_service_delivery_days', 'has_variable = rw_service_delivery_days',
                      'var:rw_service_delivery_days = scope:rw_service_delivery_days'):
            self.assertIn('uncertain legacy terms certified', self.errors(o=self.o.replace(guard, 'always = yes')))
        self.assertIn('incomplete receipt certified',
                      self.errors(o=self.o.replace('name = rw_service_last_recorded_on', 'name = removed_date')))

    def test_neutral_orphan_cancellation_removes_typed_metadata(self):
        for field in ('terms_schema', 'revision', 'mode', 'service', 'recorded_on'):
            self.assertIn('stale receipt metadata survives reset',
                          self.errors(e=self.e.replace('remove_variable = rw_service_last_' + field, 'always = yes')))
        cancel = block(self.o, 'rw_service_cancel_promise_effect')
        changed = self.o.replace(cancel, cancel.replace('rw_service_clear_receipt_terms_effect = yes', ''))
        self.assertIn('neutral cancellation inherits prior terms', self.errors(o=changed))

    def test_copy_requires_exact_breach_receipt_and_unconsumed_response(self):
        for guard in ('rw_case_can_open_trigger = yes', 'rw_service_receipt_terms_trigger = yes',
                      'var:rw_service_last_serial = scope:rw_service_serial',
                      'var:rw_service_last_client = scope:rw_service_client'):
            self.assertIn('foreign or repeated receipt copied', self.errors(e=self.e.replace(guard, 'always = yes')))

    def test_copy_cannot_overwrite_other_case_or_refresh_existing_snapshot(self):
        for guard in ('story_type = story_rw_political_case', 'story_owner = scope:rw_service_provider',
                      'var:rw_case_kind = flag:service', 'var:rw_case_serial = scope:rw_service_serial',
                      'var:rw_case_client = scope:rw_service_client', 'NOT = { has_variable = rw_case_terms_schema }'):
            self.assertIn('foreign or repeated receipt copied', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertIn('nonfresh case overwritten', self.errors(c=self.c.replace('NOT = { has_variable = rw_case_serial }', 'always = yes')))
        self.assertIn('nonfresh case overwritten', self.errors(c=self.c.replace('clear_saved_scope = rw_case_record', '')))

    def test_snapshot_uses_terminal_agreed_terms_never_current_contract(self):
        for field in FIELDS:
            self.assertIn('case copies live or incomplete terms',
                          self.errors(e=self.e.replace('scope:rw_service_provider.var:rw_service_last_' + field,
                                                       'scope:rw_service_provider.var:rw_service_' + field)))
        capture = block(self.e, 'rw_case_capture_service_terms_effect')
        self.assertNotRegex(capture, r'value\s*=\s*scope:rw_service_(?:price|revision|delivery_days)\b')

    def test_referral_copies_before_consumption_and_notification(self):
        self.assertIn('terms captured after consumption or disclosure',
                      self.errors(c=self.c.replace('rw_case_capture_service_terms_effect = yes', '')))
        scripts = '\n'.join(clean_script(p.read_text())[0] for p in MOD.rglob('*.txt'))
        self.assertEqual(1, len(re.findall(r'\brw_case_capture_service_terms_effect\s*=\s*yes', scripts)))
        # No archive callback, timer, allegation or current ruler can backfill old clauses.
        self.assertNotIn('rw_case_capture_service_terms_effect', (MOD/'common/scripted_effects/rw_case_archive_effects.txt').read_text())

    def test_reading_requires_original_known_participant_and_complete_case_identity(self):
        for guard in ('rw_case_matches_trigger = yes', 'is_alive = yes', 'var:rw_case_kind = flag:service',
                      'rw_case_reader_allowed_trigger = { READER = root }'):
            self.assertIn('unrelated reader sees clauses', self.errors(t=self.t.replace(guard, 'always = yes')))
        reader = block((MOD/'common/scripted_triggers/rw_case_triggers.txt').read_text(), 'rw_case_reader_allowed_trigger')
        self.assertIn('var:rw_case_mediator = $READER$ rw_case_disclosed_trigger = yes', reader)

    def test_typed_validation_rejects_missing_kind_schema_and_unknown_values(self):
        for name, prefix, kind in (('rw_service_receipt_terms_trigger', 'rw_service_last_', 'service'),
                                    ('rw_case_service_terms_trigger', 'rw_case_service_', 'kind')):
            b = block(self.t, name)
            self.assertIn(f'var:{prefix}{kind} = flag:endorsement', b)
            self.assertIn(f'var:{prefix}mode = flag:deferred', b)
            for field in ('revision', 'recorded_on'):
                self.assertIn('has_variable = ' + prefix + field, b)
            for field, values in (('price', (25, 50)), ('delivery_days', (14, 30))):
                for value in values:
                    self.assertRegex(b, rf'\bvar:{prefix}{field}\s*=\s*{value}\b')
            self.assertIn('terms_schema = 1', b)
        self.assertIn('story_type = story_rw_political_case', block(self.t, 'rw_case_service_terms_trigger'))

    def test_read_only_panel_rechecks_and_uses_frozen_story_not_latest_receipt(self):
        self.assertIn('rw_case_can_read_service_terms_trigger = yes', self.v)
        self.assertIn('scope:rw_case_record = { rw_case_service_terms_trigger = yes }', self.v)
        self.assertIn('desc = rw_case_terms.unknown', self.v)
        self.assertIn('desc = rw_case_terms.unavailable', self.v)
        self.assertNotRegex(clean_script(self.v)[0], r'\b(?:immediate|after|rw_\w+_effect|set_variable|add_gold|add_opinion|trigger_event)\s*=')
        self.assertNotIn('var:rw_service_', self.v)
        self.assertNotIn('scope:rw_service_price', self.v)
        for number in (1,2,3,5,6):
            event = block((MOD/'events/rw_case_events.txt').read_text(), f'rw_cases.{number:04}')
            option = event[event.index('name = rw_case_terms.read'):]
            self.assertGreaterEqual(option.count('rw_case_can_read_service_terms_trigger = yes'), 2)
            self.assertIn('trigger_event = { id = rw_case_terms.0001 }', option)
            self.assertIn('ai_chance = { base = 0 }', option)

    def test_terms_change_neither_native_effects_outcomes_nor_clocks(self):
        for injection in ('add_gold = 25', 'add_opinion = { target = root modifier = bad }',
                          'trigger_event = { id = rw_cases.0001 }', 'add_character_flag = rw_service_deadline'):
            self.assertIn('term copying changes gameplay', self.errors(e=self.e + '\n' + injection))
        for variable in ('rw_service_price', 'rw_case_pending', 'rw_case_result', 'rw_case_retained'):
            self.assertIn('term copying changes original clocks or outcome',
                          self.errors(e=self.e + f'\nset_variable = {{ name = {variable} value = 50 }}'))

    def test_all_copied_clause_writes_are_owned_by_the_single_capture_helper(self):
        all_code = '\n'.join(clean_script(p.read_text())[0] for p in MOD.rglob('*.txt'))
        for field in ('revision', 'price', 'delivery_days', 'mode', 'kind', 'recorded_on'):
            self.assertEqual(1, len(re.findall(r'\bname\s*=\s*rw_case_service_' + field + r'\b', all_code)))
        self.assertEqual(1, len(re.findall(r'\bname\s*=\s*rw_case_terms_schema\b', all_code)))

    def test_localized_clauses_and_unknown_data_explanations_exist(self):
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_case_terms\.[\w.]+)', self.v)) | {'rw_case_terms.read'}
        for lang in ('english', 'french'):
            p = MOD/f'localization/{lang}/rw_case_terms_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertTrue(keys <= actual, keys - actual)
