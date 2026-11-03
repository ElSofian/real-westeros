# Native reasoned or arbitrary sentences — J3

**Static-checked only; not engine-tested.** The original observer of a known exposed
participant may now explicitly attempt a native execution of that exact adult
prisoner in their own custody, with or without a currently recognized execution
reason. Refusal to act always remains available. No new native crime, forged
reason, direct death effect or custom penalty is introduced.

## Why this uses sentencing, not an arbitrary-arrest bypass

The supplied AGOT prison interaction has an AI-specific arrest `can_send` condition:
without an imprisonment reason it requires struggle involvement. This slice does
**not** bypass that rule or pretend arbitrary arrest is generally available to AI.
J2's conservative reasoned arrest and P4's positive-reason ultimatum remain unchanged.

The same source defines native prisoner execution without that reason-based send
restriction, and an existing native event dispatches it without explicit method
flags. J3 uses this executable path rather than adding another human-only window.
It sends the interaction under fresh validity checks with `send_threshold = decline`,
not a forced `execute_threshold`. Default method, native-player response/delay,
acceptance and actual outcome are still engine-unverified. Full method selection
remains in the existing unchanged native UI shortcut.

## Current native grounds, frozen confirmation, historical receipt

Opening the new confirmation captures the exact known participant and whether
`has_execute_reason` is currently true for the actual observer. Two mutually
exclusive buttons share the same execution effect:

- **Recognized grounds:** current native execution reason is still present.
- **No recognized grounds:** no current native execution reason is present; the
  character deliberately accepts the possibility of an arbitrary act's consequences.

Both require the captured basis to match **again at dispatch**. If reason, target,
custody or eligibility changes, the old confirmation cannot silently become the other
choice. A fresh explicit navigation is required. An arrest reason is never promoted
to an execution reason; a political accusation/rumor is never native legal grounds.
A native execution reason can concern another offense, not the observed plot.
These labels describe the recognized basis, not a universal legal oracle: native
exemptions, kinship, faith, costs and political consequences remain authoritative.

Before the one native call, the original personal record stores schema, actual
actor/target, basis, attempt date and pair lock. The receipt records an **attempt**,
not guilt, death, completed execution or causality of a later death. Its read-only
view uses the stored basis, never today's possibly consumed reason or changed
custody. Older data without this typed receipt is not retrospectively classified.
Only the original private observer can read it; owner death still ends the record.

## Shared guards and native consequence ownership

The same eligibility and effects apply to human and AI. The first source slice is
conservative: living adult original observer, landed and free, at peace and without
active diarchy; actual living adult participant in that observer's own custody;
current native interaction validity; no target strong hook on the observer; no
native keep-imprisoned or prison-break-contract protection. The peace/protection
guards preserve relevant native AI restrictions for both kinds of actor. Native
faith, landed-knight, struggle, torture/purge and other validity rules remain native.

Both choices consume one shared receipt before one `run_interaction` call. The
native interaction and its original execution helper own stress, tyranny, dread,
opinion, reason consumption, death, title succession, player reaction and other
consequences. The submod adds **none** of those penalties or rewards a second time,
never suppresses them and never calls a replacement death/helper effect. A reasoned
act need not be free of all native costs; an unrecognized basis does not invent a
fixed tyranny amount or override native exemptions.

A ten-day actor/target lock checks only the actual observer's own known observation
stories, so switching between records or the two basis choices cannot immediately
repeat a native request for the same pair. It does not block other prisoners or an
arrest as though it were the same action. Native interfaces, other mods and unrelated
requests are not globally intercepted; this is no universal native-action audit.

The original five-year private **reader deadline is unchanged**. If it expires while
a pair lock remains live, the now unreadable source is kept inert until that lock
expires and normal local sixty-day cleanup can end it. Retention dates are never
renewed. Owner death still ends the source; no lock, evidence or consent is inherited.

## Bounded AI opportunities and navigation

A fresh participant record schedules one next-day inspection. In addition, its
existing local sixty-day story maintenance can notice actual eligible own custody
later. Each retained record offers at most one automatic decision, marking that
notice before opening the event; neither callback executes a sentence. No world
character/pair scan, new global index or repeated reminder chain is introduced.

The actual decision weights use own traits and opinion, with arbitrary sentencing
much less likely by default and forgiving/compassionate actors strongly less likely
to choose it. These are discretionary choices, not deterministic punishments or a
new comprehensive AI policy. Pair lookups and actual AI volume/performance must be
measured in the final campaign.

Existing personal journal/sentencing entries open a confirmation or a read-only
receipt only. Their native execution/release windows remain unchanged. Historical
inspection neither sends a request, renews a cooldown nor reevaluates guilt.

## Source evidence, available checks and readiness

NATIVE_SENTENCE_SOURCE_RECEIPT.json contains only paths/line references/SHA-256 for
the supplied native prison interaction, default dispatch example and owned execution
helper. No native source/assets are distributed. Twenty adversarial source tests
cover current custody/authority/protections, captured target and basis, stale changes,
shared dispatch, consume-before-call, cross-record pair lock, inert-source cleanup,
historical-versus-current grounds, callback/reader isolation, no native penalty
copies, nonintervention, private EN/FR navigation and unchanged arrest restrictions.
They inspect scripts; they neither simulate executions nor establish engine behavior.

J3 earns **+3 development points**: development **60/80**, validation in CK3 **0/20**,
total **60/100**. J4/J5 remain dependent on unresolved G3 routes; AI4 includes the
unresolved war path. Next independent target is **AI5**, actual decision/abuse/
performance instrumentation ready for the final campaign, while G1/G3 stay open.

## Final campaign — all UNRUN

| Case | Required observation |
|---|---|
| SENT-01 | Exact native default interaction dispatch, method and context resolve correctly; no forced acceptance or direct death helper replaces the native path. |
| SENT-02 | Same own-custody adult subject with and without current execution reason exposes the correct explicit choice; original offense and plot knowledge remain distinct. |
| SENT-03 | Reason gained/lost after opening, wrong record/serial/target, custody transfer/escape, death and stale windows prevent dispatch without silently reclassifying the choice. |
| SENT-04 | Native validity still blocks faith/knight/strong-hook/torture/purge/struggle restrictions; peace, diarchy and protected prisoners have the same custom guards for human/AI. |
| SENT-05 | Both choices write one actual actor/target/basis/date receipt before one native request; repeated clicks, another known record and save/reload respect pair and per-record locks. |
| SENT-06 | Native tyranny/stress/dread/opinion, reason consumption and succession occur only through native effects; verify values against an otherwise identical native-window action. |
| SENT-07 | AI→player native reaction, delay, alternatives and possible noncompletion survive; a dispatch receipt never becomes an assertion of execution or cause of later death. |
| SENT-08 | Current reasons consumed/changed after dispatch do not rewrite the historical basis; unknown/legacy/corrupt receipts do not receive invented classifications. |
| SENT-09 | Fresh intake and later local custody give one explicit opportunity; no free-person execution, automatic sentence, repeated notification or global target scan. |
| SENT-10 | Only original observer reads the receipt after losing office or prisoner custody; liege/heir/other observer gains no private journal or personal guilt. |
| SENT-11 | Pair-window expiry, source reader expiry/inert storage, owner death and cleanup behave correctly without renewing original retention or losing an active dedup lock. |
| SENT-12 | Legal/arbitrary/nonintervention are actually possible for human/AI and AI↔AI; final G4/G5 measures local lookup/event volume and AGOT war, bank, secret, title and succession regression. |
