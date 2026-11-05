"""Private native-AI byte preservation and CK3 policy source guards; no engine model."""
import hashlib
import json
import re
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools import build_g3_native_confiscation as b
from tools.build_g1_native_choice import bounds
from tools.validate_mod import clean_script

FIXTURE = '''synthetic_before = { ignored = yes }
revoke_title_interaction = {
    is_valid = { synthetic_native_right = yes }
    cost = { synthetic_native_cost = 7 }
    on_send = { original_native_send = yes }
    on_accept = { original_success = "é" }
    on_decline = { original_resistance = yes }
    ai_will_do = {
        base = -1000
        # base = 123 is just a comment
        modifier = { synthetic_bad_war = yes factor = 0 }
        modifier = { add = -5000 synthetic_friend = yes }
    }
}
synthetic_after = { ignored = yes }
'''


def block(text, name):
    a, _, e = bounds(text, name)
    return clean_script(text[a:e])[0]


def contract_errors(t, e, v, i, s):
    errors=[]
    def need(source, tokens, name):
        if any(not re.search(re.escape(x)+r'(?![\w:])',source) for x in tokens): errors.append(name)
    candidate=block(t,'rw_hc_native_candidate_trigger')
    need(candidate,('rw_hc_adapter_available_trigger = yes','exists = scope:landed_title',
         'holder = scope:recipient','tier >= tier_county','is_landless_type_title = no',
         'is_noble_family_title = no','liege = scope:actor','rw_hc_has_order_trigger = yes'), 'native context')
    order=block(t,'rw_hc_has_order_trigger')
    need(order,('rw_hc_live_record_trigger = yes','story_owner = scope:actor',
         'var:rw_hc_house = scope:recipient.house','any_owned_story ='), 'own exact house order')
    live=block(t,'rw_hc_live_record_trigger')
    need(live,('story_type = story_rw_house_confiscation','var:rw_hc_schema = 1',
         'has_variable = rw_hc_live','story_owner = var:rw_hc_issuer',
         'holder = scope:rw_hc_check.var:rw_hc_issuer'), 'identity/expiry/authority')
    need(block(t,'rw_hc_can_issue_trigger'),('NOT = { rw_hc_has_order_trigger = yes }',
         'liege = scope:actor','NOT = { house = scope:actor.house }'), 'duplicate/self order')
    need(block(e,'rw_hc_issue_effect'),('limit = { rw_hc_can_issue_trigger = yes }',
         'clear_saved_scope = rw_hc_new','story_owner = scope:actor',
         'NOT = { has_variable = rw_hc_schema }','name = rw_hc_live value = flag:yes days = 180',
         'name = rw_hc_house value = scope:recipient.house','name = rw_hc_authority value = scope:actor.primary_title'), 'fresh bounded issue')
    priority=block(v,'rw_hc_native_priority_value')
    need(priority,('value = 0','limit = { rw_hc_native_candidate_trigger = yes }','add = 1500'), 'zero outside order')
    need(s,('on_owner_death = { end_story = yes }','days = 30',
         'NOT = { rw_hc_live_record_trigger = yes }'), 'cleanup/inheritance')
    for name in ('rw_hc_issue_interaction','rw_hc_withdraw_interaction'):
        current=block(i,name)
        need(current,('on_accept = { rw_hc_'+('issue' if 'issue' in name else 'withdraw')+'_effect = yes }',
             'ai_targets = { ai_recipients = vassals }'), 'actual player/AI entry')
    # Original state is intention only. The unmodified native interaction executes.
    source=clean_script(t+e+v+i+s)[0]
    for operation in ('run_interaction','change_title_holder','resolve_title_and_vassal_change',
                      'add_trait','remove_trait','add_imprisonment_reason','add_revoke_title_reason',
                      'use_hook','add_gold','add_prestige','make_story_owner','every_living_character',
                      'every_in_global_list'):
        if operation+' =' in source: errors.append('direct effect or global scan: '+operation)
    if 'is_ai' in source: errors.append('shared execution excludes an actor')
    return errors


