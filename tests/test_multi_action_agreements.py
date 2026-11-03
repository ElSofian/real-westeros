"""Adversarial CK3 source contracts, not a Python multi-action game prototype."""
from pathlib import Path
import re
import unittest
from contract_source import expand_contracts, CALL, ARG
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from test_political_ai import option
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def agreement_errors(t,e,ev):
    errors=[]
    def need(body,parts,message):
        if any(p not in body for p in parts):errors.append(message)
    record=block(t,'rw_ba_record_trigger')
    need(record,('story_type = story_rw_multi_action_agreement','var:rw_ba_schema = 1',
        'var:rw_ba_recipe = flag:gold_support_release','has_variable = rw_ba_serial',
        'var:rw_ba_issuer = var:rw_ba_payer','NOT = { var:rw_ba_payer = var:rw_ba_payee }',
        'has_variable = rw_ba_retained','var:rw_ba_accepted_revision = var:rw_ba_revision',
        'var:rw_ba_accepted_price = var:rw_ba_price'), 'foreign malformed or changed signed packet')
    reader=block(t,'rw_ba_reader_trigger')
    need(reader,('rw_ba_record_trigger = yes','$READER$ = { is_alive = yes }',
                 'OR = { var:rw_ba_payer = $READER$ var:rw_ba_payee = $READER$ }'),'custody or heir grants private access')
    if re.search(r'\b(?:story_owner|house_head|holder|house)\s*=',reader):errors.append('custody or heir grants private access')
    view=block(t,'rw_ba_view_trigger')
    for key in ('serial','issuer','payer','payee','parent_revision','source_serial','title','authority','house'):
        if 'var:rw_ba_'+key+' = scope:rw_ba_'+key not in view:errors.append('stale record source or parties admitted')
    need(view,('rw_ba_reader_trigger = { READER = root }','var:rw_ba_revision = scope:rw_ba_revision',
               'var:rw_ba_price = scope:rw_ba_price'),'stale record source or parties admitted')
    source=block(t,'rw_ba_source_context_trigger')
    need(source,('exists = scope:rw_ba_record.var:rw_ba_source','rw_lr_record_valid_trigger = yes',
        'has_variable = rw_lr_retained','var:rw_lr_serial = scope:rw_ba_source_serial',
        'var:rw_lr_title = scope:rw_ba_title','var:rw_lr_authority = scope:rw_ba_authority',
        'var:rw_lr_former_house = scope:rw_ba_house','var:rw_ch_revision = scope:rw_ba_parent_revision',
        'var:rw_ch_state = flag:active','has_variable = rw_ch_due',
        'var:rw_ch_recognized_by = scope:rw_ba_payer','holder = scope:rw_ba_payer','house_head = scope:rw_ba_payee'),
        'different charter revision or successor can release')
    response=block(t,'rw_ba_responder_trigger')
    need(response,('rw_ba_view_trigger = yes','rw_ba_parties_trigger = yes','rw_ba_source_context_trigger = yes',
        'var:rw_ba_agreement = flag:negotiating','var:rw_ba_state = flag:offered','has_variable = rw_ba_window',
        'this = scope:rw_ba_payer','var:rw_ba_offered_by = scope:rw_ba_payee',
        'this = scope:rw_ba_payee','var:rw_ba_offered_by = scope:rw_ba_payer'), 'self acceptance stale or inherited consent')
    propose=block(t,'rw_ba_can_propose_trigger')
    need(propose,('rw_ch_active_trigger = yes','this = scope:rw_ch_ruler','NOT = { has_character_flag = rw_ba_recent }',
        'NOT = { var:rw_ba_last_parent_revision = scope:rw_ch_revision }',
        'NOT = { var:rw_ba_last_payer = scope:rw_ch_ruler }','NOT = { var:rw_ba_last_payee = scope:rw_ch_head }'),
        'replayed same-context bundle or no issuer authority')
    constructor=block(e,'rw_ba_propose_effect')
    need(constructor,('limit = { scope:rw_ba_record = { rw_ba_record_trigger = yes } }',
                      'else = { scope:rw_ba_record = { rw_ba_retire_effect = yes } }'),
                      'uninitialized story consumes source context or leaks into index')
    accept=block(e,'rw_ba_accept_effect')
    need(accept,('limit = { rw_ba_responder_trigger = yes }','save_scope_as = rw_ba_signer',
        'name = rw_ba_state value = flag:closed','name = rw_ba_accepted_by value = scope:rw_ba_signer',
        'name = rw_ba_accepted_revision value = scope:rw_ba_revision','name = rw_ba_accepted_price value = scope:rw_ba_price',
        'name = rw_ba_agreement value = flag:active','name = rw_ba_due value = flag:yes days = 30',
        *('name = rw_ba_'+leg+' value = flag:pending' for leg in ('gold','support','release'))),
        'acceptance not one immutable three-clause signature')
    for name in ('propose','counter','accept'):
        if re.search(r'\b(?:add_gold|add_prestige|rw_ch_release_effect|rw_pm_public_support_effect)\s*=',block(e,'rw_ba_'+name+'_effect')):
            errors.append('native performance before signature or by acceptance')
    counter=block(e,'rw_ba_counter_effect')
    need(counter,('limit = { rw_ba_responder_trigger = yes }','change_variable = { name = rw_ba_revision add = 1 }',
                  'name = rw_ba_offered_by value = scope:rw_ba_counterer','rw_ba_snapshot_effect = yes'), 'counter reuses previous consent')
    for name in ('counter','read','notify'):
        if re.search(r'\bname\s*=\s*rw_ba_(?:due|window|retained)\b',block(e,'rw_ba_'+name+'_effect')):
            errors.append('quote refresh or notification renews deadline')
    active=block(t,'rw_ba_active_trigger')
    need(active,('rw_ba_view_trigger = yes','rw_ba_parties_trigger = yes','var:rw_ba_agreement = flag:active','has_variable = rw_ba_due'), 'execution outside signed lifetime')
    for leg,actor in (('pay','payer'),('support','payer'),('release','payee')):
        kind='gold' if leg=='pay' else leg
        gate=block(t,'rw_ba_can_'+leg+'_trigger')
        need(gate,('rw_ba_active_trigger = yes','this = scope:rw_ba_'+actor,'var:rw_ba_'+kind+' = flag:pending'),'wrong actor or repeated individual action')
        body=block(e,'rw_ba_'+leg+'_effect')
        need(body,('limit = { rw_ba_can_'+leg+'_trigger = yes }',
                   'name = rw_ba_'+kind+' value = flag:attempted','name = rw_ba_'+kind+'_actor value = scope:rw_ba_'+actor),
                   'individual effect lacks fresh guard or consumed attempt')
    if 'gold >= scope:rw_ba_price' not in block(t,'rw_ba_can_pay_trigger'):errors.append('unfunded actual payer spends')
    for name in ('rw_ba_active_trigger','rw_ba_can_pay_trigger','rw_ba_can_support_trigger'):
        if re.search(r'rw_(?:ch_active|ba_source_context)_trigger',block(t,name)):
            errors.append('earlier release blocks independent later promises')
    pay=block(e,'rw_ba_pay_effect')
    seq=[pay.find(p) for p in ('name = rw_ba_gold value = flag:attempted','name = rw_ba_paid_revision value = scope:rw_ba_revision',
        'add_gold = { value = scope:rw_ba_price multiply = -1 }','scope:rw_ba_payee = { add_gold = scope:rw_ba_price }','name = rw_ba_gold value = flag:done')]
    if min(seq)<0 or seq!=sorted(seq):errors.append('duplicate wrong-direction or unconsumed payment')
    support=block(e,'rw_ba_support_effect')
    seq=[support.find(p) for p in ('name = rw_ba_support value = flag:attempted','scope:rw_ba_payee = { add_prestige = 50 }',
        'rw_pm_public_support_effect = { PROVIDER = scope:rw_ba_payer CLIENT = scope:rw_ba_payee }','name = rw_ba_support value = flag:done')]
    if min(seq)<0 or seq!=sorted(seq):errors.append('support replay wrong recipient or memory before performance')
    release=block(e,'rw_ba_release_effect')
    need(release,('rw_ch_can_release_trigger = yes','rw_ch_release_effect = yes','var:rw_ch_state = flag:released',
        'var:rw_ch_finished_by = scope:rw_ba_payee','var:rw_ch_finished_on = current_date',
        'var:rw_ch_revision = scope:rw_ba_record.var:rw_ba_release_revision','name = rw_ba_release_result_revision',
        'name = rw_ba_release_quote_revision value = scope:rw_ba_revision'), 'unrelated release falsely credited')
    if release.find('rw_ch_release_effect = yes')<release.find('name = rw_ba_release value = flag:attempted'):
        errors.append('release replay before consumed attempt')
    refuse=block(t,'rw_ba_can_refuse_trigger')
    need(refuse,('rw_ba_view_trigger = yes','has_variable = rw_ba_due','var:rw_ba_$LEG$ = flag:pending',
                 'this = scope:rw_ba_payer always = $PAYER$','this = scope:rw_ba_payee always = $PAYEE$'),'refusal alters completed or another persons action')
    if re.search(r'gold\s*[<>]|rw_ba_(?:parties|source_context)_trigger',refuse):errors.append('refusal demands means or authority')
    for leg,pa,pe in (('gold','yes','no'),('support','yes','no'),('release','no','yes')):
        body=option(ev,'rw_multi_actions.refuse_'+leg)
        binding='LEG = '+leg+' PAYER = '+pa+' PAYEE = '+pe
        if body.count(binding)!=2:errors.append('wrong obligation owner in refusal UI')
        need(record,('var:rw_ba_'+leg+'_refused_by = var:rw_ba_'+('payee' if leg=='release' else 'payer'),
                     'has_variable = rw_ba_'+leg+'_refused_on'),'unsupported explicit-refusal receipt')
    resolver=block(e,'rw_ba_resolve_effect')
    need(resolver,('NOT = { has_variable = rw_ba_due }','var:rw_ba_gold = flag:done var:rw_ba_support = flag:done var:rw_ba_release = flag:done',
        'name = rw_ba_agreement value = flag:fulfilled','name = rw_ba_agreement value = flag:partial'), 'partial performance disguised as full settlement')
    if re.search(r'\b(?:add_gold|add_prestige|rw_ch_release_effect|create_character_memory)\s*=',resolver):errors.append('expiry rollback reward or automatic performance')
    death=block(e,'rw_ba_owner_died_effect')
    need(death,('story_owner = { save_scope_as = rw_ba_departed }','rw_ba_rehome_effect = yes','rw_ba_retire_effect = yes'),'death loses custody isolation or index cleanup')
    rehome=block(e,'rw_ba_rehome_effect')
    if rehome.count('NOT = { this = scope:rw_ba_departed }')!=2 or re.search(r'house_head|holder|dynasty',rehome):errors.append('dead custodian or heir inherits personal consent')
    retire=block(e,'rw_ba_retire_effect')
    if retire.find('remove_list_global_variable')<0 or retire.find('remove_list_global_variable')>retire.find('end_story = yes'):
        errors.append('retired agreement remains globally indexed')
    code=clean_script(t+e+ev)[0]
    if re.search(r'\b(?:imprison|run_interaction|change_title_holder|add_secret|add_hook|add_claim|is_ai|every_living_character|any_living_character)\s*=',code):errors.append('native override legal proof or AI privilege')
    return errors


