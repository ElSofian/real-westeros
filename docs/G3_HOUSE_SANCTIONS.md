# G3 — house sanctions and restoration: scoped contract and transfer trace

**Status: source-audited subset; no engine run; landholding enforcement unresolved.**
A subsequent experimental political censure/register/rehabilitation slice is in
RW010_HOUSE_AFFAIRS.md. Conditional 50-gold political rehabilitation is in RW010_HOUSE_TERMS.md.
This investigation and optional diagnostic do not clear G3
or replace the intended fifty-year landholding ban with a political marker. Its
feasibility is unresolved, not disproved. Manual runs remain deferred to the final
campaign.

## Sources and route coverage

The received scheme subset and the earlier private G1 complement were reviewed.
G3_SOURCE_RECEIPT.json publishes only relative names, hashes and marker lines.
The complement's 94 text files were safely unpacked separately; selected reviewed
files match G1_COMPLEMENT_RECEIPT.json. The scheme subset's reviewed bytes match its
private manifest. Neither private originals nor the full manifest are committed.
AGOT descriptor metadata is 0.5.2.1 / supported CK3 1.19.0.6; executable unverified.

| Acquisition route | What the received sources establish | What they do not establish |
|---|---|---|
| Grant | `can_be_granted_titles_by` is a recipient-context helper with a ruler argument and AGOT-specific rules | The initiating grant interaction, every grant caller and a universal pre-transfer exclusion are not established in this subset |
| Inheritance | Succession laws configure inheritance/partition; the native inheritance callback runs title-change consequences, including AGOT dynastic stability | A timed house predicate applied to every succession order and candidate is not established |
| Election | Feudal elective law selects an election type; an elective helper rejects several traits, including disinherited | All election-type definitions/callers and their exact coverage are not established; a personal unelectable trait is not a house ban |
| Conquest/claims | The received claim CB resolves a native title/vassal change through claim setup and resolution | Grant eligibility is not established as its gate; coverage of all other CBs and transfers is not proved by this example |

Native `on_title_gain`, `on_title_gain_inheritance`, `on_title_gain_usurpation` and
`on_title_lost` provide post-change observations, not a demonstrated veto. A log
from inheritance/usurpation does not prove which higher-level route caused it.
Usurpation is not synonymous with conquest; elective succession may share general
callbacks. Log order, composition, effective scopes and coverage need the engine.

Do not fix a missing pre-transfer gate by moving the title back in `on_title_gain`:
that could repeat consequences, trigger recursive transfers, break succession,
war resolution, vassals or AGOT state. No such reversal is added. No native law,
CB, grant helper, eligibility rule, dynastic-stability handler or title effect is
overwritten. The unresolved frontier and missing definitions must remain visible.

## Why existing personal mechanics are not the house sanction

Native disinheritance is an interaction with dynasty-head/recipient and other
AGOT eligibility, costs, personal traits, claims and opinions. The inspected helper
can create claims; it is not a harmless blanket ban marker. Native restoration
removes personal disinheritance and adjusts native opinions/house relations. Neither
is a demonstrated sovereign right to disinherit an unrelated whole house, strip
its nobility, deny all title acquisition for 50 years, or restore ancestral lands.
Do not apply/remove those native traits across relatives as a substitute.

AGOT dynastic stability can change a character's house after title transfer. A
character's present house, their house when the offense occurred, a dynasty, a cadet
branch and a set of blood relatives are different identities. A current-house
marker cannot silently answer how later births, cadets, adoption, legitimacy,
bastard branches or AGOT house changes should be treated.

A later source review located celestial family extinction with celestial supreme-ruler,
noble-family-title, human-actor and AI-recipient restrictions. It is not a generic
Westerosi house sanction or proved parity path; do not bypass those native gates.
Native inheritance restoration also retains dynasty-head/renown and AGOT
human-recipient conditions. Hash/relative markers are added to G3_SOURCE_RECEIPT.json;
these definitions are neither copied nor force-run by Real Westeros.

House-scoped variables, including a timed house variable in a native coronation
flow, are source-located persistence candidates. This does not establish a complete
sanction registry, legal enforcement or engine persistence proof. The existing
personal RW observation stories end with their owner; they are not silently
converted into inheritable guilt or long-lived public house judgments.

## Implementation contract for subsequent gameplay slices

This is the selected engineering direction, not fields that already exist at runtime.

- Separate **political house censure**, **personal punishment**, **loss of status**
  and **landholding proscription**. Implementing one must not mark the others done.
  Preserve native crimes, titles, secrets, banking and existing relationship effects.
- A decree needs its own schema/serial, exact sanctioned house, issuing person,
  authority/title/jurisdiction, explicit kind, provenance, issue date, fixed original
  expiry and closure/restoration outcome. Support distinct decrees/authorities;
  avoid a single latest-receipt slot overwriting every prior house affair.
- Use the exact house as the initial collective target; do not silently extend to
  the entire dynasty or all relatives. Record the house at issuance. Rules for
  cadets/house changes and prospective membership require explicit coverage before
  enforcement; they cannot be assumed to block or permit evasion.
