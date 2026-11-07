"""Original-source callback provenance and native-byte preservation, no game model."""
from pathlib import Path
import re
import unittest
from tools import build_g1_native_choice as b
from tools.validate_mod import clean_script
from test_g1_royal_response import block

ROOT=b.TEMPLATES
T=ROOT/'common/scripted_triggers/rw_declaration_law_triggers.txt'
E=ROOT/'common/scripted_effects/rw_declaration_law_effects.txt'
S=ROOT/'common/story_cycles/rw_declaration_law.txt'
CLAIM='''claim_cb = {
    cost = { synthetic_price = 7 }
    on_declaration = { original_declaration_effect = yes }
    on_victory = { original_success_effect = yes }
}
other_cb = { unmodified = yes }
'''
HELPER='''war_declarer_needs_hook_on_liege = {
    # scope:actor inside comment must remain unchanged
    scope:actor = { synthetic_peer = scope:recipient synthetic_text = "scope:recipient" }
}
'''


def contract_errors(t,e,s):
    errors=[]
    def need(source,parts,label):
        if any(not re.search(re.escape(p)+r'(?![\w:])',source) for p in parts):errors.append(label)
    ctx=block(t,'rw_dl_callback_context_trigger')
    need(ctx,('rw_dl_adapter_available_trigger = yes','exists = scope:attacker',
        'exists = scope:defender','exists = scope:war','using_cb = claim_cb',
        'primary_attacker = scope:attacker','primary_defender = scope:defender',
        'exists = liege','liege = { is_alive = yes is_landed = yes exists = primary_title }'),'wrong callback context')
    capture=block(e,'rw_dl_capture_effect')
    need(capture,('limit = { rw_dl_callback_context_trigger = yes }','rw_dl_native_permission_trigger = yes',
        'flag:inconsistent','flag:native_exception','flag:permission_required','flag:no_ban',
        'flag:claim_cb_on_declaration_prefix','any_owned_story =','var:rw_dl_war = scope:rw_dl_war',
        'story_owner = scope:rw_dl_actor','NOT = { has_variable = rw_dl_serial }',
        'clear_saved_scope = rw_dl_authority','exists = scope:rw_dl_authority',
        'name = rw_dl_retained value = flag:yes days = 365'),'missing provenance or immutable capture')
    internal = '''limit = {
        scope:rw_dl_rule = flag:internal
        scope:rw_dl_peer_relation = flag:same_liege
    }'''
    if ' '.join(internal.split()) not in ' '.join(clean_script(capture)[0].split()):
        errors.append('internal ban applied outside its direct hierarchy')
    if re.search(r'save_scope_as\s*=\s*(actor|recipient|target|attacker|defender|war)\b',capture):
        errors.append('native aliases overwritten')
    link=block(e,'rw_dl_link_response_effect')
    need(link,('this = scope:rw_uw_attacker','var:rw_uw_serial = scope:rw_uw_serial',
        'var:rw_uw_war = scope:rw_uw_war','var:rw_uw_issuer = scope:rw_uw_issuer',
        'var:rw_uw_authority = scope:rw_uw_authority','has_variable = rw_uw_live',
        'var:rw_uw_source = flag:native_choice_accept','NOT = { has_variable = rw_dl_link }',
        'count >= 2 rw_dl_match_response_trigger = yes','clear_saved_scope = rw_dl_link_source',
        'exists = scope:rw_dl_link_source','name = rw_dl_link_serial'),
        'ambiguous or stale attachment')
    if 'rw_dl_capture_effect = yes' in link or 'has_realm_law_flag' in link:
        errors.append('late reconstruction')
    match=block(t,'rw_dl_match_response_trigger')
    need(match,('story_type = story_rw_declaration_law','story_owner = scope:rw_uw_attacker',
        'has_variable = rw_dl_retained','var:rw_dl_phase = flag:claim_cb_on_declaration_prefix',
        'var:rw_dl_attacker = scope:rw_uw_attacker','var:rw_dl_defender = scope:rw_uw_defender',
        'var:rw_dl_war = scope:rw_uw_war','var:rw_dl_issuer = scope:rw_uw_issuer',
        'var:rw_dl_authority = scope:rw_uw_authority'),'wrong source identity')
    view=block(t,'rw_dl_link_view_trigger')
    need(view,('rw_uw_response_identity_trigger = yes','this = scope:rw_uw_issuer',
        'rw_dl_match_response_trigger = yes','var:rw_dl_serial = prev.var:rw_dl_link_serial'),'private or stale reader')
    if 'has_realm_law_flag' in view or 'rw_dl_native_permission_trigger' in view:errors.append('reader rejudges policy')
    need(s,('on_owner_death = { end_story = yes }','NOT = { has_variable = rw_dl_retained }',
        'any_character_war = { this = scope:rw_dl_check.var:rw_dl_war }'),'retention or inherited guilt')
    if re.search(r'\b(start_war|end_war|add_gold|add_opinion|use_hook|add_claim|add_realm_law|change_title_holder|run_interaction|add_imprisonment_reason)\s*=',clean_script(e+s)[0]):
        errors.append('native state changed')
    return errors


