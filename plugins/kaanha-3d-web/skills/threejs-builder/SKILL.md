---
name: threejs-builder
description: Implement a real-time 3D web scene with hard performance floors - raymarched SDF worlds, Three.js, Threlte (Svelte), or React Three Fiber, plus the GLTF/Draco/KTX2 asset pipeline. Use when building or modifying a WebGL scene, hero canvas, product configurator/turntable, or when asked to "implement the 3D" from an experience brief. NOT for choosing the narrative (experience-director), authoring shader effects in depth (shader-artist), or looking up stack/design-system reference data (ui-ux-pro-max is the database; this skill builds the scene).
---

# Three.js / WebGL builder

Performance is architecture here, not polish. Budget draw calls before
beauty; build every floor in from the first commit - they are unaddable
later.

## 1. Engine decision ladder (justify out loud)

1. **Raymarched SDF on a fullscreen triangle** - abstract brand worlds,
   procedural geometry, zero dependencies, one draw call. The kaanha.tech
   odyssey shipped this way. Choose when the world is conceptual, not
   asset-driven.
2. **Vanilla Three.js** - asset-driven scenes (GLTF products, real
   environments) in any framework; smallest abstraction tax.
3. **Threlte** (SvelteKit) / **R3F + drei** (React) - asset-driven scenes
   where the scene graph is deeply reactive to app state. Framework
   bindings are a dependency; take them only when reactivity pays for it.

## 2. The proven component shape (framework-agnostic)

From the shipped OdysseyScene - replicate this structure whatever the
engine:

- Fixed full-viewport canvas BEHIND the DOM; chapters scroll over it and
  drive the scene via a scroll uniform/state. `aria-hidden="true"`.
- Context: `webgl2`, `antialias:false` (grain hides aliasing),
  `alpha:false`, `powerPreference:"high-performance"`.
- **Floors, in code, from commit one:**
  - `prefers-reduced-motion` checked BEFORE creating GL - render a static
    CSS poster instead (gradients implying the world). GL never mounts.
  - Shader compile/link failure or no WebGL2 → same poster. Log, don't
    throw.
  - `visibilitychange` → stop the rAF loop; resume on visible.
  - `webglcontextlost` → stop + poster.
  - DPR cap: `min(devicePixelRatio, 1.75) * scale` where scale ≈ 0.75
    desktop / 0.55 coarse pointer. Fog + grain make the upscale
    invisible.
  - **Synchronous first frame** before the rAF loop starts - hidden tabs
    and static captures must show the world, never a black canvas.
  - Cleanup: cancel rAF, remove listeners, `WEBGL_lose_context`.
- Inputs are damped, never raw: `x += (target - x) * k` per frame
  (scroll k≈0.07, mouse k≈0.05). Read scroll as
  `scrollY / (scrollHeight - innerHeight)` clamped 0..1.
- Standard uniforms: `uTime uScroll uMouse uRes uQuality` - uQuality
  (0 mobile / 1 desktop) scales march steps / sample counts in one place.

## 3. Asset pipeline (asset-driven scenes)

- GLTF + **Draco** for meshes; **KTX2/basis** for any texture over
  512px; power-of-two sizes; mipmaps on.
- Draw-call budget FIRST: target <100 calls; instance anything repeated
  (`InstancedMesh`); merge static geometry; LOD or impostors past the
  mid-ground.
- Lazy-load the scene bundle; the page must be readable before the GL
  arrives (poster → scene swap, no layout shift).
- Lights: one key + environment map beats four dynamic lights; bake what
  never moves. Shadows are the most expensive beauty - one caster or
  none.

## 4. Verification (non-negotiable)

- fps is MEASURED (rAF delta over 5s, mid hardware + a coarse-pointer
  emulation), never asserted. Record numbers in the ship notes.
- Toggle `prefers-reduced-motion` in devtools → poster renders, zero GL.
- Hide the tab → loop stops (log a frame counter to prove it).
- Kill the context (devtools "lose context") → poster, no crash.
- Drive the full scroll range in the browser at mobile AND desktop
  widths before calling any milestone done.
