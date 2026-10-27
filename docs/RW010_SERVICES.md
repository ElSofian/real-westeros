# RW-010 — first negotiated service

**Original CK3-facing scripts, experimental and not engine-tested.** The original action is an
immediate exchange; the separate deferred action is described in RW010_DEFERRED.md.
Neither integrates the RW-007 Python ledger.
All CK3 runs are deferred to the final campaign at the owner's request.

## Endorsement for gold

A landed adult at peace offers to speak publicly in support of another landed adult.
The provider asks for 50 gold; the client can accept, decline, or propose 25. The
provider can accept 25, decline, or maintain 50. Requotes can repeat until the original
30-day deadline; they never extend it. A client with only 25 gold can counter but
cannot accept 50. No payment occurs during proposal/counteroffer/refusal.

Acceptance rechecks identities, eligibility, turn and current affordability. It
consumes pending identity before transferring the agreed gold from client to provider
and granting the client 50 prestige for the immediately delivered endorsement.
No automatic alliance, favor/hook, war assistance, claim, title or future obligation
is implied. These fixed prices/prestige are provisional balance values. The feature
is deliberately small so later services can own different real effects.

Both human and AI parties use the same events, gates, price choices and settlement.
The initial AI initiation policy only considers the direct liege, while humans can
choose other valid recipients. It uses base willingness 5 and response weights;
these are not measured behavioral rates. One outstanding offer per provider and a
one-year offer cooldown prevent concurrent state collisions and bound spam in this
slice, not the eventual number of useful services or clauses.

## State and boundaries

Provider stores a monotonic `rw_service_serial`, quote revision, client, price and
turn. Each event captures provider/client plus serial/revision/price values. Responses
must match all of them. New contracts increment serial; counters increment revision.
Cleanup never resets identity counters and cannot consume a newer offer. Expired or
invalid offers can be dismissed without payment, prestige or refusal punishment.
If no dismissal occurs, pending expires and old inert fields are overwritten only
when a new eligible offer begins. This is not a general historical ledger.

Replay protection, saved scalar scopes, gold-value arithmetic, same-tick ordering,
AI scheduling, popup behavior and save/reload remain engine assumptions to test.
Consume-before-effects does not establish transactional crash consistency. No retry
or compensation mechanism should be inferred. No core AGOT or vanilla hooks replaced.

## Static validation

Run `python3 -m unittest discover -s tests -v` and `python3 tools/validate_mod.py`.
Source-contract mutations detect removed identity/affordability checks and extended
quote deadlines. EN/FR display keys and localization BOMs are checked. No engine
state machine or gameplay simulation runs in Python.

## Final engine cases (unrun)

1. Use two landed adults at peace and record gold/prestige. Offer, accept 50: client
   loses 50 gold and gains 50 prestige; provider gains 50 exactly once.
2. Counter 25 and accept: same result at price 25. Requote 50, counter again and
   decline: zero transfers/prestige; original expiry not extended.
3. Client starts with 25–49 gold: direct acceptance unavailable but counter allowed.
   Spend client gold before responding: settlement must fail without any transfer.
4. Replay an earlier quote after countering and an old offer after starting a new
   contract: neither response nor dismissal may change current state or settle.
5. Test death, minority, loss of land, war, deadline, no gold, self-targeting, pending
   collision and cooldown. Never grant effects when an option becomes invalid.
6. Save/reload at every turn, then settle once. Inspect source/value scopes and logs.
   Check same-tick repeated interaction attempts. Test both human/AI party directions.
7. Run an AGOT baseline comparison and representative balance/performance observation.

## RW-010 stages

- Deferred service promises: experimental source now added, see RW010_DEFERRED.md; engine tests pending.
- Discretionary responses to known political incidents, not compulsory punishment.
- Dynastic sanctions/restoration gated by G3 and actual title/house APIs.
- Unlawful wars and political responses at the war stage, resolving G1 before claiming
  that path works. Do not silently substitute a generic CB.

This first service is a vertical slice of the owner's third scenario, not completion
of negotiations, justice, political memory or the full project.
