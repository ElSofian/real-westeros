"""Adversarial source checks; no CK3 callback, knowledge or transfer simulation."""
from pathlib import Path
import json
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mod/real_westeros'
FIELDS=('kind','request_serial','pledge_revision','pledge_days','title','former_holder','new_holder','observed_on')


def observation_errors(t,e,on,wrapper):
    out=[]
    if block(wrapper,'on_title_gain').strip()!='on_actions = { rw_on_title_revocation_context rw_on_pledged_title_gain_context }':
        out.append('native dispatcher replaced or original child lost')
    child=block(on,'rw_on_pledged_title_gain_context')
    for g in ('trigger = { rw_rg_native_context_trigger = yes }','effect = { rw_rg_observe_effect = yes }'):
        if g not in child:out.append('native callback guard bypass')
    native=block(t,'rw_rg_native_context_trigger')
    for g in ('is_alive = yes','has_variable = rw_rs_counter','exists = scope:title','exists = scope:previous_holder',
              'NOT = { this = scope:previous_holder }','scope:previous_holder = { is_alive = yes }',
              'holder = root','tier >= tier_county','is_noble_family_title = no','is_landless_type_title = no'):
        if g not in native:out.append('wrong or missing native title context')
    match='rw_rg_candidate_trigger = { RECEIVER = root GIVER = scope:previous_holder TITLE = scope:title }'
    if native.count(match)!=2 or 'count > 1' not in native or 'NOT = { has_variable = rw_rg_schema }' not in native:
        out.append('ambiguous or repeated transfer attached')
    candidate=block(t,'rw_rg_candidate_trigger')
    for g in ('rw_rs_record_valid_trigger = yes','has_variable = rw_rs_retained','story_owner = $RECEIVER$',
              'var:rw_rs_requester = $RECEIVER$','var:rw_rs_holder = $GIVER$','var:rw_rs_title = $TITLE$',
              'var:rw_rp_schema = 1','has_variable = rw_rp_proposed_on','has_variable = rw_rp_accepted_on',
              'has_variable = rw_rp_revision','var:rw_rp_days = 14','var:rw_rp_days = 30',
              'var:rw_rp_state = flag:promised','has_variable = rw_rp_due'):
        if g not in candidate:out.append('foreign expired unaccepted or malformed promise matched')
    observe=block(e,'rw_rg_observe_effect')
    for g in ('limit = { rw_rg_native_context_trigger = yes }','save_scope_as = rw_rg_receiver',
              'scope:previous_holder = { save_scope_as = rw_rg_giver }','scope:title = { save_scope_as = rw_rg_title }',
              'every_owned_story','rw_rg_candidate_trigger = { RECEIVER = scope:rw_rg_receiver GIVER = scope:rw_rg_giver TITLE = scope:rw_rg_title }',
              'NOT = { has_variable = rw_rg_schema }'):
        if g not in observe:out.append('unguarded or wrong-root observation write')
    stamp=observe.find('name = rw_rg_schema value = 1')
    for field in FIELDS:
        if not 0 <= observe.find('name = rw_rg_'+field+' value = ') < stamp:
            out.append('incomplete fact certified before write')
    view=block(t,'rw_rg_view_trigger')
    for g in ('rw_rp_view_trigger = yes','var:rw_rg_schema = 1','var:rw_rg_kind = flag:native_title_gain_context',
              'has_variable = rw_rg_observed_on','var:rw_rg_request_serial = scope:rw_rs_serial',
              'var:rw_rg_pledge_revision = scope:rw_rp_revision','var:rw_rg_pledge_days = scope:rw_rp_days',
              'var:rw_rg_title = scope:rw_rs_title','var:rw_rg_former_holder = scope:rw_rs_holder',
              'var:rw_rg_new_holder = scope:rw_rs_requester'):
        if g not in view:out.append('foreign or stale private fact displayed')
    code=clean_script(e)[0]
    if re.search(r'\b(?:name|flag)\s*=\s*rw_(?!rg_)\w+',code):out.append('observation changes promise or original history')
    if re.search(r'\b(add_gold|add_prestige|add_opinion|run_interaction|send_interaction|open_interaction_window|change_title_holder|create_title_and_vassal_change|resolve_title_and_vassal_change|create_story|end_story|make_story_owner|trigger_event|remove_variable|change_variable|add_character_flag|remove_character_flag|every_living_character|any_in_global_list|every_in_global_list|add_to_global_variable_list)\s*=',code):
        out.append('native effect replay reward notification or global scan')
    if re.search(r'\b(?:name|flag)\s*=\s*rw_rg_(?:fulfilled|voluntary_grant|caused_by_promise|paid)\b',code):
        out.append('acquisition context promoted to compliance or causation')
    return out


class PledgedTitleObservationTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_restitution_transfer_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_restitution_transfer_effects.txt').read_text()
        self.on=(MOD/'common/on_action/rw_pledged_title_gain_on_actions.txt').read_text()
        self.w=(MOD/'common/on_action/rw_title_provenance_on_actions.txt').read_text()

    def errors(self,t=None,e=None,on=None,w=None):
        return observation_errors(self.t if t is None else t,self.e if e is None else e,
                                  self.on if on is None else on,self.w if w is None else w)

    def test_contract(self):
        self.assertEqual([],self.errors())

    def test_additive_dispatch_preserves_original_guard_and_native_callback(self):
        for s in ('rw_on_title_revocation_context ',' rw_on_pledged_title_gain_context'):
            self.assertIn('native dispatcher replaced or original child lost',self.errors(w=self.w.replace(s,'')))
        self.assertIn('native dispatcher replaced or original child lost',self.errors(w=self.w.replace('on_title_gain = {','on_title_gain = { effect = {}')))
        for g in ('rw_rg_native_context_trigger = yes','rw_rg_observe_effect = yes'):
            self.assertIn('native callback guard bypass',self.errors(on=self.on.replace(g,'always = yes')))
        original=block(self.w,'rw_on_title_revocation_context')
        self.assertIn('trigger = { rw_tp_native_context_trigger = yes }',original)
        self.assertIn('effect = { rw_tp_observe_effect = yes }',original)

    def test_missing_wrong_dead_or_nonordinary_native_context_fails_closed(self):
        for g in ('has_variable = rw_rs_counter','exists = scope:title','exists = scope:previous_holder',
                  'NOT = { this = scope:previous_holder }','scope:previous_holder = { is_alive = yes }',
                  'holder = root','tier >= tier_county','is_noble_family_title = no','is_landless_type_title = no'):
            self.assertIn('wrong or missing native title context',self.errors(t=self.t.replace(g,'always = yes')))
        native=block(self.t,'rw_rg_native_context_trigger')
        self.assertLess(native.index('has_variable = rw_rs_counter'),native.index('any_owned_story'))
        self.assertNotRegex(native,r'\b(scope:actor|scope:recipient|scope:landed_title|scope:revoke_title_interaction)\b')

    def test_ambiguous_and_duplicate_callbacks_never_select_or_refresh(self):
        for g in ('count > 1','NOT = { has_variable = rw_rg_schema }'):
            self.assertIn('ambiguous or repeated transfer attached',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertNotRegex(self.e,r'\b(random_owned_story|ordered_owned_story|remove_variable|change_variable)\s*=')
        self.assertEqual(1,len(re.findall(r'\bname\s*=\s*rw_rg_observed_on\b',self.e)))
        # Count candidates regardless of an earlier note, so an observed rival cannot mask ambiguity.
        native=block(self.t,'rw_rg_native_context_trigger')
        uniqueness=native[native.index('count > 1'):]
        self.assertNotIn('has_variable = rw_rg_schema',uniqueness)

    def test_exact_retained_story_parties_title_and_live_accepted_terms_required(self):
        for g in ('rw_rs_record_valid_trigger = yes','has_variable = rw_rs_retained','story_owner = $RECEIVER$',
                  'var:rw_rs_requester = $RECEIVER$','var:rw_rs_holder = $GIVER$','var:rw_rs_title = $TITLE$',
                  'var:rw_rp_schema = 1','has_variable = rw_rp_accepted_on','has_variable = rw_rp_revision',
                  'var:rw_rp_state = flag:promised','has_variable = rw_rp_due'):
            self.assertIn('foreign expired unaccepted or malformed promise matched',self.errors(t=self.t.replace(g,'always = yes')))
        candidate=block(self.t,'rw_rg_candidate_trigger')
        self.assertNotRegex(candidate,r'\b(house_head|top_liege|rw_rs_current_context_trigger|rw_lr_record_valid_trigger)\b')

    def test_effect_rechecks_native_context_and_explicit_aliases_inside_story_iteration(self):
        for g in ('limit = { rw_rg_native_context_trigger = yes }','save_scope_as = rw_rg_receiver',
                  'scope:previous_holder = { save_scope_as = rw_rg_giver }',
                  'rw_rg_candidate_trigger = { RECEIVER = scope:rw_rg_receiver GIVER = scope:rw_rg_giver TITLE = scope:rw_rg_title }'):
            self.assertIn('unguarded or wrong-root observation write',self.errors(e=self.e.replace(g,'always = yes')))
        self.assertNotIn('RECEIVER = root',self.e)
        self.assertNotIn('rw_rp_view_trigger',self.e)

    def test_complete_first_fact_payload_written_before_schema_stamp(self):
        for field in FIELDS:
            self.assertIn('incomplete fact certified before write',self.errors(e=self.e.replace('name = rw_rg_'+field,'name = removed_'+field)))
        for pair in ('request_serial value = var:rw_rs_serial','pledge_revision value = var:rw_rp_revision',
                     'pledge_days value = var:rw_rp_days','title value = scope:rw_rg_title',
                     'former_holder value = scope:rw_rg_giver','new_holder value = scope:rw_rg_receiver',
                     'observed_on value = current_date','kind value = flag:native_title_gain_context'):
            self.assertIn('name = rw_rg_'+pair,self.e)

    def test_private_view_binds_exact_request_pledge_version_and_directed_transfer(self):
        for g in ('rw_rp_view_trigger = yes','var:rw_rg_schema = 1','has_variable = rw_rg_observed_on',
                  'var:rw_rg_request_serial = scope:rw_rs_serial','var:rw_rg_pledge_revision = scope:rw_rp_revision',
                  'var:rw_rg_pledge_days = scope:rw_rp_days','var:rw_rg_title = scope:rw_rs_title',
                  'var:rw_rg_former_holder = scope:rw_rs_holder','var:rw_rg_new_holder = scope:rw_rs_requester'):
            self.assertIn('foreign or stale private fact displayed',self.errors(t=self.t.replace(g,'always = yes')))
        # Historic facts survive later ownership changes while the original private record survives.
        view=block(self.t,'rw_rg_view_trigger')
        self.assertNotRegex(view,r'(?<![\w:])holder\s*=\s*scope:rw_rs_requester\b')
        self.assertNotIn('rw_rg_native_context_trigger',view)
        self.assertNotIn('rw_rp_due',view)

    def test_observation_never_changes_consent_deadlines_reactions_or_retention(self):
        for var in ('rw_rp_state','rw_rp_due','rw_rp_accepted_on','rw_rs_retained','rw_rs_state','rw_rp_response_done'):
            self.assertIn('observation changes promise or original history',self.errors(e=self.e+f'\nset_variable = {{ name = {var} value = flag:acknowledged }}'))
        for var in ('fulfilled','voluntary_grant','caused_by_promise','paid'):
            self.assertIn('acquisition context promoted to compliance or causation',self.errors(e=self.e+f'\nset_variable = {{ name = rw_rg_{var} value = flag:yes }}'))

    def test_no_native_effect_payment_notification_backfill_or_global_scan(self):
        for command in ('add_gold = 50','add_opinion = {}','change_title_holder = root','trigger_event = {}',
                        'create_story = {}','every_in_global_list = {}','every_living_character = {}'):
            self.assertIn('native effect replay reward notification or global scan',self.errors(e=self.e+'\n'+command))
        all_code='\n'.join(clean_script(p.read_text())[0] for p in MOD.rglob('*.txt'))
        self.assertEqual(1,len(re.findall(r'\brw_rg_observe_effect\s*=\s*yes',all_code)))
        for field in (*FIELDS,'schema'):
            self.assertEqual(1,len(re.findall(r'\bname\s*=\s*rw_rg_'+field+r'\b',all_code)))
        self.assertNotIn('rw_rg_', (MOD/'common/scripted_effects/rw_land_register_effects.txt').read_text())

    def test_missing_note_does_not_block_beneficiary_statement_or_native_grant(self):
        pledge=(MOD/'common/scripted_triggers/rw_restitution_pledge_triggers.txt').read_text()
        for name in ('rw_rp_can_acknowledge_trigger','rw_rp_can_open_grant_trigger','rw_rp_can_release_trigger','rw_rp_can_react_trigger'):
            self.assertNotIn('rw_rg_',block(pledge,name))
        e=(MOD/'common/scripted_effects/rw_restitution_pledge_effects.txt').read_text()
        self.assertNotIn('rw_rg_',e)
        v=(MOD/'events/rw_restitution_pledge_events.txt').read_text()
        self.assertIn('trigger = { rw_rg_view_trigger = yes } desc = rw_restitution_transfer.observed',v)
        self.assertIn('trigger = { NOT = { rw_rg_view_trigger = yes } } desc = rw_restitution_transfer.unobserved',v)

    def test_no_ai_exception_and_private_existing_lifecycle_is_unchanged(self):
        self.assertNotRegex(clean_script(self.t+self.e)[0],r'\b(is_ai|create_story|make_story_owner|end_story|effect_group)\s*=')
        story=(MOD/'common/story_cycles/rw_restitution_requests.txt').read_text()
        self.assertIn('on_owner_death = { rw_rs_retire_effect = yes }',story)
        self.assertIn('days = 60',story)
        self.assertNotIn('rw_rg_',story)

    def test_hash_only_source_receipt_and_marker_positions_are_complete(self):
        receipt=json.loads((ROOT/'docs/RESTITUTION_TRANSFER_SOURCE_RECEIPT.json').read_text())
        self.assertEqual(3,len(receipt['reviewed_references']))
        for ref in receipt['reviewed_references']:
            self.assertRegex(ref['sha256'],r'^[0-9a-f]{64}$')
            self.assertGreater(ref['size'],0)
            self.assertFalse(Path(ref['path']).is_absolute())
            self.assertNotIn('..',Path(ref['path']).parts)
            self.assertTrue(ref['markers'])
            self.assertTrue(all(all(n>0 for n in rows) for rows in ref['markers'].values()))
            self.assertEqual({'source','path','sha256','size','markers'},set(ref))

    def test_localized_observation_and_missing_evidence_boundaries(self):
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_restitution_transfer_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            keys=set(re.findall(r'^\s+([\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertEqual({'rw_restitution_transfer.observed','rw_restitution_transfer.unobserved'},keys)
