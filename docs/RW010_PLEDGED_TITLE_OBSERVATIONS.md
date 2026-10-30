# Conditional title-gain observations for personal restitution promises

**Original CK3 scripts; source/static-checked, not engine-tested.** This records
one native transfer context against a unique live personal promise. It does not
prove a voluntary grant, causal fulfillment, compatibility or a cleared G2/G5 gate.

## Native context and exact matching

The received CK3/AGOT source identifies `on_title_gain` with new-holder character
ROOT, `scope:title` and `scope:previous_holder`. Granting itself happens in engine
code; neither those scopes nor a matching promise establish the acquisition route.
Three received files were rechecked against the private manifest. Public
RESTITUTION_TRANSFER_SOURCE_RECEIPT.json contains only selected relative paths,
hashes, sizes and marker positions, never original scripts or installation paths.

The existing additive native wrapper now lists the original revocation-context
child **and** one separate pledged-title-gain child. The original child guards and
effects remain intact. No native `effect`, event list or transfer is replaced.
The optional G3 trace remains a separate mod; this child loads in the base mod.
Native composition, dispatch order and scope persistence still require engine proof.

Before searching stories, the callback requires a living new holder with an existing
request counter, an existing distinct living previous holder and an ordinary
county-or-higher title actually held by the new-holder ROOT. Noble-family/landless
titles, dead previous holders and incomplete/mismatched scopes fail closed. This
excludes death succession from this authored observation; it is not a general
inheritance monitor or proof that every remaining transfer was a voluntary gift.

Search is limited to the receiving character's own stories, never the global
request index or all character pairs. A candidate must be an exact typed retained
private request owned by that receiver, with matching captured requester/holder/title,
complete personal pledge provenance, supported 14/30-day terms, accepted `promised`
state and a still-live due marker. Unaccepted, withdrawn, renounced, released,
expired/unresolved, acknowledged, invalidated and incomplete promises do not match.
Later crown/house roles and public source expiry do not substitute for the original
personal identities or erase an otherwise valid accepted commitment.

At least one unobserved candidate and **exactly one candidate overall** are required.
Ambiguity is rejected even if one competing commitment already has a note. The effect
rechecks the native trigger, captures explicit receiver/giver/title aliases, then
iterates only owned matching stories. It does not mistake the story for character
ROOT or pick a random candidate. Callback composition/count predicate semantics and
real cost still await final evidence.

## First fact, private display, unchanged commitment

The unique parent request gets an immutable schema-1 note: kind
`native_title_gain_context`, request serial, accepted pledge revision/delivery period,
exact title/former/new holders and callback observation date. Schema is stamped
last. Duplicate callbacks never refresh that note or any original clock. The date
is when this code observed the callback, not an independent engine transaction ID
or proof of the acquisition's exact time. Ordered writes are not crash consistency.

Only the original private participants can see the note through their pledge panel.
The full existing private request/pledge identity and every captured note field are
rechecked. A later title move does not erase a historical context; the separate
current-ownership line stays authoritative for the present. No crown/house reader,
heir or unrelated person gains access. No new public entry or evidence pointer is
exported. Original five-year private retention and requester-death/index cleanup
apply to the parent; the observation never renews them or creates a new story.

A missing, old or malformed note is explicitly **not evidence of nonperformance**.
There is no reconstruction from present ownership, old receipts, a manual history
read or later title transfer after the promise deadline. Existing active promises
may receive a genuinely future matching callback; old completed transfers are not
backfilled. A callback before ownership/context is ready may produce no note at all.

No promise state, consent, due date, reaction, native action, title, gold, prestige,
opinion, claim or legal verdict changes. No popup is sent from native title handling.
Beneficiary confirmation remains a separate explicit personal statement requiring
current ownership. It neither requires this optional note nor becomes objective
proof of a grant/cause when one exists. An unresolved deadline remains neutral;
there is no automatic reward, payment, punishment or forced AI land gift.

AI and player use identical intake/read guards. No new periodic timer, reminder,
external service, runtime Python or LLM is used. Recipient-owned story scans occur
only on relevant title-gain dispatch, with a cheap request-counter prerequisite;
no performance guarantee follows without measurement.

## Verification and remaining work

Fourteen adversarial source tests cover additive dispatch, actual native tuple,
retained exact accepted personal terms, ambiguous/repeated callbacks, guard recheck,
story-root aliases, complete write order, private historical reads, no effect replay,
no consent/deadline change, missing evidence, AI symmetry and hash-only EN/FR sources.
They inspect code wiring, not a CK3 transfer or a Python gameplay simulation.

TRANSFER-01…10 in FINAL_ENGINE_TESTS.md all remain unrun. Final campaign must verify
both additive children alongside native AGOT effects, special/multiple-title routes,
missing scopes/ordering, privacy/persistence, AI and performance. Next broader
voluntary consideration and other service commitments; a reliable voluntary-grant
route/causal receipt remains unresolved and must precede automatic consideration.
No new file upload or intermediate game run is requested.
