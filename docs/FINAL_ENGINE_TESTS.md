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

## Individual title/status review (TITLE-01 to TITLE-09)

All unrun. See RW010_TITLE_STATUS.md. Compare disposable-save confirmations with
baseline AGOT; a successful source check is not evidence of title confiscation.

- TITLE-01: exact observer/private retained participant/current custody/free observer
  gates parent navigation and portrait; generic discovery, stale/foreign/wrong-serial
  records, another ruler's prisoner, dead participant and heirs never substitute.
- TITLE-02: independently vary arrest/execution/revocation grounds, including unrelated
  offenses. Current character-level revocation grounds are not attributed to this
  plot, a selected title's legality, innocence, pardon or completed punishment.
- TITLE-03: native knight/squire recognition, stripped-knight trait, ordinary and
  landed-knight contracts, no-liege characters: inspect independent current statuses.
  No automatic offense provenance, noble-status verdict or house landholding ban.
- TITLE-04: landed direct vassal with native-valid revocation: does the generic window
  opener populate the native title picker without a target? Does the validity query
  require one? Record this explicitly; if it fails, retain character-menu fallback,
  not force-send/target selection. Choose/cancel titles: no transfer, cost or result.
- TITLE-05: change authority, contract, hook, revocation laws or title ownership before
  clicking/confirmation. Native protection/title exclusions/selection validity govern;
  no bypass, preselected title, fabricated reason or forced duchy confiscation.
- TITLE-06: confirm a native revocation on a disposable save; compare costs, tyranny,
  reason consumption, acceptance/resistance, claims, vassals, succession and cleanup.
  No second mod transfer/penalty and no completed-result cache from simply browsing.
- TITLE-07: native release terms: inspect/cancel/confirm permitted knighthood or
  lordship removal separately. Compare exact native restrictions, duchy/contract/
  trait/memory/opinion/house consequences. Preserve existing AGOT human-only lordship
  eligibility; do not claim new AI parity or a universal 50-year family land ban.
- TITLE-08: repeat inspection, pay/refuse voluntary contributions, leave unchanged,
  lose custody or expire a record with old popups visible. No immunity, debt, extra
  penalty/timer, renewed retention or invented sanction outcome. Save/reload all phases.
- TITLE-09: native AI targeting/terms, other AGOT prison/title flows, performance/logs
  and observer succession: no new forced scheduler, inherited personal guilt or
  hidden organiser. Native title/status interactions stay authoritative.

## G3 house sanctions/transfer coverage (G3-01 to G3-12)

All unrun. See G3_HOUSE_SANCTIONS.md. The included trace observes transfers only;
collective sanctions and landholding enforcement are not implemented.

- G3-01: baseline AGOT versus base Real Westeros without the separate optional
  diagnostic, then versus explicitly loaded/unmarked diagnostic: same native title transfers,
  lifecycle/war/Mega Wars, logs and performance; no RW_G3 callback logs or gameplay effects.
- G3-02: separately install/enable Real Westeros G3 Diagnostic after AGOT in a
  disposable playset, then debug human tester starts exact selected current house trace for seven days.
  Verify UI category, save/reload and house variable; no second enable refreshes it.
  Stop early or let it expire; no logs when debug is off or the marker is absent.
- G3-03: marked AI and player holders gain/lose titles; verify actual additive native
  dispatch, ROOT character ID, scope:title display name and destination log file.
  Multiple callback labels may describe one transfer. No secret/full-scope dump.
- G3-04: grant a title to a marked member using the normal native path; document
  selection, acceptance and resulting callback(s). A helper or trace does not prove
  a pre-transfer ban. Use TITLE_ROUTE_AUDIT.md to cover ordinary, theocratic and
  co-ruler recipient alternatives where applicable, multi-title selection and
  scripted grants separately; retain all native AGOT eligibility.
- G3-05: partition and single-heir succession with deceased old holders: capture
  title gain/loss/inheritance order, split titles, heirs, claims and native cleanup.
  No title is moved back, no personal guilt transferred or reason created/consumed.
