# Individual titles and status — source review and native UI handoffs

Experimental original CK3 scripts, **not engine-tested**. This extends the private
prisoner panel, not the native definition of nobility, titles or house sanctions.

## What is implemented

From the existing personal prisoner panel, **Examine this prisoner's titles and
standing** opens a read-only view of the exact living participant in the free
observer's current custody. The existing observer-only story/schema/serial/retention
reader and exposed-participant identity remain required. Navigation and every UI
handoff recheck current access. The portrait is that exact stored participant.

The view keeps independent present-state facts:

- Observer-to-participant native title-revocation grounds, not inferred from arrest
  or execution grounds. A character-level reason does not identify this plot or
  guarantee that a selected title can be taken lawfully.
- AGOT's current knight recognition, through its existing predicate rather than a
  guessed trait-only equivalent. A current stripped-knight trait is shown separately;
  neither state is attributed to this observation or to our previous UI clicks.
- A current landed-knight contract, only in a current liege context. Presence does
  not mean landholding is banned; absence does not establish noble/family status.

For a landed direct vassal, the human observer can open the normal title-revocation
window if `is_character_interaction_valid` accepts that exact native interaction and
recipient. No title is preselected. The normal title picker, laws, contracts, hooks,
costs, consent/refusal, tyranny and title lifecycle remain authoritative. The view
can also reopen the existing guarded release window; native available terms may
include personal status sanctions. It does not assert that any particular term is
available or select it. Closing leaves the situation unchanged.

Opening is not sending, revoking, releasing, modifying status or recording a
completed sanction. No direct title/trait/contract mutation, reason consumption,
house-relation penalty, imprisonment change, pardon, reminder or inherited guilt
is added. Existing voluntary payments/refusals remain separate. The native UI
shortcuts are human-facing; existing native AI actions are not replaced or extended
with an automatic forced interaction.

## Findings from the private target-version sources

`TITLE_STATUS_SOURCE_RECEIPT.json` records relative references, SHA-256 and marker
lines only. Originals/full private manifest stay outside Git. Dispatch references
are already in JUSTICE_SOURCE_RECEIPT.json. Received AGOT metadata is 0.5.2.1 /
supported CK3 1.19.0.6; the executable remains unverified.

The inspected native revocation is a special title-target interaction with its own
title picker, title exclusions, legal/contract conditions and refusal handling.
Its helper consumes native revocation grounds and applies consequences; calling it
independently would skip the full interaction path. A native AGOT event also uses
`run_interaction` for revocation, but its execute-threshold/automatic target semantics
were not established as suitable for a voluntary choice. We deliberately do not
use that force-send path, duplicate helpers or overwrite native callbacks.

The observed release terms distinguish:

1. **Strip knighthood:** a personal status change with native traits, relationships,
   opinions, memories and future knighting restrictions. Not house-wide loss of
   nobility and not confiscation of every relative's titles.
2. **Strip lordship:** in this version, a particular native punishment involving
   landed-knight contract conversion and duchy destruction, prestige/memory/opinion
   and house-relation consequences. It does not implement a universal land ban or
   a configurable 50-year house ban. Its current native eligibility explicitly
   restricts the actor to human control and includes prisoner/vassal/tier checks.
   Preserve that existing AGOT restriction; do not silently advertise AI parity for
   this native term, or copy/rewrite it to make a new mod-only exception. New
   Real Westeros gameplay must still use shared player/AI rules.

These source findings do not prove actual engine effects, native AI behavior, load
composition or save compatibility. The dependency frontier is not fully resolved.
A current trait/contract is never treated as proof that a specific offense was
punished. A previously consumed reason is not restored on inspection.

## Limits and final verification

Twelve source-contract tests include wrong/stale custody, reason direction,
recognition/contract conflation, native validity/action/actor/recipient mutations,
preselected punishment terms, forced transfer and cached-result mutations. All
engine scenarios TITLE-01…09 remain deferred in FINAL_ENGINE_TESTS.md.

In particular, the native **title-target** picker may require scope setup not
established by the generic source-located window opener. Its validity query could
reject an unselected target or the window could fail to populate. Final testing
must demonstrate opening, selection, cancellation and confirmation separately;
until then this shortcut is experimental, not a proven confiscation feature. The
normal character menu is the fallback; do not bypass validity or invent a target
to make the button appear. Native status terms must be compared to baseline AGOT.

Next address G3: map the supported scope and lifecycle of a house sanction and
restoration, including authority, disclosure, duration and succession. Audit grant,
inheritance, election and conquest separately before claiming an enforced ban on
holding land. A political house marker alone cannot satisfy the owner's 50-year
landholding-ban scenario. Collective sanctions and restoration remain unimplemented;
G1 remains for the later unlawful-war stage. RW-010 stays in progress.
