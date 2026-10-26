"""Pure-Python G2 protocol probe; NOT CK3 script or native-effect execution.

This deliberately models offer revisions and consent only. The real CK3
persistence, UI, game effects and transaction boundaries remain unverified.
"""

from dataclasses import dataclass, replace
from typing import Mapping


class OfferRejected(ValueError):
    """The requested transition is invalid; the caller retains its old offer."""


@dataclass(frozen=True)
class Clause:
    key: str
    kind: str
    detail: str


@dataclass(frozen=True)
class Offer:
    offer_id: str
    version: int
    proposer: str
    recipient: str
    clauses: tuple[Clause, ...]
    expires_at: int
    status: str = 'pending'


def _check_clauses(clauses: tuple[Clause, ...]) -> None:
    if len(clauses) < 2:
        raise OfferRejected('G2 probe requires at least two clauses')
    keys = [clause.key for clause in clauses]
    if any(not clause.key or not clause.kind or not clause.detail for clause in clauses):
        raise OfferRejected('clauses must have a key, kind and detail')
    if len(keys) != len(set(keys)):
        raise OfferRejected('duplicate clause key')


def propose(offer_id: str, proposer: str, recipient: str,
            clauses: tuple[Clause, ...], expires_at: int, now: int) -> Offer:
    if not offer_id or not proposer or not recipient or proposer == recipient:
        raise OfferRejected('invalid parties or offer ID')
    if expires_at <= now:
        raise OfferRejected('offer already expired')
    _check_clauses(clauses)
    return Offer(offer_id, 1, proposer, recipient, clauses, expires_at)


def _guard(offer: Offer, actor: str, expected_version: int, now: int) -> None:
    if offer.status != 'pending':
        raise OfferRejected('offer already finalized')
    if expected_version != offer.version:
        raise OfferRejected('stale offer revision')
    if now >= offer.expires_at:
        raise OfferRejected('offer expired')
    if actor != offer.recipient:
        raise OfferRejected('only current recipient may respond')


def counter(offer: Offer, actor: str, expected_version: int,
            clauses: tuple[Clause, ...], now: int) -> Offer:
    _guard(offer, actor, expected_version, now)
    _check_clauses(clauses)
    return replace(offer, version=offer.version + 1, proposer=actor,
                   recipient=offer.proposer, clauses=clauses)


def accept(offer: Offer, actor: str, expected_version: int, now: int,
           preconditions: Mapping[str, bool]) -> Offer:
    """Validate the whole snapshot, then record consent; execute NO effects.

    The caller must re-check the preconditions in the CK3 engine before
    committing any native effect. This function does not provide atomicity.
    """
    _guard(offer, actor, expected_version, now)
    if any(preconditions.get(clause.key) is not True for clause in offer.clauses):
        raise OfferRejected('one or more clause preconditions failed')
    return replace(offer, status='accepted')


def decline(offer: Offer, actor: str, expected_version: int, now: int) -> Offer:
    _guard(offer, actor, expected_version, now)
    return replace(offer, status='declined')


class OfferBook:
    """Single-threaded, in-memory authority for the CURRENT revision only.

    It illustrates compare-and-swap semantics; it is not CK3 persistence,
    locking, save/load support, or a replacement for engine-side rechecks.
    """

    def __init__(self) -> None:
        self._offers: dict[str, Offer] = {}

    def create(self, offer: Offer) -> Offer:
        if offer.offer_id in self._offers:
            raise OfferRejected('duplicate offer ID')
        self._offers[offer.offer_id] = offer
        return offer

    def current(self, offer_id: str) -> Offer:
        if offer_id not in self._offers:
            raise OfferRejected('unknown offer ID')
        return self._offers[offer_id]

    def counter(self, offer_id: str, actor: str, expected_version: int,
                clauses: tuple[Clause, ...], now: int) -> Offer:
        updated = counter(self.current(offer_id), actor, expected_version, clauses, now)
        self._offers[offer_id] = updated
        return updated

    def accept(self, offer_id: str, actor: str, expected_version: int,
               now: int, preconditions: Mapping[str, bool]) -> Offer:
        updated = accept(self.current(offer_id), actor, expected_version, now, preconditions)
        self._offers[offer_id] = updated
        return updated

    def decline(self, offer_id: str, actor: str, expected_version: int,
                now: int) -> Offer:
        updated = decline(self.current(offer_id), actor, expected_version, now)
        self._offers[offer_id] = updated
        return updated
