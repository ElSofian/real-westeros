"""Reject the uninitialized first-declaration counters observed in CK3.

These inspect actual script, not a Python simulation of engine variables.
"""
import re
import unittest

from tools import build_g1_native_choice as builder
from tools.validate_mod import clean_script
from test_g1_royal_response import block


CASES = (
    ('rw_declaration_law_effects.txt', 'rw_dl_capture_effect', 'rw_dl_serial_counter'),
    ('rw_unlawful_war_response_effects.txt', 'rw_uw_notice_effect', 'rw_uw_serial_counter'),
)


def counter_errors(text, effect, counter):
    source = block(clean_script(text)[0], effect)
    name = re.escape(counter)
    initializer = (r'if\s*=\s*\{\s*limit\s*=\s*\{\s*NOT\s*=\s*\{\s*'
                   r'has_variable\s*=\s*' + name + r'\s*\}\s*\}\s*'
                   r'set_variable\s*=\s*\{\s*name\s*=\s*' + name +
                   r'\s+value\s*=\s*0\s*\}\s*\}')
    initializers = list(re.finditer(initializer, source))
    increments = list(re.finditer(r'change_variable\s*=\s*\{\s*name\s*=\s*' + name +
                                 r'\s+add\s*=\s*1\s*\}', source))
    writes = re.findall(r'(?:set|change)_variable\s*=\s*\{\s*name\s*=\s*' + name + r'\b', source)
    if len(initializers) != 1 or len(increments) != 1 or len(writes) != 2:
        return ['first use requires one missing-only initializer and one increment']
    if initializers[0].end() > increments[0].start():
        return ['initialization must precede increment']
    if source.index('create_story =') > initializers[0].start():
        return ['no counter write before receipt creation']
    # Both paths copy the incremented value into receipt/event identity next.
    if 'var:' + counter in source[:increments[0].end()]:
        return ['counter read before initialization and increment']
    return []


class FirstDeclarationCounterTests(unittest.TestCase):
    def sources(self):
        for filename, effect, counter in CASES:
            text = (builder.TEMPLATES / 'common/scripted_effects' / filename).read_text(encoding='utf-8-sig')
            yield text, effect, counter

    def test_both_production_paths_initialize_first_use_without_resetting_existing_serials(self):
        for text, effect, counter in self.sources():
            with self.subTest(counter=counter):
                self.assertEqual([], counter_errors(text, effect, counter))

    def test_observed_uninitialized_first_use_is_rejected(self):
        for text, effect, counter in self.sources():
            broken = text.replace('set_variable = { name = ' + counter + ' value = 0 }', '')
            with self.subTest(counter=counter):
                self.assertTrue(counter_errors(broken, effect, counter))

    def test_existing_serial_cannot_be_reset_on_each_new_war(self):
        for text, effect, counter in self.sources():
            broken = text.replace('NOT = { has_variable = ' + counter + ' }', 'always = yes')
            with self.subTest(counter=counter):
                self.assertTrue(counter_errors(broken, effect, counter))

    def test_initialize_after_increment_or_read_is_rejected(self):
        for text, effect, counter in self.sources():
            increment = 'change_variable = { name = ' + counter + ' add = 1 }'
            initialization = 'set_variable = { name = ' + counter + ' value = 0 }'
            for broken in (text.replace(increment, '').replace(initialization, increment + '\n' + initialization),
                           text.replace(initialization, 'save_scope_value_as = { name = bad value = var:' + counter + ' }\n' + initialization)):
                with self.subTest(counter=counter):
                    self.assertTrue(counter_errors(broken, effect, counter))


if __name__ == '__main__':
    unittest.main()
