"""Source checks of genuine native external-war intervention, no CK3 simulation."""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_g1_royal_response import block

FILES = {
    'triggers': 'common/scripted_triggers/rw_external_war_intervention_triggers.txt',
    'effects': 'common/scripted_effects/rw_external_war_intervention_effects.txt',
    'events': 'events/rw_external_war_intervention_events.txt',
    'choices': 'events/rw_external_war_response_events.txt',
    'story': 'common/story_cycles/rw_external_war_responses.txt',
    'peer_triggers': 'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt',
}


def intervention_errors(sources):
    errors = []

    def need(text, tokens, label):
        if any(not re.search(re.escape(token)+r'(?![\w:])', text) for token in tokens):
            errors.append(label)

    triggers, effects = sources['triggers'], sources['effects']
    need(block(triggers, 'rw_xw_native_adapter_available_trigger'), ('always = no',), 'older adapter enabled')
    context = block(triggers, 'rw_xw_native_context_trigger')
    need(context, ('rw_xw_identity_trigger = yes', 'this = scope:rw_xw_ruler',
                   'var:rw_xw_role = flag:declaring_liege',
                   'rw_xm_native_origin_trigger = yes',
                   'NOT = { rw_xw_other_native_attempt_trigger = yes }',
                   'NOT = { is_participant_in_war = scope:rw_xw_record.var:rw_xw_war }',
                   'any_character_war = { this = scope:rw_xw_record.var:rw_xw_war }',
                   'NOT = { any_character_war = { count >= 2 } }',
                   'NOT = { has_variable = rw_uw_native_send_record }',
                   'NOT = { has_variable = rw_xw_native_send_record }'), 'external native jurisdiction')
    if 'using_cb' in context:
        errors.append('one-war guard narrowed')
    need(block(triggers, 'rw_xw_can_queue_native_trigger'),
         ('rw_xw_native_adapter_available_trigger = yes', 'rw_xw_turn_trigger = yes',
          'rw_xw_native_context_trigger = yes'), 'unguarded native queue')
    ticket = block(triggers, 'rw_xw_native_ticket_trigger')
    need(ticket, ('this = scope:rw_xw_ruler', 'story_type = story_rw_external_war_response',
                  'story_owner = scope:rw_xw_attacker', 'var:rw_xw_schema = 1',
                  'var:rw_xw_serial = scope:rw_xw_serial', 'var:rw_xw_ruler = scope:rw_xw_ruler',
                  'var:rw_xw_attacker = scope:rw_xw_attacker', 'var:rw_xw_defender = scope:rw_xw_defender',
                  'var:rw_xw_war = scope:rw_xn_war', 'var:rw_xw_authority = scope:rw_xn_authority',
                  'var:rw_xw_role = flag:declaring_liege', 'var:rw_xw_state = flag:native_queued',
                  'exists = var:rw_xw_war', 'has_variable = rw_xw_native_window',
                  'has_variable = rw_xw_native_queued_on',
                  'NOT = { has_variable = rw_xw_native_dispatched_on }'), 'foreign or consumed native ticket')
    send_guard = block(triggers, 'rw_xw_can_send_native_trigger')
    need(send_guard, ('rw_xw_native_adapter_available_trigger = yes', 'rw_xw_native_ticket_trigger = yes',
                      'rw_xw_native_context_trigger = yes', 'scope:actor = scope:rw_xw_ruler',
                      'scope:recipient = scope:rw_xw_attacker',
                      'is_character_interaction_valid = {',
                      'interaction = stop_attacker_vassal_war_interaction'), 'native validation bypassed')
    if send_guard.count('scope:target = scope:rw_xw_record.var:rw_xw_war') != 2:
        errors.append('native target changed')
    queued = block(effects, 'rw_xw_queue_native_effect')
    need(queued, ('rw_xw_can_queue_native_trigger = yes', 'flag:native_queued',
                  'name = rw_xw_native_window value = flag:yes days = 2',
                  'remove_variable = rw_xw_window',
                  'id = rw_external_war_intervention.0001 days = 1'), 'reentrant or unconsumed queue')
    if 'run_interaction' in queued:
        errors.append('reentrant or unconsumed queue')
    dispatch = block(effects, 'rw_xw_send_native_effect')
    need(dispatch, ('rw_xw_native_ticket_trigger = yes', 'save_scope_as = actor',
                    'scope:rw_xw_attacker = { save_scope_as = recipient }',
                    'scope:rw_xw_record.var:rw_xw_war = { save_scope_as = target }',
                    'rw_xw_can_send_native_trigger = yes', 'flag:closed', 'flag:native_requested',
                    'flag:native_blocked', 'remove_variable = rw_xw_native_window',
                    'name = rw_xw_native_dispatched_on value = current_date',
                    'name = rw_xw_native_send_record value = scope:rw_xw_record days = 1',
                    'name = rw_xw_native_send_serial value = scope:rw_xw_serial days = 1',
                    'interaction = stop_attacker_vassal_war_interaction',
                    'actor = scope:rw_xw_ruler', 'recipient = scope:rw_xw_attacker',
                    'redirect = no', 'send_threshold = decline'), 'invalid native dispatch')
    if dispatch.count('run_interaction =') != 1:
        errors.append('native dispatch repeated')
    for consume in ('flag:closed', 'rw_xw_native_dispatched_on', 'remove_variable = rw_xw_native_window'):
        if dispatch.index(consume) > dispatch.index('run_interaction ='):
            errors.append('native dispatch before consumption')
    binding = block(triggers, 'rw_xw_native_binding_context_trigger')
    need(binding, ('rw_xw_native_adapter_available_trigger = yes',
                   'NOT = { has_variable = rw_uw_native_send_record }',
                   'NOT = { has_variable = rw_uw_native_send_serial }',
                   'has_variable = rw_xw_native_send_record', 'has_variable = rw_xw_native_send_serial',
                   'rw_xw_context_trigger = yes', 'var:rw_xw_ruler = scope:actor',
                   'rw_xm_native_origin_trigger = yes',
                   'var:rw_xw_attacker = scope:recipient',
                   'var:rw_xw_serial = scope:actor.var:rw_xw_native_send_serial',
                   'var:rw_xw_role = flag:declaring_liege', 'var:rw_xw_state = flag:closed',
                   'var:rw_xw_result = flag:native_requested',
                   'var:rw_xw_native_dispatched_on = current_date',
                   'NOT = { has_variable = rw_xw_native_bound_on }',
                   'NOT = { any_character_war = { count >= 2 } }'), 'foreign or replayed native binding')
    binder = block(effects, 'rw_xw_bind_native_target_effect')
    need(binder, ('rw_xw_native_binding_context_trigger = yes',
                  'var:rw_xw_native_send_record.var:rw_xw_war = { save_scope_as = target }',
                  'name = rw_xw_native_bound_on value = current_date',
                  'remove_variable = rw_xw_native_send_record',
                  'remove_variable = rw_xw_native_send_serial'), 'binding missing exact war or consumption')
    for name in ('rw_uw_can_send_native_trigger', 'rw_uw_native_binding_context_trigger'):
        need(block(sources['peer_triggers'], name),
             ('NOT = { has_variable = rw_xw_native_send_record }',
              'NOT = { has_variable = rw_xw_native_send_serial }'), 'mixed peer transport accepted')
    need(sources['events'], ('hidden = yes', 'trigger = { rw_xw_native_ticket_trigger = yes }',
                             'immediate = { rw_xw_send_native_effect = yes }'), 'missing deferred event')
    need(sources['choices'], ('trigger = { rw_xw_can_queue_native_trigger = yes }',
                              'rw_xw_queue_native_effect = yes'), 'native option missing')
    need(sources['story'], ('var:rw_xw_state = flag:native_queued',
                            'NOT = { has_variable = rw_xw_native_window }',
                            'remove_variable = rw_xw_native_window'), 'queued expiry missing')
    if re.search(r'\b(start_war|end_war|change_title_holder|add_gold|add_prestige|use_hook|add_hook|add_opinion|execute_threshold)\s*=',
                 clean_script(effects)[0]):
        errors.append('native outcome or cost duplicated')
    if any(token in triggers for token in ('is_ai', 'gold', 'opinion', 'ai_honor', 'top_liege')):
        errors.append('preference or higher authority in permission')
    return errors


