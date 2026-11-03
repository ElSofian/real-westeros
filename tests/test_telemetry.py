"""Real source contracts and offline parser negative paths; no CK3 simulation."""
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tools import report_telemetry as report
from tools import verify_telemetry as audit

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / 'mod/real_westeros/common/scripted_effects/rw_telemetry_effects.txt'
REGISTRY = json.loads((ROOT / 'docs/TELEMETRY_HOOKS.json').read_text())


def marker(stage, family='justice', action='execute', control='ai'):
    if stage in {'start', 'stop', 'truncated'}:
        family, action, control = 'telemetry', 'session', 'unknown'
    return f'[ignored header] RW_TM1 family={family} action={action} stage={stage} control={control}\n'


def csv_samples(rows=None):
    rows = rows or ['0,10,1000,2000,3,4,running', '2,13,1200,1900,4,4,running',
                    '4,14,1100,2500,3,4,running']
    return io.StringIO('elapsed_seconds,cpu_seconds,working_set_bytes,private_bytes,threads,logical_processors,status\n' + '\n'.join(rows))


class TelemetrySourceTests(unittest.TestCase):
    def test_noninterference_and_metadata_audit(self):
        self.assertEqual([], audit.verify())

    def test_native_guard_mutation_rejected(self):
        p = next(iter(REGISTRY['gameplay_sha256']))
        source = (ROOT / p).read_text()
        changed = source.replace('rw_ja_can_attempt_trigger = yes', 'rw_ja_can_attempt_trigger = no')
        self.assertNotEqual(source, changed)
        self.assertNotEqual(REGISTRY['gameplay_sha256'][p], audit.gameplay_digest(changed))

    def test_native_dispatch_mutation_rejected(self):
        p = 'mod/real_westeros/common/scripted_effects/rw_native_sentence_effects.txt'
        source = (ROOT / p).read_text().replace('send_threshold = decline', 'send_threshold = accept')
        self.assertNotEqual(REGISTRY['gameplay_sha256'][p], audit.gameplay_digest(source))

    def test_logger_cannot_add_native_cost(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for p in [*REGISTRY['gameplay_sha256'], str(LIB.relative_to(ROOT)), 'docs/TELEMETRY_HOOKS.json']:
                dest = root / p
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / p, dest)
            path = root / LIB.relative_to(ROOT)
            path.write_text(path.read_text().replace('save_scope_as = rw_tm_actor', 'add_gold = -5\n save_scope_as = rw_tm_actor'))
            self.assertTrue(any('unapproved operation' in x for x in audit.verify(root)))

    def test_trace_condition_cannot_gate_gameplay(self):
        p = next(iter(REGISTRY['gameplay_sha256']))
        source = (ROOT / p).read_text().replace('rw_ja_can_attempt_trigger = yes', 'rw_tm_enabled_trigger = yes rw_ja_can_attempt_trigger = yes')
        self.assertNotEqual(REGISTRY['gameplay_sha256'][p], audit.gameplay_digest(source))

    def test_commit_after_consumption_before_native_dispatch(self):
        for prefix, filename, receipt in [('ja', 'rw_justice_action_effects.txt', 'rw_ja_dispatched_on'),
                                          ('jp', 'rw_native_sentence_effects.txt', 'rw_jp_dispatched_on')]:
            text = (LIB.parent / filename).read_text()
            self.assertLess(text.index(receipt), text.index('rw_tm_commit_effect'))
            self.assertLess(text.index('rw_tm_commit_effect'), text.index('run_interaction'))

    def test_three_bundle_operations_have_distinct_keys(self):
        text = (LIB.parent / 'rw_multi_action_effects.txt').read_text()
        for key in ('bundle_gold', 'bundle_support', 'bundle_release'):
            self.assertEqual(1, text.count('KEY = ' + key))

    def test_fixed_budget_and_expiry_default_off(self):
        text = LIB.read_text()
        self.assertIn('name = rw_tm_budget value = 5000', text)
        self.assertIn('name = rw_tm_enabled value = flag:yes days = 90', text)
        self.assertIn('change_global_variable = { name = rw_tm_budget add = -1 }', text)
        for path in (ROOT / 'mod').rglob('*.txt'):
            if path != LIB:
                self.assertNotIn('rw_tm_start_effect =', path.read_text(encoding='utf-8-sig'))

    def test_both_actor_controls_same_observation_only(self):
        text = LIB.read_text()
        self.assertIn('control=ai', text)
        self.assertIn('control=player', text)
        self.assertEqual(1, text.count('is_ai ='))
        self.assertIn('rw_tm_enabled_trigger = yes', text[text.index('rw_tm_commit_effect ='):])

    def test_no_identifiers_names_or_dynamic_log_values(self):
        text = LIB.read_text()
        for forbidden in ('GetName', 'GetID', '[', 'character:', 'add_gold', 'run_interaction', 'kill ='):
            self.assertNotIn(forbidden, text)

    def test_every_registered_hook_is_real(self):
        for row in REGISTRY['coverage']:
            text = (ROOT / row['file']).read_text()
            self.assertIn('ACTION = ' + row['action'], text)
            self.assertIn(row.get('effect', row.get('event_option')), text)

    def test_observer_opportunity_in_character_scope(self):
        text = (LIB.parent / 'rw_native_sentence_effects.txt').read_text()
        self.assertIn('scope:rw_scheme_observer = {\n            rw_tm_emit_effect = { FAMILY = justice ACTION = custody_opportunity', text)


