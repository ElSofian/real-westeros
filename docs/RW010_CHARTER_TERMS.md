# Negotiated duration clauses for public restitution charters

**Original CK3 scripts; static-checked, not engine-tested.** The original crown
charter starts as a five-year proposal. Its original house head can now counter
**one year**; the issuing sovereign can accept that shorter undertaking or maintain
five years for the head to accept again. Only the other party's explicit agreement
to the exact current duration can accept. This negotiates a political undertaking's
period, not a guaranteed title transfer or an enforceable native legal deadline.

## Exact current proposal, original clock

New proposals store a separate duration schema, term (`year1`/`year5`) and responder
turn. Each counter increments the existing charter revision, updates term/turn,
captures the new term and sends one day-later counterpart opportunity. The existing
entry/crown/house/title and original issuer/head identities are unchanged. Current
roles, same original representatives, offered phase and original seven-day marker
are required at every accept/counter. A successor cannot accept pending consent.

A head cannot accept their own one-year counter; a ruler cannot accept their own
five-year proposal. Old panels fail charter revision and captured-term checks,
even when later counters return to the same duration. Neither counter renews the
original proposal window, starts an accepted deadline, charges gold, creates a
native right or changes the archive's retention. Repeated counters can only operate
within the original seven-day window; silence/expiry is not acceptance or guilt.

Explicit counterpart acceptance consumes offer/turn and increments the charter
revision before notices. It sets the agreed due marker **once**: 365 days for one
year, otherwise 1825 days for five years. Unknown schema/terms/turns fail closed.
The original freely chosen repudiation, house release, ownership-based satisfaction
and neutral expiry stay separate from native title decisions. No success reward,
crime, forced grant, automatic forfeiture or new war/house-ban rule is introduced.

After acceptance the term cannot be countered through this dialogue. Sovereign
recognition, representative changes, archival reading and later financial proposals
never reset or shorten an existing deadline. Public compensation remains a distinct
negotiation: its full parent-charter identity/revision and active due marker guard
any payment, including a charter accepted for one year. Gold/case/private-pledge
fields and native banking remain untouched by duration counters.

## Earlier fixed-five-year records

The old implementation only offered five years. A fresh read-only charter snapshot
therefore defaults to `year5` **only when all new protocol fields are absent**.
A partially initialized/new/unknown schema is not guessed into legacy consent.
Old saved panels without a captured term are inert until a fresh permitted review.
That fresh review never writes duration metadata, changes an accepted due marker,
pays money or replays consent. No old-save compatibility or migration is established.

An old still-unaccepted offer may be explicitly countered after a fresh eligible
review; only then does the counter write new duration metadata and require the
other original representative's new agreement. Old active/closed records remain
five-year history and their actual stored deadline is never reconstructed. Existing
character-identity (not per-reign) role guards and fixed registry retention still
apply, including loss of access if the registry expires before the undertaking.

## UI, AI and verification

Public charter panels display the exact current duration. Acceptance text refers
to those latest terms; active/history text no longer universally claims five years.
AI and player use the same term/turn/version/role guards and no counter costs.
Existing reply events provide bounded opportunities; impatient/patient weights are
provisional and not observed behavior. No new native callback, global scan, reminder
chain, story or index is added. No gameplay Python, runtime LLM or paid service.

Fifteen adversarial source tests cover explicit schema/term identity, legacy-only
default, original current roles, correct other-party consent, version/turn capture
before notice, immutable clocks, mutually exclusive 365/1825-day acceptance,
no active amendment, retained free exits, financial-parent integration, native-state
isolation, AI symmetry and EN/FR. The older charter source checker now expects the
two mutually exclusive deadline branches; extra writes still fail its renewal test.
These checks do not simulate CK3. CTERM-01…12 in FINAL_ENGINE_TESTS.md remain unrun;
root/scope/scalar capture, dates, save/load, actual negotiation/AI/economy/performance
and AGOT compatibility require the final campaign. No new source collection,
proprietary asset or intermediate game run is requested. G1 and universal G3 stay
unresolved. Next wider institutional clauses and contextual political consequences.
