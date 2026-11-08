"""Source and mutation checks of external authority routing, never a CK3 model."""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_g1_royal_response import block

FILES = {
    'triggers': 'common/scripted_triggers/rw_external_war_response_triggers.txt',
    'effects': 'common/scripted_effects/rw_external_war_response_effects.txt',
    'story': 'common/story_cycles/rw_external_war_responses.txt',
    'events': 'events/rw_external_war_response_events.txt',
    'law_effects': 'common/scripted_effects/rw_declaration_law_effects.txt',
}


def routing_errors(sources):
    errors = []

    def need(text, tokens, label):
        if any(token not in text for token in tokens):
            errors.append(label)

    triggers, effects = sources['triggers'], sources['effects']
    source = block(triggers, 'rw_xw_accepted_source_trigger')
    need(source, ('rw_dl_acceptance_match_trigger = yes', 'var:rw_dl_acceptance_schema = 1',
                  'var:rw_dl_accepted_on = current_date', 'var:rw_dl_accepted_actor = scope:actor',
                  'var:rw_dl_accepted_recipient = scope:recipient',
                  'var:rw_dl_accepted_choice = flag:defy_selected',
                  'var:rw_dl_peer_relation = flag:different_liege',
                  'var:rw_dl_ban = flag:all', 'var:rw_dl_gate = flag:permission_required'),
         'unbound or inapplicable declaration')
    need(block(triggers, 'rw_xw_source_trigger'),
         ('rw_xw_accepted_source_trigger = yes', 'has_variable = rw_xw_route_ready',
          'NOT = { has_variable = rw_xw_routed_on }'), 'legacy or replay intake')
    intake = block(effects, 'rw_xw_notice_effect')
    need(intake, ('this = scope:actor', 'scope:rw_da_record = { rw_xw_source_trigger = yes }',
                  'count >= 2', 'primary_attacker = scope:actor', 'primary_defender = scope:recipient',
                  'count >= 2 rw_dl_acceptance_match_trigger = yes',
                  'remove_variable = rw_xw_route_ready', 'name = rw_xw_routed_on value = current_date',
                  'clear_saved_scope = rw_xw_target', 'flag:declaring_liege', 'flag:target_liege',
                  'var:rw_dl_targets_state = flag:all_titles_recorded',
                  'every_owned_story = {', 'rw_xw_target_trigger = yes',
                  'var:rw_dt_holder_liege = { save_scope_as = rw_xw_ruler }'),
         'ambiguous or unconsumed route')
    if intake.index('name = rw_xw_routed_on') > intake.index('rw_xw_create_effect = yes'):
        errors.append('route consumed after allocation')
    target = block(triggers, 'rw_xw_target_trigger')
    need(target, ('story_type = story_rw_declaration_target', 'story_owner = scope:actor',
                  'var:rw_dt_schema = 1', 'var:rw_dt_parent = scope:rw_xw_source',
                  'var:rw_dt_parent_serial = scope:rw_xw_source.var:rw_dl_serial',
                  'var:rw_dt_war = scope:rw_xw_war', 'var:rw_dt_seen_on = current_date',
                  'var:rw_dt_holder_state = flag:known',
                  'exists = var:rw_dt_holder_liege', 'exists = var:rw_dt_holder_authority',
                  'NOT = { var:rw_dt_holder_liege = scope:rw_xw_source.var:rw_dl_issuer }',
                  'liege = scope:rw_xw_target_check.var:rw_dt_holder_liege',
                  'var:rw_dt_title = { holder = scope:rw_xw_target_check.var:rw_dt_holder }'),
         'foreign or reconstructed target authority')
    create_guard = block(triggers, 'rw_xw_can_create_trigger')
    need(create_guard, ('scope:rw_xw_source = { rw_xw_routed_source_trigger = yes }',
                        'NOT = {\n        any_owned_story = {',
                        'story_type = story_rw_external_war_response', 'story_owner = scope:actor',
                        'var:rw_xw_war = scope:rw_xw_war', 'var:rw_xw_role = scope:rw_xw_role',
                        'var:rw_xw_ruler = scope:rw_xw_ruler',
                        'scope:rw_xw_role = flag:declaring_liege',
                        'var:rw_dl_issuer = scope:rw_xw_ruler',
                        'scope:rw_xw_role = flag:target_liege', 'rw_xw_target_trigger = yes',
                        'var:rw_dt_holder_liege = scope:rw_xw_ruler'), 'allocation or dedup authority')
    if 'var:rw_xw_state' in create_guard:
        errors.append('closed decision excluded from dedup')
    need(block(triggers, 'rw_xw_routed_source_trigger'),
         ('rw_xw_accepted_source_trigger = yes', 'NOT = { has_variable = rw_xw_route_ready }',
          'var:rw_xw_routed_on = current_date'), 'allocation without consumed fresh source')
    context = block(triggers, 'rw_xw_context_trigger')
    need(context, ('rw_xw_exact_war_trigger = yes', 'var:rw_dl_schema = 1',
                   'var:rw_dl_serial = scope:rw_xw_check.var:rw_xw_source_serial',
                   'var:rw_dl_war = scope:rw_xw_check.var:rw_xw_war',
                   'var:rw_dl_accepted_actor = scope:rw_xw_check.var:rw_xw_attacker',
                   'var:rw_dl_accepted_recipient = scope:rw_xw_check.var:rw_xw_defender',
                   'using_cb = claim_cb', 'primary_attacker = scope:rw_xw_check.var:rw_xw_attacker',
                   'primary_defender = scope:rw_xw_check.var:rw_xw_defender',
                   'holder = scope:rw_xw_check.var:rw_xw_ruler',
                   'var:rw_xw_role = flag:declaring_liege', 'var:rw_xw_role = flag:target_liege',
                   'var:rw_dt_parent_serial = scope:rw_xw_check.var:rw_xw_source_serial',
                   'var:rw_dt_title = { holder = scope:rw_xw_target_check.var:rw_dt_holder }',
                   'liege = scope:rw_xw_check.var:rw_xw_ruler'), 'changed response context')
    need(block(triggers, 'rw_xw_turn_trigger'),
         ('this = scope:rw_xw_ruler', 'rw_xw_context_trigger = yes',
          'var:rw_xw_serial = scope:rw_xw_serial', 'var:rw_xw_ruler = scope:rw_xw_ruler',
          'var:rw_xw_attacker = scope:rw_xw_attacker', 'var:rw_xw_defender = scope:rw_xw_defender',
          'var:rw_xw_state = flag:pending', 'has_variable = rw_xw_window'), 'stale or foreign turn')
    for name in ('rw_xw_ignore_effect', 'rw_xw_disapprove_effect'):
        choice = block(effects, name)
        need(choice, ('rw_xw_turn_trigger = yes', 'name = rw_xw_state value = flag:closed',
                      'remove_variable = rw_xw_window'), 'unguarded choice')
        if 'add_opinion' in choice and choice.index('remove_variable = rw_xw_window') > choice.index('add_opinion'):
            errors.append('consequence before consumption')
    need(sources['story'], ('on_owner_death = { end_story = yes }', 'rw_xw_exact_war_trigger = yes',
                            'NOT = { rw_xw_context_trigger = yes }',
                            'NOT = { has_variable = rw_xw_window }', 'remove_variable = rw_xw_window'),
         'missing cleanup')
    need(sources['law_effects'], ('name = rw_xw_route_ready value = flag:yes',), 'missing fresh marker')
    if re.search(r'\b(start_war|end_war|run_interaction|change_title_holder|add_gold|use_hook)\s*=',
                 clean_script(effects)[0]):
        errors.append('native consequence added')
    if any(token in triggers for token in ('is_ai', 'gold', 'opinion', 'ai_honor', 'top_liege')):
        errors.append('preference or higher authority in permission')
    if re.search(r'save_(?:temporary_)?scope_as\s*=\s*(actor|recipient|attacker|defender|target|war)\b', effects+triggers):
        errors.append('native alias overwritten')
    return errors


