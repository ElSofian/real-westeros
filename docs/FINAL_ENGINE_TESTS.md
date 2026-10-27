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

## Native murder-scheme observations (SCHEME-01 to SCHEME-10)

All unrun. See RW010_SCHEME_EVIDENCE.md and the source hash receipt.

- SCHEME-01: with AGOT alone, record ordinary scheme discovery/agent exposure,
  native events, guardian/host protection effects, native penalties and cleanup.
  With Real Westeros after AGOT, verify both source-backed callbacks are extended,
  not replaced, and existing behavior remains. Inspect parser/error logs and ordering.
- SCHEME-02: exposed murder plot against a living adult landed ruler in their own
  court: one scheme-discovered record, no organiser/agent identity or extra sanction.
  A hidden plot, other scheme type, courtier/minor or target away from own host must
  not be captured by this narrow slice.
- SCHEME-03: expose one actual participant through the native path: record exactly
  that person, not the hidden organiser or other agents. Verify that the native
  exposed predicate is already true in the callback; fail closed if it is not.
- SCHEME-04: repeated same callback produces no second record/notice while retained.
  A second plot against the same ruler, a different participant, or generic discovery
  vs participant exposure must remain distinct. Test same-day callback orderings.
- SCHEME-05: a false/contested affront allegation, murder secret exposure without a
  scheme callback, or copied wrong-scheme agent scope cannot create a native evidence
  record. Native agent removal and imprisonment choices still work independently.
- SCHEME-06: browse own journal through the interaction from a character menu.
  The selected recipient gets no access/notice; lieges, relatives, scheme owner and
  unexposed agents cannot browse the target's records. Check stored participant
  name resolution, serial/type guards, missing schema and unavailable identities.
- SCHEME-07: end/abort the scheme or kill the exposed participant: retained facts
  remain readable without following a destroyed scheme pointer or substituting a
  hidden owner/heir. No active status or current guilt is invented by historical text.
- SCHEME-08: save/reload after each callback, several same-owner records, notifications
  and archive enumeration. Record notice count, iteration scopes and AI/player parity.
  Discovery intake has no additional AI political choice, cost or periodic pair scan.
- SCHEME-09: five-year retention, up to 60-day passive cleanup, observer death and
  succession: no personal guilt/knowledge inheritance. Repeated discovery near expiry
  does not bypass retention semantics or alter service receipts/other case evidence.
- SCHEME-10: older save has no automatic historical backfill; future callbacks may
  initialize new records. Compare load order/DLC, native crime/secret/opinion/title
  state, performance and error logs before making any compatibility claim.

## Voluntary political scheme response (RESPONSE-01 to RESPONSE-10)

All unrun. See RW010_SCHEME_RESPONSE.md; these add no criminal immunity.

- RESPONSE-01: new exposed-participant record initializes one 30-day window and one
  day-one target opportunity. Generic discovery, allegations and old records without
  metadata cannot initialize an offer or infer a participant/consent.
- RESPONSE-02: forgo or postpone: no gold, opinion, secret, debt, pardon or new crime.
  Postponing/browsing does not renew deadlines or create recurring reminder chains.
- RESPONSE-03: direct vassal/courtier, both adult/alive/free, target landed/own host:
  target sends a private 25-gold request and participant gets its precise terms.
  Guests, unrelated rulers, indirect vassals and wrong actor/record cannot qualify.
- RESPONSE-04: accept with sufficient funds: debit exactly 25 from participant,
  credit exactly 25 to target, once. Target grants +5 opinion for two years only if
  the identical benefit is absent; repeat independent agreements cannot stack or
  refresh it, and native negative/crime opinions remain. Replay from old/duplicate/reopened popup cannot
  charge again. Below 25, no debit/debt. Native penalties/rights remain separate.
- RESPONSE-05: refusal, contestation or silence: no payment or new penalty. Denial
  appears alongside the original exposed-participant observation without erasing it
  or relabeling it as generic discovery. Payment does not constitute an admission.
- RESPONSE-06: target withdraws before payment, including after losing authority,
  land or freedom. No funds move; old participant payment becomes invalid. Test
  withdrawal/payment in both same-day orders and after reload.
- RESPONSE-07: after request, imprison/kill either party, change liege/court/host,
  lose target land, spend funds, or expire the original window: revalidate before
  any payment. No heir/estate substitution or retroactive window starts.
- RESPONSE-08: target's private archive/history stays private. Participant can reopen
  only explicitly offered current requests addressed to them, not other observations
  or people's records. Verify per-iteration saved scopes with several simultaneous
  requests and cross-record serial substitution.
- RESPONSE-09: both AI and player receive the initial opportunities and one seven-day
  reconsideration if still live. Withdrawal and participant reply use identical
  rules. Closed/expired callbacks are inert; ignoring again schedules no new chain.
