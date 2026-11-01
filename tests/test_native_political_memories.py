"""Public-only native memory wiring; no simulation of CK3 memory UI or persistence."""
from pathlib import Path
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'
CALLS=(('rw_service_effects.txt','rw_service_settle_effect','rw_service_provider','rw_service_client'),
       ('rw_obligation_effects.txt','rw_service_fulfill_promise_effect','rw_service_provider','rw_service_client'),
       ('rw_favor_service_effects.txt','rw_fv_settle_effect','rw_fv_provider','rw_fv_client'),
       ('rw_deferred_favor_effects.txt','rw_fd_perform_effect','rw_fv_provider','rw_fv_client'))


def memory_errors(helper,types,sources):
    out=[]
    support=block(helper,'rw_pm_public_support_effect')
    for g in ('exists = $PROVIDER$','exists = $CLIENT$','NOT = { $PROVIDER$ = $CLIENT$ }',
              '$PROVIDER$ = { is_alive = yes }','$CLIENT$ = { is_alive = yes }'):
        if g not in support:out.append('wrong or missing public parties')
    for role,flag,kind,other in (('PROVIDER','given','given','CLIENT'),('CLIENT','received','received','PROVIDER')):
        match=re.search(re.escape('$'+role+'$')+r'\s*=\s*\{\s*if\s*=',support)
        owner=block('owner = '+support[support.index('{',match.start()):],'owner') if match else ''
        # Inspect each distinct creation under its named memory type and owner block.
        for g in ('has_character_flag = rw_pm_support_'+flag+'_recent','flag = rw_pm_support_'+flag+'_recent days = 365',
                  'type = rw_public_support_'+kind,'participants = { counterpart = $'+other+'$ }'):
            if g not in owner:out.append('wrong support owner participant or coalescing')
        if owner.find('add_character_flag')>owner.find('create_character_memory'):
            out.append('memory emitted before suppression consumed')
    crown=block(helper,'rw_pm_crown_recognition_effect')
    for g in ('rw_ch_active_trigger = yes','this = scope:rw_ch_ruler','has_variable = rw_ch_recognized_on',
              'var:rw_ch_recognized_on = current_date','var:rw_ch_recognized_by = scope:rw_ch_ruler',
              'NOT = { has_character_flag = rw_pm_crown_recognition_recent }',
              'flag = rw_pm_crown_recognition_recent days = 365',
              'type = rw_public_crown_recognition','participants = { counterpart = scope:rw_ch_head }'):
        if g not in crown:out.append('crown memory lacks fresh personal recognition or roles')
    if crown.find('add_character_flag')>crown.find('create_character_memory'):
        out.append('memory emitted before suppression consumed')
    for filename,name,provider,client in CALLS:
        effect=block(sources[filename],name)
        call='rw_pm_public_support_effect = { PROVIDER = scope:'+provider+' CLIENT = scope:'+client+' }'
        if sources[filename].count(call)!=1 or call not in effect:out.append('public performance call missing or elsewhere')
        if effect.find(call)<effect.find('add_prestige = 50'):out.append('memory precedes actual performance')
    charter=sources['rw_restitution_charter_effects.txt']
    assume=block(charter,'rw_ch_assume_effect')
    if charter.count('rw_pm_crown_recognition_effect = yes')!=1 or 'rw_pm_crown_recognition_effect = yes' not in assume:
        out.append('recognition memory emitted outside explicit recognition')
    elif assume.find('rw_pm_crown_recognition_effect = yes')<assume.find('name = rw_ch_recognized_on'):
        out.append('memory precedes explicit recognition')
    definitions=re.findall(r'(?m)^(rw_\w+)\s*=\s*\{',types)
    if set(definitions)!={'rw_public_support_given','rw_public_support_received','rw_public_crown_recognition'}:
        out.append('unrelated or missing public memory type')
    for name in definitions:
        t=block(types,name)
        if 'participants = { counterpart }' not in t or 'duration = { years = 5 }' not in t:
            out.append('native participants or retention wrong')
    code=clean_script(helper+types)[0]
    if len(re.findall(r'\bcreate_character_memory\s*=',code))!=3:out.append('extra memory path')
    if re.search(r'\b(?:set_variable|add_gold|add_prestige|add_opinion|create_story|trigger_event|run_interaction|imprison|is_ai|every_\w+)\s*=',code):
        out.append('memory changes gameplay privileges or introduces scan')
    if re.search(r'\b(?:rw_service_price|rw_fv_term|rw_case_evidence|rw_scheme_evidence_record|rw_lr_title)\b',code):
        out.append('private contract or case data exported')
    return out


