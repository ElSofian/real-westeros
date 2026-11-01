"""Adversarial charter-duration source contracts; not a CK3 negotiation simulator."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mod/real_westeros'


def term_errors(t,e,ch_t,ch_e):
    errors=[]
    def need(b,parts,msg):
        if any(p not in b for p in parts):errors.append(msg)
    need(block(t,'rw_ct_term_matches_trigger'),('exists = scope:rw_ct_term',
        'OR = { scope:rw_ct_term = flag:year1 scope:rw_ct_term = flag:year5 }',
        'has_variable = rw_ct_schema','var:rw_ct_schema = 1','has_variable = rw_ct_term',
        'var:rw_ct_term = scope:rw_ct_term','NOT = { has_variable = rw_ct_term }',
        'NOT = { has_variable = rw_ct_turn }','scope:rw_ct_term = flag:year5'),
        'wrong term schema or invented legacy duration')
    need(block(ch_t,'rw_ch_view_trigger'),('rw_ct_term_matches_trigger = yes',), 'term absent from full charter identity')
    accept_gate=block(ch_t,'rw_ch_can_accept_trigger')
    need(accept_gate,('rw_ch_view_trigger = yes','rw_ch_roles_trigger = yes',
        'var:rw_ch_state = flag:offered','has_variable = rw_ch_offer_window',
        'var:rw_ch_issuer = scope:rw_ch_ruler','var:rw_ch_original_head = scope:rw_ch_head',
        'AND = { this = scope:rw_ch_head rw_ct_head_offer_trigger = yes }',
        'AND = { this = scope:rw_ch_ruler rw_ct_ruler_offer_trigger = yes }'),
        'wrong responder or inherited pending consent')
    need(block(t,'rw_ct_head_offer_trigger'),('scope:rw_ct_term = flag:year5',
        'var:rw_ct_turn = flag:head','NOT = { has_variable = rw_ct_term }','NOT = { has_variable = rw_ct_turn }'),
        'head accepts unapproved short terms')
    need(block(t,'rw_ct_ruler_offer_trigger'),('scope:rw_ct_term = flag:year1',
        'var:rw_ct_schema = 1 var:rw_ct_turn = flag:ruler'), 'ruler accepts their own long proposal')
    for action,actor,old,new,turn in (('shorten','head','year5','year1','ruler'),('restate','ruler','year1','year5','head')):
        need(block(t,'rw_ct_can_'+action+'_trigger'),('rw_ch_can_accept_trigger = yes',
            'this = scope:rw_ch_'+actor,'scope:rw_ct_term = flag:'+old), 'wrong counter actor or active amendment')
        b=block(e,'rw_ct_'+action+'_effect')
        need(b,('limit = { rw_ct_can_'+action+'_trigger = yes }','name = rw_ct_schema value = 1',
            'name = rw_ct_term value = flag:'+new,'name = rw_ct_turn value = flag:'+turn,
            'change_variable = { name = rw_ch_revision add = 1 }','rw_ch_snapshot_effect = yes',
            'scope:rw_ch_'+turn+' = { trigger_event = { id = rw_restitution_charter.0001 days = 1 } }'),
            'counter preserves old version or wrong party consent')
        points=[b.find(x) for x in ('name = rw_ch_revision','rw_ch_snapshot_effect = yes','trigger_event')]
        if min(points)<0 or points!=sorted(points):errors.append('counter notice before captured latest term')
    snap=block(ch_e,'rw_ch_snapshot_effect')
    need(snap,('name = rw_ct_term value = flag:year5','has_variable = rw_ct_term',
        'name = rw_ct_term value = var:rw_ct_term'), 'missing legacy or current duration snapshot')
    need(block(ch_e,'rw_ch_propose_effect'),('name = rw_ct_schema value = 1',
        'name = rw_ct_term value = flag:year5','name = rw_ct_turn value = flag:head'),
        'new default proposal term or turn absent')
    accept=block(ch_e,'rw_ch_accept_effect')
    need(accept,('limit = { rw_ch_can_accept_trigger = yes }','remove_variable = rw_ct_turn',
        'remove_variable = rw_ch_offer_window','name = rw_ch_accepted_on value = current_date',
        'limit = { scope:rw_ct_term = flag:year1 }',
        'set_variable = { name = rw_ch_due value = flag:yes days = 365 }',
        'else = { set_variable = { name = rw_ch_due value = flag:yes days = 1825 } }'),
        'wrong deadline or unconsumed consent')
    code=clean_script(e)[0]
    if re.search(r'\bname\s*=\s*rw_(?:ch_(?:due|offer_window|accepted_on|state)|lr_|cq_)|\b(add_gold|add_prestige|add_opinion|change_title_holder|make_story_owner|every_living_character|every_in_global_list)\s*=',code):
        errors.append('counter changes deadline state money or native world')
    return errors


class CharterTermTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_charter_term_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_charter_term_effects.txt').read_text()
        self.ch_t=(MOD/'common/scripted_triggers/rw_restitution_charter_triggers.txt').read_text()
        self.ch_e=(MOD/'common/scripted_effects/rw_restitution_charter_effects.txt').read_text()
        self.ev=(MOD/'events/rw_restitution_charter_events.txt').read_text()
    def errors(self,t=None,e=None,ch_t=None,ch_e=None):
        return term_errors(self.t if t is None else t,self.e if e is None else e,
            self.ch_t if ch_t is None else ch_t,self.ch_e if ch_e is None else ch_e)
    def test_source_contract(self):self.assertEqual([],self.errors())
    def test_new_and_unknown_terms_require_explicit_schema_and_current_capture(self):
        for g in ('exists = scope:rw_ct_term','var:rw_ct_schema = 1','var:rw_ct_term = scope:rw_ct_term'):
            self.assertIn('wrong term schema or invented legacy duration',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('term absent from full charter identity',self.errors(ch_t=self.ch_t.replace('rw_ct_term_matches_trigger = yes','always = yes')))
    def test_legacy_default_only_when_all_protocol_fields_absent(self):
        for g in ('NOT = { has_variable = rw_ct_term }','NOT = { has_variable = rw_ct_turn }','scope:rw_ct_term = flag:year5'):
            self.assertIn('wrong term schema or invented legacy duration',self.errors(t=self.t.replace(g,'always = yes')))
        snap=block(self.ch_e,'rw_ch_snapshot_effect')
        self.assertIn('missing legacy or current duration snapshot',self.errors(ch_e=self.ch_e.replace('name = rw_ct_term value = flag:year5','removed')))
        self.assertNotIn('set_variable',snap)
        self.assertIn('clear_saved_scope = rw_ct_term',block(self.ch_e,'rw_ch_prepare_effect'))
    def test_new_charter_starts_five_year_head_offer_not_a_shortened_active_duty(self):
        for g in ('name = rw_ct_schema value = 1','name = rw_ct_term value = flag:year5','name = rw_ct_turn value = flag:head'):
            self.assertIn('new default proposal term or turn absent',self.errors(ch_e=self.ch_e.replace(g,'removed')))
        self.assertNotIn('name = rw_ch_due',block(self.ch_e,'rw_ch_propose_effect'))
    def test_current_original_representatives_and_offer_window_still_required(self):
        for g in ('rw_ch_roles_trigger = yes','var:rw_ch_issuer = scope:rw_ch_ruler','var:rw_ch_original_head = scope:rw_ch_head','has_variable = rw_ch_offer_window'):
            self.assertIn('wrong responder or inherited pending consent',self.errors(ch_t=self.ch_t.replace(g,'always = yes')))
    def test_only_other_party_can_accept_corresponding_duration(self):
        for g in ('AND = { this = scope:rw_ch_head rw_ct_head_offer_trigger = yes }','AND = { this = scope:rw_ch_ruler rw_ct_ruler_offer_trigger = yes }'):
            self.assertIn('wrong responder or inherited pending consent',self.errors(ch_t=self.ch_t.replace(g,'always = yes')))
        self.assertIn('head accepts unapproved short terms',self.errors(t=self.t.replace('var:rw_ct_turn = flag:head','always = yes')))
        self.assertIn('ruler accepts their own long proposal',self.errors(t=self.t.replace('var:rw_ct_schema = 1 var:rw_ct_turn = flag:ruler','always = yes')))
    def test_counter_guards_cannot_amend_accepted_or_other_actors_promises(self):
        for g in ('rw_ch_can_accept_trigger = yes','this = scope:rw_ch_head','this = scope:rw_ch_ruler'):
            self.assertIn('wrong counter actor or active amendment',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('var:rw_ch_state = flag:offered',block(self.ch_t,'rw_ch_can_accept_trigger'))
    def test_counter_versions_and_turns_change_before_notice(self):
        for g in ('change_variable = { name = rw_ch_revision add = 1 }','rw_ch_snapshot_effect = yes',
                  'name = rw_ct_term value = flag:year1','name = rw_ct_turn value = flag:head'):
            self.assertIn('counter preserves old version or wrong party consent',self.errors(e=self.e.replace(g,'removed')))
        self.assertIn('counter notice before captured latest term',self.errors(e=self.e.replace('rw_ch_snapshot_effect = yes','removed')))
    def test_exact_one_or_five_year_deadline_only_at_explicit_acceptance(self):
        for g in ('limit = { scope:rw_ct_term = flag:year1 }','days = 365','else = { set_variable = { name = rw_ch_due value = flag:yes days = 1825 } }','remove_variable = rw_ct_turn'):
            self.assertIn('wrong deadline or unconsumed consent',self.errors(ch_e=self.ch_e.replace(g,'removed')))
        accept=block(self.ch_e,'rw_ch_accept_effect')
        self.assertLess(accept.index('remove_variable = rw_ch_offer_window'),accept.index('name = rw_ch_due'))
        self.assertLess(accept.index('name = rw_ch_due'),accept.index('rw_ch_notify_effect = yes'))
    def test_counters_reading_and_succession_never_renew_existing_clocks(self):
        for command in ('set_variable = { name = rw_ch_offer_window value = flag:yes days = 7 }','set_variable = { name = rw_ch_due value = flag:yes days = 365 }','set_variable = { name = rw_ch_accepted_on value = current_date }'):
            self.assertIn('counter changes deadline state money or native world',self.errors(e=self.e+'\n'+command))
        for name in ('rw_ch_assume_effect','rw_ch_prepare_effect','rw_ch_opportunity_effect'):
            self.assertNotRegex(block(self.ch_e,name),r'\bname\s*=\s*rw_ch_(?:due|offer_window)\b')
    def test_existing_financial_guards_still_bind_full_charter_identity(self):
        cq=(MOD/'common/scripted_triggers/rw_charter_compensation_triggers.txt').read_text()
        self.assertIn('rw_ch_view_trigger = yes',block(cq,'rw_cq_view_trigger'))
        self.assertIn('scope:rw_cq_parent_revision = scope:rw_ch_revision',block(cq,'rw_cq_live_trigger'))
        self.assertIn('rw_ch_active_trigger = yes',block(cq,'rw_cq_live_trigger'))
        self.assertNotIn('rw_ct_term', (MOD/'common/scripted_effects/rw_charter_compensation_effects.txt').read_text())
    def test_free_offer_closure_and_accepted_charter_exits_remain(self):
        for name in ('close','renounce','release','satisfy'):
            self.assertIn('rw_ch_'+name+'_effect = yes',self.ev)
        self.assertNotIn('name = rw_ct_term',block(self.ch_e,'rw_ch_finish_effect'))
        self.assertNotIn('name = rw_ct_term',block(self.ch_e,'rw_ch_assume_effect'))
    def test_no_new_native_callback_global_poll_punishment_or_financial_effect(self):
        for cmd in ('add_gold','add_opinion','change_title_holder','make_story_owner','every_living_character'):
            self.assertIn('counter changes deadline state money or native world',self.errors(e=self.e+'\n'+cmd+' = {}'))
        self.assertEqual(2,len(re.findall(r'\bdays\s*=\s*1\b',self.e)))
        self.assertNotRegex(self.e,r'\b(?:create_story|on_action|add_to_global_variable_list)\s*=')
    def test_ai_and_player_share_exact_duration_turn_and_cost_rules(self):
        self.assertNotRegex(clean_script(self.t+self.e+self.ev)[0],r'\bis_ai\s*=')
        for action in ('shorten','restate'):
            self.assertIn('rw_ct_can_'+action+'_trigger = yes',self.ev)
            self.assertIn('rw_ct_'+action+'_effect = yes',self.ev)
        self.assertIn('has_trait = impatient',self.ev)
        self.assertIn('has_trait = patient',self.ev)
    def test_localized_duration_and_counter_consent_are_explicit(self):
        keys=set(re.findall(r'(?:desc|name)\s*=\s*(rw_charter_terms\.[\w.]+)',self.ev))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_charter_terms_l_{lang}.yml';s=p.read_text(encoding='utf-8-sig')
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',s,re.M));self.assertTrue(keys<=actual,keys-actual)
            self.assertIn('365',s);self.assertIn('1825',s)
