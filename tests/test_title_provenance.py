"""Adversarial source contracts, not CK3 callback/legality simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1] / 'mod/real_westeros'


def errors(t, e, on, events, story, menu):
    out = []
    native = block(on, 'on_title_gain')
    if native.strip() != 'on_actions = { rw_on_title_revocation_context }':
        out.append('native callback replaced')
    child = block(on, 'rw_on_title_revocation_context')
    if 'trigger = { rw_tp_native_context_trigger = yes }' not in child or 'effect = { rw_tp_observe_effect = yes }' not in child:
        out.append('callback guard missing')
    context = block(t, 'rw_tp_native_context_trigger')
    for guard in ('exists = scope:title', 'exists = scope:previous_holder', 'exists = scope:actor',
                  'exists = scope:recipient', 'exists = scope:landed_title', 'exists = scope:revoke_title_interaction',
                  'this = scope:actor', 'scope:recipient = scope:previous_holder', 'scope:landed_title = scope:title',
                  'is_alive = yes', 'is_adult = yes', 'scope:title = { exists = holder holder = root tier >= tier_county }',
                  'NOT = { this = scope:previous_holder }'):
        if guard not in context:
            out.append('untyped wrong or incomplete transfer')
    known = nested(context, 'any_owned_story')
    for guard in ('rw_scheme_evidence_reader_trigger = { READER = root }',
                  'var:rw_evidence_kind = flag:participant_exposed', 'var:rw_evidence_participant = scope:previous_holder'):
        if guard not in known:
            out.append('foreign hidden or irrelevant evidence')
    repeat = context.split('# Coalesce', 1)[-1]
    for guard in ('NOT = {', 'any_owned_story = {', 'rw_tp_reader_trigger = { READER = root }',
                  'has_variable = rw_tp_repeat_window', 'var:rw_tp_title = scope:title',
                  'var:rw_tp_former_holder = scope:previous_holder', 'var:rw_tp_new_holder = root'):
        if guard not in repeat:
            out.append('repeat window conflates identity')
    create = block(e, 'rw_tp_observe_effect')
    if 'limit = { rw_tp_native_context_trigger = yes }' not in create:
        out.append('direct intake bypass')
    for guard in ('story_type = story_rw_title_provenance', 'story_owner = scope:rw_tp_observer',
                  'NOT = { has_variable = rw_tp_schema }'):
        if guard not in create:
            out.append('stale constructor scope')
    for field in ('schema value = 1', 'kind value = flag:native_revocation_context_transfer',
                  'serial value = scope:rw_tp_serial', 'title value = scope:title',
                  'former_holder value = scope:previous_holder', 'new_holder value = scope:rw_tp_observer',
                  'observed_on value = current_date', 'repeat_window value = flag:yes days = 1',
                  'retained value = flag:yes years = 5'):
        if not re.search(re.escape('name = rw_tp_' + field) + r'(?![\w])', create):
            out.append('wrong provenance or clock')
    for guard in ('NOT = { has_variable = rw_tp_serial_counter }',
                  'change_variable = { name = rw_tp_serial_counter add = 1 }'):
        if guard not in create:
            out.append('serial reused')
    reader = block(t, 'rw_tp_reader_trigger')
    for guard in ('story_type = story_rw_title_provenance', 'story_owner = $READER$', 'var:rw_tp_schema = 1',
                  'var:rw_tp_kind = flag:native_revocation_context_transfer', 'has_variable = rw_tp_retained',
                  'has_variable = rw_tp_serial', 'has_variable = rw_tp_observed_on',
                  'exists = var:rw_tp_title', 'exists = var:rw_tp_former_holder', 'exists = var:rw_tp_new_holder',
                  'var:rw_tp_new_holder = $READER$'):
        if guard not in reader:
            out.append('private typed reader bypass')
    view = block(t, 'rw_tp_view_trigger')
    for guard in ('this = scope:rw_tp_observer', 'is_alive = yes', 'exists = scope:rw_tp_record',
                  'exists = scope:rw_tp_serial', 'rw_tp_reader_trigger = { READER = root }',
                  'var:rw_tp_serial = scope:rw_tp_serial'):
        if guard not in view:
            out.append('stale popup')
    for alias in ('title', 'former_holder', 'new_holder'):
        if f'exists = scope:rw_tp_{alias}' not in view or f'var:rw_tp_{alias} = scope:rw_tp_{alias}' not in view:
            out.append('popup identity swapped')
        if f'var:rw_tp_{alias} = {{ save_scope_as = rw_tp_{alias} }}' not in e:
            out.append('missing read snapshot')
    read = block(e, 'rw_tp_read_effect')
    if 'limit = { scope:actor = { is_alive = yes } }' not in read or 'limit = { rw_tp_reader_trigger = { READER = scope:rw_tp_observer } }' not in read:
        out.append('foreign enumeration')
    if 'rw_tp_reader_trigger = { READER = scope:actor }' not in menu or 'on_accept = { rw_tp_read_effect = yes }' not in menu:
        out.append('public archive bypass')
    if 'trigger = { rw_tp_view_trigger = yes }' not in nested(events, 'right_portrait') or 'trigger = { rw_tp_view_trigger = yes }' not in events.split('right_portrait')[0]:
        out.append('stale content exposed')
    if 'rw_tp_view_trigger = yes' not in block(t, 'rw_tp_still_held_trigger') or 'exists = holder holder = root' not in block(t, 'rw_tp_still_held_trigger'):
        out.append('past receipt treated as current ownership')
    if 'on_owner_death = { end_story = yes }' not in story or 'NOT = { has_variable = rw_tp_retained }' not in story:
        out.append('private record inherited or never retired')
    # Read paths contain no persistent mutation or follow-up scheduler.
    read_code = clean_script(read + events + menu + block(t, 'rw_tp_reader_trigger') + view)[0]
    if re.search(r'\b(set_variable|change_variable|remove_variable|days|years|send_interface_message)\s*=', read_code):
        out.append('reading mutates or renews record')
    code = clean_script(t+e+on+events+story+menu)[0]
    if re.search(r'\b(run_interaction|send_interaction|open_interaction_window|change_title_holder|change_title_holder_include_vassals|resolve_title_and_vassal_change|create_title_and_vassal_change|destroy_title|add_pressed_claim|revoke_title_interaction_effect|revocation_tyranny_effect|title_revocation_stress_effect|consume_revoke_title_reason|add_trait|remove_trait|add_gold|add_opinion|add_prestige|imprison|death|set_house|make_story_owner|add_to_global_variable_list)\s*=', code):
        out.append('native consequence replayed or private history transferred')
    if re.search(r'\b(scheme_owner|every_living_character|any_living_character|every_house_member|is_ai|rw_evidence_scheme)\b', code):
        out.append('hidden source world scan or AI exception')
    return out


class TitleProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_title_provenance_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_title_provenance_effects.txt').read_text()
        self.on = (MOD/'common/on_action/rw_title_provenance_on_actions.txt').read_text()
        self.v = (MOD/'events/rw_title_provenance_events.txt').read_text()
        self.s = (MOD/'common/story_cycles/rw_title_provenance.txt').read_text()
        self.i = (MOD/'common/character_interactions/rw_title_provenance_interactions.txt').read_text()

    def check(self, **kw):
        return errors(*(kw.get(k, getattr(self,k)) for k in ('t','e','on','v','s','i')))

    def test_source_contract(self):
        self.assertEqual([], self.check())

    def test_native_wrapper_and_child_cannot_override_or_bypass(self):
        for field in ('effect','trigger','events','random_events'):
            self.assertIn('native callback replaced', self.check(on=self.on.replace('on_title_gain = {', 'on_title_gain = { '+field+' = {}')))
        self.assertIn('callback guard missing', self.check(on=self.on.replace('trigger = { rw_tp_native_context_trigger = yes }','trigger = { always = yes }')))

    def test_missing_context_never_becomes_revocation(self):
        for guard in ('exists = scope:title','exists = scope:previous_holder','exists = scope:actor',
                      'exists = scope:recipient','exists = scope:landed_title','exists = scope:revoke_title_interaction'):
            self.assertIn('untyped wrong or incomplete transfer', self.check(t=self.t.replace(guard,'always = yes')))

    def test_actor_recipient_selected_title_and_holder_must_match(self):
        for guard in ('this = scope:actor', 'scope:recipient = scope:previous_holder',
                      'scope:landed_title = scope:title', 'holder = root', 'tier >= tier_county',
                      'NOT = { this = scope:previous_holder }'):
            self.assertIn('untyped wrong or incomplete transfer', self.check(t=self.t.replace(guard,'always = yes')))

    def test_existing_private_exposure_required(self):
        for guard in ('rw_scheme_evidence_reader_trigger = { READER = root }',
                      'var:rw_evidence_kind = flag:participant_exposed', 'var:rw_evidence_participant = scope:previous_holder'):
            self.assertIn('foreign hidden or irrelevant evidence',self.check(t=self.t.replace(guard,'always = yes')))

    def test_repeat_coalescing_is_exact_and_does_not_renew(self):
        for guard in ('has_variable = rw_tp_repeat_window','var:rw_tp_title = scope:title','var:rw_tp_former_holder = scope:previous_holder','var:rw_tp_new_holder = root'):
            self.assertIn('repeat window conflates identity',self.check(t=self.t.replace(guard,'always = yes')))
        self.assertEqual(1,self.e.count('name = rw_tp_repeat_window'))
        self.assertIn('wrong provenance or clock',self.check(e=self.e.replace('days = 1','days = 30')))
        self.assertIn('wrong provenance or clock',self.check(e=self.e.replace('years = 5','years = 50')))

    def test_effect_and_fresh_constructor_guards(self):
        self.assertIn('direct intake bypass',self.check(e=self.e.replace('limit = { rw_tp_native_context_trigger = yes }','limit = { always = yes }')))
        for guard in ('story_type = story_rw_title_provenance','story_owner = scope:rw_tp_observer','NOT = { has_variable = rw_tp_schema }'):
            self.assertIn('stale constructor scope',self.check(e=self.e.replace(guard,'always = yes')))

    def test_receipt_fields_and_serial_are_not_reused(self):
        for old,new in (('title value = scope:title','title value = scope:landed_title'),
                        ('former_holder value = scope:previous_holder','former_holder value = scope:actor'),
                        ('observed_on value = current_date','observed_on value = 0')):
            self.assertIn('wrong provenance or clock',self.check(e=self.e.replace(old,new)))
        self.assertIn('serial reused',self.check(e=self.e.replace('NOT = { has_variable = rw_tp_serial_counter }','always = yes')))
        self.assertNotIn('remove_variable = rw_tp_serial_counter',self.e+self.s)

    def test_private_reader_not_inherited_guilt(self):
        for guard in ('story_owner = $READER$','var:rw_tp_schema = 1','has_variable = rw_tp_retained','var:rw_tp_new_holder = $READER$'):
            self.assertIn('private typed reader bypass',self.check(t=self.t.replace(guard,'always = yes')))
        self.assertIn('private record inherited or never retired',self.check(s=self.s.replace('on_owner_death = { end_story = yes }','on_owner_death = {}')))

    def test_stale_and_swapped_popup_identity(self):
        self.assertIn('stale popup',self.check(t=self.t.replace('var:rw_tp_serial = scope:rw_tp_serial','always = yes')))
        for key in ('title','former_holder','new_holder'):
            self.assertIn('popup identity swapped',self.check(t=self.t.replace(f'var:rw_tp_{key} = scope:rw_tp_{key}','always = yes')))
            self.assertIn('missing read snapshot',self.check(e=self.e.replace(f'save_scope_as = rw_tp_{key}','save_scope_as = wrong')))
        self.assertIn('stale content exposed',self.check(v=self.v.replace('trigger = { rw_tp_view_trigger = yes }','trigger = { always = yes }')))

    def test_archiving_and_current_ownership_do_not_infer_entitlement(self):
        self.assertIn('foreign enumeration',self.check(e=self.e.replace('limit = { rw_tp_reader_trigger = { READER = scope:rw_tp_observer } }','limit = { always = yes }')))
        self.assertIn('public archive bypass',self.check(i=self.i.replace('on_accept = { rw_tp_read_effect = yes }','on_accept = {}')))
        self.assertIn('past receipt treated as current ownership',self.check(t=self.t.replace('exists = holder holder = root','always = yes')))
        self.assertIn('reading mutates or renews record',self.check(v=self.v+'\nset_variable = yes'))

    def test_no_forced_title_penalty_or_reconstruction(self):
        for effect in ('run_interaction','change_title_holder','revoke_title_interaction_effect','revocation_tyranny_effect','title_revocation_stress_effect','consume_revoke_title_reason','add_gold','make_story_owner'):
            self.assertIn('native consequence replayed or private history transferred',self.check(e=self.e+'\n'+effect+' = yes'))
        for token in ('is_ai','scheme_owner','every_living_character'):
            self.assertIn('hidden source world scan or AI exception',self.check(t=self.t+'\n'+token+' = yes'))

    def test_localization_and_callback_kind_remain_precise(self):
        keys=set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_title_provenance\.[\w.]+)',self.v))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_title_provenance_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig')
            for key in keys:self.assertIn(' '+key+':0 ',text)
            for key in ('rw_tp_title','rw_tp_former_holder','rw_tp_new_holder'):self.assertIn('['+key+'.',text)
        self.assertNotIn('rw_evidence_scheme',self.e)
        self.assertNotIn('rw_house_',self.e)
        self.assertEqual(1,self.on.count('on_actions ='))
