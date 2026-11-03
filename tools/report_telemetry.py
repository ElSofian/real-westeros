#!/usr/bin/env python3
"""Aggregate literal opt-in CK3 observations and measured process CSV, offline."""
import argparse
from collections import Counter
import csv
import json
import math
from pathlib import Path
import re

ACTIONS = {
    'telemetry': {'session'},
    'justice': {'arrest', 'execute', 'leave_arrest', 'leave_sentence', 'custody_opportunity'},
    'bundle': {'counter', 'accept', 'close', 'refuse_gold', 'refuse_support', 'refuse_release',
               'gold', 'support', 'release', 'leave'},
}
STAGES = {'evaluated', 'authorized', 'denied', 'commit', 'duplicate', 'missing_context',
          'complete', 'selected', 'visit'}
PATTERN = re.compile(r'RW_TM1 family=(\w+) action=(\w+) stage=(\w+) control=(\w+)\s*$')
LIMITATIONS = ['Source instrumentation; no engine compatibility conclusion.',
               'complete means handler returned, not native success or death.',
               'denied is a guard rejection, not proof of abuse.',
               'Whole-process CPU/memory cannot isolate mod overhead, FPS or per-effect latency.',
               'Expired, stopped or exhausted tracing leaves unobserved activity.']


def traces(lines):
    sessions, active = [], None
    counts, errors, orphaned = Counter(), 0, 0
    for line in lines:
        if 'RW_TM1' not in line:
            continue
        match = PATTERN.search(line)
        if not match:
            errors += 1
            continue
        family, action, stage, control = match.groups()
        valid = action in ACTIONS.get(family, set())
        valid &= ((family == 'telemetry' and stage in {'start', 'stop', 'truncated'} and control == 'unknown')
                  or (family != 'telemetry' and stage in STAGES and control in {'ai', 'player'}))
        if family != 'telemetry' and valid:
            permitted = ({'selected'} if action.startswith('leave') else
                         {'visit'} if action == 'custody_opportunity' else
                         STAGES - {'selected', 'visit'})
            valid &= stage in permitted
        if not valid:
            errors += 1
            continue
        if stage == 'start':
            if active is not None:
                active['end'] = 'restart_without_stop'
            active = {'counts': Counter(), 'end': 'not_observed', 'budget_exhausted': False}
            sessions.append(active)
        elif active is None:
            orphaned += 1
        elif stage == 'stop':
            active['end'] = 'stopped'
            active = None
        elif stage == 'truncated':
            active['budget_exhausted'] = True
        elif active['budget_exhausted']:
            errors += 1
        else:
            key = '/'.join((family, action, stage, control))
            active['counts'][key] += 1
            counts[key] += 1
    return {'counts': dict(sorted(counts.items())), 'sessions': sessions,
            'invalid_markers': errors, 'orphaned_markers': orphaned}


def process_samples(lines):
    reader = csv.DictReader(lines)
    expected = ['elapsed_seconds', 'cpu_seconds', 'working_set_bytes', 'private_bytes',
                'threads', 'logical_processors', 'status']
    if reader.fieldnames != expected:
        raise ValueError('Invalid sample columns')
    samples, terminal = [], None
    for row in reader:
        if None in row or None in row.values() or terminal is not None:
            raise ValueError('Malformed or post-terminal sample')
        if row['status'] in {'unavailable', 'replaced'}:
            if any(row[k] for k in expected[1:-1]):
                raise ValueError('Terminal sample contains process values')
            end = float(row['elapsed_seconds'])
            if not math.isfinite(end) or end < 0 or (samples and end < samples[-1][0]):
                raise ValueError('Invalid terminal time')
            terminal = row['status']
            continue
        if row['status'] != 'running':
            raise ValueError('Invalid sample status')
        try:
            values = [float(row[k]) for k in expected[:-1]]
        except ValueError:
            raise ValueError('Nonnumeric sample') from None
        if not all(math.isfinite(v) and v >= 0 for v in values):
            raise ValueError('Nonfinite or negative sample')
        if any(v != int(v) for v in values[2:]) or values[-1] < 1:
            raise ValueError('Invalid integer process fields')
        if samples and (values[0] <= samples[-1][0] or values[1] < samples[-1][1]
                        or values[-1] != samples[-1][-1]):
            raise ValueError('Time/CPU regression or processor count change')
        samples.append(values)
    if len(samples) < 2:
        raise ValueError('At least two running samples required')
    wall = samples[-1][0] - samples[0][0]
    cpu = samples[-1][1] - samples[0][1]
    return {'sample_count': len(samples), 'observed_seconds': wall, 'cpu_seconds': cpu,
            'core_equivalents': cpu / wall,
            'machine_cpu_percent': 100 * cpu / wall / samples[0][-1],
            'peak_observed_working_set_bytes': max(v[2] for v in samples),
            'peak_observed_private_bytes': max(v[3] for v in samples),
            'terminal_status': terminal}


def bounded_lines(path):
    if path.stat().st_size > 128 * 1024 * 1024:
        raise ValueError('Input exceeds 128 MiB; select a profiling window')
    with path.open(encoding='utf-8-sig', errors='replace') as source:
        for line in source:
            if len(line) > 65536:
                raise ValueError('Input line exceeds 64 KiB')
            yield line


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('logs', nargs='*', type=Path)
    parser.add_argument('--samples', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not args.logs and not args.samples:
        parser.error('Provide a log or process CSV')
    try:
        result = {'schema': 1, 'limitations': LIMITATIONS}
        # Each input has separate session boundaries; never join rotated files silently.
        if args.logs:
            result['traces'] = [traces(bounded_lines(p)) for p in args.logs]
        if args.samples:
            result['process'] = process_samples(bounded_lines(args.samples))
        data = json.dumps(result, indent=2, sort_keys=True) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as target:
                target.write(data)
        else:
            print(data, end='')
        return int(any(t['invalid_markers'] for t in result.get('traces', [])))
    except (OSError, ValueError):
        # Do not echo arbitrary log contents or personal paths in diagnostics.
        parser.exit(2, 'Unable to read/validate input or create a new output.\n')


if __name__ == '__main__':
    raise SystemExit(main())
