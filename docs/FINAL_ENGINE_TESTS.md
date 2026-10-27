# Final CK3 validation campaign

Owner decision: defer engine tests until the integrated candidate is ready. None of
these scenarios has run. Static passes are not game behavior or compatibility proof.
Record CK3 executable, AGOT version, DLC, playset order and commit for every run.

- Reconciliation: use RW008_INCIDENT.md and RW009_AI.md for acceptance/refusal,
  expiry, death, loss of title, war, AI target selection and cooldown cases.
- Reconciliation audit: reopen an old event after a new petition to the same target;
  neither acceptance nor dismissal may consume/affect the new revision. Save/reload
  both revisions and inspect saved recipient/value scope resolution. Run two eligible
  interactions in the same tick to assess execution revalidation.
- G1: use G1_PROBE.md and TEST_PLAN_G1.md at the war-feature stage; it remains todo,
  not a prerequisite for independent negotiation work or an engine success claim.

Keep baseline AGOT saves separate and disposable. Report failures by scenario and
log excerpt rather than treating static or zero-test results as engine validation.
