# Real Westeros

A submod for **Crusader Kings III — A Game of Thrones (AGOT)**.

**Vision:** *Liberté, conséquences, immersion.* A living political Westeros in which player and AI characters can disobey, negotiate, make and break promises, pursue justice, and face persistent consequences.

## Project status

**Experimental CK3 script slices; not engine-tested.** The repository includes a
reconciliation incident, immediate/deferred endorsement negotiations, mediation,
independent personal case records, contested allegations, voluntary repair responses
and mutual promise cancellation. Private native-scheme observations connect to
voluntary political responses, judicial inspection and native prisoner/title/status
terms. Static checks and EN/FR localization are included. All CK3 runs await the
final campaign. CI builds a downloadable experimental ZIP with a commit/hash manifest;
see [integrated build](docs/INTEGRATED_BUILD.md). See [installation](docs/INSTALL.md) and
[final engine scenarios](docs/FINAL_ENGINE_TESTS.md). Illegal-war feasibility (G1)
remains unverified and is planned for the war-feature stage.

## Current milestone

Target-version scheme sources have been received and verified. Experimental
[discovery intake and private observation records](docs/RW010_SCHEME_EVIDENCE.md)
and [voluntary political responses](docs/RW010_SCHEME_RESPONSE.md) are implemented;
personal coercive justice and legal dynastic consequences remain to develop.
A first [political house-affair register and rehabilitation flow](docs/RW010_HOUSE_AFFAIRS.md)
is experimental; it changes political favor, not native landholding rights.
[G3 source investigation and an opt-in debug trace](docs/G3_HOUSE_SANCTIONS.md)
prepare final testing; no house landholding ban is implemented.
A [conditional rehabilitation offer](docs/RW010_HOUSE_TERMS.md) can exchange 50 personal
gold for ending one political censure, with explicit consent and current-role/funds
checks; native status, titles and criminal consequences remain separate.
**G1 is back
in the development plan for the war-feature stage**, rather than the immediate task.
Retain its research and diagnostic; establish authentic-CB feasibility before shipping
unlawful-war gameplay. Independent development can continue. See the original scenarios
in [GAME_DESIGN.md](docs/GAME_DESIGN.md). CK3 behavior remains unverified until tested.

## Repository guide

- [AGENTS.md](AGENTS.md) — mandatory instructions for coding agents
- [Design specification](docs/GAME_DESIGN.md) — eight related political systems and core rules
- [Technical gates](docs/TECHNICAL_GATES.md) — G1–G5 and verification requirements
- [Development workflow](docs/WORKFLOW.md) — how to work safely with GitHub/Codex
- [Static validation](docs/STATIC_VALIDATION.md) — Python tests, CI, and limitations
- [G1 engine test plan](docs/TEST_PLAN_G1.md) — authentic CB, Mega Wars and regression scenarios
- [Backlog](docs/BACKLOG.md) — ordered, actionable next work

## Boundaries

- **No paid infrastructure or external API costs.** Work within the existing ChatGPT Plus subscription and free tooling.
- Keep AGOT and CK3 installation files out of this public repository. Only ship original submod source and documentation; reference source-script paths, not copied game assets.
- Never edit the installed game or AGOT in place.
- Gameplay decisions are delegated to the coding/design agent unless they materially change the original vision. Record decisions in Git.
- Static checks are not a substitute for running CK3. In-game validation remains outstanding.

This repository is intended to be the single source of truth for code, task progress, and development decisions.
