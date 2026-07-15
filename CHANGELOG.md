# Changelog

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
