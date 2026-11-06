# First targeted G1 engine trial — 6 November 2026

**Partial engine evidence with failures; G1 is not cleared.** Baseline/result:
68/80 source + 0/20 full-campaign validation, delta **0**. Frozen criteria and
checkpoints unchanged. These observations do not complete player/AI, exception,
cost, lifecycle or Mega Wars acceptance criteria.

## Reproduction and evidence

Owner operated CK3; agent inspected local logs and disposable saves read-only.
Runtime log/save metadata: **CK3 1.19.0.6**, pinned **AGOT 0.5.2.1**. Effective
load list and mounted-data log: AGOT, Real Westeros, PRIVATE native-choice0.0.5.
Source revision `19d567fa439b5c0025b498187f463cbd2341f0fd`; four native input,
thirteen installed runtime and three generated output hashes matched. No disabled
DLCs configured; individual entitlements not audited. Raw evidence remains private.

New Crowned Stag campaign, 2 June 284: Leyton Hightower versus Paxter Redwyne,
shared direct liege Mace Tyrell. Console fixture granted actual `d_the_arbor`
claim and set the player's direct liege's `crown_authority_2`. This does not test
claim fabrication or ordinary law enactment. No `yesmen` or fabricated CB.

Owner observed native prohibition, then checkbox enabling declaration. War began
2 June; Mace's native stop-war negotiation arrived3June. Screenshots show accept,
favor, gold and refusal options, with missing defender/war labels. Owner refused,
reports no further message and defender army raised. Final save is **10 June**.

Read-only saves confirm:

- Before: no claim_cb war or RW declaration/response stories.
- After: active **`type=claim_cb`**, Leyton attacker/claimant, Paxter defender,
  La Treille target, start2June. This is a genuine native claim war.
- Declaration story: `permission_required`, `internal`,
  `claim_cb_on_declaration_prefix`; response links to it. Declaration/response/
  linked serials are **empty**, not valid identities. Response `native_requested`
  proves an attempt, not successful peace or complete native negotiation.
- Player prestige **1050→982**, gold **1472→1472**, piety **600→600**. Net prestige
  change−68 across eight days is not exact cost/uniqueness proof: displayed price
  was not captured. No inferred passive/event adjustment is subtracted.

Private-artifact SHA256 values (artifacts themselves are not distributed):

| Artifact | SHA256 |
|---|---|
| Before save | `36f91ecbe37909292c21cf5aaa5d086192f850666dbf9ad8185420b6829b398c` |
| After save | `f2cb9dd96cd276fa7a3174bc6e6f42f099568edd63f822f1e7dc22529b9766df` |
| Engine effects documentation | `83bec80303576bc4b3bc3180ce23044a64f16215da4f604081cebedf81fcd05b` |

## Observed defects and isolated correction candidate

Engine logs report changing empty counters and missing rw_dl/rw_uw serial values.
Both original paths now initialize a **missing** personal counter to numeric0
before incrementing. Existing counters are not reset. Old malformed receipts are
not reconstructed; use the before-save for retesting.

Native `vassal_interaction.0001` reports undefined `target` and unavailable
`primary_defender`, in a stack including RW dispatch. Empty labels are not a
harmless translation-only failure; refusal does not establish functional peace.
Owner ran `script_docs`: actual run_interaction documentation lists interaction,
redirect, actor/recipient, secondary actor/recipient and thresholds, **no target**.

PRIVATE adapter **0.0.6** extracts the already pinned stop-war definition, adding
one original metadata prefix to native `on_accept`; removing it restores native
bytes. This fourth private output is not shipped publicly. Before dispatch, the
consumed exact story and serial are stored as one-day sender-local markers.
Documented `redirect=no` preserves the checked actors. The callback helper checks
current parties/authority, active exact claim war, serial/state/result/date,
single-war context and issuer non-participation, then binds native `target` and
consumes markers before the unchanged native negotiation body. No-op sends clear
remaining markers after return. Ordinary native calls without markers do not
enter this path. Base availability is false; old adapters cannot queue/send it.

**Candidate is static-checked, NOT engine-tested.** Callback synchrony, propagation
into the native event and actual peace outcomes still require a run. This is not
a demonstrated generic special-interface API. No native event, war end, title,
claim, penalty or payment is replayed. Keep risky handoff isolated; do not merge
as working gameplay before targeted engine validation.

Local checks:1084/1084 tests passed, including missing/reset/late counter negatives,
private prefix inverse preservation, double-patch/layout refusal, old-adapter
fail-closed gate and transport guards. Structure, telemetry, readiness and whitespace
pass. Actual pinned private generation checks4 native inputs/13 runtime/4 outputs
and native stop-body inverse. Initial Windows environment failures were resolved
using writable test temp, exact LF checkout, scoped Git long-path settings and
execution outside the sandbox; no tests were disabled or acceptance checks relaxed.

## Next single-restart batch

Prepared locally after owner closed CK3: code revision
`c9d6a59a0e331355f3be983c6316b5b36832971c`, PRIVATE0.0.6,303 base/5 adapter
files copied and fully hash-verified with rollback backup. No game/AGOT files,
playsets or saves changed. PR#96 remains draft; corrected runtime trial pending.

Generate matching private0.0.6/base, verify hashes and inverse native bytes, then
synchronize while CK3 is closed with rollback backup. Preserve both saves and
usual playset. No hot reload established. After one restart load before-save,
cancel unchecked declaration once, then declare genuine claim with defiance;
capture displayed price/immediate balance. Save before native demand response.
Check positive serials/exact link, actual defender/war in letter/tooltips and logs.
On separate reloads test refusal and unconditional acceptance, verifying ongoing
war versus actual white peace, native effects and RW terminal closure. A different
discretionary royal choice does not establish absence of the handoff. Full AI,
exceptions, terminal/Mega Wars and compatibility campaign remain open, +0.
