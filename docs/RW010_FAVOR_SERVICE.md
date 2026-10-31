# Immediate endorsement for native favor or negotiated gold

**Original CK3 scripts; source/static-checked, not engine-tested.** This authored
service adds a non-monetary consideration alongside gold. It is not a new native
hook type, a future promise, an unlawful-war bypass or proof of compatibility.

## Explicit offer and latest-term consent

A landed adult free provider at peace can offer a landed adult free client an
immediate endorsement in exchange for a native **`favor_hook` over that client**.
The new interaction's auto-accept only opens the scripted proposal. No prestige,
hook or gold is granted until explicit latest-term agreement.

The client may accept favor terms or counter with **25 gold instead**. The provider
may accept that exact gold counteroffer or restate favor terms. Each counter changes
revision, term and responder; the next reply arrives after one day. Serial, revision,
provider/client identities and favor-versus-gold term must all match. Older panels
cannot close, perform or change a newer offer. The fixed original thirty-day pending
marker is never renewed by counters, waiting or review; silence has no penalty.

Both parties must still be alive, adult, landed, free and at peace under the existing
service eligibility policy when acting. Favor acceptance belongs only to the client;
gold acceptance only to the provider after the client's counteroffer. The original
client always pays gold to the original provider, independent of the clicking actor.
Client poverty disables gold settlement, not countering or identity-only closure.
Either original living party may close an exact offered ticket after expiry, war,
detention or lost eligibility, without payment, prestige, hook, blame or refund.

## Preserve native hook ownership

The received AGOT and CK3 grant definitions locate native `can_add_hook`/`add_hook`
with `favor_hook`; the AGOT diarch definition locates `has_hook`. Three files were
hash/size checked against the received private manifest. FAVOR_SERVICE_SOURCE_RECEIPT.json
publishes selected relative paths, hashes, sizes and marker positions only.

Before offering, accepting or restating favor terms, the provider must have **no
hook detected by native `has_hook` on this client** and pass native
`can_add_hook = { type = favor_hook target = ... }`. These checks repeat at actual
performance, so a detected intervening hook blocks favor terms rather than being
refreshed or overwritten. A gold counteroffer may still be accepted without changing
that existing hook. The opposite-direction relationship is not spent or rewritten.

The code neither defines nor overrides `common/hook_types`. Native favor strength,
duration, cooldown, usage, expiry, visibility, inheritance and restrictions remain
native. This source selection does not contain an effective hook-type/playset proof;
no custom strength/duration or universal no-refresh guarantee is invented. Strong,
weak, unusable/cooling-down and otherwise hidden/pending states must be exercised in
final tests. Native predicate behavior is not demonstrated by locating its syntax.

A later use of this favor is a separate native decision. This code never spends it,
sends another interaction, grants a title, clears a crime, changes realm law or
starts a war. G1 remains open for genuine unlawful-war development; an ordinary
native favor is not a replacement for that feature.

## Once-only immediate performance and provider pool

Before any native effect, the exact current acceptance consumes the pending marker
and turn, records completion date and terminal fulfilled state. Then **one** selected
branch executes: native favor over the client, or client −25/provider +25 gold. The
client receives 50 prestige for the endorsement once, after that branch, and the two
original participants receive the outcome. No gold is taken under favor terms and
no favor is added under gold terms. Closure and inaction perform neither branch.

Ordered native effects are not an atomic engine transaction or crash-recovery
protocol. Metadata may not prove every effect completed after an interruption;
never automatically retry partial hook/gold/prestige effects. Final tests must
establish actual balances, hook identity and reentry behavior before gameplay claims.

This shares the existing yearly **provider service cooldown**, started on proposal,
and conservative one-active-provider service pool. Gold/deferred offers and favor
offers cannot bypass each other's pending/obligation/cooldown guards. A new independent
favor-pending flag is used; the original financial pending/obligation flag is never
reactivated. Old financial serial/quote/target/mode/receipt fields remain untouched,
so an old ignored quote cannot become active merely because this offer starts.
The old flags/variables are not reused as a favor consent ticket. The original
single-slot limitation remains an explicit slice limit, not a global action cap.

Each provider keeps only its **latest** favor-backed offer/receipt in separate
character variables, with monotonic serial and versioned current term. Private
review targets that provider and permits only the provider or captured current
client to read. Reading captures current terms into a fresh panel, never renews,
pays or grants. New offers overwrite the latest slot only with a new serial; old
readers/panels become inert. No complete archive or dynastic transfer is promised.
Death/reference loss disables performance; no scripted obligation transfers to an
heir. Actual native hook lifecycle remains the native type's responsibility.

## Separate deferred-mode extension

RW010_DEFERRED_FAVOR.md now adds a distinct personal promise interaction. New
records bind explicit original provider/mode; legacy missing-mode rows are treated
as immediate only, with no inferred future duty. Immediate acceptance keeps its
existing effects and explicitly excludes deferred tickets. Shared availability
also blocks active deferred favor obligations. Deferred consent, later execution,
withdrawal/renunciation and neutral cleanup are described separately there.

## AI, checks and final campaign

AI/player share every effect and execution guard. Bounded liege targeting and
existing availability constrain initiation; traits influence willingness to concede
a favor or pay gold. Cosmetic manual review has AI weight zero because versioned
reactive replies supply choices. No world scan, new story/index, native on_action,
periodic reminder, paid service, runtime Python or LLM is added.

Eighteen adversarial source tests cover native eligibility/detected existing hooks,
full ticket/party identity, current responder/currency, affordability, shared pool
isolation, fixed clocks/serials, delayed versioned counters, consumption/effect order,
correct hook and gold directions, free closure, private latest review, AI symmetry,
hash-only references and EN/FR strings. They inspect code, not a native favor or a
Python gameplay simulation. FAVOR-01…12 final scenarios remain unrun.

Next broader service/consideration and obligation types, with consent, facts and
native authority separate. Native API/old-ticket isolation, actual AI rates, economy,
persistence and compatibility/performance all remain engine-unverified until the
owner's final campaign; no intermediate run or new source upload is requested.
