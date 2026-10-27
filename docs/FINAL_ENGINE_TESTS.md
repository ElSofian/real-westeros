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

## Mutual release of a deferred endorsement (RW-010)

No cases executed. See RW010_MUTUAL_CANCELLATION.md.

1. Provider asks/client accepts, then client offers/provider accepts: verify explicit
   consent, distinct mutual-release receipt, no gold/prestige/opinion/service/breach.
2. Reject or ignore until request expiry: obligation remains, no penalty or deadline
   extension. War/poverty do not block consenting to a neutral release; dead/minor/
   unlanded parties and an overdue promise cannot authorize it.
3. Fulfill or break while a request is pending. Old acceptance/rejection, weekly
   reminders and deadline callbacks must not undo that outcome, duplicate effects
   or erase its breach receipt. Test both action orders on the same day.
4. Old request expires; make a new request after the seven-day cooldown. Replay the
   old response with identical parties/contract: no effect on the newer request.
5. Change provider/client/serial/revision/price/mode in a stale test context: no
   cancellation or cleanup of another obligation; no immediate-mode cancellation.
6. At original day-thirty-one expiry the normal funded/eligible accountability
   still applies even if cancellation was requested at the last moment.
7. AI client gets the initial opportunity; AI provider can propose in a due event,
   then still revisits weekly after rejection/silence. Compare player costs/guards.
8. Save/reload before/after requests and decisions, provider/client death, lost
   land, old experimental saves, and later receipt replacement. Notices must never
   claim release for a different receipt; independent case evidence stays intact.

## Integrated distribution installation (all runtime checks deferred)

1. Download the GitHub artifact, extract the outer wrapper, verify the inner ZIP
   against its `.sha256`, and record MANIFEST.json commit/version/target metadata.
2. Copy both items from the inner ZIP's `mod/` directory to the actual CK3 user-data
   `mod/` folder; enable Real Westeros after AGOT. Confirm launcher and parser logs.
3. Use the feature table in INTEGRATED_BUILD.md as entry-point inventory for the
   final campaign. Record observed EN/FR text, script errors and interactions.
4. Update by replacing the old submod folder, not by merging obsolete scripts.
   Check a disposable fresh save separately from older experimental-save migration.
   ZIP/manifest/CI success does not count as passing any CK3 scenario.

## Integrated lifecycle audit: provider decisions (LIFE-01 to LIFE-07)

All unrun. See INTEGRATION_AUDIT.md for source findings and evidence to capture.

- LIFE-01: accept deferred terms, observe one due decision at day eight. Wait once:
  one live decision seven days later, no automatic payment/breach or renewed deadline.
- LIFE-02: open review A, then review B of the same promise. Try every action on A:
  no fulfillment, refusal, cancellation request or additional weekly chain. B remains
  usable; choosing wait in B schedules one current reminder.
- LIFE-03: wait, manually review before its timer fires, wait again. Old hidden timer
  must not display another actionable decision or consume the new pending ticket.
  Repeat within the original deadline; measure popup count and event behavior.
- LIFE-04: propose cancellation from a provider decision, then accept/refuse/ignore
  on the other party. A repeated/stale provider popup cannot create another request
  or reminder chain. Separate explicit consent remains valid after provider review.
- LIFE-05: fulfill, break or mutually release while a reminder is queued. Its hidden
  callback must not display a new decision or affect later contracts/receipts/cases.
- LIFE-06: ignore all decisions, or repeatedly review without acting: original expiry
  remains accountable under the existing eligibility/funding rules at day thirty-one.
  Test same-day review/reminder/delivery/consent orderings and reload each state.
- LIFE-07: older experimental obligation with no decision serial/open marker:
  stale events permit only neutral dismissal; manual review can allocate a new
  decision without restarting dates. Original expiry still works. Also test actor
  death, land/realm changes and scope loss; do not assume migration succeeds.
