"""Adversarial source contracts only; no CK3 price/scheduler simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def amendment_errors(t, e, obligation, service):
    errors = []
    request = block(t, 'rw_amend_request_matches_trigger')
    for guard in ('rw_service_obligation_matches_trigger = yes', 'rw_service_deferred_trigger = yes',
                  'rw_amend_parties_trigger = yes', 'exists = scope:rw_amend_serial',
                  'has_character_flag = rw_amend_pending', 'var:rw_service_price = 50',
                  'var:rw_amend_serial = scope:rw_amend_serial',
                  'var:rw_amend_proposer = scope:rw_amend_proposer', 'var:rw_amend_responder = scope:rw_amend_responder'):
        if guard not in request:
            errors.append('foreign stale or expired amendment accepted')
    context = block(t, 'rw_amend_context_trigger')
    for guard in ('rw_service_obligation_live_trigger = yes', 'rw_service_deferred_trigger = yes',
                  'has_character_flag = rw_service_deadline', 'NOT = { has_character_flag = rw_service_not_due }',
                  'var:rw_service_price = 50', 'rw_service_party_eligible_trigger = yes'):
        if guard not in context:
            errors.append('early expired or unavailable contract amended')
    for name, gate in (('rw_amend_accept_effect', 'rw_amend_accept_trigger'),
                       ('rw_amend_refuse_effect', 'rw_amend_responder_turn_trigger'),
                       ('rw_amend_withdraw_effect', 'rw_amend_withdraw_trigger')):
        if f'limit = {{ {gate} = yes }}' not in block(e, name):
            errors.append('unguarded amendment action')
    accept = block(e, 'rw_amend_accept_effect')
    order = [accept.find(x) for x in ('remove_character_flag = rw_amend_pending', 'name = rw_service_price value = 25',
                                    'rw_service_snapshot_effect = yes', 'rw_service_open_decision_effect = yes')]
    if min(order) < 0 or order != sorted(order):
        errors.append('old consent or old decision survives acceptance')
    timeout = block(obligation, 'rw_service_timeout_effect')
    refresh = timeout.find('rw_service_snapshot_effect = yes')
    for guard in ('rw_service_obligation_owner_matches_trigger = yes', 'this = scope:rw_service_provider',
                  'NOT = { has_character_flag = rw_service_deadline }'):
        if not 0 <= timeout.find(guard) < refresh:
            errors.append('timeout refresh before exact expired owner check')
    if not 0 <= refresh < timeout.find('rw_service_obligation_live_trigger = yes') < timeout.find('rw_service_affordable_trigger = yes'):
        errors.append('old price misclassifies amended timeout')
    clear = block(service, 'rw_service_clear_effect')
    for guard in ('remove_character_flag = rw_amend_pending', 'remove_character_flag = rw_amend_cooldown',
                  'remove_variable = rw_amend_proposer', 'remove_variable = rw_amend_responder'):
        if guard not in clear:
            errors.append('terminal contract leaves active amendment')
    if 'remove_variable = rw_amend_serial' in service + e:
        errors.append('amendment identity reused')
    code = clean_script(e)[0]
    if re.search(r'\b(add_gold|add_prestige|add_opinion|death|imprison|change_title_holder)\s*=', code):
        errors.append('amendment performs or punishes')
    if re.search(r'\b(?:name|flag)\s*=\s*rw_service_(serial|revision|mode|turn|delivery_days|deadline|not_due|pending)\b', code):
        errors.append('amendment changes immutable clock or contract identity')
    if re.search(r'\bremove_character_flag\s*=\s*rw_service_(obligation|deadline|not_due|pending)\b', code):
        errors.append('amendment changes immutable clock or contract identity')
    return errors


class PriceAmendmentContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_amendment_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_amendment_effects.txt').read_text()
        self.o = (MOD/'common/scripted_effects/rw_obligation_effects.txt').read_text()
        self.s = (MOD/'common/scripted_effects/rw_service_effects.txt').read_text()
        self.v = (MOD/'events/rw_amendment_events.txt').read_text()
        self.i = (MOD/'common/character_interactions/rw_amendment_interactions.txt').read_text()
        self.ov = (MOD/'events/rw_obligation_events.txt').read_text()

    def errors(self, t=None, e=None, o=None, s=None):
        return amendment_errors(self.t if t is None else t, self.e if e is None else e,
                                self.o if o is None else o, self.s if s is None else s)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_current_party_contract_serial_price_and_request_id_required(self):
        for guard in ('rw_service_obligation_matches_trigger = yes', 'rw_service_deferred_trigger = yes',
                      'rw_amend_parties_trigger = yes', 'has_character_flag = rw_amend_pending',
                      'var:rw_service_price = 50', 'var:rw_amend_serial = scope:rw_amend_serial',
                      'var:rw_amend_proposer = scope:rw_amend_proposer', 'var:rw_amend_responder = scope:rw_amend_responder'):
            self.assertIn('foreign stale or expired amendment accepted', self.errors(t=self.t.replace(guard, 'always = yes')))
        parties = block(self.t, 'rw_amend_parties_trigger')
        self.assertIn('NOT = { scope:rw_service_provider = scope:rw_service_client }', parties)
        for direction in ('provider', 'client'):
            self.assertIn(f'scope:rw_amend_proposer = scope:rw_service_{direction}', parties)

    def test_no_early_expired_dead_or_warring_amendment(self):
        for guard in ('rw_service_obligation_live_trigger = yes', 'has_character_flag = rw_service_deadline',
                      'NOT = { has_character_flag = rw_service_not_due }', 'rw_service_party_eligible_trigger = yes'):
            self.assertIn('early expired or unavailable contract amended', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertIn('this = scope:rw_amend_responder', block(self.t, 'rw_amend_responder_turn_trigger'))
        self.assertIn('rw_amend_context_trigger = yes', block(self.t, 'rw_amend_responder_turn_trigger'))

    def test_affordability_at_acceptance_not_a_refusal_prerequisite(self):
        accept = block(self.t, 'rw_amend_accept_trigger')
        self.assertIn('rw_amend_responder_turn_trigger = yes', accept)
        self.assertIn('scope:rw_service_client = { gold >= 25 }', accept)
        self.assertNotIn('gold', block(self.t, 'rw_amend_responder_turn_trigger'))
        self.assertNotIn('gold', block(self.t, 'rw_amend_withdraw_trigger'))
        self.assertIn('this = scope:rw_amend_proposer', block(self.t, 'rw_amend_withdraw_trigger'))

    def test_public_actions_revalidate_and_consumption_precedes_price_change(self):
        for gate in ('rw_amend_accept_trigger', 'rw_amend_responder_turn_trigger', 'rw_amend_withdraw_trigger'):
            self.assertIn('unguarded amendment action', self.errors(e=self.e.replace(f'limit = {{ {gate} = yes }}', 'limit = { always = yes }')))
        for guard in ('remove_character_flag = rw_amend_pending', 'rw_service_snapshot_effect = yes', 'rw_service_open_decision_effect = yes'):
            changed = self.e.replace(guard, 'always = yes')
            self.assertIn('old consent or old decision survives acceptance', self.errors(e=changed))

    def test_acceptance_changes_no_deadline_mode_service_epoch_or_assets(self):
        for bad in ('add_gold = 25', 'add_prestige = 50', 'add_opinion = yes'):
            self.assertIn('amendment performs or punishes', self.errors(e=self.e + '\n' + bad))
        for field in ('revision', 'serial', 'mode', 'turn', 'delivery_days', 'deadline', 'not_due'):
            self.assertIn('amendment changes immutable clock or contract identity', self.errors(e=self.e + f'\nset_variable = {{ name = rw_service_{field} value = 30 }}'))
        self.assertIn('amendment changes immutable clock or contract identity', self.errors(e=self.e + '\nremove_character_flag = rw_service_obligation'))
        self.assertNotIn('rw_service_clear_effect', self.e)
        self.assertEqual(1, self.e.count('name = rw_service_price value = 25'))
        self.assertNotIn('rw_service_accept_promise_effect', self.e)
        self.assertNotIn('rw_service_fulfill_promise_effect', self.e)

    def test_same_original_timeout_refreshes_current_price_after_strict_identity(self):
        for guard in ('rw_service_obligation_owner_matches_trigger = yes', 'this = scope:rw_service_provider',
                      'NOT = { has_character_flag = rw_service_deadline }'):
            self.assertIn('timeout refresh before exact expired owner check', self.errors(o=self.o.replace(guard, 'always = yes')))
        timeout = block(self.o, 'rw_service_timeout_effect')
        changed = self.o.replace('rw_service_snapshot_effect = yes', '')
        self.assertIn('old price misclassifies amended timeout', self.errors(o=changed))
        self.assertIn('has_variable = rw_service_price has_variable = rw_service_mode', timeout)
        self.assertNotIn('add_gold', timeout)
        self.assertIn('rw_service_cancel_promise_effect = yes', timeout)
        self.assertIn('rw_service_record_breach_effect = yes', timeout)

    def test_old_price_popups_fail_and_new_decision_replaces_old_ticket(self):
        service_t = (MOD/'common/scripted_triggers/rw_service_triggers.txt').read_text()
        self.assertIn('var:rw_service_price = scope:rw_service_price', block(service_t, 'rw_service_matches_trigger'))
        decisions = (MOD/'common/scripted_effects/rw_service_decision_effects.txt').read_text()
        opened = block(decisions, 'rw_service_open_decision_effect')
        self.assertLess(opened.index('rw_service_refresh_decision_effect'), opened.index('trigger_event'))
        self.assertIn('remove_character_flag = rw_service_reminder_pending', decisions)
        provider_option = self.ov[self.ov.index('name = rw_amendments.propose'):]
        provider_option = provider_option[:provider_option.index('ai_chance')]
        self.assertLess(provider_option.index('rw_service_schedule_decision_effect = { DAYS = 3 }'), provider_option.index('rw_amend_provider_propose_effect'))

    def test_amendment_and_cancellation_proposals_exclude_each_other(self):
        start = block(self.t, 'rw_amend_can_start_trigger')
        for guard in ('NOT = { has_character_flag = rw_amend_pending }',
                      'NOT = { has_character_flag = rw_amend_cooldown }', 'NOT = { has_character_flag = rw_cancel_pending }'):
            self.assertIn(guard, start)
        cancel_t = (MOD/'common/scripted_triggers/rw_cancellation_triggers.txt').read_text()
        for name in ('rw_cancel_interaction_allowed_trigger', 'rw_cancel_can_propose_trigger', 'rw_cancel_event_can_propose_trigger'):
            self.assertIn('NOT = { has_character_flag = rw_amend_pending }', block(cancel_t, name))
        # Performance remains possible under original terms while the amendment is pending.
        self.assertNotIn('rw_amend_pending', block(self.o, 'rw_service_fulfill_promise_effect'))

    def test_proposal_identity_monotonic_and_seven_day_window_not_refreshed_on_review(self):
        proposal = block(self.e, 'rw_amend_propose_effect')
        self.assertIn('NOT = { has_variable = rw_amend_serial }', proposal)
        self.assertIn('change_variable = { name = rw_amend_serial add = 1 }', proposal)
        self.assertLess(proposal.index('change_variable'), proposal.index('flag = rw_amend_pending days = 7'))
        self.assertLess(proposal.index('flag = rw_amend_pending days = 7'), proposal.index('trigger_event'))
        self.assertEqual(1, self.e.count('flag = rw_amend_pending days = 7'))
        self.assertIn('flag = rw_amend_cooldown days = 7', proposal)
        prepare = block(self.e, 'rw_amend_prepare_effect')
        self.assertIn('save_scope_value_as = { name = rw_amend_serial value = var:rw_amend_serial }', prepare)
        self.assertNotIn('add_character_flag', prepare)
        self.assertIn('amendment identity reused', self.errors(s=self.s + '\nremove_variable = rw_amend_serial'))

    def test_refusal_withdrawal_silence_and_terminal_cleanup_do_not_change_terms(self):
        for name in ('rw_amend_refuse_effect', 'rw_amend_withdraw_effect'):
            code = clean_script(block(self.e, name))[0]
            self.assertNotRegex(code, r'\b(add_character_flag|add_gold|add_prestige|trigger_event)\s*=')
            self.assertNotIn('name = rw_service_price', code)
        for guard in ('remove_character_flag = rw_amend_pending', 'remove_character_flag = rw_amend_cooldown',
                      'remove_variable = rw_amend_proposer', 'remove_variable = rw_amend_responder'):
            self.assertIn('terminal contract leaves active amendment', self.errors(s=self.s.replace(guard, '')))
        # Unchanged request token without its pending flag cannot be accepted after silence/closure.
        self.assertIn('has_character_flag = rw_amend_pending', block(self.t, 'rw_amend_request_matches_trigger'))

    def test_latest_performance_receipt_records_current_price_not_old_quote(self):
        receipt = block(self.o, 'rw_service_record_receipt_effect')
        self.assertIn('name = rw_service_last_price value = scope:rw_service_price', receipt)
        self.assertIn('remove_variable = rw_service_last_price', block(self.o, 'rw_service_cancel_promise_effect'))
        fulfill = block(self.o, 'rw_service_fulfill_promise_effect')
        self.assertLess(fulfill.index('rw_service_record_receipt_effect'), fulfill.index('rw_service_clear_effect'))
        self.assertLess(fulfill.index('rw_service_clear_effect'), fulfill.index('add_gold'))
        self.assertIn('add_gold = scope:rw_service_price', fulfill)
        self.assertIn('scope:rw_service_price = 25 } desc = rw_delivery.price_25', self.ov)
        self.assertIn('scope:rw_service_price = 50 } desc = rw_delivery.price_50', self.ov)

    def test_both_menu_directions_map_exact_partners_and_open_no_consent(self):
        for name, mapping in (('rw_provider_price_amendment_interaction', 'PROVIDER = scope:actor CLIENT = scope:recipient'),
                              ('rw_client_price_amendment_interaction', 'PROVIDER = scope:recipient CLIENT = scope:actor')):
            menu = block(self.i, name)
            self.assertIn('auto_accept = yes', menu)
            self.assertIn(mapping, menu)
            self.assertNotIn('rw_amend_accept_effect', menu)
        self.assertIn('this = scope:rw_amend_proposer', block(self.e, 'rw_amend_propose_effect'))
        pair = block(self.t, 'rw_amend_interaction_pair_trigger')
        self.assertIn('var:rw_service_target = $CLIENT$', pair)
        for field in ('serial', 'revision', 'price', 'mode'):
            self.assertIn('has_variable = rw_service_' + field, pair)
        self.assertIn('exists = var:rw_amend_proposer', pair)
        self.assertIn('exists = var:rw_amend_responder', pair)

    def test_bounded_ai_opportunities_both_parties_share_same_effects(self):
        acceptance = block(self.o, 'rw_service_accept_promise_effect')
        self.assertEqual(1, acceptance.count('id = rw_amendments.0002 days = 8'))
        hidden = block(self.v, 'rw_amendments.0002')
        self.assertIn('rw_amend_can_start_trigger = yes this = scope:rw_service_client', hidden)
        self.assertNotIn('days =', hidden)
        self.assertIn('rw_amend_provider_propose_effect = yes', self.ov)
        self.assertIn('rw_amend_client_propose_effect = yes', self.v)
        self.assertNotRegex(clean_script(self.t + self.e + self.v)[0], r'\b(is_ai|is_human|every_living_character|every_house_member)\s*=')
        self.assertNotIn('rw_obligations.0002', self.e)
        self.assertEqual(1, self.o.count('id = rw_obligations.0002 days = 15'))
        self.assertEqual(1, self.o.count('id = rw_obligations.0002 days = 31'))

    def test_localization_full_terms_identity_delivery_and_all_graph_edges(self):
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_amendments\.[\w.]+)', self.v + self.i + self.ov))
        keys.update(('rw_provider_price_amendment_interaction', 'rw_client_price_amendment_interaction'))
        for lang in ('english','french'):
            p = MOD/f'localization/{lang}/rw_amendments_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            loc = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', loc, re.M)))
            for alias in ('rw_amend_proposer', 'rw_amend_responder', 'rw_service_provider', 'rw_service_client'):
                self.assertIn('[' + alias + '.GetTitledFirstName]', loc)
            self.assertIn('50', loc)
            self.assertIn('25', loc)
        request = block(self.v, 'rw_amendments.0001')
        self.assertIn('rw_delivery.days_14', request)
        self.assertIn('rw_delivery.days_30', request)
        self.assertIn('this = scope:rw_amend_proposer this = scope:rw_amend_responder', request)

    def test_no_native_sanction_status_crime_or_standby_source_dependency(self):
        code = clean_script(self.e + self.t + self.v + self.i)[0]
        self.assertNotRegex(code, r'\b(run_interaction|set_house|set_dynasty|add_trait|remove_trait|change_title_holder|add_secret|imprison|death)\s*=')
        self.assertNotIn('rw_g3', code)
        self.assertNotIn('rw_house_', code)
