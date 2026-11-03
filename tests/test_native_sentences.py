"""Native sentence policy/source mutations only; no Python sentencing simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from test_political_ai import option
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def sentence_errors(t,e,v,story):
    errors=[]
    def need(body,parts,message):
        if any(p not in body for p in parts):errors.append(message)
    eligibility=block(t,'rw_jp_can_open_trigger')
    need(eligibility,('rw_sentencing_current_prisoner_trigger = yes','is_adult = yes','is_landed = yes',
        'is_at_war = no','has_active_diarchy = no','NOT = { has_variable = rw_jp_dispatched_on }',
        'NOT = { has_strong_hook = scope:rw_scheme_observer }',
        'NOT = { has_character_flag = being_prisonbroken_by_laamp }','NOT = { has_character_flag = keep_imprisoned }',
        'NOT = { rw_jp_pair_blocked_trigger = yes }','is_character_interaction_valid = {',
        'recipient = scope:rw_scheme_evidence_record.var:rw_evidence_participant','interaction = execute_prisoner_interaction'),
        'native custody eligibility or protection bypassed')
    if 'has_execute_reason' in eligibility or 'has_imprisonment_reason' in eligibility:errors.append('basis wrongly blocks one of the discretionary choices')
    view=block(t,'rw_jp_view_trigger')
    need(view,('rw_sentencing_current_prisoner_trigger = yes','exists = scope:rw_jp_target','exists = scope:rw_jp_basis',
               'var:rw_evidence_participant = scope:rw_jp_target'),'target or confirmation basis not frozen')
    basis=block(t,'rw_jp_basis_matches_trigger')
    need(basis,('rw_jp_view_trigger = yes','scope:rw_jp_basis = flag:recognized has_execute_reason = scope:rw_jp_target',
                'scope:rw_jp_basis = flag:unrecognized NOT = { has_execute_reason = scope:rw_jp_target }'),
                'stale basis silently reclassified or arrest reason substituted')
    attempt=block(t,'rw_jp_can_attempt_trigger')
    need(attempt,('rw_jp_can_open_trigger = yes','rw_jp_basis_matches_trigger = yes'),'fresh reason or eligibility guard detached')
    for kind,flag in (('reasoned','recognized'),('arbitrary','unrecognized')):
        need(block(t,'rw_jp_can_'+kind+'_trigger'),('rw_jp_can_attempt_trigger = yes','scope:rw_jp_basis = flag:'+flag),'mutually exclusive choice disconnected')
        chosen=option(v,'rw_native_sentence.'+kind)
        need(chosen,('trigger = { rw_jp_can_'+kind+'_trigger = yes }','rw_jp_attempt_effect = yes','ai_chance = {'),'player or AI branch bypasses shared dispatch')
    opened=block(e,'rw_jp_open_effect')
    need(opened,('limit = { rw_jp_can_open_trigger = yes }',
        'scope:rw_scheme_evidence_record.var:rw_evidence_participant = { save_scope_as = rw_jp_target }',
        'has_execute_reason = scope:rw_jp_target','name = rw_jp_basis value = flag:recognized',
        'name = rw_jp_basis value = flag:unrecognized'),'confirmation silently chooses another target or lacks basis capture')
    if re.search(r'\b(?:set_variable|add_character_flag|run_interaction|add_\w+)\s*=',opened):errors.append('navigation mutates world or sentence state')
    dispatch=block(e,'rw_jp_attempt_effect')
    need(dispatch,('limit = { rw_jp_can_attempt_trigger = yes }','name = rw_jp_schema value = 1',
        'name = rw_jp_actor value = scope:rw_scheme_observer','name = rw_jp_target value = scope:rw_jp_target',
        'name = rw_jp_basis value = scope:rw_jp_basis','name = rw_jp_dispatched_on value = current_date',
        'name = rw_jp_pair_window value = flag:yes days = 10'),'missing fresh dispatch or historical attempt receipt')
    positions=[dispatch.find(g) for g in ('name = rw_jp_basis value = scope:rw_jp_basis',
        'name = rw_jp_dispatched_on value = current_date','name = rw_jp_pair_window value = flag:yes days = 10','run_interaction = {')]
    if min(positions)<0 or positions!=sorted(positions):errors.append('native request before immutable attempt and pair lock')
    native=nested_block(dispatch,'run_interaction')
    need(native,('interaction = execute_prisoner_interaction','actor = root','recipient = scope:rw_jp_target','send_threshold = decline'),
         'native default send or actual actor target replaced')
    pair=block(t,'rw_jp_pair_blocked_trigger')
    need(pair,('any_owned_story = {','story_type = story_rw_scheme_evidence','story_owner = scope:rw_scheme_observer',
        'var:rw_evidence_schema = 1','var:rw_evidence_kind = flag:participant_exposed','var:rw_jp_schema = 1',
        'var:rw_jp_actor = scope:rw_scheme_observer','var:rw_jp_target = scope:rw_scheme_evidence_record.var:rw_evidence_participant',
        'has_variable = rw_jp_dispatched_on','has_variable = rw_jp_pair_window'), 'pair check leaks or permits duplicate other-record attempt')
    need(story,('NOT = { has_variable = rw_evidence_retained }','NOT = { has_variable = rw_jp_pair_window }'),
         'source retirement can erase a live pair lock')
    receipt=block(t,'rw_jp_receipt_trigger')
    need(receipt,('rw_scheme_evidence_view_trigger = yes','var:rw_evidence_kind = flag:participant_exposed','var:rw_jp_schema = 1',
        'has_variable = rw_jp_dispatched_on','var:rw_jp_actor = scope:rw_scheme_observer',
        'var:rw_jp_target = var:rw_evidence_participant','var:rw_jp_basis = flag:recognized','var:rw_jp_basis = flag:unrecognized'),
        'foreign historical receipt admitted')
    if re.search(r'has_execute_reason|is_alive|is_imprisoned|rw_jp_can_attempt',receipt):errors.append('past receipt rejudged from current world')
    historical=block(v,'rw_native_sentences.0003')
    need(historical,('trigger = { rw_jp_receipt_view_trigger = yes }','var:rw_jp_basis = flag:recognized','rw_native_sentence.receipt_limits'), 'historical label not bound to immutable basis')
    if 'has_execute_reason' in historical or 'rw_jp_can_' in historical:errors.append('past receipt rejudged from current world')
    need(block(t,'rw_jp_receipt_view_trigger'),('rw_jp_receipt_trigger = yes','exists = scope:rw_jp_target','var:rw_jp_target = scope:rw_jp_target'),'historical portrait names another target')
    entry=block(e,'rw_jp_opportunity_effect')
    need(entry,('story_type = story_rw_scheme_evidence','has_variable = rw_evidence_retained',
        'NOT = { has_variable = rw_jp_notified }','NOT = { has_variable = rw_jp_dispatched_on }',
        'save_scope_as = rw_scheme_evidence_record','name = rw_scheme_evidence_serial value = var:rw_evidence_serial',
        'story_owner = { save_scope_as = rw_scheme_observer }','limit = { rw_jp_can_open_trigger = yes }',
        'name = rw_jp_notified value = flag:yes','rw_jp_open_effect = yes'),'unbounded or foreign custody opportunity')
    for part in (entry,block(e,'rw_jp_schedule_effect'),block(v,'rw_native_sentences.0002')):
        if 'rw_jp_attempt_effect' in part or 'run_interaction' in part:errors.append('callback sends sentence without decision')
    if e.count('name = rw_jp_pair_window value = flag:yes days = 10')!=1:errors.append('pair window renewed by observation or reads')
    if 'name = rw_native_sentence.leave ai_chance = { base = 50 }' not in v:errors.append('nonintervention choice lost')
    code=clean_script(t+e+v)[0]
    if code.count('run_interaction = {')!=1:errors.append('multiple native sanction paths')
    if re.search(r'\b(?:execute_threshold|death|execute_prisoner_effect|consume_execute_reasons|consume_imprisonment_reasons|add_gold|add_piety|add_prestige|add_tyranny|add_dread|add_opinion|add_secret|change_title_holder|is_ai|any_living_character|every_\w+)\s*=',code):
        errors.append('forced native result duplicate penalty privilege or global scan')
    fields=set(re.findall(r'\bset_variable\s*=\s*\{\s*name\s*=\s*(\w+)',code))
    if any(not name.startswith('rw_jp_') for name in fields):errors.append('native evidence or other affair rewritten')
    return errors


class NativeSentenceTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_native_sentence_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_native_sentence_effects.txt').read_text()
        self.v=(MOD/'events/rw_native_sentence_events.txt').read_text()
        self.s=(MOD/'common/story_cycles/rw_scheme_evidence.txt').read_text()
    def errors(self,field=None,old=None,new=None):
        src={k:getattr(self,k) for k in 'tevs'}
        if field:src[field]=src[field].replace(old,new)
        return sentence_errors(src['t'],src['e'],src['v'],src['s'])
    def test_source_contract(self):self.assertEqual([],self.errors())
    def test_current_custody_and_native_eligibility_are_mandatory(self):
        for g in ('rw_sentencing_current_prisoner_trigger = yes','has_active_diarchy = no','is_at_war = no','is_character_interaction_valid = {'):
            self.assertIn('native custody eligibility or protection bypassed',self.errors('t',g,'always = yes'))
    def test_native_prison_break_and_story_prisoner_protections_remain(self):
        for g in ('NOT = { has_character_flag = being_prisonbroken_by_laamp }','NOT = { has_character_flag = keep_imprisoned }','NOT = { has_strong_hook = scope:rw_scheme_observer }'):
            self.assertIn('native custody eligibility or protection bypassed',self.errors('t',g,'always = yes'))
    def test_frozen_target_and_basis_required(self):
        self.assertIn('target or confirmation basis not frozen',self.errors('t','var:rw_evidence_participant = scope:rw_jp_target','always = yes'))
        self.assertIn('target or confirmation basis not frozen',self.errors('t','exists = scope:rw_jp_basis','always = yes'))
    def test_legal_reason_change_cannot_silently_flip_confirmation(self):
        self.assertIn('stale basis silently reclassified or arrest reason substituted',self.errors('t','has_execute_reason = scope:rw_jp_target','has_imprisonment_reason = scope:rw_jp_target'))
        self.assertIn('fresh reason or eligibility guard detached',self.errors('t','rw_jp_basis_matches_trigger = yes','always = yes'))
    def test_both_qualified_choices_use_the_same_dispatch(self):
        self.assertIn('player or AI branch bypasses shared dispatch',self.errors('v','rw_jp_attempt_effect = yes',''))
        self.assertIn('mutually exclusive choice disconnected',self.errors('t','scope:rw_jp_basis = flag:unrecognized }','scope:rw_jp_basis = flag:recognized }'))
    def test_opening_confirmation_is_navigation_only(self):
        self.assertIn('navigation mutates world or sentence state',self.errors('e','rw_jp_open_effect = {','rw_jp_open_effect = {\n set_variable = { name = rw_jp_bad value = 1 }'))
    def test_dispatch_consumes_receipt_and_pair_lock_first(self):
        for g in ('name = rw_jp_dispatched_on value = current_date','name = rw_jp_basis value = scope:rw_jp_basis','name = rw_jp_pair_window value = flag:yes days = 10'):
            self.assertIn('missing fresh dispatch or historical attempt receipt',self.errors('e',g,'removed'))
    def test_native_actual_actor_target_and_safe_send_preserved(self):
        self.assertIn('native default send or actual actor target replaced',self.errors('e','recipient = scope:rw_jp_target','recipient = root'))
        self.assertIn('native default send or actual actor target replaced',self.errors('e','send_threshold = decline','execute_threshold = accept'))
    def test_pair_lock_is_own_known_records_only_and_cannot_cross_actor(self):
        for g in ('any_owned_story = {','story_owner = scope:rw_scheme_observer','var:rw_jp_actor = scope:rw_scheme_observer','var:rw_jp_target = scope:rw_scheme_evidence_record.var:rw_evidence_participant'):
            self.assertIn('pair check leaks or permits duplicate other-record attempt',self.errors('t',g,'always = yes'))
    def test_expired_source_cannot_erase_a_still_live_dedup_lock(self):
        self.assertIn('source retirement can erase a live pair lock',self.errors('s','NOT = { has_variable = rw_jp_pair_window }','always = yes'))
        evidence=(MOD/'common/scripted_triggers/rw_scheme_evidence_triggers.txt').read_text()
        self.assertIn('has_variable = rw_evidence_retained',block(evidence,'rw_scheme_evidence_reader_trigger'))
    def test_historical_basis_is_not_recomputed_after_native_reason_consumption(self):
        self.assertIn('past receipt rejudged from current world',self.errors('t','rw_jp_receipt_trigger = {','rw_jp_receipt_trigger = {\n has_execute_reason = scope:rw_jp_target'))
        self.assertIn('historical label not bound to immutable basis',self.errors('v','var:rw_jp_basis = flag:recognized','has_execute_reason = scope:rw_jp_target'))
    def test_unknown_legacy_or_foreign_receipts_fail_closed(self):
        for g in ('var:rw_jp_schema = 1','var:rw_jp_actor = scope:rw_scheme_observer','var:rw_jp_target = var:rw_evidence_participant'):
            self.assertIn('foreign historical receipt admitted',self.errors('t',g,'always = yes'))
        self.assertIn('historical portrait names another target',self.errors('t','var:rw_jp_target = scope:rw_jp_target','always = yes'))
    def test_fresh_and_local_opportunities_offer_one_decision_not_execution(self):
        self.assertIn('callback sends sentence without decision',self.errors('v','rw_jp_opportunity_effect = yes','rw_jp_attempt_effect = yes'))
        self.assertIn('unbounded or foreign custody opportunity',self.errors('e','NOT = { has_variable = rw_jp_notified }','always = yes'))
        intake=(MOD/'common/scripted_effects/rw_scheme_evidence_effects.txt').read_text()
        self.assertIn('rw_jp_schedule_effect = yes',block(intake,'rw_scheme_create_evidence_effect'))
        self.assertIn('rw_jp_opportunity_effect = yes',self.s)
    def test_actual_readonly_navigation_entries_exist_and_do_not_replace_native_windows(self):
        sentence=(MOD/'events/rw_sentencing_events.txt').read_text()
        journal=(MOD/'events/rw_scheme_evidence_events.txt').read_text()
        self.assertIn('rw_jp_open_effect = yes',option(sentence,'rw_native_sentence.open'))
        self.assertIn('rw_jp_open_receipt_effect = yes',option(journal,'rw_native_sentence.receipt'))
        self.assertIn('open_interaction_window = {',sentence)
    def test_no_second_penalty_forced_death_secret_or_ai_privilege(self):
        for bad in ('add_tyranny = 20','death = {}','execute_prisoner_effect = {}','consume_execute_reasons = scope:rw_jp_target','is_ai = yes','every_living_character = {}'):
            self.assertIn('forced native result duplicate penalty privilege or global scan',self.errors('e','rw_jp_attempt_effect = {','rw_jp_attempt_effect = {\n'+bad))
        self.assertIn('multiple native sanction paths',self.errors('e','run_interaction = {','run_interaction = {}\nrun_interaction = {'))
    def test_sentence_never_rewrites_source_evidence_or_declares_death(self):
        self.assertIn('native evidence or other affair rewritten',self.errors('e','name = rw_jp_basis value = scope:rw_jp_basis','name = rw_evidence_guilt value = flag:yes'))
        self.assertNotRegex(self.e,r'name\s*=\s*rw_jp_(?:executed|guilty|dead)\b')
    def test_localization_covers_both_choices_receipt_and_existing_entries(self):
        other=(MOD/'events/rw_sentencing_events.txt').read_text()+(MOD/'events/rw_scheme_evidence_events.txt').read_text()
        keys=set(re.findall(r'\b(?:name|title|desc)\s*=\s*(rw_native_sentence\.[\w.]+)',self.v+other))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_native_sentence_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            self.assertEqual(keys,set(re.findall(r'^\s+(rw_native_sentence\.[\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M)))
    def test_nonintervention_never_consumes_or_renews_an_attempt(self):
        leave=option(self.v,'rw_native_sentence.leave')
        self.assertNotIn('rw_jp_attempt_effect',leave)
        self.assertIn('ai_chance = { base = 50 }',leave)
        self.assertEqual(1,self.e.count('name = rw_jp_pair_window value = flag:yes days = 10'))
    def test_arbitrary_arrest_is_not_added_by_bypassing_native_ai_rules(self):
        ja=(MOD/'common/scripted_triggers/rw_justice_action_triggers.txt').read_text()
        self.assertIn('has_imprisonment_reason = scope:rw_scheme_evidence_record.var:rw_evidence_participant',block(ja,'rw_ja_can_open_trigger'))
        self.assertNotIn('imprison_interaction',self.e)
