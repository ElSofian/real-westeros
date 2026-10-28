#!/usr/bin/env python3
"""Build an original-source experimental ZIP from committed HEAD, not local files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import zipfile

if __package__:
    from .validate_mod import REQUIRED_DIRS, descriptor as parse_descriptor, validate, brace_errors
else:
    from validate_mod import REQUIRED_DIRS, descriptor as parse_descriptor, validate, brace_errors

DOCS = ('README.md', 'docs/INSTALL.md', 'docs/INTEGRATED_BUILD.md',
        'docs/FINAL_ENGINE_TESTS.md', 'docs/TEST_PLAN_G1.md',
        'docs/G3_HOUSE_SANCTIONS.md', 'docs/G3_SOURCE_RECEIPT.json',
        'docs/RW010_HOUSE_AFFAIRS.md', 'docs/RW010_HOUSE_TERMS.md',
        'docs/RW010_DELIVERY_TERMS.md')
PREFIX = 'mod/real_westeros/'
G3_ROOT = 'diagnostics/g3_house_trace/mod/'
G3_FILES = tuple(G3_ROOT + name for name in (
    'rw_g3_house_trace.mod', 'rw_g3_house_trace/descriptor.mod',
    'rw_g3_house_trace/common/character_interactions/rw_g3_trace_interactions.txt',
    'rw_g3_house_trace/common/on_action/rw_g3_trace_on_actions.txt',
    'rw_g3_house_trace/common/scripted_effects/rw_g3_trace_effects.txt',
    'rw_g3_house_trace/common/scripted_triggers/rw_g3_trace_triggers.txt',
    'rw_g3_house_trace/localization/english/rw_g3_trace_l_english.yml',
    'rw_g3_house_trace/localization/french/rw_g3_trace_l_french.yml',
))


def validate_g3_diagnostic(files):
    """Check the separately installed original diagnostic; never load it as the base mod."""
    errors = []
    outer = G3_ROOT + 'rw_g3_house_trace.mod'
    inner = G3_ROOT + 'rw_g3_house_trace/descriptor.mod'
    external = parse_descriptor(files[outer].decode('utf-8-sig'), outer, errors)
    internal = parse_descriptor(files[inner].decode('utf-8-sig'), inner, errors)
    for key in ('name', 'version', 'supported_version'):
        if external.get(key) != internal.get(key):
            errors.append('Optional G3 diagnostic descriptor mismatch')
    if external.get('path') != 'mod/rw_g3_house_trace' or 'path' in internal:
        errors.append('Optional G3 diagnostic launcher path is invalid')
    for name in G3_FILES:
        text = files[name].decode('utf-8-sig')
        if name.endswith(('.txt', '.mod')):
            errors.extend(f'{name}: {error}' for error in brace_errors(text))
        if name.endswith('.yml'):
            lang = 'french' if '/french/' in name else 'english'
            if not files[name].startswith(b'\xef\xbb\xbf') or not text.startswith('l_' + lang + ':'):
                errors.append('Optional G3 diagnostic localization encoding/header is invalid')
    return errors


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def payload(root):
    """Read committed regular blobs in a narrow allowlist; never follow symlinks."""
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    dirty = git(root, 'diff', 'HEAD', '--name-only', '--', 'mod', *DOCS, *G3_FILES)
    if dirty.strip():
        raise ValueError('Commit changes to distribution inputs before building')
    files = {}
    for row in git(root, 'ls-tree', '-r', '-z', 'HEAD', '--', 'mod', *DOCS, *G3_FILES).split(b'\0'):
        if not row:
            continue
        meta, raw_name = row.split(b'\t', 1)
        mode, kind, blob = meta.decode().split()
        name = raw_name.decode('utf-8')
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name:
            raise ValueError('Unsafe distribution path')
        if name not in (*DOCS, *G3_FILES) and name != 'mod/real_westeros.mod' and not name.startswith(PREFIX):
            raise ValueError(f'Unexpected mod path: {name}')
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError(f'Non-regular distribution input: {name}')
        if path.name == '.gitkeep':
            continue
        if name.startswith(PREFIX) and name != PREFIX + 'descriptor.mod':
            relative = name[len(PREFIX):]
            valid = (re.fullmatch(r'(common/(character_interactions|scripted_triggers|scripted_effects|opinion_modifiers|story_cycles|on_action)|events)/rw_[\w]+\.txt', relative)
                     or re.fullmatch(r'localization/(english|french)/rw_[\w]+\.yml', relative))
            if not valid:
                raise ValueError(f'Unexpected mod content: {name}')
        files[name] = git(root, 'cat-file', 'blob', blob)
    for required in (*DOCS, *G3_FILES, 'mod/real_westeros.mod', PREFIX + 'descriptor.mod'):
        if required not in files:
            raise ValueError(f'Missing committed distribution input: {required}')
    return head, files


def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    checksum = output.with_suffix(output.suffix + '.sha256')
    if output.suffix.lower() != '.zip':
        raise ValueError('Output must have a .zip suffix')
    if output.exists() or checksum.exists():
        raise ValueError('Output or checksum already exists; choose a new output path')
    head, files = payload(root)
    # Keep empty scaffold directories while excluding .gitkeep metadata.
    dirs = {'mod/real_westeros/' + folder + '/' for folder in REQUIRED_DIRS}
    for name in files:
        dirs.update(str(parent) + '/' for parent in PurePosixPath(name).parents if str(parent) != '.')
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        for directory in dirs:
            (staged / directory).mkdir(parents=True, exist_ok=True)
        for name, data in files.items():
            (staged / name).write_bytes(data)
        errors = validate(staged) + validate_g3_diagnostic(files)
        if errors:
            raise ValueError('Distribution structural validation failed:\n' + '\n'.join(errors))
    metadata = parse_descriptor(files[PREFIX + 'descriptor.mod'].decode('utf-8-sig'),
                                PREFIX + 'descriptor.mod', [])
    manifest = {
        'schema': 1, 'commit': head,
        'status': 'experimental; static-checked; not engine-tested',
        'version': metadata['version'],
        'supported_version_target': metadata['supported_version'],
        'files': [{'path': name, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(files.items())],
    }
    files['MANIFEST.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Fixed metadata and sorted entries make repeated builds identical in one toolchain.
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        archive = Path(tmp) / 'distribution.zip'
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for name in sorted(dirs | set(files)):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = ((0o40755 << 16) | 0x10) if name.endswith('/') else 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, b'' if name.endswith('/') else files[name], compresslevel=9)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        # Exclusive creation avoids overwriting another process's output.
        with output.open('xb') as dest:
            dest.write(archive.read_bytes())
        with checksum.open('x', encoding='utf-8') as dest:
            dest.write(f'{digest}  {output.name}\n')
    return digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, default=Path('build/RealWesteros-experimental.zip'))
    args = parser.parse_args()
    try:
        digest = build(args.root, args.output)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'ERROR: {error}\n')
    print(f'{digest}  {args.output}')
    print('Experimental distribution: structural checks only; no CK3 runtime proof.')


if __name__ == '__main__':
    main()
