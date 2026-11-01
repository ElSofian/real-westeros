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


## Post-rehabilitation land review (LAND-01 to LAND-08)

All unrun. RW010_TITLE_REMEDIES.md describes navigation, not completed restitution.

- LAND-01: on the exact retained restored record, current sovereign and current
  head can review; an old issuer, other house member or storage custodian cannot
  use the new option solely through archive access. Active/withdrawn/expired/purged
  records expose no review. Free/paid restoration take the same path with no new cost.
- LAND-02: landed versus landless heads show correct current standing and named
  house/authority/ruler/head; nothing asserts noble status or ancestral ownership.
  A head who is also sovereign, dead, a minor or imprisoned does not qualify.
- LAND-03: replace the head, change their house, replace the authority holder or
  change record revision while the review is open. Stale description/portrait and
  native click become unavailable; reopening captures current people. No old receipt
  is overwritten and no previous payment or goodwill is repeated.
- LAND-04: the head can read but cannot open a grant as the sovereign. Only the
  exact current free qualified ruler opens native grant terms for the captured head.
  Compare ordinary/theocratic/co-ruler validity and all AGOT restrictions to baseline.
- LAND-05: verify the targetless validity query and special title picker actually
  open/populate. Pick an eligible single title, then multiple titles where native
  rules permit; no selection is prefilled. If unavailable use the native character
  menu and record the shortcut failure; do not bypass validation or force a target.
- LAND-06: cancel review, cancel native terms, and separately confirm a native grant
  in a disposable save. Only native confirmation transfers land and applies its own
  consequences; this mod writes no completed-remedy history, payment or legal pardon.
- LAND-07: save/reload open panels and retained records, expire retention, change
  authority/roles/custody before clicking; no stale native handoff or secret/evidence
  disclosure. No new native title callbacks, reminders or scan chains appear.
- LAND-08: compare AI/player native title grants, revocations, succession, wars/Mega
  Wars and performance to baseline. This human UI does not introduce a new gameplay
  action/cost, automatic AI land gift or inherited obligation. Other decrees and
  native restrictions remain independent; no collective land ban is claimed.


## Native revocation-context provenance (PROV-01 to PROV-10)

All unrun. RW010_TITLE_PROVENANCE.md adds metadata only; no new confiscation action.

- PROV-01: compare AGOT-only/base/optional diagnostic playsets. Confirm additive
  native title effects/events and the separate provenance child both compose; base
  loads no G3 debug/log child. Test AI and human native actors with identical guards.
- PROV-02: after a real accepted native revocation involving an already privately
  exposed participant, inspect whether native actor/recipient/landed_title and
  revoke_title_interaction marker reach on_title_gain together and in time. Confirm
  the callback's previous/current holders and exact title. If missing, no entry is
  expected; record this intake as unsupported, never weaken guards to force a receipt.
- PROV-03: opening/cancelling/refusing revocation and a failed native action create
  no completed-transfer entry. Unrelated grant, inheritance, conquest, usurpation,
  scripted title movement and same-event transfers with stale marker/scopes must not
  be mislabeled. A positive false match invalidates the adapter's source contract.
- PROV-04: enforce native laws/contracts, strong hooks, allied-vassal/truce rules,
  title protections, contested/recently granted titles, administrative/religious
  exceptions and refusal/resistance as in baseline. This observer consumes no reason
  or duplicate tyranny, control, claim, opinion, prestige, stress or prison effect.
- PROV-05: reject wrong actor, recipient, selected title, previous/current holder,
  self-transfer and baronies. Hidden participants and another observer's exposed
  record do not qualify. A typed retained own observation is required; no plot ID
  or assertion of that offense's punishment is added.
- PROV-06: repeat the same title/former/new-holder tuple inside one day: one
  coalesced entry and no renewed clocks/counter. Different titles/former holders
  remain separate. A genuine same-tuple repeat inside that window is deliberately
  coalesced too; after expiry a new observation gets a fresh serial. Not a full ledger.
- PROV-07: reopen journal through another selected character; only actor's own
  records appear, selected character gets no notice. Swap record/serial/title/parties
  or expire retention while a popup is open: portrait/text become unavailable.
- PROV-08: move/destroy the title after observation. The original facts remain;
  current ownership is separate and no entitlement to seize from the new holder is
  created. Reading changes no state or costs. Verify all EN/FR names and descriptions.
- PROV-09: save/reload counters/records, one-day coalescing and original five-year
  retention; no reset/renewal on read. At expiry access stops and sixty-day maintenance
  cleans storage; owner death ends personal records, with no heir/house-head access.
- PROV-10: compare AI/player and long-run native title/war/Mega War/succession
  behavior/performance. No pair/world scan, notifications or new decision chain; only
  relevant callback owner's stories are searched. No universal land ban, lawful
  verdict, institutional provenance or multi-generation restitution is claimed.


## Exact-affair title intentions (INTENT-01 to INTENT-12)

All unrun. RW010_REVOCATION_INTENTS.md distinguishes selection, intention and transfer.

- INTENT-01: open the generic recipient-domain title picker on an eligible direct
  vassal/prisoner. Choose county/duchy/kingdom and non-primary titles where eligible;
  no hard title/affair count cap. Noble-family/landless/wrong-holder titles do not
  qualify. Selection alone creates no intention, request, payment or transfer.
- INTENT-02: two retained private exposed-participant observations for one subject
  yield separate exact confirmations. Verify title, person, captured observation
  number rendering, original-observation inspection and explicit confirmation; a
  generic discovery, foreign observer or different participant cannot supply basis.
- INTENT-03: change custody, liege, title holder, observer readiness or source
  retention/serial before confirming. Stale confirmation fails without cost. Native
  laws, protections, title-specific restrictions and refusal remain authoritative;
  a generic character-validity result is not a per-title lawful judgment.
