"""Adversarial original-source contracts, not an engine/title-transfer simulation."""
from pathlib import Path
import re
import unittest
from test_deferred_service_contract import block
from tools.validate_mod import clean_script

MOD = Path(__file__).resolve().parents[1]/'mod/real_westeros'


def pledge_errors(t, e, v):
    out = []
    view = block(t, 'rw_rp_view_trigger')
    for g in ('rw_rs_view_trigger = yes', 'exists = scope:rw_rp_revision', 'exists = scope:rw_rp_days',
              'var:rw_rp_schema = 1', 'has_variable = rw_rp_proposed_on', 'has_variable = rw_rp_accepted_on',
              'var:rw_rp_revision = scope:rw_rp_revision', 'var:rw_rp_days = scope:rw_rp_days'):
        if g not in view: out.append('stale or unrelated pledge view')
    proposal = block(t, 'rw_rp_can_propose_trigger')
    for g in ('rw_rs_view_trigger = yes', 'this = scope:rw_rs_holder', 'var:rw_rs_state = flag:talks',
              'has_variable = rw_rs_window', 'rw_rs_current_context_trigger = yes',
              'NOT = { has_variable = rw_rp_schema }'):
        if g not in proposal: out.append('pledge without current holder discussion or duplicate proposal')
    offer = block(t, 'rw_rp_offer_live_trigger')
    for g in ('rw_rp_view_trigger = yes', 'var:rw_rp_state = flag:offered', 'has_variable = rw_rp_offer_window',
              'has_variable = rw_rs_window', 'var:rw_rs_state = flag:talks', 'rw_rs_current_context_trigger = yes'):
        if g not in offer: out.append('expired or inapplicable offer accepted')
    turn = block(t, 'rw_rp_responder_trigger')
    for g in ('rw_rp_offer_live_trigger = yes', 'this = scope:rw_rs_requester', 'var:rw_rp_turn = flag:requester',
              'this = scope:rw_rs_holder', 'var:rw_rp_turn = flag:holder'):
        if g not in turn: out.append('unilateral or wrong-party acceptance')
    actions = {'propose':'can_propose', 'counter':'can_counter', 'accept':'responder',
               'close_offer':'can_close_offer', 'renounce':'can_renounce', 'release':'can_release',
               'acknowledge':'can_acknowledge', 'resent':'can_react', 'accept_renunciation':'can_react'}
    for effect, gate in actions.items():
        if f'limit = {{ rw_rp_{gate}_trigger = yes }}' not in block(e, f'rw_rp_{effect}_effect'):
            out.append('unguarded pledge effect')
    proposed = block(e, 'rw_rp_propose_effect')
    if e.count('name = rw_rp_offer_window') != 1 or 'name = rw_rp_offer_window value = flag:yes days = 7' not in proposed:
        out.append('offer clock reset')
    counter = block(e, 'rw_rp_counter_effect')
    for g in ('change_variable = { name = rw_rp_revision add = 1 }', 'name = rw_rp_days value = 14',
              'name = rw_rp_days value = 30', 'name = rw_rp_turn value = flag:holder',
              'name = rw_rp_turn value = flag:requester', 'rw_rp_snapshot_effect = yes'):
        if g not in counter: out.append('counter leaves old consent live')
    if counter.count('id = rw_restitution_pledge.0001 days = 1') != 2:
        out.append('unbounded immediate AI counter loop')
    accept = block(e, 'rw_rp_accept_effect')
    points = [accept.find(s) for s in ('remove_variable = rw_rp_offer_window', 'name = rw_rp_accepted_on',
                                     'name = rw_rp_state value = flag:promised', 'id = rw_restitution_pledge.0002',
                                     'rw_rp_notify_effect = yes')]
    if min(points) < 0 or points != sorted(points): out.append('acceptance timer before consent consumption or after notice')
    for days in (14,30):
        if f'name = rw_rp_due value = flag:yes days = {days}' not in accept or f'id = rw_restitution_pledge.0002 days = {days+1}' not in accept:
            out.append('wrong accepted clock or timeout')
    if len(re.findall(r'\bname\s*=\s*rw_rp_due\b', e)) != 2:
        out.append('accepted deadline renewed outside consent')
    timeout = block(e, 'rw_rp_timeout_effect')
    for g in ('rw_rp_view_trigger = yes', 'this = scope:rw_rs_requester', 'var:rw_rp_state = flag:promised',
              'NOT = { has_variable = rw_rp_due }', 'name = rw_rp_state value = flag:unresolved'):
        if g not in timeout: out.append('early stale timeout or fabricated breach')
    ack = block(t, 'rw_rp_can_acknowledge_trigger')
    for g in ('rw_rp_view_trigger = yes', 'this = scope:rw_rs_requester', 'rw_rp_parties_trigger = yes',
              'has_variable = rw_rp_accepted_on', 'holder = scope:rw_rs_requester'):
        if g not in ack: out.append('false recipient confirmation')
    grant = block(t, 'rw_rp_can_open_grant_trigger')
    for g in ('rw_rp_pending_trigger = yes', 'this = scope:rw_rs_holder', 'is_ai = no',
              'rw_rp_parties_trigger = yes', 'holder = scope:rw_rs_holder',
              'is_character_interaction_valid = { interaction = grant_titles_interaction recipient = scope:rw_rs_requester }'):
        if g not in grant: out.append('unsafe native window')
    if v.count('rw_rp_can_open_grant_trigger = yes') != 2 or 'open_interaction_window = { interaction = grant_titles_interaction actor = root recipient = scope:rw_rs_requester }' not in v:
        out.append('unsafe native window')
    reaction = block(t, 'rw_rp_can_react_trigger')
    for g in ('this = scope:rw_rs_requester', 'rw_rp_parties_trigger = yes', 'holder = scope:rw_rs_holder',
              'var:rw_rp_state = flag:renounced', 'has_variable = rw_rp_response_window',
              'NOT = { has_variable = rw_rp_response_done }'):
        if g not in reaction: out.append('false or repeated renunciation penalty')
    resent = block(e, 'rw_rp_resent_effect')
    marks = [resent.find(s) for s in ('name = rw_rp_response_done', 'has_opinion_modifier', 'add_opinion')]
    if min(marks) < 0 or marks != sorted(marks): out.append('stacked renewed or replayed resentment')
    code = clean_script(e+v)[0]
    if re.search(r'\b(run_interaction|send_interaction|change_title_holder|create_title_and_vassal_change|resolve_title_and_vassal_change|add_gold|add_prestige|add_claim|add_hook|add_trait|make_story_owner|every_living_character|any_living_character)\s*=', code):
        out.append('forced native performance or world scan')
    return out


class RestitutionPledgeTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_restitution_pledge_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_restitution_pledge_effects.txt').read_text()
        self.v = (MOD/'events/rw_restitution_pledge_events.txt').read_text()

    def errors(self, t=None, e=None, v=None):
        return pledge_errors(self.t if t is None else t, self.e if e is None else e, self.v if v is None else v)

    def test_contract(self):
        self.assertEqual([], self.errors())

    def test_full_private_identity_and_current_clause_version_required(self):
        for guard in ('rw_rs_view_trigger = yes', 'exists = scope:rw_rp_revision', 'exists = scope:rw_rp_days',
                      'var:rw_rp_schema = 1', 'has_variable = rw_rp_accepted_on',
                      'var:rw_rp_revision = scope:rw_rp_revision', 'var:rw_rp_days = scope:rw_rp_days'):
            self.assertIn('stale or unrelated pledge view', self.errors(t=self.t.replace(guard, 'always = yes')))

    def test_proposal_requires_actual_holder_and_current_discussion_only_once(self):
        for guard in ('this = scope:rw_rs_holder', 'rw_rs_current_context_trigger = yes',
                      'var:rw_rs_state = flag:talks', 'NOT = { has_variable = rw_rp_schema }'):
            self.assertIn('pledge without current holder discussion or duplicate proposal', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertNotIn('name = rw_rp_due', block(self.e,'rw_rp_propose_effect'))

    def test_original_offer_and_discussion_deadlines_both_limit_acceptance(self):
        for guard in ('has_variable = rw_rp_offer_window', 'has_variable = rw_rs_window',
                      'rw_rs_current_context_trigger = yes', 'var:rw_rp_state = flag:offered'):
            self.assertIn('expired or inapplicable offer accepted', self.errors(t=self.t.replace(guard, 'always = yes')))
        self.assertIn('offer clock reset', self.errors(e=self.e+'\nset_variable = { name = rw_rp_offer_window value = flag:yes days = 7 }'))

    def test_acceptance_requires_responder_of_exact_current_offer(self):
        for guard in ('rw_rp_offer_live_trigger = yes', 'var:rw_rp_turn = flag:requester', 'var:rw_rp_turn = flag:holder'):
            self.assertIn('unilateral or wrong-party acceptance', self.errors(t=self.t.replace(guard, 'always = yes')))
        for gate in ('can_propose','can_counter','responder','can_close_offer','can_renounce',
                     'can_release','can_acknowledge','can_react'):
            altered=self.e.replace(f'limit = {{ rw_rp_{gate}_trigger = yes }}','limit = { always = yes }')
            self.assertNotEqual(self.e,altered)
            self.assertIn('unguarded pledge effect', self.errors(e=altered))

    def test_counter_versions_and_one_day_dispatch_without_clock_reset(self):
        for guard in ('change_variable = { name = rw_rp_revision add = 1 }', 'rw_rp_snapshot_effect = yes',
                      'name = rw_rp_turn value = flag:requester', 'name = rw_rp_days value = 14'):
            self.assertIn('counter leaves old consent live', self.errors(e=self.e.replace(guard, 'always = yes')))
        self.assertIn('unbounded immediate AI counter loop', self.errors(e=self.e.replace('id = rw_restitution_pledge.0001 days = 1','id = rw_restitution_pledge.0001')))
        c=block(self.e,'rw_rp_counter_effect')
        self.assertNotRegex(c,r'\bname\s*=\s*rw_rp_(offer_window|due|accepted_on|proposed_on)\b')

    def test_acceptance_consumes_before_fixed_timeout_and_notices(self):
        self.assertIn('acceptance timer before consent consumption or after notice',
                      self.errors(e=self.e.replace('remove_variable = rw_rp_offer_window','')))
        for days in (14,30):
            self.assertIn('wrong accepted clock or timeout',self.errors(e=self.e.replace(f'.0002 days = {days+1}',f'.0002 days = {days+2}')))
        self.assertIn('accepted deadline renewed outside consent', self.errors(e=self.e+'\nset_variable = { name = rw_rp_due value = flag:yes days = 30 }'))

    def test_early_or_old_timeout_cannot_close_another_promise_or_punish(self):
        for guard in ('rw_rp_view_trigger = yes','this = scope:rw_rs_requester',
                      'var:rw_rp_state = flag:promised','NOT = { has_variable = rw_rp_due }'):
            self.assertIn('early stale timeout or fabricated breach',self.errors(e=self.e.replace(guard,'always = yes')))
        b=block(self.e,'rw_rp_timeout_effect')
        self.assertNotIn('add_opinion',b)
        self.assertNotIn('flag:renounced',b)
        self.assertNotIn('flag:acknowledged',b)

    def test_personal_post_consent_parties_do_not_depend_on_later_house_head_or_source(self):
        parties=block(self.t,'rw_rp_parties_trigger')
        for guard in ('is_alive = yes','is_adult = yes','is_imprisoned = no','NOT = { is_at_war_with = scope:rw_rs_requester }',
                      'tier >= tier_county','is_noble_family_title = no','is_landless_type_title = no'):
            self.assertIn(guard,parties)
        for name in ('rw_rp_pending_trigger','rw_rp_can_acknowledge_trigger','rw_rp_can_release_trigger','rw_rp_can_open_grant_trigger'):
            b=block(self.t,name)
            self.assertNotRegex(b,r'\b(rw_rs_current_context_trigger|house_head|rw_lr_record_valid_trigger|rw_rs_window)\b')

    def test_acknowledgment_requires_original_beneficiary_and_actual_exact_ownership(self):
        for guard in ('this = scope:rw_rs_requester','rw_rp_parties_trigger = yes',
                      'has_variable = rw_rp_accepted_on','holder = scope:rw_rs_requester'):
            self.assertIn('false recipient confirmation', self.errors(t=self.t.replace(guard,'always = yes')))
        ack=block(self.e,'rw_rp_acknowledge_effect')
        self.assertIn('has_variable = rw_rp_due',ack)
        self.assertIn('flag:acknowledged_late',ack)
        self.assertLess(ack.index('remove_variable = rw_rp_due'),ack.index('rw_rp_notify_effect'))
        # No passive observer or callback can turn present ownership into performance.
        for name in ('rw_rp_maintenance_effect','rw_rp_timeout_effect','rw_rp_snapshot_effect'):
            self.assertNotIn('flag:acknowledged',block(self.e,name))
        self.assertNotRegex(ack,r'\b(add_gold|add_prestige|add_opinion|change_title_holder)\s*=')

    def test_renunciation_is_explicit_holder_statement_while_still_owning(self):
        b=block(self.t,'rw_rp_can_renounce_trigger')
        for guard in ('rw_rp_pending_trigger = yes','this = scope:rw_rs_holder','holder = scope:rw_rs_holder'):
            self.assertIn(guard,b)
        renounce=block(self.e,'rw_rp_renounce_effect')
        self.assertLess(renounce.index('remove_variable = rw_rp_due'),renounce.index('rw_rp_notify_effect'))
        self.assertNotIn('add_opinion',renounce)

    def test_identity_only_offer_close_and_beneficiary_release_do_not_trap_parties(self):
        for name in ('rw_rp_can_close_offer_trigger','rw_rp_can_release_trigger'):
            b=block(self.t,name)
            self.assertIn('rw_rp_view_trigger = yes',b)
            self.assertNotRegex(b,r'\b(rw_rp_parties_trigger|rw_rs_current_context_trigger|rw_rp_due|rw_rp_offer_window)\b')
        self.assertIn('this = scope:rw_rs_requester',block(self.t,'rw_rp_can_release_trigger'))
        for name in ('rw_rp_close_offer_effect','rw_rp_release_effect'):
            self.assertNotRegex(block(self.e,name),r'\b(add_opinion|add_gold|add_prestige)\s*=')

    def test_native_window_has_fresh_owner_capacity_and_validity_checks(self):
        for guard in ('rw_rp_pending_trigger = yes','this = scope:rw_rs_holder','is_ai = no',
                      'holder = scope:rw_rs_holder','is_character_interaction_valid = { interaction = grant_titles_interaction recipient = scope:rw_rs_requester }'):
            self.assertIn('unsafe native window',self.errors(t=self.t.replace(guard,'always = yes')))
        self.assertIn('unsafe native window',self.errors(v=self.v.replace('limit = { rw_rp_can_open_grant_trigger = yes }','limit = { always = yes }')))
        b=block(self.v,'open_interaction_window')
        self.assertNotRegex(b,r'\b(target|target_titles|send_options|auto_accept|force)\b')

    def test_optional_renunciation_response_once_nonstacking_and_no_refresh(self):
        for guard in ('var:rw_rp_state = flag:renounced','has_variable = rw_rp_response_window',
                      'NOT = { has_variable = rw_rp_response_done }','holder = scope:rw_rs_holder'):
            self.assertIn('false or repeated renunciation penalty',self.errors(t=self.t.replace(guard,'always = yes')))
        self.assertIn('stacked renewed or replayed resentment',self.errors(e=self.e.replace('has_opinion_modifier','has_character_flag')))
        self.assertEqual(1,self.e.count('name = rw_rp_response_window'))
        self.assertIn('name = rw_rp_response_window value = flag:yes days = 7',self.e)
        o=(MOD/'common/opinion_modifiers/rw_restitution_pledge_opinions.txt').read_text()
        self.assertRegex(o,r'opinion\s*=\s*-15\b')
        self.assertRegex(o,r'years\s*=\s*2\b')

    def test_closing_discussion_does_not_silently_release_or_renounce_accepted_promise(self):
        original=(MOD/'common/scripted_effects/rw_restitution_effects.txt').read_text()
        for name in ('rw_rs_refuse_effect','rw_rs_withdraw_effect'):
            self.assertNotIn('rw_rp_',block(original,name))
        t=(MOD/'common/scripted_triggers/rw_restitution_triggers.txt').read_text()
        self.assertIn('NOT = { has_variable = rw_rp_accepted_on }',block(t,'rw_rs_can_react_trigger'))
        v=(MOD/'events/rw_restitution_events.txt').read_text()
        self.assertIn('desc = rw_restitution_pledge.discussion_closed',v)

    def test_maintenance_reuses_private_cadence_and_compares_nested_holder_in_story_scope(self):
        original=(MOD/'common/scripted_effects/rw_restitution_effects.txt').read_text()
        b=block(original,'rw_rs_maintenance_effect')
        self.assertLess(b.index('rw_rp_maintenance_effect'),b.index('flag:expired'))
        maint=block(self.e,'rw_rp_maintenance_effect')
        self.assertIn('save_temporary_scope_as = rw_rp_check',maint)
        for party in ('requester','holder'):
            self.assertIn('holder = scope:rw_rp_check.var:rw_rs_'+party,maint)
            self.assertNotRegex(maint,rf'\bholder\s*=\s*var:rw_rs_{party}\b')
        self.assertNotRegex(maint,r'\b(trigger_event|add_opinion|add_gold|add_prestige)\s*=')
        self.assertIn('flag:invalidated',maint)

    def test_no_new_public_export_index_lifecycle_or_original_retention(self):
        self.assertNotRegex(clean_script(self.e)[0],r'\b(?:name|flag)\s*=\s*rw_rs_(?:window|retained|cooldown|state|serial|requester|holder|title)\b')
        self.assertNotRegex(clean_script(self.e)[0],r'\b(create_story|add_to_global_variable_list|make_story_owner|end_story)\s*=')
        public=(MOD/'common/scripted_effects/rw_land_register_effects.txt').read_text()
        self.assertNotIn('rw_rp_',public)
        story=(MOD/'common/story_cycles/rw_restitution_requests.txt').read_text()
        self.assertIn('on_owner_death = { rw_rs_retire_effect = yes }',story)
        self.assertIn('days = 60',story)

    def test_ai_and_player_share_all_gameplay_guards_with_bounded_offer_dispatch(self):
        code=clean_script(self.t)[0]
        self.assertEqual(1,len(re.findall(r'\bis_ai\s*=',code)))
        # The only human-only predicate belongs to a cosmetic native-window shortcut.
        self.assertIn('is_ai = no',block(self.t,'rw_rp_can_open_grant_trigger'))
        for effect in ('accept','counter','close_offer','acknowledge','renounce','release','resent','accept_renunciation'):
            self.assertIn(f'rw_rp_{effect}_effect = yes',self.v)
        initial=block(self.e,'rw_rp_propose_effect')
        self.assertIn('id = rw_restitution_pledge.0001 days = 1',initial)
        original=(MOD/'events/rw_restitution_events.txt').read_text()
        self.assertIn('rw_rp_propose_effect = yes',original)
        self.assertIn('has_trait = generous',original)
        self.assertIn('primary_title = scope:rw_rs_title',original)

    def test_no_native_transfer_payment_forced_ai_gift_or_world_scan(self):
        for command in ('change_title_holder = root','add_gold = 50','add_prestige = 50','run_interaction = grant_titles_interaction',
                        'every_living_character = { always = yes }'):
            self.assertIn('forced native performance or world scan',self.errors(e=self.e+'\n'+command))
        self.assertNotIn('on_title_gain',self.e+self.v)

    def test_localized_state_terms_and_personal_statement_boundaries(self):
        original=(MOD/'events/rw_restitution_events.txt').read_text()
        keys=set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_restitution_pledge\.[\w.]+)',self.v+original))
        keys.add('rw_restitution_renounced_opinion')
        for lang in ('english','french'):
            p=MOD/f'localization/{lang}/rw_restitution_pledge_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            text=p.read_text(encoding='utf-8-sig')
            self.assertTrue(keys<=set(re.findall(r'^\s+([\w.]+):0',text,re.M)))
            self.assertIn('rw_restitution_pledge.acknowledged_late:0',text)
            self.assertIn('rw_restitution_pledge.unresolved:0',text)
