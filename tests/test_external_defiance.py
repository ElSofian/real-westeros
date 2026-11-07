"""Inspect actual outside-war eligibility and response boundaries, not game logic."""
import unittest

from tools import build_g1_native_choice as builder
from test_g1_royal_response import block, contract_errors as royal_errors

ROOT = builder.TEMPLATES


def external_errors(triggers, response, option):
    errors = []
    applicable = block(triggers, 'rw_uw_applicable_ban_trigger')
    actor = block(applicable, 'scope:actor')
    recipient = block(applicable, 'scope:recipient')
    expected = '''OR = {
        liege = { has_realm_law_flag = vassal_all_wars_banned }
        AND = {
            exists = scope:recipient.liege
            liege = scope:recipient.liege
            liege = { has_realm_law_flag = vassal_internal_wars_banned }
        }
    }'''
    if ' '.join(expected.split()) not in ' '.join(actor.split()):
        errors.append('territorial ban branches changed')
    for token in ('exists = scope:actor', 'exists = scope:recipient',
                  'NOT = { scope:actor = scope:recipient }',
                  'war_declarer_needs_hook_on_liege = yes'):
        if token not in applicable:
            errors.append('missing shared native eligibility')
    if 'exists = liege' not in actor or 'liege = { is_alive = yes }' not in actor:
        errors.append('missing declaring authority')
    if 'exists = liege' in recipient:
        errors.append('independent defender excluded')
    for query in ('top_liege', 'every_liege_or_above', 'is_ai', 'gold', 'opinion'):
        if query in applicable:
            errors.append('extra authority or actor-specific permission')
    if option.count('rw_uw_applicable_ban_trigger = yes') != 2 or 'rw_uw_peer_ban_trigger' in option:
        errors.append('option does not use shared applicable ban')
    selected = block(triggers, 'rw_uw_selected_defiance_trigger')
    for token in ('rw_uw_applicable_ban_trigger = yes', 'always = scope:rw_uw_defy',
                  'NOT = { always = scope:hook }'):
        if token not in selected:
            errors.append('invalid selected defiance')
    peer = block(triggers, 'rw_uw_peer_ban_trigger')
    for token in ('rw_uw_applicable_ban_trigger = yes', 'exists = scope:recipient.liege',
                  'scope:actor = { liege = scope:recipient.liege }'):
        if token not in peer:
            errors.append('peer response boundary lost')
    if 'rw_uw_peer_ban_trigger = yes' not in block(response, 'rw_uw_notice_effect'):
        errors.append('peer response boundary lost')
    return errors


class ExternalDefianceTests(unittest.TestCase):
    def setUp(self):
        self.triggers = (ROOT/'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt').read_text(encoding='utf-8-sig')
        self.response = (ROOT/'common/scripted_effects/rw_unlawful_war_response_effects.txt').read_text(encoding='utf-8-sig')
        self.story = (ROOT/'common/story_cycles/rw_unlawful_war_responses.txt').read_text(encoding='utf-8-sig')

    def test_actual_external_option_and_peer_response_contract(self):
        self.assertEqual([], external_errors(self.triggers, self.response, builder.OPTION))

    def test_internal_ban_cannot_apply_across_different_lieges(self):
        for changed in (
            self.triggers.replace('liege = scope:recipient.liege', 'always = yes', 1),
            self.triggers.replace('vassal_all_wars_banned', 'vassal_internal_wars_banned', 1),
            self.triggers.replace('liege = { has_realm_law_flag = vassal_all_wars_banned }',
                                  'scope:recipient.liege = { has_realm_law_flag = vassal_all_wars_banned }', 1),
        ):
            with self.subTest(source=changed[:80]):
                self.assertIn('territorial ban branches changed',
                              external_errors(changed, self.response, builder.OPTION))

    def test_native_exceptions_and_declaring_authority_cannot_be_removed(self):
        for token, error in (
            ('war_declarer_needs_hook_on_liege = yes', 'missing shared native eligibility'),
            ('exists = liege', 'missing declaring authority'),
        ):
            with self.subTest(guard=token):
                self.assertIn(error, external_errors(
                    self.triggers.replace(token, 'always = yes', 1), self.response, builder.OPTION))

    def test_old_peer_only_option_or_hook_combination_is_detected(self):
        option = builder.OPTION.replace('rw_uw_applicable_ban_trigger', 'rw_uw_peer_ban_trigger')
        self.assertIn('option does not use shared applicable ban', external_errors(self.triggers, self.response, option))
        changed = self.triggers.replace('NOT = { always = scope:hook }', 'always = yes')
        self.assertIn('invalid selected defiance', external_errors(changed, self.response, builder.OPTION))

    def test_outside_declaration_cannot_enter_peer_only_response(self):
        response = self.response.replace('rw_uw_peer_ban_trigger = yes', 'always = yes')
        self.assertIn('peer response boundary lost', external_errors(self.triggers, response, builder.OPTION))
        self.assertIn('declaration/replay/deadline', royal_errors(self.triggers, response, self.story))
