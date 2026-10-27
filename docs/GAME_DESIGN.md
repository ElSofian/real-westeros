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

## Scope and status
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
