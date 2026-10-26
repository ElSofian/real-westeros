# Static validation

Run from the repository root using **Python 3.10+**, with no third-party packages:

```bash
python -m unittest discover -s tests -v
python tools/validate_mod.py
```

The `Validate submod` GitHub Actions workflow runs both commands on pull requests and pushes to `main`. This workflow uses GitHub-hosted runners; the project does not use a paid external API or hosted server.

## What it checks

- Both descriptor files exist, contain required `name`, `version` and `supported_version` fields, and agree.
- The outer descriptor uses the relative path `mod/real_westeros`; the inner descriptor has no `path`.
- The expected source directories exist.
- Text files are readable as UTF-8 (localization `.yml` also supports a UTF-8 BOM); NUL bytes and obvious binary archives/executables/save files are rejected.
- CK3-style `.txt`, `.mod`, `.gui`, `.gfx` and `.asset` text has balanced braces, ignoring comments and quoted strings.
- Top-level named blocks are not duplicated across files within the same scripted-trigger, scripted-effect, or character-interaction directory.
- Localization `.yml` files have a language header and do not duplicate keys in the same language.

## Deliberate limitations

**This is not a CK3/AGOT script parser or an engine test.** It does not verify valid CK3 keywords, event IDs, effects, scopes, localization rendering, load order, supported DLC, performance, war CB preservation, or Mega Wars behavior. Top-level definition scanning is intentionally conservative (line-oriented); complex same-line constructs are not exhaustively analyzed. Files in other subdirectories may require additional checks as gameplay grows.

File-extension checks cannot establish whether a text file or asset is third-party copyrighted content. Human/code review must still ensure that no CK3/AGOT source files or proprietary assets are committed. The checks deliberately do not ban original mod-created image assets by extension.

A green CI run means **static-checked only**, never **engine-tested**. In-game verification remains necessary before declaring gameplay complete.

## Private G1 source locator (RW-004)

`python tools/audit_g1_sources.py --ck3-root "<CK3>/game" --agot-root "<AGOT>"`

This optional local-only check identifies candidate source files and identifier line numbers. It does not copy or output any source code or personal paths. It cannot be run in CI without private game files, and `LOCATED_UNVERIFIED` is **not** a CK3 parsing, feasibility, or engine-test result. Synthetic positive/negative tests for the locator run with the normal `unittest discover` command. See `docs/G1_FEASIBILITY.md`.

## G2 negotiation protocol probe (RW-006)

`tools/g2_offer_probe.py` is a **Python-only state-machine proof**, not CK3 script. Its 16 positive/negative tests run with the standard unittest command. It models versioned consent and an in-memory current-revision authority; it does **not** implement save/load, a CK3 UI, native transfers or atomic CK3 transactions. See `docs/G2_FEASIBILITY.md`.
