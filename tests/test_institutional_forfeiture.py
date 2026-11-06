"""Source-level campaign invariants; no Python simulation of G3 or native AI."""
from pathlib import Path
import re
import unittest
from tools.validate_mod import clean_script
from tools import build_g3_native_confiscation as b
from test_native_house_confiscation import FIXTURE

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def block(s,name):
    clean = clean_script(s)[0]
    match = re.search(r'(?m)^'+re.escape(name)+r'\s*=\s*\{',clean)
    if not match: raise ValueError('Missing definition '+name)
    opening = clean.index('{',match.start());depth = 1
    for end in range(opening+1,len(clean)):
        depth += (clean[end]=='{')-(clean[end]=='}')
        if depth==0:return clean[match.start():end+1]
    raise ValueError('Unclosed definition '+name)


def errors(t,e,i,v,personal,priority,return_gate,house_effects):
    out=[]
    def need(s,tokens,label):
        if any(x not in s for x in tokens):out.append(label)
    order=block(t,'rw_hs_order_trigger')
    need(order,('rw_house_record_active_trigger = yes','var:rw_hs_schema = 1',
        'has_variable = rw_hs_armed','has_variable = rw_hs_epoch','has_variable = rw_hs_armed_on',
        'exists = var:rw_hs_armed_by','rw_house_sovereign_trigger = yes',
        'primary_title = scope:rw_hs_check.var:rw_house_authority',
        'government_has_flag = government_is_feudal','has_realm_law_flag = title_revocation_allowed',
        'NOT = { house = scope:rw_hs_check.var:rw_house_target }'), 'current institutional authority')
    if 'story_owner' in order:out.append('custody mistaken for authority')
    arm=block(t,'rw_hs_can_arm_trigger')
    need(arm,('rw_hc_adapter_available_trigger = yes','rw_hs_issuer_trigger = yes',
        'NOT = { house = scope:actor.house }','rw_hs_armable_pair_trigger = yes',
        'count >= 2 rw_hs_decree_pair_trigger = yes'), 'unauthorized/ambiguous arm')
    need(block(t,'rw_hs_issuer_trigger'),('rw_house_sovereign_trigger = yes',
        'government_has_flag = government_is_feudal','is_alive = yes exists = house'), 'issuer permission')
    candidate=block(t,'rw_hs_native_candidate_trigger')
    need(candidate,('rw_hc_adapter_available_trigger = yes','exists = scope:landed_title',
        'highest_held_title_tier >= tier_duchy','has_realm_law_flag = title_revocation_allowed',
        'liege = scope:actor exists = house','NOT = { house = scope:actor.house }',
        'holder = scope:recipient tier >= tier_county','is_noble_family_title = no',
        'is_landless_type_title = no','var:rw_house_target = scope:recipient.house',
        'var:rw_house_authority = scope:actor.top_liege.primary_title','rw_hs_order_trigger = yes',
        'var:rw_house_authority = { holder = { is_at_war = no } }'), 'current route-independent target')
    if candidate.count('is_at_war = no')!=3:out.append('war context')
    # No acquisition-origin branch: these current-title guards apply after all routes.
    if re.search(r'\b(scheme_owner|acquisition_type|inheritance_type|claim_cb|electors|nominate_heir)\b',candidate):out.append('route-specific bypass')
    need(block(personal,'rw_hc_native_candidate_trigger'),('rw_hc_personal_candidate_trigger = yes',
        'rw_hs_native_candidate_trigger = yes','OR ='), 'personal path or institutional path lost')
    value=block(priority,'rw_hc_native_priority_value')
    need(value,('value = 0','rw_hs_native_candidate_trigger = yes','add = 2500','else_if = {','rw_hc_personal_candidate_trigger = yes','add = 1500'), 'single conditional priority')
    if value.count('add = 1500')!=1 or value.count('add = 2500')!=1:out.append('double bonus')
    arm_effect=block(e,'rw_hs_arm_effect')
    need(arm_effect,('limit = { rw_hs_can_arm_trigger = yes }','rw_hs_armable_pair_trigger = yes',
        'name = rw_hs_epoch add = 1','name = rw_hs_armed value = flag:yes',
        'name = rw_hs_armed_by value = scope:actor','name = rw_hs_armed_on value = current_date'), 'unguarded arm')
    code=clean_script(t+e+i+v)[0]
    if re.search(r'\b(?:name|flag)\s*=\s*rw_house_(?:term|issued_on|retained)',code):out.append('original term renewed')
    disarm=block(e,'rw_hs_disarm_effect')
    need(disarm,('limit = { rw_hs_can_disarm_trigger = yes }','rw_hs_armed_pair_trigger = yes',
        'remove_variable = rw_hs_armed','name = rw_hs_epoch add = 1','rw_hc_withdraw_effect = yes'), 'disarm or stale panel')
    if 'rw_hc_adapter_available_trigger' in block(t,'rw_hs_can_disarm_trigger')+block(t,'rw_hs_issuer_trigger'):
        out.append('cannot withdraw without adapter')
    restore=block(t,'rw_hs_blocks_return_trigger')
    need(restore,('rw_house_record_active_trigger = yes','has_variable = rw_hs_armed',
        'var:rw_house_target = $HOUSE$','var:rw_house_authority = $AUTHORITY$',
        '$ISSUER$ = {','rw_hc_live_record_trigger = yes','var:rw_hc_house = $HOUSE$',
        'var:rw_hc_authority = $AUTHORITY$'), 'revoke/return loop')
    need(block(return_gate,'rw_pcr_capacity_trigger'),('rw_hs_blocks_return_trigger = {',
        'HOUSE = scope:rw_pcr_check.var:rw_pcr_house',
        'AUTHORITY = scope:rw_pcr_check.var:rw_pcr_authority',
        'ISSUER = scope:rw_pcr_check.var:rw_pcr_issuer'), 'return lost original case bindings')
    retirement=block(e,'rw_hs_close_personal_for_decree_effect')
    need(retirement,('rw_house_record_valid_trigger = yes','var:rw_hs_schema = 1 has_variable = rw_hs_armed',
        'var:rw_house_state = flag:restored','var:rw_house_state = flag:withdrawn',
        'story_type = story_rw_house_confiscation','var:rw_hc_schema = 1',
        'var:rw_hc_house = scope:rw_hs_closing.var:rw_house_target',
        'var:rw_hc_authority = scope:rw_hs_closing.var:rw_house_authority','remove_variable = rw_hc_live'), 'unrelated personal policy changed')
    need(block(house_effects,'rw_house_close_effect'),('rw_hs_close_personal_for_decree_effect = yes',), 'rehabilitation leaves campaign running')
    snapshot=block(e,'rw_hs_snapshot_effect')
    need(snapshot,('var:rw_house_target = { save_scope_as = rw_hs_house }',
        'var:rw_house_authority = { save_scope_as = rw_hs_authority }',
        'name = rw_hs_serial value = var:rw_house_serial','name = rw_hs_epoch value = var:rw_hs_epoch'), 'public snapshot identity')
    public=block(t,'rw_hs_public_pair_trigger')
    need(public,('var:rw_house_target = scope:recipient.house',
        'var:rw_house_authority = scope:actor.top_liege.primary_title',
        'scope:actor = { exists = house house = scope:recipient.house }'), 'public knowledge parity')
    need(block(t,'rw_hs_view_trigger'),('var:rw_house_serial = scope:rw_hs_serial',
        'var:rw_hs_epoch = scope:rw_hs_epoch'), 'stale public window')
    # Institutional state authorizes preference only. Native engine owns each act.
    if re.search(r'\b(is_ai|run_interaction|change_title_holder|create_title_and_vassal_change|add_revoke_title_reason|add_imprisonment_reason|add_trait|remove_trait|add_gold|use_hook|consume_revoke_title_reason|every_living_character)\s*=',code):
        out.append('native privilege or forced reversal')
    for secret in ('rw_house_basis_serial','rw_evidence_participant','rw_scheme_evidence_record','scheme_owner'):
        if secret in e+v:out.append('private grounds exported')
    for name,action in (('rw_arm_house_forfeiture_interaction','arm'),('rw_disarm_house_forfeiture_interaction','disarm')):
        part=block(i,name)
        need(part,(f'is_valid = {{ rw_hs_can_{action}_trigger = yes }}',
            f'on_accept = {{ rw_hs_{action}_effect = yes }}','ai_targets = { ai_recipients = vassals ai_recipients = courtiers }'), 'shared command')
    return out


class InstitutionalForfeitureTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_institutional_forfeiture_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_institutional_forfeiture_effects.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_institutional_forfeiture_interactions.txt').read_text()
        self.v=(MOD/'events/rw_institutional_forfeiture_events.txt').read_text()
        self.p=(MOD/'common/scripted_triggers/rw_house_confiscation_triggers.txt').read_text()
        self.val=(MOD/'common/script_values/rw_house_confiscation_values.txt').read_text()
        self.ret=(MOD/'common/scripted_triggers/rw_post_confiscation_triggers.txt').read_text()
        self.he=(MOD/'common/scripted_effects/rw_house_affair_effects.txt').read_text()
    def errors(self,t=None,e=None,p=None,val=None,ret=None,he=None):
        return errors(t or self.t,e or self.e,self.i,self.v,p or self.p,val or self.val,ret or self.ret,he or self.he)
    def test_complete_source_contract(self):self.assertEqual([],self.errors())

    def test_censure_or_issuer_death_alone_is_not_enforcement(self):
        for token in ('rw_house_record_active_trigger = yes','var:rw_hs_schema = 1','has_variable = rw_hs_armed'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))
        self.assertNotIn('story_owner',block(self.t,'rw_hs_order_trigger'))

    def test_current_crown_and_law_cannot_be_substituted(self):
        for token in ('primary_title = scope:rw_hs_check.var:rw_house_authority',
                      'rw_house_sovereign_trigger = yes','has_realm_law_flag = title_revocation_allowed',
                      'NOT = { house = scope:rw_hs_check.var:rw_house_target }'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_wrong_house_realm_holder_or_indirect_subject_is_rejected(self):
        for token in ('var:rw_house_target = scope:recipient.house',
                      'var:rw_house_authority = scope:actor.top_liege.primary_title',
                      'liege = scope:actor exists = house','holder = scope:recipient tier >= tier_county'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_each_native_liege_acts_only_with_own_rights_and_peace(self):
        for token in ('highest_held_title_tier >= tier_duchy','is_at_war = no',
                      'is_noble_family_title = no','is_landless_type_title = no'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))

    def test_no_route_specific_or_pretransfer_veto(self):
        candidate=block(self.t,'rw_hs_native_candidate_trigger')
        self.assertNotRegex(candidate,r'\b(granted|inherited|elected|conquered)\b')
        self.assertTrue(self.errors(e=self.e+'\n bad = { change_title_holder = root }'))
        self.assertTrue(self.errors(t=self.t.replace('holder = scope:recipient tier >= tier_county','holder = scope:actor tier >= tier_county')))

    def test_one_priority_preserves_personal_and_institutional_paths(self):
        for token in ('rw_hc_personal_candidate_trigger = yes','rw_hs_native_candidate_trigger = yes'):
            with self.subTest(token=token):self.assertTrue(self.errors(p=self.p.replace(token,'')))
        self.assertTrue(self.errors(val=self.val.replace('add = 1500','add = 1500 add = 1500')))

    def test_arm_requires_explicit_current_permission_and_unique_decree(self):
        for token in ('limit = { rw_hs_can_arm_trigger = yes }','name = rw_hs_armed_by value = scope:actor'):
            with self.subTest(token=token):self.assertTrue(self.errors(e=self.e.replace(token,'')))
        self.assertTrue(self.errors(t=self.t.replace('count >= 2 rw_hs_decree_pair_trigger = yes','always = no')))

    def test_fixed_original_term_never_restarts(self):
        self.assertTrue(self.errors(e=self.e+'\n bad = { set_variable = { name = rw_house_term value = flag:yes years = 50 } }'))
        original=(MOD/'common/scripted_effects/rw_house_affair_effects.txt').read_text()
        self.assertEqual(1,original.count('name = rw_house_term'))
        self.assertIn('name = rw_house_term value = flag:yes years = 50',original)

    def test_withdrawal_survives_missing_adapter_and_does_not_undo_world_state(self):
        self.assertNotIn('rw_hc_adapter_available_trigger',block(self.t,'rw_hs_can_disarm_trigger')+block(self.t,'rw_hs_issuer_trigger'))
        self.assertTrue(self.errors(e=self.e.replace('rw_hc_withdraw_effect = yes','')))
        for native in ('add_revoke_title_reason','add_gold','run_interaction','change_title_holder'):
            with self.subTest(native=native):self.assertTrue(self.errors(e=self.e+'\n bad = { '+native+' = root }'))

    def test_rehabilitation_stops_only_armed_same_crown_personal_intentions(self):
        for token in ('var:rw_hs_schema = 1 has_variable = rw_hs_armed',
                      'var:rw_house_state = flag:restored','var:rw_house_state = flag:withdrawn',
                      'var:rw_hc_authority = scope:rw_hs_closing.var:rw_house_authority'):
            with self.subTest(token=token):self.assertTrue(self.errors(e=self.e.replace(token,'')))
        self.assertTrue(self.errors(he=self.he.replace('rw_hs_close_personal_for_decree_effect = yes','')))

    def test_no_revoke_return_loop_or_macro_scope_rebinding(self):
        for token in ('rw_hc_live_record_trigger = yes','var:rw_hc_house = $HOUSE$',
                      'var:rw_house_authority = $AUTHORITY$'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))
        self.assertTrue(self.errors(ret=self.ret.replace('HOUSE = scope:rw_pcr_check.var:rw_pcr_house','HOUSE = var:rw_pcr_house')))

    def test_promised_native_gift_uses_same_campaign_stop_rule(self):
        text=(MOD/'common/scripted_triggers/rw_native_restitution_triggers.txt').read_text()
        domain=block(text,'rw_nd_domain_trigger')
        for token in ('rw_hs_blocks_return_trigger = {','HOUSE = scope:rw_rs_requester.house',
                      'AUTHORITY = scope:rw_rs_holder.primary_title','ISSUER = scope:rw_rs_holder'):
            self.assertIn(token,domain)

    def test_all_relevant_readers_share_public_information_only(self):
        for token in ('var:rw_house_authority = scope:actor.top_liege.primary_title',
                      'scope:actor = { exists = house house = scope:recipient.house }'):
            with self.subTest(token=token):self.assertTrue(self.errors(t=self.t.replace(token,'')))
        self.assertTrue(self.errors(e=self.e+'\n leaked = { value = rw_house_basis_serial }'))

    def test_old_windows_cannot_refer_to_rearmed_campaign(self):
        self.assertTrue(self.errors(t=self.t.replace('var:rw_hs_epoch = scope:rw_hs_epoch','always = yes')))
        self.assertTrue(self.errors(e=self.e.replace('name = rw_hs_epoch add = 1','name = rw_hs_epoch add = 0')))

    def test_custody_rehome_preserves_policy_and_permissions(self):
        for name in ('rw_house_rehome_effect','rw_house_owner_died_effect'):
            part=block(self.he,name)
            self.assertIn('make_story_owner',part)
            self.assertNotIn('rw_hs_armed',part)
            self.assertNotIn('rw_house_term',part)

    def test_private_native_definition_still_inverse_preserved(self):
        before,after=b.patch_native(FIXTURE.encode());restored=after
        for addition in b.INSERTIONS:restored=restored.replace(addition.encode(),b'',1)
        self.assertEqual(before,restored)
        self.assertEqual(4,len(b.INSERTIONS))

    def test_localization_covers_public_order_without_private_ground_fields(self):
        keys=set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_institutional_forfeiture\.[\w.]+)',self.v))
        for action in ('arm','disarm','read'):
            keys|={'rw_'+action+'_house_forfeiture_interaction','rw_'+action+'_house_forfeiture_interaction_desc'}
        for lang in ('english','french'):
            raw=(MOD/f'localization/{lang}/rw_institutional_forfeiture_l_{lang}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            text=raw.decode('utf-8-sig');self.assertEqual(keys,set(re.findall(r'^\s+([\w.]+):0',text,re.M)))
            self.assertNotRegex(text,r'\b(rw_house_basis|rw_evidence|rw_scheme_evidence)')
