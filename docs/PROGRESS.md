# Progress

- RW-001: complete — repository guidance and design summary committed.
- RW-002: scaffold created in `mod/`: CK3 local `.mod` descriptor, matching inner `descriptor.mod`, independent directory structure, and `docs/INSTALL.md`.
- Target declared in both descriptors: CK3 `1.19.*` (provisional based on AGOT 0.5.2.1 support for CK3 1.19.0.6).
- **Static verification:** `python3 scripts/validate_structure.py` checks UTF-8, script brace balance, repeated top-level definitions per file, and localization syntax/duplicate keys. Descriptor launcher path and matching version metadata checked manually. Engine parser not run.
- **Engine test:** not performed; actual CK3 executable, DLC and live AGOT version unverified.
- Gameplay implemented: none.
- RW-003: complete, static-checked; malformed fixture coverage is run through the validator's CLI against a temporary repository tree. This does not establish CK3 parsing or gameplay behavior.
- Next: RW-004 proof-of-concept for G1; no fake war CB.
- Budget: ChatGPT Plus only, no paid extras.
