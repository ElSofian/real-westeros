#!/usr/bin/env python3
"""Conservative structural checks for Real Westeros (not a CK3 parser)."""

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys

MOD_DIR = Path('mod/real_westeros')
OUTER = Path('mod/real_westeros.mod')
SCRIPT_FOLDERS = {
    'common/character_interactions',
    'common/scripted_triggers',
    'common/scripted_effects',
    'common/script_values',
    'common/character_memory_types',
}
SCRIPT_SUFFIXES = {'.txt', '.mod', '.gui', '.gfx', '.asset'}
FORBIDDEN_SUFFIXES = {'.zip', '.7z', '.rar', '.exe', '.dll', '.ck3', '.sav'}
REQUIRED_DIRS = (
    'common/character_interactions', 'common/scripted_triggers',
    'common/scripted_effects', 'common/on_action',
    'events', 'localization/english',
)
META_KEYS = ('name', 'version', 'supported_version')
ASSIGNMENT = re.compile(r'^\s*([A-Za-z_][\w.]*)\s*=\s*"([^"\r\n]*)"\s*$')
DEFINITION = re.compile(r'^\s*([A-Za-z_][\w.-]*)\s*=\s*\{')
LOCALIZATION = re.compile(r'^\s*([A-Za-z_][\w.-]*):\d*\s+')


def clean_script(text):
    """Mask comments and strings, retaining newlines and brace positions."""
    output = []
    quoted = False
    escaped = False
    comment = False
    for ch in text:
        if ch == '\n':
            comment = False
            if quoted:
                output.append(' ')
                continue
            output.append(ch)
            continue
        if comment:
            output.append(' ')
        elif quoted:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                quoted = False
            output.append(' ')
        elif ch == '#':
            comment = True
            output.append(' ')
        elif ch == '"':
            quoted = True
            output.append(' ')
        else:
            output.append(ch)
    return ''.join(output), quoted


def brace_errors(text):
    clean, unterminated = clean_script(text)
    errors = []
    depth = 0
    for line_number, line in enumerate(clean.splitlines(), 1):
        for char in line:
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth < 0:
                    errors.append(f'line {line_number}: unexpected closing brace')
                    depth = 0
    if depth:
        errors.append(f'{depth} unclosed brace(s)')
    if unterminated:
        errors.append('unterminated quoted string')
    return errors


def definitions(text):
    """Find only top-level block definitions; nested repeated keys are normal."""
    clean, _ = clean_script(text)
    depth = 0
    for line in clean.splitlines():
        if depth == 0:
            match = DEFINITION.match(line)
            if match:
                yield match.group(1)
        depth += line.count('{') - line.count('}')


def descriptor(text, path, errors):
    fields = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('tags=') or stripped in ('{', '}') or stripped.startswith('"'):
            continue
        match = ASSIGNMENT.match(line)
        if not match:
            errors.append(f'{path}: unsupported descriptor line: {stripped}')
            continue
        key, value = match.groups()
        if key in fields:
            errors.append(f'{path}: duplicate descriptor key {key}')
        fields[key] = value
    for key in META_KEYS:
        if not fields.get(key):
            errors.append(f'{path}: missing {key}')
    return fields


def validate(root):
    errors = []
    mod = root / MOD_DIR
    for path in (root / OUTER, mod / 'descriptor.mod'):
        if not path.is_file():
            errors.append(f'{path.relative_to(root)}: missing descriptor')
    for directory in REQUIRED_DIRS:
        if not (mod / directory).is_dir():
            errors.append(f'{MOD_DIR / directory}: missing directory')
    if not mod.is_dir():
        return errors

    descriptors = {}
    localization_keys = defaultdict(dict)
    definitions_by_folder = defaultdict(dict)
    for path in sorted((root / 'mod').rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if path.is_symlink():
            errors.append(f'{relative}: symlinks are not supported')
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f'{relative}: forbidden archive/executable/save type')
            continue
        if path.name == '.gitkeep':
            continue
        try:
            text = path.read_text(encoding='utf-8-sig' if path.suffix == '.yml' else 'utf-8')
        except (UnicodeError, OSError):
            errors.append(f'{relative}: invalid UTF-8 or unreadable file')
            continue
        if '\0' in text:
            errors.append(f'{relative}: NUL byte in text file')
            continue
        if path.suffix in SCRIPT_SUFFIXES:
            errors.extend(f'{relative}: {problem}' for problem in brace_errors(text))
        if relative in (OUTER, MOD_DIR / 'descriptor.mod'):
            descriptors[relative] = descriptor(text, relative, errors)
        if path.suffix == '.txt':
            folder = path.parent.relative_to(mod).as_posix()
            if folder in SCRIPT_FOLDERS:
                for name in definitions(text):
                    existing = definitions_by_folder[folder].get(name)
                    if existing:
                        errors.append(f'{relative}: duplicate top-level {name} (also in {existing})')
                    else:
                        definitions_by_folder[folder][name] = relative
        if path.suffix == '.yml' and 'localization' in relative.parts:
            lines = text.splitlines()
            header = lines[0].strip() if lines else ''
            if not re.fullmatch(r'l_[a-z_]+:', header):
                errors.append(f'{relative}: missing localization language header')
                continue
            for line_no, line in enumerate(lines[1:], 2):
                if not line.strip() or line.lstrip().startswith('#'):
                    continue
                match = LOCALIZATION.match(line)
                if not match:
                    errors.append(f'{relative}:{line_no}: invalid localization key line')
                    continue
                key = match.group(1)
                previous = localization_keys[header].get(key)
                if previous:
                    errors.append(f'{relative}:{line_no}: duplicate {key} (also in {previous})')
                else:
                    localization_keys[header][key] = f'{relative}:{line_no}'

    outer = descriptors.get(OUTER, {})
    inner = descriptors.get(MOD_DIR / 'descriptor.mod', {})
    for key in META_KEYS:
        if key in outer and key in inner and outer[key] != inner[key]:
            errors.append(f'descriptors: {key} differs between outer and inner')
    if outer.get('path') != 'mod/real_westeros':
        errors.append('outer descriptor: expected relative path="mod/real_westeros"')
    if 'path' in inner:
        errors.append('inner descriptor: path must be omitted')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print('PASS: Real Westeros structural checks (not CK3 engine validation)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
