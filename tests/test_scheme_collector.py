"""Execute the standalone private collector on synthetic installs, never game assets."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/Collect-RealWesteros-Schemes.ps1'
PWSH = os.environ.get('RW_PWSH') or shutil.which('powershell.exe') or shutil.which('pwsh')


class SchemeCollectorTests(unittest.TestCase):
    def setUp(self):
        if not PWSH:
            if os.environ.get('RW_REQUIRE_POWERSHELL'):
                self.fail('PowerShell is required for this CI job')
            self.skipTest('PowerShell unavailable; execute the required PowerShell CI job')
        self.tmp = tempfile.TemporaryDirectory(prefix='rw collector ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.script = self.root / 'downloaded collector.ps1'
        shutil.copyfile(SCRIPT, self.script)
        self.ck3 = self.root / 'CK3 synthetic install'
        self.agot = self.root / 'AGOT synthetic mod'
        self.out = self.root / 'private results'
        self.put(self.ck3, 'game/common/schemes/empty.txt', '')
        self.put(self.ck3, 'game/common/schemes/types.txt', 'murder = { on_discovered = { helper_alpha_effect = yes } }')
        self.put(self.ck3, 'game/common/scripted_effects/alpha.txt', 'helper_alpha_effect = { helper_beta_trigger = yes }')
        self.put(self.ck3, 'game/common/scripted_triggers/beta.txt', 'helper_beta_trigger = { helper_gamma_effect = yes }')
        self.put(self.ck3, 'game/common/scripted_effects/gamma.txt', 'helper_gamma_effect = { is_alive = yes }')
        self.put(self.ck3, 'game/common/on_action/find.txt', 'synthetic_discovery = { trigger = { scheme_discovered = yes } }')
        self.put(self.ck3, 'game/common/secret_types/types.txt', 'secret_murder = { visible = yes }')
        self.put(self.ck3, 'game/events/related.txt', 'namespace = synthetic\nsynthetic.1 = { helper_alpha_effect = yes }')
        # Event is reached only by an explicit ID reference in another selected file.
        self.put(self.ck3, 'game/common/schemes/events.txt', 'other_scheme = { event = synthetic.1 }')
        self.put(self.ck3, 'game/events/unrelated.txt', '# murder comment\nplain = { text = "scheme string" gold = 1 }')
        self.put(self.ck3, 'game/events/private.ck3', 'PRIVATE SAVE')
        self.put(self.ck3, 'game/gfx/texture.txt', 'PRIVATE TEXTURE')
        self.put(self.ck3, 'game/settings.txt', 'PRIVATE SETTINGS')
        self.put(self.ck3, 'game/logs/error.log', 'PRIVATE LOG')
        self.put(self.agot, 'common/scripted_effects/alpha.txt', 'helper_alpha_effect = { is_ai = no }')
        self.put(self.agot, 'descriptor.mod', 'version="0.5.2.1"\nsupported_version="1.19.0.6"\npath="PRIVATE PATH"')
        self.env = dict(os.environ)
        for name in ('XDG_CACHE_HOME', 'XDG_CONFIG_HOME', 'XDG_DATA_HOME'):
            self.env[name] = str(self.root / name)

    def put(self, root, relative, text):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def run_collector(self, *extra, ck3=None, agot=None):
        return subprocess.run([PWSH, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
                               '-File', str(self.script), '-CK3Path', str(self.ck3 if ck3 is None else ck3),
                               '-AGOTPath', str(self.agot if agot is None else agot),
                               '-OutputDirectory', str(self.out), *extra],
                              capture_output=True, text=True, env=self.env, cwd=self.root, timeout=90)

    def collect(self, *args, **kwargs):
        result = self.run_collector(*args, **kwargs)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        archives = list(self.out.glob('*.zip'))
        self.assertEqual(1, len(archives))
        return zipfile.ZipFile(archives[0])

    def test_standalone_archive_integrity_dependencies_privacy_and_overlay(self):
        with self.collect() as zf:
            self.assertIsNone(zf.testzip())
            manifest_bytes = zf.read('MANIFEST.json')
            manifest = json.loads(manifest_bytes.decode('utf-8-sig'))
            records = manifest['files']
            self.assertEqual(len(records), manifest['selected_files'])
            expected = {'MANIFEST.json'}
            for item in records:
                name = item['source'] + '/' + item['path']
                expected.add(name)
                data = zf.read(name)
                self.assertEqual(item['size'], len(data))
                self.assertEqual(item['sha256'], hashlib.sha256(data).hexdigest())
            self.assertEqual(expected, set(zf.namelist()))
            for path in ('CK3/common/scripted_effects/alpha.txt', 'AGOT/common/scripted_effects/alpha.txt',
                         'CK3/common/scripted_triggers/beta.txt', 'CK3/common/scripted_effects/gamma.txt',
                         'CK3/events/related.txt'):
                self.assertIn(path, expected)
            self.assertNotIn('CK3/events/unrelated.txt', expected)
            self.assertNotIn('CK3/events/private.ck3', expected)
            self.assertFalse(any('settings' in n or 'gfx/' in n or 'logs/' in n for n in expected))
            self.assertNotIn('PRIVATE', b''.join(zf.read(n) for n in zf.namelist()).decode('utf-8'))
            self.assertNotIn(str(self.root), manifest_bytes.decode('utf-8'))
            self.assertEqual('0.5.2.1', manifest['descriptor_metadata']['AGOT']['version'])
            self.assertEqual('not_collected', manifest['ck3_executable_version'])
            self.assertIn('AGOT/common/schemes', manifest['missing_groups'])

    def test_accepts_direct_game_directory(self):
        with self.collect(ck3=self.ck3 / 'game') as zf:
            self.assertIn('CK3/common/schemes/types.txt', zf.namelist())

    def test_dependency_frontier_is_explicit_and_sources_remain_unverified(self):
        with self.collect('-DependencyDepth', '0') as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            self.assertIn('CK3/common/scripted_effects/alpha.txt', manifest['dependency_frontier'])
            self.assertNotIn('CK3/common/scripted_effects/alpha.txt', zf.namelist())
            self.assertEqual('candidates_only_not_engine_evidence', manifest['status'])

    def test_invalid_roots_fail_without_partial_archive(self):
        result = self.run_collector(ck3=self.root / 'missing')
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(list(self.out.glob('*.zip')))
        result = self.run_collector(agot=self.ck3 / 'game')
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(list(self.out.glob('*.zip')))

    def test_missing_native_scheme_folder_fails(self):
        shutil.rmtree(self.ck3 / 'game/common/schemes')
        result = self.run_collector()
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(list(self.out.glob('*.zip')))

    def test_link_cannot_collect_external_file(self):
        private = self.put(self.root, 'outside.txt', 'murder = { PRIVATE = yes }')
        link = self.agot / 'common/scripted_effects/external.txt'
        try:
            link.symlink_to(private)
        except OSError:
            self.skipTest('Symlink creation unavailable on this host')
        with self.collect() as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            self.assertNotIn('AGOT/common/scripted_effects/external.txt', zf.namelist())
            self.assertIn('AGOT/common/scripted_effects/external.txt', manifest['excluded_links'])

    def test_source_limit_has_no_partial_zip(self):
        self.put(self.ck3, 'game/common/schemes/large.txt', '# padding\n' * 120000 + '\nmurder = {}')
        result = self.run_collector('-MaxSourceMiB', '1')
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(list(self.out.glob('*.zip')))

    def test_source_tree_is_unchanged_and_second_run_never_overwrites(self):
        before = {str(p.relative_to(self.ck3)): p.read_bytes() for p in self.ck3.rglob('*') if p.is_file()}
        with self.collect():
            pass
        first = next(self.out.glob('*.zip'))
        original = first.read_bytes()
        result = self.run_collector()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(2, len(list(self.out.glob('*.zip'))))
        self.assertEqual(original, first.read_bytes())
        after = {str(p.relative_to(self.ck3)): p.read_bytes() for p in self.ck3.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_output_inside_installation_is_rejected_without_writes(self):
        self.out = self.ck3 / 'private-output'
        result = self.run_collector()
        self.assertNotEqual(0, result.returncode)
        self.assertIn('en dehors des installations', result.stderr)
        self.assertFalse(self.out.exists())
