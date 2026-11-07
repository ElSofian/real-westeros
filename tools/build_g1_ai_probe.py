#!/usr/bin/env python3
"""Build original console-only probes of the installed native war selector.

Not a gameplay AI initiator, not an autonomous-AI test, and not a native override.
"""
import argparse
import hashlib
import json
from pathlib import Path

try:
    from .validate_mod import brace_errors
except ImportError:
    from validate_mod import brace_errors

ROOT = Path(__file__).resolve().parents[1]
SMOKE = 'debug_log = "RW_AI1 smoke_ok"\n'
REBIND = '''# Current sampling of the explicitly named fixture, not historical war context.
remove_global_variable = rw_ai1_actor
remove_global_variable = rw_ai1_target
remove_global_variable = rw_ai1_title
if = {
    limit = {
        exists = character:Hightower_5
        exists = character:Redwyne_4
        character:Hightower_5 = { this = title:d_oldtown.holder }
        character:Redwyne_4 = { this = title:d_the_arbor.holder }
    }
    set_global_variable = { name = rw_ai1_actor value = character:Hightower_5 days = 7 }
    set_global_variable = { name = rw_ai1_target value = character:Redwyne_4 days = 7 }
    set_global_variable = { name = rw_ai1_title value = title:d_the_arbor days = 7 }
    debug_log = "RW_AI1 fixture_bound"
}
else = { debug_log = "RW_AI1 fixture_changed" }
'''
SETUP = '''# Run only as Leyton after loading the disposable pre-war save.
remove_global_variable = rw_ai1_actor
remove_global_variable = rw_ai1_target
remove_global_variable = rw_ai1_title
if = {
    limit = {
        is_ai = no
        this = title:d_oldtown.holder
        is_alive = yes is_adult = yes is_landed = yes is_imprisoned = no
        is_at_war = no
        gold >= 150
        has_claim_on = title:d_the_arbor
        exists = liege
        title:d_the_arbor.holder = {
            is_alive = yes is_adult = yes is_landed = yes is_imprisoned = no
            liege = root.liege
        }
    }
    # A disclosed hostile political fixture, never a native offense or sanction.
    set_relation_rival = liege
    set_global_variable = { name = rw_ai1_actor value = this days = 7 }
    set_global_variable = { name = rw_ai1_target value = title:d_the_arbor.holder days = 7 }
    set_global_variable = { name = rw_ai1_title value = title:d_the_arbor days = 7 }
    debug_log = "RW_AI1 setup_ok"
}
else = { debug_log = "RW_AI1 setup_refused" }
'''
CLEANUP = '''remove_global_variable = rw_ai1_actor
remove_global_variable = rw_ai1_target
remove_global_variable = rw_ai1_title
remove_global_variable = rw_ai1_compare_stage
debug_log = "RW_AI1 cleanup"
'''
INSPECT = '''# Extend only the exact existing diagnostic handles before a natural AI tick.
if = {
    limit = {
        exists = global_var:rw_ai1_actor
        exists = global_var:rw_ai1_target
        exists = global_var:rw_ai1_title
    }
    global_var:rw_ai1_actor = {
        if = {
            limit = {
                is_ai = yes is_alive = yes is_landed = yes is_at_war = no
                has_claim_on = global_var:rw_ai1_title
                liege = global_var:rw_ai1_target.liege
                global_var:rw_ai1_title.holder = global_var:rw_ai1_target
            }
            set_global_variable = { name = rw_ai1_actor value = this days = 7 }
            set_global_variable = { name = rw_ai1_target value = global_var:rw_ai1_target days = 7 }
            set_global_variable = { name = rw_ai1_title value = global_var:rw_ai1_title days = 7 }
            debug_log = "RW_AI1 inspect_ready"
            if = {
                limit = {
                    can_declare_war = {
                        defender = global_var:rw_ai1_target
                        casus_belli = claim_cb
                        claimant = global_var:rw_ai1_actor
                        target_titles = { global_var:rw_ai1_title }
                    }
                }
                debug_log = "RW_AI1 inspect_native_legality_yes"
            }
            else = { debug_log = "RW_AI1 inspect_native_legality_no" }
        }
        else = { debug_log = "RW_AI1 inspect_context_failed" }
    }
}
else = { debug_log = "RW_AI1 inspect_missing_setup" }
'''
# Bounded read-only audit of the same actor predicates used by the selector probe.
AUDIT_CHECKS = (
    ('ai', 'is_ai = yes'), ('alive', 'is_alive = yes'),
    ('adult', 'is_adult = yes'), ('landed', 'is_landed = yes'),
    ('free', 'is_imprisoned = no'), ('peace', 'is_at_war = no'),
    ('gold', 'gold >= 150'), ('claim', 'has_claim_on = global_var:rw_ai1_title'),
    ('uncommitted', 'rw_ai_existing_commitment_trigger = no'),
    ('hostile', 'opinion = { target = liege value <= -25 }'),
    ('peers', 'liege = global_var:rw_ai1_target.liege'),
    ('holder', 'global_var:rw_ai1_title.holder = global_var:rw_ai1_target'),
)
AUDIT = '\n'.join('if = { limit = { '+trigger+' } debug_log = "RW_AI1 check_'+name+'_yes" }\n'
                  'else = { debug_log = "RW_AI1 check_'+name+'_no" }'
                  for name, trigger in AUDIT_CHECKS)
