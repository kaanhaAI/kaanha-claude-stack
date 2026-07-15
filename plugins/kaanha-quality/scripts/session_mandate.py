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
