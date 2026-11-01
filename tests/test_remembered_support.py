"""Adversarial native-source checks, not a simulation of memories or AI choices."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from test_political_ai import option
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/real_westeros'


def memory_choice_errors(triggers, values, services, cases):
    errors = []
    query = block(triggers, 'rw_pm_remembers_support_trigger')
    memory = nested_block(query, 'any_memory')
    if not query.lstrip().startswith('exists = $COUNTERPART$') or 'NOT = { this = $COUNTERPART$ }' not in query:
        errors.append('missing or self counterpart admitted')
    # No scope hop between the querying character and the native memory iterator.
    prefix = query[:query.find('any_memory')]
    if '{' in prefix.replace('NOT = { this = $COUNTERPART$ }', '') or query.count('any_memory =') != 1:
        errors.append('another character knowledge read')
    if 'has_memory_type = rw_public_support_received' not in memory:
        errors.append('wrong experience treated as received support')
    if 'memory_age_years < 5' not in memory:
        errors.append('expired memory still used')
    if 'any_memory_participant = { this = $COUNTERPART$ }' not in memory:
        errors.append('unrelated supporter substituted')
    pair = block(triggers, 'rw_pm_remembers_counterpart_trigger')
    if 'rw_ai_known_pair_trigger = yes' not in pair:
        errors.append('foreign decider admitted')
    for own, other in (('client', 'provider'), ('provider', 'client')):
        expected = ('this = scope:rw_service_' + own + '\n            '
                    'rw_pm_remembers_support_trigger = { COUNTERPART = scope:rw_service_' + other + ' }')
        if expected not in pair:
            errors.append('wrong future counterpart')
    core = block(values, 'rw_ai_cooperation_factor')
    if 'if = { limit = { rw_pm_remembers_counterpart_trigger = yes } multiply = 1.5 }' not in core:
        errors.append('memory factor missing or stacking')
    if not core.lstrip().startswith('value = 0') or 'limit = { rw_ai_known_pair_trigger = yes }' not in core:
        errors.append('foreign decider given willingness')
    for name, guards in (
        ('rw_ai_service_accept_weight', ('rw_service_client_turn_trigger = yes', 'rw_service_affordable_trigger = yes')),
        ('rw_ai_case_repair_weight', ('rw_case_provider_turn_trigger = yes', 'prestige >= 25'))):
        value = block(values, name)
        if any(g not in value for g in (*guards, 'multiply = rw_ai_cooperation_factor')):
            errors.append('memory bypasses cost or turn')
    for text, event, action, weight, gate, desc in (
        (services, 'rw_services.0001', 'rw_services.accept_50', 'rw_ai_service_accept_weight', 'rw_service_client_turn_trigger', 'service'),
        (cases, 'rw_cases.0002', 'rw_cases.apologise', 'rw_ai_case_repair_weight', 'rw_case_provider_turn_trigger', 'repair')):
        body = block(text, event)
        if 'add = ' + weight not in nested_block(option(body, action), 'ai_chance'):
            errors.append('future independent action disconnected')
        if 'trigger = { ' + gate + ' = yes rw_pm_remembers_counterpart_trigger = yes }' not in body or 'desc = rw_remembered_support.' + desc not in body:
            errors.append('player reminder missing or foreign')
    code = clean_script(triggers)[0]
    if re.search(r'\b(?:every_\w+|random_\w+|any_living_character|any_owned_story|set_variable|save_scope_as|create_character_memory|trigger_event|add_gold|add_opinion|is_ai|has_secret|rw_case_evidence|rw_ru_\w+)\s*=', code):
        errors.append('mutation hidden records rumor or global scan')
    return errors


class RememberedSupportTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_remembered_support_triggers.txt').read_text()
        self.v = (MOD/'common/script_values/rw_political_ai_values.txt').read_text()
        self.s = (MOD/'events/rw_service_events.txt').read_text()
        self.c = (MOD/'events/rw_case_events.txt').read_text()

    def errors(self, **changes):
        return memory_choice_errors(*(changes.get(k, getattr(self, k)) for k in 'tvsc'))

    def test_source_contract(self):
        self.assertEqual([], self.errors())

    def test_missing_or_self_counterpart_rejected(self):
        for needle in ('exists = $COUNTERPART$', 'NOT = { this = $COUNTERPART$ }'):
            self.assertIn('missing or self counterpart admitted', self.errors(t=self.t.replace(needle, 'always = yes')))

    def test_counterpart_memories_cannot_be_read(self):
        wrong = self.t.replace('    any_memory = {', '    $COUNTERPART$ = { any_memory = {', 1).replace('\n}\n', '\n    }\n}\n', 1)
        self.assertIn('another character knowledge read', self.errors(t=wrong))

    def test_other_memory_types_and_expiration_rejected(self):
        for wrong in ('rw_public_support_given', 'rw_public_crown_recognition'):
            self.assertIn('wrong experience treated as received support', self.errors(t=self.t.replace('rw_public_support_received', wrong)))
        self.assertIn('expired memory still used', self.errors(t=self.t.replace('memory_age_years < 5', 'always = yes')))

    def test_other_supporter_cannot_color_current_relationship(self):
        self.assertIn('unrelated supporter substituted', self.errors(t=self.t.replace('any_memory_participant = { this = $COUNTERPART$ }', 'any_memory_participant = { always = yes }')))
        for own in ('client', 'provider'):
            other = 'provider' if own == 'client' else 'client'
            self.assertIn('wrong future counterpart', self.errors(t=self.t.replace('COUNTERPART = scope:rw_service_' + other, 'COUNTERPART = scope:rw_service_' + own)))

    def test_mediator_custodian_or_heir_cannot_borrow_pair_knowledge(self):
        self.assertIn('foreign decider admitted', self.errors(t=self.t.replace('rw_ai_known_pair_trigger = yes', 'always = yes')))
        self.assertIn('foreign decider given willingness', self.errors(v=self.v.replace('limit = { rw_ai_known_pair_trigger = yes }', 'limit = { always = yes }')))

    def test_boolean_factor_cannot_be_unbounded_by_memory_count(self):
        self.assertIn('memory factor missing or stacking', self.errors(v=self.v.replace('multiply = 1.5', 'multiply = 5')))
        self.assertNotRegex(self.t, r'\b(?:every_memory|ordered_memory|count)\s*=')

    def test_costs_turns_and_two_future_decisions_stay_connected(self):
        for guard in ('rw_service_affordable_trigger = yes', 'rw_case_provider_turn_trigger = yes', 'prestige >= 25'):
            self.assertIn('memory bypasses cost or turn', self.errors(v=self.v.replace(guard, 'always = yes')))
        for field, weight in (('s', 'rw_ai_service_accept_weight'), ('c', 'rw_ai_case_repair_weight')):
            self.assertIn('future independent action disconnected', self.errors(**{field: getattr(self, field).replace('add = '+weight, 'add = 50')}))

    def test_current_player_reminder_guarded_and_localized(self):
        self.assertIn('player reminder missing or foreign', self.errors(c=self.c.replace('desc = rw_remembered_support.repair', 'desc = rw_cases.0002.desc')))
        for lang in ('english', 'french'):
            text = (MOD/f'localization/{lang}/rw_remembered_support_l_{lang}.yml').read_text(encoding='utf-8-sig')
            for key, role in (('service', 'provider'), ('repair', 'client')):
                line = next(l for l in text.splitlines() if 'rw_remembered_support.'+key+':' in l)
                self.assertIn('[rw_service_'+role+'.GetTitledFirstName]', line)

    def test_no_mutation_rumor_private_case_or_global_scan(self):
        for bad in ('every_living_character = { always = yes }', 'any_owned_story = { always = yes }',
                    'rw_ru_holders = yes', 'rw_case_evidence = flag:admitted', 'is_ai = yes',
                    'create_character_memory = { type = rw_public_support_received }', 'add_opinion = {}'):
            self.assertIn('mutation hidden records rumor or global scan', self.errors(t=self.t+'\nrw_bad = { '+bad+' }'))

    def test_refusal_and_original_native_effects_remain_optional(self):
        self.assertIn('ai_chance = { base = 30 }', option(self.s, 'rw_services.refuse'))
        self.assertIn('ai_chance = { base = 40 }', option(self.s, 'rw_services.counter_25'))
        self.assertIn('ai_chance = { base = 50 }', option(self.c, 'rw_cases.refuse_repair'))
        self.assertIn('rw_service_settle_effect = yes', option(self.s, 'rw_services.accept_50'))
        self.assertIn('rw_case_apologise_effect = yes', option(self.c, 'rw_cases.apologise'))
