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
TEMPLATES = REPO / 'mod/real_westeros'
FILES = ('common/scripted_triggers/rw_external_title_stakes_triggers.txt',
         'common/scripted_triggers/rw_peer_title_stakes_triggers.txt',
         'common/scripted_triggers/rw_protected_title_stakes_triggers.txt',
         'common/scripted_triggers/rw_external_beneficiary_triggers.txt',
         'common/scripted_triggers/rw_peer_beneficiary_triggers.txt',
         'common/script_values/rw_declaration_ai_values.txt',
         'common/scripted_triggers/rw_declaration_ai_triggers.txt',
         'common/script_values/rw_peer_war_ai_values.txt',
         'common/script_values/rw_external_war_ai_values.txt',
         'common/scripted_triggers/rw_political_ai_triggers.txt',
         'common/scripted_effects/rw_external_war_mediation_effects.txt',
         'common/scripted_triggers/rw_external_war_mediation_triggers.txt',
         'events/rw_external_war_mediation_events.txt',
         'common/scripted_effects/rw_external_war_intervention_effects.txt',
         'common/scripted_triggers/rw_external_war_intervention_triggers.txt',
         'events/rw_external_war_intervention_events.txt',
         'common/scripted_effects/rw_external_war_response_effects.txt',
         'common/scripted_triggers/rw_external_war_response_triggers.txt',
         'common/story_cycles/rw_external_war_responses.txt',
         'events/rw_external_war_response_events.txt',
         'localization/english/rw_external_war_response_l_english.yml',
         'localization/french/rw_external_war_response_l_french.yml',
         'common/scripted_effects/rw_war_lifecycle_effects.txt',
         'common/scripted_triggers/rw_declaration_law_triggers.txt',
         'common/scripted_effects/rw_declaration_law_effects.txt',
         'common/story_cycles/rw_declaration_law.txt', 'common/scripted_effects/rw_unlawful_war_intervention_effects.txt',
         'events/rw_unlawful_war_intervention_events.txt',
         'common/scripted_effects/rw_unlawful_war_response_effects.txt',
         'common/story_cycles/rw_unlawful_war_responses.txt',
         'common/opinion_modifiers/rw_unlawful_war_response_opinions.txt',
         'events/rw_unlawful_war_response_events.txt',
         'common/scripted_triggers/rw_unlawful_war_choice_triggers.txt',
         'localization/english/rw_unlawful_war_choice_l_english.yml',
         'localization/french/rw_unlawful_war_choice_l_french.yml')
INTERACTION = 'common/character_interactions/00_war.txt'
HELPER = 'common/scripted_triggers/00_war_and_peace_triggers.txt'
CLAIM = 'common/casus_belli_types/00_claim.txt'
VASSAL = 'common/character_interactions/00_vassal_interactions.txt'
MOD_ID = 'rw_g1_native_choice'
# Original additions only. No copied native interaction/helper/CB in this file.
LAW_PREFIX = '\n    rw_dl_capture_effect = yes\n'
TERMINAL_CALLBACKS = ('on_invalidated', 'on_victory', 'on_white_peace', 'on_defeat')
TERMINAL_PREFIXES = {name: '\n    rw_uw_terminal_effect = { OUTCOME = ' + name + ' }\n'
                     for name in TERMINAL_CALLBACKS}
CLONE = 'rw_dl_native_permission_trigger'
NATIVE_PERMISSION = 'war_declarer_needs_hook_on_liege'
ACCEPT = '''
    scope:actor = {
        rw_dl_bind_acceptance_effect = yes
        rw_xw_notice_effect = yes
        rw_uw_notice_effect = yes
    }
'''
INTERVENTION_PREFIX = '\n    rw_uw_bind_native_target_effect = yes\n    rw_xw_bind_native_target_effect = yes\n'
INTERVENTION_MARKER = ('rw_uw_native_target_adapter_available_trigger = { always = yes }\n'
                       'rw_xw_native_adapter_available_trigger = { always = yes }\n')
