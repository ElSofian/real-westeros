"""Adversarial source contracts for intentions, not a CK3 transfer simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def errors(t,e,v,i,s,tp_e,tp_v,source):
    out=[]
    ctx=block(t,'rw_ri_title_context_trigger')
    for guard in ('exists = $ACTOR$','exists = $SUBJECT$','exists = $TITLE$',
                  'is_alive = yes','is_adult = yes','is_imprisoned = no','is_landed = yes',
                  'NOT = { this = $SUBJECT$ }','liege = $ACTOR$','is_imprisoned_by = $ACTOR$',
                  'holder = $SUBJECT$','tier >= tier_county','is_noble_family_title = no','is_landless_type_title = no'):
        if guard not in ctx:out.append('invalid parties or title')
    if 'is_character_interaction_valid = { interaction = revoke_title_interaction recipient = $SUBJECT$ }' not in ctx:
        out.append('native readiness bypass')
    sel=block(t,'rw_ri_selectable_trigger')
    for guard in ('rw_ri_title_context_trigger = { ACTOR = $ACTOR$ SUBJECT = $SUBJECT$ TITLE = $TITLE$ }',
                  'NOT = {','any_owned_story','story_type = story_rw_revocation_intent','var:rw_ri_issuer = $ACTOR$',
                  'var:rw_ri_state = flag:pending','has_variable = rw_ri_window','var:rw_ri_title = $TITLE$'):
        if guard not in sel:out.append('ambiguous pending title intention')
    candidate=block(t,'rw_ri_candidate_trigger')
    for guard in ('rw_scheme_justice_own_custody_trigger = yes','exists = scope:rw_ri_title','exists = scope:rw_ri_subject',
                  'scope:rw_scheme_evidence_record.var:rw_evidence_participant = scope:rw_ri_subject',
                  'rw_ri_selectable_trigger = { ACTOR = scope:rw_scheme_observer SUBJECT = scope:rw_ri_subject TITLE = scope:rw_ri_title }'):
        if guard not in candidate:out.append('wrong affair or selection')
    basis=block(t,'rw_ri_basis_valid_trigger')
    for guard in ('exists = var:rw_ri_basis','has_variable = rw_ri_basis_serial',
                  'rw_scheme_evidence_reader_trigger = { READER = $READER$ }','var:rw_evidence_kind = flag:participant_exposed',
                  'var:rw_evidence_serial = prev.var:rw_ri_basis_serial','var:rw_evidence_participant = prev.var:rw_ri_subject'):
        if guard not in basis:out.append('basis replaced or private facts bypassed')
    create=block(e,'rw_ri_create_effect')
    for guard in ('limit = { rw_ri_candidate_trigger = yes }','story_type = story_rw_revocation_intent',
                  'story_owner = scope:rw_scheme_observer','NOT = { has_variable = rw_ri_schema }',
                  'NOT = { has_variable = rw_ri_counter }','change_variable = { name = rw_ri_counter add = 1 }'):
        if guard not in create:out.append('unsafe intention constructor')
    for field in ('schema value = 1','serial value = scope:rw_ri_serial','issuer value = scope:rw_scheme_observer',
                  'title value = scope:rw_ri_title','subject value = scope:rw_ri_subject','basis value = scope:rw_scheme_evidence_record',
                  'basis_serial value = scope:rw_scheme_evidence_serial','state value = flag:pending',
                  'issued_on value = current_date','window value = flag:yes days = 30','retained value = flag:yes years = 5'):
        if not re.search(re.escape('name = rw_ri_'+field)+r'(?!\w)',create):out.append('wrong identity or immutable clock')
    if e.count('name = rw_ri_window')!=1 or e.count('name = rw_ri_retained')!=1:out.append('intention clock renewed')
    reader=block(t,'rw_ri_reader_trigger')
    for guard in ('story_type = story_rw_revocation_intent','story_owner = $READER$','var:rw_ri_schema = 1',
                  'var:rw_ri_issuer = $READER$','has_variable = rw_ri_retained','has_variable = rw_ri_basis_serial'):
        if guard not in reader:out.append('foreign intention reader')
    view=block(t,'rw_ri_view_trigger')
    for key in ('serial','basis_serial','title','subject'):
        if f'exists = scope:rw_ri_{key}' not in view or f'var:rw_ri_{key} = scope:rw_ri_{key}' not in view:out.append('stale intention popup')
    if 'rw_ri_reader_trigger = { READER = root }' not in view:out.append('foreign intention reader')
    window=block(t,'rw_ri_pending_trigger')
    if 'rw_ri_view_trigger = yes' not in window or 'var:rw_ri_state = flag:pending has_variable = rw_ri_window' not in window:out.append('expired or terminal intent acts')
    withdraw=block(e,'rw_ri_withdraw_effect')
    if 'limit = { rw_ri_can_withdraw_trigger = yes }' not in withdraw or 'remove_variable = rw_ri_window' not in withdraw or 'value = flag:withdrawn' not in withdraw:out.append('withdrawal bypass')
    permission=block(t,'rw_ri_can_withdraw_trigger')
    if 'rw_ri_view_trigger = yes' not in permission or 'var:rw_ri_state = flag:pending' not in permission:out.append('withdrawal bypass')
    if re.search(r'\b(rw_ri_title_context_trigger|rw_ri_basis_valid_trigger|rw_ri_window)\b',permission):out.append('withdrawal trapped by current context')
    fresh=block(t,'rw_ri_receipt_linkable_trigger')
    for guard in ('is_alive = yes','is_adult = yes','exists = scope:rw_tp_record','exists = scope:rw_tp_serial','exists = scope:rw_ri_fresh_receipt',
                  'scope:rw_ri_fresh_receipt = scope:rw_tp_record','exists = scope:revoke_title_interaction',
                  'this = scope:actor','scope:recipient = scope:previous_holder','scope:landed_title = scope:title',
                  'rw_tp_reader_trigger = { READER = root }','var:rw_tp_serial = scope:rw_tp_serial','var:rw_tp_title = scope:title',
                  'var:rw_tp_former_holder = scope:previous_holder','var:rw_tp_new_holder = root',
                  'NOT = { has_variable = rw_tp_intent }','any_owned_story = { rw_ri_matches_receipt_trigger = yes }',
                  'NOT = { any_owned_story = { count > 1 rw_ri_matches_receipt_trigger = yes } }'):
        if guard not in fresh:out.append('old foreign or ambiguous receipt linked')
    match=block(t,'rw_ri_matches_receipt_trigger')
    for guard in ('rw_ri_reader_trigger = { READER = scope:rw_tp_observer }','var:rw_ri_state = flag:pending',
                  'has_variable = rw_ri_window','var:rw_ri_title = scope:title','var:rw_ri_subject = scope:previous_holder',
                  'rw_ri_basis_valid_trigger = { READER = scope:rw_tp_observer }'):
        if guard not in match:out.append('wrong expired withdrawn or stale-basis intent matched')
    link=block(e,'rw_ri_link_transfer_effect')
    if 'limit = { rw_ri_receipt_linkable_trigger = yes }' not in link or 'limit = { rw_ri_matches_receipt_trigger = yes }' not in link:out.append('direct linking bypass')
    if not (0<=link.find('remove_variable = rw_ri_window')<link.find('value = flag:observed')<link.find('name = rw_ri_receipt value = scope:rw_tp_record')<link.find('name = rw_tp_intent value = scope:rw_ri_record')):out.append('link not consumed before metadata writes')
    for field in ('rw_ri_receipt_serial value = scope:rw_tp_serial','rw_tp_intent_serial value = scope:rw_ri_serial','rw_tp_basis_serial value = scope:rw_ri_basis_serial'):
        if 'name = '+field not in link:out.append('one-sided or swapped identity link')
    if not (tp_e.find('name = rw_tp_retained')<tp_e.find('save_scope_as = rw_ri_fresh_receipt')<tp_e.find('rw_ri_link_transfer_effect = yes')<tp_e.find('clear_saved_scope = rw_ri_fresh_receipt')):out.append('fresh receipt handoff order')
    gate=block(t,'rw_ri_can_open_native_trigger')
    for guard in ('rw_ri_pending_trigger = yes','is_ai = no','rw_ri_basis_valid_trigger = { READER = root }',
                  'rw_ri_title_context_trigger = { ACTOR = root SUBJECT = scope:rw_ri_subject TITLE = scope:rw_ri_title }'):
        if guard not in gate:out.append('native window readiness bypass')
    if 'trigger = { rw_ri_can_open_native_trigger = yes }' not in v or 'limit = { rw_ri_can_open_native_trigger = yes }' not in v:out.append('stale native click')
    native=nested(v,'open_interaction_window')
    for field in ('interaction = revoke_title_interaction','actor = root','recipient = scope:rw_ri_subject'):
        if field not in native:out.append('native parties swapped')
    if re.search(r'\b(target|secondary_recipient|flag|send_option|execute_threshold)\s*=',native):out.append('native title or terms forced')
    choose=block(i,'rw_consider_title_revocation_interaction')
    for guard in ('target_type = title','target_filter = recipient_domain_titles','can_be_picked_title = { rw_ri_selectable_trigger',
                  'has_valid_target_showing_failures_only = { rw_ri_selectable_trigger','on_accept = { rw_ri_select_effect = yes }'):
        if guard not in choose:out.append('generic title picker bypass')
    selection=block(e,'rw_ri_select_effect')
    for guard in ('rw_ri_selectable_trigger = { ACTOR = scope:actor SUBJECT = scope:recipient TITLE = scope:target }',
                  'rw_scheme_evidence_reader_trigger = { READER = scope:rw_scheme_observer }','var:rw_evidence_participant = scope:rw_ri_subject',
                  'var:rw_evidence_kind = flag:participant_exposed','save_scope_value_as = { name = rw_scheme_evidence_serial value = var:rw_evidence_serial }'):
        if guard not in selection:out.append('selection chooses foreign or wrong basis')
    if 'rw_ri_create_effect' in selection or 'special_interaction' in choose:out.append('selection mistaken for consent or native engine special')
    schedule=block(e,'rw_ri_schedule_effect')
    for guard in ('rw_scheme_evidence_reader_trigger = { READER = scope:rw_scheme_observer }','var:rw_evidence_kind = flag:participant_exposed',
                  'var:rw_evidence_serial = scope:rw_scheme_evidence_serial','NOT = { has_variable = rw_ri_scheduled }'):
        if guard not in schedule:out.append('unbounded or foreign opportunity')
    if schedule.count('trigger_event =')!=2 or 'days = 2' not in schedule or 'days = 30' not in schedule or schedule.find('name = rw_ri_scheduled')>schedule.find('trigger_event'):out.append('unbounded or foreign opportunity')
    offer=block(e,'rw_ri_offer_title_effect')
    if 'clear_saved_scope = rw_ri_title' not in offer or 'random_held_title' not in offer or 'rw_ri_selectable_trigger' not in offer or 'rw_ri_open_candidate_effect = yes' not in offer:out.append('AI uses different title rules')
    if source.count('rw_ri_schedule_effect = yes')!=1:out.append('opportunity constructor not wired once')
    if 'on_owner_death = { end_story = yes }' not in s or 'NOT = { has_variable = rw_ri_retained }' not in s:out.append('personal intent inherited or never retired')
    visible=block(t,'rw_ri_tp_link_visible_trigger')
    for guard in ('rw_tp_view_trigger = yes','rw_ri_reader_trigger = { READER = root }','var:rw_ri_serial = prev.var:rw_tp_intent_serial',
                  'var:rw_ri_receipt = scope:rw_tp_record','var:rw_ri_receipt_serial = scope:rw_tp_serial','var:rw_ri_state = flag:observed'):
        if guard not in visible:out.append('link disclosed without bidirectional identity')
    if 'trigger = { rw_ri_tp_link_visible_trigger = yes }' not in tp_v:out.append('provenance link not guarded')
    # Changes here are metadata/planning only; native action still uses its own window.
    code=clean_script(t+e+v+i+s)[0]
    if re.search(r'\b(run_interaction|send_interaction|change_title_holder|create_title_and_vassal_change|resolve_title_and_vassal_change|destroy_title|revoke_title_interaction_effect|revocation_tyranny_effect|consume_revoke_title_reason|add_gold|add_prestige|add_opinion|add_trait|remove_trait|imprison|death|make_story_owner|every_living_character|any_living_character|every_house_member|scheme_owner)\s*=',code):out.append('native effect private inheritance or scan added')
    return out


class RevocationIntentTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_revocation_intent_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_revocation_intent_effects.txt').read_text()
        self.v=(MOD/'events/rw_revocation_intent_events.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_revocation_intent_interactions.txt').read_text()
        self.s=(MOD/'common/story_cycles/rw_revocation_intents.txt').read_text()
        self.tp_e=(MOD/'common/scripted_effects/rw_title_provenance_effects.txt').read_text()
        self.tp_v=(MOD/'events/rw_title_provenance_events.txt').read_text()
        self.source=(MOD/'common/scripted_effects/rw_scheme_evidence_effects.txt').read_text()

    def check(self,**kw):return errors(*(kw.get(k,getattr(self,k)) for k in ('t','e','v','i','s','tp_e','tp_v','source')))

    def test_source_contract(self):self.assertEqual([],self.check())

    def test_native_readiness_roles_and_title(self):
        for g in ('liege = $ACTOR$','is_imprisoned_by = $ACTOR$','holder = $SUBJECT$','tier >= tier_county','is_noble_family_title = no','is_landless_type_title = no'):
            self.assertIn('invalid parties or title',self.check(t=self.t.replace(g,'always = yes')))
        self.assertIn('native readiness bypass',self.check(t=self.t.replace('interaction = revoke_title_interaction','interaction = grant_titles_interaction')))

    def test_exact_candidate_affair_and_private_basis(self):
        self.assertIn('wrong affair or selection',self.check(t=self.t.replace('rw_scheme_justice_own_custody_trigger = yes','always = yes')))
        for g in ('rw_scheme_evidence_reader_trigger = { READER = $READER$ }','var:rw_evidence_serial = prev.var:rw_ri_basis_serial','var:rw_evidence_participant = prev.var:rw_ri_subject'):
            self.assertIn('basis replaced or private facts bypassed',self.check(t=self.t.replace(g,'always = yes')))

    def test_no_two_pending_causes_for_same_issuer_title(self):
        for g in ('var:rw_ri_issuer = $ACTOR$','var:rw_ri_state = flag:pending','has_variable = rw_ri_window','var:rw_ri_title = $TITLE$'):
            self.assertIn('ambiguous pending title intention',self.check(t=self.t.replace(g,'always = yes',1)))

    def test_constructor_rechecks_and_preserves_all_identity(self):
        for g in ('limit = { rw_ri_candidate_trigger = yes }','NOT = { has_variable = rw_ri_schema }','story_owner = scope:rw_scheme_observer'):
            self.assertIn('unsafe intention constructor',self.check(e=self.e.replace(g,'always = yes')))
        for g in ('basis value = scope:rw_scheme_evidence_record','title value = scope:rw_ri_title','subject value = scope:rw_ri_subject'):
            self.assertIn('wrong identity or immutable clock',self.check(e=self.e.replace(g,'broken value = 0')))

    def test_deadlines_serials_and_nonrenewal(self):
        self.assertIn('wrong identity or immutable clock',self.check(e=self.e.replace('days = 30','days = 300')))
        self.assertIn('wrong identity or immutable clock',self.check(e=self.e.replace('years = 5','years = 50')))
        self.assertIn('unsafe intention constructor',self.check(e=self.e.replace('NOT = { has_variable = rw_ri_counter }','always = yes')))
        self.assertIn('intention clock renewed',self.check(e=self.e+'\nset_variable = { name = rw_ri_window days = 30 }'))
        self.assertNotIn('remove_variable = rw_ri_counter',self.e+self.s)

    def test_private_stale_or_swapped_archives(self):
        self.assertIn('foreign intention reader',self.check(t=self.t.replace('story_owner = $READER$','always = yes')))
        for k in ('serial','basis_serial','title','subject'):
            self.assertIn('stale intention popup',self.check(t=self.t.replace(f'var:rw_ri_{k} = scope:rw_ri_{k}','always = yes')))

    def test_withdrawal_not_blocked_by_changed_eligibility(self):
        self.assertIn('withdrawal bypass',self.check(e=self.e.replace('limit = { rw_ri_can_withdraw_trigger = yes }','limit = { always = yes }')))
        self.assertIn('withdrawal trapped by current context',self.check(t=self.t.replace('rw_ri_can_withdraw_trigger = {','rw_ri_can_withdraw_trigger = { rw_ri_title_context_trigger = yes')))

    def test_fresh_receipt_identity_and_native_context_required(self):
        for g in ('is_alive = yes','is_adult = yes','scope:rw_ri_fresh_receipt = scope:rw_tp_record','exists = scope:revoke_title_interaction',
                  'var:rw_tp_serial = scope:rw_tp_serial','var:rw_tp_title = scope:title','var:rw_tp_former_holder = scope:previous_holder',
                  'NOT = { has_variable = rw_tp_intent }'):
            self.assertIn('old foreign or ambiguous receipt linked',self.check(t=self.t.replace(g,'always = yes')))

    def test_ambiguous_or_wrong_pending_match_cannot_be_associated(self):
        self.assertIn('old foreign or ambiguous receipt linked',self.check(t=self.t.replace('count > 1','count > 2')))
        for g in ('rw_ri_reader_trigger = { READER = scope:rw_tp_observer }','var:rw_ri_title = scope:title',
                  'var:rw_ri_subject = scope:previous_holder','rw_ri_basis_valid_trigger = { READER = scope:rw_tp_observer }'):
            self.assertIn('wrong expired withdrawn or stale-basis intent matched',self.check(t=self.t.replace(g,'always = yes')))

    def test_link_consumes_before_both_pointers(self):
        self.assertIn('direct linking bypass',self.check(e=self.e.replace('limit = { rw_ri_receipt_linkable_trigger = yes }','limit = { always = yes }')))
        self.assertIn('link not consumed before metadata writes',self.check(e=self.e.replace('remove_variable = rw_ri_window\n            set_variable = { name = rw_ri_state value = flag:observed }','set_variable = { name = rw_ri_state value = flag:observed }')))
        self.assertIn('one-sided or swapped identity link',self.check(e=self.e.replace('rw_tp_intent_serial value = scope:rw_ri_serial','rw_tp_intent_serial value = 0')))
        self.assertIn('fresh receipt handoff order',self.check(tp_e=self.tp_e.replace('clear_saved_scope = rw_ri_fresh_receipt','clear_saved_scope = wrong')))

    def test_native_window_does_not_send_or_choose_title(self):
        self.assertIn('stale native click',self.check(v=self.v.replace('limit = { rw_ri_can_open_native_trigger = yes }','limit = { always = yes }')))
        self.assertIn('native window readiness bypass',self.check(t=self.t.replace('rw_ri_basis_valid_trigger = { READER = root }','always = yes')))
        self.assertIn('native parties swapped',self.check(v=self.v.replace('actor = root','actor = scope:rw_ri_subject')))
        self.assertIn('native title or terms forced',self.check(v=self.v.replace('actor = root','actor = root target = scope:rw_ri_title')))

    def test_title_selection_never_records_unconfirmed_case(self):
        self.assertIn('generic title picker bypass',self.check(i=self.i.replace('target_filter = recipient_domain_titles','target_filter = actor_domain_titles')))
        self.assertIn('selection chooses foreign or wrong basis',self.check(e=self.e.replace('var:rw_evidence_participant = scope:rw_ri_subject','always = yes')))
        self.assertIn('selection mistaken for consent or native engine special',self.check(e=self.e.replace('rw_ri_select_effect = {','rw_ri_select_effect = { rw_ri_create_effect = yes')))
        self.assertNotIn('rw_ri_create_effect',block(self.i,'rw_consider_title_revocation_interaction'))

    def test_fixed_shared_ai_and_player_opportunities(self):
        self.assertIn('unbounded or foreign opportunity',self.check(e=self.e.replace('NOT = { has_variable = rw_ri_scheduled }','always = yes')))
        self.assertIn('unbounded or foreign opportunity',self.check(e=self.e.replace('id = rw_revocation_intents.0003 days = 2','id = rw_revocation_intents.0003 days = 3')))
        self.assertIn('AI uses different title rules',self.check(e=self.e.replace('clear_saved_scope = rw_ri_title','clear_saved_scope = wrong')))
        self.assertIn('opportunity constructor not wired once',self.check(source=self.source.replace('rw_ri_schedule_effect = yes','')))
        self.assertNotIn('is_ai',self.e)

    def test_link_visibility_matches_both_private_records(self):
        for g in ('rw_tp_view_trigger = yes','var:rw_ri_serial = prev.var:rw_tp_intent_serial','var:rw_ri_receipt_serial = scope:rw_tp_serial'):
            self.assertIn('link disclosed without bidirectional identity',self.check(t=self.t.replace(g,'always = yes')))
        self.assertIn('provenance link not guarded',self.check(tp_v=self.tp_v.replace('trigger = { rw_ri_tp_link_visible_trigger = yes }','trigger = { always = yes }')))

    def test_personal_not_hereditary_and_no_replayed_native_effects(self):
        self.assertIn('personal intent inherited or never retired',self.check(s=self.s.replace('on_owner_death = { end_story = yes }','on_owner_death = {}')))
        for effect in ('run_interaction','change_title_holder','revoke_title_interaction_effect','consume_revoke_title_reason','add_gold','make_story_owner','scheme_owner'):
            self.assertIn('native effect private inheritance or scan added',self.check(e=self.e+'\n'+effect+' = yes'))

    def test_localization_and_explicit_consent_wiring(self):
        keys=set(re.findall(r'(?:name|title|desc)\s*=\s*(rw_revocation_intents\.[\w.]+)',self.v+self.tp_v))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_revocation_intents_l_{lang}.yml';self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig')
            for key in keys:self.assertIn(' '+key+':0 ',text)
            for key in ('rw_ri_title','rw_ri_subject'):self.assertIn('['+key+'.',text)
            self.assertIn("SCOPE.GetValue('rw_scheme_evidence_serial')",text)
            self.assertIn("SCOPE.GetValue('rw_ri_basis_serial')",text)
        self.assertEqual(1,self.v.count('rw_ri_create_effect = yes'))
        self.assertEqual(1,self.v.count('open_interaction_window ='))
