"""RW-007 offline snapshot/receipt probe. NO CK3 save API or native effects."""

from dataclasses import asdict, dataclass
import json

from g2_offer_probe import Clause, Offer, OfferRejected, accept, counter, decline, expire, propose


class SnapshotRejected(ValueError):
    """Malformed, inconsistent or unsupported snapshot."""


@dataclass(frozen=True)
class Obligation:
    offer_id: str
    version: int
    clause_key: str
    status: str = 'outstanding'

    @property
    def key(self):
        return (self.offer_id, self.version, self.clause_key)


@dataclass(frozen=True)
class Receipt:
    event_id: str
    offer_id: str
    version: int
    clause_key: str
    outcome: str

    @property
    def key(self):
        return (self.offer_id, self.version, self.clause_key)


class PoliticalLedger:
    """Single-writer reference authority; callers must persist after every transition.

    This model cannot provide atomic CK3 effects, concurrency locks or actual
    game save/reload integration. Accepted offers create obligations, not effects.
    """

    def __init__(self):
        self._offers = {}
        self._obligations = {}
        self._receipts = {}

    def current(self, offer_id):
        if offer_id not in self._offers:
            raise OfferRejected('unknown offer ID')
        return self._offers[offer_id]

    def create(self, offer_id, proposer, recipient, clauses, expires_at, now):
        if offer_id in self._offers:
            raise OfferRejected('duplicate offer ID')
        offer = propose(offer_id, proposer, recipient, clauses, expires_at, now)
        self._offers[offer_id] = offer
        return offer

    def counter(self, offer_id, actor, version, clauses, now):
        updated = counter(self.current(offer_id), actor, version, clauses, now)
        self._offers[offer_id] = updated
        return updated

    def accept(self, offer_id, actor, version, now, preconditions):
        updated = accept(self.current(offer_id), actor, version, now, preconditions)
        new = [Obligation(offer_id, updated.version, c.key) for c in updated.clauses]
        if any(item.key in self._obligations for item in new):
            raise OfferRejected('duplicate obligation')
        self._offers[offer_id] = updated
        for item in new:
            self._obligations[item.key] = item
        return updated

    def decline(self, offer_id, actor, version, now):
        updated = decline(self.current(offer_id), actor, version, now)
        self._offers[offer_id] = updated
        return updated

    def expire(self, offer_id, now):
        updated = expire(self.current(offer_id), now)
        self._offers[offer_id] = updated
        return updated

    def obligation(self, offer_id, version, clause_key):
        key = (offer_id, version, clause_key)
        if key not in self._obligations:
            raise OfferRejected('unknown obligation')
        return self._obligations[key]

    def record(self, event_id, offer_id, version, clause_key, outcome):
        """Record one observed outcome; NEVER execute or retry native effects."""
        if not isinstance(event_id, str) or not event_id:
            raise OfferRejected('invalid event ID')
        if outcome not in ('fulfilled', 'broken', 'disputed'):
            raise OfferRejected('invalid outcome')
        key = (offer_id, version, clause_key)
        receipt = Receipt(event_id, offer_id, version, clause_key, outcome)
        if event_id in self._receipts:
            if self._receipts[event_id] != receipt:
                raise OfferRejected('event ID reused for different outcome')
            return self.obligation(*key)  # identical replay is read-only
        current = self.obligation(*key)
        if current.status != 'outstanding':
            raise OfferRejected('obligation already finalized')
        updated = Obligation(*key, status=outcome)
        self._obligations[key] = updated
        self._receipts[event_id] = receipt
        return updated

    def dump(self):
        return json.dumps({
            'schema_version': 1,
            'offers': [asdict(self._offers[k]) for k in sorted(self._offers)],
            'obligations': [asdict(self._obligations[k]) for k in sorted(self._obligations)],
            'receipts': [asdict(self._receipts[k]) for k in sorted(self._receipts)],
        }, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

    @classmethod
    def load(cls, serialized):
        """Validate a whole snapshot before publishing a reconstructed authority."""
        def unique_pairs(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise SnapshotRejected('duplicate JSON field')
                result[key] = value
            return result

        def reject_constant(value):
            raise SnapshotRejected('nonstandard JSON number: ' + value)

        def fields(data, names):
            if not isinstance(data, dict) or set(data) != set(names):
                raise SnapshotRejected('unexpected snapshot fields')

        def string(value):
            return isinstance(value, str) and bool(value)

        def integer(value):
            return type(value) is int

        try:
            raw = json.loads(serialized, object_pairs_hook=unique_pairs,
                             parse_constant=reject_constant)
            fields(raw, ('schema_version', 'offers', 'obligations', 'receipts'))
            if raw['schema_version'] != 1 or type(raw['schema_version']) is not int:
                raise SnapshotRejected('unsupported schema version')
            if any(not isinstance(raw[k], list) for k in ('offers', 'obligations', 'receipts')):
                raise SnapshotRejected('snapshot collections must be arrays')
            ledger = cls()
            for item in raw['offers']:
                fields(item, ('offer_id', 'version', 'proposer', 'recipient',
                              'clauses', 'expires_at', 'status'))
                if not (all(string(item[k]) for k in ('offer_id', 'proposer', 'recipient'))
                        and item['proposer'] != item['recipient']
                        and integer(item['version']) and item['version'] >= 1
                        and integer(item['expires_at'])
                        and item['status'] in ('pending', 'accepted', 'declined', 'expired')
                        and isinstance(item['clauses'], list)):
                    raise SnapshotRejected('invalid offer fields')
                clauses = []
                for clause in item['clauses']:
                    fields(clause, ('key', 'kind', 'detail'))
                    if not all(string(clause[k]) for k in ('key', 'kind', 'detail')):
                        raise SnapshotRejected('invalid clause')
                    clauses.append(Clause(**clause))
                if len(clauses) < 2 or len({c.key for c in clauses}) != len(clauses):
                    raise SnapshotRejected('invalid clause set')
                offer = Offer(**{**item, 'clauses': tuple(clauses)})
                if offer.offer_id in ledger._offers:
                    raise SnapshotRejected('duplicate offer ID')
                ledger._offers[offer.offer_id] = offer
            for item in raw['obligations']:
                fields(item, ('offer_id', 'version', 'clause_key', 'status'))
                if not (string(item['offer_id']) and string(item['clause_key'])
                        and integer(item['version'])
                        and item['status'] in ('outstanding', 'fulfilled', 'broken', 'disputed')):
                    raise SnapshotRejected('invalid obligation fields')
                ob = Obligation(**item)
                if ob.key in ledger._obligations:
                    raise SnapshotRejected('duplicate obligation')
                ledger._obligations[ob.key] = ob
            for item in raw['receipts']:
                fields(item, ('event_id', 'offer_id', 'version', 'clause_key', 'outcome'))
                if not (all(string(item[k]) for k in ('event_id', 'offer_id', 'clause_key'))
                        and integer(item['version'])
                        and item['outcome'] in ('fulfilled', 'broken', 'disputed')):
                    raise SnapshotRejected('invalid receipt fields')
                receipt = Receipt(**item)
                if receipt.event_id in ledger._receipts:
                    raise SnapshotRejected('duplicate event ID')
                ledger._receipts[receipt.event_id] = receipt
            expected = {(offer.offer_id, offer.version, clause.key)
                        for offer in ledger._offers.values() if offer.status == 'accepted'
                        for clause in offer.clauses}
            if set(ledger._obligations) != expected:
                raise SnapshotRejected('obligations disagree with accepted offers')
            terminal = {key: ob.status for key, ob in ledger._obligations.items()
                        if ob.status != 'outstanding'}
            receipt_keys = {}
            for receipt in ledger._receipts.values():
                if receipt.key in receipt_keys:
                    raise SnapshotRejected('multiple receipts for one obligation')
                receipt_keys[receipt.key] = receipt.outcome
            if terminal != receipt_keys:
                raise SnapshotRejected('receipts disagree with obligations')
            return ledger
        except (TypeError, ValueError, KeyError, AttributeError) as error:
            if isinstance(error, SnapshotRejected):
                raise
            raise SnapshotRejected('invalid snapshot') from error
