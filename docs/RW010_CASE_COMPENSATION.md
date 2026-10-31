# Voluntary compensation for a closed service affair

**Original CK3 scripts; static-checked, not engine-tested.** This is an authored
financial-redress negotiation between the original service parties. It is not a
refund of a fee already paid, damages assessed by a court, a new debt, an admission,
a pardon, an automatic apology response or fulfillment of the original service.

## Offer, counter and explicit consent

From a retained closed service case, either original party may propose **25 or 50
gold from provider to client**. Client initiation is a request; provider initiation
is an offer. Their exact case story/type/owner/serial/client/mediator/reason/kind
must match the captured frame. Only service-kind cases qualify, not an allegation,
active case, ended story or unknown legacy kind. Present land/rank/jurisdiction is
not required for a personal financial gesture. Both must currently be living adults,
free and at peace with each other to propose, counter or settle.

A new per-case schema records amount, revision, issue date, responder and one fixed
seven-day window. Either amount may be proposed regardless of current funds; funds
are checked again when accepted. The other party alone may agree, or counter with
the other amount. A counter increments revision, swaps responder and sends the other
party a panel after one day. The original window is not extended. There is no count
cap on counteroffers or unrelated cases, and no instantaneous AI counter chain.
One offer history per exact affair prevents restarting its window or repeatedly
paying for that same financial gesture. This is not a global limit on useful actions.

The same provider always pays the same captured client, whichever participant clicks
accept. The proposer consents by offering that exact amount; the current responder
must explicitly agree to that exact revision/amount. Neither silence, reading,
opening a dialogue, a counteroffer nor an overlord's decision authorizes payment.

## Payment and failure safety

Settlement repeats full private case/quote/role/current-capacity checks and requires
**actual provider gold >= the current agreed amount**. It consumes the offer window
and turn, writes paid amount/revision/date, and marks terminal `paid` **before** the
two native gold effects and receipt notices. Provider loses the selected 25/50 and
client gains the same amount. No actor-relative debit, automatic prestige/opinion reward,
third-party recipient, banking operation, title change or native penalty is added.
The provider's active/latest service contract and original receipt are untouched.

These ordered operations are not an engine-tested atomic transaction or crash
recovery protocol. A partial native effect/crash must not trigger an automatic
retry. Actual balances, same-tick reentry and persistence require final testing.

Poverty disables settlement and is explained in the panel; it does not block a
counteroffer or make a debt. Either original participant can close an unaccepted
offer with current exact identity even after poverty, war or detention. No funds
were reserved, so no refund/escrow exists. Expired offers become inert without a
new timer, punishment or notification. A case whose original retention ended cannot
authorize a new financial action; normal per-story cleanup ends it later.

## Separate private dialogue, fresh review and old replies

Client/provider result notices and known-case history open a **separate** dialogue.
The archive itself remains read-only. A guarded hidden fresh-entry event reads
current quote scalars before showing that dialogue; this refresh never pays or
changes stored state. Delayed reply events bypass that refresh and keep their
captured revision/amount, so stale replies cannot silently consent to newer terms.
Fresh navigation explicitly starts a new view of the currently stored offer.

Only the original provider/client can enter/read the compensation panel. Although
the informed original mediator can still read the original affair, this does not
permit access to its private financial terms, replies or receipt. No financial
notice is sent to that mediator, a new ruler, a house head or an heir. There is no
new global index or public export. The existing provider-owned case is reused;
original closed retention (1825 days), sixty-day cleanup and provider-death ending
are never renewed or transferred. Client death blocks payment; heirs inherit no
consent or obligation. Lost participant references fail closed rather than substitute.

Paying compensation never changes the original closed result, breach facts, copied
service clauses, evidence, personal resentment, native legal reasons or separate
apology acceptance. The client can receive money without forgiving. An existing
apology response retains its own original consent window and conditions. No promise
of restitution, native title-gain context or uncertain grant cause authorizes money.
This independent financial slice does not resolve voluntary-grant causal receipts.

## Independent personal response after a new payment

RW010_COMPENSATION_RESPONSE.md adds a separate original-beneficiary choice after a
new payment: appreciate the gesture (+5 personal opinion/two years only if absent,
without stacking/renewal) or acknowledge without rapprochement. The fresh thirty-day
window never changes financial consent, the original affair, resentment or pardon.
Old paid receipts get no invented response window; silence is not gratitude.

## AI, checks and remaining work

AI and player use the same effects, parties, current funds and consent rules. The
existing two result notices provide bounded opportunities; no new periodic/global
scan or native on_action is added. Cosmetic archive entry has AI weight zero. Initial
financial offers use small weights with trait/current-funds preferences; replies
retain acceptance/counter/refusal/inaction. This is source policy, not observed AI
behavior, a balanced economy or proof of G4 performance.

Eighteen adversarial source-contract tests cover exact private case identity and
retention, current availability, one initial window, bilateral response, typed
versioned receipts, actual provider affordability, consume-before-effects, fixed
debit/credit direction, delayed counters, fresh-versus-old review, free closure,
read-only archive, mediator exclusion, unchanged facts/justice, lifecycle/AI and
EN/FR strings. No Python model simulates a CK3 payment or political consequence.

COMP-01…12 final cases remain unrun. All engine testing stays in the owner's final
campaign. No original CK3/AGOT assets, paid service, LLM, runtime Python or additional
upload is needed. Next broaden structured consideration and other service/obligation
types while preserving exact consent, facts and native ownership of legal actions.
