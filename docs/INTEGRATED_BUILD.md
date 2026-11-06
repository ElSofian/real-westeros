# Integrated experimental build — 0.1.0

This is an installable source snapshot, **not a gameplay-validated release**.
The descriptor targets CK3 1.19.* using AGOT 0.5.2.1 source metadata; this is not
proof of compatibility with your executable, DLC, playset or save. Runtime tests
are deferred to the final campaign, not waived. Prefer a disposable fresh save.

## Included script slices

| Entry / flow | Current scope |
|---|---|
| Reconciliation interaction | Accept/refuse/lapsed, shared AI liege targeting |
| Immediate endorsement | 50/25-gold negotiation; payment and prestige at performance |
| Favor-backed endorsement | Native favor for immediate support, or versioned 25-gold counteroffer; shared provider pool, native eligibility/detected-hook protection and one performance, private latest review |
| Deferred favor-backed support | Explicit favor/25-gold promise without payment at consent; provider performance after seven/before thirty days, client withdrawal, provider renunciation and neutral bounded expiry |
| Deferred endorsement | Consent without payment, due delivery, refusal, wait and expiry |
| Mutual promise release | Either party proposes; other accepts/refuses/ignores; original deadline retained |
| Breach response | Personal resentment/forgiveness or explicit referral to common overlord |
| Mediation | Decline, evidence-gated personal reprimand, invitation to conciliatory gesture; immutable exact service price/delivery clauses with private read-only review |
| Gesture reception | Client acceptance/refusal, personal response recorded separately |
| Affront allegation | Acknowledgment/contest/silence; withdrawal or explicit disclosure |
| Political scheme response | Voluntary 25-gold request for non-stacking goodwill, refusal/contestation/withdrawal; no criminal pardon |
| Native plot observations | Discovered murder plot vs exposed participant; target-only journal, no new sanction |
| Judicial inspection | Observer-only custody/reason check and guarded native arrest-window shortcut; no automatic send |
| Personal prisoner sentencing | Native execution/release terms or unchanged detention; no automatic send/result |
| Individual title/status review | Current grounds, knight/contract status; experimental native revocation/release terms, no forced transfer |
| Optional G3 diagnostic | Separate mod under `diagnostics/g3_house_trace/`; debug-only seven-day house/title trace, no sanction |
| Political house affairs | Fifty-year political disfavor, independent institutional records, head petitions/sovereign rehabilitation; no title ban |
| Post-rehabilitation land review | Current sovereign/head review; guarded native grant terms, no automatic transfer or restitution |
| Personal title provenance | Conditional native revocation-context observation; exact parties/title, private five-year records, no new sanction or inherited entitlement |
| Exact-affair revocation intentions | Generic title choice plus explicit private-basis confirmation; thirty-day withdrawal/match window; no forced sanction |
| Crown land register | Voluntary public title-fact filing; scoped successor/house access and custody, max hundred-year archive; no private guilt or title right |
| Restitution discussions | Exact public-entry request to current holder; private review/refusal/withdrawal and optional bounded personal rancour; no promised/automatic land transfer |
| Optional PRIVATE post-confiscation return | Native accepted revocation + exact loss → explicit keep/return → one guarded native ducal transfer, shared AI/player; POST_CONFISCATION_RESTITUTION.md, source-only J5. |
| Optional PRIVATE ducal restitution | Explicit holder choice → one-attempt native granted transfer of a ducal dignity to an existing count vassal, after native script guards; no other lands/vassals; callbacks/equivalence unverified. See RW010_NATIVE_RESTITUTION.md. |
| Personal restitution promises | Explicit 14/30-day offers and bilateral consent; separate deadline, release/renunciation, optional personal response; beneficiary satisfaction is a statement plus ownership, no forced or proven grant |
| Pledged title observations | Conditional exact native title-gain context for one unique live accepted promise; participant-private first note, no automatic fulfillment or proved grant/cause |
| Voluntary case compensation | Private 25/50-gold offers/counters for an exact closed service affair; current consent/funds and one payment from provider to client, without pardon or rewritten case facts |
| Compensation reception | Original beneficiary may appreciate a new paid gesture or acknowledge neutrally within thirty days; private bounded opinion response, no automatic pardon or payment replay |
| Known-case archive | Independent story records, role/disclosure-filtered views, retained closed records |

All rows describe intended source behavior; none has been observed in CK3 here.
AI uses the same effects/guards, with bounded initiation or event-driven choices.
No LLM, paid service or runtime Python is needed. Python is used for development
checks and packaging only. No original CK3/AGOT scripts or assets are distributed.

Not included: automatic assassination justice, custom executions,
confiscation, loss of noble status, enforced house landholding bans, unlawful war despite royal prohibition,
a complete obligation ledger, general multi-clause negotiation or engine-proven
save migration. G1/G2/G3/G4/G5 remain unverified. Personal histories stay personal; the house register carries institutional political
affairs, not a universal reputation score or inherited personal guilt.

## Obtain a ZIP

On a completed successful **Validate submod** GitHub Actions run, open **Artifacts**
and download the **RealWesteros-experimental-…** artifact. GitHub may require sign-in.
The download wraps the mod ZIP and its `.sha256` file: extract that outer artifact
first. Then follow INSTALL.md for the inner `RealWesteros-experimental.zip`.
Artifacts are retained for seven days; a source checkout can rebuild the snapshot.
A successful Actions run is static/build evidence only.

