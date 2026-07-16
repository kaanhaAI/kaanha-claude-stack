# The kaanha-grade site prompt

Paste into a fresh session in a NEW empty project folder (stack installed).
Swap the first line's placeholders. Distilled from the kaanha.tech hero-v3
build (2026-07-15) — the floors below are the ones that actually held in
production.

---

Build me a production website for {BUSINESS NAME} — {one line: what it does,
who it's for, region}. Run the full factory lifecycle, L-tier: discovery →
brand → build → verify → ship. Treat kaanha.tech's odyssey hero as the
quality bar: award-grade and cinematic, not a template with stock sections.

BRAND FIRST
- Derive a brand system before writing any page: an ink-dark base, one
  signature accent used sparingly (≤5% of any viewport), one display face +
  one mono. Write it into BRAND.md with design tokens AND performance
  floors — from then on BRAND.md is law; read it before touching anything
  visual.

THE EXPERIENCE
- One continuous 3D/WebGL surface is the storytelling spine (raymarched SDF
  world or Three.js scene — pick for the narrative, justify the choice).
  Scroll drives the camera through it; the brand story is told spatially.
- Monastic flat UI over the scene: sparse statements, one thought per
  viewport. Hero + 4–5 scroll chapters: arrival → what we do → proof →
  ways in. Proof uses only real numbers I give you — never invent metrics.
- A live conversational agent panel as the primary CTA if an API key is
  configured; an honest soft-launch banner if not.

HARD FLOORS (non-negotiable, build them in from the first commit)
- prefers-reduced-motion → static poster, the GL never mounts.
- Tab hidden → render loop pauses. WebGL unavailable/lost → same poster.
- DPR capped at 1.75 with reduced internal render scale; first frame drawn
  synchronously; 60fps on mid hardware.
- Lighthouse ≥95 and fps are MEASURED before ship, never asserted.

ENGINEERING
- SvelteKit + TypeScript strict (or argue for something else before
  starting). svelte-check zero errors, production build clean, Playwright
  smoke tests covering every chapter and key flow.
- Enroll the project in the dev hub for a port. Verify every visual change
  by driving it in the browser — mobile and desktop widths — before calling
  it done.
- Full site: services, work/case studies, contact, SEO meta + OG, sitemap.
- Deploy config for Railway included, but production is gated: run the ship
  workflow (test → adversarial verify → my explicit approval) and never
  push without it.

WORKING CONTRACT
Check don't guess. One step at a time. Complete what you started. Use the
browser wherever the task needs one. Every report/deliverable is a
self-contained HTML file updated in place and sent to me rendered. Finish
by walking me through the running site in the browser, then stop at the
gate and wait for my word: "ship".
