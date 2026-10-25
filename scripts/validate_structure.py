#!/usr/bin/env python3
"""Conservative structural checks for the Real Westeros CK3 mod scaffold."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod/real_westeros"
SCRIPT_DIRS = ("common", "events")
LOCALIZATION = MOD / "localization"
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[^\s{}#"]+')
DEFINITION = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*=\s*(?=\{)")
LOC_KEY = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*:\d+\s+\"(?:\\.|[^\"\\])*\"\s*$")


def errors_for(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    definitions: dict[Path, set[str]] = defaultdict(set)
    localization_keys: dict[str, Path] = {}
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: cannot read as UTF-8 ({exc})")
            continue
        if path.suffix == ".txt" and path.parent.name in SCRIPT_DIRS:
            depth = 0
            for token in TOKEN.findall(text):
                if token.startswith("#") or token.startswith('"'):
                    continue
                if token == "{":
                    depth += 1
                elif token == "}":
                    depth -= 1
                    if depth < 0:
                        errors.append(f"{path.relative_to(ROOT)}: unmatched closing brace")
                        depth = 0
            if depth:
                errors.append(f"{path.relative_to(ROOT)}: {depth} unclosed brace(s)")
            for line in text.splitlines():
                match = DEFINITION.match(line)
                if match:
                    key = match.group(1)
                    if key in definitions[path]:
                        errors.append(f"{path.relative_to(ROOT)}: duplicate top-level definition {key}")
                    definitions[path].add(key)
        if path.is_relative_to(LOCALIZATION):
            for number, line in enumerate(text.splitlines(), 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                match = LOC_KEY.match(line)
                if not match:
                    errors.append(f"{path.relative_to(ROOT)}:{number}: malformed localization entry")
                    continue
                key = match.group(1)
                if key in localization_keys:
                    errors.append(f"{path.relative_to(ROOT)}:{number}: duplicate localization key {key}")
                localization_keys[key] = path
    return errors


def main() -> int:
    global ROOT, MOD, LOCALIZATION
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (used for isolated checks/tests)")
    args = parser.parse_args()
    ROOT = args.root.resolve()
    MOD = ROOT / "mod/real_westeros"
    LOCALIZATION = MOD / "localization"
    paths = [p for p in (ROOT / "mod").rglob("*") if p.is_file()]
    failures = errors_for(paths)
    if failures:
        print("\n".join(f"ERROR: {item}" for item in failures), file=sys.stderr)
        return 1
    print(f"PASS: structural checks passed for {len(paths)} mod files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
