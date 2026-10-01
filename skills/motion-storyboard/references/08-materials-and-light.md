# 08 · Materials and light: glass, gradients, chrome, shine, glints

Motion design looks expensive when surfaces behave like materials: glass blurs what is behind it, metal catches a travelling highlight, a corner glints as light passes. All of the recipes below were rendered in HyperFrames (headless Chrome, software GPU) and checked frame by frame. The working file is `recipes/materials.html`.

## 0. The rule that makes materials work

**Materials only read when something moves relative to them.** A glass card over a flat gradient looks like a tinted rectangle; the same card over drifting shapes with edges (big type, rings, product imagery) reads instantly as frosted glass. Chrome only reads as metal when the highlight travels. A glint only reads when it is timed to something passing.

Verified in the test render: v1 (glass over soft blobs only) looked like a gradient card; v2 (ghost type and a ring drifting behind) read as real glass.

So every material in a storyboard comes with its **light event**: what moves behind it or across it, and when.

## 1. Gradients and mesh backgrounds

**Mesh gradient** (soft, organic colour field):
- 3–4 large radial blobs (1,000–1,300px at 1080p), each `radial-gradient(circle, colour 0%, colour-at-0-alpha 70%)`.
- Wrap them in one container with `filter: blur(80–100px) saturate(120–140%)` and `inset: -200px` so the blurred edges never show.
- Animate the blobs with **transforms only** (x, y, scale), slow, `sine.inOut`, finite. Never animate `background-position` on a full-frame layer.
- Registry alternatives: `mesh-gradient-bg`, `mk-background`.

**Grain** (kills banding, adds texture):
- An SVG `feTurbulence` noise tile as a data-URI background, `opacity .1–.18`, `mix-blend-mode: overlay`, on top of the gradient.
- Required on any dark gradient: H.264 compression bands smooth gradients visibly.

**Rules:**
- No full-frame *linear* gradients on dark backgrounds (they band). Use radial blobs or solid + localised glow.
- Use the brand's colours. If the brand forbids colours (e.g. "no blue, green or purple"), blobs use tints and shades of the allowed colours only: for a charcoal and red brand, deep red, darker charcoal and a warm grey.
- Write `"transparent"` stops as the same colour at zero alpha (`rgba(204,0,0,0)`), never the keyword (it creates dark fringes in shader capture).

## 2. Glassmorphism

**Recipe (tested):**
```css
.glass {
  background: linear-gradient(135deg, rgba(255,255,255,.18), rgba(255,255,255,.05));   /* light glass */
  /* dark glass for text contrast: rgba(20,10,30,.30) → rgba(20,10,30,.45) */
  -webkit-backdrop-filter: blur(28px) saturate(170%);
  backdrop-filter: blur(28px) saturate(170%);
  border: 2px solid rgba(255,255,255,.28);
  border-top-color: rgba(255,255,255,.6);      /* light from above */
  border-left-color: rgba(255,255,255,.45);
  border-radius: 40–56px;
  box-shadow: inset 0 2px 0 rgba(255,255,255,.55),      /* top rim highlight */
              inset 0 -20px 40px rgba(255,255,255,.05), /* inner glow */
              0 40px 80px rgba(0,0,0,.45);              /* lift */
  overflow: hidden;   /* so shine sweeps clip to the card */
}
```
- Blur 16–32px; saturate 140–200% so colour glows through instead of going grey.
- Hard-code values inside `-webkit-backdrop-filter` (CSS variables are not reliable there).
- Put moving, high-contrast content **behind** it (ghost type, rings, product shots, the gradient blobs plus at least one shape with edges).
- Text on glass needs contrast: use the darker glass tint or keep text large and bold. The `hyperframes check` contrast test will flag small text on light glass over bright colour (it did in testing: 2.4:1 for 34px text).
- Animate glass with transforms and opacity. Do not tween `backdrop-filter` blur values every frame; if the glass must "frost in", tween the opacity of a pre-blurred glass layer.
- Entrance that suits glass: rise 80–120px + rotationX 15–20° → 0 with perspective 1400, 0.8–0.9s `expo.out`.
- Registry blocks for heavy liquid-glass looks (WebGPU/html-in-canvas): `liquid-glass-widgets`, `liquid-glass-notification`, `ios26-liquid-glass`, `vfx-liquid-glass`. Heavier to render; use when the look is the point.

## 3. Shine sweep (a light band crossing a surface)

**Recipe (tested):** a skewed gradient band inside the surface, moved by transform.
```css
.shine { position:absolute; top:-20%; left:0; width:240–300px; height:140%;
  transform: translateX(-400px) skewX(-20deg);
  background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.45) 50%, rgba(255,255,255,0) 100%);
  mix-blend-mode: soft-light;   /* or screen for a brighter pass; plain for matte surfaces */ }
```
Timeline: `x: -400 → surfaceWidth + 300`, 0.7–1.0s `power2.inOut`. One pass per surface, timed to a beat or to an event (a card landing, a "Paid" state).

- Text version: the registry component `text-shimmer` (one specular band through glyphs) or a `background-clip: text` gradient (see §4).
- Whole-scene version: registry `light-sweep-pass` drives every element's highlight and shadow from one `--light-x` value as a band crosses the frame. Quiet and premium.
- Do not loop shines. One pass, then the surface rests.

## 4. Chrome / metallic text