- G3-06: elective succession across applicable types: record eligibility/winner and
  observed callbacks separately from hereditary succession. Resolve active laws and
  file overlays rather than counting comment-only AGOT definitions as active. Cover
  feudal/pirate/magisterial candidate lists where applicable, then the separate Night
  Watch succession effect; a score penalty or feudal filter is not universal exclusion.
  Preserve regional institutions; no guessed election tag or forced succession.
- G3-07: claim/conquest and usurpation separately: capture genuine native war/vassal
  resolution and callback coverage. Usurpation is not a synonym for conquest; do not
  infer all CB coverage or ban enforcement from one callback or one successful war.
- G3-08: AGOT dynastic stability, new cadet branch/house change, new births and same-
  dynasty other houses: only actual currently marked house holders trace. Record when
  native house changes occur relative to callbacks; no automatic marker propagation.
- G3-09: source/engine investigation of a future enforced ban must cover all four
  routes, exact jurisdiction, new members, foreign grants and exceptions. A marker,
  disinherited trait, one blocked interaction or post-transfer reversal is insufficient.
- G3-10: future decree registry: issuing authority dies/loses title, rightful successor,
  competing authority, house extinction/change and multi-generation save/reload. Prove
  intended institutional continuity without inherited personal criminal guilt.
- G3-11: future restoration/expiry: exact decree/authority/house/claimant, original
  fixed term, stale replay, multiple decrees and optional political reversal; do not
  remove unrelated native traits/rights or automatically grant occupied ancestral land.
- G3-12: compare native AGOT dynastic stability, title laws, disinheritance/restoration,
  banking, house relations, regional institutions and performance before declaring G3
  cleared. Trace output is diagnostic evidence only, not completed gameplay validation.

## Political house-affair register (HOUSE-01 to HOUSE-14)

All unrun. See RW010_HOUSE_AFFAIRS.md. This is political disfavor/rehabilitation,
not a prohibition on grants/inheritance/election/conquest or removal of nobility.

- HOUSE-01: generic discovery/allegation/foreign or stale observation, hidden owner,
  wrong source serial, no custody, non-sovereign, wrong jurisdiction/house or below
  50 prestige cannot issue. Confirm exact house/title snapshot and recheck after
  house/crown/custody/funds change before click; no automatic legal judgment.
- HOUSE-02: successful explicit issue registers one fresh typed record, consumes only
  that observation, costs exactly 50 prestige and applies current-head -20 opinion
  for five years once/non-renewing. Failed registration has no cost/filing. Replay
  and two same-tick confirmation popups cannot double-charge or duplicate the affair.
- HOUSE-03: active exact house/authority dedup; distinct authorities and later distinct
  observations create separate records/house serials. No latest-slot overwrite,
  arbitrary cap or accidental cross-record closure; gaps in serials are acceptable.
- HOUSE-04: current house versus house at later issue, cadet change, birth, foreign
  members and another dynasty house: exact stored house identity governs political
  access. No inherited criminal trait, automatic guilt or hidden plot identity leak.
- HOUSE-05: issuer dies while new authority holder is/is not already assigned, dying
  ruler still reports alive or is still house head, and surviving target-house members:
  verify owner-death story scope, explicit exclusion, living storage transfer and
  native lifecycle preservation. Storage custody conveys no power to judge.
- HOUSE-06: authority conquered/granted/usurped, primary title changed, target head
  dies/is replaced, house membership changes or carrier dies later. Role authority is
  computed from the stored title/current head immediately; maintenance rehomes within
  sixty days. Old issuer/custodian/old-head popups cannot decide for successors.
- HOUSE-07: landless later adult head can petition current sovereign, never themselves
  or while at war. Thirty-day request, one-year cooldown and request revision are
  separate from original fifty-year term. Repeat/cross-record/stale popups fail.
- HOUSE-08: head/ruler changes while pending: old addressee/head cannot accept/reply;
  fresh legitimate roles can submit a versioned replacement without restarting the
  decree. Save/reload at each role change and test two request/response orders.