- INTENT-04: confirm once, double-click/reopen/confirm another affair for the same
  issuer/title: only one live pending intention. Other titles remain available;
  withdrawing permits a new intention with a new serial and explicit chosen basis.
- INTENT-05: read/reopen native terms/change custody or war state. No clock refresh
  or automatic native send. Withdraw without current custody/readiness/basis even
  after the thirty-day window, while owned pending history remains readable; no
  penalty. Withdrawn/observed states cannot be reactivated.
- INTENT-06: human and AI receive at most the two fixed day-two/day-thirty initial
  opportunities per new exposed observation; both use the same selectable-title
  and confirm/withdraw effects. Empty candidate sets clear stale title aliases.
  No recurring reminders, world scan or automatic native AI revocation is added.
- INTENT-07: native-window opening/cancellation/refusal and revoking a different
  title create no execution link for this intention. Intended title is not prefilled;
  verify explicit native selection and confirmation separately. A native transfer
  without the required TP context may produce no observation/link; preserve guards.
- INTENT-08: within the original window, a fresh exact native-context TP observation
  matches one pending intention with its retained original basis/serial. Verify
  consume-before-link order, both pointers/serials and title/subject/issuer identity.
  Duplicate callbacks cannot repeat linkage. This is declared-basis correspondence,
  not proof the native action was caused by or lawfully punished that offense.
- INTENT-09: expired/withdrawn/stale-basis/wrong-title/wrong-holder/ambiguous pending
  records and previously linked TP entries do not attach. An old observation cannot
  be linked after an intention is created. TP one-day coalescing remains: a genuine
  repeated same-tuple transfer can have no new entry, never reuse its older entry.
- INTENT-10: view linked provenance through actor-only archives. Both retained
  records, serials, pointers, title, subject and observed state must match. Wrong
  or expired links hide the basis line, including stale scalar aliases; no foreign
  plot or private observation is disclosed to the selected character.
- INTENT-11: save/reload pending, withdrawn, observed and expired records/counters.
  Original thirty-day/five-year clocks remain; reading/linking never renews them.
  Personal records end on issuer death and sixty-day cleanup removes expired storage.
  No successor inherits private evidence or title entitlement.
- INTENT-12: baseline comparison for native grants/revocations, title lifecycle,
  imprisonment/reasons, succession, wars/Mega Wars, AI, performance and optional G3
  diagnostic. No native cost, tyranny, claim or penalty is duplicated. Verify
  generic-picker scopes, callback propagation/order and scalar-format UI; all remain
  experimental until observed, with no custom confiscation/restoration claim.


## Institutional public land register (ARCHIVE-01 to ARCHIVE-12)

All unrun. RW010_LAND_REGISTER.md describes metadata custody, not land restitution.

- ARCHIVE-01: create a qualifying fresh sovereign TP observation with the actual
  native context. Freeze its original primary crown and former holder's observed
  house. Missing context, no former house or non-sovereign origin creates no offer.
  Legacy TP observations without capture fields cannot be backfilled from today.
- ARCHIVE-02: one fixed day-one offer for both AI and human, or manually review
  from the private TP journal. Opening/declining costs nothing and publishes nothing;
  no recurring offer or additional native title callback. Same effect/guards for AI.
- ARCHIVE-03: confirm with the original observer still qualified and holding the
  captured crown. Losing it or swapping record/serial/crown/house invalidates the
  popup. A successor cannot read or file the predecessor's private TP record.
- ARCHIVE-04: verify exact independent public payload in the filed story/save: only
  schema/kind, crown serial, numeric source identity, original issuer/title/parties,
  frozen former house, authority, observation/filing dates and retention. The
  restitution extension adds only two public-role notification caches, never a
  private request/reply pointer. No TP, evidence, intent, plot or declared-reason
  pointer/content is exported or inherited.
- ARCHIVE-05: double-click/reopen/reload and repeat filing with a missing source
  filed marker: the typed issuer/source-serial index still prevents duplicates.
  Verify fresh constructor, monotonic crown counter, register/membership-before-
  source-consumption order and failed-registration retirement. No reward/payment.
- ARCHIVE-06: current crown holder, current transferred-title holder, original
  parties and current members of the exact frozen former house can read. A whole
  dynasty/cadet/new house does not qualify by blood; custody alone grants no access.
  A selected unrelated interaction recipient receives no journal or notification.
- ARCHIVE-07: let the depositing sovereign die before native alive/title flags
  settle. The departing custodian must be excluded; storage passes to a living
  eligible carrier, then sixty-day maintenance follows settled native roles.
  Successor reads public facts only after private source journals end.
- ARCHIVE-08: lose/destroy/recreate the crown; transfer the land again; replace the
  house head, change house/cadet membership and test original-party fallbacks.
  Check carrier priority and current-role access separately. The fixed original
  former house/date/parties never follow a new house or become inherited guilt.
- ARCHIVE-09: title/current holder changes after filing: historical tuple remains
  unchanged and current ownership is shown separately. No claim, native title
  effect, legal right against a later holder or automatic ancestral restitution.
- ARCHIVE-10: save/reload, read and rehome records. Original observation/filing
  dates, crown serial and hundred-year archival expiry persist without renewal.
  Check pointer validity over generations; missing immutable pointers can retire
  a record, so no eternal-history guarantee or engine proof is inferred.
- ARCHIVE-11: expiry, malformed entries and no eligible living custodian retire
  the exact index entry before ending the story. Access stops at retention expiry
  even before cleanup; no unrelated custodian, counter reset or dangling journal.
  Stale/foreign record/crown/house/title/party popup tuples disclose no entry.
