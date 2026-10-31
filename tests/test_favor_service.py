"""Adversarial favor/gold source wiring; no native favor or exchange simulation."""
from pathlib import Path
import json
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mod/real_westeros'


def favor_errors(t,e):
    out=[]
    native=block(t,'rw_fv_favor_available_trigger')
    for g in ('$PROVIDER$ = {','NOT = { has_hook = $CLIENT$ }','can_add_hook = { type = favor_hook target = $CLIENT$ }'):
        if g not in native:out.append('detected existing or natively invalid hook overwritten')
    begin_gate=block(t,'rw_fv_can_offer_trigger')
    for g in ('scope:actor = { rw_service_provider_available_trigger = yes is_imprisoned = no }',
              'scope:recipient = { rw_service_party_eligible_trigger = yes is_imprisoned = no }',
              'NOT = { scope:actor = scope:recipient }',
              'rw_fv_favor_available_trigger = { PROVIDER = scope:actor CLIENT = scope:recipient }'):
        if g not in begin_gate:out.append('unavailable or wrong initiating parties')
    view=block(t,'rw_fv_view_trigger')
    for g in ('exists = scope:rw_fv_provider','exists = scope:rw_fv_client','exists = scope:rw_fv_serial',
              'exists = scope:rw_fv_revision','exists = scope:rw_fv_term','this = scope:rw_fv_provider','this = scope:rw_fv_client',
              'var:rw_fv_schema = 1','var:rw_fv_serial = scope:rw_fv_serial','var:rw_fv_revision = scope:rw_fv_revision',
              'var:rw_fv_client = scope:rw_fv_client','var:rw_fv_term = scope:rw_fv_term','has_variable = rw_fv_issued_on',
              'var:rw_fv_term = flag:favor','var:rw_fv_term = flag:gold25','has_variable = rw_fv_finished_on'):
        if g not in view:out.append('stale foreign or malformed service ticket')
    live=block(t,'rw_fv_live_trigger')
    for g in ('rw_fv_view_trigger = yes','has_character_flag = rw_fv_pending','var:rw_fv_state = flag:offered'):
        if g not in live:out.append('expired terminal or unavailable exchange performed')
    if live.count('rw_service_party_eligible_trigger = yes')!=2 or live.count('is_imprisoned = no')!=2:
        out.append('expired terminal or unavailable exchange performed')
    for name,party,term in (('client','client','favor'),('provider','provider','gold25')):
        turn=block(t,'rw_fv_'+name+'_turn_trigger')
        for g in ('rw_fv_live_trigger = yes','this = scope:rw_fv_'+party,'var:rw_fv_turn = flag:'+party,'var:rw_fv_term = flag:'+term):
            if g not in turn:out.append('wrong responder or consideration accepted')
    for name,turn in (('rw_fv_can_accept_favor_trigger','client'),('rw_fv_can_restate_trigger','provider')):
        gate=block(t,name)
        if 'rw_fv_'+turn+'_turn_trigger = yes' not in gate or 'rw_fv_favor_available_trigger = { PROVIDER = scope:rw_fv_provider CLIENT = scope:rw_fv_client }' not in gate:
            out.append('native eligibility not rechecked for latest favor')
    gold=block(t,'rw_fv_can_accept_gold_trigger')
    if 'rw_fv_provider_turn_trigger = yes' not in gold or 'scope:rw_fv_client = { gold >= 25 }' not in gold:
        out.append('gold branch lacks current consent or actual payer funds')
    begin=block(e,'rw_fv_begin_effect')
    for g in ('limit = { rw_fv_can_offer_trigger = yes }','NOT = { has_variable = rw_fv_serial }',
              'change_variable = { name = rw_fv_serial add = 1 }','name = rw_fv_revision value = 0',
              'flag = rw_fv_pending days = 30','flag = rw_service_cooldown days = 365','rw_fv_snapshot_effect = yes'):
        if g not in begin:out.append('constructor identity clock or shared cooldown missing')
    if e.count('flag = rw_fv_pending days = 30')!=1:out.append('offer deadline renewed')
    for name,gate in (('rw_fv_counter_gold_effect','rw_fv_client_turn_trigger'),('rw_fv_restate_effect','rw_fv_can_restate_trigger'),('rw_fv_close_effect','rw_fv_can_close_trigger')):
        if 'limit = { '+gate+' = yes }' not in block(e,name):out.append('direct effect bypass')
    for name in ('rw_fv_counter_gold_effect','rw_fv_restate_effect'):
        counter=block(e,name)
        if 'change_variable = { name = rw_fv_revision add = 1 }' not in counter or 'rw_fv_snapshot_effect = yes' not in counter:
            out.append('old consent survives counteroffer')
        if 'id = rw_favor_service.0001 days = 1' not in counter:out.append('immediate AI counter loop')
    settle=block(e,'rw_fv_settle_effect')
    if 'OR = { rw_fv_can_accept_favor_trigger = yes rw_fv_can_accept_gold_trigger = yes }' not in settle:
        out.append('unguarded native exchange')
    points=[settle.find(g) for g in ('remove_character_flag = rw_fv_pending','name = rw_fv_state value = flag:fulfilled',
                                   'add_hook','add_prestige = 50','rw_fv_notify_effect = yes')]
    if min(points)<0 or points!=sorted(points):out.append('native performance before ticket consumption')
    for g in ('limit = { scope:rw_fv_term = flag:favor }',
              'scope:rw_fv_provider = { add_hook = { type = favor_hook target = scope:rw_fv_client } }',
              'scope:rw_fv_client = { add_gold = -25 }','scope:rw_fv_provider = { add_gold = 25 }',
              'scope:rw_fv_client = { add_prestige = 50 }'):
        if g not in settle:out.append('wrong native favor gold direction or service benefit')
    code=clean_script(e)[0]
    if len(re.findall(r'\badd_hook\s*=',code))!=1 or len(re.findall(r'\badd_gold\s*=',code))!=2 or len(re.findall(r'\badd_prestige\s*=',code))!=1:
        out.append('extra native effect or replay path')
    if re.search(r'\b(?:name|flag)\s*=\s*rw_service_(?!cooldown\b)\w+',code):out.append('old financial contract reactivated or rewritten')
    if re.search(r'\b(remove_hook|use_hook|change_title_holder|create_title_and_vassal_change|run_interaction|send_interaction|add_secret|add_claim|imprison|make_story_owner|every_living_character|every_in_global_list)\s*=',code):
        out.append('native hook use coercion or global policy added')
    return out


class FavorServiceTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_favor_service_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_favor_service_effects.txt').read_text()
        self.v=(MOD/'events/rw_favor_service_events.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_favor_service_interactions.txt').read_text()

    def errors(self,t=None,e=None):return favor_errors(self.t if t is None else t,self.e if e is None else e)

    def test_contract(self):self.assertEqual([],self.errors())

    def test_native_creation_is_preflighted_and_existing_hook_is_not_refreshed(self):
        for g in ('NOT = { has_hook = $CLIENT$ }','can_add_hook = { type = favor_hook target = $CLIENT$ }'):
            self.assertIn('detected existing or natively invalid hook overwritten',self.errors(t=self.t.replace(g,'always = yes')))
        for name in ('rw_fv_can_accept_favor_trigger','rw_fv_can_restate_trigger'):
            b=block(self.t,name)
            self.assertIn('rw_fv_favor_available_trigger = { PROVIDER = scope:rw_fv_provider CLIENT = scope:rw_fv_client }',b)
        self.assertIn('native eligibility not rechecked for latest favor',self.errors(t=self.t.replace('rw_fv_favor_available_trigger = { PROVIDER = scope:rw_fv_provider CLIENT = scope:rw_fv_client }','always = yes')))

    def test_full_actual_parties_availability_and_native_context_at_offer(self):
        for g in ('scope:actor = { rw_service_provider_available_trigger = yes is_imprisoned = no }',
                  'scope:recipient = { rw_service_party_eligible_trigger = yes is_imprisoned = no }',
                  'NOT = { scope:actor = scope:recipient }'):
            self.assertIn('unavailable or wrong initiating parties',self.errors(t=self.t.replace(g,'always = yes')))
        begin=block(self.e,'rw_fv_begin_effect')
        self.assertNotRegex(begin,r'\b(add_gold|add_hook|add_prestige)\s*=')
        self.assertIn('on_accept = { rw_fv_begin_effect = yes }',self.i)

    def test_ticket_binds_original_provider_client_serial_revision_and_consideration(self):
        for g in ('exists = scope:rw_fv_serial','exists = scope:rw_fv_revision','var:rw_fv_schema = 1',
                  'var:rw_fv_serial = scope:rw_fv_serial','var:rw_fv_revision = scope:rw_fv_revision',
                  'var:rw_fv_client = scope:rw_fv_client','var:rw_fv_term = scope:rw_fv_term','has_variable = rw_fv_finished_on'):
            self.assertIn('stale foreign or malformed service ticket',self.errors(t=self.t.replace(g,'always = yes')))

    def test_pending_deadline_and_both_current_free_landed_parties_before_execution(self):
        for g in ('rw_fv_view_trigger = yes','has_character_flag = rw_fv_pending','var:rw_fv_state = flag:offered',
                  'rw_service_party_eligible_trigger = yes','is_imprisoned = no'):
            self.assertIn('expired terminal or unavailable exchange performed',self.errors(t=self.t.replace(g,'always = yes')))

    def test_only_client_accepts_favor_and_provider_accepts_current_gold_counter(self):
        for g in ('this = scope:rw_fv_client','this = scope:rw_fv_provider','var:rw_fv_turn = flag:client',
                  'var:rw_fv_turn = flag:provider','var:rw_fv_term = flag:favor','var:rw_fv_term = flag:gold25'):
            self.assertIn('wrong responder or consideration accepted',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('unguarded native exchange',self.errors(e=self.e.replace('OR = { rw_fv_can_accept_favor_trigger = yes rw_fv_can_accept_gold_trigger = yes }','always = yes')))

    def test_gold_branch_rechecks_actual_client_funds_and_needs_no_new_hook(self):
        g='scope:rw_fv_client = { gold >= 25 }'
        self.assertIn('gold branch lacks current consent or actual payer funds',self.errors(t=self.t.replace(g,'scope:rw_fv_provider = { gold >= 25 }')))
        self.assertNotIn('rw_fv_favor_available_trigger',block(self.t,'rw_fv_can_accept_gold_trigger'))
        self.assertNotIn('gold',block(self.t,'rw_fv_client_turn_trigger'))
        self.assertIn('desc = rw_favor_service.favor_unavailable',self.v)
        self.assertIn('desc = rw_favor_service.unfunded',self.v)

    def test_shared_original_service_pool_without_reactivating_old_quote_identity(self):
        old=(MOD/'common/scripted_triggers/rw_service_triggers.txt').read_text()
        available=block(old,'rw_service_provider_available_trigger')
        for g in ('NOT = { has_character_flag = rw_service_pending }','NOT = { has_character_flag = rw_service_obligation }',
                  'NOT = { has_character_flag = rw_service_cooldown }','NOT = { has_character_flag = rw_fv_pending }'):
            self.assertIn(g,available)
        self.assertIn('flag = rw_service_cooldown days = 365',self.e)
        for var in ('pending','obligation','serial','revision','mode','target'):
            self.assertIn('old financial contract reactivated or rewritten',self.errors(e=self.e+f'\nset_variable = {{ name = rw_service_{var} value = 1 }}'))
        self.assertNotIn('rw_service_clear_effect',self.e)

    def test_monotonic_serial_shared_cooldown_and_fixed_single_original_offer_window(self):
        for g in ('NOT = { has_variable = rw_fv_serial }','change_variable = { name = rw_fv_serial add = 1 }',
                  'flag = rw_service_cooldown days = 365','flag = rw_fv_pending days = 30'):
            self.assertIn('constructor identity clock or shared cooldown missing',self.errors(e=self.e.replace(g,'removed_part')))
        self.assertIn('offer deadline renewed',self.errors(e=self.e+'\nadd_character_flag = { flag = rw_fv_pending days = 30 }'))
        self.assertNotIn('remove_variable = rw_fv_serial',self.e)
        self.assertNotIn('remove_character_flag = rw_service_cooldown',self.e)

    def test_counteroffers_change_revision_turn_and_term_without_resetting_time(self):
        for g in ('change_variable = { name = rw_fv_revision add = 1 }','rw_fv_snapshot_effect = yes'):
            self.assertIn('old consent survives counteroffer',self.errors(e=self.e.replace(g,'removed_part')))
        for name,gate in (('rw_fv_counter_gold_effect','rw_fv_client_turn_trigger'),('rw_fv_restate_effect','rw_fv_can_restate_trigger')):
            self.assertIn('direct effect bypass',self.errors(e=self.e.replace('limit = { '+gate+' = yes }','limit = { always = yes }')))
            self.assertNotIn('add_character_flag',block(self.e,name))
        self.assertIn('immediate AI counter loop',self.errors(e=self.e.replace('.0001 days = 1','.0001')))

    def test_consume_before_any_native_hook_gold_prestige_or_notice(self):
        for g in ('remove_character_flag = rw_fv_pending','name = rw_fv_state value = flag:fulfilled'):
            self.assertIn('native performance before ticket consumption',self.errors(e=self.e.replace(g,'removed_part')))
        self.assertIn('extra native effect or replay path',self.errors(e=self.e+'\nadd_hook = {}'))
        self.assertIn('extra native effect or replay path',self.errors(e=self.e+'\nadd_gold = 25'))
        self.assertIn('extra native effect or replay path',self.errors(e=self.e+'\nadd_prestige = 50'))

    def test_correct_hook_direction_and_mutually_selected_gold_alternative(self):
        for g in ('limit = { scope:rw_fv_term = flag:favor }',
                  'scope:rw_fv_provider = { add_hook = { type = favor_hook target = scope:rw_fv_client } }',
                  'scope:rw_fv_client = { add_gold = -25 }','scope:rw_fv_provider = { add_gold = 25 }',
                  'scope:rw_fv_client = { add_prestige = 50 }'):
            self.assertIn('wrong native favor gold direction or service benefit',self.errors(e=self.e.replace(g,'removed_part')))
        self.assertNotIn('rw_fv_settle_effect',block(self.e,'rw_fv_notify_effect'))

    def test_identity_only_closure_is_free_after_expiry_war_or_imprisonment(self):
        gate=block(self.t,'rw_fv_can_close_trigger')
        self.assertIn('rw_fv_view_trigger = yes',gate)
        self.assertNotRegex(gate,r'\b(rw_fv_live_trigger|rw_fv_pending|gold|can_add_hook)\b')
        close=block(self.e,'rw_fv_close_effect')
        self.assertNotRegex(close,r'\b(add_gold|add_hook|add_prestige|remove_hook)\s*=')
        self.assertIn('name = rw_fv_state value = flag:closed',close)

    def test_private_latest_record_review_does_not_renew_grant_or_pay(self):
        gate=block(self.t,'rw_fv_review_allowed_trigger')
        self.assertIn('scope:actor = scope:recipient',gate)
        self.assertIn('scope:actor = scope:recipient.var:rw_fv_client',gate)
        review=block(self.e,'rw_fv_review_effect')
        self.assertIn('limit = { rw_fv_review_allowed_trigger = yes }',review)
        self.assertNotRegex(review+block(self.e,'rw_fv_snapshot_effect'),r'\b(set_variable|add_character_flag|add_gold|add_hook|add_prestige)\s*=')
        self.assertIn('is_shown = { rw_fv_review_allowed_trigger = yes }',self.i)
        self.assertNotIn('immediate',self.v)

    def test_existing_native_hook_types_use_expiry_and_war_laws_are_not_replaced(self):
        for command in ('remove_hook = {}','use_hook = {}','run_interaction = {}','change_title_holder = root','every_living_character = {}'):
            self.assertIn('native hook use coercion or global policy added',self.errors(e=self.e+'\n'+command))
        self.assertFalse((MOD/'common/hook_types').exists())
        self.assertNotRegex(self.e,r'\b(on_action|create_story|make_story_owner)\s*=')
        self.assertNotIn('rw_case_',self.e)
        self.assertNotIn('rw_service_last_',self.e)

    def test_ai_and_player_share_execution_eligibility_and_bounded_liege_targets(self):
        self.assertNotRegex(clean_script(self.t+self.e)[0],r'\bis_ai\s*=')
        self.assertIn('ai_targets = { ai_recipients = liege }',self.i)
        self.assertIn('ai_frequency = 12',self.i)
        self.assertIn('ai_will_do = { base = 0 }',self.i)
        for choice in ('accept_favor','counter_gold','accept_gold','restate','close','leave'):
            self.assertIn('name = rw_favor_service.'+choice,self.v)
        self.assertIn('has_trait = paranoid',self.v)
        self.assertIn('has_trait = greedy',self.v)

    def test_source_receipt_is_selected_hash_only_metadata(self):
        receipt=json.loads((ROOT/'docs/FAVOR_SERVICE_SOURCE_RECEIPT.json').read_text())
        self.assertEqual(3,len(receipt['reviewed_references']))
        for ref in receipt['reviewed_references']:
            self.assertEqual({'source','path','sha256','size','markers'},set(ref))
            self.assertRegex(ref['sha256'],r'^[0-9a-f]{64}$')
            self.assertGreater(ref['size'],0)
            self.assertFalse(Path(ref['path']).is_absolute())
            self.assertTrue(all(ref['markers'].values()))

    def test_localization_bom_covers_terms_outcomes_and_native_limits(self):
        keys=set(re.findall(r'(?:name|desc|title)\s*=\s*(rw_favor_service\.[\w.]+|rw_\w+_interaction_desc)',self.v+self.i))
        keys.update(('rw_offer_favor_endorsement_interaction','rw_review_favor_endorsement_interaction'))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_favor_service_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertTrue(keys<=actual,keys-actual)