- HOUSE-09: acceptance closes the matching record before +10 ruler opinion of the
  petitioner for two years; same benefit cannot stack or refresh through another
  decree. No native pardon, title grant, disinheritance removal or unrelated closure.
- HOUSE-10: refusal/silence adds no penalty/debt; latest refused/unanswered receipt
  remains readable. Sovereign withdrawal needs no pending petition and gives no
  goodwill. Neither renews original term or clears native/old custom resentment.
- HOUSE-11: exact original fifty-year expiry blocks actions immediately, later passive
  pass marks expired; fifty-year closed retention then prunes index before ending.
  Browsing neither writes/renews terms nor restores consumed native rights.
- HOUSE-12: extinction/vacancy with no surviving custodian retires safely; no dangling
  global story entry, dummy character or assumed cadet restoration. Document limits
  before claiming universal multi-generation continuity or old-save migration.
- HOUSE-13: actor-only register interaction, multiple same-owner records and per-event
  snapshot scopes: original living issuer/current authority/exact-house members only;
  selected unrelated character is not informed. Private scheme pointer/agents/secrets
  and original source facts are not copied or rewritten. No diagnostic add-on needed.
- HOUSE-14: AI/player issue/consider/decline/petition/accept/refuse/withdraw with identical
  prerequisites/costs. Intake gives only two fixed opportunities; current head/new
  ruler opportunities are cached, and overlapping roles receive only one same-pass
  notice without losing a later legitimate role-change opportunity. No annual AI
  retry chain or all-pairs scan. Compare
  native wars, succession, banking/house relations, logs and long-run performance.

### House succession/request hardening (all unrun)

- HOUSE-15: same living head, new sovereign A→B: after the normal sixty-day pass,
  both receive their current opportunity once, not every pass. Head may replace the
  petition despite the former pair's cooldown. New sovereign cannot answer the old
  request. Overlapping head/sovereign gets only one notice and can withdraw, not
  petition themselves. Missing schema-1 cache gives at most one initial reminder.
- HOUSE-16: new holder is a child, captive, dependent ruler or at war with head:
  extra head/ruler-pair reminder is not consumed while unavailable; becoming eligible
  delivers it once. Replace the head during unavailability with the same ruler: the
  former head's cached pair must not consume the new head's later opportunity. Distinguish that from the initial head information notice and
  from annual retries (not implemented). Count notices across save/reload.
- HOUSE-17: pending head imprisoned/changed house/dead/replaced, ruler imprisoned,
  dependent or displaced, or parties at war. Replies fail current guards immediately.
  If observed within the thirty-day window, maintenance marks invalidated, removes
  only the window, increments revision once and preserves term/cooldown/dates.
  A later return to the same roles cannot revive a retired request or waive cooldown.
  A new head/ruler can issue a versioned replacement; old reply cannot touch it.
- HOUSE-18: request times out before maintenance/death: record unanswered rather than
  inventing a later cause; refusal/restoration/withdrawal remain distinct. Matching
  custodian-party death with still-alive native flags invalidates an open request
  before transfer; an unrelated custodian's death does not cancel a valid petition.
- HOUSE-19: obsolete .0002/.0003 panels explicitly refresh only their exact readable
  story/house/title/serial, even if revision changed or another request replaced it.
  Refresh opens current record without submitting/answering, cost, favor or state
  change. Forged/wrong pointer/house/title/serial, unrelated reader, expired retention
  and former ruler/custodian actions fail; old issuer may still read without judging.
- HOUSE-20: role/war/imprisonment change and reversal entirely between story passes:
  capture the known observation limit, not a supposed complete history. No new
  native callback or timer is installed. Check fifty-year expiry, pure archive,
  native succession/AGOT behaviors and long-run record/notification cost unchanged.

### Conditional rehabilitation terms (all unrun)

- TERM-01: actual exposed-prisoner political decree → free head petition → sovereign
  offers 50-gold rehabilitation. Exact price/payer/payee, closure, thirty-day deadline,
  refusal/inaction and no native pardon/land/status are shown together. Offering costs
  nothing, consumes the old reply window and revises before delivery.
