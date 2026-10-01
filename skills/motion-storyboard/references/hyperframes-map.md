# HyperFrames map: capabilities, limits, and the name of each building block

HyperFrames renders video from HTML. A composition is a web page whose timing is declared with `data-*` attributes and whose animation is one paused, seekable timeline. Headless Chrome captures it frame by frame. Anything a browser can draw is available; anything that cannot be seeked to an exact time is not.

Install or refresh its skills with `npx hyperframes skills update`. The skills are the authority on implementation; this file maps storyboard language to them. Checked against `hyperframes@latest` on 2026-10-01.

## 1. Capabilities

| Capability | How |
|---|---|
| 2D motion of any DOM element | GSAP on one paused timeline (default runtime) |
| Text effects | per-word/letter spans, masks, 24 named text effects (`hyperframes-animation/adapters/animate-text.md`) |
| SVG draw and morph | stroke-dashoffset draw (`svg-path-draw`), path morph (`hyperframes-keyframes`) |
| Masks and reveals | `clip-path` (inset, circle, polygon), `mask-image`, overflow-hidden parents |
| Blur, glow, colour | `filter` (blur, brightness, saturate), `box-shadow`, `text-shadow`, `backdrop-filter` (glass) |
| 3D | CSS `perspective` + `preserve-3d` + rotationX/Y/z; Three.js for real 3D, GLTF models |
| After Effects animation | Lottie / dotLottie (`adapters/lottie.md`), including character animation |
| Shaders | WebGL fragment shaders; 14 built-in shader transitions (`@hyperframes/shader-transitions`); TypeGPU/WebGPU |
| Canvas | Canvas 2D procedural art, particles (deterministic) |
| Media | video clips, images, audio tracks with framework-owned playback; volume automation, ducking, effects (`hyperframes-audio`) |
| Music sync | `npx hyperframes beats` → beat grid |
| Website capture | `npx hyperframes capture <URL>` → screenshots + brand tokens |
| Registry | ~400 installable blocks/components: `npx hyperframes catalog <word>`, `npx hyperframes add <name>` |
| Voice / captions | TTS (`npx hyperframes tts`), transcription, caption skins (`media-use`) |
| Verification | `npx hyperframes check` (lint, runtime, layout, contrast), `snapshot`, animation map script |
| Render | `npx hyperframes render -o out.mp4`; MP4, transparent WebM/MOV; 16:9, 9:16, 1:1, 4K |

## 2. Hard limits (the build fails or renders wrong if broken)

- One paused GSAP timeline registered on `window.__timelines["<id>"]`. No autoplaying animation.
- Deterministic: no `Math.random()`, `Date.now()`, `performance.now()`; no `repeat: -1`. Use index-seeded pseudo-random values.
- Seek-safe: `fromTo` with explicit start states; `immediateRender: false` when re-animating an element; no relative `+=` values.
- Animate transforms (x, y, scale, rotation, skew), opacity, filter, clip-path, colours. Never width, height, top, left (use scale, translate, masks).
- No CSS `transition` on animated elements; no iframes; no timeline built inside async callbacks.
- No `display`/raw `visibility` tweens; zero-duration `tl.set` at explicit boundaries is allowed.
- No exit animations before a transition (except the last scene).
- In multi-scene compositions, never measure the DOM at tween time; use constants.
- Shader transitions: every scene needs an explicit `background-color` matching `bgColor`; no `var()` colours and no `transparent` keyword in gradients on captured elements.
- Fonts: local `@font-face` files (the linter requires them); vendor GSAP locally if the CDN is blocked.
- Transitions that do not work in CSS: star iris, tilt-shift, lens flare, door hinge.

## 3. Storyboard term → building block

