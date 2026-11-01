# G1 — private exact-target intent diagnostic

**Original CK3-facing diagnostic templates; static-checked, not engine-tested.**
This prepares the war-feature track without adding a war bypass to the base mod.
G1 remains unresolved. All CK3 runs stay in the owner's final campaign; no new
source upload or intermediate run is requested. Independent RW-010 work continues.

## What changed and what did not

The earlier manual two-character flag test remains the default builder mode in
G1_PROBE.md. The new opt-in mode stages one exact actor/target/direct-liege ticket,
requires explicit confirmation and limits the contextual helper exemption to one
in-game day. It adds original manual interactions and conditional native observation.
It never creates/starts/ends a war, chooses a CB, fabricates a claim, changes laws or
contracts, creates/spends hooks, transfers a title or reproduces native costs.
The existing native Declare War interface and all other native checks still run.

The generator preserves the installed helper body and inserts only a guard calling
the new exact-pair predicate. Actual duplicate-helper loading, UI/CB enumeration,
hidden engine restrictions, cost execution and AGOT lifecycle remain unverified.
Other call sites evaluating that same pair during the armed day can see the guard;
this is not a proven UI-exclusive or production-safe hook. No fake generic CB is used.

## Build privately from the repository

Use a source checkout of this repository (or GitHub's source ZIP), which contains
`tools/build_g1_probe.py`, `tools/validate_mod.py`, receipt JSON and original templates.
The normal experimental mod archive includes this guide, not a ready-to-install G1
patch or the build toolchain. Python is a free, standard-library-only build utility;
no gameplay Python or LLM runs in CK3.

```text
python tools/build_g1_probe.py --agot-root <installed-AGOT-folder> --output <new-private-folder> --target-bound-intent
```

This mode requires the previously reported AGOT 0.5.2.1 / supported 1.19.0.6 descriptor
and exact reviewed hashes for the installed hook-helper and native claim-CB files,
from G1_SOURCE_RECEIPT.json and G1_COMPLEMENT_RECEIPT.json. Unknown layout/hash,
missing CB, wrong version, nonregular/corrupt template and existing/repository/
installation output fail before output creation. Unrelated later AGOT releases or
other mod overrides are not declared compatible. No descriptor proves the actual
CK3 executable version or effective runtime definitions.

Output is a standalone `rw_g1_intent_probe.mod` and `rw_g1_intent_probe/`, plus a
relative-path/hash receipt and PRIVATE.txt. Seven allowlisted original templates are
copied; only the generated helper includes proprietary installed code. **Never
commit or publicly distribute the generated private output.** Inputs are read-only.
Do not install templates directly from `diagnostics/g1_intent_probe/template`.

For final testing only, copy the outer descriptor/folder into the CK3 user-data
`mod/` folder. Use a disposable save and a separate AGOT-only baseline playset.
Load this probe after AGOT; disable the base Real Westeros submod, the earlier G1
probe and other submods for isolation. Do not enable both helper-override probes.
The new folder/name distinguishes the modes but cannot enforce runtime load order.

## Ticket, explicit confirmation and cleanup

Use two living adult landed free feudal peer vassals, at peace, under one living
direct liege whose ordinary realm law bans internal/all vassal wars. The actor
must have no detected liege hook and the original helper must actually require one;
this avoids arming a legal contract/hook exemption as if it were an unlawful test.
Native claim availability and all other restrictions remain the native UI's job.

1. Reproduce the legal genuine `claim_cb` baseline and the banned/no-hook baseline
   as in TEST_PLAN_G1.md. Record actual CB, title, claimant, cost and tooltip.
2. With the private probe loaded but no staged context, repeat the banned setup.
   The original behavior must remain. Any unmarked change fails isolation.
3. Select the target's **PRIVATE G1 test: stage this exact opponent** interaction.
   Auto-accept opens a confirmation only. Staging captures immutable target/liege,
   monotonic serial and a one-day offer window; it arms no exemption.
4. Explicitly confirm while the same original ticket, peer roles, current liege/
   ban/native helper and no-hook conditions still match. This consumes the offer
   and arms the exact pair for one day from confirmation. Old confirmations cannot
   arm or clear a newer serial. Review never renews either phase's one-day window.
5. Open the normal native Declare War interface manually against that opponent.
   Inspect the real `claim_cb`, selected title/claimant/cost and remaining blockers.
   The diagnostic supplies no replacement declaration or CB. Compare the actual war
   object and costs after a successful native declaration, not merely a tooltip.
6. If abandoning or cancelling, immediately use the self **clear my diagnostic
   context** interaction. It clears only the actor's flags, even after target loss,
   imprisonment or role changes. A current-ticket cancel option is also available.
   **No native-window cancellation callback is verified.** The marker can remain
   for that exact pair until explicit cleanup or one-day expiry after UI cancellation.
   This unresolved gap alone prevents treating the probe as production gameplay.

Changing target, liege, law, government, peace/eligibility or acquiring a detected
liege hook removes the contextual exemption at evaluation. Metadata may remain inert
until review/cleanup; it is not an offense or a reusable generic override. Superseding
an expired ticket increments the serial; cleanup never resets its counter.

## Native observation is deliberately limited

A named additive `on_war_started` child reads native war/primary-attacker/primary-
defender scopes. Only an armed current actor ticket with exact target/current common
liege and current ban plus native `using_cb = claim_cb` can produce an observation.
The ticket is consumed before recording latest serial/target/liege/date/kind and a
static `RW_G1P` log marker. No native war reference is kept. Duplicate callbacks
cannot produce another observation for the consumed marker.

Other attacker targets/CBs/context clear the armed ticket without that observation;
a marked primary defender also clears without an attacking-intent observation.
Missing native callback roles fail closed and the one-day/explicit cleanup remains.
Callback order or Mega War realm changes can prevent a match; absence is not proof
that no war occurred. No title/realm/cost/lifecycle effect is replayed.

The observation means only **native claim-CB/role/ban context at that callback**.
It does not prove unlawfulness, selected/spent hook state, which UI route ran, whether
this guard caused admission, normal cost parity, Mega War classification or complete
callback coverage. Hook/cost/callback ordering and effective helper selection need
engine evidence. It creates no political offense, sanction, royal reaction or
inherited guilt. Latest debug facts are not a complete political journal.

The probe is manually initiated: AI initiation/arming weights are zero and no native
AI declaration policy is supplied. Actor/target execution guards have no human-only
bypass, but no working AI flow or gameplay parity is claimed. Test that separately
before any production G1 implementation. The normal base mod loads none of this.

## Available checks and final campaign

Fifteen new adversarial source/build tests cover exact actor/target/liege/serial,
confirmation/expiry, no recursive helper guard, conservative native cleanup, genuine
claim/primary-role observation, immutable native helper body, pinned hashes, missing/
changed inputs, corrupt/symlink templates, localization and absence from the base.
The earlier eight manual-builder tests still run. These are not an engine simulation.
A local construction check used the received exact helper/claim bytes and a fixture
of previously reported descriptor metadata; it preserved the helper body/inputs and
copied seven original templates. It did not verify an installation or executable.

G1INT-01…12 in FINAL_ENGINE_TESTS.md and the existing G1 lifecycle cases all remain
unrun. This prepares an experiment, not a successful G1 result or compatibility claim.
Next war-track work depends on those final observations; it does not block other
systems, require a third source dump or move the owner's final test campaign forward.
