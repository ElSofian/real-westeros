"""RW-007 synthetic snapshot and idempotency tests; NO CK3 engine coverage."""

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from g2_offer_probe import Clause, OfferRejected  # noqa: E402
from rw007_persistence_probe import PoliticalLedger, SnapshotRejected  # noqa: E402


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.ledger = PoliticalLedger()
        self.clauses = (Clause('troops', 'promise', 'Send troops'),
                        Clause('gold', 'payment', 'Pay gold'))
        self.ledger.create('affair', 'a', 'b', self.clauses, 100, 1)

    def accepted(self):
        self.ledger.accept('affair', 'b', 1, 2, {'troops': True, 'gold': True})

    def corrupt(self, change):
        raw = json.loads(self.ledger.dump())
        change(raw)
        with self.assertRaises(SnapshotRejected):
            PoliticalLedger.load(json.dumps(raw))

    def test_pending_roundtrip_and_counter_rejects_stale(self):
        self.ledger.counter('affair', 'b', 1, self.clauses, 2)
        restored = PoliticalLedger.load(self.ledger.dump())
        with self.assertRaisesRegex(OfferRejected, 'stale'):
            restored.accept('affair', 'a', 1, 3, {'troops': True, 'gold': True})
        self.assertEqual(restored.current('affair').version, 2)

    def test_accepted_creates_obligations_not_effects(self):
        self.accepted()
        restored = PoliticalLedger.load(self.ledger.dump())
        self.assertEqual(restored.obligation('affair', 1, 'gold').status, 'outstanding')
        with self.assertRaisesRegex(OfferRejected, 'finalized'):
            restored.accept('affair', 'b', 1, 3, {'troops': True, 'gold': True})

    def test_receipt_replay_after_reload_is_noop(self):
        self.accepted()
        self.ledger.record('event-1', 'affair', 1, 'gold', 'fulfilled')
        restored = PoliticalLedger.load(self.ledger.dump())
        before = restored.dump()
        self.assertEqual(restored.record('event-1', 'affair', 1, 'gold', 'fulfilled').status, 'fulfilled')
        self.assertEqual(restored.dump(), before)

    def test_receipt_collision_fails_closed(self):
        self.accepted()
        self.ledger.record('event-1', 'affair', 1, 'gold', 'fulfilled')
        with self.assertRaisesRegex(OfferRejected, 'reused'):
            self.ledger.record('event-1', 'affair', 1, 'troops', 'broken')

    def test_different_event_cannot_finalize_twice(self):
        self.accepted()
        self.ledger.record('event-1', 'affair', 1, 'gold', 'fulfilled')
        with self.assertRaisesRegex(OfferRejected, 'finalized'):
            self.ledger.record('event-2', 'affair', 1, 'gold', 'fulfilled')

    def test_failed_precondition_no_partial_state(self):
        with self.assertRaisesRegex(OfferRejected, 'preconditions'):
            self.ledger.accept('affair', 'b', 1, 2, {'troops': True, 'gold': False})
        self.assertEqual(json.loads(self.ledger.dump())['obligations'], [])
        self.assertEqual(self.ledger.current('affair').status, 'pending')

    def test_declined_offer_has_no_obligations_after_reload(self):
        self.ledger.decline('affair', 'b', 1, 2)
        restored = PoliticalLedger.load(self.ledger.dump())
        with self.assertRaisesRegex(OfferRejected, 'unknown obligation'):
            restored.obligation('affair', 1, 'gold')

    def test_duplicate_offer_after_reload(self):
        restored = PoliticalLedger.load(self.ledger.dump())
        with self.assertRaisesRegex(OfferRejected, 'duplicate offer'):
            restored.create('affair', 'a', 'b', self.clauses, 100, 2)

    def test_deterministic_serialization(self):
        self.accepted()
        self.assertEqual(PoliticalLedger.load(self.ledger.dump()).dump(), self.ledger.dump())

    def test_reject_unknown_schema(self):
        self.corrupt(lambda raw: raw.update(schema_version=2))

    def test_reject_missing_obligation(self):
        self.accepted()
        self.corrupt(lambda raw: raw['obligations'].pop())

    def test_reject_forged_obligation(self):
        self.corrupt(lambda raw: raw['obligations'].append(dict(
            offer_id='affair', version=1, clause_key='gold', status='outstanding')))

    def test_reject_terminal_without_receipt(self):
        self.accepted()
        self.corrupt(lambda raw: raw['obligations'][0].update(status='fulfilled'))

    def test_reject_duplicate_receipt_for_obligation(self):
        self.accepted()
        self.ledger.record('event-1', 'affair', 1, 'gold', 'fulfilled')
        self.corrupt(lambda raw: raw['receipts'].append(dict(
            event_id='event-2', offer_id='affair', version=1,
            clause_key='gold', outcome='fulfilled')))

    def test_reject_duplicate_json_keys(self):
        with self.assertRaisesRegex(SnapshotRejected, 'duplicate JSON'):
            PoliticalLedger.load('{"schema_version":1,"schema_version":1}')

    def test_reject_wrong_type_and_nan(self):
        self.corrupt(lambda raw: raw['offers'][0].update(version=True))
        with self.assertRaises(SnapshotRejected):
            PoliticalLedger.load('{"schema_version":NaN}')


if __name__ == '__main__':
    unittest.main()
