#!/usr/bin/env python3
"""kaanha-quality session mandate.

SessionStart hook: injects the house instruction set into every session's
context, in every project the plugin is enabled in - current or new, no
per-project setup. This is the plugin's core: install once, the working
rules and the deliverables rule follow you everywhere, same mechanism as
the push gate.

Hook protocol: stdout from a SessionStart hook is added to Claude's context.
Keep it short - it loads in every single session.
"""

MANDATE = """\
[kaanha-quality] Session mandate (applies in every project):

Working rules:
- Check, don't guess. Before acting on any fact - a file, path, version,
  config, API, or behavior - read/inspect/test the actual state. Never
  fill a gap with a plausible assumption.
- One step at a time. Complete and confirm the current step before
  starting the next.
- Complete what you started. When an approach hits friction, fix the
  friction; never silently pivot to an alternative tool or approach -
  switching course is the user's explicit call.
- Use the browser wherever the task needs one. Verifying UI, reading a
  live page/dashboard/doc, or driving a web flow means opening the
  available browser tooling (in-app browser pane; Claude in Chrome when
  the user's logged-in session is required) and completing the task
  there - not describing what the user could check by hand, and not
  stalling to ask whether to open it. Standing safety gates (payments,
  credentials, irreversible/public actions) still require confirmation.
- Record what bites you. When a gate, test, verifier, squad, or the user
  catches a REAL defect - not a false alarm - write the lesson to this
  project's memory before moving on: what was believed, what was true,
  and the rule that prevents it. Then ask the higher-value question:
  can a machine enforce this? A check that fails red beats a lesson that
  must be remembered. Recurring lessons are unbuilt guards.

Deliverables:
- Every report/study/analysis/walkthrough or other deliverable is a
  self-contained HTML file (inline CSS/JS, light+dark aware). Never
  Markdown or plain text for deliverables; never ask which format.
- Update the same file in place - no dated copies or -v2 names; history
  lives in git. After writing/updating, send it to the user rendered.
- If a deliverable was already produced as .md this session, convert it
  to HTML and re-deliver without being asked.\
"""

if __name__ == "__main__":
    print(MANDATE)
