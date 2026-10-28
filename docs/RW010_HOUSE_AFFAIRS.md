# House political affairs — experimental registry and rehabilitation

**Original CK3 scripts; static-checked, not engine-tested.** This first house-affair
slice implements political disfavor and its rehabilitation. It implements neither
a landholding ban, loss of noble status, collective executions nor confiscation.
G3's four acquisition-route enforcement gates remain unresolved. No runtime Python,
LLM, paid service, diagnostic add-on or native title callback is required.

## Issuing political censure

A living adult free independent sovereign of kingdom tier or higher may consider
censuring the current house of an adult exposed participant currently in their
native custody and their direct vassal/courtier jurisdiction. The exact private
observation must still belong to that sovereign and pass existing typed schema,
serial, retention and participant-kind checks. Generic plot discovery, an allegation,
a hidden organiser or an inherited private observation cannot authorize this choice.
The issuer's own house is excluded in this initial slice.

The prisoner panel opens a confirmation with an exact current house/title snapshot.
Acceptance rechecks custody, authority, house, private record and 50 prestige. It
creates a distinct first-party story and registers it before consuming this
observation's filing flag and charging 50 prestige. Missing/failing registration
ends the new record without filing/cost. Serial gaps after failed construction are
acceptable; counters are never reused. An already active political censure for the
same house and authority is not duplicated. Other authorities and later distinct
observations remain independent; there is no arbitrary record-count cap.

The decree lasts fifty years from issuance. It is **political disfavor**, not the
owner's intended fifty-year prohibition on landholding. The current house head
receives -20 opinion of the issuer for five years, only if that exact custom
resentment is absent; it neither stacks nor refreshes. Existing native penalties
are not changed. New members/heads do not acquire a criminal trait or automatic
personal negative opinion. The political record and petition rights persist.

## Independent institutional records

Each record has its own story type/schema, house-scoped monotonic serial, revision,
exact house at issuance, authority title, original issuing character, issue date,
political kind, original observer/observation-serial provenance, fixed timed term,
state and closure date/actor where applicable. Provenance preserves only the
issuer plus numeric observation identity and a typed observation-basis flag. The
private observation's scheme pointer, hidden identities and secrets are not copied
or disclosed. Its later expiry/death does not rewrite the political decree.

The namespaced global list indexes these records, not every character or every
political relationship. New records do not overwrite a single latest slot. Reader
access is limited to the original living issuer, the authority title's current
holder and living members of the exact recorded house. Membership is current; a
cadet branch, all blood relatives or the whole dynasty is not silently included.
The selected character in the read-only register interaction is not a participant
and learns nothing from browsing. Actual privacy/scopes still require engine tests.

Story ownership is **storage custody**, not permission to judge or inherited guilt.
The holder of the recorded authority title can change; only its current sovereign
holder may lift this political censure or decide a petition. Former issuers/custodians
cannot retain those powers through story ownership. The current adult free house
head may petition, including a later descendant or a landless head.

On story-owner death, an own-story callback attempts custody transfer to a living
current authority holder, then the recorded house's living head, then a living
member of that exact house. It explicitly excludes the dying custodian even if
native death flags/head succession have not settled. No character is created and
no native character/house/title is modified. A per-record 60-day maintenance pass
can return storage to the authority holder after title succession settles. No new
native title/death hook is added; the optional G3 trace remains separate.

If the current custodian survives a vacancy, storage may remain there temporarily.
If no living authority/house custodian is available on owner death, the record is
removed from the index before ending. Complete extinction/vacancy and later cadet
restoration are therefore outside this first continuity guarantee. Actual callback
scope, ownership transfer, ordering, save persistence and multi-generation continuity
are **unverified in CK3**. Source call sites are not engine proof.

## Petition and restoration

The current head may request rehabilitation from the authority title's current
living adult free independent sovereign, while not at war with that person.
Petitioning is free. A pending request also requires a free current head and a
current adult free independent sovereign; imprisonment, war, role loss or a new
revision blocks replies immediately. A request captures the exact ruler/head and a new revision,
lasts thirty days, and starts a one-year institutional petition cooldown. A change
of head or title holder invalidates the old petition and permits a fresh one under
the new roles; it does not renew the decree's original fifty-year term. Requesting
oneself as sovereign is disallowed; that sovereign can withdraw the censure directly.

The addressed sovereign may accept, refuse, leave it unanswered or counteroffer a
50-gold conditional rehabilitation (RW010_HOUSE_TERMS.md). Gratuitous acceptance
closes only this exact record before granting +10 sovereign opinion of the current
petitioner for two years, only if the identical goodwill is absent. It cannot
stack/refresh through multiple records. Refusal/silence adds no penalty or debt.
The latest petition response is retained, not a full log of every petition.

