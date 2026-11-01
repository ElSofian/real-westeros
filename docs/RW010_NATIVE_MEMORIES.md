# M4 — native CK3 political memories

**Original experimental CK3 scripts; static-checked, not engine-tested.**
This integrates relevant public acts into CK3's character-memory framework instead
of implementing another custom story journal. It does not replace existing receipts,
private case history or institutional records. It does not implement M5, the separate
criterion for memory influencing future independent political decisions.

## Implemented public acts

1. **Delivered public support.** After actual immediate or deferred endorsement
   performance, the original provider can remember speaking publicly for the client;
   the original client can remember receiving that support. All four gold/favor,
   immediate/deferred fulfillment paths call the same projection after consumption
   and the existing prestige effect. Proposal, counteroffer, promise acceptance,
   refusal, expiry, renunciation and archive reads emit no support memory.
2. **Explicit Crown recognition.** Only a current ruler's deliberate recognition of
   an already accepted institutional charter can emit a memory. Existing story,
   revision, current roles and active phase must still match after recognition;
   named recognizer and recognition date must match the current actor and date.
   The counterpart is the actual house representative at that act. Succession,
   storage migration, fresh proposal, head acceptance, mere reading and old legacy
   records do not themselves imply recognition or create a memory.

The three original types have a native participant named `counterpart`, first/second/
third-person descriptions in EN/FR and a five-year native duration. The default
native icon is referenced by name; no game texture is copied. Native ownership,
biography/death display, memory expiry and the actual UI remain engine responsibilities.
No successor receives another character's consent or personal guilt from this code.

These types deliberately contain only a public act and the actual named counterpart.
Native memories can have third-person readers, so they contain **no private price,
favor, currency, deadline, contract mode, accusation, plot participant, legal verdict,
case/story pointer, exact land entry or title**. A Crown recognition memory describes
an explicit public undertaking, not fulfilled restitution, immunity or a completed
native sanction. A support memory describes public speech, not payment or a hook.
Existing private information remains in its original guarded records.

## Bounded retention and idempotency

A successful contract consumes its existing identity before performance and memory;
its stale replay cannot enter the guarded effect again. Crown recognition advances
its existing revision before projection. Each personal role/kind is coalesced once
per 365 days using a character flag consumed before memory creation. This limits
memoir noise, not gameplay: further services and recognitions keep their normal
costs/effects and remain available during the flag. A later distinct act may create
a new memory after the window; old acts are never reconstructed from history.

No timer/event, owned-story enumeration, global scan, archive rebuild or inherited
memory index is added. The existing native facts, amounts, hooks, charter deadline,
retention, AI/player prerequisites and consequences are unchanged. There is no new
opinion/reputation bonus or sanction. Ordered script effects are not a crash-safe
transaction: memory failure must not retry a financial or native effect.

## Source confidence and available checks

The received AGOT effects demonstrate `create_character_memory` with named
participants. Public RICE/Princes of Darkness examples establish the type-definition,
three-perspective, duration, participant-localization and default-icon conventions.
`NATIVE_MEMORY_SOURCE_RECEIPT.json` pins relative references/hashes and public commits;
only original Real Westeros code is shipped. Public examples are format references,
not evidence of compatibility with the target CK3 1.19.* / AGOT 0.5.2.1 installation.
No CK3 executable, memory UI or texture has been run/verified.

Eight adversarial source tests check original live/distinct parties, all performance
call sites/order, exact roles/fresh recognition, no passive/backfilled projection,
bounded role flags/retention, public localization and absence of extra gameplay
changes/scans/AI exceptions. Structural checks now reject duplicate native memory
types and the archive allowlist includes only original `rw_*.txt` memory definitions.
These tests execute no CK3 memory engine. Python is only development tooling.

M4 source credit: **43 → 45/100 (+2)**, engine **0/20**. Frozen weights/criteria and
previous checkpoints are retained. W1/W2 receive **+0**: the G1 shared-helper/cancel/AI
uncertainties remain unresolved until final engine observations; no production war
bypass or fake CB is introduced. The next independent target is O4, explicit patrimonial/
dynastic undertakings, followed by I3. M5 remains open rather than counting this UI
integration as a complete political-memory system.

## Final campaign — no cases executed

| Case | Check / expected result |
|---|---|
| NMEM-01 | Load target CK3/AGOT; no unknown memory types/fields, missing `_default.dds` or invalid participant/localization errors. Check actual native memory UI. |
| NMEM-02 | Deliver immediate 50/25 gold and favor/gold-counter support: original giver/receiver receive their corresponding memories only after performance. Normal costs/prestige/hooks unchanged. |
| NMEM-03 | Deferred gold and favor paths: no memory on consent, waiting, expiry, release or renunciation; one projection only on deliberate valid performance. Stale/duplicate fulfillment cannot add another memory or payment. |
| NMEM-04 | Repeat valid support within 365 days, with same/different counterparts: memoir coalescing does not block any service effect or alter first remembered counterpart. Actual later performance after the window can create a new memory. |
| NMEM-05 | Successor ruler explicitly recognizes an active Crown charter: native memory belongs to that actual ruler and names the current actual representative. No memory from proposal, head acceptance, succession, migration, review or stale recognition. |
| NMEM-06 | Change ruler/head/charter revision before a popup responds; stale action cannot project a memory. After a genuine recognition, later succession must not rewrite the old memory participant or copy consent/guilt to an heir. |
| NMEM-07 | First/second/third-person memory views, including other-character and dead-character biographies: show only public act/counterpart. No negotiated gold, favor, deadline, private case/title entry or verdict is exposed. |
| NMEM-08 | Save/reload before/after performance and recognition, during suppression and after five years: memory ownership, roles, retention and reference display remain native and correct; no financial effect is retried. |
| NMEM-09 | Human and AI providers, clients and rulers share effects/flags; no privilege or additional proposal loop. Invalid/dead/self parties cannot produce a new support memory. |
| NMEM-10 | Measure final G4 memory volume/performance and G5 regressions. Existing AGOT memories, house relations, banking, contracts, titles, justice and war flows keep their normal behavior. No compatibility/performance claim before those runs. |