class ExternalNativeInterventionTests(unittest.TestCase):
    def setUp(self):
        self.sources = {key: (builder.TEMPLATES/name).read_text(encoding='utf-8-sig')
                        for key, name in FILES.items()}

    def test_actual_source_contract_and_matching_delivery(self):
        self.assertEqual([], intervention_errors(self.sources))
        for name in FILES.values():
            self.assertIn(name, builder.FILES)

    def test_protector_and_multiple_wars_cannot_use_liege_intervention(self):
        for before, after in (('flag:declaring_liege', 'flag:target_liege'),
                              ('count >= 2', 'count >= 200'),
                              ('count >= 2', 'count >= 2 using_cb = claim_cb')):
            with self.subTest(guard=before, change=after):
                changed = dict(self.sources)
                changed['triggers'] = changed['triggers'].replace(before, after)
                self.assertTrue(intervention_errors(changed))

    def test_native_validation_and_target_identity_are_required(self):
        for token in ('is_character_interaction_valid = {',
                      'scope:target = scope:rw_xw_record.var:rw_xw_war',
                      'var:rw_xw_war = scope:rw_xn_war',
                      'scope:recipient = scope:rw_xw_attacker'):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed['triggers'] = changed['triggers'].replace(token, 'always = yes')
                self.assertTrue(intervention_errors(changed))

    def test_legacy_adapter_and_replayed_or_foreign_transport_are_detected(self):
        for token in ('always = no', 'var:rw_xw_serial = scope:actor.var:rw_xw_native_send_serial',
                      'NOT = { has_variable = rw_xw_native_bound_on }',
                      'NOT = { has_variable = rw_uw_native_send_record }',
                      'var:rw_xw_native_dispatched_on = current_date'):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed['triggers'] = changed['triggers'].replace(token, 'always = yes')
                self.assertTrue(intervention_errors(changed))

    def test_native_result_or_cost_cannot_be_reimplemented(self):
        for operation in ('end_war = white_peace', 'add_gold = -100', 'execute_threshold = decline',
                          'use_hook = scope:rw_xw_attacker', 'add_opinion = {}'):
            with self.subTest(operation=operation):
                changed = dict(self.sources)
                changed['effects'] += '\ninvalid_effect = { '+operation+' }'
                self.assertIn('native outcome or cost duplicated', intervention_errors(changed))

    def test_queue_is_deferred_and_consumed_before_the_single_send(self):
        dispatch = block(self.sources['effects'], 'rw_xw_send_native_effect')
        self.assertEqual(1, dispatch.count('run_interaction ='))
        self.assertLess(dispatch.index('rw_xw_native_dispatched_on'), dispatch.index('run_interaction ='))
        changed = dict(self.sources)
        changed['effects'] = changed['effects'].replace('id = rw_external_war_intervention.0001 days = 1',
                                                       'id = rw_external_war_intervention.0001 days = 0')
        self.assertIn('reentrant or unconsumed queue', intervention_errors(changed))

    def test_private_prefix_preserves_both_callbacks_and_version_gate(self):
        self.assertLess(builder.INTERVENTION_PREFIX.index('rw_uw_bind_native_target_effect'),
                        builder.INTERVENTION_PREFIX.index('rw_xw_bind_native_target_effect'))
        self.assertIn('rw_xw_native_adapter_available_trigger = { always = yes }', builder.INTERVENTION_MARKER)
        raw = b'stop_attacker_vassal_war_interaction = { on_accept = { original = yes } }'
        original, patched = builder.patch_native_intervention(raw)
        self.assertEqual(original, patched.replace(builder.INTERVENTION_PREFIX.encode(), b'', 1))
        self.assertNotIn('rw_xw_send_native_effect', builder.ACCEPT)

    def test_queued_timeout_and_mixed_peer_transport_stay_guarded(self):
        for file, token in (('story', 'remove_variable = rw_xw_native_window'),
                            ('peer_triggers', 'NOT = { has_variable = rw_xw_native_send_record }')):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed[file] = changed[file].replace(token, '')
                self.assertTrue(intervention_errors(changed))
