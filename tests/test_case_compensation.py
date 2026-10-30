"""Adversarial source contracts for financial consent; no CK3 money/state simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def compensation_errors(t,e,v):
    out=[]
    base=block(t,'rw_cc_base_trigger')
    for g in ('rw_case_matches_trigger = yes','is_alive = yes','this = scope:rw_service_provider',
              'this = scope:rw_service_client','NOT = { scope:rw_service_provider = scope:rw_service_client }',
              'var:rw_case_kind = flag:service','var:rw_case_stage = flag:closed','has_variable = rw_case_retained'):
        if g not in base:out.append('unrelated active expired or unsupported case negotiated')
    context=block(t,'rw_cc_context_trigger')
    for g in ('is_alive = yes','is_adult = yes','is_imprisoned = no'):
        if context.count(g)!=2:out.append('unavailable party pays or consents')
    if 'NOT = { is_at_war_with = scope:rw_service_client }' not in context:out.append('unavailable party pays or consents')
    propose=block(t,'rw_cc_can_propose_trigger')
    for g in ('rw_cc_base_trigger = yes','rw_cc_context_trigger = yes','NOT = { has_variable = rw_cc_schema }'):
        if g not in propose:out.append('original offer replaced or role bypass')
    view=block(t,'rw_cc_view_trigger')
    for g in ('rw_cc_base_trigger = yes','exists = scope:rw_cc_revision','exists = scope:rw_cc_price',
              'var:rw_cc_schema = 1','has_variable = rw_cc_issued_on','var:rw_cc_revision = scope:rw_cc_revision',
              'var:rw_cc_price = scope:rw_cc_price','var:rw_cc_price = 25','var:rw_cc_price = 50',
              'has_variable = rw_cc_paid_on','var:rw_cc_paid_amount = scope:rw_cc_price',
              'var:rw_cc_paid_revision = scope:rw_cc_revision'):
        if not re.search(re.escape(g)+r'(?![\w.])',view):out.append('stale or malformed financial receipt')
    live=block(t,'rw_cc_offer_live_trigger')
    for g in ('rw_cc_view_trigger = yes','rw_cc_context_trigger = yes','var:rw_cc_state = flag:offered','has_variable = rw_cc_window'):
        if g not in live:out.append('expired terminal or unavailable offer accepted')
    responder=block(t,'rw_cc_responder_trigger')
    for g in ('rw_cc_offer_live_trigger = yes','this = scope:rw_service_client','var:rw_cc_turn = flag:client',
              'this = scope:rw_service_provider','var:rw_cc_turn = flag:provider'):
        if g not in responder:out.append('unilateral or wrong-side acceptance')
    afford=block(t,'rw_cc_can_settle_trigger')
    for g in ('rw_cc_responder_trigger = yes','scope:rw_service_provider = { gold >= scope:rw_cc_price }'):
        if g not in afford:out.append('unfunded or unconsented payment')
    for name,gate in (('counter','responder'),('settle','can_settle'),('close','can_close')):
        if f'limit = {{ rw_cc_{gate}_trigger = yes }}' not in block(e,f'rw_cc_{name}_effect'):
            out.append('unguarded financial effect')
    begin=block(e,'rw_cc_propose_effect')
    for g in ('rw_cc_can_propose_trigger = yes','scope:rw_cc_start_price = 25','scope:rw_cc_start_price = 50',
              'name = rw_cc_state value = flag:offered','name = rw_cc_issued_on value = current_date',
              'name = rw_cc_window value = flag:yes days = 7','name = rw_cc_schema value = 1'):
        if not re.search(re.escape(g)+r'(?![\w.])',begin):out.append('unsupported start amount or missing first window')
    if e.count('name = rw_cc_window')!=1:out.append('original response deadline reset')
    counter=block(e,'rw_cc_counter_effect')
    for g in ('change_variable = { name = rw_cc_revision add = 1 }','name = rw_cc_price value = 25',
              'name = rw_cc_price value = 50','name = rw_cc_turn value = flag:provider',
              'name = rw_cc_turn value = flag:client','rw_cc_snapshot_effect = yes','rw_cc_send_reply_effect = yes'):
        if g not in counter:out.append('old counter consent remains live')
    send=block(e,'rw_cc_send_reply_effect')
    if send.count('id = rw_case_compensation.0001 days = 1')!=2:out.append('immediate AI counter loop')
    pay=block(e,'rw_cc_settle_effect')
    points=[pay.find(g) for g in ('remove_variable = rw_cc_window','name = rw_cc_paid_amount',
                                 'name = rw_cc_paid_revision','name = rw_cc_paid_on',
                                 'name = rw_cc_state value = flag:paid','add_gold','rw_cc_notify_effect = yes')]
    if min(points)<0 or points!=sorted(points):out.append('payment before receipt consumption or early notice')
    for g in ('scope:rw_service_provider = { add_gold = { value = scope:rw_cc_price multiply = -1 } }',
              'scope:rw_service_client = { add_gold = scope:rw_cc_price }'):
        if g not in pay:out.append('wrong payer amount or direction')
    if len(re.findall(r'\badd_gold\s*=',clean_script(e)[0]))!=2:out.append('extra payment or refund path')
    code=clean_script(e)[0]
    if re.search(r'\b(?:name|flag)\s*=\s*rw_(?!cc_)\w+',code):out.append('financial gesture rewrites original affair')
    if re.search(r'\b(add_opinion|remove_opinion|add_prestige|add_secret|add_hook|add_claim|imprison|death|change_title_holder|create_title_and_vassal_change|run_interaction|send_interaction|make_story_owner|create_story|every_living_character|every_in_global_list)\s*=',code):
        out.append('payment buys native punishment pardon or unrelated effects')
    # Old queued replies must never silently acquire the newest consent ticket.
    if 'immediate' in block(v,'rw_case_compensation.0001'):out.append('old reply refreshes consent on load')
    if 'immediate = { rw_cc_prepare_effect = yes }' not in block(v,'rw_case_compensation.0002'):
        out.append('fresh review not isolated from delayed replies')
    return out


class CaseCompensationTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_case_compensation_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_case_compensation_effects.txt').read_text()
        self.v=(MOD/'events/rw_case_compensation_events.txt').read_text()

    def errors(self,t=None,e=None,v=None):
        return compensation_errors(self.t if t is None else t,self.e if e is None else e,self.v if v is None else v)

    def test_contract(self):self.assertEqual([],self.errors())

    def test_only_original_private_parties_of_exact_closed_retained_service_case(self):
        for g in ('rw_case_matches_trigger = yes','this = scope:rw_service_provider','this = scope:rw_service_client',
                  'NOT = { scope:rw_service_provider = scope:rw_service_client }','var:rw_case_kind = flag:service',
                  'var:rw_case_stage = flag:closed','has_variable = rw_case_retained'):
            self.assertIn('unrelated active expired or unsupported case negotiated',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertNotIn('this = scope:rw_case_mediator',block(self.t,'rw_cc_base_trigger'))
        self.assertNotIn('rw_case_jurisdiction_trigger',self.t)

    def test_current_living_adult_free_peaceful_parties_without_rank_substitution(self):
        for g in ('is_alive = yes','is_adult = yes','is_imprisoned = no','NOT = { is_at_war_with = scope:rw_service_client }'):
            self.assertIn('unavailable party pays or consents',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertNotRegex(block(self.t,'rw_cc_context_trigger'),r'\b(is_landed|top_liege|house_head)\b')

    def test_each_case_has_one_initial_offer_and_supported_start_prices(self):
        self.assertIn('original offer replaced or role bypass',self.errors(t=self.t.replace('NOT = { has_variable = rw_cc_schema }','always = yes')))
        self.assertIn('unsupported start amount or missing first window',self.errors(e=self.e.replace('scope:rw_cc_start_price = 50','scope:rw_cc_start_price = 500')))
        begin=block(self.e,'rw_cc_propose_effect')
        self.assertLess(begin.index('name = rw_cc_turn'),begin.index('name = rw_cc_schema'))
        self.assertLess(begin.index('name = rw_cc_schema'),begin.index('rw_cc_send_reply_effect'))
        for amount in (25,50):self.assertIn(f'rw_cc_propose_effect = {{ PRICE = {amount} }}',self.v)

    def test_offer_or_counter_approval_cannot_be_unilateral(self):
        for g in ('rw_cc_offer_live_trigger = yes','this = scope:rw_service_client','var:rw_cc_turn = flag:client',
                  'this = scope:rw_service_provider','var:rw_cc_turn = flag:provider'):
            self.assertIn('unilateral or wrong-side acceptance',self.errors(t=self.t.replace(g,'always = yes')))
        begin=block(self.e,'rw_cc_propose_effect')
        self.assertIn('this = scope:rw_service_provider',begin)
        self.assertIn('name = rw_cc_turn value = flag:client',begin)
        self.assertIn('name = rw_cc_turn value = flag:provider',begin)

    def test_latest_revision_price_and_complete_payment_receipt_are_required(self):
        for g in ('exists = scope:rw_cc_revision','exists = scope:rw_cc_price','var:rw_cc_schema = 1',
                  'var:rw_cc_revision = scope:rw_cc_revision','var:rw_cc_price = scope:rw_cc_price',
                  'has_variable = rw_cc_paid_on','var:rw_cc_paid_amount = scope:rw_cc_price',
                  'var:rw_cc_paid_revision = scope:rw_cc_revision'):
            self.assertIn('stale or malformed financial receipt',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('stale or malformed financial receipt',self.errors(t=self.t.replace('var:rw_cc_price = 50','var:rw_cc_price = 500')))

    def test_expired_unavailable_or_paid_offers_cannot_settle(self):
        for g in ('rw_cc_view_trigger = yes','rw_cc_context_trigger = yes','var:rw_cc_state = flag:offered','has_variable = rw_cc_window'):
            self.assertIn('expired terminal or unavailable offer accepted',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('unfunded or unconsented payment',self.errors(t=self.t.replace('rw_cc_responder_trigger = yes','always = yes')))

    def test_native_funds_rechecked_on_the_actual_provider_only(self):
        g='scope:rw_service_provider = { gold >= scope:rw_cc_price }'
        self.assertIn('unfunded or unconsented payment',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('unfunded or unconsented payment',self.errors(t=self.t.replace(g,'scope:rw_service_client = { gold >= scope:rw_cc_price }')))
        self.assertNotIn('gold',block(self.t,'rw_cc_can_propose_trigger'))
        self.assertNotIn('gold',block(self.t,'rw_cc_responder_trigger'))
        self.assertIn('desc = rw_case_compensation.unfunded',self.v)

    def test_terminal_receipt_written_before_both_gold_effects_and_notices(self):
        for g in ('remove_variable = rw_cc_window','name = rw_cc_paid_amount','name = rw_cc_paid_revision',
                  'name = rw_cc_paid_on','name = rw_cc_state value = flag:paid'):
            self.assertIn('payment before receipt consumption or early notice',self.errors(e=self.e.replace(g,'removed_field')))
        for gate in ('rw_cc_can_settle_trigger = yes','rw_cc_responder_trigger = yes','rw_cc_can_close_trigger = yes'):
            self.assertIn('unguarded financial effect',self.errors(e=self.e.replace('limit = { '+gate+' }','limit = { always = yes }')))

    def test_gold_direction_and_amount_never_follow_the_clicking_actor(self):
        for g in ('scope:rw_service_provider = { add_gold = { value = scope:rw_cc_price multiply = -1 } }',
                  'scope:rw_service_client = { add_gold = scope:rw_cc_price }'):
            self.assertIn('wrong payer amount or direction',self.errors(e=self.e.replace(g,'add_gold = 50')))
        self.assertIn('extra payment or refund path',self.errors(e=self.e+'\nadd_gold = 25'))
        pay=block(self.e,'rw_cc_settle_effect')
        self.assertNotIn('root',pay)
        self.assertNotIn('rw_service_last_',pay)
        self.assertNotIn('rw_case_service_price',pay)

    def test_counter_changes_turn_price_and_revision_but_not_original_window(self):
        for g in ('change_variable = { name = rw_cc_revision add = 1 }','name = rw_cc_turn value = flag:client',
                  'name = rw_cc_price value = 25','rw_cc_snapshot_effect = yes'):
            self.assertIn('old counter consent remains live',self.errors(e=self.e.replace(g,'always = yes')))
        self.assertIn('original response deadline reset',self.errors(e=self.e+'\nset_variable = { name = rw_cc_window value = flag:yes days = 7 }'))
        self.assertNotRegex(block(self.e,'rw_cc_counter_effect'),r'\bname\s*=\s*rw_cc_(window|issued_on|schema)\b')
        self.assertIn('immediate AI counter loop',self.errors(e=self.e.replace('.0001 days = 1','.0001')))

    def test_refresh_navigation_is_separate_from_old_reply_and_never_pays(self):
        self.assertIn('old reply refreshes consent on load',self.errors(v=self.v.replace('rw_case_compensation.0001 = {','rw_case_compensation.0001 = { immediate = {}')))
        prepare=block(self.e,'rw_cc_prepare_effect')
        for g in ('limit = { rw_cc_base_trigger = yes }','clear_saved_scope = rw_cc_revision','clear_saved_scope = rw_cc_price'):
            self.assertIn(g,prepare)
        self.assertNotRegex(prepare+block(self.e,'rw_cc_snapshot_effect'),r'\b(set_variable|add_gold|change_variable|remove_variable)\s*=')
        self.assertEqual(1,self.e.count('rw_cc_prepare_effect ='))
        self.assertIn('rw_cc_prepare_effect = yes',block(self.v,'rw_case_compensation.0002'))

    def test_identity_only_close_after_poverty_war_or_detention_is_free(self):
        close=block(self.t,'rw_cc_can_close_trigger')
        self.assertIn('rw_cc_view_trigger = yes',close)
        self.assertNotRegex(close,r'\b(rw_cc_context_trigger|rw_cc_window|gold|rw_cc_can_settle_trigger)\b')
        effect=block(self.e,'rw_cc_close_effect')
        self.assertLess(effect.index('name = rw_cc_state value = flag:closed'),effect.index('rw_cc_notify_effect'))
        self.assertNotRegex(effect,r'\b(add_gold|add_opinion|add_prestige)\s*=')

    def test_archive_remains_read_only_and_all_entries_recheck_before_navigation(self):
        events=(MOD/'events/rw_case_events.txt').read_text()
        for n in (3,5,6):
            b=block(events,f'rw_cases.{n:04}')
            option=b[b.index('name = rw_case_compensation.review'):]
            self.assertEqual(2,option.count('rw_cc_base_trigger = yes'))
            self.assertIn('id = rw_case_compensation.0002',option)
            self.assertNotIn('rw_cc_settle_effect',option)
        self.assertNotRegex(block(events,'rw_cases.0006'),r'\brw_\w+_effect\s*=')
        self.assertNotRegex(block(events,'rw_cases.0006'),r'\b(add_gold|set_variable)\s*=')

    def test_private_receipts_not_sent_to_mediator_or_successor(self):
        notify=block(self.e,'rw_cc_notify_effect')
        self.assertNotIn('rw_case_mediator',notify)
        self.assertIn('scope:rw_service_provider',notify)
        self.assertIn('scope:rw_service_client',notify)
        self.assertNotIn('rw_case_reader_allowed_trigger',self.t)
        self.assertNotRegex(self.e+self.t,r'\b(make_story_owner|house_head|top_liege|every_living_character)\b')

    def test_original_case_facts_apology_opinion_and_legal_state_never_rewritten(self):
        for var in ('rw_case_result','rw_case_evidence','rw_case_stage','rw_case_retained','rw_case_gesture',
                    'rw_service_last_outcome','rw_service_price'):
            injection=f'\nset_variable = {{ name = {var} value = flag:paid }}'
            self.assertIn('financial gesture rewrites original affair',self.errors(e=self.e+injection))
        for command in ('add_opinion = {}','remove_opinion = {}','add_secret = {}','add_prestige = 50','run_interaction = {}'):
            self.assertIn('payment buys native punishment pardon or unrelated effects',self.errors(e=self.e+'\n'+command))

    def test_ai_parity_existing_death_retention_and_no_new_callbacks_or_polling(self):
        self.assertNotRegex(clean_script(self.t+self.e)[0],r'\b(is_ai|create_story|add_character_flag|effect_group|on_action)\s*=')
        story=(MOD/'common/story_cycles/rw_political_cases.txt').read_text()
        self.assertIn('on_owner_death = { end_story = yes }',story)
        self.assertIn('days = 60',story)
        self.assertNotIn('rw_cc_',story)
        for action in ('propose','counter','settle','close'):
            self.assertIn('rw_cc_'+action+'_effect',self.v)
        self.assertIn('has_trait = generous',self.v)

    def test_bom_locales_cover_all_financial_state_and_boundary_keys(self):
        events=(MOD/'events/rw_case_events.txt').read_text()
        keys=set(re.findall(r'(?:title|name|desc)\s*=\s*(rw_case_compensation\.[\w.]+)',self.v+events))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_case_compensation_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertTrue(keys<=actual,keys-actual)
