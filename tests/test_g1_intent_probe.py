"""Private-builder fixtures and adversarial original-script checks; no CK3 run."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import build_g1_probe as builder
from test_build_g1_probe import SYNTHETIC
from test_native_scheme_evidence import block
from validate_mod import brace_errors, clean_script


def intent_errors(t,e):
    errors=[]
    def need(b,parts,msg):
        if any(x not in b for x in parts):errors.append(msg)
    need(block(t,'rw_g1p_ticket_trigger'),('exists = scope:rw_g1p_actor','exists = scope:rw_g1p_target',
        'exists = scope:rw_g1p_liege','exists = scope:rw_g1p_serial','this = scope:rw_g1p_actor',
        'var:rw_g1p_schema = 1','var:rw_g1p_owner = scope:rw_g1p_actor','var:rw_g1p_serial = scope:rw_g1p_serial',
        'var:rw_g1p_target = scope:rw_g1p_target','var:rw_g1p_liege = scope:rw_g1p_liege'),
        'stale actor target liege or serial')
    need(block(t,'rw_g1p_can_stage_trigger'),('NOT = { has_character_flag = rw_g1p_offer_window }',
        'NOT = { has_character_flag = rw_g1p_armed }','war_declarer_needs_hook_on_liege = yes'),
        'live context overwritten or legal route mislabeled')
    need(block(t,'rw_g1p_can_arm_trigger'),('rw_g1p_ticket_trigger = yes',
        'scope:actor = scope:rw_g1p_actor','scope:recipient = scope:rw_g1p_target',
        'liege = scope:rw_g1p_liege','var:rw_g1p_phase = flag:offered',
        'has_character_flag = rw_g1p_offer_window','NOT = { has_character_flag = rw_g1p_armed }',
        'war_declarer_needs_hook_on_liege = yes'), 'invalid stale or replayed confirmation')
    need(block(t,'rw_g1p_bound_context_trigger'),('exists = scope:actor exists = scope:recipient',
        'rw_g1p_peer_setup_trigger = { ACTOR = scope:actor TARGET = scope:recipient }',
        'var:rw_g1p_schema = 1','has_variable = rw_g1p_serial','has_character_flag = rw_g1p_armed',
        'var:rw_g1p_phase = flag:armed','var:rw_g1p_owner = scope:actor','var:rw_g1p_target = scope:recipient','var:rw_g1p_liege = scope:actor.liege'),
        'general target or liege bypass')
    peer=block(t,'rw_g1p_peer_setup_trigger')
    need(peer,('liege = $TARGET$.liege','NOT = { has_hook = $ACTOR$.liege }',
        'has_realm_law_flag = vassal_internal_wars_banned','has_realm_law_flag = vassal_all_wars_banned'),
        'unrelated realm hook or law context bypass')
    if peer.count('government_has_flag = government_is_feudal')!=2 or peer.count('is_at_war = no')!=2:
        errors.append('unrelated realm hook or law context bypass')
    observe=block(t,'rw_g1p_claim_observation_trigger')
    need(observe,('rw_g1p_native_context_trigger = yes','scope:war = { using_cb = claim_cb }',
        'has_character_flag = rw_g1p_armed','var:rw_g1p_phase = flag:armed','var:rw_g1p_owner = scope:attacker','var:rw_g1p_target = scope:defender',
        'var:rw_g1p_liege = scope:attacker.liege','liege = scope:defender.liege'),
        'wrong CB pair or declaration context observed')
    native=block(t,'rw_g1p_native_context_trigger')
    need(native,('exists = scope:war exists = scope:attacker exists = scope:defender',
        'this = scope:war.primary_attacker','this = scope:war.primary_defender'), 'secondary or missing native roles observed')
    stage=block(e,'rw_g1p_stage_effect')
    need(stage,('limit = { rw_g1p_can_stage_trigger = yes }','change_variable = { name = rw_g1p_serial_counter add = 1 }',
        'name = rw_g1p_owner value = scope:actor','name = rw_g1p_target value = scope:recipient','name = rw_g1p_liege value = scope:actor.liege',
        'flag = rw_g1p_offer_window days = 1','rw_g1p_snapshot_effect = yes'), 'bad staging identity or clocks')
    arm=block(e,'rw_g1p_arm_effect')
    need(arm,('limit = { rw_g1p_can_arm_trigger = yes }','remove_character_flag = rw_g1p_offer_window',
        'name = rw_g1p_phase value = flag:armed','flag = rw_g1p_armed days = 1'), 'confirmation arms wrong or lasting context')
    clear=block(e,'rw_g1p_clear_effect')
    need(clear,('remove_character_flag = rw_g1p_offer_window','remove_character_flag = rw_g1p_armed'), 'owner cleanup strands bypass')
    if 'scope:' in clear or 'rw_g1p_serial_counter' in clear:errors.append('cleanup depends on missing target or resets nonce')
    callback=block(e,'rw_g1p_observe_effect')
    need(callback,('limit = { rw_g1p_native_context_trigger = yes }','limit = { rw_g1p_claim_observation_trigger = yes }',
        'rw_g1p_clear_effect = { STATE = observed }','name = rw_g1p_last_serial value = var:rw_g1p_serial',
        'name = rw_g1p_last_target value = scope:defender','name = rw_g1p_last_observed_on value = current_date',
        'name = rw_g1p_last_kind value = flag:native_claim_cb_context'), 'missing consumed declaration observation')
    if not 0<=callback.find('rw_g1p_clear_effect = { STATE = observed }')<callback.find('name = rw_g1p_last_serial'):
        errors.append('observation before consumption')
    code=clean_script(e)[0]
    if re.search(r'\b(start_war|declare_war|end_war|add_gold|add_prestige|add_hook|remove_hook|add_opinion|add_claim|change_title_holder|run_interaction|add_realm_law|remove_realm_law|every_living_character|every_in_global_list)\s*=',code):
        errors.append('native war law cost hook or policy mutated')
    return errors


class G1IntentScriptTests(unittest.TestCase):
    def setUp(self):
        self.base=builder.TEMPLATE_ROOT
        self.t=(self.base/'common/scripted_triggers/rw_g1_intent_triggers.txt').read_text()
        self.e=(self.base/'common/scripted_effects/rw_g1_intent_effects.txt').read_text()
    def errors(self,t=None,e=None):return intent_errors(self.t if t is None else t,self.e if e is None else e)
    def test_source_contract(self):self.assertEqual([],self.errors())
    def test_immutable_ticket_guards_old_confirmations_and_cancellation(self):
        for g in ('var:rw_g1p_owner = scope:rw_g1p_actor','var:rw_g1p_serial = scope:rw_g1p_serial','var:rw_g1p_target = scope:rw_g1p_target','var:rw_g1p_liege = scope:rw_g1p_liege','this = scope:rw_g1p_actor'):
            self.assertIn('stale actor target liege or serial',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('rw_g1p_ticket_trigger = yes',block(self.t,'rw_g1p_can_cancel_trigger'))
    def test_only_fresh_confirmed_exact_pair_same_liege_receives_exemption(self):
        for g in ('var:rw_g1p_owner = scope:actor','has_character_flag = rw_g1p_armed','var:rw_g1p_target = scope:recipient','var:rw_g1p_liege = scope:actor.liege'):
            self.assertIn('general target or liege bypass',self.errors(t=self.t.replace(g,'always = yes')))
        for g in ('scope:actor = scope:rw_g1p_actor','has_character_flag = rw_g1p_offer_window','war_declarer_needs_hook_on_liege = yes'):
            self.assertIn('invalid stale or replayed confirmation',self.errors(t=self.t.replace(g,'always = yes')))
    def test_no_legal_hook_contract_or_general_nonfeudal_policy_change(self):
        self.assertIn('unrelated realm hook or law context bypass',self.errors(t=self.t.replace('NOT = { has_hook = $ACTOR$.liege }','always = yes')))
        self.assertIn('unrelated realm hook or law context bypass',self.errors(t=self.t.replace('government_has_flag = government_is_feudal','always = yes')))
        for key in ('rw_g1p_bound_context_trigger','rw_g1p_peer_setup_trigger'):
            self.assertNotIn(builder.HELPER,block(self.t,key))
    def test_staging_does_not_arm_and_only_confirmation_writes_one_day_window(self):
        self.assertNotIn('flag = rw_g1p_armed',block(self.e,'rw_g1p_stage_effect'))
        self.assertEqual(1,self.e.count('flag = rw_g1p_armed days = 1'))
        self.assertEqual(1,self.e.count('flag = rw_g1p_offer_window days = 1'))
        self.assertIn('confirmation arms wrong or lasting context',self.errors(e=self.e.replace('flag = rw_g1p_armed days = 1','flag = rw_g1p_armed days = 365')))
        for name in ('rw_g1p_read_effect','rw_g1p_snapshot_effect','rw_g1p_cancel_effect'):
            self.assertNotIn('add_character_flag',block(self.e,name))
    def test_native_claim_primary_roles_and_current_ban_required_for_fact_only(self):
        for g in ('var:rw_g1p_owner = scope:attacker','scope:war = { using_cb = claim_cb }','var:rw_g1p_target = scope:defender','var:rw_g1p_liege = scope:attacker.liege'):
            self.assertIn('wrong CB pair or declaration context observed',self.errors(t=self.t.replace(g,'always = yes')))
        self.assertIn('secondary or missing native roles observed',self.errors(t=self.t.replace('this = scope:war.primary_attacker','always = yes')))
        self.assertNotIn('is_at_war = no',block(self.t,'rw_g1p_claim_observation_trigger'))
    def test_callback_consumes_before_fact_other_wars_defender_clear_without_fact(self):
        self.assertIn('observation before consumption',self.errors(e=self.e.replace('rw_g1p_clear_effect = { STATE = observed }','removed')))
        callback=block(self.e,'rw_g1p_observe_effect')
        self.assertEqual(1,callback.count('name = rw_g1p_last_kind'))
        self.assertEqual(2,callback.count('rw_g1p_clear_effect = { STATE = cleared }'))
        self.assertNotRegex(callback,r'name\s*=\s*\w+\s+value\s*=\s*scope:war\b')
    def test_self_cleanup_is_available_after_role_or_reference_loss_and_serial_not_reset(self):
        self.assertNotIn('limit =',block(self.e,'rw_g1p_clear_effect'))
        i=(self.base/'common/character_interactions/rw_g1_intent_interactions.txt').read_text()
        cleanup=block(i,'rw_g1p_clear_interaction')
        self.assertIn('scope:actor = scope:recipient',cleanup)
        self.assertIn('scope:actor = { rw_g1p_clear_effect = { STATE = cleared } }',cleanup)
        self.assertNotIn('rw_g1p_peer_setup_trigger',cleanup)
    def test_no_direct_war_cost_law_hook_transfer_or_production_ai_policy(self):
        for cmd in ('start_war','declare_war','add_gold','remove_hook','add_realm_law','run_interaction'):
            self.assertIn('native war law cost hook or policy mutated',self.errors(e=self.e+'\n'+cmd+' = {}'))
        hooks=(self.base/'common/on_action/rw_g1_intent_on_actions.txt').read_text()
        self.assertEqual('on_actions = { rw_g1p_on_war_started }',block(hooks,'on_war_started').strip())
        self.assertNotRegex(self.t+self.e,r'\bis_ai\s*=')
        self.assertIn('ai_will_do = { base = 0 }',(self.base/'common/character_interactions/rw_g1_intent_interactions.txt').read_text())
    def test_original_templates_are_structural_localized_and_absent_from_base_mod(self):
        payload=builder.intent_payload();self.assertEqual(set(builder.TEMPLATE_FILES),set(payload))
        texts='\n'.join(b.decode('utf-8-sig') for n,b in payload.items() if n.endswith('.txt'))
        keys=set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_g1p\.[\w.]+)',texts))
        keys.update(('rw_g1p_stage_interaction','rw_g1p_stage_interaction_desc','rw_g1p_review_interaction','rw_g1p_review_interaction_desc','rw_g1p_clear_interaction','rw_g1p_clear_interaction_desc'))
        for lang in ('english','french'):
            s=payload[f'localization/{lang}/rw_g1_intent_l_{lang}.yml'].decode('utf-8-sig')
            actual=set(re.findall(r'^\s+([\w.]+):0',s,re.M));self.assertTrue(keys<=actual,keys-actual)
        self.assertFalse(any('g1_intent' in p.name for p in (builder.REPO/'mod').rglob('*')))


class G1IntentBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.agot=self.root/'agot';self.out=self.root/'private'
        self.source=self.agot/builder.SOURCE;self.source.parent.mkdir(parents=True);self.source.write_text(SYNTHETIC,encoding='utf-8-sig')
        self.claim=self.agot/builder.CLAIM_SOURCE;self.claim.parent.mkdir(parents=True);self.claim.write_text('claim_cb = { always = yes }\n')
        (self.agot/'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="1.19.0.6"\n')
        self.pins={builder.SOURCE.as_posix():hashlib.sha256(self.source.read_bytes()).hexdigest(),builder.CLAIM_SOURCE.as_posix():hashlib.sha256(self.claim.read_bytes()).hexdigest()}
    def build(self):
        # Synthetic inputs are explicitly substituted only in this fixture; no real CK3 claim.
        with patch.object(builder,'pinned_sources',return_value=self.pins):return builder.build(self.agot,self.out,target_bound_intent=True)
    def test_private_build_exact_native_helper_body_and_original_templates_only(self):
        before=self.source.read_bytes();self.build();mod=self.out/'rw_g1_intent_probe'
        head,body=builder.helper_block(SYNTHETIC)
        helper=(mod/'common/scripted_triggers/zz_rw_g1_probe.txt').read_text(encoding='utf-8-sig')
        self.assertEqual(head+builder.INTENT_GUARD+body+'\n',helper)
        self.assertEqual(before,self.source.read_bytes());self.assertEqual([],brace_errors(helper))
        for name,data in builder.intent_payload().items():self.assertEqual(data,(mod/name).read_bytes())
        receipt=json.loads((self.out/'receipt.json').read_text());self.assertEqual('target_bound_intent',receipt['mode'])
        self.assertEqual(2,len(receipt['input_sources']));self.assertNotIn(str(self.agot),json.dumps(receipt))
        self.assertFalse((self.out/'rw_g1_probe.mod').exists())
        self.assertIn('path="mod/rw_g1_intent_probe"',(self.out/'rw_g1_intent_probe.mod').read_text())
    def test_crlf_native_helper_body_preserved_as_exact_bytes(self):
        source=SYNTHETIC.replace('\n','\r\n').encode('utf-8')
        self.source.write_bytes(b'\xef\xbb\xbf'+source)
        self.pins[builder.SOURCE.as_posix()]=hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.build()
        head,body=builder.helper_block(source.decode('utf-8'))
        expected=b'\xef\xbb\xbf'+(head+builder.INTENT_GUARD+body+'\n').encode('utf-8')
        self.assertEqual(expected,(self.out/'rw_g1_intent_probe/common/scripted_triggers/zz_rw_g1_probe.txt').read_bytes())
        self.assertIn(b'\r\n',body.encode('utf-8'))
        self.assertNotIn(b'\r\r\n',expected)

    def test_unknown_helper_or_claim_hash_rejected_before_output(self):
        for path in (self.source,self.claim):
            original=path.read_bytes();path.write_bytes(original+b'\n# changed\n')
            with self.assertRaisesRegex(ValueError,'exact reviewed'):self.build()
            self.assertFalse(self.out.exists());path.write_bytes(original)
    def test_missing_claim_or_unknown_version_fail_closed(self):
        self.claim.unlink()
        with self.assertRaises(OSError):self.build()
        self.assertFalse(self.out.exists())
        self.claim.write_text('claim_cb = { always = yes }\n')
        (self.agot/'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="9.*"\n')
        with self.assertRaisesRegex(ValueError,'scoped'):self.build()
        self.assertFalse(self.out.exists())
    def test_corrupt_or_symlink_template_rejected_without_partial_private_output(self):
        clone=self.root/'templates';shutil.copytree(builder.TEMPLATE_ROOT,clone)
        victim=clone/builder.TEMPLATE_FILES[0];victim.write_text('bad = {')
        with patch.object(builder,'TEMPLATE_ROOT',clone):
            with self.assertRaisesRegex(ValueError,'template structure'):self.build()
        self.assertFalse(self.out.exists())
        victim.unlink()
        try:victim.symlink_to(builder.TEMPLATE_ROOT/builder.TEMPLATE_FILES[0])
        except (OSError,NotImplementedError):return
        with patch.object(builder,'TEMPLATE_ROOT',clone):
            with self.assertRaisesRegex(ValueError,'regular'):self.build()
        self.assertFalse(self.out.exists())
    def test_reviewed_pin_records_are_exact_hashes_without_proprietary_payload(self):
        pins=builder.pinned_sources();self.assertEqual({builder.SOURCE.as_posix(),builder.CLAIM_SOURCE.as_posix()},set(pins))
        for digest in pins.values():self.assertRegex(digest,r'^[a-f0-9]{64}$')
