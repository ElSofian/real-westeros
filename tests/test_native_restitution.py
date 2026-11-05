"""Adversarial source/backend contracts; no claim to simulate CK3 transfers."""
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from tools import build_native_restitution as b
from tools.build_g1_native_choice import bounds
from tools.validate_mod import clean_script

FIXTURE = b'''grant_titles_interaction = {
 auto_accept = yes
 is_shown = { synthetic_species = yes }
 is_valid_showing_failures_only = { synthetic_right = yes }
 can_be_picked_title = { synthetic_title = yes }
 can_send = { synthetic_diarch = yes }
 on_accept = { synthetic_native_consequence = "original" }
 on_auto_accept = { synthetic_notice = yes }
}
'''
MOD=b.TEMPLATES


def block(s, name):
    a, _, c=bounds(s, name)
    return clean_script(s[a:c])[0]


def errors(t, e, v):
    out=[]
    def require(s, tokens, message):
        if any(x not in s for x in tokens): out.append(message)
    domain=block(t, 'rw_nd_domain_trigger')
    require(domain, ('rw_rp_pending_trigger = yes', 'this = scope:rw_rs_holder',
        'rw_rp_parties_trigger = yes', 'is_independent_ruler = yes',
        'highest_held_title_tier >= tier_kingdom', 'liege = scope:rw_rs_holder',
        'highest_held_title_tier = tier_county', 'holder = scope:rw_rs_holder',
        'tier = tier_duchy', 'is_landless_type_title = no', 'is_noble_family_title = no',
        'is_head_of_faith = no', 'is_leased_out = no',
        'NOT = { has_partition_succession_realm_law_trigger = yes }',
        'NOT = { this = scope:rw_rs_holder.player_heir }',
        'NOT = { has_variable = agot_title_blocked_to_give_away }'), 'unsafe transfer domain')
    if domain.count('has_active_diarchy = no') != 2 or domain.count('is_at_war = no') != 2:
        out.append('changed capacity')
    require(block(t,'rw_nd_can_deliver_trigger'), ('rw_nd_adapter_available_trigger = yes',
        'rw_nd_domain_trigger = yes', 'NOT = { has_variable = rw_nd_attempt }'), 'admission replay')
    require(block(t,'rw_nd_queued_trigger'), ('rw_nd_adapter_available_trigger = yes',
        'rw_nd_domain_trigger = yes', 'var:rw_nd_attempt = scope:rw_rp_revision',
        'var:rw_nd_result = flag:pending', 'has_variable = rw_nd_ticket'), 'stale callback')
    require(block(e,'rw_nd_queue_effect'), ('limit = { rw_nd_can_deliver_trigger = yes }',
        'name = rw_nd_attempt value = scope:rw_rp_revision',
        'name = rw_nd_ticket value = flag:yes days = 2',
        'id = rw_native_restitution.0001 days = 1'), 'unconsumed decision')
    run=block(e,'rw_nd_execute_effect')
    require(run, ('rw_rp_view_trigger = yes this = scope:rw_rs_holder',
        'var:rw_nd_attempt = scope:rw_rp_revision', 'has_variable = rw_nd_ticket',
        'limit = { rw_nd_queued_trigger = yes }', 'clear_local_variable_list = target_titles',
        'clear_local_variable_list = titles_to_grant',
        'clear_saved_scope = recipient_is_independent',
        'save_scope_as = actor', 'save_scope_as = recipient', 'save_scope_as = target',
        'save_scope_as = landed_title', 'save_scope_as = dummy_gender',
        'add_to_temporary_list = target_titles',
        'limit = { rw_nd_native_eligible_trigger = yes }'), 'unguarded backend')
    ordered=('rw_nd_native_eligible_trigger = yes', 'remove_variable = rw_nd_ticket',
        'create_title_and_vassal_change', 'change_title_holder',
        'resolve_title_and_vassal_change',
        'limit = { scope:rw_rs_title = { holder = scope:rw_rs_requester } }',
        'name = rw_nd_result value = flag:transferred',
        'rw_nd_native_consequences_effect = yes', 'rw_nd_native_notification_effect = yes')
    at=[run.find(x) for x in ordered]
    if min(at)<0 or at!=sorted(at):out.append('execution before consumption or consequences without transfer')
    for command in ('create_title_and_vassal_change','change_title_holder','resolve_title_and_vassal_change',
                    'rw_nd_native_consequences_effect','rw_nd_native_notification_effect'):
        if len(re.findall(r'\b'+command+r'\s*=',run))!=1:out.append('duplicate native action')
    require(run, ('type = granted','holder = scope:rw_rs_requester',
        'change = scope:rw_nd_change','take_baronies = no'), 'changed world target')
    source=clean_script(t+e+v)[0]
    if re.search(r'\b(is_ai|change_title_holder_include_vassals|run_interaction|add_gold|add_claim|add_trait|every_living_character)\s*=',source):
        out.append('unequal or unrelated effect')
    return out


class RestitutionSourceTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_native_restitution_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_native_restitution_effects.txt').read_text()
        self.v=(MOD/'events/rw_native_restitution_events.txt').read_text()

    def test_current_contract(self):
        self.assertEqual([],errors(self.t,self.e,self.v))

    def test_no_adapter_no_action(self):
        self.assertIn('always = no',block(self.t,'rw_nd_adapter_available_trigger'))
        self.assertIn('always = no',block(self.t,'rw_nd_native_eligible_trigger'))
        self.assertEqual('rw_nd_native_consequences_effect = { }',block(self.e,'rw_nd_native_consequences_effect').strip())

    def test_domain_mutations_rejected(self):
        for token in ('rw_rp_pending_trigger = yes','holder = scope:rw_rs_holder',
                      'liege = scope:rw_rs_holder','tier = tier_duchy',
                      'is_noble_family_title = no','has_active_diarchy = no',
                      'NOT = { has_partition_succession_realm_law_trigger = yes }'):
            with self.subTest(token=token):
                self.assertTrue(errors(self.t.replace(token,''),self.e,self.v))

    def test_replay_and_stale_callback_mutations_rejected(self):
        for token in ('NOT = { has_variable = rw_nd_attempt }',
                      'var:rw_nd_attempt = scope:rw_rp_revision',
                      'has_variable = rw_nd_ticket','rw_nd_adapter_available_trigger = yes'):
            with self.subTest(token=token):
                self.assertTrue(errors(self.t.replace(token,''),self.e,self.v))

    def test_missing_native_check_or_list_isolation_rejected(self):
        for token in ('rw_nd_native_eligible_trigger = yes',
                      'clear_local_variable_list = target_titles',
                      'clear_local_variable_list = titles_to_grant','clear_saved_scope = recipient_is_independent',
                      'save_scope_as = recipient'):
            with self.subTest(token=token):
                self.assertTrue(errors(self.t,self.e.replace(token,''),self.v))

    def test_consequences_before_world_change_rejected(self):
        altered=self.e.replace('                    rw_nd_native_consequences_effect = yes','')
        altered=altered.replace('                create_title_and_vassal_change',
            '                rw_nd_native_consequences_effect = yes\n                create_title_and_vassal_change')
        self.assertIn('execution before consumption or consequences without transfer',errors(self.t,altered,self.v))

    def test_duplicate_or_vassal_transfer_rejected(self):
        altered=self.e.replace('                resolve_title_and_vassal_change = scope:rw_nd_change',
            '                resolve_title_and_vassal_change = scope:rw_nd_change\n                resolve_title_and_vassal_change = scope:rw_nd_change')
        self.assertIn('duplicate native action',errors(self.t,altered,self.v))
        self.assertTrue(errors(self.t,self.e.replace('change_title_holder =','change_title_holder_include_vassals ='),self.v))

    def test_real_shared_option_and_hidden_dispatch(self):
        panel=(MOD/'events/rw_restitution_pledge_events.txt').read_text()
        self.assertIn('name = rw_native_restitution.deliver',panel)
        self.assertIn('trigger = { rw_nd_can_deliver_trigger = yes }',panel)
        self.assertIn('rw_nd_queue_effect = yes',panel)
        self.assertIn('ai_chance = { base = 80',panel)
        self.assertIn('hidden = yes',self.v)
        self.assertIn('immediate = { rw_nd_execute_effect = yes }',self.v)
        # Promise remains live for existing native title-gain observer; no false acknowledgement.
        self.assertNotIn('name = rw_rp_state',self.e)
        self.assertNotIn('rw_rg_observe_effect',self.e)

    def test_localized_limits(self):
        for lang in ('english','french'):
            raw=(MOD/f'localization/{lang}/rw_native_restitution_l_{lang}.yml').read_bytes()
            self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
            self.assertEqual(5,len(re.findall(r'^ rw_native_restitution\.',raw.decode('utf-8-sig'),re.M)))