**Recipe (tested):** a multi-stop gradient clipped to the glyphs, moved by `background-position`.
```css
.chrome { background: linear-gradient(100deg, #fff 0%, #d9d6ff 30%, #7a74b8 46%, #fff 52%, #bdb8ee 70%, #fff 100%);
  background-size: 250% 100%; background-position: 100% 0;
  -webkit-background-clip: text; background-clip: text; color: transparent; }
```
Timeline: `backgroundPosition "100% 0" → "0% 0"`, 1.2–1.8s `power2.inOut`. The dark band in the middle (46%) is the "reflection of the floor"; the bright stop right after it (52%) is the highlight. Tint the stops toward the brand accent. Silver: whites and cool greys. Gold: #fff6d5 / #e0b04a / #8a5a12. Red metal: #ffe3e3 / #cc0000 / #5a0000.

Add a 1–2px light top edge (text-shadow `0 -1px 0 rgba(255,255,255,.6)`) for embossing if the type is large.

## 5. Glints (a star-flare catching light)

**Recipe (tested):** two thin gradient bars crossed plus a soft core.
```css
.glint { position:absolute; width:160px; height:160px; transform: scale(0); }
.glint::before { /* horizontal ray */ content:""; position:absolute; left:50%; top:50%;
  width:160px; height:6px; margin:-3px 0 0 -80px; border-radius:6px;
  background: radial-gradient(ellipse at center, #fff 0%, rgba(255,255,255,.9) 20%, rgba(255,255,255,0) 70%); }
.glint::after  { /* vertical ray, same with width/height swapped */ }
.glint b { /* core */ width:36px; height:36px; border-radius:50%;
  background: radial-gradient(circle, #fff 0%, rgba(255,255,255,.6) 35%, rgba(255,255,255,0) 70%); }
```
Timeline: pop `scale 0 → 1, rotation −30° → 15°` 0.2s `power3.out`; die `scale → 0, rotation → 45°` 0.3s `power2.in`. Total life ≈ 0.5s.

- Place glints on **corners and edges** where a shine sweep or a moving light would hit: a card's top-right corner as the sweep exits, the tip of a logo, the edge of a coin, a diamond's facet.
- Time the glint to the moment the sweep reaches that point (glint at sweep start + sweep duration × (point x ÷ surface width)).
- 1–3 glints per moment, different sizes (1, 0.7, 0.45), staggered 0.06–0.12s.
- Variant: 6-ray or 8-ray star (add 45° bars at half length) for diamonds and jewellery; anamorphic flare (one long horizontal ray, 600–900px, low opacity) for cinematic logos.

## 6. Rim light (light travelling around an edge)

**Recipe (tested):** a large conic gradient rotating behind a ring-shaped mask.
```css
.rim { position:absolute; /* card bounds + 4px */ border-radius: cardRadius+4px; padding: 3–4px;
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; overflow:hidden; }
.rim i { position:absolute; left:50%; top:50%; width:1400px; height:1400px; margin:-700px 0 0 -700px;
  background: conic-gradient(from 0deg, rgba(255,255,255,0) 0deg 300deg, #fff 345deg, rgba(255,255,255,0) 360deg); }
```
Timeline: `rotation 0 → 360×n`, `ease: "none"`, finite. One to one-and-a-half turns per hold reads as "live". The `hyperframes check` layout pass flags the oversized child; mark it `data-layout-allow-overflow` / `data-layout-allow-occlusion` (intentional). Registry alternative: `lt-neon-border`.

## 7. Glow, bloom and light

- **Glow behind a hero:** a radial gradient in the accent at 15–30% opacity, 1.3–1.6× the object's size, blooming in (scale 0.6 → 1, opacity 0 → 1, 0.6s `power2.out`) just before the object lands. Rule `ambient-glow-bloom`.
- **Neon:** layered `text-shadow`/`box-shadow` in the accent (0 0 8px, 0 0 24px, 0 0 60px) with a slight brightness flicker on index-seeded steps (never random).
- **Light leak / flash:** see `05-transitions.md`.
- **Lens streaks:** a thin horizontal gradient line (2–4px, 600–1200px wide) crossing behind a logo on the reveal beat.

## 8. Particles and confetti

One payoff burst per film, deterministic (index-derived angles and speeds, gravity on y). Rule `particle-burst`. Brand colours only. Small sparkles (mini glints at 0.2–0.4 scale) can trail a moving glossy object.

## 9. Choosing a material treatment per video

| Treatment | Looks | Use for | Notes |
|---|---|---|---|
| Flat + bold | posters, stickers | social, playful, local brands | cheapest to render, strongest legibility |
| Glass | premium tech, fintech, OS-style UI | dashboards, notifications, wallets | needs content behind it |
| Chrome / metal | luxury, launch, gaming | logo reveals, hero titles | needs one travelling highlight |
| Paper / print | editorial, human, crafty | stories, NGOs, food | grain, torn edges, cut-out collage (Zajno "Ways We Work") |
| Neon / dark | nightlife, gaming, music | dark looks | glow layers; watch contrast |
| Clay / 3D soft | friendly, consumer apps | onboarding, kids | Lottie or Three.js |

Pick one primary treatment per film; a second only for the hero moment (e.g. flat film, chrome logo at the end).

## 10. Storyboard notation

Write materials and light as their own line in each beat:

```
MATERIAL: Glass card (dark tint), over drifting red blobs + ghost "SELL" type at 0.3× parallax.
LIGHT: shine sweep across the card at P3.2 (0.8s power2.inOut, soft-light);
       glints on the card's top-right corner at P3.2+0.62s (scale 1) and on the "6%" badge
       at +0.74s (scale 0.6); rim light idles at 1 turn per 4s.
```
