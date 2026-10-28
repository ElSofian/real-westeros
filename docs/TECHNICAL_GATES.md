# Technical feasibility gates

**Current owner direction: G1 is restored to todo for the war-feature stage, not the immediate priority. Resolve it before shipping unlawful-war gameplay; independent development can continue.**

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

## G3 source investigation and final-campaign diagnostic

G3_HOUSE_SANCTIONS.md separates four acquisition routes, personal disinheritance,
house persistence and institutional restoration. Native post-transfer callbacks are
not a demonstrated pre-transfer veto. Existing source subsets do not establish a
universal 50-year house landholding ban; no impossibility claim is made. Original
optional standalone diagnostic interactions mark one chosen current house for seven days, and additive
callback children log restricted observations only. The base mod loads none of these diagnostic callbacks. They neither enforce a sanction
nor clear G3. The targeted TitleRoutes ZIP is now verified; TITLE_ROUTE_AUDIT.md
locates grant alternatives, actual election lists and separate AGOT succession
without establishing universal enforcement. All G3-01…12 runtime cases remain
deferred; no intermediate run requested.
