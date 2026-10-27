# RW-010 — Personal consent to a conciliatory gesture

Status: original experimental CK3 scripts, static-checked; **not engine-tested**.
This extends the mediation/allegation slices, without native crime or scheme hooks.
It supersedes the automatic client opinion benefit described in the earlier slice
documents. The mediator's own +5 opinion remains a response to the requested gesture.

## Behavior

The provider can still make the invited gesture for 25 prestige, or decline.
Making it closes the mediator's case, costs the provider once, and improves the
mediator's opinion by 5 for two years. The client/claimant receives a separate
personal choice in the outcome event:

- accept: +5 client opinion of the provider for two years;
- refuse: no additional penalty, reward, refund or payment.

The response window is 30 days from the gesture. This is a new personal-response
window, not an extension of the original case deadline. The mediation must already
have reached its repair stage before its original deadline to allow a gesture.
No response, deadline expiry or loss of jurisdiction means **no recorded consent**.
There is no automatic acceptance and no recurring AI scan. Both AI and player use
the same guards and effects; AI acceptance weights respond to existing opinion.

The mediator's case result `repaired` now means a gesture was made, not that the
other party accepted. `rw_case_gesture` separately stores offered/accepted/rejected.
The party's response never changes statements, service receipts, guilt or legal
status. The original service is not performed or paid by this choice.

## State and access

A response requires the exact typed story, owner, client, mediator, kind, serial
and reason, a closed repaired case, a disclosed offered gesture, live response
window and current common-overlord jurisdiction. Only the client can decide.
Each decision removes the response window and records its answer before any
opinion effect. Old, stale or repeated callbacks cannot grant another benefit
under these source guards. These are not engine proofs of atomic execution.

Archive readers can open a read-only response view, using the existing role and
disclosure filter. Browsing cannot respond or renew the window. Missing gesture
metadata on earlier saves is not inferred as acceptance; it enables neither this
choice nor its new response view. Existing opinion effects from older versions
are not reversed or migrated. Retention stays five years, ends on provider death,
and remains subject to passive cleanup; no heirs inherit personal guilt.

## Checks and final engine cases

Adversarial static tests target wrong actor/identity, expired window, consumed
answer, effect-entry bypass, unsolicited client opinion, repeated rewards and
rewritten evidence. Reference/localization checks cover EN/FR and new event IDs.
Run the entire suite and structural validator; these do not execute CK3 scripts.
Final cases are appended to FINAL_ENGINE_TESTS.md.

## Native scheme evidence investigation

The two private source collections received so far cover war interactions,
triggers, laws, CBs and Mega Wars, not ordinary scheme definitions or discovery
actions. In the supplied AGOT source, references in
`common/casus_belli_types/00_agot_rv_revenge_wars.txt` include `secret_murder`,
`secret_target`, and `expose_secret`; they concern murder-secret handling in a
revenge CB. They do **not** establish a discovery callback, attempted regicide,
conspirator membership, who knows a scheme, or legal authority to punish.
`secret_identity_candidate` in Mega Wars is unrelated identity handling.
No proprietary source excerpt is reproduced here.

Consequently automatic assassination evidence remains source-blocked, independently
of the deferred engine tests. Before implementing it, inspect actual target-version
`common/schemes`, `common/on_action`, `common/secret_types`, and relevant scheme
events/effects/triggers, including AGOT overrides and additive on-action behavior.
Record callback scopes, discovery vs exposure, owner vs agents, living target,
observer knowledge and replay identity. Never treat a murder secret as proof of a
currently discovered plot against the ruler, or an ordinary accusation as a crime.
This does not block other independent service/incident development.
