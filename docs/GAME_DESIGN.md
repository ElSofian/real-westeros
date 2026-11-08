# Consolidated game design (v0.2 summary)

## Vision
**Liberté, conséquences, immersion.** Westeros should be politically interesting even when the player does not conquer territory. Negotiation, defiance, service, broken promises, reconciliation, institutional power and dynastic fallout can emerge between AI and player rulers without any LLM. No arbitrary cap on the number of useful player interactions.

## Eight systems and responsibilities
1. **Freedom / legality:** distinguish politically forbidden behavior from mechanically impossible actions. Judge legality under law applicable when an act occurred.
2. **Political affairs:** contextual responses, disputes, threats, tolerance, mediation and escalation; no forced lawsuit or automatic punishment.
3. **Negotiation:** versioned offers with multi-clause commitments, counteroffers and explicit acceptance; never assume complex engine operations are atomic.
4. **Promises / obligations:** deferred, conditional, continuous, personal, territorial, patrimonial and dynastic commitments; a promise does not force a future performance.
5. **Justice / sanctions:** distinguish political wrongdoing from legally recognized offenses, arbitrary power from lawful acts, and independent remedies from duplicate native penalties.
6. **Information / evidence:** objective fact, known secret, rumor, accusation and contested proof are different; false allegations must not alter native bloodline or claims.
7. **Political memory:** retain relevant political and dynastic consequences using existing CK3/AGOT memories, house relations, and title legitimacy when possible. An heir may inherit political fallout without inherited personal guilt.
8. **Political AI:** select actions using motivations, risks, means, obligations, culture and what the character knows. Same execution rules as the player, bounded target searches, reactive opportunities and anti-spam.

## Non-negotiable cross-system rules
- Native CK3/AGOT owns wars, CBs, titles, imprisonments, banks, secrets and native relationships. New subsystems own only new state.
- Record one authoritative fact; allow multiple different consequences, never execute the same native effect twice.
- An illicit vassal war must retain its real CB if supported; never pretend a fake CB is equivalent.
- A concluded promise can be fulfilled, negotiated, broken, contested or expire; do not automatically reward a title on a victory.
- Preserve Mega War resolution and cleanup, revocation resistance, existing banking inheritance and institutional authorities.
- No universal reputation meter and no exhaustive per-character log of every trivial act.
- Prefer relevant event-driven AI opportunities to periodic scans of all pairs of characters.
- Existing features of AGOT should be reused, not reconstructed.

## Decision context across all systems

The owner requires every implemented political decision to consider the relevant
known context. Review personality and combined traits, skills and education,
health/stress, resources, obligations, relationships, family and beneficiary
interests, faith/culture, law and authority, timing, expected support and probable
consequences. Each action defines how those dimensions influence its own goal.

The initiator and beneficiary retain distinct agency. A beneficiary's personality
informs their participation and the support the initiator can reasonably expect.
The initiator's choice uses their own personality and interests. Knowledge and
evidence-access rules govern information used about other characters.

AI_DECISION_CONTEXT.md records implemented coverage and the remaining review by
family. Native aggregate personality axes provide combined inputs for original
action profiles. Eligibility, decision preference and execution consequences are
reviewed separately, including the point where the engine consumes a preference.

## Scope and status

The original three scenarios are non-exhaustive examples within the eight-system
vision. Completing those examples would not complete Real Westeros. Overall progress
must not be inferred from PR counts, static test counts or completed backlog rows;
the weighted first-v0.1 readiness rubric is now defined in [V01_ROADMAP.md](V01_ROADMAP.md).
It covers all eight systems with 80 source points and 20 final engine-validation points;
it is not a measured percentage of the open-ended ultimate vision or of engineering effort.

An earlier 126-entry **candidate** action catalogue informed the eight-system design; the entries are not 126 mandatory buttons or proven implementations. All design principles are decisions delegated by the owner; all engine-dependent feasibility claims remain open.

## Primary project artifacts
The detailed GDDs v0.1, review, and v0.2 source specification were created before this repository. They should be imported selectively as **original documentation**, not confused with CK3/AGOT scripts. When importing them, retain their uncertainty labels and avoid reproducing third-party game source code.

## Owner-confirmed original scenarios

These are design goals, not a list of implemented or engine-verified features.