class TelemetryReportTests(unittest.TestCase):
    def test_counts_and_explicit_stop(self):
        result = report.traces([marker('start'), marker('evaluated'), marker('commit'), marker('complete'), marker('stop')])
        self.assertEqual(1, result['counts']['justice/execute/commit/ai'])
        self.assertEqual('stopped', result['sessions'][0]['end'])

    def test_duplicate_is_native_audit_observation(self):
        result = report.traces([marker('start'), marker('commit'), marker('duplicate'), marker('stop')])
        self.assertEqual(1, result['counts']['justice/execute/duplicate/ai'])

    def test_truncation_and_no_observed_end(self):
        result = report.traces([marker('start'), marker('truncated')])
        self.assertTrue(result['sessions'][0]['budget_exhausted'])
        self.assertEqual('not_observed', result['sessions'][0]['end'])

    def test_observations_after_truncation_flagged(self):
        result = report.traces([marker('start'), marker('truncated'), marker('commit')])
        self.assertEqual(1, result['invalid_markers'])
        self.assertEqual({}, result['counts'])

    def test_wrong_stage_for_abstention_rejected(self):
        self.assertEqual(1, report.traces([marker('commit', action='leave_sentence')])['invalid_markers'])

    def test_sessions_not_combined_silently(self):
        result = report.traces([marker('start'), marker('commit'), marker('start'), marker('commit'), marker('stop')])
        self.assertEqual(2, len(result['sessions']))
        self.assertEqual('restart_without_stop', result['sessions'][0]['end'])

    def test_orphans_cannot_be_complete_session(self):
        result = report.traces([marker('commit'), marker('stop')])
        self.assertEqual(2, result['orphaned_markers'])
        self.assertEqual({}, result['counts'])

    def test_malformed_and_macro_unexpanded_rejected(self):
        bad = ['RW_TM1 private stuff', marker('executed'), marker('commit', control='name'),
               marker('commit', family='war'), marker('commit', action='$ACTION$')]
        self.assertEqual(len(bad), report.traces(bad)['invalid_markers'])

    def test_raw_private_lines_never_exported(self):
        result = report.traces(['PRIVATE NAME SECRET LOCATION', marker('start'), 'RW_TM1 PRIVATE-SECRET', marker('stop')])
        self.assertNotIn('PRIVATE', json.dumps(result))

    def test_samples_use_measured_deltas(self):
        result = report.process_samples(csv_samples())
        self.assertEqual(4, result['cpu_seconds'])
        self.assertEqual(4, result['observed_seconds'])
        self.assertEqual(1, result['core_equivalents'])
        self.assertEqual(25, result['machine_cpu_percent'])
        self.assertEqual(1200, result['peak_observed_working_set_bytes'])
        self.assertEqual(2500, result['peak_observed_private_bytes'])

    def test_regressions_and_nonfinite_rejected(self):
        base = '2,13,1200,1900,4,4,running'
        for row in ('0,13,1200,1900,4,4,running', '2,9,1200,1900,4,4,running',
                    'nan,13,1200,1900,4,4,running', '2,13,1200,1900,4,0,running',
                    '2,13,1200,1900,4,8,running', '2,13,-1,1900,4,4,running',
                    '2,13,1.5,1900,4,4,running', base + ',extra'):
            with self.subTest(row=row), self.assertRaises(ValueError):
                report.process_samples(csv_samples(['0,10,1000,2000,3,4,running', row]))

    def test_requires_two_samples(self):
        with self.assertRaises(ValueError):
            report.process_samples(csv_samples(['0,10,1000,2000,3,4,running']))

    def test_terminal_is_not_zero_memory(self):
        result = report.process_samples(csv_samples(['0,10,1000,2000,3,4,running', '2,13,1200,1900,4,4,running', '3,,,,,,unavailable']))
        self.assertEqual('unavailable', result['terminal_status'])
        self.assertEqual(2, result['sample_count'])

    def test_post_terminal_rejected(self):
        with self.assertRaises(ValueError):
            report.process_samples(csv_samples(['0,10,1000,2000,3,4,running', '1,,,,,,replaced', '2,13,1200,1900,4,4,running']))

    def test_cli_existing_output_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)
            source, out = path / 'input.log', path / 'report.json'
            source.write_text(marker('start') + marker('stop'))
            out.write_text('KEEP')
            result = subprocess.run(['python', str(ROOT / 'tools/report_telemetry.py'), str(source), '--output', str(out)], capture_output=True)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual('KEEP', out.read_text())

    def test_cli_malformed_marker_fails_with_sanitized_report(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / 'input.log'
            source.write_text('RW_TM1 SECRET-NAME\n')
            result = subprocess.run(['python', str(ROOT / 'tools/report_telemetry.py'), str(source)], capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertNotIn('SECRET-NAME', result.stdout)
            self.assertEqual(1, json.loads(result.stdout)['traces'][0]['invalid_markers'])


class ProcessSamplerTests(unittest.TestCase):
    def setUp(self):
        self.shell = os.environ.get('RW_PWSH') or shutil.which('powershell.exe') or shutil.which('pwsh')
        if not self.shell:
            if os.environ.get('RW_REQUIRE_POWERSHELL'):
                self.fail('PowerShell required by CI')
            self.skipTest('PowerShell unavailable; required Linux/Windows CI executes sampler')
        self.tmp = tempfile.TemporaryDirectory(prefix='rw samples ')
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / 'samples.csv'

    def run_sampler(self, interval=100, prefix=""):
        # Test the real read-only sampler against its own shell, never a fake game.
        script = str(ROOT / 'tools/Measure-RealWesteros-Process.ps1').replace("'", "''")
        output = str(self.out).replace("'", "''")
        code = prefix + f"& '{script}' -TargetProcessId $PID -DurationSeconds 0.5 -IntervalMilliseconds {interval} -OutputPath '{output}'"
        return subprocess.run([self.shell, '-NoProfile', '-NonInteractive', '-Command', code], capture_output=True, text=True, timeout=30)

    def test_real_process_samples_parse(self):
        result = self.run_sampler()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        parsed = report.process_samples(report.bounded_lines(self.out))
        self.assertGreaterEqual(parsed['sample_count'], 2)
        self.assertGreater(parsed['observed_seconds'], 0)
        self.assertGreater(parsed['peak_observed_working_set_bytes'], 0)

    def test_slow_first_probe_still_spans_real_sampling_window(self):
        # Delay the first sampling probe around the REAL Get-Process cmdlet.
        # Baseline lookup is probe zero; no fake CPU/memory values are returned.
        prefix = r"""
$script:probeNumber = 0
function Get-Process {
    [CmdletBinding()]
    param([int]$Id)
    if ($script:probeNumber -eq 1) { Start-Sleep -Milliseconds 700 }
    $script:probeNumber += 1
    Microsoft.PowerShell.Management\Get-Process -Id $Id
}
"""
        result = self.run_sampler(prefix=prefix)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        parsed = report.process_samples(report.bounded_lines(self.out))
        self.assertGreaterEqual(parsed['sample_count'], 2)
        self.assertGreaterEqual(parsed['observed_seconds'], 0.45)
        self.assertGreater(parsed['peak_observed_working_set_bytes'], 0)

    def test_existing_file_never_overwritten(self):
        self.out.write_text('KEEP')
        result = self.run_sampler()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual('KEEP', self.out.read_text())

    def test_invalid_interval_creates_no_output(self):
        result = self.run_sampler(interval=1)
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(self.out.exists())


if __name__ == '__main__':
    unittest.main()
