# kaanha-agents — templates

These are the config files the squads read. They are NOT active — they are
copied into place once, during fleet bootstrap, and filled in with your
machine's targets.

## Bootstrap (say "set up the fleet" to Claude, or do it by hand)

1. Pick an **ops directory** you control — any repo or folder that stays on
   this machine (the kaanha-marketplace repo's `dev/` is the reference
   location, but any path works).
2. Copy `fleet.json` there and replace every `<...>` placeholder with your
   sites, repos, market, and paths.
3. Copy `builder-backlog.md` to the path you set as `backlog` in
   `fleet.json`, and add your first task.
4. Create the `reports` directory you named in `fleet.json`.
5. Create one scheduled task per squad (see the routines skill's table for
   schedules). Each task's prompt is one line:
   *"Launch the `<agent>` agent from the kaanha-agents plugin and relay its
   summary. It reads `<abs path>/fleet.json` for targets."*
6. Click **Run now** once per task so tool approvals are stored and future
   unattended runs never stall on a permission prompt.

The squads are generic; `fleet.json` is what makes them yours. Add a site
or repo there later and the whole fleet covers it on its next run.
