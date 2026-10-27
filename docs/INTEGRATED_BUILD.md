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
| Deferred endorsement | Consent without payment, due delivery, refusal, wait and expiry |
| Mutual promise release | Either party proposes; other accepts/refuses/ignores; original deadline retained |
| Breach response | Personal resentment/forgiveness or explicit referral to common overlord |
| Mediation | Decline, evidence-gated personal reprimand, invitation to conciliatory gesture |
| Gesture reception | Client acceptance/refusal, personal response recorded separately |
| Affront allegation | Acknowledgment/contest/silence; withdrawal or explicit disclosure |
| Known-case archive | Independent story records, role/disclosure-filtered views, retained closed records |

All rows describe intended source behavior; none has been observed in CK3 here.
AI uses the same effects/guards, with bounded initiation or event-driven choices.
No LLM, paid service or runtime Python is needed. Python is used for development
checks and packaging only. No original CK3/AGOT scripts or assets are distributed.

Not included: automatic native scheme discovery, assassination justice, executions,
confiscation, dynastic sanctions/restoration, unlawful war despite royal prohibition,
a complete obligation ledger, general multi-clause negotiation or engine-proven
save migration. G1/G2/G3/G4/G5 remain unverified. Current affairs and histories are
personal, not a universal reputation score or inherited personal guilt.

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

The ZIP has `mod/real_westeros.mod`, `mod/real_westeros/`, selected instructions,
and `MANIFEST.json`. The manifest identifies HEAD, provisional version metadata,
and each payload file's SHA-256/size. It excludes itself from its file list; directory
entries have no payload checksum. The adjacent `.sha256` hashes the whole mod ZIP.
Compare with `Get-FileHash ... -Algorithm SHA256` in PowerShell or `sha256sum`.
Hashes detect differences; they are not a signature or CK3 compatibility proof.

Packaging reads only tracked regular blobs under the narrow mod/docs allowlist.
Symlinks and unexpected mod payloads fail closed. It preserves empty scaffold
directories, verifies the staged mod structurally, and produces identical ZIP bytes
for the same committed payload/toolchain (not a promise across all zlib versions).
It cannot certify authorship or detect proprietary text intentionally committed
under an allowed script name; normal source review still applies.

## Final campaign

Follow FINAL_ENGINE_TESTS.md plus TEST_PLAN_G1.md when that war stage is ready.
Record actual CK3/AGOT versions, DLC, playset, source commit, manifest, logs and
observed results. Launcher visibility or a clean build does not make a scenario
pass. Keep unsupported features distinct from the implemented experimental slices.
