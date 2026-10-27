# RW-007 — political ledger snapshot and obligation receipts

**Scope: offline Python reference model only. CK3 save/load, UI, native effects and AGOT compatibility are NOT engine-tested.**

## Ownership and representation

`tools/rw007_persistence_probe.py` builds on the pure transition functions in `tools/g2_offer_probe.py`. A `PoliticalLedger` is the **single-writer authority** for one current offer revision per ID, accepted-clause obligations and recorded outcomes. It owns only new political bookkeeping, never native war, CB, title, gold or Mega Wars state.

A deterministic JSON **schema_version=1** snapshot contains three collections:

- `offers`: latest version, parties, complete ordered clauses, expiry and pending/accepted/declined/expired status.
- `obligations`: exactly one entry per clause of an accepted offer, keyed by `(offer_id, version, clause_key)`, with outstanding/fulfilled/broken/disputed status.
- `receipts`: stable unique event ID, obligation key and recorded outcome. This is a **record of an observed outcome**, not an instruction to execute an effect.

The complete snapshot is validated **before** replacing the in-memory authority: unknown schema/fields, malformed types, duplicate IDs, duplicate clause keys, missing or forged obligations, inconsistent receipts and nonstandard JSON values are rejected. The loader does not call any game effect. Persisted IDs must remain stable and never be recycled within the saved campaign. JSON is a probe format, **not** a proven CK3 storage mechanism.

## Transition and replay contract

1. Propose/counter/decline/expire reuse G2 validation. A counteroffer supersedes the prior revision. Rejected transitions leave the ledger unchanged.
2. Accept rechecks **all** clause preconditions and records consent plus outstanding obligations; it never performs payment, warfare or other CK3 effects. One failed precondition creates **zero** obligations.
3. `record(event_id, key, outcome)` records an externally observed fulfilled/broken/disputed result. An exact replay of the same event ID is read-only, including after serialization and reload. Reusing an event ID for another outcome, or finalizing an obligation a second time under a new event ID, is rejected.
4. Save after every accepted transition/receipt and reload **before** processing callbacks. Expiry, death, titles, legality and resources must be revalidated in the actual engine.
5. Both AI and player must use the same authority and validation path; no runtime LLM or arbitrary cap on useful clauses.

## Critical unresolved engine boundaries

- **No native atomicity or crash consistency:** if a native CK3 effect occurs and the game crashes before its receipt is durably saved, the Python ledger cannot know the effect already occurred. A future CK3 adapter must define effect ownership and durable pre-effect reservation or equivalent engine-supported guard, then test crashes/reentry. **Never retry a native effect just because a receipt is absent.**
- **No CK3 save format binding:** discover and test actual 1.19.* / AGOT 0.5.2.1 persistent variables, save/load hooks, scopes and serialization limits before porting this model.
- **No concurrency guarantee:** the reference model assumes one writer. Same-tick callbacks and reentrant on_actions need an engine-side ordering/guard strategy.
- **No authenticated snapshots:** loader consistency checks do not protect against malicious or arbitrarily forged state. It assumes trusted campaign data.
- **No fulfillment authority:** `record` takes an externally supplied result. A CK3 adapter must verify event provenance, recipient, clause conditions, and native outcome before recording anything.
- **No universal inheritance:** obligations remain attached to the parties and terms until explicit policy determines what survives succession. Heirs do not automatically inherit personal guilt.

## Verification

Run `python -m unittest discover -s tests -v` and `python tools/validate_mod.py`. The RW-007 probe has 16 synthetic tests, including negative paths for stale responses after reload, duplicate effects receipts, corrupt snapshots, and failed multi-clause acceptance. These are **static/offline tests**, not evidence of working CK3 persistence.

**Next:** RW-008 should select a bounded political incident and identify its real CK3 storage/UI hooks, while keeping all engine-dependent behavior explicitly unverified until tested.
