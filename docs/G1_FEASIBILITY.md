# G1 feasibility — politically illegal vassal war with an authentic CB

**Status (2026-10-26): BLOCKED for implementation; source-location investigation is in progress.**
**No CK3/AGOT runtime test, no gameplay script, no evidence of a working bypass.**
This document is a version-conscious engineering gate, not a promise that G1 is feasible.

## Exact question

Can a vassal deliberately defy a realm-law prohibition while using the *same*
valid vanilla/AGOT casus belli, native declaration interface, war lifecycle and
AGOT Mega Wars logic? Only the *political-law* restriction may be bypassed.
Missing claims, wrong targets, unrelated CB conditions, imprisonment, and
native impossibilities must still reject the action.

## Evidence and confidence

| Evidence | Version | Observation | Confidence for CK3 1.19 / AGOT 0.5.2.1 |
|---|---|---|---|
| Repository `docs/TECHNICAL_GATES.md` | Prior AGOT descriptor 0.5.2.1, CK3 support 1.19.0.6 | Identifies likely AGOT files and trigger names, not independently re-inspected this run | Lead only |
| [CK3DB Declare War](https://ck3db.com/interactions/declare-war) | CK3 **1.20.1.2** | Public index shows `declare_war_interaction` validity checks both `has_any_display_cb_on` and `allows_declaring_war_against_target_trigger`. The expanded conditions include hierarchy, realm-law, contract and hook checks. | Medium for 1.20.1.2; **unverified** for 1.19/AGOT |
| [CK3DB Ask for Permission](https://ck3db.com/interactions/ask-for-permission-to-declare-war) | CK3 **1.20.1.2** | Some government types have a separate permission variable; this is not evidence of a general bypass. | Low transferability |
| [CK3DB public reference](https://ck3db.com/scripted-triggers) | CK3 1.20.1.2 | A third-party index of scripted triggers, not the project's pinned executable. | Research only |
| Local installed CK3 scripts | CK3 1.19.* target | **Not available** in this execution. | None |
| Local installed AGOT scripts | AGOT 0.5.2.1 target | **Not available** in this execution. | None |
| CK3 engine run | None | **Never executed**. | None |

**Key finding:** The indexed 1.20.1.2 interaction has **multiple distinct
validity checks**, so relaxing a single `can_attack_in_hierarchy` call is not
proof that a native CB becomes selectable. The public index also shows
`on_accept` handling notifications, hooks, and other post-declaration
side effects. Replacing the interaction with a simplified copy risks dropping
native behavior. These observations cannot be assumed to apply unchanged to
CK3 1.19 or AGOT 0.5.2.1.

## Boundaries to investigate in the pinned versions

1. **Interaction visibility and validity:** Compare the *effective* AGOT
   `declare_war_interaction` against CK3's original. Identify each political
   law check and each unrelated restriction. Determine whether AGOT replaces
   the interaction definition or extends its helpers.
2. **CB enumeration / selection UI:** Trace
   `has_any_display_cb_on` and any CB `can_use`, `can_use_title`, cost,
   hierarchy, and targeting checks. Determine whether political law also
   removes the CB from the native selector. An enabled interaction alone is
   insufficient.
3. **Native declaration operation:** Identify a **documented and supported**
   way to invoke the existing CB with the normal declaration flow. Verify that
   the engine, not an invented script effect, owns war creation and CB data.
4. **AGOT lifecycle:** Inspect
   `common/scripted_triggers/00_agot_mega_wars_triggers.txt`,
   `common/on_action/agot_on_actions/agot_war_on_actions.txt`, and
   `common/story_cycles/agot_story_cycle_mega_wars.txt`. Determine which
   hooks fire from a normal declaration and whether any alternate path
   bypasses them. Check war end and cleanup too.
5. **AI parity:** Verify the same availability and CB rules for human and AI
   characters. A bounded AI opportunity selector may decide *when* to attempt
   the action; it may not grant a different mechanical bypass.
6. **Save/reload and timing:** Capture legality when war is declared, not
   retroactively from a later change of law or liege; do not store a fake
   substitute CB.

## Options (not implementations)

| Option | Condition to consider it | Current verdict |
|---|---|---|
| **A. Additive opt-in interaction** that routes to the native CB selector/declaration | Pinned source/API proves it can pass the *original* CB through without bypassing other restrictions or native AGOT hooks | **Unproven**; preferred only if demonstrable |
| **B. Narrow override of a shared scripted trigger** with explicit unlawful-war context | Pinned source proves a safe, scoped override is possible without changing all other war declarations or competing with AGOT | **High risk**; avoid unless A is impossible and complete regressions can be tested |
| **C. Replace `declare_war_interaction` or a global war on_action** | Would duplicate vanilla/AGOT definitions and lifecycle | **Rejected by default**; compatibility hazard |
| **D. Invent a generic CB / trigger an unrelated war** | Loses the authentic CB and may bypass Mega Wars | **Rejected — violates project design** |
| **E. Temporarily grant a legal exemption or change the realm law** | Changes political legality and may affect unrelated actions | **Rejected as a silent workaround** |

No isolated CK3 script spike is justified until option A or B has an
identified native entry point in the pinned source. A syntactically plausible
but unverifiable `start_war` snippet would not advance the gate.

## Reproducible private source-location check

A stdlib-only helper locates candidate files and identifier line numbers
**without copying, displaying or committing any CK3/AGOT code**:

```bash
python tools/audit_g1_sources.py --ck3-root "<CK3 installation>/game" --agot-root "<AGOT mod directory>"
python tools/audit_g1_sources.py --ck3-root "<CK3 installation>/game" --agot-root "<AGOT mod directory>" --json
```

`LOCATED_UNVERIFIED` means a file and its expected identifiers were located,
**not** that the source was parsed, that the identifier is executable, or
that any war is possible. `REVIEW_MARKERS` indicates a missing candidate
identifier, which may be a version change or an incorrect prior assumption;
`MISSING`, `EMPTY` and `UNREADABLE` likewise require investigation.
The command exits nonzero for any unresolved reference. It prints only
relative paths, identifier names and line numbers, never absolute paths or
source contents. Its fixtures are synthetic, not CK3 assets.

## Minimal next evidence required

- Pin **actual** CK3 executable build, AGOT descriptor and load order.
- Run the source locator against those private local directories, inspect
  the **full relevant blocks** privately and record only short findings
  and references in this repository. The source locator alone is insufficient.
- Identify the native war-declaration entry point that retains a chosen CB.
  If it cannot be found, keep G1 **BLOCKED** and do not write a fake war.
- Only then implement an isolated experimental spike in a separate PR,
  with negative-path checks (missing claim, wrong CB target, law exception).
- Execute the high-signal cases in
  [TEST_PLAN_G1.md](TEST_PLAN_G1.md): G1-01 through G1-05, G1-08,
  G1-10 through G1-13, then AI and regression cases. Compare against
  AGOT-only baseline. No gameplay claim before these engine tests.

## Decision

**BLOCKED / NO GO for gameplay implementation today, not a proven technical
impossibility.** Public CK3 1.20.1.2 evidence demonstrates several gates and
post-declaration side effects, but does **not** demonstrate a supported,
version-correct way to bypass only political law while preserving the
original CB and AGOT lifecycle. Continue independent G2 research while
the pinned private source/engine boundary remains unavailable.
