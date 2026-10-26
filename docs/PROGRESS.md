# Progress

- RW-001: complete — repository guidance and design summary committed.
- RW-002: complete — independent CK3 mod scaffold, relative launcher descriptor, and install instructions.
- RW-003: implemented stdlib-only validator, 12 positive/negative unit tests, and GitHub Actions CI. Local tests: **12 passed**; local scaffold structural check: **PASS**. See `docs/STATIC_VALIDATION.md`.
- **Static verification:** descriptor consistency, UTF-8, braces, selected top-level definitions, localization keys, and forbidden archive/save extensions. CI results must be checked separately after PR publication.
- **Engine test:** none. Actual CK3 executable, DLC and live AGOT version remain unverified; CK3 1.19.* descriptor target is provisional.
- Gameplay implemented: none. No CK3/AGOT scripts or assets added.
- RW-005: documented 16 reproducible G1 scenarios in `docs/TEST_PLAN_G1.md`, including real CB integrity, Mega Wars, AI parity, succession and save/reload. **Test plan only; zero scenarios executed in CK3.**
- RW-004: created `docs/G1_FEASIBILITY.md` with versioned evidence, alternatives, rejected fake-CB workarounds and **BLOCKED** gate; added private-source locator `tools/audit_g1_sources.py` and 8 synthetic positive/negative tests. The source locator reports only relative paths/identifier line numbers; no CK3/AGOT assets were copied. The 1.20.1.2 third-party source index is not validation of target 1.19.* / AGOT 0.5.2.1.
- RW-006: documented G2 multi-clause UI options and the **unverified** CK3 engine gates in `docs/G2_FEASIBILITY.md`. Added a pure-Python, immutable, versioned offer protocol probe and in-memory revision authority (`tools/g2_offer_probe.py`). **18/18 synthetic positive/negative tests passed locally**, including stale counteroffers, duplicate responses and failed preconditions. This executes no CK3 effects and is not persistence or an in-game UI. Full project CI must be checked on the PR.
- Next: RW-007 persistence model with explicit save/reload and idempotency boundaries. G1 native war/CB spike still blocked; G2 UI/engine still unverified.
- Budget: ChatGPT Plus only, no paid extras.
