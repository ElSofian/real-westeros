#!/usr/bin/env python3
"""Build a PRIVATE title-restoration adapter from exact reviewed local AGOT bytes."""
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
INPUT = 'common/character_interactions/00_grant_titles_interaction.txt'
MOD_ID = 'rw_native_restitution'
GUARDS = {
    'is_shown': 'rw_nd_native_shown_trigger',
    'is_valid_showing_failures_only': 'rw_nd_native_valid_trigger',
    'can_be_picked_title': 'rw_nd_native_picker_trigger',
    'can_send': 'rw_nd_native_send_trigger',
}
CALLBACKS = {'on_accept': 'rw_nd_native_consequences_effect',
             'on_auto_accept': 'rw_nd_native_notification_effect'}
AVAILABLE = '''rw_nd_adapter_available_trigger = { always = yes }
rw_nd_native_eligible_trigger = {
    rw_nd_native_shown_trigger = yes
    rw_nd_native_valid_trigger = yes
    rw_nd_native_picker_trigger = yes
    rw_nd_native_send_trigger = yes
}
'''


def pin():
    receipt = json.loads((REPO/'docs/NATIVE_RESTITUTION_SOURCE_RECEIPT.json').read_text())
    row, = [x for x in receipt['files'] if x['path'] == 'AGOT/'+INPUT]
    return row['sha256']


def clone_blocks(raw):
    """Rename block keys only. Prove body bytes unchanged, including native comments."""
    native = top_definition(raw, 'grant_titles_interaction')
    clean = clean_script(native)[0]
    if not re.search(r'\bauto_accept\s*=\s*yes\b', clean):
        raise ValueError('Unreviewed acceptance policy')
    if re.search(r'\b(cost|on_send|is_valid)\s*=\s*\{', clean):
        raise ValueError('Unreviewed native execution requirements')
    generated = {}
    proofs = []
    for kind, names in (('triggers', GUARDS), ('effects', CALLBACKS)):
        chunks = []
        for old, new in names.items():
            start, opening, end = bounds(native, old)
            original = native[start:end]
            replacement = new+native[start+len(old):end]
            if replacement.replace(new, old, 1) != original or brace_errors(replacement):
                raise ValueError('Native body preservation failed')
            chunks.append(replacement)
            proofs.append({'native': old, 'clone': new,
                           'body_sha256': hashlib.sha256(native[opening:end].encode()).hexdigest()})
        generated[kind] = ('\n\n'.join(chunks)+'\n').encode()
    generated['triggers'] += AVAILABLE.encode()
    return generated, proofs


def regular(path):
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
        raise ValueError('Expected regular non-symlink source')
    return path.read_bytes()


def templates():
    rows = []
    for path in sorted(TEMPLATES.rglob('*')):
        if path.is_symlink():
            raise ValueError('Runtime symlink')
        if not path.is_file():
            continue
        raw = regular(path)
        text = raw.decode('utf-8-sig')
        if '\0' in text or (path.suffix == '.txt' and brace_errors(text)):
            raise ValueError('Malformed runtime source')
        rows.append({'path': path.relative_to(TEMPLATES).as_posix(),
                     'sha256': hashlib.sha256(raw).hexdigest()})
    if not rows:
        raise ValueError('Missing base mod')
    return rows


def build(agot_root, output):
    root, out = Path(agot_root).resolve(), Path(output).resolve()
    if out.exists() or out.is_relative_to(REPO) or out.is_relative_to(root) or root.is_relative_to(out):
        raise ValueError('Choose a new external PRIVATE destination')
    # Reject symlinks BEFORE resolve, including a symlinked AGOT root.
    for path in (Path(agot_root).absolute(), Path(output).absolute().parent):
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('Symlinked directory')
    descriptor = regular(root/'descriptor.mod').decode('utf-8-sig')
    matches = re.findall(r'(?m)^\s*(version|supported_version)\s*=\s*"([^"\r\n]+)"', descriptor)
    if len(matches) != 2 or dict(matches) != {'version':'0.5.2.1', 'supported_version':'1.19.0.6'}:
        raise ValueError('Unreviewed version metadata')
    raw = regular(root/INPUT)
    if hashlib.sha256(raw).hexdigest() != pin():
        raise ValueError('Native bytes differ from reviewed input')
    clones, proofs = clone_blocks(raw)
    runtime = templates()
    payload = {
        'common/scripted_triggers/zz_rw_native_restitution.txt': clones['triggers'],
        'common/scripted_effects/zz_rw_native_restitution.txt': clones['effects'],
    }
    metadata = ('name="Real Westeros PRIVATE restitution EXPERIMENT"\n'
                'version="0.0.1"\nsupported_version="1.19.*"\n'
                'dependencies={ "Real Westeros" }\ntags={ "Gameplay" }\n')
    receipt = {'schema':1, 'status':'PRIVATE source candidate; NOT engine-tested',
               'reported_agot':dict(matches), 'input':{'path':INPUT, 'sha256':pin()},
               'runtime_sources':runtime, 'clones':proofs,
               'preservation':'Only block keys renamed; six native bodies byte-identical.',
               'outputs':[{'path':p, 'sha256':hashlib.sha256(b).hexdigest()} for p,b in payload.items()],
               'adaptation':'Original hidden event binds actor/recipient/target/target_title/landed_title and dummy_gender (TITLE macro) and a one-title target_titles list.',
               'limits':['Duchy dignity only; no vassal or county transfers.',
                         'Native hardcoded grant equivalence, callback timing and load order NOT engine-tested.',
                         'A voluntary restoration is not proof of an earlier legal sanction or house-wide title ban.']}
    out.mkdir(parents=True, exist_ok=False)
    for name, data in payload.items():
        dest=out/MOD_ID/name; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(data)
    (out/MOD_ID/'descriptor.mod').write_text(metadata)
    (out/(MOD_ID+'.mod')).write_text(metadata+'path="mod/'+MOD_ID+'"\n')
    (out/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    (out/'PRIVATE.txt').write_text('Contains proprietary AGOT code. DO NOT publish, commit or redistribute.\n'
        'Final campaign only: AGOT, matching Real Westeros, then this adapter.\n'
        'No native interaction override. Do not combine with another rw_nd adapter.\n'
        'Callback order, engine behavior and equivalence are unverified.\n')
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agot-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    try:
        build(args.agot_root, args.output)
    except (OSError, ValueError):
        parser.exit(1, 'Private generation refused: source, layout, metadata or destination failed validation.\n')
    print('PRIVATE restitution adapter generated; never distribute; NOT engine-tested.')


if __name__ == '__main__':
    main()
