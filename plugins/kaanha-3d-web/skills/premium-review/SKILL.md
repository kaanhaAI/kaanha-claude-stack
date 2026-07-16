---
name: premium-review
description: The award-grade ship review for a 3D/premium web experience - originality, craft, motion, measured performance, accessibility floors, mobile reality - before it goes live. Use when a cinematic site or 3D hero is "done", when asked "is this Awwwards-grade / premium enough", or before shipping any experience built with this plugin. NOT a substitute for the kaanha-quality ship gate (this runs BEFORE it) and NOT for ordinary code review.
---

# Premium review

The last gate before a cinematic experience meets the public. Everything
here is checked in a real browser at real widths - a claim you did not
observe is not a finding, and "should be fine" is not a verdict.

## Delegate, don't duplicate

- **Accessibility** → run `design:accessibility-review`. Bring its verdict
  back here; do not re-derive WCAG rules.
- **SEO / metadata** → run `marketing:seo-audit`.
- **Correctness / diff quality** → that is `kaanha-verifier` inside the
  ship pipeline, which runs AFTER this review passes.
This skill owns only what those cannot judge: whether the thing is
actually premium, and whether its floors are real.

## The twelve-point checklist (every point is observed, never assumed)

**Craft & direction**
1. **Originality** - does the experience have ONE idea a visitor could
   describe afterwards? Name it in a sentence. If you cannot, it is a
   template with effects.
2. **Narrative** - do the chapters build (arrival → substance → proof →
   invitation), or is it a pile of sections? One thought per viewport.
3. **Typography** - one display + one mono, display at genuine scale
   (clamp to viewport), tight tracking, legible over the scene.
4. **Restraint** - the accent stays ≤5% of any viewport; the ink does
   the work. Count it on a screenshot if unsure.

**Motion & scene**
5. **Camera/scroll feel** - damped, not raw; segment-eased; no
   overshoot or jitter at scroll extremes (test at both ends).
6. **Zero layout shift** - CLS MEASURED < 0.1. Typing/counters/reveals
   reserve their final box.
7. **Scene quality** - fog/grain unify DOM and GL; no visible aliasing,
   banding, or upscale mush; nothing pops at chapter boundaries.

**Reality**
8. **Measured fps** - rAF delta over ≥5s on desktop AND a coarse-pointer
   profile. Numbers in the report. No number = fail.
9. **Measured Lighthouse** - performance ≥95 (mobile profile), or an
   explicit written waiver from the user. Run it, screenshot it.
10. **The floors, exercised, one by one**: reduced-motion → poster and
    zero GL; tab hidden → loop stops; context lost → poster, no crash;
    DPR capped; first frame synchronous (no black flash on load).
11. **Mobile is not a shrink** - drive it at 375px: does the metaphor
    survive, is the agent/CTA reachable, do chapters still read? A
    beautiful desktop scene that is a dark smear on a phone fails.
12. **Degradation is designed** - no-JS/no-WebGL visitor still gets the
    brand, the copy, and a way to contact. Look at it; do not imagine it.

## Verdict format (self-contained HTML report, per house rules)

- Verdict up top: SHIP / SHIP WITH FIXES / NOT YET - one sentence why.
- Table: the twelve points, each PASS/FAIL/WAIVED with the OBSERVATION
  that decided it (measured number, screenshot, or the exact behavior).
- Fixes ranked by whether they block the ship.
- Then hand to `/ship` - tests, kaanha-verifier, gate approval, push.
  This review does not push; the gate does not care that the site is
  pretty.

## Honesty rules (non-negotiable)

- **No asserted metrics.** "60fps" and "Lighthouse 95+" are lies until
  measured on this build. Every number carries how it was obtained.
- **No predicted outcomes.** Never "this will win awards" or "users will
  convert better" - you have the build, not the audience.
- **Comparisons are structural.** Studying an award-winning site means
  extracting why a pattern holds attention, never lifting its assets,
  copy, or distinctive trade dress.
- A failing floor is a NOT YET, regardless of how good it looks. The
  floors are what separate a demo from a product.
