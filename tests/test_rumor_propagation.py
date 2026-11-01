"""Adversarial source checks, not a Python model of CK3 knowledge or propagation."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def rumor_errors(t,e,s,v,i,a):
    out=[]
    seed=block(t,'rw_ru_can_seed_trigger')
    for g in ('rw_allegation_claimant_turn_trigger = yes','this = scope:rw_service_client',
              'var:rw_case_kind = flag:allegation','NOT = { has_variable = rw_ru_seeded }'):
        if g not in seed:out.append('source claimant kind or once guard bypassed')
    reader=block(t,'rw_ru_reader_trigger')
    for g in ('rw_ru_packet_trigger = yes','has_variable = rw_ru_packet_retained','story_owner = $READER$','$READER$ = { is_alive = yes }'):
        if g not in reader:out.append('private packet knowledge bypassed')
    if 'rw_ru_origin_trigger' in reader or 'rw_case_reader_allowed_trigger' in reader:out.append('packet depends on private source case or retired root')
    view=block(t,'rw_ru_view_trigger')
    for g in ('this = scope:rw_ru_holder','var:rw_ru_packet_serial = scope:rw_ru_packet_serial',
              'var:rw_ru_origin_serial = scope:rw_ru_origin_serial','var:rw_ru_speaker = scope:rw_ru_speaker',
              'var:rw_ru_subject = scope:rw_ru_subject','var:rw_ru_sender = scope:rw_ru_sender',
              'var:rw_ru_issued_on = scope:rw_ru_issued_on','var:rw_ru_heard_on = scope:rw_ru_heard_on',
              'var:rw_ru_hops = scope:rw_ru_hops'):
        if g not in view:out.append('stale or substituted personal account')
    relay=block(t,'rw_ru_relayable_trigger')
    for g in ('rw_ru_view_trigger = yes','rw_ru_party_trigger = yes','NOT = { has_character_flag = rw_ru_relay_cooldown }',
              'scope:rw_ru_subject = { is_alive = yes }','var:rw_ru_origin = scope:rw_ru_origin','rw_ru_origin_trigger = yes',
              'has_variable = rw_ru_origin_retained','var:rw_ru_speaker = scope:rw_ru_speaker',
              'var:rw_ru_subject = scope:rw_ru_subject','var:rw_ru_origin_serial = scope:rw_ru_origin_serial',
              'var:rw_ru_issued_on = scope:rw_ru_issued_on','any_in_list = { variable = rw_ru_holders this = scope:rw_ru_holder }'):
        if g not in relay:out.append('unowned expired or laundered lineage relayed')
    send=block(t,'rw_ru_can_send_trigger')
    for g in ('rw_ru_relayable_trigger = yes','scope:rw_ru_receiver = { rw_ru_party_trigger = yes }',
              'NOT = { this = scope:rw_ru_receiver }','in_diplomatic_range = scope:rw_ru_receiver',
              'NOT = { any_in_list = { variable = rw_ru_holders this = scope:rw_ru_receiver } }'):
        if g not in send:out.append('known receiver self loop or range bypassed')
    for name,guard in (('rw_ru_seed_effect','rw_ru_can_seed_trigger'),('rw_ru_send_effect','rw_ru_can_send_trigger'),('rw_ru_create_packet_effect','rw_ru_can_create_packet_trigger')):
        if 'limit = { '+guard+' = yes }' not in block(e,name):out.append('direct effect bypass')
    constructor=block(e,'rw_ru_create_packet_effect')
    for g in ('clear_saved_scope = rw_ru_new_packet','story_owner = scope:rw_ru_receiver','NOT = { has_variable = rw_ru_schema }',
              'name = rw_ru_sender value = scope:rw_ru_holder','name = rw_ru_speaker value = scope:rw_ru_speaker',
              'name = rw_ru_subject value = scope:rw_ru_subject','name = rw_ru_origin_serial value = scope:rw_ru_origin_serial',
              'name = rw_ru_issued_on value = scope:rw_ru_issued_on','name = rw_ru_heard_on value = current_date',
              'name = rw_ru_hops value = scope:rw_ru_hops','change_variable = { name = rw_ru_hops add = 1 }'):
        if g not in constructor:out.append('receiver source relay date or hop provenance changed')
    order=[constructor.find(g) for g in ('name = rw_ru_packet_retained','add_to_variable_list = { name = rw_ru_holders target = scope:rw_ru_receiver }',
           'flag = rw_ru_relay_cooldown days = 30','trigger_event = { id = rw_rumors.0001 days = 1 }')]
    if min(order)<0 or order!=sorted(order):out.append('notification before knowledge dedup or cooldown')
    if e.count('name = rw_ru_origin_retained value = flag:yes days = 365')!=1 or 'rw_ru_origin_retained' in constructor:
        out.append('lineage lifetime renewed by relay')
    fields=set(re.findall(r'\bset_variable\s*=\s*\{\s*name\s*=\s*(\w+)',constructor))
    allowed={'rw_ru_schema','rw_ru_kind','rw_ru_packet_serial','rw_ru_origin','rw_ru_speaker','rw_ru_subject',
             'rw_ru_sender','rw_ru_origin_serial','rw_ru_issued_on','rw_ru_heard_on','rw_ru_hops','rw_ru_packet_retained',
             'rw_ru_packet_counter'}
    if not fields<=allowed:out.append('private source case or truth exported')
    if re.search(r'\b(?:scope:rw_case_record|rw_case_evidence|rw_service_price|rw_fd_|rw_dp_)',constructor):out.append('private source case or truth exported')
    owner=block(e,'rw_ru_origin_owner_died_effect')
    for g in ('story_owner = { save_scope_as = rw_ru_departed }','variable = rw_ru_holders',
              'NOT = { this = scope:rw_ru_departed }','any_owned_story = { rw_ru_packet_trigger = yes',
              'var:rw_ru_origin = scope:rw_ru_origin','make_story_owner = scope:rw_ru_custodian'):
        if g not in ' '.join(owner.split()):out.append('custody grants uninformed party knowledge')
    if 'on_owner_death = { end_story = yes }' not in block(s,'story_rw_rumor_packet'):out.append('personal packet inherited')
    if 'days = 60' not in s:out.append('retirement missing')
    if 'rw_ru_seed_effect = yes' not in block(a,'rw_allegations.0002'):out.append('genuine source not integrated')
    if re.search(r'\brw_ru_\w+_effect\s*=',block(a,'rw_allegations.0003')):out.append('read-only source archive changed')
    if 'trigger = { rw_ru_can_send_trigger = yes }' not in block(v,'rw_rumors.0002') or 'name = rw_rumor.keep ai_chance = { base = 50 }' not in v:
        out.append('explicit guarded sender choice lost')
    code=clean_script(t+e+s+v+i)[0]
    if re.search(r'\b(?:is_ai|add_gold|add_prestige|add_opinion|imprison|run_interaction|add_secret|expose_scheme_agent|add_hook|create_character_memory|change_title_holder|every_living_character|any_living_character)\s*=',code):
        out.append('truth native sanction or global policy mutation')
    if re.search(r'\bname\s*=\s*rw_(?:case_|dp_|service_|evidence_)',code):out.append('source case or unrelated contract rewritten')
    for name in ('rw_ru_snapshot_effect','rw_ru_read_effect'):
        if re.search(r'\b(?:set_variable|add_character_flag|add_to_variable_list)\s*=',block(e,name)):out.append('read renews knowledge or clocks')
    if 'ai_targets = { ai_recipients = liege }' not in i:out.append('unbounded AI target search')
    return out


class RumorPropagationTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_rumor_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_rumor_effects.txt').read_text()
        self.s=(MOD/'common/story_cycles/rw_rumors.txt').read_text()
        self.v=(MOD/'events/rw_rumor_events.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_rumor_interactions.txt').read_text()
        self.a=(MOD/'events/rw_allegation_events.txt').read_text()

    def errors(self,**changes):return rumor_errors(*(changes.get(k,getattr(self,k)) for k in ('t','e','s','v','i','a')))

    def test_native_propagation_source_contract(self):self.assertEqual([],self.errors())

    def test_only_original_claimant_can_seed_once(self):
        for guard in ('this = scope:rw_service_client','var:rw_case_kind = flag:allegation','NOT = { has_variable = rw_ru_seeded }'):
            with self.subTest(guard=guard):self.assertIn('source claimant kind or once guard bypassed',self.errors(t=self.t.replace(guard,'always = yes',1)))

    def test_foreign_reader_and_stale_view_fail_closed(self):
        self.assertIn('private packet knowledge bypassed',self.errors(t=self.t.replace('story_owner = $READER$','always = yes')))
        for guard in ('var:rw_ru_packet_serial = scope:rw_ru_packet_serial','var:rw_ru_origin_serial = scope:rw_ru_origin_serial','var:rw_ru_sender = scope:rw_ru_sender','var:rw_ru_hops = scope:rw_ru_hops'):
            with self.subTest(guard=guard):self.assertIn('stale or substituted personal account',self.errors(t=self.t.replace(guard,'always = yes',1)))

    def test_lineage_and_original_speaker_cannot_be_laundered(self):
        for guard in ('var:rw_ru_issued_on = scope:rw_ru_issued_on','var:rw_ru_speaker = scope:rw_ru_speaker','var:rw_ru_origin_serial = scope:rw_ru_origin_serial'):
            with self.subTest(guard=guard):
                body=block(self.t,'rw_ru_relayable_trigger');self.assertIn('unowned expired or laundered lineage relayed',self.errors(t=self.t.replace(body,body.replace(guard,'always = yes'))))
        self.assertIn('receiver source relay date or hop provenance changed',self.errors(e=self.e.replace('name = rw_ru_sender value = scope:rw_ru_holder','name = rw_ru_sender value = scope:rw_ru_speaker')))

    def test_a_b_c_a_echo_and_already_informed_receivers_rejected(self):
        self.assertIn('known receiver self loop or range bypassed',self.errors(t=self.t.replace('NOT = { any_in_list = { variable = rw_ru_holders this = scope:rw_ru_receiver } }','always = yes',1)))
        self.assertIn('unowned expired or laundered lineage relayed',self.errors(t=self.t.replace('any_in_list = { variable = rw_ru_holders this = scope:rw_ru_holder }','always = yes',1)))

    def test_range_cooldown_death_and_ttl_are_fresh_guards(self):
        self.assertIn('known receiver self loop or range bypassed',self.errors(t=self.t.replace('in_diplomatic_range = scope:rw_ru_receiver','always = yes')))
        for guard in ('NOT = { has_character_flag = rw_ru_relay_cooldown }','scope:rw_ru_subject = { is_alive = yes }','has_variable = rw_ru_origin_retained'):
            with self.subTest(guard=guard):self.assertIn('unowned expired or laundered lineage relayed',self.errors(t=self.t.replace(guard,'always = yes',1)))
        self.assertIn('lineage lifetime renewed by relay',self.errors(e=self.e+'\nrw_bad = { set_variable = { name = rw_ru_origin_retained value = flag:yes days = 365 } }'))

    def test_effects_cannot_skip_send_or_creation_guard(self):
        for guard in ('rw_ru_can_seed_trigger','rw_ru_can_send_trigger','rw_ru_can_create_packet_trigger'):
            with self.subTest(guard=guard):self.assertIn('direct effect bypass',self.errors(e=self.e.replace('limit = { '+guard+' = yes }','limit = { always = yes }',1)))

    def test_no_source_reply_financial_terms_or_native_truth_exported(self):
        body=block(self.e,'rw_ru_create_packet_effect')
        for extra in ('set_variable = { name = rw_case_evidence value = flag:admitted }','set_variable = { name = rw_ru_case value = scope:rw_case_record }'):
            with self.subTest(extra=extra):self.assertIn('private source case or truth exported',self.errors(e=self.e.replace(body,body+'\n'+extra)))
        for extra in ('add_secret = {}','imprison = {}','add_opinion = {}','create_character_memory = {}','is_ai = yes','every_living_character = {}'):
            with self.subTest(extra=extra):self.assertIn('truth native sanction or global policy mutation',self.errors(e=self.e+'\nrw_bad = { '+extra+' }'))

    def test_knowledge_registered_and_sender_cooled_before_notification(self):
        self.assertIn('notification before knowledge dedup or cooldown',self.errors(e=self.e.replace('add_to_variable_list = { name = rw_ru_holders target = scope:rw_ru_receiver }','')))
        self.assertIn('notification before knowledge dedup or cooldown',self.errors(e=self.e.replace('flag = rw_ru_relay_cooldown days = 30','flag = rw_ru_relay_cooldown days = 0')))

    def test_custody_can_only_move_to_already_informed_live_holder(self):
        for guard in ('NOT = { this = scope:rw_ru_departed }','var:rw_ru_origin = scope:rw_ru_origin'):
            with self.subTest(guard=guard):
                body=block(self.e,'rw_ru_origin_owner_died_effect');self.assertIn('custody grants uninformed party knowledge',self.errors(e=self.e.replace(body,body.replace(guard,'always = yes'))))
        self.assertIn('personal packet inherited',self.errors(s=self.s.replace('on_owner_death = { end_story = yes }','on_owner_death = { rw_ru_origin_owner_died_effect = yes }')))

    def test_archive_is_personal_and_does_not_refresh_origin(self):
        self.assertNotIn('var:rw_ru_origin',block(self.t,'rw_ru_reader_trigger'))
        self.assertNotIn('rw_case_record',block(self.e,'rw_ru_read_effect'))
        self.assertNotIn('rw_case_record',block(self.e,'rw_ru_snapshot_effect'))
        self.assertIn('read renews knowledge or clocks',self.errors(e=self.e.replace('rw_ru_snapshot_effect = {','rw_ru_snapshot_effect = { set_variable = { name = rw_ru_origin_retained value = 1 }',1)))
        self.assertIn('name = rw_ru_heard_on value = current_date',block(self.e,'rw_ru_create_packet_effect'))

    def test_en_fr_refs_preserve_unverified_speaker_relay_and_no_case_link(self):
        keys=set(re.findall(r'\b(?:title|desc|name)\s*=\s*(rw_[\w.]+)',self.v+self.i))
        keys.update(('rw_rumor.prepare','rw_relay_rumor_interaction','rw_review_my_rumors_interaction'))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_rumor_l_{lang}.yml';self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig');self.assertEqual(keys,set(re.findall(r'^\s+([\w.]+):0',text,re.M)))
            for name in ('rw_ru_speaker','rw_ru_sender','rw_ru_subject','rw_ru_receiver'):self.assertIn('['+name+'.GetTitledFirstName]',text)
            self.assertNotIn('[rw_case_record',text)
            self.assertIn('rw_ru_hops',text)
