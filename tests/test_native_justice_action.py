"""Native arrest dispatch source contracts only; no imprisonment simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def action_errors(t, e, v, intake, journal):
    out = []
    gate = block(t,'rw_ja_can_open_trigger')
    guards = ('rw_scheme_justice_free_trigger = yes','is_imprisoned = no','has_active_diarchy = no',
              'NOT = { has_character_flag = flag_hostile_actions_disabled_delay }',
              'NOT = { has_variable = rw_ja_dispatched_on }',
              'has_imprisonment_reason = scope:rw_scheme_evidence_record.var:rw_evidence_participant',
              'NOT = { has_usable_hook = scope:rw_scheme_evidence_record.var:rw_evidence_participant }',
              'is_character_interaction_valid = {','recipient = scope:rw_scheme_evidence_record.var:rw_evidence_participant','interaction = imprison_interaction')
    if any(g not in gate for g in guards): out.append('native eligibility identity or conservative terms bypassed')
    view = block(t,'rw_ja_view_trigger')
    if any(g not in view for g in ('rw_scheme_justice_living_trigger = yes','exists = scope:rw_ja_target',
                                   'var:rw_evidence_participant = scope:rw_ja_target')):
        out.append('displayed target no longer bound to record')
    attempt_gate = block(t,'rw_ja_can_attempt_trigger')
    if 'rw_ja_view_trigger = yes' not in attempt_gate or 'rw_ja_can_open_trigger = yes' not in attempt_gate:
        out.append('fresh dispatch guard bypassed')
    opened = block(e,'rw_ja_open_effect')
    if any(g not in opened for g in ('limit = { rw_ja_can_open_trigger = yes }',
                                     'scope:rw_scheme_evidence_record.var:rw_evidence_participant = { save_scope_as = rw_ja_target }',
                                     'trigger_event = { id = rw_justice_actions.0001 }')):
        out.append('confirmation captures wrong target or lacks revalidation')
    attempt = block(e,'rw_ja_attempt_effect')
    if 'limit = { rw_ja_can_attempt_trigger = yes }' not in attempt:
        out.append('fresh dispatch guard bypassed')
    positions=[attempt.find(g) for g in ('name = rw_ja_dispatched_on value = current_date',
              'name = rw_ja_actor value = scope:rw_scheme_observer','name = rw_ja_target value = scope:rw_ja_target','run_interaction = {')]
    if min(positions)<0 or positions!=sorted(positions): out.append('dispatch receipt not consumed before native attempt')
    native=nested_block(attempt,'run_interaction')
    for g in ('interaction = imprison_interaction','actor = root','recipient = scope:rw_ja_target','send_threshold = decline'):
        if g not in native:out.append('native sender target or refusal route replaced')
    code=clean_script(t+e+v)[0]
    if code.count('run_interaction = {')!=1 or 'execute_threshold' in code:
        out.append('forced acceptance or duplicate native path')
    if re.search(r'\b(?:imprison|death|rightfully_imprison_character_effect|imprison_character_effect|consume_imprisonment_reasons|add_gold|add_prestige|add_hook|use_hook|change_title_holder|add_secret|every_living_character|every_owned_story|is_ai)\s*=',code):
        out.append('native replacement privilege or global scan added')
    fields=set(re.findall(r'\bset_variable\s*=\s*\{\s*name\s*=\s*(\w+)',code))
    if not fields <= {'rw_ja_scheduled','rw_ja_dispatched_on','rw_ja_actor','rw_ja_target'}:out.append('unrelated state written')
    scheduled=block(e,'rw_ja_schedule_effect')
    for g in ('scope:rw_scheme_observer = {','rw_scheme_justice_view_trigger = yes',
              'NOT = { has_variable = rw_ja_scheduled }','NOT = { has_variable = rw_ja_dispatched_on }'):
        if g not in scheduled:out.append('schedule bypasses exact participant or once guard')
    if scheduled.find('name = rw_ja_scheduled')<0 or scheduled.find('name = rw_ja_scheduled')>scheduled.find('trigger_event = { id = rw_justice_actions.0002 days = 1 }'):
        out.append('opportunity can repeat before marking')
    create=block(intake,'rw_scheme_create_evidence_effect')
    if create.count('rw_ja_schedule_effect = yes')!=1 or create.find('rw_ja_schedule_effect = yes')<create.find('name = rw_evidence_participant'):
        out.append('opportunity not after original participant construction')
    if 'rw_ja_schedule_effect' in journal or code.count('days = 1')!=1:
        out.append('archive requeues or recurring opportunity added')
    prompt=block(v,'rw_justice_actions.0001')
    if 'trigger = { rw_ja_can_attempt_trigger = yes }' not in prompt or 'rw_ja_attempt_effect = yes' not in prompt:
        out.append('choice not guarded or dispatch disconnected')
    if 'name = rw_justice_action.leave ai_chance = { base = 50 }' not in prompt:
        out.append('discretionary no-action choice lost')
    hidden=block(v,'rw_justice_actions.0002')
    if 'hidden = yes' not in hidden or 'immediate = { rw_ja_open_effect = yes }' not in hidden or 'rw_ja_attempt_effect' in hidden:
        out.append('opportunity itself sends arrest')
    return out


class NativeJusticeActionTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_justice_action_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_justice_action_effects.txt').read_text()
        self.v=(MOD/'events/rw_justice_action_events.txt').read_text()
        self.i=(MOD/'common/scripted_effects/rw_scheme_evidence_effects.txt').read_text()
        self.j=(MOD/'events/rw_scheme_evidence_events.txt').read_text()

    def errors(self,**changes):
        return action_errors(*(changes.get(k,getattr(self,k)) for k in ('t','e','v','i','j')))

    def test_native_pipeline_contract(self):
        self.assertEqual([],self.errors())

    def test_identity_native_eligibility_and_terms_mutations(self):
        for guard in ('rw_scheme_justice_free_trigger = yes','is_imprisoned = no','has_active_diarchy = no',
                      'NOT = { has_variable = rw_ja_dispatched_on }','interaction = imprison_interaction',
                      'has_imprisonment_reason = scope:rw_scheme_evidence_record.var:rw_evidence_participant',
                      'NOT = { has_usable_hook = scope:rw_scheme_evidence_record.var:rw_evidence_participant }'):
            with self.subTest(guard=guard):
                self.assertIn('native eligibility identity or conservative terms bypassed',self.errors(t=self.t.replace(guard,'always = yes',1)))

    def test_target_frozen_in_confirmation(self):
        self.assertIn('displayed target no longer bound to record',self.errors(t=self.t.replace('var:rw_evidence_participant = scope:rw_ja_target','always = yes')))
        self.assertIn('confirmation captures wrong target or lacks revalidation',self.errors(e=self.e.replace('save_scope_as = rw_ja_target','save_scope_as = rw_other_target')))

    def test_direct_effect_cannot_skip_current_guard(self):
        self.assertIn('fresh dispatch guard bypassed',self.errors(e=self.e.replace('limit = { rw_ja_can_attempt_trigger = yes }','limit = { always = yes }')))
        self.assertIn('fresh dispatch guard bypassed',self.errors(t=self.t.replace('rw_ja_view_trigger = yes','always = yes')))

    def test_receipt_consumed_before_dispatch_and_never_claims_success(self):
        moved=self.e.replace('set_variable = { name = rw_ja_dispatched_on value = current_date }','')
        moved=moved.replace('send_threshold = decline','send_threshold = decline\nset_variable = { name = rw_ja_dispatched_on value = current_date }')
        self.assertIn('dispatch receipt not consumed before native attempt',self.errors(e=moved))
        for false_outcome in ('rw_ja_arrest_succeeded','rw_ja_guilt','rw_ja_sanction_completed'):
            self.assertNotIn(false_outcome,self.e+self.v)

    def test_native_refusal_actor_and_target_cannot_be_substituted(self):
        for fragment in ('actor = root','recipient = scope:rw_ja_target','send_threshold = decline'):
            with self.subTest(fragment=fragment):
                self.assertIn('native sender target or refusal route replaced',self.errors(e=self.e.replace(fragment,'always = yes')))
        self.assertIn('forced acceptance or duplicate native path',self.errors(e=self.e.replace('send_threshold = decline','execute_threshold = accept')))

    def test_no_native_helpers_extra_payments_privilege_or_global_scan(self):
        for extra in ('imprison = {}','rightfully_imprison_character_effect = {}','add_prestige = -10',
                      'use_hook = root','is_ai = no','every_living_character = {}'):
            with self.subTest(extra=extra):
                self.assertIn('native replacement privilege or global scan added',self.errors(e=self.e+'\nrw_bad = { '+extra+' }'))

    def test_opportunity_is_bounded_and_never_punishes(self):
        self.assertIn('schedule bypasses exact participant or once guard',self.errors(e=self.e.replace('NOT = { has_variable = rw_ja_scheduled }','always = yes')))
        self.assertIn('archive requeues or recurring opportunity added',self.errors(j=self.j+'\nrw_ja_schedule_effect = yes'))
        self.assertIn('opportunity itself sends arrest',self.errors(v=self.v.replace('immediate = { rw_ja_open_effect = yes }','immediate = { rw_ja_attempt_effect = yes }')))
        self.assertIn('discretionary no-action choice lost',self.errors(v=self.v.replace('name = rw_justice_action.leave','name = rw_justice_action.attempt')))

    def test_localization_exact_target_and_no_completion_claim(self):
        keys=set(re.findall(r'\b(?:title|desc|name)\s*=\s*(rw_justice_action\.[\w.]+)',self.v+self.j))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_justice_action_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys,set(re.findall(r'^\s+(rw_justice_action\.[\w.]+):0',text,re.M)))
            self.assertIn('[rw_ja_target.GetTitledFirstName]',text)
            self.assertNotIn('scheme_owner',text)