class PrivateRestitutionBuilderTests(unittest.TestCase):
    def test_six_native_bodies_preserved_exactly(self):
        output,proofs=b.clone_blocks(FIXTURE)
        self.assertEqual(6,len(proofs))
        for old,new in (b.GUARDS|b.CALLBACKS).items():
            a,o,c=bounds(FIXTURE.decode(),old)
            kind='triggers' if old in b.GUARDS else 'effects'
            generated=output[kind].decode();x,y,z=bounds(generated,new)
            self.assertEqual(FIXTURE.decode()[o:c],generated[y:z])
            self.assertEqual(FIXTURE.decode()[a:c],generated[x:z].replace(new,old,1))
        self.assertNotIn(b'grant_titles_interaction =',output['triggers']+output['effects'])

    def test_changed_layout_fails_closed(self):
        for raw in (FIXTURE.replace(b'auto_accept = yes',b'auto_accept = no'),
                    FIXTURE.replace(b'on_accept =',b'cost = { gold = 1 } on_accept ='),
                    FIXTURE.replace(b'can_send =',b'can_send = { duplicate = yes } can_send ='),
                    FIXTURE.replace(b'on_auto_accept =',b'unknown_callback =')):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):b.clone_blocks(raw)

    def make_root(self,root):
        p=root/b.INPUT;p.parent.mkdir(parents=True);p.write_bytes(FIXTURE)
        (root/'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="1.19.0.6"\n')

    def test_build_receipt_and_output_hashes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'input';self.make_root(root);out=Path(temp)/'private'
            with patch.object(b,'pin',return_value=hashlib.sha256(FIXTURE).hexdigest()):
                receipt=b.build(root,out)
            self.assertEqual(2,len(receipt['outputs']))
            for row in receipt['outputs']:
                self.assertEqual(row['sha256'],hashlib.sha256((out/b.MOD_ID/row['path']).read_bytes()).hexdigest())
            for row in receipt['runtime_sources']:
                self.assertEqual(row['sha256'],hashlib.sha256((MOD/row['path']).read_bytes()).hexdigest())
            self.assertIn('DO NOT publish',(out/'PRIVATE.txt').read_text())
            self.assertFalse(any('character_interactions' in r['path'] for r in receipt['outputs']))

    def test_wrong_hash_or_version_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'input';self.make_root(root);out=Path(temp)/'private'
            with patch.object(b,'pin',return_value='0'*64):
                with self.assertRaises(ValueError):b.build(root,out)
            self.assertFalse(out.exists())
            (root/'descriptor.mod').write_text('version="0.5.2.2"\nsupported_version="1.19.0.6"\n')
            with self.assertRaises(ValueError):b.build(root,out)
            self.assertFalse(out.exists())

    def test_symlink_input_and_existing_destination_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'input';self.make_root(root);out=Path(temp)/'private';out.mkdir()
            with self.assertRaises(ValueError):b.build(root,out)
            link=Path(temp)/'link';link.symlink_to(root,target_is_directory=True)
            with self.assertRaises(ValueError):b.build(link,Path(temp)/'new')

    def test_public_distribution_contains_builder_only(self):
        from tools.build_distribution import DOCS
        self.assertIn('tools/build_native_restitution.py',DOCS)
        self.assertIn('docs/NATIVE_RESTITUTION_SOURCE_RECEIPT.json',DOCS)
        self.assertFalse(any('zz_rw_native_restitution' in s for s in DOCS))


if __name__ == '__main__':unittest.main()