- TERM-02: head accepts with ≥50 personal gold; verify head -50/current addressed
  sovereign +50 once, exact decree restored, closed-by and payer/payee/date receipt,
  existing retained history, no extra +10 goodwill and no native/old resentment removal.
- TERM-03: two response popups, old ruler reply, old head offer, archive reopens,
  save/reload before/after choice and two same-day choices: no repeat charge, stale
  closure, wrong-payee transfer, receipt overwrite or cross-authority settlement.
- TERM-04: gold falls below 50 after opening, exact 50 boundary, zero/negative balance:
  acceptance fails without debt/partial closure. Refusal/inaction still available.
  Inspect both balances, closure and receipt for engine errors/partial effects;
  no automatic rollback/atomicity is assumed or proved by the source ordering.
- TERM-05: reject, ignore until thirty days, original fifty-year decree expires before
  terms deadline, or sovereign withdraws while offer outstanding: no payment, extra
  penalty, renewed term or revived old acceptance. Unanswered/refused/invalidated and
  paid receipts remain distinct; retirement occurs once on existing maintenance.
- TERM-06: head dies, changes house, is replaced/imprisoned, or goes to war; current
  sovereign dies, loses exact title/independence or is imprisoned. Existing acceptance
  fails immediately; no debt/consent inherited by either successor. Owner-party death
  with unsettled alive/head flags invalidates open terms before custody transfer.
- TERM-07: new head/ruler submits replacement via role-change exception; old terms,
  price/date/window cleared, new offer requires fresh explicit consent. Same eligible
  pair cannot overwrite a valid counteroffer or evade original petition cooldown.
  Change/reversal entirely between observations remains a documented limit.
- TERM-08: stale terms panel refreshes the exact still-readable record only, never
  accepts a replacement. Stranger/former custodian/old ruler cannot pay, collect or
  decide for successors; browsing is actor-only and discloses no private plot data.
- TERM-09: player↔AI and AI↔AI offer/accept/refuse/ignore with identical guards, funds,
  costs and results. Free rehabilitation and sovereign withdrawal remain choices.
  Count notifications/records across repeated passes; no extra timer or annual retry.
- TERM-10: legacy schema-1 record without terms fields works unchanged; distinguish
  paid political restoration from native title/status restoration, dynasty disinheritance
  and celestial family extinction. Baseline AGOT wars, titles, succession, banking,
  release terms, AI and optional-diagnostic isolation remain unchanged in final runs.

### Negotiated delivery clauses (all unrun)

- DELIV-01: deferred default 50 gold/30 days; client counters delivery to 14 preserving
  price, provider accepts. Both names, exact price/deadline, consent-only and future
  effects visible together. No gold/prestige at consent; new obligation has 14 days.
- DELIV-02: combine both clause changes in both orders: 25/14, 25/30, 50/14, 50/30.
  Provider counters duration to 30 without changing price; price requote preserves
  14. Every change revises/reverses turn; no preset bundle or implicit partial consent.
- DELIV-03: original price-only panels append the captured current delivery term.
  Stale price/deadline popups, missing/invalid scalar, wrong party/revision/mode or
  unsupported day count cannot accept, mutate, pay or clear a newer record.
- DELIV-04: fourteen-day promise: no fulfillment before seven days; first decision day
  eight, payable performance once before day fourteen; due flag blocks at expiry,
  timeout at day fifteen. Thirty-day promise retains deadline thirty/timeout thirty-one.
- DELIV-05: wait from day eight into/after fourteen-day expiry; pending weekly ticket,
  timeout and review/cancellation events collide. Only current ticket acts; no deadline
  renewal, duplicate payment/breach receipt or continuing reminder chain after cleanup.
- DELIV-06: counter repeatedly near original thirty-day negotiation expiry; neither
  clause change renews the pending flag/cooldown. Save/reload before either clause
  counter, acceptance and timeout preserves price/deadline/serial/revision together.
- DELIV-07: funds spent, death, loss of land or war before consent/performance: no
  prepayment, unfunded transfer or inherited obligation. Accountable timeout versus
  neutral cancellation follows existing rules, not a newly automatic punishment.
