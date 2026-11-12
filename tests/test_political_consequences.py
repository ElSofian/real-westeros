"""Native legitimacy/stress source wiring and negative mutation checks."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'
FILES=['rw_house_affair_effects.txt','rw_restitution_charter_effects.txt','rw_obligation_effects.txt','rw_deferred_favor_effects.txt','rw_restitution_pledge_effects.txt','rw_dynastic_pledge_effects.txt','rw_military_restraint_effects.txt','rw_multi_action_effects.txt']

def consequence_errors(helper,sources):
    errors=[]
    breach=block(helper,'rw_promise_breach_stress_effect')
    traits=block(breach,'stress_impact')
    if set(re.findall(r'(\w+)\s*=\s*(\d+)',traits))!={('honest','15'),('just','10'),('compassionate','5')}:
        errors.append('wrong personal breach stress policy')
    censure=block(helper,'rw_house_censure_consequence_effect')
    for token in ('rw_house_record_active_trigger = yes','var:rw_house_issuer = root','var:rw_house_issued_on = current_date',
                  'NOT = { has_variable = rw_house_censure_consequences_done }','name = rw_house_censure_consequences_done value = flag:yes',
                  'if = { limit = { has_legitimacy = yes } add_legitimacy = -10 }','stress_impact = { just = 10 compassionate = 10 }'):
        if not re.search(re.escape(token)+r'(?![\w.])',censure):errors.append('unbound or repeated decree consequence')
    clemency=block(helper,'rw_house_clemency_consequence_effect')
    for token in ('rw_house_record_valid_trigger = yes','var:rw_house_state = flag:restored','var:rw_house_state = flag:withdrawn',
                  'var:rw_house_closed_by = root','var:rw_house_closed_on = current_date',
                  'NOT = { var:rw_house_last_response = flag:terms_settled }',
                  'NOT = { has_variable = rw_house_clemency_consequences_done }',
                  'name = rw_house_clemency_consequences_done value = flag:yes',
                  'has_legitimacy = yes','NOT = { this = scope:rw_house_record.var:rw_house_issuer }','add_legitimacy = 10','stress_impact = { vengeful = 10 }'):
        if not re.search(re.escape(token)+r'(?![\w.])',clemency):errors.append('unbound paid or repeated clemency consequence')
    for body,marker in [(censure,'rw_house_censure_consequences_done'),(clemency,'rw_house_clemency_consequences_done')]:
        if body.find('name = '+marker)>body.find('add_legitimacy ='):errors.append('consequence before consumed marker')
    recognition=block(helper,'rw_crown_recognition_consequence_effect')
    for token in ('rw_ch_active_trigger = yes','this = scope:rw_ch_ruler','var:rw_ch_recognized_on = current_date',
                  'var:rw_ch_recognized_by = scope:rw_ch_ruler','has_legitimacy = yes',
                  'NOT = { has_character_flag = rw_public_recognition_bonus_recent }',
                  'flag = rw_public_recognition_bonus_recent days = 365','add_legitimacy = 10'):
        if not re.search(re.escape(token)+r'(?![\w.])',recognition):errors.append('unbound or repeated public recognition')
    # The awarding block has exactly the head's flag followed by its legitimacy effect.
    if not re.search(r'scope:rw_ch_head\s*=\s*\{\s*add_character_flag\s*=\s*\{[^{}]*\}\s*add_legitimacy\s*=\s*10(?![\w.])',recognition):
        errors.append('recognition rewards the wrong actor')
    if recognition.find('add_character_flag =')>recognition.find('add_legitimacy ='):errors.append('recognition reward before consumption')
    financial=block(sources['rw_obligation_effects.txt'],'rw_service_record_breach_effect')
    for token in ('scope:rw_service_breach_reason = flag:refusal','scope:rw_service_breach_reason = flag:deadline',
                  'var:rw_service_last_performance_capacity = flag:available','scope:rw_service_provider = { rw_promise_breach_stress_effect = yes }'):
        if token not in financial:errors.append('unproven financial breach stress')
    if financial.find('rw_service_clear_effect = yes')>financial.find('rw_promise_breach_stress_effect ='):errors.append('stress before consumed promise')
    favor=block(sources['rw_deferred_favor_effects.txt'],'rw_fd_renounce_effect')
    if 'NOT = { var:rw_fr_capacity = flag:unavailable }' not in favor:errors.append('known inability incurs renunciation stress')
    if favor.find('rw_fd_finish_effect = { RESULT = provider_renounced }')>favor.find('rw_promise_breach_stress_effect ='):errors.append('stress before consumed promise')
    restitution=block(sources['rw_restitution_pledge_effects.txt'],'rw_rp_renounce_effect')
    for token in ('rw_rp_parties_trigger = yes','name = rw_rp_renunciation_stress_due value = flag:no',
                  'scope:rw_rp_renunciation_stress_due = flag:yes','rw_promise_breach_stress_effect = yes'):
        if token not in restitution:errors.append('invalid restitution party stress')
    legacy=block(sources['rw_dynastic_pledge_effects.txt'],'rw_dp_renounce_effect')
    if 'scope:rw_dp_record = { var:rw_dp_payer_recognized = root }' not in legacy:errors.append('successor inherits personal breach stress')
    if legacy.find('rw_dp_close_story_effect = { RESULT = renounced }')>legacy.find('rw_promise_breach_stress_effect ='):errors.append('stress before consumed promise')
    for name in ['rw_ch_accept_effect','rw_ch_assume_effect']:
        body=block(sources['rw_restitution_charter_effects.txt'],name)
        if 'name = rw_ch_recognized_on value = current_date' not in body or 'rw_crown_recognition_consequence_effect = yes' not in body:
            errors.append('explicit recognition bypasses its consequence')
    charter=block(helper,'rw_crown_renunciation_consequence_effect')
    for token in ('rw_ch_view_trigger = yes','this = scope:rw_ch_ruler','var:rw_ch_state = flag:renounced',
                  'var:rw_ch_recognized_by = root','var:rw_ch_finished_by = root','var:rw_ch_finished_on = current_date',
                  'NOT = { has_variable = rw_ch_renunciation_consequences_done }',
                  'name = rw_ch_renunciation_consequences_done value = flag:yes','rw_promise_breach_stress_effect = yes'):
        if not re.search(re.escape(token)+r'(?![\w.])',charter):errors.append('inherited or repeated charter renunciation cost')
    if charter.find('name = rw_ch_renunciation_consequences_done')>charter.find('add_legitimacy ='):
        errors.append('charter cost before consumption')
    military=block(sources['rw_military_restraint_effects.txt'],'rw_mr_renounce_effect')
    if 'rw_promise_breach_stress_effect = yes' not in military or military.find('flag:renounced')>military.find('rw_promise_breach_stress_effect ='):
        errors.append('military renunciation cost before consumed promise')
    bundle=block(sources['rw_multi_action_effects.txt'],'rw_ba_refuse_effect')
    for leg,gate in [('gold','pay'),('support','support'),('release','release')]:
        if 'scope:rw_ba_refused_leg = flag:'+leg+' rw_ba_can_'+gate+'_trigger = yes' not in bundle:
            errors.append('bundle refusal lacks actual leg capacity')
    if 'scope:rw_ba_refusal_stress_due = flag:yes' not in bundle:errors.append('bundle cost ignores capacity snapshot')
    for role in ['payer','payee']:
        for token in ('this = scope:rw_ba_'+role,'NOT = { has_variable = rw_ba_'+role+'_stress_done }','name = rw_ba_'+role+'_stress_done value = flag:yes'):
            if token not in bundle:errors.append('bundle costs repeat or inherit a personal party')
    if bundle.find('flag:refused')>bundle.find('rw_promise_breach_stress_effect ='):errors.append('bundle cost precedes consumed clause')
    if re.search(r'\b(run_interaction|start_war|end_war|change_title_holder|add_gold|add_prestige|add_trait|add_imprisonment_reason)\s*=',helper):
        errors.append('consequence helper owns an unrelated native action')
    if 'is_ai' in helper:errors.append('actor-specific consequence rules')
    return errors

class PoliticalConsequenceTests(unittest.TestCase):
    def setUp(self):
        self.helper=(MOD/'common/scripted_effects/rw_political_consequence_effects.txt').read_text()
        self.sources={name:(MOD/'common/scripted_effects'/name).read_text() for name in FILES}
    def errors(self,helper=None,sources=None):return consequence_errors(self.helper if helper is None else helper,self.sources if sources is None else sources)
    def test_real_native_counter_stress_and_owned_callers(self):self.assertEqual([],self.errors())
    def test_censure_requires_fresh_original_issuer_and_one_marker(self):
        for token in ['var:rw_house_issuer = root','var:rw_house_issued_on = current_date','NOT = { has_variable = rw_house_censure_consequences_done }']:
            self.assertIn('unbound or repeated decree consequence',self.errors(helper=self.helper.replace(token,'always = yes')))
    def test_clemency_requires_actual_free_closure_and_personal_actor(self):
        for token in ['var:rw_house_closed_by = root','var:rw_house_closed_on = current_date','NOT = { var:rw_house_last_response = flag:terms_settled }','NOT = { has_variable = rw_house_clemency_consequences_done }','NOT = { this = scope:rw_house_record.var:rw_house_issuer }']:
            self.assertIn('unbound paid or repeated clemency consequence',self.errors(helper=self.helper.replace(token,'always = yes')))
    def test_native_counter_availability_is_required_for_both_signed_amounts(self):
        self.assertIn('unbound or repeated decree consequence',self.errors(helper=self.helper.replace('has_legitimacy = yes','always = yes')))
        self.assertIn('unbound paid or repeated clemency consequence',self.errors(helper=self.helper.replace('add_legitimacy = 10','add_legitimacy = 1000')))
    def test_recognition_is_fresh_personal_current_head_and_consumed_before_reward(self):
        for token in ['var:rw_ch_recognized_on = current_date','var:rw_ch_recognized_by = scope:rw_ch_ruler','NOT = { has_character_flag = rw_public_recognition_bonus_recent }']:
            self.assertIn('unbound or repeated public recognition',self.errors(helper=self.helper.replace(token,'always = yes')))
        self.assertIn('recognition rewards the wrong actor',self.errors(helper=self.helper.replace('scope:rw_ch_head = {','scope:rw_ch_ruler = {')))
    def test_financial_breach_requires_known_capacity_including_accountable_timeout(self):
        changed=dict(self.sources);key='rw_obligation_effects.txt';changed[key]=changed[key].replace('var:rw_service_last_performance_capacity = flag:available','always = yes')
        self.assertIn('unproven financial breach stress',self.errors(sources=changed))
    def test_favor_due_inability_is_exempt_but_voluntary_early_renunciation_is_distinct(self):
        changed=dict(self.sources);key='rw_deferred_favor_effects.txt';changed[key]=changed[key].replace('NOT = { var:rw_fr_capacity = flag:unavailable }','always = yes')
        self.assertIn('known inability incurs renunciation stress',self.errors(sources=changed))
    def test_successor_must_have_personally_recognized_the_legacy_promise(self):
        changed=dict(self.sources);key='rw_dynastic_pledge_effects.txt';changed[key]=changed[key].replace('scope:rw_dp_record = { var:rw_dp_payer_recognized = root }','always = yes')
        self.assertIn('successor inherits personal breach stress',self.errors(sources=changed))
    def test_restitution_checks_current_personal_participation_before_consumption(self):
        changed=dict(self.sources);key='rw_restitution_pledge_effects.txt';changed[key]=changed[key].replace('limit = { rw_rp_parties_trigger = yes }','limit = { always = yes }')
        self.assertIn('invalid restitution party stress',self.errors(sources=changed))
    def test_stress_policy_is_trait_based_and_other_native_actions_are_excluded(self):
        self.assertIn('wrong personal breach stress policy',self.errors(helper=self.helper.replace('honest = 15','honest = 150')))
        self.assertIn('consequence helper owns an unrelated native action',self.errors(helper=self.helper+'\nrun_interaction = {}'))
        for body in ['rw_service_cancel_promise_effect','rw_service_forgive_breach_effect']:
            self.assertNotIn('rw_promise_breach_stress_effect',block(self.sources['rw_obligation_effects.txt'],body))
    def test_unrecognised_successor_does_not_pay_for_a_predecessor_charter(self):
        changed=self.helper.replace('var:rw_ch_recognized_by = root','always = yes')
        self.assertIn('inherited or repeated charter renunciation cost',self.errors(helper=changed))
        changed=self.helper.replace('NOT = { has_variable = rw_ch_renunciation_consequences_done }','always = yes')
        self.assertIn('inherited or repeated charter renunciation cost',self.errors(helper=changed))
    def test_bundle_refusal_uses_actual_leg_capacity_and_one_cost_per_original_actor(self):
        for role in ['payer','payee']:
            sources=dict(self.sources);name='rw_multi_action_effects.txt'
            sources[name]=sources[name].replace('NOT = { has_variable = rw_ba_'+role+'_stress_done }','always = yes')
            self.assertIn('bundle costs repeat or inherit a personal party',self.errors(sources=sources))
        sources=dict(self.sources);name='rw_multi_action_effects.txt';sources[name]=sources[name].replace('scope:rw_ba_refusal_stress_due = flag:yes','always = yes')
        self.assertIn('bundle cost ignores capacity snapshot',self.errors(sources=sources))
    def test_military_renunciation_is_consumed_before_cost_and_callback_keeps_its_observation_role(self):
        source=self.sources['rw_military_restraint_effects.txt']
        self.assertNotIn('rw_promise_breach_stress_effect',block(source,'rw_mr_observe_effect'))
        self.assertNotIn('rw_promise_breach_stress_effect',block(source,'rw_mr_release_effect'))
        changed=dict(self.sources);changed['rw_military_restraint_effects.txt']=source.replace('        rw_promise_breach_stress_effect = yes','')
        self.assertIn('military renunciation cost before consumed promise',self.errors(sources=changed))
if __name__=='__main__':unittest.main()