class MultiActionAgreementTests(unittest.TestCase):
    def setUp(self):
        self.t=expand_contracts((MOD/'common/scripted_triggers/rw_multi_action_triggers.txt').read_text())
        self.e=expand_contracts((MOD/'common/scripted_effects/rw_multi_action_effects.txt').read_text())
        self.v=(MOD/'events/rw_multi_action_events.txt').read_text()

    def errors(self,field=None,old=None,new=None):
        src={'t':self.t,'e':self.e,'v':self.v}
        if field:src[field]=src[field].replace(old,new)
        return agreement_errors(src['t'],src['e'],src['v'])

    def test_source_contract(self):self.assertEqual([],self.errors())
    def test_identity_recipe_revision_originals_and_retention_fail_closed(self):
        for g in ('var:rw_ba_recipe = flag:gold_support_release','var:rw_ba_accepted_revision = var:rw_ba_revision','has_variable = rw_ba_retained','var:rw_ba_issuer = var:rw_ba_payer'):
            self.assertIn('foreign malformed or changed signed packet',self.errors('t',g,'always = yes'))
    def test_custody_or_house_succession_is_not_access(self):
        self.assertIn('custody or heir grants private access',self.errors('t','OR = { var:rw_ba_payer = $READER$ var:rw_ba_payee = $READER$ }','story_owner = $READER$'))
    def test_stale_record_source_and_party_aliases_rejected(self):
        for field in ('serial','issuer','parent_revision','payer','payee','title','house','authority'):
            self.assertIn('stale record source or parties admitted',self.errors('t','var:rw_ba_'+field+' = scope:rw_ba_'+field,'always = yes'))
    def test_no_retargeting_charter_or_successor(self):
        for g in ('var:rw_ch_revision = scope:rw_ba_parent_revision','var:rw_lr_serial = scope:rw_ba_source_serial','holder = scope:rw_ba_payer','house_head = scope:rw_ba_payee'):
            self.assertIn('different charter revision or successor can release',self.errors('t',g,'always = yes'))
    def test_other_party_must_accept_exact_latest_packet(self):
        for g in ('has_variable = rw_ba_window','var:rw_ba_offered_by = scope:rw_ba_payer','var:rw_ba_agreement = flag:negotiating'):
            self.assertIn('self acceptance stale or inherited consent',self.errors('t',g,'always = yes'))
    def test_proposal_cannot_repeat_same_context_or_ignore_issuer_cooldown(self):
        self.assertIn('replayed same-context bundle or no issuer authority',self.errors('t','NOT = { has_character_flag = rw_ba_recent }','always = yes'))
        self.assertIn('uninitialized story consumes source context or leaks into index',self.errors('e','limit = { scope:rw_ba_record = { rw_ba_record_trigger = yes } }','limit = { always = yes }'))
    def test_acceptance_is_one_signature_with_no_early_payment_or_release(self):
        self.assertIn('acceptance not one immutable three-clause signature',self.errors('e','name = rw_ba_support value = flag:pending','name = rw_ba_support value = flag:done'))
        self.assertIn('native performance before signature or by acceptance',self.errors('e','rw_ba_accept_effect = {','rw_ba_accept_effect = {\n add_gold = 25'))
    def test_counter_invalidates_prior_version_and_owner(self):
        self.assertIn('counter reuses previous consent',self.errors('e','change_variable = { name = rw_ba_revision add = 1 }',''))
    def test_native_actions_require_correct_original_actor_pending_leg_and_due(self):
        for g in ('this = scope:rw_ba_payee','var:rw_ba_support = flag:pending','has_variable = rw_ba_due'):
            found=self.errors('t',g,'always = yes')
            self.assertTrue('wrong actor or repeated individual action' in found or 'execution outside signed lifetime' in found)
    def test_payment_uses_original_payer_funds_and_consumes_before_transfer(self):
        self.assertIn('unfunded actual payer spends',self.errors('t','gold >= scope:rw_ba_price','always = yes'))
        self.assertIn('duplicate wrong-direction or unconsumed payment',self.errors('e','name = rw_ba_gold value = flag:attempted','name = rw_ba_gold value = flag:pending'))
    def test_support_is_performance_only_with_exact_memory_parties(self):
        self.assertIn('support replay wrong recipient or memory before performance',self.errors('e','PROVIDER = scope:rw_ba_payer CLIENT = scope:rw_ba_payee','PROVIDER = scope:rw_ba_payee CLIENT = scope:rw_ba_payer'))
    def test_release_checks_original_context_and_observed_own_result(self):
        self.assertIn('unrelated release falsely credited',self.errors('e','var:rw_ch_finished_by = scope:rw_ba_payee','always = yes'))
        self.assertIn('unrelated release falsely credited',self.errors('e','var:rw_ch_revision = scope:rw_ba_record.var:rw_ba_release_revision','always = yes'))
    def test_release_first_does_not_cancel_independent_gold_and_support(self):
        for name in ('rw_ba_can_pay_trigger','rw_ba_can_support_trigger'):
            changed=self.t.replace(name+' = {',name+' = {\n rw_ba_source_context_trigger = yes')
            self.assertIn('earlier release blocks independent later promises',agreement_errors(changed,self.e,self.v))
    def test_refusal_is_free_only_for_own_unperformed_leg(self):
        self.assertIn('wrong obligation owner in refusal UI',self.errors('v','LEG = release PAYER = no PAYEE = yes','LEG = release PAYER = yes PAYEE = no'))
        self.assertIn('refusal alters completed or another persons action',self.errors('t','var:rw_ba_$LEG$ = flag:pending','always = yes'))
    def test_refusal_requires_actual_actor_and_date_receipt(self):
        self.assertIn('unsupported explicit-refusal receipt',self.errors('t','has_variable = rw_ba_gold_refused_on','always = yes'))
    def test_partial_completion_cannot_pay_again_rollback_or_claim_all_done(self):
        self.assertIn('partial performance disguised as full settlement',self.errors('e','var:rw_ba_gold = flag:done var:rw_ba_support = flag:done var:rw_ba_release = flag:done','always = yes'))
        self.assertIn('expiry rollback reward or automatic performance',self.errors('e','rw_ba_resolve_effect = {','rw_ba_resolve_effect = {\n add_gold = 25'))
    def test_one_execution_window_and_fixed_total_retention(self):
        self.assertEqual(1,self.e.count('name = rw_ba_due value = flag:yes days = 30'))
        self.assertEqual(1,self.e.count('name = rw_ba_retained value = flag:yes days = 1863'))
        self.assertEqual(1,self.e.count('name = rw_ba_window value = flag:yes days = 7'))
    def test_dead_owner_excluded_and_no_heir_inherits_actions(self):
        self.assertIn('dead custodian or heir inherits personal consent',self.errors('e','NOT = { this = scope:rw_ba_departed }','always = yes'))
    def test_ending_story_removes_index_before_end(self):
        self.assertIn('retired agreement remains globally indexed',self.errors('e','remove_list_global_variable = { name = rw_multi_action_agreements target = scope:rw_ba_record }',''))
    def test_reading_snapshot_never_executes_or_refreshes_saved_reply(self):
        read=block(self.e,'rw_ba_read_effect')
        self.assertIn('rw_ba_reader_trigger = { READER = scope:rw_ba_reader }',read)
        self.assertNotRegex(read,r'rw_ba_(?:accept|pay|release|support|counter)_effect')
        self.assertNotIn('rw_ba_snapshot_effect',self.v)
    def test_actual_player_ai_entry_and_per_action_status_board(self):
        charter=(MOD/'events/rw_restitution_charter_events.txt').read_text()
        self.assertIn('rw_ba_propose_effect = yes',option(charter,'rw_multi_actions.propose'))
        for leg in ('gold','support','release'):
            self.assertIn('rw_multi_actions.'+leg+'_label',self.v)
            self.assertIn('var:rw_ba_'+leg+' = flag:done',self.v)
        self.assertIn('name = rw_multi_actions.leave ai_chance = { base = 30 }',self.v)
    def test_no_native_legal_override_or_player_ai_privilege(self):
        for bad in ('add_secret = murder','run_interaction = {}','is_ai = yes','every_living_character = {}'):
            self.assertIn('native override legal proof or AI privilege',self.errors('e','rw_ba_accept_effect = {','rw_ba_accept_effect = {\n'+bad))
    def test_all_six_native_model_bindings_target_only_this_bundle(self):
        raw=(MOD/'common/scripted_triggers/rw_multi_action_triggers.txt').read_text()+(MOD/'common/scripted_effects/rw_multi_action_effects.txt').read_text()
        calls=CALL.findall(raw)
        self.assertEqual({'rw_contract_'+n+'_effect' for n in ('offer','snapshot','counter','consume','close')}|{'rw_contract_quote_trigger'},{n for n,_ in calls})
        for name,args in calls:
            values=dict(ARG.findall(args))
            self.assertEqual('ba',values['PREFIX'])
            if name in ('rw_contract_quote_trigger','rw_contract_counter_effect'):
                self.assertEqual(('ruler','head'),(values['TURN_A'],values['TURN_B']))
            if name=='rw_contract_offer_effect':self.assertEqual('25',values['PRICE'])

    def test_individual_done_receipts_bind_the_actual_signed_version_and_actor(self):
        record=block(self.t,'rw_ba_record_trigger')
        for guard in ('var:rw_ba_paid_revision = var:rw_ba_accepted_revision',
                      'var:rw_ba_paid_amount = var:rw_ba_accepted_price',
                      'var:rw_ba_support_actor = var:rw_ba_payer',
                      'var:rw_ba_support_revision = var:rw_ba_accepted_revision',
                      'var:rw_ba_release_quote_revision = var:rw_ba_accepted_revision',
                      'var:rw_ba_release_result_revision = var:rw_ba_release_revision',
                      'var:rw_ba_release_result_by = var:rw_ba_payee'):
            self.assertIn(guard,record)
        death=block(self.e,'rw_ba_owner_died_effect')
        self.assertIn('OR = { var:rw_ba_payer = scope:rw_ba_departed var:rw_ba_payee = scope:rw_ba_departed }',death)

    def test_french_english_cover_all_bundle_ui_and_history(self):
        charter=(MOD/'events/rw_restitution_charter_events.txt').read_text()
        keys=set(re.findall(r'\b(?:name|title|desc)\s*=\s*(rw_multi_actions\.[\w.]+)',self.v+charter))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_multi_actions_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            found=set(re.findall(r'^\s+(rw_multi_actions\.[\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertEqual(keys,found)
