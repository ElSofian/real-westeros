"""Static adversarial contracts for financial rehabilitation, not CK3 execution."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def terms_errors(t, e, base_t, base_e):
    errors = []
    valid = block(t, 'rw_house_terms_valid_trigger')
    for guard in ('rw_house_record_active_trigger = yes', 'var:rw_house_last_response = flag:terms_offered',
                  'has_variable = rw_house_terms_window', 'var:rw_house_terms_price = 50',
                  'exists = var:rw_house_petitioner', 'exists = var:rw_house_requested_ruler',
                  'is_alive = yes', 'is_adult = yes', 'is_imprisoned = no', 'exists = house',
                  'house = prev.var:rw_house_target', 'house.house_head = this',
                  'NOT = { is_at_war_with = prev.var:rw_house_requested_ruler }',
                  'NOT = { this = prev.var:rw_house_requested_ruler }',
                  'holder = prev.var:rw_house_requested_ruler',
                  'var:rw_house_requested_ruler = { rw_house_sovereign_trigger = yes }'):
        if guard not in valid:
            errors.append('stale roles price or terms accepted')
    turn = block(t, 'rw_house_terms_turn_trigger')
    for guard in ('rw_house_current_head_trigger = yes', 'rw_house_terms_valid_trigger = yes', 'var:rw_house_petitioner = root'):
        if guard not in turn:
            errors.append('foreign head or obsolete consent can settle')
    if 'rw_house_terms_turn_trigger = yes' not in block(t, 'rw_house_terms_affordable_trigger') or 'gold >= 50' not in block(t, 'rw_house_terms_affordable_trigger'):
        errors.append('payment can create debt')
    for name, gate in (('rw_house_offer_terms_effect', 'rw_house_ruler_reply_trigger'),
                       ('rw_house_review_terms_effect', 'rw_house_terms_turn_trigger'),
                       ('rw_house_accept_terms_effect', 'rw_house_terms_affordable_trigger'),
                       ('rw_house_refuse_terms_effect', 'rw_house_terms_turn_trigger')):
        if f'limit = {{ {gate} = yes }}' not in block(e, name):
            errors.append('public terms effect bypass')
    offer = block(e, 'rw_house_offer_terms_effect')
    for guard in ('remove_variable = rw_house_request_window', 'name = rw_house_revision add = 1',
                  'name = rw_house_terms_price value = 50', 'name = rw_house_terms_window value = flag:yes days = 30'):
        if guard not in offer:
            errors.append('old consent or unbounded offer survives')
    if not 0 <= offer.find('change_variable') < offer.find('rw_house_snapshot_effect') < offer.find('trigger_event'):
        errors.append('offer sent before new revision')
    accept = block(e, 'rw_house_accept_terms_effect')
    if not 0 <= accept.find('rw_house_close_effect = { RESULT = restored }') < accept.find('add_gold = -50') < accept.find('add_gold = 50') < accept.find('flag:terms_settled'):
        errors.append('unconsumed or premature payment receipt')
    for guard in ('scope:rw_house_record.var:rw_house_requested_ruler = { save_scope_as = rw_house_terms_payee }',
                  'scope:rw_house_terms_payee = { add_gold = 50 }', 'name = rw_house_terms_paid_by value = root',
                  'name = rw_house_terms_paid_to value = scope:rw_house_terms_payee'):
        if guard not in accept:
            errors.append('payment goes to wrong party')
    if 'remove_variable = rw_house_terms_window' not in block(base_e, 'rw_house_close_effect'):
        errors.append('closed censure retains executable terms')
    petition = block(base_e, 'rw_house_petition_effect')
    for field in ('rw_house_terms_window', 'rw_house_terms_price', 'rw_house_terms_offered_on'):
        if f'remove_variable = {field}' not in petition:
            errors.append('replacement petition keeps old financial terms')
    if 'NOT = { rw_house_terms_valid_trigger = yes }' not in block(base_t, 'rw_house_can_petition_trigger'):
        errors.append('valid counteroffer can be overwritten')
    invalid = block(e, 'rw_house_invalidate_terms_effect')
    for guard in ('rw_house_record_active_trigger = yes', 'var:rw_house_last_response = flag:terms_offered',
                  'has_variable = rw_house_terms_window', 'remove_variable = rw_house_terms_window',
                  'flag:terms_invalidated', 'name = rw_house_revision add = 1'):
        if guard not in invalid:
            errors.append('retired financial offer can revive')
    return errors


class HouseTermsContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_house_terms_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_house_terms_effects.txt').read_text()
        self.bt = (MOD/'common/scripted_triggers/rw_house_affair_triggers.txt').read_text()
        self.be = (MOD/'common/scripted_effects/rw_house_affair_effects.txt').read_text()
        self.v = (MOD/'events/rw_house_terms_events.txt').read_text()
        self.bv = (MOD/'events/rw_house_affair_events.txt').read_text()

    def errors(self, t=None, e=None, bt=None, be=None):
        return terms_errors(self.t if t is None else t, self.e if e is None else e,
                            self.bt if bt is None else bt, self.be if be is None else be)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_dead_changed_captive_warring_or_wrong_ruler_cannot_settle(self):
        for guard in ('rw_house_record_active_trigger = yes', 'var:rw_house_last_response = flag:terms_offered',
                      'has_variable = rw_house_terms_window', 'is_alive = yes', 'is_adult = yes', 'is_imprisoned = no',
                      'house = prev.var:rw_house_target', 'house.house_head = this',
                      'holder = prev.var:rw_house_requested_ruler',
                      'NOT = { is_at_war_with = prev.var:rw_house_requested_ruler }',
                      'var:rw_house_requested_ruler = { rw_house_sovereign_trigger = yes }'):
            self.assertIn('stale roles price or terms accepted', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_exact_head_and_latest_record_revision_are_mandatory(self):
        for guard in ('rw_house_current_head_trigger = yes', 'rw_house_terms_valid_trigger = yes', 'var:rw_house_petitioner = root'):
            self.assertIn('foreign head or obsolete consent can settle', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertIn('rw_house_view_trigger = yes', block(self.bt, 'rw_house_current_head_trigger'))
        view = block(self.bt, 'rw_house_view_trigger')
        for guard in ('var:rw_house_serial = scope:rw_house_serial', 'var:rw_house_revision = scope:rw_house_revision',
                      'var:rw_house_target = scope:rw_house_target', 'var:rw_house_authority = scope:rw_house_authority'):
            self.assertIn(guard, view)

    def test_offer_price_and_solvency_fail_closed(self):
        self.assertIn('stale roles price or terms accepted', self.errors(t=self.t.replace('var:rw_house_terms_price = 50', 'always = yes')))
        self.assertIn('payment can create debt', self.errors(t=self.t.replace('gold >= 50', 'always = yes')))
        self.assertNotIn('gold >= 50', block(self.t, 'rw_house_terms_turn_trigger'))
        self.assertIn('rw_house_terms_turn_trigger = yes', block(self.e, 'rw_house_refuse_terms_effect'))

    def test_every_public_effect_rechecks_and_old_reply_is_consumed(self):
        for gate in ('rw_house_ruler_reply_trigger', 'rw_house_terms_turn_trigger', 'rw_house_terms_affordable_trigger'):
            self.assertIn('public terms effect bypass', self.errors(e=self.e.replace(f'limit = {{ {gate} = yes }}', 'limit = { always = yes }')))
        for guard in ('remove_variable = rw_house_request_window', 'name = rw_house_revision add = 1'):
            self.assertIn('old consent or unbounded offer survives', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertIn('offer sent before new revision', self.errors(e=self.e.replace('rw_house_snapshot_effect = yes', '', 1)))
        # Offering never executes the payment, free restoration or a forced native send.
        self.assertNotRegex(clean_script(block(self.e, 'rw_house_offer_terms_effect'))[0], r'\b(add_gold|rw_house_close_effect|run_interaction)\s*=')

    def test_consume_before_two_money_legs_and_receipt_after_both(self):
        accept = block(self.e, 'rw_house_accept_terms_effect')
        self.assertEqual(2, accept.count('add_gold'))
        self.assertIn('unconsumed or premature payment receipt', self.errors(e=self.e.replace('rw_house_close_effect = { RESULT = restored }', '')))
        self.assertIn('unconsumed or premature payment receipt', self.errors(e=self.e.replace('add_gold = -50', '').replace('rw_house_close_effect = { RESULT = restored }', 'add_gold = -50 rw_house_close_effect = { RESULT = restored }')))
        self.assertIn('unconsumed or premature payment receipt', self.errors(e=self.e.replace('flag:terms_settled', 'flag:terms_offered')))
        self.assertNotIn('add_opinion', accept)
        self.assertNotIn('rw_house_restore_effect', accept)

    def test_payee_is_exact_current_addressed_ruler_and_payer_is_head(self):
        for guard in ('scope:rw_house_record.var:rw_house_requested_ruler = { save_scope_as = rw_house_terms_payee }',
                      'scope:rw_house_terms_payee = { add_gold = 50 }', 'name = rw_house_terms_paid_by value = root',
                      'name = rw_house_terms_paid_to value = scope:rw_house_terms_payee'):
            self.assertIn('payment goes to wrong party', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertNotIn('story_owner', self.t + self.e)
        self.assertNotIn('rw_house_issuer', self.t + self.e)

    def test_refusal_silence_invalidation_and_navigation_take_nothing(self):
        for name in ('rw_house_review_terms_effect', 'rw_house_refuse_terms_effect',
                     'rw_house_invalidate_terms_effect', 'rw_house_reconcile_terms_effect'):
            text = clean_script(block(self.e, name))[0]
            self.assertNotRegex(text, r'\b(add_gold|add_opinion|add_prestige|rw_house_close_effect)\s*=')
            self.assertNotRegex(text, r'\b(?:name|remove_variable)\s*=\s*(?:rw_house_term|rw_house_petition_cooldown|rw_house_issued_on|rw_house_requested_on|rw_house_retained)\b')
        self.assertIn('flag:terms_refused', block(self.e, 'rw_house_refuse_terms_effect'))
        self.assertNotRegex(block(self.e, 'rw_house_review_terms_effect'), r'\b(set_variable|remove_variable|change_variable)\s*=')

    def test_expiry_and_invalidation_are_once_only_and_distinct(self):
        for guard in ('rw_house_record_active_trigger = yes', 'var:rw_house_last_response = flag:terms_offered',
                      'has_variable = rw_house_terms_window', 'remove_variable = rw_house_terms_window', 'flag:terms_invalidated'):
            self.assertIn('retired financial offer can revive', self.errors(e=self.e.replace(guard, 'always = yes')))
        reconcile = block(self.e, 'rw_house_reconcile_terms_effect')
        self.assertIn('NOT = { rw_house_terms_valid_trigger = yes }', reconcile)
        self.assertIn('limit = { has_variable = rw_house_terms_window }', reconcile)
        self.assertIn('flag:terms_unanswered', reconcile)
        self.assertNotIn('trigger_event', reconcile)

    def test_death_closure_and_replacement_cancel_financial_offer(self):
        self.assertIn('closed censure retains executable terms', self.errors(be=self.be.replace('remove_variable = rw_house_terms_window', 'always = yes')))
        for field in ('rw_house_terms_window', 'rw_house_terms_price', 'rw_house_terms_offered_on'):
            self.assertIn('replacement petition keeps old financial terms', self.errors(be=self.be.replace(f'remove_variable = {field}', 'always = yes')))
        self.assertIn('valid counteroffer can be overwritten', self.errors(bt=self.bt.replace('NOT = { rw_house_terms_valid_trigger = yes }', 'always = yes')))
        death = block(self.be, 'rw_house_owner_died_effect')
        self.assertLess(death.index('rw_house_invalidate_terms_effect'), death.index('make_story_owner'))
        maintenance = block(self.be, 'rw_house_maintenance_effect')
        self.assertLess(maintenance.index('rw_house_reconcile_terms_effect'), maintenance.index('rw_house_offer_opportunities_effect'))

    def test_fixed_decree_and_cooldown_no_new_recurring_timer(self):
        all_e = self.e + self.be
        self.assertEqual(1, all_e.count('name = rw_house_term value = flag:yes years = 50'))
        self.assertEqual(1, all_e.count('name = rw_house_petition_cooldown value = flag:yes days = 365'))
        self.assertEqual(1, all_e.count('name = rw_house_terms_window value = flag:yes days = 30'))
        story = (MOD/'common/story_cycles/rw_house_affairs.txt').read_text()
        self.assertEqual(1, story.count('effect_group'))
        self.assertIn('days = 60', story)
        for name in ('rw_house_read_register_effect', 'rw_house_refresh_effect'):
            self.assertNotIn('rw_house_accept_terms_effect', block(self.be, name))
            self.assertNotIn('rw_house_reconcile_terms_effect', block(self.be, name))

    def test_free_restoration_and_withdrawal_remain_available(self):
        panel = block(self.bv, 'rw_house_affairs.0003')
        for effect in ('rw_house_restore_effect = yes', 'rw_house_refuse_effect = yes', 'rw_house_offer_terms_effect = yes'):
            self.assertIn(effect, panel)
        self.assertIn('rw_house_withdraw_effect = yes', block(self.bv, 'rw_house_affairs.0002'))
        self.assertIn('remove_variable = rw_house_terms_window', block(self.be, 'rw_house_close_effect'))
        self.assertNotIn('add_gold', block(self.be, 'rw_house_withdraw_effect'))

    def test_ai_and_player_have_identical_action_graph_and_whole_terms(self):
        self.assertNotRegex(clean_script(self.t + self.e + self.v)[0], r'\b(is_ai|is_human)\s*=')
        self.assertIn('rw_house_terms.offer', block(self.bv, 'rw_house_affairs.0003'))
        self.assertIn('rw_house_review_terms_effect = yes', block(self.bv, 'rw_house_affairs.0002'))
        panel = block(self.v, 'rw_house_terms.0001')
        for item in ('rw_house_terms.conditions', 'rw_house_terms.unaffordable', 'rw_house_accept_terms_effect = yes',
                     'rw_house_refuse_terms_effect = yes', 'rw_house_refresh_effect = yes', 'rw_house_affairs.leave_unchanged'):
            self.assertIn(item, panel)
        self.assertIn('trigger = { rw_house_terms_affordable_trigger = yes }', panel)
        self.assertIn('NOT = { rw_house_terms_turn_trigger = yes }', panel)
        self.assertNotRegex(self.e + self.t, r'\b(every_living_character|every_house_member|random_house_member)\s*=')

    def test_localization_has_full_terms_and_distinct_receipts(self):
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_house_terms\.[\w.]+)', self.v + self.bv))
        for lang in ('english', 'french'):
            p = MOD/f'localization/{lang}/rw_house_terms_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            loc = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', loc, re.M)))
            for receipt in ('settled', 'refused', 'unanswered', 'invalidated', 'pending'):
                self.assertIn('rw_house_terms.' + receipt, loc)
            self.assertIn('50', loc)
        self.assertLess(self.bv.index('desc = rw_house_terms.settled'), self.bv.index('desc = rw_house_affairs.restored'))

    def test_no_native_status_property_pardon_or_private_evidence_mutation(self):
        code = clean_script(self.t + self.e + self.v)[0]
        self.assertNotRegex(code, r'\b(death|imprison|change_title_holder|destroy_title|set_house|set_dynasty|add_trait|remove_trait|run_interaction|add_secret|consume_revoke_title_reason|restore_inheritance_effect|agot_strip_lordship_as_punishment_effect)\s*=')
        self.assertNotIn('rw_evidence_', code)
        self.assertNotIn('rw_g3_trace', code)
