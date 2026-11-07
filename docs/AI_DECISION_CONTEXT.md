# Context and personality in political decisions

## Current client-response extension

AI_CLIENT_BREACH_RESPONSES.md weights seven original-client choices with native
vengeance/compassion/honor, own opinion and recorded capacity at breach. Legacy
unknown capacity stays neutral. Later wealth or a newer service receipt does not
reconstruct history. Repair acceptance uses its independent concluded case.
The private reader provides a separate per-trait client review. Source-only,
AI3/O1 quality,74/80+0/20, delta0. Complete contextual implementation remains open.

## Current timing extension

AI_PROMISE_TIMING.md extends the initial profile below to native energy and
actual promise horizons. Gold wait and favor leave now have provider-context
weights. Execution gains moderate promptness and urgency factors. Current
contract serials bind two temporary timing indicators, while legacy missing
metadata remains timing-neutral. Seven source regressions and inverse effect
checks cover the extension. Engine validation remains deferred. Source74/80,
campaign0/20, delta0. The first-profile section retains its original scope.

AI_DECIDER_AUDIT.md records the owner-requested per-trait inventory and separates
zero direct honor/greed input from a justified zero contextual effect. Complete
contextual review remains pending for all enumerated traits.

AI_PERSONALITY_PROMISE_REVIEW.md follows all39 non-dragon personality traits
through the six current provider choices, payment branches and indirect
opinion/resource inputs. The private reader reports conservative per-option
axis directions without final weights or probabilities. Contextual gameplay
implementation remains incomplete.

The owner requires contextual reasoning across every Real Westeros action family.
The audit covers the decision maker, other participating characters, the action's
purpose and the consequences the decision maker can anticipate. This is an ongoing
decision-by-decision rollout. The first new shared profile covers four promise
choices. Its source is static-checked. Its runtime behavior awaits the final
campaign.

## Review dimensions

| Dimension | Inputs to review for the particular action |
|---|---|
| Decision maker | Combined traits and native personality axes, skills/education, health, stress, age and current role |
| Means | Actual available money/prestige/piety, current obligations, military resources and credible allied support |
| Interests | Personal and dynastic benefit, claimant/beneficiary interests, domain/house position and competing goals |
| Relationships | Own opinion, trust, fear, rivalry, marriage/kinship, alliances and known political memory |
| Norms and authority | Applicable laws, native rights/exceptions, faith/culture, legitimate authority, known offense and existing commitments |
| Situation | Timing, deadlines, war/activity/captivity, urgency and available alternatives |
| Consequences | Immediate effects, later exposure, response by the authority, gain/loss, diplomatic fallout and dependents affected |
| Knowledge | Facts available to this actor, public information and evidence the actor is entitled to inspect |

Each profile records the meaning of its factors for its goal. Receiving payment
can encourage paid performance. Giving away money has a different incentive.
Honor can favor keeping an accepted promise, while a political oath can conflict
with other duties and perceived legitimacy. Faith-related motivation depends on
the religious stakes of the action. Personal prowess and the ability to command
or recruit an army represent different capabilities.

For an action concerning a spouse's claim, review both characters' interests and
their relationship. The initiator's personality governs initiation. The claimant's
personality informs their own choices, known willingness and anticipated support.
Consent follows the actual action's native or authored rules. Existing information
access rules apply to private promises, evidence and intentions.

## Current entry families and remaining review

| Family | Existing anchors | Remaining context review |
|---|---|---|
| War and defiance | Native planner/CB scoring, shared native-window option, simple initial reserve/hostility preference | Political risk of disobedience, severity/capacity of the authority, claimant support, combined personality and effective option weighting |
| Political affairs | Case/ultimatum choices, shared cooperation factors, current parties and costs | Stakes, conflicting duties, proportional response and contextual alternatives across each option |
| Negotiation | Versioned quote/terms, own opinion/memory, resources, bounded targeting | Expected value, reliability, relationship changes and personality across offer, counteroffer, refusal and consent |
| Promises | Current identity/due/means guards, new personality profiles for gold and favor performance/renunciation | Other obligation families, urgency, competing duties, delay and negotiated release/amendment |
| Justice and houses | Known reasons, native action validity, current authority, selected sanctions and some trait weights | Proportionality, lawful/arbitrary motivation, power/support, family consequences and rehabilitation choices |
| Evidence and rumors | Provenance, knowledge/access guards, accusation and admission kept distinct | Credibility, uncertainty, actor motives and disclosure incentives in each choice |
| Political memory | Retained personal memories, public service multiplier and house/institution continuity | Which remembered facts should influence each goal, strength/duration and successor perspective |
| Cross-system AI | Native entry points, owned event choices and common contextual values | Trace each relevant input to its effective decision weight and verify counterfactual behavior/performance |

