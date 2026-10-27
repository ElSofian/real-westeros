# RW-010 — contextual mediation of a recorded breach

Current amendment: RW010_REPAIR_RESPONSE.md replaces the automatic client opinion benefit with explicit acceptance/refusal; mediator opinion remains separate. Earlier flow descriptions below predate this change.

**Experimental CK3 scripts; not engine-tested.** All runtime checks remain deferred
to the final campaign at the owner's request.

## Facts, disclosure and authority

A recorded broken endorsement now distinguishes **explicit refusal** from an
**elapsed deadline with eligible parties and possible payment at expiry**. The latter
records nonperformance, not motive or continuous eligibility throughout the agreement.
Neither means a native crime. Neutral cancellation is not a breach and cannot open
this case. Only the client with the current, unreacted receipt may refer it.

Referral discloses the narrow agreement/outcome to the parties' common top liege,
provided that ruler is neither party and is living, adult and landed. This is a
specific jurisdiction policy, not a universal court. It excludes a ruler judging
their own dispute and cases with no common superior. Personal resentment/forgiveness
remain available where referral is unavailable. No free-form accusation, forged
receipt, rumor spread, scheme knowledge, native secret, hook or criminal status is
created. Private mod variables are not authenticated against arbitrary external mods.

Opening snapshots provider/client/mediator, contract serial and recorded reason into
case-owned fields, then consumes the client's personal-response opportunity. The
client delegates this slice's response rather than stacking resentment and referral.
The breach record is not rewritten when mediation succeeds. Case state remains
independent of later service state/outcomes. Each referral now has a separate CK3
story record rather than the latest provider slot; see RW010_RECORDS.md. This is
limited personal case history, not a general evidence ledger or dynastic history.

## Discretionary choices

The common overlord can:

- **Decline intervention:** no adverse effect or transfer.
- **Reprimand:** the ruler's personal opinion of the provider falls by 10 for two
  years. No title loss, imprisonment, claim, crime or other automatic sanction.
- **Invite voluntary repair:** the provider can apologise for 25 prestige, improving
  client and mediator opinion by 5 for two years, or refuse without an automatic
  extra penalty. Apology does not perform the original service, take payment or
  erase the recorded breach. Insufficient prestige hides the paid apology option.

Ruler AI has all three options. War increases non-intervention weight and reduces
repair weight; positive provider opinion favors non-intervention; negative provider
opinion favors reprimand; positive client opinion favors repair. Provider opinion
of the mediator influences apology weight. These are provisional contextual weights,
not measured political behavior, guaranteed decisions or proven performance.

Both parties receive outcome notices. Information stays with the involved characters;
no global reputation score or automatic public disclosure is implied.

## Guarding decisions

Every public decision rechecks exact case identity, acting role/stage and **current**
shared jurisdiction. Realm/succession changes, deaths, an obsolete case or a stale
ruler popup must not authorize effects. Transition to the repair stage invalidates
the ruler's decision options. Closure marks the case closed before opinion/prestige
effects and notices, preventing a source-level replay route.

A thirty-day pending variable on each story and independent day-thirty-one callback limit the case;
asking for repair never renews the deadline. Expiry or jurisdiction loss closes
neutrally, without adverse effects. Old notices keep their own record even when later cases open. Destroyed records
render inert text. Lost/dead character scopes may prevent a callback; per-story
cleanup closes overdue records neutrally. Closed records are retained for 1825 days,
then cleaned periodically, or ended on owner death; no guilt transfers to heirs.
Actual event/flag timing, saved scopes and callback behavior require final engine tests.
No transactional crash-consistency guarantee is claimed.

Old experimental breach receipts without a recorded reason can still use personal
responses but cannot be referred; no evidence is invented during migration.

## Verification

Run the full unit/static suite and `python3 tools/validate_mod.py`. Mutation checks
cover unsupported allegations, wrong client/serial, lost authority, self-judging,
missing apology funds, early/repeated closure and rewriting the original breach.
Reference and EN/FR/BOM coverage checks also run. These inspect code structure and
wiring, not the game's trigger or effect semantics. No gameplay runs in Python.

## Final engine scenarios (none executed)

1. Explicit refusal and accountable timeout produce different factual descriptions.
   Fulfillment, neutral cancellation and invented/stale receipts cannot open a case.
2. Referral is available to human and AI clients only with a separate common ruler.
   A ruler who is a party, different realms, no common superior or minority/death
   cannot authorize mediation. No referral to a global or invented arbitrator.
3. Run decline, reprimand and repair invitation separately. Observe contextual AI
   choices under war and changed relations, without asserting deterministic outcomes.
4. Apologise with sufficient prestige: exactly -25 and the two +5 opinions once.
   With insufficient prestige or deliberate refusal: no forced deduction/penalty.
   Confirm the original breach and service payment remain unchanged.
5. Replay/double-click old ruler and provider popups after stage transition, closure
   and a new case. No second prestige cost/opinion/notice and no new-case cleanup.
6. Change lieges or ruler, kill/unland a party, or wait thirty-one days at each stage:
   close without a sanction; preserve native realm/title/war behavior.
7. Save/reload at referral, ruler decision, repair and closure; inspect scopes/logs.
   Verify notifications to both parties and inert superseded notices. Test no
   inheritance of personal guilt and verify the AGOT-only baseline/performance.

Broader evidence systems, discretionary severe sanctions and dynastic restoration
remain future work; they must not be inferred from this narrow service-breach case.
