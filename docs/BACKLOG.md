# Development backlog

A task is done only when the deliverable and verification evidence are present.

| Priority | ID | Task | State |
|---|---|---|---|
| P0 | RW-001 | Initialize public repository, instructions, design summary and gates | Done |
| P0 | RW-002 | Establish independent mod directory and descriptor with conservative version metadata | Done (scaffold; engine untested) |
| P0 | RW-003 | Build basic structural checks (file encodings, brace balance, duplicate definitions, localization keys as applicable); avoid false assurance | Done (12 local unit tests; static only) |
| P0 | RW-004 | Investigate G1 against local AGOT/CK3 sources and create smallest safe experimental war prototype | In progress — source map + negative fixtures; BLOCKED for gameplay spike (pinned source/engine absent) |
| P0 | RW-005 | Write reproducible engine test plan and logging for genuine CB / Mega Wars scenarios | Done (test plan only; engine execution pending) |
| P1 | RW-006 | Identify a viable multi-clause negotiation UI/model or document engine limits (G2) | Done (research + 16 synthetic protocol tests; G2 UI/engine unverified) |
| P1 | RW-007 | Create persistence model for pending political affairs and obligations | Todo |
| P1 | RW-008 | Implement one end-to-end political incident with status as static-only until CK3 tested | Todo |
| P1 | RW-009 | Add AI actor selection and negative-path tests for one end-to-end incident | Todo |
| P2 | RW-010 | Expand political memory, justice, diplomacy and other systems incrementally | Todo |

**Next task:** RW-007 persistence architecture and synthetic tests, **not** a claim of CK3 save/load functionality. RW-004 remains blocked at the pinned-source/native-CB boundary. G2 UI requires target-version source inspection and in-game validation; see docs/G2_FEASIBILITY.md. Do not start the full gameplay implementation before G1 feasibility is understood; isolated proofs are allowed without claiming engine success.
