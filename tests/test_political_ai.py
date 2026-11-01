"""Adversarial checks of CK3 policy wiring; no AI/CK3 behavior simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def option(text, name):
    match = re.search(r'\boption\s*=\s*\{\s*name\s*=\s*' + re.escape(name) + r'\b', text)
    return nested_block(text[match.start():], 'option') if match else ''


def policy_errors(triggers, values, service, cases):
    errors = []
    pair = block(triggers, 'rw_ai_known_pair_trigger')
    for guard in ('exists = scope:rw_service_provider', 'exists = scope:rw_service_client',
                  'NOT = { scope:rw_service_provider = scope:rw_service_client }',
                  'OR = { this = scope:rw_service_provider this = scope:rw_service_client }'):
        if guard not in pair:
            errors.append('foreign or missing decider admitted')
    core = block(values, 'rw_ai_cooperation_factor')
    if not core.lstrip().startswith('value = 0') or 'limit = { rw_ai_known_pair_trigger = yes }' not in core:
        errors.append('unknown context given willingness')
    for name,threshold in (('trusted', '>= 25'), ('hostile', '<= -25')):
        t = block(triggers, 'rw_ai_' + name + '_counterpart_trigger')
        for own,other in (('client','provider'), ('provider','client')):
            branch = 'this = scope:rw_service_' + own + '\n            opinion = { target = scope:rw_service_' + other + ' value ' + threshold + ' }'
            if branch not in t:
                errors.append('counterpart or decider opinion substituted')
        if 'rw_ai_known_pair_trigger = yes' not in t:
            errors.append('foreign or missing decider admitted')
    for name,factor in (('trusted_counterpart', '2'), ('hostile_counterpart', '0.5'), ('existing_commitment','0.5')):
        if 'limit = { rw_ai_' + name + '_trigger = yes } multiply = ' + factor not in core:
            errors.append('context factor disconnected')
    if 'limit = { is_at_war = yes } multiply = 0.5' not in core:
        errors.append('military burden disconnected')
    commitments = block(triggers,'rw_ai_existing_commitment_trigger')
    for flag in ('rw_service_obligation','rw_fv_obligation'):
        if 'has_character_flag = ' + flag not in commitments:
            errors.append('own existing duty ignored')
    reserve = block(values,'rw_ai_service_reserve_value')
    for fragment in ('exists = scope:rw_service_price','add = scope:rw_service_price','multiply = 2'):
        if fragment not in reserve:
            errors.append('reserve ignores latest cost')
    for name,guards,base,resource in (
        ('rw_ai_service_accept_weight',('rw_service_client_turn_trigger = yes','rw_service_affordable_trigger = yes'),30,'gold < rw_ai_service_reserve_value'),
        ('rw_ai_case_repair_weight',('rw_case_provider_turn_trigger = yes','prestige >= 25'),50,'prestige < 50')):
        value = block(values,name)
        for fragment in ('value = 0', 'multiply = rw_ai_cooperation_factor','add = '+str(base), *guards,
                         'limit = { '+resource+' } multiply = 0.5'):
            if fragment not in value:
                errors.append('family bypasses shared policy cost or turn')
    for text,name,weight,guards in (
        (service,'rw_services.accept_50','rw_ai_service_accept_weight',('rw_service_client_turn_trigger = yes','rw_service_affordable_trigger = yes','NOT = { rw_service_deferred_trigger = yes }')),
        (service,'rw_services.promise_50','rw_ai_service_accept_weight',('rw_service_client_turn_trigger = yes','rw_service_affordable_trigger = yes','rw_service_deferred_trigger = yes')),
        (cases,'rw_cases.apologise','rw_ai_case_repair_weight',('rw_case_provider_turn_trigger = yes','prestige >= 25'))):
        view = option(text,name)
        chance = nested_block(view,'ai_chance')
        if 'base = 0' not in chance or 'add = '+weight not in chance or 'always = yes' not in chance:
            errors.append('policy not used by both families')
        gate = nested_block(view,'trigger')
        if any(guard not in gate for guard in guards):
            errors.append('AI wiring bypasses action prerequisites')
    code = clean_script(triggers + values)[0]
    if re.search(r'\b(?:is_ai|set_variable|save_scope_as|save_scope_value_as|add_gold|add_prestige|add_opinion|add_hook|trigger_event|create_story|every_\w+|any_living_character|is_scheme_exposed|has_secret|rw_case_evidence)\s*=',code):
        errors.append('policy mutates state scans globally or reads hidden information')
    return errors


class PoliticalAiTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_political_ai_triggers.txt').read_text()
        self.v = (MOD/'common/script_values/rw_political_ai_values.txt').read_text()
        self.s = (MOD/'events/rw_service_events.txt').read_text()
        self.c = (MOD/'events/rw_case_events.txt').read_text()

    def errors(self, **changes):
        return policy_errors(changes.get('t',self.t),changes.get('v',self.v),
                             changes.get('s',self.s),changes.get('c',self.c))

    def test_policy_wired_to_two_families(self):
        self.assertEqual(self.errors(), [])

    def test_missing_foreign_or_self_party_mutations(self):
        for guard in ('exists = scope:rw_service_provider','exists = scope:rw_service_client',
                      'NOT = { scope:rw_service_provider = scope:rw_service_client }',
                      'OR = { this = scope:rw_service_provider this = scope:rw_service_client }'):
            with self.subTest(guard=guard):
                self.assertIn('foreign or missing decider admitted',self.errors(t=self.t.replace(guard,'always = yes',1)))
        self.assertIn('unknown context given willingness',self.errors(v=self.v.replace('value = 0','value = 1',1)))

    def test_opinion_belongs_to_actual_decider(self):
        for role in ('provider','client'):
            with self.subTest(role=role):
                self.assertIn('counterpart or decider opinion substituted',self.errors(t=self.t.replace(
                    'opinion = { target = scope:rw_service_'+role,'opinion = { target = scope:rw_case_mediator',1)))

    def test_context_factors_cannot_become_cosmetic(self):
        for trigger in ('trusted_counterpart','hostile_counterpart','existing_commitment'):
            with self.subTest(trigger=trigger):
                self.assertIn('context factor disconnected',self.errors(v=self.v.replace(
                    'rw_ai_'+trigger+'_trigger = yes','always = yes',1)))
        self.assertIn('military burden disconnected',self.errors(v=self.v.replace('is_at_war = yes','always = yes')))

    def test_own_obligation_and_actual_cost_required(self):
        self.assertIn('own existing duty ignored',self.errors(t=self.t.replace('has_character_flag = rw_fv_obligation','always = yes')))
        self.assertIn('reserve ignores latest cost',self.errors(v=self.v.replace('add = scope:rw_service_price','add = 50')))
        self.assertIn('family bypasses shared policy cost or turn',self.errors(v=self.v.replace('gold < rw_ai_service_reserve_value','gold < 1')))
        self.assertIn('family bypasses shared policy cost or turn',self.errors(v=self.v.replace('prestige < 50','prestige < 1')))

    def test_existing_turn_and_affordability_guards_remain(self):
        for field,guard in (('s','rw_service_affordable_trigger = yes'),('c','prestige >= 25')):
            with self.subTest(field=field):
                self.assertIn('AI wiring bypasses action prerequisites',self.errors(**{field:getattr(self,field).replace(guard,'always = yes',1)}))
        self.assertIn('family bypasses shared policy cost or turn',self.errors(v=self.v.replace('rw_case_provider_turn_trigger = yes','always = yes')))

    def test_removing_one_family_call_is_detected(self):
        self.assertIn('policy not used by both families',self.errors(c=self.c.replace('add = rw_ai_case_repair_weight','add = 50')))
        self.assertIn('policy not used by both families',self.errors(s=self.s.replace('add = rw_ai_service_accept_weight','add = 30')))

    def test_policy_cannot_add_effects_privilege_or_secret_access(self):
        for injected in ('add_gold = 100','is_ai = yes','every_living_character = { always = yes }',
                         'has_secret = murder','rw_case_evidence = flag:admitted','set_variable = { name = rw_ai_cache value = 1 }'):
            with self.subTest(injected=injected):
                self.assertIn('policy mutates state scans globally or reads hidden information',self.errors(v=self.v+'\nrw_bad = { '+injected+' }'))

    def test_refusal_counteroffer_and_lapsed_paths_stay_available(self):
        self.assertIn('ai_chance = { base = 40 }',option(self.s,'rw_services.counter_25'))
        self.assertIn('ai_chance = { base = 30 }',option(self.s,'rw_services.refuse'))
        self.assertIn('ai_chance = { base = 50 }',option(self.c,'rw_cases.refuse_repair'))
        for text,name in ((self.s,'rw_services.lapsed'),(self.c,'rw_cases.lapsed')):
            self.assertIn('ai_chance = { base = 100 }',option(text,name))
