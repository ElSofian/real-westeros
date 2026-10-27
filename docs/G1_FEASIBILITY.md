# G1 feasibility — politically forbidden war with an authentic CB

**Current status: ON HOLD by owner decision; may resume later.**
No engine test or additional collection is currently requested. Preserve the research
below as historical findings, not an active instruction to implement a crown-law
bypass. Native crown-authority, hook and faction behavior remains in scope to preserve.
The owner has not defined illegal war as merely violating promises/agreements; original
examples must be recovered before adopting a new definition. Engine feasibility remains
UNVERIFIED; standby is neither completion nor a verdict of impossibility.

**Research status before standby: source-backed candidate identified.**
Updated after private source inspection on 2026-10-27. No war script spike has been
shipped and no CK3 engine test has run. This is not a verdict of impossibility.

## Question and target

Can a vassal defy a political prohibition while retaining the original CB, normal
CB selector, costs, declaration and AGOT war lifecycle? Missing claims, wrong targets,
imprisonment and unrelated restrictions must remain effective. No substitute generic
CB, temporary legal exemption, changed realm law or fake hook is acceptable.

The user reports CK3 1.19.* and AGOT 0.5.2.1. The private collector report contains
AGOT descriptor fields `version=0.5.2.1` and `supported_version=1.19.0.6`. These are
reported metadata, not independent verification of CK3's executable build, active
playset, load order or effective runtime scripts. Seven supplied script files were
inspected privately. They are not committed here. Relative filenames, raw-file hashes
and marker line numbers are recorded in `G1_SOURCE_RECEIPT.json`.

## Findings from the supplied files

| Reference (relative to each source root) | Finding |
|---|---|
| AGOT `common/character_interactions/00_war.txt:1–5` | Declaration uses the native special interaction and declaration interface. |
| Same file, lines 68 and 89 | Hierarchy validation and displayable-CB enumeration are distinct gates; relaxing one is insufficient evidence. |
| AGOT `common/scripted_triggers/00_war_and_peace_triggers.txt:223–246` | `war_declarer_needs_hook_on_liege` expresses the ordinary law/contract gate: internal/all-vassal-war bans, war-contract exemption, and government/hierarchy conditions. This helper is identical in the supplied CK3 and AGOT files. |
| AGOT interaction, lines 366–412 | Target validity accepts either no need for a liege hook or a selected hook send option. The option separately checks usable hook possession. |
| AGOT interaction, lines 414–578 | Acceptance performs existing feedback and post-declaration side effects, including hook use and native war handling. Replacing it would risk losing behavior. |
| AGOT interaction, lines 200–295 | Administrative/permanent war bans and permission policies have separate checks. A feudal hook-gate change is not a universal bypass. |
| AGOT `common/on_action/agot_on_actions/agot_war_on_actions.txt:7–16` | Native war-start dispatch includes `agot_mega_war_action` and other AGOT handlers. |
| Same file, lines 18–60 and 130 onward | Victory, defeat, white peace, invalidation and transfer have separate handlers. Mega War initialization uses the war scope and separate classification trigger. |
| AGOT `common/scripted_triggers/00_agot_mega_wars_triggers.txt:3–67` | Mega War eligibility includes hierarchy, government and historical exceptions. An unlawful peer war must not automatically become a Mega War. |
| AGOT `common/story_cycles/agot_story_cycle_mega_wars.txt:29–80, 691 onward` | Story termination rebuilds realm state through external effects; there is also a fallback for missing/invalidated wars. Referenced effects are not included in this upload. |

### Correction to earlier research

The earlier lead `allows_declaring_war_against_target_trigger` came from a third-party
CK3 1.20.1.2 index. It is absent from both supplied war-interaction/helper files.
`can_attack_in_hierarchy` is called by the interaction, not defined by the supplied
war-and-peace helper file. Its implementation/complete semantics are not established
by this subset. The locator now searches the actual observed hook-gate identifier;
it must not report the newer index as evidence for the target build.

## Implementation route to investigate first

The strongest source-backed candidate is a **narrow contextual change to the
hook-requirement helper**, preserving the existing native declaration interaction,
selector and CB. It would apply only to an explicitly selected unlawful attempt
with a recorded actor/target/context; outside that context behavior must be identical.
The actual law/contract must remain unchanged so political illegality can be recorded.
This is a candidate, not implemented code or proof the engine accepts it.

Before writing this spike, establish:

1. Whether hierarchy/CB enumeration and individual CB validity independently reject
   the same crown-law condition. The helper alone cannot establish this.
