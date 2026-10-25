# Installing the Real Westeros submod (manual development build)

> **Status:** The repository currently includes a bare mod scaffold only, with **no gameplay changes**. No in-game test has been performed.

## Development target and version

- CK3 AGOT audit source: AGOT descriptor version `0.5.2.1`, advertising supported CK3 version `1.19.0.6`.
- The Real Westeros descriptors **provisionally target CK3 `1.19.*`**; this metadata is a target, not proof of compatibility with the installed game or all AGOT versions.
- Actual CK3 executable version, AGOT version at future test time, DLC and playset combinations remain to be verified.

## Install the scaffold on Windows

1. Locate the active CK3 user-data folder. The usual Windows location is `Documents/Paradox Interactive/Crusader Kings III/mod/`, but it can be relocated (e.g., OneDrive). The Paradox Launcher **Show in Folder** option for an existing mod helps determine the actual path.
2. From this repository, copy **both** `mod/real_westeros.mod` and the complete `mod/real_westeros/` folder into that CK3 `mod/` directory.
3. The resulting structure must look like:

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

4. The outer `real_westeros.mod` uses the **relative** entry `path="mod/real_westeros"`. Do not replace it with an invented absolute path. If the launcher does not resolve the mod, inspect its actual game-data directory and adjust the local copy of the outer descriptor as needed.
5. In the Launcher, enable **A Game of Thrones** and **Real Westeros**, loading Real Westeros **after** AGOT in the playset.
6. Reopen the launcher if needed. Seeing the mod is **not** evidence that any gameplay has been implemented or tested.

## What to validate later

- Launcher recognizes the outer and inner descriptors.
- Actual CK3 + AGOT versions match the selected development target.
- Mod loads after AGOT, without descriptor/path errors.
- Future scripted content passes CK3's parser and the specific runtime scenarios.

Never commit installation files, full CK3 or AGOT scripts, downloaded game assets, personal saves or credentials.
