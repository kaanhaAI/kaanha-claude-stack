# FAQ

**Does any of this phone home?**
No. The gate is a local Python script; the dev hub is a local Python script; skills and agents are markdown instructions. No telemetry, no accounts, no network calls from anything we ship. The whole auditable surface is ~400 lines of stdlib Python plus markdown — read it.

**Does it send my code anywhere?**
Nothing beyond what Claude Code itself already does. The tester and verifier are Claude agents reading your repo in your own session, under your own Anthropic account.

**Why is the first push blocked? I didn't ask for that.**
Installing kaanha-quality *is* asking for it — a quality gate that only applies when convenient isn't a gate. The one-word cost ("ship it") buys you a real test run and an adversarial review on every push. If a repo shouldn't have it, [opt out per-repo](push-gate.md#per-repo-opt-out); if a moment demands it, `KAANHA_GATE=off`.

**What exactly runs automatically?**
Two things: skill descriptions load at session start (a few hundred tokens — bodies load only when relevant), and the PreToolUse hook checks Bash/PowerShell commands for `git push`. That's the entire ambient footprint. The dev hub does nothing until you invoke it — we deliberately ship no auto-scanning of your disk.

**How do I update?**
`/plugin marketplace update kaanha-stack`, then restart your session. No versions are pinned; you get the latest on each update.

**How do I uninstall?**
`/plugin uninstall kaanha-quality@kaanha-stack` (and `kaanha-dev@kaanha-stack`), or disable per-repo with `"enabledPlugins": {"kaanha-quality@kaanha-stack": false}` in that repo's `.claude/settings.json`. Leftover `.git/kaanha-gate` stamps are inert one-line files — delete or ignore.

**Does the gate work with worktrees / submodules / monorepos?**
The stamp lives in the repo's resolved `.git` directory (`git rev-parse --git-dir`), so worktrees each get their own stamp. Monorepos: one stamp per repo, not per package.

**Can I use the agents without the gate?**
Yes — `kaanha-tester` and `kaanha-verifier` are ordinary Claude Code agents. Ask Claude to "run kaanha-verifier on this diff" any time, gate or no gate.

**Why Python for the gate?**
Ubiquitous, stdlib-only, auditable in one read, and not part of any JS toolchain your repo might be messing with mid-change.

**Who's behind this?**
[Kaanha Tech](https://github.com/kaanhaAI) — an Australian AI & technology studio. The curated plugins belong to their respective authors (see [credits](curated-plugins.md)); the original plugins are MIT-licensed.
