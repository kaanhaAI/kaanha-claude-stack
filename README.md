# kaanha-claude-stack

**One marketplace that turns Claude Code into a self-managing engineering environment** — a hard quality gate in front of every `git push`, one registry for every dev server on your machine, and curated pointers to the best open-source skills.

Built and battle-tested by [Kaanha Tech](https://kaanha.tech) across a multi-project Windows dev machine.

## Install

```
/plugin marketplace add kaanhaAI/kaanha-claude-stack
/plugin install kaanha-quality@kaanha-stack
/plugin install kaanha-dev@kaanha-stack
```

## Original plugins (ours)

### kaanha-quality — verified pushes only

A `git push` is **blocked by a deterministic hook** until the exact HEAD commit has passed the ship workflow:

```
task done → kaanha-tester   (runs your real test/build/lint, fills test gaps)
          → kaanha-verifier (adversarial diff review: fidelity, correctness,
                             call-site regressions, leftovers)
          → fix findings → final commit
          → gate approval stamps that HEAD sha
          → git push passes; any new commit re-locks the gate
```

No model judgment in the gate itself — it's a ~100-line stdlib Python
PreToolUse hook (exit 2 blocks, approval file compared against HEAD).
Works on Bash and PowerShell, fails safe, dry-runs pass through.
User-only escape hatch via `KAANHA_GATE=off`.

### kaanha-dev — one hub for every dev server

Stop juggling ports and per-project configs:

- `registry.json` — every project, every port, one file
- `kaanha_dev.py list | status | start | stop | logs` — from anywhere; detached servers, per-server logs
- `scan` — auto-enrolls new projects with the next free port
- `sync` — generates each project's `.claude/launch.json` so Claude's browser preview works natively
- Windows PATH wrapper included (Claude sessions don't inherit your interactive shell's PATH — this bites everyone eventually)

## Curated pointers (not ours — install straight from their authors)

| Plugin | Author | What it does |
|---|---|---|
| [ponytail](https://github.com/DietrichGebert/ponytail) | Dietrich Gebert | YAGNI persona: the laziest senior dev in the room |
| [impeccable](https://github.com/pbakaus/impeccable) | Paul Bakaus | 23-command design lifecycle + 44 anti-slop detectors |
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | nextlevelbuilder | Offline searchable design database |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | forrestchang | Four principles against classic LLM coding failures |
| [mempalace](https://github.com/MemPalace/mempalace) | MemPalace | Local-first verbatim AI memory |

Also pairs beautifully with [hallmark](https://github.com/Nutlope/hallmark) by Hassan El Mghari (Together AI) — anti-slop page building with structural variety (`npx skills add nutlope/hallmark`).

The marketplace entries for these point at the **upstream repos**, so you always get the authors' latest — full credit to them; this repo just curates and composes.

## The pattern this repo demonstrates

Skills are passive knowledge. The stack becomes autonomous when you add:

1. **Agents** — pair related skills into a worker with a mission and an output contract
2. **Hooks** — deterministic event triggers (session start, pre-push, post-edit)
3. **Schedules** — time triggers that run agents with nobody at the keyboard
4. **Standing reports** — each routine rewrites its own HTML report in place; history lives in git

kaanha-quality and kaanha-dev are working examples of layers 1–2. Compose your own squads on top.

## License

MIT — see [LICENSE](LICENSE).