class ExternalWarResponseTests(unittest.TestCase):
    def setUp(self):
        self.sources = {key: (builder.TEMPLATES/name).read_text(encoding='utf-8-sig')
                        for key, name in FILES.items()}

    def test_actual_source_contract(self):
        self.assertEqual([], routing_errors(self.sources))

    def test_unbound_lawful_legacy_and_replayed_intake_are_detected(self):
        for token in ('rw_dl_acceptance_match_trigger = yes', 'var:rw_dl_accepted_on = current_date',
                      'var:rw_dl_accepted_choice = flag:defy_selected', 'var:rw_dl_ban = flag:all',
                      'var:rw_dl_gate = flag:permission_required', 'has_variable = rw_xw_route_ready',
                      'NOT = { has_variable = rw_xw_routed_on }'):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed['triggers'] = changed['triggers'].replace(token, 'always = yes', 1)
                self.assertTrue(routing_errors(changed))

    def test_actual_holder_authority_and_target_parent_are_required(self):
        for token in ('var:rw_dt_parent = scope:rw_xw_source',
                      'var:rw_dt_parent_serial = scope:rw_xw_source.var:rw_dl_serial',
                      'var:rw_dt_war = scope:rw_xw_war',
                      'var:rw_dt_title = { holder = scope:rw_xw_target_check.var:rw_dt_holder }',
                      'liege = scope:rw_xw_target_check.var:rw_dt_holder_liege'):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed['triggers'] = changed['triggers'].replace(token, 'always = yes', 1)
                self.assertIn('foreign or reconstructed target authority', routing_errors(changed))

    def test_closed_choices_still_dedup_and_partial_capture_cannot_route_protectors(self):
        for key, before in (
            ('triggers', 'var:rw_xw_role = scope:rw_xw_role'),
            ('triggers', 'var:rw_xw_ruler = scope:rw_xw_ruler'),
            ('effects', 'var:rw_dl_targets_state = flag:all_titles_recorded'),
            ('effects', 'remove_variable = rw_xw_route_ready'),
            ('effects', 'count >= 2 rw_dl_acceptance_match_trigger = yes'),
        ):
            with self.subTest(guard=before):
                changed = dict(self.sources)
                changed[key] = changed[key].replace(before, 'always = yes')
                self.assertTrue(routing_errors(changed))

    def test_changed_roles_war_authority_and_expired_event_are_detected(self):
        for token in ('primary_defender = scope:rw_xw_check.var:rw_xw_defender',
                      'holder = scope:rw_xw_check.var:rw_xw_ruler',
                      'var:rw_xw_serial = scope:rw_xw_serial',
                      'var:rw_xw_state = flag:pending', 'has_variable = rw_xw_window'):
            with self.subTest(guard=token):
                changed = dict(self.sources)
                changed['triggers'] = changed['triggers'].replace(token, 'always = yes')
                self.assertTrue(routing_errors(changed))

    def test_consequences_are_one_time_political_opinion_only(self):
        choice = block(self.sources['effects'], 'rw_xw_disapprove_effect')
        self.assertLess(choice.index('remove_variable = rw_xw_window'), choice.index('add_opinion'))
        self.assertEqual(1, choice.count('add_opinion ='))
        self.assertIn('modifier = rw_uw_censured_opinion', choice)
        changed = dict(self.sources)
        changed['effects'] += '\ninvalid_effect = { end_war = yes }'
        self.assertIn('native consequence added', routing_errors(changed))

    def test_native_hook_order_and_delivery_keep_peer_path(self):
        self.assertLess(builder.ACCEPT.index('rw_dl_bind_acceptance_effect'), builder.ACCEPT.index('rw_xw_notice_effect'))
        self.assertLess(builder.ACCEPT.index('rw_xw_notice_effect'), builder.ACCEPT.index('rw_uw_notice_effect'))
        for name in FILES.values():
            self.assertIn(name, builder.FILES)
        peer = (builder.TEMPLATES/'common/scripted_effects/rw_unlawful_war_response_effects.txt').read_text()
        self.assertIn('rw_uw_peer_ban_trigger = yes', block(peer, 'rw_uw_notice_effect'))

    def test_same_guard_for_human_ai_and_role_specific_text(self):
        events = self.sources['events']
        self.assertEqual(4, events.count('rw_xw_turn_trigger = yes'))
        self.assertIn('flag:declaring_liege', events)
        self.assertIn('desc = rw_xw.target_desc', events)
        for lang in ('english', 'french'):
            name = f'localization/{lang}/rw_external_war_response_l_{lang}.yml'
            self.assertIn(name, builder.FILES)
            raw = (builder.TEMPLATES/name).read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            self.assertIn('[rw_xw_holder.GetTitledFirstName]', raw.decode('utf-8-sig'))
