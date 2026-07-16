---
name: shader-artist
description: Author custom GLSL - raymarched SDF worlds, fresnel rims, fog, grain, noise, glow, dissolve - as performance-budgeted fragments with documented uniforms and mobile GPU cost notes. Use when writing or tuning shader code, when a scene needs a bespoke material/effect, or when a shader is slow. NOT for scene/component architecture (threejs-builder) or picking the visual language (experience-director).
---

# Shader artist

Every pattern below shipped in production (kaanha.tech odyssey). Each
lists its cost. Compose from these before inventing; when you invent,
document uniforms + cost the same way.

## 0. Ground rules

- `#version 300 es`, `precision highp float`. Colors as `const vec3`
  from BRAND.md tokens - never hex-in-a-comment-nobody-updates.
- **Loop bounds must be DYNAMIC (uniform-derived), never compile-time
  constants** - see §3; getting this wrong freezes the page on Windows
  Chrome. Scale the bound with a `uQuality` uniform (0 mobile / 1
  desktop) via `mix()` - one knob, whole shader adapts.
- No divergent branching in hot loops; prefer `mix/step/smoothstep`
  over `if` where the compiler can't flatten.
- Fullscreen pass: draw one triangle from `gl_VertexID`, no buffers:
  `vec2 pos = vec2((id<<1)&2, id&2); gl_Position = vec4(pos*2-1, 0, 1);`

## 1. Hash noise (cheap, no textures)

```glsl
float hash13(vec3 p){ p=fract(p*.3183099+.1); p*=17.;
  return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }          // per-cell ids
float hash12(vec2 p){ vec3 q=fract(vec3(p.xyx)*.1031);
  q+=dot(q,q.yzx+33.33); return fract((q.x+q.y)*q.z); } // film grain
```
Cost: negligible. Film grain, added to the final color:

```glsl
float grain = (hash12(frag + fract(uTime)*61.7) - .5) * .035;  // ~±.017
col += grain;
```

**The `- .5` is not optional.** `hash12` returns [0,1); without
centering, the term is strictly positive and you have added a constant
~+0.017 DC lift to every channel of every pixel - blacks off zero,
washed shadows, and half the banding-hiding benefit gone. It still
looks like grain at a glance, which is what makes it worth catching.
Use hash13 for per-cell variation.

## 2. SDF world building

```glsl
float sdRBox(vec3 p, vec3 b, float r){ vec3 q=abs(p)-b;
  return length(max(q,0.))+min(max(q.x,max(q.y,q.z)),0.)-r; }
```
- **Domain repetition**: `id=floor(p/cell); q=mod(p,cell)-cell*.5;` then
  size/offset/rotate per cell from `hash13(id)`. Skip ~25% of cells
  (`if(h>.78) return cell*.4;`) - empty slots read as paths and the
  field breathes.
- **Strata blending**: `blend = smoothstep(y0, y1, p.y)` then `mix()`
  cell size, box dims, rounding - two worlds become one continuous one.
- Per-cell rotation costs one `mat2` multiply - keep it to the sparse
  stratum (`spin *= blend`).

## 3. The march (budgeted) - and the ANGLE trap

```glsl
// steps comes in as a uniform-derived value: mix(44., 72., uQuality)
float march(vec3 ro, vec3 rd, float tMax, float steps){
  float t = 0.;
  for(float i = 0.; i < steps; i++){          // DYNAMIC bound - see below
    float d = map(ro + rd*t);
    if(d < .0012*t + .0004) return t;         // scaled epsilon + FLOOR
    t += d * mix(.72, 1., min(t*.025, 1.));   // relax with distance
    if(t > tMax) break;
  }
  return -1.;
}
```

**The trap (learned the hard way in production, do not undo it):** bound
the loop with a compile-time constant - `for(float i=0.; i<72.; i++)`,
even with an `if(i>=steps) break;` inside - and ANGLE's D3D backend
fully unrolls it, inlining 72 copies of `map()`. fxc's optimizer goes
over a cliff: the shader "compiles" for MINUTES inside the first draw
call, which reads as a frozen tab on Windows Chrome/Edge (the default
for most visitors). A dynamic, uniform-derived bound emits a real GPU
loop and compiles in milliseconds. The inner `break` does not rescue a
constant bound - fxc unrolls first.

- **Epsilon needs the constant floor** (`+ .0004`): a purely
  distance-scaled epsilon collapses toward zero near the origin, so
  close rays never register a hit and burn the whole budget.
- **Relaxation ramps with distance**: careful 0.72 steps near the
  camera, full-length strides in the far field - the fog owns that
  range anyway, and the wide establishing shot is exactly where every
  pixel used to burn all its steps. A flat `t += d*.72` is the version
  that cost the frame.
- Cost: THE budget - everything else is noise next to step count ×
  map() cost. Tune steps down until it breaks, then +8. Tetrahedral
  normals (4 map calls, not 6):
  `e.xyy*map(p+e.xyy)+e.yyx*map(p+e.yyx)+...`

## 4. The light kit (ink world, one accent)

```glsl
float fres = pow(clamp(1.+dot(n,rd),0.,1.), 2.6);            // copper rim
col = mix(base, EMBER, fres*rimStrength*shimmer);
col = mix(col, GLOW, pow(fres,3.2)*(rimStrength+spot)*shimmer); // hot peaks
float fog = 1.-exp(-t*.048); col = mix(col, skyCol, fog);    // depth
col += EMBER * horizonHaze * .10;                             // low warmth
col *= 1.-.45*dot(ndc*.62,ndc*.62);                           // vignette
```
- Fresnel exponent 2.4-2.8 = material feel; the glow layer is the SAME
  fresnel to a higher power - peaks live only at extreme grazing angles.
  The cursor `spot` term rides the glow, not the base rim.
- **Fog mixes to the SKY color, not to a constant ink.** Mixing to a
  fixed ink is what pins the world to one time of day; targeting the
  sky color is what lets the same world hold a night AND a dawn
  chapter. If the art direction has any temperature journey, fog owes
  it to skyCol.
- `shimmer = .85+.15*sin(uTime*.6 + p.y*.7 + p.x*.3)` - alive without
  visible motion. Drop the `p.x` term and every column shimmers in
  lockstep, which reads as a global flicker rather than material life.
  Scroll-driven `warmth` swelling mid-journey and cooling at the ends
  gives the page an emotional temperature curve for ~free.
- One faint cool key light (`dot(n, keyDir) * 0.045`) so dark faces keep
  form. That's the whole kit - more lights is less ink.

## 5. Other effects, with costs

- **Dissolve**: `if(noise3(p*k) < uProgress) discard;` + emissive edge
  `smoothstep(0.,.05, noise-uProgress)`. Cost: one noise/frag. Discard
  disables early-Z on some tile GPUs - keep dissolving meshes small.
- **Refraction/glass** (mesh scenes): screen-space refraction via
  render-target readback = one extra full pass; mobile budget usually
  says no - fake with fresnel + env map first.
- **Bloom**: real bloom = multi-pass blur; the fresnel glow layer above
  fakes 80% of it for zero passes. Reach for real bloom only on desktop
  uQuality and only if the art direction demands halos crossing edges.

## Verification

A shader is done when: compiles with zero warnings, holds MEASURED fps
on a coarse-pointer profile at its uQuality=0 path, survives
uTime > 10min (no precision drift - wrap long times), and its uniforms
are documented where the component sets them.
