# Working with Codex Cloud and GitHub

1. Connect `ElSofian/real-westeros` in Codex Cloud using the GitHub connection (ChatGPT GitHub connection may be separate).
2. Use `AGENTS.md` as the permanent guidance. Create an isolated branch for each bounded issue and open a PR with a short summary.
3. Run static tests; clearly label untested engine behavior. Never use the public repo to distribute installed AGOT/CK3 assets.
4. Record progress, blockers, next task and relevant checks in `docs/PROGRESS.md`.
5. A recurring ChatGPT automation has been configured to revisit this GitHub repository approximately every 3 hours and continue self-contained tasks where its tools allow. This is **not** guaranteed to launch a new Codex Cloud task. Codex `/goal` can pursue a bounded goal within a compatible Codex session and quota, but it is not a paid-free 24/7 fleet. Work event-triggered GitHub PR tasks are another option if separately set up.
6. Do not ask the owner to carry messages between Codex and ChatGPT for ordinary development. Agents should use accessible GitHub tools and perform bounded work themselves.
7. Allow autonomous merges for well-checked documentation, tooling, and incrementally statically validated original code, with clear **not engine-tested** labels. Isolate high-risk Mega War / CB changes until enough evidence exists. Never merge failing changes.
8. Do not claim success for engine-dependent behavior without CK3. But missing CK3/AGOT is **not** a blocker to scaffolding, documentation, static validation, and independently verifiable changes. If GitHub PR creation is unavailable in a specific session, commit and use whatever Git/GitHub publishing capability is available; otherwise report the exact blocker without discarding completed local work.
9. No paid APIs or servers. ChatGPT Plus does not automatically include Agents API consumption.
10. Keep reports to the owner concise; normal engineering choices are delegated.

**Note:** The owner currently expects broad in-game testing at the end; this introduces risk. Static validation cannot prove mod compatibility, so mark critical gameplay features as provisional until those tests.
