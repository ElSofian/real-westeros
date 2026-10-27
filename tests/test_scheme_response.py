"""Static/adversarial contracts for consent-based political responses, not CK3 execution."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def response_errors(t, e):
    errors = []
    identity = block(t, 'rw_scheme_response_identity_trigger')
    for guard in ('exists = scope:rw_scheme_observer', 'exists = scope:rw_scheme_evidence_record',
                  'exists = scope:rw_scheme_evidence_serial', 'exists = scope:rw_scheme_participant',
                  'rw_scheme_evidence_reader_trigger = { READER = scope:rw_scheme_observer }',
                  'var:rw_evidence_serial = scope:rw_scheme_evidence_serial',
                  'var:rw_evidence_kind = flag:participant_exposed',
                  'var:rw_evidence_participant = scope:rw_scheme_participant', 'has_variable = rw_scheme_response_state'):
        if guard not in identity:
            errors.append('wrong actor/record/provenance can respond')
    for role, state in (('owner', 'open'), ('participant', 'offered')):
        turn = block(t, f'rw_scheme_response_{role}_turn_trigger')
        actor = 'observer' if role == 'owner' else 'participant'
        for guard in ('rw_scheme_response_identity_trigger = yes', f'this = scope:rw_scheme_{actor}',
                      'has_variable = rw_scheme_response_window', f'var:rw_scheme_response_state = flag:{state}'):
            if guard not in turn:
                errors.append('expired/replayed/wrong-root response possible')
    authority = block(t, 'rw_scheme_response_authority_trigger')
    if authority.count('is_imprisoned = no') != 2:
        errors.append('native imprisonment ignored')
    for guard in ('liege = scope:rw_scheme_observer', 'is_courtier_of = scope:rw_scheme_observer',
                  'NOT = { this = scope:rw_scheme_observer }', 'host = this'):
        if guard not in authority:
            errors.append('current authority bypass')
    for name in ('rw_scheme_response_can_request_trigger', 'rw_scheme_response_participant_turn_trigger'):
        if 'rw_scheme_response_authority_trigger = yes' not in block(t, name):
            errors.append('request or reply ignores lost authority')
    payable = block(t, 'rw_scheme_response_can_pay_trigger')
    if 'rw_scheme_response_participant_turn_trigger = yes' not in payable or 'gold >= 25' not in payable:
        errors.append('unfunded/unconsented payment')
    pay = block(e, 'rw_scheme_response_pay_effect')
    if 'limit = { rw_scheme_response_can_pay_trigger = yes }' not in pay:
        errors.append('payment execution bypass')
    if not 0 <= pay.find('name = rw_scheme_response_state value = flag:paid') < pay.find('add_gold'):
        errors.append('payment before consumption')
    if 'remove_variable = rw_scheme_response_window' not in pay:
        errors.append('payment leaves window live')
    request = block(e, 'rw_scheme_response_request_effect')
    if 'rw_scheme_response_can_request_trigger = yes' not in request:
        errors.append('request execution bypass')
    if not 0 <= request.find('value = flag:offered') < request.find('trigger_event'):
        errors.append('request not consumed before disclosure')
    if re.search(r'\badd_gold\s*=', request):
        errors.append('unilateral charge')
    initial = block(e, 'rw_scheme_response_initialise_effect')
    for guard in ('var:rw_evidence_kind = flag:participant_exposed', 'NOT = { has_variable = rw_scheme_response_state }'):
        if guard not in initial:
            errors.append('generic or old record initializes a response')
    if e.count('name = rw_scheme_response_window value = flag:yes days = 30') != 1:
        errors.append('response deadline renewed')
    # Response files may add stance/consent, never revise the original discovery.
    if re.search(r'\b(?:set_variable|remove_variable)\s*=\s*(?:\{\s*name\s*=\s*)?rw_evidence_', clean_script(e)[0]):
        errors.append('original evidence rewritten')
    if 'NOT = { has_opinion_modifier = { target = scope:rw_scheme_participant modifier = rw_scheme_reparation_opinion } }' not in pay:
        errors.append('goodwill can stack or renew')
    received = block(t, 'rw_scheme_response_received_filter_trigger')
    for guard in ('story_type = story_rw_scheme_evidence', 'var:rw_evidence_schema = 1',
                  'var:rw_evidence_kind = flag:participant_exposed', 'var:rw_evidence_participant = $READER$',
                  'var:rw_scheme_response_state = flag:offered', 'has_variable = rw_scheme_response_window'):
        if guard not in received:
            errors.append('unshared or unrelated observation exposed')
    return errors


class SchemeResponseTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_scheme_response_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_scheme_response_effects.txt').read_text()
        self.v = (MOD / 'events/rw_scheme_response_events.txt').read_text()

    def errors(self, t=None, e=None):
        return response_errors(self.t if t is None else t, self.e if e is None else e)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_identity_and_generic_discovery_mutations(self):
        for guard in ('exists = scope:rw_scheme_evidence_record',
                      'rw_scheme_evidence_reader_trigger = { READER = scope:rw_scheme_observer }',
                      'var:rw_evidence_serial = scope:rw_scheme_evidence_serial',
                      'var:rw_evidence_kind = flag:participant_exposed',
                      'var:rw_evidence_participant = scope:rw_scheme_participant'):
            with self.subTest(guard=guard):
                self.assertIn('wrong actor/record/provenance can respond', self.errors(t=self.t.replace(guard, 'always = yes', 1)))

    def test_wrong_actor_expired_or_replayed_response_mutations(self):
        for guard in ('this = scope:rw_scheme_observer', 'this = scope:rw_scheme_participant',
                      'var:rw_scheme_response_state = flag:open', 'var:rw_scheme_response_state = flag:offered',
                      'has_variable = rw_scheme_response_window'):
            with self.subTest(guard=guard):
                self.assertIn('expired/replayed/wrong-root response possible', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_prison_and_lost_authority_mutations(self):
        self.assertIn('native imprisonment ignored', self.errors(t=self.t.replace('is_imprisoned = no', 'always = yes', 1)))
        self.assertIn('current authority bypass', self.errors(t=self.t.replace('liege = scope:rw_scheme_observer', 'always = yes')))
        self.assertIn('request or reply ignores lost authority', self.errors(t=self.t.replace('rw_scheme_response_authority_trigger = yes', 'always = yes')))

    def test_unfunded_or_unconsented_payment_mutations(self):
        self.assertIn('unfunded/unconsented payment', self.errors(t=self.t.replace('gold >= 25', 'always = yes')))
        self.assertIn('payment execution bypass', self.errors(e=self.e.replace('limit = { rw_scheme_response_can_pay_trigger = yes }', 'limit = { always = yes }')))

    def test_duplicate_payment_or_charge_on_request_mutations(self):
        self.assertIn('payment leaves window live', self.errors(e=self.e.replace('remove_variable = rw_scheme_response_window', '')))
        e = self.e.replace('name = rw_scheme_response_state value = flag:paid', 'name = rw_scheme_response_state value = flag:offered')
        self.assertIn('payment before consumption', self.errors(e=e))
        e = self.e.replace('rw_scheme_response_request_effect = {', 'rw_scheme_response_request_effect = { add_gold = -25')
        self.assertIn('unilateral charge', self.errors(e=e))
        pay = block(self.e, 'rw_scheme_response_pay_effect')
        self.assertEqual(1, pay.count('add_gold = -25'))
        self.assertEqual(1, pay.count('add_gold = 25'))

    def test_agreed_goodwill_cannot_stack_renew_or_remove_native_penalty(self):
        pay = block(self.e, 'rw_scheme_response_pay_effect')
        guard = 'NOT = { has_opinion_modifier = { target = scope:rw_scheme_participant modifier = rw_scheme_reparation_opinion } }'
        self.assertIn(guard, pay)
        self.assertIn('goodwill can stack or renew', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertEqual(1, self.e.count('add_opinion ='))
        self.assertLess(pay.index('value = flag:paid'), pay.index('add_opinion'))
        self.assertNotIn('remove_opinion', self.e)
        modifier = (MOD / 'common/opinion_modifiers/rw_scheme_response_opinions.txt').read_text()
        self.assertIn('opinion = 5', modifier)
        self.assertIn('years = 2', modifier)
        self.assertIn('factor = 0', self.v)

    def test_no_implicit_migration_or_deadline_renewal_mutations(self):
        e = self.e.replace('NOT = { has_variable = rw_scheme_response_state }', 'always = yes')
        self.assertIn('generic or old record initializes a response', self.errors(e=e))
        e = self.e.replace('rw_scheme_response_request_effect = {', 'rw_scheme_response_request_effect = { set_variable = { name = rw_scheme_response_window value = flag:yes days = 30 }')
        self.assertIn('response deadline renewed', self.errors(e=e))
        self.assertNotIn('rw_evidence_retained value', self.e)

    def test_contestation_cannot_rewrite_evidence(self):
        e = self.e.replace('rw_scheme_response_decline_effect = {', 'rw_scheme_response_decline_effect = { set_variable = { name = rw_evidence_kind value = flag:scheme_discovered }')
        self.assertIn('original evidence rewritten', self.errors(e=e))
        self.assertIn('ANSWER = refused', self.v)
        self.assertIn('ANSWER = contested', self.v)
        decline = block(self.e, 'rw_scheme_response_decline_effect')
        self.assertIn('rw_scheme_response_participant_turn_trigger = yes', decline)
        self.assertNotIn('add_gold', decline)
        self.assertIn('rw_scheme_response_owner_turn_trigger = yes', block(self.e, 'rw_scheme_response_forego_effect'))

    def test_silence_delay_and_tolerance_cannot_sanction_or_reschedule(self):
        self.assertNotRegex(block(self.e, 'rw_scheme_response_forego_effect'), r'\b(add_gold|add_opinion|trigger_event)\s*=')
        for event_name, option_name, next_option in (('rw_scheme_response.0001', 'later', 'acknowledge'),
                                                     ('rw_scheme_response.0002', 'ignore', 'acknowledge')):
            event = block(self.v, event_name)
            option = event[event.index('name = rw_scheme_response.' + option_name):event.index('name = rw_scheme_response.' + next_option)]
            self.assertNotRegex(clean_script(option)[0], r'\b(?:rw_\w+_effect|trigger_event|add_gold|set_variable)\s*=')
        self.assertEqual(1, self.e.count('id = rw_scheme_response.0004 days = 1'))
        self.assertNotIn('scheme_owner', clean_script(self.t + self.e + self.v)[0])
        self.assertNotRegex(clean_script(self.e)[0], r'\b(add_secret|expose_secret|expose_scheme|expose_scheme_agent|end_scheme|imprison|death|revoke_title|add_prestige|add_hook)\s*=')

    def test_withdrawal_consumes_request_without_payment_or_new_jurisdiction(self):
        gate = block(self.t, 'rw_scheme_response_can_withdraw_trigger')
        for guard in ('rw_scheme_response_identity_trigger = yes', 'this = scope:rw_scheme_observer',
                      'var:rw_scheme_response_state = flag:offered', 'has_variable = rw_scheme_response_window'):
            self.assertIn(guard, gate)
        self.assertNotIn('rw_scheme_response_authority_trigger', gate)
        withdraw = block(self.e, 'rw_scheme_response_withdraw_effect')
        self.assertIn('rw_scheme_response_can_withdraw_trigger = yes', withdraw)
        self.assertIn('remove_variable = rw_scheme_response_window', withdraw)
        self.assertIn('value = flag:withdrawn', withdraw)
        self.assertNotRegex(withdraw, r'\b(add_gold|add_opinion|add_prestige)\s*=')
        self.assertLess(withdraw.index('value = flag:withdrawn'), withdraw.index('send_interface_message'))

    def test_actor_only_history_and_explicit_request_sharing(self):
        history = block(self.v, 'rw_scheme_response.0003')
        self.assertNotRegex(history, r'\b(?:rw_\w+_effect|set_variable|add_gold)\s*=')
        self.assertIn('rw_scheme_evidence_view_trigger = yes', block(self.t, 'rw_scheme_response_can_read_trigger'))
        received = block(self.t, 'rw_scheme_response_received_filter_trigger')
        for guard in ('story_type = story_rw_scheme_evidence', 'var:rw_evidence_schema = 1',
                      'var:rw_evidence_kind = flag:participant_exposed', 'var:rw_evidence_participant = $READER$',
                      'var:rw_scheme_response_state = flag:offered', 'has_variable = rw_scheme_response_window'):
            self.assertIn(guard, received)
        review = block(self.e, 'rw_scheme_response_review_received_effect')
        self.assertIn('rw_scheme_response_participant_turn_trigger = yes', review)
        self.assertIn('id = rw_scheme_response.0002', review)
        self.assertNotIn('id = rw_scheme_evidence.0001', review)
        self.assertNotIn('id = rw_scheme_response.0003', review)

    def test_received_request_filter_rejects_undisclosed_other_person_mutations(self):
        for guard in ('var:rw_evidence_participant = $READER$', 'var:rw_scheme_response_state = flag:offered'):
            with self.subTest(guard=guard):
                self.assertIn('unshared or unrelated observation exposed', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_shared_ai_opportunity_and_rechecked_dispatch(self):
        initial = block(self.e, 'rw_scheme_response_initialise_effect')
        self.assertIn('id = rw_scheme_response.0004 days = 1', initial)
        self.assertIn('rw_scheme_response_owner_turn_trigger = yes', block(self.v, 'rw_scheme_response.0004'))
        self.assertNotIn('is_ai', self.t + self.e + self.v)
        for choice in ('forego', 'request', 'later', 'pay', 'refuse', 'contest', 'ignore'):
            self.assertIn('name = rw_scheme_response.' + choice, self.v)
        self.assertIn('opinion = { target = scope:rw_scheme_participant', self.v)
        self.assertIn('gold < 100', self.v)
        self.assertNotIn('rw_evidence_scheme', self.t + self.e + self.v)

    def test_one_shared_reconsideration_without_recursive_reminders(self):
        request = block(self.e, 'rw_scheme_response_request_effect')
        for event in ('0005', '0006'):
            self.assertEqual(1, self.e.count('id = rw_scheme_response.' + event + ' days = 7'))
        self.assertLess(request.index('value = flag:offered'), request.index('id = rw_scheme_response.0005'))
        for event, gate in (('0005', 'rw_scheme_response_can_withdraw_trigger'),
                            ('0006', 'rw_scheme_response_participant_turn_trigger')):
            dispatcher = block(self.v, 'rw_scheme_response.' + event)
            self.assertIn(gate + ' = yes', dispatcher)
            self.assertNotRegex(dispatcher, r'\bdays\s*=')
        # Wait/ignore and manual browsing never schedule another series.
        self.assertNotIn('days =', block(self.e, 'rw_scheme_response_review_received_effect'))

    def test_journal_resolves_only_its_recorded_participant(self):
        journal = (MOD / 'events/rw_scheme_evidence_events.txt').read_text()
        self.assertIn('rw_scheme_response_can_open_trigger = yes', journal)
        self.assertIn('scope:rw_scheme_evidence_record.var:rw_evidence_participant = { save_scope_as = rw_scheme_participant }', journal)
        self.assertIn('rw_scheme_response_owner_turn_trigger = yes', journal)
        self.assertNotRegex(journal, r'\b(add_gold|set_variable|change_variable)\s*=')

    def test_display_keys_and_no_claim_of_immunity(self):
        interaction = (MOD / 'common/character_interactions/rw_scheme_response_interactions.txt').read_text()
        journal = (MOD / 'events/rw_scheme_evidence_events.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', self.v + journal + interaction))
        keys = {key for key in keys if key.startswith('rw_scheme_response.')}
        keys.update(('rw_scheme_response.notice_title', 'rw_scheme_response.notice_desc',
                     'rw_scheme_response.withdraw_notice_title', 'rw_scheme_response.withdraw_notice_desc',
                     'rw_review_received_scheme_request_interaction', 'rw_review_received_scheme_request_interaction_desc', 'rw_scheme_reparation_opinion'))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_scheme_response_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', text, re.M)))
            self.assertNotIn('scheme_owner', text)
