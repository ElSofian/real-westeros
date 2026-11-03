# Shared native-script contract model — N4

**Static-checked only; not engine-tested.** A single original CK3 protocol now serves
both private allegation settlements and public charter-release compensation.
This is an integrated script refactor, not a new dialogue variant or Python runtime.

N5 now also binds this protocol to `ba` multi-action agreements; its financial
`paid` state describes only the gold leg, while the complete agreement has a separate
result. See RW010_MULTI_ACTION_AGREEMENTS.md. N4's original delivery/history remains.

## Shared protocol and existing storage

The model binds a `PREFIX` and two responder flags to the existing story's schema,
revision, price, turn, state, issue date, seven-day window and payment receipt.
It owns six shared primitives:

| Primitive | Common responsibility |
|---|---|
| Quote trigger | Schema 1, exact captured revision/price, allowed 25/50 quote, known states and valid offered responder |
| Snapshot | Capture revision and price only during explicit navigation or a genuine proposal/counter |
| Offer | Write price, offered state, issue date, one seven-day window and schema |
| Counter | Increment version first, toggle the quoted price and next responder, never renew a deadline |
| Consume | Remove window/turn and record the accepted price/revision/date before marking paid |
| Close | Remove window/turn and mark closed, without cost or native operation |

`rw_contract_triggers.txt` and `rw_contract_effects.txt` contain these definitions
once. Both systems call all six definitions in actual view/propose/counter/settle/
close paths. Bindings are hard-coded script arguments, never text supplied by players.
Literal CK3 parameter substitution selects existing `rw_as_*` or `rw_cq_*` fields
and captured aliases. No new contract shadow record, world index, common public
journal, duplicated authoritative price or serialized schema is introduced.
Existing live and retained offers continue to use their existing field names/schema;
this introduces no save migration. That is a source property, not proven save
compatibility. The model deliberately supports these two gold-quote protocols;
it is not a universal parser or support for every future service/currency.

## Domain adapters remain authoritative

| Adapter | Rules that remain local |
|---|---|
| Allegation settlement (`as`, provider/client) | Exact original private case/reader and kind, claimant stage, undisclosed admitted/contested statement, jurisdiction/free parties, first claimant offer, case deadline, responder and original payer funds, withdrawal result and five-year retention |
| Charter compensation (`cq`, ruler/head) | Exact public land record and charter, frozen parent revision and original monetary parties, current representatives/recognition, genuinely new context for a fresh offer, monotonic revision, responder/payer funds, consumed charter release and linked actual-actor/result receipt |

The primitives are internal story-scope operations, not public authorization entry
points. Every caller retains its existing fresh domain identity, reader, turn,
context/deadline, roles and resource checks. First revision/first responder and
immutable domain identities are initialized by the adapter. Counters capture the
new quote only after the common revision increment; delayed reply events never
refresh their own quote silently.

The common consume helper writes the financial receipt first. The adapter then
consumes its own action (case withdrawal or charter release) **before** the existing
one personal gold debit/credit and notices. Native effects are not an atomic engine
transaction: there is no rollback or retry claim. Gold direction, actual payer,
actual settling actor, parent result revision, original terms, evidence/disclosure,
free closing, private/public access and existing human/AI execution remain local
and unchanged in source. No access or consent transfers between the two systems.
Native wars, titles, succession, banks, hooks and secrets receive no new override.

This model prepares reuse for N5, but it does **not** deliver an agreement combining
several independent actions, partial outcomes or compensation/rollback machinery.
N5 and the other open criteria earn no points here.

## Available verification

The 39 existing settlement/compensation source checks now inspect the literal
expansion of our own shared templates. Their adversarial mutations still protect
identity, private readers, stale quotes, roles/successors, original deadlines,
receipt/result integrity, cost direction and consume-before-transfer behavior.
Twelve additional source checks validate all six bindings in both systems, correct
storage scope, guarded callers, cross-system contamination, version/receipt removal,
non-renewal, existing serialized keys and exclusion of domain/native effects in the
core. Missing/unknown/duplicate/extra/nonliteral test expansion arguments fail closed.

`tests/contract_source.py` performs only bounded literal substitution for assertions;
it neither evaluates CK3 triggers/effects nor simulates contracts. The distributed
mod contains actual CK3 scripts and has no runtime Python dependency. Native
parameter-in-key/reference syntax is source-located in
CONTRACT_MODEL_SOURCE_RECEIPT.json (paths/line references/hashes only). It does not
prove target-version expansion, scope handling, runtime privacy or save semantics.

N4 contributes **+2 development points** on the frozen rubric: development **55/80**,
validation in CK3 **0/20**, total **55/100**. No other criterion or engine credit.

## Final campaign — all UNRUN

| Case | Required observation |
|---|---|
| MODEL-01 | Both actual systems resolve the native parameterized helpers without missing effect/trigger/variable errors; validate actual scopes and quoted aliases. |
| MODEL-02 | New private settlement and public charter offers capture their own schema, price, revision and responder, never the other system's values. |
| MODEL-03 | Alternating counters increment version before notification; reopening, delayed events and simultaneous distinct offers cannot spend stale consent. |
| MODEL-04 | Fixed seven-day windows and original case/charter deadlines survive counter/reopen/save-load with no renewal. |
| MODEL-05 | Each current authorized acceptance consumes offer and domain action before exactly one correctly directed personal gold transfer; replay and insufficient funds do not pay. |
| MODEL-06 | Private mediation/disclosure/jurisdiction changes and public head/ruler/parent-revision changes invalidate old choices; heirs never inherit monetary consent. |
| MODEL-07 | Legacy schema-1 active/closed/paid records load and remain correctly guarded/readable with the same serialized fields; do not infer compatibility from identical names. |
| MODEL-08 | Free close after expiry/context loss neither pays nor withdraws a case/releases a charter; unknown/malformed schemas and missing snapshots fail safely. |
| MODEL-09 | Public charter history exposes only its original public terms/actual receipt; private allegation terms/replies remain limited to original parties. |
| MODEL-10 | Player/AI and AI↔AI follow identical costs/actions; final G2/G4/G5 covers callback order, native partial-effect failures, performance and AGOT regression. |
