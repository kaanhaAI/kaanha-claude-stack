# Getting started

## Requirements

- **Claude Code** (CLI, desktop, or IDE extension)
- **Python 3.8+ on PATH** — the push gate is a ~200-line stdlib script, zero pip packages
  - Windows: `winget install Python.Python.3.12`
  - macOS: `brew install python`
  - Linux: `sudo apt install python3`

## Install

In any Claude Code session:

```
/plugin marketplace add kaanhaAI/kaanha-claude-stack
/plugin install kaanha-quality@kaanha-stack
/plugin install kaanha-dev@kaanha-stack
```

Plugins install at **user level** — they're active in every project on your machine, not just the current one.

## First run: two things to expect

1. **A trust prompt, once per workspace.** kaanha-quality ships a hook (the push gate), and Claude Code asks you to approve third-party hooks before they can run. That prompt is the security model working — review and approve.
2. **Your next `git push` fails.** This is the product, not a bug:

```
kaanha-gate BLOCKED this push: HEAD a1b2c3d has not passed the ship workflow.
  1. Run the project's tests and make sure they pass.
  2. Run the kaanha-verifier agent on the diff and resolve real findings.
  3. After the FINAL commit, approve the gate.
```

Say **"ship it"** and Claude runs the whole workflow for you — see [the push gate guide](push-gate.md).

## Your first 60 seconds

```text
$ git push
kaanha-gate BLOCKED this push ...

> ship it
  kaanha-tester    npm test ............ 14/14 PASS (added a test for your untested handler)
  kaanha-verifier  3 findings .......... fixed, re-verified
  kaanha-gate      approved a1b2c3d

$ git push
   e4f5g6h..a1b2c3d  main -> main
```

## Optional next steps

- Set up the [dev hub](dev-hub.md) (one-time, ~2 minutes) for centralized dev servers
- Install the [curated companion plugins](curated-plugins.md)
- Read the [FAQ](faq.md) for per-repo opt-outs and the escape hatch
