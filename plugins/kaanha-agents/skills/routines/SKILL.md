---
name: routines
description: The autonomous squad system - how scheduled routines run, where reports live, and the shared report contract. Use when a scheduled task fires, when the user asks about their autonomous agents/routines/reports, or when adding a new squad.
---

# kaanha routines

Eleven squads run on local schedules (while the Claude app is open; missed
runs fire on next launch). Each squad = one agent in this plugin + one
scheduled task + one HTML report it owns.

The original four squads are project-aware by convention; the **fleet
seven** (added 2026-07-15) are fully config-driven: they read their targets
from `dev/fleet.json` at the marketplace repo root (sites, repos, market,
backlog, reports root — each machine's scheduled tasks carry the absolute
path). Add a site or repo to `fleet.json` and every fleet agent covers it
on its next run — nothing in the agents is specific to one website.

| Squad | Agent | Schedule | Report |
|---|---|---|---|
| Code Guardian | code-guardian | nightly 02:00 | docs/reports/code-health.html |
| Daily Ops | daily-ops | daily 08:00 | docs/reports/daily.html |
| Design Warden | design-warden | Mon 09:30 | docs/reports/design.html |
| Growth Marketer | growth-marketer | Fri 15:00 | docs/reports/growth.html |
| Site Sentinel | site-sentinel | every 6h | docs/reports/site-sentinel.html |
| Repo Night-Watch | repo-night-watch | nightly 01:00 | docs/reports/repo-night-watch.html |
| Code Reviewer | code-reviewer | nightly 03:00 | docs/reports/code-review.html |
| Security Auditor | security-auditor | Sun 02:30 | docs/reports/security.html |
| Growth Scout | growth-scout | Wed 10:00 | docs/reports/growth-scout.html |
| Overnight Builder | overnight-builder | nightly 04:00 | docs/reports/overnight-builder.html |
| Flow Tester | flow-tester | nightly 05:00 | docs/reports/flow-test.html |

Division of labour, so squads never duplicate a report: Code Guardian
audits repo HEALTH, Code Reviewer reviews the last-24h DIFF. Growth Scout
RESEARCHES upstream (Wed), Growth Marketer EXECUTES (Fri). Repo
Night-Watch finds advisories nightly, Security Auditor goes deep weekly.
Overnight Builder is the only squad that writes code — one backlog task
per night, on a `builder/*` branch, never pushed. Flow Tester runs after
it and exercises real user flows in a real Chromium (Playwright): the
builder's branch when one exists, otherwise main + production — Site
Sentinel checks that pages RESPOND, Flow Tester checks that flows WORK.

Reports root: `D:\Github\kaanha-marketplace\docs\reports\`
Dashboard: `index.html` there links all reports.

## Bootstrapping the fleet on a new machine

Installing this plugin ships the agents and the config **templates**
(`templates/fleet.json`, `templates/builder-backlog.md` inside the plugin).
Scheduled tasks and the filled-in config are machine-local and created
once. When the user asks to "set up the fleet" (or the tasks are missing):

1. Pick an ops directory the user controls (the reference layout uses the
   kaanha-marketplace repo's `dev/`, but any path works). Copy
   `templates/fleet.json` there as `fleet.json` and fill in the machine's
   sites/repos/market/paths — replace every `<...>` placeholder. Copy
   `templates/builder-backlog.md` to the path set as `backlog`. Create the
   `reports` directory named in the config.
2. Create one scheduled task per squad row in the table above (cron from
   the Schedule column, staggered a few minutes apart if the scheduler
   collides). Each task's prompt is one line: *"Launch the `<agent>` agent
   from the kaanha-agents plugin and relay its run summary. It reads
   `<absolute path>/fleet.json` for targets."* — the absolute path is the
   ONLY machine-specific value, and it lives in the task prompt, never in
   the agent files.
3. Recommend one manual "Run now" per task so tool approvals get stored on
   the task and future runs never stall on permission prompts.

All eleven agents are path-free: they resolve every target through
`fleet.json`. Nothing in `agents/` is specific to one machine or one site.

## Dependencies — works standalone, better together

kaanha-agents runs on its own: every squad names the *doctrine* it applies
and falls back to it when a companion skill isn't installed ("invoke the
X skill if loadable; otherwise apply its doctrine"). It is richer with:

- **kaanha-quality** — squads use its `kaanha-verifier` agent to confirm
  findings before reporting; without it, they self-verify by re-reading
  the code. The Overnight Builder's "never push" guarantee is reinforced
  by kaanha-quality's push gate but does not require it.
- **kaanha-dev** — the dev hub tells squads how each project runs and which
  port its server uses; without it, they detect run commands from the repo.
- **impeccable / seo-audit / tech-debt / code-review** — doctrine sources
  for Design Warden, Growth squads, Code Guardian/Reviewer; all optional.

Requires the scheduled-tasks capability to run unattended (that is what
fires the squads on their cron). Playwright (for flow-tester) and a package
manager (for repo-night-watch) are per-repo, not plugin dependencies.

## Ownership contract (read before adding a target)

The security-auditor and site-sentinel squads probe live sites; several
squads run against repos. Only ever add sites and repos to `fleet.json`
that you **own or have written permission to test**. The squads skip any
target whose ownership is unattested and treat anything that would amount
to testing a third party's infrastructure as out of scope. This is not a
penetration-testing tool for arbitrary targets.

## Report contract (all squads)

1. **Rewrite in place** - same filename every run, never ask permission,
   never create dated copies. History lives in git: after writing, commit
   the master repo (`git add docs/reports && git commit`) so every run is
   diffable.
2. **Self-contained HTML** - inline CSS, light/dark via
   `prefers-color-scheme`, no external requests. Header must show: squad
   name, run timestamp, scope covered, and a one-line verdict.
3. **Honest scope** - if a source was unreachable (connector not
   authorized, repo missing, site down) say so in the report rather than
   silently narrowing scope.
4. **Findings must be verified** before they enter a report - squads use
   the kaanha-verifier agent (from kaanha-quality) or their own
   verification pass; unverified suspicions go in a clearly-marked
   "unconfirmed" section.
5. **No pushes.** Squads commit locally only; the kaanha-quality gate
   still governs any push, and pushes stay human-triggered.

## When a scheduled task fires

The schedule's prompt names one agent. Launch that agent, let it work,
then relay its one-paragraph summary (and whether the report changed
materially) as the run result. If the agent fails, say what failed - do
not fabricate a green run.

## Adding a squad

Agent file in this plugin's `agents/` + report file claimed in the table
above + a scheduled task whose prompt says "launch agent X". Update this
skill's table. Commit the marketplace repo.
