"""Source and delivered mediation contracts, not an engine decision model."""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_g1_royal_response import block

FILES = {
    'triggers': 'common/scripted_triggers/rw_external_war_mediation_triggers.txt',
    'effects': 'common/scripted_effects/rw_external_war_mediation_effects.txt',
    'events': 'events/rw_external_war_mediation_events.txt',
    'native': 'common/scripted_triggers/rw_external_war_intervention_triggers.txt',
    'choices': 'events/rw_external_war_response_events.txt',
    'story': 'common/story_cycles/rw_external_war_responses.txt',
}


def mediation_errors(sources):
    errors = []

    def need(text, tokens, label):
        if any(not re.search(re.escape(token)+r'(?![\w:])', text) for token in tokens):
            errors.append(label)

    triggers, effects = sources['triggers'], sources['effects']
    need(block(triggers, 'rw_xm_can_request_trigger'),
         ('rw_xw_native_adapter_available_trigger = yes', 'rw_xw_turn_trigger = yes',
          'var:rw_xw_role = flag:target_liege', 'var:rw_dl_issuer', 'var:rw_dl_authority',
          'liege = scope:rw_xm_law_check.var:rw_dl_issuer'), 'invalid protector request')
    need(block(triggers, 'rw_xm_context_trigger'),
         ('rw_xw_context_trigger = yes', 'var:rw_xw_role = flag:target_liege',
          'var:rw_dl_issuer = scope:rw_xm_check.var:rw_xm_mediator',
          'var:rw_dl_authority = scope:rw_xm_check.var:rw_xm_authority',
          'holder = scope:rw_xm_check.var:rw_xm_mediator',
          'liege = scope:rw_xm_check.var:rw_xm_mediator'), 'changed mediation authority')
    need(block(triggers, 'rw_xm_turn_trigger'),
         ('rw_xw_identity_trigger = yes', 'this = scope:rw_xm_mediator',
          'rw_xm_context_trigger = yes', 'var:rw_xm_mediator = scope:rw_xm_mediator',
          'var:rw_xm_authority = scope:rw_xm_authority',
          'var:rw_xw_ruler = scope:rw_xm_protector', 'var:rw_xw_state = flag:mediation_requested',
          'has_variable = rw_xm_requested_on', 'has_variable = rw_xm_window'), 'foreign or stale mediator turn')
    need(block(triggers, 'rw_xm_can_accept_trigger'),
         ('rw_xm_turn_trigger = yes', 'rw_xw_native_adapter_available_trigger = yes',
          'NOT = { is_participant_in_war = scope:rw_xw_record.var:rw_xw_war }',
          'NOT = { any_character_war = { count >= 2 } }',
          'NOT = { rw_xw_other_native_attempt_trigger = yes }',
          'NOT = { has_variable = rw_uw_native_send_record }',
          'NOT = { has_variable = rw_xw_native_send_record }'), 'unavailable mediated attempt')
    request = block(effects, 'rw_xm_request_effect')
    need(request, ('rw_xm_can_request_trigger = yes', 'flag:mediation_requested',
                   'var:rw_dl_issuer = { save_scope_as = rw_xm_mediator }',
                   'var:rw_dl_authority = { save_scope_as = rw_xm_authority }',
                   'remove_variable = rw_xw_window', 'name = rw_xm_window value = flag:yes days = 7',
                   'id = rw_external_war_mediation.0001'), 'unconsumed mediation request')
    if request.index('remove_variable = rw_xw_window') > request.index('trigger_event'):
        errors.append('request sent before consumption')
    if 'rw_xw_queue_native_effect' in request:
        errors.append('native attempt without mediator consent')
    for name, guard in (('rw_xm_accept_effect', 'rw_xm_can_accept_trigger'),
                         ('rw_xm_decline_effect', 'rw_xm_turn_trigger'),
                         ('rw_xm_note_existing_effect', 'rw_xm_turn_trigger')):
        answer = block(effects, name)
        need(answer, (guard+' = yes', 'name = rw_xw_state value = flag:closed',
                      'name = rw_xm_answered_on value = current_date', 'remove_variable = rw_xm_window'),
             'unconsumed mediation answer')
        if answer.index('remove_variable = rw_xm_window') > answer.index('send_interface_message'):
            errors.append('answer sent before consumption')
    accepted = block(effects, 'rw_xm_accept_effect')
    if accepted.index('remove_variable = rw_xm_window') > accepted.index('rw_xm_prepare_native_effect'):
        errors.append('handoff before explicit consent')
    prepare = block(effects, 'rw_xm_prepare_native_effect')
    need(prepare, ('this = scope:rw_xm_mediator', 'rw_xm_context_trigger = yes',
                   'story_owner = scope:rw_xw_attacker', 'var:rw_xm_mediator = scope:rw_xm_mediator',
                   'var:rw_xm_authority = scope:rw_xm_authority',
                   'var:rw_xw_result = flag:mediation_accepted', 'var:rw_xm_answered_on = current_date',
                   'NOT = { has_variable = rw_xm_handoff_started }',
                   'name = rw_xm_handoff_started value = current_date',
                   'create_story = { type = story_rw_external_war_response save_scope_as = rw_xm_ticket }',
                   'NOT = { has_variable = rw_xw_schema }',
                   'name = rw_xw_seen_on value = scope:rw_xm_request.var:rw_xw_seen_on',
                   'name = rw_xm_origin value = scope:rw_xm_request',
                   'name = rw_xm_origin_serial value = scope:rw_xm_request.var:rw_xw_serial',
                   'name = rw_xm_native_ticket value = scope:rw_xm_ticket',
                   'name = rw_xm_native_serial value = scope:rw_xm_ticket_serial',
                   'rw_xm_native_origin_trigger = yes', 'rw_xw_queue_native_effect = yes'),
         'foreign replayed or rewritten mediation handoff')
    if prepare.index('name = rw_xm_handoff_started') > prepare.index('create_story'):
        errors.append('handoff allocated before consumption')
    origin = block(triggers, 'rw_xm_native_origin_trigger')
    need(origin, ('NOT = { has_variable = rw_xm_ticket_schema }', 'var:rw_xm_ticket_schema = 1',
                  'NOT = { has_variable = rw_xm_origin }', 'NOT = { has_variable = rw_xm_origin_serial }',
                  'rw_xm_context_trigger = yes', 'story_owner = scope:rw_xm_job.story_owner',
                  'var:rw_xw_serial = scope:rw_xm_job.var:rw_xm_origin_serial',
                  'var:rw_xw_source_serial = scope:rw_xm_job.var:rw_xw_source_serial',
                  'var:rw_xw_war = scope:rw_xm_job.var:rw_xw_war',
                  'var:rw_xm_mediator = scope:rw_xm_job.var:rw_xw_ruler',
                  'var:rw_xm_authority = scope:rw_xm_job.var:rw_xw_authority',
                  'var:rw_xw_result = flag:mediation_accepted',
                  'var:rw_xm_native_ticket = scope:rw_xm_job',
                  'var:rw_xm_native_serial = scope:rw_xm_job.var:rw_xw_serial'), 'foreign or absent mediation consent')
    busy = block(sources['native'], 'rw_xw_other_native_attempt_trigger')
    need(busy, ('any_owned_story = {', 'story_type = story_rw_external_war_response',
                'story_owner = scope:rw_xw_busy_check.var:rw_xw_attacker',
                'var:rw_xw_war = scope:rw_xw_busy_check.var:rw_xw_war',
                'var:rw_xw_role = flag:declaring_liege', 'NOT = { this = scope:rw_xw_busy_check }',
                'var:rw_xw_state = flag:native_queued', 'has_variable = rw_xw_native_window',
                'has_variable = rw_xw_native_dispatched_on', 'var:rw_xw_native_dispatched_on = current_date'),
         'competing native attempt allowed')
    if sources['native'].count('rw_xm_native_origin_trigger = yes') != 2:
        errors.append('consent omitted at send or binding')
    need(sources['story'], ('var:rw_xw_state = flag:mediation_requested',
                            'NOT = { has_variable = rw_xm_window }',
                            'NOT = { rw_xm_context_trigger = yes }', 'remove_variable = rw_xm_window'),
         'missing mediation expiry')
    need(sources['choices'], ('rw_xm_can_request_trigger = yes', 'rw_xm_request_effect = yes'), 'missing protector choice')
    need(sources['events'], ('rw_xm_can_accept_trigger = yes', 'rw_xm_accept_effect = yes',
                             'rw_xm_decline_effect = yes', 'rw_xm_note_existing_effect = yes'), 'missing mediator choice')
    if re.search(r'\b(run_interaction|start_war|end_war|add_gold|add_prestige|add_opinion|use_hook|execute_threshold)\s*=',
                 clean_script(effects)[0]):
        errors.append('mediation duplicates native outcomes')
    if any(token in triggers for token in ('is_ai', 'ai_honor', 'opinion', 'top_liege')):
        errors.append('preference or superior authority in permission')
    return errors


