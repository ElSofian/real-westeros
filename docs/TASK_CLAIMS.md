# Exclusive task claims

This protocol coordinates **independent ChatGPT scheduled/manual sessions and Codex Cloud sessions**. Reading GitHub or creating a working branch is **not** ownership of a task.

## Authoritative lock

The sole authoritative claim is the UTF-8 JSON file on **`main`** at:

```text
.github/task-claims/RW-008.json
```

Replace `RW-008` with the exact backlog task ID. The lock lives on `main`, **not** a feature branch. A unique owner ID identifies the individual execution, not merely "ChatGPT" or "Codex".

Example contents:

```json
{
  "schema": 1,
  "task": "RW-008",
  "owner": "chatgpt-scheduled-20261027T080000Z-unique",
  "branch": "feat/rw-008-political-incident",
  "claimed_at": "2026-10-27T08:00:00Z",
  "expires_at": "2026-10-27T12:00:00Z"
}
```

Use the actual UTC time and a unique suffix for each execution. **Do not invent an owner identity that might collide.** No credentials, game data or personal information go into a claim.

## Acquire (mandatory before work)

1. Fetch the current `main` backlog, open PRs and the target claim path. Pick one actionable, unclaimed task.
2. Use the GitHub Contents API to **create** the exact file on `main`, **without** supplying `sha`. In the ChatGPT GitHub connector, call `create_file` with `branch="main"`. In an authenticated Codex environment, use GitHub REST `PUT /repos/ElSofian/real-westeros/contents/.github/task-claims/RW-008.json` with `message`, base64 `content`, `branch="main"` and **no `sha`**.
3. A `201` success means acquisition. **A `409` or `422` is not success.** Fetch the file again: if another owner has it, stop work on that task. If a concurrent main update caused the failure but the file is still absent, retry the create after refetching `main`.
4. Fetch the file again and confirm your **exact owner** before beginning task-specific edits. Do not use label-only or issue-assignee-only "claims": they are not exclusive.
5. If the connector cannot create/read the claim, **do not develop the task in parallel**. Select unrelated, clearly independent work that can be safely claimed, or report the access problem.

**Verified:** On 2026-10-27, the GitHub connector successfully created a probe claim on an isolated branch. A second `create_file` on the identical path was rejected with HTTP 422 (missing old `sha`); the probe was then deleted. This confirms collision rejection for the tested API, **not** that arbitrary third-party agents automatically follow this protocol.

## During work

- Develop on a feature branch; the claim is on `main` and is excluded from gameplay PRs.
- Re-fetch the claim and check exact owner **before pushing updates, opening/merging a PR, and releasing**. If ownership changed or claim expired, stop before publishing and reacquire; never merge using an obsolete claim.
- If work exceeds the lease, renew it using GitHub `update_file` and the current blob `sha`, only after checking that `owner` still matches. Check the new claim after renewal. Conflicts mean **stop**, not force-update.
- A task may have multiple PRs sequentially, but it must not have multiple active owners.
- Reviewers also claim a task before merging a PR. Prefer finishing an existing PR before opening duplicate work.

## Release

After finishing or explicitly pausing, fetch the claim on `main`, confirm the owner, and delete it using `delete_file` with the **current blob SHA**. A different owner must never release another owner's lock. When the work is not complete, note its state and branch/PR in `docs/PROGRESS.md` before releasing. Deletion conflicts must be investigated, not blindly retried.

## Stale and abandoned claims

- A claim older than its `expires_at` is **stale**, not automatically free. Never delete or overwrite it merely because the clock elapsed.
- An agent may take over a stale claim **only after** inspecting the owner's branch/PR, latest commits, CI, and available run status to establish no active work. If active status is uncertain, do not take over; take another independent task.
- Recovery must be a compare-and-swap replacement using `update_file` with the *previous claim's* blob SHA on `main`. Confirm the new owner afterward. If update is rejected, someone else changed the claim: stop. Any resumed original owner must re-read and recognize lost ownership before publishing.
- GitHub has no knowledge of ChatGPT/Codex internal worker liveness. These checks reduce accidental overlap but cannot prevent an uncooperative external agent from ignoring the protocol.

## Practical implications

- A user may request "continue" manually while the scheduled automation is configured; **the lock decides which session owns RW-008**, not who was prompted first.
- Do not launch duplicate Codex Cloud work on the same task unless it can obtain this claim.
- The system prioritizes **no concurrent duplicate editing** over maximizing simultaneous sessions. If no safe claim is available, stop instead of wasting quota.
- This is a cooperation protocol enforced by an atomic GitHub file creation and ownership checks; it is **not a GitHub permission rule** or a guarantee against arbitrary agents that ignore instructions.
