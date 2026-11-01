"""Reject progress inflation; these tests do not exercise CK3."""
import copy
import json
import unittest
from tools.report_progress import ROOT, report


class ProgressReportTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'docs/V01_PROGRESS.json').read_text())

    def test_committed_assessment_is_consistent(self):
        result = report(self.data)
        self.assertEqual(result['score'], result['source'] + result['engine'])
        self.assertEqual(result['denominator'], 100)
        self.assertEqual(len(result['lots']), 9)

    def test_single_baseline_has_no_velocity_or_delivery_gain(self):
        # Stable synthetic ledger from the actual rubric, irrespective of later deliveries.
        self.data['checkpoints'] = [self.data['checkpoints'][-1] | {'kind': 'baseline'}]
        result = report(self.data)
        self.assertIsNone(result['delta'])
        self.assertIsNone(result['velocity'])

    def test_seven_day_delivery_and_same_day_checkpoint(self):
        # A prior incomplete source criterion is fulfilled; no fabricated engine result.
        criterion = next(c for lot in self.data['lots'] for c in lot['criteria']
                         if c['status'] == 'source_complete')
        end = copy.deepcopy(self.data['checkpoints'][-1])
        end.update(kind='delivery', date='2026-11-08')
        start = copy.deepcopy(end)
        start.update(kind='baseline', date='2026-11-01')
        start['completed'].remove(criterion['id'])
        start['score'] -= criterion['points']
        self.data['checkpoints'] = [start, end]
        result = report(self.data)
        self.assertEqual(result['velocity']['points_per_week'], criterion['points'])
        self.assertEqual(result['delta'], criterion['points'])
        end['date'] = start['date']
        self.assertIsNone(report(self.data)['velocity'])

    def test_rejects_inflation_and_duplicate_criteria(self):
        for mutation in ('score', 'duplicate', 'denominator', 'rubric'):
            with self.subTest(mutation=mutation):
                d = copy.deepcopy(self.data)
                if mutation == 'score':
                    d['checkpoints'][-1]['score'] += 1
                elif mutation == 'duplicate':
                    d['lots'][0]['criteria'][1]['id'] = d['lots'][0]['criteria'][0]['id']
                elif mutation == 'denominator':
                    d['lots'][0]['weight'] -= 1
                else:
                    d['lots'][0]['criteria'][0]['acceptance'] = 'Weaker requirement'
                with self.assertRaises(ValueError):
                    report(d)

    def test_rejects_status_without_actual_evidence(self):
        for mutation in ('no_evidence', 'no_script', 'missing_file', 'engine_as_source', 'wrong_snapshot'):
            with self.subTest(mutation=mutation):
                d = copy.deepcopy(self.data)
                c = next(c for lot in d['lots'] for c in lot['criteria'] if c['status'] == 'source_complete')
                if mutation == 'no_evidence':
                    c['evidence'] = []
                elif mutation == 'no_script':
                    c['evidence'] = ['docs/PROGRESS.md']
                elif mutation == 'missing_file':
                    c['evidence'] += ['docs/DOES_NOT_EXIST.md']
                elif mutation == 'engine_as_source':
                    d['lots'][-1]['criteria'][0].update(status='source_complete', evidence=c['evidence'])
                else:
                    c['status'] = 'open'
                with self.assertRaises(ValueError):
                    report(d)

    def test_engine_completion_needs_dedicated_results(self):
        d = copy.deepcopy(self.data)
        c = d['lots'][-1]['criteria'][0]
        c.update(status='engine_complete', evidence=['docs/FINAL_ENGINE_TESTS.md'])
        with self.assertRaisesRegex(ValueError, 'game results'):
            report(d)

    def test_velocity_does_not_extrapolate_stale_checkpoint(self):
        start = copy.deepcopy(self.data['checkpoints'][-1])
        start.update(kind='baseline', date='2026-09-01')
        end = copy.deepcopy(start)
        end.update(kind='delivery', date='2026-11-01')
        self.data['checkpoints'] = [start, end]
        self.assertIsNone(report(self.data)['velocity'])
