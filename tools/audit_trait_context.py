#!/usr/bin/env python3
"""Private trait inventory and narrow promise-input audit, never engine evaluation.

Reads installed sources without copying definitions into the public repository.
Same relative trait filenames are overlaid CK3 then AGOT. Duplicate surviving IDs
are rejected. Conditional/track/script-valued inputs remain explicitly unresolved.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|@\[[^\]]*\]|[{}=]|[^\s{}=#]+')
NUMBER = re.compile(r'-?\d+(?:\.\d+)?\Z')
IDENTIFIER = re.compile(r'[A-Za-z_][A-Za-z_0-9]*\Z')
AXES = ('ai_boldness', 'ai_compassion', 'ai_energy', 'ai_greed', 'ai_honor',
        'ai_rationality', 'ai_sociability', 'ai_vengefulness', 'ai_zeal')
PERSONAL = ('diplomacy', 'martial', 'stewardship', 'intrigue', 'learning',
            'prowess', 'health', 'fertility', 'stress_gain_mult', 'stress_loss_mult',
            'minimum_age', 'maximum_age')


def tokens(text):
    return [(match.group(), match.start()) for match in TOKEN.finditer(text)
            if not match.group().startswith('#')]


def assignments(items):
    """Read one assignment level, retaining nested tokens without interpreting them."""
    result = []
    index = 0
    while index < len(items):
        if index + 2 >= len(items) or items[index + 1][0] != '=':
            raise ValueError('Unsupported assignment near offset ' + str(items[index][1]))
        key, offset = items[index]
        value = items[index + 2][0]
        end = index + 3
        nested = None
        if value == '{':
            depth = 1
            while end < len(items) and depth:
                depth += (items[end][0] == '{') - (items[end][0] == '}')
                end += 1
            if depth:
                raise ValueError('Unclosed block near offset ' + str(offset))
            nested = items[index + 3:end - 1]
        elif value in ('}', '='):
            raise ValueError('Invalid scalar near offset ' + str(offset))
        result.append((key, value, nested, offset))
        index = end
    return result


def numeric(value, constants):
    if value.startswith('@'):
        value = constants.get(value, value)
    return float(value) if NUMBER.fullmatch(value) else None


def read_traits(text, source, relative_path, scalar_values=None):
    definitions = assignments(tokens(text))
    constants = dict(scalar_values or {})
    constants.update({key: value for key, value, body, _ in definitions
                      if key.startswith('@') and body is None})
    rows = []
    for name, _, body, offset in definitions:
        if name.startswith('@'):
            continue
        if body is None or not IDENTIFIER.fullmatch(name):
            raise ValueError('Unsupported trait definition ' + name)
        fields = assignments(body)
        direct = {}
        for key, value, nested, _ in fields:
            if key in AXES + PERSONAL:
                resolved_value = constants.get(value, value)
                direct.setdefault(key, []).append(numeric(resolved_value, constants) if nested is None else None)
        resolved = {key: values[0] for key, values in direct.items()
                    if len(values) == 1 and values[0] is not None}
        direct_offsets = {position for _, _, _, position in fields}
        nested_axes = sorted({body[index][0] for index in range(len(body) - 1)
                              if body[index][0] in AXES and body[index + 1][0] == '='
                              and body[index][1] not in direct_offsets})
        unresolved = sorted(set(direct) - set(resolved))
        relevant = {'ai_honor', 'ai_greed'}
        if relevant.intersection(unresolved + nested_axes):
            coverage = 'conditional_or_unresolved'
        elif any(resolved.get(key, 0) != 0 for key in relevant):
            coverage = 'native_axes_input'
        else:
            coverage = 'zero_direct_axis_input'
        rows.append({
            'id': name, 'source': source, 'file': relative_path,
            'line': text.count('\n', 0, offset) + 1,
            'category': next((value.strip('"') for key, value, nested, _ in fields
                              if key == 'category' and nested is None), 'unspecified'),
            'personality_trait': any((key == 'personality' and value == 'yes') or
                                    (key == 'category' and value == 'personality')
                                     for key, value, _, _ in fields),
            'direct_axes': {key: value for key, value in resolved.items() if key in AXES},
            'direct_personal_fields': {key: value for key, value in resolved.items() if key in PERSONAL},
            'nested_axes': nested_axes, 'unresolved_fields': unresolved,
            'promise_input_status': coverage,
            'context_review': 'pending',
        })
    return rows


def literal_script_values(ck3_root, agot_root):
    """Resolve only literal top-level values. Never evaluate scripted expressions."""
    files = {}
    for root in (ck3_root, agot_root):
        for path in sorted((root/'common/script_values').rglob('*.txt')):
            files[path.relative_to(root).as_posix()] = path
    found, duplicates, receipts = {}, set(), []
    for relative, path in sorted(files.items()):
        data = path.read_bytes()
        try:
            definitions = assignments(tokens(data.decode('utf-8-sig')))
        except ValueError as error:
            raise ValueError(relative + ': ' + str(error)) from error
        for key, value, body, _ in definitions:
            if key in found:
                duplicates.add(key)
            found[key] = value if body is None and NUMBER.fullmatch(value) else None
        receipts.append({'file': relative, 'sha256': hashlib.sha256(data).hexdigest()})
    return {key: value for key, value in found.items()
            if value is not None and key not in duplicates}, receipts


def french_names(ck3_root, agot_root):
    names = {}
    pattern = re.compile(r'^\s*(trait_[\w.-]+):\d*\s+"((?:\\.|[^"\\])*)"')
    for root in (ck3_root, agot_root):
        for path in sorted((root/'localization').rglob('*_l_french.yml'),
                           key=lambda path: ('replace' in path.parts, path.as_posix())):
            for line in path.read_text(encoding='utf-8-sig').splitlines():
                match = pattern.match(line)
                if match:
                    names[match[1]] = match[2]
    return names


def inventory(ck3_root, agot_root):
    effective = {}
    replaced = []
    for source, root in (('CK3', ck3_root), ('AGOT', agot_root)):
        directory = root / 'common/traits'
        files = sorted(directory.rglob('*.txt'))
        if not files:
            raise ValueError('Missing or empty ' + source + ' common/traits')
        for path in files:
            relative = path.relative_to(root).as_posix()
            if relative in effective:
                replaced.append(relative)
            effective[relative] = (source, path)
    values, value_receipts = literal_script_values(ck3_root, agot_root)
    names = french_names(ck3_root, agot_root)
    rows, receipts, seen = [], [], set()
    for relative, (source, path) in sorted(effective.items()):
        data = path.read_bytes()
        parsed = read_traits(data.decode('utf-8-sig'), source, relative, values)
        for row in parsed:
            if row['id'] in seen:
                raise ValueError('Ambiguous surviving duplicate trait ' + row['id'])
            seen.add(row['id'])
            label = names.get('trait_' + row['id'], row['id'])
            row['label_fr'] = label if not any(mark in label for mark in ('[', '$', '#')) else row['id']
        rows.extend(parsed)
        receipts.append({'source': source, 'file': relative,
                         'sha256': hashlib.sha256(data).hexdigest(), 'traits': len(parsed)})
    return {'schema': 1, 'status': 'source_inventory_not_engine_tested',
            'scope': 'CK3 then AGOT, filename overlay only, no other mods or DLC enablement filtering',
            'profile': 'four promise choices using native honor/greed; other indirect effects unreviewed',
            'summary': dict(Counter(row['promise_input_status'] for row in rows)),
            'trait_count': len(rows), 'replaced_files': replaced,
            'files': receipts, 'script_value_files': value_receipts,
            'traits': sorted(rows, key=lambda row: (row['label_fr'].casefold(), row['id']))}


def markdown(report):
    lines = ['# Inventaire privé des traits — personnage qui décide', '',
             'Inventaire source CK3 + AGOT. Compatibilité moteur non validée.', '',
             f"{report['trait_count']} traits recensés. Tous restent à examiner pour leur contexte politique complet.", '',
             'Les colonnes honneur et avidité décrivent les entrées directes du profil de promesses actuel.',
             '0 signifie aucune contribution directe déclarée sur cet axe dans la définition examinée.',
             'Des effets indirects, conditionnels, de piste ou de compétence peuvent encore intervenir.',
             'Une valeur native ne constitue pas un bonus final ni une probabilité.', '']
    labels = {'native_axes_input': 'Entrée native utilisée',
              'zero_direct_axis_input': '0 direct · contexte à examiner',
              'conditional_or_unresolved': 'Conditionnel / non résolu'}
    groups = {'Personnalité hors dragons': [], 'Personnalité des dragons': [], 'Autres traits': []}
    for row in report['traits']:
        group = 'Autres traits'
        if row['personality_trait']:
            group = 'Personnalité des dragons' if row['id'].startswith('dragon_') else 'Personnalité hors dragons'
        groups[group].append(row)
    for heading, rows in groups.items():
        lines.extend([f'## {heading} — {len(rows)}', '',
                      '| Trait | Identifiant | Honneur | Avidité | Couverture des promesses | Autres axes déclarés |',
                      '|---|---|---:|---:|---|---|'])
        for row in rows:
            axes = row['direct_axes']
            unresolved = set(row['nested_axes'] + row['unresolved_fields'])
            def value(key):
                return 'À résoudre' if key in unresolved else f"{axes.get(key, 0):+g}"
            other = ', '.join(key.removeprefix('ai_') + f' {number:+g}'
                              for key, number in axes.items() if key not in ('ai_honor', 'ai_greed')) or '—'
            label = row.get('label_fr', row['id']).replace('|', '\\|')
            lines.append(f"| {label} | `{row['id']}` | {value('ai_honor')} | {value('ai_greed')} | {labels[row['promise_input_status']]} | {other} |")
        lines.append('')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ck3-root', type=Path, required=True)
    parser.add_argument('--agot-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='Private JSON output, outside tracked source')
    parser.add_argument('--markdown', type=Path, help='Optional private owner-readable inventory')
    args = parser.parse_args()
    try:
        report = inventory(args.ck3_root, args.agot_root)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        if args.markdown:
            args.markdown.parent.mkdir(parents=True, exist_ok=True)
            args.markdown.write_text(markdown(report), encoding='utf-8')
    except (ValueError, OSError, UnicodeError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps({'traits': report['trait_count'], 'summary': report['summary']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
