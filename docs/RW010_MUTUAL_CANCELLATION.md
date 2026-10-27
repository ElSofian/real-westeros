# RW-010 — mutual release of a deferred promise

Status: original experimental CK3 scripts, **not engine-tested**. Runtime testing
is deferred to the final campaign. This extends RW010_DEFERRED.md without changing
native CK3/AGOT crimes, secrets, hooks, wars, titles or relations.

## Consent and timing

Both provider and client have a separate interaction on the other party to propose
ending their active deferred endorsement. The auto-accepted interaction **only opens
a request**; the other party must explicitly accept in an event to end the promise.
They may instead reject or leave it unanswered. An accepted release has no gold,
prestige, opinion, payment, refund, service or breach effect.

The request lasts seven days. One active request and a shared seven-day cooldown
per provider prevent duplicate requests/popups. There is no lifetime request count
limit. A new request after the cooldown gets a new serial; it cannot revive an old
response. Requests may be made before delivery is due, during war or without funds,
as neither offering nor accepting them performs the service. Both parties must
still be alive, adult and landed, and the original promise must be unexpired.

A request **does not suspend the promise**, change its quote revision, price or mode,
or extend either its delivery window or deadline. While a request is pending the
provider can still fulfill, explicitly break, wait or become accountable at the
ordinary deadline. Those outcomes invalidate its pending cancellation request.
Silence/expiry/rejection alone neither cancels the promise nor records a breach.
Once the obligation has ended, a stale cancellation response cannot reclassify it.

## AI and state

The client receives a keep/propose opportunity once when deferred terms are accepted.
The provider receives the same proposal action alongside fulfillment/refusal/wait
at the existing scheduled decision. Choosing to propose there schedules the ordinary
weekly revisit, so ignoring/rejecting a request cannot stop provider reconsideration.
Both AI and player have the same guards, choices and effects. Interaction AI initiation
is disabled in favor of these event-driven opportunities, avoiding a second popup
loop or scans of all character pairs. Actual timing and choices remain unverified.

Every response checks the full saved service identity (both parties, contract serial,
quote revision, price and mode), live original deadline, request serial, proposer,
responder, request window and responder root. A separate persistent request counter
never changes the service revision, preserving existing delivery/expiry callbacks.
A stale/different request cannot accept or clear a newer one under these guards.

Acceptance writes the latest receipt as `mutually_released`, including request serial
and proposer, then consumes the original obligation and request before notices. Existing
break/fulfillment/neutral-cancel cleanup also clears pending request state. Counters
and the seven-day cooldown survive cleanup. Rejection clears only its matching request.
Expired requests may leave inert actor variables until replacement/terminal cleanup;
these are not permission to settle without the live request flag.

This uses the existing **latest receipt only** model; a later terminal receipt replaces
that provider's previous receipt. It does not implement a complete history of every
promise. Existing independent case records and evidence remain unchanged. A broken
promise cannot itself be retrospectively relabeled as mutually released. No obligation
or personal guilt is transferred to heirs. Existing old saves need no inferred consent;
new state is initialized only when a valid request is made. Migration remains untested.

## Verification

Adversarial source tests cover stale/wrong actor/request identity, expired or ended
obligations, effect-entry bypass, unilateral release/payment, serial reuse, delayed
consumption and changed obligation timing. Graph/localization checks include EN/FR.
These are static source checks, not engine execution or atomicity/persistence proof.
See FINAL_ENGINE_TESTS.md for the final campaign cases.