INSPECT = INSPECT.replace('global_var:rw_ai1_actor = {\n',
                          'global_var:rw_ai1_actor = {\n'+AUDIT+'\n', 1)


def case(mode):
    if mode not in ('allowed', 'banned', 'reject'):
        raise ValueError('Unknown diagnostic mode')
    law = 'crown_authority_2' if mode == 'banned' else 'crown_authority_0'
    reject = '\n                    always = no' if mode == 'reject' else ''
    hostility = 'opinion = { target = liege value <= -25 }' if mode == 'banned' else ''
    return '''# Manually invoked native-selector diagnostic, never autonomous initiative.
if = {
    limit = {
        exists = global_var:rw_ai1_actor
        exists = global_var:rw_ai1_target
        exists = global_var:rw_ai1_title
    }
    global_var:rw_ai1_actor = {
        if = {
            limit = {
                is_ai = yes
                is_alive = yes is_adult = yes is_landed = yes is_imprisoned = no
                is_at_war = no
                gold >= 150
                has_claim_on = global_var:rw_ai1_title
                rw_ai_existing_commitment_trigger = no
                HOSTILITY
                liege = global_var:rw_ai1_target.liege
                global_var:rw_ai1_target = {
                    is_alive = yes is_adult = yes is_landed = yes is_imprisoned = no
                }
                global_var:rw_ai1_title.holder = global_var:rw_ai1_target
            }
            liege = {
                if = {
                    limit = { NOT = { has_realm_law = LAW } }
                    add_realm_law = LAW
                }
            }
            save_scope_as = actor
            global_var:rw_ai1_target = { save_scope_as = recipient }
            save_scope_value_as = { name = hook value = no }
            save_scope_value_as = { name = rw_uw_defy value = no }
            debug_log = "RW_AI1 MODE_begin"
            if = {
                limit = { rw_uw_ai_default_defiance_trigger = yes }
                debug_log = "RW_AI1 MODE_default_defiance_yes"
            }
            else = { debug_log = "RW_AI1 MODE_default_defiance_no" }
            # This requests native recalculation once. It does not prove regular
            # scheduler discovery, choice, option construction or dispatch.
            ai_start_best_war = {
                cb = { claim_cb }
                recalculate_cb_targets = yes
                is_valid = {
                    scope:target_character = global_var:rw_ai1_target
                    scope:target_title = global_var:rw_ai1_titleREJECT
                    debug_log_details = yes
                }
                on_success = { debug_log = "RW_AI1 MODE_success" }
                on_failure = { debug_log = "RW_AI1 MODE_failure" }
            }
            debug_log = "RW_AI1 MODE_end"
        }
        else = { debug_log = "RW_AI1 MODE_precondition_failed" }
    }
}
else = { debug_log = "RW_AI1 MODE_missing_setup" }
'''.replace('LAW', law).replace('MODE', mode).replace('REJECT', reject).replace('HOSTILITY', hostility)


