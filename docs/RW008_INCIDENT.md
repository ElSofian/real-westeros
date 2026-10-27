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
in the overall mod. A 30-day pending flag, character-valued target variable and monotonic revision
identify the outstanding petition. The event snapshots the revision; an old response
cannot match a later petition to the same target. Effects recheck both parties and target identity,
then consume the pending marker before adding opinions. Expired/invalid responses
have a dismissal option and no opinion effect. An identity-checked dismissal clears obsolete target/pending state. Without dismissal,
an expired target is inert and overwritten on the next petition. The revision is never
cleared, preventing identity reuse. No global hooks,
AGOT overrides, runtime LLM or offline-ledger bridge are introduced. RW-007 informs
the consume-before-consequence design; its JSON is not used by CK3.

AI recipients have accept/refuse weights. RW-009 adds AI initiation toward the direct
liege when the actor has a negative opinion. AI and players share validity, cooldown
and consequences. This is a deliberately bounded initial AI policy; runtime scheduling,
performance and compatibility remain unverified. See `RW009_AI.md`.

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

Static audit update: initiation now revalidates parties inside the execution effect. Response validity rechecks landed status too. Explicit saved recipient scope replaces implicit ROOT in opinion targets. Source-contract mutation tests protect revision/recipient guards and identity-checked dismissal; they do not execute engine transitions. Add stale-response-after-new-petition to the final CK3 test campaign.
