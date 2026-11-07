"""Source contracts for personality, original-party context and unchanged actions."""
from pathlib import Path
import hashlib
import re
import unittest

from test_deferred_service_contract import block
from test_political_ai import option
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'
FAMILIES = (
    ('gold_promise_perform', 'gold', 'rw_service_obligation_fulfillable_trigger', 'rw_service_provider', 'rw_service_client', 70, 'keep'),
    ('gold_promise_break', 'gold', 'rw_service_obligation_actionable_trigger', 'rw_service_provider', 'rw_service_client', 10, 'break'),
    ('favor_promise_perform', 'favor', 'rw_fd_can_perform_trigger', 'rw_fv_provider', 'rw_fv_client', 70, 'keep'),
    ('favor_promise_renounce', 'favor', 'rw_fd_can_renounce_trigger', 'rw_fv_provider', 'rw_fv_client', 5, 'break'),
)


def policy_errors(values):
    errors = []
    for name, context, guard, provider, client, base, intent in FAMILIES:
        body = block(values, 'rw_ai_'+name+'_weight')
        required = ('value = 0', 'rw_ai_'+context+'_promise_context_trigger = yes',
                    guard+' = yes', 'this = scope:'+provider, 'add = '+str(base),
                    'multiply = rw_ai_'+intent+'_word_factor',
                    'target = scope:'+client+' value >= 25',
                    'target = scope:'+client+' value <= -25')
        if any(fragment not in body for fragment in required):
            errors.append(name)
    return errors


def action_digest(text):
    """Keep the executable event graph while removing its AI weights."""
    text = clean_script(text)[0]
    spans = []
    for match in re.finditer(r'\bai_chance\s*=\s*\{', text):
        start = text.index('{', match.start())
        end, depth = start + 1, 1
        while depth:
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        spans.append((match.start(), end))
    for start, end in reversed(spans):
        text = text[:start] + text[end:]
    return hashlib.sha256(re.sub(r'\s+', '', text).encode()).hexdigest()


