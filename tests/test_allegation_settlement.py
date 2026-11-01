"""Source-contract mutations for paid allegation withdrawal; no CK3 simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/real_westeros'


def settlement_errors(t, e):
    errors = []
    def need(body, parts, message):
        if any(p not in body for p in parts): errors.append(message)
    need(block(t, 'rw_as_base_trigger'), (
        'rw_case_matches_trigger = yes', 'is_alive = yes',
        'OR = { this = scope:rw_service_provider this = scope:rw_service_client }',
        'NOT = { scope:rw_service_provider = scope:rw_service_client }',
        'var:rw_case_kind = flag:allegation'), 'foreign story or reader')
    need(block(t, 'rw_as_context_trigger'), (
        'rw_case_jurisdiction_trigger = yes', 'is_imprisoned = no',
        'NOT = { is_at_war_with = scope:rw_service_client }',
        'var:rw_case_stage = flag:claimant', 'has_variable = rw_case_pending',
        'NOT = { has_variable = rw_case_disclosed }',
        'OR = { var:rw_case_evidence = flag:admitted var:rw_case_evidence = flag:contested }'),
        'expired referred or invalid case settles')
    if block(t, 'rw_as_context_trigger').count('is_imprisoned = no') != 2:
        errors.append('expired referred or invalid case settles')
    need(block(t, 'rw_as_can_propose_trigger'), (
        'rw_as_base_trigger = yes', 'rw_as_context_trigger = yes',
        'this = scope:rw_service_client', 'NOT = { has_variable = rw_as_schema }'),
        'wrong initiator or repeated proposal')
    need(block(t, 'rw_as_view_trigger'), (
        'rw_as_base_trigger = yes', 'exists = scope:rw_as_revision', 'exists = scope:rw_as_price',
        'var:rw_as_schema = 1', 'var:rw_as_revision = scope:rw_as_revision',
        'var:rw_as_price = scope:rw_as_price', 'has_variable = rw_as_issued_on',
        'OR = { var:rw_as_price = 25 var:rw_as_price = 50 }',
        'OR = { var:rw_as_turn = flag:provider var:rw_as_turn = flag:client }',
        'has_variable = rw_as_paid_on', 'var:rw_as_paid_revision = scope:rw_as_revision',
        'var:rw_as_paid_amount = scope:rw_as_price', 'var:rw_case_result = flag:withdrawn'),
        'stale price revision or paid receipt')
    need(block(t, 'rw_as_live_trigger'), (
        'rw_as_view_trigger = yes', 'rw_as_context_trigger = yes',
        'var:rw_as_state = flag:offered', 'has_variable = rw_as_window'), 'inactive offer spends')
    need(block(t, 'rw_as_responder_trigger'), (
        'rw_as_live_trigger = yes',
        'AND = { this = scope:rw_service_provider scope:rw_case_record = { var:rw_as_turn = flag:provider } }',
        'AND = { this = scope:rw_service_client scope:rw_case_record = { var:rw_as_turn = flag:client } }'),
        'proposer or outsider self accepts')
    need(block(t, 'rw_as_can_settle_trigger'), (
        'rw_as_responder_trigger = yes', 'scope:rw_service_provider = { gold >= scope:rw_as_price }'),
        'wrong payer or missing current funds')
    propose = block(e, 'rw_as_propose_effect')
    need(propose, ('limit = { rw_as_can_propose_trigger = yes }',
        'name = rw_as_revision value = 0', 'name = rw_as_price value = 50',
        'name = rw_as_turn value = flag:provider', 'name = rw_as_state value = flag:offered',
        'name = rw_as_window value = flag:yes days = 7', 'name = rw_as_schema value = 1'),
        'unguarded proposal or mutable deadline')
    counter = block(e, 'rw_as_counter_effect')
    need(counter, ('limit = { rw_as_responder_trigger = yes }',
        'change_variable = { name = rw_as_revision add = 1 }',
        'name = rw_as_price value = 25', 'name = rw_as_price value = 50',
        'name = rw_as_turn value = flag:client', 'name = rw_as_turn value = flag:provider',
        'rw_as_snapshot_effect = yes'), 'counter keeps stale consent')
    for b in (propose, counter):
        if re.search(r'\b(add_gold|add_opinion|rw_case_close_effect)\s*=', clean_script(b)[0]):
            errors.append('negotiation charges or withdraws early')
    settle = block(e, 'rw_as_settle_effect')
    need(settle, ('limit = { rw_as_can_settle_trigger = yes }', 'remove_variable = rw_as_window',
        'remove_variable = rw_as_turn', 'name = rw_as_paid_amount value = scope:rw_as_price',
        'name = rw_as_paid_revision value = scope:rw_as_revision', 'name = rw_as_paid_on value = current_date',
        'name = rw_as_state value = flag:paid', 'remove_variable = rw_case_pending',
        'name = rw_case_retained value = flag:yes days = 1825',
        'name = rw_case_stage value = flag:closed', 'name = rw_case_result value = flag:withdrawn'),
        'settlement not consumed or unsupported withdrawal')
    points = [settle.find(p) for p in ('name = rw_as_state value = flag:paid',
        'remove_variable = rw_case_pending', 'name = rw_case_stage value = flag:closed',
        'scope:rw_service_provider = { add_gold = { value = scope:rw_as_price multiply = -1 } }',
        'scope:rw_service_client = { add_gold = scope:rw_as_price }', 'rw_as_notify_effect = yes')]
    if min(points) < 0 or points != sorted(points): errors.append('wrong payment direction or premature notice')
    closing = block(e, 'rw_as_close_effect')
    need(closing, ('limit = { rw_as_can_close_trigger = yes }', 'remove_variable = rw_as_window',
        'remove_variable = rw_as_turn', 'name = rw_as_state value = flag:closed'), 'refusal not consumed')
    if re.search(r'\b(add_gold|add_opinion|rw_case_close_effect)\s*=|name\s*=\s*rw_case_', clean_script(closing)[0]):
        errors.append('refusal charges or withdraws')
    code = clean_script(e)[0]
    if re.search(r'\bname\s*=\s*(rw_case_evidence|rw_case_disclosed|rw_cc_\w+|rw_cp_\w+|rw_service_\w+)', code):
        errors.append('facts disclosure or unrelated contract rewritten')
    if re.search(r'\b(add_hook|remove_hook|add_secret|add_opinion|add_prestige|imprison|run_interaction|every_living_character|change_title_holder)\s*=', code):
        errors.append('native punishment or global scan')
    return errors


class AllegationSettlementTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_allegation_settlement_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_allegation_settlement_effects.txt').read_text()
        self.ev = (MOD/'events/rw_allegation_settlement_events.txt').read_text()

    def errors(self, t=None, e=None):
        return settlement_errors(self.t if t is None else t, self.e if e is None else e)

    def test_source_contract(self): self.assertEqual([], self.errors())

    def test_only_exact_allegation_and_original_private_parties(self):
        for g in ('rw_case_matches_trigger = yes', 'var:rw_case_kind = flag:allegation',
                  'OR = { this = scope:rw_service_provider this = scope:rw_service_client }'):
            self.assertIn('foreign story or reader', self.errors(t=self.t.replace(g, 'always = yes')))
        native = (MOD/'common/scripted_triggers/rw_case_triggers.txt').read_text()
        for g in ('story_type = story_rw_political_case', 'story_owner = scope:rw_service_provider',
                  'var:rw_case_client = scope:rw_service_client', 'var:rw_case_kind = scope:rw_case_kind'):
            self.assertIn(g, block(native, 'rw_case_matches_trigger'))

    def test_disclosure_jurisdiction_deadline_and_stage_rechecked(self):
        for g in ('rw_case_jurisdiction_trigger = yes', 'var:rw_case_stage = flag:claimant',
                  'has_variable = rw_case_pending', 'NOT = { has_variable = rw_case_disclosed }', 'is_imprisoned = no'):
            self.assertIn('expired referred or invalid case settles', self.errors(t=self.t.replace(g, 'always = yes')))

    def test_acknowledgment_and_contest_eligible_but_unanswered_is_not(self):
        self.assertIn('var:rw_case_evidence = flag:admitted var:rw_case_evidence = flag:contested', block(self.t, 'rw_as_context_trigger'))
        self.assertNotIn('flag:unanswered', self.t)
        self.assertIn('expired referred or invalid case settles', self.errors(t=self.t.replace('flag:contested', 'flag:unanswered')))

    def test_claimant_initiates_only_one_window_per_case(self):
        for g in ('this = scope:rw_service_client', 'NOT = { has_variable = rw_as_schema }'):
            self.assertIn('wrong initiator or repeated proposal', self.errors(t=self.t.replace(g, 'always = yes')))
        self.assertEqual(1, len(re.findall(r'name\s*=\s*rw_as_schema\b', self.e)))

    def test_captured_version_price_and_typed_paid_receipt(self):
        for g in ('exists = scope:rw_as_revision', 'var:rw_as_revision = scope:rw_as_revision',
                  'var:rw_as_price = scope:rw_as_price', 'var:rw_as_paid_amount = scope:rw_as_price',
                  'var:rw_as_paid_revision = scope:rw_as_revision', 'has_variable = rw_as_paid_on'):
            self.assertIn('stale price revision or paid receipt', self.errors(t=self.t.replace(g, 'always = yes')))

    def test_only_current_other_party_can_accept_or_counter(self):
        g = 'AND = { this = scope:rw_service_provider scope:rw_case_record = { var:rw_as_turn = flag:provider } }'
        self.assertIn('proposer or outsider self accepts', self.errors(t=self.t.replace(g, 'always = yes')))
        self.assertIn('inactive offer spends', self.errors(t=self.t.replace('has_variable = rw_as_window', 'always = yes')))
        self.assertIn('wrong payer or missing current funds', self.errors(t=self.t.replace('rw_as_responder_trigger = yes', 'always = yes')))

    def test_current_respondent_gold_always_funds_agreed_price(self):
        g = 'scope:rw_service_provider = { gold >= scope:rw_as_price }'
        self.assertIn('wrong payer or missing current funds', self.errors(t=self.t.replace(g, 'scope:rw_service_client = { gold >= 50 }')))
        self.assertEqual(2, len(re.findall(r'\badd_gold\s*=', self.e)))
        self.assertIn('wrong payment direction or premature notice', self.errors(e=self.e.replace('multiply = -1', 'multiply = 1')))

    def test_no_payment_or_case_closure_at_proposal_counter(self):
        for g in ('rw_as_propose_effect = {', 'rw_as_counter_effect = {'):
            self.assertIn('negotiation charges or withdraws early', self.errors(e=self.e.replace(g, g+' add_gold = -50')))
        self.assertIn('unguarded proposal or mutable deadline', self.errors(e=self.e.replace('limit = { rw_as_can_propose_trigger = yes }', 'limit = { always = yes }')))

    def test_counter_invalidates_consent_before_capturing_new_terms(self):
        self.assertIn('counter keeps stale consent', self.errors(e=self.e.replace('change_variable = { name = rw_as_revision add = 1 }', '')))
        b = block(self.e, 'rw_as_counter_effect')
        self.assertLess(b.index('name = rw_as_revision'), b.index('rw_as_snapshot_effect = yes'))
        self.assertLess(b.index('rw_as_snapshot_effect = yes'), b.index('rw_as_send_reply_effect = yes'))

    def test_offer_and_case_clocks_are_not_renewed_by_counters_or_review(self):
        self.assertEqual(1, len(re.findall(r'name\s*=\s*rw_as_window\b', self.e)))
        self.assertNotRegex(self.e, r'name\s*=\s*rw_case_pending\b')
        self.assertIn('unguarded proposal or mutable deadline', self.errors(e=self.e.replace('days = 7', 'days = 30')))
        for name in ('rw_as_counter_effect', 'rw_as_prepare_effect', 'rw_as_notify_effect'):
            self.assertNotRegex(block(self.e, name), r'\b(?:days|months|years)\s*=')

    def test_both_offer_and_case_consumed_before_gold_and_notices(self):
        for g in ('remove_variable = rw_as_window', 'remove_variable = rw_case_pending',
                  'name = rw_case_stage value = flag:closed', 'name = rw_as_paid_amount value = scope:rw_as_price'):
            self.assertIn('settlement not consumed or unsupported withdrawal', self.errors(e=self.e.replace(g, 'removed')))
        self.assertIn('wrong payment direction or premature notice', self.errors(e=self.e.replace('name = rw_as_state value = flag:paid', 'removed')))

    def test_original_withdrawal_and_referral_remain_free_and_invalidate_live_offer(self):
        allegations = (MOD/'common/scripted_effects/rw_allegation_effects.txt').read_text()
        for name in ('rw_allegation_withdraw_effect', 'rw_allegation_refer_effect'):
            b = block(allegations, name)
            self.assertNotRegex(b, r'\brw_as_|\badd_gold\s*=')
        for name, effect in (('refer', 'rw_allegation_refer_effect'), ('withdraw', 'rw_allegation_withdraw_effect')):
            self.assertIn('name = rw_allegations.'+name, self.ev)
            self.assertIn(effect+' = yes', self.ev)
        self.assertIn('var:rw_case_stage = flag:claimant', block(self.t, 'rw_as_context_trigger'))

    def test_declining_talks_does_not_withdraw_or_pay(self):
        self.assertIn('refusal charges or withdraws', self.errors(e=self.e.replace('rw_as_close_effect = {', 'rw_as_close_effect = { add_gold = -25')))
        b = block(self.t, 'rw_as_can_close_trigger')
        self.assertIn('rw_as_view_trigger = yes', b)
        self.assertNotIn('rw_as_context_trigger', b)
        self.assertNotIn('rw_as_live_trigger', b)
        self.assertNotIn('rw_case_close_effect', self.e)

    def test_no_truth_disclosure_or_native_privilege_created(self):
        for command in ('add_secret = {}', 'add_hook = {}', 'imprison = {}', 'add_opinion = {}'):
            self.assertIn('native punishment or global scan', self.errors(e=self.e+'\n'+command))
        for name in ('rw_case_evidence', 'rw_case_disclosed', 'rw_cc_state', 'rw_service_pending'):
            self.assertIn('facts disclosure or unrelated contract rewritten', self.errors(e=self.e+'\nset_variable = { name = '+name+' value = flag:yes }'))

    def test_fixed_original_retention_without_archive_extension(self):
        self.assertEqual(1, self.e.count('name = rw_case_retained value = flag:yes days = 1825'))
        self.assertIn('name = rw_case_result value = flag:withdrawn', block(self.e, 'rw_as_settle_effect'))
        self.assertNotIn('rw_case_retained', block(self.e, 'rw_as_prepare_effect'))
        self.assertNotRegex(self.e, r'\b(create_story|make_story_owner|on_action|add_to_global_variable_list)\s*=')

    def test_explicit_archive_navigation_and_no_refresh_in_saved_reply(self):
        archive = block((MOD/'events/rw_case_events.txt').read_text(), 'rw_cases.0006')
        self.assertIn('trigger = { rw_as_base_trigger = yes }', archive)
        self.assertIn('id = rw_allegation_settlement.0002', archive)
        self.assertNotIn('rw_as_settle_effect', archive)
        self.assertNotIn('immediate =', block(self.ev, 'rw_allegation_settlement.0001'))
        prep = block(self.e, 'rw_as_prepare_effect')
        for g in ('limit = { rw_as_base_trigger = yes }', 'clear_saved_scope = rw_as_revision', 'clear_saved_scope = rw_as_price'):
            self.assertIn(g, prep)
        self.assertNotIn('rw_as_propose_effect', prep)
        self.assertNotIn('rw_as_settle_effect', prep)

    def test_no_mediator_financial_notice_or_recurring_poll(self):
        self.assertNotIn('scope:rw_case_mediator', self.e + self.ev)
        self.assertEqual(2, len(re.findall(r'\bdays\s*=\s*1\b', self.e)))
        self.assertEqual(2, block(self.e, 'rw_as_send_reply_effect').count('trigger_event ='))
        self.assertEqual(2, block(self.e, 'rw_as_notify_effect').count('trigger_event ='))
        self.assertNotRegex(self.e, r'\b(every_living_character|every_owned_story|every_in_global_list)\s*=')

    def test_identical_ai_player_guards_with_contextual_reply_weights(self):
        self.assertNotRegex(clean_script(self.t+self.e+self.ev)[0], r'\bis_ai\s*=')
        self.assertIn('has_trait = greedy', self.ev)
        self.assertIn('var:rw_case_evidence = flag:admitted', self.ev)
        self.assertIn('value < -25', self.ev)
        initial = block((MOD/'events/rw_allegation_events.txt').read_text(), 'rw_allegations.0002')
        self.assertIn('trigger = { rw_as_can_propose_trigger = yes }', initial)

    def test_localization_bom_keys_and_display_boundaries(self):
        keys = set(re.findall(r'(?:name|desc|title)\s*=\s*(rw_allegation_settlement\.[\w.]+)', self.ev))
        keys.add('rw_allegation_settlement.review')
        for lang in ('english', 'french'):
            p = MOD/f'localization/{lang}/rw_allegation_settlement_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertTrue(keys <= actual, keys-actual)