GUARD = '\n            rw_uw_selected_defiance_trigger = yes\n'
OPTION = '''
    # RW isolated experiment: the native window owns this transient send flag.
    send_option = {
        flag = rw_uw_defy
        localization = rw_uw_defy_option
        is_shown = { rw_uw_applicable_ban_trigger = yes }
        is_valid = {
            custom_tooltip = {
                text = rw_uw_defy_warning
                rw_uw_applicable_ban_trigger = yes
                NOT = { always = scope:hook }
            }
        }
        starts_enabled = { rw_uw_ai_default_defiance_trigger = yes }
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
    """Insert a guard, option and guarded post-native response; preserve all old bytes."""
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
    _, _, accept_end = bounds(native, 'on_accept')
    accept_at = accept_end - 1
    if accept_at <= option_at:
        raise ValueError('Unexpected native acceptance block ordering')
    patched = native[:accept_at] + ACCEPT + native[accept_at:]
    patched = patched[:option_at] + OPTION + patched[option_at:]
    patched = patched[:insertion] + GUARD + patched[insertion:]
    if brace_errors(patched) or patched.replace(GUARD, '', 1).replace(OPTION, '', 1).replace(ACCEPT, '', 1) != native:
        raise ValueError('Native-byte preservation failed')
    return native.encode('utf-8'), patched.encode('utf-8')



def top_definition(raw, name):
    text = raw.decode('utf-8-sig')
    if brace_errors(text):
        raise ValueError('Invalid native source structure')
    a, opening, end = bounds(text, name)
    clean = clean_script(text)[0]
    if clean[:a].count('{') != clean[:a].count('}'):
        raise ValueError('Native definition must be top-level')
    return text[a:end]


def patch_claim_law(raw):
    native = top_definition(raw, 'claim_cb')
    if 'rw_dl_' in native:
        raise ValueError('Claim already contains declaration-law adapter')
    _, opening, _ = bounds(native, 'on_declaration')
    patched = native[:opening+1] + LAW_PREFIX + native[opening+1:]
    if brace_errors(patched) or patched.replace(LAW_PREFIX, '', 1) != native:
        raise ValueError('Claim-body preservation failed')
    return native.encode('utf-8'), patched.encode('utf-8')


def patch_claim_lifecycle(raw):
    """Original metadata prefixes only; refuse missing/ambiguous native callbacks."""
    native = top_definition(raw, 'claim_cb')
    if 'rw_uw_terminal_effect' in native:
        raise ValueError('Claim already contains lifecycle adapter')
    additions = []
    for name, prefix in TERMINAL_PREFIXES.items():
        _, opening, _ = bounds(native, name)
        additions.append((opening + 1, prefix))
    patched = native
    for position, prefix in sorted(additions, reverse=True):
        patched = patched[:position] + prefix + patched[position:]
    restored = patched
    for prefix in TERMINAL_PREFIXES.values():
        restored = restored.replace(prefix, '', 1)
    if brace_errors(patched) or restored != native:
        raise ValueError('Native terminal callback preservation failed')
    return native.encode('utf-8'), patched.encode('utf-8')


def clone_permission(raw):
    native = top_definition(raw, NATIVE_PERMISSION)
    clean = clean_script(native)[0]
    if 'rw_dl_' in native or re.search(r'\b(root|prev)\b', clean):
        raise ValueError('Unsupported native helper context')
    refs = set(re.findall(r'\bscope:(\w+)', clean))
    if refs != {'actor', 'recipient'}:
        raise ValueError('Unexpected native helper aliases')
    # Replace ONLY actual code tokens; keep every other byte, comment and string.
    changes = [(m.start(),m.end(),'scope:rw_dl_actor' if m.group(1)=='actor' else 'scope:rw_dl_target')
               for m in re.finditer(r'\bscope:(actor|recipient)\b',clean)]
    copied = native
    for a,b,value in reversed(changes):
        copied = copied[:a] + value + copied[b:]
    copied = copied.replace(NATIVE_PERMISSION, CLONE, 1)
    restored = copied.replace(CLONE,NATIVE_PERMISSION,1).replace('scope:rw_dl_actor','scope:actor').replace('scope:rw_dl_target','scope:recipient')
    if brace_errors(copied) or restored != native:
        raise ValueError('Native helper preservation failed')
    # The base's false availability marker stays fail-closed if load order is wrong.
    prefix = 'rw_dl_adapter_available_trigger = { always = yes }\n'
    return native.encode('utf-8'), (prefix+copied).encode('utf-8')


def patch_native_intervention(raw):
    """Restore only the RW dispatch target before the unchanged native callback."""
    native = top_definition(raw, 'stop_attacker_vassal_war_interaction')
    if 'rw_uw_' in native:
        raise ValueError('Native intervention already patched')
    _, opening, _ = bounds(native, 'on_accept')
    patched = native[:opening + 1] + INTERVENTION_PREFIX + native[opening + 1:]
    if brace_errors(patched) or patched.replace(INTERVENTION_PREFIX, '', 1) != native:
        raise ValueError('Native intervention preservation failed')
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
    intervention = json.loads((REPO / 'docs/G1_NATIVE_INTERVENTION_SOURCE_RECEIPT.json').read_text())['files']
    hits = [r['sha256'] for r in intervention if r['path'] == 'AGOT/' + VASSAL]
    if len(hits) != 1:
        raise ValueError('Missing reviewed native intervention source')
    result[VASSAL] = hits[0]
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
    original_claim, law_claim = patch_claim_law(sources[CLAIM])
    _, patched_claim = patch_claim_lifecycle(law_claim)
    original_helper, cloned_helper = clone_permission(sources[HELPER])
    original_intervention, patched_intervention = patch_native_intervention(sources[VASSAL])
    runtime = template_payload()
    payload = {
        'common/character_interactions/zz_rw_native_war_choice.txt': b'\xef\xbb\xbf' + patched + b'\n',
        'common/casus_belli_types/zz_rw_native_claim_law.txt': b'\xef\xbb\xbf' + patched_claim + b'\n',
        'common/scripted_triggers/zz_rw_native_law_permission.txt': b'\xef\xbb\xbf' + cloned_helper + b'\n' + INTERVENTION_MARKER.encode(),
        'common/character_interactions/zz_rw_native_war_intervention.txt': b'\xef\xbb\xbf' + patched_intervention + b'\n',
    }
    metadata = ('name="Real Westeros PRIVATE native war choice EXPERIMENT"\n'
                'version="0.0.10"\nsupported_version="1.19.*"\ntags={ "Gameplay" }\n'
                'dependencies={ "Real Westeros" }\n')
    receipt = {'schema': 1, 'status': 'PRIVATE isolated experimental source; NOT engine-tested',
               'reported_agot': fields,
               'requires_base_mod': 'Real Westeros',
               'native_intervention_definition_sha256': hashlib.sha256(original_intervention).hexdigest(),
               'patched_intervention_definition_sha256': hashlib.sha256(patched_intervention).hexdigest(),
               'intervention_preservation': 'Removing INTERVENTION_PREFIX restores native stop interaction; exact target transport is NOT engine-tested',
               'runtime_sources': [{'path': p, 'sha256': hashlib.sha256(b).hexdigest()} for p,b in runtime.items()],
               'inputs': [{'path': p, 'sha256': hashlib.sha256(b).hexdigest()} for p,b in sources.items()],
               'law_capture_phase': 'claim_cb.on_declaration prefix; engine callback order NOT VERIFIED',
               'native_claim_definition_sha256': hashlib.sha256(original_claim).hexdigest(),
               'patched_claim_definition_sha256': hashlib.sha256(patched_claim).hexdigest(),
               'native_helper_definition_sha256': hashlib.sha256(original_helper).hexdigest(),
               'claim_preservation': 'Removing LAW_PREFIX and four TERMINAL_PREFIXES restores native claim_cb; no native cost or lifecycle replay',
               'terminal_callbacks': list(TERMINAL_CALLBACKS),
               'terminal_order': 'Original metadata prefix only; engine scope availability and Mega War ordering NOT VERIFIED',
               'helper_preservation': 'Inverse owned-name/actor/recipient alias substitution restores native helper',
               'native_definition_sha256': hashlib.sha256(original).hexdigest(),
               'patched_definition_sha256': hashlib.sha256(patched).hexdigest(),
               'native_byte_preservation': 'Removing exactly the three original insertions restores the native definition',
               'outputs': [{'path': p, 'sha256': hashlib.sha256(b).hexdigest()} for p,b in payload.items()],
               'ai_option_initialization': 'Contextual starts_enabled only; native AI candidate discovery and dispatch NOT VERIFIED',
               'limits': ['No historical unlawful-war verdict, forced peace or demonstrated autonomous war initiation.',
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
        'Install only for final campaign, after AGOT and Real Westeros. Mutually exclusive with every other G1 probe/adapter.\n', encoding='utf-8')
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
