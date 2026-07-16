# Changelog

## marketplace 1.8.0 — 2026-07-16

- **New plugin: kaanha-3d-web 0.1.0 — premium 3D web experiences.** Five
  skills: **experience-director** (narrative → spatial metaphor → chapter
  structure → build-ready brief), **threejs-builder** (engine decision
  ladder from raymarched SDF to Three.js/Threlte/R3F, GLTF/Draco/KTX2
  pipeline, draw-call budgets, and the hard floors — reduced-motion
  poster, tab-hidden pause, DPR cap, synchronous first frame — in code
  from commit one), **motion-director** (Lenis + GSAP/ScrollTrigger,
  damped scroll-driven cameras, reduced-motion as a designed artifact,
  zero-CLS discipline), **shader-artist** (GLSL pattern library with GPU
  cost notes), **premium-review** (12-point ship gate accepting only
  measured fps/CLS/Lighthouse, delegating a11y and SEO to the skills
  that own them).
  Seeded from a cinematic hero that shipped to production, so each
  pattern carries the failure that produced it — most usefully,
  shader-artist teaches the **dynamic** march loop bound because a
  constant-bounded loop makes ANGLE's D3D backend unroll 72 inlined
  copies of your SDF and stall fxc for minutes inside the first draw
  call, which reads as a frozen tab on Windows Chrome.
- **README: a "fork it, don't edit your install" section.** Plugin
  updates overwrite the local plugin cache, so local edits are silently
  destroyed — forking is the supported way to customize, and MIT means
  you may fork, strip, rebrand, and ship commercially (upstream authors'
  attribution on curated pointers stays).



## marketplace 1.7.6 — 2026-07-15

