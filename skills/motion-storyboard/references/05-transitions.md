# 05 · Transitions

A transition tells the viewer how two scenes relate. Pick it for what it says, then specify it so precisely that the build has nothing to decide.

## 1. What transitions mean

| Transition | Says | Use for |
|---|---|---|
| Hard cut | "wake up", disruption, rhythm | rapid lists, cuts on percussion, comic timing |
| Smash cut | contrast, punchline | quiet → loud, problem → answer |
| Push / slide | "next point", continuation along a path | between related features |
| Whip pan | energy, "meanwhile", speed | high-energy promos, travel between places |
| Zoom through | "go deeper", entering a thing | from overview into detail, into a product |
| Zoom out / pull back | "here's the bigger picture" | reveal context, one item → many |
| Iris / circle reveal | focus, a new world opening from one point | reveals from an object (a dot, a button, a ball) |
| Wipe / line wipe | a page turned, structured change | editorial, section changes |
| Cover (blocks, blinds) | a reset, new chapter | topic change |
| Match cut | "this is the same thing" | shape or motion continuity across scenes |
| Morph | "this becomes that" | product causes change, storytelling |
| Focus pull / blur through | drift, dream, softening | calm brands, wind-down |
| Light leak / flash | memory, energy burst | reveals, music drops |
| Glitch / chromatic | instability, tech, error | tension, "the old way breaks" |
| 3D flip | a card or board turning over | before/after, two sides of a thing |
| Gravity drop | collapse, ending | problem beats collapsing, outros |
| Crossfade | "this continues", nothing changed | almost never between scenes; fine for ambient layers |

## 2. The grammar

1. **One primary, one or two accents.** Use the primary for 60–70% of cuts between related beats, an accent for topic changes, and the boldest accent once, on the hero reveal. A different transition at every cut makes none of them land.
2. **The transition is the exit.** Outgoing content is fully visible when the transition starts; never fade elements out first (that is a jump cut with a dip). The last scene of the video is the only one allowed to fade.
3. **Velocity matching.** The outgoing scene accelerates out (`.in` ease) with a blur ramp; the incoming decelerates in (`.out` ease) with blur clearing. The fastest moment of both curves sits on the cut, and the speeds match within ~5%. The eye reads one continuous move instead of two animations.
4. **One direction rule.** Pick a travel direction for the film (leftward by default: new content enters from the right, like reading forward) and break it only on purpose (going backwards in time, a reversal).
5. **Land on the beat.** The cut point (the moment of peak velocity, or the frame the new scene is fully revealed for a hard cut) lands on a strong music beat, 1–2 frames early.
6. **Object-carried beats full-frame.** The best transitions are performed by something already in scene A: the ball, the bubble, the stamp, the link line. A full-frame effect with no motivating object is decoration.
7. **Match the energy.**

| Energy | Duration | Blur peak | Eases |
|---|---|---|---|
| Calm (luxury, wellness) | 0.5–0.8s | 20–30px | `sine.inOut`, `power1` |
| Medium (SaaS, explainer) | 0.3–0.5s | 8–15px | `power2`, `power3` |
| High (promo, sports, music) | 0.15–0.3s | 3–6px (motion carries it) | `power4`, `expo` |

## 3. Catalogue with build numbers

`T` = cut time. `old` / `new` = outgoing / incoming scene wrappers (1920×1080). All tweens on the one timeline.

### Push family
- **Push slide:** old `x 0 → −1920`, new `x 1920 → 0`, both 0.5s `power3.inOut` at T. Variant: old moves only −30% with a darken overlay (parallax push), which feels richer.
- **Vertical push:** same on y.
- **Elastic push:** old `x → −1920` 0.5s `power3.in`; new `x 1920 → 30` 0.4s `power4.out` at T+0.1, then `→ −15` 0.15s, `→ 0` 0.1s.
- **Squeeze:** old `scaleX 1 → 0` (origin left) 0.4s `power3.inOut`; new `scaleX 0 → 1` (origin right) at T+0.1.

### Whip pan
- old `x 0 → −400, blur 0 → 24px` 0.3s `power3.in`; new `x 400 → 0, blur 24 → 0` 0.3s `power3.out` at T+0.3 (or overlap 0.05s). Add `skewX ±6°` at peak for extra speed.
- Registry: `whip-pan-cut` (both scenes on one strip, velocity exact by construction). Shader: `whip-pan`.
- Terrain version: the ball/object streaks across first and the camera follows it.

