"""Adversarial deferred consideration contracts; no CK3 scheduler/favor simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def deferred_errors(t,e,fv,vt):
    out=[]
    mode=block(t,'rw_fv_mode_matches_trigger')
    for g in ('exists = scope:rw_fv_mode','scope:rw_fv_mode = flag:immediate','scope:rw_fv_mode = flag:deferred',
              'has_variable = rw_fv_mode','var:rw_fv_mode = scope:rw_fv_mode','var:rw_fv_provider = scope:rw_fv_provider',
              'trigger_else = { scope:rw_fv_mode = flag:immediate }'):
        if g not in mode:out.append('legacy or wrong-mode ticket converted')
    if 'rw_fv_mode_matches_trigger = yes' not in block(vt,'rw_fv_view_trigger'):out.append('mode absent from full ticket identity')
    accept_gate=block(t,'rw_fd_can_accept_trigger')
    if 'rw_fd_deferred_trigger = yes' not in accept_gate or 'OR = { rw_fv_can_accept_favor_trigger = yes rw_fv_can_accept_gold_trigger = yes }' not in accept_gate:
        out.append('wrong mode or responder accepts promise')
    accept=block(e,'rw_fd_accept_effect')
    for g in ('limit = { rw_fd_can_accept_trigger = yes }','remove_character_flag = rw_fv_pending','remove_variable = rw_fv_turn',
              'change_variable = { name = rw_fv_revision add = 1 }','name = rw_fd_accepted_on value = current_date',
              'name = rw_fv_state value = flag:promised','flag = rw_fv_obligation days = 32',
              'flag = rw_fd_not_due days = 7','flag = rw_fd_due days = 30'):
        if g not in accept:out.append('consent identity or immutable clocks missing')
    if re.search(r'\b(add_hook|add_gold|add_prestige)\s*=',accept):out.append('consent executes native consideration')
    points=[accept.find(g) for g in ('change_variable = { name = rw_fv_revision','rw_fv_snapshot_effect = yes',
                                   'id = rw_deferred_favor.0002 days = 8','id = rw_deferred_favor.0003 days = 31','rw_fv_notify_effect = yes')]
    if min(points)<0 or points!=sorted(points):out.append('old identity or premature notice scheduled')
    if accept.count('id = rw_deferred_favor.0002')!=2 or 'id = rw_deferred_favor.0002 days = 22' not in accept:
        out.append('reactive opportunities missing or unbounded')
    owner=block(t,'rw_fd_owner_matches_trigger')
    for g in ('exists = scope:rw_fv_provider','exists = scope:rw_fv_serial','exists = scope:rw_fv_revision',
              'exists = scope:rw_fv_term','exists = scope:rw_fv_mode','scope:rw_fv_mode = flag:deferred',
              'var:rw_fv_schema = 1','var:rw_fv_provider = scope:rw_fv_provider','var:rw_fv_serial = scope:rw_fv_serial','var:rw_fv_revision = scope:rw_fv_revision',
              'var:rw_fv_term = scope:rw_fv_term','var:rw_fv_mode = flag:deferred','var:rw_fv_state = flag:promised',
              'has_variable = rw_fd_accepted_on','has_character_flag = rw_fv_obligation'):
        if g not in owner:out.append('foreign stale or incomplete owner cleanup')
    due=block(t,'rw_fd_due_trigger')
    for g in ('rw_fd_pending_trigger = yes','has_character_flag = rw_fd_due','NOT = { has_character_flag = rw_fd_not_due }'):
        if g not in due:out.append('early expired or wrong promise performed')
    perform=block(t,'rw_fd_can_perform_trigger')
    for g in ('rw_fd_due_trigger = yes','this = scope:rw_fv_provider',
              'rw_fv_favor_available_trigger = { PROVIDER = scope:rw_fv_provider CLIENT = scope:rw_fv_client }',
              'scope:rw_fv_term = flag:favor','scope:rw_fv_term = flag:gold25','scope:rw_fv_client = { gold >= 25 }'):
        if g not in perform:out.append('performance bypasses current native eligibility or funds')
    if perform.count('rw_service_party_eligible_trigger = yes')!=2 or perform.count('is_imprisoned = no')!=2:
        out.append('performance bypasses current native eligibility or funds')
    body=block(e,'rw_fd_perform_effect')
    if 'limit = { rw_fd_can_perform_trigger = yes }' not in body:out.append('unguarded deferred performance')
    points=[body.find(g) for g in ('rw_fd_finish_effect = { RESULT = fulfilled }','add_hook','add_prestige = 50','rw_fv_notify_effect = yes')]
    if min(points)<0 or points!=sorted(points):out.append('native consideration before terminal consumption')
    for g in ('scope:rw_fv_provider = { add_hook = { type = favor_hook target = scope:rw_fv_client } }',
              'scope:rw_fv_client = { add_gold = -25 }','scope:rw_fv_provider = { add_gold = 25 }',
              'scope:rw_fv_client = { add_prestige = 50 }'):
        if g not in body:out.append('wrong native consideration or beneficiary')
    finish=block(e,'rw_fd_finish_effect')
    for g in ('limit = { rw_fd_owner_matches_trigger = yes }','remove_character_flag = rw_fv_obligation',
              'remove_character_flag = rw_fd_due','remove_character_flag = rw_fd_not_due','name = rw_fv_finished_on value = current_date'):
        if g not in finish:out.append('terminal path strands original service slot')
    timeout=block(e,'rw_fd_timeout_effect')
    for g in ('rw_fd_owner_matches_trigger = yes','this = scope:rw_fv_provider','NOT = { has_character_flag = rw_fd_due }',
              'rw_fd_finish_effect = { RESULT = unresolved }'):
        if g not in timeout:out.append('early stale or blaming timeout')
    if 'NOT = { rw_fd_deferred_trigger = yes }' not in block(fv,'rw_fv_settle_effect'):
        out.append('immediate path spends deferred consent')
    code=clean_script(e)[0]
    if re.search(r'\b(add_opinion|add_secret|add_claim|imprison|remove_hook|use_hook|run_interaction|change_title_holder|make_story_owner|every_living_character|every_in_global_list)\s*=',code):
        out.append('promise adds punishment hook use or global policy')
    if re.search(r'\b(?:name|flag|add_character_flag|remove_character_flag|remove_variable)\s*=\s*rw_service_\w+',code):out.append('original financial ticket overwritten')
    if len(re.findall(r'\bflag\s*=\s*rw_fd_due\b',e))!=1:out.append('accepted deadline renewed')
    return out


class DeferredFavorTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_deferred_favor_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_deferred_favor_effects.txt').read_text()
        self.fv=(MOD/'common/scripted_effects/rw_favor_service_effects.txt').read_text()
        self.vt=(MOD/'common/scripted_triggers/rw_favor_service_triggers.txt').read_text()
        self.ev=(MOD/'events/rw_deferred_favor_events.txt').read_text()
        self.v=(MOD/'events/rw_favor_service_events.txt').read_text()

    def errors(self,t=None,e=None,fv=None,vt=None):
        return deferred_errors(self.t if t is None else t,self.e if e is None else e,self.fv if fv is None else fv,self.vt if vt is None else vt)

    def test_contract(self):self.assertEqual([],self.errors())

    def test_mode_is_explicit_and_legacy_missing_mode_is_immediate_only(self):
        for g in ('exists = scope:rw_fv_mode','var:rw_fv_mode = scope:rw_fv_mode','var:rw_fv_provider = scope:rw_fv_provider','trigger_else = { scope:rw_fv_mode = flag:immediate }'):
            self.assertIn('legacy or wrong-mode ticket converted',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('mode absent from full ticket identity',self.errors(vt=self.vt.replace('rw_fv_mode_matches_trigger = yes','always = yes')))
        snapshot=block(self.fv,'rw_fv_snapshot_effect')
        self.assertIn('name = rw_fv_mode value = flag:immediate',snapshot)
        self.assertIn('name = rw_fv_mode value = var:rw_fv_mode',snapshot)
        self.assertIn('name = rw_fv_mode value = flag:$MODE$',block(self.fv,'rw_fv_begin_effect'))
        self.assertIn('name = rw_fv_provider value = scope:rw_fv_provider',block(self.fv,'rw_fv_begin_effect'))
        self.assertIn('var:rw_fv_provider = scope:recipient',block(self.vt,'rw_fv_review_allowed_trigger'))

    def test_explicit_interactions_and_counteroffers_preserve_captured_mode(self):
        i=(MOD/'common/character_interactions/rw_favor_service_interactions.txt').read_text()
        for mode in ('immediate','deferred'):self.assertIn('rw_fv_begin_effect = { MODE = '+mode+' }',i)
        for effect in ('rw_fv_counter_gold_effect','rw_fv_restate_effect'):
            self.assertNotIn('name = rw_fv_mode',block(self.fv,effect))
        self.assertNotIn('immediate =',self.v)
        self.assertIn('NOT = { rw_fd_deferred_trigger = yes }',self.v)

    def test_only_current_mode_and_exact_responder_can_consent(self):
        for g in ('rw_fd_deferred_trigger = yes','OR = { rw_fv_can_accept_favor_trigger = yes rw_fv_can_accept_gold_trigger = yes }'):
            self.assertIn('wrong mode or responder accepts promise',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('consent identity or immutable clocks missing',self.errors(e=self.e.replace('limit = { rw_fd_can_accept_trigger = yes }','limit = { always = yes }')))

    def test_acceptance_transfers_nothing_and_invalidates_older_offer_panels(self):
        self.assertIn('consent executes native consideration',self.errors(e=self.e.replace('rw_fd_accept_effect = {','rw_fd_accept_effect = { add_hook = {}')))
        for g in ('remove_character_flag = rw_fv_pending','change_variable = { name = rw_fv_revision add = 1 }',
                  'name = rw_fd_accepted_on value = current_date','flag = rw_fv_obligation days = 32'):
            self.assertIn('consent identity or immutable clocks missing',self.errors(e=self.e.replace(g,'removed_part')))
        self.assertIn('old identity or premature notice scheduled',self.errors(e=self.e.replace('rw_fv_snapshot_effect = yes','')))

    def test_original_seven_thirty_day_clocks_never_renew_on_review_or_wait(self):
        for g in ('flag = rw_fd_not_due days = 7','flag = rw_fd_due days = 30'):
            self.assertIn('consent identity or immutable clocks missing',self.errors(e=self.e.replace(g,'removed_part')))
        # A lost timeout cannot strand this provider slot forever; it grants no extra delivery time.
        self.assertIn('flag = rw_fv_obligation days = 32',block(self.e,'rw_fd_accept_effect'))
        self.assertIn('accepted deadline renewed',self.errors(e=self.e+'\nadd_character_flag = { flag = rw_fd_due days = 30 }'))
        self.assertNotIn('rw_fd_accept_effect',block(self.fv,'rw_fv_review_effect'))
        self.assertNotIn('rw_deferred_favor.0002',block(self.fv,'rw_fv_review_effect'))

    def test_two_fixed_ai_opportunities_and_one_independent_timeout(self):
        accept=block(self.e,'rw_fd_accept_effect')
        self.assertEqual(2,accept.count('id = rw_deferred_favor.0002'))
        self.assertEqual(1,accept.count('id = rw_deferred_favor.0003 days = 31'))
        self.assertIn('reactive opportunities missing or unbounded',self.errors(e=self.e.replace('.0002 days = 22','.0002 days = 8')))
        dispatcher=block(self.ev,'rw_deferred_favor.0002')
        self.assertIn('rw_fd_due_trigger = yes this = scope:rw_fv_provider',dispatcher)
        self.assertIn('id = rw_favor_service.0001',dispatcher)
        self.assertNotIn('rw_fd_perform_effect',dispatcher)

    def test_immutable_owner_cleanup_identity_never_guesses_an_orphan_client(self):
        for g in ('exists = scope:rw_fv_serial','exists = scope:rw_fv_revision','scope:rw_fv_mode = flag:deferred',
                  'var:rw_fv_provider = scope:rw_fv_provider','var:rw_fv_serial = scope:rw_fv_serial','var:rw_fv_revision = scope:rw_fv_revision',
                  'var:rw_fv_term = scope:rw_fv_term','var:rw_fv_mode = flag:deferred','has_character_flag = rw_fv_obligation'):
            self.assertIn('foreign stale or incomplete owner cleanup',self.errors(t=self.t.replace(g,'always = yes')))
        owner=block(self.t,'rw_fd_owner_matches_trigger')
        self.assertNotIn('scope:rw_fv_client',owner)
        self.assertNotIn('rw_fv_view_trigger',owner)
        self.assertNotRegex(block(self.e,'rw_fd_finish_effect'),r'\b(add_hook|add_gold|add_prestige)\s*=')

    def test_performance_requires_full_private_ticket_and_original_provider(self):
        self.assertIn('rw_fv_view_trigger = yes',block(self.t,'rw_fd_pending_trigger'))
        for g in ('rw_fd_due_trigger = yes','this = scope:rw_fv_provider','rw_service_party_eligible_trigger = yes','is_imprisoned = no'):
            self.assertIn('performance bypasses current native eligibility or funds',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('unguarded deferred performance',self.errors(e=self.e.replace('limit = { rw_fd_can_perform_trigger = yes }','limit = { always = yes }')))

    def test_native_favor_and_gold_eligibility_rechecked_only_for_agreed_consideration(self):
        for g in ('rw_fv_favor_available_trigger = { PROVIDER = scope:rw_fv_provider CLIENT = scope:rw_fv_client }',
                  'scope:rw_fv_client = { gold >= 25 }','scope:rw_fv_term = flag:favor','scope:rw_fv_term = flag:gold25'):
            self.assertIn('performance bypasses current native eligibility or funds',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('desc = rw_deferred_favor.consideration_unavailable',self.v)

    def test_early_and_expired_performance_is_blocked(self):
        for g in ('rw_fd_pending_trigger = yes','has_character_flag = rw_fd_due','NOT = { has_character_flag = rw_fd_not_due }'):
            self.assertIn('early expired or wrong promise performed',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('immediate path spends deferred consent',self.errors(fv=self.fv.replace('NOT = { rw_fd_deferred_trigger = yes }','always = yes')))

    def test_consumption_before_one_selected_native_branch_then_service_reward(self):
        self.assertIn('native consideration before terminal consumption',self.errors(e=self.e.replace('rw_fd_finish_effect = { RESULT = fulfilled }','')))
        for g in ('scope:rw_fv_provider = { add_hook = { type = favor_hook target = scope:rw_fv_client } }',
                  'scope:rw_fv_client = { add_gold = -25 }','scope:rw_fv_provider = { add_gold = 25 }',
                  'scope:rw_fv_client = { add_prestige = 50 }'):
            self.assertIn('wrong native consideration or beneficiary',self.errors(e=self.e.replace(g,'removed_part')))
        perform=block(self.e,'rw_fd_perform_effect')
        self.assertIn('limit = { scope:rw_fv_term = flag:favor }',perform)
        self.assertEqual(1,len(re.findall(r'\badd_hook\s*=',perform)))
        self.assertEqual(2,len(re.findall(r'\badd_gold\s*=',perform)))

    def test_original_provider_renunciation_and_client_withdrawal_are_identity_only(self):
        for gate,actor in (('rw_fd_can_renounce_trigger','provider'),('rw_fd_can_withdraw_trigger','client')):
            b=block(self.t,gate)
            self.assertIn('rw_fd_pending_trigger = yes',b)
            self.assertIn('this = scope:rw_fv_'+actor,b)
            self.assertNotRegex(b,r'\b(rw_fd_due|gold|can_add_hook|rw_service_party_eligible_trigger)\b')
        for name,gate,result in (('renounce','renounce','provider_renounced'),('withdraw','withdraw','client_withdrew')):
            b=block(self.e,'rw_fd_'+name+'_effect')
            self.assertIn('limit = { rw_fd_can_'+gate+'_trigger = yes }',b)
            self.assertIn('RESULT = '+result,b)
            self.assertNotRegex(b,r'\b(add_hook|add_gold|add_prestige|add_opinion|remove_hook)\s*=')

    def test_terminal_cleanup_releases_slot_and_never_touches_old_financial_flags(self):
        for g in ('limit = { rw_fd_owner_matches_trigger = yes }','remove_character_flag = rw_fv_obligation',
                  'remove_character_flag = rw_fd_due','remove_character_flag = rw_fd_not_due'):
            self.assertIn('terminal path strands original service slot',self.errors(e=self.e.replace(g,'removed_part')))
        self.assertIn('original financial ticket overwritten',self.errors(e=self.e+'\nadd_character_flag = rw_service_obligation'))
        old=(MOD/'common/scripted_triggers/rw_service_triggers.txt').read_text()
        self.assertIn('NOT = { has_character_flag = rw_fv_obligation }',block(old,'rw_service_provider_available_trigger'))

    def test_only_original_provider_and_real_expiry_allow_neutral_orphan_timeout(self):
        for g in ('rw_fd_owner_matches_trigger = yes','this = scope:rw_fv_provider','NOT = { has_character_flag = rw_fd_due }'):
            self.assertIn('early stale or blaming timeout',self.errors(e=self.e.replace(g,'always = yes')))
        timeout=block(self.e,'rw_fd_timeout_effect')
        self.assertIn('RESULT = unresolved',timeout)
        self.assertIn('limit = { rw_fv_view_trigger = yes }',timeout)
        self.assertNotRegex(timeout,r'\b(add_hook|add_gold|add_prestige|add_opinion)\s*=')
        self.assertIn('immediate = { rw_fd_timeout_effect = yes }',self.ev)

    def test_no_new_legal_hook_spending_war_inheritance_or_global_scans(self):
        for command in ('add_opinion = {}','remove_hook = {}','use_hook = {}','run_interaction = {}','every_living_character = {}'):
            self.assertIn('promise adds punishment hook use or global policy',self.errors(e=self.e+'\n'+command))
        self.assertNotRegex(clean_script(self.e)[0],r'\b(create_story|add_to_global_variable_list|on_action)\s*=')

    def test_ai_and_player_share_all_mode_cost_and_actor_guards(self):
        self.assertNotRegex(clean_script(self.t+self.e)[0],r'\bis_ai\s*=')
        for name in ('accept','perform','renounce','withdraw'):
            self.assertIn('rw_fd_'+name+'_effect = yes',self.v)
            self.assertIn('name = rw_deferred_favor.'+name,self.v)
        i=(MOD/'common/character_interactions/rw_favor_service_interactions.txt').read_text()
        self.assertIn('rw_offer_deferred_favor_endorsement_interaction = {',i)
        self.assertEqual(2,i.count('ai_targets = { ai_recipients = liege }'))
        self.assertIn('has_trait = honest',self.v)

    def test_bom_localizations_cover_new_consent_status_and_timing(self):
        keys=set(re.findall(r'(?:name|desc)\s*=\s*(rw_deferred_favor\.[\w.]+)',self.v))
        keys.update(('rw_offer_deferred_favor_endorsement_interaction','rw_offer_deferred_favor_endorsement_interaction_desc'))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_deferred_favor_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual=set(re.findall(r'^\s+([\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertTrue(keys<=actual,keys-actual)
