# One agreement, three independent actions — N5

**Static-checked only; not engine-tested.** Original CK3 scripts now offer a single
versioned agreement combining a gold payment, public endorsement and release of one
exact political restitution charter. This releases a custom political commitment,
not a native title, claim, crime or landholding restriction.

## Actual shared consent

An eligible current sovereign can propose the bundle from an active, explicitly
recognized charter involving a living landed house head. Both are at peace at issue.
The sovereign promises **25 gold and public support**; the head promises to release
the specified charter. A counter changes the gold amount between **25 and 50** and
moves the responder. The source charter/serial/revision, authority, house, title,
original payer/payee and fixed three-clause recipe cannot be changed by a counter.

The latest proposer consents by proposing/countering. The other original party
explicitly accepts **all three clauses at the same revision and price**. Acceptance
closes negotiation and stores proposer, actual accepter, revision, price and date,
then initializes all three action results as pending. It performs **no** transfer,
endorsement or release. There is no self-acceptance, inherited signature or partial
acceptance masquerading as a complete deal. Either original party can freely close
an unaccepted proposal after losing resources, office or the deadline.

This third adapter reuses all six N4 native contract primitives with `PREFIX = ba`.
The negotiation state `paid` concerns the gold leg only; `rw_ba_agreement` separately
tracks negotiating/declined/active/fulfilled/partial. A paid gold receipt never
means the other two actions happened. This fixed recipe is the first multi-action
agreement, not arbitrary user-authored action lists or support for every service.

## Separate voluntary execution and results

After acceptance, each original person has **thirty days** to perform their own
clauses, in any order, or explicitly refuse each still-pending clause:

| Action | Actor and current guard | Receipt / result |
|---|---|---|
| Gold | Original sovereign personally has the quoted gold; both endpoints living free adults, not at war with each other | Attempt consumed and exact price/version receipt written before one debit/credit; completed after the commands |
| Public support | Original sovereign and recipient meet existing public-service eligibility | Attempt/version/actor/date written first, recipient gains 50 Prestige, then existing public native-memory projection; completed after commands |
| Charter release | Original head, exact still-active source revision, current sovereign/head roles and recognition, plus original guarded release entry | Attempt consumed before `rw_ch_release_effect`; completion requires the exact source's released state, next revision, actual head and date; observed result is copied into this agreement |

Original party identities remain fixed. The release checks do not silently refresh
an obsolete parent revision. A successor cannot perform or inherit a predecessor's
personal signature. Once the original release is completed, **payment and support
remain executable** independently of that charter becoming inactive. Loss of title
need not prevent voluntary personal gold payment; support retains its own eligibility.
Native title/war/succession/banking/secret behavior is not replaced.

Every action has its own pending/attempted/done/refused/expired/unavailable state.
A refusal requires the actual responsible actor and records its date. Lack of funds,
changed jurisdiction or death is never automatically an explicit refusal or crime.
An unrelated external charter release does not retroactively fulfill this clause.
An uncertain release attempt is retained as attempted and cannot be sent again.
The agreement is fulfilled only when **all three** results are done. Otherwise,
when no pending actions remain, it closes as partial. Completed actions are never
undone, silently refunded, repeated or converted into an automatic sanction.

There is no atomic native transaction, rollback or guarantee that future performance
will occur. In particular, one party may receive performance then refuse its own
clause. The record preserves that distinction rather than forcing compliance.
Completed command receipts are script state, not external engine-validation evidence.

## Bounds, information, custody and AI

- Seven-day proposal window, with no counter/review renewal. Acceptance can occur
  only once; its thirty-day execution window is written once, so execution cannot
  extend beyond 37 days from issue. Fixed retention is 1,863 days from issue;
  no terminal action extends it.
- One proposal per exact charter revision/representative context, plus a shared
  ninety-day issuer cooldown. A genuinely changed context may permit a new proposal;
  an old record never becomes a new party's consent. Multiple independent sources
  can have independent records and results.
- Only the two original addressed parties can read the independent agreement. The
  title/house/authority were known public source terms; no private evidence, reply,
  native secret or other affair is copied. Parent history, money and signatures are
  not granted to a custodian, liege, heir or other current representative.
