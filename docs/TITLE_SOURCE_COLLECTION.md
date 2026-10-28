# Missing title-grant and election sources — private G3 collection

The received 1,724-file scheme collection and earlier G1 complement contain neither
native title-grant interaction definitions nor the complete election-type directory.
They do contain grant eligibility helpers and election references, which are not
substitutes for those definitions. G3's universal landholding gate remains unresolved.

A new `TitleRoutes` profile in the **same standalone collector** prepares the missing
source inspection. Its legacy filename is retained for existing users and tests.
The default `Schemes` profile keeps its prior selection and depth of three. This is
source tooling, not runtime Python, new gameplay or an engine test.

## Windows: one downloaded file, no game launch

Download the complete original script:

<https://raw.githubusercontent.com/ElSofian/real-westeros/main/tools/Collect-RealWesteros-Schemes.ps1>

Or paste this block in PowerShell from Downloads or another writable directory
outside the installations. It downloads the script into a fresh temporary filename,
then runs that file; no manual copy of function fragments is necessary:

```powershell
$rwCollector = Join-Path $env:TEMP ('RW-Titles-' + [guid]::NewGuid().ToString('N') + '.ps1')
Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/ElSofian/real-westeros/main/tools/Collect-RealWesteros-Schemes.ps1' -OutFile $rwCollector
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $rwCollector -Profile TitleRoutes
```

The collector prompts for the CK3 installation (or `game` folder) and installed AGOT
folder. Parameters `-CK3Path`, `-AGOTPath` and `-OutputDirectory` can supply them instead.
It requires CK3's `common/character_interactions`, not the scheme folder. CK3/AGOT
stay read-only; no CK3 launch, network or upload occurs inside the collector. The
only network command above downloads our original script from the public repository.

The current directory is the default output location. A unique
`RealWesteros-TitleRoutes-PRIVATE-….zip` is printed when complete. Attach that ZIP
**privately in the conversation**, never in GitHub, an artifact or a release. This
new input is needed for stronger title/status research, not an intermediate game run.

## Selection, probe and limits

Only `.txt` within explicit candidate groups are scanned: character interactions,
`common/succession_election`, laws, scripted effects/triggers/values, on-actions,
story cycles and events. Election candidate files and laws are seeds. Grant/revoke/
disinherit/restore identifiers and election/succession/inheritance helpers find
additional candidates. Existing comment/string masking, definition indexing, both
CK3/AGOT versions and lexical dependencies remain; the default depth is **one** for
this profile to limit repeated collection. An explicit `-DependencyDepth` overrides it.
No saves, logs, settings, textures, executable, descriptor path or credentials are
included. Linked entries are excluded; originals are not modified. The existing
8-MiB/file, 512-MiB scanned, selected-source and 30-MiB ZIP limits fail without a
partial published archive; no file is silently truncated.

`MANIFEST.json` includes profile/kind, scanned groups, exact relative files/hashes/
sizes/reasons/depth, sanitized descriptor versions, missing groups and explicit
remaining dependency frontier. `title_route_probe` separately lists:

- Top-level grant-interaction candidates in character-interaction files. A caller
  containing the identifier does not count as its definition.
- Grant-eligibility helper definitions, separately from the initiating interaction.
- Election references and actual top-level candidate definitions under the election
  directory. A same-named helper elsewhere does not count as an election definition.
- Referenced election identifiers without a candidate definition in the selection.

The probe scans only selected files, masks strings/comments and is lexical, not a
Paradox parser. Dynamic/quoted/parameterized references, other storage groups, index
collisions and unselected callers can be missed or overselected. An empty missing
list does **not** prove full coverage. Missing grant/election definitions produce
explicit empty lists/warnings; neither caller text nor a partial ZIP fabricates them.
Both CK3/AGOT candidates remain; effective load order is not resolved.

## Validation and next step

Ten additional executable synthetic tests cover integrity/privacy/overlays, shallow
frontier and explicit depth, profile-specific root checks, missing definitions,
comment/string masking, unchanged sources/non-overwrite, failure bounds and links.
They run alongside the original nine scheme tests on PowerShell/Linux and Windows
PowerShell 5.1 CI. Local hosts without PowerShell report skips explicitly.

After receiving the ZIP, verify every hash/size before source inspection and keep
originals outside Git. Resolve the grant sender/recipient/title-picker/conditions,
election candidate predicates and referenced dependency frontier. Inspect actual
inheritance and conquest separately; a grant helper or post-transfer reversal cannot
stand in for all four routes. Preserve native/AGOT restrictions, refusal, succession,
Mega Wars and AI; do not widen human-only native sanctions. Original experimental
adapters need a known source contract, and all final engine scenarios remain unrun.
