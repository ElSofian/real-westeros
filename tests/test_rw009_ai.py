"""Source-contract checks, not simulation or execution of CK3's AI."""
from pathlib import Path
import unittest
from tools.validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1] / 'mod/real_westeros'
INTERACTION = ROOT / 'common/character_interactions/rw_reconciliation.txt'
TRIGGERS = ROOT / 'common/scripted_triggers/rw_reconciliation_triggers.txt'


def ai_contract_errors(interaction, triggers):
    """Detect removal of the documented bounded-selection/shared-gate contract."""
    interaction, _ = clean_script(interaction)
    triggers, _ = clean_script(triggers)
    import re
    errors = []
    if not re.search(r'ai_targets\s*=\s*\{\s*ai_recipients\s*=\s*liege\s*\}', interaction):
        errors.append('unbounded or changed target policy')
    if len(re.findall(r'rw_can_petition_trigger\s*=\s*yes', interaction + triggers)) != 2:
        errors.append('missing shared player/AI eligibility')
    for marker in ('rw_petition_cooldown', 'rw_petition_pending'):
        if not re.search(r'NOT\s*=\s*\{\s*has_character_flag\s*=\s*'+marker+r'\s*\}', triggers):
            errors.append('missing '+marker+' exclusion')
    return errors


class AiContractTests(unittest.TestCase):
    def setUp(self):
        self.interaction = INTERACTION.read_text()
        self.triggers = TRIGGERS.read_text()

    def test_bounded_shared_contract(self):
        self.assertEqual([], ai_contract_errors(self.interaction, self.triggers))

    def test_global_target_mutation_is_rejected(self):
        self.assertTrue(ai_contract_errors(self.interaction.replace('ai_recipients = liege', 'ai_recipients = all'), self.triggers))

    def test_ai_eligibility_bypass_is_rejected(self):
        changed = self.interaction.replace('ai_potential = { scope:actor = { rw_can_petition_trigger = yes } }', 'ai_potential = { always = yes }')
        self.assertTrue(ai_contract_errors(changed, self.triggers))

    def test_missing_cooldown_is_rejected(self):
        changed = self.triggers.replace('NOT = { has_character_flag = rw_petition_cooldown }', '')
        self.assertTrue(ai_contract_errors(self.interaction, changed))

    def test_missing_pending_guard_is_rejected(self):
        changed = self.triggers.replace('NOT = { has_character_flag = rw_petition_pending }', '')
        self.assertTrue(ai_contract_errors(self.interaction, changed))
