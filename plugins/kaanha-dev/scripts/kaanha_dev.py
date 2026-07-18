#!/usr/bin/env python3
"""kaanha dev hub - one launcher for every project's dev server.

Portable: this script is bundled in the kaanha-dev plugin and resolves its
config + state from a machine-local HOME, so it works on ANY machine from a
one-command install - not just the repo it was authored in.

  KAANHA_HOME env var           -> use that directory as the ops home
  else ~/.claude/kaanha         -> default; created + bootstrapped on first run

The home holds registry.json (projects + ports, single source of truth),
fleet.json (24/7 squad targets), plus .state/ and logs/. On first run the
home is bootstrapped from this plugin's templates/.

Commands:
  list                 show all registered projects
  status               which servers are up (pid + port probe)
  start <name> [...]   start one or more servers (detached, logged)
  stop <name|all>      stop server(s) started by this hub
  logs <name> [-n N]   tail a server's log
  sync                 write each project's .claude/launch.json from the registry
  scan                 auto-enroll new projects; also reconciles fleet targets
  fleet                point the 24/7 squads at every enrolled project

Stdlib only. State: <home>/.state/<name>.pid   Logs: <home>/logs/<name>.log
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import time

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(PLUGIN_ROOT, "templates")


def config_home():
    """The machine-local ops home. KAANHA_HOME wins; else ~/.claude/kaanha.

    A client who installed via one command has no marketplace checkout, so
    the home cannot be 'the repo'. This machine keeps its existing dev/ layout
    by setting KAANHA_HOME to it - zero migration.
    """
    h = os.environ.get("KAANHA_HOME")
    if h:
        return os.path.abspath(os.path.expanduser(h))
    return os.path.join(os.path.expanduser("~"), ".claude", "kaanha")


HOME = config_home()
STATE = os.path.join(HOME, ".state")
LOGS = os.path.join(HOME, "logs")
REG_PATH = os.path.join(HOME, "registry.json")
FLEET_PATH = os.path.join(HOME, "fleet.json")
WRAPPER = os.path.join(HOME, "withnode.cmd")  # optional; plain tool if absent
PORT_POOL_START = 3010  # auto-enrolled projects get ports from here up


def bootstrap():
    """Create the ops home + seed config from templates on first run.

    Idempotent: only writes files that are missing, never clobbers a real
    registry/fleet. Silent unless it actually created something.
    """
    created = []
    os.makedirs(HOME, exist_ok=True)
    if not os.path.isfile(REG_PATH):
        seed = os.path.join(TEMPLATES, "registry.json")
        if os.path.isfile(seed):
            shutil.copyfile(seed, REG_PATH)
        else:
            with open(REG_PATH, "w", encoding="utf-8") as f:
                json.dump({"projectsRoot": None, "projects": [], "ignore": []}, f, indent=2)
        created.append("registry.json")
    if not os.path.isfile(FLEET_PATH):
        seed = os.path.join(TEMPLATES, "fleet.json")
        if os.path.isfile(seed):
            shutil.copyfile(seed, FLEET_PATH)
            # point reports at this home so squads write somewhere real
            reports = os.path.join(HOME, "reports")
            os.makedirs(reports, exist_ok=True)
            try:
                with open(FLEET_PATH, encoding="utf-8") as f:
                    fleet = json.load(f)
                if not fleet.get("reports"):
                    fleet["reports"] = reports
                    with open(FLEET_PATH, "w", encoding="utf-8") as f:
                        json.dump(fleet, f, indent=1)
            except Exception:
                pass
            created.append("fleet.json")
    return created


def load_registry():
    with open(REG_PATH, encoding="utf-8") as f:
        return json.load(f)


def registry():
    return list(load_registry().get("projects", []))


def by_name(name):
    for p in registry():
        if p["name"] == name:
            return p
    sys.exit(f"unknown project: {name} (try: list)")


def port_open(port):
    if not port:
        return False
    with socket.socket() as s:
        s.settimeout(0.4)
        return s.connect_ex(("127.0.0.1", port)) == 0


def pid_alive(pid):
    if os.name == "nt":
        r = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            capture_output=True, text=True,
        )
        return str(pid) in r.stdout
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def saved_pid(name):
    path = os.path.join(STATE, f"{name}.pid")
    if os.path.isfile(path):
        try:
            return int(open(path).read().strip())
        except ValueError:
            return None
    return None


def cmd_list():
    for p in registry():
        port = p.get("port") or "-"
        print(f"{p['name']:<14} port={port!s:<6} {p['path']}  ({p.get('note','')})")


def cmd_status():
    for p in registry():
        pid = saved_pid(p["name"])
        alive = pid is not None and pid_alive(pid)
        up = port_open(p.get("port"))
        state = "RUNNING" if (alive or up) else "stopped"
        extra = f"pid={pid}" if alive else ("port responds (started elsewhere)" if up else "")
        print(f"{p['name']:<14} {state:<8} {extra}")


def cmd_start(names):
    os.makedirs(STATE, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)
    for name in names:
        p = by_name(name)
        if port_open(p.get("port")):
            print(f"{name}: already responding on port {p['port']} - skipping")
            continue
        if not os.path.isdir(p["path"]):
            print(f"{name}: path missing: {p['path']} - skipping")
            continue
        env = {**os.environ, **p.get("env", {})}
        log = open(os.path.join(LOGS, f"{name}.log"), "a", encoding="utf-8")
        kwargs = dict(cwd=p["path"], env=env, stdout=log, stderr=subprocess.STDOUT,
                      stdin=subprocess.DEVNULL)
        cmd = [p["runtimeExecutable"]] + p["runtimeArgs"]
        if os.name == "nt":
            kwargs["creationflags"] = (
                subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
            )
            kwargs["shell"] = True  # resolves npm.cmd/pnpm.cmd shims
            cmd = subprocess.list2cmdline(cmd)
        proc = subprocess.Popen(cmd, **kwargs)
        with open(os.path.join(STATE, f"{name}.pid"), "w") as f:
            f.write(str(proc.pid))
        port = f"http://localhost:{p['port']}" if p.get("port") else "(see log for port)"
        print(f"{name}: started pid={proc.pid} -> {port}  log: {LOGS}\\{name}.log")


def cmd_stop(names):
    if names == ["all"]:
        names = [p["name"] for p in registry() if saved_pid(p["name"])]
        if not names:
            print("nothing started by the hub")
            return
    for name in names:
        by_name(name)  # validate
        pid = saved_pid(name)
        if pid is None or not pid_alive(pid):
            print(f"{name}: not running (or not started by the hub)")
        else:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                               capture_output=True)
            else:
                os.kill(pid, 15)
            print(f"{name}: stopped (pid {pid})")
        path = os.path.join(STATE, f"{name}.pid")
        if os.path.isfile(path):
            os.remove(path)


def cmd_logs(name, n=40):
    path = os.path.join(LOGS, f"{name}.log")
    if not os.path.isfile(path):
        sys.exit(f"no log yet for {name}")
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f.readlines()[-n:]:
            print(line.rstrip())


def cmd_sync():
    # group registry entries by project path: one launch.json may hold
    # several configurations (e.g. web app + db studio)
    grouped = {}
    for p in registry():
        grouped.setdefault(os.path.normcase(p["path"]), []).append(p)
    for entries in grouped.values():
        path = entries[0]["path"]
        if not os.path.isdir(path):
            print(f"{entries[0]['name']}: path missing, skipped")
            continue
        launch = {
            "version": "0.0.1",
            "configurations": [{
                "name": p["name"],
                "runtimeExecutable": p["runtimeExecutable"],
                "runtimeArgs": p["runtimeArgs"],
                **({"port": p["port"]} if p.get("port") else {}),
                **({"env": p["env"]} if p.get("env") else {}),
            } for p in entries],
        }
        target_dir = os.path.join(path, ".claude")
        os.makedirs(target_dir, exist_ok=True)
        target = os.path.join(target_dir, "launch.json")
        with open(target, "w", encoding="utf-8") as f:
            json.dump(launch, f, indent=2)
        names = ", ".join(p["name"] for p in entries)
        print(f"{names}: wrote {target}")


def cmd_scan(quiet=False):
    """Auto-enroll: register any new project (under projectsRoot) with a dev script."""
    data = load_registry()
    projects_root = data.get("projectsRoot")
    if not projects_root or not os.path.isdir(projects_root):
        if not quiet:
            print("scan: projectsRoot is not set to a real directory in registry.json - "
                  "set it to where your repos live, then re-run.")
        sync_fleet_targets(quiet=quiet)  # still reconcile whatever is registered
        return
    known = {os.path.normcase(p["path"]) for p in data["projects"]}
    ignore = {n.lower() for n in data.get("ignore", [])}
    used = {p["port"] for p in data["projects"] if p.get("port")}
    runtime = WRAPPER if os.path.isfile(WRAPPER) else None

    def next_port():
        port = PORT_POOL_START
        while port in used:
            port += 1
        used.add(port)
        return port

    added = []
    for entry in sorted(os.listdir(projects_root)):
        path = os.path.join(projects_root, entry)
        pkg = os.path.join(path, "package.json")
        if entry.lower() in ignore:
            continue
        if os.path.normcase(path) in known or not os.path.isfile(pkg):
            continue
        try:
            with open(pkg, encoding="utf-8") as f:
                scripts = json.load(f).get("scripts", {})
        except Exception:
            continue
        if not scripts.get("dev"):
            continue
        tool = "pnpm" if os.path.isfile(os.path.join(path, "pnpm-lock.yaml")) else "npm"
        port = next_port()
        name = entry.lower().replace(".", "-").replace(" ", "-")
        data["projects"].append({
            "name": name,
            "path": path,
            "runtimeExecutable": runtime or tool,
            "runtimeArgs": ([tool, "run", "dev"] if runtime else ["run", "dev"]),
            "port": port,
            "env": {"PORT": str(port)},
            "note": f"auto-enrolled by scan; verify port wiring (dev: {scripts['dev'][:50]})",
        })
        added.append(f"{name} -> port {port}")

    if added:
        with open(REG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        cmd_sync()
        print("scan: enrolled " + ", ".join(added))
        print("scan: review the new entries in registry.json (port flags for "
              "Next/Vite may need -p/--port args).")
    elif not quiet:
        print("scan: no new projects found")
    # every scan also reconciles the fleet: any registry project not yet a
    # fleet target gets added, so a new repo is covered by BOTH the dev hub
    # and the 24/7 squads from the moment it is enrolled.
    sync_fleet_targets(quiet=quiet)
    # surface fresh fleet reports so they are not invisible from a project
    fresh_reports_notice()


def sync_fleet_targets(quiet=False):
    """Make the 24/7 fleet cover every enrolled project automatically.

    The fleet squads read fleet.json -> repos[]. Hand-maintained, that list
    drifts: the dev hub auto-enrolls new projects into registry.json, but the
    fleet never hears about them, so squads silently skip repos that ARE on
    this machine. This derives repos[] from the registry (the single source of
    truth), so dev-hub enrollment IS fleet enrollment - one scan, every project
    covered, no hand editing ever.

    Non-destructive: a repo already in fleet.json is kept even when it is not a
    registry project (e.g. the marketplace repo itself). Only real dirs count.
    """
    if not os.path.isfile(FLEET_PATH):
        return []
    reg = load_registry()
    with open(FLEET_PATH, encoding="utf-8") as f:
        fleet = json.load(f)

    ignore = {n.lower() for n in reg.get("ignore", [])}
    seen, repos = set(), []

    def add(path):
        if not path or not os.path.isdir(path):
            return
        key = os.path.normcase(os.path.abspath(path))
        if key in seen:
            return
        seen.add(key)
        repos.append(path)

    for p in fleet.get("repos", []):
        add(p)
    for p in reg.get("projects", []):
        if os.path.basename(p.get("path", "")).lower() in ignore:
            continue
        add(p.get("path"))

    before = {os.path.normcase(os.path.abspath(x)) for x in fleet.get("repos", [])}
    added = [r for r in repos if os.path.normcase(os.path.abspath(r)) not in before]
    if added:
        fleet["repos"] = repos
        with open(FLEET_PATH, "w", encoding="utf-8") as f:
            json.dump(fleet, f, indent=1)
        if not quiet:
            print("fleet: now covering " + ", ".join(os.path.basename(r) for r in added))
    return added


def fresh_reports_notice():
    """One-line SessionStart pointer to fleet reports written in the last day.

    The squads write into the ops home's reports folder - which a project
    session never opens, so their output stays invisible (gap 2 of the fleet
    audit). This surfaces it: on every session it names any report touched in
    the last 24h and points at the dashboard, even under --quiet. Fail-silent
    and silent when nothing is fresh.
    """
    if not os.path.isfile(FLEET_PATH):
        return
    try:
        with open(FLEET_PATH, encoding="utf-8") as f:
            reports = json.load(f).get("reports")
    except Exception:
        return
    if not reports or not os.path.isdir(reports):
        return
    cutoff = time.time() - 24 * 3600
    fresh = []
    for name in sorted(os.listdir(reports)):
        if not name.endswith(".html") or name == "index.html":
            continue
        try:
            if os.path.getmtime(os.path.join(reports, name)) >= cutoff:
                fresh.append(name)
        except OSError:
            continue
    if fresh:
        dash = os.path.join(reports, "index.html")
        print(f"fleet: {len(fresh)} report(s) updated in the last 24h "
              f"({', '.join(fresh)}) - dashboard: {dash}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    bootstrap()
    cmd, rest = args[0], args[1:]
    if cmd == "list":
        cmd_list()
    elif cmd == "status":
        cmd_status()
    elif cmd == "start" and rest:
        cmd_start(rest)
    elif cmd == "stop" and rest:
        cmd_stop(rest)
    elif cmd == "logs" and rest:
        n = int(rest[rest.index("-n") + 1]) if "-n" in rest else 40
        cmd_logs(rest[0], n)
    elif cmd == "sync":
        cmd_sync()
    elif cmd == "scan":
        cmd_scan(quiet="--quiet" in rest)
    elif cmd == "fleet":
        added = sync_fleet_targets()
        if not added:
            print("fleet: already covering every enrolled project")
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
