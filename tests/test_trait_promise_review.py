"""Symbolic directions for the existing promise axes, with synthetic trait inputs."""

from pathlib import Path
import re
import unittest

from tools.audit_trait_context import promise_axis_review, promise_markdown, read_traits
from test_promise_ai_policy import action_digest, policy_errors


ROOT = Path(__file__).resolve().parents[1]


def review(fields):
    row, = read_traits('example = { category = personality ' + fields + ' }', 'CK3', 'traits.txt')
    return row, row['promise_axis_review']


class TraitPromiseReviewTests(unittest.TestCase):
    def test_honor_and_reward_directions_are_separate(self):
        _, result = review('ai_honor = 20 ai_greed = -35')
        self.assertEqual('mixed', result['gold_perform'])
        self.assertEqual('mixed', result['favor_perform_gold25'])
        self.assertEqual('nondecreasing', result['favor_perform_hook'])
        self.assertEqual('nonincreasing', result['gold_break'])
        self.assertEqual('nonincreasing', result['favor_renounce_living'])

    def test_neutral_axes_do_not_establish_neutral_context(self):
        row, result = review('ai_boldness = 50 diplomacy = 2')
        self.assertEqual({'zero_direct'}, set(result.values()))
        self.assertEqual('pending', row['context_review'])
        self.assertEqual(2, row['direct_personal_fields']['diplomacy'])

    def test_single_and_aligned_axes_have_monotone_not_strict_directions(self):
        for fields, direction in (
            ('ai_honor = 20 ai_greed = 35', 'nondecreasing'),
            ('ai_honor = -20 ai_greed = -35', 'nonincreasing'),
            ('ai_greed = -35', 'nonincreasing'),
        ):
            _, result = review(fields)
            self.assertEqual(direction, result['gold_perform'])

    def test_unresolved_greed_does_not_contaminate_honor_only_or_deceased_options(self):
        _, result = review('ai_honor = 20 modifier = { ai_greed = scripted_value }')
        self.assertEqual('unresolved', result['gold_perform'])
        self.assertEqual('nonincreasing', result['gold_break'])
        self.assertEqual('nondecreasing', result['favor_perform_hook'])
        self.assertEqual('zero_direct', result['favor_renounce_deceased'])

    def test_unresolved_honor_cannot_be_reported_as_zero(self):
        _, result = review('ai_honor = scripted_value')
        self.assertEqual('unresolved', result['gold_perform'])
        self.assertEqual('unresolved', result['gold_break'])

    def test_private_report_retains_scope_and_excludes_nonpersonality(self):
        person, _ = review('ai_honor = 20')
        technical, = read_traits('hidden = { ai_honor = 20 }', 'AGOT', 'traits.txt')
        rendered = promise_markdown({'traits': [person, technical]})
        self.assertIn('`example`', rendered)
        self.assertNotIn('`hidden`', rendered)
        self.assertIn('Validation moteur en attente', rendered)
        self.assertIn('opinions, moyens', rendered)

    def test_symbolic_mapping_is_tied_to_current_owned_policy_and_unchanged_actions(self):
        values = (ROOT/'mod/real_westeros/common/script_values/rw_promise_ai_values.txt').read_text(encoding='utf-8-sig')
        self.assertEqual([], policy_errors(values))
        self.assertEqual({'ai_honor', 'ai_greed'}, set(re.findall(r'\bai_(?:honor|greed|boldness|compassion|energy|rationality|sociability|vengefulness|zeal)\b', values)))
        for filename, expected in (
            ('rw_obligation_events.txt', '3e937926b1425d3141b471efb5a8ea27f39c6bcd1fbbb195221fd4e9ee025ea5'),
            ('rw_favor_service_events.txt', 'a0f079aa0e9ab8700a00add3c2248e17948dc81f809b84f027ca315664f91cc3'),
        ):
            self.assertEqual(expected, action_digest((ROOT/'mod/real_westeros/events'/filename).read_text(encoding='utf-8-sig')))


if __name__ == '__main__':
    unittest.main()
