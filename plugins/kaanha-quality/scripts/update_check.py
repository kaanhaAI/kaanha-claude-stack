#!/usr/bin/env python3
"""kaanha-quality self-notifying update check.

SessionStart hook: compares the installed plugin version against the
latest published version and, when a newer one exists, prints an update
notice into the session so Claude tells the user - no auto-update toggle
or manual polling needed.

Design constraints (in order):
- NEVER break or slow a session: any failure of any kind exits 0 silently;
  the network fetch has a hard 3s timeout.
- At most ONE network request per 24h, cached in
  ~/.claude/plugins/data/kaanha-quality/update_check.json.
- stdlib only, ASCII-only output (same philosophy as the push gate).
- Opt out: set KAANHA_UPDATE_CHECK=off, or delete this hook's line from
  hooks/hooks.json.
- Privacy: the only request is an HTTPS GET of the public plugin manifest
  on raw.githubusercontent.com; nothing about the user or repo is sent.
"""
import json
import os
import sys
import time
import urllib.request

MANIFEST_URL = (
    "https://raw.githubusercontent.com/kaanhaAI/kaanha-claude-stack/"
    "main/plugins/kaanha-quality/.claude-plugin/plugin.json"
)
CHECK_INTERVAL = 24 * 3600  # one fetch per day, max
TIMEOUT = 3  # seconds; a slow network must not slow the session


def parse_version(v):
    return tuple(int(p) for p in str(v).strip().split("."))


def installed_version():
    root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    with open(os.path.join(root, ".claude-plugin", "plugin.json")) as f:
        return json.load(f)["version"]


def cache_path():
    return os.path.join(
        os.path.expanduser("~"), ".claude", "plugins", "data",
        "kaanha-quality", "update_check.json",
    )


def load_cache(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def fetch_latest():
    req = urllib.request.Request(
        MANIFEST_URL, headers={"User-Agent": "kaanha-quality-update-check"}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)["version"]


def main():
    if os.environ.get("KAANHA_UPDATE_CHECK", "").lower() in ("off", "0", "false"):
        return

    local = installed_version()
    path = cache_path()
    cache = load_cache(path)
    now = time.time()

    latest = cache.get("latest")
    if now - cache.get("checked_at", 0) >= CHECK_INTERVAL:
        # Record the attempt BEFORE fetching: a machine that is offline for
        # weeks must not pay the 3s timeout on every single session start.
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"checked_at": now, "latest": latest}, f)
        latest = fetch_latest()
        with open(path, "w") as f:
            json.dump({"checked_at": now, "latest": latest}, f)
    if latest is None:
        return  # nothing known yet (first runs while offline)

    if parse_version(latest) > parse_version(local):
        print(
            "[kaanha-quality] Update available: {latest} (installed {local}).\n"
            "Tell the user a kaanha-quality update is available and that they\n"
            "can get it by running:\n"
            "  /plugin marketplace update kaanha-stack\n"
            "  /plugin update kaanha-quality@kaanha-stack".format(
                latest=latest, local=local
            )
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # a broken update check must never surface into a session
    sys.exit(0)
