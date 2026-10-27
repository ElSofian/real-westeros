# RW-008 — an offered olive branch

**Experimental; static-checked only, not engine-tested.** This is original CK3 script,
not a Python gameplay simulation. CK3 scope propagation, UI, variable persistence and
AGOT compatibility still require runtime validation against actual installed versions.

## Slice

A landed adult at peace can ask another landed adult at peace for reconciliation.
The interaction delivers an event; `auto_accept` delivers the petition, not consent
to reconciliation. The recipient chooses acceptance or refusal. Acceptance adds
mutual +10 opinion for two years; refusal adds -5 opinion from petitioner to recipient
for one year. No title, oath, debt, war, imprisonment or native secret is transferred.
French and English localization are supplied. The interaction category is diplomacy.

One actor-side yearly cooldown bounds spam, not the number of useful interactions
in the overall mod. A 30-day pending flag plus character-valued target variable
identifies the outstanding petition. Effects recheck both parties and target identity,
then consume the pending marker before adding opinions. Expired/invalid responses
have a dismissal option and no opinion effect. A stale target variable is inert after
the flag expires and is overwritten on the next eligible petition. No global hooks,
AGOT overrides, runtime LLM or offline-ledger bridge are introduced. RW-007 informs
the consume-before-consequence design; its JSON is not used by CK3.

AI recipients have accept/refuse weights. AI initiation is deliberately disabled
until RW-009 adds bounded target selection; this slice is experimental and does not
yet meet full AI/player initiation parity. Both choices share the same effects for
human and AI recipients. No performance or compatibility claim is made.

## Verification

Run `python3 -m unittest discover -s tests -v` and `python3 tools/validate_mod.py`.
Integration fixtures detect broken event braces, colliding trigger definitions and
colliding translations. Translation coverage checks both languages. These checks do
not execute CK3 triggers/effects or prove replay guards work in the engine.

## Future reproducible engine checks (none executed)

1. Record CK3 executable, DLC, AGOT version and playset order; enable debug mode.
   Install following INSTALL.md; inspect error.log for the new script identifiers.
2. Use two living landed adults at peace. Send the diplomacy petition from A to B.
   Confirm B receives the event and the names/localization resolve in both languages.
3. Accept: inspect mutual +10 opinions and two-year duration. Attempt a second
   petition immediately; cooldown must prevent it. Repeat in a fresh save and refuse:
   only A's opinion of B should decrease by 5 for one year.
4. Save with B's event open, reload, then respond. No scope/target loss or duplicate
   opinions should occur. Replay the response/event via debug tooling: consumed
   petitions must have no additional consequence. Check AI recipient choices too.
5. Before response kill A, unland a party, start a war, or wait over 30 days.
   Only dismissal should remain, with no new opinion modifier. Verify minors,
   self-targeting and cooldown actors cannot initiate. Test each case in a fresh save.
6. Advance one year: a new eligible petition must work. Check death/succession does
   not impose personal guilt or carry a usable petition to an heir. Run a baseline
   AGOT war/Mega War separately and compare logs; no lifecycle change is intended.

A failure is a script defect to fix, never evidence to bypass native war mechanics.
