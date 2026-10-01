# 06 · Camera, parallax, zoom and depth

A HyperFrames frame has no real camera, so you build one: a `.world` wrapper that holds the scene, which you scale and translate. Everything inside moves together, like a camera move. Layers inside move by different amounts, like depth.

## 1. Camera rig (write this into every storyboard's global section)

```
.stage   perspective 1400px (only if any 3D)
 └ .world      ← the camera: x, y, scale, rotation (and rotationX/Y for 3D)
    ├ .bg      ← far layer (moves 0.2–0.4× the camera)
    ├ .mid     ← content layer (1×)
    └ .fg      ← near accents, particles, light streaks (1.2–1.5×)
```

Rule from HyperFrames: never put an entrance tween and a camera tween on the same element (they overwrite each other). Entrances go on the element; camera moves go on `.world` or a wrapper.

## 2. Camera moves

| Move | Spec | Feels | Use |
|---|---|---|---|
| Travelling push | scale 1 → 1.05–1.1 over the scene, `power1.in`/`power2.in` | momentum, always going somewhere | every hold over ~1s (the default) |
| Drift | scale 1 → 1.02–1.04, or x ±20–30px, over the whole beat, `none`/`sine.inOut` | alive, but reads as still over 2s+ | under a travelling move, or holds under 1s |
| Push in | scale 1 → 1.15–1.3 over 1–2s, `power2.inOut` | focus, importance | landing on a hero element |
| Punch in | scale 1 → 1.2–1.4 in 0.15–0.25s, `expo.out`, on a beat | impact | emphasis on a word or number |
| Pull back | scale 1.5–3 → 1 over 0.5–1s, `expo.out` | reveal, context | one → many, detail → whole |
| Pan / truck | x across a wide canvas, `power3.inOut`, 0.6–1.2s per station | travel, sequence | stations on one canvas (blueprint `spatial-pan-stations`) |
| Target zoom | scale around a non-centred element (outer scales, inner counter-translates) | "look here" | explaining a UI element (rule `coordinate-target-zoom`) |
| Orbit / tilt | rotationY ±8–15°, rotationX ±5–10° | dimensional product view | devices, cards, logos |
| Camera flight | `.world` laid out in 3D; camera travels in z between surfaces | cinematic | rule `3d-camera-flight` |
| Shake | x/y ±6–12px decaying over 0.15–0.25s (deterministic offsets) | impact | slams, stamps, bass hits |

Camera moves ease `inOut` (they move between two framings); punch-ins and pull-backs on a beat use `expo.out`.

## 3. Parallax

"The farther the object, the less it moves." Assign every layer a depth factor and move it by camera × factor:
- far background (gradient blobs, ghost type): 0.2–0.4×
- background props: 0.5–0.7×
- content: 1×
- foreground accents (sparkles, streaks, blurred near objects): 1.2–1.6×

Even a slow 30px drift with three layers at different rates makes a flat frame read as a built space. During a pan or whip, parallax sells the speed.

Measured example (Zajno): a translucent panel rises while the cards beneath it shift slightly in the opposite direction; the counter-motion is what makes the panel feel on top.

## 4. Dimension (floating depth)

- **Floating tilted object:** rotationY −12 to −18°, rotationX 6–10°, soft large shadow, idle drift ±1–2°. Products, cards, tickets, phones.
- **Tilt to flatten:** an object enters tilted (rotationY ~ −60°) and flattens to 0° as it becomes readable.
- **Exploded view (measured, Zajno "Mobile House"):** a product's parts separate along an axis (axonometric), one part highlights, parts reassemble. Great for "what's inside" or features of a physical/system product.
- **Fan / stack:** cards or records stacked in depth (z or y offsets with scale falloff), flicked through one by one.
- **3D text depth:** stacked offset copies of a word (rule `3d-text-depth-layers`).
- Keep reading text flat (≤ 10° rotation) whenever it must be read; tilt during motion only.

## 5. Depth of field

Blur the layers that are not the subject: background 6–14px, foreground near objects 10–20px, subject sharp. Rack focus by tweening which layer is blurred (rule `depth-of-field-blur`). Depth of field is what makes a 2D frame look photographed.

## 6. Zoom as transition

See `05-transitions.md` for the numbers. The key decision is the **anchor**: zoom into a specific, meaningful point (the phone screen, the "Pay" button, the box opening, the centre of the "O" in the logo), never the frame centre by default.

## 7. Framing and composition

- Safe area: keep text inside 90% of width/height (5% margins); for 9:16 social keep key content out of the top ~250px and bottom ~450px (platform UI).
- Rule of thirds or a strong grid; anchor content to an edge.
- Alternate sides between beats (UI left / words right, then swap) so the eye travels.
- Reflow: when something new arrives, what is already there shifts or scales to make room on the same beat (0.35–0.45s `power3.inOut`). Nothing jumps, nothing is stranded.
