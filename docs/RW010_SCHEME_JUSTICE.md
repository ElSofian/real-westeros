# Native judicial situation — inspection and native UI handoff

Static-checked only; no CK3 execution. This slice adds an explicit examination
button to a retained exposed-participant observation and a guarded native arrest-window handoff. It does not implement a new
arrest, execution, confiscation, pardon or dynastic penalty.

## Source findings and boundary

The private target-version sources were inspected, not copied. References and
byte hashes are in JUSTICE_SOURCE_RECEIPT.json. AGOT 0.5.2.1 declares support for
CK3 1.19.0.6; the installed executable remains unverified.

- The discovery event's arrest option first applies its native accusation/removal
  consequences, then calls the special rightful-imprisonment effect. The discovery
  callback alone does not establish that this choice was taken.
- `basic_allowed_to_imprison_character_trigger` is expressly a visibility/basic
  relationship check. Its existence is not an authoritative lawful-arrest verdict.
  Advanced checks include current detention, war, ransom and hook conditions.
- `rightfully_imprison_character_effect` explicitly avoids tyranny. It must not be
  used as if it checked legality; calling it independently would bypass the native
  decision path and could repeat a native consequence.
- The normal AGOT `imprison_interaction` has additional visibility/validity rules,
  acceptance handling and refusal/resistance logic. Preserve that interaction.
- `has_imprisonment_reason` is a current character-to-character predicate. It
  neither identifies the particular offense nor proves that its reason concerns
  this observation. Native helpers can consume reasons. Absence is not proof of
  innocence, pardon, or prior punishment; presence is not sufficient for arrest.

No complete per-offense native penalty history or sanction-completion callback was
established by this review. Current detention is not such a history. The mod does
not guess a historical judgment or record one from a snapshot. The private source
collection has an unresolved dependency frontier; this is not an exhaustive engine
API audit. No new collection or manual game run is required for this slice.

## Implemented original CK3 scripts

The observer's journal has a separate **Examine the current judicial situation**
button for a retained participant record. Reading generic scheme discovery cannot
invent a participant. All access reuses the typed, schema/serial/retention-checked,
observer-only reader, and navigation rechecks access before opening the event.
The examination reports independently:

1. The recorded participant is currently free, imprisoned by the observer, or
   imprisoned elsewhere. No other jailer identity or private case is exposed.
2. The observer currently has, or does not have, a native imprisonment reason
   against that exact participant. No reason is attributed to the plot.

Deceased/invalid participants receive a neutral fallback. No heir, hidden
organiser, random participant or relative is substituted. Opening and closing do
not persist a verdict, renew retention or alter evidence, reasons, secrets, titles,
war, opinions, gold or voluntary-response state. There is no new timer, pair scan,
AI privilege or gameplay effect; AI retains the same native justice actions. This
read-only journal interface is manually opened, just like the existing archive.

The values describe the present state when displayed; reopening queries again.
An already visible popup is not a live historical/transactional guarantee. Closing
has no effect. A second, explicitly named option can open the native arrest window
without sending the interaction. Its shared availability/execution guard rechecks
the exact record/participant, living/free status, observer freedom and native
`is_character_interaction_valid` for `imprison_interaction`. It then uses the
source-located `open_interaction_window` effect with observer actor and recorded
participant recipient. It never invokes acceptance, arrest or refusal effects.
No native reason is required by our UI gate: the normal interaction remains
responsible for displaying any tyranny and other terms, rather than confusing a
current reason with authorization. The player can cancel the native window.

Only human observers get this UI shortcut (`is_ai = no`); it does not create an
exclusive gameplay action. AI keeps the same native imprisonment interaction,
conditions and consequences through its existing native selection logic. We do
not fabricate an AI automatic send or claim new evidence-aware arrest weights.
Our mod does not add an AI prison-action scheduler. A refused or paid voluntary request has no effect on
these predicates and is not a pardon.

## Verification and next work

Nine source-contract tests check reader dependencies, wrong/generic/dead identity,
reason direction, custody separation, navigation revalidation, localization and
absence of cached judgments or punitive effects, including negative mutations.
The native handoff is checked for exact actor/recipient, revalidation and no send.
They do not execute CK3 or prove API/scope/description evaluation semantics.
Final JUSTICE-01…08 scenarios remain unrun in FINAL_ENGINE_TESTS.md.

The personal prisoner execution/release handoff is now in RW010_PRISONER_SENTENCING.md;
it preserves native eligibility and does not send or record a completed sentence.
Next inspect native individual confiscation/status removal before house-wide aftermath.
The UI handoff is source-backed but not engine-proven; if its window fails, the
normal character-menu arrest remains available without a replacement arrest
implementation. A genuinely new personal sanction needs attributable facts,
consumption/idempotency and a preserved native consequence path before activation.
No complete per-offense punishment history is inferred. Family/house sanctions and
restoration remain separate G3 work. G1 returns at the war stage. This examination
does not complete RW-010 or the original justice goal.
