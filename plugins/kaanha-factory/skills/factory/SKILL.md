---
name: factory
description: Full product lifecycle for NEW products or major features - "build me an app/SaaS/bot/API/extension/tool from scratch" or "add a major new capability". NOT for bug fixes, small changes, or questions (handle those directly - ponytail rules apply). Runs discovery through deployment, scaled to project size.
---

# kaanha factory

Treat a greenfield request as a product, not a snippet - but scale the
process to the ask. Ponytail's laziness doctrine governs code WITHIN
phases; this skill governs which phases exist. The two never fight:
factory decides *what must be true before shipping*, ponytail decides
*how little code achieves it*.

## Step 0 - Restate the goal, then classify size (say both out loud)

Before classifying, restate the request as the underlying GOAL in one
sentence ("you asked for X; the goal is Y"). Scope against the goal, not
the phrasing - but the goal statement is for aim, never a license to
expand scope past what was asked.

- **S** - single feature, one repo, days of work. Phases: 1, 3, 5, 6.
- **M** - full product MVP (app, bot, API, extension). Phases: 1-7.
- **L** - multi-service platform or client production system. All phases,
  and propose the plan to the user BEFORE building.

If the request is a bug fix, small change, or question: this skill does
not apply - say nothing about it and just do the work.

## The phases (each delegates to enforced machinery)

1. **Discovery & requirements** - one document, not ten: problem, users,
   success metric, constraints, non-goals, and testable acceptance
   criteria. Ask the user only what cannot be inferred; state assumptions
   explicitly and proceed.
2. **Research** (M/L) - use the deep-research skill for market/competitor
   scan; technical research inline. Deliver a short recommendation with
   trade-offs, not a survey.
3. **Architecture** - stack choice, data model, integration points,
   deployment target. For UI products, generate the design system NOW,
   routing to the right design skill by need (they do NOT overlap):
     - **ui-ux-pro-max** - reference database: palettes, font pairings,
       styles, stack guidelines. Persist the choices in MASTER.md.
     - **impeccable** - anti-slop detectors + design critique on what
       gets built.
     - **hallmark** - page macrostructure / anti-slop page building
       (where enabled; it is per-project, not global).
     - **kaanha-3d-web** - the specialist for premium / cinematic / 3D
       / WebGL / scroll-driven experiences. If the brief is "award-grade"
       or names a 3D hero, this is the design lead, not a section tool.
   One architecture doc with diagrams only where they change a
   decision. For L-tier decisions that could go multiple ways, use the
   rubric: list 2-3 real alternatives, score them on complexity /
   performance / maintainability / security / cost, pick the winner, and
   record WHY in one paragraph (that paragraph is the ADR).
4. **Plan** (M/L) - milestones as verifiable outcomes
   ("[action] -> verify: [expected result]"), riskiest assumption first.
5. **Implement** - smallest end-to-end slice first, then widen. Register
   the dev server in the hub registry (scan or manual entry + sync) so
   preview and the squads see it. Ponytail ladder applies to every
   component.
6. **Verify & secure** - the ship pipeline IS this phase: kaanha-tester
   (real checks + test gaps), kaanha-verifier (adversarial review),
   security-review doctrine for auth/secrets/input-validation on anything
   network-facing. The push gate enforces it - do not narrate quality,
   pass the gate.
7. **Document & deploy** - README (run, configure, deploy), .env.example,
   deploy per the project's platform (engineering:deploy-checklist
   doctrine); rollback path stated. Docs match what was actually built.
8. **Operate** (L, or on request) - add the project to Code Guardian's
   scope via the dev-hub registry; define the 2-3 metrics worth watching;
   wire monitoring available on the platform.

## Phase transitions - reorient before entering each phase

Long builds drift. At every phase boundary answer five questions in one
line each, out loud: where are we / what is the end goal / what is
missing / what is blocking / what happens next. If the answers surprise
you, fix the plan before writing more code. This is a compass check, not
a license to add scope - "next" is always the next agreed phase.

## Gates (the enforced kind)

- No implementation before phase 1's acceptance criteria exist.
- No push without the kaanha-gate approval (machinery, not promise).
- No "done" claim without: acceptance criteria demonstrably met, checks
  green, docs current, dev server registered.
- Artifacts are proportional: if no one will read a document, do not
  write it. An artifact exists to change a decision or survive handoff.

## Definition of done (all sizes)

Acceptance criteria met and demonstrated - tests pass via ship pipeline -
secrets out of code - README lets a stranger run it - registered in the
dev hub - known gaps and next steps written down honestly.
