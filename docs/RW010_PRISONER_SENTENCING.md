# Personal prisoner sentencing — native interaction handoff

Experimental original CK3 scripts; **not engine-tested**. This slice connects a
retained exposed-participant observation to the actual prisoner's native execution
and release interfaces. It adds no replacement execution or fabricated judgment.

## Personal flow

From the observer's own scheme journal, **Consider this prisoner's personal
sentence** opens only when the exact recorded living participant is currently
imprisoned by the observer and the observer is free. The shared reader chain checks
story type, schema, owner, serial, retention and participant kind. Generic discovery,
a contested allegation, another ruler's prisoner, a hidden organiser or an heir
cannot be substituted. Custody alone is not proof of guilt for this plot.

The panel independently reads the observer's current `has_execute_reason` against
that participant. It never promotes `has_imprisonment_reason` to an execution
reason, infers the reason's offense, or interprets absence as acquittal or pardon.
Reasons and custody are queried on inspection; they are not historical snapshots.

The observer may:

- Inspect the normal execution window, if the exact native interaction is valid.
  That window controls methods, costs, tyranny and other native consequences.
- Inspect the normal release window, if its native interaction is valid. It may
  contain conditions; opening it does not promise an unconditional release/pardon.
- Leave detention unchanged for now. This is a no-effect close: no extra imprisonment,
  `keep_imprisoned` flag, extension, pardon, order, timer or political reward.

Opening either window does **not send** it. The native interaction must still be
confirmed; it can be canceled. Both availability and execution recheck the same
custody/reader and native-validity guards. The opener supplies only the original
observer actor, exact recorded participant recipient and native interaction name;
no execution/release option is preselected by a fabricated scope. Changed custody,
death, an inaccessible record or observer imprisonment makes old panel actions
ineligible. A neutral stale fallback closes without a sentence.

No mod variable records a completed execution, release or acquittal merely from
opening a window. In particular, native execution can include delayed player-facing
follow-ups; click intent is not evidence of completed death. Reopening the journal
queries actual current custody/life. Existing observation retention is unchanged;
this is not a universal sentencing ledger or deduplication of historical offenses.

## Source contracts and preserved behavior

`SENTENCING_SOURCE_RECEIPT.json` gives hashes and relative line references for the
inspected prison interactions in CK3 and AGOT from the received private collection.
The `open_interaction_window` / `is_character_interaction_valid` source references
are already in JUSTICE_SOURCE_RECEIPT.json. No proprietary source text is committed.
AGOT metadata is 0.5.2.1 / supported CK3 1.19.0.6; the actual executable is unverified.

The inspected AGOT execution interaction includes current custody, hooks, ongoing
procedures, faith and landed-knight restrictions, diarchy costs, method-dependent
execution handling and player follow-ups. Its AI selects among actual prisoners
with existing contextual weights. The inspected release interaction includes
ongoing-procedure restrictions and multiple optional terms, including AGOT-specific
terms. These examples are source observations, not an exhaustive engine contract.
We call neither interaction's `on_accept` nor low-level death/release helper and
copy none of their logic. The native window/interaction stays authoritative.

Only human observers receive the UI opener (`is_ai = no`); the same native execution
and release gameplay remains available to AI through its existing selection logic.
This slice adds no evidence-aware AI sentencing policy, automatic send or pair scan.
It does not turn every discovery into an automatic death sentence. The flow also
allows no action; it adds no action cap or new mandatory punishment.

Voluntary contribution, refusal or silence changes neither execution grounds nor
native interaction eligibility. No new criminal reason, immunity, gold transfer,
family penalty, house-wide judgment, title transfer or inherited personal guilt is
created. Native consequences of a subsequently confirmed interaction remain native;
we do not apply them again. Compatibility with native special-interaction windows,
method selection, AI, persistence and other AGOT prison flows still needs CK3.

## Verification and continuation

Twelve source-contract tests include negative custody/actor/participant, stale
click, wrong native action, reason-direction and forced-effect mutations. They also
check absence of cached outcomes, family scans, reminder scheduling and unrelated
service/voluntary-response writes. They do not execute the game. Final
SENTENCE-01…09 scenarios are recorded in FINAL_ENGINE_TESTS.md, all unrun.

Next inspect native individual confiscation and AGOT status-removal options before
introducing house-wide consequences/restoration (G3). Keep personal responsibility,
political family fallout and legal landholding constraints distinct. A universal
50-year title ban must not be claimed from a marker that does not guard all title
acquisition paths. G1 stays planned for the war stage. This integration does not
complete custom coercive justice, dynastic aftermath, RW-010 or the original mod.
