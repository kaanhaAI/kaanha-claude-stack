#!/usr/bin/env python3
"""PostToolUse (Edit/Write/MultiEdit): remember which CODE files changed this
turn, for the end-of-turn auto-review checkpoint (auto_review_stop.py).

Cheap and silent: it only appends a path to a per-session manifest. No agent
runs here. Fail-open and stdlib-only - a bug here must never disturb a session.

Off switch: KAANHA_AUTO_REVIEW=off (also skips the checkpoint).
"""
import json
import os
import sys
import tempfile

CODE_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".go", ".rs", ".java",
    ".rb", ".php", ".svelte", ".vue", ".cs", ".cpp", ".cc", ".c", ".h", ".hpp",
    ".kt", ".swift", ".scala", ".sql", ".sh", ".ps1", ".lua", ".dart", ".ex",
}


def off():
    return os.environ.get("KAANHA_AUTO_REVIEW", "").lower() in ("off", "0", "false", "no")


def manifest_path(session_id):
    d = os.path.join(tempfile.gettempdir(), "kaanha-auto-review")
    os.makedirs(d, exist_ok=True)
    sid = "".join(c for c in (session_id or "default") if c.isalnum() or c in "-_")[:64]
    return os.path.join(d, f"{sid or 'default'}.files")


def main():
    if off():
        return
    data = json.load(sys.stdin)
    fp = (data.get("tool_input") or {}).get("file_path")
    if not fp:
        return
    if os.path.splitext(fp)[1].lower() not in CODE_EXT:
        return  # only code files earn a review; docs/config do not
    low = fp.replace("\\", "/").lower()
    if any(skip in low for skip in ("/agent-memory/", "/.git/", "/node_modules/", "/.claude/")):
        return
    with open(manifest_path(data.get("session_id")), "a", encoding="utf-8") as f:
        f.write(fp + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # fail open: never break a session over a review nudge
    sys.exit(0)
