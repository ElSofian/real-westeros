"""Inspect real CK3 source and reject dangerous mutations; no runtime game model."""
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from tools import build_g1_native_choice as builder
from tools.validate_mod import brace_errors, clean_script, validate

ROOT = builder.TEMPLATES
EFFECT = 'common/scripted_effects/rw_unlawful_war_response_effects.txt'
TRIGGER = 'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt'
STORY = 'common/story_cycles/rw_unlawful_war_responses.txt'
EVENT = 'events/rw_unlawful_war_response_events.txt'


def block(text,name):
    a,_,b=builder.bounds(text,name)
    return clean_script(text[a:b])[0]


def contract_errors(t,e,s):
    errors=[]
    def require(text,parts,label):
        if any(not re.search(re.escape(x)+r'(?![\w:])',text) for x in parts): errors.append(label)
    register=block(e,'rw_uw_notice_effect')
    require(register,('this = scope:actor','rw_uw_selected_defiance_trigger = yes',
        'count >= 2','using_cb = claim_cb','primary_attacker = scope:actor',
        'primary_defender = scope:recipient','exists = scope:rw_uw_war',
        'any_owned_story =','story_owner = scope:rw_uw_attacker',
        'var:rw_uw_war = scope:rw_uw_war','NOT = { has_variable = rw_uw_serial }',
        'name = rw_uw_source value = flag:native_choice_accept',
        'name = rw_uw_live value = flag:yes days = 14',
        'name = rw_uw_issuer_window value = flag:yes days = 7'),'declaration/replay/deadline')
    require(block(t,'rw_uw_active_record_trigger'),('story_owner = var:rw_uw_attacker',
        'exists = var:rw_uw_war','this = scope:rw_uw_check.var:rw_uw_war',
        'primary_attacker = scope:rw_uw_check.var:rw_uw_attacker',
        'primary_defender = scope:rw_uw_check.var:rw_uw_defender','using_cb = claim_cb'),'exact active native war')
    identity=block(t,'rw_uw_response_identity_trigger')
    require(identity,('rw_uw_active_record_trigger = yes','has_variable = rw_uw_live',
        'holder = scope:rw_uw_issuer','var:rw_uw_serial = scope:rw_uw_serial',
        'var:rw_uw_war = scope:rw_uw_war','var:rw_uw_authority = scope:rw_uw_authority',
        'var:rw_uw_attacker = scope:rw_uw_attacker','var:rw_uw_defender = scope:rw_uw_defender',
        'var:rw_uw_issuer = scope:rw_uw_issuer'),'identity/authority')
    if identity.count('liege = scope:rw_uw_issuer')!=2: errors.append('current jurisdiction')
    for name,turn,state in [('rw_uw_issuer_turn_trigger','scope:rw_uw_issuer','pending'),
                            ('rw_uw_answer_turn_trigger','scope:rw_uw_attacker','demanded')]:
        require(block(t,name),('rw_uw_response_identity_trigger = yes','this = '+turn,
            'var:rw_uw_state = flag:'+state,'has_variable = rw_uw_'+('issuer_window' if state=='pending' else 'answer_window')),'current turn')
    for name,guard,result in [('ignore','issuer','ignored'),('censure','issuer','censured'),
                              ('acknowledge','answer','acknowledged'),('refuse','answer','refused')]:
        current=block(e,'rw_uw_'+name+'_effect')
        require(current,('limit = { rw_uw_'+guard+'_turn_trigger = yes }',
            'name = rw_uw_state value = flag:closed','name = rw_uw_result value = flag:'+result,
            'remove_variable = rw_uw_live'),'consumed action')
        for operation in ('add_opinion =','send_interface_message ='):
            if operation in current and ('flag:closed' not in current or current.index(operation)<current.index('flag:closed')):
                errors.append('effect before consumption')
    demand=block(e,'rw_uw_demand_effect')
    require(demand,('limit = { rw_uw_issuer_turn_trigger = yes }',
        'name = rw_uw_state value = flag:demanded','name = rw_uw_answer_window value = flag:yes days = 7',
        'remove_variable = rw_uw_issuer_window'),'bounded demand')
    if 'name = rw_uw_live' in demand: errors.append('renewed total deadline')
    require(s,('on_owner_death = { end_story = yes }','rw_uw_active_record_trigger = yes',
        'flag:timed_out','NOT = { has_variable = rw_uw_live }'),'inert retention and cleanup')
    forbidden=r'\b(start_war|end_war|run_interaction|add_claim|add_trait|remove_trait|imprison|execute|change_title_holder|add_gold|add_prestige|add_realm_law|remove_realm_law|use_hook|every_living_character|every_in_global_list|make_story_owner|add_imprisonment_reason)\s*='
    if re.search(forbidden,clean_script(t+e+s)[0]): errors.append('native state/rights mutated')
    return errors


