"""Opt-in diagnostic source contracts; no house ban or title-transfer simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'
CALLBACKS = {'on_title_gain': 'gain', 'on_title_gain_inheritance': 'inheritance',
             'on_title_gain_usurpation': 'usurpation', 'on_title_lost': 'loss'}


def trace_errors(t, e, on, interactions):
    errors = []
    select = block(t, 'rw_g3_trace_can_select_house_trigger')
    for guard in ('debug_only = yes', 'exists = scope:actor', 'exists = scope:recipient',
                  'scope:actor = { is_alive = yes is_ai = no }', 'scope:recipient = { is_alive = yes exists = house }'):
        if guard not in select:
            errors.append('ordinary gameplay or invalid house can enable diagnostic')
    for state, condition in (('start', 'NOT = { has_variable = rw_g3_trace_active }'),
                             ('stop', 'has_variable = rw_g3_trace_active')):
        trigger = block(t, f'rw_g3_trace_can_{state}_trigger')
        if 'rw_g3_trace_can_select_house_trigger = yes' not in trigger or condition not in trigger:
            errors.append('diagnostic marker lifecycle bypass')
        effect = block(e, f'rw_g3_trace_{state}_effect')
        if f'limit = {{ rw_g3_trace_can_{state}_trigger = yes }}' not in effect:
            errors.append('debug execution bypass')
        interaction = block(interactions, f'rw_g3_trace_{state}_interaction')
        for guard in ('category = interaction_debug_main', f'is_shown = {{ rw_g3_trace_can_{state}_trigger = yes }}',
                      f'on_accept = {{ rw_g3_trace_{state}_effect = yes }}', 'ai_will_do = { base = 0 }'):
            if guard not in interaction:
                errors.append('diagnostic interaction unguarded')
    start = block(e, 'rw_g3_trace_start_effect')
    if start.count('set_variable = { name = rw_g3_trace_active value = flag:enabled days = 7 }') != 1 or 'scope:recipient.house = {' not in start:
        errors.append('trace expires incorrectly or marks wrong scope')
    if 'scope:recipient.house = { remove_variable = rw_g3_trace_active }' not in block(e, 'rw_g3_trace_stop_effect'):
        errors.append('stop cannot clear exact house marker')
    gate = block(t, 'rw_g3_trace_title_callback_trigger')
    for guard in ('debug_only = yes', 'exists = scope:title', 'exists = house', 'house = { var:rw_g3_trace_active = flag:enabled }'):
        if guard not in gate:
            errors.append('unmarked or nondebug transfer logged')
    for native, kind in CALLBACKS.items():
        wrapper = block(on, native)
        if f'on_actions = {{ rw_g3_trace_{kind} }}' not in wrapper:
            errors.append('native callback lost')
        if re.search(r'\b(effect|trigger|events|random_events)\s*=', wrapper):
            errors.append('native behavior overwritten')
        child = block(on, f'rw_g3_trace_{kind}')
        for guard in ('trigger = { rw_g3_trace_title_callback_trigger = yes }',
                      'limit = { rw_g3_trace_title_callback_trigger = yes }',
                      'scope:title = {'):
            if guard not in child:
                errors.append('wrong diagnostic dispatch or scope')
        if on.count(f'RW_G3 callback={kind} holder=[ROOT.Char.GetID] title=[THIS.Title.GetNameNoTooltip]') != 1:
            errors.append('wrong diagnostic dispatch or scope')
    code = clean_script(t + e + on + interactions)[0]
    if re.search(r'\b(debug_log_scopes|death|imprison|run_interaction|trigger_event|change_title_holder|change_liege|set_house|set_dynasty|make_story_owner|destroy_title|add_trait|remove_trait|add_gold|add_opinion|consume_revoke_title_reason)\s*=', code):
        errors.append('trace leaks scopes or mutates gameplay')
    return errors


class G3HouseTraceTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD / 'common/scripted_triggers/rw_g3_trace_triggers.txt').read_text()
        self.e = (MOD / 'common/scripted_effects/rw_g3_trace_effects.txt').read_text()
        self.on = (MOD / 'common/on_action/rw_g3_trace_on_actions.txt').read_text()
        self.i = (MOD / 'common/character_interactions/rw_g3_trace_interactions.txt').read_text()

    def errors(self, t=None, e=None, on=None, interactions=None):
        return trace_errors(self.t if t is None else t, self.e if e is None else e,
                            self.on if on is None else on, self.i if interactions is None else interactions)

    def test_original_diagnostic_contract(self):
        self.assertEqual([], self.errors())

    def test_ordinary_game_invalid_actor_or_no_house_mutations(self):
        for guard in ('debug_only = yes', 'exists = scope:actor', 'exists = scope:recipient',
                      'scope:actor = { is_alive = yes is_ai = no }', 'scope:recipient = { is_alive = yes exists = house }'):
            self.assertIn('ordinary gameplay or invalid house can enable diagnostic', self.errors(t=self.t.replace(guard, 'always = yes', 1)))

    def test_only_debug_marked_house_logs_mutations(self):
        for guard in ('debug_only = yes', 'exists = scope:title', 'exists = house', 'house = { var:rw_g3_trace_active = flag:enabled }'):
            t = self.t.replace(guard, 'always = yes')
            self.assertIn('unmarked or nondebug transfer logged', self.errors(t=t))
        gate = block(self.t, 'rw_g3_trace_title_callback_trigger')
        self.assertNotIn('is_ai', gate)  # A marked AI holder is traced too.
        self.assertNotIn('is_alive', gate)  # Native loss may have a deceased root.

    def test_no_marker_refresh_and_exact_expiry(self):
        self.assertIn('diagnostic marker lifecycle bypass', self.errors(t=self.t.replace('NOT = { has_variable = rw_g3_trace_active }', 'always = yes')))
        self.assertIn('trace expires incorrectly or marks wrong scope', self.errors(e=self.e.replace('days = 7', 'years = 50')))
        self.assertEqual(1, self.e.count('set_variable ='))
        self.assertIn('stop cannot clear exact house marker', self.errors(e=self.e.replace('remove_variable = rw_g3_trace_active', 'remove_variable = rw_wrong_marker')))

    def test_direct_effect_and_interaction_revalidation(self):
        for state in ('start', 'stop'):
            self.assertIn('debug execution bypass', self.errors(e=self.e.replace(f'limit = {{ rw_g3_trace_can_{state}_trigger = yes }}', 'limit = { always = yes }')))
            self.assertIn('diagnostic interaction unguarded', self.errors(interactions=self.i.replace(f'is_shown = {{ rw_g3_trace_can_{state}_trigger = yes }}', 'is_shown = { always = yes }')))

    def test_native_callback_replacement_mutations(self):
        for native in CALLBACKS:
            self.assertIn('native behavior overwritten', self.errors(on=self.on.replace(f'{native} = {{', f'{native} = {{ effect = {{ }}', 1)))
        self.assertEqual(4, self.on.count('on_actions ='))

    def test_each_callback_gate_scope_and_kind_mutations(self):
        for kind in CALLBACKS.values():
            on = self.on.replace(f'RW_G3 callback={kind}', 'RW_G3 callback=conquest')
            self.assertIn('wrong diagnostic dispatch or scope', self.errors(on=on))
        self.assertIn('wrong diagnostic dispatch or scope', self.errors(on=self.on.replace('limit = { rw_g3_trace_title_callback_trigger = yes }', 'limit = { always = yes }')))
        self.assertNotIn('callback=conquest', self.on)
        self.assertNotIn('callback=election', self.on)

    def test_no_title_reversion_family_mutation_or_scope_dump(self):
        for effect in ('debug_log_scopes', 'change_title_holder', 'destroy_title', 'set_house', 'add_trait', 'run_interaction', 'trigger_event'):
            self.assertIn('trace leaks scopes or mutates gameplay', self.errors(on=self.on + f'\n{effect} = yes'))
        code = clean_script(self.t + self.e + self.on + self.i)[0]
        self.assertNotRegex(code, r'\b(every_house_member|every_dynasty_member|every_held_title|every_living_character|any_living_character|create_story)\s*=')

    def test_trace_marker_is_not_a_sanction_or_native_eligibility_input(self):
        allowed = {'rw_g3_trace_triggers.txt', 'rw_g3_trace_effects.txt'}
        for path in MOD.rglob('*.txt'):
            if 'rw_g3_trace_active' in clean_script(path.read_text(encoding='utf-8-sig'))[0]:
                self.assertIn(path.name, allowed)
        self.assertNotRegex(self.t + self.e + self.on, r'has_trait\s*=\s*disinherited|can_be_granted_titles_by\s*=')

    def test_debug_localization_and_restrained_log_fields(self):
        for lang in ('english', 'french'):
            p = MOD / f'localization/{lang}/rw_g3_trace_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            keys = set(re.findall(r'^\s+(\w+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertEqual({'rw_g3_trace_start_interaction', 'rw_g3_trace_stop_interaction'}, keys)
        self.assertNotRegex(self.on, r'scope:(?:agent|scheme|previous_holder|new_holder)|\.GetSecrets')
        self.assertEqual(4, self.on.count('debug_log ='))
