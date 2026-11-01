"""Static allegation/provenance/access mutations; no Python truth or gameplay model."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def allegation_errors(triggers, effects, case_triggers, case_effects):
    errors = []
    start = block(effects, 'rw_allegation_begin_effect')
    if 'rw_allegation_can_start_trigger = yes' not in start:
        errors.append('initiation bypass')
    for marker in ('name = rw_case_kind value = flag:allegation',
                   'name = rw_case_evidence value = flag:unanswered',
                   'name = rw_case_stage value = flag:respondent'):
        if marker not in start:
            errors.append('allegation starts as something other than unanswered claim')
    if 'rw_case_disclosed value' in clean_script(start)[0]:
        errors.append('undisclosed accusation leaks to ruler')
    answer = block(effects, 'rw_allegation_answer_effect')
    if 'rw_allegation_respondent_turn_trigger = yes' not in answer:
        errors.append('reply not bound to respondent')
    if 'name = rw_case_stage value = flag:claimant' not in answer:
        errors.append('reply remains replayable')
    refer = block(effects, 'rw_allegation_refer_effect')
    if 'rw_allegation_claimant_turn_trigger = yes' not in refer:
        errors.append('unsupported referral')
    if 'name = rw_case_disclosed value = flag:yes' not in refer:
        errors.append('referral does not record disclosure')
    reading = block(case_triggers, 'rw_case_reader_allowed_trigger')
    if 'AND = { var:rw_case_mediator = $READER$ rw_case_disclosed_trigger = yes }' not in reading:
        errors.append('planned mediator can read undisclosed claim')
    admonish = block(case_triggers, 'rw_case_can_admonish_trigger')
    if 'AND = { var:rw_case_kind = flag:allegation var:rw_case_evidence = flag:admitted }' not in admonish:
        errors.append('contested claim can authorize reprimand')
    if 'rw_case_can_admonish_trigger = yes' not in block(case_effects, 'rw_case_admonish_effect'):
        errors.append('reprimand effect bypasses evidence')
    if 'rw_case_disclosed_trigger = yes' not in block(case_triggers, 'rw_case_ruler_turn_trigger'):
        errors.append('ruler can decide before disclosure')
    if 'var:rw_case_kind = scope:rw_case_kind' not in block(case_triggers, 'rw_case_matches_trigger'):
        errors.append('cross-kind callback possible')
    if 'rw_case_evidence' in block(case_effects, 'rw_case_apologise_effect'):
        errors.append('conciliation rewrites statement')
    return errors


class AllegationContractTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_allegation_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_allegation_effects.txt').read_text()
        self.ct = (MOD / 'common/scripted_triggers/rw_case_triggers.txt').read_text()
        self.ce = (MOD / 'common/scripted_effects/rw_case_effects.txt').read_text()

    def errors(self, t=None, e=None, ct=None, ce=None):
        return allegation_errors(self.t if t is None else t, self.e if e is None else e,
                                 self.ct if ct is None else ct, self.ce if ce is None else ce)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_invented_evidence_mutation(self):
        changed = self.e.replace('name = rw_case_evidence value = flag:unanswered', 'name = rw_case_evidence value = flag:admitted')
        self.assertIn('allegation starts as something other than unanswered claim', self.errors(e=changed))

    def test_automatic_disclosure_mutation(self):
        e = self.e.replace('name = rw_case_evidence value = flag:unanswered', 'name = rw_case_disclosed value = flag:yes')
        self.assertIn('undisclosed accusation leaks to ruler', self.errors(e=e))

    def test_forged_reply_mutation(self):
        self.assertIn('reply not bound to respondent', self.errors(e=self.e.replace('rw_allegation_respondent_turn_trigger = yes', 'always = yes')))

    def test_replayed_reply_mutation(self):
        e = self.e.replace('name = rw_case_stage value = flag:claimant', 'name = rw_case_stage value = flag:respondent')
        self.assertIn('reply remains replayable', self.errors(e=e))

    def test_unsupported_referral_mutation(self):
        self.assertIn('unsupported referral', self.errors(e=self.e.replace('rw_allegation_claimant_turn_trigger = yes', 'always = yes')))

    def test_archive_disclosure_bypass(self):
        ct = self.ct.replace('AND = { var:rw_case_mediator = $READER$ rw_case_disclosed_trigger = yes }', 'var:rw_case_mediator = $READER$')
        self.assertIn('planned mediator can read undisclosed claim', self.errors(ct=ct))

    def test_denial_treated_as_admission_mutation(self):
        ct = self.ct.replace('flag:allegation var:rw_case_evidence = flag:admitted', 'flag:allegation var:rw_case_evidence = flag:contested')
        self.assertIn('contested claim can authorize reprimand', self.errors(ct=ct))

    def test_effect_bypasses_evidence_mutation(self):
        ce = self.ce.replace('rw_case_can_admonish_trigger = yes', 'rw_case_ruler_turn_trigger = yes')
        self.assertIn('reprimand effect bypasses evidence', self.errors(ce=ce))

    def test_cross_kind_mutation(self):
        ct = self.ct.replace('var:rw_case_kind = scope:rw_case_kind', 'always = yes')
        self.assertIn('cross-kind callback possible', self.errors(ct=ct))

    def test_apology_does_not_become_admission(self):
        ce = self.ce.replace('add_prestige = -25', 'add_prestige = -25\nset_variable = { name = rw_case_evidence value = flag:admitted }')
        self.assertIn('conciliation rewrites statement', self.errors(ce=ce))

    def test_silence_and_withdrawal_do_not_penalize(self):
        text = (MOD / 'events/rw_allegation_events.txt').read_text()
        ignore = text[text.index('name = rw_allegations.ignore'):text.index('name = rw_cases.lapsed')]
        self.assertNotRegex(clean_script(ignore)[0], r'\brw_\w+_effect\s*=')
        self.assertNotRegex(clean_script(self.e)[0], r'\b(add_gold|add_prestige|add_opinion|death|imprison|add_secret|add_hook)\s*=')
        self.assertNotIn('rw_service_last_outcome', clean_script(self.e)[0])

    def test_missing_provenance_is_not_inferred_as_legacy_truth(self):
        identity = block(self.ct, 'rw_case_matches_trigger')
        self.assertIn('has_variable = rw_case_kind', identity)
        self.assertIn('exists = scope:rw_case_kind', identity)
        knowledge = block(self.ct, 'rw_case_disclosed_trigger')
        self.assertIn('has_variable = rw_case_disclosed', knowledge)
        self.assertNotIn('NOT', knowledge)
        reading = block(self.ct, 'rw_case_reader_allowed_trigger')
        self.assertIn('has_variable = rw_case_kind', reading)

    def test_private_statement_view_has_no_effects(self):
        text = (MOD / 'events/rw_allegation_events.txt').read_text()
        view = block(text, 'rw_allegations.0003')
        self.assertNotRegex(view, r'\brw_\w+_effect\s*=')
        self.assertIn('rw_allegation_can_read_statement_trigger = yes', view)
        access = block(self.t, 'rw_allegation_can_read_statement_trigger')
        self.assertIn('rw_case_reader_allowed_trigger = { READER = scope:rw_case_reader }', access)

    def test_ai_uses_same_reply_and_claimant_events(self):
        text = (MOD / 'events/rw_allegation_events.txt').read_text()
        self.assertIn('ANSWER = admitted', text)
        self.assertIn('ANSWER = contested', text)
        self.assertNotIn('is_ai = no', text)
        # Includes optional claimant settlement and preparation of a shareable account.
        self.assertEqual(9, text.count('ai_chance ='))

    def test_all_display_keys_are_localized(self):
        text = (MOD / 'events/rw_allegation_events.txt').read_text() + (MOD / 'events/rw_case_events.txt').read_text()
        keys = {k for k in re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', text) if k.startswith('rw_allegations.')}
        keys.update(('rw_raise_affront_allegation_interaction', 'rw_raise_affront_allegation_interaction_desc'))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_allegations_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertEqual(keys, actual)
