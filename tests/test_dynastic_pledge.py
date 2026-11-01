"""Adversarial CK3 source contracts; no simulation of succession or native debt."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'


def pledge_errors(t,e,s,v,i):
    out=[]
    record=block(t,'rw_dp_record_trigger')
    for g in ('story_type = story_rw_dynastic_pledge','var:rw_dp_schema = 1',
              'var:rw_dp_kind = flag:legacy_endowment','var:rw_dp_amount = 50',
              'exists = var:rw_dp_original_payer','exists = var:rw_dp_original_payee',
              'exists = var:rw_dp_payer_house','exists = var:rw_dp_payee_house',
              'NOT = { var:rw_dp_payer_house = var:rw_dp_payee_house }'):
        if g not in record:out.append('untyped foreign or malformed pact admitted')
    reader=block(t,'rw_dp_reader_trigger')
    for g in ('rw_dp_record_trigger = yes','has_variable = rw_dp_cap','has_variable = rw_dp_retained',
              '$READER$ = { is_alive = yes }','var:rw_dp_original_payer = $READER$',
              'var:rw_dp_original_payee = $READER$','var:rw_dp_paid_by = $READER$',
              'var:rw_dp_paid_to = $READER$', 'house_head = $READER$'):
        if g not in reader:out.append('private reader or retention bypassed')
    if re.search(r'\b(story_owner|any_house_member|top_liege)\b',reader):out.append('custody or kinship grants private access')
    view=block(t,'rw_dp_view_trigger')
    for g in ('this = scope:rw_dp_viewer','var:rw_dp_serial = scope:rw_dp_serial',
              'var:rw_dp_revision = scope:rw_dp_revision',
              'var:rw_dp_original_payer = scope:rw_dp_original_payer',
              'var:rw_dp_original_payee = scope:rw_dp_original_payee',
              'house_head = scope:rw_dp_payer','house_head = scope:rw_dp_payee',
              'var:rw_dp_paid_by = scope:rw_dp_paid_payer','var:rw_dp_paid_to = scope:rw_dp_paid_payee'):
        if g not in view:out.append('stale foreign or substituted identity')
    roles=block(t,'rw_dp_roles_trigger')
    for g in ('rw_dp_view_trigger = yes','house_head = scope:rw_dp_payer','house_head = scope:rw_dp_payee',
              'house = scope:rw_dp_record.var:rw_dp_payer_house','house = scope:rw_dp_record.var:rw_dp_payee_house'):
        if g not in roles:out.append('current house representative substituted')
    offer=block(t,'rw_dp_can_offer_trigger')
    for g in ('rw_dp_party_trigger = yes','NOT = { has_character_flag = rw_dp_offer_cooldown }',
              'NOT = { scope:actor.house = scope:recipient.house }','variable = rw_dynastic_pledges',
              'var:rw_dp_payer_house = scope:actor.house','var:rw_dp_payee_house = scope:recipient.house'):
        if g not in offer:out.append('offer bypasses headship pair dedup or cooldown')
    begin=block(e,'rw_dp_begin_effect')
    for g in ('limit = { rw_dp_can_offer_trigger = yes }','clear_saved_scope = rw_dp_record',
              'story_owner = scope:actor','NOT = { has_variable = rw_dp_schema }',
              'name = rw_dp_original_payer value = scope:actor','name = rw_dp_original_payee value = scope:recipient',
              'name = rw_dp_payer_house value = scope:actor.house','name = rw_dp_payee_house value = scope:recipient.house',
              'name = rw_dp_offer_window value = flag:yes days = 7',
              'name = rw_dp_cap value = flag:yes days = 10957',
              'add_to_global_variable_list = { name = rw_dynastic_pledges target = scope:rw_dp_record }'):
        if g not in begin:out.append('fresh construction facts or bounded index missing')
    acceptance=block(t,'rw_dp_can_accept_trigger')
    for g in ('rw_dp_roles_trigger = yes','this = scope:rw_dp_payee','has_variable = rw_dp_offer_window',
              'var:rw_dp_original_payer = scope:rw_dp_payer','var:rw_dp_original_payee = scope:rw_dp_payee'):
        if g not in acceptance:out.append('pending consent inherited')
    recognize=block(t,'rw_dp_can_recognize_trigger')
    for g in ('rw_dp_active_trigger = yes','this = scope:rw_dp_payer','this = scope:rw_dp_payee',
              'NOT = { var:rw_dp_payer_recognized = scope:rw_dp_payer }',
              'NOT = { var:rw_dp_payee_recognized = scope:rw_dp_payee }'):
        if g not in recognize:out.append('personal recognition can replay or target another role')
    paygate=block(t,'rw_dp_can_pay_trigger')
    for g in ('rw_dp_active_trigger = yes','this = scope:rw_dp_payer','gold >= 50',
              'var:rw_dp_original_payer = { is_alive = no }',
              'NOT = { var:rw_dp_original_payer = scope:rw_dp_payer }',
              'var:rw_dp_payer_recognized = scope:rw_dp_payer',
              'var:rw_dp_payee_recognized = scope:rw_dp_payee'):
        if g not in paygate:out.append('death funds or explicit successor consent bypassed')
    for method in ('accept','recognize','pay','decline','renounce','release'):
        if 'limit = { rw_dp_can_'+method+'_trigger = yes }' not in block(e,'rw_dp_'+method+'_effect'):
            out.append('direct effect bypass')
    pay=block(e,'rw_dp_pay_effect')
    ordering=[pay.find(g) for g in ('limit = { rw_dp_can_pay_trigger = yes }','rw_dp_close_story_effect = { RESULT = paid }',
                                   'name = rw_dp_paid_by value = scope:rw_dp_payer','name = rw_dp_paid_to value = scope:rw_dp_payee',
                                   'scope:rw_dp_payer = { add_gold = -50 }','scope:rw_dp_payee = { add_gold = 50 }','rw_dp_notify_effect = yes')]
    if min(ordering)<0 or ordering!=sorted(ordering):out.append('payment before consent consumption or wrong personal purse')
    close=block(e,'rw_dp_close_story_effect')
    for g in ('var:rw_dp_state = flag:offered var:rw_dp_state = flag:active',
              'remove_variable = rw_dp_offer_window','remove_variable = rw_dp_due',
              'change_variable = { name = rw_dp_revision add = 1 }',
              'name = rw_dp_retained value = flag:yes days = 1825'):
        if g not in close:out.append('terminal replay or archive lifetime extended')
    if e.count('name = rw_dp_due value = flag:yes days = 9125')!=1 or e.count('name = rw_dp_cap value = flag:yes days = 10957')!=1:
        out.append('fixed deadline or absolute cap renewed')
    for method,house in (('renounce','payer'),('release','payee')):
        exitgate=block(t,'rw_dp_can_'+method+'_trigger')
        if 'rw_dp_view_trigger = yes' not in exitgate or 'var:rw_dp_'+house+'_house = { house_head = scope:rw_dp_viewer }' not in exitgate:
            out.append('free exit wrong actor')
        if 'rw_dp_roles_trigger' in exitgate or 'rw_dp_active_trigger' in exitgate:
            out.append('free exit blocked by counterpart eligibility')
    owner=block(e,'rw_dp_owner_died_effect')
    if 'story_owner = { save_scope_as = rw_dp_departed }' not in owner or 'rw_dp_rehome_effect = yes' not in owner:
        out.append('owner death loses explicit custodian exclusion')
    custodian=block(t,'rw_dp_custodian_trigger')
    if 'NOT = { this = scope:rw_dp_departed }' not in custodian:out.append('owner death loses explicit custodian exclusion')
    for name in ('rw_dp_owner_died_effect','rw_dp_rehome_effect','rw_dp_maintenance_effect'):
        if re.search(r'\b(?:add_gold|name\s*=\s*rw_dp_(?:payer|payee)_recognized)\b',block(e,name)):
            out.append('storage or maintenance inherits consent or pays automatically')
    rehome=block(e,'rw_dp_rehome_effect')
    if 'random_house_member' in rehome or 'name = rw_dp_state' in rehome:out.append('storage grants authority or changes outcome')
    retire=block(e,'rw_dp_retire_effect')
    if retire.find('remove_list_global_variable')<0 or retire.find('remove_list_global_variable')>retire.find('end_story = yes'):
        out.append('retired story remains indexed')
    if 'on_owner_death = { rw_dp_owner_died_effect = yes }' not in s or 'days = 60' not in s:
        out.append('independent lifecycle missing')
    snapshot=block(e,'rw_dp_snapshot_effect')
    if re.search(r'\b(?:set_variable|add_gold|add_character_flag|trigger_event)\s*=',snapshot):out.append('read changes consent money or clocks')
    read=block(e,'rw_dp_read_effect')
    if 'rw_dp_reader_trigger = { READER = scope:rw_dp_reader }' not in read:out.append('private reader or retention bypassed')
    code=clean_script(t+e+s+v+i)[0]
    if len(re.findall(r'\badd_gold\s*=',code))!=2:out.append('extra money path')
    if re.search(r'\b(?:is_ai|imprison|death|change_title_holder|add_hook|add_prestige|add_opinion|create_character_memory|every_living_character|any_living_character|on_death|on_title_gain|consume_imprisonment_reasons)\s*=',code):
        out.append('native inheritance bank justice publicity or AI privilege changed')
    if 'ai_targets = { ai_recipients = liege }' not in i or 'ai_frequency = 12' not in i:
        out.append('unbounded AI initiation')
    return out


class DynasticPledgeTests(unittest.TestCase):
    def setUp(self):
        self.t=(MOD/'common/scripted_triggers/rw_dynastic_pledge_triggers.txt').read_text()
        self.e=(MOD/'common/scripted_effects/rw_dynastic_pledge_effects.txt').read_text()
        self.s=(MOD/'common/story_cycles/rw_dynastic_pledges.txt').read_text()
        self.v=(MOD/'events/rw_dynastic_pledge_events.txt').read_text()
        self.i=(MOD/'common/character_interactions/rw_dynastic_pledge_interactions.txt').read_text()

    def errors(self,**changes):return pledge_errors(*(changes.get(k,getattr(self,k)) for k in ('t','e','s','v','i')))

    def test_source_contract(self):self.assertEqual([],self.errors())

    def test_foreign_malformed_and_unretained_records_fail_closed(self):
        for guard in ('story_type = story_rw_dynastic_pledge','var:rw_dp_schema = 1','var:rw_dp_amount = 50'):
            with self.subTest(guard=guard):self.assertIn('untyped foreign or malformed pact admitted',self.errors(t=self.t.replace(guard,'always = yes',1)))
        for guard in ('has_variable = rw_dp_cap','has_variable = rw_dp_retained'):
            with self.subTest(guard=guard):self.assertIn('private reader or retention bypassed',self.errors(t=self.t.replace(guard,'always = yes',1)))

    def test_private_access_never_comes_from_storage_or_general_kinship(self):
        changed=self.t.replace('var:rw_dp_original_payer = $READER$','story_owner = $READER$')
        self.assertIn('custody or kinship grants private access',self.errors(t=changed))
        self.assertIn('private reader or retention bypassed',self.errors(t=self.t.replace('var:rw_dp_paid_by = $READER$','always = yes')))

    def test_old_revision_serial_origin_and_payment_parties_rejected(self):
        for guard in ('var:rw_dp_revision = scope:rw_dp_revision','var:rw_dp_serial = scope:rw_dp_serial',
                      'var:rw_dp_original_payer = scope:rw_dp_original_payer','house_head = scope:rw_dp_payer','var:rw_dp_paid_by = scope:rw_dp_paid_payer'):
            with self.subTest(guard=guard):self.assertIn('stale foreign or substituted identity',self.errors(t=self.t.replace(guard,'always = yes',1)))

    def test_successor_cannot_accept_original_pending_offer(self):
        for guard in ('var:rw_dp_original_payer = scope:rw_dp_payer','var:rw_dp_original_payee = scope:rw_dp_payee'):
            with self.subTest(guard=guard):self.assertIn('pending consent inherited',self.errors(t=self.t.replace(guard,'always = yes',1)))

    def test_new_heads_both_must_recognize_and_original_must_be_dead(self):
        for guard in ('var:rw_dp_original_payer = { is_alive = no }','var:rw_dp_payer_recognized = scope:rw_dp_payer','var:rw_dp_payee_recognized = scope:rw_dp_payee','gold >= 50'):
            with self.subTest(guard=guard):self.assertIn('death funds or explicit successor consent bypassed',self.errors(t=self.t.replace(guard,'always = yes')))

    def test_current_house_heads_and_membership_revalidated(self):
        for guard in ('house_head = scope:rw_dp_payer','house = scope:rw_dp_record.var:rw_dp_payee_house'):
            with self.subTest(guard=guard):self.assertIn('current house representative substituted',self.errors(t=self.t.replace(guard,'always = yes')))

    def test_all_public_effects_revalidate_before_mutating(self):
        for method in ('accept','recognize','pay','decline','renounce','release'):
            with self.subTest(method=method):self.assertIn('direct effect bypass',self.errors(e=self.e.replace('limit = { rw_dp_can_'+method+'_trigger = yes }','limit = { always = yes }',1)))

    def test_payment_consumes_once_and_uses_only_actual_personal_purses(self):
        for change in (self.e.replace('rw_dp_close_story_effect = { RESULT = paid }',''),self.e.replace('scope:rw_dp_payer = { add_gold = -50 }','scope:rw_dp_original_payer = { add_gold = -50 }'),self.e.replace('scope:rw_dp_payee = { add_gold = 50 }','scope:rw_dp_original_payee = { add_gold = 50 }')):
            self.assertIn('payment before consent consumption or wrong personal purse',self.errors(e=change))

    def test_recognition_and_reads_never_reset_accepted_deadline(self):
        self.assertIn('fixed deadline or absolute cap renewed',self.errors(e=self.e+'\nrw_bad = { set_variable = { name = rw_dp_due value = flag:yes days = 9125 } }'))
        self.assertIn('read changes consent money or clocks',self.errors(e=self.e.replace('rw_dp_snapshot_effect = {','rw_dp_snapshot_effect = { set_variable = { name = rw_dp_due value = 1 }',1)))

    def test_owner_death_excludes_departed_even_before_native_flags_settle(self):
        self.assertIn('owner death loses explicit custodian exclusion',self.errors(t=self.t.replace('NOT = { this = scope:rw_dp_departed }','always = yes')))
        self.assertIn('storage or maintenance inherits consent or pays automatically',self.errors(e=self.e.replace('rw_dp_owner_died_effect = {','rw_dp_owner_died_effect = { add_gold = -50',1)))

    def test_free_exits_do_not_require_healthy_or_consented_counterpart(self):
        self.assertIn('free exit blocked by counterpart eligibility',self.errors(t=self.t.replace('rw_dp_can_renounce_trigger = {','rw_dp_can_renounce_trigger = { rw_dp_roles_trigger = yes',1)))
        self.assertIn('free exit wrong actor',self.errors(t=self.t.replace('var:rw_dp_payer_house = { house_head = scope:rw_dp_viewer }','always = yes',1)))

    def test_index_retirement_and_bounded_ai_no_external_effects(self):
        self.assertIn('retired story remains indexed',self.errors(e=self.e.replace('remove_list_global_variable = { name = rw_dynastic_pledges target = scope:rw_dp_record }','')))
        for extra in ('is_ai = yes','create_character_memory = {}','change_title_holder = root','every_living_character = {}'):
            with self.subTest(extra=extra):self.assertIn('native inheritance bank justice publicity or AI privilege changed',self.errors(e=self.e+'\nrw_bad = { '+extra+' }'))

    def test_notice_coalescing_and_refresh_do_not_loop_or_renew(self):
        notice=block(self.e,'rw_dp_notify_effect')
        for marker,call in (('name = rw_dp_notified_payer','scope:rw_dp_payer = {\n                    save_scope_as = rw_dp_viewer'),('name = rw_dp_notified_payee','scope:rw_dp_payee = { save_scope_as = rw_dp_viewer trigger_event')):
            self.assertGreaterEqual(notice.find(marker),0);self.assertLess(notice.find(marker),notice.find(call))
        for method in ('rw_dp_read_effect','rw_dp_refresh_effect'):
            self.assertNotRegex(block(self.e,method),r'\b(set_variable|add_character_flag|add_gold)\s*=')
        self.assertIn('days = 1',block(self.e,'rw_dp_refresh_effect'))
        self.assertNotIn('rw_dp_pay_effect',self.s)

    def test_localization_privacy_and_actor_choice_guards(self):
        keys=set(re.findall(r'\b(?:title|desc|name)\s*=\s*(rw_[\w.]+)',self.v+self.i))
        keys.update(('rw_offer_dynastic_endowment_interaction','rw_review_dynastic_endowments_interaction'))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_dynastic_pledge_l_{lang}.yml';self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig');self.assertEqual(keys,set(re.findall(r'^\s+([\w.]+):0',text,re.M)))
            self.assertIn('[rw_dp_paid_payer.GetTitledFirstName]',text);self.assertIn('[rw_dp_original_payer.GetTitledFirstName]',text)
        for method in ('accept','decline','recognize','pay','renounce','release'):
            self.assertIn('trigger = { rw_dp_can_'+method+'_trigger = yes }',self.v)
        self.assertIn('name = rw_dynastic_pledge.leave ai_chance = { base = 50 }',self.v)