- DELIV-08: new 14-day field with missing/old scalar fails; legacy field-less quote and
  legacy obligation default to original 30 under exact old identity. New snapshots
  capture actual value; fallback never overwrites a 14-day field or its flags.
- DELIV-09: complete, deliberately break, mutually cancel or time out; receipt retains
  accepted delivery when appropriate. Cleanup removes active clause, not counters.
  New offer gets fresh serial/default 30; old timeout cannot consume it.
- DELIV-10: AI↔AI and both player/AI directions negotiate either clause with identical
  eligibility/funds/effects and full terms. Immediate service and existing breach
  mediation/cancellation still work; AGOT wars/titles/banking unchanged. All engine,
  UI/migration/atomicity/balance/performance claims require these final observations.

### Bilateral price amendments (all unrun)

- AMEND-01: provider/client directions propose 50→25 on a due 50-gold deferred promise;
  both names, both prices, no immediate payment and unchanged 14/30-day clause shown.
  Only the other party can accept/refuse; proposer can review/withdraw, never self-accept.
- AMEND-02: accept with ≥25 client gold, including 25–49 after original consent. No gold,
  prestige or performance now; original serial/revision/due flag/timeout unchanged.
  New provider decision shows 25. Fulfillment later transfers 25 and grants 50 client
  prestige exactly once, with current-price receipt before cleanup.
- AMEND-03: propose/refuse/withdraw/ignore seven days; original price remains 50 until
  valid acceptance, no penalty or renewed deadline. Review does not restart the window;
  current request serial cannot be replayed against a later request/contract.
- AMEND-04: before day seven, at/after original due expiry, immediate mode, already 25,
  missing funds, dead/changed parties, war, land loss and old snapshots fail appropriately.
  An insolvent/warring responder can refuse and free the cancellation lane; proposer
  withdrawal likewise stays distinct from performance eligibility.
- AMEND-05: amendment accepted then original timeout fires with captured price 50 while
  client holds 25–49: exact owner/actor/serial/revision and expired flag checked before
  scalar refresh. Current 25 determines accountable breach; no obsolete-price neutral
  cancellation. Current funds <25/unavailable party still follow existing neutral rules.
- AMEND-06: early/stale/foreign timeout, newer accepted contract, missing stored price/
  mode or orphaned client: no unauthorized refresh, payment, renewed clock or false
  blame. Save/reload before acceptance and around original day fifteen/thirty-one.
- AMEND-07: old visible 50-gold panel and weekly ticket after amendment cannot perform
  or duplicate payment. New snapshot and ticket permit one price-25 decision. The
  provider's three-day revisit is allocated before offer; immediate AI consent replaces
  it without a later continuation overwriting the fresh ticket.
- AMEND-08: ignored amendment on fourteen-day promise: provider gets another ordinary
  performance opportunity via three-day revisit when still in time. A late request
  never delays expiry; waits and silence can still lead to original breach/timeout.
- AMEND-09: fulfillment/break/timeout or mutual release wins before amendment reply:
  cleanup removes pending request/parties/cooldown, never the monotonic amendment serial.
  Late acceptance cannot alter a terminal or newer contract; neutral cancellation clears
  uncertain price metadata, and latest outcome retains actual terms when recorded.
- AMEND-10: pending cancellation prevents price proposal and vice versa in every menu/
  event direction. After rejection/withdrawal/expiry, the other lane can open under its
  normal cooldown. Ordinary performance/breach remain available under current terms.
- AMEND-11: player↔AI and AI↔AI proposal/accept/refuse/withdraw/ignore share exact rules.
  One fixed day-eight client opportunity plus provider decisions, no global scan,
  no proposal recurrence or parallel weekly chain; existing promises receive no retroactive
  client timer. Count notices/tickets and verify same-day orderings in both directions.
- AMEND-12: original price/deadline quote counters, immediate services, deferred breach
  mediation, mutual cancellation, house affairs and native AGOT wars/titles/banking
  remain distinct. UI/scalar persistence, old saves, event order, atomicity and long-run
  behavior require direct final engine observations, not source-contract tests.