- ARCHIVE-12: compare native war/Mega War, title/succession, prison, banks, house
  stability and optional G3 diagnostic with baseline. Benchmark index reads and
  sixty-day per-record maintenance at sustained load. Verify EN/FR and scalar
  serial rendering; no new world/pair scan, native sanction or recurring AI policy.


## Restitution discussion and personal response (REST-01 to REST-14)

All unrun. RW010_RESTITUTION_DIALOGUES.md creates discussion, not promised restitution.

- REST-01: from an exact retained public entry, a living adult free original former
  holder may ask. After their death, the current adult free head of the exact
  frozen house may ask for themselves. A living minor/prisoner is not bypassed by
  a house head. Wrong house/dynasty/cadet/current-crown authority grants no claim.
- REST-02: capture the actual current land holder, not an old recipient or sovereign
  who does not own it. Ownership, source retention/serial/title/house/crown changes
  before confirmation reject the stale popup. No title/claim/payment is created.
- REST-03: confirm once; registration precedes both captured-party notifications.
  Repeat/double-click/reload and alternate public entries for the same pair/title
  cannot evade the one-year cooldown. Other titles and new party identities remain
  independent. Fresh serials are not reset by refusal, cleanup or succession.
- REST-04: only the two original participants can read replies/history, through
  captured record/serial/title/source-serial/crown/house/former/party identity.
  The arbitrary character selected for the archive receives no information. Public
  crown/house successors and storage custodians inherit no private request/consent.
- REST-05: accept examination only as the captured holder while both parties and
  source/current ownership remain eligible and the original thirty-day window lives.
  State changes to talks before notice; no payment, title grant, promise, completion
  reward or deadline/cooldown/retention renewal. Repeat acceptance fails.
- REST-06: original holder refuses/closes or requester withdraws, even after role,
  custody, war, source or title changes while typed history is readable. This does
  not speak for a new holder. Consume before notice; silence, withdrawal and
  observed invalidation produce no automatic penalty or recurring reminder.
- REST-07: only original requester can react to actual refusal within seven days,
  once, with the original refuser alive and requester not already holding the title.
  Acknowledge adds no penalty and removes no earlier opinion; resentment targets
  that person alone, −10 for two years only if same modifier absent. It neither
  stacks nor refreshes across other titles/requests. No inherited guilt/crime.
- REST-08: accept review, then verify native grant validity and window opening with
  current exact holder/requester/title. No title/hook/terms are preselected or sent.
  Pick/confirm intended title separately; cancellation/another grant is not labeled
  fulfillment. A blocked native query keeps the shortcut absent, with native menu
  fallback. AI native grant policy remains authoritative, without a forced gift.
- REST-09: requester acquires the title by gift, inheritance, war or another route.
  View shows current ownership without attributing cause to the discussion. Moving
  title to a third party blocks old native handoff; historical entry is no right to
  confiscate from that person. No restored/fulfilled cache is written.
- REST-10: at filing and sixty-day public maintenance, offer the actual current
  eligible claimant/holder pair, never the public story ROOT or custodian. The pair
  cache advances before event; unchanged pairs skip private-index cooldown scans.
  Ineligible adulthood/release transitions can allow a first later opportunity;
  transient changes/reversals can be missed. No request is sent without confirmation.
- REST-11: public entry's extension fields contain only two public-role notice IDs,
  not private request pointers/replies/reaction/consent. Request stories have their
  own private index and owner; no private plot/evidence/intent material is imported.
  Public reads send no offers and private reads mutate no flags, costs or clocks.
- REST-12: source expiry, holder/requester death, head/house change, war/custody
  change and expired windows disable acceptance/transfer before maintenance.
  Observed invalidation is neutral; a new holder/head needs a new request and
  captured consent. Death/expiry retirement removes the private index before end.
- REST-13: save/reload pending/talks/refused/withdrawn/expired/invalidated histories,
  original thirty-day/one-year/five-year/seven-day flags, serials and opinion expiry.
  Pointer loss may retire/invalidate history; do not assume universal long-term
  preservation. Successors keep only public facts, never personal rancour/consent.
- REST-14: baseline native titles/AI grants/revocation/laws/refusal, Mega Wars,
  succession/banks, house stability, optional G3 diagnostic and performance. Measure
  registry changed-pair/index costs and private per-record maintenance at scale;
  verify EN/FR/event scopes and no extra recurring requests or doubled native effects.


## Exact service clauses in private mediation (all unrun)

- CASE-TERMS-01: negotiate and breach each 25/50-gold × 14/30-day deferred
  endorsement; refer to a separate common overlord. All original informed parties
  read the exact copied clauses from ruler/repair/result/history panels. Merely
  reading changes no resources, opinions, stages, deadlines or outcomes.
- CASE-TERMS-02: accept a due 50→25 amendment, then explicitly refuse or let the
  original timeout fire with only 25–49 client gold. Receipt/case must say 25;
  original delivery clause/revision remain. A pending/refused/ignored amendment
  must still yield price 50. No second payment, timer reset or false insolvency.
- CASE-TERMS-03: refer A, then create/finish B for the same provider, with another
  client/price/delivery. Old A notices/history still show A; A's copied fields
  do not alter B. Repeated browsing/clicks cannot copy a new receipt into A.
- CASE-TERMS-04: replay old referral after response consumption, new receipt,
  different case serial/client, ended story or wrong owner/type/kind. No foreign
  clauses, duplicate referral or response consumption. Probe same-tick construction.
- CASE-TERMS-05: known provider/client/disclosed mediator can read; unrelated
  characters, an undisclosed planned mediator in an allegation, later rulers and
  heirs cannot learn private clauses. Loss of current authority does not erase an
  already informed original mediator's memory or grant a new decision right.
- CASE-TERMS-06: old case/receipt without schema, missing term/date/revision or
  unsupported price/delivery stays explicitly unknown. A later contract never
  backfills it; normal old-case decisions remain eligible under original guards.
  A neutral orphan cancellation after a typed receipt cannot inherit its metadata.
