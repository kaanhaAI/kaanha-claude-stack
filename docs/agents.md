# Autonomous squads (kaanha-agents)

Eleven unattended agents that run on a local schedule, do one focused job,
and rewrite a self-contained HTML report. This page is the honest brief —
**read it before you install.**

## What it actually does to your machine

Installing the plugin ships the agent definitions and config templates.
Nothing runs until you bootstrap. Once you do, and while the Claude app is
open, these agents:

- **create scheduled tasks** that fire on a cron (from every 6 hours to
  weekly);
- **launch a real Chromium** (the flow-tester runs Playwright end-to-end);
- **make local git commits** to your reports directory (they **never
  `git push`** and never touch `main` in your code repos);
- **write to a `builder/*` branch** (the overnight-builder builds one
  backlog task per night, on its own branch, for you to review);
- **send one gentle HTTP probe** per endpoint to sites you list (uptime +
  defensive security checks).

They are read-only toward your source code (except the overnight-builder,
which only ever works on its own branch) and read-only toward production.

## Ownership — the one hard rule

The `site-sentinel` and `security-auditor` squads probe the sites in your
config. **Only add sites and repos you own or have written permission to
test.** The agents skip any target whose ownership you haven't attested and
treat anything that would amount to testing a third party's infrastructure
as out of scope. This is a defensive tool for your own systems, not a
scanner for arbitrary targets.

## The eleven squads

| Squad | Schedule | Job |
|---|---|---|
| code-guardian | nightly | repo health: security, correctness, tech debt |
| daily-ops | daily | morning briefing from your connectors + git |
| design-warden | weekly | frontend anti-slop + accessibility + brand |
| growth-marketer | weekly | SEO health + competitive scan (execution) |
| site-sentinel | every 6h | uptime + route + endpoint health |
| repo-night-watch | nightly | dependency + advisory audit |
| code-reviewer | nightly | reviews the last 24h of commits |
| security-auditor | weekly | defensive audit of **your own** assets |
| growth-scout | weekly | market/competitor/SEO research (upstream) |
| overnight-builder | nightly | builds one backlog task on a `builder/*` branch |
| flow-tester | nightly | Playwright e2e in a real browser |

## Setup

1. Install:
   ```
   /plugin marketplace add kaanhaAI/kaanha-claude-stack
   /plugin install kaanha-agents@kaanha-stack
   ```
2. Say **"set up the fleet"** to Claude. It copies the bundled
   `fleet.json` template, walks you through filling in your sites, repos,
   market, and paths, creates the scheduled tasks, and points you at a
   "Run now" for each so tool approvals get stored.
3. Add your first task to `builder-backlog.md` if you want the
   overnight-builder to build something tonight.

## Works standalone, better together

Every squad names the *doctrine* it applies and falls back to it when a
companion isn't installed. It is richer with **kaanha-quality** (verified
findings + the push gate reinforcing "never push"), **kaanha-dev** (the dev
hub tells squads how each project runs), and design/SEO skills like
impeccable and seo-audit. None are required.

## Requirements & honesty

- Runs **while the Claude app is open**; missed runs fire on next launch.
  This is not a cloud service — it is not literally 24/7 unless your
  machine and the app stay on.
- The scheduled-tasks capability must be available for unattended runs.
- Playwright (flow-tester) and a package manager (repo-night-watch) are
  per-repo tools, installed in your repos, not by this plugin.
- This is a young system. Treat the first week as a shakedown: watch each
  squad's first run, read its report, and tune the config before you rely
  on it.

## Stopping them

Disable or delete any task from the Scheduled panel in the Claude app.
Nothing persists beyond the scheduled tasks you created and the reports
directory you named.
