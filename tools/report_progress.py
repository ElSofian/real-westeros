#!/usr/bin/env python3
"""Read-only v0.1 readiness report; no CK3 simulation or runtime dependency."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
SYSTEMS = {'W', 'P', 'N', 'O', 'J', 'I', 'M', 'AI'}


def rubric_hash(data):
    """Freeze acceptance/weights across comparable checkpoints, excluding status."""
    rubric = [{k: lot[k] for k in ('id', 'phase', 'weight')} | {
        'criteria': [{k: c[k] for k in ('id', 'points', 'acceptance')}
                     for c in lot['criteria']]} for lot in data['lots']]
    return hashlib.sha256(json.dumps(rubric, ensure_ascii=False,
                                    sort_keys=True).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def report(data, root=ROOT):
    require(data['schema'] == 1, 'Unsupported schema')
    require(re.fullmatch(r'[0-9a-f]{40}', data['assessed_commit']), 'Missing source commit')
    lots = data['lots']
    require(len(lots) == 9 and {lot['id'] for lot in lots} == SYSTEMS | {'V'},
            'Exactly eight systems and final validation required')
    criteria = {}
    totals = []
    current = set()
    for lot in lots:
        phase = 'engine' if lot['id'] == 'V' else 'source'
        require(lot['phase'] == phase, 'Wrong phase')
        require(type(lot['weight']) is int and lot['weight'] > 0, 'Invalid weight')
        require(sum(c['points'] for c in lot['criteria']) == lot['weight'], 'Lot weight mismatch')
        earned = 0
        for c in lot['criteria']:
            require(c['id'] not in criteria, 'Duplicate criterion')
            require(c['id'].startswith(lot['id']) and c['acceptance'].strip(), 'Invalid criterion')
            require(type(c['points']) is int and c['points'] > 0, 'Invalid points')
            require(c['status'] in ('open', phase + '_complete'), 'Wrong completion phase')
            criteria[c['id']] = c
            evidence = c['evidence']
            for name in evidence:
                p = PurePosixPath(name)
                require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,
                        'Unsafe evidence path')
                require((root / name).is_file(), 'Missing evidence: ' + name)
            if c['status'] != 'open':
                require(bool(evidence), 'Completion needs evidence')
                if phase == 'source':
                    require(any(p.startswith('mod/real_westeros/') and p.endswith('.txt')
                                for p in evidence), 'Source completion needs CK3 script evidence')
                    require(any(p.startswith('docs/') for p in evidence), 'Completion needs assessment guide')
                else:
                    require(any(p.startswith('docs/engine-results/') for p in evidence),
                            'Engine completion needs reproducible game results')
                current.add(c['id'])
                earned += c['points']
        totals.append(dict(id=lot['id'],title=lot['title'],earned=earned,weight=lot['weight']))
    require(sum(lot['weight'] for lot in lots if lot['phase'] == 'source') == 80
            and next(lot['weight'] for lot in lots if lot['id'] == 'V') == 20,
            'Readiness denominator must stay 80 source + 20 engine')
    checkpoints = data['checkpoints']
    require(bool(checkpoints), 'Baseline required')
    fingerprint = rubric_hash(data)
    previous = None
    for i, cp in enumerate(checkpoints):
        day = date.fromisoformat(cp['date'])
        require(previous is None or day >= previous, 'Checkpoints out of order')
        require(cp['kind'] == 'baseline' if i == 0 else cp['kind'] in ('delivery', 'regression'),
                'One baseline followed by delivery/regression checkpoints')
        require(cp['metric_version'] == data['metric_version']
                and cp['rubric_sha256'] == fingerprint, 'Recalibration needs a new explicit baseline')
        ids = cp['completed']
        require(len(ids) == len(set(ids)) and set(ids) <= criteria.keys(), 'Invalid checkpoint criteria')
        require(type(cp['score']) is int and cp['score'] == sum(criteria[c]['points'] for c in ids),
                'Checkpoint score mismatch')
        require(bool(cp['reference'].strip()) and bool(cp['note'].strip()), 'Checkpoint needs reference and note')
        if i:
            delta = cp['score'] - checkpoints[i-1]['score']
            require(delta <= 0 if cp['kind'] == 'regression' else delta >= 0, 'Wrong delta kind')
        previous = day
    latest = checkpoints[-1]
    require(set(latest['completed']) == current, 'Latest checkpoint must match assessed status')
    # Calendar-time throughput at the latest checkpoint, never PRs or active work hours.
    end = date.fromisoformat(latest['date'])
    comparable = [cp for cp in checkpoints[:-1]
                  if 7 <= (end - date.fromisoformat(cp['date'])).days <= 30]
    velocity = None
    if comparable:
        first = comparable[0]
        days = (end - date.fromisoformat(first['date'])).days
        velocity = {'from': first['date'], 'to': latest['date'], 'days': days,
                    'points_per_week': round((latest['score'] - first['score']) * 7 / days, 2)}
    return dict(metric_version=data['metric_version'],as_of=latest['date'],score=latest['score'],
                denominator=100,source=sum(t['earned'] for t in totals if t['id'] != 'V'),
                engine=next(t['earned'] for t in totals if t['id'] == 'V'),
                delta=None if len(checkpoints) == 1 else latest['score'] - checkpoints[-2]['score'],
                velocity=velocity,lots=totals)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Machine-readable assessed report')
    args = parser.parse_args()
    try:
        result = report(json.loads((ROOT / 'docs/V01_PROGRESS.json').read_text()))
    except (ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Invalid progress assessment: {exc}\n')
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"v0.1 readiness ({result['metric_version']}, {result['as_of']}): {result['score']}/100")
    print(f"Source: {result['source']}/80; engine: {result['engine']}/20 (source is not engine proof)")
    for lot in result['lots']:
        print(f"  {lot['id']}: {lot['earned']}/{lot['weight']} — {lot['title']}")
    print('Delta: baseline only' if result['delta'] is None else f"Delta: {result['delta']:+d} points")
    print('Velocity: unavailable (need comparable checkpoints spanning 7–30 days)' if result['velocity'] is None
          else f"Velocity at latest checkpoint: {result['velocity']['points_per_week']:+g} points/week")


if __name__ == '__main__':
    main()
