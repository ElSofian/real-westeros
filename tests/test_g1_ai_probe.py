"""Probe construction and fail-closed controls; never simulate the CK3 planner."""
from pathlib import Path
import tempfile
import unittest

from tools import build_g1_ai_probe as probe
from tools.validate_mod import clean_script


class AIProbeTests(unittest.TestCase):
    def test_exact_pair_and_cb_without_direct_or_fake_war(self):
        for mode in ('allowed', 'banned', 'reject'):
            text = clean_script(probe.case(mode))[0]
            self.assertEqual(1, text.count('ai_start_best_war ='))
            self.assertIn('cb = { claim_cb }', text)
            self.assertIn('scope:target_character = global_var:rw_ai1_target', text)
            self.assertIn('scope:target_title = global_var:rw_ai1_title', text)
            for forbidden in ('start_war =', 'run_interaction =', 'add_claim =', 'end_war =', 'every_living_character', 'execute_threshold'):
                self.assertNotIn(forbidden, text)

    def test_missing_setup_player_control_or_bad_context_refuses_call(self):
        text = probe.case('banned')
        for guard in ('exists = global_var:rw_ai1_actor', 'is_ai = yes', 'is_at_war = no',
                      'has_claim_on = global_var:rw_ai1_title', 'gold >= 150',
                      'rw_ai_existing_commitment_trigger = no', 'value <= -25',
                      'liege = global_var:rw_ai1_target.liege'):
            self.assertLess(text.index(guard), text.index('ai_start_best_war ='))
        self.assertIn('banned_missing_setup', text)
        self.assertIn('banned_precondition_failed', text)

    def test_reject_control_cannot_authorize_a_candidate(self):
        reject = probe.case('reject')
        self.assertIn('always = no', reject)
        self.assertIn('crown_authority_0', reject)
        self.assertNotIn('always = no', probe.case('allowed'))
        self.assertIn('crown_authority_2', probe.case('banned'))
        with self.assertRaises(ValueError):
            probe.case('arbitrary_target')

    def test_existing_native_law_is_not_added_twice(self):
        for mode, law in (('banned', 'crown_authority_2'), ('allowed', 'crown_authority_0'), ('reject', 'crown_authority_0')):
            text = probe.case(mode)
            self.assertIn('limit = { NOT = { has_realm_law = '+law+' } }', text)
            self.assertLess(text.index('has_realm_law = '+law), text.index('add_realm_law = '+law))

    def test_only_setup_changes_fixture_relationship_and_all_handles_expire(self):
        self.assertIn('this = title:d_oldtown.holder', probe.SETUP)
        self.assertIn('set_relation_rival = liege', probe.SETUP)
        self.assertEqual(3, probe.SETUP.count('days = 7'))
        for mode in ('allowed', 'banned', 'reject'):
            self.assertNotIn('set_relation_rival', probe.case(mode))

    def test_new_output_only_and_all_original_files_are_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'new'
            receipt = probe.build(out)
            self.assertEqual(8, len(receipt['files']))
            for name in receipt['files']:
                self.assertTrue((out/name).read_bytes().startswith(b'\xef\xbb\xbf'))
            with self.assertRaises(ValueError):
                probe.build(out)
        with self.assertRaises(ValueError):
            probe.build(probe.ROOT/'build'/'must-not-create')

    def test_inspect_extends_existing_context_without_starting_or_initializing_ai(self):
        text = clean_script(probe.INSPECT)[0]
        self.assertEqual(3, text.count('days = 7'))
        self.assertIn('exists = global_var:rw_ai1_actor', text)
        self.assertIn('can_declare_war = {', text)
        self.assertNotIn('ai_start_best_war', text)
        self.assertNotIn('add_realm_law', text)
        self.assertNotIn('initialized', text)
        self.assertNotIn('set_relation', text)

    def test_audit_reports_each_predicate_without_weakening_the_probe(self):
        self.assertEqual(12, len(probe.AUDIT_CHECKS))
        for name, trigger in probe.AUDIT_CHECKS:
            self.assertIn(trigger, probe.INSPECT)
            self.assertIn('check_'+name+'_yes', probe.INSPECT)
            self.assertIn('check_'+name+'_no', probe.INSPECT)
            if name == 'hostile':
                self.assertIn(trigger, probe.case('banned'))
                self.assertNotIn(trigger, probe.case('allowed'))
                self.assertNotIn(trigger, probe.case('reject'))
            else:
                self.assertIn(trigger, probe.case('allowed'))

    def test_expired_handles_cannot_redirect_or_disable_fixture_sampling(self):
        self.assertIn('exists = character:Hightower_5', probe.REBIND)
        self.assertIn('exists = character:Redwyne_4', probe.REBIND)
        self.assertIn('character:Hightower_5 = { this = title:d_oldtown.holder }', probe.REBIND)
        self.assertIn('character:Redwyne_4 = { this = title:d_the_arbor.holder }', probe.REBIND)
        self.assertNotIn('ai_start_best_war', probe.REBIND)
        self.assertNotIn('add_realm_law', probe.REBIND)
        for name, raw in probe.payload().items():
            if any(key in name for key in ('inspect', 'allowed', 'banned', 'reject')):
                self.assertTrue(raw.decode('utf-8-sig').startswith(probe.REBIND))

    def test_comparison_requires_negative_control_before_ban_and_stops_on_war(self):
        text = probe.comparison()
        self.assertEqual(3, text.count('ai_start_best_war ='))
        self.assertLess(text.index('name = rw_ai1_compare_stage value = flag:unready'),
                        text.index('global_var:rw_ai1_compare_stage = flag:hostile_ready'))
        self.assertLess(text.index('RW_AI1 reject_begin'), text.index('RW_AI1 banned_begin'))
        self.assertLess(text.index('RW_AI1 banned_begin'), text.index('RW_AI1 allowed_begin'))
        for required in ('hostile_ready', 'reject_ok', 'banned_failure'):
            self.assertIn('limit = { global_var:rw_ai1_compare_stage = flag:'+required+' }', text)
        self.assertNotIn('limit = { global_var:rw_ai1_compare_stage = flag:reject_bad }', text)
        self.assertNotIn('limit = { global_var:rw_ai1_compare_stage = flag:banned_success }', text)
        self.assertEqual(1, text.count('add_opinion ='))
        self.assertIn('modifier = debug_hates_liege_opinion days = 7', text)
        self.assertIn('opinion = { target = liege value <= -25 }', text)
        self.assertIn('remove_global_variable = rw_ai1_compare_stage', probe.CLEANUP)

    def test_comparison_keeps_real_cb_filters_and_no_direct_war_or_means_grants(self):
        text = clean_script(probe.comparison())[0]
        self.assertEqual(3, text.count('cb = { claim_cb }'))
        self.assertEqual(3, text.count('scope:target_character = global_var:rw_ai1_target'))
        self.assertEqual(3, text.count('scope:target_title = global_var:rw_ai1_title'))
        for forbidden in ('start_war =', 'end_war =', 'add_claim =', 'add_gold =', 'add_prestige =', 'run_interaction ='):
            self.assertNotIn(forbidden, text)


if __name__ == '__main__':
    unittest.main()
