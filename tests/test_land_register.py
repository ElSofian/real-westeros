"""Adversarial source checks for public-fact custody, not CK3 succession simulation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'
FIELDS={
 'schema':'1','kind':'flag:title_transfer_observation','serial':'scope:rw_lr_serial',
 'source_serial':'scope:rw_tp_serial','issuer':'scope:rw_tp_observer','title':'scope:rw_tp_title',
 'former_holder':'scope:rw_tp_former_holder','new_holder':'scope:rw_tp_new_holder',
 'authority':'scope:rw_lr_authority','former_house':'scope:rw_lr_house',
 'observed_on':'scope:rw_tp_record.var:rw_tp_observed_on','filed_on':'current_date',
 'retained':'flag:yes years = 100'}


def contract_errors(t,e,v,i,s,tp_e,tp_v):
    out=[]
    capture=block(t,'rw_lr_capture_trigger')
    for g in ('exists = scope:rw_ri_fresh_receipt','scope:rw_ri_fresh_receipt = scope:rw_tp_record',
              'this = scope:rw_tp_observer','rw_house_sovereign_trigger = yes','scope:previous_holder = { exists = house }',
              'exists = scope:revoke_title_interaction','this = scope:actor','scope:recipient = scope:previous_holder',
              'scope:landed_title = scope:title','scope:title = { exists = holder holder = root }',
              'rw_tp_reader_trigger = { READER = root }','var:rw_tp_serial = scope:rw_tp_serial','var:rw_tp_title = scope:title',
              'var:rw_tp_new_holder = root','var:rw_tp_former_holder = scope:previous_holder',
              'NOT = { has_variable = rw_lr_offer_scheduled }','NOT = { has_variable = rw_tp_land_authority }',
              'NOT = { has_variable = rw_tp_former_house }'):
        if g not in capture:out.append('old incomplete or wrong capture')
    freeze=block(e,'rw_lr_capture_effect')
    for g in ('limit = { rw_lr_capture_trigger = yes }',
              'name = rw_tp_land_authority value = scope:rw_tp_observer.primary_title',
              'name = rw_tp_former_house value = scope:previous_holder.house'):
        if g not in freeze:out.append('historical authority or house guessed')
    if not (freeze.find('name = rw_lr_offer_scheduled')<freeze.find('trigger_event')) or freeze.count('trigger_event =')!=1 or 'id = rw_land_registry.0002 days = 1' not in freeze:out.append('offer repeated or clock renewed')
    consider=block(t,'rw_lr_can_consider_trigger')
    for g in ('rw_tp_view_trigger = yes','rw_house_sovereign_trigger = yes','exists = var:rw_tp_land_authority',
              'exists = var:rw_tp_former_house','var:rw_tp_land_authority = { exists = holder holder = root }',
              'NOT = { has_variable = rw_tp_land_deposited }','has_global_variable_list = rw_land_register',
              'NOT = {','any_in_global_list','rw_lr_record_valid_trigger = yes','var:rw_lr_issuer = root',
              'var:rw_lr_source_serial = scope:rw_tp_serial'):
        if g not in consider:out.append('unauthorized or repeated publication')
    turn=block(t,'rw_lr_deposit_turn_trigger')
    for g in ('rw_lr_can_consider_trigger = yes','exists = scope:rw_lr_authority','exists = scope:rw_lr_house',
              'var:rw_tp_land_authority = scope:rw_lr_authority','var:rw_tp_former_house = scope:rw_lr_house'):
        if g not in turn:out.append('stale deposit confirmation')
    deposit=block(e,'rw_lr_deposit_effect')
    for g in ('limit = { rw_lr_deposit_turn_trigger = yes }','story_type = story_rw_land_register',
              'story_owner = scope:rw_tp_observer','NOT = { has_variable = rw_lr_schema }',
              'NOT = { has_variable = rw_lr_counter }','change_variable = { name = rw_lr_counter add = 1 }'):
        if g not in deposit:out.append('unsafe public constructor')
    before=deposit.split('add_to_global_variable_list',1)[0]
    body=nested(before[before.rfind('scope:rw_lr_record = {'):],'scope:rw_lr_record')
    fields=dict(re.findall(r'set_variable\s*=\s*\{\s*name\s*=\s*rw_lr_(\w+)\s+value\s*=\s*([^}\n]+)',body))
    fields={k:val.strip() for k,val in fields.items()}
    if fields!=FIELDS:out.append('public payload is not the exact fact allowlist')
    if not (0<=deposit.find('add_to_global_variable_list')<deposit.find('any_in_global_list')<deposit.find('name = rw_tp_land_deposited')<deposit.find('id = rw_land_registry.0003')):out.append('source consumed before verified registration')
    if 'else = { scope:rw_lr_record = { rw_lr_retire_effect = yes } }' not in deposit:out.append('failed registration not retired')
    if e.count('name = rw_lr_retained')!=1:out.append('archive retention renewed')
    if 'remove_variable = rw_lr_counter' in e:out.append('authority serial reused')
    valid=block(t,'rw_lr_record_valid_trigger')
    for g in ('story_type = story_rw_land_register','var:rw_lr_schema = 1','var:rw_lr_kind = flag:title_transfer_observation',
              'has_variable = rw_lr_serial','has_variable = rw_lr_source_serial','has_variable = rw_lr_observed_on',
              'has_variable = rw_lr_filed_on','var:rw_lr_issuer = var:rw_lr_new_holder'):
        if g not in valid:out.append('untyped malformed public fact')
    reader=block(t,'rw_lr_reader_trigger')
    for g in ('rw_lr_record_valid_trigger = yes','has_variable = rw_lr_retained','$READER$ = { is_alive = yes }',
              'var:rw_lr_authority = { exists = holder holder = $READER$ }','var:rw_lr_title = { exists = holder holder = $READER$ }',
              'var:rw_lr_former_holder = $READER$','var:rw_lr_new_holder = $READER$',
              'AND = { $READER$ = { exists = house } var:rw_lr_former_house = $READER$.house }'):
        if g not in reader:out.append('reader role or expiry bypass')
    if re.search(r'\b(story_owner|dynasty|is_ai)\b',reader):out.append('custody dynasty or AI substituted for role')
    view=block(t,'rw_lr_view_trigger')
    if 'rw_lr_reader_trigger = { READER = root }' not in view:out.append('stale public popup')
    for key,alias in (('serial','serial'),('authority','authority'),('former_house','house'),('title','title'),('former_holder','former_holder'),('new_holder','new_holder')):
        if f'exists = scope:rw_lr_{alias}' not in view or f'var:rw_lr_{key} = scope:rw_lr_{alias}' not in view:out.append('stale public popup')
    current=block(t,'rw_lr_original_owner_still_holds_trigger')
    if 'rw_lr_view_trigger = yes' not in current or 'exists = holder holder = scope:rw_lr_new_holder' not in current:out.append('history treated as current title ownership')
    carry=block(t,'rw_lr_can_carry_trigger')
    for g in ('is_alive = yes','exists = scope:rw_lr_departed','NOT = { this = scope:rw_lr_departed }'):
        if g not in carry:out.append('departing owner can keep record')
    rehome=block(e,'rw_lr_rehome_effect')
    if 'rw_lr_record_valid_trigger = yes has_variable = rw_lr_retained' not in rehome:out.append('malformed or expired storage moved')
    for g in ('var:rw_lr_authority = { exists = holder holder = { rw_lr_can_carry_trigger = yes } }',
              'var:rw_lr_title = { exists = holder holder = { rw_lr_can_carry_trigger = yes } }',
              'var:rw_lr_former_house = { exists = house_head house_head = { rw_lr_can_carry_trigger = yes } }',
              'var:rw_lr_former_holder = { rw_lr_can_carry_trigger = yes }',
              'var:rw_lr_new_holder = { rw_lr_can_carry_trigger = yes }',
              'any_house_member = { rw_lr_can_carry_trigger = yes }',
              'random_house_member = { limit = { rw_lr_can_carry_trigger = yes }'):
        if g not in rehome:out.append('storage succession bypass')
    death=block(e,'rw_lr_owner_died_effect')
    if not (0<=death.find('save_scope_as = rw_lr_departed')<death.find('rw_lr_rehome_effect = yes')):out.append('owner death assumed native alive flag settled')
    maintenance=block(e,'rw_lr_maintenance_effect')
    if not (0<=maintenance.find('clear_saved_scope = rw_lr_departed')<maintenance.find('rw_lr_rehome_effect = yes')):out.append('maintenance retained stale departed alias')
    retire=block(e,'rw_lr_retire_effect')
    for g in ('limit = { story_type = story_rw_land_register }','remove_list_global_variable = { name = rw_land_register target = scope:rw_lr_record }'):
        if g not in retire:out.append('wrong registry retired')
    if not (0<=retire.find('remove_list_global_variable')<retire.find('end_story = yes')):out.append('ended record remains indexed')
    if 'on_owner_death = { rw_lr_owner_died_effect = yes }' not in s or 'rw_lr_maintenance_effect = yes' not in s or 'days = 60' not in s:out.append('archive lifecycle unwired')
    read=block(e,'rw_lr_read_effect')
    for g in ('scope:actor = { is_alive = yes }','has_global_variable_list = rw_land_register',
              'limit = { rw_lr_reader_trigger = { READER = scope:actor } }','rw_lr_snapshot_effect = yes'):
        if g not in read:out.append('foreign registry enumeration')
    if 'rw_lr_reader_trigger = { READER = scope:actor }' not in i or 'on_accept = { rw_lr_read_effect = yes }' not in i:out.append('public interaction bypass')
    if 'trigger = { rw_lr_deposit_turn_trigger = yes }' not in v or 'rw_lr_deposit_effect = yes' not in v or 'trigger = { rw_lr_view_trigger = yes }' not in v:out.append('public event guard missing')
    if 'trigger = { rw_lr_can_consider_trigger = yes }' not in tp_v or 'rw_lr_open_deposit_effect = yes' not in tp_v:out.append('private publication navigation bypass')
    if not (tp_e.find('save_scope_as = rw_ri_fresh_receipt')<tp_e.find('rw_lr_capture_effect = yes')<tp_e.find('clear_saved_scope = rw_ri_fresh_receipt')):out.append('capture outside fresh receipt lifetime')
    code=clean_script(t+e+v+i+s)[0]
    if re.search(r'\b(run_interaction|send_interaction|open_interaction_window|change_title_holder|create_title_and_vassal_change|resolve_title_and_vassal_change|destroy_title|consume_revoke_title_reason|revoke_title_interaction_effect|add_gold|add_prestige|add_opinion|add_trait|remove_trait|set_house|set_dynasty|imprison|death|every_living_character|any_living_character|every_dynasty_member|every_house_member|scheme_owner)\s*=',code):out.append('native sanction or world scan added')
    if re.search(r'\b(rw_scheme_evidence_record|rw_evidence_[\w]+|rw_ri_basis[\w]*|rw_tp_intent[\w]*)\b',code):out.append('private case material in institutional module')
    # Reading, storage movement and cleanup cannot modify retention or public facts.
    for name in ('rw_lr_read_effect','rw_lr_snapshot_effect','rw_lr_rehome_effect','rw_lr_owner_died_effect','rw_lr_maintenance_effect','rw_lr_retire_effect'):
        if re.search(r'\b(set_variable|change_variable|add_to_global_variable_list)\s*=',clean_script(block(e,name))[0]):out.append('reading or custody rewrites history or clock')
    return out


class LandRegisterTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_land_register_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_land_register_effects.txt').read_text()
        self.v=(MOD/'events/rw_land_register_events.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_land_register_interactions.txt').read_text()
        self.s=(MOD/'common/story_cycles/rw_land_register.txt').read_text()
        self.tp_e=(MOD/'common/scripted_effects/rw_title_provenance_effects.txt').read_text()
        self.tp_v=(MOD/'events/rw_title_provenance_events.txt').read_text()

    def check(self,**kw):return contract_errors(*(kw.get(k,getattr(self,k)) for k in ('t','e','v','i','s','tp_e','tp_v')))

    def test_contract(self):self.assertEqual([],self.check())

    def test_capture_cannot_backfill_old_or_missing_native_context(self):
        for g in ('exists = scope:rw_ri_fresh_receipt','scope:rw_ri_fresh_receipt = scope:rw_tp_record',
                  'exists = scope:revoke_title_interaction','scope:landed_title = scope:title','var:rw_tp_title = scope:title',
                  'NOT = { has_variable = rw_tp_land_authority }','NOT = { has_variable = rw_tp_former_house }'):
            self.assertIn('old incomplete or wrong capture',self.check(t=self.t.replace(g,'always = yes')))
        self.assertIn('historical authority or house guessed',self.check(e=self.e.replace('value = scope:previous_holder.house','value = scope:rw_tp_observer.house')))
        self.assertIn('capture outside fresh receipt lifetime',self.check(tp_e=self.tp_e.replace('rw_lr_capture_effect = yes','')))

    def test_current_authority_and_private_owner_required_to_publish(self):
        for g in ('rw_tp_view_trigger = yes','rw_house_sovereign_trigger = yes',
                  'var:rw_tp_land_authority = { exists = holder holder = root }','NOT = { has_variable = rw_tp_land_deposited }'):
            self.assertIn('unauthorized or repeated publication',self.check(t=self.t.replace(g,'always = yes')))

    def test_global_source_identity_cannot_be_republished(self):
        for g in ('rw_lr_record_valid_trigger = yes','var:rw_lr_issuer = root','var:rw_lr_source_serial = scope:rw_tp_serial'):
            self.assertIn('unauthorized or repeated publication',self.check(t=self.t.replace(g,'always = yes')))

    def test_confirmed_authority_house_cannot_silently_change(self):
        for g in ('var:rw_tp_land_authority = scope:rw_lr_authority','var:rw_tp_former_house = scope:rw_lr_house'):
            self.assertIn('stale deposit confirmation',self.check(t=self.t.replace(g,'always = yes')))
        self.assertIn('unsafe public constructor',self.check(e=self.e.replace('limit = { rw_lr_deposit_turn_trigger = yes }','limit = { always = yes }')))

    def test_public_payload_exactly_excludes_private_case_and_intention(self):
        self.assertIn('public payload is not the exact fact allowlist',self.check(e=self.e.replace('name = rw_lr_kind value = flag:title_transfer_observation','name = rw_lr_kind value = flag:convicted')))
        self.assertIn('public payload is not the exact fact allowlist',self.check(e=self.e.replace('name = rw_lr_filed_on value = current_date','name = rw_lr_filed_on value = current_date } set_variable = { name = rw_lr_private_case value = scope:rw_scheme_evidence_record')))
        self.assertIn('private case material in institutional module',self.check(e=self.e+'\nrw_ri_basis = yes'))

    def test_fresh_constructor_counter_and_registration_order(self):
        for g in ('NOT = { has_variable = rw_lr_schema }','NOT = { has_variable = rw_lr_counter }','story_owner = scope:rw_tp_observer'):
            self.assertIn('unsafe public constructor',self.check(e=self.e.replace(g,'always = yes')))
        self.assertIn('source consumed before verified registration',self.check(e=self.e.replace('name = rw_tp_land_deposited','name = wrong_flag')))
        self.assertIn('failed registration not retired',self.check(e=self.e.replace('else = { scope:rw_lr_record = { rw_lr_retire_effect = yes } }','else = {}')))

    def test_fixed_hundred_year_archive_not_a_land_ban(self):
        self.assertIn('public payload is not the exact fact allowlist',self.check(e=self.e.replace('years = 100','years = 1000')))
        self.assertIn('archive retention renewed',self.check(e=self.e+'\nset_variable = { name = rw_lr_retained years = 100 }'))
        self.assertIn('reading or custody rewrites history or clock',self.check(e=self.e.replace('rw_lr_read_effect = {','rw_lr_read_effect = { set_variable = { name = rw_lr_retained years = 100 }')))
        self.assertIn('authority serial reused',self.check(e=self.e+'\nremove_variable = rw_lr_counter'))

    def test_readers_are_current_roles_not_custody_or_whole_dynasty(self):
        for g in ('has_variable = rw_lr_retained','$READER$ = { is_alive = yes }','var:rw_lr_title = { exists = holder holder = $READER$ }',
                  'var:rw_lr_authority = { exists = holder holder = $READER$ }','var:rw_lr_former_house = $READER$.house'):
            self.assertIn('reader role or expiry bypass',self.check(t=self.t.replace(g,'always = yes')))
        for g in ('story_owner = $READER$','dynasty = $READER$.dynasty','is_ai = no'):
            self.assertIn('custody dynasty or AI substituted for role',self.check(t=self.t.replace('rw_lr_reader_trigger = {','rw_lr_reader_trigger = { '+g)))

    def test_stale_or_wrong_public_record_tuple(self):
        for k,a in (('serial','serial'),('authority','authority'),('former_house','house'),('title','title'),('former_holder','former_holder'),('new_holder','new_holder')):
            self.assertIn('stale public popup',self.check(t=self.t.replace(f'var:rw_lr_{k} = scope:rw_lr_{a}','always = yes')))
        self.assertIn('history treated as current title ownership',self.check(t=self.t.replace('exists = holder holder = scope:rw_lr_new_holder','always = yes')))

    def test_owner_death_does_not_depend_on_native_flag_order(self):
        self.assertIn('departing owner can keep record',self.check(t=self.t.replace('NOT = { this = scope:rw_lr_departed }','always = yes')))
        self.assertIn('owner death assumed native alive flag settled',self.check(e=self.e.replace('save_scope_as = rw_lr_departed','save_scope_as = wrong')))
        self.assertIn('maintenance retained stale departed alias',self.check(e=self.e.replace('clear_saved_scope = rw_lr_departed','clear_saved_scope = wrong')))

    def test_storage_fallbacks_keep_only_living_eligible_carriers(self):
        for g in ('var:rw_lr_authority = { exists = holder holder = { rw_lr_can_carry_trigger = yes } }',
                  'var:rw_lr_title = { exists = holder holder = { rw_lr_can_carry_trigger = yes } }',
                  'var:rw_lr_former_holder = { rw_lr_can_carry_trigger = yes }','var:rw_lr_new_holder = { rw_lr_can_carry_trigger = yes }',
                  'any_house_member = { rw_lr_can_carry_trigger = yes }'):
            self.assertIn('storage succession bypass',self.check(e=self.e.replace(g,'always = yes')))
        self.assertIn('malformed or expired storage moved',self.check(e=self.e.replace('rw_lr_record_valid_trigger = yes has_variable = rw_lr_retained','always = yes')))

    def test_retirement_removes_index_before_ending(self):
        self.assertIn('wrong registry retired',self.check(e=self.e.replace('name = rw_land_register target = scope:rw_lr_record','name = wrong_index target = scope:rw_lr_record')))
        self.assertIn('ended record remains indexed',self.check(e=self.e.replace('end_story = yes','')))
        self.assertIn('archive lifecycle unwired',self.check(s=self.s.replace('rw_lr_owner_died_effect = yes','end_story = yes')))

    def test_journal_actor_only_no_selected_recipient_notice(self):
        self.assertIn('foreign registry enumeration',self.check(e=self.e.replace('limit = { rw_lr_reader_trigger = { READER = scope:actor } }','limit = { always = yes }')))
        self.assertIn('public interaction bypass',self.check(i=self.i.replace('on_accept = { rw_lr_read_effect = yes }','on_accept = {}')))
        self.assertNotIn('scope:recipient',self.e+self.i+self.v)

    def test_single_shared_offer_no_repeat_or_automatic_deposit(self):
        self.assertIn('offer repeated or clock renewed',self.check(e=self.e.replace('id = rw_land_registry.0002 days = 1','id = rw_land_registry.0002 days = 2')))
        self.assertIn('public event guard missing',self.check(v=self.v.replace('trigger = { rw_lr_deposit_turn_trigger = yes }','trigger = { always = yes }')))
        self.assertIn('private publication navigation bypass',self.check(tp_v=self.tp_v.replace('trigger = { rw_lr_can_consider_trigger = yes }','trigger = { always = yes }')))
        self.assertNotIn('is_ai',self.t+self.e)
        self.assertNotIn('rw_lr_deposit_effect',block(self.e,'rw_lr_capture_effect'))

    def test_no_native_effect_or_new_gameplay_entitlement(self):
        for g in ('change_title_holder','add_gold','consume_revoke_title_reason','set_house','every_living_character','open_interaction_window'):
            self.assertIn('native sanction or world scan added',self.check(e=self.e+'\n'+g+' = yes'))
        self.assertNotIn('scheme_owner',self.t+self.e)
        self.assertNotIn('rw_tp_record',block(self.e,'rw_lr_rehome_effect'))
        self.assertNotIn('rw_tp_record',block(self.e,'rw_lr_read_effect'))

    def test_complete_bilingual_refs_and_public_only_names(self):
        keys=set(re.findall(r'(?:name|title|desc)\s*=\s*(rw_land_registry\.[\w.]+)',self.v+self.tp_v))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_land_register_l_{lang}.yml';self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig')
            for k in keys:self.assertIn(' '+k+':0 ',text)
            for k in ('rw_lr_authority','rw_lr_house','rw_lr_title','rw_lr_former_holder','rw_lr_new_holder'):self.assertIn('['+k+'.',text)
            self.assertNotIn('rw_scheme_',text)
            self.assertNotIn('rw_ri_basis',text)
