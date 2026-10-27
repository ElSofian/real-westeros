#!/usr/bin/env python3
"""Locate G1 war integration points in privately installed CK3/AGOT sources.

Only relative file names, marker names, and line numbers are printed.
This is a source-location aid, NOT a CK3 parser or a feasibility verdict.
"""

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys

from validate_mod import clean_script


@dataclass(frozen=True)
class SourceReference:
    source: str
    relative_path: str
    markers: tuple[str, ...] = ()


REFERENCES = (
    SourceReference(
        "CK3", "common/character_interactions/00_war.txt",
        ("declare_war_interaction", "has_any_display_cb_on",
         "war_declarer_needs_hook_on_liege"),
    ),
    SourceReference(
        "CK3", "common/scripted_triggers/00_war_and_peace_triggers.txt",
        ("war_declarer_needs_hook_on_liege",),
    ),
    SourceReference(
        "AGOT", "common/character_interactions/00_war.txt",
        ("declare_war_interaction", "can_attack_in_hierarchy"),
    ),
    SourceReference(
        "AGOT", "common/scripted_triggers/00_war_and_peace_triggers.txt",
        ("war_declarer_needs_hook_on_liege",),
    ),
    SourceReference(
        "AGOT", "common/scripted_triggers/00_agot_mega_wars_triggers.txt",
    ),
    SourceReference(
        "AGOT", "common/on_action/agot_on_actions/agot_war_on_actions.txt",
    ),
    SourceReference(
        "AGOT", "common/story_cycles/agot_story_cycle_mega_wars.txt",
    ),
)


def marker_line_numbers(text: str, markers: tuple[str, ...]) -> dict[str, list[int]]:
    """Search uncommented, unquoted script for exact identifier tokens."""
    cleaned, _ = clean_script(text)
    lines = cleaned.splitlines()
    return {
        marker: [
            number for number, line in enumerate(lines, 1)
            if re.search(r"(?<![A-Za-z0-9_])" + re.escape(marker)
                         + r"(?![A-Za-z0-9_])", line)
        ]
        for marker in markers
    }


def audit(ck3_root: Path, agot_root: Path, references=REFERENCES) -> list[dict]:
    roots = {"CK3": ck3_root, "AGOT": agot_root}
    findings = []
    for reference in references:
        entry = {
            "source": reference.source,
            "file": reference.relative_path,
            "status": "MISSING",
            "markers": {},
        }
        path = roots[reference.source] / reference.relative_path
        if not path.is_file():
            findings.append(entry)
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            entry["status"] = "UNREADABLE"
            findings.append(entry)
            continue
        if not text.strip():
            entry["status"] = "EMPTY"
            findings.append(entry)
            continue
        entry["markers"] = marker_line_numbers(text, reference.markers)
        entry["status"] = (
            "REVIEW_MARKERS" if any(not positions for positions in entry["markers"].values())
            else "LOCATED_UNVERIFIED"
        )
        findings.append(entry)
    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ck3-root", type=Path, required=True,
                        help="Local CK3 game/ directory (contains common/)")
    parser.add_argument("--agot-root", type=Path, required=True,
                        help="Local AGOT mod directory (contains common/)")
    parser.add_argument("--json", action="store_true",
                        help="Print only relative references and marker line numbers as JSON")
    args = parser.parse_args(argv)
    findings = audit(args.ck3_root, args.agot_root)
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        for entry in findings:
            print(f"{entry['status']}: {entry['source']}/{entry['file']}")
            for marker, lines in entry["markers"].items():
                print(f"  {marker}: {','.join(map(str, lines)) or 'NOT FOUND'}")
        print("Source locations only. No CB, war, AGOT hook, or engine behavior verified.")
    return 0 if all(f["status"] == "LOCATED_UNVERIFIED" for f in findings) else 1


if __name__ == "__main__":
    sys.exit(main())
