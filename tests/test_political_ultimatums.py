"""Adversarial source contracts for native CK3 ultimatum wiring, not a game model."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from test_political_ai import option
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT/'mod/real_westeros'
FILES = {
    't': 'common/scripted_triggers/rw_ultimatum_triggers.txt',
    'e': 'common/scripted_effects/rw_ultimatum_effects.txt',
    'v': 'events/rw_ultimatum_events.txt',
    'jt': 'common/scripted_triggers/rw_justice_action_triggers.txt',
    'je': 'common/scripted_effects/rw_justice_action_effects.txt',
    'jv': 'events/rw_justice_action_events.txt',
    'journal': 'events/rw_scheme_justice_events.txt',
}


def ultimatum_errors(src):
    t,e,v,jt,je,jv,journal = (src[k] for k in FILES)
    errors = []
    identity = block(t,'rw_ut_identity_trigger')
    for guard in ('exists = scope:rw_scheme_observer','exists = scope:rw_scheme_evidence_record',
                  'exists = scope:rw_scheme_evidence_serial','exists = scope:rw_ja_target',
                  'NOT = { scope:rw_scheme_observer = scope:rw_ja_target }',
                  'story_type = story_rw_scheme_evidence','story_owner = scope:rw_scheme_observer',
                  'var:rw_evidence_schema = 1','has_variable = rw_evidence_retained',
                  'var:rw_evidence_serial = scope:rw_scheme_evidence_serial',
                  'var:rw_evidence_kind = flag:participant_exposed',
                  'var:rw_evidence_participant = scope:rw_ja_target','var:rw_ut_schema = 1',
                  'var:rw_ut_issuer = scope:rw_scheme_observer','var:rw_ut_target = scope:rw_ja_target',
                  'has_variable = rw_ut_issued_on','has_variable = rw_ut_state'):
        if guard not in identity: errors.append('wrong original identity or expired observation')
    for role,who in (('issuer','rw_scheme_observer'),('target','rw_ja_target')):
        reader = block(t,'rw_ut_'+role+'_view_trigger')
        if any(g not in reader for g in ('rw_ut_identity_trigger = yes','this = scope:'+who,'is_alive = yes')):
            errors.append('foreign reader or actor admitted')
    parties = block(t,'rw_ut_parties_trigger')
    for g in ('scope:rw_scheme_observer = {','scope:rw_ja_target = {','is_adult = yes',
              'is_landed = yes','is_imprisoned = no','host = this','exists = liege liege = scope:rw_scheme_observer',
              'is_courtier_of = scope:rw_scheme_observer'):
        if g not in parties:errors.append('authority or living free parties bypassed')
    if parties.count('is_alive = yes') != 2 or parties.count('is_adult = yes') != 2 or parties.count('is_imprisoned = no') != 2:
        errors.append('authority or living free parties bypassed')
    for g in ('rw_ja_can_attempt_trigger = yes','rw_ut_parties_trigger = yes',
              'NOT = { has_character_flag = rw_ut_recent }','NOT = { has_variable = rw_ut_schema }'):
        if g not in block(t,'rw_ut_can_issue_trigger'): errors.append('uncredible repeated or spam issue')
    answer = block(t,'rw_ut_can_answer_trigger')
    if any(g not in answer for g in ('rw_ut_target_view_trigger = yes','rw_ut_parties_trigger = yes',
                                    'has_variable = rw_ut_live','has_variable = rw_ut_answer_window','var:rw_ut_state = flag:waiting')):
        errors.append('stale or foreign answer admitted')
    # The target never queries the issuer's private present legal grounds or journal.
    if re.search(r'rw_ja_can_|rw_scheme_evidence_(?:view|reader)|has_imprisonment_reason',answer):
        errors.append('target reads undisclosed legal state')
    if any(g not in block(t,'rw_ut_can_apologise_trigger') for g in ('rw_ut_can_answer_trigger = yes','prestige >= 25')):
        errors.append('apology cost or turn bypassed')
    for name,guard in (('issue','rw_ut_can_issue_trigger'),('apologise','rw_ut_can_apologise_trigger'),
                       ('reject','rw_ut_can_answer_trigger'),('withdraw','rw_ut_can_withdraw_trigger'),
                       ('escalate','rw_ut_can_escalate_trigger'),('mark_shared_attempt','rw_ut_can_escalate_trigger')):
        if 'limit = { '+guard+' = yes }' not in block(e,'rw_ut_'+name+'_effect'):
            errors.append('execution lacks fresh revalidation')
    for field,days in (('answer_window',7),('live',14)):
        needle = 'set_variable = { name = rw_ut_'+field+' value = flag:yes days = '+str(days)+' }'
        if e.count(needle) != 1 or needle not in block(e,'rw_ut_issue_effect'):
            errors.append('deadline renewed or changed')
    issue = block(e,'rw_ut_issue_effect')
    for g in ('name = rw_ut_issuer value = scope:rw_scheme_observer','name = rw_ut_target value = scope:rw_ja_target',
              'name = rw_ut_issued_on value = current_date','name = rw_ut_state value = flag:waiting',
              'flag = rw_ut_recent days = 30','scope:rw_ja_target = { trigger_event = { id = rw_ultimatums.0001 } }',
              'trigger_event = { id = rw_ultimatums.0003 days = 8 }'):
        if g not in issue: errors.append('wrong offer snapshot notice or fixed callback')
    apology = block(e,'rw_ut_apologise_effect')
    positions = [apology.find(g) for g in ('name = rw_ut_state value = flag:complied','remove_variable = rw_ut_answer_window',
                                          'remove_variable = rw_ut_live','add_prestige = -25')]
    if min(positions)<0 or positions != sorted(positions) or e.count('add_prestige = -25') != 1:
        errors.append('apology unconsumed or duplicate cost')
    reject = block(e,'rw_ut_reject_effect')
    if 'name = rw_ut_state value = flag:rejected' not in reject or 'remove_variable = rw_ut_answer_window' not in reject:
        errors.append('rejection conflated with silence')
    deadline = block(e,'rw_ut_deadline_effect')
    for g in ('rw_ut_issuer_view_trigger = yes','has_variable = rw_ut_live',
              'NOT = { has_variable = rw_ut_answer_window }','var:rw_ut_state = flag:waiting',
              'name = rw_ut_state value = flag:timed_out'):
        if g not in deadline: errors.append('premature repeated or forged timeout')
    route = block(t,'rw_ut_arrest_route_allowed_trigger')
    if any(g not in route for g in ('NOT = { has_variable = rw_ut_schema }','var:rw_ut_schema = 1',
                                    'has_variable = rw_ut_live','var:rw_ut_state = flag:rejected','var:rw_ut_state = flag:timed_out')):
        errors.append('shared route fails to honor forbearance or expiry')
    if re.search(r'flag:(?:waiting|complied|withdrawn|arrest_requested)',route):
        errors.append('closed or waiting threat can arrest')
    if 'rw_ut_shared_arrest_trigger = yes' not in block(jt,'rw_ja_can_open_trigger'):
        errors.append('old arrest entry bypasses ultimatum')
    shared = block(t,'rw_ut_shared_arrest_trigger')
    if any(g not in shared for g in ('NOT = { has_variable = rw_ut_schema }','rw_ut_identity_trigger = yes',
                                      'rw_ut_parties_trigger = yes','rw_ut_arrest_route_allowed_trigger = yes')):
        errors.append('old arrest entry bypasses identity or authority')
    escalate = block(t,'rw_ut_can_escalate_trigger')
    if any(g not in escalate for g in ('rw_ut_issuer_view_trigger = yes','rw_ut_parties_trigger = yes',
                                       'has_variable = rw_ut_live','var:rw_ut_state = flag:rejected',
                                       'var:rw_ut_state = flag:timed_out','rw_ja_can_attempt_trigger = yes')):
        errors.append('escalation lacks fresh native reason or failed demand')
    marker = block(e,'rw_ut_mark_shared_attempt_effect')
    if any(g not in marker for g in ('name = rw_ut_state value = flag:arrest_requested','remove_variable = rw_ut_live')):
        errors.append('shared arrest lacks one terminal receipt')
    attempt = block(je,'rw_ja_attempt_effect')
    order = [attempt.find(g) for g in ('limit = { rw_ja_can_attempt_trigger = yes }','rw_ut_mark_shared_attempt_effect = yes',
                                      'name = rw_ja_dispatched_on value = current_date','run_interaction = {')]
    if min(order)<0 or order != sorted(order) or 'rw_ja_attempt_effect = yes' not in block(e,'rw_ut_escalate_effect'):
        errors.append('native dispatch detached duplicated or before consumption')
    withdraw = block(t,'rw_ut_can_withdraw_trigger')
    if 'rw_ut_issuer_view_trigger = yes' not in withdraw or re.search(r'rw_ja_can_|rw_ut_parties|gold|prestige|rw_ut_live',withdraw):
        errors.append('free exit requires authority resources or live term')
    open_review = block(t,'rw_ut_can_open_review_trigger')
    if any(g not in open_review for g in ('rw_scheme_justice_view_trigger = yes','var:rw_ut_schema = 1',
                                          'var:rw_ut_issuer = scope:rw_scheme_observer','var:rw_ut_target = var:rw_evidence_participant')):
        errors.append('journal review admits other record or target')
    restore = block(e,'rw_ut_open_review_effect')
    if 'limit = { rw_ut_can_open_review_trigger = yes }' not in restore or 'scope:rw_scheme_evidence_record.var:rw_ut_target = { save_scope_as = rw_ja_target }' not in restore:
        errors.append('journal review admits other record or target')
    if 'rw_ut_issue_effect = yes' not in option(jv,'rw_ut.issue') or 'rw_ut_open_review_effect = yes' not in option(journal,'rw_ut.review'):
        errors.append('player AI or journal entry disconnected')
    for evt,gate in (('rw_ultimatums.0001','rw_ut_target_view_trigger'),('rw_ultimatums.0002','rw_ut_issuer_view_trigger')):
        if 'trigger = { '+gate+' = yes }' not in block(v,evt):errors.append('event delivered to foreign reader')
    if 'name = rw_ut.silent ai_chance = { base = 20 }' not in v or 'name = rw_ut.leave ai_chance = { base = 10 }' not in v:
        errors.append('discretionary silence or nonaction lost')
    code = clean_script(t+e+v)[0]
    if re.search(r'\b(?:run_interaction|execute_threshold|imprison|death|add_gold|add_secret|add_hook|add_imprisonment_reason|consume_imprisonment_reasons|change_title_holder|is_ai|every_\w+|any_living_character|any_owned_story)\s*=',code):
        errors.append('native override privilege mutation or global scan')
    if re.search(r'\b(?:rw_evidence_\w+|rw_case_\w+|rw_ru_\w+)\s*=',clean_script(v)[0]):
        errors.append('event leaks or reinterprets private evidence')
    fields=set(re.findall(r'\bset_variable\s*=\s*\{\s*name\s*=\s*(\w+)',code))
    if any(not f.startswith('rw_ut_') for f in fields):errors.append('native evidence or other protocol rewritten')
    return errors


class PoliticalUltimatumTests(unittest.TestCase):
    def setUp(self):
        self.src = {k:(MOD/p).read_text() for k,p in FILES.items()}

    def errors(self, field=None, old=None, new=None):
        src = self.src.copy()
        if field:src[field] = src[field].replace(old,new)
        return ultimatum_errors(src)

    def test_source_contract(self):
        self.assertEqual([],self.errors())

    def test_stale_serial_owner_target_kind_schema_and_retention_rejected(self):
        for guard in ('story_owner = scope:rw_scheme_observer','var:rw_evidence_serial = scope:rw_scheme_evidence_serial',
                      'var:rw_evidence_participant = scope:rw_ja_target','var:rw_ut_target = scope:rw_ja_target',
                      'var:rw_evidence_kind = flag:participant_exposed','has_variable = rw_evidence_retained','var:rw_ut_schema = 1'):
            with self.subTest(guard=guard):self.assertIn('wrong original identity or expired observation',self.errors('t',guard,'always = yes'))

    def test_wrong_readers_cannot_view_or_answer(self):
        self.assertIn('foreign reader or actor admitted',self.errors('t','this = scope:rw_ja_target','this = scope:rw_scheme_observer'))
        self.assertIn('event delivered to foreign reader',self.errors('v','trigger = { rw_ut_target_view_trigger = yes }','trigger = { always = yes }'))

    def test_current_authority_and_free_living_parties_required(self):
        for guard in ('is_courtier_of = scope:rw_scheme_observer','liege = scope:rw_scheme_observer','is_alive = yes','is_imprisoned = no'):
            self.assertIn('authority or living free parties bypassed',self.errors('t',guard,'always = yes'))

    def test_issue_cannot_fabricate_credibility_replay_or_spam(self):
        for guard in ('rw_ja_can_attempt_trigger = yes','NOT = { has_character_flag = rw_ut_recent }','NOT = { has_variable = rw_ut_schema }'):
            self.assertIn('uncredible repeated or spam issue',self.errors('t',guard,'always = yes'))

    def test_target_does_not_read_private_legal_state(self):
        self.assertIn('target reads undisclosed legal state',self.errors('t','rw_ut_target_view_trigger = yes\n    rw_ut_parties_trigger = yes','rw_ut_target_view_trigger = yes\n    rw_ut_parties_trigger = yes\n    rw_ja_can_attempt_trigger = yes'))

    def test_deadlines_cannot_be_renewed(self):
        for old,new in (('days = 7 }','days = 30 }'),('days = 14 }','days = 60 }')):
            self.assertIn('deadline renewed or changed',self.errors('e',old,new))
        self.assertIn('wrong offer snapshot notice or fixed callback',self.errors('e','id = rw_ultimatums.0003 days = 8','id = rw_ultimatums.0003 days = 7'))

    def test_expired_or_already_answered_view_cannot_charge(self):
        for guard in ('has_variable = rw_ut_answer_window','var:rw_ut_state = flag:waiting','has_variable = rw_ut_live'):
            self.assertIn('stale or foreign answer admitted',self.errors('t',guard,'always = yes'))
        self.assertIn('apology cost or turn bypassed',self.errors('t','prestige >= 25','always = yes'))
        self.assertIn('apology unconsumed or duplicate cost',self.errors('e','name = rw_ut_state value = flag:complied','name = rw_ut_state value = flag:waiting'))

    def test_rejection_is_not_silence_or_admission(self):
        self.assertIn('rejection conflated with silence',self.errors('e','name = rw_ut_state value = flag:rejected','name = rw_ut_state value = flag:timed_out'))
        self.assertIn('native evidence or other protocol rewritten',self.errors('e','name = rw_ut_answered_on','name = rw_evidence_guilt'))

    def test_deadline_checks_window_role_and_prior_response(self):
        for guard in ('NOT = { has_variable = rw_ut_answer_window }','var:rw_ut_state = flag:waiting','rw_ut_issuer_view_trigger = yes'):
            self.assertIn('premature repeated or forged timeout',self.errors('e',guard,'always = yes'))

    def test_older_arrest_entry_cannot_skip_wait_close_or_expiry(self):
        self.assertIn('old arrest entry bypasses ultimatum',self.errors('jt','rw_ut_shared_arrest_trigger = yes','always = yes'))
        self.assertIn('closed or waiting threat can arrest',self.errors('t','var:rw_ut_state = flag:rejected\n                var:rw_ut_state = flag:timed_out','var:rw_ut_state = flag:waiting\n                var:rw_ut_state = flag:timed_out'))
        self.assertIn('shared route fails to honor forbearance or expiry',self.errors('t','has_variable = rw_ut_live','always = yes'))

    def test_shared_older_entry_rechecks_exact_parties_and_authority(self):
        for guard in ('rw_ut_identity_trigger = yes','rw_ut_parties_trigger = yes','rw_ut_arrest_route_allowed_trigger = yes'):
            self.assertIn('old arrest entry bypasses identity or authority',self.errors('t',guard,'always = yes'))

    def test_escalation_preserves_actual_native_prerequisites(self):
        for guard in ('rw_ja_can_attempt_trigger = yes','rw_ut_parties_trigger = yes','has_variable = rw_ut_live'):
            self.assertIn('escalation lacks fresh native reason or failed demand',self.errors('t',guard,'always = yes'))
        # The unchanged J2 source tests separately cover native reason, hook,
        # diarchy, interaction validity, send threshold and exact dispatch target.
        self.assertIn('send_threshold = decline',self.src['je'])
        self.assertNotIn('execute_threshold',self.src['je'])

    def test_both_arrest_entries_consume_same_shared_attempt_before_dispatch(self):
        self.assertIn('native dispatch detached duplicated or before consumption',self.errors('je','rw_ut_mark_shared_attempt_effect = yes',''))
        self.assertIn('shared arrest lacks one terminal receipt',self.errors('e','name = rw_ut_state value = flag:arrest_requested','name = rw_ut_state value = flag:rejected'))

    def test_withdrawal_does_not_require_prestige_reason_or_authority(self):
        self.assertIn('free exit requires authority resources or live term',self.errors('t','rw_ut_can_withdraw_trigger = {\n    rw_ut_issuer_view_trigger = yes','rw_ut_can_withdraw_trigger = {\n    rw_ut_issuer_view_trigger = yes\n    rw_ut_parties_trigger = yes'))

    def test_review_restores_original_exact_target_without_resending(self):
        self.assertIn('journal review admits other record or target',self.errors('e','scope:rw_scheme_evidence_record.var:rw_ut_target = { save_scope_as = rw_ja_target }','scope:rw_scheme_observer = { save_scope_as = rw_ja_target }'))
        review=block(self.src['e'],'rw_ut_open_review_effect')
        self.assertNotRegex(review,r'\b(?:set_variable|rw_ut_issue_effect|rw_ja_attempt_effect)\s*=')

    def test_player_ai_entries_and_optional_silence_preserved(self):
        self.assertIn('player AI or journal entry disconnected',self.errors('jv','rw_ut_issue_effect = yes',''))
        self.assertIn('discretionary silence or nonaction lost',self.errors('v','name = rw_ut.silent','name = rw_ut.apologise'))
        self.assertIn('event leaks or reinterprets private evidence',self.errors('v','namespace = rw_ultimatums','namespace = rw_ultimatums\nrw_case_evidence = flag:admitted'))

    def test_no_native_replacement_global_scan_or_inherited_guilt(self):
        for bad in ('imprison = {}','add_imprisonment_reason = scope:rw_ja_target','run_interaction = {}',
                    'add_gold = 25','every_living_character = {}','is_ai = yes'):
            self.assertIn('native override privilege mutation or global scan',self.errors('e','rw_ut_issue_effect = {','rw_bad = { '+bad+' }\nrw_ut_issue_effect = {'))
        story=(MOD/'common/story_cycles/rw_scheme_evidence.txt').read_text()
        self.assertIn('on_owner_death = { end_story = yes }',story)

    def test_recipient_effect_previews_hide_private_record_internals(self):
        for name,key in (('apologise','apology_effect'),('reject','rejection_effect')):
            body=block(self.src['e'],'rw_ut_'+name+'_effect')
            hidden=nested_block(body,'hidden_effect')
            self.assertIn('custom_tooltip = rw_ut.'+key,body)
            self.assertIn('limit = { rw_ut_can_',hidden)
            self.assertIn('scope:rw_scheme_evidence_record = {',hidden)
            self.assertNotIn('rw_scheme_evidence_record',body.replace('hidden_effect = {'+hidden+'}',''))

    def test_localization_covers_new_entries_in_both_languages(self):
        keys=set(re.findall(r'\b(?:name|title|desc|custom_tooltip)\s*=\s*(rw_ut\.[\w.]+)',self.src['e']+self.src['v']+self.src['jv']+self.src['journal']))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_ultimatum_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            found=set(re.findall(r'^\s+(rw_ut\.[\w.]+):0',p.read_text(encoding='utf-8-sig'),re.M))
            self.assertEqual(keys,found)
