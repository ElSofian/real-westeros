# O4 — voluntary dynastic endowments

**Original CK3 scripts; static-checked, not engine-tested.** This implements one
private dynastic undertaking, distinct from personal promises and public Crown
charters. It is not a bank loan, a will, an estate reservation, forced inheritance,
a title transfer or a completed general contract framework.

## Playable source flow

A living adult landed free house head at peace may propose a fixed **50-gold legacy
endowment** to a different house's eligible head. The proposal explicitly permits
future heads of those two named houses to consult its private record, while leaving
them free to recognise it or refuse it. Native auto-accept creates only the proposal;
the original recipient must explicitly accept within seven days. Original people,
houses, issue date, amount, owner-local serial and revision are frozen at creation.

The original heads must still hold their respective roles at acceptance. A pending
offer is not inherited: death, replacement or expiry cannot let another person accept
for a predecessor. There is one live directed-house-pair proposal/pact, and an annual
proposal cooldown per proposer. AI only considers its direct liege and uses the same
eligibility and effects. No money is taken at proposal or acceptance; no escrow or
inherited financial account is created.

Acceptance starts a fixed **9,125-day (25 × 365) window**. Initial consenting people
are recorded separately from the two original signatories and from current headship.
A new head must personally recognise the unchanged undertaking; owning the house or
storing the record does not copy consent. Either side's current eligible head can
recognise, and a later change of either head invalidates the old person's ability to
act for that role. Recognition advances the revision without restarting the deadline.
The model retains the latest named recognition per side, not an exhaustive reign log;
an unobserved temporary role reversal is not claimed to be completely reconstructed.

After the **original benefactor has actually died**, the current contributing head
may choose to honour the promise, only if both current heads have personally recognised
it and the contributor currently has 50 gold. Both heads must be living, adult,
landed, free and at peace for performance. The original dead person's assets are
never debited. The live contributor pays their own 50 gold to the live beneficiary
head's personal purse; no house treasury or bank ledger is touched.

Payment rechecks private identity, origin/serial/revision, current houses/heads,
original death, both named recognitions, deadline and funds. It consumes the active
state and stores exact actual payer/payee/date before debit, credit and notices.
Old windows cannot replay the exchange or substitute successors into a paid receipt.
These are ordered native effects, not atomic crash recovery; do not retry a partially
executed exchange based on a missing notice. Original and actual payment parties may
read their retained history even after losing headship.

The current contributing head may refuse to carry the undertaking forward, and the
current beneficiary head may release the other house. These free exits require only
the acting adult free head's current role, not the other head's health, funds or war.
They do not inherit blame or change native debt. Original/private readers can withdraw
or decline an unaccepted proposal. Waiting and expiry are neutral. No default penalty,
crime, hook, title, prestige, public memory or universal reputation effect is applied.

## Private persistence, storage and opportunities

One independent `story_rw_dynastic_pledge` stores the undertaking and an isolated
`rw_dynastic_pledges` index supports discovery after succession. Readers are the
original signatories, current heads of the exact two houses and actual paid parties;
being a custodian, relative, liege or another house member grants no access. Becoming
head grants the knowledge explicitly allowed by the proposal, never consent.

Storage can move to a living current head or original signatory. Owner-death handling
explicitly excludes the departing person even if native alive/head flags have not
yet settled, and never transfers money or recognition. A local sixty-day maintenance
cycle reconciles heads, neutral offer/term expiry and custody; it scans no world
character pairs. If no legitimate living custodian survives, the story is unindexed
and retired; it is not handed to a convenient outsider. Callback ordering and actual
survival across simultaneous deaths still require engine evidence.

Terminal history is retained for at most five more years, within an absolute
**10,957-day cap** from creation (30 × 365 + seven proposal days), which is never
renewed. Expiry display/actions fail closed immediately on timed-marker loss; neutral
terminal-state cleanup may lag until the next sixty-day cycle. Retirement removes
the index entry before ending the story. No permanent orphan index is intended.

