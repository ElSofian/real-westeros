"""AI entry-scope regression checks, not native planner or gameplay simulation."""
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from tools.validate_mod import ai_availability_errors, clean_script, validate
from tools.build_g1_native_choice import bounds, top_definition

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'mod/real_westeros'
CASES=(
 ('rw_reconciliation.txt','rw_seek_reconciliation_interaction','rw_can_petition_trigger = yes'),
 ('rw_service_interactions.txt','rw_offer_endorsement_interaction','rw_service_provider_available_trigger = yes'),
 ('rw_service_interactions.txt','rw_offer_deferred_endorsement_interaction','rw_service_provider_available_trigger = yes'),
 ('rw_favor_service_interactions.txt','rw_offer_favor_endorsement_interaction','rw_service_provider_available_trigger = yes is_imprisoned = no'),
 ('rw_favor_service_interactions.txt','rw_offer_deferred_favor_endorsement_interaction','rw_service_provider_available_trigger = yes is_imprisoned = no'),
 ('rw_allegation_interactions.txt','rw_raise_affront_allegation_interaction','NOT = { has_character_flag = rw_allegation_cooldown }'),
 ('rw_military_restraint_interactions.txt','rw_offer_military_restraint_interaction','rw_service_party_eligible_trigger = yes is_imprisoned = no NOT = { has_character_flag = rw_mr_cooldown }'),
 ('rw_dynastic_pledge_interactions.txt','rw_offer_dynastic_endowment_interaction','rw_dp_party_trigger = yes NOT = { has_character_flag = rw_dp_offer_cooldown }'),
 ('rw_rumor_interactions.txt','rw_relay_rumor_interaction','rw_ru_party_trigger = yes NOT = { has_character_flag = rw_ru_relay_cooldown }'),
)


class AiAvailabilityScopeTests(unittest.TestCase):
    def test_nine_filters_keep_their_conditions_on_current_character(self):
        self.assertEqual(9,len(CASES))
        for filename,name,expected in CASES:
            with self.subTest(interaction=name):
                text=top_definition((MOD/'common/character_interactions'/filename).read_bytes(),name)
                _,opening,end=bounds(text,'ai_potential')
                body=clean_script(text[opening+1:end-1])[0]
                self.assertEqual(re.sub(r'\s+','',expected),re.sub(r'\s+','',body))
                self.assertIn('ai_targets = { ai_recipients = liege }',text)
                self.assertIn('ai_frequency = 12',text)
                self.assertIn('is_valid_showing_failures_only =',text)
                self.assertIn('on_accept =',text)
                self.assertEqual([],ai_availability_errors(text))
                # Reintroduce the old wrapper: the ordinary validator must reject it.
                bad=text[:opening+1]+' scope:actor = {'+body+' } '+text[end-1:]
                self.assertTrue(ai_availability_errors(bad))

    def test_implicit_character_helpers_need_no_actor_or_recipient_alias(self):
        helpers={
          'rw_reconciliation_triggers.txt':('rw_can_petition_trigger',),
          'rw_service_triggers.txt':('rw_service_provider_available_trigger','rw_service_party_eligible_trigger'),
          'rw_dynastic_pledge_triggers.txt':('rw_dp_party_trigger',),
          'rw_rumor_triggers.txt':('rw_ru_party_trigger',),
        }
        for filename,names in helpers.items():
            text=(MOD/'common/scripted_triggers'/filename).read_text()
            for name in names:
                with self.subTest(helper=name):
                    start,_,end=bounds(text,name)
                    self.assertNotRegex(clean_script(text[start:end])[0],r'\bscope:(?:actor|recipient)\b')

    def test_known_actor_and_recipient_wrappers_rejected_with_location(self):
        for alias in ('actor','recipient'):
            out=ai_availability_errors('\n owned = {\n ai_potential = { scope:'+alias+' = { is_adult = yes } }\n }')
            self.assertEqual(1,len(out));self.assertTrue(out[0].startswith('line 3:'))
            self.assertIn('scope:'+alias,out[0])

    def test_comments_and_strings_are_not_fields(self):
        self.assertEqual([],ai_availability_errors('''
            # ai_potential = { scope:actor = { is_adult = yes } }
            debug_log = "ai_potential = { scope:recipient = { } }"
            ai_potential = { is_adult = yes }
        '''))

    def test_normal_selected_interaction_context_is_preserved(self):
        self.assertEqual([],ai_availability_errors('''
            is_shown = { scope:actor = { is_landed = yes } }
            is_valid_showing_failures_only = { scope:recipient = { is_adult = yes } }
            on_accept = { scope:actor = { owned_effect = yes } }
            ai_will_do = { base = 5 modifier = { factor = 2 scope:actor = { is_adult = yes } } }
        '''))

    def test_narrow_rule_does_not_claim_general_saved_scope_resolution(self):
        self.assertEqual([],ai_availability_errors('''
            ai_potential = { save_temporary_scope_as = actor scope:actor = { is_adult = yes } }
        '''))

    def test_integrated_validator_rejects_old_shape_and_accepts_rooted_guard(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(ROOT/'mod',root/'mod')
            p=root/'mod/real_westeros/common/character_interactions/rw_ai_scope_fixture.txt'
            p.write_text('rw_ai_scope_fixture = { ai_potential = { scope:actor = { is_adult = yes } } }\n')
            self.assertTrue(any('ai_potential starts with unbound scope:actor' in e for e in validate(root)))
            p.write_text('rw_ai_scope_fixture = { ai_potential = { is_adult = yes } }\n')
            self.assertEqual([],validate(root))


if __name__ == '__main__':unittest.main()
