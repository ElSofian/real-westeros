"""Native UI handoff contracts, not execution, sentencing or CK3 runtime simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'
PARTICIPANT = 'scope:rw_scheme_evidence_record.var:rw_evidence_participant'


def sentencing_errors(t, v, journal):
    errors = []
    current = block(t, 'rw_sentencing_current_prisoner_trigger')
    for guard in ('rw_scheme_justice_own_custody_trigger = yes', 'is_imprisoned = no'):
        if guard not in current:
            errors.append('wrong keeper or stale custody')
    for action, interaction in (('execution', 'execute_prisoner_interaction'),
                                ('release', 'release_from_prison_interaction')):
        gate = block(t, f'rw_sentencing_can_open_{action}_trigger')
        for guard in ('rw_sentencing_current_prisoner_trigger = yes', 'is_ai = no'):
            if guard not in gate:
                errors.append('window bypasses current prisoner or human UI')
        native = nested_block(gate, 'is_character_interaction_valid')
        if f'interaction = {interaction}' not in native or f'recipient = {PARTICIPANT}' not in native:
            errors.append('wrong native validity query')
        if v.count(f'trigger = {{ rw_sentencing_can_open_{action}_trigger = yes }}') != 1 or v.count(f'limit = {{ rw_sentencing_can_open_{action}_trigger = yes }}') != 1:
            errors.append('window execution not revalidated')
        # Find the precise option, not an unrelated matching window elsewhere.
        option = v.split(f'name = rw_sentencing.review_{action}', 1)[-1].split('ai_chance', 1)[0]
        window = nested_block(option, 'open_interaction_window')
        for field in (f'interaction = {interaction}', 'actor = root', f'recipient = {PARTICIPANT}'):
            if field not in window:
                errors.append('wrong sentencing window target or action')
    reason = block(t, 'rw_sentencing_execution_reason_trigger')
    no_reason = block(t, 'rw_sentencing_no_execution_reason_trigger')
    if f'has_execute_reason = {PARTICIPANT}' not in reason or 'rw_sentencing_current_prisoner_trigger = yes' not in reason:
        errors.append('execution reason confused with arrest or wrong character')
    if f'NOT = {{ has_execute_reason = {PARTICIPANT} }}' not in no_reason or 'rw_sentencing_current_prisoner_trigger = yes' not in no_reason:
        errors.append('absence of execution reason invented')
    if journal.count('limit = { rw_sentencing_current_prisoner_trigger = yes }') != 1:
        errors.append('journal navigation bypass')
    code = clean_script(t + v)[0].replace('trigger_event = { id = rw_title_status.0001 }', '')
    if re.search(r'\b(death|execute_prisoner_effect|release_from_prison|imprison|send_interaction|consume_imprisonment_reasons|consume_execute_reasons|add_opinion|add_gold|set_variable|remove_variable|add_character_flag|trigger_event)\s*=', code):
        errors.append('sentence or cached result applied by navigation')
    return errors


class PrisonerSentencingTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_sentencing_triggers.txt').read_text()
        self.v = (MOD / 'events/rw_sentencing_events.txt').read_text()
        self.j = (MOD / 'events/rw_scheme_evidence_events.txt').read_text()

    def errors(self, t=None, v=None, j=None):
        return sentencing_errors(self.t if t is None else t, self.v if v is None else v, self.j if j is None else j)

    def test_native_handoff_contract(self):
        self.assertEqual([], self.errors())

    def test_foreign_prisoner_and_captive_observer_mutations(self):
        for guard in ('rw_scheme_justice_own_custody_trigger = yes', 'is_imprisoned = no'):
            with self.subTest(guard=guard):
                self.assertIn('wrong keeper or stale custody', self.errors(t=self.t.replace(guard, 'always = yes', 1)))

    def test_each_window_requires_current_prisoner_and_human_ui(self):
        for guard in ('rw_sentencing_current_prisoner_trigger = yes', 'is_ai = no'):
            with self.subTest(guard=guard):
                self.assertIn('window bypasses current prisoner or human UI', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_native_action_and_recipient_mutations(self):
        for action in ('execute_prisoner_interaction', 'release_from_prison_interaction'):
            self.assertIn('wrong native validity query', self.errors(t=self.t.replace(action, 'imprison_interaction')))
        self.assertIn('wrong native validity query', self.errors(t=self.t.replace(f'recipient = {PARTICIPANT}', 'recipient = root')))

    def test_click_revalidates_each_native_interaction(self):
        for action in ('execution', 'release'):
            with self.subTest(action=action):
                v = self.v.replace(f'limit = {{ rw_sentencing_can_open_{action}_trigger = yes }}', 'limit = { always = yes }')
                self.assertIn('window execution not revalidated', self.errors(v=v))

    def test_arrest_is_not_execution_reason_and_direction_is_preserved(self):
        self.assertIn('execution reason confused with arrest or wrong character', self.errors(t=self.t.replace('has_execute_reason', 'has_imprisonment_reason')))
        self.assertIn('execution reason confused with arrest or wrong character', self.errors(t=self.t.replace(f'has_execute_reason = {PARTICIPANT}', 'has_execute_reason = scope:rw_scheme_observer')))
        for action in ('execution', 'release'):
            gate = block(self.t, f'rw_sentencing_can_open_{action}_trigger')
            self.assertNotIn('has_execute_reason', gate)
            self.assertNotIn('has_imprisonment_reason', gate)

    def test_exact_native_window_and_actor_mutations(self):
        for old, new in (('actor = root', 'actor = scope:rw_scheme_participant'),
                         (f'recipient = {PARTICIPANT}', 'recipient = root'),
                         ('interaction = execute_prisoner_interaction', 'interaction = release_from_prison_interaction')):
            self.assertIn('wrong sentencing window target or action', self.errors(v=self.v.replace(old, new)))

    def test_no_force_send_release_death_or_completed_sentence_mutations(self):
        for effect in ('death', 'execute_prisoner_effect', 'release_from_prison', 'send_interaction', 'set_variable', 'add_character_flag'):
            with self.subTest(effect=effect):
                self.assertIn('sentence or cached result applied by navigation', self.errors(v=self.v + f'\n{effect} = yes'))

    def test_journal_navigation_is_guarded(self):
        self.assertIn('journal navigation bypass', self.errors(j=self.j.replace('limit = { rw_sentencing_current_prisoner_trigger = yes }', 'limit = { always = yes }')))
        self.assertIn('trigger_event = { id = rw_sentencing.0001 }', self.j)

    def test_no_family_target_or_scheduler_or_implicit_payment(self):
        code = clean_script(self.t + self.v)[0]
        self.assertNotRegex(code, r'\b(scheme_owner|every_living_character|every_owned_story|every_close_family_member|every_dynasty_member|every_house_member|days|months|years|after|immediate)\b')
        self.assertNotIn('rw_scheme_response_state', code)
        self.assertNotIn('rw_service_', code)
        self.assertEqual(2, self.v.count('open_interaction_window = {'))
        self.assertEqual(1, self.v.count('trigger_event = { id = rw_title_status.0001 }'))
        self.assertIn('limit = { rw_title_status_view_trigger = yes }', self.v)
        portrait = nested_block(self.v, 'right_portrait')
        self.assertIn('trigger = { rw_sentencing_current_prisoner_trigger = yes }', portrait)
        self.assertIn(f'character = {PARTICIPANT}', portrait)
        unchanged = self.v.split('name = rw_sentencing.leave_unchanged', 1)[1].split('option = {', 1)[0]
        self.assertNotIn('open_interaction_window', unchanged)
        self.assertNotIn('trigger_event', unchanged)

    def test_existing_private_reader_and_custody_chain_is_used(self):
        justice = (MOD / 'common/scripted_triggers/rw_scheme_justice_triggers.txt').read_text()
        own = block(justice, 'rw_scheme_justice_own_custody_trigger')
        self.assertIn('rw_scheme_justice_living_trigger = yes', own)
        self.assertIn('is_imprisoned_by = scope:rw_scheme_observer', own)
        self.assertIn('rw_scheme_justice_view_trigger = yes', block(justice, 'rw_scheme_justice_living_trigger'))
        self.assertIn('rw_scheme_evidence_view_trigger = yes', block(justice, 'rw_scheme_justice_view_trigger'))
        evidence = (MOD / 'common/scripted_triggers/rw_scheme_evidence_triggers.txt').read_text()
        self.assertIn('var:rw_evidence_serial = scope:rw_scheme_evidence_serial', block(evidence, 'rw_scheme_evidence_view_trigger'))
        reader = block(evidence, 'rw_scheme_evidence_reader_trigger')
        for guard in ('story_type = story_rw_scheme_evidence', 'story_owner = $READER$', 'var:rw_evidence_schema = 1', 'has_variable = rw_evidence_retained'):
            self.assertIn(guard, reader)

    def test_localization_and_private_identity(self):
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_sentencing\.[\w.]+)', self.v + self.j))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_sentencing_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', text, re.M)))
            self.assertNotIn('[', text)
