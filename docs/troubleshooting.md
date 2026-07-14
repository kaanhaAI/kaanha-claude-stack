# Troubleshooting

## Push gate

**"My push is blocked and I don't know why."**
That's the gate working. HEAD doesn't match the approval stamp. Say "ship it" to run the workflow, or if you genuinely just verified everything: `python <plugin>/scripts/push_gate.py --approve` from the repo, then push.

**"I approved, amended a commit, and it's blocked again."**
By design — a new commit means new content that hasn't been verified. Re-approve after the final commit.

**"The hook prints a Python error / 'python' is not recognized."**
Python 3 isn't on PATH. The gate fails **open** in this state (pushes go through with a warning — you're unprotected, not stuck). Install Python (see [Getting started](getting-started.md)) and restart your session.

**"I need to push NOW, no questions."**
`KAANHA_GATE=off git push` (set the env var however your shell does it). The escape hatch is deliberately user-only — decide consciously.

**"The gate blocks pushes in a repo where I don't want it."**
Per-repo opt-out — see [the push gate guide](push-gate.md#per-repo-opt-out).

**"Pushes from my terminal (outside Claude) aren't gated."**
Correct — the gate is a Claude Code hook; it governs pushes *Claude* makes. Your own terminal is your own judgment. If you want it everywhere, wire `push_gate.py` into git's native `pre-push` hook yourself.

## Ship workflow

**"The tester says 'no automated checks found'."**
Your project has no detectable test/build/lint commands (package.json scripts, pytest, Makefile). The verifier still runs; the report will say the push is going out test-less. Add a test script to change that.

**"The verifier reported findings I disagree with."**
It ranks them and shows its evidence (file:line + failure scenario). MINOR findings are explicitly fix-if-quick. If a BLOCKER is genuinely wrong, tell Claude why — the workflow requires findings to be *verified*, not just plausible, and a wrong finding should be challenged.

## Dev hub

**"start fails with 'npm/pnpm is not recognized' (Windows)."**
Claude sessions don't inherit your shell's PATH. Route the registry entry through `withnode.cmd` — see [dev hub setup](dev-hub.md), step 3.

**"The server starts but on the wrong port."**
Registry port and the app's own config disagree. For `PORT`-reading servers add `"env": {"PORT": "<port>"}`; for Next.js pass `-p` in `runtimeArgs`; then `sync`.

**"scan didn't find my project."**
`scan` looks for `package.json` with a `dev`/`start` script under `projectsRoot`, and skips anything in `ignore` or already registered. Python/other projects: add a registry entry manually.

**"stop says 'not running' but the port is busy."**
`stop` only kills servers the hub started (it tracks PIDs). Something else owns that port — find it with your OS tools, or restart it through the hub so it's tracked.

## Install / plugins

**"Skills aren't triggering after install."**
Plugins load at session start. Close and reopen the session. Also check the trust prompt wasn't dismissed — hooks and skills wait for workspace trust.

**"I updated but nothing changed."**
Run `/plugin marketplace update kaanha-stack`, then restart the session.
