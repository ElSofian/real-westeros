# Deferred endorsement for a future native favor or agreed gold

**Original CK3 scripts; static-checked, not engine-tested.** This adds a personal
promise mode to the favor-backed service. Consent does not perform the service or
grant consideration. Immediate offers remain a separate explicit interaction.

## Exact negotiation, then consent without payment

Both interactions use the existing favor/gold counteroffers and private latest
provider record. New offers store explicit provider identity and mode. Every view
compares captured mode with stored mode and original provider; a copied successor
record is not authority to act. Mode-less legacy tickets can be reviewed as
**immediate only**, never inferred as deferred duties. Older popups lacking a mode
cannot spend; fresh manual review may recover an otherwise eligible immediate view.
No old consent, missed event or inherited obligation is reconstructed.

Client favor acceptance and provider gold-counteroffer acceptance still require
current latest responder/term/serial/revision and current native eligibility/funds.
In deferred mode, explicit acceptance removes the offer marker/turn, increments
revision to invalidate all quote panels, records accepted date/promised state and
captures the accepted identity before scheduling decisions. No hook, gold, prestige,
escrow, new debt or automatic performance occurs. The original shared annual service
cooldown is never restarted by consent, decisions, performance or closure.

Performance is possible **after seven days and before thirty days from acceptance**.
A separate due marker fixes that deadline. Two original provider opportunities at
days eight and twenty-two open the existing private panel only while the accepted
promise is due/live. There is no automatic performance, rescheduling on waiting or
manual review, recurring reminder chain, world scan or new native on_action.
A separate original day-thirty-one timeout handles neutral closure.

## Performance remains a choice with fresh native checks

Only the captured original provider may perform a due promise. The complete private
provider/client/mode/serial/accepted revision/consideration must still match; both
parties must currently be living adult/free landed service participants at peace.
For native-favor consideration, NOT `has_hook` and native `can_add_hook` recheck the
same pair just before performance. A detected intervening hook is neither refreshed
nor replaced; current inability blocks performance rather than manufacturing gold
terms. For agreed 25-gold consideration, the original client must still have 25 gold.
The accepted currency cannot be silently changed after consent.

Terminal consumption clears obligation/due/wait flags and records finished outcome
before the one selected native favor-or-gold branch, client +50 prestige and notices.
The immediate settlement path explicitly rejects deferred mode. Older offer panels,
other actors, delayed provider opportunities and timeout replays cannot perform a
closed or newer accepted ticket. Ordered native effects are not an atomic engine
transaction or crash-recovery protocol; partial effects must never be retried.
Native hook strength/duration/use and bank/war/title/legal rules remain native.

## Freedom to renounce or withdraw, no automatic verdict

The original provider may explicitly renounce an accepted unperformed promise.
The original client may withdraw future consideration before performance. Exact
personal identity and current accepted ticket are required; present money, rank,
peace, freedom or native-favor availability need not permit performance merely to
close it. No hook is removed, money refunded, service delivered, automatic opinion
penalty/crime generated or debt transferred to an heir. Statements are recorded
separately as provider renunciation or client withdrawal, not native legal findings.

The expired original-provider callback checks immutable owner identity, mode,
serial/revision/term, accepted state and actual missing due marker before recording
neutral unresolved. That owner-only cleanup needs no surviving client scope and
can release an orphaned slot; it cannot authorize gold/hook/prestige. A missing
client prevents invalid-scope notices. Missing other immutable callback identity
fails closed rather than clearing an arbitrary newer promise.

The technical obligation-slot marker also expires after **32 days**, as a long-stop
if the timeout is lost. This is never extra delivery time: performance always needs
the original thirty-day due marker. Lost-callback latest history may retain promised
metadata, but renders expired/inactive as unresolved and cannot perform; the stale
slot cannot indefinitely block new service availability. Original shared annual
cooldown still applies. The usual immediate/favor/financial provider-pool guards
now also reject an active deferred-favor slot.

Private review is still limited to original provider/current captured client and
never changes terms/clocks. No complete historical ledger or save migration is
promised. Provider death/reference loss disables performance; personal latest-record
metadata is not an inherited service. Actual native favor lifecycle stays native.

## Verification and final campaign

Eighteen adversarial source tests cover explicit/legacy mode, original-provider
binding, exact consent, no native effects at acceptance, version invalidation,
immutable seven/thirty-day clocks and 32-day slot long-stop, two fixed opportunities,
owner-only orphan timeout, current native favor/gold eligibility, no early/late or
immediate-path spending, consume-before-effects, free original-party exits, shared
pool isolation, no coercive/global hooks, AI symmetry and EN/FR strings. Existing
immediate-service tests still apply. These inspect source, not a CK3 simulation.

DFAVOR-01…12 in FINAL_ENGINE_TESTS.md all remain unrun. The existing favor API source
receipt is reused; no new native API or third-party source is distributed. Game
scheduling, flag expiry, date/scalar snapshots, native effects, save/load, AI/economy
and performance remain unverified until the owner's final campaign. No paid service,
runtime Python/LLM, new file upload or intermediate CK3 run is requested. Next wider
service/consideration types and contextual consequences with explicit personal consent.
