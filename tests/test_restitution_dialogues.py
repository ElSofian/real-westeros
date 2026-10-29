"""Adversarial source contracts; no CK3 dialogue, succession or grant simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def errors(t,e,v,i,s,o,lr_e,lr_v):
    out=[]
    ctx=block(t,'rw_rs_context_trigger')
    for g in ('rw_lr_record_valid_trigger = yes','has_variable = rw_lr_retained','var:rw_lr_serial = $ENTRY_SERIAL$',
              'var:rw_lr_title = $TITLE$','var:rw_lr_authority = $AUTHORITY$','var:rw_lr_former_house = $HOUSE$',
              'var:rw_lr_former_holder = $FORMER$','holder = $HOLDER$','tier >= tier_county',
              'is_noble_family_title = no','is_landless_type_title = no','is_imprisoned = no',
              'NOT = { this = $HOLDER$ }','NOT = { is_at_war_with = $REQUESTER$ }'):
        if g not in ctx:out.append('wrong entry parties or current title')
    for g in ('limit = { $FORMER$ = { is_alive = yes } }','$REQUESTER$ = $FORMER$',
              '$REQUESTER$ = { exists = house house = $HOUSE$ }','$HOUSE$ = { exists = house_head house_head = $REQUESTER$ }'):
        if g not in ctx:out.append('living former holder bypassed or wrong house successor')
    cool=block(t,'rw_rs_no_cooldown_trigger')
    for g in ('NOT = {','rw_rs_record_valid_trigger = yes','has_variable = rw_rs_cooldown',
              'var:rw_rs_requester = $REQUESTER$','var:rw_rs_holder = $HOLDER$','var:rw_rs_title = $TITLE$'):
        if g not in cool:out.append('pair title cooldown bypass')
    start=block(t,'rw_rs_can_consider_trigger')
    if 'rw_lr_view_trigger = yes' not in start or 'rw_rs_no_cooldown_trigger = { REQUESTER = root HOLDER = scope:rw_lr_title.holder TITLE = scope:rw_lr_title }' not in start:out.append('request lacks registry or cooldown guard')
    turn=block(t,'rw_rs_request_turn_trigger')
    if 'rw_rs_can_consider_trigger = yes' not in turn or 'exists = scope:rw_rs_holder' not in turn or 'scope:rw_lr_title = { holder = scope:rw_rs_holder }' not in turn:out.append('confirmation changed recipient')
    create=block(e,'rw_rs_create_effect')
    for g in ('limit = { rw_rs_request_turn_trigger = yes }','story_type = story_rw_restitution_request',
              'story_owner = scope:rw_rs_requester','NOT = { has_variable = rw_rs_schema }',
              'NOT = { has_variable = rw_rs_counter }','change_variable = { name = rw_rs_counter add = 1 }'):
        if g not in create:out.append('constructor or serial guard missing')
    for field in ('schema value = 1','kind value = flag:restitution_review','serial value = scope:rw_rs_serial',
                  'requester value = scope:rw_rs_requester','holder value = scope:rw_rs_holder','title value = scope:rw_lr_title',
                  'authority value = scope:rw_lr_authority','house value = scope:rw_lr_house','former value = scope:rw_lr_former_holder',
                  'entry value = scope:rw_lr_record','entry_serial value = scope:rw_lr_serial','state value = flag:pending','issued_on value = current_date',
                  'window value = flag:yes days = 30','cooldown value = flag:yes days = 365','retained value = flag:yes years = 5'):
        if not re.search(re.escape('name = rw_rs_'+field)+r'(?!\w)',create):out.append('wrong immutable identity or clocks')
    if not (0<=create.find('add_to_global_variable_list')<create.find('any_in_global_list')<create.find('scope:rw_rs_holder = { trigger_event')):out.append('notified before verified registration')
    if 'else = { scope:rw_rs_record = { rw_rs_retire_effect = yes } }' not in create:out.append('failed registration retained')
    if e.count('name = rw_rs_window')!=1 or e.count('name = rw_rs_cooldown')!=1 or e.count('name = rw_rs_retained')!=1:out.append('deadline cooldown or retention renewed')
    valid=block(t,'rw_rs_record_valid_trigger')
    if 'story_owner = var:rw_rs_requester' not in valid or 'var:rw_rs_kind = flag:restitution_review' not in valid:out.append('private request custody transferred')
    reader=block(t,'rw_rs_reader_trigger')
    for g in ('rw_rs_record_valid_trigger = yes','has_variable = rw_rs_retained','$READER$ = { is_alive = yes }',
              'OR = { var:rw_rs_requester = $READER$ var:rw_rs_holder = $READER$ }'):
        if g not in reader:out.append('nonparticipant private reader')
    if 'house_head' in reader or 'var:rw_rs_authority' in reader or re.search(r'(?<![\w:])holder\s*=\s*\$READER\$',reader):out.append('successor inherits private consent')
    view=block(t,'rw_rs_view_trigger')
    for key in ('serial','requester','holder','title','entry_serial','authority','house','former'):
        if f'exists = scope:rw_rs_{key}' not in view or f'var:rw_rs_{key} = scope:rw_rs_{key}' not in view:out.append('stale private tuple')
    if 'rw_rs_reader_trigger = { READER = root }' not in view:out.append('nonparticipant private reader')
    current=block(t,'rw_rs_current_context_trigger')
    if 'save_temporary_scope_as = rw_rs_check' not in current or 'ENTRY = scope:rw_rs_check.var:rw_rs_entry ENTRY_SERIAL = scope:rw_rs_check.var:rw_rs_entry_serial' not in current or 'REQUESTER = scope:rw_rs_check.var:rw_rs_requester HOLDER = scope:rw_rs_check.var:rw_rs_holder' not in current:out.append('stored context resolves in wrong scope')
    accept_gate=block(t,'rw_rs_can_accept_trigger')
    for g in ('rw_rs_view_trigger = yes','this = scope:rw_rs_holder','var:rw_rs_state = flag:pending has_variable = rw_rs_window rw_rs_current_context_trigger = yes'):
        if g not in accept_gate:out.append('stale late or nonholder acceptance')
    accept=block(e,'rw_rs_accept_effect')
    if 'limit = { rw_rs_can_accept_trigger = yes }' not in accept or not (0<=accept.find('value = flag:talks')<accept.find('trigger_event')):out.append('acceptance not consumed before notice')
    if 'name = rw_rs_window' in accept or 'flag:restored' in accept or 'flag:fulfilled' in accept:out.append('review mistaken for transfer or deadline reset')
    for name,party in (('refuse','holder'),('withdraw','requester')):
        gate=block(t,f'rw_rs_can_{name}_trigger');effect=block(e,f'rw_rs_{name}_effect')
        if 'rw_rs_view_trigger = yes' not in gate or f'this = scope:rw_rs_{party}' not in gate:out.append('terminal action identity bypass')
        if any(x in gate for x in ('rw_rs_current_context_trigger','rw_rs_window','is_character_interaction_valid')):out.append('terminal action trapped by changed context')
        if f'limit = {{ rw_rs_can_{name}_trigger = yes }}' not in effect or not (0<=effect.find('remove_variable = rw_rs_window')<effect.find('name = rw_rs_state')):out.append('terminal effect bypass')
    react=block(t,'rw_rs_can_react_trigger')
    for g in ('rw_rs_view_trigger = yes','this = scope:rw_rs_requester','scope:rw_rs_holder = { is_alive = yes }',
              'scope:rw_rs_title = { NOT = { holder = scope:rw_rs_requester } }','var:rw_rs_state = flag:refused',
              'has_variable = rw_rs_response_window','NOT = { has_variable = rw_rs_response_done }'):
        if g not in react:out.append('wrong late or already-held refusal reaction')
    resent=block(e,'rw_rs_resent_effect')
    if 'limit = { rw_rs_can_react_trigger = yes }' not in resent or not (0<=resent.find('name = rw_rs_response_done')<resent.find('has_opinion_modifier')<resent.find('add_opinion =')):out.append('reaction not consumed before opinion')
    if 'NOT = { has_opinion_modifier = { target = scope:rw_rs_holder modifier = rw_restitution_refused_opinion } }' not in resent or 'add_opinion = { target = scope:rw_rs_holder modifier = rw_restitution_refused_opinion }' not in resent:out.append('opinion wrong target stacks or renews')
    if not re.search(r'\bopinion\s*=\s*-10(?!\d)',o) or not re.search(r'\byears\s*=\s*2(?!\d)',o):out.append('wrong bounded opinion')
    if not re.search(r'name = rw_rs_response_window value = flag:yes days = 7(?!\d)',block(e,'rw_rs_refuse_effect')) or 'rw_rs_resent_effect' in block(e,'rw_rs_refuse_effect'):out.append('automatic or unbounded refusal penalty')
    acknowledge=block(e,'rw_rs_accept_refusal_effect')
    if 'limit = { rw_rs_can_react_trigger = yes }' not in acknowledge or 'name = rw_rs_response_done value = flag:acknowledged' not in acknowledge or 'add_opinion' in acknowledge:out.append('acknowledgement changes unrelated opinion')
    grant=block(t,'rw_rs_can_open_grant_trigger')
    for g in ('rw_rs_view_trigger = yes','this = scope:rw_rs_holder','is_ai = no',
              'var:rw_rs_state = flag:talks has_variable = rw_rs_window rw_rs_current_context_trigger = yes',
              'is_character_interaction_valid = { interaction = grant_titles_interaction recipient = scope:rw_rs_requester }'):
        if g not in grant:out.append('native grant guard bypass')
    if 'trigger = { rw_rs_can_open_grant_trigger = yes }' not in v or 'limit = { rw_rs_can_open_grant_trigger = yes }' not in v:out.append('native click not revalidated')
    win=nested(v,'open_interaction_window')
    for g in ('interaction = grant_titles_interaction','actor = root','recipient = scope:rw_rs_requester'):
        if g not in win:out.append('native grant parties swapped')
    if re.search(r'\b(target|flag|send_option|execute_threshold|secondary_recipient)\s*=',win):out.append('native grant preselected or forced')
    maint=block(e,'rw_rs_maintenance_effect')
    for g in ('rw_rs_record_valid_trigger = yes has_variable = rw_rs_retained','NOT = { has_variable = rw_rs_window }',
              'flag:expired','NOT = { rw_rs_current_context_trigger = yes }','flag:invalidated'):
        if g not in maint:out.append('expired or changed request revived')
    if 'trigger_event' in maint:out.append('maintenance sends recurring requests')
    retire=block(e,'rw_rs_retire_effect')
    if 'story_type = story_rw_restitution_request' not in retire or 'name = rw_restitution_requests target = scope:rw_rs_record' not in retire or not (0<=retire.find('remove_list_global_variable')<retire.find('end_story')):out.append('private index not retired first')
    if 'on_owner_death = { rw_rs_retire_effect = yes }' not in s or 'days = 60' not in s:out.append('request or consent inherited')
    offer=block(e,'rw_rs_offer_opportunity_effect')
    for g in ('rw_lr_record_valid_trigger = yes has_variable = rw_lr_retained','rw_lr_snapshot_effect = yes','clear_saved_scope = rw_rs_candidate',
              'limit = { var:rw_lr_former_holder = { is_alive = yes } }','var:rw_lr_former_house.house_head = { save_scope_as = rw_rs_candidate }',
              'rw_lr_reader_trigger = { READER = scope:rw_rs_candidate }','REQUESTER = scope:rw_rs_candidate HOLDER = scope:rw_lr_title.holder',
              'NOT = { var:rw_rs_notice_requester = scope:rw_rs_candidate }','NOT = { var:rw_rs_notice_holder = var:rw_lr_title.holder }',
              'scope:rw_rs_candidate = { trigger_event = { id = rw_restitution.0001 } }'):
        if g not in offer:out.append('wrong or repeated public-role opportunity')
    if 'rw_rs_can_consider_trigger' in offer or 'rw_rs_open_request_effect' in offer:out.append('story ROOT mistaken for claimant')
    if not (0<=offer.find('var:rw_rs_notice_holder = var:rw_lr_title.holder')<offer.find('rw_rs_no_cooldown_trigger')<offer.find('name = rw_rs_notice_requester')<offer.find('trigger_event')):out.append('unchanged pair rescan or notice loop')
    cache_fields=dict(re.findall(r'set_variable = \{ name = (\w+) value = ([^}\n]+)',offer));cache_fields={k:val.strip() for k,val in cache_fields.items()}
    if cache_fields!={'rw_rs_notice_requester':'scope:rw_rs_candidate','rw_rs_notice_holder':'var:rw_lr_title.holder'}:out.append('private negotiation exported to public entry')
    if lr_e.count('rw_rs_offer_opportunity_effect = yes')!=2 or 'trigger = { rw_rs_can_consider_trigger = yes }' not in lr_v:out.append('opportunity or manual request not integrated')
    lr_maint=block(lr_e,'rw_lr_maintenance_effect')
    if not (0<=lr_maint.find('rw_rs_offer_opportunity_effect')<lr_maint.find('rw_lr_rehome_effect')):out.append('public story read after possible retirement')
    read=block(e,'rw_rs_read_effect')
    if 'rw_rs_reader_trigger = { READER = scope:actor }' not in read or 'rw_rs_reader_trigger = { READER = scope:actor }' not in i or 'on_accept = { rw_rs_read_effect = yes }' not in i:out.append('archive participant bypass')
    if re.search(r'\b(set_variable|change_variable|add_opinion)\s*=',read+block(e,'rw_rs_snapshot_effect')):out.append('reading mutates conversation or clocks')
    code=clean_script(t+e+v+i+s+o)[0]
    if re.search(r'\b(run_interaction|send_interaction|change_title_holder|create_title_and_vassal_change|resolve_title_and_vassal_change|destroy_title|consume_revoke_title_reason|add_gold|add_prestige|add_trait|remove_trait|set_house|set_dynasty|make_story_owner|every_living_character|any_living_character|scheme_owner)\s*=',code):out.append('native title penalty inheritance or world scan added')
    if re.search(r'\b(rw_evidence_\w+|rw_ri_basis\w*|rw_scheme_evidence_record|rw_tp_record)\b',code):out.append('private evidence imported into restitution')
    return out


class RestitutionDialogueTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_restitution_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_restitution_effects.txt').read_text()
        self.v=(MOD/'events/rw_restitution_events.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_restitution_interactions.txt').read_text()
        self.s=(MOD/'common/story_cycles/rw_restitution_requests.txt').read_text()
        self.o=(MOD/'common/opinion_modifiers/rw_restitution_opinions.txt').read_text()
        self.lr_e=(MOD/'common/scripted_effects/rw_land_register_effects.txt').read_text()
        self.lr_v=(MOD/'events/rw_land_register_events.txt').read_text()

    def check(self,**kw):return errors(*(kw.get(k,getattr(self,k)) for k in ('t','e','v','i','s','o','lr_e','lr_v')))

    def test_contract(self):self.assertEqual([],self.check())

    def test_exact_public_entry_and_real_current_holder(self):
        for g in ('has_variable = rw_lr_retained','var:rw_lr_serial = $ENTRY_SERIAL$','var:rw_lr_title = $TITLE$',
                  'var:rw_lr_authority = $AUTHORITY$','var:rw_lr_former_house = $HOUSE$','holder = $HOLDER$',
                  'NOT = { this = $HOLDER$ }','NOT = { is_at_war_with = $REQUESTER$ }'):
            self.assertIn('wrong entry parties or current title',self.check(t=self.t.replace(g,'always = yes')))

    def test_original_living_party_precedes_house_head(self):
        for g in ('limit = { $FORMER$ = { is_alive = yes } }','$REQUESTER$ = $FORMER$',
                  '$REQUESTER$ = { exists = house house = $HOUSE$ }','$HOUSE$ = { exists = house_head house_head = $REQUESTER$ }'):
            self.assertIn('living former holder bypassed or wrong house successor',self.check(t=self.t.replace(g,'always = yes')))

    def test_cooldown_cannot_be_evaded_using_another_entry(self):
        for g in ('has_variable = rw_rs_cooldown','var:rw_rs_requester = $REQUESTER$','var:rw_rs_holder = $HOLDER$','var:rw_rs_title = $TITLE$'):
            self.assertIn('pair title cooldown bypass',self.check(t=self.t.replace(g,'always = yes')))
        self.assertNotIn('var:rw_rs_entry',block(self.t,'rw_rs_no_cooldown_trigger'))

    def test_stale_request_confirmation_cannot_pick_new_owner(self):
        self.assertIn('confirmation changed recipient',self.check(t=self.t.replace('scope:rw_lr_title = { holder = scope:rw_rs_holder }','always = yes')))
        self.assertIn('request lacks registry or cooldown guard',self.check(t=self.t.replace('rw_lr_view_trigger = yes','always = yes')))

    def test_fresh_constructor_serial_and_registration_before_notice(self):
        for g in ('limit = { rw_rs_request_turn_trigger = yes }','NOT = { has_variable = rw_rs_schema }','NOT = { has_variable = rw_rs_counter }'):
            self.assertIn('constructor or serial guard missing',self.check(e=self.e.replace(g,'always = yes')))
        self.assertIn('notified before verified registration',self.check(e=self.e.replace('add_to_global_variable_list','wrong_command')))
        self.assertIn('failed registration retained',self.check(e=self.e.replace('else = { scope:rw_rs_record = { rw_rs_retire_effect = yes } }','else = {}')))

    def test_all_captured_identities_are_immutable(self):
        for g in ('holder value = scope:rw_rs_holder','entry value = scope:rw_lr_record','entry_serial value = scope:rw_lr_serial','title value = scope:rw_lr_title','issued_on value = current_date'):
            self.assertIn('wrong immutable identity or clocks',self.check(e=self.e.replace(g,'broken value = 0')))
        self.assertIn('private request custody transferred',self.check(t=self.t.replace('story_owner = var:rw_rs_requester','always = yes')))

    def test_thirty_day_window_and_year_cooldown_never_renew(self):
        for a,b in (('days = 30','days = 300'),('days = 365','days = 3650'),('years = 5','years = 50')):
            self.assertIn('wrong immutable identity or clocks',self.check(e=self.e.replace(a,b)))
        self.assertIn('deadline cooldown or retention renewed',self.check(e=self.e+'\nset_variable = { name = rw_rs_window days = 30 }'))
        self.assertNotIn('remove_variable = rw_rs_counter',self.e+self.s)

    def test_only_original_participants_can_read_private_replies(self):
        self.assertIn('nonparticipant private reader',self.check(t=self.t.replace('OR = { var:rw_rs_requester = $READER$ var:rw_rs_holder = $READER$ }','always = yes')))
        self.assertIn('successor inherits private consent',self.check(t=self.t.replace('rw_rs_reader_trigger = {','rw_rs_reader_trigger = { var:rw_rs_authority = yes')))
        self.assertIn('archive participant bypass',self.check(i=self.i.replace('on_accept = { rw_rs_read_effect = yes }','on_accept = {}')))

    def test_stale_private_popup_matches_complete_tuple(self):
        for k in ('serial','requester','holder','title','entry_serial','authority','house','former'):
            self.assertIn('stale private tuple',self.check(t=self.t.replace(f'var:rw_rs_{k} = scope:rw_rs_{k}','always = yes')))
        self.assertIn('stored context resolves in wrong scope',self.check(t=self.t.replace('save_temporary_scope_as = rw_rs_check','save_temporary_scope_as = wrong')))

    def test_acceptance_revalidates_roles_owner_window_and_consumes_once(self):
        self.assertIn('stale late or nonholder acceptance',self.check(t=self.t.replace('var:rw_rs_state = flag:pending has_variable = rw_rs_window rw_rs_current_context_trigger = yes','always = yes')))
        self.assertIn('acceptance not consumed before notice',self.check(e=self.e.replace('name = rw_rs_state value = flag:talks','name = wrong value = 0')))
        self.assertNotIn('name = rw_rs_window',block(self.e,'rw_rs_accept_effect'))
        self.assertNotIn('flag:restored',self.e)
        self.assertNotIn('flag:fulfilled',self.e)

    def test_refusal_and_withdrawal_are_not_trapped_by_changed_context(self):
        for name in ('refuse','withdraw'):
            self.assertIn('terminal effect bypass',self.check(e=self.e.replace(f'limit = {{ rw_rs_can_{name}_trigger = yes }}','limit = { always = yes }')))
            self.assertIn('terminal action trapped by changed context',self.check(t=self.t.replace(f'rw_rs_can_{name}_trigger = {{',f'rw_rs_can_{name}_trigger = {{ rw_rs_current_context_trigger = yes')))

    def test_expiry_invalid_roles_cleanup_and_no_inherited_consent(self):
        self.assertIn('expired or changed request revived',self.check(e=self.e.replace('NOT = { rw_rs_current_context_trigger = yes }','always = yes')))
        self.assertIn('private index not retired first',self.check(e=self.e.replace('remove_list_global_variable','wrong_command')))
        self.assertIn('request or consent inherited',self.check(s=self.s.replace('on_owner_death = { rw_rs_retire_effect = yes }','on_owner_death = {}')))
        self.assertIn('maintenance sends recurring requests',self.check(e=self.e.replace('rw_rs_maintenance_effect = {','rw_rs_maintenance_effect = { trigger_event = yes')))

    def test_optional_reaction_has_exact_requester_refuser_and_seven_day_limit(self):
        for g in ('this = scope:rw_rs_requester','scope:rw_rs_holder = { is_alive = yes }','var:rw_rs_state = flag:refused',
                  'has_variable = rw_rs_response_window','NOT = { has_variable = rw_rs_response_done }',
                  'scope:rw_rs_title = { NOT = { holder = scope:rw_rs_requester } }'):
            self.assertIn('wrong late or already-held refusal reaction',self.check(t=self.t.replace(g,'always = yes')))
        self.assertIn('automatic or unbounded refusal penalty',self.check(e=self.e.replace('name = rw_rs_response_window value = flag:yes days = 7','name = rw_rs_response_window value = flag:yes days = 70')))

    def test_rancour_is_once_nonstacking_nonrenewing_and_personal(self):
        self.assertIn('reaction not consumed before opinion',self.check(e=self.e.replace('name = rw_rs_response_done value = flag:resented','name = wrong value = 0')))
        self.assertIn('opinion wrong target stacks or renews',self.check(e=self.e.replace('NOT = { has_opinion_modifier = { target = scope:rw_rs_holder modifier = rw_restitution_refused_opinion } }','always = yes')))
        self.assertIn('wrong bounded opinion',self.check(o=self.o.replace('opinion = -10','opinion = -100')))
        self.assertIn('acknowledgement changes unrelated opinion',self.check(e=self.e.replace('rw_rs_accept_refusal_effect = {','rw_rs_accept_refusal_effect = { add_opinion = yes')))
        self.assertNotIn('add_opinion',block(self.e,'rw_rs_refuse_effect'))

    def test_native_grant_requires_both_current_parties_and_explicit_review(self):
        self.assertIn('native grant guard bypass',self.check(t=self.t.replace('var:rw_rs_state = flag:talks has_variable = rw_rs_window rw_rs_current_context_trigger = yes','always = yes')))
        self.assertIn('native click not revalidated',self.check(v=self.v.replace('limit = { rw_rs_can_open_grant_trigger = yes }','limit = { always = yes }')))
        self.assertIn('native grant parties swapped',self.check(v=self.v.replace('actor = root','actor = scope:rw_rs_requester')))
        self.assertIn('native grant preselected or forced',self.check(v=self.v.replace('actor = root','actor = root target = scope:rw_rs_title')))

    def test_opportunities_use_candidate_not_story_root(self):
        self.assertIn('story ROOT mistaken for claimant',self.check(e=self.e.replace('rw_rs_offer_opportunity_effect = {','rw_rs_offer_opportunity_effect = { rw_rs_can_consider_trigger = yes')))
        self.assertIn('wrong or repeated public-role opportunity',self.check(e=self.e.replace('REQUESTER = scope:rw_rs_candidate HOLDER = scope:rw_lr_title.holder','REQUESTER = root HOLDER = scope:rw_lr_title.holder')))
        self.assertIn('unchanged pair rescan or notice loop',self.check(e=self.e.replace('NOT = { var:rw_rs_notice_holder = var:rw_lr_title.holder }','always = yes')))
        self.assertNotIn('is_ai',self.e)

    def test_public_entry_gets_only_public_role_notification_caches(self):
        self.assertIn('private negotiation exported to public entry',self.check(e=self.e.replace('name = rw_rs_notice_requester value = scope:rw_rs_candidate','name = rw_rs_notice_requester value = scope:rw_rs_record')))
        self.assertIn('opportunity or manual request not integrated',self.check(lr_e=self.lr_e.replace('rw_rs_offer_opportunity_effect = yes','')))
        self.assertIn('reading mutates conversation or clocks',self.check(e=self.e.replace('rw_rs_read_effect = {','rw_rs_read_effect = { set_variable = yes')))

    def test_no_forced_title_native_punishment_or_private_evidence(self):
        for g in ('change_title_holder','run_interaction','add_gold','consume_revoke_title_reason','make_story_owner','scheme_owner'):
            self.assertIn('native title penalty inheritance or world scan added',self.check(e=self.e+'\n'+g+' = yes'))
        self.assertIn('private evidence imported into restitution',self.check(e=self.e+'\nrw_scheme_evidence_record = yes'))

    def test_complete_bilingual_consent_and_reaction_terms(self):
        keys=set(re.findall(r'(?:name|title|desc)\s*=\s*(rw_restitution\.[\w.]+)',self.v+self.lr_v))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_restitution_l_{lang}.yml';self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig')
            for k in keys:self.assertIn(' '+k+':0 ',text)
            for k in ('rw_lr_title','rw_rs_title','rw_rs_holder','rw_rs_requester','rw_rs_authority'):self.assertIn('['+k+'.',text)
            self.assertIn(' rw_restitution_refused_opinion:0 ',text)
        self.assertEqual(1,self.v.count('open_interaction_window ='))
