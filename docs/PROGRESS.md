# Progress

- RW-001: complete — repository guidance and design summary committed.
- RW-002: complete — independent CK3 mod scaffold, relative launcher descriptor, and install instructions.
- RW-003: implemented stdlib-only validator, 12 positive/negative unit tests, and GitHub Actions CI. Local tests: **12 passed**; local scaffold structural check: **PASS**. See `docs/STATIC_VALIDATION.md`.
- **Static verification:** descriptor consistency, UTF-8, braces, selected top-level definitions, localization keys, and forbidden archive/save extensions. CI results must be checked separately after PR publication.
- **Engine test:** none. Actual CK3 executable, DLC and live AGOT version remain unverified; CK3 1.19.* descriptor target is provisional.
- Gameplay implemented: none. No CK3/AGOT scripts or assets added.
- RW-005: documented 16 reproducible G1 scenarios in `docs/TEST_PLAN_G1.md`, including real CB integrity, Mega Wars, AI parity, succession and save/reload. **Test plan only; zero scenarios executed in CK3.**
- Next: RW-004 — investigate G1 feasibility (illegal vassal war retaining original CB) against versioned CK3/AGOT sources. No fake CB.
- Budget: ChatGPT Plus only, no paid extras.
