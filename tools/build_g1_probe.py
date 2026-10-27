#!/usr/bin/env python3
"""Build a PRIVATE, opt-in CK3 diagnostic from installed sources; not a simulation."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from validate_mod import brace_errors, clean_script

REPO = Path(__file__).resolve().parents[1]
HELPER = 'war_declarer_needs_hook_on_liege'
SOURCE = Path('common/scripted_triggers/00_war_and_peace_triggers.txt')
# This original guard is added to the installed helper, never a law/CB change.
GUARD = '''
    # DIAGNOSTIC ONLY: one explicitly marked feudal peer pair, during a one-day test.
    NOT = {
        AND = {
            scope:actor = {
                has_character_flag = rw_g1_probe_actor
                government_has_flag = government_is_feudal
                liege = scope:recipient.liege
                liege = {
                    OR = {
                        has_realm_law_flag = vassal_internal_wars_banned
                        has_realm_law_flag = vassal_all_wars_banned
                    }
                }
            }
            scope:recipient = { has_character_flag = rw_g1_probe_target }
        }
    }
'''


def helper_block(text):
    """Extract exactly one top-level helper, masking comments/strings for scanning."""
    if brace_errors(text):
        raise ValueError('Source has unbalanced braces or unterminated strings')
    clean, _ = clean_script(text)
    matches = list(re.finditer(r'(?m)^' + HELPER + r'\s*=\s*\{', clean))
    if len(matches) != 1:
        raise ValueError('Expected exactly one hook helper definition')
    match = matches[0]
    if clean[:match.start()].count('{') != clean[:match.start()].count('}'):
        raise ValueError('Helper must be top-level')
    opening = clean.index('{', match.start())
    depth = 1
    for pos in range(opening + 1, len(clean)):
        depth += (clean[pos] == '{') - (clean[pos] == '}')
        if depth == 0:
            return text[match.start():opening + 1], text[opening + 1:pos + 1]
    raise ValueError('Helper closing brace missing')


def build(agot_root, output):
    root = agot_root.resolve()
    out = output.resolve()
    if out.is_relative_to(REPO):
        raise ValueError('Private output must be outside the public repository')
    if out == root or out.is_relative_to(root) or root.is_relative_to(out):
        raise ValueError('Private output must be separate from the installed mod')
    if out.exists():
        raise ValueError('Output already exists; choose a new empty destination')
    raw = (root / SOURCE).read_bytes()
    text = raw.decode('utf-8-sig')
    head, body = helper_block(text)
    for marker in ('scope:actor', 'scope:recipient', 'vassal_internal_wars_banned',
                   'vassal_all_wars_banned', 'vassal_contract_war_override'):
        if marker not in clean_script(body)[0]:
            raise ValueError('Unexpected helper layout; inspect source before adapting probe')
    descriptor = root / 'descriptor.mod'
    if not descriptor.is_file():
        raise ValueError('AGOT descriptor.mod is required for the version guard')
    fields = dict(re.findall(r'(?m)^\s*(version|supported_version)\s*=\s*"([^"\r\n]+)"',
                             descriptor.read_text(encoding='utf-8-sig')))
    if fields.get('version') != '0.5.2.1' or fields.get('supported_version') != '1.19.0.6':
        raise ValueError('Probe is scoped to reported AGOT 0.5.2.1 / supported 1.19.0.6')
    patched = head + GUARD + body + '\n'
    if brace_errors(patched):
        raise ValueError('Generated helper failed structural checks')
    mod = out / 'rw_g1_probe'
    scripts = mod / 'common/scripted_triggers'
    scripts.mkdir(parents=True)
    (scripts / 'zz_rw_g1_probe.txt').write_text(patched, encoding='utf-8-sig')
    metadata = ('name="Real Westeros G1 PRIVATE PROBE"\nversion="0.0.1"\n'
                'supported_version="1.19.*"\ntags={ "Gameplay" }\n')
    (mod / 'descriptor.mod').write_text(metadata, encoding='utf-8')
    (out / 'rw_g1_probe.mod').write_text(metadata + 'path="mod/rw_g1_probe"\n', encoding='utf-8')
    receipt = dict(source_relative_path=SOURCE.as_posix(), source_sha256=hashlib.sha256(raw).hexdigest(),
                   reported_agot=fields, ck3_runtime='NOT VERIFIED',
                   purpose='PRIVATE diagnostic, not gameplay implementation; never publish generated scripts')
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    (out / 'PRIVATE.txt').write_text(
        'Contains an installed proprietary helper. DO NOT commit or distribute.\n'
        'Copy rw_g1_probe.mod and rw_g1_probe to the CK3 user-data mod folder, not game files.\n'
        'Use a disposable save. Load after AGOT. Follow docs/G1_PROBE.md in Real Westeros.\n'
        'Diagnostic bypass only: no political consequences, cancellation receipt or AI policy.\n', encoding='utf-8')
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agot-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        build(args.agot_root, args.output)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(1, f'Cannot build private diagnostic: {exc}\n')
    print('Private diagnostic built. No source changed, no engine run. See docs/G1_PROBE.md.')


if __name__ == '__main__':
    main()