- CASE-TERMS-07: save/reload before/after receipt, referral, mediation closure and
  browse. Verify independent stories, notice scopes, original retention/death
  cleanup and EN/FR fallback rendering. No heir receives personal consent or guilt.
- CASE-TERMS-08: compare AI/player receipt/referral paths, AI political choices,
  AGOT-only baseline, logs and archive performance. No extra automatic request,
  world scan, effect replay or native title/war/justice behavior should be added.


## Personal restitution promises (all unrun)

- PLEDGE-01: eligible talks allow only the captured actual holder to explicitly
  propose thirty days. Examining talks/opening native terms alone creates no
  promise. Repeat initiation cannot reset the one offer per discussion; unrelated
  requests/titles remain possible under their existing pair/title cooldowns.
- PLEDGE-02: beneficiary counters fourteen, holder counters thirty, then either
  responder accepts the exact latest version. Replay old/wrong-party panels: no
  acceptance or counter. Verify one-day replies and unchanged original seven-day
  offer and thirty-day discussion windows for humans and AI, without instant loops.
- PLEDGE-03: either party closes an unaccepted offer after war, prison, source/role
  loss or deadline; no promise/penalty. Expired/current-mismatch proposals cannot be
  accepted. No automatic reconstruction from old requests or absent pledge data.
- PLEDGE-04: acceptance starts one fourteen/thirty-day due window, consumes offer,
  schedules original exact requester/tuple/revision callback on day fifteen/thirty-one
  before notices. Reentry/reload cannot renew it, pay, transfer or create an heir duty.
- PLEDGE-05: close/refuse/withdraw discussion or let its earlier window/source expire
  after acceptance. The private personal promise retains its own clock/outcome;
  no implicit release/renunciation or additional old refusal opinion applies.
- PLEDGE-06: holder's native window requires exact unexpired promise, original
  available parties/current actual owner and fresh native validity. Choose intended
  title and confirm manually; opening never selects/sends it. Check native laws,
  special title restrictions/AI grants, AGOT institutions, wars and succession.
- PLEDGE-07: beneficiary ownership from grant, inheritance, war or another route
  alone writes no acknowledgment/reward. Only beneficiary's explicit confirmation
  while actually holding this exact title records personal satisfaction. Wrong
  title/third party/stale revision cannot confirm. Confirm after deadline: late
  confirmation, never inferred late acquisition or proof of voluntary grant/cause.
- PLEDGE-08: beneficiary freely releases promised/unresolved commitment despite loss
  of grant eligibility or current authority; no cost or penalty. Holder explicitly
  renounces only a live accepted promise while still owning that title. Both consume
  the due marker before notifications; old timeout/replies become inert.
- PLEDGE-09: renunciation creates no automatic penalty. Within seven days the original
  beneficiary may acknowledge or choose −15 opinion/two years once, with current
  original parties available and holder still owning the title. Repeated/different
  title reactions cannot stack/renew it; later ownership/successors cannot be targets.
- PLEDGE-10: stale/early/other-owner timeout cannot affect another promise. Actual
  expiry without confirmation records unresolved, not blame; lost callback fallback
  at sixty-day maintenance is also neutral. Probe missing party/title, third-party
  ownership, death and rapid role/title reversals between observations.
- PLEDGE-11: save/reload every offer/counter/accepted/renounced/released/unresolved/
  acknowledgment state; inspect exact request private role filtering, source pointer
  loss, original five-year retention, requester death/index cleanup and holder death.
  No heir/crown/house successor inherits private replies, consent or guilt.
- PLEDGE-12: measure AI choices/native grants, EN/FR event scope/statement rendering,
  same-tick order, save size, private reconciliation cost and AGOT-only baseline.
  No new native hook/world scan/recurring reminder or native transfer replay should
  load; optional G3 trace stays separate. No compatibility/performance claim yet.


## Conditional pledged-title transfer context (all unrun)

- TRANSFER-01: accept exact-title 14/30-day pledge, then use native grant while
  original parties live and due marker remains. Validate actual callback ROOT,
  title/previous holder/current holder, exact first note and unchanged native grant.
  Observation is not automatic confirmation, payment or proof of voluntary cause.
- TRANSFER-02: acquire matching title through another native route with living
  previous holder. If callback/context matches, note stays route-unknown. Death
  inheritance/absent previous holder/noble-family/landless/wrong/currently unowned
  title or reversed parties must not yield this authored note.
- TRANSFER-03: missing actor/recipient/interaction marker must not be required by
  this generic context intake. Missing actual title/previous holder/new-holder or
  premature callback before ownership settles yields no note, never a fallback.
  Absence does not block independent beneficiary acknowledgment or native UI.
- TRANSFER-04: wrong owner/retention, unaccepted/expired/released/renounced/acknowledged/
  invalidated promise, missing schema/revision or wrong 14/30-day clause is rejected.
  Late native transfer cannot backfill a now-unresolved promise's missing note.
- TRANSFER-05: two matching live candidates cause no selection or write, including
  one already observed candidate. Repeated same callback leaves the original date,
  all fact fields, consent, due marker and parent retention unchanged.
- TRANSFER-06: move title onward after a valid note. Known original participants
  still see its historical context and separate current ownership. Another title,
  request/revision/delivery or party tuple cannot display or rewrite the note.
- TRANSFER-07: outsider, house/crown successor and heir cannot read private notes;
  public archive gains no pointer/reply. Source expiry/head change cannot silently
  substitute a new personal beneficiary or rewrite accepted consent.
- TRANSFER-08: save/reload before/after intake, acknowledgment and original five-year
  expiry. Requester death removes original private index/story; no inherited duty,
  renewed retention, transfer replay or automatic reward/penalty follows.
