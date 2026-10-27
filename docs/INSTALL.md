# Installing the Real Westeros submod (manual development build)

> **Status:** Experimental integrated scripts for reconciliation, services, mediation and allegations are included. **No in-game test has been performed.** See INTEGRATED_BUILD.md for included features, exclusions, build integrity and GitHub artifact downloads.

## Development target and version

- CK3 AGOT audit source: AGOT descriptor version `0.5.2.1`, advertising supported CK3 version `1.19.0.6`.
- The Real Westeros descriptors **provisionally target CK3 `1.19.*`**; this metadata is a target, not proof of compatibility with the installed game or all AGOT versions.
- Actual CK3 executable version, AGOT version at future test time, DLC and playset combinations remain to be verified.

## Install on Windows

1. If using a build artifact, extract the outer GitHub artifact first, then extract the inner `RealWesteros-experimental.zip` into a temporary folder. Its `mod/` directory contains the two items to copy below. For a source checkout, use the repository’s `mod/` directory directly. Do not install the repository, its Python tools or the ZIP into the Steam game directory.
2. Locate the active CK3 user-data folder. The usual Windows location is `Documents/Paradox Interactive/Crusader Kings III/mod/`, but it can be relocated (e.g., OneDrive). The Paradox Launcher **Show in Folder** option for an existing mod helps determine the actual path.
3. From the extracted build or repository, copy **both** `mod/real_westeros.mod` and the complete `mod/real_westeros/` folder into that CK3 `mod/` directory.
4. The resulting structure must look like:

```text
Crusader Kings III/
└── mod/
    ├── real_westeros.mod
    └── real_westeros/
        ├── descriptor.mod
        ├── common/
        ├── events/
        └── localization/
```

5. The outer `real_westeros.mod` uses the **relative** entry `path="mod/real_westeros"`. Do not replace it with an invented absolute path. If the launcher does not resolve the mod, inspect its actual game-data directory and adjust the local copy of the outer descriptor as needed.
6. In the Launcher, enable **A Game of Thrones** and **Real Westeros**, loading Real Westeros **after** AGOT in the playset.
7. Reopen the launcher if needed. Seeing the mod is **not** evidence that its scripts parse or gameplay works.

## What to validate later

- Launcher recognizes the outer and inner descriptors.
- Actual CK3 + AGOT versions match the selected development target.
- Mod loads after AGOT, without descriptor/path errors.
- Included scripted content passes CK3's parser and the specific runtime scenarios.

Never commit installation files, full CK3 or AGOT scripts, downloaded game assets, personal saves or credentials.

## Updating and removing an experimental build

Before updating, retain a copy of the previous mod folder and use a disposable save.
Remove the previous `real_westeros/` folder, then copy the new folder and outer
`real_westeros.mod`; merging folders can leave obsolete scripts behind. Do not remove
AGOT, game files or personal saves. Older experimental-save migration is unverified.
To stop using the submod, disable it in the playset; do not assume an existing save
with active stories/obligations will safely migrate after removal.
