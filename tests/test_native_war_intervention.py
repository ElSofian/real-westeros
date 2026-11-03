"""Verify actual native intervention wiring and source safety, never a war simulation."""
import json
from pathlib import Path
import re
import unittest
from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_g1_royal_response import block

ROOT=builder.TEMPLATES
TRIGGER=ROOT/'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt'
EFFECT=ROOT/'common/scripted_effects/rw_unlawful_war_intervention_effects.txt'
EVENT=ROOT/'events/rw_unlawful_war_intervention_events.txt'


def errors(t,e):
    found=[]
    def need(source,parts,label):
        if any(not re.search(re.escape(p)+r'(?![\w:])',source) for p in parts):found.append(label)
    context=block(t,'rw_uw_native_context_trigger')
    need(context,('rw_uw_response_identity_trigger = yes','this = scope:rw_uw_issuer',
        'NOT = { is_participant_in_war = scope:rw_uw_war }',
        'any_character_war = { this = scope:rw_uw_war }',
        'NOT = { any_character_war = { count >= 2 } }'),'unique war and jurisdiction')
    # Restrict ALL wars, not only matching claim wars: native interface may choose a war.
    if 'using_cb' in context:found.append('ambiguity guard was narrowed')
    ticket=block(t,'rw_uw_native_ticket_trigger')
    need(ticket,('this = scope:rw_uw_issuer','story_type = story_rw_unlawful_war_response',
        'story_owner = scope:rw_uw_attacker','var:rw_uw_serial = scope:rw_uw_serial',
        'var:rw_uw_authority = scope:rw_uw_authority','var:rw_uw_issuer = scope:rw_uw_issuer',
        'var:rw_uw_attacker = scope:rw_uw_attacker','var:rw_uw_defender = scope:rw_uw_defender',
        'var:rw_uw_war = scope:rw_uw_war','var:rw_uw_state = flag:native_queued',
        'NOT = { has_variable = rw_uw_native_dispatched_on }'),'immutable ticket')
    send=block(t,'rw_uw_can_send_native_trigger')
    need(send,('rw_uw_native_ticket_trigger = yes','rw_uw_native_context_trigger = yes',
        'scope:actor = scope:rw_uw_issuer','scope:recipient = scope:rw_uw_attacker',
        'is_character_interaction_valid = {','interaction = stop_attacker_vassal_war_interaction'),
        'fresh native validity')
    if send.count('scope:target = scope:rw_uw_war')!=2:found.append('native target changed or unbound')
    queued=block(e,'rw_uw_queue_native_effect')
    need(queued,('limit = { rw_uw_can_queue_native_trigger = yes }','flag:native_queued',
        'remove_variable = rw_uw_issuer_window','id = rw_unlawful_war_intervention.0001 days = 1'),'deferred consumption')
    if 'run_interaction' in queued or 'name = rw_uw_live' in queued:found.append('declaration reentry or extended lifetime')
    dispatch=block(e,'rw_uw_send_native_effect')
    need(dispatch,('limit = { rw_uw_native_ticket_trigger = yes }','save_scope_as = actor',
        'scope:rw_uw_attacker = { save_scope_as = recipient }',
        'scope:rw_uw_war = { save_scope_as = target }','limit = { rw_uw_can_send_native_trigger = yes }',
        'flag:native_requested','flag:native_blocked','remove_variable = rw_uw_live',
        'interaction = stop_attacker_vassal_war_interaction','actor = scope:rw_uw_issuer',
        'recipient = scope:rw_uw_attacker','send_threshold = decline'),'guarded native dispatch')
    if dispatch.count('run_interaction =')!=1:found.append('native dispatch repeated')
    if 'run_interaction =' in dispatch and ('rw_uw_native_dispatched_on' not in dispatch or
        dispatch.index('rw_uw_native_dispatched_on')>dispatch.index('run_interaction =')):
        found.append('dispatch before receipt')
    forbidden=r'\b(start_war|end_war|change_title_holder|add_gold|add_prestige|use_hook|add_hook|add_opinion|execute_threshold|add_imprisonment_reason|every_living_character)\s*='
    if re.search(forbidden,clean_script(e)[0]):found.append('native result/cost forced or copied')
    return found


