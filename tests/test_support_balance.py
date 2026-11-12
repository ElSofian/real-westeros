"""Check the common delivered support reward and negative source mutations."""
from pathlib import Path
import re
import unittest
from test_native_political_memories import CALLS
from test_g1_royal_response import block

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'
CALLERS=CALLS+(('rw_multi_action_effects.txt','rw_ba_support_effect','rw_ba_payer','rw_ba_payee'),)

def reward_errors(helper,values,modifier,sources):
    errors=[]
    body=block(helper,'rw_public_support_reward_effect')
    for token in ('exists = $PROVIDER$','exists = $CLIENT$','NOT = { $PROVIDER$ = $CLIENT$ }',
                  '$PROVIDER$ = { is_alive = yes is_landed = yes }',
                  '$CLIENT$ = { is_alive = yes is_landed = yes }',
                  'NOT = { has_opinion_modifier = { target = $PROVIDER$ modifier = rw_public_support_received_opinion } }',
                  'add_prestige = $PROVIDER$.rw_public_support_prestige_value'):
        if token not in body:errors.append('unbound or repeated support reward')
    marker=body.find('add_opinion = { target = $PROVIDER$ modifier = rw_public_support_received_opinion }')
    if marker<0 or marker>body.find('add_prestige ='):errors.append('reward before pair marker')
    if helper.count('add_prestige =')!=1:errors.append('extra prestige execution')
    value=block(values,'rw_public_support_prestige_value')
    for token in ('value = 10','tier_empire } value = 50','tier_kingdom } value = 35','tier_duchy } value = 20'):
        if not re.search(re.escape(token)+r'(?![\w.])',value):errors.append('wrong provider rank reward')
    if value.find('tier_empire')>value.find('tier_kingdom') or value.find('tier_kingdom')>value.find('tier_duchy'):
        errors.append('rank branches shadow stronger providers')
    for token in ('opinion = 5','years = 1','stacking = no','decaying = no'):
        if token not in modifier:errors.append('wrong shared pair reward lifetime')
    for filename,name,provider,client in CALLERS:
        effect=block(sources[filename],name)
        call='rw_public_support_reward_effect = { PROVIDER = scope:'+provider+' CLIENT = scope:'+client+' }'
        memory='rw_pm_public_support_effect = { PROVIDER = scope:'+provider+' CLIENT = scope:'+client+' }'
        if effect.count(call)!=1 or 'add_prestige =' in effect:errors.append('bypassed shared support reward')
        if effect.find(memory)<effect.find(call):errors.append('memory before delivered reward')
    if re.search(r'\b(add_gold|remove_short_term_gold|run_interaction|start_war|end_war|create_story)\s*=',helper):
        errors.append('reward changes another contract leg')
    return errors

class SupportBalanceTests(unittest.TestCase):
    def setUp(self):
        self.helper=(MOD/'common/scripted_effects/rw_public_support_effects.txt').read_text()
        self.values=(MOD/'common/script_values/rw_public_support_values.txt').read_text()
        self.modifier=(MOD/'common/opinion_modifiers/rw_public_support_opinions.txt').read_text()
        self.sources={f:(MOD/'common/scripted_effects'/f).read_text() for f,_,_,_ in CALLERS}
    def errors(self,helper=None,values=None,modifier=None,sources=None):
        return reward_errors(self.helper if helper is None else helper,self.values if values is None else values,
                             self.modifier if modifier is None else modifier,self.sources if sources is None else sources)
    def test_real_rank_reward_and_all_five_delivered_callers(self):
        self.assertEqual([],self.errors())
    def test_missing_identity_living_parties_or_pair_cooldown_is_detected(self):
        for token in ('exists = $PROVIDER$','NOT = { $PROVIDER$ = $CLIENT$ }',
                      '$CLIENT$ = { is_alive = yes is_landed = yes }',
                      'NOT = { has_opinion_modifier = { target = $PROVIDER$ modifier = rw_public_support_received_opinion } }'):
            self.assertIn('unbound or repeated support reward',self.errors(helper=self.helper.replace(token,'always = yes')))
    def test_reward_uses_provider_rank_and_never_the_recipient_rank(self):
        self.assertIn('unbound or repeated support reward',self.errors(helper=self.helper.replace('$PROVIDER$.rw_public_support_prestige_value','$CLIENT$.rw_public_support_prestige_value')))
        self.assertIn('wrong provider rank reward',self.errors(values=self.values.replace('tier_empire } value = 50','tier_empire } value = 500')))
    def test_pair_marker_is_consumed_before_native_prestige(self):
        before='add_opinion = { target = $PROVIDER$ modifier = rw_public_support_received_opinion }'
        self.assertIn('reward before pair marker',self.errors(helper=self.helper.replace(before,'')))
    def test_extra_prestige_or_another_native_leg_is_rejected(self):
        self.assertIn('extra prestige execution',self.errors(helper=self.helper+'\nadd_prestige = 50'))
        self.assertIn('reward changes another contract leg',self.errors(helper=self.helper+'\nadd_gold = 25'))
    def test_each_call_is_shared_and_cannot_fall_back_to_a_flat_reward(self):
        for filename,_,provider,client in CALLERS:
            changed=dict(self.sources)
            call='rw_public_support_reward_effect = { PROVIDER = scope:'+provider+' CLIENT = scope:'+client+' }'
            changed[filename]=changed[filename].replace(call,'scope:'+client+' = { add_prestige = 50 }')
            self.assertIn('bypassed shared support reward',self.errors(sources=changed))
    def test_same_pair_reward_cannot_stack_or_renew_each_repeat(self):
        self.assertIn('wrong shared pair reward lifetime',self.errors(modifier=self.modifier.replace('years = 1','years = 5')))
        self.assertIn('wrong shared pair reward lifetime',self.errors(modifier=self.modifier.replace('stacking = no','stacking = yes')))
    def test_comparable_broken_promises_share_two_years_and_service_grudge_is_not_refreshed(self):
        for filename in ['rw_obligation_opinions.txt','rw_favor_renunciation_opinions.txt','rw_restitution_pledge_opinions.txt','rw_restraint_response_opinions.txt']:
            text=(MOD/'common/opinion_modifiers'/filename).read_text()
            self.assertIn('opinion = -15',text)
            self.assertIn('years = 2',text)
        effect=block(self.sources['rw_obligation_effects.txt'],'rw_service_resent_breach_effect')
        self.assertIn('NOT = { has_opinion_modifier = { target = scope:rw_service_provider modifier = rw_broken_service_opinion } }',effect)
        self.assertLess(effect.index('name = rw_service_reacted_serial'),effect.index('add_opinion ='))

if __name__=='__main__':unittest.main()
