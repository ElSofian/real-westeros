# RW-010 — deferred endorsement promise

**Experimental native CK3 scripts; not engine-tested.** All runtime tests are deferred
to the final campaign per owner. No Python model performs or simulates these effects.

## Consent and terms

Delivery-term extension: RW010_DELIVERY_TERMS.md adds independent price/delivery
counters and 14/30-day accepted deadlines. The original thirty-day default described
below is retained; fourteen-day obligations expire sooner under their accepted terms.

The existing immediate endorsement remains available. A separate **Promise a Future
Endorsement** interaction offers deferred delivery, so player and AI can initiate
it without an implicit checkbox policy. Both use the same eligibility, 25/50-gold
negotiation, cooldown and identity mechanism. Quote mode is explicit, saved, compared
on every response and preserved through counteroffers. Accepting deferred terms
increments revision, invalidates negotiation popups and records a live obligation.
No gold or prestige is transferred at acceptance; the client promises payment only
when the provider performs the service. No escrow, debt, automatic alliance or crime.

Delivery is possible after seven game days and before the thirty-day deadline from
acceptance. The provider receives a decision event on day eight: fulfill, break or
wait. Waiting schedules another decision in seven days without extending the deadline.
The provider may also reopen the same obligation through a review interaction.
AI and humans get the same decision effects and outcomes. AI review interaction
initiation is disabled because scheduled reconsideration supplies its opportunities;
no global character scan is introduced. Actual event timing/AI behavior is unverified.

## Mutual cancellation amendment

RW010_MUTUAL_CANCELLATION.md adds explicit proposals by either party, accepted only
by the other party, without payment/penalty or changing the original deadline.
Pending requests never suspend ordinary performance, breach or timeout.

## Decision lifecycle audit amendment

INTEGRATION_AUDIT.md replaces direct visible reminder scheduling with a hidden,
versioned decision ticket. Reviewing invalidates older decisions and reminders;
waiting creates one current seven-day reminder. The independent original timeout
and cancellation-consent identities remain unchanged. Engine behavior is unverified.

## Performance and failure

- **Fulfill:** recheck exact contract/revision, parties' eligibility, delivery window
  and client funds. Record outcome, consume active state, then transfer agreed gold
  and grant client 50 prestige once. No forced transfer if the client cannot pay.
- **Deliberately break:** a provider can refuse within the delivery window. Record
  a broken commitment, consume the obligation and inform the client. No payment.
- **Wait/ignore:** an independent hidden event checks expiry on day thirty-one.
  If both parties remain eligible and payment is possible, record nonperformance
  as breach. Otherwise cancel neutrally without payment, prestige or blame.
- **React:** after a recorded breach the client chooses resentment (-15 personal
  opinion for five years) or forgiveness without penalty. Contextual referral to a separate common overlord is
  now another option (RW010_CASES.md), consuming this same personal-response opportunity. The response is bound to
  the receipt serial and consumed before the opinion effect. No compulsory execution,
  confiscation, universal reputation, criminal status or inherited guilt.

Gold is never held during the waiting period, so no refund/escrow is needed. Payment
insolvency or loss of eligibility at expiry is deliberately neutral in this first
slice, not a general political-justice rule. A future service may need different
responsibility attribution. Explicit refusal is observable to its client; no wider
rumor/public-knowledge system is implemented.

## Identity, cleanup and migration

Provider holds contract serial, quote revision, client, price, mode and obligation
state. Events save both parties and serial/revision/price/mode. Offer acceptance
invalidates quote events; completion invalidates obligation events. A stale reminder,
quote or timeout cannot clear another contract. Cleanup retains counters.

An owner-only serial/revision guard permits cancellation at timeout even when the
client scope disappears; it cannot authorize fulfillment or payment. The latest
receipt retains serial/client/outcome and reacted serial, not a complete historical
ledger. Multiple receipts/obligations per provider and dynastic transfer are not
implemented. One active service per provider is a conservative slice limitation.

Death of the provider may stop its scheduled events; inert state remains on that
character and no duty transfers to the heir. There is no global death hook. Confirm
actual engine cleanup and save/load behavior in final testing. The client has not
paid anything, so provider death cannot strand funds.

Old pre-mode experimental offer popups cannot settle under the new identity guard;
let their pending flags expire and begin a new offer. This is not a claim that old
saves were tested. Prefer disposable fresh saves for the final campaign.

## Static checks and unresolved engine assumptions

Run `python3 -m unittest discover -s tests -v` and `python3 tools/validate_mod.py`.
Checks cover reference resolution and translation/BOM completeness plus negative
source mutations: payment at consent, unchanged revision at acceptance, unguarded
fulfillment, consume-after-payment, early/stale expiry, missing affordability and
replayed reactions. These inspect source wiring, not CK3 predicate semantics.

Saved value scopes, parameterized begin effects, hidden/delayed character events,
flag timing, AI scheduling, same-tick ordering and save/reload remain unverified.
Consume-before-effects is not proof of crash consistency or transactional native
operations. Do not automatically retry effects after crashes.

## Final engine cases (all unrun)

1. Immediate mode still settles immediately; deferred consent at both prices changes
   neither gold nor prestige and cannot use the immediate settlement option.
2. Deferred counter/requote retains mode and original quote expiry. Acceptance creates
   its own delivery window; old quote acceptance/dismissal then has no effect.
3. Before day seven no fulfillment/review; from day eight fulfill at agreed price once.
   Replaying a popup/review after fulfillment cannot pay or grant prestige again.
4. Explicitly break: no funds/prestige move. Test forgiveness and resentment separately,
   including replay after reload or after a later contract receipt supersedes it.
5. Wait several times, close/ignore the popup, and run time to day thirty-one. A live,
   funded and eligible unperformed obligation should break once, with optional reaction.
   Delayed reminders firing after expiry/completion must be inert.
6. Spend client funds, start a war, lose land, kill a party or invalidate the client
   scope before expiry: no transfer/false punishment. Verify owner-only orphan cleanup
   cannot clear a newer serial or revision and cannot cause payment. No heir inherits it.
7. Save/reload before/after acceptance, each wait and every outcome. Compare AI/player
   decisions; use repeated review interactions and same-tick clicks to probe reentry.
8. Compare an AGOT-only baseline, error logs, balance and performance. Record actual
   CK3 build, AGOT version, DLC, playset and commit before any gameplay success claim.
