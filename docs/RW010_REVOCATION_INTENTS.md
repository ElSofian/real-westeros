# Exact-affair title-revocation intentions

**Original CK3 scripts, static-checked; not engine-tested.** This adds a private
declared intention and optional correspondence to the conditional native transfer
journal. It does not force revocation, create a lawful conviction or implement
ancestral restitution. Native action and the issuer's declared basis stay separate.

## Select a title, then explicitly confirm an affair

For a direct vassal currently in the observer's custody, **Consider revoking a
specific title** offers a generic title picker. It uses `target_type = title` and
recipient-domain selection, not the native revocation special interaction. Three
private source references were hash/size/marker verified; only references are in
REVOCATION_INTENT_SOURCE_RECEIPT.json. No native interaction or its effects are copied.

Selection opens a confirmation for each retained, typed, observer-owned exposed-
participant observation concerning that exact recipient. Each confirmation captures
that observation's pointer/serial plus the selected title and subject. It names the
title, person and private observation number; it can instead open the original
observation for reading. Selecting a title or auto-accepting this navigation is
**not consent** to an intention. No candidate observation is selected arbitrarily.

Explicit confirmation rechecks the current free adult landed observer, living adult
direct vassal/prisoner, exact selected title's holder, retained private observation
and subject identity. Native character-interaction validity must allow reviewing
revocation. Ordinary county-or-higher land titles are considered, excluding noble-
family/landless titles. This readiness check does not establish title-specific
lawfulness: the native picker still owns contested/protected/recent-grant and other
restrictions. If the unselected native validity query rejects the context, no
intention is offered. No guard is bypassed to make it appear.

Only one live pending intention per issuer/title is allowed, so the same native
transfer cannot silently choose between competing declared affairs. This is not a
cap on the number of titles or affairs: other titles remain available, and the
issuer can withdraw the first intention before recording a different basis.

## Intention lifecycle and native action

A fresh independent personal story stores issuer, title, subject, basis pointer/
serial, monotonic intention serial, issue date, pending state, a fixed thirty-day
window and five-year retention. Construction verifies fresh type/owner/uninitialized
schema before writing. Recording costs nothing, sends no demand, creates no native
legal reason and transfers no title. No native crime/scheme pointer is copied.

**Review my title-revocation intentions** shows only the actor's own records; the
selected character receives nothing. Record serial, basis serial, title and subject
are captured and rechecked for every popup. Pending, withdrawn, corresponding-
transfer-observed and expired are distinct. Withdrawal is permitted for an owned
pending record even after custody, title ownership, legal readiness, basis retention
or the thirty-day window has changed; it charges nothing and cannot undo a transfer.
Observed/withdrawn records cannot be reactivated. Reads and links never renew clocks.

For a still-current pending record with its exact retained basis, a human issuer may
open ordinary native revocation terms after fresh current-party/title/native checks.
No title, hook or terms are preselected or sent. The person must select the intended
title and confirm within the native window; selecting a different title leaves this
intention unmatched. Opening, cancelling or native refusal is not execution. AI
retains its native revocation decision/refusal/war policy; no forced interaction or
duplicate native helper/cost/consequence is introduced by the intention.

## Match only a fresh conditional transfer observation

The existing TP constructor first requires its complete native revocation context
and creates/initializes its typed transfer record. Only then does it set a temporary
fresh-receipt alias, call the linker and clear the alias. An existing journal entry
cannot be attached later merely because somebody now records an intention.

The linker rechecks that fresh alias, typed/private TP identity and serial, native
actor/recipient/selected-title/acceptance marker, actual current holder and exact
title/former/new holder. It requires exactly one matching owned pending intention,
still inside its original window, with the same title/subject and exact retained
private basis/serial. Zero or ambiguous matches do nothing. Missing native callback
scope propagation/order remains an unresolved TP limitation: it creates no entry
and no association. This feature adds no new native title callback.

The intention's window is removed and its state becomes `observed` **before** the
two records receive their pointer/serial links. Repeated linking cannot reuse that
pending record. Ordered metadata writes do not prove engine atomicity. The source
basis is the issuer's declared political reason, not proof that the native engine
identified or punished that offense. A matching title transfer is correspondence,
not a newly inferred legal verdict or causal attribution.

TP's existing one-day tuple coalescing is preserved. A second genuine same-tuple
transfer inside that interval may have no fresh TP entry and hence no new link;
never attach the earlier entry as a workaround. Neither journal is exhaustive.

The TP view reveals the declared-basis line only when both private retained records
agree on intention/receipt serials, pointers, title, subject, observed state and basis
serial. Expiry, owner death or a broken link hides it without altering any title.
Intention stories remain personal, end on issuer death and expire after five years;
they do not yet provide institutional/multi-generation restitution provenance.

## AI opportunities, persistence and final evidence

Each newly exposed-participant observation marks scheduling once, then supplies
two fixed opportunities at days two and thirty. Both AI and human get the same
confirmation and create/withdraw effects. Current custody and readiness are checked
when dispatched. A random currently selectable held title supplies the suggestion;
the helper clears stale title aliases before selection. There is no primary-title
restriction, global character scan, recurring reminder or automatic native sanction.
The human generic chooser and shared random suggestion use the same eligibility.
AI generic-menu scanning is disabled because these bounded events supply initiation.
Old observations receive no retroactive timers; the chooser remains available.

Sixty-day story maintenance removes expired storage; retention gates access at the
actual expiry. Serial counters are never reset by cleanup, withdrawal or observation.
Optional independent institutional provenance without private inherited evidence is
now in RW010_LAND_REGISTER.md. Personal intentions are not copied into it; exact-entry
individual restitution is next. Custom coercive title
effects, universal landholding bans and G1 remain unimplemented/unresolved.

Seventeen adversarial source-contract tests cover readiness, exact affairs/titles,
private basis, duplicate pending causes, constructor/serials/clocks, stale popups,
untrapped withdrawal, fresh-only/unique/bidirectional links, consumption order,
native-window guards, explicit consent, shared bounded opportunities, EN/FR and
absence of forced effects/inherited records. They execute no CK3 callback or UI.
INTENT-01…12 in FINAL_ENGINE_TESTS.md remain unrun, including generic-picker and
saved-scalar observation-number rendering. All game runs remain in the final
campaign; no new source upload or intermediate run is requested.
