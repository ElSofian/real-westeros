"""Validate real native-request/title-gain association, not a CK3 simulation."""
import re
import unittest
from tools import build_g3_native_confiscation as b
from tools.build_g1_native_choice import bounds
from tools.validate_mod import clean_script
from test_native_house_confiscation import FIXTURE


def block(text,name):
    a,_,e=bounds(text,name)
    return clean_script(text[a:e])[0]


def errors(t,e,event,wrapper,story):
    found=[]
    def need(source,parts,label):
        if any(not re.search(re.escape(x)+r'(?![\w:])',source) for x in parts):found.append(label)
    before=block(e,'rw_hcr_register_request_effect')
    need(before,('rw_hcr_before_trigger = yes','NOT = { any_owned_story = { rw_hcr_same_request_trigger = yes } }',
         'clear_saved_scope = rw_hcr_request','NOT = { has_variable = rw_hcr_schema }',
         'name = rw_hcr_title value = scope:landed_title',
         'name = rw_hcr_former value = scope:recipient','name = rw_hcr_house value = scope:recipient.house',
         'name = rw_hcr_authority value = scope:actor.primary_title',
         'name = rw_hcr_pending value = flag:yes days = 30'), 'exact fresh native request')
    match=block(t,'rw_hcr_matches_gain_trigger')
    need(match,('story_type = story_rw_house_revocation_request','story_owner = root',
         'var:rw_hcr_schema = 1','has_variable = rw_hcr_pending','has_variable = rw_hcr_sent_on','var:rw_hcr_issuer = root',
         'var:rw_hcr_title = scope:title','var:rw_hcr_former = scope:previous_holder',
         'var:rw_hcr_house = scope:previous_holder.house','holder = root'), 'wrong request or owner')
    context=block(t,'rw_hcr_gain_context_trigger')
    need(context,('rw_hc_adapter_available_trigger = yes','scope:title = { holder = root tier >= tier_county }',
         'scope:previous_holder = { is_alive = yes exists = house }',
         'NOT = { any_owned_story = { count >= 2 rw_hcr_matches_gain_trigger = yes } }'), 'actual/unique gain')
    for token in ('scope:actor','scope:recipient','scope:landed_title','revoke_title_interaction'):
        if token in context+match:found.append('requires unproved callback propagation')
    observe=block(e,'rw_hcr_observe_gain_effect')
    need(observe,('limit = { rw_hcr_gain_context_trigger = yes }',
         'remove_variable = rw_hcr_pending','end_story = yes',
         'NOT = { any_owned_story = { rw_hcr_matching_receipt_trigger = yes } }',
         'type = story_rw_title_provenance','NOT = { has_variable = rw_tp_schema }',
         'name = rw_hcr_receipt_serial value = -1',
         'var:rw_tp_serial = scope:rw_hcr_receipt_serial',
         'name = rw_tp_source value = flag:pending_native_revocation_transfer',
         'name = rw_tp_repeat_window value = flag:yes days = 1',
         'name = rw_tp_retained value = flag:yes years = 5'), 'consume/dedup/canonical record')
    if 'remove_variable = rw_hcr_pending' in observe and observe.index('remove_variable = rw_hcr_pending')>observe.index('create_story'):found.append('request consumed late')
    need(observe,('always = scope:rw_hcr_sovereign','rw_house_sovereign_trigger = yes',
         'NOT = { has_variable = rw_lr_offer_scheduled }',
         'name = rw_tp_land_authority value = scope:rw_hcr_authority',
         'name = rw_tp_former_house value = scope:rw_hcr_house',
         'name = rw_tp_hc_offer_pending value = flag:yes days = 7',
         'id = rw_confiscation_transfer.0001 days = 1'), 'fresh filing snapshot/isolated offer')
    need(block(e,'rw_hcr_declined_effect'),('rw_hcr_same_request_trigger = yes','remove_variable = rw_hcr_pending',
         'end_story = yes'), 'refusal association not closed')
    need(wrapper,('rw_on_title_revocation_context rw_on_pledged_title_gain_context rw_on_house_revocation_gain',
         'trigger = { rw_hcr_gain_context_trigger = yes }','effect = { rw_hcr_observe_gain_effect = yes }'), 'additive child')
    need(story,('on_owner_death = { end_story = yes }','NOT = { has_variable = rw_hcr_pending }'), 'request inheritance/expiry')
    ticket=block(t,'rw_hcr_offer_ticket_trigger')
    need(ticket,('this = scope:rw_hcr_issuer','var:rw_tp_serial = scope:rw_hcr_receipt_serial',
         'var:rw_tp_title = scope:rw_hcr_title','var:rw_tp_former_house = scope:rw_hcr_house',
         'var:rw_tp_land_authority = scope:rw_hcr_authority','has_variable = rw_tp_hc_offer_pending'), 'stale offer')
    open_effect=block(e,'rw_hcr_open_filing_effect')
    need(open_effect,('limit = { rw_hcr_offer_ticket_trigger = yes }','remove_variable = rw_tp_hc_offer_pending',
         'rw_lr_open_deposit_effect = yes'), 'offer consumed before UI')
    if open_effect.index('remove_variable')>open_effect.index('rw_lr_open_deposit_effect'):found.append('UI before consumption')
    need(event,('hidden = yes','trigger = { rw_hcr_offer_ticket_trigger = yes }',
         'immediate = { rw_hcr_open_filing_effect = yes }'), 'isolated event')
    if re.search(r'save_scope_as\s*=\s*(actor|recipient|title|previous_holder|landed_title)\b',clean_script(e)[0]):
        found.append('native aliases overwritten')
    for token in ('run_interaction =','change_title_holder =','resolve_title_and_vassal_change =',
                  'revoke_title_interaction_effect =','add_revoke_title_reason =','add_gold =',
                  'use_hook =','make_story_owner =','rw_ri_link_transfer_effect =','rw_lr_capture_effect =',
                  'every_living_character','every_in_global_list','is_ai ='):
        if token in clean_script(t+e+event+story)[0]:found.append('native/private-case state changed')
    return found