def payload():
    files = {'rw_ai1_smoke.txt': SMOKE, 'rw_ai1_setup.txt': SETUP,
             'rw_ai1_cleanup.txt': CLEANUP, 'rw_ai1_inspect.txt': INSPECT}
    files.update({'rw_ai1_' + mode + '.txt': case(mode) for mode in ('allowed', 'banned', 'reject')})
    for name in ('rw_ai1_inspect.txt', 'rw_ai1_allowed.txt', 'rw_ai1_banned.txt', 'rw_ai1_reject.txt'):
        files[name] = REBIND + files[name]
    files['rw_ai1_compare.txt'] = comparison()
    for text in files.values():
        if brace_errors(text):
            raise ValueError('Invalid original console script')
    return {name: ('\ufeff' + text).encode('utf-8') for name, text in files.items()}


def comparison():
    """One disposable matched comparison, stopping immediately on a bad control."""
    fixture = '''set_global_variable = { name = rw_ai1_compare_stage value = flag:unready days = 1 }
if = {
    limit = {
        exists = global_var:rw_ai1_actor
        exists = global_var:rw_ai1_target
        global_var:rw_ai1_actor = {
            is_ai = yes is_alive = yes is_at_war = no
            liege = global_var:rw_ai1_target.liege
            has_claim_on = global_var:rw_ai1_title
        }
    }
    # Disclosed seven-day native debug opinion in the disposable comparison only.
    global_var:rw_ai1_actor = {
        add_opinion = { target = liege modifier = debug_hates_liege_opinion days = 7 }
        if = {
            limit = { opinion = { target = liege value <= -25 } }
            set_global_variable = { name = rw_ai1_compare_stage value = flag:hostile_ready days = 1 }
            debug_log = "RW_AI1 compare_hostile_ready"
        }
        else = { debug_log = "RW_AI1 compare_hostility_failed" }
    }
}
else = { debug_log = "RW_AI1 compare_fixture_failed" }
'''
    result = REBIND + fixture
    stages = (
        ('reject', 'hostile_ready', 'reject_bad', 'reject_ok'),
        ('banned', 'reject_ok', 'banned_success', 'banned_failure'),
        ('allowed', 'banned_failure', 'allowed_success', 'allowed_failure'),
    )
    for mode, required, success, failure in stages:
        script = case(mode)
        for outcome, stage in (('success', success), ('failure', failure)):
            marker = 'debug_log = "RW_AI1 '+mode+'_'+outcome+'"'
            script = script.replace(marker, marker+'\n                    set_global_variable = { name = rw_ai1_compare_stage value = flag:'+stage+' days = 1 }', 1)
        result += '\nif = {\n    limit = { global_var:rw_ai1_compare_stage = flag:'+required+' }\n'+script+'\n}\n'
    result += '\ndebug_log = "RW_AI1 compare_end"\n'
    return result


def build(output):
    out = Path(output).resolve()
    if out.is_relative_to(ROOT) or out.exists():
        raise ValueError('Choose a new output folder outside the repository')
    files = payload()
    out.mkdir(parents=True, exist_ok=False)
    for name, raw in files.items():
        (out/name).write_bytes(raw)
    receipt = {'schema': 1, 'status': 'Original console-only diagnostic; NOT autonomous AI or engine-tested',
               'files': {name: hashlib.sha256(raw).hexdigest() for name, raw in files.items()}}
    (out/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        build(args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc)+'\n')
    print('Original console probes prepared; no game or installed mod changed.')