- TRANSFER-09: both original revocation and new pledge children compose with native
  effects in the actual AGOT playset. Probe special/batched multiple-title grants,
  tyranny/revocation, wars/Mega Wars, succession, laws and optional separate G3 trace.
  No popup, native override, second title transfer or changed promise state is added.
- TRANSFER-10: compare recipient-owned scan cost with/without a request counter,
  many owned stories and unrelated title changes, AI/player parity, EN/FR warnings,
  logs and AGOT-only baseline. Callback composition/order, performance and knowledge
  semantics remain unverified until these cases are actually run.


## Voluntary private compensation for closed service cases (all unrun)

- COMP-01: original provider offers 25/50; original client separately requests 25/50
  on different retained closed service cases. Opening result/archive dialogue moves
  no money. Mediator, outsider, active/expired/ended/allegation/unknown-kind cases
  cannot initiate or read private financial data; current rank is not a substitute.
- COMP-02: provider offer → client counter → provider consent, and client request →
  provider counter → client consent. Only latest exact responder/revision/amount
  can settle; counter never charges. Replay proposer/older/wrong-case panels.
- COMP-03: let the payer spend below 25/50 before consent; acceptance must disappear
  and explain current inability to pay. Counter lower or close, with no debt,
  borrowing, refund, automatic sanction or silent transfer. Restore funds within
  the original window and explicitly accept exact current terms.
- COMP-04: accepted 25/50 debits original provider and credits original client by
  exactly the same amount once, regardless of clicking actor/proposer. Compare
  receipt amount/revision/date, same-tick double clicks, save/reload and stale reply
  after payment. No extra gold, prestige, opinion, pardon or title effect.
- COMP-05: fixed seven-day offer window survives counters, reviews and waits without
  reset. Replies arrive after one day, with no immediate AI counter loop. Silence
  and expiry pay nothing; expired offers cannot reopen as a new window for that case.
  Other cases retain independent offers/receipts with no global count truncation.
- COMP-06: detention, death, war between parties, reference loss and expired case
  retention disable settlement. Either original living party can close after poverty/
  war/detention while the exact parent remains retained. No escrow or heir debt.
- COMP-07: fresh result/archive entry displays current terms but changes no stored
  data. An old delayed reply never refreshes itself into a newer consent ticket.
  Queue A/B cases for same provider with different clients/amounts; notices and
  payments must keep their own captured story/serial/parties/reason/kind.
- COMP-08: original known mediator can still read affair history but cannot see or
  receive compensation terms, counteroffers or paid receipts. Crown/house/ruler
  successors and unrelated characters cannot inherit either party's private consent.
- COMP-09: after compensation, original service breach, copied clauses, closed result,
  legal reasons and existing resentment remain unchanged. Separately accept/refuse
  a prior apology within its own unchanged window; payment is not forgiveness.
  A newer live service/receipt for the provider must remain untouched.
- COMP-10: save/reload proposed/countered/paid/closed/expired offers, parent original
  1825-day retention and sixty-day cleanup. Provider death ends personal stories;
  neither reading nor compensation extends memory or creates an inherited obligation.
- COMP-11: compare AI/player paths and actual payer/recipient balances, trait/funds
  preferences, refusal/inaction and economic abuse over multiple cases. Existing
  result notices provide opportunities; no new global scan, hook or timer should run.
- COMP-12: compare AGOT-only baseline, errors, native banking/debt inheritance,
  justice/war/title behavior, EN/FR rendering, event order and performance. Ordered
  script consumption is not crash consistency; probe partial-effect cases safely
  and never automatically replay a payment after a crash or missing confirmation.


## Personal response to a new paid compensation (all unrun)

- COMP-REACT-01: settle new 25/50 compensation in both initiation/acceptance directions.
  Response metadata is created once after both gold calls and before receipt notices,
  binding exact case, paid revision/amount/date. Cash alone sets no appreciation.
- COMP-REACT-02: only original beneficiary may appreciate or neutrally acknowledge
  pending response within thirty days. Wrong payer/client/case/revision/amount/date,
  mediator, successor, ended/expired parent or dead payer cannot authorize a response.
- COMP-REACT-03: appreciate consumes response before +5 opinion/two years and payer
  notice. Double click, replay, read/reload and old receipt cannot renew a choice,
  pay again or add a second modifier. Missing schema/date/receipt fields fail closed.
- COMP-REACT-04: pay another distinct case while the same pair modifier exists.
  Beneficiary may record appreciation but its value/expiry neither stacks nor
  refreshes. After actual natural expiry, a later new eligible response may add it.
- COMP-REACT-05: neutral acknowledgment records statement/date with no benefit,
  penalty, refund, legal reason, erased resentment or accepted apology. Paid amounts,
  case result/evidence, current service terms and original personal grudge stay.
- COMP-REACT-06: leave undecided, let thirty days lapse or kill beneficiary. No
  automatic gratitude/refusal/blame; unavailable status is explicit. Old paid records
  without metadata get no backfill window and no inference of personal consent.
- COMP-REACT-07: after payment change rank, funds, war or detention. Personal response
  is separate from financial-transfer eligibility and current judicial authority;
  living exact original parties may still record it without paying or reopening.
- COMP-REACT-08: original payer alone receives the new response notice. Original
  financial parties can read private history; mediator/house/crown/heirs cannot
  discover it through case history or inherit personal consent/opinion effects.
- COMP-REACT-09: save/reload all response states and test original parent retention,
  provider death and cleanup. No timer/index/story/new native hook, renewed retention
  or global scan. Do not retry/refund money after missing response/partial effects.
- COMP-REACT-10: compare AI/player receipt choices, trait/existing-opinion weights,
  native opinion expiry, EN/FR rendering, same-tick callback order and AGOT-only
  baseline. Economic/political balance, privacy/persistence and performance remain
  engine-unverified; no service, bank, title, native justice or war is replayed.


