# J2 — explicit native individual arrest request

**Original experimental CK3 scripts; static checks only, not engine-tested.**
J2 source acceptance is one real individual coercive path: a native arrest request,
not another window opener. Execution/confiscation/house sanctions remain separate.
No native definitions, helpers or callbacks are replaced.

## Flow and exact scope

The original observer may use the known-participant journal to consider sending a
native arrest request. A fresh exposed-participant observation also schedules one
character-root opportunity after one day, for human and AI observers alike. The
one-day delay lets the original native event finish; it proves no callback order.
Generic discovery, undisclosed organisers, relatives and heirs are not substituted.
Old records get no automatic opportunity; manual review still needs current native
eligibility. There is no repeated retry, character scan or inherited sanction.

The confirmation captures the exact displayed participant. The same guard is checked
before opening, on the choice and inside the dispatch effect. It requires the existing
observer-only story type/schema/serial/retention chain, living distinct participant,
free target, free original observer, and no prior dispatch from this exact record.
It also requires a current native imprisonment reason in observer→participant direction
and fresh `is_character_interaction_valid` for `imprison_interaction`. A current
reason is NOT attributed to the recorded plot or a prior verdict.

This first route conservatively excludes active diarchies, usable hooks against the
participant and the native hostile-actions delay. The inspected version has an
optional hook and a diarchy prestige surcharge; this avoids pretending to choose
unreviewed options or calculate their price outside native context. Both human/AI
use these same restrictions. Their normal native menus remain available for other
terms or arbitrary actions; this does not remove those actions from the game.

On deliberate confirmation, the record consumes its dispatch slot and stores date,
original actor and exact target BEFORE calling `run_interaction`, supplying the native
interaction, explicit actor/recipient and `send_threshold = decline`. It never sets
`execute_threshold = accept`, calls `on_accept`, uses a no-tyranny helper, consumes a
reason itself, or applies another arrest/cost/war. Native eligibility, fees, acceptance,
refusal/resistance and subsequent events remain native responsibilities. Actual
threshold, default-option and cost handling MUST be verified in the final engine run;
source syntax is not proof those engine semantics work for both human and AI senders.

The slot is a record of a **dispatch attempt**, even if the engine does not send,
refuses or leaves a pending request. It is never a receipt for successful custody,
punishment, guilt or pardon. A stale second choice cannot dispatch again. A distinct
native matter is not globally banned; the native menu is not disabled. The original
record retention/owner death lifecycle is unchanged, and no completed-sanction
callback or universal per-offense history is fabricated.

The human/AI may always leave the matter alone. The AI opportunity offers the same
choice, with positive nonintervention weight; traits and current war influence its
preference but never eligibility. It does not automatically sentence every participant.
Opening/ignoring cannot spend prestige/gold or change the evidence. The old read-only
judicial panel and human-only native-window shortcuts keep their existing scope.

## Evidence and available checks

`NATIVE_JUSTICE_ACTION_SOURCE_RECEIPT.json` contains only hashes/relative references
from the already supplied private sources: AGOT's existing `run_interaction` arrest
call with `send_threshold = decline`, native prison validity/can-send/hook/cost and
accept/decline handling, and the diarchy value. No proprietary source is distributed.
AGOT descriptor metadata previously reported 0.5.2.1 / CK3 1.19.0.6 support; executable
and actual compatibility remain unverified.

Nine adversarial source tests cover wrong/stale/foreign target and record, direct
effect guard bypass, consumption order, native actor/recipient/threshold, forced
acceptance, helpers/extra costs, AI exceptions, global scans, repeat opportunities,
discretionary no-action and localized exact identity. Existing observation/read-only
justice checks remain intact. These tests execute no native interaction or CK3.

Frozen J2 source criterion: individual arrest pipeline shared by player/AI through
the native interaction, with its refusal/resistance path retained in source.
**40 → 43/100 (+3 source); engine 0/20.** This does not complete J3/J4/J5 or establish
successful arrest, all sanction types, final game behavior or engine performance.
Next: W1/W2 genuine illegal-war track, under a separate RW-004 claim.

## Final campaign — no cases executed

| Case | Check / expected result |
|---|---|
| NARREST-01 | Load target CK3/AGOT; validate new triggers, event scopes, native run API, threshold and native default-option semantics. Stop enabling this route if they bypass cost/refusal/validity. |
| NARREST-02 | Fresh exposed participant with a current reason and valid ordinary arrest: one next-day opportunity; generic discovery or unknown participant gives none. Native prior arrest makes the later opportunity inert. |
| NARREST-03 | Human observer opens journal, confirms request. Observe native acceptance and actual custody separately; cancel via leave and verify no arrest, reason consumption or cost. |
| NARREST-04 | Native refusal/escape/resistance or rebellion: observe native consequences exactly once, no forced acceptance, direct prison effect, doubled war, sanction or cost. |
| NARREST-05 | AI observer and AI/human target: same eligibility/terms; observe both attempts and nonintervention, native recipient response and any pending request. No original-party substitution. |
| NARREST-06 | Lose current reason, gain native prohibition, imprisonment/war incompatibility or target detention/death after popup opens: fresh choice/effect guard blocks the attempt; no success claim. |
| NARREST-07 | Active diarchy, usable hook, hostile-delay flag: route unavailable for both player/AI; normal native menu remains. Confirm no optional hook consumed or surcharge bypassed. |
| NARREST-08 | Two open copies, save/reload before and after dispatch, obsolete serial, wrong observer/record/target, expired retained field and owner death: at most one attempt per record; no heir attribution. |
| NARREST-09 | Inspect receipt after native no-send, pending/refused and successful requests: it means attempt only; changed custody remains queried through existing panel. No native historical guilt inferred. |
| NARREST-10 | Multiple participants/plots, duplicate callbacks and archive browsing: one scheduled opportunity per fresh participant record, no retries/global pair scan. Measure final G4 spam/performance; regress ordinary AGOT arrest/execution/release/title/war/bank paths. |
