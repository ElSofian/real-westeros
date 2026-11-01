"""Adversarial CK3-source contracts; no war simulation or compatibility proof."""
from pathlib import Path
import json
import re
import unittest
from test_native_scheme_evidence import block
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'mod/real_westeros'


def restraint_errors(t, e, hook, story):
    errors = []
    def need(body, fragments, message):
        if any(x not in body for x in fragments): errors.append(message)
    need(block(t, 'rw_mr_view_trigger'), ('exists = scope:rw_mr_record',
        'exists = scope:rw_mr_provider', 'exists = scope:rw_mr_beneficiary', 'exists = scope:rw_mr_serial',
        'OR = { this = scope:rw_mr_provider this = scope:rw_mr_beneficiary }',
        'story_type = story_rw_military_restraint', 'var:rw_mr_schema = 1', 'has_variable = rw_mr_retained',
        'story_owner = scope:rw_mr_provider', 'var:rw_mr_provider = scope:rw_mr_provider',
        'var:rw_mr_beneficiary = scope:rw_mr_beneficiary', 'var:rw_mr_serial = scope:rw_mr_serial',
        'has_variable = rw_mr_accepted_on', 'has_variable = rw_mr_finished_on',
        'has_variable = rw_mr_observed_on', 'var:rw_mr_observed_on = var:rw_mr_finished_on'),
        'foreign private story or incomplete observation')
    need(block(t, 'rw_mr_can_accept_trigger'), ('rw_mr_view_trigger = yes',
        'this = scope:rw_mr_beneficiary', 'var:rw_mr_state = flag:offered', 'has_variable = rw_mr_offer_window'),
        'wrong actor expired or replayed acceptance')
    if block(t, 'rw_mr_can_accept_trigger').count('rw_service_party_eligible_trigger = yes') != 2:
        errors.append('wrong actor expired or replayed acceptance')
    need(block(t, 'rw_mr_active_trigger'), ('rw_mr_view_trigger = yes', 'var:rw_mr_state = flag:active',
        'has_variable = rw_mr_accepted_on', 'has_variable = rw_mr_due'), 'expired or terminal pledge actionable')
    need(block(t, 'rw_mr_native_context_trigger'), ('exists = scope:war', 'exists = scope:attacker',
        'exists = scope:defender', 'NOT = { scope:attacker = scope:defender }',
        'this = scope:war.primary_attacker', 'this = scope:war.primary_defender'),
        'missing secondary or reversed native roles observed')
    need(block(t, 'rw_mr_observable_trigger'), ('rw_mr_native_context_trigger = yes',
        'story_type = story_rw_military_restraint', 'story_owner = scope:attacker', 'var:rw_mr_schema = 1',
        'var:rw_mr_provider = scope:attacker', 'var:rw_mr_beneficiary = scope:defender',
        'var:rw_mr_state = flag:active', 'has_variable = rw_mr_serial', 'has_variable = rw_mr_accepted_on',
        'has_variable = rw_mr_due', 'has_variable = rw_mr_retained'),
        'wrong pledge owner parties or time observed')
    begin = block(e, 'rw_mr_begin_effect')
    need(begin, ('limit = { rw_mr_can_offer_trigger = yes }',
        'change_variable = { name = rw_mr_serial_counter add = 1 }',
        'create_story = { type = story_rw_military_restraint save_scope_as = rw_mr_record }',
        'NOT = { has_variable = rw_mr_schema }',
        'name = rw_mr_provider value = scope:actor', 'name = rw_mr_beneficiary value = scope:recipient',
        'name = rw_mr_serial value = scope:rw_mr_serial', 'name = rw_mr_offer_window value = flag:yes days = 7',
        'name = rw_mr_retained value = flag:yes days = 1825', 'flag = rw_mr_cooldown days = 365'),
        'offer identity or fixed clocks missing')
    accept = block(e, 'rw_mr_accept_effect')
    need(accept, ('limit = { rw_mr_can_accept_trigger = yes }', 'remove_variable = rw_mr_offer_window',
        'name = rw_mr_accepted_on value = current_date', 'name = rw_mr_due value = flag:yes days = 90',
        'name = rw_mr_state value = flag:active'), 'consent not consumed before active duty')
    if accept.find('name = rw_mr_state value = flag:active') > accept.find('rw_mr_notify_effect = yes'):
        errors.append('consent not consumed before active duty')
    observe = block(e, 'rw_mr_observe_effect')
    need(observe, ('limit = { rw_mr_native_context_trigger = yes this = scope:attacker }',
        'every_owned_story = {', 'limit = { rw_mr_observable_trigger = yes }',
        'rw_mr_snapshot_effect = yes', 'remove_variable = rw_mr_due',
        'name = rw_mr_observed_on value = current_date', 'name = rw_mr_finished_on value = current_date',
        'name = rw_mr_state value = flag:war_observed'), 'unguarded callback or repeat notice')
    if not 0 <= observe.find('remove_variable = rw_mr_due') < observe.find('name = rw_mr_state value = flag:war_observed') < observe.find('rw_mr_notify_effect = yes'):
        errors.append('unguarded callback or repeat notice')
    entry = block(hook, 'on_war_started').strip()
    if entry != 'on_actions = { rw_on_military_restraint_war_started }':
        errors.append('native war entry overwritten')
    need(block(hook, 'rw_on_military_restraint_war_started'), ('trigger = { rw_mr_native_context_trigger = yes }',
        'effect = { scope:attacker = { rw_mr_observe_effect = yes } }'), 'unscoped callback intake')
    need(story, ('on_owner_death = { end_story = yes }', 'name = rw_mr_state value = flag:elapsed',
        'NOT = { has_variable = rw_mr_retained }'), 'inherited duty or no neutral retention cleanup')
    code = clean_script(e+hook+story)[0]
    if re.search(r'\b(add_gold|add_prestige|add_opinion|add_hook|remove_hook|add_secret|add_claim|add_truce|declare_war|start_war|end_war|run_interaction|make_story_owner|change_title_holder|every_living_character|every_in_global_list)\s*=', code):
        errors.append('native coercion inheritance or world scan')
    if re.search(r'\bname\s*=\s*rw_(?:service|fv|case|as)_', code):
        errors.append('unrelated contract state overwritten')
    return errors


