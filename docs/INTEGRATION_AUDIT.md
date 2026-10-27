# Integrated lifecycle audit — RW-010

Scope: source review of the integrated experimental slices, not proof of CK3
execution, scheduler semantics, save compatibility, atomicity or performance.
All engine scenarios remain deferred to the final campaign. The audit does not
complete RW-010 or the three original owner scenarios.

## Finding corrected: repeated decision reminders

Previously, a provider could review the same promise more than once and choose
wait in each popup. Each wait scheduled another visible decision seven days later;
all had the same live obligation identity. Each could wait again, creating several
independent reminder chains. The cancellation-proposal option also scheduled wait.
Contract identity alone prevented cross-contract settlement, not this fan-out.

The correction uses an independent monotonically increasing decision serial:

- Acceptance schedules one hidden reminder for day eight; wait schedules one for
  seven days later. The hidden dispatcher checks contract, due window, current
  decision serial and a pending ticket before consuming it and opening a popup.
- Manual review allocates a new decision serial and opens a decision immediately.
  It cancels the old reminder ticket and invalidates older popup choices. Review
  itself schedules no recurring event and adds no player action count limit.
- A provider choice requires the current ticket and open-decision marker. Wait
  consumes/replaces them; fulfillment, breach and cancellation clear both markers.
  An obsolete popup may still be visible with only its neutral dismissal option.
- The provider's popup cancellation proposal checks the same decision identity.
  The separate cancellation interactions and the other party's consent retain
  their independent guards; reviewing a promise never invalidates their request.
- Decision identity never changes the original quote revision, price, mode, due
  date or deadline. The independent day-thirty-one timeout does not require an
  open decision or current reminder; silence cannot indefinitely suspend it.

Queued obsolete hidden events are not physically deleted from the engine queue.
Their source guards make them inert. This removes the observed source path for
multiple live reminder chains, not a measured engine performance result. Ticket
scope capture, flag timing, same-day ordering and persistence still need CK3 tests.

Old experimental saves may have visible popups/reminders without decision metadata.
They fail the new decision gate. A valid manual review allocates fresh metadata;
existing original timeout callbacks remain independent. This is a fail-closed source
policy, not an engine-tested migration guarantee. Prefer a disposable fresh save.

## Boundaries reviewed

| Boundary | Source result and remaining limit |
|---|---|
| Quote → promise | Consent increments revision; old quotations cannot settle the accepted obligation under saved identity checks. No prepayment. |
| Promise → performance/breach/release | Terminal cleanup consumes active identity and invalidates cancellation/reminder state; original timeout has independent ownership guards. |
| Provider decision → cancellation request | Decision ticket is required for the popup action; request serial and explicit responder consent remain separate. |
| Breach receipt → referred case | Only an unreacted observed breach can open a service case; story identity/kind keeps later cases independent. Latest non-referred receipts remain single-slot. |
| Allegation → mediator | An accusation is not native evidence; mediator gets access only after explicit disclosure. Contested allegations cannot authorize the reprimand option. |
| Mediation → conciliatory gesture | Provider cost and mediator opinion are distinct from the client's voluntary response; response does not rewrite evidence, service facts or native guilt. |
| Archive → active gameplay | Archive views retain role/disclosure filtering and contain no settlement/response effect. Story scope capture during enumeration remains engine-unverified. |
| Owner death → succession | Personal stories end on provider death; no scripted obligation/guilt transfer to heirs. No general dynastic system is implemented. |
| Source → distribution | Only committed allowlisted regular inputs enter the ZIP; manifest/ZIP checks validate packaging, not CK3 semantics. |

No further defect is asserted from these boundaries based only on this review.
Existing absence of native scheme-discovery sources remains a specific source gate;
no global CK3/AGOT lifecycle hook was invented or overwritten during the audit.

## Available verification

`tests/test_integrated_lifecycle.py` checks the dispatch/consumption graph and rejects
mutations removing ticket/actor/deadline guards, resetting counters, bypassing the
scheduler or leaving terminal tickets live. It also checks independent timeout,
consent and story flows plus duplicate public event/story/effect definitions.
These tests inspect original CK3 source; they are not Python gameplay prototypes.
Run the full suite, structural validator, whitespace check and real ZIP build.

## Final-campaign observability

Use the existing FINAL_ENGINE_TESTS.md scenarios and the additional LIFE-* cases.
For every case record actual versions, DLC/playset, manifest commit, test save,
actors/roles, starting state, exact action sequence, elapsed game days, observed
balances/opinions and notices. Keep pending/not-run distinct from pass/fail.
Where available, attach the relevant parser/error-log excerpt and screenshots.
Missing errors alone are not a pass; compare the actual outcome with the expected
result. No always-on telemetry, runtime LLM, paid service or global polling is added.

After the engine campaign, fix reproducible failures by scenario, rebuild from the
corrected commit and rerun affected regressions before any compatibility claim.
