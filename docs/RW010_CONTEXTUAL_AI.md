# RW-010 / AI3 — contextual political choices

**Original CK3 scripts, static-checked; not engine-tested.** This delivers the
source criterion AI3, not all political AI. AI4 (autonomous war/justice/negotiation
coverage), AI5 (instrumentation/performance) and all engine gates remain open.
No Python gameplay or runtime service is involved.

## Shared decision policy

The current event character evaluates a read-only common cooperation multiplier.
The two existing original-party aliases are used without creating new scopes,
variables, records, timers or callbacks. The known-pair guard requires both distinct
parties and that the decider is one of them; missing/foreign context returns zero.
Opinion is read **from the decider toward the other original party**, never from
the story owner or mediator toward someone else.

| Input | Effect on cooperation weight |
|---|---|
| Decider's opinion of counterpart ≥25 | ×2 |
| Decider's opinion of counterpart ≤−25 | ×0.5 |
| Decider has an outstanding personal gold-service or favor-service promise | ×0.5 once, even if both |
| Decider is at war | ×0.5 |
| Relevant liquid resource below twice this action's cost | ×0.5 |

The first four inputs are centralized in `rw_ai_cooperation_factor` and shared
triggers. Family adapters apply the actual resource reserve and existing eligibility:

- **Negotiation:** `rw_services.accept_50` and `rw_services.promise_50` use
  `rw_ai_service_accept_weight`, base 30, current original-client turn, current
  agreed price/revision, current funds and reserve `2 × scope:rw_service_price`.
  This influences immediate payment or explicit deferred consent; it does not perform
  a promise. Existing 25-gold counteroffers, refusal, shortening and expiry remain.
- **Political affairs:** `rw_cases.apologise` uses `rw_ai_case_repair_weight`, base
  50, current original-provider turn and ≥25 prestige, with reserve 50 prestige.
  This applies to both service disputes and independent admitted/contested allegations.
  The existing ×2 preference for a mediator liked **>25** is retained. Refusal remains base 50.
  The gesture's original 25-prestige cost and later beneficiary consent stay intact;
  an apology is not an admission of native crime or a pardon.

These are weights, not percentages, guaranteed outcomes or measured probabilities.
For example, neutral/unburdened acceptance weighs 30; a trusted counterpart gives
60; funds between the affordable price and twice that price reduce it to 15.
Neutral repair weighs 50, reduced to 25 when 25 ≤ prestige <50. Existing mediator
preference multiplies repair separately. Refusal remains positive, so even strong
cooperation preferences do not compel agreement. Existing obligations count as
commitment risk, not guilt; at war is an additional burden (service eligibility
already excludes war, while a case party can still be at war).

## Boundaries and evidence

Only AI weights change in three existing options; their action triggers and effects
are unchanged. The family adapters recheck the same turn and cost guards. Human and
AI characters retain the same actions, money/prestige costs, consent, rejection,
revision and replay rules. No hidden counterpart promise, secret, plot, undisclosed
case, inherited personal duty, native sanction, title, CB or war state is consulted
or changed. Own opinion, own resources and own commitments are the inputs. The old
bounded targeting/cooldowns are untouched; weights alone do not prove performance.
No claim that every decision in the mod now uses this policy.

Native syntax references were inspected in the already supplied private CK3 source
subset: `AI_POLICY_SOURCE_RECEIPT.json` contains only relative paths, hashes and line
references for named numeric values in AI weight modifiers and script-value arithmetic.
No native code is distributed. Native value evaluation, event-current-character scope,
weight precision and actual AI behavior remain unverified on the target installation.

Available checks: nine adversarial source tests reject removed pair/role/turn/cost
checks, disconnected factors, wrong counterpart opinions, missing family calls,
added effects, global scans and private-information reads. A structural-validator
negative fixture rejects duplicate script-value definitions. These checks do not
execute CK3. The developer utility `tools/report_progress.py` records the source
criterion, never engine credit.

## Final campaign — no cases run

| Case | Reproducible check / expected result |
|---|---|
| AIPOL-01 | Load CK3 target + AGOT + submod; no unknown value/trigger or invalid numeric-weight errors. Confirm existing interactions/events open. |
| AIPOL-02 | Neutral original client, ≥twice quotation in gold, no own commitment, at peace: inspect acceptance weight 30. Raise own opinion of provider to ≥25: 60; lower to ≤−25: 15. Swap player/AI roles and verify original decider/counterpart direction. |
| AIPOL-03 | Keep quotation affordable but drop client gold below twice price: weight halves. Below price, action unavailable and direct effect cannot pay. Confirm latest quote determines reserve, not an old saved amount. |
| AIPOL-04 | Give original client one outstanding gold or favor promise: cooperation halves. Both flags still give only one burden multiplier; ending the own promise removes it. Other party's undisclosed promise changes nothing. |
| AIPOL-05 | Independent admitted and contested allegations: repair at ≥50 prestige gives weight 50 before opinion/commitment/mediator adjustments; at 25 ≤ prestige <50 gives 25; below 25 unavailable and effect cannot spend. It never creates a crime admission. |
| AIPOL-06 | Service-breach repair uses the same policy. Keep decider's opinion of claimant fixed while changing story owner/mediator opinion: only the explicitly retained mediator modifier may affect it. Decider at war halves repair preference; existing jurisdiction still required. |
| AIPOL-07 | Repeat with AI client/provider/claimant and service immediate/deferred modes. Observe both acceptance and refusal/counteroffer; unchanged original 50/25 gold and 25 prestige costs, no automatic fulfillment. |
| AIPOL-08 | Save/reload offered service and invited repair. Resource/opinion/own-promise changes after opening must affect the fresh decision; stale revision, expired case, missing or foreign parties cannot spend or acquire willingness. |
| AIPOL-09 | Missing aliases, same-party aliases, foreign decider: common factor zero; stale UI only existing expiry/cleanup. Read-only evaluation creates no flags, records or timers. |
| AIPOL-10 | Compare scheduler frequency, event volume and performance to baseline during the final G4/G5 run. No new scan/reminder; actual spam/performance remains unproved until measured. Test unrelated AGOT wars, titles, justice and hooks unchanged. |

Source acceptance: two independent action families, shared relation/commitment policy
and relevant resource means (three concrete factors), with war burden additionally.
Baseline **38 → 40/100 (+2 source points)**; engine remains **0/20**.
Next substantive target: **J2**, native individual sanction pipeline, not another AI
weight variant; all final-engine cases remain deferred as requested.