## Native-favor or negotiated-gold immediate endorsement (all unrun)

- FAVOR-01: new interaction auto-accept opens only a proposal. Client explicit favor
  acceptance gives original provider one native favor over client and client 50
  prestige once, with no gold. Verify actual native eligibility, direction/type and
  original serial/revision/term, not merely metadata saying fulfilled.
- FAVOR-02: client counters 25 gold, provider accepts current version with client
  funds >=25: client −25/provider +25/client +50 prestige, no new hook. Swap initiation
  contexts/ranks and replay proposer/client/old-version/old-term panels: no exchange.
- FAVOR-03: provider restates favor, requiring client consent again. All counters
  increment revision/change turn and delay replies one day without resetting original
  thirty-day pending window or shared annual cooldown. No immediate AI counter loop.
- FAVOR-04: existing weak/strong/different-type/pending/unusable/cooling-down hooks
  must not be overwritten or refreshed. Acquire a hook between proposal/acceptance
  and reject favor terms at fresh checks; counter gold or close without touching it.
  Native predicate/type semantics require direct proof, not assumed coverage.
- FAVOR-05: native can_add_hook failure, lost rank, war, prison, death, reference loss,
  self-target and expired pending marker block performance. Poverty blocks gold
  agreement but not proposal/counter/free closure. No forced payment or debt appears.
- FAVOR-06: close either role after expiry/war/prison/native favor ineligibility.
  Only current exact offered ticket clears; replay after a newer serial cannot
  close it or grant a service. Shared cooldown remains; no refund/automatic sanction.
- FAVOR-07: before favor start, retain an old ignored/expired financial quote and
  its saved panels. Starting favor never re-adds rw_service_pending/obligation or
  changes old serial/target/mode. Replay old financial accept/clear/timeout: no
  payment, prestige or cancellation of the new independent favor ticket.
- FAVOR-08: exercise gold/deferred→favor and favor→gold/deferred availability. One
  active provider pool and shared year cooldown prevent bypass by switching types.
  Current native favor use outside this mod and unrelated financial cases remain.
- FAVOR-09: private latest review by provider/client does not renew, pay or grant.
  Outsider/former client/new heir cannot see a replacement serial. After fulfillment
  consume/expire the favor natively: old receipt never claims it is still active or
  creates another. No complete historical/dynastic ledger is implied.
- FAVOR-10: save/reload offered/countered/closed/fulfilled and old/new serials;
  verify original offer/cooldown dates, native favor identity/expiry, root/saved-value
  scopes and no duplicate prestige/hook/gold. Never retry partial/crashed effects.
- FAVOR-11: compare AI/player eligibility/effects, bounded liege initiation, trait/
  gold preferences, refusals and realistic native favor value/prestige economy.
  Review-only AI is disabled; reactive latest-version reply paths must still work.
- FAVOR-12: compare AGOT-only baseline, hook-type/playset/DLC behavior, existing bank
  debts, native favor uses/law/war restrictions and institutions. No automatic hook
  spend, sent interaction, realm-law change, title/war operation or new callback
  should occur. Record actual timing, EN/FR logs, save growth and performance.


## Deferred native-favor or agreed-gold support (all unrun)

- DFAVOR-01: choose distinct immediate/deferred interactions, negotiate favor/25-gold
  terms and accept exact current responder/version. Deferred consent moves no hook,
  gold or prestige, invalidates quote panels and schedules accepted identity only.
- DFAVOR-02: immediate offers still perform immediately and cannot spend a deferred
  quote. Legacy mode-less rows reopen as immediate only; old panels without captured
  mode stay inert. Copied new-mode records cannot replace the stored original provider.
- DFAVOR-03: before seven days no provider performance; after minimum and before
  thirty-day due expiry perform one agreed branch and client +50 prestige. Duplicate
  clicks/replies, client-as-performer and other mode/serial/revision/term cannot pay.
- DFAVOR-04: acquire another native hook between consent/performance; detected hook
  is never replaced/refreshed. Native can_add_hook failure blocks favor performance.
  Later insolvency blocks gold performance. Neither silently switches consideration.
- DFAVOR-05: original provider may renounce and original client may withdraw before
  performance, including war/detention/poverty/capacity loss. No payment, hook
  removal, debt, refund, penalty or inherited guilt. Old opportunities become inert.
- DFAVOR-06: exactly two provider opportunities at day eight/twenty-two, with active
  due guard and identical AI/player decisions. Leave/review repeatedly: no new timer,
  extended due marker or recursive decision chain. Native favor/gold terms stay fixed.
- DFAVOR-07: original day-thirty-one callback needs actual expiry, original provider,
  accepted mode/serial/revision/term and slot. Early/stale/wrong-owner/newer-ticket
  callbacks cannot clear it. Expiry is neutral unresolved, not a crime or blame.
- DFAVOR-08: purge/kill client or lose their reference: no transfer to substitute/heir;
  owner-only expiry still releases valid original slot without requiring full client
  view or sending invalid-scope notices. Provider death authorizes no successor.
- DFAVOR-09: suppress timeout in a disposable test save: technical slot long-stop
  expires at thirty-two days and cannot block future availability forever. It grants
  no extra performance time beyond the separate thirty-day due flag. History may
  remain promised metadata but displays expired/unresolved without inferring blame.
- DFAVOR-10: immediate favor, monetary immediate/deferred and deferred-favor pools
  share availability/cooldown without reviving original financial pending/obligation/
  serial/target flags. Terminal paths clear only their exact own accepted slot.
