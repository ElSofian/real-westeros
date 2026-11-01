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
CLAIM_SOURCE = Path('common/casus_belli_types/00_claim.txt')
TEMPLATE_ROOT = REPO / 'diagnostics/g1_intent_probe/template'
TEMPLATE_FILES = (
    'common/scripted_triggers/rw_g1_intent_triggers.txt',
    'common/scripted_effects/rw_g1_intent_effects.txt',
    'common/character_interactions/rw_g1_intent_interactions.txt',
    'common/on_action/rw_g1_intent_on_actions.txt',
    'events/rw_g1_intent_events.txt',
    'localization/english/rw_g1_intent_l_english.yml',
    'localization/french/rw_g1_intent_l_french.yml',
)
INTENT_GUARD = '\n    NOT = { rw_g1p_bound_context_trigger = yes }\n'
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


def pinned_sources():
    """Exact privately reviewed inputs, not a claim of effective runtime definitions."""
    original = json.loads((REPO / 'docs/G1_SOURCE_RECEIPT.json').read_text())
    complement = json.loads((REPO / 'docs/G1_COMPLEMENT_RECEIPT.json').read_text())
    helper = [row['sha256'] for row in original['files']
              if row['source'] == 'AGOT' and row['file'] == SOURCE.as_posix()]
    claim = [row['sha256'] for row in complement['files']
             if row['file'] == 'AGOT/' + CLAIM_SOURCE.as_posix()]
    if len(helper) != 1 or len(claim) != 1 or any(not re.fullmatch(r'[a-f0-9]{64}', x) for x in helper + claim):
        raise ValueError('Expected exact reviewed helper and native claim source receipts')
    return {SOURCE.as_posix(): helper[0], CLAIM_SOURCE.as_posix(): claim[0]}


def intent_payload():
    """Read original allowlisted templates only; fail before writing any output."""
    payload = {}
    for name in TEMPLATE_FILES:
        path = TEMPLATE_ROOT / name
        if any(part.is_symlink() for part in (path, *path.parents)) or not path.is_file():
            raise ValueError('Intent template must be a regular checked-in file')
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig')
        if '\0' in text or (name.endswith('.txt') and brace_errors(text)):
            raise ValueError('Invalid intent template structure')
        if name.endswith('.yml'):
            language = 'french' if '/french/' in name else 'english'
            if not raw.startswith(b'\xef\xbb\xbf') or not text.startswith('l_' + language + ':'):
                raise ValueError('Invalid intent localization encoding/header')
        payload[name] = raw
    return payload


def build(agot_root, output, target_bound_intent=False):
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
    templates = {}
    input_sources = []
    if target_bound_intent:
        checked_inputs = {}
        for relative, expected in pinned_sources().items():
            data = raw if relative == SOURCE.as_posix() else (root / relative).read_bytes()
            actual = hashlib.sha256(data).hexdigest()
            if actual != expected:
                raise ValueError('Target-bound diagnostic requires exact reviewed helper/claim hashes')
            input_sources.append(dict(path=relative, sha256=actual, size=len(data)))
            checked_inputs[relative] = data
        claim_text = checked_inputs[CLAIM_SOURCE.as_posix()].decode('utf-8-sig')
        if brace_errors(claim_text) or len(re.findall(r'(?m)^claim_cb\s*=\s*\{', clean_script(claim_text)[0])) != 1:
            raise ValueError('Expected the reviewed native claim_cb definition')
        templates = intent_payload()
    guard = INTENT_GUARD if target_bound_intent else GUARD
    patched = head + guard + body + '\n'
    if brace_errors(patched):
        raise ValueError('Generated helper failed structural checks')
    mod_id = 'rw_g1_intent_probe' if target_bound_intent else 'rw_g1_probe'
    mod = out / mod_id
    scripts = mod / 'common/scripted_triggers'
    scripts.mkdir(parents=True)
    # Byte output avoids Windows newline translation changing the preserved native body.
    (scripts / 'zz_rw_g1_probe.txt').write_bytes(b'\xef\xbb\xbf' + patched.encode('utf-8'))
    for relative, data in templates.items():
        target = mod / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    probe_name = 'Real Westeros G1 PRIVATE INTENT PROBE' if target_bound_intent else 'Real Westeros G1 PRIVATE PROBE'
    metadata = (f'name="{probe_name}"\nversion="0.0.1"\n'
                'supported_version="1.19.*"\ntags={ "Gameplay" }\n')
    (mod / 'descriptor.mod').write_text(metadata, encoding='utf-8')
    (out / (mod_id + '.mod')).write_text(metadata + f'path="mod/{mod_id}"\n', encoding='utf-8')
    receipt = dict(source_relative_path=SOURCE.as_posix(), source_sha256=hashlib.sha256(raw).hexdigest(),
                   reported_agot=fields, ck3_runtime='NOT VERIFIED',
                   mode='target_bound_intent' if target_bound_intent else 'manual_flags',
                   input_sources=input_sources,
                   original_templates=[dict(path=n, sha256=hashlib.sha256(b).hexdigest(), size=len(b)) for n, b in templates.items()],
                   purpose='PRIVATE diagnostic, not gameplay implementation; never publish generated scripts')
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    (out / 'PRIVATE.txt').write_text(
        'Contains an installed proprietary helper. DO NOT commit or distribute.\n'
        f'Copy {mod_id}.mod and {mod_id} to the CK3 user-data mod folder, not game files.\n'
        'Use a disposable save. Load after AGOT; disable all other G1 probes/base submod.\n'
        'Follow docs/G1_INTENT_PROBE.md for intent mode or docs/G1_PROBE.md for manual mode.\n'
        'Diagnostic only: no political consequences, verified native cancel hook or production AI policy.\n', encoding='utf-8')
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agot-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--target-bound-intent', action='store_true',
                        help='Private exact-target staged diagnostic; pins reviewed helper/claim hashes')
    args = parser.parse_args()
    try:
        build(args.agot_root, args.output, target_bound_intent=args.target_bound_intent)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(1, f'Cannot build private diagnostic: {exc}\n')
    guide = 'docs/G1_INTENT_PROBE.md' if args.target_bound_intent else 'docs/G1_PROBE.md'
    print(f'Private diagnostic built. No source changed, no engine run. See {guide}.')


if __name__ == '__main__':
    main()