1. **Defy a royal war ban.** A duke in the Reach fabricates a claim on a neighbor
   and declares despite the king's ban on vassal wars, using the genuine CB. The
   king may demand peace, confiscate the duchy while leaving a county, grant the
   duchy to the attacked lord (making that lord the aggressor's new liege), or do
   nothing based on interests, means and circumstances. None is an automatic result.
   This is G1, restored to planned development for the war-feature stage.
2. **Discovered assassination plot and dynastic aftermath.** The king may choose
   among sanctions against the conspirator, family or house: execution, confiscation,
   loss of noble status or a 50-year bar on landholding. Descendants may later restore
   their house/status. These possibilities require engine and policy investigation;
   do not assume universal landholding bans work or heirs inherit personal guilt.
3. **Negotiate services for compensation.** Structured buttons/options allow parties
   to offer a service, negotiate consideration and make promises, obligations or
   betrayals with consequences. No runtime LLM or free-form dialogue is required.

Do not replace scenario 1 with agreement-breaking alone. Preserve discretionary
responses and equal execution rules for player and AI across all three scenarios.

## Owner-directed post-foundation review

After reaching the80/80 foundation milestone, revisit the substantive rules of
all eight systems against the intended design. The owner permits this review
alongside the grouped engine campaign. Establish what each current baseline
supports, observe the complete implemented variant where available, identify
missing context and improve iteratively from the results. Track simplified
feasibility paths and their remaining gaps explicitly. The finite readiness
rubric retains its existing acceptance text and checkpoint history.

## Territorial war authority review

The owner retains direct territorial authority at each hierarchy level and defers
a royal general-peace proclamation. Distinguish the declaring actor's applicable
war restriction from another ruler's competence or willingness to intervene.
Native internal-war and all-war bans retain their native exception logic.
G1_TERRITORIAL_LAW.md records the current table and incremental source coverage.
The Leyton/Dayne scenario needs proven native actor/defender/title binding before
Mace/Doran response routing and requests to a common superior are implemented.

G1_DECLARATION_PARTIES.md records the first role-capture extension. Keep native
primary attacker/defender, supplied claimant and each target title's holder and
direct authority distinct. Missing identities stay explicit. Link original
interaction initiators through demonstrated native context before enabling new
external-defiance responses. Capture facts once and retain partial-source limits.

G1_DECLARATION_ACCEPTANCE.md records the experimental native acceptance link.
Bind supplied interaction identities only to an exact unique fresh war receipt;
keep selected flags distinct from demonstrated native costs and legal verdicts.
Ambiguous/changed contexts retain an unbound record.

G1_EXTERNAL_DEFIANCE.md records the experimental external action extension.
The declaring actor's direct all-war ban can expose the native defiance option
against another branch or independent target. Internal bans remain same-liege,
with native exceptions and other conditions preserved. Existing political
responses explicitly remain peer-scoped pending distinct Mace/Doran routing.

G1_EXTERNAL_RESPONSES.md records the first separate external reaction route.
Fresh accepted defiance facts permit independent declaring-liege and actual
target-holder-liege ignore/disapprove choices. Distinct personal opinion effects
carry no new native crime or peace outcome. Demands, mediation, higher assistance
and broader contextual AI remain further development. New routing is experimental
and requires grouped engine validation.

G1_EXTERNAL_DEMANDS.md extends each personal external case with one political
demand and the original attacker's acknowledgement or refusal. Keep reception,
agreement, promise and actual native peace distinct. Opinion for refusal depends
on the original authority role, with no inferred refusal from silence. Negotiated
response terms, native peace linkage and broader AI context remain further work.

G1_EXTERNAL_NATIVE_PEACE.md records the experimental link from the original
declaring liege to the native stop-vassal-war negotiation. Current native validity
and exact-target transport remain mandatory. The protective authority retains its
distinct political capacity. Native terms, costs and outcomes remain owned by
CK3/AGOT, with grouped engine proof required. Protector mediation, additional
authority capacities and broader contextual AI remain further development.

G1_EXTERNAL_MEDIATION.md adds the protector's discretionary request to the
captured declaring liege. Explicit personal consent precedes a separate native
ticket and preserves the earlier political decision. Revalidate both authorities
and the protective context, retain historical law facts, and guard concurrent
attempts on the same war. Superior assistance and broader contextual motivations
remain separate development. New mediation behavior is not engine-tested.

AI_EXTERNAL_WAR_RESPONSES.md refines ten existing external response/mediation
preferences using the current decider's personality and known role-specific
context. Preserve action/eligibility parity and distinguish a political reply
from actual peace. Source-only weight changes leave the event action graphs and
gameplay effects intact. Peer/declaration policy and broader contextual coverage
remain further review, with grouped engine comparisons required.

AI_DECLARATION_DEFIANCE.md refines the native AI checkbox's initial political
preference with a deterministic known-context comparison. Keep boolean
initialization distinct from candidate discovery, CB selection and native send.
Do not infer a claimant, beneficiary or title stake from unavailable candidate
identity. Preserve player/AI action parity, native exceptions and authentic CBs.
New score evaluation requires grouped engine proof.

AI_PEER_WAR_RESPONSES.md applies guarded contextual preferences to six peer
choices. Share only current-decider factors with the external profile and retain
separate party/record/war frames. Preserve the existing event action graph and
execution guards. Native declaration preference and broader contextual coverage
remain further review, with grouped engine comparisons required.