class MilitaryRestraintTests(unittest.TestCase):
    def setUp(self):
        self.t = (MOD/'common/scripted_triggers/rw_military_restraint_triggers.txt').read_text()
        self.e = (MOD/'common/scripted_effects/rw_military_restraint_effects.txt').read_text()
        self.hook = (MOD/'common/on_action/rw_military_restraint_on_actions.txt').read_text()
        self.story = (MOD/'common/story_cycles/rw_military_restraint.txt').read_text()
        self.ev = (MOD/'events/rw_military_restraint_events.txt').read_text()
        self.i = (MOD/'common/character_interactions/rw_military_restraint_interactions.txt').read_text()

    def errors(self, t=None, e=None, hook=None, story=None):
        return restraint_errors(self.t if t is None else t, self.e if e is None else e,
            self.hook if hook is None else hook, self.story if story is None else story)

    def test_source_contract(self): self.assertEqual([], self.errors())

    def test_exact_private_record_owner_parties_serial_and_observation_dates(self):
        for g in ('exists = scope:rw_mr_record', 'story_owner = scope:rw_mr_provider',
                  'var:rw_mr_provider = scope:rw_mr_provider', 'var:rw_mr_beneficiary = scope:rw_mr_beneficiary',
                  'var:rw_mr_serial = scope:rw_mr_serial', 'has_variable = rw_mr_retained',
                  'var:rw_mr_observed_on = var:rw_mr_finished_on'):
            self.assertIn('foreign private story or incomplete observation', self.errors(t=self.t.replace(g, 'always = yes')))

    def test_guarded_creation_monotonic_identity_and_no_old_quote_fields(self):
        for g in ('limit = { rw_mr_can_offer_trigger = yes }', 'name = rw_mr_provider value = scope:actor',
                  'name = rw_mr_beneficiary value = scope:recipient', 'change_variable = { name = rw_mr_serial_counter add = 1 }'):
            self.assertIn('offer identity or fixed clocks missing', self.errors(e=self.e.replace(g, 'removed')))
        self.assertIn('unrelated contract state overwritten', self.errors(e=self.e+'\nset_variable = { name = rw_service_serial value = 0 }'))

    def test_only_original_beneficiary_may_accept_live_eligible_offer(self):
        for g in ('rw_mr_view_trigger = yes', 'this = scope:rw_mr_beneficiary',
                  'has_variable = rw_mr_offer_window', 'rw_service_party_eligible_trigger = yes'):
            self.assertIn('wrong actor expired or replayed acceptance', self.errors(t=self.t.replace(g, 'always = yes')))

    def test_acceptance_consumes_offer_and_fixes_ninety_days_before_notices(self):
        for g in ('remove_variable = rw_mr_offer_window', 'name = rw_mr_accepted_on value = current_date',
                  'name = rw_mr_due value = flag:yes days = 90'):
            self.assertIn('consent not consumed before active duty', self.errors(e=self.e.replace(g, 'removed')))
        self.assertNotIn('rw_mr_due', block(self.e, 'rw_mr_begin_effect'))

    def test_reading_and_exits_never_renew_offer_duty_retention_or_cooldown(self):
        for field in ('rw_mr_offer_window', 'rw_mr_due', 'rw_mr_retained'):
            self.assertEqual(1, len(re.findall(r'\bname\s*=\s*'+field+r'\b', self.e)))
        for name in ('rw_mr_read_effect', 'rw_mr_renounce_effect', 'rw_mr_release_effect', 'rw_mr_notify_effect'):
            self.assertNotRegex(block(self.e, name), r'\b(?:days|months|years)\s*=')

    def test_native_callback_requires_exact_primary_roles_and_complete_context(self):
        for g in ('exists = scope:war', 'exists = scope:attacker', 'exists = scope:defender',
                  'this = scope:war.primary_attacker', 'this = scope:war.primary_defender'):
            self.assertIn('missing secondary or reversed native roles observed', self.errors(t=self.t.replace(g, 'always = yes')))

    def test_only_current_attacker_owned_matching_accepted_live_record_is_observed(self):
        for g in ('story_owner = scope:attacker', 'var:rw_mr_provider = scope:attacker',
                  'var:rw_mr_beneficiary = scope:defender', 'has_variable = rw_mr_due',
                  'has_variable = rw_mr_accepted_on', 'var:rw_mr_state = flag:active'):
            self.assertIn('wrong pledge owner parties or time observed', self.errors(t=self.t.replace(g, 'always = yes')))
        self.assertNotIn('rw_service_party_eligible_trigger', block(self.t, 'rw_mr_observable_trigger'))
        self.assertNotIn('is_ai', block(self.t, 'rw_mr_observable_trigger'))

    def test_consumed_observation_precedes_once_only_private_notices(self):
        for g in ('limit = { rw_mr_native_context_trigger = yes this = scope:attacker }',
                  'limit = { rw_mr_observable_trigger = yes }', 'remove_variable = rw_mr_due',
                  'name = rw_mr_observed_on value = current_date'):
            self.assertIn('unguarded callback or repeat notice', self.errors(e=self.e.replace(g, 'removed')))
        self.assertEqual(1, self.e.count('name = rw_mr_state value = flag:war_observed'))

    def test_native_entry_is_additive_and_child_scopes_actual_attacker(self):
        self.assertIn('native war entry overwritten', self.errors(hook=self.hook.replace('on_war_started = {', 'on_war_started = { effect = {}')))
        self.assertIn('unscoped callback intake', self.errors(hook=self.hook.replace('scope:attacker =', 'scope:defender =')))
        self.assertNotIn('events =', block(self.hook, 'on_war_started'))
        self.assertNotIn('trigger =', block(self.hook, 'on_war_started'))

    def test_renounce_and_release_are_free_original_actor_choices_until_expiry(self):
        for name, actor, result in (('renounce', 'provider', 'renounced'), ('release', 'beneficiary', 'released')):
            gate = block(self.t, 'rw_mr_can_'+name+'_trigger')
            self.assertIn('rw_mr_active_trigger = yes', gate)
            self.assertIn('this = scope:rw_mr_'+actor, gate)
            b = block(self.e, 'rw_mr_'+name+'_effect')
            self.assertIn('limit = { rw_mr_can_'+name+'_trigger = yes }', b)
            self.assertIn('remove_variable = rw_mr_due', b)
            self.assertIn('value = flag:'+result, b)
            self.assertNotRegex(gate, r'\b(gold|is_imprisoned|rw_service_party_eligible_trigger)\b')
        self.assertIn('expired or terminal pledge actionable', self.errors(t=self.t.replace('has_variable = rw_mr_due', 'always = yes')))

    def test_no_native_cb_truce_war_penalty_or_inherited_promise(self):
        for cmd in ('add_truce', 'declare_war', 'end_war', 'add_opinion', 'add_gold', 'make_story_owner', 'every_living_character'):
            self.assertIn('native coercion inheritance or world scan', self.errors(e=self.e+'\n'+cmd+' = {}'))
        self.assertIn('inherited duty or no neutral retention cleanup', self.errors(story=self.story.replace('on_owner_death = { end_story = yes }', '')))

    def test_local_expiry_is_neutral_and_cannot_infer_fulfillment_or_guilt(self):
        code = clean_script(self.story)[0]
        self.assertIn('flag:elapsed', code)
        self.assertNotRegex(code, r'flag:(fulfilled|breached|guilty|war_observed)\b')
        self.assertNotRegex(code, r'\b(trigger_event|add_opinion|add_gold)\s*=')
        self.assertNotIn('rw_mr_observe_effect', self.story)
        self.assertIn('desc = rw_military_restraint.elapsed', self.ev)

    def test_archive_reads_only_selected_owner_known_records_without_truncation(self):
        b = block(self.e, 'rw_mr_read_effect')
        self.assertIn('scope:recipient = {', b)
        self.assertIn('limit = { rw_mr_reader_trigger = { READER = scope:rw_mr_reader } }', b)
        self.assertNotRegex(b, r'\b(?:random_owned_story|set_variable|rw_mr_accept_effect|rw_mr_begin_effect)\s*=')
        reader = block(self.t, 'rw_mr_reader_trigger')
        self.assertIn('story_owner = var:rw_mr_provider', reader)
        self.assertIn('var:rw_mr_provider = $READER$ var:rw_mr_beneficiary = $READER$', reader)

    def test_ai_uses_bounded_liege_initiation_and_identical_execution(self):
        self.assertIn('ai_targets = { ai_recipients = liege }', self.i)
        self.assertIn('ai_frequency = 12', self.i)
        self.assertNotRegex(clean_script(self.t+self.e+self.i+self.ev)[0], r'\bis_ai\s*=')
        self.assertIn('NOT = { has_character_flag = rw_mr_cooldown }', block(self.t, 'rw_mr_can_offer_trigger'))
        for action in ('accept', 'close', 'renounce', 'release'):
            self.assertIn('rw_mr_'+action+'_effect = yes', self.ev)
            self.assertIn('rw_mr_can_'+action+'_trigger = yes', self.ev)

    def test_hash_only_receipt_is_source_evidence_not_runtime_or_reproduced_assets(self):
        receipt = json.loads((ROOT/'docs/MILITARY_RESTRAINT_SOURCE_RECEIPT.json').read_text())
        self.assertEqual(2, len(receipt['reviewed_references']))
        self.assertIn('not_engine_evidence', receipt['kind'])
        for row in receipt['reviewed_references']:
            self.assertRegex(row['sha256'], r'^[a-f0-9]{64}$')
            self.assertGreater(row['size'], 0)
            self.assertTrue(row['markers']['on_war_started = {'])
            self.assertFalse(Path(row['path']).is_absolute())
        self.assertIn('G1 remains unresolved', str(receipt['limits']))

    def test_localized_all_ui_keys_and_explicit_inference_limits(self):
        keys = set(re.findall(r'(?:title|desc|name)\s*=\s*(rw_military_restraint\.[\w.]+)', self.ev))
        keys.update(('rw_offer_military_restraint_interaction', 'rw_offer_military_restraint_interaction_desc',
                     'rw_review_military_restraint_interaction', 'rw_review_military_restraint_interaction_desc'))
        for lang in ('english', 'french'):
            p = MOD/f'localization/{lang}/rw_military_restraint_l_{lang}.yml'
            self.assertTrue(p.read_bytes().startswith(b'\xef\xbb\xbf'))
            actual = set(re.findall(r'^\s+([\w.]+):0', p.read_text(encoding='utf-8-sig'), re.M))
            self.assertTrue(keys <= actual, keys-actual)
