# I3 — controlled propagation of unverified accounts

**Original CK3 scripts, static-checked; not engine-tested.** This introduces actual
character-to-character knowledge transmission, independent of legal facts. It is
one structured topic, not a complete rumor/belief simulator or a runtime Python model.

## Source and transmission

The original claimant of a current answered house-affront allegation may prepare
their own account for later sharing. Existing case kind/identity, original claimant
turn and current jurisdiction are rechecked; a mediator, respondent, generic plot
observer or stranger cannot originate that claimant's speech. Preparing the account
informs only its own speaker. The original claimant dialogue resumes one day later
without renewing its existing thirty-day deadline; referral/withdrawal remain separate.
One source case can start only one lineage, after successful initial packet creation.

The copied topic is only **“the named speaker had alleged an affront by the named
subject.”** This is a historical report of an allegation, not proof of an insult,
current maintained accusation, admission, native crime or house guilt. The respondent's
reply, contested/admitted status, mediator, source-case pointer/serial, private price,
settlement, favor, plot and dynastic contract are never included in the payload.
The publication date is the first preparation/publication of this account, not a
fabricated date of the alleged underlying act.

A holder selects a recipient through a targeted **Pass on an unverified account**
interaction, reviews a specific personal account and explicitly chooses whether
to send. The native menu filters out retired accounts and the sender’s own prior targets; execution
rechecks exact packet owner/serial, original speaker/subject/lineage/date/hops,
lineage lifetime, actual living/free adult landed sender/receiver, diplomatic range,
the sender’s own previous attempts and sender cooldown. War is not itself a ban on communication.
The actor's owned packets are enumerated, not world character pairs or a global
latest-rumor slot. New knowledge is registered before the next-day UI notice.

Each personal packet preserves the original named speaker, original lineage serial
and publication date; delivery records the actual immediate sender, recipient through
ownership, hearing date and incremented hop count. A relay is never relabeled as the
original source. A listener merely knows that they were told this account; reading/
acknowledging it stores no belief, agreement, corroboration or guilt. Human and AI use
the same guarded actions; AI initialization targets its direct liege, and confirmation
always permits keeping the account to oneself.

## Echoes, aging and private knowledge

An independent story with immutable origin fields holds a fixed **365-day diffusion window**
and the set of informed characters. A recipient receives at most one packet from
that lineage: an A→B→C→A attempt or repeated telling by different messengers creates
no extra receipt, renewed hearing date or independent evidence. The internal recipient
set is consulted only when constructing knowledge, never as a sender-facing query.
A sender remembers their own attempted targets and cooldown equally whether the
recipient was new or already knew the story through someone else. Therefore the menu
cannot reveal B→C to an uninformed A. Different source cases remain separately identified, never
counted as proof by this feature. There is no universal reputation/confidence meter.

Relays cannot renew the lineage window or change its source date. A valid
non-self sending attempt records its target in that sender’s personal packet and gives
the sender a shared thirty-day relay cooldown before any notice. Receiver deduplication
does not reveal itself through a different sender cooldown or success report. Invalid
or canceled confirmations create no knowledge, cooldown or legal effect.

Only the personal packet's owner may read it; its retention is **365 days from hearing**,
so a final received copy can remain historical for up to a year after diffusion stops.
Read/refresh never extends either clock. Historical packets remain readable after
origin retirement, but cannot be forwarded without the original live lineage. A lost
lineage, expired clock, dead subject or failed link is not evidence about truth.
Packets end on their owner's death; heirs do not inherit private hearing automatically.

An origin custodian's death may move only its internal lineage record to an already
informed living holder with a matching retained personal copy. The departing person
is explicitly excluded before native alive flags need settle. Custody grants no new
knowledge or view of other recipients; the holder set is internal deduplication/storage
data and is not a public graph. If no legitimate holder survives, the origin ends.
Local sixty-day cleanup ends expired/malformed roots and packets. No global index,
world pair scan, recurring notification or source-case ownership change is added.