class RoyalResponseSourceTests(unittest.TestCase):
    def setUp(self):
        self.t=(ROOT/TRIGGER).read_text();self.e=(ROOT/EFFECT).read_text();self.s=(ROOT/STORY).read_text()

    def test_current_real_source_contract(self):
        self.assertEqual([],contract_errors(self.t,self.e,self.s))

    def test_missing_declaration_choice_rejected(self):
        self.assertTrue(contract_errors(self.t,self.e.replace('rw_uw_selected_defiance_trigger = yes','always = yes'),self.s))

    def test_wrong_war_or_roles_rejected(self):
        for old,new in [('this = scope:rw_uw_check.var:rw_uw_war','always = yes'),
                        ('primary_defender = scope:rw_uw_check.var:rw_uw_defender','primary_defender = scope:rw_uw_issuer')]:
            with self.subTest(old=old): self.assertTrue(contract_errors(self.t.replace(old,new),self.e,self.s))

    def test_wrong_serial_or_successor_authority_rejected(self):
        for old,new in [('var:rw_uw_serial = scope:rw_uw_serial','has_variable = rw_uw_serial'),
                        ('holder = scope:rw_uw_issuer','holder = scope:rw_uw_attacker'),
                        ('liege = scope:rw_uw_issuer','liege = scope:rw_uw_defender')]:
            with self.subTest(old=old): self.assertTrue(contract_errors(self.t.replace(old,new),self.e,self.s))

    def test_duplicate_registration_and_ambiguous_pair_rejected(self):
        for old,new in [('any_owned_story =','any_other_story ='),('count >= 2','count >= 200')]:
            with self.subTest(old=old): self.assertTrue(contract_errors(self.t,self.e.replace(old,new),self.s))

    def test_replay_turn_or_deadline_mutations_rejected(self):
        for old,new in [('flag:closed','flag:pending'),('flag:demanded','flag:pending'),
                        ('days = 14','days = 140'),('days = 7','days = 70')]:
            with self.subTest(old=old): self.assertTrue(contract_errors(self.t,self.e.replace(old,new),self.s))

    def test_native_war_title_crime_or_cost_mutation_rejected(self):
        for operation in ('end_war = white_peace','start_war = yes','run_interaction = {}',
                          'change_title_holder = yes','add_gold = -50','add_imprisonment_reason = yes'):
            with self.subTest(operation=operation): self.assertTrue(contract_errors(self.t,self.e+'\n bad = { '+operation+' }',self.s))

    def test_source_callback_has_only_one_tail_call_after_native_effects(self):
        from test_g1_native_choice import FIXTURE
        old,patched=builder.patch_native(FIXTURE.encode())
        self.assertEqual(1,patched.count(builder.ACCEPT.encode()))
        self.assertGreater(patched.index(builder.ACCEPT.encode()),patched.index(b'preserved_native_callback = yes'))
        self.assertEqual(old,patched.replace(builder.GUARD.encode(),b'',1).replace(builder.OPTION.encode(),b'',1).replace(builder.ACCEPT.encode(),b'',1))

    def test_censure_and_refusal_have_exact_direction_and_opinion(self):
        self.assertIn('add_opinion = { target = scope:rw_uw_attacker modifier = rw_uw_censured_opinion }',self.e)
        refusal=block(self.e,'rw_uw_refuse_effect')
        self.assertIn('scope:rw_uw_issuer = {',refusal)
        self.assertIn('target = scope:rw_uw_attacker modifier = rw_uw_refused_stop_opinion',refusal)
        opinions=(ROOT/'common/opinion_modifiers/rw_unlawful_war_response_opinions.txt').read_text()
        self.assertIn('opinion = -10 years = 2',opinions)
        self.assertIn('opinion = -15 years = 2',opinions)

    def test_acknowledgement_has_no_native_effect_or_opinion(self):
        text=block(self.e,'rw_uw_acknowledge_effect')
        self.assertNotIn('add_opinion',text)
        self.assertNotIn('complied',text)
        self.assertNotIn('fulfilled',text)

    def test_timeout_and_cleanup_have_no_automatic_punishment(self):
        self.assertNotIn('add_opinion',self.s)
        self.assertNotIn('trigger_event',self.s)
        self.assertIn('days = 30',self.s)
        self.assertNotIn('on_war_started',self.s+self.e)
        # Dedup includes closed/inert records, not just live windows.
        a,_,b=builder.bounds(self.e,'rw_uw_notice_effect')
        dedup=self.e[self.e.index('any_owned_story',a):self.e.index('clear_saved_scope = rw_uw_record',a,b)]
        self.assertNotIn('rw_uw_live',dedup)
        self.assertNotIn('rw_uw_state',dedup)

    def test_ai_uses_burden_means_and_opinion_without_rule_exceptions(self):
        event=(ROOT/EVENT).read_text()
        for condition in ('is_at_war = yes','gold < 50','opinion = { target = scope:rw_uw_attacker'):
            self.assertIn(condition,event)
        a, _, b = builder.bounds(self.t, 'rw_uw_ai_default_defiance_trigger')
        shared = self.t[:a] + self.t[b:] + self.e + event
        # Only initial option preference may branch on AI identity.
        self.assertNotIn('is_ai', shared)
        self.assertNotIn('rw_uw_ai_default_defiance_trigger', shared)
        for effect in ('ignore','censure','demand','acknowledge','refuse'):
            self.assertIn('rw_uw_'+effect+'_effect = yes',event)

    def test_original_module_requires_base_for_structure_and_localization_checks(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);mod=root/'mod/real_westeros';mod.mkdir(parents=True)
            for name in builder.FILES:
                target=mod/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
            for name in ('descriptor.mod',): shutil.copyfile(builder.REPO/'mod/real_westeros'/name,mod/name)
            shutil.copyfile(builder.REPO/'mod/real_westeros.mod',root/'mod/real_westeros.mod')
            for name in ('common/character_interactions','common/on_action'): (mod/name).mkdir(parents=True,exist_ok=True)
            # The adapter declares a Real Westeros dependency. Its thirteen
            # attested runtime inputs alone do not include the shared AI guard.
            self.assertTrue(any('undefined owned trigger rw_ai_existing_commitment_trigger' in error
                                for error in validate(root)))
            shutil.copytree(ROOT, mod, dirs_exist_ok=True)
            self.assertEqual([],validate(root))


if __name__=='__main__': unittest.main()
