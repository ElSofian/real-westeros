# RW-010 — contested affront allegation

Current amendment: RW010_REPAIR_RESPONSE.md replaces the automatic client opinion benefit with explicit acceptance/refusal; mediator opinion remains separate. Earlier flow descriptions below predate this change.

**Original experimental CK3 scripts, not engine-tested.** This is a structured
political allegation action, not automatic detection of vanilla insults, discovered
assassination schemes, fabricated objective truth or an offline Python simulation.

## Incident and statements

A living landed adult may allege that another ruler affronted their house if both
have a separate common top liege. There is a ninety-day initiator cooldown. The
new action creates an independent case story, with kind `allegation`, immutable
reason `allegation`, evidence `unanswered` and stage `respondent`. It transfers no
gold/prestige/opinion and changes no native secret, hook, crime, title or relationship.
The alleged underlying insult is not simulated or independently verified by this
slice; characters may make strategic allegations or acknowledgments.

The respondent can acknowledge the remarks, contest the account, or ignore it.
Acknowledgment/contest is recorded as the actual statement chosen, then the stage
moves to the claimant. Neither is an independent finding of underlying truth. A
denial does not prove innocence or a false accusation. Silence remains unanswered,
and deadline expiry never promotes it to admission or guilt.

After a statement, the claimant can withdraw neutrally or refer the account to the
separate common overlord. No response means only neutral expiry. The original
thirty-day case deadline is never renewed by replies or referral. Explicit stage,
record/kind/owner/serial/party/reason and current-jurisdiction checks protect actions
and stale popups. AI and human parties use the same choices/effects; initial AI
selection is bounded to liege targets and requires opinion below -25. No runtime
LLM or global character-pair search.

## Disclosure and ruler response

Merely selecting a possible mediator does not inform that ruler. Before claimant
referral only claimant and respondent can browse the case. Referral records the
specific disclosure and moves to the ruler stage. Shared archive filters use the
same parameterized reader-role trigger in visibility and execution; a stored mediator
role additionally requires disclosure. Outsiders cannot query the case.

The ruler can decline or invite a voluntary conciliatory gesture for either account.
The existing personal reprimand (-10 opinion, not a criminal sanction) requires a
recorded service breach or an acknowledged allegation. A contested allegation alone
cannot use that option. This is a deliberately narrow soft-mediation policy, not a
universal law forbidding arbitrary rulers or a legal proof standard for other crimes.

The respondent may decline repair without an automatic extra penalty, or pay 25
prestige for the existing +5 opinion conciliatory gesture. This does not change
`rw_case_evidence`, establish a crime, erase the statement or perform/pay any service.
Withdrawal/conciliation/outcome are distinct from what was alleged and answered.

## Persistent record and reading

Case kind now participates in identity checks so independent allegation/service
serial counters cannot authorize cross-kind callbacks. Record stories still retain
closed cases for 1825 days with periodic cleanup, or end on owner death; there is no
heir transfer or house-memory claim. The internal provider/client aliases mean
respondent/claimant for this kind; no service receipt is consumed or modified.

Known participants can open the record archive and read the preserved allegation
and reply separately from the outcome. Statement reading rechecks the reader and
case and has no native effects. Destroyed/inaccessible records yield inert text,
not a conclusion about truth or silence.

Earlier experimental stories without kind/disclosure metadata are **not** inferred
to be disclosed service facts. New decision/read guards fail closed for them; no
missing provenance is invented. Existing passive expiry/retention cleanup remains.
Fresh disposable saves are preferred for final testing; no old-save migration or
runtime scope-persistence compatibility is established.

## Checks and final campaign (no game runs performed)

Run the full unit/static suite and structural validator. Mutations detect invented
admissions, automatic disclosure, unsupported/replayed replies/referral, reading
before disclosure, contested reprimands, wrong case kind and apology-as-admission.
Reference/localization/BOM checks cover all new scripts and EN/FR display keys.
These inspect source structure, not CK3 truth, AI or save/load semantics.

Final engine cases:

1. Create the allegation: zero penalties and `unanswered` evidence. The planned ruler
   and strangers cannot browse; both parties can read their record.
2. Acknowledge, contest and ignore in separate saves. Verify exact statement storage,
   no automatic native crime and neutral deadline expiry for unanswered allegations.
3. Withdraw after either reply: no penalty, but the reply remains in the archive and
   no ruler disclosure occurs. Referral instead reveals only this case to its ruler.
4. In the admitted case, ruler personal reprimand is optional; in the contested case,
   only non-intervention/voluntary repair is available. Confirm the effect-level guard
   rejects a stale/forced reprimand response too.
5. Decline a conciliatory gesture, or accept with sufficient prestige. Verify no
   compelled admission, no evidence rewriting, no service settlement and no repeated
   cost on replay. Insufficient prestige must hide/deny the paid gesture.
6. Open service and allegation cases for the same respondent, including equal serial
   numbers in their distinct kinds. No cross-case/kind state, effects or disclosures.
7. Save/reload every turn and read the archived statement after closure; test old
   popups, deadline, changed lieges, deaths, minorities and lost scopes. No inherited
   guilt or native AGOT lifecycle change. Test legacy metadata absence is inert.
8. Observe AI choices, accusation spam/incentives, performance and AGOT baseline logs.
   Do not claim calibrated behavior, privacy/persistence guarantees or compatibility
   before this campaign. Native scheme-discovery integration remains separate work.
