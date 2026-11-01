"""Adversarial source checks for public compensation; no native transaction proof."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script
ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mod/real_westeros'


def compensation_errors(t,e):
    errors=[]
    def need(body,parts,msg):
        if any(p not in body for p in parts):errors.append(msg)
    need(block(t,'rw_cq_can_propose_trigger'),('rw_ch_active_trigger = yes',
        'OR = { this = scope:rw_ch_ruler this = scope:rw_ch_head }','NOT = { has_variable = rw_cq_schema }',
        'var:rw_cq_schema = 1','OR = { var:rw_cq_state = flag:offered var:rw_cq_state = flag:closed }',
        'NOT = { var:rw_cq_parent_revision = scope:rw_ch_revision }',
        'NOT = { var:rw_cq_payer = scope:rw_ch_ruler }','NOT = { var:rw_cq_payee = scope:rw_ch_head }'),
        'unauthorized proposal or same-context deadline restart')
    need(block(t,'rw_cq_view_trigger'),('rw_ch_view_trigger = yes','exists = scope:rw_cq_revision',
        'exists = scope:rw_cq_price','exists = scope:rw_cq_parent_revision','exists = scope:rw_cq_payer','exists = scope:rw_cq_payee',
        'var:rw_cq_revision = scope:rw_cq_revision','var:rw_cq_price = scope:rw_cq_price',
        'var:rw_cq_parent_revision = scope:rw_cq_parent_revision','var:rw_cq_payer = scope:rw_cq_payer',
        'var:rw_cq_payee = scope:rw_cq_payee','OR = { var:rw_cq_price = 25 var:rw_cq_price = 50 }',
        'rw_cq_paid_receipt_trigger = yes'),'foreign record quote or historical parties')
    need(block(t,'rw_cq_live_trigger'),('rw_cq_view_trigger = yes','rw_ch_active_trigger = yes',
        'scope:rw_cq_parent_revision = scope:rw_ch_revision','scope:rw_cq_payer = scope:rw_ch_ruler',
        'scope:rw_cq_payee = scope:rw_ch_head','var:rw_cq_state = flag:offered','has_variable = rw_cq_window'),
        'obsolete charter or successor spends old consent')
    need(block(t,'rw_cq_responder_trigger'),('rw_cq_live_trigger = yes',
        'AND = { this = scope:rw_ch_ruler scope:rw_lr_record = { var:rw_cq_turn = flag:ruler } }',
        'AND = { this = scope:rw_ch_head scope:rw_lr_record = { var:rw_cq_turn = flag:head } }'),
        'wrong current responder')
    need(block(t,'rw_cq_can_settle_trigger'),('rw_cq_responder_trigger = yes',
        'scope:rw_cq_payer = { gold >= scope:rw_cq_price }'),'insufficient or wrong personal funds')
    receipt=block(t,'rw_cq_paid_receipt_trigger')
    need(receipt,('rw_lr_record_valid_trigger = yes','has_variable = rw_lr_retained','var:rw_ch_state = flag:released',
        'var:rw_cq_state = flag:paid','has_variable = rw_cq_paid_on','has_variable = rw_cq_paid_revision',
        'has_variable = rw_cq_result_revision','exists = var:rw_cq_payer','exists = var:rw_cq_payee',
        'exists = var:rw_cq_settled_by','var:rw_cq_paid_amount = var:rw_cq_price',
        'var:rw_cq_paid_revision = var:rw_cq_revision','var:rw_cq_result_revision = var:rw_ch_revision',
        'var:rw_cq_paid_on = var:rw_ch_finished_on','var:rw_cq_settled_by = var:rw_ch_finished_by'),
        'incomplete or unrelated paid release receipt')
    propose=block(e,'rw_cq_propose_effect')
    need(propose,('rw_cq_can_propose_trigger = yes','this = scope:rw_ch_ruler scope:rw_cq_start_price = 25',
        'this = scope:rw_ch_head scope:rw_cq_start_price = 50','change_variable = { name = rw_cq_revision add = 1 }',
        'name = rw_cq_parent_revision value = scope:rw_ch_revision','name = rw_cq_payer value = scope:rw_ch_ruler',
        'name = rw_cq_payee value = scope:rw_ch_head','name = rw_cq_window value = flag:yes days = 7'),
        'unguarded proposal identity or clock')
    counter=block(e,'rw_cq_counter_effect')
    need(counter,('limit = { rw_cq_responder_trigger = yes }','change_variable = { name = rw_cq_revision add = 1 }',
        'name = rw_cq_price value = 25','name = rw_cq_price value = 50',
        'name = rw_cq_turn value = flag:head','name = rw_cq_turn value = flag:ruler','rw_cq_snapshot_effect = yes'),
        'counter preserves old consent')
    for b in (propose,counter):
        if re.search(r'\badd_gold\s*=|name\s*=\s*rw_ch_(?:state|revision|due)',clean_script(b)[0]):errors.append('early payment or release')
    settle=block(e,'rw_cq_settle_effect')
    need(settle,('limit = { rw_cq_can_settle_trigger = yes }','save_scope_as = rw_cq_settler',
        'remove_variable = rw_cq_window','remove_variable = rw_cq_turn','name = rw_cq_state value = flag:paid',
        'name = rw_cq_paid_on value = current_date','name = rw_cq_paid_amount value = scope:rw_cq_price',
        'name = rw_cq_paid_revision value = scope:rw_cq_revision','name = rw_cq_settled_by value = scope:rw_cq_settler',
        'remove_variable = rw_ch_due','remove_variable = rw_ch_offer_window',
        'change_variable = { name = rw_ch_revision add = 1 }','name = rw_ch_state value = flag:released',
        'name = rw_ch_finished_on value = current_date','name = rw_ch_finished_by value = scope:rw_cq_settler',
        'rw_ch_snapshot_effect = yes','name = rw_cq_result_revision value = scope:rw_ch_revision'),
        'paired release not consumed with actual actor')
    points=[settle.find(x) for x in ('name = rw_cq_state value = flag:paid','remove_variable = rw_ch_due',
        'name = rw_ch_state value = flag:released','name = rw_cq_result_revision value = scope:rw_ch_revision',
        'scope:rw_cq_payer = { add_gold = { value = scope:rw_cq_price multiply = -1 } }',
        'scope:rw_cq_payee = { add_gold = scope:rw_cq_price }','rw_cq_notify_effect = yes')]
    if min(points)<0 or points!=sorted(points):errors.append('wrong transfer direction or premature native effect or notice')
    closing=block(e,'rw_cq_close_effect')
    need(closing,('limit = { rw_cq_can_close_trigger = yes }','remove_variable = rw_cq_window',
        'remove_variable = rw_cq_turn','name = rw_cq_state value = flag:closed'),'unguarded refusal')
    if re.search(r'\badd_gold\s*=|name\s*=\s*rw_ch_',clean_script(closing)[0]):errors.append('refusal changes money or charter')
    code=clean_script(e)[0]
    if re.search(r'\bname\s*=\s*rw_(?:lr|house|rs|rp|service)_|\b(add_opinion|add_prestige|add_secret|add_hook|add_claim|change_title_holder|run_interaction|make_story_owner|every_living_character|every_in_global_list)\s*=',code):
        errors.append('unrelated native public or private state rewritten')
    if re.search(r'\bname\s*=\s*rw_ch_(?:due|offer_window)\b',code):errors.append('original charter deadline renewed')
    return errors


class CharterCompensationTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_charter_compensation_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_charter_compensation_effects.txt').read_text()
        self.ev=(MOD/'events/rw_charter_compensation_events.txt').read_text()
        self.ch=(MOD/'events/rw_restitution_charter_events.txt').read_text()
    def errors(self,t=None,e=None):return compensation_errors(self.t if t is None else t,self.e if e is None else e)
    def test_source_contract(self):self.assertEqual([],self.errors())
    def test_proposal_requires_active_exact_charter_and_real_new_context_for_reopening(self):
        for g in ('rw_ch_active_trigger = yes','NOT = { var:rw_cq_parent_revision = scope:rw_ch_revision }','NOT = { var:rw_cq_payer = scope:rw_ch_ruler }','NOT = { var:rw_cq_payee = scope:rw_ch_head }'):
            self.assertIn('unauthorized proposal or same-context deadline restart',self.errors(t=self.t.replace(g,'always = yes')))
    def test_public_entry_charter_and_frozen_monetary_parties_are_bound(self):
        for g in ('rw_ch_view_trigger = yes','var:rw_cq_revision = scope:rw_cq_revision','var:rw_cq_price = scope:rw_cq_price','var:rw_cq_payer = scope:rw_cq_payer','var:rw_cq_payee = scope:rw_cq_payee'):
            self.assertIn('foreign record quote or historical parties',self.errors(t=self.t.replace(g,'always = yes')))
    def test_successor_cannot_spend_predecessor_financial_consent(self):
        for g in ('scope:rw_cq_parent_revision = scope:rw_ch_revision','scope:rw_cq_payer = scope:rw_ch_ruler','scope:rw_cq_payee = scope:rw_ch_head','has_variable = rw_cq_window'):
            self.assertIn('obsolete charter or successor spends old consent',self.errors(t=self.t.replace(g,'always = yes')))
    def test_only_current_other_responder_can_counter_or_accept(self):
        for g in ('rw_cq_live_trigger = yes','AND = { this = scope:rw_ch_ruler scope:rw_lr_record = { var:rw_cq_turn = flag:ruler } }','AND = { this = scope:rw_ch_head scope:rw_lr_record = { var:rw_cq_turn = flag:head } }'):
            self.assertIn('wrong current responder',self.errors(t=self.t.replace(g,'always = yes')))
    def test_actual_personal_sovereign_funds_rechecked_regardless_accepting_actor(self):
        g='scope:rw_cq_payer = { gold >= scope:rw_cq_price }'
        self.assertIn('insufficient or wrong personal funds',self.errors(t=self.t.replace(g,'scope:rw_cq_payee = { gold >= 25 }')))
        self.assertIn('insufficient or wrong personal funds',self.errors(t=self.t.replace('rw_cq_responder_trigger = yes','always = yes')))
    def test_role_specific_opening_price_and_monotonic_quote(self):
        for g in ('this = scope:rw_ch_ruler scope:rw_cq_start_price = 25','this = scope:rw_ch_head scope:rw_cq_start_price = 50','change_variable = { name = rw_cq_revision add = 1 }'):
            self.assertIn('unguarded proposal identity or clock',self.errors(e=self.e.replace(g,'removed')))
        self.assertIn('rw_cq_propose_effect = { PRICE = 25 }',self.ch)
        self.assertIn('rw_cq_propose_effect = { PRICE = 50 }',self.ch)
    def test_negotiating_never_charges_or_changes_charter_state(self):
        for name in ('rw_cq_propose_effect','rw_cq_counter_effect'):
            self.assertIn('early payment or release',self.errors(e=self.e.replace(name+' = {',name+' = { add_gold = -25')))
        self.assertIn('counter preserves old consent',self.errors(e=self.e.replace('limit = { rw_cq_responder_trigger = yes }','limit = { always = yes }')))
    def test_counters_swap_responder_capture_latest_and_keep_original_clocks(self):
        b=block(self.e,'rw_cq_counter_effect')
        self.assertLess(b.index('name = rw_cq_revision'),b.index('rw_cq_snapshot_effect = yes'))
        self.assertLess(b.index('rw_cq_snapshot_effect = yes'),b.index('rw_cq_send_reply_effect = yes'))
        self.assertNotRegex(b,r'\bname\s*=\s*rw_(?:ch|cq)_(?:window|due|offer_window)\b')
        self.assertEqual(1,len(re.findall(r'\bname\s*=\s*rw_cq_window\b',self.e)))
        self.assertIn('original charter deadline renewed',self.errors(e=self.e+'\nset_variable = { name = rw_ch_due value = flag:yes days = 1825 }'))
    def test_paired_consumption_precedes_personal_gold_and_only_then_notices(self):
        for g in ('limit = { rw_cq_can_settle_trigger = yes }','remove_variable = rw_cq_window','remove_variable = rw_ch_due','name = rw_ch_finished_by value = scope:rw_cq_settler','name = rw_cq_result_revision value = scope:rw_ch_revision'):
            self.assertIn('paired release not consumed with actual actor',self.errors(e=self.e.replace(g,'removed')))
        self.assertIn('wrong transfer direction or premature native effect or notice',self.errors(e=self.e.replace('multiply = -1','multiply = 1')))
        self.assertNotIn('rw_ch_finish_effect',block(self.e,'rw_cq_settle_effect'))
        self.assertEqual(2,len(re.findall(r'\badd_gold\s*=',self.e)))
    def test_release_bookkeeping_matches_free_charter_shape_without_early_notice(self):
        base=block((MOD/'common/scripted_effects/rw_restitution_charter_effects.txt').read_text(),'rw_ch_finish_effect')
        paid=block(self.e,'rw_cq_settle_effect')
        for part in ('remove_variable = rw_ch_offer_window','remove_variable = rw_ch_due','change_variable = { name = rw_ch_revision add = 1 }','name = rw_ch_finished_on value = current_date','rw_ch_snapshot_effect = yes'):
            self.assertIn(part,base);self.assertIn(part,paid)
        self.assertNotIn('rw_ch_notify_effect',paid)
    def test_paid_packet_requires_amount_quote_parent_result_actor_and_date(self):
        for g in ('has_variable = rw_cq_paid_revision','var:rw_cq_paid_amount = var:rw_cq_price','var:rw_cq_result_revision = var:rw_ch_revision','var:rw_cq_paid_on = var:rw_ch_finished_on','var:rw_cq_settled_by = var:rw_ch_finished_by'):
            self.assertIn('incomplete or unrelated paid release receipt',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('rw_cq_paid_receipt_trigger = yes',self.ch)
    def test_free_charter_choices_remain_available_and_invalidate_quote_by_parent_revision(self):
        for action in ('release','renounce','satisfy'):
            self.assertIn('rw_ch_can_'+action+'_trigger = yes',self.ev)
            self.assertIn('rw_ch_'+action+'_effect = yes',self.ev)
        base=(MOD/'common/scripted_effects/rw_restitution_charter_effects.txt').read_text()
        self.assertNotIn('rw_cq_',base)
        self.assertIn('var:rw_ch_state = flag:active',(MOD/'common/scripted_triggers/rw_restitution_charter_triggers.txt').read_text())
    def test_declining_financial_offer_does_not_release_charter_or_pay(self):
        self.assertIn('refusal changes money or charter',self.errors(e=self.e.replace('rw_cq_close_effect = {','rw_cq_close_effect = { add_gold = -25')))
        close=block(self.t,'rw_cq_can_close_trigger')
        self.assertIn('rw_ch_roles_trigger = yes',close)
        self.assertNotIn('rw_cq_live_trigger',close)
        self.assertNotIn('rw_ch_active_trigger',close)
    def test_read_only_navigation_does_not_refresh_parent_or_saved_replies(self):
        prep=block(self.e,'rw_cq_prepare_effect')
        self.assertIn('limit = { rw_ch_view_trigger = yes }',prep)
        for scope in ('revision','price','parent_revision','payer','payee'):self.assertIn('clear_saved_scope = rw_cq_'+scope,prep)
        self.assertNotIn('rw_ch_snapshot_effect',prep)
        self.assertNotIn('rw_ch_prepare_effect',prep)
        self.assertNotIn('set_variable',prep)
        self.assertNotIn('immediate =',block(self.ev,'rw_charter_compensation.0001'))
    def test_no_new_global_timer_bank_title_or_unrelated_private_effect(self):
        for cmd in ('add_opinion = {}','change_title_holder = {}','make_story_owner = {}','every_in_global_list = {}','set_variable = { name = rw_lr_retained value = flag:yes years = 100 }','set_variable = { name = rw_rp_state value = flag:released }'):
            self.assertIn('unrelated native public or private state rewritten',self.errors(e=self.e+'\n'+cmd))
        self.assertNotRegex(self.e,r'\b(?:create_story|on_action|add_to_global_variable_list)\s*=')
    def test_only_fixed_counter_replies_and_original_named_representative_notices(self):
        self.assertEqual(2,len(re.findall(r'\bdays\s*=\s*1\b',self.e)))
        notify=block(self.e,'rw_cq_notify_effect')
        self.assertIn('scope:rw_ch_ruler',notify);self.assertIn('scope:rw_ch_head',notify)
        self.assertEqual(2,notify.count('trigger_event ='))
        self.assertNotIn('scope:rw_lr_former_holder',notify)
    def test_ai_player_same_roles_funds_effects_and_public_offer_choices(self):
        self.assertNotRegex(clean_script(self.t+self.e+self.ev+self.ch)[0],r'\bis_ai\s*=')
        for action in ('accept','counter','close'):
            self.assertIn('rw_cq_'+('can_settle' if action=='accept' else 'responder' if action=='counter' else 'can_close')+'_trigger = yes',self.ev)
        self.assertIn('has_trait = greedy',self.ev+self.ch)
    def test_localized_original_monetary_names_not_successor_names(self):
        keys=set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_charter_compensation\.[\w.]+)',self.ev+self.ch))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_charter_compensation_l_{lang}.yml';s=p.read_text(encoding='utf-8-sig')
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',s,re.M));self.assertTrue(keys<=actual,keys-actual)
            self.assertIn('[rw_cq_payer.GetShortUIName]',s);self.assertIn('[rw_cq_payee.GetShortUIName]',s)
