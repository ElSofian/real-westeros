# Codex implementation handoff

## Current owner direction (supersedes the historical session text below)

RW-008/009 source slices are integrated, not engine-tested. G1 / RW-004 is restored
to todo for the war-feature stage; it is neither on hold nor the immediate task.
Resolve it before shipping unlawful-war gameplay, without blocking independent work.
The original three scenarios are recorded in GAME_DESIGN.md. Next: reconciliation
audit and validation. The RW-008 launch text below is historical.

## Current target: RW-008

Implement a first **original CK3-facing political incident**, not merely another Python simulation. Read `AGENTS.md`, `docs/TASK_CLAIMS.md`, `docs/BACKLOG.md`, and `docs/PROGRESS.md`.

- Acquire the exclusive RW-008 GitHub claim on `main` before task edits.
- Work in an isolated feature branch. Avoid blocked unlawful-war / real CB / Mega Wars mechanics.
- Add genuine Paradox/CK3 mod scripts, localization, appropriate triggers and effects. Do not represent the RW-007 offline Python ledger as native CK3 persistence.
- Include static checks, negative-path tests, and a reproducible future in-game test scenario.
- Give AI actors access to applicable actions or label the vertical slice experimental.
- Create a PR and update progress. All CK3 behavior remains **not engine-tested** until actually run.
- Do not commit proprietary CK3/AGOT assets, use paid APIs, or demand the owner's PC remain online.

RW-008 counts as implemented only with reviewable CK3 mod files and supporting evidence, not a Python-only probe. After completion, proceed to RW-009 in a separately claimed task if the Codex session allows.

## Session start text

```text
Continue Real Westeros as principal implementation agent. Read AGENTS.md, docs/CODEX_HANDOFF.md, docs/TASK_CLAIMS.md, docs/BACKLOG.md and docs/PROGRESS.md. Deliver RW-008 as a genuine CK3-facing political incident with original scripts, localization, tests and a PR. Acquire and verify the exclusive GitHub RW-008 claim on main first; otherwise do not duplicate anyone's work. Work through implementation, checks, failures and fixes within the current session; proceed to RW-009 only after RW-008 is integrated and separately claimed. Do not claim engine validation without CK3, invent missing source hooks, ask the owner to relay messages, or spend beyond Plus.
```

If a Codex Goal-enabled surface supports `/goal`, the owner can use this as a bounded persistent objective. This is **not guaranteed to be available in every Codex Cloud interface**. ChatGPT has no tool to launch Codex Cloud, and GitHub access alone is not a Codex execution trigger.

## Coordinator checks

The scheduled worker prioritizes reviewing actual PR diffs, test evidence and CI results, correcting clear problems, and safely merging. It must honor task claims. If Codex is not working, it can continue independently on a safely claimed task. Green static CI does not prove CK3 gameplay. Do not substitute a paid Agents API schedule for included Plus access.
