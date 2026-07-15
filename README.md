# kaanha-claude-stack

> **One prompt in, verified working product out — humans only at consent, credentials, and the ship decision.**

**One marketplace that turns Claude Code into a self-managing engineering environment** — a hard quality gate in front of every `git push`, one registry for every dev server on your machine, and curated pointers to the best open-source skills.

Built and battle-tested by [Kaanha Tech](https://kaanha.tech) across a multi-project Windows dev machine.

## Install

```
/plugin marketplace add kaanhaAI/kaanha-claude-stack
/plugin install kaanha-quality@kaanha-stack
/plugin install kaanha-dev@kaanha-stack
```

**📚 Full documentation: [Knowledge Base](docs/README.md)** — getting started, the push gate, the dev hub, troubleshooting, FAQ.

**Staying updated — since v1.3.0 the plugin notifies you itself:** at session start it compares your installed version against this repo's latest (one HTTPS GET per day max, 3-second timeout, silent on any failure, Python stdlib only — nothing about you or your repo is sent) and tells you in-session when an update exists. Opt out with `KAANHA_UPDATE_CHECK=off`. For hands-free installs on top of that, open `/plugin` → **Marketplaces** → `kaanha-stack` → **Enable auto-update** — Claude Code then pulls new versions shortly after startup and prompts `/reload-plugins`. Prefer manual control? Pull updates any time with:

```
/plugin marketplace update kaanha-stack
/plugin update kaanha-quality@kaanha-stack
```

Releases are versioned (see [CHANGELOG.md](CHANGELOG.md)) — **Watch → Custom → Releases** on this repo if you want GitHub to email you when a new version ships.

**Requirements:** Python 3.8+ on PATH — the push gate is a ~200-line stdlib script, zero pip packages.
(Windows: `winget install Python.Python.3.12` · macOS: `brew install python` · Linux: `sudo apt install python3`.)
The ship workflow checks this first and refuses to push until Python is present — without it the gate can't protect you.

## Quick start — your first 60 seconds

```text
$ git push
kaanha-gate BLOCKED this push: HEAD a1b2c3d has not passed the ship workflow.
  1. Run the project's tests and make sure they pass.
  2. Run the kaanha-verifier agent on the diff and resolve real findings.
  3. After the FINAL commit, approve the gate.

> ship it
  kaanha-tester    npm test ............ 14/14 PASS (added test/api.test.js — your handler had zero coverage)
  kaanha-verifier  3 findings .......... fixed, re-verified over live HTTP
  kaanha-gate      approved a1b2c3d

$ git push
   e4f5g6h..a1b2c3d  main -> main
```

That blocked first push is the product: quality stops being advice and becomes a locked door.
Any commit after approval re-locks the gate automatically. Escape hatch (yours, not the model's): `KAANHA_GATE=off`.

## Original plugins (ours)

### kaanha-quality — verified pushes only

A `git push` is **blocked by a deterministic hook** until the exact HEAD commit has passed the ship workflow:

```
task done → kaanha-tester   (runs your real test/build/lint, fills test gaps)
          → kaanha-verifier (adversarial diff review: fidelity, correctness,
                             call-site regressions, leftovers)
          → fix findings → final commit
          → gate approval stamps that HEAD sha
          → git push passes; any new commit re-locks the gate
```

No model judgment in the gate itself — it's a ~100-line stdlib Python
PreToolUse hook (exit 2 blocks, approval file compared against HEAD).
Works on Bash and PowerShell, fails safe, dry-runs pass through.
User-only escape hatch via `KAANHA_GATE=off`.

Also ships a **session mandate**: a SessionStart hook that injects a short
instruction set into every session, in every project — current or new:

- **Check, don't guess** — read the actual file/config/version before acting
  on it; never fill a gap with a plausible assumption
- **One step at a time** — complete and confirm each step before the next
- **Complete what you started** — fix friction instead of silently pivoting
  to an alternative approach
- **Use the browser wherever the task needs one** — verify UI and drive web
  flows in the available browser tooling instead of describing manual steps
  (payments, credentials, and irreversible actions still confirm first)
- **Deliverables are self-contained HTML** — updated in place (never dated
  copies), delivered rendered

Install the plugin once and the working discipline follows you everywhere.
Don't want it? Delete the `SessionStart` block from `hooks/hooks.json`.

### kaanha-dev — one hub for every dev server

Stop juggling ports and per-project configs:

- `registry.json` — every project, every port, one file
- `kaanha_dev.py list | status | start | stop | logs` — from anywhere; detached servers, per-server logs
- `scan` — auto-enrolls new projects with the next free port
- `sync` — generates each project's `.claude/launch.json` so Claude's browser preview works natively
- Windows PATH wrapper included (Claude sessions don't inherit your interactive shell's PATH — this bites everyone eventually)

### kaanha-ugc — video creator analytics

Turn any video into a creator report: hook strength, retention/pacing
heuristics, scroll-stop moments, CTA placement, best-clip picks per platform,
and ready-to-post captions — every claim timestamp-anchored, no invented
metrics, delivered as one self-contained HTML report.

It's an **analysis layer**, engine-agnostic by design: pair it with
**watch-skill** (recommended — persistent video memory + cross-library
search, local-first, `$0` offline mode) or **claude-video** (lightweight
watch-once). Both are curated in this marketplace:

```
/plugin install kaanha-ugc@kaanha-stack
/plugin install watch-skill@kaanha-stack
```

The engine needs one-time machine setup (Python 3.11+; ffmpeg and yt-dlp
auto-bootstrap) — run `/setup-watch-skill` once after installing and its
doctor handles the rest. kaanha-ugc self-announces when it's ready and
refuses to fabricate an analysis without real frames + a real transcript.

## Curated pointers (not ours — install straight from their authors)

| Plugin | Author | What it does |
|---|---|---|
| [ponytail](https://github.com/DietrichGebert/ponytail) | Dietrich Gebert | YAGNI persona: the laziest senior dev in the room |
| [impeccable](https://github.com/pbakaus/impeccable) | Paul Bakaus | 23-command design lifecycle + 44 anti-slop detectors |
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | nextlevelbuilder | Offline searchable design database |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | forrestchang | Four principles against classic LLM coding failures |
| [mempalace](https://github.com/MemPalace/mempalace) | MemPalace | Local-first verbatim AI memory |
| [watch-skill](https://github.com/oxbshw/watch-skill) | oxbshw | Persistent video memory + cross-library search — the recommended kaanha-ugc engine |
| [claude-video](https://github.com/bradautomates/claude-video) | bradautomates | `/watch` — frames + transcript for Claude's own vision, watch-once |

Also pairs beautifully with [hallmark](https://github.com/Nutlope/hallmark) by Hassan El Mghari (Together AI) — anti-slop page building with structural variety (`npx skills add nutlope/hallmark`).

The marketplace entries for these point at the **upstream repos**, so you always get the authors' latest — full credit to them; this repo just curates and composes.

## Cloud fleet templates + phone alerts

[`templates/workflows/`](templates/workflows/) holds copy-in GitHub Actions
that run whether your machine is on or off:

- **site-sentinel.yml** — 6-hourly uptime + route health for any site; files
  a GitHub issue on failure
- **dependency-audit.yml** — weekly high/critical advisory scan; files a
  labelled issue
- **cloud-reasoning.yml** — provider-agnostic nightly LLM review of the
  last-24h diff (Gemini / OpenAI / Grok; bring one API key)
- **telegram-test.yml** — one-click verification of the alert channel

Every failure-filing template carries an optional **Telegram push alert**:
create a bot with @BotFather, add it to your group, then run
[`scripts/connect-telegram.ps1`](scripts/connect-telegram.ps1) — it validates
the token live, auto-detects your group's chat id, and sets the two secrets
on every repo you name. From then on failures land on your phone. All
templates are hardened against report-content injection (toJSON assigned to
a variable, never spliced into template literals; unique heredoc delimiters;
alert messages are static text + run link only).

## The pattern this repo demonstrates

Skills are passive knowledge. The stack becomes autonomous when you add:

1. **Agents** — pair related skills into a worker with a mission and an output contract
2. **Hooks** — deterministic event triggers (session start, pre-push, post-edit)
3. **Schedules** — time triggers that run agents with nobody at the keyboard
4. **Standing reports** — each routine rewrites its own HTML report in place; history lives in git

kaanha-quality and kaanha-dev are working examples of layers 1–2. Compose your own squads on top.

## License

MIT — see [LICENSE](LICENSE).
