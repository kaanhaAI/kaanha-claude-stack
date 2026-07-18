---
name: auto-agents
description: The on-demand per-project agent suite - eight reviewers that fire WHILE you work in any repo and adapt to it. Use when the user asks what these agents do, when to run them, or right after installing kaanha-auto. Also the reference for which agent to invoke at which moment during normal work.
---

# kaanha-auto — per-project agents

Eight agents that adapt to whatever project you are in. Unlike the **fleet**
(kaanha-agents, scheduled cron squads) and the **pre-push gate**
(kaanha-quality, tester + verifier before a push), these fire **on demand while
you work** - the main session invokes the right one at the right moment. Every
one reads the current project's `CLAUDE.md`, stack, and conventions first, so
the same suite works in a Next.js SaaS, a SvelteKit site, or a Python API with
no per-project setup.

| Agent | What it does | Invoke it when |
|---|---|---|
| **code-reviewer** | bugs, security, perf, project-convention adherence | after code is written, before commit |
| **compliance-reviewer** | the frameworks the project is actually subject to (SOC 2 / GDPR / HIPAA / PCI / platform policy) | after changes to auth, data handling, webhooks, billing, AI, or user data |
| **architecture-reviewer** | module boundaries, dependency direction, data flow, structural risk | new files/modules, or a change spanning 3+ files |
| **test-writer** | tests in the project's own framework, security-critical paths first (edits test files only) | after new library / business-logic code |
| **doc-generator** | CLAUDE.md sections, README, API docs, doc comments | after a feature lands |
| **claude-md-sync** | keeps CLAUDE.md true to the code | after a change alters routes/models/commands/key files |
| **agent-watcher** | verifies the other agents' findings against real code (catches hallucinations) | after another agent reports, before acting on it |
| **deploy-monitor** | diagnoses deploy/build/healthcheck failures, proposes a fix as a PR — never deploys unattended | when a deploy or build breaks |

## How they behave (shared contract)

- **Adapt to the project first, never assume.** Read its `CLAUDE.md` and detect
  its stack before reviewing or writing anything. A finding that assumes the
  wrong framework is worse than no finding. (Claude Code also auto-loads the
  project's CLAUDE.md into every subagent, so adaptation is both instructed and
  structural.)
- **Learn the project over time.** Each agent has project-scoped memory
  (`memory: project` — stored in `.claude/agent-memory/<agent>/`, committable to
  the repo). It reads what it has learned about this project at the start and
  records durable patterns, conventions, and false-positive traps at the end, so
  the same agent gets sharper on a codebase the more it runs there. Adaptation is
  per-run; memory is what makes it compound. The read-only reviewers keep their
  memory even though they cannot edit code — memory I/O is enabled independently
  of the tool allowlist.
- **Stay in their lane.** The reviewers (code / compliance / architecture /
  agent-watcher) are **read-only** - they report, they do not edit. test-writer
  edits **test files only**. doc-generator and claude-md-sync edit **docs only**.
  deploy-monitor proposes a **PR**, never a live deploy.
- **Verify, don't guess.** Cite real file:line evidence; run tests you write;
  label anything unverified as a hypothesis. agent-watcher exists to catch the
  confident-but-wrong finding, so run it when a finding will drive a change.

## Auto-review at end of turn (on by default)

Since 0.3.0 the suite fires **automatically** at a checkpoint, so you don't have
to remember to invoke it. A `PostToolUse` hook logs which **code** files you edit
each turn (docs/config are ignored); a `Stop` hook, when the turn ends, tells the
session to run the reviewers relevant to what changed — always `code-reviewer`,
plus `compliance-reviewer` if an auth/webhook/billing/privacy path was touched,
plus `architecture-reviewer` if three or more files changed — apply any
blocker-level fixes, and report a one-line verdict each, before stopping.

Why a checkpoint and not per-edit: a hook cannot spawn a subagent, and reviewing
after every keystroke is noisy and expensive. The checkpoint reviews the turn's
changes once, targeted to what actually changed.

Safety: it is **loop-safe** (the `stop_hook_active` guard means the reviewers'
own fix-edits are never re-reviewed in the same turn) and **fail-open** (any hook
error simply lets the turn end — it can never wedge a session). Turn it off per
machine with `KAANHA_AUTO_REVIEW=off` in your settings `env` (the off switch is
also printed in the checkpoint message itself).

## Relationship to the rest of the stack

- kaanha-quality's **kaanha-verifier** is the adversarial pre-push check;
  **code-reviewer** here is the lighter, continuous read while you work. Use
  code-reviewer as you go, verifier at the gate.
- kaanha-agents' scheduled **code-reviewer squad** reviews the last-24h diff
  overnight; this one reviews the change in front of you, now.
- Nothing here is Kaanha-specific: the suite ships generic and adapts per repo.
