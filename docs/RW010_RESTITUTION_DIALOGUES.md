# Land-restitution discussions — public facts, private choices

**Experimental original CK3 scripts; static-checked, not engine-tested.** An exact
filed land entry can support a request to its title's actual current holder. The
parties may open discussions, refuse, withdraw or stay silent; the requester can
choose a bounded personal reaction to refusal. Agreement to examine is neither a
promise to grant land nor completed restitution. This connects information, memory,
negotiation, political consequences and AI beyond the original example scenarios.

## Who can ask whom

From a retained public land-register entry, while its original former holder lives,
only that person can initiate this authored request. After their death, the current
head of the exact frozen former house may ask for themselves. No dynasty-wide or
blood-relationship entitlement is inferred; a living former holder cannot be
bypassed because they are a minor, prisoner or have changed house. Other native
interactions remain available independently of this authored flow.

Requester and holder must be living, adult and free, distinct and at peace with
one another; the holder must be the actual current landed holder of the exact
ordinary county-or-higher title. The archive's crown is provenance, not permission
for a sovereign to take a third party's land. Noble-family and landless titles are
outside this slice. A historical observation does not create a legal claim or
declare a past confiscation unlawful.

The public entry, serial, title, crown, former house and former holder must match
the captured snapshot. Request confirmation also captures the current holder;
ownership changing while the popup is open invalidates it. Current native grant
validity is **not** required merely to ask for discussion, so a political request
does not pretend the game has already authorized a grant.

## Explicit request, current-party response

Confirming creates a separate participant-private story/index entry: original
requester and holder, exact public source pointer/serial and public tuple, monotonic
request serial, issue date, pending state, thirty-day window, one-year requester/holder/title
cooldown and five-year personal retention. Fresh story/type/owner is checked;
registration and index membership precede either party's notification. Failed
registration retires the new story and sends no request. No money moves.

The cooldown covers the same pair/title across different historical entries. It
starts at the original request and is never renewed by replies or reads. A new
claimant or new holder is a different pair, not inherited consent. No cap is placed
on requests concerning different titles. Neither archive reads nor crown succession
lets a successor view the predecessor's private conversation.

Only the captured holder may accept examination. Acceptance rechecks the source
entry's retention/identity, the claimant's current role, both parties and current
ownership/peace, then changes pending to `talks` before notices. The original
thirty-day window stays fixed. Acceptance can happen once and grants nothing.

The captured holder can refuse or close pending/talks, and the requester can
withdraw, even after current eligibility, ownership, war or the source entry changes,
while the typed private history remains accessible. These are identity-only closures,
not decisions for a new holder. They consume the window before notices and create
no automatic punishment, reimbursement or native crime. Silence has no penalty.

Within talks, a human current holder may open native `grant_titles_interaction`
terms for the exact requester only after full current-context and native validity
checks, repeated on click. No title, hook or send option is preselected or force-sent.
The holder must choose and confirm the intended title there. Unselected-title
validity/special-window behavior remains experimental; the ordinary character menu
is the fallback. AI retains native grant selection; examination does not introduce
a forced AI land-gift policy or new player-only gameplay action.

The view independently checks whether the requester now holds the title. It never
labels that acquisition as caused by this discussion: inheritance, war or another
native action could explain it. There is no fulfilled/restored flag or automatic
reward. A title moving to somebody else blocks the old parties' native handoff.

## A discretionary personal consequence

Refusal opens a fixed seven-day response window for the captured requester. They
may acknowledge the answer without a new penalty, leave it, or resent the captured
refuser. Resentment consumes this request's personal-response marker before applying
the new mod-owned **−10 opinion for two years**, only if the same pair's modifier is
absent. It neither stacks nor refreshes across repeated requests/different titles.
Acknowledgment does not remove unrelated earlier resentment. Both choices and
their effect guards are shared by AI and player.

There is no automatic opinion loss on refusal, silence, invalidation or withdrawal.
The reaction requires the exact living parties, refused state, live seven-day window,
no previous response and a title not already held by the requester. It targets the
original refuser, never a successor, house or dynasty. History records the choice
without claiming the modifier remains active forever or that a refusal was a crime.

## Bounded opportunities, private history and cleanup

Initial public filing and the existing sixty-day land-record maintenance can offer
the original former holder, or the current house head after that person's death,
one request confirmation per observed eligible claimant/current-holder pair. Two
optional public-role notice caches live on the public entry; they contain no private
request pointer, reply or consent. Cache changes precede the event. Unchanged pairs
skip the private cooldown index entirely; readiness precedes that scan too. Ineligible
pairs are not consumed, so adulthood/release can allow the first opportunity later.
Pair changes/reversals between observations can be missed; this is not a universal
native lifecycle monitor or a recurring request/resend policy.

Eligibility here is parameterized by the actual candidate. The public story's ROOT
is never treated as the claimant; only the dispatched character event has that ROOT.
Manual public-archive initiation uses the same eligibility/cooldown and confirmation.
There is no world/character-pair scan. Public archive reads themselves send nothing.

The private request archive enumerates only records where the actor is an original
participant. Views recheck record/serial and all captured identities. Only the two
participants see replies and reactions; house/crown successors do not. No private
scheme/evidence/intent material is imported into this flow or its public cache.

Sixty-day private maintenance marks a pending/talks request expired once its original
window is absent, or invalidates an observed current-role/source change while that
window lives. Buttons stop at the actual deadline/current mismatch without waiting
for maintenance. Transient changes and reversals can be missed. There is no reminder
chain or automatic invalidation penalty. Original retention/cooldown stay unchanged.
Requester death removes the exact private index entry before ending the story;
malformed/expired storage is retired similarly. If immutable pointers disappear,
history may become inaccessible/retire; no long-term private persistence is promised.
The independent public land entry remains unchanged apart from its two public-role
notice caches and can offer a later generation a fresh discussion under current roles.

## Verification and next work

Twenty adversarial source-contract tests cover exact public source/current holder,
original-holder/house-head rules, cross-entry cooldown, captured confirmation,
constructor/serial/register order, immutable clocks, participant-only history,
current acceptance, untrapped closure, expiry/owner death, once-only bounded reaction,
native-window safety, story-versus-character ROOT, public cache allowlist, EN/FR and
absence of forced native effects/private-evidence import. They do not execute CK3.

REST-01…14 in FINAL_ENGINE_TESTS.md remain unrun. Native callback and registry
creation/custody, event/scalar snapshots, special grant UI, opinion duration, actual
AI rates, compatibility and performance all require the final campaign. The archived
public provenance is not an enforced ban or a universal restitution right.

Next: negotiated consideration/commitments and safe observation of an actual native
grant, keeping examination, promise, performance and refusal distinct. The eight
systems remain the project scope; three original scenarios are non-exhaustive tests.
No runtime Python, LLM, paid service or further source upload is needed for this slice.
