# [Project] · [length]s motion design video · build prompt

<!--
  Written by the motion-storyboard skill. Hand this whole file to Claude Code (Opus) in the
  project folder that holds the assets. It is self-contained: the builder does not need the
  motion-storyboard skill, only HyperFrames.
-->

## 0. Your job

Build this video in HyperFrames exactly as storyboarded below. The creative decisions are made: do not redesign, add scenes, add text or swap transitions. If something in the storyboard cannot work, change the smallest thing that fixes it and list the change in your hand-off.

Deliverable: `renders/[slug].mp4`, [W]×[H], [fps] fps, [length]s, with the music.

## 1. Before writing anything

1. Read the HyperFrames skills: `hyperframes`, `hyperframes-core`, `hyperframes-animation` (install with `npx hyperframes skills update` if missing). They are the authority on how to build; this file is the authority on what to build.
2. Check the assets listed in §3 exist. If one is missing, stop and say which.
3. Music first: put the track in the composition as `<audio id="music" data-timeline-role="music" src="...">`, run `npx hyperframes beats .`, and read the beat grid. The storyboard gives times as music positions `P<phrase>.<pulse>` (phrase = 8 pulses) with the seconds they resolve to at [BPM] BPM. **Re-derive every time from the measured grid** with a helper:
   ```js
   const BEATS = [/* beat times from the beat file */];
   const at = (phrase, pulse = 0, nudge = -0.033) => BEATS[phrase * 8 + pulse] + nudge; // land 1 frame early
   ```
   If the measured tempo differs from [BPM], keep the phrase structure and let the seconds move.

## 2. The video in one paragraph

[Message as a claim.] [Concept: the idea, the spine, the signature moments.] [Arc.] [Rhythm shape and where the peak is.]

## 3. Brief and assets

- Product: 
- Audience: 
- Message (lands by the end of frame 2): ""
- End line: ""
- CTA: 
- Assets: fonts `...` (only these, local `@font-face`) · logo `...` (never distort or recolour) · screens `...` · music `...`

## 4. Look

- Palette: bg `#` · text `#` · accent `#` (only on [rule]) · allowed tints · banned colours
- Type: hero ( px) · headline ( px) · label ( px)
- Medium / material: [flat | glass | chrome | paper | painted], with its rules
- Background layer: 
- Light events (shine sweeps, glints, rim light): 

## 5. Motion system

- Energy and default durations:
- Entrance vocabulary (name → from → to, duration, ease):
- Ease palette: 
- Ambient rule per scene:
- Camera rig: `.world` > `.bg` (×) · `.mid` (1×) · `.fg` (×); entrances on elements, camera moves on `.world` only
- Direction rule:

## 6. Seam map

| Cut | Time | From → to | Transition | Role | Carried by | Spec |
|---|---|---|---|---|---|---|

## 7. Storyboard

<!-- One block per frame, in the format of references/11-storyboard-format.md -->

## Frame 1 — [Name]

- time: P0.0–P1.0 ( – s)
- role / why: 
- transition in: 

**Event:** 
**Reads:**
- – 
**On screen (verbatim):** 
**Layout:** 
**Depth:** BG · MG · FG
**Material/light:** 

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|

**Camera:** 
**Audio cue:** 
**Transition out:** seam map cut 1
**Do not:** 
**Frame check:**
- @ s: 

## 8. Rules for the build (non-negotiable)

- One paused GSAP timeline registered on `window.__timelines`; nothing autoplays.
- Deterministic: no `Math.random`, `Date.now`, `performance.now`, no `repeat: -1`. Seed any variation from indices.
- `fromTo` with explicit start states; `immediateRender: false` on any `fromTo` that is not the element's first appearance.
- Animate only transforms (x, y, scale, rotation, skew), opacity, filter, clip-path and colours. Never width, height, top or left.
- Never two concurrent transform tweens on one element: entrance on the element, drift on a wrapper.
- Ambient loops live on the timeline with finite repeats.
- The transition is the exit: no fading elements out before a transition (the last frame may fade).
- Vendor GSAP and fonts into `assets/`; no CDN dependencies.
- Text stays inside the safe area; [9:16: key content out of the top 250px and bottom 450px].
- [Project bans: no em dashes, ≤ 3 words of message on screen, banned colours, banned props.]

## 9. Verify, then hand off

1. `npx hyperframes check .` and fix every error. A wall of contrast errors usually means a wipe panel left covering the frame; intentional overlaps get `data-layout-allow-overlap` / `data-layout-allow-occlusion`.
2. Render a draft: `npx hyperframes render -o renders/draft.mp4`.
3. Extract a still at every **Frame check** time and look at each one against its check:
   `ffmpeg -v error -ss <t> -i renders/draft.mp4 -frames:v 1 renders/check-<t>.png`
   Then a strip of every frame across each cut (`-ss <T-0.2> -t 0.4 -vf "fps=30,scale=480:-2,tile=6x2"`) and a contact sheet of the whole film (`-vf "fps=4,scale=320:-2,tile=8x8"`).
4. Look for: overlaps and clipping, a word still mid-entrance at its check time, two things moving at once where one should lead, identical simultaneous entrances, blank or flashing transition midpoints, wrong fonts or colours, glass that looks like a flat box, any read that gets only a few frames.
5. Fix, re-render, re-check (2–3 rounds is normal). Then render `renders/[slug].mp4`.
6. Hand off: the file path, duration, resolution, the stills you checked, every deviation from this storyboard and why, and what you could not verify (audio feel, motion at full speed).
