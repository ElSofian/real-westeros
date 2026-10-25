# G1 — Illegal vassal war: reproducible CK3 test plan

**Status:** Test plan only. **No CK3 engine test has been performed.** This plan is not proof that G1 can be implemented. It must be adjusted after RW-004 verifies the actual CK3/AGOT hooks.

## Goal and hard gate

Allow a character to *attempt* a politically forbidden vassal war while retaining the **original, valid CK3/AGOT casus belli (CB)** and the ordinary war lifecycle. Political illegality may cause a reaction or sanction; it must not silently turn the war into a fabricated generic CB, bypass native AGOT Mega Wars processing, or make the AI obey different execution rules.

**G1 is blocked** if there is no supported way to preserve the original CB and the native war lifecycle. In that case, record the exact failing source/API boundary and do not ship a fake substitute.

## Required environment (record before testing)

| Field | Record |
|---|---|
| CK3 executable version / platform | Unverified |
| AGOT mod version, source, checksum | Prior audit descriptor: 0.5.2.1; current install unverified |
| Real Westeros commit SHA and version | Unverified |
| DLCs and other enabled mods | Unverified |
| Playset load order | AGOT before Real Westeros; unverified |
| Save date, bookmark, start character and realm | Unverified |
| Relevant realm law and vassal contract terms | Unverified |
| Original CB identifier and its usual legal requirements | Unverified |
| Game rules / debug mode / logs path | Unverified |

Use a disposable save and a separate baseline playset. Never alter AGOT or vanilla files in place. Do not commit game scripts, personal saves, log dumps containing personal paths, or proprietary assets.

## Evidence to collect for every case

1. Case ID, exact save/setup steps, character IDs or anonymized references, applicable law and original CB identifier.
2. Whether the interaction is offered and why it is enabled/disabled.
3. War type and CB *before and after* start, attacker/defender, titles targeted, and war result.
4. Relevant CK3 error log entries, mod-specific logs and screenshots; redact personal paths and keep large/binary evidence outside the public repository.
5. End-state checks: realm law, titles, vassal relationships, prisoners, truces, political sanctions, Mega Wars state and cleanup.
6. A pass/fail/blocked verdict, reproduction steps, CK3/AGOT version, Real Westeros commit and whether the result was observed in engine or only inferred.

**Do not mark a case PASS from source inspection or a green Python CI run.**

## Scenario matrix

| ID | Setup / action | Expected outcome to verify |
|---|---|---|
| G1-01 Baseline lawful war | With no political prohibition, declare a vanilla/AGOT-legal vassal war using a recorded authentic CB. | Existing interaction, CB, war start, war end and hooks work exactly as with AGOT alone. |
| G1-02 Forbidden war available | Enable a relevant law forbidding vassal warfare, keeping the same authentic CB requirements satisfied. Attempt the same declaration through Real Westeros. | An explicit *politically unlawful* option exists if technically feasible; it does not silently override the CB's original non-political requirements. |
| G1-03 CB integrity | Start G1-02; inspect the resulting war, target, participants and effects. | **Original CB identifier and effects remain intact.** Any generic/fake CB or altered war target is a hard failure. |
| G1-04 Validity negative | Remove the underlying claim/CB or fail an unrelated native prerequisite while retaining the political prohibition. | The new option cannot manufacture a CB or bypass unrelated CK3 restrictions. |
| G1-05 Law/contract exception | Configure a lawful vassal-war exception or change the applicable contract while preserving a real CB. | The war is classified lawful when the exception applies; no unlawful penalty is invented. |
| G1-06 AI parity | Create a comparable AI↔AI pair with the same prohibition, real CB and political incentives. | AI can evaluate the same action and legal/illegal conditions without guaranteed spam or player-only privilege. |
| G1-07 Refusal / non-action | Give AI a weak incentive, high risk, or no CB. Observe multiple comparable opportunities. | AI can abstain; no repeated invalid declarations or runaway event loop. |
| G1-08 AGOT Mega Wars | Trigger a qualifying large-scale conflict where AGOT's Mega Wars lifecycle should apply. | Classification, escalation, participants, outcome and cleanup are preserved. Compare with AGOT-only baseline. |
| G1-09 Non-Mega-War | Start a local conflict that should not qualify as a Mega War. | No accidental Mega Wars activation or lingering story-cycle state. |
| G1-10 War resolution | Resolve an unlawful war by victory, defeat and white peace in separate disposable saves. | Native peace effects, truces, occupation cleanup, titles and hooks work; new sanctions are separate and not duplicated. |
| G1-11 Mid-war changes | Change realm law, contracts, liege, or a participant's status while a war is ongoing, where game rules permit. | Legality of the original act is evaluated at the act's time; lifecycle is not orphaned by later political changes. |
| G1-12 Succession / death | Kill or replace a principal war participant or liege during the war; test relevant inheritance paths. | Native war succession and AGOT state remain coherent; personal guilt is not automatically inherited. |
| G1-13 Save/reload | Save before declaration, during war and after peace; reload each save. | CB, participants, war and political state survive reload without double sanctions or ghost state. |
| G1-14 Multiple wars | Start two permitted concurrent conflicts or independent realm conflicts, if native rules allow. | No cross-war state contamination; each incident has stable identifiers and cleanup. |
| G1-15 Other native actions | Exercise revocation resistance, imprisonment, title grant and unrelated diplomatic actions before/after war. | Real Westeros does not replace or duplicate native sanctions or authority rules. |
| G1-16 Stress / logs | Repeatedly create and conclude representative wars, including AI opportunities, on a disposable save. | No increasing error count, runaway AI loops, significant performance regression or persistent war state. Quantify against baseline. |

**Pass criteria:** G1-01 through G1-05 and G1-08 through G1-13 must have reproducible engine evidence; G1-06/07 must demonstrate AI parity and non-spam; G1-14 through G1-16 are regression gates before broad release. Any fake CB, broken Mega Wars lifecycle or corrupted title/succession state blocks G1.

## Minimal reproducible procedure

1. Install a known CK3 + AGOT version, record version and load order, and confirm AGOT-only baseline.
2. Select a reproducible vassal, liege, target and original CB; document the original interaction's enablement and legal restrictions.
3. Create a disposable save, toggle the political prohibition, and compare the interaction/war behavior with and without Real Westeros.
4. Record the war's actual CB, all relevant native hooks and the political consequences separately.
5. Repeat across each applicable scenario, collecting failures before broadening the implementation.
6. Only after the above passes, label G1 **engine-tested** for the specific version/playset. Re-run after CK3/AGOT updates.

## Interpretation

- **Static-checked:** scripts and metadata passed repository checks; no gameplay guarantee.
- **Engine-tested:** the exact scenario was observed in a recorded CK3/AGOT environment.
- **Blocked:** source/API limitations or unavailable game environment prevent verification.
- **Failed:** the engine demonstrably violated a pass criterion.

The owner prefers minimizing manual testing. Use static checks for every change and prioritize a small, high-signal in-game matrix when CK3 becomes available; do not reduce the critical CB/Mega Wars tests or claim that an untested feature is finished.
