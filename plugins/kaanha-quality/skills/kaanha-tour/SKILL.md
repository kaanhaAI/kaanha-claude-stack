---
name: kaanha-tour
description: Guided walkthrough of everything the kaanha stack installed and how it fits together. Use when the user asks "what did I just install", "give me the kaanha tour", "how does the kaanha stack / kaanha-quality work", "what do these plugins do", or right after they install or enable a kaanha-stack plugin. NOT for debugging a specific gate failure (explain that directly).
---

# The kaanha tour

Walk the user through their installation in this order, briefly — the
whole tour should read in about two minutes. Ground every claim in what
is actually installed: check the installed-plugin records (e.g.
`~/.claude/plugins/installed_plugins.json` or the plugin list command)
and only present the pieces that are really there.

## 1. What is installed

List which kaanha-stack plugins are present, one line each:

- **kaanha-quality** — the flagship. A deterministic push gate, the
  session mandate, and a ship pipeline (details below).
- **kaanha-dev** (if present) — one registry for every project's dev
  server: unique ports, start/stop/status/logs from anywhere,
  auto-enrollment of new projects.
- **kaanha-ugc** (if present) — creator analytics for video: hook /
  retention / scroll-stop / CTA / best-clip lenses over a video engine
  (watch-skill or claude-video), timestamp-anchored, HTML reports.
- Curated pointers (if present): ponytail, impeccable, ui-ux-pro-max,
  watch-skill, claude-video, and others — each credits its upstream
  author; the stack curates, it does not absorb.

## 2. How kaanha-quality actually works

Explain the loop concretely:

1. **Session mandate** (they have already seen it print): working rules —
   check don't guess, one step at a time, complete what you started, use
   the browser wherever the task needs one — plus the deliverables rule
   (self-contained HTML, updated in place, delivered rendered). Injected
   at SessionStart in every project, always.
2. **Push gate**: a PreToolUse hook watches every shell call. A
   `git push` in a project repo is refused unless the current HEAD
   commit has a recorded ship approval. New commit = approval invalid =
   gate closed again. Dry-runs pass through. User-only escape hatch:
   `KAANHA_GATE=off`.
3. **/ship**: the workflow that opens the gate — kaanha-tester runs the
   project's real checks and fills test gaps, kaanha-verifier does an
   adversarial pre-push review, then the USER approves, and only then
   does the push go out.
4. **Updates**: a daily, silent, privacy-safe version check; when a new
   release exists the session says so with the exact update commands.

Offer to demonstrate the gate: in any git repo, attempt a `git push`
without a ship approval and show the refusal message (nothing is pushed;
the block IS the demo). Skip the demo if they are not in a git repo.

## 3. Where things live

- README (install + per-plugin docs) and CHANGELOG (what each version
  changed): https://github.com/kaanhaAI/kaanha-claude-stack
- Workflow templates they can copy into any repo (site sentinel /
  dependency audit / cloud reasoning / telegram-test):
  `templates/workflows/` in that repo — each file's header says what it
  does and what to fill in.
- Update commands, whenever notified:
  `/plugin marketplace update kaanha-stack` then
  `/plugin update <plugin>@kaanha-stack`.

## 4. Close

End by asking which piece they want to go deeper on, and offer the
gate demo if it was skipped. Do not dump further detail unasked.
