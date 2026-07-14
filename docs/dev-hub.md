# The dev hub (kaanha-dev)

One registry for every dev server on your machine. Each project gets a permanently assigned port, so five Next.js apps stop fighting over 3000 — and Claude knows how to start, stop, and check any of them from any session.

## One-time setup (~2 minutes)

The plugin ships samples; you create your real config next to them (Claude can do all of this for you — just ask it to "set up the dev hub"):

1. Find the plugin's scripts directory (ask Claude, or look under `~/.claude/plugins/cache/.../kaanha-dev/scripts/`). You can also copy the `scripts/` folder somewhere permanent like `~/dev-hub/` — the launcher is self-contained.
2. Copy `registry.sample.json` → `registry.json` and edit:
   - `projectsRoot` — the folder that holds your repos (used by `scan`)
   - `projects` — one entry per dev server: name, path, command, **unique port**
   - `ignore` — folders scan should skip (forks, archives)
3. **Windows only:** copy `withnode.sample.cmd` → `withnode.cmd` and set your Node directory. Claude sessions don't inherit your interactive shell's PATH, so registry entries route through this wrapper: `"runtimeExecutable": "<path>\\withnode.cmd"`, `"runtimeArgs": ["npm", "run", "dev"]`.
4. Run `python kaanha_dev.py sync` — generates each project's `.claude/launch.json` so Claude Code's browser preview works natively.

## Commands (run from anywhere)

```
python kaanha_dev.py list              # all projects + ports
python kaanha_dev.py status            # what's running right now
python kaanha_dev.py start <name> ...  # start one or more (detached, logged)
python kaanha_dev.py stop <name|all>   # stop hub-started servers
python kaanha_dev.py logs <name> [-n N]
python kaanha_dev.py scan              # auto-enroll new projects found in projectsRoot
python kaanha_dev.py sync              # regenerate every launch.json from the registry
```

Servers start **detached** — they survive the Claude session ending — and log to `logs/<name>.log` next to the script.

## Assigning ports

- **Vite/SvelteKit**: default 5173 is fine if only one app uses it
- **Next.js**: pin with args — `"runtimeArgs": ["run", "dev", "--", "-p", "3001"]`
- **Node/Express or anything reading `PORT`**: set `"env": {"PORT": "3005"}` — the hub injects it, and `sync` writes it into launch.json too
- Two entries can share a `path` (e.g. an app plus its DB studio) — `sync` merges them into one launch.json

## How Claude uses it

The `dev-hub` skill teaches every session the rules: check `status` before starting anything, prefer the project's launch.json for previews of the *current* project, use hub `start` for other projects or several at once, and fix port conflicts in the registry (then `sync`) instead of improvising.
