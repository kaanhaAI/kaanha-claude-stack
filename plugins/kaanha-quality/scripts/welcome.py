#!/usr/bin/env python3
"""kaanha-quality first-session welcome.

SessionStart hook: exactly once per machine, tell the user what the
kaanha stack just gave them and how to learn it. Every later session is
silent (marker file). Same constraints as update_check.py: stdlib only,
ASCII only, any failure exits 0 without a sound - onboarding must never
break a session.
"""
import json
import os
import sys
import time

MARKER = os.path.join(
    os.path.expanduser("~"), ".claude", "plugins", "data",
    "kaanha-quality", "welcomed.json",
)

WELCOME = """\
[kaanha-quality] First session with the kaanha stack. What you now have:
- Push gate: in your project repos, `git push` is blocked until the
  /ship workflow has passed the exact commit (test -> adversarial
  verify -> your explicit approval). Quality is a locked door, not advice.
- Session mandate: the working rules printed above load into every
  session, in every project - no per-project setup.
- /ship skill + kaanha-tester / kaanha-verifier agents run that pipeline.
- Self-notifying updates: when a new version ships you are told
  in-session, with the exact update commands (KAANHA_UPDATE_CHECK=off
  to opt out).
Tell the user this is a one-time notice, and that they can say
"give me the kaanha tour" (or run /kaanha-tour) for a short guided
walkthrough of everything installed and how it fits together.
Docs and changelog: https://github.com/kaanhaAI/kaanha-claude-stack\
"""


def main():
    if os.path.exists(MARKER):
        return
    os.makedirs(os.path.dirname(MARKER), exist_ok=True)
    with open(MARKER, "w") as f:
        json.dump({"welcomed_at": time.time()}, f)
    print(WELCOME)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass  # never surface onboarding failures into a session
    sys.exit(0)
