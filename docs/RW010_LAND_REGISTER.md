# Crown land register — institutional public-fact provenance

**Original experimental CK3 scripts; static-checked, not engine-tested.** A qualified
sovereign can voluntarily file a narrowly defined title-transfer observation in an
independent crown register. Only public land facts survive: no private plot, proof,
intention or inherited legal guilt is copied. This prepares later restitution; it
neither grants land nor implements a collective sanction or landholding ban.

## Capture once, then choose whether to file

The existing conditional TP intake still requires its exact native revocation
context (RW010_TITLE_PROVENANCE.md). During fresh TP construction only, the new
helper captures the observer's then-current primary crown and the former holder's
then-current exact house. The observer must satisfy the existing independent,
adult, free, landed kingdom-or-higher sovereign predicate. Native title/actor/
recipient/acceptance marker, current/previous holder and fresh receipt identity
are checked again. This house is the one observed at that callback, not an assertion
about membership when an offense occurred or before AGOT's other consequences.

Old TP observations without these captured fields cannot be retrofitted from a
later crown/house. No native title history is reconstructed. The TP callback's
scope propagation/order remains unproved; if it produces no observation, this
module cannot manufacture one or fill the register by inference.

One day after capture, one fixed opportunity lets either AI or human choose **Deposit
only these title-transfer facts**, or leave the source private. The TP journal also
offers the same manual review. Opening/ignoring the confirmation does not publish
or charge anything. Both actors use the same guard/effect and zero cost; there is
no periodic AI scan or forced filing. No intermediate CK3 run is requested.

On confirmation, the original observer must still own/read the exact retained TP
record and be qualified, and still hold its captured crown. The captured authority
and former-house aliases must match. Losing that crown invalidates the old popup;
a successor does not inherit the private TP journal and cannot file it. Moving the
land again does not erase the historical transfer, so current ownership is not a
prerequisite for filing that old fact. Current ownership is displayed separately.

## Strict public payload and deduplicated registration

A fresh, separately owned story contains only:

- Registry schema/kind (`title_transfer_observation`) and a crown-scoped serial.
- Filing issuer and an internal numeric TP source serial for duplicate detection.
- Exact title, former holder, observed new holder and frozen former house.
- Captured crown/authority title, original observation date and filing date.
- Original one-hundred-year archival retention, starting at filing.

No pointer to a TP record, private evidence, scheme, allegation, intention or declared
reason is stored in the institutional story. The subsequent restitution module may
add two public-role notification caches (current candidate and current title holder);
these are opportunity metadata, not private request pointers, replies or consent. The internal numeric source serial is
not an offense identifier and is not shown as a private case number. The original
observer is also the recorded new holder; neither is changed to a later sovereign.

Publication rechecks both the source's filed marker and the typed registry index
for the same issuer/source serial. It verifies a fresh story/type/owner before
incrementing the crown's own monotonic counter and writing the exact public payload.
The record is appended to `rw_land_register`, index membership is verified, and
only then is the private source marked filed. Failed registration retires the new
story without consuming the source. No counter is reset or reused. This ordered
metadata sequence is not a demonstrated atomic CK3 transaction.

The registry entry becomes independent of the private journal's five-year retention
and personal owner death. Filing is explicit disclosure of the title facts only;
it is not a public conviction or proof that a plot caused a native confiscation.
TP's one-day coalescing and incomplete callback coverage remain upstream limits.

## Successors, custody and consultation

Current living readers are the holder of the captured crown, the current holder of
the transferred title, either original transfer party, or a member of the exact
frozen former house. A new crown holder or later member of that house can therefore
read the land facts without receiving an ancestor's private case or personal guilt.
An entire dynasty, cadet branch or another house does not qualify by blood alone;
an original party remains a party even after changing house.

Storage ownership gives **no additional read permission or legal power**. When the
storage owner dies, its known identity is excluded even if native alive/holder flags
have not settled. Custody can pass to a living crown holder, current land holder,
former-house head, either original party, or a living exact-house member, in that
priority order. Sixty-day maintenance reconciles later native succession/role
settlement. These operations move only the new RW story, not land or native rights.
They reuse the source-located storage/index primitives already discussed in
RW010_HOUSE_AFFAIRS.md / the repository’s HOUSE_REGISTER_SOURCE_RECEIPT.json; no new native callback is added.

Current-role permission is checked on every view, independently of physical story
custody. Each popup captures record, crown, house, serial, title and original parties
and revalidates the entire immutable tuple. The selected interaction recipient is
not informed. Reading and migration rewrite no fact, counter or retention term.
The register stores observation/filing dates; this first view identifies entries
by crown serial and parties rather than promising a tested calendar-date renderer.

Retention gates access at its original expiry. Expired/malformed entries, or entries
with no surviving eligible custodian, leave the exact global index before their
story ends. One hundred years is a maximum archival period, not a guaranteed eternal
archive, a title prohibition, a claim, or a limitation on a later native right.
If immutable character/title/house pointers cease to exist, the entry may be retired;
that engine persistence behavior remains to be measured. No orphan is silently
assigned to an unrelated character solely to keep it alive.

## Boundaries and next work

This feature changes only its own story fields, index, source-filed marker and
crown serial counter. It creates no title/claim/status/opinion/payment, consumes no
native reason, and modifies no war, succession, Mega War, bank or native law.
The optional G3 diagnostic remains separately installed and unchanged. Registry
operations inspect their own index or the current record's house as a custody
fallback; there is no world/pair scan. Global history reads/deduplication and
sixty-day per-record maintenance still need long-run performance evidence.

The subsequent individual request/review flow is in RW010_RESTITUTION_DIALOGUES.md,
with exact source/current holder/claimant/consent checks and a separately guarded
native grant-window handoff. Acceptance is examination, not promised land. A historical
entry must not authorize taking land from a third party or restoring an ancestor's
private guilt. No automatic ancestral restitution or noble-status restoration is
implemented, and G3's universal fifty-year land ban remains unresolved.

Seventeen adversarial static tests cover fresh-only frozen capture, original-authority
consent, duplicate detection, exact public-field allowlist, fresh constructor and
register-before-consume order, immutable clocks/counters, current-role access,
stale views, owner-death flag timing, custody fallbacks, index retirement, shared
bounded opportunities, EN/FR and absence of private-case export/native effects.
They do not execute CK3 succession, ownership transfer, persistence, load order or
privacy. ARCHIVE-01…12 in FINAL_ENGINE_TESTS.md remain unrun; all game tests stay
in the owner's final campaign. No further source upload is requested.
