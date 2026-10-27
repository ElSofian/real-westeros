# RW-010 — independent political-case records

**Experimental CK3 story scripts; not engine-tested.** No Python gameplay/history
simulation, external database, paid service or changed AGOT story is used.

## Scope

Each approved service-breach referral or separately raised affront allegation creates its own `story_rw_political_case`,
owned by the provider. Its serial, client, mediator, reason, stage, deadline and
result belong to that story. New records do not overwrite earlier records. Each
callback carries the actual story scope plus the expected provider/serial/parties/
reason. Matching checks type and owner as well as these identifiers. This supports
multiple retained referrals without a count cap; the current service pipeline still
has one active offer/obligation per provider and a yearly offer cooldown.

Service referrals and the separate allegation kind are archived here; allegation
records exist before ruler disclosure and restrict access accordingly. The service
engine still stores its latest service receipt, so this is not an archive of every unreferred promise,
a general evidence ledger, a house history or dynastic persistence implementation.

## Creation, closure and expiry

A separate story is created for each valid referral. The client's receipt-response
opportunity is consumed only after a story exists and before decision delivery.
No provider-global case-pending lock remains. Ruler/provider turn, authority and
expiry checks use the selected story; closing one must not modify another story
or the current service negotiation. Original breach facts remain unchanged.

Closed records retain the outcome for **1825 days after closure** (about five years).
A passive per-story check every 60 days ends records after that retention expires;
actual removal can therefore lag the retention deadline by up to one check interval.
There is no global character-pair scan or random/count-based eviction.

The same check neutrally closes an overdue active record if its day-31 callback
was lost, then starts its retention timer. It does not apply sanctions, costs,
notifications or original service effects; it requires no surviving participant
scope. Normal callbacks still deliver the outcome notices. Real scheduling and
performance require final engine verification.

`on_owner_death` ends the provider's stories. There is no `make_story_owner` or heir
transfer: this personal memory ends on owner death, even before five years. Client
and mediator characters do not own replicated copies. Preserving evidence across
death/house restoration is future G3 work, not a claimed feature of this slice.

## Read-only consultation and privacy

**Review Known Political Cases** targets a provider. It enumerates only that
provider's case stories and filters by the reader's stored role: provider, original
client or original mediator. It then delivers a read-only notice per known record,
including active ruler/repair stages or closed outcomes. The planned mediator role requires recorded disclosure (RW010_ALLEGATIONS.md). Current rank is not required
to remember a previously disclosed case, but decision effects still require current
jurisdiction. Outsiders cannot query private cases through this interaction.

Reading known records does not require diplomatic range; stored-role filtering still
applies. Neither archive reading nor notification acknowledgement can settle, reopen,
re-sanction, charge prestige or extend deadlines. Superseded/destroyed story scopes
render inert text. Lost participant references may make a record unreadable but must
not reveal another case or authorize effects. AI uses the guarded political events;
it does not launch cosmetic archive browsing. This is a basic native-popup archive,
not a dedicated sortable journal GUI.

## Source basis and migration

The privately supplied AGOT story scripts use `create_story`, `story_type`,
`story_owner`, `on_owner_death`, `every_owned_story` and periodic `effect_group`.
That supports the API choice, not proof of this new story's engine behavior. Timed
variables, story scope persistence, per-iteration event scope capture, self-targeted
archive visibility and save/load still need runtime testing.

Old provider-slot cases from earlier experimental builds are not reconstructed into
stories: doing so would invent missing context. Their old callbacks cannot satisfy
the new story identity check. Legacy pending character flags expire without being
consulted by the new code. Prefer fresh disposable saves for final testing; no old-save
migration compatibility has been demonstrated.

## Verification and final engine scenarios (none run)

Run `python3 -m unittest discover -s tests -v` and `python3 tools/validate_mod.py`.
Static mutations reject missing story/type/owner identity, single-slot/global-lock
regressions, unfiltered/random history, lost retention protection and heir transfer.
Existing source-contract and localization checks remain active. No test executes
CK3 persistence or creates real engine stories.

Final campaign must verify:

1. At least two different referrals for the same provider create separate stories;
   close A while B remains open, then compare serials, clients, deadlines and results.
2. Queue A's notices/timeouts, then create B. Replaying A cannot decide, close, charge
   or change B, nor change any active service receipt/obligation.
3. Provider, original client and original mediator can read their known records only;
   strangers and a client of another case cannot enumerate unrelated cases. Former
   mediators may read disclosed history but cannot decide without current authority.
4. Enumerating several stories produces one correctly scoped notice per record,
   not repeated notices of the last iteration. Test self-browsing and all party roles.
5. Save/reload active and closed stories, then read/decide the correct case once.
   End a story before its notice is read: no stale effect or wrong-case information.
6. Test day-30 inactivity, normal day-31 closure, lost-callback fallback at a later
   60-day check, and retention ending after 1825 days plus at most 60 days. Cleanup
   must not remove active/unexpired records or apply native sanctions/transfer.
7. Provider death ends records without heir guilt or native inheritance changes.
   Lost/purged client/mediator references remain inert. Check legacy/fresh saves.
8. Compare AGOT-only baseline, logs, save size and performance before claiming any
   compatibility, persistence guarantee or acceptable long-term archive overhead.

Format update: decision/archive guards now require explicit kind provenance. Old stories lacking kind are not assumed to be service/disclosed facts; no migration was engine-tested. See RW010_ALLEGATIONS.md.
