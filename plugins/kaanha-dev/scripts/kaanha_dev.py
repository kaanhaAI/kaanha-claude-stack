#!/usr/bin/env python3
"""kaanha dev hub - one launcher for every project's dev server.

Registry: dev/registry.json (single source of truth, unique ports).

Commands:
  list                 show all registered projects
  status               which servers are up (pid + port probe)
  start <name> [...]   start one or more servers (detached, logged)
  stop <name|all>      stop server(s) started by this hub
  logs <name> [-n N]   tail a server's log
  sync                 write each project's .claude/launch.json from the registry

Stdlib only. State: dev/.state/<name>.pid  Logs: dev/logs/<name>.log
"""
import json
import os
import socket
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, ".state")
LOGS = os.path.join(HERE, "logs")


def registry():
    with open(os.path.join(HERE, "registry.json"), encoding="utf-8") as f:
        return [p for p in json.load(f)["projects"]]


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
        print(f"{name}: started pid={proc.pid} -> {port}  log: dev/logs/{name}.log")


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


WRAPPER = os.path.join(HERE, "withnode.cmd")
PORT_POOL_START = 3010  # auto-enrolled projects get ports from here up


def cmd_scan(quiet=False):
    """Auto-enroll: register any new project (under projectsRoot) with a dev script."""
    reg_path = os.path.join(HERE, "registry.json")
    with open(reg_path, encoding="utf-8") as f:
        data = json.load(f)
    projects_root = data.get("projectsRoot", r"D:\Github")
    known = {os.path.normcase(p["path"]) for p in data["projects"]}
    ignore = {n.lower() for n in data.get("ignore", [])}
    used = {p["port"] for p in data["projects"] if p.get("port")}

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
            "runtimeExecutable": WRAPPER,
            "runtimeArgs": [tool, "run", "dev"],
            "port": port,
            "env": {"PORT": str(port)},
            "note": f"auto-enrolled by scan; verify port wiring (dev: {scripts['dev'][:50]})",
        })
        added.append(f"{name} -> port {port}")

    if added:
        with open(reg_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        cmd_sync()
        print("scan: enrolled " + ", ".join(added))
        print("scan: review the new entries in dev/registry.json (port flags for "
              "Next/Vite may need -p/--port args) and commit the marketplace repo.")
    elif not quiet:
        print("scan: no new projects found")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
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
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
