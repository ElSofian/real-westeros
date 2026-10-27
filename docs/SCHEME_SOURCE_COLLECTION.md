# Native scheme/discovery source collection — RW-010

Current update: the scheme ZIP has been received and hash-verified; see
RW010_SCHEME_EVIDENCE.md and SCHEME_SOURCE_RECEIPT.json. No further collection is
currently requested. The instructions below remain available for later versions.

The earlier private war collections did not establish native scheme discovery,
its observer/actor scopes, agent membership or legal consequences. The collector
prepares source inspection without inventing a callback or running CK3. It is a
development tool, **not a Python gameplay prototype or runtime mod dependency**.

## Download and run on Windows

Download the complete original script from the repository:

<https://raw.githubusercontent.com/ElSofian/real-westeros/main/tools/Collect-RealWesteros-Schemes.ps1>

Save it as `Collect-RealWesteros-Schemes.ps1`, not an HTML page or a partial code
fragment. All functions are included in that file. Windows PowerShell 5.1 and
PowerShell 7 are supported targets; executable CI results are separate evidence.
In PowerShell, from the directory containing the downloaded script:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Collect-RealWesteros-Schemes.ps1
```

It prompts for the CK3 installation (or its `game` folder) and installed AGOT mod
folder. These must contain `common`; CK3 must also contain `common/schemes`.
The Steam Workshop directory for AGOT is a mod folder, not the CK3 installation.
Paths can contain spaces. Parameters avoid prompts when preferred:

```powershell
.\Collect-RealWesteros-Schemes.ps1 -CK3Path 'YOUR_CK3_INSTALLATION' -AGOTPath 'YOUR_AGOT_MOD' -OutputDirectory .
```

The ZIP is written in the current directory unless `-OutputDirectory` is given.
The selected output directory must be outside both installations. The script
prints its full local filename, file count and compressed size when finished.
Each run uses a unique name and never replaces an earlier result.

**Attach `RealWesteros-Schemes-PRIVATE-….zip` privately in this conversation. Do not
commit it or publish it in a GitHub issue, PR, artifact or release.** No upload,
network access, CK3 launch or game modification is performed by the collector.
The owner still defers all actual CK3 tests until the final campaign.

## Selection and manifest

Only `.txt` files in these installed-script groups are considered, separately for
CK3 and AGOT:

- `common/schemes` and `common/secret_types`: definition seeds;
- `common/on_action`, `common/scripted_effects`, `common/scripted_triggers`,
  `common/script_values`, `common/character_interactions`, and `events`: related
  candidate files and lexical dependency index.

Matching looks for scheme/murder/assassination/conspiracy/regicide and secret
exposure/discovery identifiers or filenames. Comments and quoted strings are masked
for content matching; filename matching remains a heuristic. Top-level block names
are indexed, then matching referenced definitions are collected to a default depth
of three. Both CK3 and AGOT definitions are retained for override inspection; the
collector never decides effective load order or merges their source definitions.

`MANIFEST.json` contains source-relative paths, selected-byte SHA-256 hashes, sizes,
selection reason/depth, numeric descriptor version metadata if present, missing
groups, skipped links, unresolved helper/event identifiers, and a depth frontier.
It contains no installation roots or raw descriptor path field. Expected targets
CK3 `1.19.*` / AGOT `0.5.2.1` are labeled expectations; they do not verify installed
versions. CK3 executable version and runtime compatibility are not collected/proven.
Each payload is hashed from the same bytes written to the ZIP, and a detected source
change during scanning/packing aborts the collection. No atomic installation snapshot
is promised; avoid updating installed mods during collection.

Missing AGOT groups can be normal inheritance from CK3; the report preserves absence.
A missing CK3 scheme directory, invalid roots, unreadable/non-UTF-8 scripts or oversized
inputs cause a visible failure, never a silently incomplete final ZIP. The output is
marked `candidates_only_not_engine_evidence` even when collection succeeds.

## Bounds and privacy

The collector scans only those groups, not the whole Steam library, user-data
folder or machine. Saves, binaries, textures, credentials, settings and logs are
excluded by location/type. It refuses links/junctions below the selected source
roots; the manifest reports their relative names. Review the private ZIP before
sharing if an installation was manually customized with private data in script files.
This is source collection from the owner's installation, not redistribution rights.

Limits: 8 MiB per script, 512 MiB scanned text, 128 MiB selected source by default,
and 30 MiB compressed ZIP to fit the current upload limit. The script fails rather
than truncating files. `-DependencyDepth 0` collects only initial candidates;
`-DependencyDepth` permits 0–8, and `-MaxSourceMiB` permits 1–512. Increasing a limit
never changes the 30 MiB final ZIP bound. A nonempty dependency frontier or unresolved
identifiers means further inspection/collection may be required. No claim that this
heuristic finds every dynamic/quoted/parameterized reference or legal hook is made.
Temporary ZIPs are removed on failure; originals are read only. The collector is
separate from the public mod distribution builder, which excludes its private output.

## Verification and next inspection

Executable synthetic tests run the downloaded-script copy alone in an isolated
working directory, with spaces in paths, both installation-root forms, dependency
chains, CK3/AGOT overrides, manifest checks, comment/string exclusions, non-script
private files, invalid roots, source bounds, non-overwrite and unchanged inputs.
PowerShell 7 tests run on Linux; a separate CI job runs Windows PowerShell 5.1.
Symlink testing may skip on Windows if the runner cannot create one; Linux tests
exercise actual link exclusion. This is collector verification, not CK3 testing.

After receiving the private archive, verify manifest hashes before inspection and
keep original files outside Git. Establish exact scheme definitions and discovery
call sites; record installed-version evidence, owner/agent/target/observer scopes,
private discovery versus public exposure, additive action composition and once-only
identity. A callback-looking identifier is only a lead. Preserve native secrets,
crimes and AGOT behavior; do not infer guilt from a contested allegation or treat
`secret_murder` as proof of a currently discovered assassination attempt. Implement
the smallest original additive hook only after its actual source contract is known.
Final engine tests remain required to establish runtime behavior.
