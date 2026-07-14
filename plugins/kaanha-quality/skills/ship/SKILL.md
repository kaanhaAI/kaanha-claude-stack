---
name: ship
description: Verify-and-test-before-push workflow. Use whenever a coding task is complete and work is about to be committed or pushed, or when the user says "push", "ship it", "we're done", "deploy", or asks to finish up. Runs tests, adversarial verification, then approves the push gate.
---

# Ship: verified pushes only

A `git push` in any repo is blocked by the kaanha-gate hook until the
current HEAD has been approved. This skill is the approval path. Follow it
in full - the gate exists so that no step can be silently skipped.

## Workflow

0. **Environment mandate.** Run `python --version` first. If it fails,
   STOP the workflow: tell the user the gate and this pipeline require
   Python 3 on PATH (Windows: `winget install Python.Python.3.12` ·
   macOS: `brew install python` · Linux: `sudo apt install python3`) and
   do not push until it is installed. Without Python the gate fails open
   and unverified pushes would slip through silently - refusing here is
   the mandate.

1. **Scope the change.** `git status` and `git diff` (or
   `git diff main...HEAD` for a branch). Restate in one sentence what this
   change is supposed to do. If mixed unrelated work is staged, tell the
   user before proceeding.

2. **Test.** Launch the `kaanha-tester` agent with the task description and
   the diff scope. It runs the project's real test/build/lint commands,
   diagnoses failures, and adds missing tests for new behavior.
   - FAIL verdict caused by this change: fix the problem, then rerun the
     tester. Do not proceed on a failing suite.
   - PRE-EXISTING failures: report them to the user; they do not block, but
     never hide them.

3. **Verify.** Launch the `kaanha-verifier` agent with the task description
   and diff scope. It adversarially checks task fidelity, correctness,
   regressions at call sites, and leftovers.
   - Fix every BLOCKER and MAJOR finding, then re-run the verifier on the
     new diff. MINOR findings: fix if quick, otherwise list them for the
     user.
   - Run steps 2 and 3 as parallel agents when the diff is small; run the
     tester first when the change is risky enough that a failing suite
     would change what the verifier should look at.

4. **Commit.** Make the final commit (or amend only if the user prefers).
   All fixes from steps 2-3 must be in this commit.

5. **Approve the gate.** After the final commit only:
   `python "${CLAUDE_PLUGIN_ROOT}/scripts/push_gate.py" --approve`
   (Any new commit after approval invalidates it - re-approve after
   amending.)

6. **Push**, then report to the user: what was tested (real commands +
   results), what the verifier found and how it was resolved, and the
   pushed commit hash.

## Rules

- Never run `--approve` without steps 2 and 3 actually having passed in
  this session. The approval is a statement that they did.
- Never suggest KAANHA_GATE=off to route around a failure - that escape
  hatch belongs to the user alone.
- If the repo has no tests at all, the tester will say so; verification
  (step 3) still runs, and you must tell the user the push is going out
  test-less.
- Small docs-only or config-only diffs still get step 3 (a 30-second
  verification), but the tester may be skipped if nothing executable
  changed - say so explicitly when you skip it.