class NativeConfiscationSourceTests(unittest.TestCase):
    def setUp(self):
        self.t=(b.TEMPLATES/'common/scripted_triggers/rw_house_confiscation_triggers.txt').read_text();self.e=(b.TEMPLATES/'common/scripted_effects/rw_house_confiscation_effects.txt').read_text()
        self.v=(b.TEMPLATES/'common/script_values/rw_house_confiscation_values.txt').read_text();self.i=(b.TEMPLATES/'common/character_interactions/rw_house_confiscation_interactions.txt').read_text()
        self.s=(b.TEMPLATES/'common/story_cycles/rw_house_confiscation.txt').read_text()

    def test_current_runtime_contract(self):
        self.assertEqual([],contract_errors(self.t,self.e,self.v,self.i,self.s))
        self.assertIn('rw_hc_adapter_available_trigger = { always = no }',self.t)

    def test_wrong_title_owner_house_or_context_rejected(self):
        for old,new in [('holder = scope:recipient','holder = scope:actor'),
                        ('var:rw_hc_house = scope:recipient.house','exists = var:rw_hc_house'),
                        ('story_owner = scope:actor','always = yes'),
                        ('liege = scope:actor','exists = liege'),
                        ('exists = scope:landed_title','always = yes')]:
            with self.subTest(old=old): self.assertTrue(contract_errors(self.t.replace(old,new),self.e,self.v,self.i,self.s))

    def test_expired_successor_or_duplicate_order_rejected(self):
        for old,new in [('has_variable = rw_hc_live','always = yes'),
                        ('holder = scope:rw_hc_check.var:rw_hc_issuer','exists = holder'),
                        ('NOT = { rw_hc_has_order_trigger = yes }','always = yes')]:
            with self.subTest(old=old): self.assertTrue(contract_errors(self.t.replace(old,new),self.e,self.v,self.i,self.s))

    def test_zero_priority_without_adapter_or_matching_intention(self):
        self.assertTrue(contract_errors(self.t,self.e,self.v.replace('value = 0','value = 1500'),self.i,self.s))
        self.assertTrue(contract_errors(self.t.replace('rw_hc_adapter_available_trigger = yes','always = yes'),self.e,self.v,self.i,self.s))
        self.assertNotIn('rw_house_censured',self.t+self.v)

    def test_no_auto_renewal_or_stale_new_story(self):
        for old,new in [('days = 180','days = 1800'),('clear_saved_scope = rw_hc_new',''),
                        ('NOT = { has_variable = rw_hc_schema }','always = yes')]:
            with self.subTest(old=old): self.assertTrue(contract_errors(self.t,self.e.replace(old,new),self.v,self.i,self.s))
        self.assertEqual(1,self.e.count('name = rw_hc_live'))

    def test_withdrawal_does_not_restore_or_charge(self):
        current=block(self.e,'rw_hc_withdraw_effect')
        self.assertIn('limit = { rw_hc_has_order_trigger = yes }',current)
        self.assertIn('remove_variable = rw_hc_live',current)
        self.assertIn('end_story = yes',current)
        self.assertNotIn('set_variable',current)
        self.assertNotIn('cost =',self.i)

    def test_ai_policy_changes_decisions_not_eligibility(self):
        start=block(self.i,'rw_hc_issue_interaction')
        self.assertIn('has_revoke_title_reason = scope:recipient',start)
        self.assertIn('opinion = { target = scope:recipient value <= -25 }',start)
        self.assertIn('gold >= 150',start)
        self.assertIn('ai_frequency = 6',start)
        for token in ('has_revoke_title_reason','opinion','gold'):
            self.assertNotIn(token,block(self.t,'rw_hc_can_issue_trigger'))

    def test_native_mutations_and_human_only_rules_rejected(self):
        for addition in ('change_title_holder = {}','run_interaction = {}','add_revoke_title_reason = yes','is_ai = no'):
            with self.subTest(addition=addition): self.assertTrue(contract_errors(self.t,self.e+'\n bad = { '+addition+' }',self.v,self.i,self.s))

    def test_public_source_has_no_native_definition(self):
        self.assertFalse((b.TEMPLATES/'common/character_interactions/zz_rw_native_confiscation.txt').exists())
        for path in b.TEMPLATES.rglob('*.txt'):
            self.assertNotIn('revoke_title_interaction = {',path.read_text(encoding='utf-8-sig'))


class NativeConfiscationBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='rw-hc-tests-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.agot=self.root/'synthetic AGOT';self.agot.mkdir()
        (self.agot/'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="1.19.0.6"\n')
        self.raw=FIXTURE.encode();self.path=self.agot/b.INPUT;self.path.parent.mkdir(parents=True);self.path.write_bytes(self.raw)
        self.out=self.root/'private'

    def build(self):
        with patch.object(b,'pin',return_value=hashlib.sha256(self.raw).hexdigest()):return b.build(self.agot,self.out)

    def test_three_insertions_preserve_every_native_byte_and_zero_factor(self):
        for newline in ('\n','\r\n'):
            original,patched=b.patch_native(b'\xef\xbb\xbf'+FIXTURE.replace('\n',newline).encode())
            restored=patched
            for addition in b.INSERTIONS: restored=restored.replace(addition.encode(),b'',1)
            self.assertEqual(original,restored)
            self.assertEqual(1,patched.count(b.PREFIX.encode()))
            self.assertLess(patched.index(b.PREFIX.encode()),patched.index(b'synthetic_bad_war'))
            self.assertIn(b'factor = 0',patched)
            self.assertNotIn(b'synthetic_before',patched)
            self.assertNotIn(b'synthetic_after',patched)

    def test_manifest_original_runtime_and_no_installed_writes(self):
        r=self.build()
        self.assertEqual(len(b.FILES),len(r['runtime_sources']));self.assertEqual(2,len(r['outputs']))
        self.assertEqual(self.raw,self.path.read_bytes())
        for row in r['outputs']:
            self.assertEqual(row['sha256'],hashlib.sha256((self.out/b.MOD_ID/row['path']).read_bytes()).hexdigest())
        for row in r['runtime_sources']:
            self.assertFalse((self.out/b.MOD_ID/row['path']).exists())
        self.assertNotIn(str(self.agot),json.dumps(r))
        self.assertIn('dependencies={ "Real Westeros" }',(self.out/b.MOD_ID/'descriptor.mod').read_text())

    def test_changed_missing_duplicate_or_nested_native_block_refused(self):
        for changed in (FIXTURE.replace('base = -1000','base = 0'),
                        FIXTURE.replace('ai_will_do','other_value'),
                        FIXTURE+FIXTURE,'wrapper = { '+FIXTURE+' }',FIXTURE[:-10]):
            with self.subTest(changed=changed[:20]),self.assertRaises(ValueError):b.patch_native(changed.encode())

    def test_prepatched_native_definition_refused(self):
        _,patched=b.patch_native(self.raw)
        with self.assertRaises(ValueError):b.patch_native(patched)

    def test_modified_native_hash_and_metadata_fail_before_output(self):
        self.path.write_bytes(self.raw+b' changed')
        with self.assertRaises(ValueError):self.build()
        self.assertFalse(self.out.exists());self.path.write_bytes(self.raw)
        (self.agot/'descriptor.mod').write_text('version="0.5.2.2"\nsupported_version="1.19.0.6"\n')
        with self.assertRaises(ValueError):self.build()
        self.assertFalse(self.out.exists())

    def test_existing_or_internal_output_refused(self):
        self.out.mkdir();(self.out/'keep').write_text('keep')
        with self.assertRaises(ValueError):self.build()
        self.assertEqual('keep',(self.out/'keep').read_text())
        for out in (self.agot/'private',b.REPO/'private-forbidden',self.root):
            with self.assertRaises(ValueError):b.build(self.agot,out)

    def test_symlink_native_or_descriptor_refused(self):
        for path in (self.path,self.agot/'descriptor.mod'):
            original=path.read_bytes();other=self.root/'outside';other.write_bytes(original);path.unlink();path.symlink_to(other)
            with self.assertRaises(ValueError):self.build()
            self.assertFalse(self.out.exists());path.unlink();path.write_bytes(original)

    def test_corrupt_runtime_fails_before_output(self):
        with patch.object(b,'templates',side_effect=ValueError('invalid runtime')):
            with self.assertRaises(ValueError):self.build()
        self.assertFalse(self.out.exists())

    def test_localizations_and_source_receipt(self):
        self.assertEqual(len(b.FILES),len(b.templates()))
        self.assertEqual(64,len(b.pin()))
        for lang in ('english','french'):
            p=b.TEMPLATES/f'localization/{lang}/rw_house_confiscation_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            self.assertIn('rw_hc_withdraw_interaction_desc:0',p.read_text(encoding='utf-8-sig'))


if __name__=='__main__':unittest.main()
