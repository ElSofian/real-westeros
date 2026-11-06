#!/usr/bin/env python3
"""Assemble a PRIVATE final-campaign folder from one verified public distribution."""
import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import zipfile

if __package__:
    from . import build_g1_native_choice as war
    from . import build_g3_native_confiscation as revoke
    from . import build_native_restitution as grant
    from . import build_distribution as distribution
    from .validate_mod import validate
else:
    import build_g1_native_choice as war
    import build_g3_native_confiscation as revoke
    import build_native_restitution as grant
    import build_distribution as distribution
    from validate_mod import validate

REPO = Path(__file__).resolve().parents[1]
BUILDERS = (war, revoke, grant)
TOOL_NAMES = ('prepare_final_campaign.py', 'build_g1_native_choice.py',
              'build_g3_native_confiscation.py', 'build_native_restitution.py',
              'build_distribution.py', 'validate_mod.py')
READY = 'PRIVATE_CAMPAIGN.json'
LIMIT = 128 * 1024 * 1024


def regular(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file():
        raise ValueError('Expected a regular, non-symlink file')
    return path.read_bytes()


def safe_name(name):
    p = PurePosixPath(name.rstrip('/'))
    if (not name or p.is_absolute() or '\\' in name or ':' in name
            or any(x in ('', '.', '..') for x in name.rstrip('/').split('/'))):
        raise ValueError('Unsafe archive path')
    return p


def unpack(archive, dest):
    """Verify all bytes before extraction. A checksum is integrity, not a signature."""
    archive = Path(archive).absolute()
    raw = regular(archive)
    checksum = regular(archive.with_suffix(archive.suffix + '.sha256')).decode('utf-8')
    match = re.fullmatch(r'([0-9a-f]{64})  ([^\r\n]+)\r?\n?', checksum)
    digest = hashlib.sha256(raw).hexdigest()
    if not match or match[1] != digest or match[2] != archive.name:
        raise ValueError('Distribution checksum does not match')
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if len(infos) > 5000 or sum(x.file_size for x in infos) > LIMIT:
            raise ValueError('Unexpected distribution size')
        names = [x.filename for x in infos]
        if len({n.rstrip('/').casefold() for n in names}) != len(names):
            raise ValueError('Duplicate or case-colliding archive path')
        for info in infos:
            safe_name(info.filename)
            kind = stat.S_IFMT(info.external_attr >> 16)
            if kind not in (0, stat.S_IFDIR, stat.S_IFREG) or info.flag_bits & 1:
                raise ValueError('Unsupported archive entry')
        manifest = json.loads(z.read('MANIFEST.json'))
        if manifest['schema'] != 1 or not re.fullmatch(r'[0-9a-f]{40}', manifest['commit']):
            raise ValueError('Invalid distribution manifest')
        rows = manifest['files']
        files = {r['path']: r for r in rows}
        if len(files) != len(rows) or set(n for n in names if not n.endswith('/')) != set(files) | {'MANIFEST.json'}:
            raise ValueError('Manifest coverage mismatch')
        required = set(distribution.DOCS) | set(distribution.G3_FILES) | {'mod/real_westeros.mod', 'mod/real_westeros/descriptor.mod'}
        if not required <= files.keys():
            raise ValueError('Incomplete distribution')
        for name in files:
            safe_name(name)
            if name not in required and not name.startswith('mod/real_westeros/'):
                raise ValueError('Unexpected distribution payload')
        for name, row in files.items():
            data = z.read(name)
            if len(data) != row['size'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                raise ValueError('Distribution file hash mismatch')
        # Never mix running tools with a different release, or execute ZIP-supplied code.
        for name in TOOL_NAMES:
            if z.read('tools/' + name) != regular(REPO / 'tools' / name):
                raise ValueError('Use the tools shipped with this exact distribution')
        for info in infos:
            target = dest / safe_name(info.filename)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(z.read(info))
    errors = validate(dest) + distribution.validate_g3_diagnostic(
        {name: (dest/name).read_bytes() for name in distribution.G3_FILES})
    if errors:
        raise ValueError('Extracted distribution failed structural validation')
    return manifest, digest


@contextmanager
def source_root(module, root):
    old = module.REPO, module.TEMPLATES
    module.REPO, module.TEMPLATES = root, root/'mod/real_westeros'
    try:
        yield
    finally:
        module.REPO, module.TEMPLATES = old


def prepare(archive, agot_root, output):
    original_root, original_out = Path(agot_root).absolute(), Path(output).absolute()
    for path in (original_root, original_out):
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('Symlinked input/output directory')
    root, out = original_root.resolve(), original_out.resolve()
    if (out.exists() or not out.parent.is_dir() or not root.is_dir()
            or out.is_relative_to(REPO) or REPO.is_relative_to(out)
            or out.is_relative_to(root) or root.is_relative_to(out)):
        raise ValueError('Choose a new external folder, outside AGOT and the checkout')
    with tempfile.TemporaryDirectory(prefix='rw-private-campaign-', dir=out.parent) as tmp:
        tmp = Path(tmp)
        base = tmp/'base'
        base.mkdir()
        manifest, digest = unpack(archive, base)
        adapters = []
        for module in BUILDERS:
            private = tmp/module.MOD_ID
            with source_root(module, base):
                receipt = module.build(root, private)
            # Each existing builder must attest to the exact base being assembled.
            for row in receipt['runtime_sources']:
                if hashlib.sha256((base/'mod/real_westeros'/row['path']).read_bytes()).hexdigest() != row['sha256']:
                    raise ValueError('Adapter/base runtime mismatch')
            for row in receipt['outputs']:
                if hashlib.sha256((private/module.MOD_ID/row['path']).read_bytes()).hexdigest() != row['sha256']:
                    raise ValueError('Adapter output mismatch')
            shutil.copytree(private/module.MOD_ID, base/'mod'/module.MOD_ID)
            shutil.copyfile(private/(module.MOD_ID+'.mod'), base/'mod'/(module.MOD_ID+'.mod'))
            evidence = base/'private_receipts'/module.MOD_ID
            evidence.mkdir(parents=True)
            shutil.copyfile(private/'receipt.json', evidence/'receipt.json')
            adapters.append({'id': module.MOD_ID, 'receipt': evidence.relative_to(base).as_posix()+'/receipt.json'})
        note = (
            'REAL WESTEROS — CAMPAGNE PRIVEE, NON TESTEE DANS CK3\n\n'
            'Ce dossier contient du code AGOT genere : ne jamais publier ou redistribuer.\n'
            'Aucune installation, sauvegarde ou configuration du launcher n’a ete modifiee.\n'
            'Copier seulement le contenu de mod/ dans le dossier mod des donnees utilisateur CK3,\n'
            'apres sauvegarde de vos anciens dossiers RW. Remplacer entierement les anciens\n'
            'adaptateurs ; ne pas les superposer. Ne pas activer d’anciens diagnostics G1.\n'
            'Ordre : AGOT, Real Westeros, rw_g1_native_choice, rw_g3_native_confiscation,\n'
            'rw_native_restitution. Verifier cet ordre dans le launcher.\n'
            'Les chemins des descripteurs sont relatifs, aucune installation n’est detectee.\n'
            'Ouvrir docs/FINAL_ENGINE_TESTS.md et docs/FINAL_CAMPAIGN_PACK.md avant la session.\n'
            'Regrouper les observations sur une sauvegarde jetable ; zero cas execute par cet outil.\n'
            'Les diagnostics separes sous diagnostics/ restent optionnels et inactifs.\n'
        )
        (base/'PRIVATE_README.txt').write_text(note, encoding='utf-8')
        files = [{'path': p.relative_to(base).as_posix(), 'size': p.stat().st_size,
                  'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                 for p in sorted(base.rglob('*')) if p.is_file()]
        ready = {'schema': 1, 'status': 'PRIVATE source assembly; NOT engine-tested',
                 'distribution_commit': manifest['commit'], 'distribution_sha256': digest,
                 'load_order': ['AGOT', 'real_westeros'] + [x['id'] for x in adapters],
                 'adapters': adapters, 'files': files, 'engine_cases_executed': 0}
        # Exclusive final directory creation: never overwrite an existing installation.
        out.mkdir()
        try:
            shutil.copytree(base, out, dirs_exist_ok=True)
            # Completion receipt is written last; a partial copy is not a ready pack.
            (out/READY).write_text(json.dumps(ready, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        except BaseException:
            shutil.rmtree(out)
            raise
    return ready


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--distribution', required=True, type=Path)
    parser.add_argument('--agot-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        receipt = prepare(args.distribution, args.agot_root, args.output)
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile):
        parser.exit(1, 'Assembly refused: check the matching ZIP/checksum/tools, reviewed AGOT inputs and new external output folder.\n')
    print('PRIVATE campaign folder ready: '+receipt['distribution_commit'])
    print('Base + three matching adapters; no installation changed; zero CK3 tests executed. Do not redistribute.')


if __name__ == '__main__':
    main()
