#!/usr/bin/env python3
"""Generate a PRIVATE native revocation AI adapter; never distribute its output."""
import argparse
import hashlib
import json
from pathlib import Path
import re
try:
    from .build_g1_native_choice import bounds, top_definition
    from .validate_mod import brace_errors, clean_script
except ImportError:
    from build_g1_native_choice import bounds, top_definition
    from validate_mod import brace_errors, clean_script

REPO = Path(__file__).resolve().parents[1]
TEMPLATES = REPO/'mod/real_westeros'
INPUT = 'common/character_interactions/00_revoke_title_interaction.txt'
MOD_ID = 'rw_g3_native_confiscation'
FILES = ('common/scripted_triggers/rw_post_confiscation_triggers.txt', 'common/scripted_effects/rw_post_confiscation_effects.txt', 'common/story_cycles/rw_post_confiscation.txt', 'common/character_interactions/rw_post_confiscation_interactions.txt', 'events/rw_post_confiscation_events.txt', 'localization/english/rw_post_confiscation_l_english.yml', 'localization/french/rw_post_confiscation_l_french.yml', 'events/rw_title_provenance_events.txt',
         'localization/english/rw_title_provenance_l_english.yml',
         'localization/french/rw_title_provenance_l_french.yml', 'common/scripted_effects/rw_title_provenance_effects.txt', 'common/story_cycles/rw_house_revocation_request.txt',
         'common/on_action/rw_title_provenance_on_actions.txt', 'common/scripted_triggers/rw_confiscation_transfer_triggers.txt',
         'common/scripted_effects/rw_confiscation_transfer_effects.txt',
         'events/rw_confiscation_transfer_events.txt',
         'common/story_cycles/rw_title_provenance.txt',
         'common/scripted_triggers/rw_title_provenance_triggers.txt',
         'common/scripted_triggers/rw_land_register_triggers.txt',
         'common/scripted_effects/rw_land_register_effects.txt',
         'events/rw_land_register_events.txt',
         'common/scripted_triggers/rw_house_affair_triggers.txt', 'common/character_interactions/rw_house_confiscation_interactions.txt',
         'common/scripted_triggers/rw_house_confiscation_triggers.txt',
         'common/scripted_effects/rw_house_confiscation_effects.txt',
         'common/story_cycles/rw_house_confiscation.txt',
         'common/script_values/rw_house_confiscation_values.txt',
         'localization/english/rw_house_confiscation_l_english.yml',
         'localization/french/rw_house_confiscation_l_french.yml')
PREFIX = '\n        modifier = { add = rw_hc_native_priority_value }\n'
BEFORE = '\n        rw_hcr_register_request_effect = yes\n'
AFTER = '\n        rw_hcr_declined_effect = yes\n'
ACCEPTED = '\n        rw_pcr_native_accepted_effect = yes\n'
INSERTIONS = (PREFIX, BEFORE, AFTER, ACCEPTED)
AVAILABLE = 'rw_hc_adapter_available_trigger = { always = yes }\n'


def pin():
    receipt = json.loads((REPO/'docs/HOUSE_CONFISCATION_SOURCE_RECEIPT.json').read_text())
    row, = [x for x in receipt['files'] if x['path'] == 'AGOT/'+INPUT]
    return row['sha256']


def patch_native(raw):
    original = top_definition(raw, 'revoke_title_interaction')
    if 'rw_hc_' in original:
        raise ValueError('Already contains confiscation adapter')
    a, opening, _ = bounds(original, 'ai_will_do')
    clean = clean_script(original)[0]
    base = re.match(r'\s*base\s*=\s*-1000\b', clean[opening+1:])
    if not base:
        raise ValueError('Unexpected native AI base/layout')
    position = opening+1+base.end()
    _, send_start, _ = bounds(original, 'on_send')
    _, decline_start, _ = bounds(original, 'on_decline')
    _, _, accept_end = bounds(original, 'on_accept')
    patched = original
    for at, addition in sorted(((position,PREFIX),(send_start+1,BEFORE),(decline_start+1,AFTER),(accept_end-1,ACCEPTED)),reverse=True):
        patched = patched[:at]+addition+patched[at:]
    restored = patched
    for addition in INSERTIONS: restored = restored.replace(addition,'',1)
    if brace_errors(patched) or restored != original:
        raise ValueError('Native byte preservation failed')
    return original.encode('utf-8'), patched.encode('utf-8')


