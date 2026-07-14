# The push gate & ship workflow (kaanha-quality)

## The idea

"Tests green" and "verified" are different claims. A change can pass its own tests and still be wrong — the tests only check what someone thought to test. kaanha-quality makes the second claim enforceable:

- **`kaanha-tester`** (agent) runs your project's *real* test/build/lint commands, diagnoses failures, and writes missing tests for behavior your change introduced (test files only — it never touches production source).
- **`kaanha-verifier`** (agent) adversarially attacks the diff: does it actually do what was asked? What inputs break it? Which call sites did you forget? Any leftover debug prints or secrets? It only reports findings it verified by reading code, ranked BLOCKER / MAJOR / MINOR.
- **The gate** (deterministic hook) intercepts every `git push` Claude attempts and blocks it unless the exact HEAD commit was approved after those two passed.

## How a push gets approved

Say **"ship it"** (or "push this", "we're done") and the ship workflow runs:

1. **Environment check** — verifies Python 3 is on PATH (refuses to continue if not; the gate can't protect you without it)
2. **Scope** — diffs the change, restates what it's supposed to do
3. **Test** — kaanha-tester runs your real checks; failures caused by the change get fixed
4. **Verify** — kaanha-verifier reviews; BLOCKER/MAJOR findings get fixed and re-verified
5. **Commit + approve** — after the final commit: `python <plugin>/scripts/push_gate.py --approve` stamps that HEAD sha
6. **Push** — the hook compares HEAD to the stamp: match → allowed

## Rules the gate enforces

- **Any new commit invalidates the approval.** Amend after approving → blocked again → re-approve. Nothing sneaks in after verification.
- **Dry runs pass** (`git push --dry-run` is never blocked).
- **Fail-open on environment errors** — if the gate script itself can't run (Python missing, malformed input), it warns and lets the push through rather than bricking you. The *mandate* lives in the ship workflow, which refuses to proceed without Python.
- **The escape hatch is yours, not the model's**: set the environment variable `KAANHA_GATE=off` to bypass the gate for a session. The ship skill is instructed never to suggest it.

## Where the approval lives

`<your-repo>/.git/kaanha-gate` — a one-line file with the approved commit sha. It's inside `.git/`, so it's never committed or pushed. Delete it any time to force re-verification.

## Manual commands

```bash
# approve the current HEAD (normally the ship workflow does this)
python "<plugin-cache>/kaanha-quality/scripts/push_gate.py" --approve

# bypass for one session (your call)
KAANHA_GATE=off git push
```

## Per-repo opt-out

In a repo where the gate shouldn't apply, add to that repo's `.claude/settings.json`:

```json
{ "enabledPlugins": { "kaanha-quality@kaanha-stack": false } }
```
