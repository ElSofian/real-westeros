"""Native byte preservation and actual CK3 receipt guards, no war simulation."""
from pathlib import Path
import re
import unittest
from tools import build_g1_native_choice as b
from tools.validate_mod import clean_script
from test_g1_royal_response import block

ROOT = b.TEMPLATES
T = ROOT/'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt'
E = ROOT/'common/scripted_effects/rw_war_lifecycle_effects.txt'
S = ROOT/'common/story_cycles/rw_unlawful_war_responses.txt'
FIXTURE = '''claim_cb = {
    on_declaration = { original_declaration = yes }
    on_invalidated = { }
    on_victory = { original_success = "é" }
    # on_defeat = { text in comment is not a block }
    on_defeat = { original_loss = yes }
    on_white_peace = { original_peace = yes }
    other_setting = yes
}
other_cb = { untouched = yes }
'''


def errors(t, e, s):
    found = []
    def need(text, tokens, label):
        if any(x not in text for x in tokens): found.append(label)
    retained = block(t, 'rw_uw_exact_war_present_trigger')
    need(retained, ('story_type = story_rw_unlawful_war_response', 'var:rw_uw_schema = 1',
         'story_owner = var:rw_uw_attacker', 'this = scope:rw_wc_check.var:rw_uw_war'), 'retention identity')
    for x in ('using_cb', 'primary_attacker', 'primary_defender', 'rw_uw_live',
              'rw_uw_state', 'rw_uw_issuer', 'rw_uw_active_record_trigger'):
        if x in retained: found.append('action-dependent retention')
    context = block(t, 'rw_uw_record_context_trigger')
    need(context, ('rw_uw_active_record_trigger = yes',
         'holder = scope:rw_wc_check.var:rw_uw_issuer'), 'live context')
    if context.count('liege = scope:rw_wc_check.var:rw_uw_issuer') != 2: found.append('jurisdiction')
    worker_definition = e[e.index('\nrw_uw_close_owned_receipts_effect = {'):]
    terminal = block(e, 'rw_uw_terminal_effect') + block(worker_definition, 'rw_uw_close_owned_receipts_effect')
    need(terminal, ('exists = scope:war', 'exists = scope:attacker',
         'story_owner = scope:rw_wc_actor', 'var:rw_uw_attacker = scope:rw_wc_actor',
         'var:rw_uw_schema = 1', 'has_variable = rw_uw_serial',
         'var:rw_uw_war = scope:rw_wc_war', 'NOT = { has_variable = rw_uw_terminal_seen }',
         'name = rw_uw_terminal_seen value = flag:yes',
         'name = rw_uw_terminal_kind value = flag:$OUTCOME$',
         'name = rw_uw_terminal_seen_on value = current_date'), 'callback identity/replay')
    # Existing action result must be changed only inside the not-already-closed branch.
    match = re.search(r'if\s*=\s*\{\s*limit\s*=\s*\{\s*NOT\s*=\s*\{\s*var:rw_uw_state\s*=\s*flag:closed\s*\}\s*\}\s*set_variable\s*=\s*\{\s*name\s*=\s*rw_uw_state\s+value\s*=\s*flag:closed\s*\}\s*set_variable\s*=\s*\{\s*name\s*=\s*rw_uw_result\s+value\s*=\s*flag:war_callback_closed\s*\}\s*\}', terminal)
    if not match: found.append('previous result overwritten')
    for name in ('rw_uw_live', 'rw_uw_issuer_window', 'rw_uw_answer_window'):
        need(terminal, ('remove_variable = '+name,), 'remaining action window')
    need(s, ('trigger = { NOT = { rw_uw_exact_war_present_trigger = yes } }',
         'NOT = { rw_uw_record_context_trigger = yes }', 'flag:context_lost',
         'NOT = { var:rw_uw_state = flag:closed }'), 'cleanup versus permission')
    native = r'\b(start_war|end_war|run_interaction|add_gold|add_opinion|change_title_holder|use_hook|trigger_event|make_story_owner)\s*='
    if re.search(native, clean_script(e+s)[0]): found.append('native mutation/redispatch')
    if re.search(r'save_(?:temporary_)?scope_as\s*=\s*(war|attacker|defender|actor|recipient|target)\b', terminal): found.append('native aliases overwritten')
    return found


class WarReceiptLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.t = T.read_text(); self.e = E.read_text(); self.s = S.read_text()

    def test_current_source_contract(self):
        self.assertEqual([], errors(self.t, self.e, self.s))
        self.assertIn('common/scripted_effects/rw_war_lifecycle_effects.txt', b.FILES)

    def test_terminal_visits_callback_attacker_and_other_exact_war_participants(self):
        terminal = block(self.e, 'rw_uw_terminal_effect')
        self.assertIn('rw_uw_close_owned_receipts_effect = { OUTCOME = $OUTCOME$ }',
                      block(terminal, 'scope:attacker'))
        self.assertIn('scope:war = { every_war_participant = {', ' '.join(terminal.split()))
        participants = block(terminal, 'every_war_participant')
        self.assertIn('limit = { NOT = { this = scope:attacker } }', participants)
        self.assertIn('rw_uw_close_owned_receipts_effect = { OUTCOME = $OUTCOME$ }', participants)
        self.assertEqual(2, terminal.count('rw_uw_close_owned_receipts_effect ='))
        for restricted_role in ('primary_attacker', 'primary_defender', 'liege', 'using_cb'):
            self.assertNotIn(restricted_role, participants)
        for global_scan in ('every_living_character', 'every_ruler', 'every_character'):
            self.assertNotIn(global_scan, terminal)

    def test_receipt_worker_requires_original_owner_and_exact_war_on_either_side(self):
        worker_definition = self.e[self.e.index('\nrw_uw_close_owned_receipts_effect = {'):]
        worker = block(worker_definition, 'rw_uw_close_owned_receipts_effect')
        self.assertIn('save_scope_as = rw_wc_actor', worker)
        self.assertIn('story_owner = scope:rw_wc_actor', worker)
        self.assertIn('var:rw_uw_attacker = scope:rw_wc_actor', worker)
        self.assertIn('var:rw_uw_war = scope:rw_wc_war', worker)
        self.assertNotIn('var:rw_uw_attacker = scope:attacker', worker)
        for operation in ('create_story', 'make_story_owner', 'run_interaction', 'end_war'):
            self.assertNotIn(operation, worker)

    def test_all_terminal_bodies_and_law_prefix_preserve_native_bytes(self):
        for newline in ('\n', '\r\n'):
            original, law = b.patch_claim_law(b'\xef\xbb\xbf'+FIXTURE.replace('\n', newline).encode())
            old, patched = b.patch_claim_lifecycle(law)
            restored = patched
            for name, prefix in b.TERMINAL_PREFIXES.items():
                self.assertEqual(1, patched.count(prefix.encode()))
                restored = restored.replace(prefix.encode(), b'', 1)
                current = block(patched.decode(), name)
                self.assertLess(current.index('rw_uw_terminal_effect'), current.index('original_') if 'original_' in current else len(current))
            self.assertEqual(old, restored)
            self.assertEqual(original, restored.replace(b.LAW_PREFIX.encode(), b'', 1))
            self.assertNotIn(b'other_cb', patched)
            self.assertIn(b'other_setting = yes', patched)

    def test_missing_or_duplicate_terminal_callback_refused(self):
        for name in b.TERMINAL_CALLBACKS:
            for changed in (FIXTURE.replace(name+' =', name+'_removed ='),
                            FIXTURE.replace('other_setting = yes', name+' = {}')):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    b.patch_claim_lifecycle(changed.encode())

    def test_already_patched_or_unbalanced_claim_refused(self):
        _, patched = b.patch_claim_lifecycle(FIXTURE.encode())
        for raw in (patched, FIXTURE[:-15].encode()):
            with self.assertRaises(ValueError): b.patch_claim_lifecycle(raw)

    def test_other_war_owner_schema_and_replayed_callback_rejected(self):
        for old, new in [('var:rw_uw_war = scope:rw_wc_war', 'has_variable = rw_uw_war'),
                         ('story_owner = scope:rw_wc_actor', 'always = yes'),
                         ('var:rw_uw_schema = 1', 'var:rw_uw_schema = 2'),
                         ('NOT = { has_variable = rw_uw_terminal_seen }', 'always = yes')]:
            with self.subTest(old=old): self.assertTrue(errors(self.t, self.e.replace(old,new), self.s))

    def test_role_cb_or_law_changes_cannot_delete_retained_war_receipt(self):
        for condition in ('using_cb = claim_cb', 'primary_attacker = scope:rw_wc_actor', 'has_variable = rw_uw_live'):
            changed = self.t.replace('rw_uw_exact_war_present_trigger = {', 'rw_uw_exact_war_present_trigger = { '+condition)
            with self.subTest(condition=condition): self.assertTrue(errors(changed,self.e,self.s))
        self.assertTrue(errors(self.t,self.e,self.s.replace('NOT = { rw_uw_exact_war_present_trigger = yes }', 'NOT = { rw_uw_active_record_trigger = yes }')))

    def test_closed_censure_or_native_dispatch_result_not_overwritten(self):
        self.assertTrue(errors(self.t,self.e.replace('NOT = { var:rw_uw_state = flag:closed }', 'always = yes'),self.s))
        self.assertNotIn('rw_uw_native_dispatched_on', self.e)
        self.assertNotIn('rw_dl_', self.e)

    def test_callback_clears_every_action_window_without_renewing(self):
        for name in ('rw_uw_live', 'rw_uw_issuer_window', 'rw_uw_answer_window'):
            with self.subTest(name=name): self.assertTrue(errors(self.t,self.e.replace('remove_variable = '+name,''),self.s))
        self.assertNotIn('days =',self.e)
        self.assertNotIn('create_story',self.e)
        self.assertNotIn('end_story',self.e)

    def test_stale_authority_is_closed_without_personal_consequence(self):
        self.assertTrue(errors(self.t.replace('holder = scope:rw_wc_check.var:rw_uw_issuer','always = yes'), self.e, self.s))
        self.assertIn('on_owner_death = { end_story = yes }', self.s)
        self.assertNotIn('every_living_character', self.t+self.e+self.s)

    def test_native_effects_and_alias_overwrites_are_rejected(self):
        for addition in ('end_war = white_peace', 'run_interaction = {}', 'add_gold = -50', 'save_scope_as = war'):
            with self.subTest(addition=addition): self.assertTrue(errors(self.t,self.e+'\n bad = { '+addition+' }',self.s) if 'save_scope' not in addition else errors(self.t,self.e.replace('save_scope_as = rw_wc_war',addition),self.s))


if __name__ == '__main__': unittest.main()