The original private case remains private. Sending hearsay to its planned mediator
DOES NOT set the original disclosure marker or grant that ruler dossier access.
No native secret/reason/bloodline/claim, war, hook, money, prestige, opinion, public
memory or punishment is created. Withdrawal or a private settlement does not silently
erase past speech or become a retraction. This slice adds no retraction/verification
protocol, persuasion policy or automatic sanction; those remain separate work.

## Source confidence and checks

`RUMOR_SOURCE_RECEIPT.json` records only relative paths, hashes and syntax lines from
the supplied native sources for variable lists, known-list iteration and diplomatic
range. No original native source/assets are committed. Existing story/owner/packet
patterns do not prove variable-list scope, save/load, event snapshot or callback
semantics on target CK3 1.19.* / AGOT 0.5.2.1. All compatibility remains unverified.

Fourteen adversarial source tests cover claimant-only seeding, personal access, stale
snapshots, stable original/relay/recipient provenance, A→B→C→A echo rejection, fresh
range/cooldown/lifetime checks, direct effects, no private truth/financial export,
attempt/cooldown-before-notice ordering, no hidden-audience queries, informed-only custody and EN/FR references. Existing
allegation evidence/disclosure/read-only checks remain. These tests do not execute CK3.

I3 source credit: **47 → 49/100 (+2)**; engine **0/20**. The frozen rubric and old
checkpoints remain intact. This is not M5 (memory affecting future independent
choices), a complete information system or proof of actual performance. Next: **M5**.

## Final campaign — no scenarios executed

| Case | Check / expected result |
|---|---|
| RUMOR-01 | Valid original answered-allegation claimant prepares one account. No disclosure to anyone else, no case deadline renewal or reply/evidence change; existing decision resumes. Respondent/mediator/outsider/wrong kind/stale claimant cannot seed. |
| RUMOR-02 | A selects B, confirms: B gains exactly one personal packet with A as original speaker and immediate sender, same lineage/publication date, hearing date now and one hop. Cancel/keep changes nothing. |
| RUMOR-03 | B tells C: C keeps A as original speaker and B as actual immediate relay, same origin/date, incremented hops. No wording calls this verified or an admission. |
| RUMOR-04 | C→A and other senders→already informed B create no new packet/notice/date or corroboration. A sender cannot infer another sender’s audience from menu validity or cooldown. Own repeated targets and stale confirmations are blocked. |
| RUMOR-05 | Receiver moves out of range, dies/is imprisoned, subject dies, source/packet expires or ownership/serial/metadata changes before confirmation: no new delivery or fabricated replacement/heir. |
| RUMOR-06 | A claimed in an admitted/contested or later withdrawn/settled case: outgoing text contains neither reply nor finances/outcome. Planned mediator who hears rumor still cannot browse the original undisclosed case. |
| RUMOR-07 | Packet owner can read; original speaker/custodian/liege/heir/stranger cannot read someone else's receipt or see/query the global listener set through sender menus. Native duplicate handling gives no different sender success signal or cooldown. No native evidence/reason/secret/public memory or penalty is created. |
| RUMOR-08 | Root custodian dies before native alive/head flags settle: only an already informed live packet holder may store the root; original source remains named. Packet owner's death ends that personal packet, without inherited knowledge. |
| RUMOR-09 | After root's fixed 365 days, all relays stop despite a recent packet. Own retained history remains unverified until its hearing-based expiry; reads/relays/custody never reset source age. Local cleanup retires data neutrally. |
| RUMOR-10 | Save/reload before/after preparation, delivery, two confirmations, custody and retirement. Confirm StoryScope variable-list storage, independent event receiver snapshots and scalar/hop/date preservation. |
| RUMOR-11 | Human/AI origin and intermediate senders, direct-liege AI targeting, explicit keeping/relay choices; measure G4 message volume, loop suppression and performance without global pair searches. |
| RUMOR-12 | Target-version G5 regression: source case evidence/referral/settlement, other private contracts, native secrets/justice, titles/banks/AGOT wars retain normal behavior. Native no-range/invalid-recipient paths fail closed. |