class DeclarationLawBuilderTests(unittest.TestCase):
    def test_claim_prefix_preserves_complete_native_definition_bytes(self):
        for newline in ('\n','\r\n'):
            old,new=b.patch_claim_law(b'\xef\xbb\xbf'+CLAIM.replace('\n',newline).encode())
            self.assertEqual(old,new.replace(b.LAW_PREFIX.encode(),b'',1))
            self.assertNotIn(b'other_cb',new)
            self.assertLess(new.index(b'rw_dl_capture_effect'),new.index(b'original_declaration_effect'))
            self.assertIn(b'original_success_effect',new)

    def test_helper_inverse_restores_bytes_and_comment_strings(self):
        for newline in ('\n','\r\n'):
            old,new=b.clone_permission(HELPER.replace('\n',newline).encode())
            clone=new.decode().split('\n',1)[1]
            restored=clone.replace(b.CLONE,b.NATIVE_PERMISSION,1).replace('scope:rw_dl_actor','scope:actor').replace('scope:rw_dl_target','scope:recipient')
            self.assertEqual(old,restored.encode())
            self.assertIn('# scope:actor inside comment',clone)
            self.assertIn('"scope:recipient"',clone)

    def test_helper_unknown_scope_or_root_context_rejected(self):
        for old,new in [('scope:recipient','scope:other'),('synthetic_peer','root'),('synthetic_peer','prev')]:
            with self.subTest(old=old),self.assertRaises(ValueError):b.clone_permission(HELPER.replace(old,new).encode())

    def test_changed_missing_duplicate_or_nested_claim_refused(self):
        for text in (CLAIM.replace('on_declaration','other_hook'),CLAIM+CLAIM,'wrap = { '+CLAIM+' }'):
            with self.subTest(text=text[:20]),self.assertRaises(ValueError):b.patch_claim_law(text.encode())

    def test_double_patch_refused(self):
        _,new=b.patch_claim_law(CLAIM.encode())
        with self.assertRaises(ValueError):b.patch_claim_law(new)