class NativeWarInterventionTests(unittest.TestCase):
    def setUp(self):self.t=TRIGGER.read_text();self.e=EFFECT.read_text()

    def test_actual_source_contract(self):self.assertEqual([],errors(self.t,self.e))

    def test_multilateral_war_target_ambiguity_rejected(self):
        for old,new in [('count >= 2','count >= 200'),
                        ('any_character_war = { count >= 2 }','any_character_war = { count >= 2 using_cb = claim_cb }')]:
            with self.subTest(old=old):self.assertTrue(errors(self.t.replace(old,new),self.e))

    def test_wrong_war_or_recipient_rejected(self):
        for old,new in [('scope:target = scope:rw_uw_war','scope:target = scope:rw_uw_authority'),
                        ('scope:recipient = scope:rw_uw_attacker','scope:recipient = scope:rw_uw_defender')]:
            with self.subTest(old=old):self.assertTrue(errors(self.t.replace(old,new),self.e))

    def test_stale_serial_authority_or_repeated_ticket_rejected(self):
        for old,new in [('var:rw_uw_serial = scope:rw_uw_serial','has_variable = rw_uw_serial'),
                        ('var:rw_uw_authority = scope:rw_uw_authority','var:rw_uw_authority = scope:rw_uw_war'),
                        ('flag:native_queued','flag:pending'),
                        ('NOT = { has_variable = rw_uw_native_dispatched_on }','always = yes')]:
            with self.subTest(old=old):self.assertTrue(errors(self.t.replace(old,new),self.e))

    def test_native_validation_cannot_be_bypassed(self):
        self.assertTrue(errors(self.t.replace('is_character_interaction_valid = {','always = {'),self.e))

    def test_native_dispatch_cannot_be_retargeted(self):
        self.assertTrue(errors(self.t,self.e.replace('recipient = scope:rw_uw_attacker','recipient = scope:rw_uw_defender')))

    def test_reentrant_declaration_or_renewed_total_window_rejected(self):
        self.assertTrue(errors(self.t,self.e.replace('days = 1','days = 0')))
        self.assertTrue(errors(self.t,self.e.replace('remove_variable = rw_uw_issuer_window','set_variable = { name = rw_uw_live value = flag:yes days = 14 }')))

    def test_direct_war_end_native_cost_or_forced_acceptance_rejected(self):
        for op in ('end_war = white_peace','execute_threshold = decline','use_hook = scope:rw_uw_attacker',
                   'add_gold = -100','add_opinion = {}','change_title_holder = {}'):
            with self.subTest(op=op):self.assertTrue(errors(self.t,self.e+'\n bad = { '+op+' }'))

    def test_receipt_is_consumed_before_the_one_native_call(self):
        pos=self.e.index('run_interaction =')
        self.assertLess(self.e.index('flag:closed'),pos)
        self.assertLess(self.e.index('rw_uw_native_dispatched_on'),pos)
        self.assertLess(self.e.index('remove_variable = rw_uw_live'),pos)
        self.assertNotIn('native_completed',self.e)

    def test_hidden_event_is_isolated_from_declaration_stack(self):
        text=EVENT.read_text()
        self.assertIn('hidden = yes',text)
        self.assertIn('trigger = { rw_uw_native_ticket_trigger = yes }',text)
        self.assertIn('rw_uw_send_native_effect = yes',text)
        self.assertNotIn('save_scope_as = actor',builder.ACCEPT)
        self.assertNotIn('run_interaction',builder.ACCEPT)

    def test_real_royal_event_exposes_shared_optional_intervention(self):
        text=(ROOT/'events/rw_unlawful_war_response_events.txt').read_text()
        self.assertIn('trigger = { rw_uw_can_queue_native_trigger = yes }',text)
        self.assertIn('rw_uw_queue_native_effect = yes',text)
        self.assertNotIn('is_ai',text+self.t+self.e)

    def test_known_native_api_fields_only(self):
        api=block(self.e,'run_interaction')
        fields=re.findall(r'(?m)^\s*(\w+)\s*=',api)
        self.assertEqual(['run_interaction','interaction','actor','recipient','send_threshold'],fields)
        self.assertNotIn('target =',api)  # No invented run_interaction argument.

    def test_original_runtime_libraries_are_integrated_without_native_override(self):
        self.assertTrue((ROOT/'common/scripted_effects/rw_unlawful_war_response_effects.txt').is_file())
        self.assertFalse((ROOT/'common/character_interactions/zz_rw_native_war_choice.txt').exists())
        self.assertFalse((builder.REPO/'experiments/g1_native_choice/template/common/scripted_effects/rw_unlawful_war_response_effects.txt').exists())
        for path in (ROOT/'common/on_action').glob('*.txt'):
            self.assertNotIn('rw_uw_',clean_script(path.read_text())[0])

    def test_native_source_receipt_covers_actual_stop_and_followups(self):
        receipt=json.loads((builder.REPO/'docs/G1_NATIVE_INTERVENTION_SOURCE_RECEIPT.json').read_text())
        vassal=next(r for r in receipt['files'] if r['path']=='AGOT/'+builder.VASSAL)
        self.assertTrue(vassal['markers']['stop_attacker_vassal_war_interaction'])
        self.assertTrue(vassal['markers']['vassal_interaction.0001'])
        self.assertEqual(vassal['sha256'],builder.pinned_sources()[builder.VASSAL])


if __name__=='__main__':unittest.main()
