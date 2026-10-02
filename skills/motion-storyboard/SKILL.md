---
name: motion-storyboard
description: Write the prompt for a motion design video. Turns a rough idea or product brief into one self-contained Markdown prompt file, storyboard first, that the user hands to Claude (Opus) in a separate session to build the video in HyperFrames. The prompt carries the message and features, the product's visual terrain (football → ball, pitch, scoreboard; privacy → redaction blocks, hashes), a concept with a spine, the look, a motion system, a seam map of transitions, and every frame specified (event, reads, words, layout, depth, motion with eases and durations, camera, materials like glass, gradients, shine and glints, transition out, frame check), plus the build rules and verification steps. Use whenever someone wants a video prompt, storyboard or brief for a promo, launch video, explainer, social clip or motion graphic, or says "make a video for X" in a session meant for writing the prompt. Brand-agnostic; the brand is supplied per project.
---

# Motion storyboard: the video prompt writer

You are the director and the writer. Your output is **a prompt file**, not a video. The user takes the file to a fresh Claude Code session (Opus, with HyperFrames) and that session builds the video from it. So:

- **The file must stand alone.** The builder has never seen this conversation and does not have this skill. Everything it needs (the story, the look, every frame, the transition specs, the build rules, how to verify) is in the file.
- **Every creative decision is made in the file.** A vague prompt ("logo slams in, push transition out") forces the builder to improvise, and improvised motion is generic. The builder should only have to execute.
- **Storyboard first.** The storyboard is the heart of the file; the build instructions wrap around it.

Output file: `<slug>-video-prompt.md`, following `templates/video-prompt.md`.

## When the request arrives

1. Read what the user gave you. If it lacks the product, the audience, the length or the aspect, ask once, in one message. Everything else gets a sensible default that you state.
2. Run the stages below. Show the user the concept (stage 3) before writing the full storyboard; it is cheap to change there.
3. Write the prompt file, run the self-review, fix, then give the user the file and a short summary table (frame · time · event · transition out).
4. If the user's music file is available to you, run `npx hyperframes beats` on it and write real times. If not, write music positions with an assumed BPM; the prompt tells the builder to re-derive the times from the measured grid.
5. Do not build the video unless the user explicitly asks you to in this session.

## The stages

