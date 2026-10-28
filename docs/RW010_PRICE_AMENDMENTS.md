# Mutual price amendments to accepted promises

**Original CK3 scripts; static-checked, not engine-tested.** The title-source
collection stays on standby. This independent slice lets either existing party
propose a reduction from 50 to 25 gold on a due deferred endorsement. It is a single
authored amendment type, not an arbitrary multi-clause composer or a limit on future
useful types. There is no runtime Python, native title/war change or paid service.

## Explicit consent while the original contract keeps running

After the minimum seven days and before the original 14/30-day delivery deadline,
the provider can offer a reduction or the client can request it. The other party
must explicitly accept. The request shows both names, old/new price, unchanged
delivery clause, seven-day response window and no payment/performance now. The
original price remains 50 until acceptance. Either party can review through the
mapped interaction; only the responder can accept/refuse, only the proposer can
withdraw. The interaction's automatic acceptance merely opens this negotiation.

New requests require current eligible parties and at least 25 client gold. Acceptance
rechecks those current funds; refusal does not require money. War, death, loss of
eligibility, contract change, request expiry or delivery expiry block consent.
Proposer withdrawal is identity-checked separately and need not pass performance
eligibility. A party's heir inherits neither this offer nor personal consent.

The seven-day request/cooldown and monotonic per-provider amendment serial bound
repeat offers without resetting the original clock. An outstanding amendment and
an outstanding mutual-cancellation request cannot be proposed concurrently. Refuse,
withdraw or let the request lapse to free that negotiation lane. Ordinary fulfillment,
wait, deliberate breach and the original timeout remain available throughout; there
is no new penalty for rejecting or ignoring an amendment. Reviewing never renews it.
An unexpired request cannot survive the original delivery deadline for acceptance.

## Acceptance changes one term, not the service clock

The request binds the original contract parties/serial/accepted revision/mode/price/
delivery plus its own proposer/responder/serial/window. Consume the request before
writing price 25. No gold, prestige, opinion, new service or criminal reason is
produced. Consent does not itself perform the promised endorsement.

The accepted contract's serial/revision, minimum wait, due flag and original timeout
are left intact. The separate request serial versions amendment consent. Old visible
or pending decisions capture price 50 and fail the existing exact-price identity after
acceptance; a fresh price-25 snapshot and provider decision ticket replace them.
The latest performance/breach/release receipt records the actual agreed price before
terminal cleanup. Neutral orphan/unavailable cancellation clears uncertain price
metadata rather than carrying a previous receipt's value forward.

A critical timeout adaptation keeps the **original** callback authoritative: only
its exact immutable contract owner/serial/revision, actual provider actor and expired
due flag may refresh current stored price/mode/delivery scalars. Missing price/mode
skips that read and falls back to existing neutral cleanup. Then the existing live/
eligibility/affordability checks determine accountable breach or neutral cancellation.
A client holding 25–49 gold after an agreed reduction is no longer judged against the
obsolete 50-gold snapshot. This refresh cannot pay, target another contract, reset
expiry or turn an early/stale callback into an authorized timeout.

## Reactive opportunities and races

New promise acceptance schedules one fixed client opportunity on day eight. Providers
receive the new choice in their existing decision panel. AI/player use the same
proposal, consent, funds, cooldown and result rules. Manual menu initiation has AI
weight zero because those bounded opportunities supply targeting; no all-pairs scan
or automatic acceptance is added. Existing promises get the menu/provider option
without retroactively manufacturing the client's missed one-off opportunity.

A provider choosing the amendment from a performance panel first replaces the current
reminder with a single three-day revisit, **before** sending the proposal. This gives
shorter contracts another ordinary performance opportunity while a reply is pending.
If consent arrives immediately, it can replace that ticket without a later caller
continuation overwriting the fresh decision. Subsequent normal waits keep their
existing seven-day cadence. No independent parallel reminder chain or new timeout is
created. A late request/revisit can still outlast the original deadline; it never
extends the promise or excuses its breach.

If the provider performs/breaks first, or mutual release/timeout closes the contract,
ordinary cleanup removes amendment flags/parties; an old reply cannot alter a new
contract. Pending offers remain seven-day timed markers with inert latest-response
fields after silence, not a complete request history. Lifecycle, event ordering,
request/ticket isolation and save/reload still require CK3 evidence. Ordered state
changes are not a demonstrated atomic engine transaction or recovery mechanism.

Sixteen adversarial source-contract tests cover exact identity/roles/funds, once-only
consent, immutable clock, current-price timeout, old decisions, separate cancellation
lane, cleanup/receipts, full terms/localization and bounded shared AI opportunities.
AMEND-01…12 final scenarios remain unrun. G2/G4/G5 and runtime compatibility remain
open. Next audit integration of revised obligations, receipts and mediated disputes
without requesting the standby title sources or intermediate CK3 runs.
