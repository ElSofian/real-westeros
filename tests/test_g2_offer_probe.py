"""Synthetic protocol invariants only; not CK3 gameplay tests."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from g2_offer_probe import Clause, OfferBook, OfferRejected, accept, counter, decline, propose  # noqa: E402


class OfferProbeTests(unittest.TestCase):
    def setUp(self):
        self.clauses = (
            Clause('service', 'promise', 'Supply troops after a later request'),
            Clause('payment', 'immediate', 'Pay agreed gold'),
        )
        self.offer = propose('affair-1', 'lord_a', 'lord_b', self.clauses, 100, 1)

    def test_two_clause_acceptance_records_consent_only(self):
        accepted = accept(self.offer, 'lord_b', 1, 2, {'service': True, 'payment': True})
        self.assertEqual(accepted.status, 'accepted')
        self.assertEqual(self.offer.status, 'pending')
        self.assertEqual(accepted.clauses, self.clauses)

    def test_stale_acceptance_after_counteroffer_rejected(self):
        changed = counter(self.offer, 'lord_b', 1, self.clauses, 2)
        self.assertEqual((changed.proposer, changed.recipient, changed.version), ('lord_b', 'lord_a', 2))
        with self.assertRaisesRegex(OfferRejected, 'stale'):
            accept(changed, 'lord_a', 1, 3, {'service': True, 'payment': True})

    def test_counteroffer_requires_new_recipient_consent(self):
        changed = counter(self.offer, 'lord_b', 1, self.clauses, 2)
        with self.assertRaisesRegex(OfferRejected, 'recipient'):
            accept(changed, 'lord_b', 2, 3, {'service': True, 'payment': True})

    def test_missing_clause_precondition_rejects_entire_offer(self):
        with self.assertRaisesRegex(OfferRejected, 'preconditions'):
            accept(self.offer, 'lord_b', 1, 2, {'service': True, 'payment': False})
        self.assertEqual(self.offer.status, 'pending')

    def test_unlisted_clause_precondition_fails_closed(self):
        with self.assertRaisesRegex(OfferRejected, 'preconditions'):
            accept(self.offer, 'lord_b', 1, 2, {'service': True})

    def test_double_acceptance_rejected(self):
        accepted = accept(self.offer, 'lord_b', 1, 2, {'service': True, 'payment': True})
        with self.assertRaisesRegex(OfferRejected, 'finalized'):
            accept(accepted, 'lord_b', 1, 3, {'service': True, 'payment': True})

    def test_expired_offer_rejected(self):
        with self.assertRaisesRegex(OfferRejected, 'expired'):
            accept(self.offer, 'lord_b', 1, 100, {'service': True, 'payment': True})

    def test_unrelated_actor_cannot_decline(self):
        with self.assertRaisesRegex(OfferRejected, 'recipient'):
            decline(self.offer, 'lord_c', 1, 2)

    def test_duplicate_clause_key_rejected(self):
        with self.assertRaisesRegex(OfferRejected, 'duplicate'):
            counter(self.offer, 'lord_b', 1, (self.clauses[0], self.clauses[0]), 2)

    def test_one_clause_offer_rejected(self):
        with self.assertRaisesRegex(OfferRejected, 'at least two'):
            propose('affair-2', 'lord_a', 'lord_b', self.clauses[:1], 100, 1)

    def test_valid_decline_finalizes(self):
        declined = decline(self.offer, 'lord_b', 1, 2)
        self.assertEqual(declined.status, 'declined')
        with self.assertRaisesRegex(OfferRejected, 'finalized'):
            counter(declined, 'lord_b', 1, self.clauses, 3)

    def test_book_rejects_superseded_snapshot(self):
        book = OfferBook()
        book.create(self.offer)
        book.counter('affair-1', 'lord_b', 1, self.clauses, 2)
        with self.assertRaisesRegex(OfferRejected, 'stale'):
            book.accept('affair-1', 'lord_a', 1, 3, {'service': True, 'payment': True})
        self.assertEqual(book.current('affair-1').status, 'pending')

    def test_book_rejects_duplicate_commit(self):
        book = OfferBook()
        book.create(self.offer)
        book.accept('affair-1', 'lord_b', 1, 2, {'service': True, 'payment': True})
        with self.assertRaisesRegex(OfferRejected, 'finalized'):
            book.accept('affair-1', 'lord_b', 1, 3, {'service': True, 'payment': True})

    def test_book_preserves_state_on_failed_precondition(self):
        book = OfferBook()
        book.create(self.offer)
        with self.assertRaisesRegex(OfferRejected, 'preconditions'):
            book.accept('affair-1', 'lord_b', 1, 2, {'service': True, 'payment': False})
        self.assertEqual(book.current('affair-1'), self.offer)

    def test_book_rejects_duplicate_offer_id(self):
        book = OfferBook()
        book.create(self.offer)
        with self.assertRaisesRegex(OfferRejected, 'duplicate offer ID'):
            book.create(self.offer)

    def test_no_self_dealing(self):
        with self.assertRaisesRegex(OfferRejected, 'parties'):
            propose('affair-2', 'lord_a', 'lord_a', self.clauses, 100, 1)


if __name__ == '__main__':
    unittest.main()
