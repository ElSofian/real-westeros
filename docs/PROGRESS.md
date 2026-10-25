# Progress

- RW-001: complete — repository guidance and design summary committed.
- RW-002: complete — independent CK3 mod scaffold, relative launcher descriptor, and install instructions.
- RW-003: implemented stdlib-only validator, 12 positive/negative unit tests, and GitHub Actions CI. Local tests: **12 passed**; local scaffold structural check: **PASS**. See `docs/STATIC_VALIDATION.md`.
- **Static verification:** descriptor consistency, UTF-8, braces, selected top-level definitions, localization keys, and forbidden archive/save extensions. CI results must be checked separately after PR publication.
- **Engine test:** none. Actual CK3 executable, DLC and live AGOT version remain unverified; CK3 1.19.* descriptor target is provisional.
- Gameplay implemented: none. No CK3/AGOT scripts or assets added.
- Next: RW-004 — investigate G1 (illegal vassal war retaining original CB), followed by RW-005 reproducible engine test plan. No fake CB.
- Budget: ChatGPT Plus only, no paid extras.
