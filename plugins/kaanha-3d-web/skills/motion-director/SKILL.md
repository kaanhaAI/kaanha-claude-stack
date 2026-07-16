---
name: motion-director
description: Choreograph premium web motion - smooth scroll (Lenis), GSAP/ScrollTrigger timelines, scroll-driven cameras, reveals, page transitions, micro-interactions - always with reduced-motion fallbacks and zero layout shift. Use when wiring scroll behavior, adding/tuning animations, or when motion "feels off / janky / cheap". NOT for building the 3D scene itself (threejs-builder), writing shaders (shader-artist), or looking up motion presets/design-system data (ui-ux-pro-max is the database; this skill is the choreography).
---

# Motion director

Motion is pacing, not decoration. Every animation needs a reason a
first-time visitor would feel; everything else is jitter.

## 1. The scroll foundation

- Lenis for smooth scroll, initialised once at layout level, destroyed on
  unmount. The wrapper must self-disable for `prefers-reduced-motion`
  and SSR - native scroll is the fallback, and everything must still
  work on it.
- Scene cameras read damped scroll progress (lerp k≈0.07), never raw
  scroll - the damping IS the cinematic feel.
- Camera paths: 4-6 keyframes (position + target), segment-eased with
  smoothstep (`f*f*(3-2f)` per segment). More keyframes = mush; ease the
  segments, not the whole path.

## 2. GSAP / ScrollTrigger discipline

- Timelines over one-off tweens: chapters own a timeline each; scrub
  (`scrub: true` or 0.5-1s) for scroll-bound, plain timeline for
  entrance.
- Pinning is expensive attention - at most one pinned sequence per page,
  and only when the content genuinely narrates in place.
- Reveals: translate+fade 12-24px, 0.6-0.9s, expo/quart-out, stagger
  60-120ms. Reveal once (`once: true`) - re-triggering on scroll-up
  reads as a bug.
- Kill and rebuild triggers on navigation; leaked ScrollTriggers are the
  #1 SPA jank source.

## 3. Zero layout shift (hard rule)

Animations must not move layout. The shipped lesson (agent-panel typing
animation, 0.17 CLS before the fix): reserve the FINAL box from first
paint - render an invisible full-length copy and absolutely position the
animating content over it. The same pattern covers typewriters, counters
(reserve widest number with `font-variant-numeric: tabular-nums`), and
accordion reveals (animate transform/clip-path, never height where it
pushes siblings).

## 4. Micro-interactions

- Hovers: color/opacity/decoration transitions 150-300ms; transforms of
  1-2px max. Nothing bounces.
- Cursor effects: default to none. A custom cursor must earn its bytes
  on a genuinely pointer-driven experience, and must not exist on touch.
- Focus states are motion too: visible, instant, never animated away -
  keyboard users get the same quality bar.
- The accent color's motion budget is the art-direction budget (≤5% of
  viewport) - hover glows count against it.

## 5. Reduced motion - for EVERY animation

`prefers-reduced-motion: reduce` means: smooth scroll off, scene replaced
by poster (builder's floor), scrubbed timelines replaced by their END
state, reveals replaced by visible content, autoplaying motion gone. The
reduced experience is a designed artifact - review it explicitly, don't
let it be whatever breaks.

## Verification

Drive the page in the browser: full scroll range, mobile + desktop
widths, reduced-motion toggled both ways, and a CLS measurement
(Performance panel or web-vitals) - CLS < 0.1 MEASURED, and no animation
visibly re-flows neighbors.
