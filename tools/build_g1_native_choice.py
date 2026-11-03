#!/usr/bin/env python3
"""Generate a PRIVATE isolated native-war-window experiment; never public assets."""
import argparse
import hashlib
import json
from pathlib import Path
import re
try:
    from .validate_mod import brace_errors, clean_script
except ImportError:
    from validate_mod import brace_errors, clean_script

REPO = Path(__file__).resolve().parents[1]
TEMPLATES = REPO / 'experiments/g1_native_choice/template'
FILES = ('common/scripted_triggers/rw_unlawful_war_choice_triggers.txt',
         'localization/english/rw_unlawful_war_choice_l_english.yml',
         'localization/french/rw_unlawful_war_choice_l_french.yml')
INTERACTION = 'common/character_interactions/00_war.txt'
HELPER = 'common/scripted_triggers/00_war_and_peace_triggers.txt'
CLAIM = 'common/casus_belli_types/00_claim.txt'
MOD_ID = 'rw_g1_native_choice'
# Original additions only. No copied native interaction/helper/CB in this file.
GUARD = '\n            rw_uw_selected_defiance_trigger = yes\n'
OPTION = '''
    # RW isolated experiment: the native window owns this transient send flag.
    send_option = {
        flag = rw_uw_defy
        localization = rw_uw_defy_option
        is_shown = { rw_uw_peer_ban_trigger = yes }
        is_valid = {
            custom_tooltip = {
                text = rw_uw_defy_warning
                rw_uw_peer_ban_trigger = yes
                NOT = { always = scope:hook }
            }
        }
        can_invalidate_interaction = yes
    }
'''


def bounds(text, name):
    """Find a single assignment block, using masked character offsets."""
    clean = clean_script(text)[0]
    matches = list(re.finditer(r'\b' + re.escape(name) + r'\s*=\s*\{', clean))
    if len(matches) != 1:
        raise ValueError('Expected one block: ' + name)
    match = matches[0]
    opening = clean.index('{', match.start())
    depth = 1
    for pos in range(opening + 1, len(clean)):
        depth += (clean[pos] == '{') - (clean[pos] == '}')
        if depth == 0:
            return match.start(), opening, pos + 1
    raise ValueError('Unclosed assignment block')


def patch_native(raw):
    """Insert only one extra OR branch and one send option; preserve all old bytes."""
    text = raw.decode('utf-8-sig')
    if brace_errors(text):
        raise ValueError('Invalid source structure')
    start, _, end = bounds(text, 'declare_war_interaction')
    clean = clean_script(text)[0]
    if clean[:start].count('{') != clean[:start].count('}'):
        raise ValueError('Expected top-level native interaction')
    native = text[start:end]
    if 'rw_uw_' in native:
        raise ValueError('Source already contains experiment')
    a, b, c = bounds(native, 'has_valid_target_showing_failures_only')
    target = native[a:c]
    masked = clean_script(target)[0]
    branches = list(re.finditer(r'\bOR\s*=\s*\{\s*war_declarer_needs_hook_on_liege\s*=\s*no\s+always\s*=\s*scope:hook\s*\}', masked))
    if len(branches) != 1:
        raise ValueError('Unexpected native hook guard; do not adapt automatically')
    insertion = a + branches[0].end() - 1
    send = list(re.finditer(r'\bsend_options_exclusive\s*=\s*no\b', clean_script(native)[0]))
    if len(send) != 1:
        raise ValueError('Unexpected native send-option layout')
    option_at = send[0].end()
    if option_at <= insertion:
        raise ValueError('Unexpected declaration block ordering')
    patched = native[:option_at] + OPTION + native[option_at:]
    patched = patched[:insertion] + GUARD + patched[insertion:]
    if brace_errors(patched) or patched.replace(GUARD, '', 1).replace(OPTION, '', 1) != native:
        raise ValueError('Native-byte preservation failed')
    return native.encode('utf-8'), patched.encode('utf-8')


