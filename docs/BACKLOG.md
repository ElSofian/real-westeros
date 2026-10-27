# Development backlog

A task is done only when the deliverable and verification evidence are present.

| Priority | ID | Task | State |
|---|---|---|---|
| P0 | RW-001 | Initialize public repository, instructions, design summary and gates | Done |
| P0 | RW-002 | Establish independent mod directory and descriptor with conservative version metadata | Done (scaffold; engine untested) |
| P0 | RW-003 | Build basic structural checks (file encodings, brace balance, duplicate definitions, localization keys as applicable); avoid false assurance | Done (12 local unit tests; static only) |
| P0 | RW-004 | Investigate G1 against local AGOT/CK3 sources and create smallest safe experimental war prototype | Todo — planned for the war feature stage; research/probe retained; engine feasibility unverified |
| P0 | RW-005 | Write reproducible engine test plan and logging for genuine CB / Mega Wars scenarios | Done (test plan only; engine execution pending) |
| P1 | RW-006 | Identify a viable multi-clause negotiation UI/model or document engine limits (G2) | Done (research + 18 synthetic protocol tests; G2 UI/engine unverified) |
| P1 | RW-007 | Create persistence model for pending political affairs and obligations | Done (offline snapshot + 16 synthetic tests; CK3 save/load unverified) |
| P1 | RW-008 | Implement one end-to-end political incident with status as static-only until CK3 tested | Implemented experimentally — CK3 scripts; engine untested |
| P1 | RW-009 | Add AI actor selection and negative-path tests for one end-to-end incident | Implemented experimentally — bounded liege targeting; engine untested |
| P2 | RW-010 | Expand political memory, justice, diplomacy and other systems incrementally | In progress — first immediate negotiated service; later stages in RW010_SERVICES.md |

**Next task:** deferred service promises and fulfillment/breach under RW-010, following the static reconciliation audit and immediate-service slice. All CK3 runtime tests are deferred to the final campaign per owner; see docs/FINAL_ENGINE_TESTS.md. G1 / RW-004 is restored to the development plan, not on hold and not an immediate G1-first assignment. Resume its source/probe/engine work when preparing the unlawful-war feature; resolve it before shipping that feature, without blocking independent negotiation/incident work. Existing P0 reflects its importance within that war track, not a command to preempt current work. The original goal is deliberately declaring a valid-CB war despite the king's ban, followed by discretionary political responses; see docs/GAME_DESIGN.md. G2 UI/engine remains unverified; see docs/G2_FEASIBILITY.md.

RW-010 stages: immediate endorsement-for-gold negotiation (experimental scripts); deferred promises (todo); discretionary political responses (todo); dynastic aftermath/restoration (todo, G3); unlawful war stage (todo, G1). See docs/RW010_SERVICES.md for scope and final engine cases.
