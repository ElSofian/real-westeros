"""Source and arithmetic checks only. Native flag expiry awaits the campaign."""

import hashlib
import json
from pathlib import Path
import re
import unittest

from test_deferred_service_contract import block
from test_political_ai import option
from test_gold_effects import restore_later_updates
from tools.audit_trait_context import read_traits
from tools.validate_mod import clean_script


MOD = Path(__file__).resolve().parents[1]/'mod/real_westeros'
TIMING_FIELDS = ('rw_service_ai_timing_serial', 'rw_service_ai_wait_room',
                 'rw_fd_ai_timing_serial', 'rw_fd_ai_later_prompt')


def timing_guard_errors(text):
    errors = []
    for family, pending, provider, serial, marker, room in (
        ('gold', 'rw_service_obligation_actionable_trigger', 'rw_service_provider',
         'rw_service_serial', 'rw_service_ai_timing_serial', 'rw_service_ai_wait_room'),
        ('favor', 'rw_fd_due_trigger', 'rw_fv_provider',
         'rw_fv_serial', 'rw_fd_ai_timing_serial', 'rw_fd_ai_later_prompt'),
    ):
        body = block(text, 'rw_ai_'+family+'_promise_urgent_trigger')
        required = ('rw_ai_'+family+'_promise_context_trigger = yes', pending+' = yes',
                    'scope:'+provider, 'limit = { has_variable = '+marker+' }',
                    'var:'+marker+' = scope:'+serial, 'NOT = { has_character_flag = '+room+' }')
        if any(fragment not in body for fragment in required) or body.count('trigger_else = { always = no }') != 2:
            errors.append(family)
    return errors


