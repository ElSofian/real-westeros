# RW-009 — bounded AI reconciliation

**Experimental source integration; not engine-tested.** AI scheduling keywords,
frequency units, target expansion and scopes must be verified in the actual CK3 build.

The first policy considers only the actor's direct liege. This bounds target search
without scanning all character pairs. Both parties must still satisfy RW-008's common
living/adult/landed/peace requirements. Pending and yearly cooldown exclusions apply
to humans and AI alike. AI willingness is zero when its opinion of the recipient is
nonnegative, otherwise base 10. `ai_frequency = 12` is a provisional scheduler setting,
not a measured rate. The annual character flag is the actual scripted spam guard.
AI recipients retain the same accept/refuse consequences as human recipients.

Static tests detect mutations that remove shared eligibility, remove either exclusion,
or broaden the target selector. These are source-contract checks only. They do not
prove the game honors the syntax or predicates and are not an AI gameplay simulation.

## Engine acceptance scenarios (not run)

- With a landed adult AI vassal and a living adult landed liege at peace, establish a
  negative opinion and observe AI initiation with debug logs; record elapsed game time.
- With nonnegative opinion, no petition should be selected by this AI policy. With
  cooldown, pending petition, death, minority, unlanded status or war, no initiation
  should occur. Run each case from an independent save.
- An independent ruler has no liege target. AI must not fall back to a global search.
- Force acceptance and refusal in separate saves; compare opinion effects to a human
  using the same interaction. Verify save/reload retains pending state and cooldown.
- Profile a representative AGOT save before and after enabling the mod. Record
  actor counts, petitions/year, game speed and logs before claiming performance.

RW-010 remains an open-ended expansion task; engine feedback on this first slice
should guide further content rather than adding unvalidated global systems.
