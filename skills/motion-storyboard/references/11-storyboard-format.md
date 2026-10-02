# 11 · The storyboard format

This is the storyboard section (§7) of the prompt file, plus the decisions it depends on (§2, §4–§6). Its test: **could a fresh session, with no other context and without this skill, build the video from the prompt without making a single creative decision?** If a field would make the builder guess, it is underspecified.

The whole prompt file follows `templates/video-prompt.md`. The sections below describe the content of each part; in the prompt file the global decisions go in §2–§6 and the frames in §7 as `### Frame N — Name` blocks. (The frame format also parses as a HyperFrames `STORYBOARD.md` if the builder wants to save one.)

## 1. Header facts (prompt §0–§3)

```yaml
---
format: 1920x1080          # or 1080x1920, 1080x1080
duration: 30s
fps: 30
message: "Sell to all of Nigeria in one link."
endline: "Shop smart. Sell big."
arc: Pain → Turn → Proof ×3 → Sign-off
audience: Nigerian small sellers on IG/TikTok/WhatsApp; shoppers wary of fake sellers
music: assets/music.mp3 (Afrobeats, 108 BPM, phrase = 8 pulses = 4.44s)
mode: collaborative
---
```

## 2. Global sections (above the first frame)

Write these before any frame. Frames refer to them by name instead of repeating.

### Concept
One paragraph: the idea, the spine, the signature moments, the rhythm shape. (From `03-concept.md`.)

### Terrain
The terrain table, signature props, props to avoid. (From `02-terrain.md`.)

### Look
- Palette by role with hex: background(s), text, accent, plus allowed tints. One accent.
- Type roles: font file, weight, sizes for hero / headline / label / meta.
- Material treatment and light rules (from `08-materials-and-light.md`).
- Background layer recipe (gradient, grain, ghost type, grid), shared or per scene.
- Logo rules: minimum size, clear space, never recoloured or distorted.

### Motion system
- Energy level and default durations (e.g. high: entrances 0.15–0.3s, transitions 0.2–0.35s).
- Entrance vocabulary to draw from (names from `04-motion-language.md` §15).
- Ease palette: 3–5 named eases and what each is for.
- Ambient rule (what keeps holds alive, per scene).
- Pace rule: scene unit (bar / phrase), arrival grid (one per pulse), entrance speed for information vs hero moves, the hold budget for static frames (`15-pace-and-flow.md`).
- Camera rig and parallax factors.
- Direction rule for travel.

### Beat grid
BPM, pulse length, phrase length, the table of phrase start times, where the drop/build is. All frame times derive from this.

### Seam map
Table of every transition (from `05-transitions.md` §5).

### Bans
Project "do nots", including slideshow and screensaver.

## 3. Per-frame sections

One `## Frame N — Name` per beat (a beat is one idea; usually one bar, a phrase for a demo or the hero).

