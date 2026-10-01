# 04 · Motion language: how motion design works

The principles below come from classic animation (Disney's twelve principles), interface motion (Zajno's motion.zajno.com, Material, Apple HIG) and measured promo work. Each ends in something you can write in a storyboard.

## 1. Easing: nothing in nature moves linearly

Objects gain speed as they start and lose it as they stop ("slow in, slow out"). Easing is the curve of that speed. **The motion is the verb; the ease is the adverb**: the same slide reads as confident, dreamy or playful depending on the curve.

| Curve | Feels | Use for | GSAP |
|---|---|---|---|
| Linear | mechanical, constant | continuous ambient travel (a ticker, a rotating rim light), never for arrivals | `none` |
| Ease-out (fast start, soft stop) | responsive, confident | **entrances**, things arriving | `power2.out` soft · `power3.out` firm · `power4.out` / `expo.out` snappy |
| Ease-in (slow start, fast end) | departing, thrown | **exits**, things leaving, the outgoing half of a transition | `power2.in`, `power3.in`, `expo.in` |
| Ease-in-out | deliberate, smooth | moving between two on-screen positions, camera moves, reflow | `power2.inOut`, `power3.inOut`, `sine.inOut` (gentle) |
| Cubic / long-tail ease | premium, "Apple" glide: long acceleration and deceleration, fast middle | hero moves, UI panels | `expo.inOut`, `power4.inOut`, `cubic-bezier(0.65,0,0.35,1)` |
| Overshoot (back) | springy, physical | pops, badges, stamps, cards landing | `back.out(1.4)` gentle · `back.out(2.5)` punchy |
| Elastic | playful, cartoon | kids, games, one comic beat; never on body text | `elastic.out(1, 0.5)` |
| Steps | mechanical ticking | clocks, split-flap, typewriter | `steps(n)` |

Rules:
- Entrances `.out`, exits `.in`, between positions `.inOut`. Getting this backwards is the most common amateur tell: ease-in entrances feel sluggish, ease-out exits feel reluctant.
- No more than two tweens in one beat share an ease.
- Overshoot only on objects with "weight" (cards, badges, stamps). Text rarely overshoots more than `back.out(1.2)`.

## 2. Timing: duration is weight and energy

| Duration | Reads as | Typical use |
|---|---|---|
| 0.08–0.15s | instant, percussive | word slams on a beat, state flips, flashes |
| 0.15–0.3s | fast, energetic | sticker words, pops, badges, social promo entrances |
| 0.3–0.5s | professional, clear | cards, UI panels, most transitions |
| 0.5–0.8s | weighty, premium | hero objects, logo reveals, product spins |
| 0.8–2s | cinematic, emotional | camera moves, slow pushes, atmospheric reveals |

Pace by medium (measured, see `measured-references.md`):
- **Social promo / launch clip:** entrances 0.13–0.3s, transitions 0.17–0.35s, cuts every 2–3s.
- **House-look promo (the default):** entrances 0.3–0.7s, transitions 0.3–0.45s, a scene every 4s (6s for the hero), holds ≤ 1.5s, no quiet run over 1.5s. Measured: the same film felt stalled at 60s (8s scenes, holds up to 5.5s) and right at 38s.
- **Website / UI showcase:** element motion 0.4–1.4s, long holds (35–60% of the time nothing moves).
- **Brand film:** 0.6–2s moves, few cuts.

Contrast is what makes speed visible: the slowest beat should be about 3× slower than the fastest. A whole video at 0.4s feels like nothing happened.

## 3. Offset and delay (stagger)

A slight delay between related objects creates softness and layered movement, and tells the viewer the order of importance.

- Stagger in order of importance, not reading or DOM order.
- Typical offsets: 0.03–0.06s per letter, 0.06–0.12s per word or list item, 0.1–0.2s per card.
- Cap the whole group at about 0.5s, whatever the count, so it reads as one arrival.
- Let the next item start before the previous finishes (overlap), never wait for completion.
- Distinguish neighbours: animate one with opacity + position, its neighbour with opacity only (a Zajno trick for separating adjacent elements).

## 4. Follow-through and overlapping action

Different parts of a thing stop at different times. When a card lands, its shadow settles a frame later, its badge pops after, its contents slide in last. When a phone stops moving, the UI inside drifts 10–20px further and settles.

Storyboard it as a **secondary** line under the primary motion: *"Card lands (0.35s back.out(1.3)); +0.08s shadow settles; +0.12s badge pops."*

## 5. Anticipation

Before a big action, a small opposite one: a button dips 4% before being pressed; a card pulls back 20px before shooting off; a logo shrinks to 0.92 before the slam. 0.1–0.2s. Use on hero moments only; overused, it feels cartoonish.

## 6. Squash, stretch and impact

Fast objects stretch along their direction (scaleX 1.15, scaleY 0.9) and squash on impact (scaleX 1.1, scaleY 0.9 for 2–3 frames), then recover. In flat graphics, fake impact with: a 2–4 frame scale overshoot, a 6–12px frame shake decaying over 0.2s, a flash of the accent colour, or a shockwave ring expanding from the impact point.

## 7. Arcs

Natural motion travels on curves, not straight lines. A card flying in from the corner should arc (x and y on different eases, e.g. x `power3.out`, y `power2.out`), or rotate slightly as it travels. Straight-line diagonal moves look computer-made.

## 8. Fade, but never fade alone

Opacity is the most used and least interesting property. It works when combined with position, scale, blur or a mask. On its own it is a dissolve, and dissolves between scenes read as "nothing happened". Alone it is fine for ambient elements and for the neighbour-distinction trick in §3.

## 9. Transform and morph

