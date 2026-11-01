# Voluntary negotiated withdrawal of an allegation

**Original CK3 scripts; static-checked, not engine-tested.** A second concrete
service now exchanges gold for withdrawal of one exact mod-created allegation,
rather than prestige or a native legal privilege. This applies only to the existing
house-affront allegation, not native secrets, discovered murder schemes, service
breaches or sanctions. The underlying offense is not independently established.

After an acknowledgment or contest, the claimant may propose withdrawing the
allegation for **50 gold paid by the respondent to the claimant**. The respondent
may accept, refuse, wait or counter **25 gold**. The claimant may accept the counter,
end talks or maintain fifty for the respondent to accept again. Each counter
increments the quote revision, swaps the responder and captures the current price.
Only the other party's explicit acceptance of those exact terms can settle; neither
proposing, negotiating nor merely reading moves money or withdraws the case.

One fixed **seven-day** dialogue window is allowed per exact allegation; it also
requires the original **thirty-day case deadline**. Counters, refusal, notices and
archive review renew neither clock. There is no recurring reminder. One-day reply
notices use the current captured quote; stale delayed panels do not refresh on load.
This per-case dialogue limit prevents restarting negotiations to extend a deadline,
not a global cap on useful interactions. Original allegation initiation cooldown
still applies; no new repeated-pair/world scan is added.

## Freedom and current circumstances

The claimant remains free to refer the allegation to the common overlord or to
withdraw without payment, even during negotiations. These original actions retain
their existing guards/effects. Either changes the case stage, so every old financial
panel immediately fails the live settlement guard. Refusing settlement only closes
the financial dialogue; it neither closes the allegation nor creates resentment,
guilt or a forced referral. Silence/expiry is not agreement or a payment.

Settlement rechecks exact typed story/owner/client/mediator/serial/reason identity,
original parties, current common jurisdiction, claimant stage, non-disclosure,
original pending window and acknowledged/contested statement. Both must still be
living landed adults, free from imprisonment and not at war with each other.
Unanswered, already referred, closed, expired, wrong-kind or successor cases cannot
settle. The original respondent must still hold the **current agreed price** at
acceptance, even when the claimant clicks acceptance of a twenty-five counteroffer.
No escrow, borrowed money, partial charge, automatic retry or substituted payer.

## Once-only payment and preserved facts

The exact offer is consumed and stores paid amount/revision/date, then the active
case is closed as withdrawn with the same original five-year retention used by a
free withdrawal. Both consumptions precede the original respondent's debit and
claimant's credit, then private notices. Replays cannot debit again or act on a newer
counteroffer. These ordered effects are not an atomic native transaction or crash
recovery; no attempt to retry a partial native exchange is added.

Neither settlement nor free withdrawal changes the original acknowledgment or
contest. Payment is not evidence of underlying guilt, a false accusation, native
crime, pardon, apology or immunity. No prestige, opinion, hook, secret, arrest,
claim, title or native penalty is created/cleared. Existing affairs remain separate.
The new dialogue never invokes service-compensation/paid-response effects and never
rewrites their fields. No obligation is inherited and no native lifecycle is changed.

Original parties can reopen a fresh private dialogue view from the record archive;
that explicit navigation only captures current terms. The archive does not propose,
settle, reopen a closed matter, refresh retention or infer missing consent. Paid
terms remain readable while the original personal story survives. The planned or
later disclosed mediator cannot read these financial terms; only the allegation
itself is disclosed if the claimant chooses referral. There is no claim that this
withdrawal prevents later new allegations or native discovery.

## AI, verification and remaining risks

AI and players use identical actions, costs and guards. Existing claimant response
opportunities now include a settlement proposal; both reply actors use shared
versioned options. AI acceptance weights consider a recorded acknowledgment,
greed and current personal hostility; refusal, counter, free withdrawal and referral
remain possible. Weights/economy/spam incentives are provisional, not calibrated or
observed in CK3. Strategic allegations remain possible under the existing model.

Twenty adversarial source tests cover private typed identity, jurisdiction/stage/
disclosure/deadlines, initiator/responder, once-per-case window, current payer funds,
versioned counters, no premature charge, both consumptions before gold/notice,
retained facts, neutral refusal, archive navigation, AI parity and EN/FR. They are
not a gameplay simulation. ASET-01…12 in FINAL_ENGINE_TESTS.md remain unrun;
saved-scope arithmetic, event ordering, actual UI/AI/privacy/save/load/economy,
native effects and AGOT compatibility need the final campaign. Existing gold/story
APIs are reused; no proprietary script, new source upload, paid service, runtime
Python/LLM or intermediate game run is required.
