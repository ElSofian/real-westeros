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
        self.inputs = {builder.INTERACTION: FIXTURE.encode(), builder.HELPER: b'synthetic helper',
                       builder.CLAIM: b'synthetic original CB'}
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
        self.assertEqual(8, len(receipt['outputs']))
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
        self.assertFalse((builder.REPO/'mod/real_westeros/common/scripted_triggers/rw_unlawful_war_choice_triggers.txt').exists())

    def test_templates_have_bom_headers_and_complete_localizations(self):
        payload=builder.template_payload()
        for name in builder.FILES:
            if not name.endswith('.yml'): continue
            self.assertTrue(payload[name].startswith(b'\xef\xbb\xbf'))
            for key in ('rw_uw_defy_option:0','rw_uw_defy_warning:0'):
                self.assertIn(key,payload[name].decode('utf-8-sig'))

    def test_source_pins_remain_the_reviewed_three_files(self):
        pins=builder.pinned_sources()
        self.assertEqual({builder.INTERACTION,builder.HELPER,builder.CLAIM},set(pins))
        self.assertTrue(all(len(h)==64 for h in pins.values()))


if __name__=='__main__': unittest.main()
