# G3 title-route source intake — resumed investigation

**Source-checked; not engine-tested.** The owner returned and supplied the targeted
TitleRoutes collection. Collection is no longer on standby. No further upload or
intermediate CK3 run is requested. This audit does not implement a title ban,
confiscation, restoration of noble status or an acquisition veto.

## Verified input and privacy

The private ZIP SHA-256 is recorded in TITLE_ROUTE_SOURCE_RECEIPT.json. All **719
files / 46,140,537 bytes** match the private manifest, including 301 CK3 and 418
AGOT files. Exact ZIP/manifest membership, duplicate names, traversal, link entries,
sizes and hashes were checked before extraction outside Git. Thirty reviewed files
are referenced publicly by relative path, hash, size and short marker positions only.
Original scripts, ZIP, full manifest and installation paths are not published.

Descriptor metadata reports AGOT 0.5.2.1 supporting CK3 1.19.0.6. The executable and
DLC remain unverified. Depth-one collection leaves **716 dependency-frontier
paths**; no missing scanned group is reported. Neither fact proves full coverage.
The collector's empty missing-election list is a lexical candidate result, not
proof of active laws, effective load order or an enforceable restriction.

## Grant interaction: real entry point, several eligibility branches

Both collections now contain `common/character_interactions/00_grant_titles_interaction.txt`.
The grant definition uses a native special interaction, grant interface, title
target and actor-domain title filter. Actor is the giver; recipient receives titles;
the per-title picker examines `scope:target`, while checks may inspect `target_titles`.
The native source explicitly places the actual grant in engine code. Scripted
`on_accept` consequences do not establish when that engine transfer occurs.

The AGOT recipient validity check accepts alternative branches: ordinary
`can_be_granted_titles_by`, theocratic eligibility, or an eligible co-ruler diarch.
Blocking only the ordinary helper would leave alternatives. Actor/recipient
visibility, recipient validity, selected-title eligibility and send-time checks are
separate. Existing Night's Watch, religious/status, settlement, administrative,
nomadic and diarchy conditions must be preserved. Native auto-accept is a property
of this grant flow, not evidence of a negotiated restitution contract.

Finding the definition allows a precise future native-window investigation. It
does **not** establish an additive way to inject a sovereign house ban into that
definition. Replacing it, cloning its special interaction or applying a post-grant
reversal is not authorized by this source result. Scripted transfers elsewhere
also need their own coverage; the inspected Wall action directly resolves a
title/vassal change without calling this interaction's recipient helper.

## Elections: candidate lists are distinct from voting scores

The collection contains sixteen election files and thirteen uncommented top-level
definitions: seven CK3 types and six AGOT types. Four AGOT files for princely,
Gaelic, Saxon and Scandinavian elections contain no uncommented definition.
Their presence must not be mistaken for an active type, nor their emptiness for
proof that CK3 falls back to its version. The sanitized metadata does not establish
effective file replacement/load order for the actual playset.

Feudal candidates come from direct vassals, de jure vassals, claimants and family,
with separate helper predicates. AGOT pirate election adds its own candidate
checks. Magisterial types use a different direct-vassal/government eligibility
list; Kingsguard's inspected list adds the holder. A score penalty is not candidate
exclusion. Changing the shared unelectable-trait helper would not cover all these
lists, and native disinheritance is a personal mechanic with other consequences.

Most importantly, the Night's Watch election file and title law point to a
separate `agot_nw_elect_lc` effect. The received definition and Lord Commander
death action locate that route: it builds and scores candidates, uses its own
fallback, temporarily adjusts personal traits/law and designates an heir. This is
not the ordinary feudal candidate list. The Silent Sisterhood law likewise names
a separate succession effect; its definition was not located in this selection.
Do not infer its implementation from the Night's Watch or change either institution.

## Remaining route coverage and selected next work

| Route | New evidence | Still required before enforcement |
|---|---|---|
| Ordinary grant | Initiating interaction, three recipient eligibility branches, title picker and native special interface | A supported pre-transfer extension, scripted/other grant coverage, final dispatch/selection evidence |
| Hereditary succession | Native inheritance/partition configuration is present again | A demonstrated per-candidate house/jurisdiction gate for every applicable succession path |
| Elections | Actual type definitions, distinct candidate lists and a separate AGOT succession route | Active playset/law resolution, special routes and an actual exclusion mechanism, not a voting penalty |
| Conquest/claims | Earlier G3 claim-CB resolution audit remains applicable | CB/transfer coverage and a safe pre-transfer hook; this ZIP does not contain the CB directory |

G3 remains unresolved, not disproved. The four routes are a minimum matrix, not an
exhaustive list of all title movements; appointments, scripted transfers and regional
institutions can add paths. Do not reinterpret political censure as legal title
ineligibility or apply personal disinheritance to a whole house.

Next on this track: design a bounded, explicitly authorized **individual title
remedy** using native revocation/grant eligibility and genuine native UI/AI behavior
before considering stronger adapters. The subsequent read-only bridge to native
grant terms is in RW010_TITLE_REMEDIES.md; it is not that full remedy contract.
Opening terms is not a completed transfer;
confiscation and voluntary restitution must remain distinct, with current title,
holder, authority and consent rechecked. No forced native sanction or universal
house-ban implementation follows from this audit. The independent revised-promise /
receipt / mediation audit remains available without waiting for G3.

G3-04 and G3-06 in FINAL_ENGINE_TESTS.md now name the newly located branch and
special-succession risks. All final cases remain unrun. This PR changes only audit
documentation, hash references and the distribution documentation allowlist;
base gameplay and the separate optional trace are unchanged.