class PromiseTimingPolicyTests(unittest.TestCase):
    def setUp(self):
        self.values = (MOD/'common/script_values/rw_promise_ai_values.txt').read_text(encoding='utf-8-sig')
        self.triggers = (MOD/'common/scripted_triggers/rw_political_ai_triggers.txt').read_text(encoding='utf-8-sig')

    def test_energy_factors_are_opposed_bounded_and_read_only(self):
        for name in ('rw_ai_prompt_action_factor', 'rw_ai_deliberate_delay_factor'):
            body = block(self.values, name)
            for fragment in ('value = ai_energy', 'divide = 200', 'add = 1', 'min = 0.5', 'max = 1.5'):
                self.assertIn(fragment, body)
            self.assertNotIn('scope:', body)
        self.assertIn('multiply = -1', block(self.values, 'rw_ai_deliberate_delay_factor'))
        self.assertNotIn('multiply = -1', block(self.values, 'rw_ai_prompt_action_factor'))

    def test_missing_foreign_early_and_expired_timing_cannot_create_urgency(self):
        self.assertEqual([], timing_guard_errors(self.triggers))
        for fragment in ('var:rw_service_ai_timing_serial = scope:rw_service_serial',
                         'limit = { has_variable = rw_fd_ai_timing_serial }',
                         'rw_service_obligation_actionable_trigger = yes', 'rw_fd_due_trigger = yes'):
            changed = self.triggers.replace(fragment, 'always = yes', 1)
            self.assertTrue(timing_guard_errors(changed))

    def test_acceptance_clocks_match_existing_wait_and_prompt_schedules(self):
        gold = (MOD/'common/scripted_effects/rw_obligation_effects.txt').read_text(encoding='utf-8-sig')
        accept = block(gold, 'rw_service_accept_promise_effect')
        for fragment in ('name = rw_service_ai_timing_serial value = var:rw_service_serial',
                         'flag = rw_service_ai_wait_room days = 7',
                         'flag = rw_service_ai_wait_room days = 23',
                         'flag = rw_service_deadline days = 14',
                         'flag = rw_service_deadline days = 30'):
            self.assertIn(fragment, accept)
        self.assertIn('rw_service_schedule_decision_effect = { DAYS = 7 }', block(gold, 'rw_service_wait_promise_effect'))
        favor = (MOD/'common/scripted_effects/rw_deferred_favor_effects.txt').read_text(encoding='utf-8-sig')
        accept = block(favor, 'rw_fd_accept_effect')
        for fragment in ('name = rw_fd_ai_timing_serial value = var:rw_fv_serial',
                         'flag = rw_fd_ai_later_prompt days = 22',
                         'id = rw_deferred_favor.0002 days = 8',
                         'id = rw_deferred_favor.0002 days = 22'):
            self.assertIn(fragment, accept)

    def test_urgency_prefers_available_performance_without_pressuring_blocked_execution(self):
        for family, guard in (('gold', 'rw_service_obligation_fulfillable_trigger'), ('favor', 'rw_fd_can_perform_trigger')):
            perform = block(self.values, 'rw_ai_'+family+'_promise_perform_weight')
            self.assertIn('multiply = rw_ai_prompt_action_factor', perform)
            self.assertIn('rw_ai_'+family+'_promise_urgent_trigger = yes } multiply = 1.5', perform)
            wait_name = 'rw_ai_gold_promise_wait_weight' if family == 'gold' else 'rw_ai_favor_promise_leave_weight'
            wait = block(self.values, wait_name)
            self.assertIn('multiply = rw_ai_deliberate_delay_factor', wait)
            self.assertIn('limit = { '+guard+' = yes rw_ai_'+family+'_promise_urgent_trigger = yes }', wait)
            self.assertIn('multiply = 0.25', wait)
        # Breach remains its own choice, without a new urgency multiplier.
        for name in ('rw_ai_gold_promise_break_weight', 'rw_ai_favor_promise_renounce_weight'):
            self.assertNotIn('urgent_trigger', block(self.values, name))

    def test_leave_retains_a_positive_safe_exit_outside_current_provider_promises(self):
        leave = block(self.values, 'rw_ai_favor_promise_leave_weight')
        self.assertTrue(leave.strip().startswith('value = 30'))
        self.assertIn('rw_fd_pending_trigger = yes this = scope:rw_fv_provider', leave)
        self.assertNotIn('value = 0', leave)
        gold = (MOD/'events/rw_obligation_events.txt').read_text(encoding='utf-8-sig')
        favor = (MOD/'events/rw_favor_service_events.txt').read_text(encoding='utf-8-sig')
        for text, name, value in ((gold, 'rw_obligations.wait', 'rw_ai_gold_promise_wait_weight'),
                                  (favor, 'rw_favor_service.leave', 'rw_ai_favor_promise_leave_weight')):
            self.assertIn('add = '+value, block(option(text, name), 'ai_chance'))

    def test_timing_metadata_is_the_only_effect_change(self):
        expected = {
            'rw_obligation_effects.txt': '4e4400701a67d5e80bb70639f44a848d2baf9bddbc1c57457f194a67ad70ee48',
            'rw_service_effects.txt': '235a67613fbb185fe808bc4cba222a8e24f9ba510c6616aab4a6213912f1f431',
            'rw_deferred_favor_effects.txt': '2e17cf4e011309d24a4c18821e2cbcba357f9cd019395cdc4441db97d35bfd79',
            'rw_favor_service_effects.txt': '50a400cc2569f63585cfb3d5ded282fef5e42224cf146a370e67fa9c673918c0',
        }
        receipt = MOD.parents[1]/'docs/GOLD_DEBIT_SOURCE_RECEIPT.json'
        all_updates = json.loads(receipt.read_text())['subsequent_updates']
        last_timing = max(i for i,row in enumerate(all_updates) if row.get('reason') == 'RW-010 promise timing metadata, reversible source-only addition')
        later_updates = all_updates[last_timing+1:]
        for filename, digest in expected.items():
            path = MOD/'common/scripted_effects'/filename
            relative = path.relative_to(MOD.parents[1]).as_posix()
            raw = restore_later_updates(path.read_bytes(), relative, later_updates)
            text = raw.decode('utf-8-sig')
            restored = '\n'.join(line for line in text.splitlines() if not any(field in line for field in TIMING_FIELDS))
            restored = re.sub(r'\s+', '', clean_script(restored)[0])
            self.assertEqual(digest, hashlib.sha256(restored.encode()).hexdigest(), filename)
        service = (MOD/'common/scripted_effects/rw_service_effects.txt').read_text(encoding='utf-8-sig')
        favor = (MOD/'common/scripted_effects/rw_deferred_favor_effects.txt').read_text(encoding='utf-8-sig')
        for body, field, flag in ((block(service, 'rw_service_clear_effect'), TIMING_FIELDS[0], TIMING_FIELDS[1]),
                                  (block(favor, 'rw_fd_finish_effect'), TIMING_FIELDS[2], TIMING_FIELDS[3])):
            self.assertIn('remove_variable = '+field, body)
            self.assertIn('remove_character_flag = '+flag, body)

    def test_arithmetic_keeps_choices_positive_and_timing_horizons_consistent(self):
        # Isolated policy arithmetic, not a simulation of CK3 flag expiration.
        for energy in (-200, -10, 0, 10, 200):
            action = min(1.5, max(.5, 1+energy/200))
            delay = min(1.5, max(.5, 1-energy/200))
            self.assertGreater(70*action*1.5, 0)
            self.assertGreater(20*delay*.25, 0)
        self.assertEqual(7, 14-7)
        self.assertEqual(23, 30-7)
        for fields, action, wait in (('ai_energy = -10', 'nonincreasing', 'nondecreasing'),
                                     ('ai_energy = 10', 'nondecreasing', 'nonincreasing')):
            row, = read_traits('example = { '+fields+' }', 'CK3', 'traits.txt')
            self.assertEqual(action, row['promise_axis_review']['gold_perform'])
            self.assertEqual(wait, row['promise_axis_review']['gold_wait'])


if __name__ == '__main__':
    unittest.main()