The initial send-option preference and the option ultimately selected are separate
observation points. Source review tracks both. A successful AI action establishes
access and execution. A personality policy also needs controlled comparisons of
weights and decisions when relevant inputs change. The existing frozen readiness
rubric retains its original meaning and history. This refinement adds0points.

## First profile implemented

rw_promise_ai_values.txt supplies four current-provider weights. Existing event
options retain their action triggers, effects and timers. Complete saved-frame
checks precede each family's current identity/eligibility checks. Stale, missing
or foreign frames yield zero willingness.

| Choice | Existing base weight | Current inputs |
|---|---|---|
| Gold promise performance | 70 | Own honor/greed, current quoted payment, own funds, own opinion of client and actual fulfillability |
| Gold promise breach | 10 | Own honor, own opinion of client and current actionable commitment |
| Favor-family performance | 70 | Own honor, own opinion of client, current term/eligibility, greed and own funds for the monetary25 term |
| Favor-family renunciation | 5 | Current pending commitment, own honor/opinion when the client is alive |

The shared honor factor is `clamp(1 + ai_honor/100, 0.25, 2)` for performance.
The breach/renunciation factor is `clamp(1 - ai_honor/100, 0.25, 2)`. The monetary
reward factor is `clamp(1 + ai_greed/200, 0.5, 1.5)`. Native traits and modifiers
combine into those axes before the profile reads them. Every personality factor
remains positive within the eligible action context.

Performance weights multiply by1.25 for own opinion of the client at least25 and
by0.75 for opinion at most−25. Breach/renunciation uses the opposite relationship
factors. A provider whose funds are below the incoming quoted payment gets a1.25
income-importance multiplier. That cash motivation applies to the current monetary
term. For a deceased favor client, renunciation retains its neutral base.

The favor snapshot correction precedes this policy so term/mode flags retain their
types. Legacy mode-less offers keep their immediate interpretation. Client
withdrawal represents a separate decision and retains its existing policy in
this first profile.

## Primary source checks

Installed CK3 1.19.0.6 and AGOT 0.5.2.1 were inspected directly. Metadata below
identifies the reviewed primary sources. Proprietary definitions remain local.

| Relative reference | SHA256 |
|---|---|
| AGOT/common/traits/00_traits.txt | `3764f1db75d4939639f84e727cea46c09fa586cb59ed82caadf1cd6336237806` |
| CK3/common/script_values/_script_values.info | `764ad711339c61bf239851bd52d87168dc1a2c91fe0c385c308ec4b85e2b5ef1` |
| CK3/common/script_values/00_lifestyle_values.txt | `9777e31bb8f2629fc02d9646049c1a452267e33592263ef409e7d0d6882011e0` |
| Engine-generated triggers.log | `e9414145681561c9a7c734203fc20cc7f5c3aa88af29afedfbaca272f7814318` |

These sources establish native personality-axis getters, trait contributions,
ordered script-value arithmetic and clamp syntax. Static regressions check
provider identity, complete frames, current costs/terms, decider-to-counterpart
opinion, opposite honor direction and positive bounds. Event-action hashes after
removing AI weights match the existing action graph at5617c9.

## Final campaign cases

1. Keep the same valid promise and vary the provider's aggregate honor. Check
   performance/breach weight direction and supported value evaluation.
2. Vary aggregate greed and provider funds for the current quoted payment. Compare
   monetary and native-favor terms, with the ordinary client-funds/hook guards.
3. Change provider-to-client opinion independently of client-to-provider opinion.
   Swap the player/AI roles and verify the original provider remains the decider.
4. Reopen a stale revision, foreign-party frame or expired promise. Check existing
   cleanup and current availability before any actual transfer.
5. Compare living/deceased favor-client context and explicit renunciation. Verify
   the established outcomes, deadline handling and saved state.
6. Measure decision frequency and evaluation cost with the existing G4/G5 sampler.
   Broader personality/context coverage remains tracked by the matrix above.
