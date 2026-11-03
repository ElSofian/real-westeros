"""Native-template and adapter contracts; no Python negotiation/game simulation."""
from pathlib import Path
import re
import unittest
from contract_source import contract_templates, expand_contracts, CALL, ARG
from test_native_scheme_evidence import block
from test_deferred_service_contract import block as nested_block
from test_allegation_settlement import settlement_errors
from test_charter_compensation import compensation_errors
from tools.validate_mod import clean_script

MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'
FAMILIES={
    'as':('rw_allegation_settlement','scope:rw_case_record','provider','client','50'),
    'cq':('rw_charter_compensation','scope:rw_lr_record','ruler','head','scope:rw_cq_start_price'),
}


def adapter_errors(t,e,prefix):
    stem,story,a,b,price=FAMILIES[prefix]
    expected={
        'quote':{'PREFIX':prefix,'TURN_A':a,'TURN_B':b},
        'snapshot':{'PREFIX':prefix},'offer':{'PREFIX':prefix,'PRICE':price},
        'counter':{'PREFIX':prefix,'TURN_A':a,'TURN_B':b},
        'consume':{'PREFIX':prefix},'close':{'PREFIX':prefix},
    }
    calls=[(name,dict(ARG.findall(args))) for name,args in CALL.findall(t+e)]
    wanted=[('rw_contract_'+kind+('_trigger' if kind=='quote' else '_effect'),args) for kind,args in expected.items()]
    errors=[]
    if len(calls)!=len(wanted) or any(calls.count(call)!=1 for call in wanted):
        errors.append('wrong binding duplicate or disconnected shared protocol')
    for name,guard,core in (('propose','can_propose','offer'),('counter','responder','counter'),
                             ('settle','can_settle','consume'),('close','can_close','close')):
        body=block(e,'rw_'+prefix+'_'+name+'_effect')
        if 'rw_'+prefix+'_'+guard+'_trigger = yes' not in nested_block(body,'limit'):
            errors.append('shared primitive bypasses domain authorization')
        if 'rw_contract_'+core+'_effect' not in nested_block(body,story):
            errors.append('contract mutates wrong storage scope')
    if 'rw_contract_quote_trigger' not in nested_block(block(t,'rw_'+prefix+'_view_trigger'),story):
        errors.append('quote reads wrong storage scope')
    return errors


