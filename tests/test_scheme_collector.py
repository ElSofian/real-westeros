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

    def seed_title_routes(self):
        # Deliberately unusual filenames: discovery must inspect definitions, not guess names.
        self.put(self.ck3, 'game/common/character_interactions/unusual.txt',
                 'grant_titles_interaction = { can_be_granted_titles_by = yes route_alpha_effect = yes feudal_elective = yes }')
        self.put(self.agot, 'common/character_interactions/override.txt',
                 'grant_titles_interaction = { can_be_granted_titles_by = yes }')
        self.put(self.ck3, 'game/common/scripted_triggers/eligibility.txt',
                 'can_be_granted_titles_by = { is_alive = yes }')
        self.put(self.ck3, 'game/common/scripted_effects/route_alpha.txt',
                 'route_alpha_effect = { route_beta_trigger = yes }')
        self.put(self.ck3, 'game/common/scripted_triggers/route_beta.txt',
                 'route_beta_trigger = { is_alive = yes }')
        self.put(self.ck3, 'game/common/laws/laws.txt',
                 'synthetic_law = { election_type = feudal_elective }')
        self.put(self.agot, 'common/laws/laws.txt',
                 'synthetic_law = { election_type = missing_example_elective }')
        self.put(self.ck3, 'game/common/succession_election/types.txt',
                 'feudal_elective = { candidate_trigger = { is_alive = yes } }')
        self.put(self.agot, 'common/succession_election/nested/types.txt',
                 'feudal_elective = { candidate_trigger = { is_adult = yes } }')
        self.put(self.ck3, 'game/common/character_interactions/comment_only.txt',
                 '# grant_titles_interaction = {}\nplain = { text = "election_type = private_example" }')
        self.put(self.ck3, 'game/common/character_interactions/save.ck3', 'PRIVATE SAVE grant_titles_interaction')

    def test_title_profile_archive_integrity_overlay_and_privacy(self):
        self.seed_title_routes()
        with self.collect('-Profile', 'TitleRoutes') as zf:
            manifest_bytes = zf.read('MANIFEST.json')
            manifest = json.loads(manifest_bytes.decode('utf-8-sig'))
            self.assertEqual('TitleRoutes', manifest['profile'])
            self.assertEqual('private_title_route_source_candidates', manifest['kind'])
            self.assertEqual('lexical_candidates_not_enforcement_or_load_order_evidence', manifest['title_route_probe']['status'])
            self.assertEqual('candidates_only_not_engine_evidence', manifest['status'])
            names = {'MANIFEST.json'}
            total = 0
            for record in manifest['files']:
                name = record['source'] + '/' + record['path']
                names.add(name)
                data = zf.read(name)
                total += len(data)
                self.assertEqual(len(data), record['size'])
                self.assertEqual(hashlib.sha256(data).hexdigest(), record['sha256'])
            self.assertEqual(names, set(zf.namelist()))
            self.assertEqual(len(names) - 1, manifest['selected_files'])
            self.assertEqual(total, manifest['selected_bytes'])
            grants = manifest['title_route_probe']['grant_interaction_definitions']
            self.assertEqual({'CK3', 'AGOT'}, {x['source'] for x in grants})
            self.assertTrue(all(x['identifier'] == 'grant_titles_interaction' for x in grants))
            self.assertEqual({'CK3', 'AGOT'}, {x['source'] for x in manifest['title_route_probe']['election_definitions']})
            self.assertEqual(['missing_example_elective'], manifest['title_route_probe']['missing_election_identifiers'])
            self.assertTrue(manifest['title_route_probe']['grant_eligibility_definitions'])
            self.assertIn('common/succession_election', manifest['scanned_groups'])
            self.assertNotIn('common/schemes', manifest['scanned_groups'])
            self.assertFalse(any('/schemes/' in n or '/secret_types/' in n or n.endswith('.ck3') for n in names))
            self.assertNotIn('PRIVATE', b''.join(zf.read(n) for n in names).decode('utf-8'))
            self.assertNotIn(str(self.root), manifest_bytes.decode('utf-8'))
            self.assertIsNone(zf.testzip())
            self.assertTrue(next(self.out.glob('*.zip')).name.startswith('RealWesteros-TitleRoutes-PRIVATE-'))

    def test_title_profile_default_depth_is_one_and_frontier_explicit(self):
        self.seed_title_routes()
        with self.collect('-Profile', 'TitleRoutes') as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            self.assertEqual(1, manifest['dependency_depth'])
            self.assertIn('CK3/common/scripted_effects/route_alpha.txt', zf.namelist())
            self.assertNotIn('CK3/common/scripted_triggers/route_beta.txt', zf.namelist())
            self.assertIn('CK3/common/scripted_triggers/route_beta.txt', manifest['dependency_frontier'])

    def test_title_profile_honors_explicit_depth_zero(self):
        self.seed_title_routes()
        with self.collect('-Profile', 'TitleRoutes', '-DependencyDepth', '0') as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            self.assertEqual(0, manifest['dependency_depth'])
            self.assertNotIn('CK3/common/scripted_effects/route_alpha.txt', zf.namelist())
            self.assertIn('CK3/common/scripted_effects/route_alpha.txt', manifest['dependency_frontier'])

    def test_title_profile_does_not_require_scheme_definitions(self):
        self.seed_title_routes()
        shutil.rmtree(self.ck3 / 'game/common/schemes')
        with self.collect('-Profile', 'TitleRoutes', ck3=self.ck3 / 'game') as zf:
            self.assertIn('CK3/common/succession_election/types.txt', zf.namelist())

    def test_title_missing_grant_definition_not_inferred_from_calls(self):
        self.seed_title_routes()
        (self.ck3 / 'game/common/character_interactions/unusual.txt').unlink()
        (self.agot / 'common/character_interactions/override.txt').unlink()
        self.put(self.ck3, 'game/common/scripted_effects/caller.txt',
                 'caller_effect = { interaction = grant_titles_interaction }')
        with self.collect('-Profile', 'TitleRoutes') as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            self.assertEqual([], manifest['title_route_probe']['grant_interaction_definitions'])
            self.assertTrue(manifest['title_route_probe']['grant_eligibility_definitions'])

    def test_title_missing_election_not_inferred_from_same_name_helper(self):
        self.seed_title_routes()
        shutil.rmtree(self.ck3 / 'game/common/succession_election')
        shutil.rmtree(self.agot / 'common/succession_election')
        self.put(self.ck3, 'game/common/scripted_triggers/wrong_group.txt', 'feudal_elective = { is_alive = yes }')
        with self.collect('-Profile', 'TitleRoutes') as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            probe = manifest['title_route_probe']
            self.assertEqual([], probe['election_definitions'])
            self.assertIn('feudal_elective', probe['missing_election_identifiers'])
            self.assertIn('CK3/common/succession_election', manifest['missing_groups'])
            self.assertIn('CK3/common/scripted_triggers/wrong_group.txt', zf.namelist())

    def test_title_comments_and_strings_are_not_candidate_definitions_or_types(self):
        self.seed_title_routes()
        self.put(self.ck3, 'game/common/laws/strings.txt',
                 '# election_type = commented_type\nstring_law_example = { text = "election_type = quoted_type" }')
        with self.collect('-Profile', 'TitleRoutes') as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            self.assertNotIn('CK3/common/character_interactions/comment_only.txt', zf.namelist())
            ids = {x['identifier'] for x in manifest['title_route_probe']['election_references']}
            self.assertEqual({'feudal_elective', 'missing_example_elective'}, ids)

    def test_title_sources_unchanged_and_second_archive_distinct(self):
        self.seed_title_routes()
        before = {str(p.relative_to(self.root)): p.read_bytes() for r in (self.ck3, self.agot) for p in r.rglob('*') if p.is_file()}
        with self.collect('-Profile', 'TitleRoutes'):
            pass
        first = next(self.out.glob('*.zip'))
        original = first.read_bytes()
        result = self.run_collector('-Profile', 'TitleRoutes')
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(2, len(list(self.out.glob('*.zip'))))
        self.assertEqual(original, first.read_bytes())
        after = {str(p.relative_to(self.root)): p.read_bytes() for r in (self.ck3, self.agot) for p in r.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_title_invalid_profile_missing_required_group_or_size_limit_has_no_zip(self):
        self.seed_title_routes()
        for extra in (('-Profile', 'not-a-profile'),):
            result = self.run_collector(*extra)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse(list(self.out.glob('*.zip')))
        self.put(self.ck3, 'game/common/laws/large.txt', '# padding\n' * 120000)
        result = self.run_collector('-Profile', 'TitleRoutes', '-MaxSourceMiB', '1')
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(list(self.out.glob('*.zip')))
        shutil.rmtree(self.ck3 / 'game/common/character_interactions')
        result = self.run_collector('-Profile', 'TitleRoutes')
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(list(self.out.glob('*.zip')))

    def test_title_link_cannot_supply_external_election_definition(self):
        self.seed_title_routes()
        private = self.put(self.root, 'outside-election.txt', 'outside_elective = { PRIVATE = yes }')
        link = self.agot / 'common/succession_election/external.txt'
        try:
            link.symlink_to(private)
        except OSError:
            self.skipTest('Symlink creation unavailable on this host')
        with self.collect('-Profile', 'TitleRoutes') as zf:
            manifest = json.loads(zf.read('MANIFEST.json').decode('utf-8-sig'))
            self.assertNotIn('AGOT/common/succession_election/external.txt', zf.namelist())
            self.assertIn('AGOT/common/succession_election/external.txt', manifest['excluded_links'])
            self.assertNotIn('outside_elective', {x['identifier'] for x in manifest['title_route_probe']['election_definitions']})
