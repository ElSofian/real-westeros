"""Adversarial source contracts for institutional political records, not CK3 execution."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def affair_errors(t, e, story):
    errors = []
    valid = block(t, 'rw_house_record_valid_trigger')
    for guard in ('story_type = story_rw_house_affair', 'var:rw_house_schema = 1',
                  'var:rw_house_kind = flag:political_disfavor', 'has_variable = rw_house_serial',
                  'has_variable = rw_house_revision', 'exists = var:rw_house_target',
                  'exists = var:rw_house_authority', 'exists = var:rw_house_issuer',
                  'has_variable = rw_house_issued_on', 'var:rw_house_basis_kind = flag:exposed_participant_observation'):
        if guard not in valid:
            errors.append('untyped or incomplete decree')
    view = block(t, 'rw_house_view_trigger')
    for guard in ('rw_house_reader_allowed_trigger = { READER = root }',
                  'var:rw_house_target = scope:rw_house_target', 'var:rw_house_authority = scope:rw_house_authority',
                  'var:rw_house_serial = scope:rw_house_serial', 'var:rw_house_revision = scope:rw_house_revision'):
        if guard not in view:
            errors.append('wrong reader identity or revision')
    censure = block(t, 'rw_house_can_consider_censure_trigger')
    for guard in ('rw_scheme_justice_own_custody_trigger = yes', 'rw_house_sovereign_trigger = yes',
                  'prestige >= 50', 'NOT = { has_variable = rw_house_filed }',
                  'var:rw_house_target = scope:rw_scheme_evidence_record.var:rw_evidence_participant.house',
                  'var:rw_house_authority = scope:rw_scheme_observer.primary_title'):
        if guard not in censure:
            errors.append('unfunded unsupported or duplicate censure')
    turn = block(t, 'rw_house_censure_turn_trigger')
    for guard in ('rw_house_can_consider_censure_trigger = yes',
                  'scope:rw_house_target = scope:rw_scheme_evidence_record.var:rw_evidence_participant.house',
                  'scope:rw_house_authority = primary_title'):
        if guard not in turn:
            errors.append('censure target switched after confirmation')
    issue = block(e, 'rw_house_issue_censure_effect')
    for guard in ('limit = { rw_house_censure_turn_trigger = yes }',
                  'story_owner = scope:rw_house_issuer', 'NOT = { has_variable = rw_house_schema }',
                  'any_in_global_list = { variable = rw_house_affairs this = scope:rw_house_record }'):
        if guard not in issue:
            errors.append('constructor or registry check bypass')
    if not 0 <= issue.find('add_to_global_variable_list') < issue.find('name = rw_house_filed') < issue.find('add_prestige = -50'):
        errors.append('cost before registration/consumption')
    for name, gate in (('rw_house_petition_effect', 'rw_house_can_petition_trigger'),
                       ('rw_house_restore_effect', 'rw_house_ruler_reply_trigger'),
                       ('rw_house_refuse_effect', 'rw_house_ruler_reply_trigger'),
                       ('rw_house_withdraw_effect', 'rw_house_can_withdraw_trigger')):
        if f'limit = {{ {gate} = yes }}' not in block(e, name):
            errors.append('public mutation bypass')
    ruler = block(t, 'rw_house_current_ruler_trigger')
    if 'rw_house_view_trigger = yes' not in ruler or 'scope:rw_house_authority = { exists = holder holder = root }' not in ruler:
        errors.append('custodian or past issuer can judge')
    head = block(t, 'rw_house_current_head_trigger')
    if 'rw_house_view_trigger = yes' not in head or 'house = scope:rw_house_target' not in head or 'house_head = root' not in head:
        errors.append('descendant automatically gets head authority')
    reply = block(t, 'rw_house_ruler_reply_trigger')
    for guard in ('rw_house_current_ruler_trigger = yes', 'rw_house_pending_roles_valid_trigger = yes', 'var:rw_house_requested_ruler = root'):
        if guard not in reply:
            errors.append('stale pending petition accepted')
    restore = block(e, 'rw_house_restore_effect')
    if not 0 <= restore.find('rw_house_close_effect = { RESULT = restored }') < restore.find('add_opinion'):
        errors.append('reward before closure')
    if 'NOT = { has_opinion_modifier = { target = scope:rw_house_petitioner modifier = rw_house_restored_opinion } }' not in restore:
        errors.append('restoration goodwill stacks')
    if 'on_owner_death = { rw_house_owner_died_effect = yes }' not in story:
        errors.append('institutional death handling removed')
    death = block(e, 'rw_house_owner_died_effect')
    if death.count('NOT = { this = scope:rw_house_departed_custodian }') != 4:
        errors.append('dying custodian selected again')
    cleanup = block(e, 'rw_house_maintenance_effect')
    if not 0 <= cleanup.find('remove_list_global_variable') < cleanup.find('end_story = yes'):
        errors.append('dead record left in register')
    if e.count('name = rw_house_term value = flag:yes years = 50') != 1:
        errors.append('original decree term renewed')
    code = clean_script(t + e + story)[0]
    if re.search(r'\b(death|imprison|change_title_holder|destroy_title|set_house|set_dynasty|add_trait|remove_trait|run_interaction|consume_revoke_title_reason|add_secret|expose_scheme_agent)\s*=', code):
        errors.append('political record changes native guilt or property')
    return errors


class HouseAffairRegisterTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_house_affair_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_house_affair_effects.txt').read_text()
        self.s = (MOD / 'common/story_cycles/rw_house_affairs.txt').read_text()
        self.v = (MOD / 'events/rw_house_affair_events.txt').read_text()
        self.i = (MOD / 'common/character_interactions/rw_house_affair_interactions.txt').read_text()

    def errors(self, t=None, e=None, story=None):
        return affair_errors(self.t if t is None else t, self.e if e is None else e, self.s if story is None else story)

    def test_register_contract(self):
        self.assertEqual([], self.errors())

    def test_wrong_type_kind_schema_or_missing_provenance(self):
        for guard in ('story_type = story_rw_house_affair', 'var:rw_house_schema = 1',
                      'var:rw_house_kind = flag:political_disfavor', 'exists = var:rw_house_target',
                      'exists = var:rw_house_authority', 'has_variable = rw_house_issued_on'):
            self.assertIn('untyped or incomplete decree', self.errors(t=self.t.replace(guard, 'always = yes', 1)))

    def test_foreign_reader_house_title_serial_or_revision(self):
        for guard in ('rw_house_reader_allowed_trigger = { READER = root }',
                      'var:rw_house_target = scope:rw_house_target', 'var:rw_house_authority = scope:rw_house_authority',
                      'var:rw_house_serial = scope:rw_house_serial', 'var:rw_house_revision = scope:rw_house_revision'):
            self.assertIn('wrong reader identity or revision', self.errors(t=self.t.replace(guard, 'always = yes', 1)))

    def test_current_private_observation_custody_and_funds_required(self):
        for guard in ('rw_scheme_justice_own_custody_trigger = yes', 'prestige >= 50', 'NOT = { has_variable = rw_house_filed }'):
            self.assertIn('unfunded unsupported or duplicate censure', self.errors(t=self.t.replace(guard, 'always = yes', 1)))
        sovereign = block(self.t, 'rw_house_sovereign_trigger')
        for guard in ('is_alive = yes', 'is_adult = yes', 'is_imprisoned = no', 'is_independent_ruler = yes'):
            self.assertIn(guard, sovereign)

    def test_confirmation_cannot_switch_house_or_crown(self):
        for guard in ('scope:rw_house_target = scope:rw_scheme_evidence_record.var:rw_evidence_participant.house', 'scope:rw_house_authority = primary_title'):
            self.assertIn('censure target switched after confirmation', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_typed_fresh_constructor_and_index_before_cost(self):
        for guard in ('story_owner = scope:rw_house_issuer', 'NOT = { has_variable = rw_house_schema }', 'any_in_global_list = { variable = rw_house_affairs this = scope:rw_house_record }'):
            self.assertIn('constructor or registry check bypass', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertIn('house = scope:rw_house_target', block(self.e, 'rw_house_issue_censure_effect'))
        self.assertIn('NOT = { this = scope:rw_house_issuer }', block(self.e, 'rw_house_issue_censure_effect'))
        self.assertIn('cost before registration/consumption', self.errors(e=self.e.replace('add_prestige = -50', '').replace('save_scope_as = rw_house_issuer', 'save_scope_as = rw_house_issuer add_prestige = -50')))

    def test_independent_pair_dedup_and_house_serial_never_reused(self):
        for guard in ('var:rw_house_target = scope:rw_scheme_evidence_record.var:rw_evidence_participant.house', 'var:rw_house_authority = scope:rw_scheme_observer.primary_title'):
            self.assertIn('unfunded unsupported or duplicate censure', self.errors(t=self.t.replace(guard, 'always = yes')))
        issue = block(self.e, 'rw_house_issue_censure_effect')
        self.assertIn('NOT = { has_variable = rw_house_affair_serial }', issue)
        self.assertIn('change_variable = { name = rw_house_affair_serial add = 1 }', issue)
        self.assertEqual(1, self.e.count('name = rw_house_affair_serial value = 0'))

    def test_public_effects_always_revalidate(self):
        for gate in ('rw_house_can_petition_trigger', 'rw_house_ruler_reply_trigger', 'rw_house_can_withdraw_trigger'):
            self.assertIn('public mutation bypass', self.errors(e=self.e.replace(f'limit = {{ {gate} = yes }}', 'limit = { always = yes }')))

    def test_current_title_holder_not_story_custodian_or_old_issuer(self):
        self.assertIn('custodian or past issuer can judge', self.errors(t=self.t.replace('scope:rw_house_authority = { exists = holder holder = root }', 'story_owner = root')))
        self.assertIn('descendant automatically gets head authority', self.errors(t=self.t.replace('house_head = root', 'always = yes')))
        for name in ('rw_house_current_ruler_trigger', 'rw_house_current_head_trigger'):
            self.assertNotIn('story_owner', block(self.t, name))

    def test_pending_reply_requires_live_current_roles(self):
        for guard in ('rw_house_pending_roles_valid_trigger = yes', 'var:rw_house_requested_ruler = root'):
            self.assertIn('stale pending petition accepted', self.errors(t=self.t.replace(guard, 'always = yes')))
        pending = block(self.t, 'rw_house_pending_roles_valid_trigger')
        for guard in ('has_variable = rw_house_request_window', 'is_alive = yes', 'house.house_head = this', 'holder = prev.var:rw_house_requested_ruler'):
            self.assertIn(guard, pending)

    def test_fixed_deadlines_and_revision_consumption(self):
        self.assertIn('original decree term renewed', self.errors(e=self.e.replace('years = 50', 'years = 51', 1)))
        petition = block(self.e, 'rw_house_petition_effect')
        self.assertLess(petition.find('change_variable = { name = rw_house_revision add = 1 }'), petition.find('trigger_event'))
        self.assertIn('days = 30', petition)
        self.assertIn('days = 365', petition)
        self.assertNotIn('name = rw_house_term', petition)
        self.assertNotIn('name = rw_house_term', block(self.e, 'rw_house_refuse_effect'))

    def test_restoration_consumes_before_nonstacking_benefit(self):
        self.assertIn('reward before closure', self.errors(e=self.e.replace('rw_house_close_effect = { RESULT = restored }', '').replace('scope:rw_house_record = { rw_house_snapshot_effect = yes }', 'rw_house_close_effect = { RESULT = restored } scope:rw_house_record = { rw_house_snapshot_effect = yes }', 1)))
        self.assertIn('restoration goodwill stacks', self.errors(e=self.e.replace('NOT = { has_opinion_modifier = { target = scope:rw_house_petitioner modifier = rw_house_restored_opinion } }', 'always = yes')))

    def test_refusal_withdrawal_and_silence_have_no_extra_penalty(self):
        for name in ('rw_house_refuse_effect', 'rw_house_withdraw_effect'):
            self.assertNotRegex(block(self.e, name), r'\b(add_prestige|add_opinion|add_gold|imprison)\s*=')
        self.assertIn('RESULT = withdrawn', block(self.e, 'rw_house_withdraw_effect'))
        self.assertIn('name = rw_house_last_response value = flag:refused', block(self.e, 'rw_house_refuse_effect'))
        self.assertIn('rw_house_affairs.leave_unchanged', self.v)

    def test_owner_death_transfers_only_storage_excluding_dying_owner(self):
        self.assertIn('institutional death handling removed', self.errors(story=self.s.replace('rw_house_owner_died_effect = yes', 'end_story = yes')))
        self.assertIn('dying custodian selected again', self.errors(e=self.e.replace('NOT = { this = scope:rw_house_departed_custodian }', 'always = yes', 1)))
        death = block(self.e, 'rw_house_owner_died_effect')
        self.assertIn('make_story_owner = var:rw_house_authority.holder', death)
        self.assertIn('make_story_owner = var:rw_house_target.house_head', death)
        self.assertIn('random_house_member', death)
        self.assertNotRegex(death, r'\b(add_opinion|add_trait|set_house|change_title_holder)\s*=')

    def test_expiry_and_retention_remove_index_before_ending(self):
        self.assertIn('dead record left in register', self.errors(e=self.e.replace('remove_list_global_variable = { name = rw_house_affairs target = scope:rw_house_record }', '', 1 + self.e.count('remove_list_global_variable = { name = rw_house_affairs target = scope:rw_house_record }'))))
        maintenance = block(self.e, 'rw_house_maintenance_effect')
        self.assertIn('RESULT = expired', maintenance)
        self.assertIn('NOT = { has_variable = rw_house_retained }', maintenance)
        self.assertIn('days = 60', self.s)

    def test_archive_is_role_filtered_read_only_and_uncapped(self):
        read = block(self.e, 'rw_house_read_register_effect')
        self.assertIn('rw_house_reader_allowed_trigger = { READER = scope:rw_house_reader }', read)
        self.assertNotRegex(read, r'\b(set_variable|remove_variable|add_opinion|make_story_owner|random_in_global_list)\s*=')
        self.assertIn('var:rw_house_issuer = $READER$', self.t)
        self.assertIn('var:rw_house_target = $READER$.house', self.t)
        self.assertNotIn('scope:recipient', read)
        self.assertNotIn('limit = 1', read)

    def test_bounded_ai_opportunities_and_no_player_only_action(self):
        scheduled = block(self.e, 'rw_house_schedule_censure_review_effect')
        self.assertIn('NOT = { has_variable = rw_house_review_scheduled }', scheduled)
        self.assertEqual(2, scheduled.count('trigger_event ='))
        self.assertIn('days = 2', scheduled)
        self.assertIn('days = 30', scheduled)
        self.assertNotIn('is_ai', self.t + self.e)
        offers = block(self.e, 'rw_house_offer_opportunities_effect')
        self.assertIn('name = rw_house_last_head', offers)
        self.assertIn('name = rw_house_last_ruler', offers)
        self.assertNotRegex(self.e + self.s, r'\b(every_living_character|every_house_member|every_dynasty_member|every_held_title)\s*=')

    def test_provenance_and_dates_never_rewritten_on_restoration(self):
        for field in ('rw_house_issuer', 'rw_house_target', 'rw_house_authority', 'rw_house_basis_serial', 'rw_house_issued_on'):
            self.assertEqual(1, self.e.count(f'set_variable = {{ name = {field} '))
        self.assertIn('name = rw_house_closed_on value = current_date', self.e)
        for name in ('rw_house_restore_effect', 'rw_house_withdraw_effect'):
            self.assertNotIn('rw_evidence_', block(self.e, name))

    def test_no_native_property_guilt_or_optional_probe_dependency(self):
        for effect in ('imprison', 'change_title_holder', 'set_house', 'add_trait', 'run_interaction'):
            self.assertIn('political record changes native guilt or property', self.errors(e=self.e + f'\n{effect} = yes'))
        self.assertNotIn('rw_g3_trace', self.t + self.e + self.s + self.v)
        self.assertNotIn('disinherited', self.t + self.e)
        self.assertNotIn('scheme_owner', self.t + self.e)

    def test_localization_graph_and_explicit_political_kind(self):
        parent = (MOD / 'events/rw_sentencing_events.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_house_affairs\.[\w.]+|rw_review_house_affairs_interaction_desc)', self.v + self.i + parent))
        keys.update(('rw_review_house_affairs_interaction', 'rw_house_censured_opinion', 'rw_house_restored_opinion'))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_house_affair_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            loc = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', loc, re.M)))
        opinions = (MOD / 'common/opinion_modifiers/rw_house_affair_opinions.txt').read_text()
        self.assertIn('opinion = -20', opinions)
        self.assertIn('opinion = 10', opinions)
