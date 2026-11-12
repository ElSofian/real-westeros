"""Guard real review source and negative mutations, without simulating CK3."""
from pathlib import Path
import unittest
from tools import build_g1_native_choice as builder
from test_g1_royal_response import reconsideration_errors, block, definition_bounds

CASES = (
    ('uw', 'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt',
     'common/scripted_effects/rw_unlawful_war_response_effects.txt',
     'events/rw_unlawful_war_response_events.txt'),
    ('xw', 'common/scripted_triggers/rw_external_war_response_triggers.txt',
     'common/scripted_effects/rw_external_war_response_effects.txt',
     'events/rw_external_war_response_events.txt'),
)

class WarDemandReviewTests(unittest.TestCase):
    def sources(self):
        for prefix, triggers, effects, events in CASES:
            yield prefix, *( (builder.TEMPLATES/name).read_text(encoding='utf-8-sig')
                            for name in (triggers,effects,events) )

    def test_real_bound_review_and_one_request(self):
        for prefix,t,e,_ in self.sources():
            with self.subTest(prefix=prefix):
                self.assertEqual([],reconsideration_errors(t,e,prefix))

    def test_wrong_identity_expired_lifetime_or_repeat_is_rejected(self):
        for prefix,t,e,_ in self.sources():
            identity='rw_uw_response_identity_trigger' if prefix=='uw' else 'rw_xw_identity_trigger'
            lifetime='rw_uw_live' if prefix=='uw' else 'rw_xw_review_limit'
            name='rw_'+prefix+'_can_reconsider_trigger'
            start,_,end=definition_bounds(t,name)
            for token in [identity+' = yes','has_variable = '+lifetime,
                          'NOT = { has_variable = rw_'+prefix+'_reviewed_on }']:
                with self.subTest(prefix=prefix,token=token):
                    changed=t[:start]+t[start:end].replace(token,'always = yes')+t[end:]
                    self.assertIn('unbound or repeated review',reconsideration_errors(changed,e,prefix))

    def test_a_second_demand_and_a_renewed_total_timer_are_rejected(self):
        for prefix,t,e,_ in self.sources():
            token='NOT = { has_variable = rw_'+prefix+'_reviewed_on }'
            self.assertIn('repeat demand allowed',reconsideration_errors(t.replace(token,'always = yes'),e,prefix))
            name='rw_'+prefix+'_reconsider_effect'
            start,_,end=definition_bounds(e,name)
            lifetime='rw_uw_live' if prefix=='uw' else 'rw_xw_review_limit'
            changed=e[:end-1]+' set_variable = { name = '+lifetime+' value = flag:yes days = 14 } '+e[end-1:]
            self.assertIn('review renews original total lifetime',reconsideration_errors(t,changed,prefix))

    def test_both_answers_reach_review_after_consuming_their_turn(self):
        for prefix,t,e,_ in self.sources():
            for answer in ['acknowledged','refused']:
                token='rw_'+prefix+'_reconsider_effect = { ANSWER = '+answer+' }'
                self.assertIn('answer bypasses review',reconsideration_errors(t,e.replace(token,'always = yes'),prefix))

    def test_silence_requires_the_original_expired_answer_window(self):
        for prefix,t,e,_ in self.sources():
            name='rw_'+prefix+'_unanswered_effect'
            start,_,end=definition_bounds(e,name)
            token='NOT = { has_variable = rw_'+prefix+'_answer_window }'
            changed=e[:start]+e[start:end].replace(token,'always = yes')+e[end:]
            self.assertIn('stale or early silence review',reconsideration_errors(t,changed,prefix))

    def test_review_and_deadline_never_force_native_or_resource_effects(self):
        for prefix,t,e,_ in self.sources():
            name='rw_'+prefix+'_reconsider_effect'
            start,_,end=definition_bounds(e,name)
            for addition in ['run_interaction = {}','end_war = yes','add_prestige = 50']:
                changed=e[:end-1]+addition+e[end-1:]
                self.assertIn('review executes a consequence automatically',reconsideration_errors(t,changed,prefix))

    def test_deadline_is_scheduled_once_and_native_choices_keep_existing_gates(self):
        for prefix,t,e,event in self.sources():
            namespace='rw_unlawful_war_response' if prefix=='uw' else 'rw_external_war_response'
            self.assertIn('trigger_event = { id = '+namespace+'.0003 days = 8 }',block(e,'rw_'+prefix+'_demand_effect'))
            self.assertIn('rw_'+prefix+'_unanswered_effect = yes',block(event,namespace+'.0003'))
            self.assertIn('trigger = { rw_'+prefix+'_can_queue_native_trigger = yes }',event)
            self.assertIn('trigger = { rw_'+prefix+'_can_demand_trigger = yes }',event)

    def test_legacy_external_timer_is_initialized_once_and_expiry_is_not_reset(self):
        e=(builder.TEMPLATES/CASES[1][2]).read_text(encoding='utf-8-sig')
        for choice in ['demand','acknowledge','refuse']:
            body=block(e,'rw_xw_'+choice+'_effect')
            self.assertIn('NOT = { has_variable = rw_xw_review_schema }',body)
            self.assertIn('name = rw_xw_review_schema value = 1',body)
            self.assertIn('name = rw_xw_review_limit value = flag:yes days = 7',body)

if __name__ == '__main__':
    unittest.main()
