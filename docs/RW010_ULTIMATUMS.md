# Credible political ultimatums — P4

**Static-checked only; not engine-tested.** Original CK3 scripts connect a structured
political demand to the existing guarded native arrest-request path. No runtime
Python, LLM, native override or new legal ground is introduced.

## Scripted path

From the existing arrest confirmation for an original known exposed participant,
the original observer may issue one ultimatum instead of immediately requesting an
arrest. Issue requires an **already current native imprisonment reason**, native
interaction validity, the existing conservative hook/diarchy/delay guards and no
prior shared dispatch. Both actual parties must be living free adults; the observer
must still rule from their court and the addressee must be their direct vassal or
courtier. This is not a demand to an arbitrary stranger or an invented crime.

Terms are fixed, not editable: **public regret for damaged trust within seven days**,
at a personal cost of **25 Prestige**. The addressee explicitly chooses regret,
rejection or silence. Regret is not an admission of the plot, truth of the observation,
a legal verdict or purchase of immunity. It consumes the pending demand before the
one prestige debit, closes this custom arrest route for this observation and changes
no native legal reason. Rejection records an actual reply; silence is observed only
after the answer window expires. Neither creates a crime or authorizes punishment.
An absent answer does not prove the addressee was able or willing to answer.

Following rejection or timeout, the issuer may **withdraw**, leave the matter alone,
or **attempt a native arrest request** if the original target, current authority,
current native reason and actual interaction conditions still permit it. The same
J2 helper owns the single dispatch receipt, native costs, refusal/resistance path and
`send_threshold = decline`. There is no forced execution or imprisonment effect.
The receipt records only an attempted request, never a successful arrest or guilt.

## One authoritative lifecycle

- State and immutable issuer/target/issue date attach to the exact retained personal
  observation, bound to story type/owner/schema, original participant and serial.
  One ultimatum per observation, one issuer-wide thirty-day issue cooldown shared
  by player and AI. Another observation cannot reset this one's state or deadlines.
- The seven-day answer window and fourteen-day total lifetime are written **once at
  issue**. One day-eight callback avoids relying on same-day timer ordering. It only
  marks a still-waiting live record, never overwrites a reply or reschedules itself.
  Reviewing/answering never renews the total lifetime. A late review may leave fewer
  than seven days to escalate. After total expiry no custom arrest can follow here.
- The shared J2 route now honors waiting, closure and expiry, including older/stale
  arrest entries. After rejection/timeout both entry paths mark the same terminal
  ultimatum state before J2's consumed dispatch receipt and native request. There is
  no separate arrest implementation or second attempt from the other button.
- Explicit compliance or withdrawal closes this custom observation's arrest route.
  **Native CK3/AGOT interaction windows remain unchanged** and can still be used
  under their own rules; this demand grants no universal immunity, pardon, suspended
  native legal right or promise to obstruct unrelated justice.
- Free withdrawal remains possible after losing land, freedom, legal reason, means,
  jurisdiction or the fixed lifetime, while the original issuer still lives and the
  retained record exists. Withdrawal changes only this demand and sends its actual
  addressee a notice. Dead targets do not receive it.
- The original observer can reopen the demand from their private justice journal,
  independently of current arrest availability. This restores only the exact stored
  target after original reader/record checks; it issues no demand, cost or request.
  Original owner death ends the existing observation story; no heir inherits guilt,
  gratitude, consent, the threat or an opportunity to execute it.

## Information and AI

The addressee sees only the terms and their own action, not the observer's journal,
source proof or other participants. Recipient answer guards never query the issuer's
private current legal grounds or another record. Effect previews use fixed EN/FR
text and hide internal record changes. Recipient identity is not journal access;
original private reader filters remain unchanged. There is no rumor/proof conversion,
claim of causality, native evidence rewrite or public disclosure of a private dossier.

Existing one-day fresh-observation J2 opportunity lets both human and AI issuers
choose this same action. Receiver choices and issuer escalation/withdrawal use the
same guards/effects for AI and player. Bounded weights use own traits, prestige,
opinion and war burden; they never guarantee compliance or punishment. Only existing
fresh-record opportunities and explicit replies/deadline queue events; no global
character/story scan, recurring reminder or new worldwide index is added. Actual AI,
callback, timing/save behavior, privacy of native UI and performance need engine tests.

Native arrest syntax remains referenced by NATIVE_JUSTICE_ACTION_SOURCE_RECEIPT.json.
This slice reuses original project timed-variable/event/message patterns; it adds
no new target-version API claim and distributes no CK3/AGOT source or assets.

## Verification and readiness

Twenty adversarial source tests cover exact identity, role, authority, native
credibility, spam/replay, expiry, consume-before-cost, explicit reply versus silence,
old entry bypass, shared one-attempt dispatch, free exits, private previews, reader
restoration, player/AI parity and EN/FR coverage. Existing J2/justice tests continue
to protect native reason, hook/diarchy/delay checks, actual target, native refusal,
read-only inspection and separate UI handoff. These are source checks, not a Python
simulation of ultimatum behavior or a CK3 parser.

P4 earns **+2 source points** upon checked integration: development **53/80**,
engine validation **0/20**, total **53/100**. No J3, war or engine criterion is credited.
Next substantive target is N4: a reusable contract model shared by two systems.

## Final campaign — all UNRUN

| Case | Required observation |
|---|---|
| ULT-01 | Eligible original observer issues once from a fresh known-participant arrest opportunity; unrelated actors/records or missing native reason cannot issue. |
| ULT-02 | Actual addressee sees terms, cost and refusal/silence; no private observation text, participants, proof or legal-state side channel appears in previews. |
| ULT-03 | Regret consumes before exactly one 25-prestige debit, including double click/reload/stale windows; it changes no native crime/reason and closes this custom route only. |
| ULT-04 | Explicit rejection is distinct from no reply. Day-eight callback observes expired seven-day window only once, never rewrites compliance/rejection/withdrawal. |
| ULT-05 | Old J2 entries cannot bypass waiting/compliance/withdrawal/expiry. After rejection both arrest entries share one terminal demand and dispatch attempt. |
| ULT-06 | Refusal/silence creates no native reason. Loss of reason, court, direct jurisdiction, freedom, target validity, optional-hook/diarchy eligibility blocks escalation but not withdrawal. |
| ULT-07 | Native arrest actually checks its own costs, acceptance/refusal/resistance and default options; an attempted send must not be reported as custody. |
| ULT-08 | Seven/fourteen/thirty-day limits survive reopening/save-load and multiple observations; no deadline renewal, repeated debit or reminder loop. |
| ULT-09 | Original issuer can read/withdraw after losing land or authority; custodian/parent/heir/stranger cannot read or inherit this demand. Owner death ends the source record. |
| ULT-10 | Withdrawal mid-event and actor/target death, custody or changed authority invalidate stale recipient choices without cost or false admission. |
| ULT-11 | Human/AI and AI↔AI have the same actions/costs; observe compliance, rejection, silence, withdrawal and escalation rather than assuming deterministic outcomes. |
| ULT-12 | Final G4/G5 volume/privacy/save-load and AGOT wars/MegaWars, banking, titles, succession and native secrets/memories regressions remain clean. |
