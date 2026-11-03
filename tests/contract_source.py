"""Bounded literal expansion of our six CK3 templates for source assertions only.

No trigger/effect evaluation, game model or claim to implement CK3's preprocessor.
Reject unsupported arguments rather than inventing engine fallback behavior.
"""
from pathlib import Path
import re
from test_native_scheme_evidence import block

MOD = Path(__file__).resolve().parents[1]/'mod/real_westeros'
TOKEN = re.compile(r'\$([A-Z_]+)\$')
CALL = re.compile(r'\b(rw_contract_\w+)\s*=\s*\{([^{}]*)\}')
ARG = re.compile(r'([A-Z_]+)\s*=\s*([A-Za-z0-9_:.-]+)')


def contract_templates():
    text = '\n'.join((MOD/p).read_text() for p in (
        'common/scripted_triggers/rw_contract_triggers.txt',
        'common/scripted_effects/rw_contract_effects.txt'))
    return {name:block(text,name) for name in re.findall(r'(?m)^(rw_contract_\w+)\s*=',text)}


def expand_contracts(text, templates=None):
    templates = contract_templates() if templates is None else templates
    def substitute(match):
        name,args = match.groups()
        if name not in templates:raise ValueError('Unknown contract template: '+name)
        pairs = ARG.findall(args)
        if ARG.sub('',args).strip() or len(pairs)!=len(dict(pairs)):
            raise ValueError('Unsupported or duplicate contract argument')
        values = dict(pairs)
        required = set(TOKEN.findall(templates[name]))
        if set(values)!=required:raise ValueError('Missing or extra contract argument: '+name)
        return TOKEN.sub(lambda token:values[token.group(1)],templates[name])
    expanded = CALL.sub(substitute,text)
    if re.search(r'\brw_contract_\w+\s*=',expanded):
        raise ValueError('Unsupported nested or nonliteral contract call')
    return expanded