class DeclarationLawSourceTests(unittest.TestCase):
    def setUp(self):self.t=T.read_text();self.e=E.read_text();self.s=S.read_text()
    def test_real_source_contract(self):self.assertEqual([],contract_errors(self.t,self.e,self.s))

    def test_capture_reads_attacker_liege_across_different_defender_hierarchies(self):
        context = block(self.t, 'rw_dl_callback_context_trigger')
        self.assertIn('exists = liege', block(context, 'scope:attacker'))
        self.assertNotIn('liege = scope:defender.liege', context)
        self.assertNotIn('exists = liege', block(context, 'scope:defender'))
        self.assertIn('scope:attacker.liege = {', self.e)
        for other_authority in ('scope:defender.liege = {', 'top_liege = {', 'every_liege_or_above'):
            self.assertNotIn(other_authority, block(self.e, 'rw_dl_capture_effect'))

    def test_direct_hierarchy_relation_is_guarded_and_archived_once(self):
        capture = block(self.e, 'rw_dl_capture_effect')
        expected = '''
            save_scope_value_as = { name = rw_dl_peer_relation value = flag:different_liege }
            if = {
                limit = {
                    exists = scope:defender.liege
                    scope:attacker.liege = scope:defender.liege
                }
                save_scope_value_as = { name = rw_dl_peer_relation value = flag:same_liege }
            }
        '''
        self.assertIn(' '.join(expected.split()), ' '.join(capture.split()))
        writes = re.findall(r'\bset_variable\s*=\s*\{\s*name\s*=\s*rw_dl_peer_relation\s+value\s*=\s*([^}]+)\}',
                            clean_script(self.e + self.s)[0])
        self.assertEqual(['scope:rw_dl_peer_relation'], [value.strip() for value in writes])
        self.assertIn('set_variable = { name = rw_dl_rule value = scope:rw_dl_rule }', capture)
        self.assertNotIn('rw_dl_peer_relation', block(self.t, 'rw_dl_match_response_trigger'))
        self.assertNotIn('rw_dl_peer_relation', block(self.t, 'rw_dl_link_view_trigger'))

    def test_internal_ban_domain_removal_or_inversion_is_detected(self):
        for replacement in ('always = yes', 'scope:rw_dl_peer_relation = flag:different_liege'):
            changed = self.e.replace('scope:rw_dl_peer_relation = flag:same_liege', replacement)
            self.assertIn('internal ban applied outside its direct hierarchy',
                          contract_errors(self.t, changed, self.s))

    def test_authority_rule_is_preserved_separately_from_applicability(self):
        expected = '''
            save_scope_value_as = { name = rw_dl_rule value = flag:none }
            if = {
                limit = { scope:rw_dl_issuer = { has_realm_law_flag = vassal_all_wars_banned } }
                save_scope_value_as = { name = rw_dl_rule value = flag:all }
            }
            else_if = {
                limit = { scope:rw_dl_issuer = { has_realm_law_flag = vassal_internal_wars_banned } }
                save_scope_value_as = { name = rw_dl_rule value = flag:internal }
            }
        '''
        self.assertIn(' '.join(expected.split()), ' '.join(clean_script(self.e)[0].split()))
        writes = re.findall(r'\bset_variable\s*=\s*\{\s*name\s*=\s*rw_dl_rule\s+value\s*=\s*([^}]+)\}',
                            clean_script(self.e + self.s)[0])
        self.assertEqual(['scope:rw_dl_rule'], [value.strip() for value in writes])
        self.assertNotIn('rw_dl_rule', block(self.t, 'rw_dl_match_response_trigger'))
        self.assertNotIn('rw_dl_rule', block(self.t, 'rw_dl_link_view_trigger'))

    def test_total_ban_keeps_priority_and_response_entry_keeps_its_peer_guard(self):
        capture = block(self.e, 'rw_dl_capture_effect')
        self.assertLess(capture.index('vassal_all_wars_banned'), capture.index('vassal_internal_wars_banned'))
        self.assertIn('limit = { scope:rw_dl_rule = flag:all }', capture)
        choice = (ROOT/'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt').read_text()
        self.assertIn('liege = scope:recipient.liege', block(choice, 'rw_uw_peer_ban_trigger'))
        self.assertIn('rw_uw_peer_ban_trigger = yes', block(choice, 'rw_uw_selected_defiance_trigger'))

    def test_native_permission_outcomes_keep_their_exact_branch_conditions(self):
        # Presence-only checks miss swapped outcomes or an inverted ban test.
        expected = '''
            save_scope_value_as = { name = rw_dl_gate value = flag:no_ban }
            if = {
                limit = { rw_dl_native_permission_trigger = yes }
                save_scope_value_as = { name = rw_dl_gate value = flag:permission_required }
                if = {
                    limit = { scope:rw_dl_ban = flag:none }
                    save_scope_value_as = { name = rw_dl_gate value = flag:inconsistent }
                }
            }
            else_if = {
                limit = { NOT = { scope:rw_dl_ban = flag:none } }
                save_scope_value_as = { name = rw_dl_gate value = flag:native_exception }
            }
        '''
        self.assertIn(' '.join(expected.split()), ' '.join(clean_script(self.e)[0].split()))

    def test_archived_gate_is_copied_once_from_the_early_snapshot(self):
        writes = re.findall(r'\bset_variable\s*=\s*\{\s*name\s*=\s*rw_dl_gate\s+value\s*=\s*([^}]+)\}',
                            clean_script(self.e + self.s)[0])
        self.assertEqual(['scope:rw_dl_gate'], [value.strip() for value in writes])
        capture = block(self.e, 'rw_dl_capture_effect')
        self.assertLess(capture.index('rw_dl_native_permission_trigger = yes'), capture.index('create_story ='))
        self.assertNotIn('rw_dl_native_permission_trigger', block(self.e, 'rw_dl_link_response_effect'))

    def test_base_without_adapter_fails_closed(self):
        self.assertIn('always = no',block(self.t,'rw_dl_adapter_available_trigger'))
        self.assertIn('always = no',block(self.t,'rw_dl_native_permission_trigger'))
        self.assertNotIn('rw_dl_adapter_available_trigger = { always = yes }',self.t)

    def test_wrong_callback_pair_or_war_rejected(self):
        for old,new in [('primary_attacker = scope:attacker','primary_attacker = scope:defender'),
                        ('using_cb = claim_cb','using_cb = other_cb')]:
            with self.subTest(old=old):self.assertTrue(contract_errors(self.t.replace(old,new),self.e,self.s))

    def test_late_capture_fallback_rejected(self):
        changed=self.e.replace('rw_dl_link_response_effect = {','rw_dl_link_response_effect = { rw_dl_capture_effect = yes')
        self.assertTrue(contract_errors(self.t,changed,self.s))

    def test_native_alias_overwrite_rejected(self):
        changed=self.e.replace('save_scope_as = rw_dl_actor','save_scope_as = actor')
        self.assertTrue(contract_errors(self.t,changed,self.s))

    def test_duplicate_receipt_and_expiry_mutations_rejected(self):
        for old,new in [('any_owned_story =','any_other_story ='),('days = 365','days = 3650'),
                        ('count >= 2 rw_dl_match_response_trigger = yes','count >= 20 rw_dl_match_response_trigger = yes')]:
            with self.subTest(old=old):self.assertTrue(contract_errors(self.t,self.e.replace(old,new),self.s))

    def test_foreign_or_stale_source_identity_rejected(self):
        for old,new in [('var:rw_dl_war = scope:rw_uw_war','has_variable = rw_dl_war'),
                        ('var:rw_dl_issuer = scope:rw_uw_issuer','has_variable = rw_dl_issuer'),
                        ('var:rw_dl_serial = prev.var:rw_dl_link_serial','has_variable = rw_dl_serial')]:
            with self.subTest(old=old):self.assertTrue(contract_errors(self.t.replace(old,new),self.e,self.s))

    def test_reader_cannot_recompute_native_law(self):
        changed=self.t.replace('rw_dl_link_view_trigger = {','rw_dl_link_view_trigger = { has_realm_law_flag = vassal_internal_wars_banned')
        self.assertTrue(contract_errors(changed,self.e,self.s))

    def test_no_crime_cost_or_war_side_effect(self):
        for op in ('end_war = white_peace','add_imprisonment_reason = yes','use_hook = liege','add_gold = -50'):
            with self.subTest(op=op):self.assertTrue(contract_errors(self.t,self.e+'\n bad = { '+op+' }',self.s))

    def test_link_is_after_response_initialization_before_notification(self):
        text=(ROOT/'common/scripted_effects/rw_unlawful_war_response_effects.txt').read_text()
        self.assertLess(text.index('name = rw_uw_war value ='),text.index('rw_dl_link_response_effect = yes'))
        self.assertLess(text.index('rw_dl_link_response_effect = yes'),text.index('id = rw_unlawful_war_response.0001'))

    def test_readers_do_not_extend_retention(self):
        self.assertNotIn('days =',block(self.e,'rw_dl_link_response_effect'))
        self.assertNotIn('set_variable',block(self.t,'rw_dl_link_view_trigger'))
        self.assertNotIn('is_ai',self.t+self.e)


if __name__=='__main__':unittest.main()