class ExternalMediationTests(unittest.TestCase):
    def setUp(self):
        self.sources = {key: (builder.TEMPLATES/name).read_text(encoding='utf-8-sig') for key, name in FILES.items()}

    def test_actual_contract_and_delivery(self):
        self.assertEqual([], mediation_errors(self.sources))
        for name in FILES.values():
            self.assertIn(name, builder.FILES)

    def test_wrong_role_changed_liege_and_expired_request_are_detected(self):
        for token in ('var:rw_xw_role = flag:target_liege', 'this = scope:rw_xm_mediator',
                      'holder = scope:rw_xm_check.var:rw_xm_mediator',
                      'liege = scope:rw_xm_check.var:rw_xm_mediator', 'has_variable = rw_xm_window'):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed['triggers'] = changed['triggers'].replace(token, 'always = yes')
                self.assertTrue(mediation_errors(changed))

    def test_explicit_consent_precedes_the_separate_native_ticket(self):
        changed = dict(self.sources)
        changed['effects'] = changed['effects'].replace('rw_xm_request_effect = {',
            'rw_xm_request_effect = { rw_xw_queue_native_effect = yes')
        self.assertIn('native attempt without mediator consent', mediation_errors(changed))
        prepare = block(self.sources['effects'], 'rw_xm_prepare_native_effect')
        self.assertLess(prepare.index('name = rw_xm_handoff_started'), prepare.index('create_story'))

    def test_request_replay_and_foreign_consent_ticket_are_detected(self):
        for file, token in (
            ('triggers', 'NOT = { has_variable = rw_xm_ticket_schema }'),
            ('effects', 'NOT = { has_variable = rw_xm_handoff_started }'),
            ('triggers', 'var:rw_xw_serial = scope:rw_xm_job.var:rw_xm_origin_serial'),
            ('triggers', 'var:rw_xm_native_ticket = scope:rw_xm_job'),
            ('triggers', 'var:rw_xm_native_serial = scope:rw_xm_job.var:rw_xw_serial'),
        ):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed[file] = changed[file].replace(token, 'always = yes')
                self.assertTrue(mediation_errors(changed))

    def test_competing_attempts_exclude_self_and_need_live_or_same_day_evidence(self):
        for token in ('NOT = { this = scope:rw_xw_busy_check }', 'has_variable = rw_xw_native_window',
                      'var:rw_xw_native_dispatched_on = current_date'):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed['native'] = changed['native'].replace(token, 'always = yes')
                self.assertIn('competing native attempt allowed', mediation_errors(changed))

    def test_initial_decision_and_historical_law_are_preserved(self):
        prepare = block(self.sources['effects'], 'rw_xm_prepare_native_effect')
        self.assertIn('create_story = { type = story_rw_external_war_response save_scope_as = rw_xm_ticket }', prepare)
        self.assertIn('name = rw_xw_seen_on value = scope:rw_xm_request.var:rw_xw_seen_on', prepare)
        self.assertNotIn('rw_dl_capture_effect', prepare)
        self.assertNotIn('has_realm_law_flag', prepare)
        self.assertNotIn('random_owned_story', prepare)

    def test_refusal_silence_and_existing_attempt_have_no_automatic_penalty(self):
        for name in ('rw_xm_decline_effect', 'rw_xm_note_existing_effect'):
            choice = block(self.sources['effects'], name)
            self.assertLess(choice.index('remove_variable = rw_xm_window'), choice.index('send_interface_message'))
            self.assertNotIn('add_opinion', choice)
        changed = dict(self.sources)
        changed['story'] = changed['story'].replace('remove_variable = rw_xm_window', '')
        self.assertIn('missing mediation expiry', mediation_errors(changed))

    def test_native_costs_cannot_be_copied_and_legacy_tickets_remain_valid(self):
        origin = block(self.sources['triggers'], 'rw_xm_native_origin_trigger')
        self.assertIn('NOT = { has_variable = rw_xm_origin_serial }', origin)
        changed = dict(self.sources)
        changed['effects'] += '\nbad_effect = { end_war = white_peace }'
        self.assertIn('mediation duplicates native outcomes', mediation_errors(changed))
