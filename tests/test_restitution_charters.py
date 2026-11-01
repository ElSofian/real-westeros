"""Adversarial original-source contracts; no CK3 inheritance/title simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script
ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT/'mod/real_westeros'


def charter_errors(t, e):
    errors=[]
    def need(b, xs, message):
        if any(x not in b for x in xs): errors.append(message)
    need(block(t,'rw_ch_roles_trigger'), ('rw_lr_view_trigger = yes','exists = scope:rw_ch_ruler',
        'exists = scope:rw_ch_head','rw_ch_roles_available_trigger = yes',
        'scope:rw_lr_authority = { holder = scope:rw_ch_ruler }',
        'scope:rw_lr_house = { house_head = scope:rw_ch_head }'), 'stale or foreign institutional role')
    need(block(t,'rw_ch_can_propose_trigger'), ('rw_ch_roles_trigger = yes','this = scope:rw_ch_ruler',
        'NOT = { has_variable = rw_ch_schema }'), 'wrong issuer or repeated charter')
    need(block(t,'rw_ch_view_trigger'), ('rw_lr_view_trigger = yes','exists = scope:rw_ch_revision',
        'var:rw_ch_schema = 1','var:rw_ch_revision = scope:rw_ch_revision',
        'exists = var:rw_ch_issuer','exists = var:rw_ch_original_head','has_variable = rw_ch_issued_on',
        'has_variable = rw_ch_accepted_on','exists = var:rw_ch_recognized_by',
        'has_variable = rw_ch_finished_on','exists = var:rw_ch_finished_by','exists = var:rw_ch_recovery_holder'),
        'foreign revision or incomplete public charter')
    need(block(t,'rw_ch_can_accept_trigger'), ('rw_ch_view_trigger = yes','rw_ch_roles_trigger = yes',
        'this = scope:rw_ch_head','var:rw_ch_state = flag:offered','has_variable = rw_ch_offer_window',
        'var:rw_ch_issuer = scope:rw_ch_ruler','var:rw_ch_original_head = scope:rw_ch_head'),
        'pending consent inherited or replayed')
    need(block(t,'rw_ch_active_trigger'), ('rw_ch_view_trigger = yes','rw_ch_roles_trigger = yes',
        'var:rw_ch_state = flag:active','has_variable = rw_ch_due'), 'expired or terminal charter acted on')
    need(block(t,'rw_ch_can_assume_trigger'), ('rw_ch_active_trigger = yes','this = scope:rw_ch_ruler',
        'NOT = { var:rw_ch_recognized_by = scope:rw_ch_ruler }'), 'silent or duplicate recognition')
    need(block(t,'rw_ch_can_satisfy_trigger'), ('rw_ch_can_release_trigger = yes',
        'scope:rw_lr_title = { exists = holder holder = { is_alive = yes exists = house house = scope:rw_lr_house } }'),
        'recovery asserted without exact present house ownership')
    propose=block(e,'rw_ch_propose_effect')
    need(propose, ('limit = { rw_ch_can_propose_trigger = yes }','name = rw_ch_revision value = 0',
        'name = rw_ch_issuer value = scope:rw_ch_ruler','name = rw_ch_original_head value = scope:rw_ch_head',
        'name = rw_ch_offer_window value = flag:yes days = 7','name = rw_ch_state value = flag:offered'),
        'proposal identity or fixed clock missing')
    accept=block(e,'rw_ch_accept_effect')
    need(accept, ('limit = { rw_ch_can_accept_trigger = yes }','remove_variable = rw_ch_offer_window',
        'change_variable = { name = rw_ch_revision add = 1 }','name = rw_ch_accepted_on value = current_date',
        'name = rw_ch_due value = flag:yes days = 1825','name = rw_ch_recognized_by value = scope:rw_ch_ruler',
        'name = rw_ch_state value = flag:active'), 'consent not consumed before accepted charter')
    assume=block(e,'rw_ch_assume_effect')
    need(assume, ('limit = { rw_ch_can_assume_trigger = yes }',
        'change_variable = { name = rw_ch_revision add = 1 }',
        'name = rw_ch_recognized_by value = scope:rw_ch_ruler','name = rw_ch_recognized_on value = current_date'),
        'recognition not explicit current version')
    finish=block(e,'rw_ch_finish_effect')
    need(finish, ('rw_ch_view_trigger = yes rw_ch_roles_trigger = yes',
        'OR = { this = scope:rw_ch_ruler this = scope:rw_ch_head }','save_scope_as = rw_ch_finisher',
        'remove_variable = rw_ch_due','remove_variable = rw_ch_offer_window',
        'change_variable = { name = rw_ch_revision add = 1 }','name = rw_ch_finished_on value = current_date',
        'name = rw_ch_finished_by value = scope:rw_ch_finisher','rw_ch_snapshot_effect = yes'),
        'terminal charter not consumed with exact actor')
    for b in (accept,assume,finish):
        if not 0 <= b.find('name = rw_ch_revision') < b.find('rw_ch_snapshot_effect = yes') < b.find('rw_ch_notify_effect = yes'):
            errors.append('old revision or premature notice')
    code=clean_script(e)[0]
    if re.search(r'\bname\s*=\s*rw_(?:lr|rs|rp|house|service)_|\b(add_gold|add_prestige|add_opinion|add_claim|change_title_holder|run_interaction|imprison|create_story|make_story_owner|every_living_character|every_in_global_list)\s*=',code):
        errors.append('public facts private consent or native title state rewritten')
    # One mutually exclusive one-year/five-year acceptance branch each.
    if len(re.findall(r'\bname\s*=\s*rw_ch_due\b',code))!=2 or len(re.findall(r'\bname\s*=\s*rw_ch_offer_window\b',code))!=1:
        errors.append('charter deadlines renewed')
    return errors


class RestitutionCharterTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_restitution_charter_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_restitution_charter_effects.txt').read_text()
        self.ev=(MOD/'events/rw_restitution_charter_events.txt').read_text()
        self.lr=(MOD/'common/scripted_effects/rw_land_register_effects.txt').read_text()
    def errors(self,t=None,e=None):return charter_errors(self.t if t is None else t,self.e if e is None else e)
    def test_source_contract(self):self.assertEqual([],self.errors())
    def test_exact_public_entry_and_fresh_current_role_tuple(self):
        for g in ('rw_lr_view_trigger = yes','scope:rw_lr_authority = { holder = scope:rw_ch_ruler }','scope:rw_lr_house = { house_head = scope:rw_ch_head }'):
            self.assertIn('stale or foreign institutional role',self.errors(t=self.t.replace(g,'always = yes')))
        base=(MOD/'common/scripted_triggers/rw_land_register_triggers.txt').read_text()
        for g in ('var:rw_lr_serial = scope:rw_lr_serial','var:rw_lr_authority = scope:rw_lr_authority','var:rw_lr_former_house = scope:rw_lr_house','var:rw_lr_title = scope:rw_lr_title'):
            self.assertIn(g,block(base,'rw_lr_view_trigger'))
    def test_real_sovereign_and_exact_house_head_not_storage_owner(self):
        roles=block(self.t,'rw_ch_roles_available_trigger')
        for g in ('rw_house_sovereign_trigger = yes','house = scope:rw_lr_house','NOT = { scope:rw_lr_authority.holder = scope:rw_lr_house.house_head }'):self.assertIn(g,roles)
        self.assertNotIn('story_owner',self.t+self.e)
    def test_only_current_crown_can_propose_once_per_entry(self):
        for g in ('this = scope:rw_ch_ruler','NOT = { has_variable = rw_ch_schema }'):
            self.assertIn('wrong issuer or repeated charter',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('NOT = { scope:rw_lr_title',block(self.t,'rw_ch_can_propose_trigger'))
    def test_revision_and_terminal_date_identity_fail_closed(self):
        for g in ('var:rw_ch_revision = scope:rw_ch_revision','exists = var:rw_ch_original_head','has_variable = rw_ch_finished_on','exists = var:rw_ch_recovery_holder'):
            self.assertIn('foreign revision or incomplete public charter',self.errors(t=self.t.replace(g,'always = yes')))
    def test_pending_proposal_consent_is_never_inherited(self):
        for g in ('var:rw_ch_issuer = scope:rw_ch_ruler','var:rw_ch_original_head = scope:rw_ch_head','this = scope:rw_ch_head','has_variable = rw_ch_offer_window'):
            self.assertIn('pending consent inherited or replayed',self.errors(t=self.t.replace(g,'always = yes')))
    def test_acceptance_consumes_offer_and_invalidates_older_panels(self):
        for g in ('remove_variable = rw_ch_offer_window','name = rw_ch_accepted_on value = current_date','name = rw_ch_due value = flag:yes days = 1825'):
            self.assertIn('consent not consumed before accepted charter',self.errors(e=self.e.replace(g,'removed')))
        self.assertIn('old revision or premature notice',self.errors(e=self.e.replace('rw_ch_snapshot_effect = yes','removed')))
    def test_successor_recognition_is_explicit_and_versioned(self):
        for g in ('NOT = { var:rw_ch_recognized_by = scope:rw_ch_ruler }','this = scope:rw_ch_ruler'):
            self.assertIn('silent or duplicate recognition',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('recognition not explicit current version',self.errors(e=self.e.replace('name = rw_ch_recognized_on value = current_date','removed')))
        self.assertNotIn('rw_ch_assume_effect',block(self.e,'rw_ch_opportunity_effect'))
    def test_recognition_reading_and_role_changes_never_restart_due(self):
        for name in ('rw_ch_assume_effect','rw_ch_prepare_effect','rw_ch_opportunity_effect'):
            b=block(self.e,name)
            self.assertNotRegex(b,r'\bname\s*=\s*rw_ch_(?:due|offer_window)\b')
            self.assertNotRegex(b,r'\b(?:days|years|months)\s*=')
        self.assertIn('charter deadlines renewed',self.errors(e=self.e+'\nset_variable = { name = rw_ch_due value = flag:yes days = 1825 }'))
    def test_current_representatives_can_end_without_inherited_guilt(self):
        for action,actor in (('renounce','ruler'),('release','head')):
            gate=block(self.t,'rw_ch_can_'+action+'_trigger')
            self.assertIn('rw_ch_active_trigger = yes',gate)
            self.assertIn('this = scope:rw_ch_'+actor,gate)
            self.assertNotIn('rw_ch_recognized_by',gate)
            self.assertIn('limit = { rw_ch_can_'+action+'_trigger = yes }',block(self.e,'rw_ch_'+action+'_effect'))
    def test_exact_actual_house_holding_required_for_satisfaction(self):
        g='scope:rw_lr_title = { exists = holder holder = { is_alive = yes exists = house house = scope:rw_lr_house } }'
        self.assertIn('recovery asserted without exact present house ownership',self.errors(t=self.t.replace(g,'always = yes')))
        b=block(self.e,'rw_ch_satisfy_effect')
        self.assertIn('limit = { rw_ch_can_satisfy_trigger = yes }',b)
        self.assertIn('name = rw_ch_recovery_holder value = scope:rw_lr_title.holder',b)
        self.assertLess(b.index('name = rw_ch_recovery_holder'),b.index('rw_ch_finish_effect'))
    def test_terminal_action_consumes_before_notice_and_captures_actual_actor(self):
        for g in ('remove_variable = rw_ch_due','name = rw_ch_finished_by value = scope:rw_ch_finisher','save_scope_as = rw_ch_finisher'):
            self.assertIn('terminal charter not consumed with exact actor',self.errors(e=self.e.replace(g,'removed')))
        self.assertIn('expired or terminal charter acted on',self.errors(t=self.t.replace('has_variable = rw_ch_due','always = yes')))
    def test_offered_expiry_or_changed_roles_can_only_be_closed_neutrally(self):
        b=block(self.t,'rw_ch_can_close_trigger')
        self.assertIn('rw_ch_roles_trigger = yes',b)
        self.assertIn('var:rw_ch_state = flag:offered',b)
        self.assertNotIn('rw_ch_issuer',b)
        self.assertNotIn('has_variable = rw_ch_offer_window',b)
        self.assertIn('desc = rw_restitution_charter.expired',self.ev)
    def test_public_storage_migration_does_not_migrate_private_consent(self):
        for cmd in ('make_story_owner = {}','create_story = {}','set_variable = { name = rw_rp_state value = flag:accepted }','set_variable = { name = rw_lr_retained value = flag:yes years = 100 }'):
            self.assertIn('public facts private consent or native title state rewritten',self.errors(e=self.e+'\n'+cmd))
        self.assertNotRegex(self.e,r'\b(?:rw_rp_|rw_rs_|rw_house_|rw_service_)')
    def test_new_role_notices_use_character_event_root_and_coalesce_before_sending(self):
        opp=block(self.e,'rw_ch_opportunity_effect')
        self.assertIn('rw_lr_record_valid_trigger = yes',opp)
        self.assertIn('has_variable = rw_lr_retained',opp)
        self.assertIn('NOT = { var:rw_ch_notified_ruler = scope:rw_lr_authority.holder }',opp)
        self.assertIn('NOT = { var:rw_ch_notified_head = scope:rw_lr_house.house_head }',opp)
        self.assertIn('NOT = { var:rw_ch_notified_recovery_holder = scope:rw_lr_title.holder }',opp)
        self.assertIn('house = scope:rw_lr_house',opp)
        self.assertLess(opp.index('name = rw_ch_notified_recovery_holder'),opp.index('scope:rw_lr_house.house_head = { trigger_event'))
        self.assertEqual(2,opp.count('id = rw_restitution_charter.0002'))
        self.assertNotIn('rw_ch_prepare_effect = yes',opp)
        self.assertLess(opp.index('name = rw_ch_notified_ruler'),opp.index('trigger_event'))
        self.assertIn('rw_ch_opportunity_effect = yes',block(self.lr,'rw_lr_deposit_effect'))
        self.assertIn('limit = { var:rw_ch_schema = 1 var:rw_ch_state = flag:active has_variable = rw_ch_due } rw_ch_opportunity_effect = yes',block(self.lr,'rw_lr_maintenance_effect'))
    def test_no_new_global_pulse_callback_index_or_native_operation(self):
        for cmd in ('change_title_holder','add_claim','add_gold','add_opinion','run_interaction','every_living_character','every_in_global_list'):
            self.assertIn('public facts private consent or native title state rewritten',self.errors(e=self.e+'\n'+cmd+' = {}'))
        self.assertNotRegex(self.e,r'\b(?:add_to_global_variable_list|trigger_event_on_next_tick)\s*=')
    def test_read_only_fresh_navigation_and_no_refresh_in_saved_reply(self):
        prep=block(self.e,'rw_ch_prepare_effect')
        for g in ('limit = { rw_lr_view_trigger = yes }','clear_saved_scope = rw_ch_ruler','clear_saved_scope = rw_ch_head','clear_saved_scope = rw_ch_revision'):self.assertIn(g,prep)
        self.assertNotIn('set_variable =',prep)
        self.assertNotIn('immediate =',block(self.ev,'rw_restitution_charter.0001'))
        lr_events=(MOD/'events/rw_land_register_events.txt').read_text()
        self.assertIn('id = rw_restitution_charter.0002',lr_events)
        self.assertNotIn('rw_ch_accept_effect',lr_events)
    def test_ai_and_player_share_costs_roles_and_choices(self):
        self.assertNotRegex(clean_script(self.t+self.e+self.ev)[0],r'\bis_ai\s*=')
        for action in ('propose','accept','assume','renounce','release','satisfy','close'):
            self.assertIn('rw_ch_can_'+action+'_trigger = yes',self.ev)
            self.assertIn('rw_ch_'+action+'_effect = yes',self.ev)
        self.assertIn('has_trait = honest',self.ev)
    def test_localized_public_roles_choices_and_causal_limits(self):
        keys=set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_restitution_charter\.[\w.]+)',self.ev));keys.add('rw_restitution_charter.review')
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_restitution_charter_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertTrue(keys<=actual,keys-actual)