Notices coalesce current-person/revision changes before one-day queued opportunities.
A contributor who becomes eligible and able to pay gets one additional readiness
opportunity per revision; readiness is not separately disclosed to the beneficiary.
No recurring demand or guaranteed AI performance is claimed. The private register
remains manually accessible. Snapshots/refreshes never renew terms or accept anything;
a stale panel must refresh exact record/serial under current private access before
acting. A stable read identity prevents nested notices changing the next record's reader.

## Boundaries and available checks

Only original additive CK3 files are introduced. Existing story/index/headship
patterns are described in RW010_HOUSE_AFFAIRS.md and RW010_RESTITUTION_CHARTERS.md,
with their existing source receipts. No new proprietary source is copied. Native
banking/debt inheritance, titles, succession, wars/Mega Wars and public/private evidence
systems are untouched. Source reuse does not establish CK3 1.19.* / AGOT 0.5.2.1
compatibility, lifecycle semantics, save/load correctness or actual AI performance.

Fifteen adversarial source tests cover typed/origin/serial/revision identity, private
readers, noninherited pending consent, explicit current-head recognition and death,
actual personal funds and once-only ordering, fixed timers, free exits, departed-owner
exclusion, storage/consent separation, index retirement, bounded AI/notices, privacy
and EN/FR references. They do not simulate CK3 inheritance or banking.

Frozen O4 source criterion: explicit dynastic private undertaking with voluntary
successor lifecycle. **45 → 47/100 (+2 source), engine 0/20.** This does not certify
all patrimonial arrangements, banking compatibility or the ultimate promise catalogue.
Next target: **I3**, controlled rumor propagation; G1/G3 and final game tests remain open.

## Final campaign — no scenarios run

| Case | Check / expected result |
|---|---|
| DYN-01 | Valid distinct heads propose/accept within seven days: exact original people/houses, 50 amount, no money/claim/hook/escrow on proposal/acceptance. Refusal/withdrawal/expiry are neutral. |
| DYN-02 | Original head dies or is replaced before acceptance, including new head reusing an old popup: no inherited acceptance or duty; pending offer lapses, original facts remain. |
| DYN-03 | Accepted benefactor dies: record survives via a legitimate other head/signatory, departing person excluded even before native death/head flags settle. New head can privately review but is not yet recognised. |
| DYN-04 | New contributing head recognises; new beneficiary head, if changed, separately recognises. No payment until both exact current names match; recognitions do not restart due/cap timers. |
| DYN-05 | Original benefactor still alive after losing headship: no premature performance. After actual death, valid current contributor with ≥50 gold chooses to pay once; verify −50/+50 on actual personal purses and exact terminal receipt. |
| DYN-06 | Below 50 gold, changed head/house/revision, imprisonment/war, expired deadline, foreign/obsolete record or lost access at click: no payment. Newly recovered capacity gives one payer readiness opportunity, no recurring demands. |
| DYN-07 | Renounce/release while the other head is minor, imprisoned, unlanded or at war: free exit remains available for the acting adult free current head. Neither side incurs native guilt or forced transfer. |
| DYN-08 | Custodian dies; current heads change repeatedly, including minority, house extinction and simultaneous deaths: legitimate storage only, no consent from custody, explicit retirement if no valid custodian remains. No complete transient-reign history claimed. |
| DYN-09 | Save/reload pending, accepted, unrecognised successor, both recognised and paid. Two copies of a payment popup cannot pay twice. Paid history continues naming actual payer/payee after later head changes. |
| DYN-10 | Original signatories/current exact heads/actual paid parties can read; custodian-only outsider, liege, other member/house cannot. No private endowment appears in native public memories or another political dossier. |
| DYN-11 | Observe neutral offer expiry, 9,125-day active expiry, five-year terminal history and absolute cap; index removed before retirement. Reads/refresh/recognition never extend clocks. Duplicate pair proposals and stale reader serials fail closed. |
| DYN-12 | Human/AI initiation, refusal, successor recognition, voluntary payment/nonintervention and bounded notices; measure final G4 spam/performance. Regression-test native bank loan/debt inheritance, estate/title succession, AGOT wars, hooks and other contracts unchanged. |