def pinned_sources():
    first = json.loads((REPO / 'docs/G1_SOURCE_RECEIPT.json').read_text())['files']
    second = json.loads((REPO / 'docs/G1_COMPLEMENT_RECEIPT.json').read_text())['files']
    result = {}
    for path in (INTERACTION, HELPER):
        hits = [r['sha256'] for r in first if r['source'] == 'AGOT' and r['file'] == path]
        if len(hits) != 1:
            raise ValueError('Missing reviewed native source')
        result[path] = hits[0]
    hits = [r['sha256'] for r in second if r['file'] == 'AGOT/' + CLAIM]
    if len(hits) != 1:
        raise ValueError('Missing reviewed claim source')
    result[CLAIM] = hits[0]
    return result


def template_payload(root=TEMPLATES):
    result = {}
    for relative in FILES:
        path = root / relative
        if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
            raise ValueError('Templates must be regular files')
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig')
        if '\0' in text or (relative.endswith('.txt') and brace_errors(text)):
            raise ValueError('Invalid original template')
        if relative.endswith('.yml'):
            lang = 'french' if '/french/' in relative else 'english'
            if not raw.startswith(b'\xef\xbb\xbf') or not text.startswith('l_' + lang + ':'):
                raise ValueError('Invalid localization encoding/header')
        result[relative] = raw
    return result


def build(agot_root, output):
    root, out = Path(agot_root).resolve(), Path(output).resolve()
    if out.is_relative_to(REPO) or out.is_relative_to(root) or root.is_relative_to(out):
        raise ValueError('Private output must be outside repository and installed mod')
    if out.exists():
        raise ValueError('Choose a new private output destination')
    descriptor = root / 'descriptor.mod'
    if descriptor.is_symlink():
        raise ValueError('Descriptor must be a regular file')
    fields = dict(re.findall(r'(?m)^\s*(version|supported_version)\s*=\s*"([^"\r\n]+)"',
                             descriptor.read_text(encoding='utf-8-sig')))
    if fields != {'version': '0.5.2.1', 'supported_version': '1.19.0.6'}:
        raise ValueError('Only reviewed AGOT 0.5.2.1 / supported 1.19.0.6 is accepted')
    sources = {}
    for relative, expected in pinned_sources().items():
        path = root / relative
        if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
            raise ValueError('Native input must be a regular file')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Native input differs from reviewed hash; stop for source review')
        sources[relative] = raw
    original, patched = patch_native(sources[INTERACTION])
    payload = template_payload()
    payload['common/character_interactions/zz_rw_native_war_choice.txt'] = b'\xef\xbb\xbf' + patched + b'\n'
    metadata = ('name="Real Westeros PRIVATE native war choice EXPERIMENT"\n'
                'version="0.0.1"\nsupported_version="1.19.*"\ntags={ "Gameplay" }\n')
    receipt = {'schema': 1, 'status': 'PRIVATE isolated experimental source; NOT engine-tested',
               'reported_agot': fields,
               'inputs': [{'path': p, 'sha256': hashlib.sha256(b).hexdigest()} for p,b in sources.items()],
               'native_definition_sha256': hashlib.sha256(original).hexdigest(),
               'patched_definition_sha256': hashlib.sha256(patched).hexdigest(),
               'native_byte_preservation': 'Removing exactly the two original insertions restores the native definition',
               'outputs': [{'path': p, 'sha256': hashlib.sha256(b).hexdigest()} for p,b in payload.items()],
               'limits': ['No unlawful-war verdict, royal response or AI policy is implemented.',
                          'No cost, cancel, callback-order, override-loading or Mega War engine result.']}
    # All validation precedes exclusive directory creation; never touch installation.
    out.mkdir(parents=True, exist_ok=False)
    for relative, raw in payload.items():
        target = out / MOD_ID / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    (out / MOD_ID / 'descriptor.mod').write_text(metadata, encoding='utf-8')
    (out / (MOD_ID + '.mod')).write_text(metadata + f'path="mod/{MOD_ID}"\n', encoding='utf-8')
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    (out / 'PRIVATE.txt').write_text('Contains proprietary native interaction. DO NOT publish, commit or redistribute.\n'
        'Install only for final campaign, after AGOT. Mutually exclusive with every other G1 probe/adapter.\n', encoding='utf-8')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agot-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        build(args.agot_root, args.output)
    except (OSError, ValueError):
        parser.exit(1, 'Private generation refused: inputs, layout or destination failed validation.\n')
    print('Private isolated experiment generated. Do not distribute output; no engine compatibility demonstrated.')


if __name__ == '__main__':
    main()