class ConfiscationTransferTests(unittest.TestCase):
    def setUp(self):
        root=b.TEMPLATES
        self.t=(root/'common/scripted_triggers/rw_confiscation_transfer_triggers.txt').read_text()
        self.e=(root/'common/scripted_effects/rw_confiscation_transfer_effects.txt').read_text()
        self.event=(root/'events/rw_confiscation_transfer_events.txt').read_text()
        self.wrapper=(root/'common/on_action/rw_title_provenance_on_actions.txt').read_text()
        self.story=(root/'common/story_cycles/rw_house_revocation_request.txt').read_text()

    def check(self,t=None,e=None,event=None,wrapper=None,story=None):
        return errors(t or self.t,e or self.e,event or self.event,wrapper or self.wrapper,story or self.story)

    def test_actual_runtime_contract(self):self.assertEqual([],self.check())

    def test_three_additions_preserve_native_bodies_and_zero_factor(self):
        for newline in ('\n','\r\n'):
            old,new=b.patch_native(b'\xef\xbb\xbf'+FIXTURE.replace('\n',newline).encode());restored=new
            for addition in b.INSERTIONS:
                self.assertEqual(1,new.count(addition.encode()));restored=restored.replace(addition.encode(),b'',1)
            self.assertEqual(old,restored)
            self.assertLess(new.index(b.BEFORE.encode()),new.index(b'original_native_send'))
            self.assertLess(new.index(b.AFTER.encode()),new.index(b'original_resistance'))
            self.assertEqual(block(old.decode(),'on_accept'),block(new.decode(),'on_accept'))

    def test_missing_or_duplicate_send_or_decline_refused(self):
        for name in ('on_send','on_decline'):
            for changed in (FIXTURE.replace(name,'other_block'),FIXTURE.replace('cost = {',name+' = {} cost = {')):
                with self.assertRaises(ValueError):b.patch_native(changed.encode())

    def test_request_replay_and_other_selected_title_refused(self):
        for old,new in [('name = rw_hcr_title value = scope:landed_title','name = rw_hcr_title value = scope:actor.primary_title'),
                        ('NOT = { any_owned_story = { rw_hcr_same_request_trigger = yes } }','always = yes'),
                        ('days = 30','days = 300')]:
            with self.subTest(old=old):self.assertTrue(self.check(e=self.e.replace(old,new)))

    def test_other_holder_title_house_authority_or_ambiguous_request_refused(self):
        for old,new in [('var:rw_hcr_title = scope:title','exists = var:rw_hcr_title'),
                        ('var:rw_hcr_former = scope:previous_holder','exists = var:rw_hcr_former'),
                        ('var:rw_hcr_house = scope:previous_holder.house','exists = var:rw_hcr_house'),
                        ('holder = root','exists = holder'),('count >= 2 rw_hcr_matches_gain_trigger','count >= 200 rw_hcr_matches_gain_trigger')]:
            with self.subTest(old=old):self.assertTrue(self.check(t=self.t.replace(old,new)))

    def test_dead_previous_holder_not_associated_with_inheritance(self):
        self.assertTrue(self.check(t=self.t.replace('scope:previous_holder = { is_alive = yes exists = house }','scope:previous_holder = { exists = house }')))

    def test_existing_canonical_fact_never_reannotated_or_refreshed(self):
        observe=block(self.e,'rw_hcr_observe_gain_effect')
        self.assertNotIn('random_owned_story',observe[observe.index('type = story_rw_title_provenance'):])
        for name in ('rw_tp_observed_on','rw_tp_retained','rw_tp_repeat_window'):
            self.assertEqual(1,observe.count('name = '+name+' '))
        self.assertTrue(self.check(e=self.e.replace('NOT = { any_owned_story = { rw_hcr_matching_receipt_trigger = yes } }','always = yes')))

    def test_fresh_constructor_failure_cannot_use_stale_pointer_or_serial(self):
        for old,new in [('NOT = { has_variable = rw_tp_schema }','always = yes'),
                        ('var:rw_tp_serial = scope:rw_hcr_receipt_serial','has_variable = rw_tp_serial')]:
            with self.subTest(old=old):self.assertTrue(self.check(e=self.e.replace(old,new)))

    def test_refusal_expires_request_without_war_outcome_inference(self):
        decline=block(self.e,'rw_hcr_declined_effect')
        self.assertNotIn('create_story',decline)
        self.assertTrue(self.check(e=self.e.replace('remove_variable = rw_hcr_pending','always = yes',1)))

    def test_delayed_filing_other_serial_or_reader_refused(self):
        for old,new in [('var:rw_tp_serial = scope:rw_hcr_receipt_serial','has_variable = rw_tp_serial'),
                        ('this = scope:rw_hcr_issuer','always = yes'),
                        ('has_variable = rw_tp_hc_offer_pending','always = yes')]:
            with self.subTest(old=old):self.assertTrue(self.check(t=self.t.replace(old,new)))

    def test_no_native_replay_or_private_case_backfill(self):
        for op in ('run_interaction = {}','revoke_title_interaction_effect = yes','rw_ri_link_transfer_effect = yes','add_gold = -100'):
            with self.subTest(op=op):self.assertTrue(self.check(e=self.e+'\n bad = { '+op+' }'))
        tp=(b.TEMPLATES/'common/scripted_triggers/rw_title_provenance_triggers.txt').read_text()
        self.assertIn('var:rw_evidence_kind = flag:participant_exposed',tp)
        self.assertNotIn('rw_ri_',self.e)

    def test_original_callback_children_preserved_and_no_duplicate_wrapper(self):
        self.assertEqual(1,self.wrapper.count('on_title_gain = {'))
        self.assertTrue(self.check(wrapper=self.wrapper.replace('rw_on_pledged_title_gain_context ','')))


if __name__=='__main__':unittest.main()
