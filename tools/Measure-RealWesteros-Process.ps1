# Read-only whole-process samples. No CK3 command, injection or network access.
[CmdletBinding()]
param(
    [int]$TargetProcessId = 0,
    [ValidateRange(0.1,3600)][double]$DurationSeconds = 60,
    [ValidateRange(100,10000)][int]$IntervalMilliseconds = 1000,
    [string]$OutputPath = (Join-Path (Get-Location) ('RW-process-' + [guid]::NewGuid().ToString('N') + '.csv'))
)
$ErrorActionPreference = 'Stop'
$invariant = [Globalization.CultureInfo]::InvariantCulture
if ($TargetProcessId -eq 0) {
    $candidates = @(Get-Process -Name ck3 -ErrorAction SilentlyContinue)
    if ($candidates.Count -ne 1) { throw 'Specify TargetProcessId when exactly one ck3 process cannot be found.' }
    $TargetProcessId = $candidates[0].Id
}
$initial = Get-Process -Id $TargetProcessId
$started = $initial.StartTime.ToUniversalTime()
$initial.Dispose()
# CreateNew fails on an existing file. Do not disclose process name/path/arguments.
$stream = [IO.File]::Open($OutputPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::Read)
$writer = New-Object IO.StreamWriter($stream, (New-Object Text.UTF8Encoding($true)))
$watch = [Diagnostics.Stopwatch]::StartNew()
$sampleCount = 0
$sampleElapsed = 0
try {
    $writer.WriteLine('elapsed_seconds,cpu_seconds,working_set_bytes,private_bytes,threads,logical_processors,status')
    do {
        $process = $null
        $status = 'running'
        try {
            $process = Get-Process -Id $TargetProcessId -ErrorAction Stop
            if ($process.StartTime.ToUniversalTime() -ne $started) { $status = 'replaced' }
            if ($status -eq 'running') {
                $sampleCpu = $process.TotalProcessorTime.TotalSeconds
                # Begin the window at the first real CPU observation, not cold API setup.
                if ($sampleCount -eq 0) { $watch.Restart() }
                $sampleElapsed = $watch.Elapsed.TotalSeconds
                $row = @($sampleElapsed.ToString('R',$invariant),
                    $sampleCpu.ToString('R',$invariant),
                    $process.WorkingSet64, $process.PrivateMemorySize64,
                    $process.Threads.Count, [Environment]::ProcessorCount, 'running')
                $writer.WriteLine(($row -join ','))
                $sampleCount += 1
            }
        } catch { $status = 'unavailable' }
        finally { if ($null -ne $process) { $process.Dispose() } }
        if ($status -ne 'running') {
            $writer.WriteLine(($watch.Elapsed.TotalSeconds.ToString('R',$invariant) + ',,,,,,' + $status))
        }
        $writer.Flush()
        # End only after two real observations spanning the requested CPU window.
        # Slow collection may extend wall time; never fabricate a second sample.
        if ($status -ne 'running' -or ($sampleCount -ge 2 -and $sampleElapsed -ge $DurationSeconds)) { break }
        $remaining = [Math]::Max(1, [Math]::Ceiling(($DurationSeconds - $watch.Elapsed.TotalSeconds) * 1000))
        Start-Sleep -Milliseconds ([int][Math]::Min($IntervalMilliseconds,$remaining))
    } while ($true)
} finally {
    $watch.Stop()
    $writer.Dispose()
    $stream.Dispose()
}
Write-Output 'Process samples written. Whole-process measurements do not establish mod overhead or gameplay compatibility.'