- RESPONSE-10: end the native plot, save/reload every phase, test evidence retention
  and observer death. Original observation, service receipts, native crimes/secrets,
  titles and AGOT outcomes remain unchanged except the explicitly accepted gold
  transfer and distinct agreed goodwill.

## Read-only native judicial inspection (JUSTICE-01 to JUSTICE-07)

All unrun; compare the same native states with and without the submod. See
RW010_SCHEME_JUSTICE.md. No arrest is performed by this examination.

- JUSTICE-01: only the observer can open the examination of their retained exposed
  participant; generic discovery, foreign/expired/wrong-schema/serial records and
  participant access cannot leak current legal information or infer an organiser.
- JUSTICE-02: inspect a free participant, observer-held prisoner and other-held
  prisoner. Verify exactly one custody description, no new jailer identity, and
  no arrest/transfer/release or inferred previous penalty.
- JUSTICE-03: with and without a native imprisonment reason, compare the normal
  native interaction. Display grounds in the observer-to-participant direction;
  an unrelated reason must not be attributed to the plot. A reason alone does not
  guarantee native validity, success or lawful execution/confiscation.
- JUSTICE-04: use native discovery choices/arrest/release/consumption before and
  after inspection; reopening reflects current state without reconstructing a
  punishment history or restoring consumed reasons. Native refusal/rebellion and
  AGOT conditions remain unchanged.
- JUSTICE-05: pay/refuse/contest/ignore/withdraw the voluntary request, then inspect:
  no pardon, immunity, reason creation/consumption or changed original observation.
- JUSTICE-06: kill the participant, end the plot, expire the record or kill the
  observer; old popups cannot open an invalid arrest window. No heir substitution.
  Save/reload, verify description concatenation, scope evaluation and privacy.
- JUSTICE-07: browse repeatedly and compare AI/player native actions, retention,
  notifications, logs and performance: no timers, duplicated penalties, private
  disclosures or persistent cached legal judgment.

- JUSTICE-08: for a human observer and an exact living/free recorded participant,
  compare the native arrest interaction validity with the shortcut. Open then cancel:
  no message, imprisonment, penalty or consumed reason. Confirm manually only in a
  disposable test and compare native success/refusal/rebellion/tyranny with baseline.
  Loss of authority, detention or invalidity between popup and click blocks handoff;
  native UI rechecks before actual sending. No reason requirement is fabricated and
  no reason is attributed to this plot. AI still uses its native interaction (same
  gameplay conditions/consequences) rather than a scripted player-window send.

## Personal prisoner sentencing (SENTENCE-01 to SENTENCE-09)

All unrun. See RW010_PRISONER_SENTENCING.md. Use disposable saves for actual
native confirmations and compare with the same AGOT flow without the submod.

- SENTENCE-01: observer-only retained exposed-participant record plus exact current
  native custody gives access. Generic scheme discovery, allegations, foreign/expired/
  wrong-schema/serial records and another prisoner's substitution must not qualify.
- SENTENCE-02: independently vary native arrest and execution reasons, including an
  unrelated offense. Display only current execution grounds in the observer-to-subject
  direction; no offense attribution, guilt, pardon or historical penalty inference.
- SENTENCE-03: native execution validity: test hooks, faith/landed-knight restrictions,
  ongoing procedures and relevant diarchy costs. Shortcut and character-menu behavior
  agree. Native terms, methods, costs and consequences remain authoritative; a missing
  reason is not turned into a custom UI prohibition or a lawful-execution guarantee.
- SENTENCE-04: open execution window and cancel: no message, costs, death, native
  reason consumption or recorded completed sentence. Confirm separately and compare
  native method handling, player-facing follow-ups, tyranny/stress/family opinions,
  death/succession and AGOT cleanup; no second mod penalty or premature result.
- SENTENCE-05: open release and cancel: no release/pardon. Confirm separately with
  available native terms and compare restrictions, follow-ups and consequences.
  No terms are preselected or promised by the mod; no inferred unconditional pardon.
- SENTENCE-06: leave detention unchanged, browse repeatedly, change custody, free/kill
  the subject, imprison/kill the observer or expire the record before clicking an
  old panel. Recheck before either window; stale actions have no penalty/result.
  No permanent keep-imprisoned flag, extra detention, timer or duplicated effect.
- SENTENCE-07: pay/refuse/contest/ignore/withdraw a voluntary political request, then
  inspect: native custody/reasons/eligibility remain independent; no immunity/debt.
- SENTENCE-08: save/reload, several records for the same/different participants,
  delayed native execution follow-ups and observer succession. Preserve exact private
  scope identity; no hidden organiser, relative/heir or completed result is invented.
- SENTENCE-09: compare AI/player native prison actions, costs and conditions, logs
  and performance. Human-only window shortcut adds no exclusive gameplay action;
  AI retains existing native targeting/weights. No custom automatic sentencing or
  discovery-triggered family punishment is claimed.
