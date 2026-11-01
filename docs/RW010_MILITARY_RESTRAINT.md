# Personal military-restraint pledges and conditional native war observations

**Original CK3 scripts; static-checked, not engine-tested.** This adds a continuous
personal undertaking and private memory. It is separate from G1 / RW-004: declaring
a genuine-CB war despite a royal ban is still unresolved and must not be represented
as implemented by this pledge. No native war declaration or restriction is changed.

A living landed adult at peace may offer another such adult a personal undertaking
**not to become primary attacker against that beneficiary for ninety days after
explicit acceptance**. Both must be free from imprisonment. The beneficiary has
seven days to accept, decline or wait; native interaction auto-accept merely opens
the offer, never creates consent. Refusal, silence and expired offers create no
obligation, truce, payment, prestige, opinion or legal consequence.

Explicit acceptance consumes the offer window, stores its date and starts exactly
ninety days before notices. The original promisor may freely renounce an active
pledge and the beneficiary may release it. Those exits need exact personal identity
and a live accepted record, not current wealth, rank, peace or imprisonment capacity.
No automatic sanction, refund, debt, forced peace, hook or legal finding follows.
Reading or waiting never renews offer, undertaking, retention or cooldown.

## Independent personal records and private access

Each offer creates its own typed story owned by its original promisor. Stored
provider/beneficiary, schema, monotonic serial, story identity and current actor
must match at every action. Accepted/terminal/observed views additionally require
the corresponding dates. Copied successor metadata cannot authorize a different
owner, and owner death ends this personal story rather than migrating a duty.
Other financial/favor/service/case records and indexes are not modified.

Retention is fixed to five years from proposal, never reset by acceptance or closure.
Local sixty-day cleanup retires expired records. It may label lapsed offer/active
metadata neutral elapsed, without notifications or an inferred verdict. Before that
cleanup, due/window guards and event display already prevent late acceptance or
continued actions. No callback is needed to unblock a single character-wide slot:
records are independent, with no latest-record overwrite or count-based truncation.

Both original parties can inspect known stories owned by a selected promisor through
a private review interaction. Outsiders, heirs and a merely common liege get no
reader role. Review filters only that owner's stories, captures immutable identity
and opens the current panel; it never creates acceptance, performs a native action,
reschedules events or extends retention. No exhaustive historical ledger is promised.

## Conditional observation, preserving native wars

A new named child is appended to `on_war_started`; it replaces no native/AGOT effect,
trigger, event list, CB, Mega War, truce or war-lifecycle definition. The source
receipt identifies two privately received original files by hash/size and marker
locations; no proprietary source is distributed. The CK3 source describes the
callback's declaration context and uses attacker/defender/war scopes; native source
also uses the war's primary role accessors. AGOT attaches its own Mega War children
to the same entry point. This is source evidence, not proof of runtime composition.

Intake requires a fresh callback with existing war, distinct living attacker and
defender and both agreeing with that war's **primary** roles. It enumerates only the
actual attacker's owned stories, then checks exact original promisor/beneficiary,
schema, accepted date, active state, live ninety-day marker and retained record.
It consumes that record before writing observation/finish dates and notifying its
two original parties once. Duplicate callbacks see a terminal record and cannot
notify again. No world-pair scan, native effect replay or old-war backfill is added.
No native war object is retained across war termination or reference destruction.

The resulting fact is **primary attacker/defender roles observed during an accepted
undertaking**, not a claim of voluntary initiation, deliberate betrayal, legal guilt,
CB validity or culpability for a scripted/revolt/Mega War outcome. Defensive roles,
secondary participation, other targets, old/expired/unaccepted/renounced/released
pledges and missing or inconsistent scopes create no observation. Missing callback
coverage/order cannot certify fulfillment: expiry stays neutral, with no automatic
success reward or breach penalty. Native declaration, resistance, wars, succession,
CBs, bans and hook exceptions continue to decide what the game permits.

## AI and checks

AI and player use the same offers, consent and exits. Initial AI selection is bounded
to the direct liege, with low willingness and honest/paranoid/deceitful/forgiving
response weights; manual review is cosmetic. A shared actor offer cooldown of one
year bounds spam for both, without a global cap on available target/story records.
Durations/weights are provisional and actual AI opportunities/behavior/performance
have not been measured. No new recurrent notification or character-pair polling.

Seventeen adversarial source tests cover private identity/owner/dates, consent,
immutable clocks, exact native primary roles, accepted target matching, expiry,
consume-before-notice duplicate protection, additive callback composition, free
exits, neutral cleanup, independent archive access, native-state isolation, AI parity,
EN/FR and the hash-only source receipt. The full suite and structural/distribution
checks run separately. They do not simulate CK3. MREST-01…12 in FINAL_ENGINE_TESTS.md
remain unrun. Callback propagation/order/scope lifetimes, war categorization, date
expiry, UI/privacy/save/load, story costs and actual AGOT compatibility require the
owner's final campaign. No intermediate game run, upload, paid service or runtime
Python/LLM is needed. Further contextual responses and other undertaking types remain
separate work; G1 and universal G3 enforcement stay unresolved.

## Voluntary personal response extension

RW010_RESTRAINT_RESPONSES.md adds a fresh original-party explanation/reaction
window after a new exact role observation. Request, acknowledgment/contest and
optional personal rancour remain separate from native roles and legal truth.
Silence, old records and expiry never create a penalty or admission.
