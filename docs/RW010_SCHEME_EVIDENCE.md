# RW-010 — native murder-scheme observations

**Experimental original CK3 scripts; not engine-tested.** Runtime runs remain
reserved for the final campaign. This is intake and private political memory,
not implemented assassination justice, dynastic sanctions or proof of compatibility.

## Received source evidence

The owner's private collection contains 1,724 files / 107,379,853 uncompressed bytes.
All manifest names, sizes and SHA-256 hashes were checked before private extraction.
The AGOT descriptor metadata reports 0.5.2.1 / supported 1.19.0.6; CK3 executable
version remains uncollected. The collector left 241 frontier files and 2,876
unresolved candidate identifiers. This archive is not a full dependency proof.

SCHEME_SOURCE_RECEIPT.json records the archive hash and twelve inspected file hashes,
relative references and marker line numbers only. No proprietary source excerpt,
installation path, save or full private manifest is published.

Observed source contracts:

- `common/on_action/scheme_on_actions.txt` in both sources defines
  `on_scheme_discovered` with the scheme as root, and separately defines
  `on_scheme_agent_discovered` with scheme root and exposed `scope:agent`.
- Murder has native scheme type `murder`. Its monthly processing uses
  `hostile_scheme_monthly_discovery_chance_effect`; discovery events use
  `expose_scheme` and `expose_scheme_agent` in different paths. Detecting the
  plot does not by itself identify the organiser.
- `is_scheme_exposed` and `is_agent_exposed_in_scheme` occur in target sources.
  The hold-court source explicitly treats the latter on an organiser as knowledge
  of that person by the target. The integration never reads `scheme_owner` to
  manufacture an identity from discovery alone.
- AGOT uses native action wrapper definitions containing `on_actions` entries
  dispatching to uniquely named custom actions in its general on-actions file.
  That is the composition pattern used here. **Actual merge/load-order behavior
  and callback ordering remain unverified in the engine.**
- Native scheme scope values are stored in variables elsewhere in the supplied
  source. Story persistence itself follows the existing experimental project
  pattern. Their existence in scripts is not a successful save/load test.

No discovery event, scheme definition, scripted effect or native action `effect`
block is copied or replaced. Only the two native dispatch names are extended by
original `on_actions` entries pointing to namespaced custom actions. Compare native
and AGOT behavior against a baseline in final testing; suspend these hooks if field
composition replaces rather than extends native behavior in the actual engine.

## Implemented narrow slice

The scheme must be `murder`. Its target must be a living, adult, landed ruler whose
`host` is themselves, restricting intake to the target's own court. It does not
forward information to a liege, host of a visiting courtier, family or other observer.

Two distinct retained facts are recorded:

1. **Scheme discovered:** only when the native exposed flag is set. The record
   contains no organiser or participant identity.
2. **Participant exposed:** only when the native callback supplies a living agent
   whose native exposed predicate matches that exact scheme. The target cannot
   be substituted as agent. The record stores only that exposed person, without
   inferring that they organised it or revealing other agents.

Each entry is an original story owned by the observing target, not by a suspect.
It stores schema, per-observer serial, kind, live-scheme reference for deduplication,
optional exposed participant and five-year retention. Duplicate callbacks match
same observer/story type/schema/kind/scheme, plus participant for exposure records.
Different plots, kinds or participants remain separate. There is no useful-action
count cap, global pair scan, automatic accusation or periodic scheme search.

Current amendment: RW010_SCHEME_RESPONSE.md adds a separate voluntary political
response on new exposed-participant records, with its own short window.

A discreet interface notice follows record initialization. It adds no modal choice
to the existing native discovery events and grants no reward, cost or opinion effect.
Players can use **Review My Discovered Murder Plots** from a character menu to read
their own records; the selected character's records are never enumerated and that
character receives no notification. AI receives the same record/notice logic; the intake itself
applies no political decision. The response amendment supplies shared actor events. Read-only archive browsing
is not proactively scheduled for AI.

Viewing requires typed story, supported schema/kind, retained record, observer root
and saved serial identity. Participant names resolve from the stored record only,
with a neutral fallback if that character reference is gone. The view never follows
the live native scheme pointer, so plot termination is not permission to substitute
an organiser or heir. Actual dangling-reference behavior requires engine testing.

Retention expires after 1,825 days; passive per-story cleanup runs every 60 days.
Unexpired entries remain independent of service receipts and allegation case history.
Expired records may suppress duplicate callbacks until cleanup removes them. Observer
death ends their personal stories; no guilt, duty or knowledge is transferred to heirs.
This is limited personal memory, not a universal intelligence or criminal ledger.

## Boundaries and checks

No secret exposure, crime recognition, imprisonment, execution, confiscation, war
termination, agent removal, native opinion or family sanction is triggered. Native
CK3/AGOT events keep responsibility for their existing choices and effects. This
record is an observation, not a new legal basis or duplicated native punishment.
A false allegation cannot create one through the existing allegation interaction.
No game rule, service promise, mediation state or existing case evidence is rewritten.

Source-contract tests include negative mutations for replacing native action blocks,
wrong scheme/target/observer, undiscovered plots, hidden/wrong agents, intake bypass,
cross-plot/participant deduplication and hidden-organiser substitution. Archive access,
read-only behavior, no native side effects, localization, retention, reference graph
and duplicate public definitions are also checked. These tests do not execute CK3.

The exposed-state guard intentionally fails closed if the native callback runs before
that state is visible; no delayed retry or polling is invented. Final testing must
establish ordering, predicate knowledge semantics, additive dispatch, notice rate,
saved story iteration scopes, privacy, deduplication, plot end and reload behavior.
Older saves gain entries only from future callbacks; no historical plot is scanned
or backfilled. No migration success is claimed.

The voluntary response is now in RW010_SCHEME_RESPONSE.md. Next investigate native
legal eligibility and prior consequences before coercive personal sanctions,
while preserving native justice and avoiding duplicate effects. Actual family/house
sanctions and restoration remain a separate G3 stage. The unlawful-war feature stays
at its G1 stage. Source entry points are now located; engine feasibility is still open.
