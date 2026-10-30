# Native individual-title revocation: legality review and private provenance

**Experimental source implementation; not engine-tested.** Native revocation still
performs the confiscation and handles acceptance/refusal. This slice adds a narrowly
guarded post-transfer observation and private provenance journal. It does not create
a new coercive interaction, force a title transfer or prove a particular offense
was punished. All CK3 runs remain deferred to the final campaign.

## Source findings: three independent checks

Six received files were rechecked against the verified TitleRoutes manifest.
TITLE_PROVENANCE_SOURCE_RECEIPT.json publishes hashes, relative references and short
marker positions only. Original sources/full manifest remain outside Git.

1. The AGOT interaction requires native realm-law authority, current direct-vassal
   eligibility and protections, including contracts, strong hooks, protected titles
   and diarchy. Its referenced standard validity helper separately checks war/truce
   and an allied vassal without a revocation reason. The inspected standard helper
   definition is CK3's; this subset does not establish all effective AGOT overrides.
2. Title selection has its own exclusions: contested titles, noble-family and
   religious-head titles, recent grants and special administrative restrictions.
   A character-level revocation reason does not identify which title can be taken
   lawfully. Native tyranny evaluation also considers claims, religious protection
   and administrative cases. The mod does not copy this into a new verdict.
3. Acceptance and refusal are different native paths. Acceptance marks its native
   revocation context and invokes the existing helper, which consumes native reasons
   and applies consequences. Refusal has its own consequences/resistance. Calling
   the helper or forcing a transfer independently would bypass that full route.

The existing native revocation window remains the action entry. Neither opening
it, a known plot, political censure, a current reason nor a generic title loss is
recorded as completed confiscation.

## Conditional post-transfer intake

The original provenance slice appends **one named child** to source-located
`on_title_gain`. The wrapper now also dispatches an independent conditional
pledged-title observation child (RW010_PLEDGED_TITLE_OBSERVATIONS.md); it does not
change this revocation-context child or prove a native transfer route.
This is separate from the optional G3 diagnostic: no debug marker, log or trace UI
is added to the base. Existing native effect/event fields are not replaced.

Intake and effect both require all of:

- Native root equals the native actor, and is a living adult new holder.
- Exact native title exists, is currently held by root, and is county tier or above.
- Previous holder differs from root and equals native recipient.
- Native selected `landed_title` equals that exact transferred title.
- Native `revoke_title_interaction` marker is present.
- Root already owns a retained, typed exposed-participant observation concerning
  that exact former holder. Hidden participants and other observers' facts do not qualify.

**Scope propagation is unresolved.** Source locates the acceptance marker and the
post-transfer callback separately; it does not demonstrate that actor, recipient,
selected title and marker survive together, or that the marker is set before that
callback. Missing or mismatched context creates **no entry**. Do not weaken this to
"any title moved to a liege", infer a cause from usurpation, use an earlier UI click
as proof, or replay native effects to obtain a receipt. Engine evidence must also
exclude stale inherited context in unrelated same-event transfers.

Thus the stored kind is explicitly `native_revocation_context_transfer`, not a
per-offense conviction or universally certified revocation transaction. The original
transfer facts contain no scheme pointer, per-offense legal verdict or pardon.
The subsequent optional private intention link (RW010_REVOCATION_INTENTS.md) records
the issuer's declared basis, not a native causal attribution.
Having relevant private evidence explains why this observer keeps the note; it
does not establish why the native action occurred.

## Stored facts, repetition and privacy

A fresh independent personal story stores schema/kind, a monotonic observer serial,
the exact title, former and new holder, observation date and five-year retention.
Creation verifies fresh story type/owner/uninitialized schema before writing.
One-day coalescing checks exact observer/title/former/new holder before creation;
repeated observations do not renew the original window or five-year term.
This deliberately coalesces distinct genuine same-tuple transfers inside that
window too. It is **not an exhaustive transaction ledger** or native operation ID.
Other titles or former holders remain separate. No original fact is overwritten.

The journal interaction enumerates only the actor's own valid retained records.
The character selected to open the interaction receives nothing. Every popup
captures record serial/title/former/new holder and rechecks exact owner/identity,
retention, description and portrait before access. Current ownership is queried
separately: if the title moved again or lost its holder, the note grants no power
over its present holder. Reading creates no state, payment or retention renewal.

Retention gates access immediately; the existing story pattern checks cleanup
every sixty days. Personal records end on owner death and are not inherited by
heirs, current sovereigns or house heads. This is not yet the durable institutional
provenance needed for restitution generations later. The existing political house
register remains separate and does not acquire private guilt/evidence from this note.

## AI, scope and next implementation

Both AI and player native actors use identical automatic intake/retention guards.
There is no new AI decision or forced revocation policy, no world/pair scan and no
human-only exception in collection. Archive UI adds no gameplay action. Only the
callback's relevant owner's stories are inspected; no global provenance index or
per-title native state is changed. The effect writes only new RW metadata and its
own counter; it consumes no reason and repeats no native costs or sanctions.

The subsequent explicit association is in RW010_REVOCATION_INTENTS.md: one fresh
transfer observation can match a previously confirmed exact-affair/title intention,
with private bidirectional serial/pointer checks and no retroactive link. Native
callback context still needs final evidence. A subsequent optional independent
**public-fact** crown archive is in RW010_LAND_REGISTER.md: only fresh sovereign
observations capture authority/former house, and explicit filing copies title facts
without private case pointers. Its successor custody/long retention is experimental;
individual restitution remains next. A later restitution must recheck the
exact current title/holder, authority, recipient, consent and native grant rules;
it must never seize land from a third party on an old note's authority. G3's house
ban/status restoration and G1 remain unresolved. No full confiscation/restoration
feature is marked complete by this journal.

Thirteen adversarial static tests cover native wrapper preservation, missing/wrong
marker/scopes, exact current holder/title, already-known private evidence, repeat
window identity/non-renewal, fresh constructor, immutable receipt fields/serials,
private retention/owner death, stale/swapped popups, read-only ownership, EN/FR and
absence of native effects, hidden knowledge or AI exceptions. These tests do not
execute the callback or establish engine timing, load composition or performance.
PROV-01…10 in FINAL_ENGINE_TESTS.md remain unrun.
