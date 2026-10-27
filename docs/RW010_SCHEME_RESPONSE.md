# RW-010 — discretionary response to an exposed participant

Original experimental CK3 scripts; **not engine-tested**. This extends the private
native observation intake in RW010_SCHEME_EVIDENCE.md. It is a bounded political
settlement, not assassination justice, an arbitrary fine or a criminal pardon.
All CK3 runs remain reserved for the final campaign.

## Choices and explicit consent

A new exposed-participant record receives a 30-day response window. A guarded hidden
event offers the target a political decision one day later, letting native discovery
choices run first. Generic scheme discovery without a known participant cannot
initialize this flow. The target may:

- leave this political contribution aside, with no payment or legal pardon;
- request a voluntary contribution of **25 gold** from a direct vassal or courtier;
- postpone, leaving the original deadline unchanged.

Sending a request explicitly discloses that limited knowledge to that participant.
It records the target's consent to receive the contribution and close this request
if the participant agrees. The participant may pay, refuse, contest, or remain silent.
Payment requires at least 25 gold and transfers that amount once to the targeted
ruler. In return the requestor grants +5 opinion of the participant for two years
if that same custom modifier is not already active. Existing identical goodwill
is neither stacked nor refreshed; AI will not pay for an already-active benefit.
Existing negative opinions/crime modifiers are never removed. No service, prestige, friendship, debt, hook, imprisonment right, native secret
or criminal status is added. It is neither an admission nor a promise of immunity.
Existing native discovery/justice effects remain separate and available.

The target can withdraw an unpaid request. Withdrawal is available even after loss
of land/authority or imprisonment because it charges nobody; the exposed person is
notified if still alive. Payment, refusal, contestation, withdrawal and forgoing
consume this response. None can be repeated to reopen the same record. A later,
independent plot/participant may generate its own record; there is no global count cap.

The participant's denial is recorded alongside the original observation, never as
a replacement. Refusal, silence, expiry and inability to pay create no new offense,
penalty, payment obligation or automatic guilt. Forgoing the contribution also does
not pardon native crimes. The original murder observation remains intact in all paths.

## Authority and liveness

Every demand and reply revalidates the exact typed story, schema, owner/observer,
record serial, recorded participant, participant provenance, original window and
phase. The requestor must be the living adult landed target at their own court;
the participant must be living and adult, their direct vassal (exact liege) or
courtier, and a different person. Neither may be imprisoned for a request/payment.
This narrowly scopes a private political request; it does not establish legal
jurisdiction to execute, imprison or revoke titles.

Only the observer may request/forego/withdraw. Only the named participant may accept,
refuse or contest an offered request. A lost liege/court relationship, imprisonment,
death or expired deadline prevents payment even if a popup remains open. Withdrawal
has a separate harmless owner-only guard. There is no estate/heir substitution.

Successful payment records `paid` and removes the window **before** gold/opinion effects.
The source guard rejects stale/repeated replies; it does not prove CK3 transaction
atomicity or crash recovery between the debit and credit. No automatic retry is added.

## Timing, browsing and AI

The window begins with the original exposed-participant observation. Requesting,
reopening and delaying do not renew it or the five-year evidence retention.
Expired open/offered state is displayed as an unanswered expiry, not as a refusal
or agreement. Existing old records without response metadata gain neither inferred
consent nor a new window; this is not a tested migration claim.

The private journal retains its read-only observation/history views. Explicit
**Consider My Political Response** opens a separate decision; mere browsing changes
nothing. It can reopen an active target decision or an unpaid withdrawal decision.
**Read the Recorded Political Response** shows the outcome, including an unexpired
pending offer versus silence after expiry, without executing a response.

A separate interaction on the requestor permits the named participant to revisit
only still-active requests explicitly addressed to them. It enumerates only offered,
retained, schema-bound participant-matching records and opens the reply event after
full execution revalidation. It grants no access to the target's private journal,
other participants, hidden organisers, or other people's observation records.

The target gets the initial day-one opportunity; the participant gets the explicit
demand. If still unanswered, both get **one** guarded reconsideration seven days
after the request: the target can withdraw and the participant can reply. Later/ignore
and manual browsing never schedule additional reminder chains. AI and player use
the same events, guards, costs and outcomes, with contextual opinion/war/funds weights.
There is no global character-pair scan, recurring popup loop or runtime LLM. This is
bounded opportunity selection, not a complete proactive political AI implementation.

Each delayed event rechecks record/role/state/window before opening anything. Same-day
withdrawal/payment ordering should allow only the first valid terminal choice, not
both. Native end-of-plot does not itself end this short political response: it relies
on the retained observation, not a dangling live scheme pointer. Observer death ends
the personal story; participant death prevents payment. No duty/guilt is inherited.

## Available verification and next stage

Static adversarial tests cover wrong/old/generic records, wrong actor, phase/window
replay, missing funds, lost authority/prison state, unilateral charging, consume-after-
payment, deadline renewal, evidence rewriting, private demand filtering, withdrawal,
AI opportunity wiring, non-stacking goodwill and reminder recursion. EN/FR and custom references are checked.
CI still exercises the collector on Linux/Windows; actual CK3 tests remain unrun.

Final RESPONSE-* scenarios are in FINAL_ENGINE_TESTS.md. Verify exact gold conservation,
separate native rights/penalties, privacy, scoped history, stale callbacks, save/reload,
AI timing and dead/relocated/imprisoned parties before any runtime claim.

Next investigate native legal eligibility and prior consequence state before adding
coercive personal sanctions. Confiscation, execution, family/house consequences and
restoration remain unimplemented stages (including G3), not implied by this payment.