class NativePoliticalMemoryTests(unittest.TestCase):
    def setUp(self):
        self.h=(MOD/'common/scripted_effects/rw_political_memory_effects.txt').read_text()
        self.t=(MOD/'common/character_memory_types/rw_political_memories.txt').read_text()
        self.s={f:(MOD/'common/scripted_effects'/f).read_text() for f in [r[0] for r in CALLS]+['rw_restitution_charter_effects.txt']}

    def errors(self,h=None,t=None,s=None):
        return memory_errors(h or self.h,t or self.t,s or self.s)

    def test_native_projection_contract(self):
        self.assertEqual([],self.errors())

    def test_original_live_distinct_parties_required(self):
        for guard in ('exists = $PROVIDER$','exists = $CLIENT$','NOT = { $PROVIDER$ = $CLIENT$ }',
                      '$PROVIDER$ = { is_alive = yes }','$CLIENT$ = { is_alive = yes }'):
            with self.subTest(guard=guard):
                self.assertIn('wrong or missing public parties',self.errors(h=self.h.replace(guard,'always = yes',1)))

    def test_counterpart_and_role_suppression_not_swapped(self):
        self.assertIn('wrong support owner participant or coalescing',self.errors(h=self.h.replace('counterpart = $CLIENT$','counterpart = $PROVIDER$',1)))
        self.assertIn('wrong support owner participant or coalescing',self.errors(h=self.h.replace('days = 365','days = 1',1)))

    def test_memories_follow_performance_in_all_four_paths(self):
        for filename,name,provider,client in CALLS:
            with self.subTest(filename=filename):
                sources=self.s.copy();call='rw_pm_public_support_effect = { PROVIDER = scope:'+provider+' CLIENT = scope:'+client+' }'
                sources[filename]=sources[filename].replace(call,'')
                sources[filename]=sources[filename].replace('        scope:'+client+' = { add_prestige = 50 }', '        '+call+'\n        scope:'+client+' = { add_prestige = 50 }')
                self.assertIn('memory precedes actual performance',self.errors(s=sources))

    def test_old_or_foreign_crown_statement_is_not_new_memory(self):
        for guard in ('rw_ch_active_trigger = yes','this = scope:rw_ch_ruler',
                      'var:rw_ch_recognized_on = current_date','var:rw_ch_recognized_by = scope:rw_ch_ruler'):
            with self.subTest(guard=guard):
                self.assertIn('crown memory lacks fresh personal recognition or roles',self.errors(h=self.h.replace(guard,'always = yes')))

    def test_passive_read_or_proposal_cannot_emit_memory(self):
        sources=self.s.copy();sources['rw_restitution_charter_effects.txt']=sources['rw_restitution_charter_effects.txt'].replace('rw_pm_crown_recognition_effect = yes','')+'\nrw_bad_read_effect = { rw_pm_crown_recognition_effect = yes }'
        self.assertIn('recognition memory emitted outside explicit recognition',self.errors(s=sources))
        self.assertIn('native participants or retention wrong',self.errors(t=self.t.replace('years = 5','years = 100')))

    def test_no_gameplay_effect_privilege_scan_or_private_terms(self):
        for extra in ('add_gold = 25','add_opinion = {}','is_ai = no','every_owned_story = {}','trigger_event = {}'):
            with self.subTest(extra=extra):
                self.assertIn('memory changes gameplay privileges or introduces scan',self.errors(h=self.h+'\nrw_bad = { '+extra+' }'))
        self.assertIn('private contract or case data exported',self.errors(h=self.h+'\nrw_bad = { value = rw_service_price }'))

    def test_three_perspectives_are_public_only_in_both_languages(self):
        keys=set(re.findall(r'\bdesc\s*=\s*(rw_memory\.[\w.]+)',self.t))
        self.assertEqual(9,len(keys))
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_political_memory_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig')
            self.assertEqual(keys,set(re.findall(r'^\s+([\w.]+):0',text,re.M)))
            self.assertIn('[counterpart.GetTitledFirstName]',text)
            self.assertIn('[owner.GetName]',text)
            self.assertNotRegex(text,r'\b(?:gold|hook|crime|complot|accusation|promise|or|faveur)\b')