- DFAVOR-11: save/reload mode, accepted revision, minimum/due/long-stop flags, both
  fixed decisions, withdrawal/renunciation/unresolved/fulfilled states; inspect
  exact participant privacy, late callbacks and native effect order. No automatic
  retry after interruption or claim of atomic hook/gold/prestige exchange.
- DFAVOR-12: compare actual AI native favor willingness, economy, old-hook semantics,
  bank debt/inheritance, law/war/title behavior, EN/FR, timing/flag expiry and AGOT-only
  baseline/performance. No extra native hook type, forced hook spend, on_action,
  global scan, inherited scripted service or automatic sanction is added.

## Deferred support renunciation responses (all unrun)

| ID | Final campaign scenario | Expected observation, not demonstrated |
|---|---|---|
| FREN-01 | Accept deferred favor/gold terms, then provider explicitly renounces | Closed unperformed promise; original client receives a fixed thirty-day personal choice, with no hook/gold/prestige exchange |
| FREN-02 | Client chooses resentment; replay same popup and fresh review | One −15 opinion/two-year modifier; one response/date/provider notice; replay cannot choose again |
| FREN-03 | New later promise is explicitly renounced while pair's modifier remains active | New personal choice is possible, but resentment neither stacks nor renews existing modifier; other grievances stay intact |
| FREN-04 | Client takes note, or waits past day thirty | Neutral statement or expired silence respectively; no opinion removal/addition, pardon or new legal fact |
| FREN-05 | Timeout, client withdrawal, offer closure, actual performance, or pre-update renunciation | No response opportunity created or retrospectively backfilled; no payment/hook replay |
| FREN-06 | Save/load before and after response; reopen an older panel after a new serial/revision/mode/term | Exact terminal-date and ticket matching; no renewed window, stale response or changed newer record |
| FREN-07 | Client/provider death, copied successor data, unrelated actor or mediator | No inherited personal response, leaked private notice or actor substitution; original identity guards apply |
| FREN-08 | AI↔AI and AI↔player, including imprisonment/poverty/war after renunciation | Same personal response guards/costs; ordinary incapacity does not prevent taking note; no new scan/reminder spam or native-state change |

## Private allegation settlement (all unrun)

| ID | Final campaign scenario | Expected observation, not demonstrated |
|---|---|---|
| ASET-01 | Claimant alleges affront, respondent acknowledges or contests, claimant proposes fifty gold | One private seven-day offer after either statement; no money, opinion, prestige, disclosure or withdrawal at proposal |
| ASET-02 | Respondent explicitly accepts fifty with funds | Exact respondent pays fifty to claimant once; both offer and case already consumed; withdrawal and payment recorded separately from unchanged statement |
| ASET-03 | Respondent counters twenty-five; claimant accepts | Revision/turn updated; original respondent still pays, despite claimant clicking accept; no charge at counter |
| ASET-04 | Claimant maintains fifty; replay initial fifty or older twenty-five panels | New revision requires new respondent agreement; stale panels cannot pay/close current offer |
| ASET-05 | Respondent spends gold before either party's acceptance | No payment or withdrawal until current agreed funds exist; no negative-balance fallback, escrow or automatic retry |
| ASET-06 | Wait beyond seven-day offer or original thirty-day case deadline, or repeatedly counter/review | No renewed deadline, payment, admission, inferred agreement or new offer for same case; original neutral case expiry still works |
| ASET-07 | Either party refuses settlement | Financial dialogue closes without gold, case withdrawal, new grievance or judgment; claimant may still independently withdraw/refer |
| ASET-08 | Claimant freely withdraws or refers before payment, then old acceptance arrives | Existing free action succeeds; old financial offer cannot charge or undo case stage; mediator learns only actually referred allegation |
| ASET-09 | Wrong story/kind/serial/parties, changed lieges, war, imprisonment, minority, death or reference loss | No settlement or substituted/inherited payment; identity-only financial closure stays free where original scopes survive |
| ASET-10 | Read exact archived paid receipt and statement; try mediator/outsider/archive navigation | Original parties read exact terms/payment; mediator cannot read financial dialogue; navigation never renews retention, proposes, pays or reopens |
| ASET-11 | Save/load at each turn and terminal state; independent allegations with equal serials | Story/kind/owner/client/revision/amount remain isolated; no duplicate debit, statement change, hook, secret, pardon or title/native-justice effect |
| ASET-12 | AI↔AI and AI↔player, with admission/contest, hostility, greed and low funds | Same actions/costs/guards; observe incentives, spam/economy, event scheduling and baseline AGOT compatibility before balance claims |

## Personal military-restraint pledges (all unrun)

| ID | Final campaign scenario | Expected observation, not demonstrated |
|---|---|---|
| MREST-01 | Offer between valid original parties; decline, ignore or accept before day seven in separate saves | Explicit original-beneficiary consent only; no truce, gold, prestige, opinion, hook or legal consequence from offer/refusal |
| MREST-02 | Accept; replay offer/acceptance and inspect after ninety days | Original accepted date/ninety-day marker set once; no renewal on read or repeated clicks; elapsed remains neutral |
| MREST-03 | Original promisor becomes primary attacker against original beneficiary while accepted/live | Exact native callback roles recorded once before two private notices; native war/CB and normal AGOT resolution unchanged |
| MREST-04 | Duplicate callback, reverse roles, defensive war, secondary ally participation or unrelated target | No duplicate notice and no reversed/secondary/other-target observation; no intent/legal verdict |
| MREST-05 | Offer unaccepted/expired, pledge renounced/released/expired, then same pair wars | No observation attached or old-war backfill; existing historical result retained |
| MREST-06 | Missing native war/attacker/defender, role mismatch or changed context during AGOT children | Fail closed without native mutation; investigate callback order; no assumption of exhaustive coverage |
| MREST-07 | Renounce or release while personal identities survive but rank/war/wealth/imprisonment changed | Original actor can use their own free exit during active window; other actors/stale/deadline panels cannot |
| MREST-08 | Promisor dies, heir/copy obtains metadata, beneficiary dies or scopes disappear | Personal owner-death cleanup; no inherited duty, substituted actor or invalid-scope action |
| MREST-09 | Read independent records for same parties/other parties, including equal serials under different owners | Exact story/owner/beneficiary/serial isolation; only original parties see records, with no truncation or latest-pointer overwrite |
| MREST-10 | Save/load before/after consent, exit, callback, war end and elapsed cleanup | Dates/role record remain coherent; no retained destroyed-war reference, repeated observation, renewed retention or reconstructed fulfillment |
| MREST-11 | Observe AI↔AI and AI↔player, offer cooldown, story cleanup and numerous retained records | Same actions/costs/guards, bounded liege initiation and owner-local queries; measure actual event/privacy/performance behavior |
| MREST-12 | Compare normal claim/revolt/Mega War and native ban/hook rules against AGOT baseline | Observer alone never enables declaration, changes CB, forces peace or claims voluntary war cause; G1 genuine-ban bypass remains separate/unresolved |

