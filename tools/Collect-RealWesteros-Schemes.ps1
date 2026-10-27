#Requires -Version 5.1
<#
Collect private, installed scheme-source candidates. Does not run or modify CK3.
All helper functions are defined before execution. No network or upload operation.
#>
[CmdletBinding()]
param(
    [string]$CK3Path = '',
    [string]$AGOTPath = '',
    [string]$OutputDirectory = (Get-Location).Path,
    [ValidateRange(0, 8)][int]$DependencyDepth = 3,
    [ValidateRange(1, 512)][int]$MaxSourceMiB = 128
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:Utf8 = [System.Text.UTF8Encoding]::new($false, $true)
$script:Relevant = '(?i)\b\w*(scheme|murder|assassin|conspir|regicid)\w*\b|\b\w*(secret\w*(expos|discover)|(expos|discover)\w*secret)\w*\b'
$script:Groups = @('common/schemes', 'common/secret_types', 'common/on_action',
    'common/scripted_effects', 'common/scripted_triggers', 'common/script_values',
    'common/character_interactions', 'events')

function Get-SourceRoot([string]$Path, [string]$Label) {
    if ([string]::IsNullOrWhiteSpace($Path)) { throw "Dossier $Label manquant." }
    $item = Get-Item -LiteralPath $Path -Force
    if (-not $item.PSIsContainer) { throw "Le dossier $Label est invalide." }
    $root = $item.FullName
    if ($Label -eq 'CK3' -and (Test-Path -LiteralPath (Join-Path $root 'game/common') -PathType Container)) {
        $root = Join-Path $root 'game'
    }
    if (-not (Test-Path -LiteralPath (Join-Path $root 'common') -PathType Container)) {
        throw "Le dossier $Label doit contenir common (CK3 accepte aussi le dossier parent de game)."
    }
    return [IO.Path]::GetFullPath($root).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
}
function Get-Relative([string]$Root, [string]$Path) {
    return $Path.Substring($Root.Length + 1).Replace('\', '/')
}
function Get-Scripts([string]$Root, [string]$Group, $Excluded) {
    $directory = Join-Path $Root $Group
    if (-not (Test-Path -LiteralPath $directory -PathType Container)) { return }
    # Check each ancestor: a junction at common/events must not be traversed.
    $current = $Root
    foreach ($part in $Group.Split('/')) {
        $current = Join-Path $current $part
        if (((Get-Item -LiteralPath $current -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            [void]$Excluded.Add((Get-Relative $Root $current)); return
        }
    }
    $stack = [Collections.Generic.Stack[string]]::new()
    $stack.Push($directory)
    while ($stack.Count -gt 0) {
        foreach ($item in Get-ChildItem -LiteralPath $stack.Pop() -Force) {
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                [void]$Excluded.Add((Get-Relative $Root $item.FullName)); continue
            }
            if ($item.PSIsContainer) { $stack.Push($item.FullName) }
            elseif ($item.Extension -ieq '.txt') { $item }
        }
    }
}
function Get-Sha256([byte[]]$Bytes) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
function Get-CleanScript([string]$Text) {
    # Mask quoted strings/comments while retaining line positions. Not a CK3 parser.
    return [regex]::Replace($Text, '"(?:\\.|[^"\\])*"|#[^\r\n]*', [Text.RegularExpressions.MatchEvaluator]{
        param($match)
        return [regex]::Replace($match.Value, '[^\r\n]', ' ')
    })
}
function Get-Definitions([string]$Clean) {
    $depth = 0
    foreach ($line in ($Clean -split '\r?\n')) {
        if ($depth -eq 0 -and $line -match '^\s*([A-Za-z_][\w.]*)\s*=\s*\{') { $Matches[1] }
        $depth += [regex]::Matches($line, '\{').Count - [regex]::Matches($line, '\}').Count
    }
}
function Get-VersionMetadata([string]$Root) {
    $result = [ordered]@{ version = $null; supported_version = $null }
    $descriptor = Join-Path $Root 'descriptor.mod'
    if (Test-Path -LiteralPath $descriptor -PathType Leaf) {
        if (((Get-Item -LiteralPath $descriptor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            return $result
        }
        $text = [IO.File]::ReadAllText($descriptor, $script:Utf8)
        foreach ($key in @('version', 'supported_version')) {
            $match = [regex]::Match($text, '(?m)^\s*' + $key + '\s*=\s*"([^"\r\n]*)"')
            if ($match.Success -and $match.Groups[1].Value -match '^\d+(?:\.(?:\d+|\*))*$') { $result[$key] = $match.Groups[1].Value }
        }
    }
    return $result
}
function Write-ZipBytes($Archive, [string]$Name, [byte[]]$Bytes) {
    $entry = $Archive.CreateEntry($Name, [IO.Compression.CompressionLevel]::Optimal)
    $stream = $entry.Open()
    try { $stream.Write($Bytes, 0, $Bytes.Length) }
    finally { $stream.Dispose() }
}

$tempZip = $null
try {
    if ([string]::IsNullOrWhiteSpace($CK3Path)) { $CK3Path = Read-Host 'Dossier CK3 (installation ou sous-dossier game)' }
    if ([string]::IsNullOrWhiteSpace($AGOTPath)) { $AGOTPath = Read-Host 'Dossier du mod AGOT installe' }
    $roots = [ordered]@{ CK3 = (Get-SourceRoot $CK3Path 'CK3'); AGOT = (Get-SourceRoot $AGOTPath 'AGOT') }
    if ($roots.CK3 -eq $roots.AGOT) { throw 'CK3 et AGOT doivent etre deux dossiers distincts.' }
    if (-not (Test-Path -LiteralPath (Join-Path $roots.CK3 'common/schemes') -PathType Container)) {
        throw 'Les definitions common/schemes de CK3 sont absentes. Verifiez le dossier du jeu complet.'
    }
    if (-not [IO.Path]::IsPathRooted($OutputDirectory)) {
        $OutputDirectory = Join-Path (Get-Location).Path $OutputDirectory
    }
    $outputRoot = [IO.Path]::GetFullPath($OutputDirectory)
    $ck3Installation = $roots.CK3
    if ((Split-Path -Leaf $ck3Installation) -eq 'game') { $ck3Installation = Split-Path -Parent $ck3Installation }
    foreach ($sourceRoot in @($ck3Installation, $roots.AGOT)) {
        $prefix = $sourceRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
        if ($outputRoot -eq $sourceRoot -or $outputRoot.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
            throw 'Le dossier de sortie doit etre en dehors des installations CK3 et AGOT.'
        }
    }
    $entries = [Collections.Generic.List[object]]::new()
    $definitions = @{}
    $excluded = [Collections.Generic.List[object]]::new()
    $missing = [Collections.Generic.List[object]]::new()
    $versions = [ordered]@{}
    [long]$scannedBytes = 0
    foreach ($label in $roots.Keys) {
        Write-Host "Recherche des scripts $label..."
        $root = $roots[$label]
        $versions[$label] = Get-VersionMetadata $root
        foreach ($group in $script:Groups) {
            if (-not (Test-Path -LiteralPath (Join-Path $root $group) -PathType Container)) {
                [void]$missing.Add("$label/$group"); continue
            }
            $links = [Collections.Generic.List[string]]::new()
            foreach ($file in @(Get-Scripts $root $group $links | Sort-Object FullName)) {
                $relative = Get-Relative $root $file.FullName
                if ($file.Length -gt 8MB) { throw "Script trop volumineux : $label/$relative (limite 8 Mio par fichier)." }
                $scannedBytes += $file.Length
                if ($scannedBytes -gt 512MB) { throw 'Limite de lecture de 512 Mio atteinte. Aucune archive partielle ne sera publiee.' }
                $bytes = [IO.File]::ReadAllBytes($file.FullName)
                $clean = Get-CleanScript ($script:Utf8.GetString($bytes).TrimStart([char]0xFEFF))
                $seed = $group -in @('common/schemes', 'common/secret_types')
                $relevant = $seed -or ($relative -match $script:Relevant) -or ($clean -match $script:Relevant)
                $entry = [pscustomobject]@{
                    Key = "$label/$relative"; Source = $label; Relative = $relative
                    FullPath = $file.FullName; Hash = (Get-Sha256 $bytes)
                    Size = $bytes.Length; Selected = $relevant; Depth = 0
                    Reason = $(if ($seed) { 'scheme_or_secret_definition' } else { 'candidate_marker' })
                }
                [void]$entries.Add($entry)
                foreach ($name in @(Get-Definitions $clean)) {
                    if (-not $definitions.ContainsKey($name)) { $definitions[$name] = [Collections.Generic.List[object]]::new() }
                    [void]$definitions[$name].Add($entry)
                }
            }
            foreach ($link in $links) { [void]$excluded.Add("$label/$link") }
        }
    }
    # CK3 and AGOT definitions are both retained; this does not resolve load order.
    $queue = [Collections.Generic.Queue[object]]::new()
    foreach ($entry in $entries) { if ($entry.Selected) { $queue.Enqueue($entry) } }
    $frontier = [Collections.Generic.HashSet[string]]::new()
    $unresolved = [Collections.Generic.HashSet[string]]::new()
    while ($queue.Count -gt 0) {
        $entry = $queue.Dequeue()
        $bytes = [IO.File]::ReadAllBytes($entry.FullPath)
        if ((Get-Sha256 $bytes) -ne $entry.Hash) { throw 'Des sources ont change pendant la collecte. Relancez le script.' }
        $clean = Get-CleanScript ($script:Utf8.GetString($bytes).TrimStart([char]0xFEFF))
        $tokens = [Collections.Generic.HashSet[string]]::new()
        foreach ($match in [regex]::Matches($clean, '\b[A-Za-z_][\w.]*\b')) { [void]$tokens.Add($match.Value) }
        foreach ($token in $tokens) {
            if ($definitions.ContainsKey($token)) {
                foreach ($dependency in $definitions[$token]) {
                    if (-not $dependency.Selected) {
                        if ($entry.Depth -ge $DependencyDepth) { [void]$frontier.Add($dependency.Key) }
                        else {
                            $dependency.Selected = $true; $dependency.Depth = $entry.Depth + 1
                            $dependency.Reason = 'referenced_definition'; $queue.Enqueue($dependency)
                        }
                    }
                }
            }
            elseif ($token -match '(_effect|_trigger|_on_action)$|^[A-Za-z_]\w*\.\d+$') {
                [void]$unresolved.Add($token)
            }
        }
    }
    $selected = @($entries | Where-Object Selected | Sort-Object Key)
    if ($selected.Count -eq 0) { throw 'Aucun candidat trouve. Verifiez les dossiers installes.' }
    $selectedKeys = [Collections.Generic.HashSet[string]]::new()
    [long]$total = 0
    foreach ($entry in $selected) { $total += $entry.Size; [void]$selectedKeys.Add($entry.Key) }
    if ($total -gt ([long]$MaxSourceMiB * 1MB)) {
        throw 'Limite de sources selectionnees depassee. Reduisez DependencyDepth ou ajustez MaxSourceMiB ; aucun fichier ne sera tronque.'
    }
    $remainingFrontier = @($frontier | Where-Object { -not $selectedKeys.Contains($_) } | Sort-Object)
    $manifest = [ordered]@{
        schema = 1; kind = 'private_scheme_source_candidates'
        collected_at_utc = [DateTime]::UtcNow.ToString('o')
        status = 'candidates_only_not_engine_evidence'
        expected_targets = @{ CK3 = '1.19.*'; AGOT = '0.5.2.1' }
        descriptor_metadata = $versions; ck3_executable_version = 'not_collected'
        dependency_depth = $DependencyDepth; scanned_files = $entries.Count
        selected_files = $selected.Count; selected_bytes = $total
        missing_groups = @($missing); excluded_links = @($excluded)
        dependency_frontier = $remainingFrontier; unresolved_identifiers = @($unresolved | Sort-Object)
        files = @()
    }
    $records = [Collections.Generic.List[object]]::new()
    [void][IO.Directory]::CreateDirectory($outputRoot)
    $id = [Guid]::NewGuid().ToString('N')
    $finalZip = Join-Path $outputRoot "RealWesteros-Schemes-PRIVATE-$id.zip"
    $tempZip = Join-Path ([IO.Path]::GetTempPath()) "rw-schemes-$id.zip"
    Add-Type -AssemblyName System.IO.Compression
    $stream = [IO.File]::Open($tempZip, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    try {
        $archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Create, $true)
        try {
            foreach ($entry in $selected) {
                $bytes = [IO.File]::ReadAllBytes($entry.FullPath)
                if ((Get-Sha256 $bytes) -ne $entry.Hash) { throw 'Des sources ont change pendant la collecte. Relancez le script.' }
                Write-ZipBytes $archive $entry.Key $bytes
                [void]$records.Add([ordered]@{ source = $entry.Source; path = $entry.Relative
                    sha256 = $entry.Hash; size = $bytes.Length; reason = $entry.Reason; depth = $entry.Depth })
            }
            $manifest.files = @($records.ToArray())
            Write-ZipBytes $archive 'MANIFEST.json' ($script:Utf8.GetBytes(($manifest | ConvertTo-Json -Depth 8)))
        }
        finally { $archive.Dispose() }
    }
    finally { $stream.Dispose() }
    if ((Get-Item -LiteralPath $tempZip).Length -gt 30MB) { throw 'ZIP superieur a 30 Mio : reduisez DependencyDepth. Aucune archive partielle ne sera publiee.' }
    # Move with no overwrite; delete the temporary archive even on failure.
    [IO.File]::Move($tempZip, $finalZip)
    $tempZip = $null
    Write-Host "Termine : $($selected.Count) fichiers, $([Math]::Round((Get-Item -LiteralPath $finalZip).Length / 1MB, 2)) Mio."
    Write-Host "ZIP PRIVE : $finalZip"
    Write-Host 'Joignez ce ZIP dans la conversation. Ne le publiez pas sur GitHub.'
    Write-Host 'Aucun test CK3 realise. Les references trouvees restent des candidats a examiner.'
}
catch {
    [Console]::Error.WriteLine("Collecte interrompue : " + $_.Exception.Message)
    exit 1
}
finally {
    if ($null -ne $tempZip -and (Test-Path -LiteralPath $tempZip)) { Remove-Item -LiteralPath $tempZip -Force }
}