One object becomes another: a round icon expands into a full-bleed photo; a button becomes a panel; a coin becomes the logo dot. Morph keeps the eye on one object across a change, which is why it is the strongest storytelling transition. In HyperFrames: `card-morph-anchor`, `scale-swap-transition`, `morph-swap` (registry), SVG path morph, or clip-path shape tweens.

## 10. Masking

Content revealed through a moving window: text rising from behind a baseline, an image opening inside a slit, a photo shifting inside a shape. The content can move independently of the mask (photo drifts or scales slowly inside a fixed window), which reads as soft and spacious. Implemented with `clip-path` tweens (`inset()`, `circle()`, `polygon()`) or an `overflow: hidden` parent with the child translating.

## 11. Dimension and parallax

Layers moving at different speeds create depth: the farther the layer, the less it moves (background 0.2×, midground 0.5×, foreground 1×, front overlay 1.3×). Even a 20–40px parallax difference during a slow drift makes a flat frame feel built. See `06-camera-and-depth.md`.

## 12. Zoom

Zoom gives continuity between levels: from a whole to a detail (zoom in to a UI element to explain it) or from a detail to a whole (pull back to reveal context). Zoom through an element into the next scene is one of the strongest transitions. See `06-camera-and-depth.md`.

## 13. Hierarchy and staging

- The first thing to move is the most important. Nothing else should move at the same moment unless it supports it.
- One focal action at a time; secondary motion is quieter (smaller, slower, lower contrast).
- Every beat has three phases: **build** (0–40%: elements arrive, one per pulse), **breathe** (a short hold, 0.5–1.5s, while the camera keeps travelling), **resolve** (the decisive end or the transition). If the breath would run longer than 1.5s, the beat is too long: cut time, not reads.
- First visible motion within 0.1–0.3s of a beat starting; never at exactly 0 (it reads as a jump cut).

## 14. Motion verbs

Give every element a verb. If you cannot name the verb, the element is not designed yet.

| Character | Verbs |
|---|---|
| Impact / weight | SLAM, CRASH, PUNCH, STAMP, DROP, SHATTER |
| Directional | SLIDE, PUSH, PULL, WIPE, SWEEP, WHIP |
| Build / reveal | DRAW, FILL, GROW, EXPAND, ASSEMBLE, COUNT UP, TYPE ON, UNROLL |
| Organic / ambient | FLOAT, DRIFT, BREATHE, PULSE, ORBIT, MORPH, RIPPLE |
| Mechanical / precise | SNAP, CLICK, LOCK IN, STEP, FLIP, TICK |
| Light | GLINT, SWEEP (shine), BLOOM, FLARE, FLICKER |

## 15. The entrance vocabulary (with numbers)

Defaults for 1920×1080; scale offsets for other sizes.

| Name | From | To | Duration | Ease |
|---|---|---|---|---|
| **Scale slam** | scale 1.6–2.2, opacity 0, blur 12px | scale 1, sharp | 0.15–0.25s | `expo.out`, + 6–10px frame shake |
| **Side snap** | x ±120–200px, opacity 0, blur 8px, skewX ∓8° | x 0, skew 0 | 0.15–0.25s | `power4.out` |
| **Drop** | y −160px, opacity 0 | y 0 | 0.3s | `back.out(1.6)` |
| **Rise** | y +60–100px, opacity 0 (often inside a mask) | y 0 | 0.4–0.6s | `power3.out` / `expo.out` |
| **Blur resolve** | blur 12–16px, scale 1.06, opacity 0 | sharp | 0.13–0.2s | `power3.out` |
| **Mask rise** | text y 105% inside overflow-hidden line | y 0 | 0.5–0.7s, 0.06s per line | `expo.out` |
| **Spring pop** | scale 0, opacity 0 | scale 1 | 0.3–0.45s | `back.out(1.7–2.5)` |
| **Stamp** | scale 2.5, rotation −25°, opacity 0 | scale 1, rotation −8° | 0.25s | `back.out(2.5)` + shake |
| **Flip in** | rotationX −90° (perspective 1200) | 0° | 0.4s | `back.out(1.2)` |
| **Type on** | characters revealed one by one | — | 0.03–0.05s per char | `steps` |
| **Draw on** | SVG stroke-dashoffset = length | 0 | 0.5–1s | `power2.inOut` |
| **Fly in on arc** | off-frame corner, rotation ±12° | rest, tilt ±2° | 0.4s | x `power3.out`, y `power2.out` |
| **Count up** | 0 | value | 0.8–1.5s | `power2.out` (snap to integers) |

Exits: 60–70% of the entrance duration, `.in` ease, or no exit at all because the transition covers it.

## 16. Ambient motion (the "never still" layer)

During every hold, something moves. Two layers:

**The camera keeps travelling** (required on any hold over ~1s): a push of scale 1 → 1.05–1.1 over the scene (`power1.in` or `power2.in`, so it gathers speed into the cut), a truck across the set, a rack focus, or a lean into the next subject. It must be visible: a 1.02 drift over 4s reads as stopped.

**Decorative ambience** underneath, a different one per scene:
- Camera drift: scale 1 → 1.02–1.04 or x ±20–30px over the beat, `none` or `sine.inOut` (only under a travelling move, never instead of one).
- Parallax layers drifting at different rates.
- Light travel: a shine sweep or a slowly rotating rim light.
- Background gradient blobs drifting (transforms only).
- Idle bob on a hero object: y ±6px, rotation ±1°, `sine.inOut`, finite yoyo repeats.

Decorative ambience must be at least 5× slower and quieter than action motion; if you notice it, it is too strong. The travelling camera is not ambience: it is the motion of the hold, and the viewer should feel it.
