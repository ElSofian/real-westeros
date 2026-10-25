# Working with Codex Cloud and GitHub

1. Connect `ElSofian/real-westeros` in Codex Cloud using the GitHub connection (ChatGPT GitHub connection may be separate).
2. Use `AGENTS.md` as the permanent guidance. Create an isolated branch for each bounded issue and open a PR with a short summary.
3. Run static tests; clearly label untested engine behavior. Never use the public repo to distribute installed AGOT/CK3 assets.
4. Record progress, blockers, next task and relevant checks in `docs/PROGRESS.md`.
5. Have Codex continue through the ordered backlog **within the task session limits available**. Any scheduled restart or background continuation is a distinct feature that must be configured and confirmed — a GitHub connection by itself does not create it.
6. Do not claim success for engine-dependent behavior without CK3. But missing CK3/AGOT is **not** a blocker to scaffolding, documentation, static validation, and independently verifiable changes. If GitHub PR creation is unavailable in a specific session, commit and use whatever Git/GitHub publishing capability is available; otherwise report the exact blocker without discarding completed local work.
7. No paid APIs or servers. ChatGPT Plus does not automatically include Agents API consumption.
8. Keep reports to the owner concise; normal engineering choices are delegated.

**Note:** The owner currently expects broad in-game testing at the end; this introduces risk. Static validation cannot prove mod compatibility, so mark critical gameplay features as provisional until those tests.
