#!/usr/bin/env python3
"""Verify registered gameplay text is unchanged after removing observation calls."""
import hashlib
import json
from pathlib import Path
import re
try:
    from .validate_mod import clean_script
except ImportError:
    from validate_mod import clean_script

ROOT = Path(__file__).resolve().parents[1]
CALL = re.compile(r'\brw_tm_(?:emit|commit)_effect\s*=\s*\{[^{}]*\}')


def gameplay_digest(text):
    clean = clean_script(text)[0]
    clean = CALL.sub('', clean)
    clean = re.sub(r'\belse\s*=\s*\{\s*\}', '', clean)
    return hashlib.sha256(re.sub(r'\s+', '', clean).encode()).hexdigest()


def verify(root=ROOT):
    registry = json.loads((root / 'docs/TELEMETRY_HOOKS.json').read_text())
    errors = []
    for name, expected in registry['gameplay_sha256'].items():
        if gameplay_digest((root / name).read_text(encoding='utf-8-sig')) != expected:
            errors.append(name + ': gameplay changed beyond telemetry')
    library = (root / 'mod/real_westeros/common/scripted_effects/rw_telemetry_effects.txt').read_text()
    # A small explicit vocabulary prevents native operations slipping into the logger.
    allowed = {'rw_tm_start_effect', 'rw_tm_stop_effect', 'rw_tm_emit_effect',
               'rw_tm_commit_effect', 'rw_tm_enabled_trigger', 'set_global_variable',
               'remove_global_variable', 'change_global_variable', 'name', 'value',
               'days', 'debug_log', 'if', 'limit', 'else', 'is_ai', 'add',
               'FAMILY', 'ACTION', 'STAGE', 'save_scope_as', 'exists', 'has_variable', 'set_variable',
               'global_var:rw_tm_budget', 'scope:rw_tm_actor', '$CONTAINER$'}
    clean = clean_script(library)[0]
    for key in re.findall(r'([\w:$]+)\s*=\s*', clean):
        if key not in allowed:
            errors.append('logger has unapproved operation: ' + key)
    for value in re.findall(r'\bname\s*=\s*(\S+)', clean):
        if not value.startswith('rw_tm_'):
            errors.append('logger writes non-telemetry state')
    for line in re.findall(r'debug_log\s*=\s*"([^"]*)"', library):
        if not re.fullmatch(r'RW_TM1 family=(?:telemetry|\$FAMILY\$) action=(?:session|\$ACTION\$) stage=(?:start|stop|truncated|\$STAGE\$) control=(?:unknown|ai|player)', line):
            errors.append('logger contains nonliteral or personal data')
    return errors


if __name__ == '__main__':
    errors = verify()
    print('\n'.join(errors) if errors else 'PASS: telemetry removal restores registered gameplay; logger is metadata-only')
    raise SystemExit(bool(errors))
