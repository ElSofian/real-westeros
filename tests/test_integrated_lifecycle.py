"""Source contracts for reminder fan-out and independent lifecycle ownership."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import definitions
from collections import Counter

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def reminder_errors(triggers, decisions, obligations, events, cleanup):
    errors = []
    actionable = block(triggers, 'rw_service_obligation_actionable_trigger')
    for guard in ('rw_service_obligation_due_trigger = yes', 'rw_service_decision_matches_trigger = yes',
                  'has_character_flag = rw_service_decision_open'):
        if guard not in actionable:
            errors.append('obsolete decision can act')
    identity = block(triggers, 'rw_service_decision_matches_trigger')
    if 'exists = scope:rw_service_decision_serial' not in identity or 'var:rw_service_decision_serial = scope:rw_service_decision_serial' not in identity:
        errors.append('decision ticket is not checked')
    refresh = block(decisions, 'rw_service_refresh_decision_effect')
    for required in ('change_variable = { name = rw_service_decision_serial add = 1 }',
                     'remove_character_flag = rw_service_reminder_pending',
                     'remove_character_flag = rw_service_decision_open'):
        if required not in refresh:
            errors.append('previous decision or reminder remains current')
    schedule = block(decisions, 'rw_service_schedule_decision_effect')
    for guard in ('rw_service_obligation_live_trigger = yes', 'this = scope:rw_service_provider', 'has_character_flag = rw_service_deadline'):
        if guard not in schedule:
            errors.append('invalid contract can schedule')
    for name in ('rw_service_schedule_decision_effect', 'rw_service_open_decision_effect'):
        body = block(decisions, name)
        if not 0 <= body.find('rw_service_refresh_decision_effect = yes') < body.find('trigger_event'):
            errors.append('event dispatched before new identity')
    dispatcher = block(events, 'rw_obligations.0004')
    for guard in ('rw_service_obligation_due_trigger = yes', 'rw_service_decision_matches_trigger = yes', 'has_character_flag = rw_service_reminder_pending'):
        if guard not in dispatcher:
            errors.append('stale reminder can display')
    if not 0 <= dispatcher.find('remove_character_flag = rw_service_reminder_pending') < dispatcher.find('trigger_event'):
        errors.append('duplicate reminder can display twice')
    if 'rw_service_schedule_decision_effect = { DAYS = 7 }' not in block(obligations, 'rw_service_wait_promise_effect'):
        errors.append('wait bypasses ticket scheduler')
    if re.search(r'id\s*=\s*rw_obligations\.0001\s+days', decisions + obligations):
        errors.append('visible reminders bypass hidden dispatcher')
    if 'remove_variable = rw_service_decision_serial' in cleanup:
        errors.append('decision identity reset')
    for flag in ('rw_service_reminder_pending', 'rw_service_decision_open'):
        if 'remove_character_flag = ' + flag not in block(cleanup, 'rw_service_clear_effect'):
            errors.append('terminal outcome leaves decision live')
    return errors


class IntegratedLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_service_triggers.txt').read_text()
        self.d = (MOD / 'common/scripted_effects/rw_service_decision_effects.txt').read_text()
        self.o = (MOD / 'common/scripted_effects/rw_obligation_effects.txt').read_text()
        self.v = (MOD / 'events/rw_obligation_events.txt').read_text()
        self.s = (MOD / 'common/scripted_effects/rw_service_effects.txt').read_text()

    def errors(self, t=None, d=None, o=None, v=None, s=None):
        return reminder_errors(self.t if t is None else t, self.d if d is None else d,
                               self.o if o is None else o, self.v if v is None else v,
                               self.s if s is None else s)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_reopened_or_consumed_popup_mutations(self):
        for guard in ('rw_service_decision_matches_trigger = yes', 'has_character_flag = rw_service_decision_open'):
            with self.subTest(guard=guard):
                self.assertIn('obsolete decision can act', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_missing_or_wrong_ticket_mutations(self):
        for guard in ('exists = scope:rw_service_decision_serial', 'var:rw_service_decision_serial = scope:rw_service_decision_serial'):
            with self.subTest(guard=guard):
                self.assertIn('decision ticket is not checked', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_refresh_does_not_retain_old_branch_mutations(self):
        for guard in ('change_variable = { name = rw_service_decision_serial add = 1 }',
                      'remove_character_flag = rw_service_reminder_pending', 'remove_character_flag = rw_service_decision_open'):
            with self.subTest(guard=guard):
                self.assertIn('previous decision or reminder remains current', self.errors(d=self.d.replace(guard, '')))

    def test_stale_hidden_callback_mutations(self):
        for guard in ('rw_service_obligation_due_trigger = yes', 'rw_service_decision_matches_trigger = yes', 'has_character_flag = rw_service_reminder_pending'):
            with self.subTest(guard=guard):
                self.assertIn('stale reminder can display', self.errors(v=self.v.replace(guard, 'always = yes')))
        self.assertIn('duplicate reminder can display twice', self.errors(v=self.v.replace('remove_character_flag = rw_service_reminder_pending', '')))

    def test_dead_or_overdue_contract_cannot_schedule_mutations(self):
        for guard in ('rw_service_obligation_live_trigger = yes', 'this = scope:rw_service_provider', 'has_character_flag = rw_service_deadline'):
            with self.subTest(guard=guard):
                self.assertIn('invalid contract can schedule', self.errors(d=self.d.replace(guard, 'always = yes')))

    def test_wait_cannot_create_unversioned_reminder_mutation(self):
        o = self.o.replace('rw_service_schedule_decision_effect = { DAYS = 7 }', 'trigger_event = { id = rw_obligations.0001 days = 7 }')
        self.assertIn('wait bypasses ticket scheduler', self.errors(o=o))
        self.assertIn('visible reminders bypass hidden dispatcher', self.errors(o=o))

    def test_terminal_cleanup_and_counter_reset_mutations(self):
        self.assertIn('terminal outcome leaves decision live', self.errors(s=self.s.replace('remove_character_flag = rw_service_decision_open', '')))
        self.assertIn('decision identity reset', self.errors(s=self.s + '\nremove_variable = rw_service_decision_serial'))

    def test_review_rotates_identity_without_scheduling_more_reminders(self):
        review = (MOD / 'common/character_interactions/rw_obligation_interactions.txt').read_text()
        self.assertIn('rw_service_open_decision_effect = yes', review)
        self.assertNotIn('id = rw_obligations.0001', review)
        opened = block(self.d, 'rw_service_open_decision_effect')
        self.assertIn('rw_service_obligation_due_trigger = yes', opened)
        self.assertIn('add_character_flag = rw_service_decision_open', opened)
        self.assertNotIn('rw_service_schedule_decision_effect', opened)
        self.assertNotRegex(opened, r'\bdays\s*=')

    def test_all_provider_choices_share_current_decision_guard(self):
        for effect in ('rw_service_wait_promise_effect', 'rw_service_break_promise_effect'):
            self.assertIn('rw_service_obligation_actionable_trigger = yes', block(self.o, effect))
        self.assertIn('rw_service_obligation_actionable_trigger = yes', block(self.t, 'rw_service_obligation_fulfillable_trigger'))
        cancel = (MOD / 'common/scripted_effects/rw_cancellation_effects.txt').read_text()
        self.assertIn('rw_service_obligation_actionable_trigger = yes', block(cancel, 'rw_cancel_provider_propose_effect'))
        provider = block(self.v, 'rw_obligations.0001')
        proposal = provider[provider.index('name = rw_cancellations.propose'):provider.index('name = rw_obligations.wait')]
        self.assertIn('rw_service_obligation_actionable_trigger = yes', proposal)

    def test_timeout_consent_and_case_records_do_not_depend_on_popup_ticket(self):
        self.assertNotIn('rw_service_decision', block(self.o, 'rw_service_timeout_effect'))
        cancel_triggers = (MOD / 'common/scripted_triggers/rw_cancellation_triggers.txt').read_text()
        self.assertNotIn('rw_service_decision', cancel_triggers)
        for name in ('rw_case_effects.txt', 'rw_case_archive_effects.txt', 'rw_repair_effects.txt'):
            self.assertNotIn('rw_service_decision', (MOD / 'common/scripted_effects' / name).read_text())
        self.assertNotIn('rw_service_revision', self.d)
        self.assertNotRegex(self.d, r'flag = rw_service_(?:deadline|not_due)\s+days')
        acceptance = block(self.o, 'rw_service_accept_promise_effect')
        self.assertIn('rw_service_schedule_decision_effect = { DAYS = 8 }', acceptance)
        self.assertIn('id = rw_obligations.0002 days = 31', acceptance)

    def test_no_duplicate_public_script_definitions_across_slices(self):
        counts = Counter(name for p in MOD.rglob('*.txt')
                         for name in definitions(p.read_text(encoding='utf-8-sig'))
                         if name.startswith(('rw_', 'story_rw_')))
        self.assertEqual({}, {name: count for name, count in counts.items() if count > 1})

    def test_duplicate_event_and_story_are_not_hidden_by_reference_sets(self):
        for name in ('rw_obligations.0001', 'story_rw_political_case'):
            with self.subTest(name=name):
                texts = [p.read_text(encoding='utf-8-sig') for p in MOD.rglob('*.txt')]
                texts.append(name + ' = { }')
                counts = Counter(n for text in texts for n in definitions(text))
                self.assertEqual(2, counts[name])
