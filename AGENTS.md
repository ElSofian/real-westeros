# Instructions for Codex and other contributors

## Product intent
Develop Real Westeros as an independent CK3 AGOT submod. The three non-negotiable pillars are **Freedom, Consequences, Immersion**. Characters controlled by AI must have access to the same implemented gameplay actions, costs, prerequisites and consequences as player characters. Do not use an LLM at game runtime, and do not impose an arbitrary cap on useful interactions.

## Work discipline
1. Read `docs/GAME_DESIGN.md`, `docs/TECHNICAL_GATES.md`, and `docs/BACKLOG.md` before choosing work.
2. Deliver one bounded, testable change per PR. Prefer additive script files and avoid overwriting vanilla/AGOT definitions, especially global war and lifecycle hooks.
3. Preserve vanilla and AGOT behaviors (Mega Wars, wars, titles, dynastic succession, banking and secrets). An assumption found only in source scripts is not a successful in-game test.
4. Keep a brief progress record in `docs/PROGRESS.md`: what's implemented, checks run, remaining risks and next task. Update backlog status in the same PR.
5. Use available static checks and include a negative-path test. Never claim CK3 gameplay functionality or performance without a real CK3 run.
6. Never commit any original CK3 or AGOT code, textures, copyrighted assets, full extracted scripts, personal saves, credentials, or local installation paths.
7. No paid cloud services, credits, APIs, hosted servers or new subscriptions.
8. Keep responses and PR summaries concise. The owner delegates normal engineering and design choices; escalate only major vision changes or real blockers.
9. If an action depends on a technical gate, mark it experimental; never silently replace the authentic casus belli with a fake generic one.
10. Do not autonomously merge an unverified gameplay PR to `main`. Open a draft PR when there is uncertainty.

## First assignment
Investigate G1: a vassal war disallowed by political law while retaining the authentic CB and CK3/AGOT lifecycle. Start with a precise feasibility investigation and a minimal isolated spike. If local CK3/AGOT sources are absent, document exact references to inspect rather than guess code or claim tests.

## Validation labels
- **Static-checked:** parser or structural checks pass, but engine behavior not demonstrated.
- **Engine-tested:** observed directly in CK3 with reproducible steps.
- **Blocked:** missing engine capability, source, or required environment.
