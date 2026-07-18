# Changelog

## marketplace 1.14.0 — 2026-07-18

- **The fleet now covers every project automatically, and the dev hub is
  truly portable.** Two long-standing gaps closed together. (1) **Auto
  coverage:** the 24/7 squads read a hand-maintained repo list, so a new
  project got dev-hub enrollment but zero fleet coverage. The dev hub's
  SessionStart scan now derives fleet targets from its registry — enrol a
  project once and both the hub and every squad cover it, no hand editing.
  (2) **Portability (kaanha-dev 1.1.0):** the launcher is bundled in the
  plugin and resolves its config from an ops home (`KAANHA_HOME`, else
  `~/.claude/kaanha`), bootstrapped from templates on first run — so a
  one-command client install gets a working dev hub + auto fleet coverage
  instead of a hook pointing at a path that only existed on the author's
  machine. Fresh fleet reports are surfaced at SessionStart so they aren't
  invisible from a project. (3) **kaanha-agents 1.3.0:** all 11 agent docs
  + the routines skill are genericized off "the marketplace repo root" onto
  the resolved ops home, and fleet setup now asks (MCQ) how each squad
  should run — local (skips when the machine is off) vs cloud (GitHub
  Actions, always on) — with storing tool approvals made a required step so
  local squads stop firing-without-finishing.


## marketplace 1.13.0 — 2026-07-18

- **kaanha-quality 1.9.0 — two new hard mandate rules: NEVER ASSUME, and
  ask in MCQ.** The SessionStart mandate that every project inherits gains
  two firm working rules. **NEVER ASSUME:** if acting would require
  assuming any unverified fact, stop and ask rather than proceed on a best
  guess — this overrides "act autonomously," so even reversible work waits
  when it rests on an unchecked assumption. **Always ask in MCQ format:**
  every hand-back to the user is multiple choice — questions, decisions,
  approvals, review requests, and status updates alike — so choices are
  explicit and nothing advances on a silent assumption. Ships to every
  project the plugin is enabled in, same mechanism as the push gate.


## marketplace 1.12.0 — 2026-07-18

- **kaanha-quality 1.8.0 — the state probe now catches plugin-version
  drift.** A directory-source marketplace ships a version the moment
  `plugin.json` changes, but the machine's installed record and
  materialized cache do not move with it — so the app keeps loading the
  old code while the release *looks* done. This gap had bitten twice
  (kaanha-agents stuck at 1.0.0, kaanha-factory at 1.1.0), each caught
  only by hand. The `state_probe.py` SessionStart hook now compares every
  installed record against the version its repo declares and names any
  that lag, with the fix (materialize the cache, repoint the record,
  restart). Self-limiting: github-source plugins have no local
  `plugin.json` to read, so they are skipped rather than false-flagged.
  Still stdlib-only, fail-silent, and silent when everything is aligned.
  Opt out with `KAANHA_STATE_PROBE=off`.


## marketplace 1.11.1 — 2026-07-16

- **One-command install now delivers the whole stack.** The install-all
  scripts had drifted: they installed five plugins and missed the two
  newest — **kaanha-factory** and **kaanha-3d-web** — so a new user's
  single command silently shipped an incomplete stack. Both scripts, the
  README's zero-command team snippet (`enabledPlugins`), and the
  install-e2e CI (which now asserts all **seven** core plugins register
  and load error-free on a clean Linux + Windows runner) are updated
  together, so this cannot drift unnoticed again — the CI fails red if
  the installer and the catalog disagree.


## marketplace 1.11.0 — 2026-07-16

- **New plugin: kaanha-factory 1.2.0 — build-from-scratch lifecycle.**
  The public catalog now has the greenfield orchestrator that was
  internal-only: on a "build me an app/SaaS/bot/API from scratch"
  request it runs discovery → research → architecture → plan → implement
  → verify (via the ship gate) → document → deploy, scaled S/M/L. It
  governs *which phases exist*; ponytail still governs the code within
  them. Pairs with kaanha-3d-web (factory runs the lifecycle, 3d-web
  builds the premium hero inside it) and every phase delegates to
  enforced machinery — the gate, the squads, the design skills — instead
  of prose promises. Its architecture phase now routes design work to the
  right skill by need (reference vs critique vs page-structure vs
  premium-3D) rather than lumping them together.


## marketplace 1.10.0 — 2026-07-16

- **kaanha-quality 1.7.0 — the stack now learns, locally.** Two additions,
  both local-only: **nothing is transmitted, ever** (this stack has no
  telemetry, and the update check's promise — *"nothing about you or your
  repo is sent"* — is not up for renegotiation). Your machine is the only
  place your state lives.
  - **Project state probe** (SessionStart): reads the project you are
    actually in — anchored to the repo root, workspace-aware — and injects
    only what changes what happens next: no test script anywhere (the gate
    will have nothing to run), a UI project with no BRAND.md, a 3D/WebGL
    project (detected by deps *or* a scenes/shaders directory, because a
    hand-written raymarched scene has no three.js in package.json). Silent
    when there is nothing worth saying. Opt out: `KAANHA_STATE_PROBE=off`.
  - **Lessons store** (`scripts/lessons.py`): the machine-readable half of
    the mandate's *record what bites you* rule. Memory files are prose, for
    humans, for one folder; this is structured, tagged by project shape, and
    **countable** — so a lesson recorded in one repo reaches the next repo of
    the same shape, and a lesson recorded three times gets flagged for what
    it is: an unbuilt guard. `lessons.py --stats` shows what keeps biting.
    Re-phrasings group by similarity, so the counter cannot be fooled by
    typing the same lesson three different ways. Opt out: `KAANHA_LESSONS=off`.


## marketplace 1.9.0 — 2026-07-16

- **kaanha-quality 1.6.0 — the mandate learns.** New sixth working rule:
  *record what bites you.* When a gate, test, verifier, squad, or the
  user catches a **real** defect, the lesson goes into project memory
  before moving on — what was believed, what was true, the rule that
  prevents it — and then the higher-value question gets asked: **can a
  machine enforce this?** A check that fails red beats a lesson that must
  be remembered; recurring lessons are unbuilt guards.
  This rule is why this changelog reads the way it does. Every CRITICAL
  FIX above (the silent-death manifest, BOM-at-install, duplicate hooks,
  green-checks-that-lie) was a lesson that became a validator check —
  previously that promotion happened because someone noticed. Now it is
  standard procedure.



## marketplace 1.8.1 — 2026-07-16

- **kaanha-quality 1.5.3 / kaanha-ugc 0.1.1 — hooks failed to load from
  the manifest.** Both manifests declared `"hooks": "./hooks/hooks.json"`,
  but Claude Code loads that standard path automatically and then rejects
  the manifest's duplicate reference: *"Hook load failed: Duplicate hooks
  file detected"*, recorded against the plugin while the install still
  reports success. The field is now omitted (auto-discovery), which is
  what `manifest.hooks` was never meant to duplicate — it is for
  ADDITIONAL hook files only.
- **The e2e assert no longer trusts "installed".** `claude plugin list
  --json` reports per-plugin load failures in an `errors[]` array while
  still listing the plugin and exiting 0 — the first green install-e2e
  run was green *while carrying this bug*. The workflow now fails red on
  any non-empty `errors[]` or any `enabled: false`, and validate-plugins
  rejects a `hooks` field pointing at the default path, so this class
  cannot land on main again.

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
