"""Role, amount and consent contracts for the original compensation UI."""

import hashlib
from pathlib import Path
import unittest

from test_deferred_service_contract import block
from test_political_ai import option
from test_promise_ai_policy import action_digest
from tools.validate_mod import clean_script
from tools.audit_trait_context import compensation_markdown, read_traits


MOD = Path(__file__).resolve().parents[1]/'mod/real_westeros'
CHOICES = (('propose_25', 2), ('propose_50', 1), ('accept', 60),
           ('counter', 10), ('close', 10), ('appreciate', 50), ('note', 50))


class CompensationAIPolicyTests(unittest.TestCase):
    def setUp(self):
        self.values = (MOD/'common/script_values/rw_compensation_ai_values.txt').read_text(encoding='utf-8-sig')
        self.triggers = (MOD/'common/scripted_triggers/rw_compensation_ai_triggers.txt').read_text(encoding='utf-8-sig')
        self.events = (MOD/'events/rw_case_compensation_events.txt').read_text(encoding='utf-8-sig')

    def test_all_seven_options_consume_guarded_zero_default_profiles(self):
        for name, base in CHOICES:
            body = block(self.values, 'rw_ai_compensation_'+name+'_weight')
            self.assertTrue(body.strip().startswith('value = 0'))
            self.assertIn('add = '+str(base), body)
            prefix = 'rw_compensation_response.' if name in ('appreciate', 'note') else 'rw_case_compensation.'
            chance = block(option(self.events, prefix+name), 'ai_chance')
            self.assertIn('add = rw_ai_compensation_'+name+'_weight', chance)

    def test_case_identity_precedes_quote_and_paid_response_validation(self):
        case = block(self.triggers, 'rw_ai_compensation_case_context_trigger')
        for field in ('rw_service_provider','rw_service_client','rw_case_record','rw_case_mediator',
                      'rw_case_serial','rw_case_reason','rw_case_kind'):
            self.assertIn('exists = scope:'+field, block(case, 'limit'))
        self.assertIn('rw_cc_base_trigger = yes', case)
        quote = block(self.triggers, 'rw_ai_compensation_quote_context_trigger')
        for fragment in ('rw_ai_compensation_case_context_trigger = yes','exists = scope:rw_cc_revision','exists = scope:rw_cc_price'):
            self.assertIn(fragment, block(quote, 'limit'))
        self.assertIn('rw_cc_view_trigger = yes', quote)
        paid = block(self.triggers, 'rw_ai_compensation_response_context_trigger')
        self.assertIn('this = scope:rw_service_client', paid)
        self.assertIn('rw_cp_can_respond_trigger = yes', paid)
        for body in (case, quote, paid):
            self.assertIn('trigger_else = { always = no }', body)

    def test_original_affordability_and_turn_gates_are_still_consumed(self):
        gates = {'propose_25':'rw_cc_can_propose_trigger','propose_50':'rw_cc_can_propose_trigger',
                 'accept':'rw_cc_can_settle_trigger','counter':'rw_cc_responder_trigger','close':'rw_cc_can_close_trigger'}
        for name, gate in gates.items():
            body = block(self.values, 'rw_ai_compensation_'+name+'_weight')
            self.assertIn('limit = { '+gate+' = yes }', body)
        for amount in (25, 50):
            body = block(self.values, 'rw_ai_compensation_price_'+str(amount)+'_factor')
            self.assertIn('scope:rw_service_provider = { gold >= '+str(amount)+' }', body)
            self.assertIn('rw_cc_context_trigger = yes', body)
            self.assertIn('gold < '+str(amount*2), body)
            self.assertIn('this = scope:rw_service_provider', body)
            reward = 'rw_ai_compensation_receive_25_factor' if amount == 25 else 'rw_ai_paid_reward_factor'
            self.assertIn('multiply = '+reward, body)
        self.assertNotIn('rw_service_price', self.values)

    def test_accept_uses_displayed_amount_but_counter_scores_the_opposite_amount(self):
        accept = block(self.values, 'rw_ai_compensation_accept_weight')
        counter = block(self.values, 'rw_ai_compensation_counter_weight')
        self.assertIn('scope:rw_cc_price = 25 } multiply = rw_ai_compensation_price_25_factor', accept)
        self.assertIn('else = { multiply = rw_ai_compensation_price_50_factor }', accept)
        self.assertIn('scope:rw_cc_price = 25 } multiply = rw_ai_compensation_price_50_factor', counter)
        self.assertIn('else = { multiply = rw_ai_compensation_price_25_factor }', counter)
        self.assertIn('this = scope:rw_service_provider scope:rw_cc_price = 50', counter)
        self.assertIn('this = scope:rw_service_client scope:rw_cc_price = 25', counter)
        self.assertIn('gold < scope:rw_cc_price', counter)

    def test_payer_cost_and_recipient_reward_have_opposite_greed_directions(self):
        for amount, divisor in ((25,400),(50,200)):
            body = block(self.values, 'rw_ai_compensation_spend_'+str(amount)+'_factor')
            for fragment in ('value = ai_greed','multiply = -1','divide = '+str(divisor),'min = 0.5','max = 1.5'):
                self.assertIn(fragment, body)
        conciliation = block(self.values, 'rw_ai_compensation_conciliation_factor')
        self.assertIn('value = ai_honor', conciliation)
        self.assertIn('add = ai_compassion', conciliation)
        self.assertNotIn('scope:', conciliation)
        receiving = block(self.values, 'rw_ai_compensation_receive_25_factor')
        self.assertIn('value = ai_greed', receiving)
        self.assertIn('divide = 400', receiving)
        self.assertNotIn('multiply = -1', receiving)

    def test_prior_repair_belongs_to_this_case_without_reconstructing_damage_or_history(self):
        for name in ('price_25_factor','price_50_factor','propose_50_weight','counter_weight'):
            body = block(self.values, 'rw_ai_compensation_'+name)
            self.assertIn('scope:rw_case_record = { var:rw_case_result = flag:repaired }', body)
        for forbidden in ('rw_service_last_', 'rw_service_price', 'rw_case_service_price', 'rw_fr_capacity'):
            self.assertNotIn(forbidden, self.values)

    def test_close_and_leave_remain_possible_after_expiry_or_lost_capacity(self):
        body = block(self.values, 'rw_ai_compensation_close_weight')
        self.assertIn('NOT = { rw_cc_offer_live_trigger = yes }', body)
        self.assertIn('scope:rw_service_provider = { gold < 25 }', body)
        self.assertNotIn('rw_cc_can_settle_trigger', body)
        self.assertIn('option = { name = rw_case_compensation.leave ai_chance = { base = 50 } }', self.events)

    def test_cash_acceptance_does_not_require_personal_appreciation(self):
        for name in ('accept_weight','price_25_factor','price_50_factor'):
            body = block(self.values, 'rw_ai_compensation_'+name)
            for forbidden in ('rw_cp_', 'forgiveness', 'resentment', 'ai_vengefulness'):
                self.assertNotIn(forbidden, body)
        for name in ('appreciate','note'):
            body = block(self.values, 'rw_ai_compensation_'+name+'_weight')
            self.assertIn('rw_ai_compensation_response_context_trigger = yes', body)
        self.assertNotIn('rw_ai_compensation_price_', block(self.values, 'rw_ai_compensation_note_weight'))

    def test_transaction_and_response_effects_and_event_action_graph_are_identical(self):
        self.assertEqual('03a80fb61962d6a8682c91fc1ce550280d5b8645673f81c3d5afa22199711c4f', action_digest(self.events))
        for filename, digest in (
            ('rw_case_compensation_effects.txt','c759f9ace01ece7fc0254b46444ef2c89568fd3408c299ca18f67703e0c09f52'),
            ('rw_compensation_response_effects.txt','f25f26150afd872104f7ed00db89d0611c206aad43d25f7822cb8d215a9195d5'),
        ):
            self.assertEqual(digest, hashlib.sha256((MOD/'common/scripted_effects'/filename).read_bytes()).hexdigest())

    def test_policy_cannot_change_money_deadlines_authority_or_private_facts(self):
        code = clean_script(self.values+self.triggers)[0]
        for forbidden in ('set_variable','change_variable','add_gold','remove_short_term_gold','add_opinion',
                          'trigger_event','has_secret','has_trait','is_ai =','every_','create_story'):
            self.assertNotIn(forbidden, code)

    def test_isolated_cost_arithmetic_preserves_feasible_cheaper_counter(self):
        # Boundary examples only, not an engine-state simulator or probabilities.
        for provider_gold in (0,24,25,49,50,99,100):
            feasible25, feasible50 = provider_gold >= 25, provider_gold >= 50
            if 25 <= provider_gold < 50:
                self.assertTrue(feasible25)
                self.assertFalse(feasible50)
            self.assertEqual(50,2*25)
            self.assertEqual(100,2*50)
        for greed in (-100,0,100):
            spend25 = min(1.5,max(.5,1-greed/400))
            spend50 = min(1.5,max(.5,1-greed/200))
            self.assertGreater(spend25,0)
            self.assertGreater(spend50,0)
            if greed > 0:
                self.assertLess(spend50,spend25)

    def test_private_trait_review_separates_payer_recipient_and_later_appreciation(self):
        row, = read_traits('example = { category = personality ai_greed = 50 ai_vengefulness = 50 }', 'CK3', 'traits.txt')
        result = row['financial_repair_axis_review']
        self.assertEqual('nonincreasing', result['payer_payment'])
        self.assertEqual('nondecreasing', result['client_receive'])
        self.assertEqual('nonincreasing', result['client_appreciate'])
        self.assertEqual('nondecreasing', result['client_note'])
        text = compensation_markdown({'traits': [row]})
        self.assertIn('`example`', text)
        self.assertIn('La contre-offre change de montant', text)
        self.assertIn('Validation moteur en attente', text)


if __name__ == '__main__':
    unittest.main()