| # | Stage | Goes into the prompt as | Reference |
|---|---|---|---|
| 1 | **Brief → message and features** | §3 Brief: the message as a claim; 2–4 features, each with its *proof moment* | `01-brief-and-features.md` |
| 2 | **Terrain** | §2 and the props, devices and transitions used in every frame | `02-terrain.md` |
| 3 | **Concept** (show the user) | §2: the idea, the spine, signature moments, rhythm shape, bans | `03-concept.md` |
| 4 | **Look** (default: the house look, with the brand's colours) | §4: palette, type, medium/material, 3D, background layer, light events | `14-house-look.md`, `07-type-in-motion.md`, `08-materials-and-light.md`, `13` §8 |
| 5 | **Motion system and seam map** | §5 and §6 | `04-motion-language.md`, `05-transitions.md`, `06-camera-and-depth.md`, `09-rhythm-and-music.md`, `15-pace-and-flow.md` |
| 6 | **Storyboard** | §7: every frame, fully specified | `11-storyboard-format.md`, `10-product-ui.md`, `13-reads-events-and-acting.md` |
| 7 | **Build rules and verification** | §8 and §9, adapted to the project | `hyperframes-map.md`, `12-build-and-review.md` |
| 8 | **Self-review** | fixes before handing over | `12-build-and-review.md` §1 |

## Reference map

| Need | Read |
|---|---|
| What motion design is: principles, easing, timing, offset, follow-through, hierarchy | `references/04-motion-language.md` |
| Scene-to-scene transitions: meaning, catalogue with numbers, velocity matching, match cuts | `references/05-transitions.md` |
| Camera, parallax, zoom, 3D, depth of field | `references/06-camera-and-depth.md` |
| Kinetic type: entrances, masks, reading time, word limits | `references/07-type-in-motion.md` |
| The default look: dark premium, neon signal, dark glass, glints, real 3D | `references/14-house-look.md` |
| Glass, gradients, chrome, shine sweeps, glints, rim light, grain, bloom | `references/08-materials-and-light.md` (tested recipes in `recipes/materials.html`) |
| Music, beats, phrases, holds | `references/09-rhythm-and-music.md` |
| Pace: when to go fast or slow, hold budgets, pulse sync, flow through continuity, smells of lag | `references/15-pace-and-flow.md` |
| Showing a product or app UI working | `references/10-product-ui.md` |
| What HyperFrames can and cannot do, and the name of each building block | `references/hyperframes-map.md` |
| Reads (timing for the viewer), an event in every frame, show-don't-write, sets and diegetic props, characters and acting, choosing a medium | `references/13-reads-events-and-acting.md` |
| Measured numbers from reference work | `references/measured-references.md` |
| The prompt file template (the output) | `templates/video-prompt.md` |
| Intake questions for a new video | `templates/brief.md` |

Load references as the stage needs them; you do not need all of them for a 6-second logo sting.

## Default look

Unless the user asks otherwise, design in the **house look** (`references/14-house-look.md`): a near-black stage with accent light curtains, dark glass UI, glints, a neon signal colour reserved for the payoff, and **real 3D as a priority** (the extruded logo with a flat face, a signature 3D sculpture from the product's idea, 3D objects carrying the transitions). Swap in the brand's colours, fonts and logo; keep the look. Describe it fully in the prompt's §4, because the builder has never seen it.

## Rules every prompt's storyboard follows

**Story**
- The message is a claim ("Sell to all of Nigeria in one link"), not a topic ("About AvioMax"). It lands on screen by the second beat.
- Every beat has a *why* traced to the message. A beat whose why you cannot write gets cut.
- Show the product doing the thing (state changes on real-looking UI), never a screenshot with a caption.
- Every prop comes from the terrain. If a prop could appear unchanged in another product's video, replace it.
- Every frame has an **event**: something is different between its first and last frame. Cause, then reaction. Whatever is set up pays off.
- **Show it, don't write it.** Never label what the picture already shows; words carry only the message, proof numbers, the brand and the CTA.
- **Sets, not cards; props, not overlays.** Acts happen in places the camera moves through; data lives in the world as objects that can be acted on and escalate.
- The ending **rhymes** with the opening.

**Pace (default; the judgment is in `references/15-pace-and-flow.md`, read it for every storyboard)**
- The goal is no waiting: each new thing arrives just as the viewer finishes the last. Lag is time after the reads have ended, rarely slow tweens.
- Size scenes by their reads in bars: one idea is usually **one bar** (about 2s at 120–130 BPM), a demo with 2–3 state changes or the end card two bars (a phrase), the hero up to a phrase and a half. Never give a one-idea scene a phrase because phrases are tidy.
- Sync at the pulse, not only at the cut: words, list rows, state flips and end-card pieces arrive **one per pulse**, so the viewer reads during the build and the hold after can be short.
- Static camera, nothing travelling: hold only for reading time (0.4–0.8s for a line built word by word, about 1s for headline + card, 1–1.5s for a dense grid or list), then cut. Typing, count-ups, live footage, a list filling or a build into a drop can run longer because they are new information. Decorative ambience (glints, drift, bob) never earns time.
- Fast for information, slow for weight: UI, labels and chips enter in 0.15–0.35s; slow moves (0.5–1.5s) only for a hero reveal, a build that accelerates into a drop, or the last line. A quiet passage in the music is not a pause: keep one thing changing per bar.
- Flow comes from continuity before camera moves: a persistent object that changes state on the beat, persistent chrome (a header, a clock), carried transitions, background colour flips per section.
- A 30–40s film is the default for a promo with 3–4 proofs; at a bar per idea, 30s fits 10–14 scenes.
- Measure the draft with `recipes/motion-profile.py` (no quiet run over 1.5s) and look at a timestamped 10fps strip of every scene (`measured-references.md`, how to measure): mark when each new element arrives and check the arrivals sit on pulses and the last read is followed by the cut, not by waiting.

**Timing (model the viewer)**
- List each frame's **reads** (what the viewer must understand, in order, with start and end). One read at a time; each gets time to be found, understood and registered. Fast actions, slow meanings. The reads set the frame's length, never the other way round.

**Motion**
- Each element gets a verb, a start state, an end state, an ease and a duration. "Animates in" is not a spec.
- Every beat has build → breathe → resolve. Write where the breath is; a breath is what makes the next hit land. A breath is short: 0.5–1s, never more than 1.5s; past about 1s something meaningful must still be changing (a travelling camera, typing, a count, a list filling), or cut.
- Order of motion is order of importance. The first thing that moves is what the viewer reads first.
- Entrances use `.out` eases, exits `.in`, moves between positions `.inOut`. Exits are faster than entrances.
- Vary on purpose: at most two tweens in a beat share an ease; the slowest beat is about 3× slower than the fastest; entrances come from different directions and use different properties.
- Avoid twinning: no two arms, cards or characters move identically at the same moment; offset timing and amount.
- Ambient motion alone does not keep a hold alive. A hold over about 1s needs a visible travelling camera (1 → 1.05–1.1, a truck, a rack focus) or content still changing; with neither, shorten the frame. Decorative ambience (curtains, grain, blobs) stays quieter than the action.

**Transitions**
- A transition carries meaning (continue, next point, new section, reveal). Pick it for what it says.
- One primary transition for most cuts, one or two accents, the boldest on the hero moment. Not a different transition at every cut.
- Outgoing accelerates out, incoming decelerates in, peak speed at the cut (velocity matching). The transition is the exit: no fading things out before it.
- Prefer object-carried transitions (an element from scene A becomes the frame, the mask or the subject of scene B) over full-frame effects.

**Frame**
- At most 2–3 words of a message on screen at once, plain language, no em dashes.
- Two focal points per frame, three depth layers, one accent colour, content anchored to edges or a grid, not floating centred by default.
- Video scale: headlines 96–220px at 1080p, body 32–44px, nothing under 24px without a reason.

**HyperFrames (write these into §8 of every prompt)**
- One paused GSAP timeline on `window.__timelines`; deterministic (no `Math.random`, `Date.now`, `repeat: -1`); `fromTo` with explicit start states; transforms, opacity, filter, clip-path, colour only (never width/height/top/left); ambient loops live on the timeline. Details in `references/hyperframes-map.md`.

## What to hand the user

- After stage 3: the message, the terrain table, the five concepts in three lines each, your pick and why. Wait for a reaction.
- At the end: the prompt file, a summary table (frame · time · event · transition out), the assumptions the builder will need to check (BPM, missing assets), and one line on how to use it: *"Open Claude Code in the folder with your assets and say: Build the video in `<slug>-video-prompt.md`."*