- **CRITICAL FIX — kaanha-quality and kaanha-agents could not install:
  UTF-8 BOM in their plugin.json.** Caught by the new install-e2e
  workflow on its very first run (both OSes): `claude plugin install`
  rejects a BOM'd manifest as "corrupt" (`JSON Parse error: Unrecognized
  token '﻿'`), so the one-command install delivered only 3 of 5
  plugins — without the quality gate itself. The BOM (a Windows
  PowerShell write artifact) is stripped from both manifests (and from
  two workflow YAMLs for hygiene). If your install printed
  "corrupt manifest" for these two plugins, re-run install-all.
- **validate-plugins now fails red on BOM.** The validator read files
  with `utf-8-sig`, tolerating exactly what Claude Code's parser
  rejects — a green guard in front of an uninstallable plugin. It now
  checks the raw bytes of every JSON file it validates.

## marketplace 1.7.5 — 2026-07-15

- **install-all proven end-to-end in CI.** New `install-e2e` GitHub
  workflow (manual dispatch + weekly + on installer changes): a clean
  runner installs the Claude Code CLI via npm, runs the install-all
  script exactly as the README instructs — `install-all.sh` on Linux,
  `install-all.ps1` through `powershell.exe` on Windows — and fails red
  unless all five core plugins actually register in `claude plugin
  list`. No Anthropic login is needed for plugin commands (git-clone +
  local-cache operations; noted honestly in the workflow header).
- **Fix: install-all.ps1 could die on a stderr warning.** Windows
  PowerShell 5.1 wraps native stderr into throwing ErrorRecords when
  the stream is redirected; with the script's `$ErrorActionPreference
  = "Stop"`, a mere "already registered" notice from `claude plugin
  marketplace add` killed the installer before it installed anything.
  Now `Continue`, with failures still tracked per plugin.
- **Fix: both install-all scripts now exit non-zero when any plugin
  fails to install** (previously they printed the failure list but
  exited 0, so scripted/CI use could not detect a partial install).

## marketplace 1.7.4 — 2026-07-15

- **kaanha-quality 1.5.2 — push gate hardened + fully behavior-verified.**
  Found during a claims-vs-reality audit: a payload with a UTF-8 BOM (as
  Windows shells produce when piping) failed JSON parsing, and the gate's
  fail-open clause allowed the push. Real Claude Code hook payloads are
  clean UTF-8, but a gate should not fail open that easily — stdin is now
  BOM-stripped. Full matrix verified live: unapproved push blocks (exit
  2), --approve then push passes, dry-runs and non-push commands pass.

## marketplace 1.7.3 — 2026-07-15

- **Guarantee against silent plugin death.** New `validate-plugins`
  GitHub workflow + `scripts/validate-plugins.py`: every push touching a
  plugin now validates all manifests against the loading rules that bit
  us in 1.7.2 (agents field must be .md file paths or omitted, hooks
  JSON must parse, skills need SKILL.md frontmatter, versions present).
  An unloadable manifest fails the push red — it can no longer land on
  main unnoticed. Forks inherit the same protection.

## marketplace 1.7.2 — 2026-07-15

- **CRITICAL FIX — kaanha-quality 1.5.1 / kaanha-agents 1.2.1 silently
  failed to load.** Both manifests declared `"agents": "./agents/"`, but
  the plugin spec requires the agents field to list individual .md files
  (or be omitted for auto-discovery) — a directory value makes Claude Code
  skip the ENTIRE plugin with no error: no push gate, no session mandate,
  no /ship, no squads. If your gate never blocked a push or the squads
  never appeared, this was why. The field is now omitted (default
  auto-discovery). Update both plugins, then restart your session.

## marketplace 1.7.1 — 2026-07-15

- **One-command install.** `scripts/install-all.ps1` (Windows) and
  `scripts/install-all.sh` (macOS/Linux) register the marketplace and
  install the four kaanha plugins + watch-skill via the `claude` CLI —
  add `-WithCurated` / `--with-curated` for the third-party pointers.
  The README also documents the zero-command team option:
  `extraKnownMarketplaces` + `enabledPlugins` in a project's
  `.claude/settings.json` auto-installs everything on folder trust.

## marketplace 1.7.0 — 2026-07-15

- **kaanha-agents published — the eleven autonomous squads.** The fleet
  layer joins the public catalog: code-guardian, daily-ops, design-warden,
  growth-marketer, growth-scout, site-sentinel, repo-night-watch,
  code-reviewer, security-auditor, overnight-builder, and flow-tester —
  config-driven from a bundled fleet.json template, running on local
  schedules while the Claude app is open, each rewriting its own HTML
  report. Read **docs/agents.md before installing** — this plugin creates
  scheduled tasks, launches a browser, and makes local commits. Cloud
  forms of the mechanical squads remain available as the top-level
  workflow templates.

## marketplace 1.6.0 — 2026-07-15

- **kaanha-quality 1.5.0 — onboarding.** New users no longer discover the
  stack piece by piece: the first session after install prints a one-time
  "what you now have" notice (push gate, mandate, /ship pipeline, update
  notifications), and a new **/kaanha-tour** skill gives a two-minute
  guided walkthrough of everything installed — including a live demo of
  the push gate refusing an unapproved push. The notice shows exactly
  once per machine; delete
  `~/.claude/plugins/data/kaanha-quality/welcomed.json` to see it again.

## marketplace 1.5.1 — 2026-07-15

- **Fix: site-sentinel template died before probing anything.** The runner's
  `bash -e` killed the script on its first statement: `read` from a
  process-substituted `curl -w` returns 1 because curl emits no trailing
  newline. Every run failed red in ~0.5s with zero output — looking exactly
  like a site outage. Now reads via a here-string. If you copied
  site-sentinel.yml before 1.5.1, re-copy it.

## marketplace 1.5.0 — 2026-07-15

- **kaanha-quality 1.4.0**: new session-mandate working rule — *use the
  browser wherever the task needs one*. Verifying UI, reading live pages
  or dashboards, and driving web flows should happen in the available
  browser tooling (in-app browser pane, or Claude in Chrome when a
  logged-in session is required) instead of being described back as
  manual steps for the user. Payments, credentials, and irreversible or
  public actions still require explicit confirmation.

## marketplace 1.4.3 — 2026-07-15

- **cloud-reasoning**: provider errors (quota, bad key, unknown model) now
  fail the run red instead of filing bogus "findings" issues on every cron.
- **telegram-test**: the Telegram API response body is no longer printed to
  run logs (it echoed the chat id and group metadata).

## marketplace 1.4.2 — 2026-07-15

- **Fix: cloud-reasoning template crashed on large diffs.** `git log -p`
  piped into `head -c` was SIGPIPE-killed once the 24h diff passed 120KB,
  failing the step under Actions' strict bash flags — i.e. the nightly
  review died exactly on busy days. Now writes to a file and truncates
  from it. If you copied cloud-reasoning.yml from 1.4.1, re-copy it.

## marketplace 1.4.1 — 2026-07-15

- **Cloud fleet templates published** (`templates/workflows/`): site-sentinel
  (6-hourly uptime), dependency-audit (weekly advisories), cloud-reasoning
  (provider-agnostic nightly LLM diff review — Gemini/OpenAI/Grok), and
  telegram-test. All hardened against report-content injection.
- **Telegram push alerts**: every failure-filing template carries an optional
  alert step (dormant until TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID secrets
  exist). `scripts/connect-telegram.ps1` sets both secrets on all your repos
  from one prompt, with live token validation and group-id auto-detection.

## marketplace 1.4.0 — 2026-07-15

- **Video stack published**: new original plugin **kaanha-ugc 0.1.0**
  (creator analytics — hook/retention/scroll-stop/CTA/best-clips analysis,
  timestamp-anchored, self-contained HTML report) plus curated pointers to
  its engines: **watch-skill** by oxbshw (recommended; persistent video
  memory, local-first) and **claude-video** by bradautomates (lightweight
  watch-once). Full credit to the upstream authors.

All client-visible changes to the kaanha-stack plugins. Update detection in
Claude Code is keyed on each plugin's `version` field — every entry here
corresponds to a version bump you can pull with
`/plugin marketplace update kaanha-stack` + `/plugin update <plugin>@kaanha-stack`
(or automatically, with auto-update enabled for this marketplace).

## kaanha-quality 1.3.0 — 2026-07-15

- **Self-notifying update check** (SessionStart hook): compares the installed
  version against this repo's published manifest and prints an in-session
  notice when a newer version exists. One HTTPS GET per 24h max, 3s timeout,
  silent on any failure, stdlib only; no data about you or your repos is
  sent. Opt out with `KAANHA_UPDATE_CHECK=off` or by removing the hook line.

## kaanha-quality 1.2.0 — 2026-07-15

- **Session mandate**: the SessionStart hook now injects the full working
  instruction set in every project — check don't guess, one step at a time,
  complete what you started, plus the deliverables rule below.
- Opt out by deleting the `SessionStart` block from `hooks/hooks.json`.

## kaanha-quality 1.1.0 — 2026-07-15

- **Deliverables mandate** (SessionStart hook): reports and deliverables are
  produced as self-contained HTML files, updated in place (no dated copies),
  delivered rendered.

## kaanha-quality 1.0.0

- Initial release: deterministic push gate (PreToolUse hook blocking
  unapproved `git push`), kaanha-tester + kaanha-verifier agents, and the
  ship workflow that ties them together.

## kaanha-dev 1.0.0

- Initial release: centralized dev-server hub — one registry with unique
  ports, stdlib launcher (list/start/stop/status/logs), project scan, and
  sync-generated launch.json files.
