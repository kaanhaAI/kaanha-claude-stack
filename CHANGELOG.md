# Changelog

All client-visible changes to the kaanha-stack plugins. Update detection in
Claude Code is keyed on each plugin's `version` field — every entry here
corresponds to a version bump you can pull with
`/plugin marketplace update kaanha-stack` + `/plugin update <plugin>@kaanha-stack`
(or automatically, with auto-update enabled for this marketplace).

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