class PromisePolicyTests(unittest.TestCase):
    def setUp(self):
        self.values = (MOD/'common/script_values/rw_promise_ai_values.txt').read_text(encoding='utf-8-sig')
        self.triggers = (MOD/'common/scripted_triggers/rw_political_ai_triggers.txt').read_text(encoding='utf-8-sig')
        self.gold = (MOD/'events/rw_obligation_events.txt').read_text(encoding='utf-8-sig')
        self.favor = (MOD/'events/rw_favor_service_events.txt').read_text(encoding='utf-8-sig')

    def test_native_axes_have_opposite_word_preferences_and_positive_bounds(self):
        keep = block(self.values, 'rw_ai_keep_word_factor')
        breaking = block(self.values, 'rw_ai_break_word_factor')
        for body in (keep, breaking):
            for fragment in ('value = ai_honor', 'divide = 100', 'add = 1', 'min = 0.25', 'max = 2'):
                self.assertIn(fragment, body)
            self.assertLess(body.index('divide = 100'), body.index('add = 1'))
            self.assertLess(body.index('add = 1'), body.index('min = 0.25'))
        self.assertNotIn('multiply = -1', keep)
        self.assertIn('multiply = -1', breaking)
        self.assertLess(breaking.index('multiply = -1'), breaking.index('divide = 100'))
        reward = block(self.values, 'rw_ai_paid_reward_factor')
        for fragment in ('value = ai_greed', 'divide = 200', 'add = 1', 'min = 0.5', 'max = 1.5'):
            self.assertIn(fragment, reward)
        self.assertNotIn('has_trait', self.values)
        self.assertNotIn('scope:', keep+breaking+reward)
        self.assertTrue((MOD/'common/script_values/rw_promise_ai_values.txt').read_bytes().startswith(b'\xef\xbb\xbf'))

    def test_original_provider_context_and_family_guards_are_required(self):
        self.assertEqual([], policy_errors(self.values))
        for name, context, guard, provider, client, _, _ in FAMILIES:
            with self.subTest(name=name):
                changed = self.values.replace(guard+' = yes', 'always = yes', 1)
                self.assertIn(name, policy_errors(changed))
                body = block(self.values, 'rw_ai_'+name+'_weight')
                changed_body = body.replace('this = scope:'+provider, 'this = scope:'+client, 1)
                self.assertNotEqual(body, changed_body)
                self.assertIn(name, policy_errors(self.values.replace(body, changed_body)))
                changed_body = body.replace('rw_ai_'+context+'_promise_context_trigger = yes', 'always = yes', 1)
                self.assertIn(name, policy_errors(self.values.replace(body, changed_body)))

    def test_complete_frame_precedes_party_checks_and_missing_context_fails_closed(self):
        for family, prefix, fields in (
            ('gold', 'rw_service', ('provider', 'client', 'serial', 'revision', 'price', 'mode', 'decision_serial')),
            ('favor', 'rw_fv', ('provider', 'client', 'serial', 'revision', 'term', 'mode')),
        ):
            context = block(self.triggers, 'rw_ai_'+family+'_promise_context_trigger')
            for field in fields:
                self.assertIn('exists = scope:'+prefix+'_'+field, block(context, 'limit'))
            self.assertIn('this = scope:'+prefix+'_provider', context)
            self.assertIn('trigger_else = { always = no }', context)

    def test_reward_uses_current_quote_and_favor_money_term_only(self):
        gold = block(self.values, 'rw_ai_gold_promise_perform_weight')
        self.assertIn('gold < scope:rw_service_price', gold)
        favor = block(self.values, 'rw_ai_favor_promise_perform_weight')
        gate = favor.index('limit = { scope:rw_fv_term = flag:gold25 }')
        self.assertLess(gate, favor.index('multiply = rw_ai_paid_reward_factor'))
        self.assertLess(gate, favor.index('gold < 25'))
        renounce = block(self.values, 'rw_ai_favor_promise_renounce_weight')
        self.assertLess(renounce.index('scope:rw_fv_client = { is_alive = yes }'),
                        renounce.index('multiply = rw_ai_break_word_factor'))

    def test_counterpart_opinion_cannot_be_substituted_by_beneficiary_or_owner(self):
        for name, _, _, provider, client, _, _ in FAMILIES:
            body = block(self.values, 'rw_ai_'+name+'_weight')
            changed = body.replace('target = scope:'+client, 'target = scope:'+provider)
            self.assertIn(name, policy_errors(self.values.replace(body, changed)))

    def test_four_choices_use_profiles_and_other_event_actions_are_preserved(self):
        for text, name, profile in (
            (self.gold, 'rw_obligations.fulfill', 'gold_promise_perform'),
            (self.gold, 'rw_obligations.break', 'gold_promise_break'),
            (self.favor, 'rw_deferred_favor.perform', 'favor_promise_perform'),
            (self.favor, 'rw_deferred_favor.renounce', 'favor_promise_renounce'),
        ):
            chance = block(option(text, name), 'ai_chance')
            self.assertIn('base = 0', chance)
            self.assertIn('add = rw_ai_'+profile+'_weight', chance)
        # Own event graph at5617c9, preserving costs, guards, timers and outcomes.
        self.assertEqual('3e937926b1425d3141b471efb5a8ea27f39c6bcd1fbbb195221fd4e9ee025ea5', action_digest(self.gold))
        self.assertEqual('a0f079aa0e9ab8700a00add3c2248e17948dc81f809b84f027ca315664f91cc3', action_digest(self.favor))
        self.assertNotEqual(action_digest(self.gold), action_digest(self.gold.replace('rw_service_fulfill_promise_effect = yes', 'rw_service_break_promise_effect = yes', 1)))

    def test_values_are_read_only_and_do_not_use_hidden_or_global_information(self):
        text = clean_script(self.values)[0]
        for forbidden in ('set_variable', 'save_scope', 'add_gold', 'add_opinion', 'trigger_event',
                          'create_story', 'has_secret', 'global_var', 'every_', 'any_living', 'is_ai ='):
            self.assertNotIn(forbidden, text)
