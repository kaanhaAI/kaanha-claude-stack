#!/usr/bin/env python3
"""kaanha-quality deliverables mandate.

SessionStart hook: injects the house deliverables rule into every session's
context, in every project the plugin is enabled in (globally, by default).
This is what makes the rule ride the marketplace instead of depending on any
per-folder CLAUDE.md or memory: install once, applies everywhere.

Hook protocol: stdout from a SessionStart hook is added to Claude's context.
Keep it short - it loads in every single session.
"""

MANDATE = """\
[kaanha-quality] Deliverables mandate (applies in every project):
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