| Storyboard says | HyperFrames rule / blueprint / registry item |
|---|---|
| word slams on beats, each differently | rule `kinetic-beat-slam`; blueprint `kinetic-type-beats` |
| cascade of words/items | rule `waterfall-entry` |
| spring pop / badge pop | rule `spring-pop-entrance`; registry `badge-pop` |
| fast entrance with motion blur | rule `motion-blur-streak` |
| decode / scramble | rule `hacker-flip-3d` |
| counter | rule `counting-dynamic-scale`; registry `number-pop-in` |
| slot-machine digits / ticker | rule `vertical-spring-ticker` |
| highlight / marker / underline | rule `css-marker-patterns` |
| typewriter | rule `gsap-effects` (typewriter); blueprint `typewriter-reveal` |
| cursor clicks UI | rules `cursor-click-ripple`, `cursor-drag`, `press-release-spring`; blueprint `cursor-ui-demo` |
| phone tap | registry `touch-indicator` |
| notification drops, panel expands | rule `anchored-layout-expand` |
| device hero, screens cycle | blueprint `device-surface-showcase`; registry `parallax-device-dive` |
| live control → target | rule `control-target-sync`; blueprint `panel-edit-live-sync` |
| list / grid assembles | blueprint `grid-card-assemble` |
| bars, progress, charts | rules `stat-bars-and-fills`, `chart-scrub-readout`; blueprint `dataviz-countup` |
| camera push / pull / zoom to element | rules `multi-phase-camera`, `coordinate-target-zoom`, `viewport-change` |
| pan across stations | blueprint `spatial-pan-stations` |
| zoom out to reveal | blueprint `zoom-out-workspace-reveal` |
| 3D camera flight | rule `3d-camera-flight`; blueprint `camera-journey` |
| depth of field / rack focus | rule `depth-of-field-blur` |
| tilted card pair | rule `split-tilt-cards`; blueprint `comparison-split` |
| orbit / 3D entry | rule `orbit-3d-entry` |
| scatter and reassemble | rule `depth-scatter-assemble`; `center-outward-expansion` |
| hub with satellites | rule `avatar-cloud-network`; blueprint `constellation-hub` |
| one element shoves another | rule `reactive-displacement`; blueprint `ticker-takeover` |
| morph one thing into another | rules `card-morph-anchor`, `scale-swap-transition`; registry `morph-swap` |
| theme change in place | rule `theme-crossfade-morph`; blueprint `fixed-anchor-cycle` |
| logo assembles | blueprint `logo-assemble-lockup`; registry `logo-outro` |
| CTA button press | blueprint `cta-morph-press` |
| confetti / burst | rule `particle-burst` |
| glow behind hero | rule `ambient-glow-bloom` |
| idle bob / breathing | rule `sine-wave-loop` |
| icon details alive | rule `svg-icon-enrichment` |
| SVG draws itself | rule `svg-path-draw` |
| glitch | rule `chromatic-glitch` |
| gradient through text | rule `gradient-text-sweep`; registry `text-shimmer`, `shimmer-sweep` |
| light sweep over the scene | registry `light-sweep-pass` |
| mesh gradient background | registry `mesh-gradient-bg`, `mk-background` |
| liquid glass | registry `liquid-glass-widgets`, `liquid-glass-notification`, `ios26-liquid-glass`, `vfx-liquid-glass`, `glass-shard-title` |
| neon border light | registry `lt-neon-border` |
| whip pan | registry `whip-pan-cut`; shader `whip-pan` |
| match cut | registry `match-cut`, `text-match-cut`, `type-match-cut`, `cut-the-curve` |
| iris | registry `iris-reveal`; shader `sdf-iris`; CSS `transitions/css-radial.md` |
| zoom through | CSS `transitions/css-scale.md`; registry `parallax-zoom`; shader `cinematic-zoom` |
| push / squeeze / elastic push | CSS `transitions/css-push.md`; registry `page-slide`, `rubber-band-bumper` |
| blocks / blinds | CSS `transitions/css-cover.md` |
| blur through / focus pull | CSS `transitions/css-blur.md`, `css-dissolve.md` |
| light leak / flash | CSS `transitions/css-light.md`; registry `organic-light-leak-overlay`, `editorial-flash-overlay` |
| pixel / grid / halftone dissolve | registry `grid-pixelate-wipe`, `halftone-dissolve` |
| beat freeze, speed ramp | registry `beat-freeze-cut` |

Before hand-building any named effect, search the registry: `npx hyperframes catalog <word>`.
