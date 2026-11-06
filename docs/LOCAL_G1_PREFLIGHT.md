# Local G1 preflight — 6 November 2026

**Static-checked; zero engine scenarios executed.** Target: the first player
G1CHOICE/DECLAW observation with a genuine claim CB. Baseline and result remain
68/80 source + 0/20 engine = 68/100; delta **0**. W1/W2/W4/W5/AI4 stay open.
This owner-requested targeted trial supersedes the earlier deferral for this run.

## Observed installation

- The source ZIP SHA256 matches
  `8871178a77b35f77b76983b52b996f0a3adefa225fc9f206e33bd45c92cbccc4`.
  Its source revision is `19d567fa439b5c0025b498187f463cbd2341f0fd`.
  It has no Git metadata; a separate genuine Git clone was created for further work.
- All 303 installed base-mod files match that extracted source tree, with no
  missing, changed or extra files. All four installed private adapter files match
  the existing generation, including descriptor version 0.0.5.
- The private receipt's four AGOT input hashes, thirteen installed runtime hashes
  and three installed generated output hashes match. No regeneration or overwrite
  was needed. Generated native scripts remain private and outside the clone.
- Installed AGOT descriptor declares 0.5.2.1/support 1.19.0.6. Installed CK3
  launcher metadata declares 1.19.0.6; Steam records beta 1.19.0/build 23530548.
  The executable exists, but its Windows file/product version fields are empty.
  These are installation observations, not a running-engine version observation.
- Read-only launcher database inspection finds a separate **Real Westeros**
  playset with exactly AGOT, Real Westeros and the private native-war-choice
  experiment, enabled in positions 0/1/2. No **RW-Test** playset exists yet.
  The active **AGOT + Mods** playset and effective `dlc_load.json` still contain
  the usual extensions. They must not be mistaken for the isolated test setup.
- Steam configuration contains `-debug_mode`; actual runtime debug activation
  and console commands have not been observed. The installed launcher also
  explicitly offers a debug executable with that argument.
- No CK3 or Paradox launcher process was observed. Latest CK3 log writes date
  from 1 November, before RW installation; they cannot establish RW loading.

## Available checks and blocker

The native-choice (21), declaration-law (16), war-receipt lifecycle (10) and
native-intervention (14) tests all pass: **61 total**, including negative paths.
The structural validator passes. `py -3 -X utf8 tools/report_progress.py` passes
with 68/100 and delta zero. Without UTF-8 mode the local Windows default decoding
caused the rubric check to reject the JSON; no rubric or checkpoint was changed.

Windows Computer Use initialized, but `sky.list_apps()` failed with
`Computer Use native pipe is unavailable` / OS error 2. The documented retry and
fresh-kernel retry failed identically. Thus no game window, console, character
selection or launcher action can currently be observed or controlled through that
connector. No game launch, database/configuration write, save modification,
hot reload or installed-file change was performed during this preflight.

## Minimal first trial, before any launch

1. Restore a usable game-control channel, or use an explicitly coordinated human
   operator. In the launcher, rename the isolated Real Westeros playset to
   **RW-Test**, select it, and verify its exact three-mod order and effective mod
   list. Preserve AGOT + Mods and existing saves. Capture the current log baseline
   privately before launching once in configured debug mode.
2. In a disposable campaign, pause and identify two adult, living, free, landed
   feudal peers with the same living direct liege. Record their exact identities,
   target title, genuine claim, relevant law/contract exception and native costs.
   Verify that the native helper actually requires permission; unrelated native
   restrictions must still pass. Do not grant a replacement CB or bypass them.
3. Negative path first: inspect the unchecked defiance option and blocked native
   permission, close/cancel the window, and verify no war, cost or RW receipt.
   Reopen against the same exact target, select defiance without a hook, retain
   the genuine claim CB, record displayed costs, and send once.
4. Observe the actual war/CB/parties and cost deltas, then declaration-law receipt,
   callback phase and linkage to the royal-response record. Separate a missing
   scope/link from successful capture; do not infer callback order from source.
   Record the actual royal choice and any native intervention/refusal separately.
5. Query available console help, including `help reload`, before proposing any
   reload command. Demonstrate a file's changed behavior before crediting reload.
   Treat generated interaction/CB changes as restart-required until demonstrated
   otherwise. Reuse the running session for observations that need no source edit.

No short wait without an AI war demonstrates native planner discovery. Mega Wars,
all terminal paths, AI initiation and the broader final campaign remain unexecuted.
Next task: resolve the control-channel blocker and execute this narrow trial;
claim RW-004 separately before any gameplay or generator correction.
