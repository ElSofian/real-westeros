# G2 feasibility — multi-clause political negotiation

**Assessment date: 2026-10-26. Protocol: STATIC-CHECKED (synthetic Python only).**
**CK3 UI, persistence and native-effect execution: UNVERIFIED / NOT ENGINE-TESTED.**
No CK3/AGOT scripts or assets were copied or executed.

## Question

Can two rulers (player or AI) propose **two or more distinct clauses**, inspect a complete offer, accept, refuse or counteroffer **a specific revision**, and later fulfill or break commitments without duplicating CK3/AGOT effects? Promises must not force future performance. Native CK3/AGOT must retain ownership of wars, CBs, titles, hooks, banks and other native state.

## Evidence and uncertainty

| Public reference | Observation | Limit |
|---|---|---|
| [CWTools CK3 interaction schema](https://github.com/cwtools/cwtools-ck3-config/blob/master/config/common/character_interactions.cwt) (revision not pinned) | Defines repeatable send_option blocks, send_options_exclusive, visibility/validity conditions, on_send/on_accept/on_decline, ai_accept. | A static grammar does **not** prove that arbitrary dynamic clauses, selected flags, revisions or persistence work in CK3 1.19/AGOT. |
| [Community interaction guide](https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Interactions_modding.md) (unversioned) | Describes custom character interactions and actor/recipient scopes. | Does not demonstrate an arbitrary multi-clause composer or transactional effects. |
| [Community event guide](https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Event_modding.md) (unversioned) | Describes multiple event options. | Separate choices do not themselves compose a complete agreement. |
| [Community UI guide](https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Interface.md) (unversioned) | Describes scripted GUIs, lists and standalone windows/widgets. | Entry points, effects and AGOT compatibility require in-game validation. |
| [CK3DB Demand Hostage](https://ck3db.com/interactions/demand-hostage) (CK3 1.20.1.2) | An existing acceptance interaction with selectable option and lifecycle hooks. | Different game version, not a generic negotiation system. |
| Target CK3 1.19.* / AGOT 0.5.2.1 installation | Not accessible in this run. | No pinned script inspection or CK3 runtime test. |

These are **leads**, not evidence of a functioning G2 mod.

## UI alternatives and decision

| Route | Benefit | Risk | Decision |
|---|---|---|---|
| Additive character interaction with nonexclusive send_option flags | Native diplomatic entry point, possible small multi-clause selector, AI hooks | Finite authored flags; verify selection survives reply and can be associated with a revision | **First in-engine UI spike candidate** (two clause types) |
| Character interaction + event-chain composer | Native multiple options, avoids replacing main GUI | Many screens for larger agreements; scopes and persistence need verification | **Fallback** for first vertical slice |
| Standalone additive scripted GUI composer | Long-term expandable clause lists and offer summary | Dynamic data/effects and opening entry point need testing; compatibility cost | **Long-term candidate**, not yet proven |
| Override vanilla/AGOT diplomacy GUI | Can replace existing panels | High mod conflict risk | **Rejected by default** |
| Pre-authored buttons for every combination | Easy small demos | Combinatorial explosion and no genuine negotiation freedom | **Rejected as final design** |

**Decision:** implement a UI-agnostic **versioned offer protocol** first. Investigate a new additive character interaction with two nonexclusive send_option flags and a complete reply summary; fall back to an event sequence if the flags cannot reliably represent an offer. A standalone GUI remains the candidate for extensible composition. Neither UI path has passed the target engine gate. This is **not** an arbitrary cap on future useful actions or clauses.

## Protocol contract (not CK3 script)

A negotiation has a stable offer ID, one authoritative **current revision**, two parties, expiry, and an ordered collection of uniquely identified clauses. Clause type and payload are extensible; native effect adapters and their legality checks are separate.

1. **Propose:** create revision 1 with at least two clauses for this proof; present the **whole** offer.
2. **Counteroffer:** only the current recipient can replace the entire clause set; increment the revision and reverse proposer/recipient. The prior revision becomes stale.
3. **Accept:** only the current recipient may accept the current unexpired revision. Recheck **all** clause preconditions first; if one fails, record **no consent**.
4. **Decline / expire:** terminal; no future effects from that offer.
5. **Idempotency:** reject duplicate IDs, repeated acceptance and stale revisions. A current-revision authority is mandatory, including after reload.
6. **AI parity:** AI and player use the **same** protocol, costs, restrictions and execution. AI selects actions, but cannot bypass validation.
7. **Native-effect boundary:** accepted means **consent**, not that a multi-effect CK3 transaction was atomically executed. Never assume rollback. Track individual obligations and performance separately; failed performance may become outstanding, broken or disputed, rather than silently completed.
8. **Revalidation:** check parties, claims, titles, gold, laws and relevant targets at response and performance time. Do not automatically transfer personal guilt or promises to heirs.

### State transitions

pending(v1) -> pending(v2) (counteroffer), accepted, declined or expired. Later counters yield pending(v+1). Accepted records consent only. Performance/breach states belong to separate obligations. Terminal offers cannot return to pending.

### Example

Lord A offers Lord B: (1) a conditional promise of military assistance; (2) immediate payment of 100 gold. B counters with 60 gold, producing revision 2. A cannot accept revision 1. Before accepting revision 2, both prerequisites are checked. If payment is impossible, **the consent attempt fails in full**. If consent succeeds, any gold transfer and later assistance are still separately validated and tracked; later bankruptcy or war can cause breach without retroactively changing the offer.

## Offline protocol proof

- tools/g2_offer_probe.py: immutable offer transitions and a **single-threaded in-memory current-revision authority** (OfferBook). Executes **zero** CK3 effects.
- tests/test_g2_offer_probe.py: **18** positive/negative tests: two-clause consent, counteroffer, stale revision, wrong recipient, failed/missing precondition, duplicate response/ID/clauses, expiry, terminal decline, invalid parties.
- Run: python -m unittest discover -s tests -v ; python tools/validate_mod.py

**Limit:** a detached old Offer object can still be inspected and manipulated by pure functions; only OfferBook consults the latest authoritative revision. OfferBook is volatile, single-threaded, and **not** CK3 persistence, concurrency control or an engine-side transaction. RW-007 must design real save/reload state and idempotent reentrant callbacks. Do not port the Python code into CK3 as if it were a validated game API.

## In-engine G2 gate

1. Inspect actual target _character_interactions.info, native examples and AGOT overrides. Verify multiple send_option selections persist from send to response, and can be bound to one versioned offer.
2. Demonstrate a player can review **all** clauses together before acceptance, and an AI can produce/receive the same offer without UI shortcuts.
3. Verify actor/recipient scopes, offer IDs and revisions across **save/reload**; stale offers must remain rejected.
4. Change one of two prerequisites while a response is pending (gold spent, death, title change, war). No partial **consent**, and no duplicate native effects.
5. Test refusal, expiry, repeated callbacks, same-tick responses, counteroffers, invalid recipients and AGOT compatibility.
6. If interaction UI cannot represent the offer, test event-chain fallback. If both fail, mark G2 UI **BLOCKED**, and separately assess additive scripted GUI.

## Verdict

**RW-006 research deliverable complete:** a plausible UI route, explicit alternatives and limits, and a statically verified *non-runtime* protocol. **G2 gameplay remains UNVERIFIED**: no playable negotiations, no tested save/load and no proven atomic native transaction. RW-007 may independently design persistence, but cannot claim engine behavior without a CK3 run.
