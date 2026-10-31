"""Adversarial private-response wiring; no CK3 payment/opinion simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def response_errors(t,e,cc):
    out=[]
    begin=block(e,'rw_cp_begin_effect')
    for g in ('rw_cc_view_trigger = yes','exists = scope:rw_cp_fresh_payment',
              'scope:rw_cp_fresh_payment = scope:rw_case_record','var:rw_cc_state = flag:paid',
              'NOT = { has_variable = rw_cp_schema }'):
        if g not in begin:out.append('old foreign or repeated receipt creates consent')
    stamp=begin.find('name = rw_cp_schema value = 1')
    for g in ('paid_revision value = scope:rw_cc_revision','paid_amount value = scope:rw_cc_price',
              'paid_on value = var:rw_cc_paid_on','state value = flag:pending','window value = flag:yes days = 30'):
        if not 0 <= begin.find('name = rw_cp_'+g) < stamp:out.append('response identity or fixed window missing')
    pay=block(cc,'rw_cc_settle_effect')
    debit=pay.find('scope:rw_service_provider = { add_gold')
    credit=pay.find('scope:rw_service_client = { add_gold')
    token=pay.find('save_scope_as = rw_cp_fresh_payment')
    init=pay.find('rw_cp_begin_effect = yes')
    clear=pay.find('clear_saved_scope = rw_cp_fresh_payment')
    notice=pay.find('rw_cc_notify_effect = yes')
    if not 0 <= debit < credit < token < init < clear < notice:out.append('response created before payment or token survives notice')
    view=block(t,'rw_cp_view_trigger')
    for g in ('rw_cc_view_trigger = yes','var:rw_cc_state = flag:paid','var:rw_cp_schema = 1',
              'var:rw_cp_paid_revision = scope:rw_cc_revision','var:rw_cp_paid_amount = scope:rw_cc_price',
              'has_variable = rw_cp_paid_on','var:rw_cp_paid_on = var:rw_cc_paid_on','has_variable = rw_cp_responded_on'):
        if g not in view:out.append('wrong incomplete private payment response read')
    turn=block(t,'rw_cp_can_respond_trigger')
    for g in ('rw_cp_view_trigger = yes','this = scope:rw_service_client','scope:rw_service_provider = { is_alive = yes }',
              'var:rw_cp_state = flag:pending','has_variable = rw_cp_window'):
        if g not in turn:out.append('wrong payer heir dead target or expired response')
    for name,state in (('appreciate','appreciated'),('note','noted')):
        effect=block(e,'rw_cp_'+name+'_effect')
        for g in ('limit = { rw_cp_can_respond_trigger = yes }','remove_variable = rw_cp_window',
                  'name = rw_cp_state value = flag:'+state,'name = rw_cp_responded_on value = current_date'):
            if g not in effect:out.append('unguarded or replayable personal choice')
        points=[effect.find(g) for g in ('remove_variable = rw_cp_window','name = rw_cp_state',
                                         'name = rw_cp_responded_on','rw_cp_notify_payer_effect = yes')]
        if min(points)<0 or points!=sorted(points):out.append('notification before response consumed')
    appreciate=block(e,'rw_cp_appreciate_effect')
    points=[appreciate.find(g) for g in ('remove_variable = rw_cp_window','flag:appreciated','has_opinion_modifier','add_opinion','rw_cp_notify_payer_effect')]
    if min(points)<0 or points!=sorted(points):out.append('opinion replayed stacked or renewed')
    if 'NOT = { has_opinion_modifier = { target = scope:rw_service_provider modifier = rw_compensation_appreciated_opinion } }' not in appreciate:
        out.append('opinion replayed stacked or renewed')
    if 'add_opinion = { target = scope:rw_service_provider modifier = rw_compensation_appreciated_opinion }' not in appreciate:
        out.append('wrong opinion target or benefit')
    code=clean_script(e)[0]
    if re.search(r'\b(?:name|flag)\s*=\s*rw_(?!cp_)\w+',code):out.append('response rewrites financial or judicial fact')
    if re.search(r'\b(add_gold|add_prestige|remove_opinion|add_secret|add_hook|add_claim|imprison|death|run_interaction|send_interaction|change_title_holder|make_story_owner|create_story|every_living_character|every_in_global_list)\s*=',code):
        out.append('response refunds pays pardons or scans')
    if e.count('name = rw_cp_window')!=1:out.append('personal response window renewed')
    return out


class CompensationResponseTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_compensation_response_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_compensation_response_effects.txt').read_text()
        self.cc=(MOD/'common/scripted_effects/rw_case_compensation_effects.txt').read_text()
        self.v=(MOD/'events/rw_case_compensation_events.txt').read_text()

    def errors(self,t=None,e=None,cc=None):
        return response_errors(self.t if t is None else t,self.e if e is None else e,self.cc if cc is None else cc)

    def test_contract(self):self.assertEqual([],self.errors())

    def test_constructor_requires_fresh_exact_paid_receipt_not_history_or_duplicate(self):
        for g in ('rw_cc_view_trigger = yes','exists = scope:rw_cp_fresh_payment',
                  'scope:rw_cp_fresh_payment = scope:rw_case_record','var:rw_cc_state = flag:paid',
                  'NOT = { has_variable = rw_cp_schema }'):
            self.assertIn('old foreign or repeated receipt creates consent',self.errors(e=self.e.replace(g,'always = yes')))
        code='\n'.join(clean_script(p.read_text())[0] for p in MOD.rglob('*.txt'))
        self.assertEqual(1,len(re.findall(r'\brw_cp_begin_effect\s*=\s*yes',code)))
        self.assertEqual(1,len(re.findall(r'\bsave_scope_as\s*=\s*rw_cp_fresh_payment\b',code)))

    def test_initialization_after_both_gold_effects_then_token_cleared_before_notices(self):
        for g in ('scope:rw_service_provider = { add_gold','scope:rw_service_client = { add_gold',
                  'save_scope_as = rw_cp_fresh_payment','rw_cp_begin_effect = yes','clear_saved_scope = rw_cp_fresh_payment'):
            self.assertIn('response created before payment or token survives notice',self.errors(cc=self.cc.replace(g,'removed_part')))
        init=block(self.e,'rw_cp_begin_effect')
        self.assertNotRegex(init,r'\b(add_opinion|add_gold|add_prestige|trigger_event)\s*=')
        self.assertNotIn('rw_cp_appreciate_effect',self.cc)
        self.assertNotIn('rw_cp_note_effect',self.cc)

    def test_complete_paid_amount_revision_date_and_window_before_schema(self):
        for field in ('paid_revision','paid_amount','paid_on','state','window'):
            self.assertIn('response identity or fixed window missing',self.errors(e=self.e.replace('name = rw_cp_'+field,'name = removed_'+field)))
        self.assertIn('personal response window renewed',self.errors(e=self.e+'\nset_variable = { name = rw_cp_window value = flag:yes days = 30 }'))

    def test_private_response_binds_full_case_payment_tuple_and_original_date(self):
        for g in ('rw_cc_view_trigger = yes','var:rw_cc_state = flag:paid','var:rw_cp_schema = 1',
                  'var:rw_cp_paid_revision = scope:rw_cc_revision','var:rw_cp_paid_amount = scope:rw_cc_price',
                  'has_variable = rw_cp_paid_on','var:rw_cp_paid_on = var:rw_cc_paid_on','has_variable = rw_cp_responded_on'):
            self.assertIn('wrong incomplete private payment response read',self.errors(t=self.t.replace(g,'always = yes')))

    def test_only_original_beneficiary_with_living_original_payer_may_respond(self):
        for g in ('rw_cp_view_trigger = yes','this = scope:rw_service_client',
                  'scope:rw_service_provider = { is_alive = yes }','var:rw_cp_state = flag:pending','has_variable = rw_cp_window'):
            self.assertIn('wrong payer heir dead target or expired response',self.errors(t=self.t.replace(g,'always = yes')))
        # A personal reaction is separate from payment eligibility and judicial authority.
        turn=block(self.t,'rw_cp_can_respond_trigger')
        self.assertNotRegex(turn,r'\b(gold|rw_cc_context_trigger|rw_case_jurisdiction_trigger|top_liege|house_head)\b')

    def test_each_personal_effect_rechecks_and_consumes_before_date_and_notice(self):
        for g in ('limit = { rw_cp_can_respond_trigger = yes }','remove_variable = rw_cp_window',
                  'name = rw_cp_responded_on value = current_date'):
            self.assertIn('unguarded or replayable personal choice',self.errors(e=self.e.replace(g,'always = yes')))
        for state in ('appreciated','noted'):
            self.assertIn('unguarded or replayable personal choice',self.errors(e=self.e.replace('flag:'+state,'flag:pending')))
        self.assertIn('notification before response consumed',self.errors(e=self.e.replace('rw_cp_notify_payer_effect = yes','')))

    def test_appreciation_once_only_without_modifier_stacking_or_refresh(self):
        self.assertIn('opinion replayed stacked or renewed',self.errors(e=self.e.replace('has_opinion_modifier','has_character_flag')))
        self.assertIn('opinion replayed stacked or renewed',self.errors(e=self.e.replace('remove_variable = rw_cp_window','')))
        self.assertIn('wrong opinion target or benefit',self.errors(e=self.e.replace('add_opinion = { target = scope:rw_service_provider','add_opinion = { target = scope:rw_service_client')))
        opinion=(MOD/'common/opinion_modifiers/rw_compensation_response_opinions.txt').read_text()
        self.assertRegex(opinion,r'\bopinion\s*=\s*5\b')
        self.assertRegex(opinion,r'\byears\s*=\s*2\b')

    def test_neutral_acknowledgment_has_no_opinion_cost_refund_or_forced_forgiveness(self):
        note=block(self.e,'rw_cp_note_effect')
        self.assertIn('flag:noted',note)
        self.assertNotRegex(note,r'\b(add_opinion|remove_opinion|add_gold|add_prestige|rw_cc_settle_effect)\s*=')
        self.assertNotIn('rw_case_gesture',self.e)
        self.assertNotIn('rw_broken_service_opinion',self.e)

    def test_expired_missing_or_malformed_data_never_means_silent_consent(self):
        self.assertIn('desc = rw_compensation_response.unanswered',self.v)
        self.assertIn('desc = rw_compensation_response.unknown',self.v)
        self.assertIn('scope:rw_service_client = { is_alive = yes }',self.v)
        self.assertNotIn('rw_cp_begin_effect',self.v)
        self.assertNotIn('rw_cp_appreciate_effect',block(self.v,'rw_case_compensation.0002'))
        self.assertNotRegex(self.e+self.t,r'\b(effect_group|on_owner_death|on_action|every_owned_story)\b')

    def test_response_does_not_repeat_payment_or_change_parent_case_terms(self):
        for var in ('rw_cc_state','rw_cc_price','rw_cc_paid_on','rw_case_retained','rw_case_result','rw_case_gesture','rw_service_last_outcome'):
            self.assertIn('response rewrites financial or judicial fact',self.errors(e=self.e+f'\nset_variable = {{ name = {var} value = flag:appreciated }}'))
        for command in ('add_gold = 50','add_prestige = 25','remove_opinion = {}','add_hook = {}','run_interaction = {}'):
            self.assertIn('response refunds pays pardons or scans',self.errors(e=self.e+'\n'+command))
        self.assertEqual(2,len(re.findall(r'\badd_gold\s*=',clean_script(self.cc)[0])))

    def test_payer_notice_is_private_and_never_to_the_mediator_or_successor(self):
        notify=block(self.e,'rw_cp_notify_payer_effect')
        self.assertIn('scope:rw_service_provider',notify)
        self.assertIn('limit = { is_alive = yes }',notify)
        self.assertIn('id = rw_case_compensation.0001',notify)
        self.assertNotRegex(notify,r'\b(rw_case_mediator|rw_service_client|top_liege|house_head|heir)\b')
        self.assertEqual(1,len(re.findall(r'\btrigger_event\s*=',self.e)))

    def test_ai_and_player_share_explicit_choices_and_opinion_prerequisites(self):
        self.assertNotRegex(clean_script(self.e+self.t)[0],r'\bis_ai\s*=')
        for name in ('appreciate','note'):
            self.assertIn('rw_cp_'+name+'_effect = yes',self.v)
        self.assertEqual(2,self.v.count('trigger = { rw_cp_can_respond_trigger = yes }'))
        self.assertIn('has_trait = forgiving',self.v)
        self.assertIn('has_trait = vengeful',self.v)
        self.assertIn('target = scope:rw_service_provider value < -25',self.v)
        self.assertIn('option = { name = rw_case_compensation.leave ai_chance = { base = 50 } }',self.v)

    def test_existing_retention_provider_death_and_private_role_filter_still_apply(self):
        cc=(MOD/'common/scripted_triggers/rw_case_compensation_triggers.txt').read_text()
        base=block(cc,'rw_cc_base_trigger')
        self.assertIn('this = scope:rw_service_provider',base)
        self.assertIn('this = scope:rw_service_client',base)
        self.assertIn('has_variable = rw_case_retained',base)
        story=(MOD/'common/story_cycles/rw_political_cases.txt').read_text()
        self.assertIn('on_owner_death = { end_story = yes }',story)
        self.assertNotIn('rw_cp_',story)
        self.assertNotRegex(self.e,r'\b(make_story_owner|create_story|add_to_global_variable_list)\s*=')

    def test_bom_localizations_cover_choices_historical_effects_and_silence(self):
        keys=set(re.findall(r'(?:name|desc)\s*=\s*(rw_compensation_response\.[\w.]+)',self.v))
        keys.add('rw_compensation_appreciated_opinion')
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_compensation_response_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertTrue(keys<=actual,keys-actual)
