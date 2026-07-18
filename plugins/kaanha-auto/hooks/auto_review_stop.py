#!/usr/bin/env python3
"""Stop (turn ends): if code files changed this turn, block ONCE and tell the
main session to run the relevant kaanha-auto reviewers on them before finishing.

This is the "auto-fire" mechanism. A hook cannot spawn a subagent directly, so
it returns a blocking decision whose reason instructs the model to invoke the
agents itself - the model acts on it, reviews, applies blocker fixes, then stops.

Loop-safe: `stop_hook_active` is true once we have already blocked this turn, so
the second stop attempt passes through (the review's own edits are not
re-reviewed in the same turn). Fail-open and stdlib-only: any error lets the
turn end normally - an on-by-default global hook must never wedge a session.

Off switch: KAANHA_AUTO_REVIEW=off
"""
import json
import os
import sys
import tempfile

# paths that make the change security/compliance relevant -> add that reviewer
SENSITIVE = (
    "auth", "login", "session", "webhook", "billing", "payment", "credential",
    "token", "secret", "privacy", "consent", "gdpr", "/api/", "oauth", "password",
    "encrypt", "permission",
)


def off():
    return os.environ.get("KAANHA_AUTO_REVIEW", "").lower() in ("off", "0", "false", "no")


def manifest_path(session_id):
    d = os.path.join(tempfile.gettempdir(), "kaanha-auto-review")
    sid = "".join(c for c in (session_id or "default") if c.isalnum() or c in "-_")[:64]
    return os.path.join(d, f"{sid or 'default'}.files")


def discard(path):
    try:
        os.remove(path)
    except OSError:
        pass


def main():
    if off():
        return
    data = json.load(sys.stdin)
    mp = manifest_path(data.get("session_id"))

    # Loop guard: we already blocked once this turn. Let it stop now, and reset
    # so the reviewers' own fix-edits are not re-reviewed in the same turn.
    if data.get("stop_hook_active"):
        discard(mp)
        return

    if not os.path.isfile(mp):
        return
    try:
        with open(mp, encoding="utf-8") as f:
            files = [ln.strip() for ln in f if ln.strip()]
    except OSError:
        return

    seen = set()
    files = [x for x in files if not (x in seen or seen.add(x))]
    discard(mp)  # consume now, so the review round does not re-trigger
    if not files:
        return

    agents = ["code-reviewer"]
    blob = " ".join(files).lower()
    if any(s in blob for s in SENSITIVE):
        agents.append("compliance-reviewer")
    if len(files) >= 3:
        agents.append("architecture-reviewer")

    flist = "\n".join("  - " + x for x in files[:25])
    alist = ", ".join(f"kaanha-auto:{a}" for a in agents)
    reason = (
        "Auto-review (kaanha-auto): code changed this turn:\n"
        f"{flist}\n\n"
        f"Before finishing, invoke {alist} on these files (in parallel is fine), "
        "apply any blocker-level fixes they surface, and give a one-line verdict "
        "per reviewer. Then stop. Disable this checkpoint with KAANHA_AUTO_REVIEW=off."
    )
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # fail open
    sys.exit(0)