The existing sixty-day maintenance pass retires an observed invalid pending request,
removes its window and increments the record revision once. A request whose window
has already expired is instead recorded as unanswered. Neither path resets the
institutional cooldown, dates or original decree term, charges money/prestige, or
sends another event. Losing and regaining the same role after recorded invalidation
cannot revive that request. On story-owner death, a still-open request naming that
owner as petitioner/addressee is invalidated before custody transfer, even if the
native alive/head flags have not settled. A bystander custodian's death alone does
not invalidate the parties' request; a timed-out request is not relabeled as a death.

This observes changes at the own-story callback/pass, not every native transition.
A role/war/imprisonment change and reversal between observations is not guaranteed
to leave a historical trace. No universal succession hook or engine ordering proof
is claimed. Passive retirement can lag up to sixty days; current action guards apply
immediately. Current-head/ruler replacement still gets a fresh revision and may bypass
the old pair's cooldown; temporary unavailability of the same pair does not waive it.

A stale record/reply panel may explicitly reopen the **same** readable record using
its exact story pointer, house, authority and serial. Only this read-only refresh
ignores the old revision. The refreshed panel takes a current snapshot and requires
another explicit choice; it never answers a replacement petition or submits one,
charges a cost, grants favor, changes storage, or writes persistent state. An
unrelated reader, wrong identity or expired retention cannot use refresh. A former
sovereign may read as original issuer but gains no successor's decision rights.

A current sovereign may instead withdraw the decree without a pending petition;
that closes it without a goodwill reward. Neither route grants land, restores a
native disinheritance trait, removes old resentment, creates immunity or closes a
different authority's decree. Ordinary native rights and consequences stay separate.

After the original term expires all political actions fail immediately; the
60-day pass records expiry and starts fifty years of closed-record retention.
Browsing and petitions never extend either deadline. Cleanup removes the index
entry before ending the record. Closed histories remain readable to the same roles
until retention expires; cleanup can lag up to sixty days but access is gated.

## AI opportunities and validation

Fresh exposed-participant intake schedules at most two independent consideration
opportunities, at day two and day thirty, with the same eligibility/costs as players.
A scheduling marker prevents duplicate timer chains. Each head gets an initial or
changed-head opportunity. The same head also gets a new opportunity when the recorded
authority's holder changes; the delivery cache records both identities before sending.
An additional ruler-change notice waits until that ruler is a qualified sovereign
and the head is not at war with them. Cache updates obey the same availability check,
so a child, captive, dependent ruler or war does not consume that opportunity; a later
pass can deliver it when available. If a new head's initial notice occurs while the
ruler is unavailable, clear the former head's delivery pair rather than treating it
as the new head's delivered opportunity. This is not an annual retry for a refused petition.
A new sovereign also gets an opportunity to review inherited political disfavor. The 60-day record pass caches recipients before notices and sends only one notice
when head/ruler roles overlap in the same pass; the ruler cache still advances.
Refusal/restoration notices do not restart requests; cooldown/revision guards still
apply. AI and player use the same effects; traits affect weights, not prerequisites.
Players can also reopen known affairs explicitly. Proactive annual AI re-petitioning
is not implemented; G4 behavior/performance remains unverified.

Twenty original register tests plus ten succession/refresh source-contract tests cover identity, proof/custody/funds,
registration/cost ordering, independent pairs, ownership versus authority, current
roles/revisions, expiry, replay/non-stacking, privacy and absence of native property/
guilt effects. They do not simulate or execute CK3 or prove transaction atomicity.
HOUSE-01…20 final scenarios are in FINAL_ENGINE_TESTS.md, all unrun.
HOUSE_REGISTER_SOURCE_RECEIPT.json holds only hashes/relative API call-site markers.
No private original code or full manifest is distributed. Target metadata remains
AGOT 0.5.2.1 / CK3 1.19.*; actual executable and compatibility unverified.

Succession/request hardening is source-checked, not an engine guarantee. Existing
schema-1 records need no identity/term rewrite; a missing head/ruler delivery cache
can cause one initial reminder, then is cached. Old pending states settle on ordinary
maintenance. Old-save migration itself remains untested.

Next review cross-system political consequences and the remaining G3 sanction routes
before attaching stronger house sanctions. Native loss of status and an
enforced title ban remain separate G3 work; do not advertise political disfavor as
the completed landholding-ban goal. G1 remains planned for the war-feature stage.

## Post-rehabilitation land review

RW010_TITLE_REMEDIES.md adds a guarded read-only view from retained restored
records for the current sovereign/head, and a sovereign-only native grant-window
shortcut. Opening terms does not restore an ancestral title, establish noble status,
charge again or record a transfer. Exact current parties/native eligibility are
rechecked; AI retains native title behavior. Special-picker behavior is engine-unverified.