## Military-restraint explanations and reactions (all unrun)

| ID | Final campaign scenario | Expected observation, not demonstrated |
|---|---|---|
| MRESP-01 | Fresh exact role observation, compared with old record/expiry/renunciation/release/wrong target | New observation alone opens one thirty-day response window before notices; no legacy backfill or automatic opinion/admission |
| MRESP-02 | Beneficiary requests explanation twice; promisor answers with acknowledgment or contest in separate saves | One request and one explicit original-promisor statement/date; no renewed deadline or change to role fact/native legal status |
| MRESP-03 | Ignore request and pass response deadline | Statement stays unanswered; silence creates no deliberate-breach finding, opinion, consent or pardon |
| MRESP-04 | Beneficiary chooses resentment before request, after acknowledgment or after contest | Same optional personal reaction allowed; consume before once-only −15 opinion/two years and private notice; no forced verdict |
| MRESP-05 | Later pledge yields a fresh observation while pair's same modifier remains active | New personal response can be recorded but existing modifier never stacks/refreshes; other grievances remain |
| MRESP-06 | Beneficiary takes note; pending promisor reply arrives afterward | Neutral response preserved, no opinion add/remove; late reply cannot rewrite closed response; original fact and prior statement remain |
| MRESP-07 | Replay request/answer/reaction popups, wrong actor/story/serial/date, observer/liege or successor | No duplicate request, changed statement/reaction, personal penalty, leaked private terms or inherited authority |
| MRESP-08 | Save/load at each state; war ends/reference disappears; original party dies or loses rank/freedom/peace/funds | Exact retained personal facts remain separate; living original parties need no new-pledge capacity to reply/react; death/retention guards apply |
| MRESP-09 | Request on day twenty-nine, wait/review/reply, then expire and inspect archive | Original deadline never renewed; no repeated timer or extra notification chain; archive shows silence/statement/reaction separately |
| MRESP-10 | AI↔AI and AI↔player across traits and observed war contexts, compared to AGOT baseline | Same actions/effects/guards, bounded notices, no native war/CB/truce/secret/justice effect; measure actual privacy/AI/performance before compatibility claims |

## Public institutional restitution charters (all unrun)

| ID | Final campaign scenario | Expected observation, not demonstrated |
|---|---|---|
| RCHART-01 | Fresh public entry, current sovereign proposes; exact head accepts within seven days | No charter consent from auto-open, payment or title transfer; exact representatives and version required |
| RCHART-02 | Sovereign/head changes before acceptance; replay original offer, then close stale proposal | New representative cannot inherit pending personal consent; neutral current-role closure, no new rights |
| RCHART-03 | Accepted charter, new sovereign chooses recognize or repudiate in separate saves | Explicit representative choice; no personal guilt/assumption from crown inheritance alone; original five-year deadline preserved |
| RCHART-04 | Crown A→B→A, heads change, and short unobserved role reversals | Fresh current-role checks; recognition tracks character identity, not reign history; no claimed detection of unseen transitions |
| RCHART-05 | Exact title held by original crown, third party, different house, then exact former-house member | Only current exact head can record satisfaction in the last case; no automatic transfer/seizure or causal grant inference |
| RCHART-06 | Current head releases, current crown repudiates, or offer is closed; replay all panels | Windows consumed and revision/actor/date stored before notices; no replay or opinion/claim/title effect |
| RCHART-07 | Expire offer/five-year accepted period; repeatedly read, recognize or reopen | No deadline reset, new proposal for same entry, automatic breach/fulfillment/guilt/pardon or record retention renewal |
| RCHART-08 | Original storage owner dies, normal registry migration; archive reaches fixed retention end or native refs vanish | Public fields follow storage with current access/roles; no private consent copied; fail closed when entry/reference no longer accessible |
| RCHART-09 | Original parties, current house/crown/title roles, custodian and outsider browse public entry | Existing public reader policy only; storage ownership creates no authority; archive navigation never accepts/proposes by itself |
| RCHART-10 | Fresh deposit vs older empty entries, accepted charter and new ruler/head maintenance | Initial fresh opportunity, no old automatic offers, active-role and exact-house recovery-holder notices coalesced before sending; same head can acknowledge later recovery; correct character-event root, no repeated unchanged-role/holder prompts |
| RCHART-11 | AI↔AI and player↔AI across dispositions and repeated records | Same actions/costs/role/revision guards; measure actual AI response/spam/performance; no automated native grant claimed |
| RCHART-12 | Save/load all phases; native grant/inheritance/election/conquest, private restitution pledge and AGOT baseline | Independent public institutional state; no private promise exposure/rewrite, new hook/war/title/house-ban effect or invented universal G3 enforcement |
