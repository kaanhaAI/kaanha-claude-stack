---
name: experience-director
description: Design a cinematic 3D web experience from concept to build-ready brief - narrative arc, spatial metaphor, chapter structure, art direction. Use when the user wants an award-grade / Awwwards-level / cinematic site or hero, a "scroll journey", a 3D landing experience, or asks "design the experience" before building. NOT for ordinary marketing pages or component-level UI (design/ui-ux-pro-max skills handle those), and NOT for implementing the scene (threejs-builder does that).
---

# Experience director

The output of this skill is a **build-ready experience brief**, not code
and not vibes. Every downstream skill (threejs-builder, motion-director,
shader-artist) consumes this brief.

## 1. Narrative before pixels

Find the brand's story and give it a SPATIAL metaphor - the single
decision everything else hangs on. The scene is the story told in space;
scroll is time.

Reference pattern (kaanha.tech odyssey, shipped): "from broken laptops to
custom AI" became a vertical world - sparse intelligence monoliths above,
dense infrastructure grid below - and the camera DESCENDS the stack as
the visitor scrolls. One metaphor, held for the whole page.

Test for a good metaphor: you can say it in one sentence, it survives
being drawn as a 5-frame storyboard, and each frame maps to something
the business actually does.

## 2. Chapter structure

- Hero/arrival + 4-5 scroll chapters. One thought per viewport - if a
  section needs two paragraphs, it is two chapters or too much copy.
- Canonical arc: arrival (wordmark over the wide reveal) → what we make →
  what we keep running → proof → ways in. Adapt the middle, keep the
  bookends.
- Proof chapters use ONLY real numbers the user supplies, each linking to
  its source/case study. Never invent metrics - an empty proof section
  is more premium than a fake one.
- The primary CTA is ideally alive (an agent panel, a configurator) -
  the most interactive element on screen, but never fighting the
  typography for hierarchy.

## 3. Art direction rules

- Ink-dark base world; ONE signature accent, budgeted at ≤5% of any
  viewport (rim light, punctuation, hover - not fills).
- One display face (editorial serif or grotesk at massive scale,
  tight leading ~0.85-0.95, letter-spacing -0.02 to -0.04em) + one mono
  for meta/labels (uppercase, tracking 0.2-0.25em). Nothing else.
- Copy over the scene gets a subtle text-shadow onto the world
  (e.g. `0 1px 28px rgba(ink, .85)`) - legibility without panels.
- Film grain + fog are unifiers: they marry DOM and GL into one surface
  and hide upscale artifacts from reduced render scales.
- Light is language: grazing-angle rim = craft/precision; white-hot
  glow peaks = energy - reserve them for meaning, not decoration.

## 4. The brief (deliverable format)

One document containing:

1. The metaphor sentence + 5-frame storyboard (words are fine).
2. Chapter table: title / one-line copy intent / what the camera does /
   what the scene does.
3. Camera path: 4-6 keyframes as positions+targets in plain language
   ("wide reveal above the field" → "drift between monoliths" → ...).
4. Token sheet: base, accent, glow, type pairing - handed to BRAND.md.
5. The floors (copy verbatim into the brief - they are contractual):
   reduced-motion → static poster, GL never mounts; tab hidden → loop
   pauses; DPR cap 1.75 + reduced internal scale; synchronous first
   frame; 60fps mid hardware; graceful WebGL-absent fallback.
6. Non-goals: what this experience deliberately does NOT do.

## Honesty rules

- Reference sites (Apple/Nike/Porsche-class, Awwwards winners) are for
  extracting PATTERNS ("why does this hold attention"), never for
  copying assets, copy, or distinctive trade dress.
- If the brand story is thin, say so and ask for the real material -
  a cinematic surface over nothing reads as slop within seconds.
