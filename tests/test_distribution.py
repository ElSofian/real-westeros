"""Exercise actual ZIP building, payload integrity, and private-file exclusion."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from tools.build_distribution import DOCS, G3_FILES, build
from tools.validate_mod import validate

REPO = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        shutil.copytree(REPO / 'mod', self.root / 'mod')
        for name in (*DOCS, *G3_FILES):
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, dest)
        self.git('init', '-q')
        self.commit()
        self.output = Path(self.tmp.name) / 'package.zip'

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.PIPE)

    def commit(self):
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'Fixture')

    def test_real_payload_manifest_checksum_and_reproducibility(self):
        digest = build(self.root, self.output)
        second = self.output.with_name('second.zip')
        self.assertEqual(digest, build(self.root, second))
        self.assertEqual(self.output.read_bytes(), second.read_bytes())
        self.assertEqual(digest, hashlib.sha256(self.output.read_bytes()).hexdigest())
        self.assertEqual(f'{digest}  package.zip\n', self.output.with_suffix('.zip.sha256').read_text())
        with zipfile.ZipFile(self.output) as zf:
            self.assertIsNone(zf.testzip())
            manifest = json.loads(zf.read('MANIFEST.json'))
            self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), manifest['commit'])
            self.assertIn('not engine-tested', manifest['status'])
            payload_names = {r['path'] for r in manifest['files']}
            self.assertEqual(payload_names | {'MANIFEST.json'}, {n for n in zf.namelist() if not n.endswith('/')})
            for record in manifest['files']:
                data = zf.read(record['path'])
                self.assertEqual(record['size'], len(data))
                self.assertEqual(record['sha256'], hashlib.sha256(data).hexdigest())
                self.assertEqual((self.root / record['path']).read_bytes(), data)
            zf.extractall(Path(self.tmp.name) / 'extracted')
        self.assertEqual([], validate(Path(self.tmp.name) / 'extracted'))

    def test_untracked_private_files_and_claims_are_not_packaged(self):
        marker = 'RW_TEST_UNPUBLISHED_PAYLOAD_f3a8d51a'
        (self.root / 'mod/real_westeros/private.txt').write_text(marker)
        (self.root / '.env').write_text(marker)
        claim = self.root / '.github/task-claims/RW-010.json'
        claim.parent.mkdir(parents=True)
        claim.write_text(marker)
        self.git('add', '.github')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Claim fixture')
        build(self.root, self.output)
        with zipfile.ZipFile(self.output) as zf:
            self.assertNotIn('mod/real_westeros/private.txt', zf.namelist())
            self.assertFalse(any('.github' in n or '.env' in n for n in zf.namelist()))
            # Public documentation can legitimately say PRIVATE; reject the test payload.
            self.assertFalse(any(marker.encode() in zf.read(n) for n in zf.namelist()))

    def test_tracked_unexpected_payload_fails_without_archive(self):
        for name in ('private.txt', 'rw_test.ck3', 'rw_test.zip'):
            with self.subTest(name=name):
                path = self.root / 'mod/real_westeros' / name
                path.write_text('PRIVATE')
                self.commit()
                with self.assertRaisesRegex(ValueError, 'Unexpected mod content'):
                    build(self.root, self.output)
                self.assertFalse(self.output.exists())
                path.unlink()
                self.commit()

    def test_symlink_cannot_exfiltrate_file(self):
        private = Path(self.tmp.name) / 'secret.txt'
        private.write_text('PRIVATE')
        link = self.root / 'mod/real_westeros/events/rw_symlink.txt'
        link.symlink_to(private)
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Non-regular'):
            build(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_dirty_payload_rejected_but_dirty_unrelated_notes_ignored(self):
        source = self.root / 'mod/real_westeros/events/rw_reconciliation_events.txt'
        original = source.read_bytes()
        source.write_text('broken')
        with self.assertRaisesRegex(ValueError, 'Commit changes'):
            build(self.root, self.output)
        source.write_bytes(original)
        (self.root / 'private-notes.txt').write_text('PRIVATE')
        build(self.root, self.output)

    def test_invalid_committed_script_fails_staged_validation(self):
        (self.root / 'mod/real_westeros/events/rw_broken.txt').write_text('rw_broken = {')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'structural validation failed'):
            build(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_preserved(self):
        self.output.write_bytes(b'keep me')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            build(self.root, self.output)
        self.assertEqual(b'keep me', self.output.read_bytes())

    def test_missing_committed_document_fails(self):
        (self.root / 'docs/INSTALL.md').unlink()
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Missing committed distribution input'):
            build(self.root, self.output)

    def test_g3_diagnostic_is_separate_and_included_without_base_hooks(self):
        build(self.root, self.output)
        with zipfile.ZipFile(self.output) as zf:
            for name in G3_FILES:
                self.assertIn(name, zf.namelist())
            for name in zf.namelist():
                if name.startswith('mod/real_westeros/') and not name.endswith('/'):
                    self.assertNotIn(b'rw_g3_trace', zf.read(name))
            outer = zf.read('diagnostics/g3_house_trace/mod/rw_g3_house_trace.mod')
            self.assertIn(b'path="mod/rw_g3_house_trace"', outer)

    def test_g3_diagnostic_rejects_bad_launcher_and_unbalanced_script(self):
        launcher = self.root / 'diagnostics/g3_house_trace/mod/rw_g3_house_trace.mod'
        original = launcher.read_text()
        launcher.write_text(original.replace('mod/rw_g3_house_trace', '/invalid/launcher'))
        self.commit()
        with self.assertRaisesRegex(ValueError, 'diagnostic launcher path'):
            build(self.root, self.output)
        self.assertFalse(self.output.exists())
        launcher.write_text(original)
        script = self.root / 'diagnostics/g3_house_trace/mod/rw_g3_house_trace/common/on_action/rw_g3_trace_on_actions.txt'
        script.write_text(script.read_text() + '{')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'unclosed brace'):
            build(self.root, self.output)
        self.assertFalse(self.output.exists())
