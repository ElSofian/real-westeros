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
10. Routine decisions, documentation, scaffolds, and statically verifiable submod code can be reviewed and merged autonomously after actual available checks pass. Explicitly mark CK3 behavior as **not engine-tested** until in-game validation. Keep risky core war / Mega Wars changes isolated when they cannot be checked without the engine, and never present them as working. Do not merge failing checks or changes that distribute third-party assets.

## Exclusive task ownership (mandatory)
Before starting, modifying, or merging a backlog task, follow [docs/TASK_CLAIMS.md](docs/TASK_CLAIMS.md). The **exclusive claim** is an atomic GitHub Contents API `create_file` on `main` at `.github/task-claims/RW-XXX.json` with no old-file SHA. Give each execution a unique owner. A preexisting claim means **do not touch that task**; pick another independent task or stop. Recheck ownership before pushes/PR merges and release with a checked blob SHA. Never assume a mere issue label, existing branch or elapsed TTL means ownership. If claim tools/auth are unavailable, fail closed for task development. This applies equally to scheduled ChatGPT, manual ChatGPT and Codex Cloud.

## Nonblocking environment policy
A missing local CK3/AGOT installation does **not** block repository scaffolding, game design, ordinary Git operations, static verification, or isolated experimental source changes. Use the verified relative launcher path `path="mod/real_westeros"`; document the usual CK3 user-data destination instead of requesting or inventing a personal absolute path. The descriptor currently targets CK3 `1.19.*` based on AGOT 0.5.2.1 declaring support for 1.19.0.6; do not claim it was engine-verified. Mark engine-dependent behavior *unverified* until tested. If a particular GitHub action is unavailable in your agent session, use the configured Git CLI if possible; otherwise commit locally and report the precise missing permission/tool, without discarding finished work. A lack of one publishing action is not a reason to avoid working on files.

## First assignment
After RW-002 scaffold, undertake RW-003 static checks, then investigate G1: a vassal war disallowed by political law while retaining the authentic CB and CK3/AGOT lifecycle. Start with a precise feasibility investigation and a minimal isolated spike. If local CK3/AGOT sources are absent, document exact references to inspect rather than guess code or claim tests. Continue with independent tasks that do not require those sources.

## Validation labels
- **Static-checked:** parser or structural checks pass, but engine behavior not demonstrated.
- **Engine-tested:** observed directly in CK3 with reproducible steps.
- **Blocked:** missing engine capability, source, or required environment.

## Autonomous continuation
The owner does not want to relay messages between separate agents or approve ordinary PRs. When operating in a scheduled ChatGPT/Work run with GitHub tools, advance the next self-contained backlog task directly if possible: inspect repository, edit on a feature branch, verify what can be verified, create/review a PR, merge safe changes, and update `docs/PROGRESS.md`. If an integration cannot launch Codex Cloud, do not request that the owner copy/paste prompts as a routine workaround; use available capabilities for useful direct progress. A scheduled task is *not* evidence of uninterrupted Codex execution. Stop on quota exhaustion and record genuine blockers. No new paid services.
