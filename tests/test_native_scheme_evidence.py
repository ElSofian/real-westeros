"""Adversarial source checks only: no simulation of CK3 discovery or secrecy."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block as any_block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def block(text, name):
    # Parameterized invocations may precede a definition; inspect definitions only.
    match = re.search(r'(?m)^' + re.escape(name) + r'\s*=\s*\{', text)
    return any_block(text[match.start():], name) if match else ''


def intake_errors(t, e, on):
    errors = []
    for key, child in (('on_scheme_discovered', 'rw_on_murder_scheme_discovered'),
                       ('on_scheme_agent_discovered', 'rw_on_murder_participant_exposed')):
        wrapper = block(on, key)
        suffix = 'discovery' if key == 'on_scheme_discovered' else 'participant'
        dispatch = block(on, child)
        if f'trigger = {{ rw_scheme_{suffix}_intake_trigger = yes }}' not in dispatch or f'effect = {{ rw_scheme_{suffix}_intake_effect = yes }}' not in dispatch:
            errors.append('custom dispatch uses wrong intake')
        if f'on_actions = {{ {child} }}' not in wrapper:
            errors.append('native dispatch missing')
        if re.search(r'\b(effect|trigger|events|random_events)\s*=', wrapper):
            errors.append('native action behavior overwritten')
    target = block(t, 'rw_scheme_target_observer_trigger')
    for guard in ('scheme_type = murder', 'exists = scheme_target_character',
                  'is_alive = yes', 'is_adult = yes', 'is_landed = yes', 'is_ruler = yes', 'host = this'):
        if guard not in target:
            errors.append('wrong scheme or observer admitted')
    discovery = block(t, 'rw_scheme_discovery_intake_trigger')
    if 'is_scheme_exposed = yes' not in discovery or 'rw_scheme_target_observer_trigger = yes' not in discovery:
        errors.append('undiscovered scheme recorded')
    participant = block(t, 'rw_scheme_participant_intake_trigger')
    for guard in ('rw_scheme_target_observer_trigger = yes', 'exists = scope:agent',
                  'is_agent_exposed_in_scheme = root', 'NOT = { this = root.scheme_target_character }'):
        if guard not in participant:
            errors.append('hidden or wrong participant recorded')
    for name, gate, kind in (('discovery', 'discovery', 'scheme_discovered'),
                             ('participant', 'participant', 'participant_exposed')):
        effect = block(e, f'rw_scheme_{name}_intake_effect')
        if f'limit = {{ rw_scheme_{gate}_intake_trigger = yes }}' not in effect:
            errors.append('effect bypasses native intake guard')
        for guard in ('any_owned_story', 'story_type = story_rw_scheme_evidence',
                      'var:rw_evidence_schema = 1', f'var:rw_evidence_kind = flag:{kind}',
                      'var:rw_evidence_scheme = scope:rw_observed_scheme'):
            if guard not in effect:
                errors.append('repeated or different scheme observation conflated')
        if name == 'participant' and 'var:rw_evidence_participant = scope:rw_scheme_participant' not in effect:
            errors.append('participant identity not deduplicated')
    if re.search(r'\bscheme_owner\b', clean_script(t + e + on)[0]):
        errors.append('hidden organiser read')
    return errors


class NativeSchemeEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_scheme_evidence_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_scheme_evidence_effects.txt').read_text()
        self.on = (MOD / 'common/on_action/rw_scheme_on_actions.txt').read_text()
        self.v = (MOD / 'events/rw_scheme_evidence_events.txt').read_text()
        self.s = (MOD / 'common/story_cycles/rw_scheme_evidence.txt').read_text()

    def errors(self, t=None, e=None, on=None):
        return intake_errors(self.t if t is None else t, self.e if e is None else e,
                             self.on if on is None else on)

    def test_intake_contract(self):
        self.assertEqual([], self.errors())

    def test_native_behavior_replacement_mutations(self):
        for key in ('effect', 'trigger', 'events', 'random_events'):
            with self.subTest(key=key):
                on = self.on.replace('on_scheme_discovered = {', f'on_scheme_discovered = {{ {key} = {{ }}')
                self.assertIn('native action behavior overwritten', self.errors(on=on))

    def test_dispatch_cannot_substitute_another_intake(self):
        on = self.on.replace('effect = { rw_scheme_participant_intake_effect = yes }',
                             'effect = { rw_scheme_discovery_intake_effect = yes }')
        self.assertIn('custom dispatch uses wrong intake', self.errors(on=on))

    def test_wrong_scheme_target_and_host_mutations(self):
        for guard in ('scheme_type = murder', 'exists = scheme_target_character',
                      'is_alive = yes', 'is_adult = yes', 'is_landed = yes', 'is_ruler = yes', 'host = this'):
            with self.subTest(guard=guard):
                self.assertIn('wrong scheme or observer admitted', self.errors(t=self.t.replace(guard, 'always = yes', 1)))

    def test_hidden_plot_mutation(self):
        self.assertIn('undiscovered scheme recorded', self.errors(t=self.t.replace('is_scheme_exposed = yes', 'always = yes')))

    def test_hidden_or_wrong_agent_mutations(self):
        for guard in ('exists = scope:agent', 'is_agent_exposed_in_scheme = root', 'NOT = { this = root.scheme_target_character }'):
            with self.subTest(guard=guard):
                self.assertIn('hidden or wrong participant recorded', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_effect_revalidation_mutations(self):
        for kind in ('discovery', 'participant'):
            e = self.e.replace(f'limit = {{ rw_scheme_{kind}_intake_trigger = yes }}', 'limit = { always = yes }')
            self.assertIn('effect bypasses native intake guard', self.errors(e=e))

    def test_duplicate_and_cross_scheme_mutations(self):
        e = self.e.replace('var:rw_evidence_scheme = scope:rw_observed_scheme', 'always = yes')
        self.assertIn('repeated or different scheme observation conflated', self.errors(e=e))
        e = self.e.replace('var:rw_evidence_participant = scope:rw_scheme_participant', 'always = yes')
        self.assertIn('participant identity not deduplicated', self.errors(e=e))
        self.assertIn('NOT = {', block(self.e, 'rw_scheme_discovery_intake_effect'))
        self.assertIn('NOT = {', block(self.e, 'rw_scheme_participant_intake_effect'))

    def test_hidden_organiser_substitution_mutation(self):
        self.assertIn('hidden organiser read', self.errors(e=self.e.replace('scope:agent = { save_scope_as', 'scheme_owner = { save_scope_as')))

    def test_no_native_or_service_side_effects_and_no_scan(self):
        scripts = clean_script(self.t + self.e + self.on + self.s + self.v)[0]
        self.assertNotRegex(scripts, r'\b(add_gold|add_prestige|add_opinion|death|imprison|revoke_title|add_secret|expose_secret|expose_scheme|expose_scheme_agent|end_scheme|forbid_from_scheme|make_story_owner)\s*=')
        self.assertNotRegex(scripts, r'\b(any_living_character|every_living_character|any_scheme|every_scheme)\s*=')
        self.assertNotIn('rw_service_last_', scripts)
        self.assertNotIn('rw_case_evidence', scripts)
        self.assertNotIn('is_ai', scripts)

    def test_actor_only_archive_and_no_native_pointer_dereference(self):
        reader = block(self.t, 'rw_scheme_evidence_reader_trigger')
        self.assertIn('story_type = story_rw_scheme_evidence', reader)
        self.assertIn('story_owner = $READER$', reader)
        self.assertIn('var:rw_evidence_schema = 1', reader)
        self.assertIn('has_variable = rw_evidence_retained', reader)
        archive = block(self.e, 'rw_scheme_read_evidence_effect')
        self.assertIn('scope:actor = {', archive)
        self.assertIn('rw_scheme_evidence_reader_trigger = { READER = scope:rw_scheme_observer }', archive)
        self.assertNotIn('scope:recipient', archive)
        self.assertNotIn('rw_evidence_scheme', archive + self.v)
        self.assertNotRegex(archive + self.v, r'\b(set_variable|change_variable|add_opinion|end_story)\s*=')
        access = block(self.t, 'rw_scheme_evidence_view_trigger')
        self.assertIn('this = scope:rw_scheme_observer', access)
        self.assertIn('var:rw_evidence_serial = scope:rw_scheme_evidence_serial', access)
        # Rendering resolves only the specific, recorded exposed participant.
        self.assertIn('var:rw_evidence_participant = scope:rw_evidence_visible_participant', self.v)

    def test_notify_after_record_without_new_modal_or_inferred_organiser(self):
        create = block(self.e, 'rw_scheme_create_evidence_effect')
        self.assertLess(create.index('name = rw_evidence_schema'), create.index('send_interface_message'))
        self.assertNotIn('trigger_event', create)
        self.assertIn('exists = scope:rw_scheme_evidence_record', create)
        self.assertIn('limit = { var:rw_evidence_kind = flag:participant_exposed }', create)
        self.assertEqual(1, create.count('name = rw_evidence_participant'))

    def test_constructor_requires_fresh_owned_story(self):
        create = block(self.e, 'rw_scheme_create_evidence_effect')
        guard = create[:create.index('scope:rw_scheme_observer = {\n            if')]
        self.assertIn('story_type = story_rw_scheme_evidence', guard)
        self.assertIn('story_owner = scope:rw_scheme_observer', guard)
        self.assertIn('NOT = { has_variable = rw_evidence_schema }', guard)

    def test_personal_retention_and_no_inherited_guilt(self):
        self.assertIn('days = 1825', self.e)
        self.assertIn('on_owner_death = { end_story = yes }', self.s)
        self.assertIn('days = 60', self.s)
        self.assertIn('NOT = { has_variable = rw_evidence_retained }', self.s)
        self.assertNotIn('make_story_owner', clean_script(self.s)[0])

    def test_localization_and_no_hidden_identity_rendering(self):
        interaction = (MOD / 'common/character_interactions/rw_scheme_evidence_interactions.txt').read_text()
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_[\w.]+)', self.v + interaction))
        keys = {key for key in keys if not key.startswith(('rw_scheme_response.', 'rw_scheme_justice.'))}
        keys.update(('rw_review_my_scheme_evidence_interaction', 'rw_scheme_evidence.notice_title', 'rw_scheme_evidence.notice_desc'))
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_scheme_evidence_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text = p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys, set(re.findall(r'^\s+([\w.]+):0', text, re.M)))
            self.assertNotIn('scheme_owner', text)
            self.assertNotIn('scope:agent', text)
            self.assertIn('[rw_evidence_visible_participant.GetTitledFirstName]', text)
