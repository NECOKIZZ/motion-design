---
name: motion-storyboard
description: Direct a motion design video before building it. Turns a product brief into a beat-by-beat storyboard that Claude can build in HyperFrames without guessing — message and features, the product's visual terrain (football → ball, pitch, scoreboard; privacy → redaction blocks, hashes), a concept with a spine, then every beat specified with music position, layout, verbs, eases, durations, depth layers, camera, transitions, materials (glass, gradients, shine, glints) and a frame check. Use whenever someone asks for a promo, launch video, explainer, social clip, motion graphic or HyperFrames video, asks to write or improve a storyboard or video prompt, or hands over a brief like "make a 30-second video for X". Brand-agnostic; supply the brand per project.
---

# Motion storyboard

You are the director, not the animator. The animator (you, later, in HyperFrames) builds exactly what the storyboard says, so every decision that matters is made here, on paper, where changing it costs seconds. A vague storyboard ("logo slams in, push transition out") forces the build to improvise, and improvised motion is generic motion.

The output of this skill is a **storyboard file** (`STORYBOARD.md`, format in `references/11-storyboard-format.md`) detailed enough that a fresh session could build the video from it alone.

## When the request arrives

1. Read the brief. If it lacks the product, the audience, the length or the aspect, ask once, in one message. Anything else gets a sensible default that you state.
2. Run the seven stages below in order. Show the user the result of stage 3 (concept) and stage 5 (storyboard) before building anything over 15 seconds.
3. If the user also wants the video built, hand the approved storyboard to the HyperFrames build loop (`references/12-build-and-review.md`).

## The seven stages

| # | Stage | Output | Reference |
|---|---|---|---|
| 1 | **Brief → message and features** | One message written as a claim. 2–4 features, each with the single *proof moment* that shows it working. | `01-brief-and-features.md` |
| 2 | **Terrain** | The product's visual world: objects, actions, materials, sounds, signature transitions, and the generic props to avoid. | `02-terrain.md` |
| 3 | **Concept** | Five candidate concepts (two of them unlikely), one chosen. The **spine** (one device threading every beat), 1–2 **signature moments**, the rhythm shape. | `03-concept.md` |
| 4 | **Look** | Brand tokens, light/dark, material treatment (flat, glass, chrome, paper, neon), type roles, one accent. | `08-materials-and-light.md`, `07-type-in-motion.md` |
| 5 | **Beat sheet** | Every beat specified: music position, on-screen words verbatim, layout zones, depth layers, element-by-element motion (verb, from → to, ease, duration, offset), camera, breath, transition out, do-not, frame check. | `11-storyboard-format.md` + `04`–`10` |
| 6 | **Self-review** | The storyboard checked against the critique list before anyone sees it. | `12-build-and-review.md` §1 |
| 7 | **Build and verify** (if asked) | Composition built from the storyboard; frames extracted at every frame check; fixed until they match. | `12-build-and-review.md` §2–3 |

## Reference map

| Need | Read |
|---|---|
| What motion design is: principles, easing, timing, offset, follow-through, hierarchy | `references/04-motion-language.md` |
| Scene-to-scene transitions: meaning, catalogue with numbers, velocity matching, match cuts | `references/05-transitions.md` |
| Camera, parallax, zoom, 3D, depth of field | `references/06-camera-and-depth.md` |
| Kinetic type: entrances, masks, reading time, word limits | `references/07-type-in-motion.md` |
| Glass, gradients, chrome, shine sweeps, glints, rim light, grain, bloom | `references/08-materials-and-light.md` (tested recipes in `recipes/materials.html`) |
| Music, beats, phrases, holds | `references/09-rhythm-and-music.md` |
| Showing a product or app UI working | `references/10-product-ui.md` |
| What HyperFrames can and cannot do, and the name of each building block | `references/hyperframes-map.md` |
| Measured numbers from reference work | `references/measured-references.md` |
| Fill-in templates | `templates/brief.md`, `templates/storyboard.md` |
| A complete worked storyboard | `examples/aviomax-30s.md` |

Load references as the stage needs them; you do not need all of them for a 6-second logo sting.

## Rules that hold for every storyboard

**Story**
- The message is a claim ("Sell to all of Nigeria in one link"), not a topic ("About AvioMax"). It lands on screen by the second beat.
- Every beat has a *why* traced to the message. A beat whose why you cannot write gets cut.
- Show the product doing the thing (state changes on real-looking UI), never a screenshot with a caption.
- Every prop comes from the terrain. If a prop could appear unchanged in another product's video, replace it.

**Motion**
- Each element gets a verb, a start state, an end state, an ease and a duration. "Animates in" is not a spec.
- Every beat has build → breathe → resolve. Write where the breath is; a breath is what makes the next hit land.
- Order of motion is order of importance. The first thing that moves is what the viewer reads first.
- Entrances use `.out` eases, exits `.in`, moves between positions `.inOut`. Exits are faster than entrances.
- Vary on purpose: at most two tweens in a beat share an ease; the slowest beat is about 3× slower than the fastest; entrances come from different directions and use different properties.
- Ambient motion on every hold (drift, parallax, light travel) so nothing freezes, but it must be quieter than the action.

**Transitions**
- A transition carries meaning (continue, next point, new section, reveal). Pick it for what it says.
- One primary transition for most cuts, one or two accents, the boldest on the hero moment. Not a different transition at every cut.
- Outgoing accelerates out, incoming decelerates in, peak speed at the cut (velocity matching). The transition is the exit: no fading things out before it.
- Prefer object-carried transitions (an element from scene A becomes the frame, the mask or the subject of scene B) over full-frame effects.

**Frame**
- At most 2–3 words of a message on screen at once, plain language, no em dashes.
- Two focal points per frame, three depth layers, one accent colour, content anchored to edges or a grid, not floating centred by default.
- Video scale: headlines 96–220px at 1080p, body 32–44px, nothing under 24px without a reason.

**HyperFrames (non-negotiable at build)**
- One paused GSAP timeline on `window.__timelines`; deterministic (no `Math.random`, `Date.now`, `repeat: -1`); `fromTo` with explicit start states; transforms, opacity, filter, clip-path, colour only (never width/height/top/left); ambient loops live on the timeline. Details in `references/hyperframes-map.md`.

## What to hand the user

- After stage 3: the message, the terrain table, the five concepts in three lines each, your pick and why.
- After stage 5: the storyboard file path, plus a summary table (beat · time · on screen · transition out · why).
- After stage 7: the video path, the frames you checked, and anything you could not verify (audio feel, font fallback).