def templates():
    rows = []
    for name in FILES:
        path = TEMPLATES/name
        if any(x.is_symlink() for x in (path,*path.parents)) or not path.is_file():
            raise ValueError('Runtime source must be regular')
        raw = path.read_bytes(); text = raw.decode('utf-8-sig')
        if '\0' in text or (name.endswith('.txt') and brace_errors(text)):
            raise ValueError('Invalid original source')
        if name.endswith('.yml'):
            lang = 'french' if '/french/' in name else 'english'
            if not raw.startswith(b'\xef\xbb\xbf') or not text.startswith('l_'+lang+':'):
                raise ValueError('Invalid localization')
        rows.append({'path':name,'sha256':hashlib.sha256(raw).hexdigest()})
    return rows


def build(agot_root, output):
    root, out = Path(agot_root).resolve(), Path(output).resolve()
    if out.exists() or out.is_relative_to(REPO) or out.is_relative_to(root) or root.is_relative_to(out):
        raise ValueError('Choose a new external private destination')
    descriptor = root/'descriptor.mod'
    source = root/INPUT
    for path in (descriptor,source):
        if any(x.is_symlink() for x in (path,*path.parents)) or not path.is_file():
            raise ValueError('Input must be regular')
    fields = dict(re.findall(r'(?m)^\s*(version|supported_version)\s*=\s*"([^"\r\n]+)"',descriptor.read_text(encoding='utf-8-sig')))
    if fields != {'version':'0.5.2.1','supported_version':'1.19.0.6'}:
        raise ValueError('Unreviewed metadata')
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != pin():
        raise ValueError('Native input differs from reviewed bytes')
    original, patched = patch_native(raw)
    runtime = templates()
    payload = {
        'common/character_interactions/zz_rw_native_confiscation.txt': b'\xef\xbb\xbf'+patched+b'\n',
        'common/scripted_triggers/zz_rw_native_confiscation_available.txt': AVAILABLE.encode(),
    }
    metadata = ('name="Real Westeros PRIVATE confiscation AI EXPERIMENT"\n'
                'version="0.0.3"\nsupported_version="1.19.*"\n'
                'dependencies={ "Real Westeros" }\ntags={ "Gameplay" }\n')
    receipt = {'schema':1,'status':'PRIVATE experimental source; NOT engine-tested',
               'reported_agot':fields,'requires_base_mod':'Real Westeros',
               'input':{'path':INPUT,'sha256':hashlib.sha256(raw).hexdigest()},
               'runtime_sources':runtime,
               'native_definition_sha256':hashlib.sha256(original).hexdigest(),
               'patched_definition_sha256':hashlib.sha256(patched).hexdigest(),
               'preservation':'Removing PREFIX/BEFORE/AFTER/ACCEPTED restores native definition; native bodies/modifiers unchanged',
               'outputs':[{'path':p,'sha256':hashlib.sha256(b).hexdigest()} for p,b in payload.items()],
               'receipt_phase':'Snapshot at native on_send, exact on_title_gain association, close at decline; callback timing/scopes NOT engine-tested',
               'limits':['Native AI scheduling, title scope, scoring, costs/resistance and outcomes NOT engine-tested.',
                         'Policy and conditional request-matched title facts only; no acquisition veto, fifty-year ban or legal verdict; optional actual ducal restitution requires the separate native grant adapter.']}
    out.mkdir(parents=True,exist_ok=False)
    for name, data in payload.items():
        dest = out/MOD_ID/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    (out/MOD_ID/'descriptor.mod').write_text(metadata)
    (out/(MOD_ID+'.mod')).write_text(metadata+'path="mod/'+MOD_ID+'"\n')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    (out/'PRIVATE.txt').write_text('Contains proprietary native code. DO NOT publish, commit or redistribute.\n'
        'Only for final campaign. AGOT then matching Real Westeros then this adapter.\n'
        'Do not combine with another revoke_title_interaction override. Native behavior is unverified.\n')
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agot-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try: build(args.agot_root,args.output)
    except (OSError,ValueError):parser.exit(1,'Private generation refused: inputs, layout or destination failed validation.\n')
    print('Private confiscation AI adapter generated; never distribute; NOT engine-tested.')


if __name__ == '__main__': main()
