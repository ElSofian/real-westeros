"""PRIVATE native callback byte preservation and guarded target transport.

No test here executes CK3 or asserts propagation into the native event.
"""
import unittest

from tools import build_g1_native_choice as builder
from test_g1_royal_response import block


class NativeTargetBindingTests(unittest.TestCase):
    def setUp(self):
        root = builder.TEMPLATES / 'common'
        self.effects = (root/'scripted_effects/rw_unlawful_war_intervention_effects.txt').read_text(encoding='utf-8-sig')
        self.triggers = (root/'scripted_triggers/rw_unlawful_war_choice_triggers.txt').read_text(encoding='utf-8-sig')

    def test_private_prefix_restores_native_bytes_including_crlf_and_comments(self):
        native = 'stop_attacker_vassal_war_interaction = {\r\n on_accept = { # é\r\n synthetic_native_event = yes\r\n }\r\n}'
        original, patched = builder.patch_native_intervention(('unrelated = {}\n'+native+'\nother = {}').encode())
        self.assertEqual(native.encode(), original)
        self.assertEqual(original, patched.replace(builder.INTERVENTION_PREFIX.encode(), b'', 1))
        self.assertLess(patched.index(builder.INTERVENTION_PREFIX.encode()), patched.index(b'synthetic_native_event'))
        self.assertNotIn(b'unrelated', patched)

    def test_double_patch_missing_or_ambiguous_callback_refused(self):
        native = b'stop_attacker_vassal_war_interaction = { on_accept = {} }'
        _, patched = builder.patch_native_intervention(native)
        for invalid in (patched, b'stop_attacker_vassal_war_interaction = {}',
                        b'stop_attacker_vassal_war_interaction = { on_accept = {} on_accept = {} }'):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    builder.patch_native_intervention(invalid)

    def test_old_adapter_cannot_queue_or_send_unsupported_transport(self):
        self.assertIn('rw_uw_native_target_adapter_available_trigger = { always = no }', self.triggers)
        for name in ('rw_uw_can_queue_native_trigger', 'rw_uw_can_send_native_trigger'):
            self.assertIn('rw_uw_native_target_adapter_available_trigger = yes', block(self.triggers, name))
        self.assertIn('always = yes', builder.INTERVENTION_MARKER)

    def test_sender_transport_is_temporary_and_follows_consumed_receipt(self):
        dispatch = block(self.effects, 'rw_uw_send_native_effect')
        marker = 'set_variable = { name = rw_uw_native_send_record value = scope:rw_uw_record days = 1 }'
        self.assertIn(marker, dispatch)
        self.assertIn('name = rw_uw_native_send_serial value = scope:rw_uw_serial days = 1', dispatch)
        self.assertLess(dispatch.index('flag:native_requested'), dispatch.index(marker))
        self.assertLess(dispatch.index(marker), dispatch.index('run_interaction ='))
        self.assertIn('redirect = no', block(dispatch, 'run_interaction'))
        self.assertGreater(dispatch.index('remove_variable = rw_uw_native_send_record'), dispatch.index('run_interaction ='))

    def test_native_binding_requires_exact_current_consumed_request(self):
        guard = block(self.triggers, 'rw_uw_native_binding_context_trigger')
        for token in ('rw_uw_record_context_trigger = yes', 'var:rw_uw_issuer = scope:actor',
                      'var:rw_uw_attacker = scope:recipient',
                      'var:rw_uw_serial = scope:actor.var:rw_uw_native_send_serial',
                      'var:rw_uw_state = flag:closed', 'var:rw_uw_result = flag:native_requested',
                      'var:rw_uw_native_dispatched_on = current_date', 'count >= 2', 'is_participant_in_war'):
            self.assertIn(token, guard)

    def test_binding_consumes_marker_without_replaying_native_events_or_outcomes(self):
        effect = block(self.effects, 'rw_uw_bind_native_target_effect')
        self.assertLess(effect.index('has_variable = rw_uw_native_send_record'), effect.index('rw_uw_native_binding_context_trigger'))
        self.assertIn('var:rw_uw_native_send_record.var:rw_uw_war = { save_scope_as = target }', effect)
        self.assertIn('remove_variable = rw_uw_native_send_record', effect)
        self.assertIn('remove_variable = rw_uw_native_send_serial', effect)
        for forbidden in ('trigger_event', 'run_interaction', 'end_war', 'add_opinion', 'add_gold', 'add_prestige'):
            self.assertNotIn(forbidden, effect)


if __name__ == '__main__':
    unittest.main()