To build locally from a committed source checkout, with Git and Python 3.10+:

```sh
python -m unittest discover -s tests -v
python tools/validate_mod.py
python tools/build_distribution.py --output build/RealWesteros-experimental.zip
```

The builder packages **committed HEAD**, rejects modified tracked distribution
inputs, and ignores untracked local files. Commit intended changes before building.
If the output already exists, choose another path; it never replaces it implicitly.
Paths are not derived from a personal game installation. No game installation is
needed to build, and the ZIP contains no Python gameplay runtime.

## Integrity and limits

The ZIP has `mod/real_westeros.mod`, `mod/real_westeros/`, selected instructions
(including the G3 diagnostic notice, resumed title-route audit and hash-only source receipts),
and `MANIFEST.json`. The manifest identifies HEAD, provisional version metadata,
and each payload file's SHA-256/size. It excludes itself from its file list; directory
entries have no payload checksum. The adjacent `.sha256` hashes the whole mod ZIP.
Compare with `Get-FileHash ... -Algorithm SHA256` in PowerShell or `sha256sum`.
Hashes detect differences; they are not a signature or CK3 compatibility proof.

Packaging reads only tracked regular blobs under the narrow mod/docs allowlist
and eight explicitly listed optional G3 diagnostic files. The diagnostic is outside
the main mod payload and is installed/enabled separately; its descriptors, launcher
path, script braces and localization encodings receive separate structural checks.
Symlinks and unexpected mod payloads fail closed. It preserves empty scaffold
directories, verifies the staged mod structurally, and produces identical ZIP bytes
for the same committed payload/toolchain (not a promise across all zlib versions).
It cannot certify authorship or detect proprietary text intentionally committed
under an allowed script name; normal source review still applies.

## Integration audit

The current provider decision flow uses versioned hidden reminders to prevent
repeated reviews/waits from creating multiple live weekly chains. See the source
repository’s INTEGRATION_AUDIT.md and the LIFE-* cases in FINAL_ENGINE_TESTS.md.
This is a source correction, not an observed CK3 scheduler/performance result.

## Final campaign

Follow FINAL_ENGINE_TESTS.md plus TEST_PLAN_G1.md when that war stage is ready.
Record actual CK3/AGOT versions, DLC, playset, source commit, manifest, logs and
observed results. Launcher visibility or a clean build does not make a scenario
pass. Keep unsupported features distinct from the implemented experimental slices.

The experimental house register also includes a sovereign's conditional 50-gold
rehabilitation offer (RW010_HOUSE_TERMS.md): current-head consent and funds are required,
free restoration/withdrawal remain separate, and no native title/status sanction is
implemented. Payment/closure ordering and persistence still require final CK3 tests.

## Isolated G1 candidate sources

G1_NATIVE_CHOICE.md documents a private native-window send-option experiment. The
public ZIP includes only original templates and the local generator, outside `mod/`.
It never contains the installed native declaration definition. Do not activate this
candidate with the older G1 probes or other declaration overrides; base installation
is unchanged. Native CB/cost/cancel/AI/Mega Wars behavior remains engine-unverified.

The G1 candidate's original source kit now also includes personal sovereign-response
story/effects/events/opinions (G1_ROYAL_RESPONSES.md), called only at the end of its
private generated declaration's acceptance. No forced peace, native crime or title
sanction. Seven templates remain outside base `mod/`; generated native code remains
private. Human/AI reaction choices do not establish autonomous native war initiation.

## Current W3 integration and private declaration adapter

G1_NATIVE_INTERVENTION.md supersedes the earlier source-kit layout: nine original
runtime files now live under base `mod/real_westeros`, including the guarded native
stop-attacker-war request. No native definition or global war hook is added there.
The private generator now checks four AGOT inputs and produces only a declaration
adapter explicitly dependent on Real Westeros. It never duplicates the runtime
libraries. Without that optional adapter, ordinary declarations create no new
response record. The request is not proof of peace/negotiation; target propagation,
AI, callbacks and all final scenarios remain engine-unverified.

## Current private adapter 0.0.5

G1_DECLARATION_LAW_CONTEXT.md supersedes the earlier minimal adapter's file counts.
Thirteen original runtime inputs are public; three generated native files stay private
(declaration override, genuine claim_cb prefix and readonly owned helper clone).
No global native helper or installed file is overwritten. Remove the old adapter
folder before copying the new generation, use matching Real Westeros source hashes
and do not combine with another claim_cb/declaration override. Availability is not
engine compatibility; W1 and historical law/ordering remain unverified.

Adapter 0.0.4 adds the source-supported contextual initial AI option preference
(G1_AI_OPTION_POLICY.md), not demonstrated autonomous native war initiation.
Replace the entire old adapter and update the base mod from the same commit.

Adapter 0.0.5 additionally closes original pending response windows from four native
claim-CB terminal callback prefixes and retains exact-war dedup independently of
roles/CB/authority. G1_WAR_RECEIPT_LIFECYCLE.md covers the metadata-only effect and
non-executed lifecycle/Mega Wars cases; W4 remains open (+0). No native state reset.
