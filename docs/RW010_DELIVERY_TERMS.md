# Two-clause service negotiation — original CK3 scripts, experimental

**Static-checked; not engine-tested.** Title-route collection/stronger G3 source
adapters are on standby per owner while away from their installation. This independent
slice expands the existing deferred endorsement, without new source uploads, native
title/war effects, runtime Python, paid services or a replacement diplomacy GUI.

## Price and delivery are distinct clauses

Initial deferred quotation stays 50 gold and thirty days from acceptance. The client
may counter the price to 25 **or** request delivery before fourteen days. A delivery
counter leaves the price intact; a price counter leaves the proposed deadline intact.
The provider may accept the whole current offer, counter back to thirty days, restore
50 gold, or decline. Every counter reverses the decision turn and increments revision
before saving the full snapshot and notifying the other party.

A shared event shows both named parties, the full promise/payment terms, captured
25/50-gold price and captured 14/30-day delivery clause together. Existing price panels
also append the captured delivery term. This is independent authored clause editing,
not four pre-authored combined bargains or an arbitrary limit on future clause types.
A general dynamic multi-clause composer remains future G2 work.

The original thirty-day **negotiation** expiry never changes during counters. The
accepted **delivery** deadline instead starts at consent; the seven-day minimum
wait stays fixed. All current party, pending flag, serial, revision, mode, price and
delivery checks apply before mutation; accepted promises cannot be renegotiated
through these quote-only actions. Changing either clause needs renewed explicit
acceptance of the entire resulting offer, not partial consent.

## Promise, performance and timeout

Consent checks the client's current funds but moves no gold or prestige. It advances
revision and records the obligation plus its agreed 14- or 30-day flag exactly once.
The first performance decision stays day eight. The one timeout callback is scheduled
at day fifteen or thirty-one respectively; the due flag gates fulfillment immediately
at the actual deadline, without waiting for that callback. Existing timeout logic
keeps accountable breach separate from neutral cancellation for dead/unavailable or
unfunded parties. Waiting, review and mutual-cancellation talks never extend the term
or allocate a second independent weekly decision chain.

Performance still consumes the live obligation before the agreed gold transfer and
50 client prestige; the latest receipt now retains the agreed delivery term. Refusal,
expired quotes and unsuccessful counters charge nothing. No alliance, war, criminal
reason, title, native sanction, inherited obligation or debt is introduced. Actor
rules/effects/terms are identical for AI and player; the existing bounded initial
liege selection and scheduler remain. Behavioral rates, balance and performance
are not measured. Ordered effects are not proof of engine transaction atomicity.

## Identity, old state and validation

New quotes store delivery days and every snapshot captures them. A persistent field
requires the matching captured value and only fourteen/thirty are supported here;
missing/stale/unsupported delivery cannot authorize consent or performance. Serial,
revision, price/mode and party checks remain required as before.

Only records **without** the new field use the original thirty-day legacy default.
Snapshots default to thirty before reading an actual field; an old callback without
a delivery scalar may still match an old field-less record under its exact original
identity. Legacy acceptance initializes thirty only if absent. A fourteen-day field
cannot be reset by this fallback. Existing field-less obligations retain their original
flags/callbacks; owner-only orphan cleanup stays possible without weakening payment
checks. New offers overwrite old inert fields with a fresh serial and default thirty;
cleanup removes the active delivery field, never identity counters. Old-save migration,
scalar persistence and stale-event isolation themselves remain engine-unverified.

Fourteen adversarial source-contract tests cover clause identity/fallback, mutation
order, independent counters, exact role/mode, deadline/timeout pairing, no prepayment,
no renewal, receipts, full summary/localization and AI parity. They execute no CK3
simulation. DELIV-01…10 in FINAL_ENGINE_TESTS.md remain unrun. G2's arbitrary-clause UI,
engine consent/persistence and G3's title enforcement gates stay open. Next continue
independent negotiation/obligation work; do not request the standby title ZIP until
the owner is available or brings it back.