```markdown
## Frame 3 — Buyers: verified sellers

- time: P3.0–P4.0 (8.89–13.33s, 4.44s)
- role: proof (feature 1)
- why: Shoppers doubt seller honesty; seeing a seller get verified is the proof.
- transition_in: Bubble morph from Frame 2 (see seam map, cut 2)
- status: outline

**Event:** a grey seller tag gets stamped "Verified" (cause: the scroll stops on it; reaction: the card lifts and turns accent).
**Reads:**
- 8.95–9.6 phone arrives; it's the AvioMax home feed (eye: centre-right, big, moving)
- 9.6–10.4 card 3's seller tag is grey (the scroll stops on it)
- 10.4–11.2 it gets stamped "Verified" (brightest, fastest thing on screen)
- 11.2–12.4 "Verified sellers" · "Delivered" (eye travels left after the stamp)
**On screen (verbatim):** "Verified sellers" · "Delivered"
**Layout:** phone mockup right third (62% height, centre x 1290); words left third, top-aligned at y 340; ghost type "SAFE" bottom-left.
**Depth:** BG charcoal mesh (red/charcoal blobs, grain) 0.3× · MG phone + chips 1× · FG two small red glints + blurred parcel corner 1.4×.
**Material/light:** flat UI inside the phone; the phone frame has a glass rim light idling 1 turn / 4s; one shine sweep across the phone at P3.5.

**Motion (in order of appearance):**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P3.0 | phone | TILT-FLATTEN | rotationY −35°, x +120 → 0°, 0 | 0.6s | expo.out | arrives from the expanding bubble |
| P3.1 | home feed | SCROLL | y 0 → −420 | 1.8s | power2.inOut | product cards pass; pauses on card 3 |
| P3.2 | card 3 seller tag | STAMP | grey "Seller" → red check "Verified" | 0.25s | back.out(2.5) | 6px shake on phone |
| P3.2 | "Verified sellers" | SIDE SNAP | x −160, skew 8°, blur 8 → sharp | 0.2s | power4.out | lands with the stamp |
| P3.4 | "Delivered" chip | RISE | y +80, opacity 0 → 0, 1 | 0.45s | power3.out | below the first chip, smaller |
| P3.5 | phone | SHINE | band x −300 → 900 | 0.8s | power2.inOut | soft-light; glint top-right at +0.6s |
| P3.6–7 | — | BREATHE | camera push scale 1 → 1.06 continues, gathering speed into the cut | — | power1.in | nothing new enters; 1s |

**Camera:** `.world` pushes x 0 → −30px, scale 1 → 1.06 across the whole frame (power1.in).
**Audio cue:** stamp thud on P3.2; soft whoosh into the cut.
**Transition out:** see seam map, cut 3 (Bubble morph, primary).
**Do not:** no shopping-cart icon; no fade on the chips; phone never smaller than 55% height.
**Frame check:**
- @P3.3 (10.2s): phone flat and sharp, "Verified" stamp visible on card 3, "Verified sellers" fully in, no overlap with the phone.
- @P3.6 (11.6s): both chips visible, left column aligned on one x, only drift moving.
```

### Field rules

| Field | Rule |
|---|---|
| time | Music positions + resolved seconds + duration. Durations sum to the total (state it). |
| role / why | Role in the arc; why traces to the message. No why → cut the frame. |
| Event | What is different between the frame's first and last moment; cause → reaction. No event → not a frame. |
| Reads | What the viewer must understand, in order, each with start–end and where the eye is. No overlapping reads; reads set the length (`13-reads-events-and-acting.md`). |
| On screen | Every word verbatim, in quotes. ≤ 3 words of message at once. Never a label repeating what the picture shows. |
| Layout | Zones and coordinates or thirds; sizes as % of frame or px. Two focal points. |
| Depth | BG / MG / FG with parallax factors. |
| Material/light | Treatment + the light event and its time. |
| Motion table | Every element that moves: time (music position), verb, from → to with values, duration, ease, notes. Order = order of importance. Arrivals on pulses. Include the breath as a row, with what is still changing during it (or why a still breath is short enough). |
| Camera | The `.world` move for the frame. |
| Audio cue | SFX and music events. |
| Transition out | Reference the seam map; the full spec lives there once. |
| Do not | At least one per frame that could go generic. |
| Frame check | 1–3 timestamps with what a still frame must show. These become the review frames. |

## 4. Quality bar for a finished storyboard

- Every element on screen has a verb, values, a duration and an ease.
- Every frame has an event, reads that fit its length, a breath of 1.5s or less and a frame check.
- The seam map has one primary, one or two accents, and the boldest transition on the hero moment.
- The message is on screen by the end of the second frame.
- Each feature has its proof moment, depicted as a state change.
- All props trace to the terrain; nothing from the generic-avoid list appears.
- Total duration adds up; every scene change is on a bar start; no frame runs on after its last read.
- A fresh reader could build it without asking anything.