### Zoom family
- **Zoom through:** old `scale 1 → 2.5, blur 0 → 8–20px, opacity → 0` 0.2–0.4s `power3.in`; new `scale 0.5–0.75 → 1, blur 8–20 → 0` 0.4–0.5s `expo.out` at T+0.15. Best when zooming *into* a specific element (a phone screen, a box opening, a letter's counter): scale around that element's centre (`transformOrigin` at the target).
- **Zoom out:** old on top (`zIndex 10`) `scale 1 → 0.3, opacity → 0` 0.4s `power3.in`, new already behind.
- **Pull-back reveal:** the whole world scales 3 → 1 in 0.5–0.8s `expo.out` to show one item becoming many.
- Registry: `parallax-zoom`, `parallax-unzoom`, `parallax-device-dive`. Shader: `cinematic-zoom`.

### Reveal / mask family
- **Circle iris:** new `clip-path circle(0% at X Y) → circle(75% at X Y)` 0.17–0.5s `power2.out`. Put `X Y` on a motivating object (the ball, a button, the logo dot). A thin accent ring riding the edge sells it. Registry: `iris-reveal`. Shader: `sdf-iris`.
- **Diamond iris, clock wipe, shutter:** see HyperFrames `transitions/css-radial.md`, `css-mechanical.md`.
- **Line wipe:** new `clip-path inset(0 100% 0 0) → inset(0 0 0 0)` 0.25–0.4s `power3.inOut`, with a 6–12px accent bar riding the edge.
- **Diagonal two-tone wipe:** an ink panel with an accent leading edge sweeps diagonally (`polygon` clip or a rotated panel translating), 0.25s.
- **Letterbox slit (measured, Zajno):** black bars close from top and bottom until the old scene is a thin horizontal slit (0.4–0.5s `power3.inOut`); the new image is already inside the slit; then the slit opens or the new title rises above it. Elegant for editorial and premium.
- **Hairline collapse (measured, Zajno):** an image collapses to a 2px line (`scaleY → 0.003`, origin bottom, 0.4s `power3.in`) while the next content is already laid out.

### Cover family
- **Staggered blocks:** 2–5 full-frame colour panels slide across, 0.04–0.06s apart, 0.25s each `power3.inOut`; scene swaps while covered; panels continue out. Use brand colours, accent last.
- **Blinds:** 6–16 strips, 0.018–0.03s stagger, 0.2s each.
- **Colour panel rise (measured, Zajno):** an accent panel rises from the bottom, holds a section title, then wipes up to reveal the new section.

### Match and morph
- **Match cut:** an element in A (a circle, a line, a phone outline) is exactly matched in position, size and motion by an element in B; hard-swap at the speed peak. Registry: `match-cut`, `text-match-cut`, `type-match-cut`.
- **Card morph:** a container morphs size, radius and fill from A's element into B's frame, then reveals B. HyperFrames rule `card-morph-anchor`; `scale-swap-transition`; registry `morph-swap`.
- **Collapse into logo:** all elements of A converge (staggered 0.03s, `power3.in`, 0.3s) into the logo mark at centre.

### Dissolve and light
- **Blur through:** old `blur → 15–30px, scale 1.05` then new resolves from `blur 15–30px, scale 0.95`, total 0.4–1.2s.
- **Focus pull:** like blur through, but the new scene is already in place behind, defocused.
- **Flash through white:** 0.01–0.3s; on a music drop. Shader `flash-through-white`; registry `editorial-flash-overlay`.
- **Light leak / overexposure:** warm overlay larger than frame drifts across while `filter: brightness(1 → 2.5 → 1)`. Registry `organic-light-leak-overlay`.

### 3D
- **Card flip:** stage `perspective 1400px`; old `rotationY 0 → 90°` 0.2s `power2.in`, new `−90° → 0` 0.25s `back.out(1.2)`.
- **Split-flap:** each half of the frame flips like a scoreboard flap, 0.12s per half, staggered.
- **Gravity drop:** old (on top) `y 0 → 1200, rotation 0 → 8°` 0.5s `power3.in`, new already behind.

### Distortion
- Glitch, chromatic split, VHS, ripple: 0.2–0.4s. Use only where instability is the meaning (the old way breaking). Shader `glitch`, `chromatic-split`; registry `chromatic-aberration-wipe`.

### Shader transitions (WebGL, `@hyperframes/shader-transitions`)
domain-warp, ridged-burn, whip-pan, sdf-iris, ripple-waves, gravitational-lens, cinematic-zoom, chromatic-split, swirl-vortex, thermal-distortion, flash-through-white, cross-warp-morph, light-leak, glitch. Use 1–2 per film at most, on the hero reveal and maybe the CTA. Shader scenes need explicit `background-color` and no `var()` colours during capture (see `hyperframes-map.md`).

### Do not use (broken or cheap in CSS)
Star iris, tilt-shift, lens flare, door hinge; transitions that show a visible repeating grid pattern.

## 4. How to write a transition in a storyboard

Not "push transition out". Write:

```
OUT @ P4.0 (17.78s) — Bubble morph (accent, signature).
  The WhatsApp bubble holding the link (A, right third) expands to full frame:
  scale 1 → 9 around its centre, radius 28px → 0, 0.45s expo.inOut, starts T−0.25s.
  At full frame it is the white background of scene 5. Scene 5's first element (the
  vendor dashboard) is already in place at opacity 0 and rises in at T+0.05s.
  Direction: forward (expansion). Sound: soft whoosh into the drop.
```

Required parts: cut time and beat; name and role (primary / accent / hero); the motivating object and where it is; what each scene does, with numbers; what the new scene shows on its first frame; direction; sound.

## 5. Planning the whole film's transitions

Write a seam map before the beat sheet, one row per cut:

| Cut | Time | From → to | Transition | Role | Carried by |
|---|---|---|---|---|---|
| 1 | 4.44s | Hook → Logo | Iris from the red full stop of "way." | accent | the full stop |
| 2 | 8.89s | Logo → Buyers | Link-line wipe | primary | the link line drawn from the logo |
| 3 | 13.33s | Buyers → One link | Link-line wipe | primary | the Share button's link line |
| 4 | 17.78s | One link → Sellers | Bubble morph | accent (signature) | the WhatsApp bubble |
| 5 | 22.22s | Sellers → Trust | Link-line wipe | primary | the line leaving the wallet |
| 6 | 26.67s | Trust → End | Collapse into logo + red flood | hero | the trust cards and the line |

(From `examples/aviomax-30s-prompt.md`.)

Check: one primary used most; boldest on the hero moment; direction rule kept; every cut on a strong beat; no two consecutive accents of the same kind.