2. All call sites of the hook helper and all effective definitions supplied by mods.
   A global helper override can affect other contexts and mod load-order conflicts.
3. How an opt-in actor/target context survives the native UI, cancellation, same-tick
   revalidation and AI declaration. No marker may grant a general lasting bypass.
4. How legality is recorded at actual declaration, then consumed once without replacing
   AGOT start/end hooks. Cancellation must not count as a political offense.

An additive interaction routing to the native selector remains an alternative only
if target-version source/API and runtime tests show it preserves the full flow.
Do not copy the existing interaction wholesale into the public submod. Do not invent
an undocumented `start_war` effect or claim an override can alter engine internals.

## Remaining evidence and smallest useful test

The seven-file subset is sufficient to locate the scripted crown-law gate, but lacks
CB definitions and the other helper call sites. Inspect the installed claim CB
(`common/casus_belli_types`), relevant laws/contracts, and matching references in
scripted triggers/effects before selecting the patch boundary. Obtain the exact CK3
menu/executable version. Source review cannot prove the engine's hidden checks.

Then run an isolated, disposable-save spike against an AGOT-only baseline:

- A legal claim war at peace: same native CB, target title, cost and declaration.
- The same valid claim under the relevant crown-law ban, without a hook or contractual
  exemption: only explicit unlawful intent may admit it. Verify CB identity afterwards.
- Missing claim, wrong target and imprisonment: still rejected; cancellation leaves
  no offense or reusable bypass. Existing legal hook/contract routes remain intact.
- Save/reload and AI: context cannot leak to a second target; AI uses the same gate.
- Resolve by victory, defeat, white peace and invalidation; compare title/realm state
  and AGOT logs. Test an eligible Mega War separately, including story cleanup.

Use `TEST_PLAN_G1.md` for the expanded cases. Failure of a particular helper override
rules out that patch, not automatically every possible implementation of G1.

## Private inspection tool

Run `python tools/audit_g1_sources.py --ck3-root <private-game-root> --agot-root <private-mod-root>`.
It reports only relative paths and identifiers; `LOCATED_UNVERIFIED` is a location
result, not a semantic or engine pass. Its tests use synthetic data. No private local
installation paths, source code, saves, archives or game assets belong in Git.

## Decision

**Proceed with targeted source investigation and then an isolated engine spike.**
The source hurdle is narrower than previously known: a concrete script-level gate
exists. G1 is neither approved as working nor rejected as impossible. The next blocker
is missing CB/call-site evidence and engine execution, not missing war-interaction files.

## Complement inspection and private diagnostic (2026-10-27)

A second private upload supplies 94 script files: 76 CB files, 14 law files, three
trigger files and one Mega War effects file. Hashes only are recorded in
`G1_COMPLEMENT_RECEIPT.json`. The requested `common/vassal_contracts` directories
were absent; that collector path was a lead, not a verified CK3 directory name.
No complete installation or all-mod call-site coverage is implied.

The AGOT `common/casus_belli_types/00_claim.txt` defines the original `claim_cb`.
Its visible conditions (lines 49–58, 64 onward) include Mega War availability,
invalid-target checks, claimant/title conditions and the normal costs. Lines 296–300
retain claim-based targeting and the existing declaration callback. No direct
reference to the crown-law flags or the hook helper was found in this supplied
claim file, or in the other 75 supplied CB files. This is a source-text finding,
not proof that delegated triggers, cost helpers or engine internals cannot reject it.

AGOT `common/laws/00_realm_laws.txt:156,252` supplies the ordinary internal/all-war
ban flags. `common/scripted_triggers/99_agot_rv_triggers.txt:59` also defines a distinct
rescue/revenge helper using attacker/defender scopes; it is not the declaration
interaction's actor/recipient helper and must not be silently changed with it.
Mega War effects call `start_war` in several rebuild paths (around lines 2111–2276),
but those calls are not evidence that a replacement declaration would retain normal
UI, costs or callbacks. The native UI route remains the preferred test.

There is now enough source evidence to build a **private diagnostic**, not a
production bypass: `tools/build_g1_probe.py` preserves the installed helper body
and adds a narrowly flagged feudal-peer exemption. It generates a separate mod
outside the checkout; no installed file is modified and no proprietary helper is
committed. See `G1_PROBE.md` for baseline, negative, declaration and cleanup checks.
Its one-day flags are manual diagnostic controls, not a proven production intent
or receipt mechanism. All runtime semantics and actual override loading remain
unverified. G1 stays OPEN pending execution; no third source dump is prerequisite
to attempting this narrow test, although a failure may reveal another dependency.
