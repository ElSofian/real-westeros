# Final CK3 validation campaign

Owner decision: defer engine tests until the integrated candidate is ready. None of
these scenarios has run. Static passes are not game behavior or compatibility proof.
Record CK3 executable, AGOT version, DLC, playset order and commit for every run.

- Reconciliation: use RW008_INCIDENT.md and RW009_AI.md for acceptance/refusal,
  expiry, death, loss of title, war, AI target selection and cooldown cases.
- Reconciliation audit: reopen an old event after a new petition to the same target;
  neither acceptance nor dismissal may consume/affect the new revision. Save/reload
  both revisions and inspect saved recipient/value scope resolution. Run two eligible
  interactions in the same tick to assess execution revalidation.
- G1: use G1_PROBE.md and TEST_PLAN_G1.md at the war-feature stage; it remains todo,
  not a prerequisite for independent negotiation work or an engine success claim.

Keep baseline AGOT saves separate and disposable. Report failures by scenario and
log excerpt rather than treating static or zero-test results as engine validation.

- Negotiated endorsement: execute all seven groups in RW010_SERVICES.md, including 25/50-gold settlement, counter/requote, lost affordability, stale quote and old-contract response, unchanged deadline, save/reload, AI and same-tick attempts. Verify exact gold conservation and one-time prestige. None executed.

- Deferred endorsement: execute all eight case groups in RW010_DEFERRED.md. Verify no prepayment, preserved deferred mode, invalidated negotiation quotes, seven-day lower bound, voluntary fulfillment/refusal/wait, independent thirty-day deadline, optional reaction and receipt replay. Include orphan/dead-party cleanup, old reminders, repeated review and fresh/pre-mode saves. None executed.

- Contextual mediation: execute all seven groups in RW010_CASES.md, including factual refusal versus deadline, no case from cancellation, disclosure/jurisdiction/self-party checks, optional ruler choices, AI context, voluntary prestige cost, unchanged breach, deadline/realm changes and stale callbacks/notices. None executed.

- Independent case records: execute the eight groups in RW010_RECORDS.md. Emphasize two same-provider cases, cross-case stale callback isolation, retained outcomes, per-iteration archive scopes, role-filtered visibility, current authority versus historical knowledge, lost-callback fallback, save/reload, retention/owner death and resource overhead. None executed.

- Non-contractual allegations: execute the eight groups in RW010_ALLEGATIONS.md. Prioritize unanswered/admitted/contested distinction, no silence-to-proof conversion, disclosure-gated mediator archive access, soft response eligibility, evidence unchanged by apology/withdrawal, cross-kind equal serial isolation, read-only statement history and absent legacy metadata. None executed.

## Voluntary reception of conciliatory gestures (RW-010)

No cases executed. See RW010_REPAIR_RESPONSE.md.

1. Service case and admitted/contested allegation: invite a gesture, provider makes
   it once for 25 prestige, mediator gains +5, client gains nothing before choice.
2. Accept: client gains +5 for two years once. Reject: no client opinion change,
   extra sanction, refund or service payment; mediator opinion remains independent.
3. Ignore past 30 days, then choose a stale option: no consent or opinion change.
   The original mediation deadline is unchanged; no-response history is explicit.
4. Execute a stale/duplicate/wrong-client/wrong-kind response while another case
   exists: neither case receives an unintended answer or repeated benefit.
5. Lose common jurisdiction, land or an actor before response; acknowledge only,
   no benefit. Test provider death/story deletion and client death/save reload.
6. Save/reload offered, accepted and rejected records. Check response view for both
   parties and informed mediator, deny outsiders; browsing never responds/renews.
7. Load an older repaired record lacking gesture metadata: no inferred acceptance,
   no new benefit, no migration/reversal of existing old opinion effects.
8. Observe AI accepting/refusing through the same event/effects; ensure an unfunded
   provider cannot make a gesture, retention stays unchanged, and statements,
   native crimes/secrets, titles and service receipts are untouched.
