"""Static regression checks for finite flag transport and legacy mode handling."""
from pathlib import Path
import re
import unittest

from test_deferred_service_contract import block

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


class FavorSnapshotFlagTests(unittest.TestCase):
    def setUp(self):
        self.effects = (MOD/'common/scripted_effects/rw_favor_service_effects.txt').read_text(encoding='utf-8-sig')
        self.triggers = (MOD/'common/scripted_triggers/rw_favor_service_triggers.txt').read_text(encoding='utf-8-sig')
        self.snapshot = block(self.effects, 'rw_fv_snapshot_effect')

    def test_flag_snapshots_use_literal_values_and_preserve_numeric_identity(self):
        for name, allowed in (('term', ['invalid', 'favor', 'gold25']),
                              ('mode', ['immediate', 'invalid', 'immediate', 'deferred'])):
            values = re.findall(r'name = rw_fv_'+name+r' value = ([^\s}]+)', self.snapshot)
            self.assertEqual(['flag:'+value for value in allowed], values)
        for name in ('serial', 'revision'):
            self.assertIn('name = rw_fv_'+name+' value = var:rw_fv_'+name, self.snapshot)

    def test_missing_term_stays_invalid_and_mode_less_offer_stays_immediate(self):
        self.assertLess(self.snapshot.index('value = flag:invalid'),
                        self.snapshot.index('has_variable = rw_fv_term'))
        self.assertLess(self.snapshot.index('name = rw_fv_mode value = flag:immediate'),
                        self.snapshot.index('has_variable = rw_fv_mode'))
        for name, values in (('term', ('favor', 'gold25')), ('mode', ('immediate', 'deferred'))):
            for value in values:
                self.assertIn('limit = { var:rw_fv_'+name+' = flag:'+value+' }', self.snapshot)

    def test_unknown_mode_is_invalid_inside_present_mode_branch(self):
        mode_guard = self.snapshot.index('limit = { has_variable = rw_fv_mode }')
        invalid = self.snapshot.index('name = rw_fv_mode value = flag:invalid')
        selected = self.snapshot.index('limit = { var:rw_fv_mode = flag:immediate }')
        self.assertLess(mode_guard, invalid)
        self.assertLess(invalid, selected)

    def test_review_only_reads_schema_and_counterpart_after_presence_guards(self):
        review = block(self.triggers, 'rw_fv_review_allowed_trigger')
        self.assertLess(review.index('limit = { has_variable = rw_fv_schema }'),
                        review.index('var:rw_fv_schema = 1'))
        self.assertLess(review.index('limit = { scope:recipient = { exists = var:rw_fv_client } }'),
                        review.index('scope:recipient.var:rw_fv_client'))
        self.assertEqual(2, review.count('trigger_else = { always = no }'))

    def test_snapshot_has_no_economic_or_offer_state_effects(self):
        for forbidden in ('set_variable =', 'change_variable =', 'add_gold =', 'add_hook =',
                          'trigger_event =', 'add_character_flag ='):
            self.assertNotIn(forbidden, self.snapshot)
