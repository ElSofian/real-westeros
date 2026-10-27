# G1 — private, isolated hook-gate diagnostic

**Not engine-tested. Not a playable Real Westeros feature.** This test answers only:
does bypassing the scripted hook gate for one selected feudal peer pair leave the
native claim CB selectable and declarable? A successful declaration is not full G1
acceptance; lifecycle, AI parity and political consequences remain separate work.

## Build and isolation

`tools/build_g1_probe.py` is a build utility, not a Python gameplay prototype. It
reads the installed helper, preserves its original body, and adds a contextual AND
condition which makes the helper false only for explicitly flagged feudal peers
under an internal/all-vassal-war ban. The original definition remains effective for
all other contexts. This relies on CK3 loading the duplicate helper override after
AGOT; actual load order and engine handling must be checked, not assumed.

Build privately, outside this Git checkout and outside the game/mod installation:

```text
python tools/build_g1_probe.py --agot-root <installed-AGOT-folder> --output <new-private-output-folder>
```

The builder requires the declared AGOT 0.5.2.1 / supported 1.19.0.6 descriptor. It
rejects preexisting output, installation/repository output, malformed/duplicate
helpers, and unexpected source layout. It writes an independent `rw_g1_probe.mod`
and `rw_g1_probe/` folder, a hash receipt, and instructions. **The generated helper
contains private installed code: never commit or distribute it publicly.** The
builder itself and synthetic tests contain no proprietary source.

Copy only the outer `.mod` file and folder to the CK3 **user-data** `mod/` folder,
not the Steam game/mod folders. In a new playset load AGOT then this PRIVATE PROBE;
disable Real Westeros and all other submods to isolate the hypothesis. Remove the
probe from the playset after testing. Keep an AGOT-only baseline. Use a disposable
save and record exact executable version, checksum and active playset.

## Minimal comparison (pause the game)

Choose two landed feudal peer vassals A and B with the same immediate liege. A must
have a valid personal claim on B's title, no usable liege hook or war-contract
exemption, no imprisonment, debt, raised armies or other war blocker. The liege's
law must ban internal war. Use debug mode and `play <numeric-character-id>` to switch
between A and B; note the IDs before beginning. Do not assume bookmark characters
have the needed laws or claims; verify the setup in the UI.

1. In the AGOT-only baseline verify A is blocked specifically by the liege-hook
   requirement. Record the tooltip and CB/title. Verify the same claim works when
   legally permitted in a separate baseline setup.
2. Load the probe playset and same disposable setup. With **no markers**, the same
   restriction must remain. A difference here fails the isolation requirement.
3. As A, paused, run in the debug console:
   `effect add_character_flag = { flag = rw_g1_probe_actor days = 1 }`
4. Switch with `play <B-id>`, run:
   `effect add_character_flag = { flag = rw_g1_probe_target days = 1 }`
   Then switch back with `play <A-id>` without advancing time.
5. Open the **normal Declare War interface** against B. Record all remaining
   restrictions. The claim must remain the original `claim_cb`, same target title,
   claimant and cost as the legal baseline; do not select a fabricated CB. Attempt
   declaration only if other conditions pass. Record the actual result and CB.
6. Before unpausing, clear both flags using character switching:
   `effect remove_character_flag = rw_g1_probe_actor` as A;
   `effect remove_character_flag = rw_g1_probe_target` as B. Return to A.
   If abandoning/cancelling the test, clear both flags too. Otherwise they expire
   after one game day. This diagnostic deliberately has no automated cancellation
   handler or offense recording; do not use it for a campaign.

If a console command or duplicate-helper override errors, stop and report it; the
setup has failed, not G1 itself. Do not repeatedly force a war through the console.
The probe leaves hierarchy, individual CB conditions, costs and AGOT callbacks alone.
It does not guarantee that the engine will honor the exemption.

## Negative and lifecycle checks

- A/B unmarked, only A marked, or only B marked: native hook restriction remains.
- A targets unmarked C, parties have different direct lieges, A is not feudal or no
  relevant law ban exists: no contextual override. Original helper behavior applies.
- Missing claim, wrong target, imprisonment and other restrictions remain effective.
- Expiry/flag removal restores the original gate. Reload with flags cleared must not
  leave a bypass. Production context capture/consumption is not implemented here.
- If declaration succeeds: finish separate copies by victory, defeat, white peace
  and invalidation. Compare titles, vassals, truces and logs to baseline.
- A normal peer conflict should not automatically become a Mega War. Later test an
  independently eligible Mega War; native classification and cleanup must remain.

Report exact CK3 build; whether baseline was blocked; whether the unmarked probe
was identical; whether marked `claim_cb` appeared and started; final war CB/title/cost;
and any relevant error lines with personal paths redacted. No full log dump needed.

Only an in-game run can close this diagnostic. Full G1 also requires target-bound
intent, legality recorded at declaration, safe cancellation/reload and identical
mechanical access for AI; the probe intentionally does not implement those systems.
