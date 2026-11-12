"""Institutional contribution source contracts and adversarial mutations."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
MOD=Path(__file__).resolve().parents[1]/'mod/real_westeros'
CASES=(('house','rw_house_terms_effects.txt','rw_house_terms_triggers.txt','rw_house_terms_valid_trigger','rw_house_terms_price','scope:rw_house_record.var:rw_house_terms_price','rw_house_accept_terms_effect','rw_house_terms_affordable_trigger'),
       ('legacy','rw_dynastic_pledge_effects.txt','rw_dynastic_pledge_triggers.txt','rw_dp_record_trigger','rw_dp_amount','scope:rw_dp_record.var:rw_dp_amount','rw_dp_pay_effect','rw_dp_can_pay_trigger'))

def institutional_errors(values,sources):
    errors=[]
    for token in ('value = 50','tier_empire } value = 400','tier_kingdom } value = 200','tier_duchy } value = 100'):
        if not re.search(re.escape(token)+r'(?![\w.])',values):errors.append('wrong contribution tier')
    for kind,ef,tf,valid,field,price,pay,gate in CASES:
        effects,triggers=sources[ef],sources[tf]
        amount_guard=block(block(triggers,valid),'OR')
        amounts={int(n) for n in re.findall(r'var:'+field+r'\s*=\s*(\d+)\b',amount_guard)}
        if amounts!={50,100,200,400} or 'always =' in amount_guard:errors.append('invalid or legacy amount accepted')
        if 'gold >= '+price not in block(triggers,gate):errors.append('wrong affordability amount')
        payout=block(effects,pay)
        if 'remove_short_term_gold = '+price not in payout or 'add_gold = '+price not in payout:
            errors.append('payment differs from accepted amount')
        if 'rw_institutional_payment_value' in payout:errors.append('payment reprices an accepted contribution')
        if kind=='house':
            offer=block(effects,'rw_house_offer_terms_effect')
            payer=block(offer,'scope:rw_house_record.var:rw_house_petitioner')
            if 'name = rw_house_terms_offer_price value = rw_institutional_payment_value' not in payer:
                errors.append('house quote uses wrong payer or unfrozen amount')
            for token in ('scope:rw_house_record.var:rw_house_petitioner = {','name = rw_house_terms_offer_price value = rw_institutional_payment_value','name = rw_house_terms_price value = scope:rw_house_terms_offer_price'):
                if token not in offer:errors.append('house quote uses wrong payer or unfrozen amount')
        else:
            offer=block(effects,'rw_dp_begin_effect')
            for token in ('scope:actor = {','name = rw_dp_offer_amount value = rw_institutional_payment_value','name = rw_dp_amount value = scope:rw_dp_offer_amount'):
                if token not in offer:errors.append('legacy quote uses wrong payer or unfrozen amount')
    return errors

class InstitutionalCostTests(unittest.TestCase):
    def setUp(self):
        self.values=(MOD/'common/script_values/rw_institutional_payment_values.txt').read_text()
        self.sources={}
        for _,ef,tf,*_ in CASES:
            self.sources[ef]=(MOD/'common/scripted_effects'/ef).read_text()
            self.sources[tf]=(MOD/'common/scripted_triggers'/tf).read_text()
    def errors(self,sources=None,values=None):
        return institutional_errors(self.values if values is None else values,self.sources if sources is None else sources)
    def test_actual_tiers_and_both_frozen_contributions(self):self.assertEqual([],self.errors())
    def test_invalid_zero_or_unsupported_amount_is_rejected(self):
        for _,_,tf,_,field,*_ in CASES:
            for number in [0,75,500]:
                changed=dict(self.sources);changed[tf]=changed[tf].replace('var:'+field+' = 50','var:'+field+' = '+str(number),1)
                self.assertIn('invalid or legacy amount accepted',self.errors(changed))
    def test_old_fifty_gold_records_still_match_the_same_validity_gate(self):
        for _,_,tf,valid,field,*_ in CASES:
            self.assertIn('var:'+field+' = 50',block(self.sources[tf],valid))
    def test_affordability_uses_the_stored_price_instead_of_fifty(self):
        for _,_,tf,_,_,price,_,_ in CASES:
            changed=dict(self.sources);changed[tf]=changed[tf].replace('gold >= '+price,'gold >= 50')
            self.assertIn('wrong affordability amount',self.errors(changed))
    def test_debit_and_credit_must_use_the_same_immutable_amount(self):
        for _,ef,_,_,_,price,*_ in CASES:
            for operation in ['remove_short_term_gold','add_gold']:
                changed=dict(self.sources);changed[ef]=changed[ef].replace(operation+' = '+price,operation+' = 50')
                self.assertIn('payment differs from accepted amount',self.errors(changed))
    def test_payment_or_successor_recognition_cannot_reprice_the_offer(self):
        for kind,ef,_,_,field,price,pay,_ in CASES:
            changed=dict(self.sources);changed[ef]=changed[ef].replace('remove_short_term_gold = '+price,'remove_short_term_gold = rw_institutional_payment_value')
            self.assertIn('payment reprices an accepted contribution',self.errors(changed))
            if kind=='legacy':self.assertNotIn('name = '+field,block(self.sources[ef],'rw_dp_recognize_effect'))
    def test_quote_constructors_freeze_the_original_payer_tier(self):
        changed=dict(self.sources);file='rw_house_terms_effects.txt';changed[file]=changed[file].replace('scope:rw_house_record.var:rw_house_petitioner = {','scope:rw_house_terms_payee = {',1)
        self.assertIn('house quote uses wrong payer or unfrozen amount',self.errors(changed))
        self.assertIn('wrong contribution tier',self.errors(values=self.values.replace('value = 400','value = 4000')))
    def test_all_four_prices_are_shown_before_acceptance_in_both_languages(self):
        for stem,record,field in [('rw_house_terms','rw_house_record','rw_house_terms_price'),('rw_dynastic_pledge','rw_dp_record','rw_dp_amount')]:
            file='rw_house_terms_events.txt' if stem=='rw_house_terms' else 'rw_dynastic_pledge_events.txt'
            event=(MOD/'events'/file).read_text()
            for amount in [50,100,200,400]:
                self.assertIn('scope:'+record+' = { var:'+field+' = '+str(amount)+' }',event)
                self.assertIn('desc = rw_institutional.amount_'+str(amount),event)
                for language in ['english','french']:
                    text=(MOD/f'localization/{language}/rw_institutional_payments_l_{language}.yml').read_text(encoding='utf-8-sig')
                    self.assertIn('rw_institutional.amount_'+str(amount)+':0',text)
if __name__=='__main__':unittest.main()
