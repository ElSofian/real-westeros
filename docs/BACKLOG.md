# Development backlog

A task is done only when the deliverable and verification evidence are present.

| Priority | ID | Task | State |
|---|---|---|---|
| P0 | RW-001 | Initialize public repository, instructions, design summary and gates | Done |
| P0 | RW-002 | Establish independent mod directory and descriptor with conservative version metadata | Done (scaffold; engine untested) |
| P0 | RW-003 | Build basic structural checks (file encodings, brace balance, duplicate definitions, localization keys as applicable); avoid false assurance | Done (12 local unit tests; static only) |
| P0 | RW-004 | Investigate G1 against local AGOT/CK3 sources and create smallest safe experimental war prototype | On hold by owner — research retained; no engine experiment requested; may resume later |
| P0 | RW-005 | Write reproducible engine test plan and logging for genuine CB / Mega Wars scenarios | Done (test plan only; engine execution pending) |
| P1 | RW-006 | Identify a viable multi-clause negotiation UI/model or document engine limits (G2) | Done (research + 18 synthetic protocol tests; G2 UI/engine unverified) |
| P1 | RW-007 | Create persistence model for pending political affairs and obligations | Done (offline snapshot + 16 synthetic tests; CK3 save/load unverified) |
| P1 | RW-008 | Implement one end-to-end political incident with status as static-only until CK3 tested | Implemented experimentally — CK3 scripts; engine untested |
| P1 | RW-009 | Add AI actor selection and negative-path tests for one end-to-end incident | Implemented experimentally — bounded liege targeting; engine untested |
| P2 | RW-010 | Expand political memory, justice, diplomacy and other systems incrementally | Todo |

**Next task:** clarify the owner's original political-war scenarios, then resume the reconciliation audit and integration checks. RW-004 / G1 is on hold by explicit owner decision and does not block independent development. Do not substitute broken promises/agreements as the definition of illegal war without confirming the intended examples. Retain the existing G1 findings and private diagnostic tooling for possible later resumption; no engine feasibility verdict has been reached. G2 UI/engine remains unverified; see docs/G2_FEASIBILITY.md.