- Explicit review filters the bundle index for that actual reader and snapshots
  only their own records. No world-character-pair scan. Saved reply events never
  refresh their quotes. Read-only status text shows an elapsed deadline even before
  the expiry callback updates stored pending results.
- Storage can move only to a living original party, explicitly excluding a departing
  owner even if native alive flags lag. Known signatory death marks pending actions
  unavailable, preserves previous results and transfers no obligation. Mere storage
  owner death is not a signatory's failure. With neither party alive, retire the
  record after removing its global index entry.
- Only local sixty-day maintenance and one fixed day-31 post-acceptance callback per
  original party reconcile expiration; callbacks do not execute clauses. Original
  performance/refusal/counter replies queue bounded next-day opportunities. Reads
  and maintenance do not repeatedly schedule action prompts.
- The existing charter opportunity reaches both human and AI sovereigns; replies
  and individual execution use identical rules and costs. Resource, context and
  pending-state guards apply to both. AI weights use traits without guaranteed
  cooperation. Spam, volume and native event/snapshot semantics await final testing.

## Available checks and readiness

Twenty-six adversarial source tests cover immutable packet/recipe/reader/source,
latest opposite-party signature, fixed deadlines, all six N4 bindings, absence of
performance at acceptance, exact original actors, consume-before-effect, per-action
receipt integrity, all-done versus partial completion, free own refusal, independent
execution after release, native release postcondition, custody/death/index cleanup,
EN/FR status board and exclusion of native law/AI privilege/global-pair overrides.
These inspect actual CK3 source and literal template substitutions; no Python game
simulation or engine parser is introduced. Existing N4, charter, public-memory and
other available checks remain applicable. Native APIs are the existing N4 model,
M4 public support and original guarded charter-release path; no new target-version
API claim, third-party source or assets are distributed.

N5 earns **+2 development points** on the frozen rubric: development **57/80**,
validation in CK3 **0/20**, total **57/100**. Next substantive target is J3, the
lawful/arbitrary sanction distinction with native penalty deduplication. G1/G3 stay
open; this agreement does not implement coercive house/title sanctions.

## Final campaign — all UNRUN

| Case | Required observation |
|---|---|
| BUNDLE-01 | Current recognized sovereign proposes only for the exact eligible active charter; source context replay and issuer cooldown cannot be bypassed. |
| BUNDLE-02 | Each current responder sees the same fixed three clauses and gold version; counter/self/stale/deadline/role changes cannot reuse old consent. |
| BUNDLE-03 | Acceptance records both original people and all three pending clauses without any early gold/prestige/release. |
| BUNDLE-04 | Execute all six orders of the three actions, including release first; independent pending gold/support still work afterward. |
| BUNDLE-05 | Poor or imprisoned/dead/ineligible actors, war, stale views and changed head/ruler/source revision block their relevant actions without inventing refusal. |
| BUNDLE-06 | Duplicate clicks, queued old boards and save/reload produce at most one correctly directed gold transfer, support performance/memory and release attempt. |
| BUNDLE-07 | Original guarded charter release and exact result receipt agree; unrelated prior/external release or changed source never becomes fulfillment by inference. |
| BUNDLE-08 | Each party can explicitly refuse only its own pending clause, even without means/office; already completed actions remain and no automatic refund occurs. |
| BUNDLE-09 | Three successful results alone produce fulfilled; partial/refused/expired/unavailable/uncertain outcomes stay distinct and cause no native legal reason. |
| BUNDLE-10 | Seven/thirty/1,863-day limits survive counter/review/save; day-31 callbacks and local maintenance close pending results without repeat prompts or native actions. |
| BUNDLE-11 | Only original addressees see terms/results; successor, custodian, liege and unrelated journal readers gain neither knowledge nor consent. |
| BUNDLE-12 | Either original party dies first, including lagging alive flag; surviving original retains completed receipts, no heir pays, and no dangling index remains after retirement. |
| BUNDLE-13 | Source retirement, outside charter resolution, competing voluntary agreements and changing representatives preserve actual independent receipts without causal relabeling. |
| BUNDLE-14 | Human/AI and AI↔AI exhibit acceptance, counter, refusal, partial execution and fulfillment with the same guards/costs; final G2/G4/G5 measures event/index volume and AGOT regression. |
