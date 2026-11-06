"""Real CK3 source contracts and adversarial mutations; no simulated title engine."""
from pathlib import Path
import re
import unittest
from tools.validate_mod import clean_script
from tools.build_g1_native_choice import bounds
from tools import build_g3_native_confiscation as builder
from test_native_house_confiscation import FIXTURE

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def block(s,name):
    a,_,end=bounds(s,name)
    return clean_script(s[a:end])[0]


def contract_errors(t,e,i,v,story):
    out=[]
    def need(source,parts,label):
        if any(x not in source for x in parts):out.append(label)
    need(block(t,'rw_pcr_gain_source_trigger'),('story_type = story_rw_house_revocation_request',
        'var:rw_hcr_schema = 1','story_owner = scope:rw_hcr_issuer','has_variable = rw_pcr_primary',
        'NOT = { has_variable = rw_hcr_pending }','var:rw_hcr_former = scope:rw_hcr_former',
        'var:rw_hcr_title = scope:rw_hcr_title','holder = scope:rw_hcr_issuer'), 'gain source')
    need(block(t,'rw_pcr_pending_accept_trigger'),('story_owner = scope:actor','has_variable = rw_hcr_pending',
        'has_variable = rw_pcr_primary','NOT = { has_variable = rw_pcr_accept_seen }',
        'var:rw_hcr_former = scope:recipient','var:rw_hcr_title = scope:landed_title'), 'native accept tuple')
    need(block(t,'rw_pcr_awaiting_accept_trigger'),('rw_pcr_record_trigger = yes',
        'has_variable = rw_pcr_gain_ticket','NOT = { has_variable = rw_pcr_accept_seen }',
        'var:rw_pcr_former = scope:recipient','var:rw_pcr_title = scope:landed_title',
        'holder = scope:actor'), 'gain-first accept tuple')
    need(block(e,'rw_pcr_confirm_effect'),('rw_pcr_record_trigger = yes','has_variable = rw_pcr_gain_ticket',
        'has_variable = rw_pcr_accept_seen','NOT = { has_variable = rw_pcr_confirmed_on }',
        'holder = scope:rw_pcr_confirm.var:rw_pcr_issuer','remove_variable = rw_pcr_gain_ticket',
        'name = rw_pcr_restore_window value = flag:yes years = 5'), 'both proofs before confirmation')
    need(block(e,'rw_pcr_capture_gain_effect'),('limit = { rw_pcr_gain_source_trigger = yes }',
        'NOT = { has_variable = rw_pcr_schema }','name = rw_pcr_gain_ticket value = flag:yes days = 2',
        'scope:rw_pcr_request = { has_variable = rw_pcr_accept_seen }',
        'scope:rw_pcr_request = { has_variable = rw_pcr_accepted }','rw_pcr_confirm_effect = yes'), 'accept-first branch')
    accepted=block(e,'rw_pcr_native_accepted_effect')
    need(accepted,('rw_pcr_pending_accept_trigger = yes','rw_pcr_awaiting_accept_trigger = yes',
        'name = rw_pcr_accepted value = flag:yes days = 2','name = rw_pcr_accept_seen value = flag:yes',
        'rw_pcr_confirm_effect = yes'), 'gain-first branch')
    capacity=block(t,'rw_pcr_capacity_trigger')
    need(capacity,('rw_pcr_record_trigger = yes','is_independent_ruler = yes',
        'highest_held_title_tier >= tier_kingdom','highest_held_title_tier = tier_county',
        'liege = scope:rw_pcr_check.var:rw_pcr_issuer','house = scope:rw_pcr_check.var:rw_pcr_house',
        'primary_title = scope:rw_pcr_check.var:rw_pcr_authority',
        'holder = scope:rw_pcr_check.var:rw_pcr_issuer tier = tier_duchy',
        'is_noble_family_title = no','is_landless_type_title = no','is_head_of_faith = no',
        'has_partition_succession_realm_law_trigger = yes','has_variable = agot_title_blocked_to_give_away'), 'current personal capacity')
    if capacity.count('is_at_war = no')!=2 or capacity.count('is_imprisoned = no')!=2:out.append('current personal capacity')
    need(block(t,'rw_pcr_offerable_trigger'),('has_variable = rw_pcr_confirmed_on',
        'has_variable = rw_pcr_restore_window','NOT = { has_variable = rw_pcr_attempt }',
        'rw_pcr_capacity_trigger = yes'), 'offer on intent or retry')
    view=block(t,'rw_pcr_view_trigger')
    need(view,('this = scope:rw_pcr_issuer','rw_pcr_record_trigger = yes',
        'var:rw_pcr_serial = scope:rw_pcr_serial','var:rw_pcr_issuer = scope:rw_pcr_issuer',
        'var:rw_pcr_former = scope:rw_pcr_former','var:rw_pcr_title = scope:rw_pcr_title',
        'var:rw_pcr_house = scope:rw_pcr_house','var:rw_pcr_authority = scope:rw_pcr_authority'), 'stale panel')
    queue=block(e,'rw_pcr_queue_effect')
    need(queue,('limit = { rw_pcr_can_return_trigger = yes }','name = rw_pcr_attempt value = flag:yes',
        'name = rw_pcr_execute_ticket value = flag:yes days = 2','id = rw_post_confiscation.0002 days = 1'), 'queue replay')
    run=block(e,'rw_pcr_execute_effect')
    need(run,('rw_pcr_view_trigger = yes','has_variable = rw_pcr_execute_ticket var:rw_pcr_result = flag:pending',
        'rw_nd_adapter_available_trigger = yes','rw_pcr_capacity_trigger = yes',
        'clear_local_variable_list = target_titles','clear_local_variable_list = titles_to_grant',
        'clear_saved_scope = recipient_is_independent','save_scope_as = actor','save_scope_as = recipient',
        'save_scope_as = target','save_scope_as = dummy_gender','add_to_temporary_list = target_titles',
        'type = granted','holder = scope:rw_pcr_former change = scope:rw_pcr_change take_baronies = no'), 'exact guarded grant')
    order=('remove_variable = rw_pcr_execute_ticket','rw_pcr_capacity_trigger = yes',
        'rw_nd_native_eligible_trigger = yes','create_title_and_vassal_change',
        'change_title_holder','resolve_title_and_vassal_change',
        'limit = { scope:rw_pcr_title = { holder = scope:rw_pcr_former } }',
        'name = rw_pcr_result value = flag:transferred','rw_nd_native_consequences_effect = yes',
        'rw_nd_native_notification_effect = yes')
    at=[run.find(x) for x in order]
    if min(at)<0 or at!=sorted(at):out.append('world action before consumption or consequences before verified transfer')
    for native in ('create_title_and_vassal_change','change_title_holder','resolve_title_and_vassal_change',
                   'rw_nd_native_consequences_effect','rw_nd_native_notification_effect'):
        if len(re.findall(r'\b'+native+r'\s*=',run))!=1:out.append('replayed native effect')
    need(block(e,'rw_pcr_title_left_effect'),('scope:previous_holder = {','every_owned_story','NOT = { holder = scope:previous_holder }',
        'scope:previous_holder = { has_variable = rw_pcr_counter }',
        'var:rw_pcr_title = scope:title','remove_variable = rw_pcr_gain_ticket',
        'remove_variable = rw_pcr_restore_window'), 'reacquisition revives old case')
    need(i,('is_shown = { rw_pcr_can_review_trigger = yes }','is_valid = { rw_pcr_can_review_trigger = yes }',
        'on_accept = { rw_pcr_open_effect = yes }','ai_targets = { ai_recipients = vassals }','ai_frequency = 6'), 'shared initiation')
    need(v,('trigger = { rw_pcr_can_return_trigger = yes }','rw_pcr_queue_effect = yes',
        'name = rw_post_confiscation.keep','ai_chance = { base = 40',
        'immediate = { rw_pcr_execute_effect = yes }'), 'actual explicit choice')
    need(story,('on_owner_death = { end_story = yes }','days = 30',
        'var:rw_pcr_former = { is_alive = no }'), 'cleanup/inherited entitlement')
    source=clean_script(t+e+i+v+story)[0]
    if re.search(r'\b(is_ai|run_interaction|add_gold|add_claim|add_revoke_title_reason|consume_revoke_title_reason|change_title_holder_include_vassals|every_living_character|every_in_global_list)\s*=',source):out.append('privilege, replay or unrelated world state')
    return out


class PostConfiscationTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_post_confiscation_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_post_confiscation_effects.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_post_confiscation_interactions.txt').read_text()
        self.v=(MOD/'events/rw_post_confiscation_events.txt').read_text()
        self.s=(MOD/'common/story_cycles/rw_post_confiscation.txt').read_text()

    def errors(self,t=None,e=None):return contract_errors(t or self.t,e or self.e,self.i,self.v,self.s)
    def test_full_source_contract(self):self.assertEqual([],self.errors())

    def test_native_accept_suffix_preserves_original_bytes_and_all_other_bodies(self):
        for newline in ('\n','\r\n'):
            before,after=builder.patch_native(b'\xef\xbb\xbf'+FIXTURE.replace('\n',newline).encode())
            restored=after
            for addition in builder.INSERTIONS:
                self.assertEqual(1,after.count(addition.encode()));restored=restored.replace(addition.encode(),b'',1)
            self.assertEqual(before,restored)
            self.assertGreater(after.index(builder.ACCEPTED.encode()),after.index(b'original_success'))

    def test_no_case_from_an_intention_or_wrong_transfer(self):
        for token in ('story_type = story_rw_house_revocation_request','NOT = { has_variable = rw_hcr_pending }',
                      'var:rw_hcr_former = scope:rw_hcr_former','holder = scope:rw_hcr_issuer'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_acceptance_and_gain_both_required(self):
        for token in ('has_variable = rw_pcr_gain_ticket','has_variable = rw_pcr_accept_seen',
                      'NOT = { has_variable = rw_pcr_confirmed_on }'):
            with self.subTest(token=token):self.assertTrue(self.errors(e=self.e.replace(token,'')))

    def test_both_orders_have_actual_routes_without_clock_refresh(self):
        for token in ('scope:rw_pcr_request = { has_variable = rw_pcr_accepted }',
                      'rw_pcr_awaiting_accept_trigger = yes','name = rw_pcr_accepted value = flag:yes days = 2'):
            with self.subTest(token=token):self.assertTrue(self.errors(e=self.e.replace(token,'')))
        self.assertEqual(1,self.e.count('name = rw_pcr_restore_window'))
        self.assertEqual(2,self.t.count('NOT = { has_variable = rw_pcr_accept_seen }'))

    def test_wrong_pair_title_or_duplicate_acceptance_is_rejected(self):
        for token in ('var:rw_hcr_title = scope:landed_title','var:rw_pcr_former = scope:recipient',
                      'NOT = { has_variable = rw_pcr_accept_seen }'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_missing_confirmation_or_repeated_gift_is_rejected(self):
        for token in ('has_variable = rw_pcr_confirmed_on','NOT = { has_variable = rw_pcr_attempt }'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_current_capacity_and_native_protections_are_mandatory(self):
        for token in ('highest_held_title_tier = tier_county','house = scope:rw_pcr_check.var:rw_pcr_house',
                      'primary_title = scope:rw_pcr_check.var:rw_pcr_authority','is_at_war = no',
                      'is_noble_family_title = no','has_variable = agot_title_blocked_to_give_away'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_old_panel_identity_is_rejected(self):
        for token in ('var:rw_pcr_serial = scope:rw_pcr_serial','var:rw_pcr_title = scope:rw_pcr_title',
                      'var:rw_pcr_former = scope:rw_pcr_former'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_consume_and_native_eligibility_before_world_action(self):
        for token in ('remove_variable = rw_pcr_execute_ticket','rw_nd_native_eligible_trigger = yes',
                      'clear_local_variable_list = target_titles','save_scope_as = recipient'):
            with self.subTest(token=token):self.assertTrue(self.errors(e=self.e.replace(token,'')))

    def test_consequences_without_verified_holder_are_rejected(self):
        self.assertTrue(self.errors(e=self.e.replace('limit = { scope:rw_pcr_title = { holder = scope:rw_pcr_former } }','limit = { always = yes }')))
        altered=self.e.replace('                    rw_nd_native_consequences_effect = yes','').replace('                create_title_and_vassal_change', '                rw_nd_native_consequences_effect = yes\n                create_title_and_vassal_change')
        self.assertIn('world action before consumption or consequences before verified transfer',self.errors(e=altered))

    def test_duplicate_native_effect_or_vassal_grab_is_rejected(self):
        self.assertTrue(self.errors(e=self.e+'\n bad = { is_ai = no }'))
        self.assertTrue(self.errors(e=self.e.replace('change_title_holder =','change_title_holder_include_vassals =')))
        self.assertTrue(self.errors(e=self.e.replace('resolve_title_and_vassal_change = scope:rw_pcr_change','resolve_title_and_vassal_change = scope:rw_pcr_change\n resolve_title_and_vassal_change = scope:rw_pcr_change')))

    def test_title_left_closes_both_pending_proof_and_restoration(self):
        for token in ('remove_variable = rw_pcr_gain_ticket','remove_variable = rw_pcr_restore_window','NOT = { holder = scope:previous_holder }'):
            with self.subTest(token=token):self.assertTrue(self.errors(e=self.e.replace(token,'')))

    def test_native_refusal_closes_only_unconfirmed_matching_cases(self):
        part=block(self.e,'rw_pcr_native_declined_effect')
        for token in ('has_variable = rw_pcr_gain_ticket','var:rw_pcr_former = scope:recipient',
                      'exists = scope:landed_title','var:rw_pcr_title = scope:landed_title','end_story = yes'):
            self.assertIn(token,part)
        self.assertNotIn('has_variable = rw_pcr_restore_window',part)

    def test_real_shared_entry_and_no_global_or_third_party_path(self):
        self.assertNotIn('is_ai =',clean_script(self.t+self.e+self.i+self.v)[0])
        self.assertNotIn('any_in_global_list',self.t+self.e)
        self.assertIn('every_owned_story',block(self.e,'rw_pcr_open_effect'))
        self.assertIn('rw_nd_adapter_available_trigger = yes',block(self.t,'rw_pcr_can_review_trigger'))

    def test_original_gain_and_decline_delegate_without_changing_canonical_facts(self):
        old=(MOD/'common/scripted_effects/rw_confiscation_transfer_effects.txt').read_text()
        gain=block(old,'rw_hcr_observe_gain_effect')
        self.assertLess(gain.index('remove_variable = rw_hcr_pending'),gain.index('rw_pcr_capture_gain_effect = yes'))
        self.assertLess(gain.index('rw_pcr_capture_gain_effect = yes'),gain.index('end_story = yes'))
        self.assertIn('rw_pcr_capture_primary_trigger = yes',block(old,'rw_hcr_register_request_effect'))
        self.assertIn('rw_pcr_native_declined_effect = yes',block(old,'rw_hcr_declined_effect'))
        wrapper=(MOD/'common/on_action/rw_title_provenance_on_actions.txt').read_text()
        self.assertIn('rw_on_title_revocation_context rw_on_pledged_title_gain_context rw_on_house_revocation_gain rw_on_post_confiscation_title_left',wrapper)
        self.assertNotRegex(self.e,r'\bname\s*=\s*(rw_tp_|rw_rs_|rw_rp_|rw_lr_|rw_ch_)')

    def test_localizations_are_original_bom_and_cover_all_display_keys(self):
        needed=set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_post_confiscation\.[\w.]+)',self.v))
        needed|={'rw_review_post_confiscation_return_interaction','rw_review_post_confiscation_return_interaction_desc'}
        for lang in ('english','french'):
            raw=(MOD/f'localization/{lang}/rw_post_confiscation_l_{lang}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            self.assertEqual(needed,set(re.findall(r'^\s+([\w.]+):0',raw.decode('utf-8-sig'),re.M)))
