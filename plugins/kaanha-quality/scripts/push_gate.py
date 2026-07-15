#!/usr/bin/env python3
"""kaanha-quality push gate.

PreToolUse hook: blocks `git push` unless the current HEAD commit has been
approved by the ship workflow (tests run + verification done).

Approval marker: <git-dir>/kaanha-gate containing the approved HEAD sha.
Approve with:   python push_gate.py --approve   (run from the repo, after
                tests and verification pass, after the final commit)
Bypass:         set environment variable KAANHA_GATE=off for the session.

Hook protocol: exit 0 = allow, exit 2 = block (stderr is shown to Claude).
"""
import json
import os
import re
import subprocess
import sys


def git(args, cwd):
    return subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=15
    )


def gate_path(cwd):
    r = git(["rev-parse", "--git-dir"], cwd)
    if r.returncode != 0:
        return None
    git_dir = r.stdout.strip()
    if not os.path.isabs(git_dir):
        git_dir = os.path.join(cwd, git_dir)
    return os.path.join(git_dir, "kaanha-gate")


def head_sha(cwd):
    r = git(["rev-parse", "HEAD"], cwd)
    return r.stdout.strip() if r.returncode == 0 else None


def approve():
    cwd = os.getcwd()
    path = gate_path(cwd)
    sha = head_sha(cwd)
    if not path or not sha:
        print("kaanha-gate: not a git repository (or no commits yet)", file=sys.stderr)
        return 1
    with open(path, "w") as f:
        f.write(sha + "\n")
    print(f"kaanha-gate: approved {sha[:12]} for push")
    return 0


def main():
    if "--approve" in sys.argv:
        sys.exit(approve())

    if os.environ.get("KAANHA_GATE", "").lower() in ("off", "0", "skip"):
        sys.exit(0)

    try:
        # lstrip BOM: Windows shells (PowerShell pipes) prepend U+FEFF,
        # and a gate that fails open on parse errors must not be that
        # easy to trip. Real hook payloads are clean UTF-8 either way.
        payload = json.loads(sys.stdin.read().lstrip("\ufeff"))
    except Exception:
        sys.exit(0)  # malformed input: never break unrelated tool calls

    command = (payload.get("tool_input") or {}).get("command", "") or ""
    # Only gate real pushes; ignore dry runs.
    if not re.search(r"\bgit\b[^\n|;&]*\bpush\b", command):
        sys.exit(0)
    if "--dry-run" in command:
        sys.exit(0)

    cwd = payload.get("cwd") or os.getcwd()
    if not os.path.isdir(cwd):
        cwd = os.getcwd()
    try:
        path = gate_path(cwd)
        sha = head_sha(cwd)
    except Exception as e:
        print(f"kaanha-gate: internal error, allowing push ({e})", file=sys.stderr)
        sys.exit(0)
    if not path or not sha:
        sys.exit(0)  # not a repo; nothing to gate

    approved = None
    if os.path.isfile(path):
        with open(path) as f:
            approved = f.read().strip()

    if approved == sha:
        sys.exit(0)

    print(
        "kaanha-gate BLOCKED this push: HEAD "
        f"{sha[:12]} has not passed the ship workflow.\n"
        "Required before pushing:\n"
        "  1. Run the project's tests/build and make sure they pass.\n"
        "  2. Run the kaanha-verifier agent on the diff being pushed and "
        "resolve real findings.\n"
        "  3. After the FINAL commit, approve: python "
        '"${CLAUDE_PLUGIN_ROOT}/scripts/push_gate.py" --approve\n'
        "(User-only escape hatch: KAANHA_GATE=off environment variable.)",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
