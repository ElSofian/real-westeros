# Individual land review after political rehabilitation

**Experimental CK3 scripts; static checks only, not engine-tested.** This is
read-only review and a native-window shortcut, not a new confiscation or restitution
mechanic. It connects an already rehabilitated house record to current native title
grant terms without changing ownership or recording a completed remedy.

## Access and exact parties

Open the existing house/crown archive, then an exact retained record whose state
is `restored`. The current qualified sovereign of that record's authority title or
the current adult, living, free head of its exact house may inspect landed standing.
An old issuer, other house member or storage custodian does not gain this shortcut
merely by being able to read the archive. Active, withdrawn, expired and purged
records do not qualify. Free and paid rehabilitation use the same record state;
this review never charges again or repeats political goodwill.

The parent option and dispatch effect revalidate record access, serial/revision,
restored state and current roles. Before opening, temporary aliases capture the
specific current sovereign and house head. Description, portrait and native-window
click require both people still hold those exact roles and remain qualified. A
new head or ruler does not silently replace an old panel's parties. Reopen the
archive/current record to inspect successors. This checks current identity; it is
not a historical monitor of role changes and reversals between observations.

The view distinguishes a currently landed head from a landless head. Neither fact
establishes noble status, ownership of ancestral lands, past confiscation, inherited
personal guilt or an entitlement to a particular title. The record documents
political rehabilitation only. Other authorities' records remain independent.

## Native grant handoff

Only the current sovereign can open grant terms for the captured current head,
and only if the native `grant_titles_interaction` validity query allows that
recipient at the time of the click. No ordinary/theocratic/co-ruler eligibility
branch is copied or bypassed. No title, hook, secondary party or send option is
preselected, and nothing is force-sent. Native title selection, restrictions,
confirmation, effects and any costs remain authoritative.

The head's view sends no demand and commits neither person. Closing either panel
changes nothing. There is no promise, automatic notification, timer, decree write,
receipt, payment, status change, post-transfer reversal or title/war lifecycle hook.
The navigation is human-facing UI only; no new player-exclusive gameplay effect
is introduced. AI retains its existing native grant/revocation selection and rules;
there is no claim that political rehabilitation now makes AI grant land.

TITLE_ROUTE_AUDIT.md / TITLE_ROUTE_SOURCE_RECEIPT.json locate the actual grant
interaction, alternatives and title picker. The generic native validity/window
primitives were source-located in JUSTICE_SOURCE_RECEIPT.json. Their application
to an **unselected title-target grant** remains experimental: a targetless validity
query may reject it, or the special picker may not populate. Do not invent a target
or bypass validation to reveal the button. The ordinary character menu is the
fallback. Opening, picking, cancelling and confirming need separate final evidence.

## Scope and validation

The existing prisoner/title panel still delegates revocation to the native window
with current custody, direct-vassal and validity checks. This grant review does not
infer which title was revoked or who previously held it. A future genuine
restitution contract must identify an exact title, provenance, present holder,
authority, recipient, consent and native consequences; this UI is not that contract.
No custom coercive confiscation, loss of noble status or fifty-year landholding ban
is implemented. G3 stays unresolved; hereditary, elective, conquest and special
regional transfers require their own coverage.

Eleven adversarial source-contract tests cover stale/restored records, role versus
archive permission, unqualified/dead/imprisoned/wrong-house heads, self-recipient,
successor aliasing, native validity direction, guarded dispatch/clicks, no selected
terms/force-send, no state writes/timers, privacy and full EN/FR references. These
tests execute no CK3 behavior. LAND-01…08 in FINAL_ENGINE_TESTS.md remain unrun.

Next: audit native individual-title legality/provenance before any coercive remedy;
independent revised-promise/receipt/mediation integration can continue. All CK3 runs
remain in the owner's final campaign. No further source upload is required for
this navigation slice.
