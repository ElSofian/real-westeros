# Conditional political rehabilitation — experimental CK3 scripts

**Static-checked, not engine-tested.** This joins the institutional house register to
one explicit negotiated consequence: a current sovereign may answer a current head's
petition with **50 personal gold in exchange for closing this exact political censure**.
The head can accept, refuse or ignore. It is not a compulsory house fine, inherited
debt, confiscation, native status restoration or landholding-ban implementation.

## Offer and informed choice

The existing petition/reply checks remain authoritative: exact story/house/authority/
serial/revision, living adult free current head, qualified current sovereign, no war,
active original decree and thirty-day pending request. The ruler retains free
rehabilitation, refusal and inaction. A counteroffer consumes the original reply window,
increments revision before notification, records a fixed price of 50 and offer date,
and opens a separate thirty-day terms window. It changes no gold or original decree
term and does not restart the institutional one-year petition cooldown.

The head receives the whole exchange, amount, personal payer, institutional payee,
deadline, refusal/inaction and native-rights limits together. The current record can
reopen those same terms without a new offer, charge or timer. The personal treasury
must contain at least 50 gold at the actual acceptance, not just when shown. An
insolvent head can still refuse or leave it unanswered; no debt/loan is created.
The same effects, requirements and price apply to AI/player. Authored AI weights are
choices, not special execution permissions; no family scan or recurring AI retry.

## Settlement and replay protection

Acceptance revalidates the exact current head, addressed sovereign/title holder,
peace, live term/window, exact price and current record revision. It closes only this
censure and removes both request windows before gold effects. Then the consenting
head loses 50 and that exact current addressed sovereign receives 50. The receipt
records payer/payee/date only after both money effects. Old popups, duplicate responses
and another authority's record cannot repeat the transfer or close a different decree.

This is an ordered CK3 effect chain, **not a demonstrated atomic engine transaction**.
If the engine interrupts/fails partway through, no rollback/recovery is proved. Final
runs must check both balances, closure, receipts and save/reload together; do not infer
settlement from a UI click or mere closure. Consuming before money avoids ordinary
replay but cannot by itself prove every effect completed.

Paid settlement grants no extra +10 personal goodwill; the existing gratuitous
rehabilitation's bounded goodwill stays separate. Old -20 resentment, native reasons,
prison terms, claims, title ownership, house membership and other authorities' censure
remain untouched. Closing starts the existing fifty-year closed-record retention;
the original fifty-year active term is never renewed. Only the existing role-filtered
readers can inspect the political settlement; private plot pointers are not copied.

## Refusal, withdrawal, expiry and succession

Refusal consumes the terms window, increments revision and records refusal; no money,
new penalty, debt, goodwill or deadline extension. Silence fails acceptance as soon as
the thirty-day window expires. The existing sixty-day maintenance records unanswered
terms or, if still in-window but no longer valid, invalidates them once. Neither path
sends recurring notices. A current sovereign can withdraw the censure while terms
are outstanding, closing without payment; old acceptance then fails.

Current head/ruler changes, death, imprisonment, war or loss of qualifying sovereignty
block acceptance immediately. A matching party's story-owner death invalidates open
terms before custody transfer even if native alive flags have not settled. No debt
or consent passes to heirs. New legitimate head/ruler can replace the request under
the existing role-change cooldown exception; that clears old terms/price/date and
requires a new explicit offer/acceptance. A still-valid counteroffer cannot be
replaced by a fresh petition. Recorded invalid terms cannot revive after return to
old roles. A change and reversal between observations can still go unrecorded.

Only read-only refresh ignores an old revision to reopen the same still-readable
record. It neither settles nor silently accepts a replacement offer. No new native
hook, timer, law, forced interaction, status trait, legal immunity or diagnostic
add-on is required. Existing schema-1 records need no term/identity rewrite; actual
old-save migration and ownership persistence remain untested.

## Native sanctions boundary and next work

The source review also located native celestial family extinction: its celestial
supreme-ruler/noble-family-title and human-actor/AI-recipient requirements do not
establish a Westerosi sovereign's general house-sanction right or AI parity. Native
inheritance restoration likewise has dynasty-head, renown and AGOT human-recipient
conditions. G3_SOURCE_RECEIPT.json contains hashes/relative markers only. Neither
interaction/helper is copied, force-run or widened. Existing AGOT lordship conversion
remains distinct from house-wide nobility loss and a fifty-year landholding ban.

Fifteen new adversarial source-contract tests cover stale roles/revisions, funds,
price, consent, two-leg ordering/receipts, refusal, silence, death/replacement,
fixed deadlines, AI/player graph and absence of native mutation. TERM-01…10 final
scenarios remain unrun. Target metadata stays CK3 1.19.* / AGOT 0.5.2.1; no runtime
compatibility claim. The subsequent title-route intake reviews native grant/election
entry definitions absent from the earlier subset; see TITLE_ROUTE_AUDIT.md. G3's
four acquisition-route gate remains unresolved; G1 stays for the war stage.