- A disclosed scheme observation remains an observation, not an automatic legal
  conviction. Jurisdiction and legal basis must be explicit; later current native
  reasons cannot reconstruct law applicable when the act occurred. Arbitrary political
  action and lawful sanction must have distinct stated consequences.
- Political continuity belongs to an explicit institution/authority, not inherited
  personal guilt. A carrier surviving issuer death and authority succession must be
  demonstrated before claiming a multi-generation registry. Story reassignment,
  title/house variables and multiple-authority conflicts remain design/engine work.
- A genuine 50-year prohibition needs verified coverage of grants, inheritance,
  elections and conquest for the applicable realm. A variable, modifier, negative
  opinion or one blocked interaction is insufficient. No unverified global veto or
  automatic title reversal may be shipped as working enforcement.
- Restoration is a separate explicit decision by an authorized successor/current
  authority, or expiry under the decree's own terms. It closes only the matching
  decree, consumes no unrelated native rights and grants no automatic territory.
  Restoring status/eligibility and restituting a particular title are distinct.
- Later descendants may face the house's political aftermath without becoming
  guilty of the ancestor's crime. A claimant's living identity, authority, decree,
  scope and eligibility must be rechecked. Stale requests and repeated acceptances
  must not repeat rewards, transfers, penalties or silently renew the original term.
- AI and player must share the eventual new actions/costs/guards, with bounded
  institutional targeting. Diagnostic UI is not a new gameplay privilege or an AI
  sanctions policy. No paid service, runtime Python or language model.

The first explicitly scoped political house-affair persistence/restoration slice is
now in RW010_HOUSE_AFFAIRS.md. Its succession/request lifecycle is source-hardened, and conditional financial
rehabilitation joins political restoration to personal consent while keeping **landholding enforcement unresolved** until its
four route gates and engine evidence exist. Inspect missing grant/election definitions
before deciding whether another targeted private collection is necessary; no new
upload or intermediate game run is requested by this investigation.

## Original optional CK3 diagnostic included now

The trace is a **separate optional mod**, stored under
`diagnostics/g3_house_trace/mod/` in the source/ZIP. Copy that folder's
`rw_g3_house_trace.mod` and `rw_g3_house_trace/` into the usual CK3 user-data `mod/`
directory only for final testing. Add **Real Westeros G3 Diagnostic** to a test
playset after AGOT. It is standalone; the base Real Westeros mod does not register
these title callbacks or diagnostic UI. Installing the main `mod/real_westeros/`
payload alone cannot load this diagnostic. Disable the separate playset entry after
testing. Its provisional descriptor target is not engine compatibility evidence.

In a disposable save launched with CK3 debug mode, right-click a living character
with a house and choose **G3 diagnostic: trace this character's current house for
seven days** in the debug interaction menu. A human tester selects the house;
callbacks observe both AI and player holders with the same diagnostic guard.
The exact house receives only a seven-day `rw_g3_trace_active` marker. The start
option is unavailable while marked, so it does not refresh the original expiry.
The stop option clears the current selected house's marker early; after expiry it
can be enabled again as a new diagnostic window. House changes may require choosing
a member of the original marked house to stop it; no marker follows relatives.

While debug mode and that marker are both active, named child actions append to
the four source-located native callbacks. They revalidate before logging. Logs
contain only `RW_G3`, a literal callback kind, the root holder's ID and the changed
title's display name. No full scope dump, secret, agent or plot record is logged.
Repeated labels for one transfer can be expected when several native callbacks run;
they are observations, not duplicate punishments or a deduplicated transfer ledger.
Title display names are localized and not guaranteed unique; record controlled
save/title identity separately during testing. Actual log file and interpolation
must be verified in CK3; this tool has not been run in the game.

The optional trace is inactive outside debug mode and cannot be enabled through these effects
outside debug mode. An old marker has no logging effect outside debug mode and
expires on its original timer. It is not a 50-year sanction, house-status mutation,
AI policy or landholding gate. It changes no titles, dynasty/house membership,
claims, relations, laws, obligations or native on-action effects/events. There are
no recurring events, global house scans, automatic uploads or external services.

The isolated diagnostic dispatch is additive in source form; actual native/AGOT load
composition remains unverified. Baseline comparison is required before using traces
to assess coverage. A missing trace may mean inactive mode/marker, changed house,
log/scope/dispatch failure or missing callback coverage; it does not prove a ban.

## Final evidence still required

Ten adversarial source-contract tests cover opt-in identity/debug guards, timeout,
non-renewal, enable/stop revalidation, native-wrapper preservation, callback scope,
absence of game-state/title reversal and restricted log fields. Two archive tests verify optional placement and reject an invalid launcher/unbalanced
diagnostic script. These checks do not execute
CK3, prove load order, persistent house state or clear G3. G3-01…12 in
FINAL_ENGINE_TESTS.md remain unrun, including four-route and multi-generation cases.
