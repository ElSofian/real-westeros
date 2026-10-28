"""Adversarial source contracts for two negotiated clauses; no CK3 simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def delivery_errors(t, e, service_t, service_e, obligation):
    errors = []
    identity = block(t, 'rw_service_delivery_matches_trigger')
    for guard in ('limit = { has_variable = rw_service_delivery_days }',
                  'exists = scope:rw_service_delivery_days',
                  'var:rw_service_delivery_days = scope:rw_service_delivery_days',
                  'OR = { var:rw_service_delivery_days = 14 var:rw_service_delivery_days = 30 }',
                  'scope:rw_service_delivery_days = 30'):
        if guard not in identity:
            errors.append('missing or stale delivery clause accepted')
    if 'rw_service_delivery_matches_trigger = yes' not in block(service_t, 'rw_service_matches_trigger'):
        errors.append('delivery detached from quote identity')
    for name, gate in (('rw_service_shorten_delivery_effect', 'rw_service_can_shorten_delivery_trigger'),
                       ('rw_service_extend_delivery_effect', 'rw_service_can_extend_delivery_trigger')):
        action = block(e, name)
        if f'limit = {{ {gate} = yes }}' not in action:
            errors.append('wrong turn or immediate quote can change delivery')
        if not 0 <= action.find('name = rw_service_revision add = 1') < action.find('rw_service_snapshot_effect') < action.find('trigger_event'):
            errors.append('delivery counter sent with old consent')
        if re.search(r'\b(add_character_flag|add_gold|add_prestige)\s*=|\bname\s*=\s*rw_service_(price|mode)\b', clean_script(action)[0]):
            errors.append('deadline counter mutates other clause or expiry')
    for name in ('rw_service_counter_effect', 'rw_service_requote_effect'):
        if 'name = rw_service_delivery_days' in block(service_e, name):
            errors.append('price counter resets delivery clause')
    snapshot = block(service_e, 'rw_service_snapshot_effect')
    for guard in ('name = rw_service_delivery_days value = 30',
                  'limit = { has_variable = rw_service_delivery_days }',
                  'name = rw_service_delivery_days value = var:rw_service_delivery_days'):
        if guard not in snapshot:
            errors.append('delivery missing from saved snapshot')
    accept = block(obligation, 'rw_service_accept_promise_effect')
    for guard in ('limit = { NOT = { has_variable = rw_service_delivery_days } }',
                  'limit = { var:rw_service_delivery_days = 14 }',
                  'flag = rw_service_deadline days = 14', 'flag = rw_service_deadline days = 30',
                  'id = rw_obligations.0002 days = 15', 'id = rw_obligations.0002 days = 31'):
        if guard not in accept:
            errors.append('negotiated deadline not enforced or legacy overwritten')
    if 'remove_variable = rw_service_delivery_days' not in block(service_e, 'rw_service_clear_effect'):
        errors.append('delivery clause survives cleanup')
    return errors


class DeliveryContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_delivery_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_delivery_effects.txt').read_text()
        self.st = (MOD/'common/scripted_triggers/rw_service_triggers.txt').read_text()
        self.se = (MOD/'common/scripted_effects/rw_service_effects.txt').read_text()
        self.o = (MOD/'common/scripted_effects/rw_obligation_effects.txt').read_text()
        self.v = (MOD/'events/rw_delivery_events.txt').read_text()
        self.sv = (MOD/'events/rw_service_events.txt').read_text()

    def errors(self, t=None, e=None, st=None, se=None, o=None):
        return delivery_errors(self.t if t is None else t, self.e if e is None else e,
                               self.st if st is None else st, self.se if se is None else se,
                               self.o if o is None else o)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_full_identity_binds_delivery_and_rejects_unsupported_values(self):
        for guard in ('exists = scope:rw_service_delivery_days',
                      'var:rw_service_delivery_days = scope:rw_service_delivery_days',
                      'OR = { var:rw_service_delivery_days = 14 var:rw_service_delivery_days = 30 }'):
            self.assertIn('missing or stale delivery clause accepted', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertIn('delivery detached from quote identity', self.errors(st=self.st.replace('rw_service_delivery_matches_trigger = yes', 'always = yes')))
        for field in ('serial', 'revision', 'price', 'mode'):
            self.assertIn(f'var:rw_service_{field} = scope:rw_service_{field}', block(self.st, 'rw_service_matches_trigger'))

    def test_snapshot_binds_actual_value_and_legacy_defaults_to_thirty_only(self):
        for guard in ('name = rw_service_delivery_days value = 30', 'limit = { has_variable = rw_service_delivery_days }',
                      'name = rw_service_delivery_days value = var:rw_service_delivery_days'):
            self.assertIn('delivery missing from saved snapshot', self.errors(se=self.se.replace(guard, 'always = yes')))
        match = block(self.t, 'rw_service_delivery_matches_trigger')
        self.assertIn('trigger_else', match)
        self.assertIn('scope:rw_service_delivery_days = 30', match)
        self.assertNotIn('set_variable', match)
        self.assertIn('name = rw_service_delivery_days value = 30', block(self.se, 'rw_service_begin_effect'))

    def test_only_current_client_can_shorten_current_provider_can_extend(self):
        for gate in ('rw_service_can_shorten_delivery_trigger', 'rw_service_can_extend_delivery_trigger'):
            self.assertIn('wrong turn or immediate quote can change delivery', self.errors(e=self.e.replace(f'limit = {{ {gate} = yes }}', 'limit = { always = yes }')))
        for name, role in (('rw_service_can_shorten_delivery_trigger', 'client'), ('rw_service_can_extend_delivery_trigger', 'provider')):
            self.assertIn(f'rw_service_{role}_turn_trigger = yes', block(self.t, name))
            self.assertIn('rw_service_delivery_turn_trigger = yes', block(self.t, name))
        self.assertIn('rw_service_deferred_trigger = yes', block(self.t, 'rw_service_delivery_turn_trigger'))

    def test_delivery_counter_preserves_price_mode_and_original_pending_deadline(self):
        for bad in ('set_variable = { name = rw_service_price value = 50 }', 'add_character_flag = { flag = rw_service_pending days = 30 }', 'add_gold = 25'):
            changed = self.e.replace('rw_service_snapshot_effect = yes', bad + ' rw_service_snapshot_effect = yes', 1)
            self.assertIn('deadline counter mutates other clause or expiry', self.errors(e=changed))
        self.assertEqual(1, self.se.count('flag = rw_service_pending days = 30'))

    def test_price_counter_preserves_negotiated_delivery(self):
        for name in ('rw_service_counter_effect', 'rw_service_requote_effect'):
            changed = self.se.replace(name + ' = {', name + ' = { set_variable = { name = rw_service_delivery_days value = 30 }')
            self.assertIn('price counter resets delivery clause', self.errors(se=changed))

    def test_counters_revise_and_snapshot_before_notifying_other_party(self):
        self.assertIn('delivery counter sent with old consent', self.errors(e=self.e.replace('name = rw_service_revision add = 1', 'name = unrelated add = 1')))
        self.assertIn('delivery counter sent with old consent', self.errors(e=self.e.replace('rw_service_snapshot_effect = yes', '')))
        self.assertIn('flag:provider', block(self.e, 'rw_service_shorten_delivery_effect'))
        self.assertIn('flag:client', block(self.e, 'rw_service_extend_delivery_effect'))
        self.assertIn('scope:rw_service_provider = { trigger_event', block(self.e, 'rw_service_shorten_delivery_effect'))
        self.assertIn('scope:rw_service_client = { trigger_event', block(self.e, 'rw_service_extend_delivery_effect'))

    def test_acceptance_honors_fourteen_or_thirty_without_prepayment(self):
        for guard in ('limit = { var:rw_service_delivery_days = 14 }', 'flag = rw_service_deadline days = 14',
                      'flag = rw_service_deadline days = 30', 'id = rw_obligations.0002 days = 15', 'id = rw_obligations.0002 days = 31'):
            self.assertIn('negotiated deadline not enforced or legacy overwritten', self.errors(o=self.o.replace(guard, 'always = yes')))
        accept = block(self.o, 'rw_service_accept_promise_effect')
        self.assertIn('rw_service_affordable_trigger = yes', accept)
        self.assertNotRegex(clean_script(accept)[0], r'\b(add_gold|add_prestige)\s*=')
        self.assertIn('flag = rw_service_not_due days = 7', accept)
        self.assertIn('rw_service_schedule_decision_effect = { DAYS = 8 }', accept)
        self.assertLess(accept.index('change_variable'), accept.index('rw_service_snapshot_effect'))

    def test_only_legacy_missing_field_can_be_initialized_on_acceptance(self):
        self.assertIn('negotiated deadline not enforced or legacy overwritten', self.errors(o=self.o.replace('limit = { NOT = { has_variable = rw_service_delivery_days } }', 'limit = { always = yes }')))
        accept = block(self.o, 'rw_service_accept_promise_effect')
        self.assertLess(accept.index('NOT = { has_variable = rw_service_delivery_days }'), accept.index('name = rw_service_delivery_days value = 30'))
        owner = block(self.st, 'rw_service_obligation_owner_matches_trigger')
        self.assertNotIn('rw_service_delivery_days', owner)
        self.assertIn('var:rw_service_revision = scope:rw_service_revision', owner)

    def test_wait_cancel_and_review_never_renegotiate_accepted_deadline(self):
        cancellation = (MOD/'common/scripted_effects/rw_cancellation_effects.txt').read_text()
        decisions = (MOD/'common/scripted_effects/rw_service_decision_effects.txt').read_text()
        for text in (cancellation, decisions, block(self.o, 'rw_service_wait_promise_effect')):
            self.assertNotIn('name = rw_service_delivery_days', text)
            self.assertNotIn('flag = rw_service_deadline days', text)
        self.assertIn('has_character_flag = rw_service_deadline', block(self.st, 'rw_service_obligation_due_trigger'))
        self.assertIn('NOT = { has_character_flag = rw_service_deadline }', block(self.o, 'rw_service_timeout_effect'))

    def test_cleanup_and_receipt_keep_no_live_renegotiable_clause(self):
        self.assertIn('delivery clause survives cleanup', self.errors(se=self.se.replace('remove_variable = rw_service_delivery_days', '')))
        receipt = block(self.o, 'rw_service_record_receipt_effect')
        self.assertIn('name = rw_service_last_delivery_days value = scope:rw_service_delivery_days', receipt)
        fulfill = block(self.o, 'rw_service_fulfill_promise_effect')
        self.assertLess(fulfill.index('rw_service_record_receipt_effect'), fulfill.index('rw_service_clear_effect'))
        self.assertLess(fulfill.index('rw_service_clear_effect'), fulfill.index('add_gold'))

    def test_complete_offer_summary_both_prices_deadlines_and_shared_ai_choices(self):
        panel = block(self.v, 'rw_delivery.0001')
        for key in ('summary', 'price_25', 'price_50', 'days_14', 'days_30', 'accept', 'shorten', 'extend'):
            self.assertIn('rw_delivery.' + key, panel)
        for call in ('rw_service_accept_promise_effect', 'rw_service_counter_effect', 'rw_service_requote_effect',
                     'rw_service_shorten_delivery_effect', 'rw_service_extend_delivery_effect', 'rw_service_clear_effect'):
            self.assertIn(call + ' = yes', panel)
        self.assertIn('rw_service_affordable_trigger = yes', panel)
        self.assertIn('character = scope:rw_service_provider', panel)
        self.assertIn('character = scope:rw_service_client', panel)
        self.assertNotRegex(clean_script(self.t + self.e + self.v)[0], r'\b(is_ai|is_human)\s*=')
        self.assertNotIn('var:rw_service_delivery_days', block(self.t, 'rw_service_short_delivery_trigger'))
        self.assertIn('scope:rw_service_delivery_days = 14', block(self.t, 'rw_service_short_delivery_trigger'))

    def test_localization_reference_graph_covers_every_captured_clause(self):
        obligation_events = (MOD/'events/rw_obligation_events.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_delivery\.[\w.]+)', self.v + self.sv + obligation_events))
        for lang in ('english', 'french'):
            p = MOD/f'localization/{lang}/rw_delivery_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M)))
            old = (MOD/f'localization/{lang}/rw_services_l_{lang}.yml').read_text(encoding='utf-8-sig')
            quote = next(line for line in old.splitlines() if 'rw_services.0001.deferred_desc:' in line)
            self.assertNotIn('within thirty days', quote)
            self.assertNotIn('délai de trente jours', quote)

    def test_no_native_title_or_war_or_runtime_model_dependency(self):
        self.assertNotRegex(clean_script(self.t + self.e + self.v)[0], r'\b(change_title_holder|death|imprison|run_interaction|add_secret|set_house|every_living_character)\s*=')
        self.assertNotIn('rw_g3', self.t + self.e + self.v)
        self.assertNotIn('python', clean_script(self.t + self.e + self.v)[0].lower())