class SharedContractModelTests(unittest.TestCase):
    def setUp(self):
        self.templates=contract_templates()
        self.raw={p:tuple((MOD/f'common/{folder}/{stem}_{suffix}.txt').read_text()
                           for folder,suffix in (('scripted_triggers','triggers'),('scripted_effects','effects')))
                  for p,(stem,*_) in FAMILIES.items()}

    def legacy_errors(self,prefix,templates=None,raw=None):
        t,e=self.raw[prefix] if raw is None else raw
        fn=settlement_errors if prefix=='as' else compensation_errors
        return fn(expand_contracts(t,templates),expand_contracts(e,templates))

    def test_both_systems_use_all_six_shared_primitives_with_exact_bindings(self):
        self.assertEqual(6,len(self.templates))
        for p,(t,e) in self.raw.items():
            self.assertEqual([],adapter_errors(t,e,p))
            self.assertEqual([],self.legacy_errors(p))

    def test_cross_system_prefix_cannot_reinterpret_terms(self):
        for p,(t,e) in self.raw.items():
            wrong='cq' if p=='as' else 'as'
            self.assertIn('wrong binding duplicate or disconnected shared protocol',adapter_errors(t.replace('PREFIX = '+p,'PREFIX = '+wrong),e,p))

    def test_wrong_turn_flags_price_or_missing_call_are_detected(self):
        for p,(t,e) in self.raw.items():
            a=FAMILIES[p][2]
            for changed_t,changed_e in ((t.replace('TURN_A = '+a,'TURN_A = stranger'),e),
                                        (t,e.replace('rw_contract_consume_effect = { PREFIX = '+p+' }','')),
                                        (t,e.replace('PRICE = '+FAMILIES[p][4],'PRICE = 100'))):
                self.assertIn('wrong binding duplicate or disconnected shared protocol',adapter_errors(changed_t,changed_e,p))

    def test_domain_authorization_and_correct_story_are_mandatory(self):
        for p,(t,e) in self.raw.items():
            self.assertIn('shared primitive bypasses domain authorization',adapter_errors(t,e.replace('rw_'+p+'_can_settle_trigger = yes','always = yes'),p))
            self.assertIn('contract mutates wrong storage scope',adapter_errors(t,e.replace(FAMILIES[p][1]+' = {','scope:wrong_record = {'),p))

    def test_shared_quote_revision_or_price_loss_breaks_both_existing_contracts(self):
        for needle in ('var:rw_$PREFIX$_revision = scope:rw_$PREFIX$_revision','var:rw_$PREFIX$_price = scope:rw_$PREFIX$_price'):
            changed=self.templates|{'rw_contract_quote_trigger':self.templates['rw_contract_quote_trigger'].replace(needle,'always = yes')}
            for p in FAMILIES:self.assertTrue(self.legacy_errors(p,changed))

    def test_shared_counter_without_revision_invalidates_both_source_contracts(self):
        name='rw_contract_counter_effect'
        changed=self.templates|{name:self.templates[name].replace('change_variable = { name = rw_$PREFIX$_revision add = 1 }','')}
        for p in FAMILIES:self.assertTrue(self.legacy_errors(p,changed))

    def test_shared_consume_cannot_omit_receipt_or_leave_offer_replayable(self):
        name='rw_contract_consume_effect'
        for needle in ('remove_variable = rw_$PREFIX$_window','set_variable = { name = rw_$PREFIX$_state value = flag:paid }'):
            changed=self.templates|{name:self.templates[name].replace(needle,'')}
            for p in FAMILIES:self.assertTrue(self.legacy_errors(p,changed))

    def test_snapshot_only_captures_existing_names_and_never_renews(self):
        body=self.templates['rw_contract_snapshot_effect']
        self.assertNotRegex(body,r'\b(?:set_variable|change_variable|remove_variable|trigger_event)\s*=')
        for p in FAMILIES:
            expanded=expand_contracts('rw_contract_snapshot_effect = { PREFIX = '+p+' }')
            self.assertIn('name = rw_'+p+'_revision value = var:rw_'+p+'_revision',expanded)
            self.assertIn('name = rw_'+p+'_price value = var:rw_'+p+'_price',expanded)

    def test_only_new_offer_sets_one_seven_day_clock(self):
        for name,body in self.templates.items():
            if name=='rw_contract_offer_effect':self.assertEqual(1,body.count('days = 7'))
            else:self.assertNotRegex(body,r'\b(?:days|months|years)\s*=')
        for p in FAMILIES:
            _,effects=(expand_contracts(s) for s in self.raw[p])
            for name in ('counter','prepare','snapshot','notify','settle','close'):
                self.assertNotIn('name = rw_'+p+'_window value =',block(effects,'rw_'+p+'_'+name+'_effect'))

    def test_no_new_serialized_schema_or_cross_system_state(self):
        for p in FAMILIES:
            expanded='\n'.join(expand_contracts(s) for s in self.raw[p])
            self.assertNotRegex(expanded,r'\$(?:PREFIX|TURN_A|TURN_B)\$')
            other='cq' if p=='as' else 'as'
            self.assertNotIn('rw_'+other+'_',expanded)
            self.assertIn('name = rw_'+p+'_schema value = 1',expanded)
            self.assertIn('name = rw_'+p+'_paid_revision value = scope:rw_'+p+'_revision',expanded)

    def test_core_has_no_domain_lookup_native_effect_or_player_ai_privilege(self):
        code='\n'.join(self.templates.values())
        self.assertNotRegex(code,r'\b(?:add_gold|add_prestige|add_opinion|run_interaction|create_story|end_story|is_ai|any_\w+|every_\w+|trigger_event)\s*=')
        self.assertNotRegex(code,r'\brw_(?:case|ch|lr|house|ru|evidence)_')
        fields=re.findall(r'\bname\s*=\s*(\S+)',code)
        self.assertTrue(all(f.startswith('rw_$PREFIX$_') for f in fields))

    def test_unknown_missing_duplicate_extra_or_nonliteral_arguments_fail_closed(self):
        for call in ('rw_contract_missing_effect = { PREFIX = as }',
                     'rw_contract_offer_effect = { PREFIX = as }',
                     'rw_contract_close_effect = { PREFIX = as EXTRA = bad }',
                     'rw_contract_close_effect = { PREFIX = as PREFIX = cq }',
                     'rw_contract_close_effect = { PREFIX = { hidden = yes } }'):
            with self.subTest(call=call),self.assertRaises(ValueError):expand_contracts(call)
