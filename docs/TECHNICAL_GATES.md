# Technical feasibility gates

**Current owner direction: G1 is ON HOLD and may be resumed later. It does not block independent development. No G1 engine test is currently requested.**

**Status: none engine-tested.** AGOT script extracts were audited from an AGOT 0.5.2.1 installation descriptor reporting CK3 support for 1.19.0.6. The actual CK3 executable version and installed DLC set were not verified.

| Gate | Need to demonstrate | Failure risk |
|---|---|---|
| G1 — Illegal war / authentic CB | War initiated in spite of political ban; genuine CB retained; correct war start/end, Mega Wars, inheritance and cleanup | A fake CB, bypassed AGOT hooks or corrupted war state |
| G2 — Negotiations | Two or more clauses, safe acceptance/versioning, conditional performance, counteroffer and reloading | Partial or duplicate transfers; impossible UI |
| G3 — Dynastic aftermath | Explicit sanctions and correctly scoped persistence; test grant, inheritance, election and conquest separately | Claims of universal title bans that actually fail |
| G4 — Political AI | AI↔AI action while at peace, appropriate negotiation or refusal, no exploit loops; performance baseline | Spam, unfair exceptions, severe slowdown |
| G5 — Compatibility | Existing AGOT war, Mega Wars, title revocation, debt inheritance, lineage and regional institutions keep working | Double effects or missing native hooks |

## G1 reference points (inspect actual local sources)
- `AGOT/common/character_interactions/00_war.txt` — `declare_war_interaction`, `can_attack_in_hierarchy`, `has_any_display_cb_on`.
- `AGOT/common/scripted_triggers/00_war_and_peace_triggers.txt` — war-preventing realm law and contract exceptions, historically around lines 223–245.
- `AGOT/common/scripted_triggers/00_agot_mega_wars_triggers.txt` — Mega Wars classification.
- `AGOT/common/on_action/agot_on_actions/agot_war_on_actions.txt` — war-start action.
- `AGOT/common/story_cycles/agot_story_cycle_mega_wars.txt` — lifecycle handling.

The above paths are **source inspection references**. No CK3 engine feasibility has been demonstrated by their existence.

## Validation rules
- Record static inspection versus game evidence separately.
- A spike may be committed as explicitly experimental only when it does not overwrite installed game assets.
- A playable feature is *not* accepted as complete without reproducible CK3 engine evidence.
- Owner plans end-of-project global manual tests; automated static checks must run during development. Flag the risk of deferring engine tests so blocked features do not become invisible.
