"""Adversarial source checks for succession; neither a CK3 simulation nor runtime proof."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def succession_errors(t, e, v):
    errors = []
    pending = block(t, 'rw_house_pending_roles_valid_trigger')
    for guard in ('var:rw_house_last_response = flag:pending', 'is_imprisoned = no',
                  'var:rw_house_requested_ruler = { rw_house_sovereign_trigger = yes }',
                  'house.house_head = this', 'NOT = { is_at_war_with = prev.var:rw_house_requested_ruler }'):
        if guard not in pending:
            errors.append('unavailable party can answer pending petition')
    retire = block(e, 'rw_house_invalidate_request_effect')
    for guard in ('rw_house_record_active_trigger = yes', 'var:rw_house_last_response = flag:pending',
                  'has_variable = rw_house_request_window', 'name = rw_house_last_response value = flag:invalidated',
                  'has_variable = rw_house_request_window', 'remove_variable = rw_house_request_window', 'name = rw_house_revision add = 1'):
        if guard not in retire:
            errors.append('invalidation replay or stale reply remains possible')
    reconcile = block(e, 'rw_house_reconcile_request_effect')
    for guard in ('rw_house_record_active_trigger = yes', 'var:rw_house_last_response = flag:pending',
                  'NOT = { rw_house_pending_roles_valid_trigger = yes }',
                  'limit = { has_variable = rw_house_request_window }',
                  'rw_house_invalidate_request_effect = yes', 'flag:unanswered'):
        if guard not in reconcile:
            errors.append('live request retired or stale request revived')
    death = block(e, 'rw_house_owner_died_effect')
    for role in ('petitioner', 'requested_ruler'):
        if f'var:rw_house_{role} = scope:rw_house_departed_custodian' not in death:
            errors.append('known death can leave pending request live')
    if not 0 <= death.find('rw_house_invalidate_request_effect = yes') < death.find('make_story_owner'):
        errors.append('known death can leave pending request live')
    refresh = block(t, 'rw_house_refresh_allowed_trigger')
    for guard in ('exists = scope:rw_house_record', 'exists = scope:rw_house_target',
                  'exists = scope:rw_house_authority', 'exists = scope:rw_house_serial',
                  'rw_house_reader_allowed_trigger = { READER = root }',
                  'var:rw_house_target = scope:rw_house_target', 'var:rw_house_authority = scope:rw_house_authority',
                  'var:rw_house_serial = scope:rw_house_serial'):
        if guard not in refresh:
            errors.append('refresh can switch record or disclose another house')
    if 'rw_house_revision' in refresh:
        errors.append('obsolete revision blocks read-only recovery')
    available = block(t, 'rw_house_head_ruler_available_trigger')
    for guard in ('exists = holder', 'rw_house_sovereign_trigger = yes', 'exists = house_head',
                  'NOT = { is_at_war_with = prev.var:rw_house_authority.holder }'):
        if guard not in available:
            errors.append('successor opportunity consumed before available')
    offers = block(e, 'rw_house_offer_opportunities_effect')
    for guard in ('NOT = { exists = var:rw_house_last_head_ruler }',
                  'NOT = { var:rw_house_last_head_ruler = var:rw_house_authority.holder }'):
        if guard not in offers:
            errors.append('same head misses successor opportunity')
    if 'else = { remove_variable = rw_house_last_head_ruler }' not in offers:
        errors.append('new head inherits unavailable former pair')
    if offers.count('rw_house_head_ruler_available_trigger = yes') != 2:
        errors.append('successor opportunity consumed before available')
    if not 0 <= offers.find('set_variable = { name = rw_house_last_head_ruler') < offers.find('trigger_event'):
        errors.append('successor opportunity can loop')
    return errors


class HouseSuccessionContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_house_affair_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_house_affair_effects.txt').read_text()
        self.v = (MOD / 'events/rw_house_affair_events.txt').read_text()

    def errors(self, t=None, e=None):
        return succession_errors(self.t if t is None else t, self.e if e is None else e, self.v)

    def test_succession_contract(self):
        self.assertEqual([], self.errors())

    def test_imprisonment_war_and_lost_sovereignty_block_pending_reply(self):
        for guard in ('var:rw_house_last_response = flag:pending', 'is_imprisoned = no',
                      'var:rw_house_requested_ruler = { rw_house_sovereign_trigger = yes }',
                      'house.house_head = this', 'NOT = { is_at_war_with = prev.var:rw_house_requested_ruler }'):
            self.assertIn('unavailable party can answer pending petition', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_observed_invalidation_is_consumed_once_before_possible_new_reply(self):
        for guard in ('rw_house_record_active_trigger = yes', 'var:rw_house_last_response = flag:pending',
                      'remove_variable = rw_house_request_window', 'name = rw_house_revision add = 1'):
            self.assertIn('invalidation replay or stale reply remains possible', self.errors(e=self.e.replace(guard, 'always = yes')))
        retire = block(self.e, 'rw_house_invalidate_request_effect')
        self.assertLess(retire.index('flag:invalidated'), retire.index('change_variable'))

    def test_maintenance_distinguishes_timeout_from_observed_invalidity(self):
        for guard in ('NOT = { rw_house_pending_roles_valid_trigger = yes }',
                      'limit = { has_variable = rw_house_request_window }', 'flag:unanswered'):
            self.assertIn('live request retired or stale request revived', self.errors(e=self.e.replace(guard, 'always = yes')))
        maintenance = block(self.e, 'rw_house_maintenance_effect')
        self.assertLess(maintenance.index('rw_house_reconcile_request_effect'), maintenance.index('rw_house_offer_opportunities_effect'))
        for name in ('rw_house_reconcile_request_effect', 'rw_house_invalidate_request_effect'):
            code = clean_script(block(self.e, name))[0]
            self.assertNotRegex(code, r'\b(add_gold|add_prestige|add_opinion|trigger_event|end_story)\s*=')
            self.assertNotRegex(code, r'\b(?:name|remove_variable)\s*=\s*(?:rw_house_term|rw_house_petition_cooldown|rw_house_issued_on|rw_house_requested_on|rw_house_retained)\b')

    def test_owner_death_invalidates_matching_party_without_waiting_for_alive_flags(self):
        for role in ('petitioner', 'requested_ruler'):
            guard = f'var:rw_house_{role} = scope:rw_house_departed_custodian'
            self.assertIn('known death can leave pending request live', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertIn('known death can leave pending request live', self.errors(e=self.e.replace('rw_house_invalidate_request_effect = yes', 'always = yes')))
        # Death is not the same thing as temporary imprisonment or observed role change.
        death = block(self.e, 'rw_house_owner_died_effect')
        before_transfer = death[:death.index('make_story_owner')]
        self.assertNotIn('rw_house_pending_roles_valid_trigger', before_transfer)

    def test_head_gets_new_ruler_opportunity_once_when_eligible(self):
        for guard in ('NOT = { exists = var:rw_house_last_head_ruler }',
                      'NOT = { var:rw_house_last_head_ruler = var:rw_house_authority.holder }'):
            self.assertIn('same head misses successor opportunity', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertIn('successor opportunity can loop', self.errors(e=self.e.replace('set_variable = { name = rw_house_last_head_ruler value = var:rw_house_authority.holder }', '')))
        self.assertIn('new head inherits unavailable former pair', self.errors(e=self.e.replace('else = { remove_variable = rw_house_last_head_ruler }', '')))
        for guard in ('rw_house_sovereign_trigger = yes', 'NOT = { is_at_war_with = prev.var:rw_house_authority.holder }'):
            self.assertIn('successor opportunity consumed before available', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertIn('successor opportunity consumed before available', self.errors(e=self.e.replace('rw_house_head_ruler_available_trigger = yes', 'always = yes', 1)))
        offers = block(self.e, 'rw_house_offer_opportunities_effect')
        self.assertEqual(2, offers.count('trigger_event'))
        self.assertIn('scope:rw_house_head_notified = 0', offers)
        self.assertNotIn('is_ai', self.t + self.e)

    def test_refresh_ignores_revision_but_not_identity_or_permission(self):
        refresh = block(self.t, 'rw_house_refresh_allowed_trigger')
        for guard in ('rw_house_reader_allowed_trigger = { READER = root }',
                      'var:rw_house_target = scope:rw_house_target', 'var:rw_house_authority = scope:rw_house_authority',
                      'var:rw_house_serial = scope:rw_house_serial'):
            self.assertIn('refresh can switch record or disclose another house', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertNotIn('rw_house_revision', refresh)
        self.assertIn('var:rw_house_revision = scope:rw_house_revision', block(self.t, 'rw_house_view_trigger'))
        for name in ('rw_house_current_head_trigger', 'rw_house_current_ruler_trigger'):
            self.assertIn('rw_house_view_trigger = yes', block(self.t, name))
        self.assertNotIn('rw_house_refresh_allowed_trigger', block(self.t, 'rw_house_ruler_reply_trigger'))

    def test_refresh_never_answers_or_files_a_new_petition(self):
        refresh = block(self.e, 'rw_house_refresh_effect')
        self.assertIn('limit = { rw_house_refresh_allowed_trigger = yes }', refresh)
        self.assertIn('scope:rw_house_record = { rw_house_snapshot_effect = yes }', refresh)
        self.assertIn('trigger_event = { id = rw_house_affairs.0002 }', refresh)
        self.assertNotRegex(clean_script(refresh)[0], r'\b(set_variable|remove_variable|change_variable|add_gold|add_prestige|add_opinion|rw_house_petition_effect|rw_house_restore_effect|rw_house_refuse_effect|rw_house_withdraw_effect|rw_house_reconcile_request_effect)\s*=')
        snapshot = block(self.e, 'rw_house_snapshot_effect')
        self.assertNotRegex(clean_script(snapshot)[0], r'\b(set_variable|remove_variable|change_variable)\s*=')
        for event, gate in (('0002', 'rw_house_view_trigger'), ('0003', 'rw_house_ruler_reply_trigger')):
            panel = block(self.v, 'rw_house_affairs.' + event)
            self.assertIn(f'rw_house_refresh_allowed_trigger = yes NOT = {{ {gate} = yes }}', panel)
            self.assertEqual(1, panel.count('rw_house_refresh_effect = yes'))
        # Pure archive and explicit refresh never perform administrative retirement.
        self.assertNotIn('rw_house_reconcile_request_effect', block(self.e, 'rw_house_read_register_effect'))

    def test_invalidation_is_distinct_from_expiry_refusal_and_restoration(self):
        panel = block(self.v, 'rw_house_affairs.0002')
        self.assertIn('flag:invalidated', panel)
        self.assertIn('flag:unanswered', panel)
        self.assertLess(panel.index('rw_house_affairs.restored'), panel.index('rw_house_affairs.last_invalidated'))
        for lang in ('english', 'french'):
            loc = (MOD / f'localization/{lang}/rw_house_affair_l_{lang}.yml').read_text(encoding='utf-8-sig')
            self.assertIn('rw_house_affairs.last_invalidated:0', loc)
            self.assertIn('rw_house_affairs.refresh:0', loc)

    def test_no_additional_timer_or_native_hook_or_deadline_refresh(self):
        story = (MOD / 'common/story_cycles/rw_house_affairs.txt').read_text()
        self.assertEqual(1, story.count('effect_group'))
        self.assertIn('days = 60', story)
        self.assertEqual(1, self.e.count('name = rw_house_term value = flag:yes years = 50'))
        self.assertEqual(1, self.e.count('name = rw_house_petition_cooldown value = flag:yes days = 365'))
        new_code = ''.join(block(self.e, n) for n in ('rw_house_refresh_effect', 'rw_house_invalidate_request_effect', 'rw_house_reconcile_request_effect'))
        self.assertNotRegex(clean_script(new_code)[0], r'\b(every_living_character|imprison|death|change_title_holder|make_story_owner|set_house|on_actions)\s*=')
