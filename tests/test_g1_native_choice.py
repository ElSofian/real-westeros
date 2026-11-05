"""Original synthetic native-window fixtures and private generation contracts."""
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from tools import build_g1_native_choice as builder
from tools.validate_mod import brace_errors, clean_script

# Deliberately synthetic layout, not an extracted native interaction.
FIXTURE = '''synthetic_before = { untouched = yes }
declare_war_interaction = {
    preserved_setting = "synthetic-é"
    preserved_condition = { original_guard = yes }
    has_valid_target_showing_failures_only = {
        custom_description = {
            OR = {
                war_declarer_needs_hook_on_liege = no
                always = scope:hook
            }
        }
        unchanged_other_target_guard = yes
    }
    send_options_exclusive = no
    send_option = { flag = hook synthetic_native_option = yes }
    on_accept = { preserved_native_callback = yes }
}
synthetic_after = { untouched = yes }
'''


class NativeChoiceBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='rw-native-choice-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.agot = self.root / 'synthetic AGOT'
        self.agot.mkdir()
        self.out = self.root / 'private'
        (self.agot / 'descriptor.mod').write_text('version="0.5.2.1"\nsupported_version="1.19.0.6"\n')
        self.inputs = {builder.INTERACTION: FIXTURE.encode(), builder.HELPER: b'war_declarer_needs_hook_on_liege = { scope:actor = { synthetic_peer = scope:recipient } }',
                       builder.CLAIM: b'claim_cb = { target_titles = synthetic on_declaration = { synthetic_native_declaration = yes } on_victory = { synthetic_resolution = yes } }', builder.VASSAL: b'synthetic native intervention'}
        for name, raw in self.inputs.items():
            path = self.agot / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.pins = {name: hashlib.sha256(raw).hexdigest() for name,raw in self.inputs.items()}

    def build(self):
        with patch.object(builder, 'pinned_sources', return_value=self.pins):
            return builder.build(self.agot, self.out)

    def test_only_three_insertions_preserve_native_bytes(self):
        for newline in ('\n', '\r\n'):
            raw = FIXTURE.replace('\n',newline).encode()
            original, result = builder.patch_native(b'\xef\xbb\xbf' + raw)
            self.assertEqual(original, result.replace(builder.GUARD.encode(),b'',1).replace(builder.OPTION.encode(),b'',1).replace(builder.ACCEPT.encode(),b'',1))
            self.assertEqual([], brace_errors(result.decode()))
            self.assertNotIn(b'synthetic_before', result)
            self.assertNotIn(b'synthetic_after', result)
            self.assertIn(b'preserved_native_callback = yes', result)

    def test_real_original_templates_and_private_manifest(self):
        receipt = self.build()
        self.assertIn('NOT VERIFIED', receipt['ai_option_initialization'])
        self.assertIn('version="0.0.4"', (self.out/builder.MOD_ID/'descriptor.mod').read_text())
        self.assertEqual(3, len(receipt['outputs']))
        self.assertEqual(len(builder.FILES), len(receipt['runtime_sources']))
        self.assertEqual('Real Westeros', receipt['requires_base_mod'])
        self.assertIn('dependencies={ "Real Westeros" }', (self.out/builder.MOD_ID/'descriptor.mod').read_text())
        for row in receipt['runtime_sources']:
            self.assertEqual(row['sha256'], hashlib.sha256((builder.TEMPLATES/row['path']).read_bytes()).hexdigest())
            self.assertFalse((self.out/builder.MOD_ID/row['path']).exists())
        for row in receipt['outputs']:
            raw = (self.out / builder.MOD_ID / row['path']).read_bytes()
            self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertNotIn(str(self.agot), json.dumps(receipt))
        self.assertFalse((self.out / builder.MOD_ID / builder.HELPER).exists())
        self.assertFalse((self.out / builder.MOD_ID / builder.CLAIM).exists())
        for name,raw in self.inputs.items():
            self.assertEqual(raw,(self.agot/name).read_bytes())

    def test_unreviewed_inputs_rejected_before_output(self):
        for name,raw in self.inputs.items():
            (self.agot/name).write_bytes(raw+b' altered')
            with self.assertRaises(ValueError): self.build()
            self.assertFalse(self.out.exists())
            (self.agot/name).write_bytes(raw)

    def test_missing_input_rejected_before_output(self):
        (self.agot/builder.CLAIM).unlink()
        with self.assertRaises(ValueError): self.build()
        self.assertFalse(self.out.exists())

    def test_version_mismatch_rejected(self):
        (self.agot/'descriptor.mod').write_text('version="0.5.2.2"\nsupported_version="1.19.0.6"')
        with self.assertRaises(ValueError): self.build()
        self.assertFalse(self.out.exists())

    def test_existing_output_never_overwritten(self):
        self.out.mkdir();(self.out/'KEEP').write_text('keep')
        with self.assertRaises(ValueError): self.build()
        self.assertEqual('keep',(self.out/'KEEP').read_text())

    def test_output_inside_repository_or_installation_rejected(self):
        for path in (self.agot/'private',self.agot,self.root,builder.REPO/'private-forbidden'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                builder.build(self.agot,path)

    def test_symlink_native_input_rejected(self):
        path = self.agot / builder.CLAIM
        path.unlink(); target = self.root/'outside';target.write_bytes(self.inputs[builder.CLAIM])
        path.symlink_to(target)
        with self.assertRaises(ValueError): self.build()
        self.assertFalse(self.out.exists())

    def test_duplicate_or_missing_native_blocks_rejected(self):
        for raw in ((FIXTURE+FIXTURE).encode(),FIXTURE.replace('declare_war_interaction','other').encode()):
            with self.assertRaises(ValueError): builder.patch_native(raw)

    def test_nested_native_definition_rejected(self):
        with self.assertRaises(ValueError): builder.patch_native(('wrapper = {\n'+FIXTURE+'\n}').encode())

    def test_changed_native_hook_guard_or_send_layout_rejected(self):
        for before,after in [('always = scope:hook','always = no'),
                             ('send_options_exclusive = no','send_options_exclusive = yes'),
                             ('war_declarer_needs_hook_on_liege = no','other_helper = no')]:
            with self.subTest(before=before), self.assertRaises(ValueError):
                builder.patch_native(FIXTURE.replace(before,after).encode())

    def test_already_patched_and_unbalanced_inputs_rejected(self):
        for raw in (FIXTURE.replace('preserved_setting','rw_uw_already_patched').encode(),FIXTURE[:-4].encode()):
            with self.assertRaises(ValueError): builder.patch_native(raw)

    def test_corrupt_template_and_missing_localization_fail_before_output(self):
        with patch.object(builder,'template_payload',side_effect=ValueError('bad template')):
            with self.assertRaises(ValueError): self.build()
        self.assertFalse(self.out.exists())
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for relative in builder.FILES:
                dest=root/relative;dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(builder.TEMPLATES/relative,dest)
            path=root/builder.FILES[-1];path.write_text('wrong header')
            with self.assertRaises(ValueError): builder.template_payload(root)


class NativeChoiceSourceTests(unittest.TestCase):
    def setUp(self):
        self.text=(builder.TEMPLATES/'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt').read_text()

    def test_same_live_peer_and_native_exception_guards(self):
        start,_,end=builder.bounds(self.text,'rw_uw_peer_ban_trigger')
        text=clean_script(self.text[start:end])[0]
        self.assertIn('liege = scope:recipient.liege',text)
        self.assertEqual(2,text.count('government_has_flag = government_is_feudal'))
        self.assertEqual(2,text.count('is_imprisoned = no'))
        self.assertIn('vassal_internal_wars_banned',text)
        self.assertIn('vassal_all_wars_banned',text)
        self.assertIn('war_declarer_needs_hook_on_liege = yes',text)
        self.assertNotIn('is_ai',text)

    def test_explicit_window_flag_without_hook_combination(self):
        self.assertIn('always = scope:rw_uw_defy',self.text)
        self.assertIn('NOT = { always = scope:hook }',self.text)
        self.assertIn('NOT = { always = scope:hook }',builder.OPTION)
        self.assertIn('can_invalidate_interaction = yes',builder.OPTION)
        self.assertIn('rw_uw_selected_defiance_trigger = yes',builder.GUARD)

    def test_no_persistent_bypass_cost_cb_or_lifecycle_mutation(self):
        original=self.text+builder.GUARD+builder.OPTION
        for forbidden in ('set_variable','set_character_flag','start_war','end_war','run_interaction',
                          'add_gold','use_hook =','on_accept =','on_war_started','ai_will_do','claim_cb ='):
            self.assertNotIn(forbidden,original)
        self.assertFalse((builder.REPO/'mod/real_westeros/common/character_interactions/zz_rw_native_war_choice.txt').exists())

    def test_ai_initial_choice_never_changes_shared_permission(self):
        # Identity/AI/means are preference only, never a new eligibility branch.
        for name in ('rw_uw_peer_ban_trigger', 'rw_uw_selected_defiance_trigger'):
            start, _, end = builder.bounds(self.text, name)
            block = clean_script(self.text[start:end])[0]
            self.assertNotIn('is_ai', block)
            self.assertNotIn('gold', block)
            self.assertNotIn('opinion', block)
            self.assertNotIn('rw_uw_ai_default_defiance_trigger', block)
        self.assertEqual(1, builder.OPTION.count('starts_enabled'))
        self.assertIn('starts_enabled = { rw_uw_ai_default_defiance_trigger = yes }', builder.OPTION)
        self.assertNotIn('starts_enabled', builder.GUARD)
        self.assertNotIn('can_be_changed', builder.OPTION)

    def test_ai_preference_fails_closed_on_context_hook_or_burden(self):
        start, _, end = builder.bounds(self.text, 'rw_uw_ai_default_defiance_trigger')
        block = clean_script(self.text[start:end])[0]
        for guard in ('rw_uw_peer_ban_trigger = yes', 'NOT = { always = scope:hook }',
                      'is_ai = yes', 'is_at_war = no', 'gold >= 150',
                      'rw_ai_existing_commitment_trigger = no',
                      'opinion = { target = scope:actor.liege value <= -25 }'):
            self.assertIn(guard, block)
        _, opening, actor_end = builder.bounds(block, 'scope:actor')
        actor = block[opening:actor_end]
        for token in ('is_ai = yes', 'gold >= 150', 'is_at_war = no', 'opinion ='):
            self.assertIn(token, actor)
        for token in ('random', 'set_', 'save_', 'every_', 'any_', 'run_interaction',
                      'start_war', 'add_gold', 'use_hook'):
            self.assertNotIn(token, block)

    def test_ai_preference_does_not_claim_native_planner_support(self):
        receipt = json.loads((builder.REPO/'docs/G1_AI_OPTION_SOURCE_RECEIPT.json').read_text())
        self.assertEqual(1, len(receipt['files']))
        row = receipt['files'][0]
        self.assertEqual(64, len(row['sha256']))
        self.assertEqual([2505, 3323], row['markers']['send_option.starts_enabled'])
        self.assertNotIn('native_source', row)

    def test_templates_have_bom_headers_and_complete_localizations(self):
        payload=builder.template_payload()
        for name in builder.FILES:
            if not name.endswith('.yml'): continue
            self.assertTrue(payload[name].startswith(b'\xef\xbb\xbf'))
            for key in ('rw_uw_defy_option:0','rw_uw_defy_warning:0'):
                self.assertIn(key,payload[name].decode('utf-8-sig'))

    def test_source_pins_cover_declaration_and_native_intervention(self):
        pins=builder.pinned_sources()
        self.assertEqual({builder.INTERACTION,builder.HELPER,builder.CLAIM,builder.VASSAL},set(pins))
        self.assertTrue(all(len(h)==64 for h in pins.values()))


if __name__=='__main__': unittest.main()
