# 12 · Self-review, and what the prompt tells the builder

§1 is for you, before handing the prompt over. §2–§4 are what the prompt's build-rules and verification sections (§8–§9 in `templates/video-prompt.md`) must tell the builder; adapt them to the project and copy them in.

## §1 Self-review the prompt (before handing it over)

Read the prompt as a critic, then once more as the builder: could you build every frame from it without asking anything? Fix every "no" before presenting.

**Stands alone**
- [ ] Could a fresh Opus session without this skill build it? No references to this skill's files, no "as discussed", every term explained or specified with numbers.
- [ ] Every asset listed with its path; the BPM assumption and how to re-derive times stated?
- [ ] Build rules (§8) and verification steps (§9) present and adapted to this project (its bans, its materials, its safe zones)?

**Story**
- [ ] Is the message a claim, and is it on screen by the end of frame 2?
- [ ] Delete every proof frame: does the rest still state the value? Delete the value frames: does it collapse into a feature tour? (It should.)
- [ ] Does every feature have a proof moment shown as a state change?
- [ ] Would the video read as this product with the logo covered?

**Motion**
- [ ] Every element: verb, from → to values, duration, ease?
- [ ] Entrances `.out`, exits `.in`, moves `.inOut`?
- [ ] No more than two tweens per frame share an ease? Durations vary (slowest ≈ 3× fastest)?
- [ ] Neighbouring words/chips enter differently?
- [ ] Each frame has a breath of 1.5s or less, with the camera travelling through it? Decorative ambience quieter than action?
- [ ] One scene per phrase (two only for the hero and the drop)? Does any frame have time left after its last read? Shorten it.
- [ ] First motion of each frame within 0.1–0.3s, not at 0?

**Transitions**
- [ ] One primary for most cuts, accents for topic changes, boldest on the hero moment?
- [ ] Each transition carried by an object, with direction, timing, eases, and the new scene's first frame described?
- [ ] No fade-outs before transitions? No plain crossfades between scenes?
- [ ] Velocity matched (out `.in`, in `.out`, peak at the cut)?

**Reads and events**
- [ ] Every frame has an event (different at the end than the start), with cause then reaction?
- [ ] Every frame lists its reads, none overlapping, each long enough to land? Does the last read of the film have time?
- [ ] No word labels what the picture already shows?
- [ ] Does the ending rhyme with the opening?

**Frame**
- [ ] ≤ 3 words of message on screen at once, held ≥ 0.3s/word + 0.5s?
- [ ] Two focal points, three depth layers, one accent per frame?
- [ ] Text sizes at video scale; nothing under 24px without a reason?
- [ ] Materials have a light event; glass has moving content behind it?

**Music**
- [ ] Every scene change on a phrase start; impacts arrive 1–2 frames early?
- [ ] The hero moment on the drop; a held frame before or after it?
- [ ] End card holds 1.5–2s?

## §2 Build from the storyboard (builder instructions)

1. Read the HyperFrames skills first (`hyperframes`, `hyperframes-core`, `hyperframes-animation`), then build. `references/hyperframes-map.md` lists the building block for each storyboard term.
2. Project: `npx hyperframes init <dir> --non-interactive --resolution landscape|portrait|square`. Vendor fonts and GSAP into `assets/` (CDN loads can fail behind proxies).
3. Music first: add the audio, run `npx hyperframes beats .`, put the beat times in a constant, write the `at(phrase, pulse)` helper. Every time in the code comes from the helper.
4. One sub-composition per frame (or one file with scene wrappers for short pieces); one paused timeline; global camera rig and background layer built once.
5. Build frame by frame in storyboard order. Within a frame, **block the key poses first** (the storytelling states at the frame's key times) and check them as stills before animating between them. If the key poses don't read, motion won't fix them.
   For long pieces, write a short production guide (shared helpers, the camera rig, the palette, the rules, how to check work) and build acts in parallel, one file per act, each act painting its whole frame as a pure function of time. Do not redesign: if something in the storyboard does not work, change the storyboard first and say why.
6. After each frame: `npx hyperframes check .`, then fix every error. Common causes: a wipe panel left covering the frame (many contrast errors at once); intentional overlaps need `data-layout-allow-overlap` / `data-layout-allow-occlusion`; opaque scene backgrounds making push/zoom transitions show blank (paint backgrounds on the root or the world).

GSAP pitfalls that lint will not catch:
- `fromTo` everywhere; `immediateRender: false` on any `fromTo` that is not the element's first appearance (otherwise its "from" state is applied at build time and corrupts earlier frames).
- Never two concurrent transform tweens on one element (entrance + camera drift): split across a wrapper and a child.
- Ambient loops on the timeline, never bare `gsap.to`; finite repeats only.
- Move with `x`/`y`, never `left`/`top`.

## §3 Render, look, fix (builder instructions, 2–3 rounds)

1. Render a draft: `npx hyperframes render -o out/draft.mp4`.
2. Extract the frame-check stills and transition midpoints:
   ```bash
   # one still per frame-check timestamp
   for t in 3.1 6.2 10.2 11.6; do ffmpeg -v error -y -ss $t -i out/draft.mp4 -frames:v 1 out/check-$t.png; done
   # transition close-up: 12 frames across a cut at T
   ffmpeg -v error -y -ss $(echo "T-0.2"|bc) -t 0.4 -i out/draft.mp4 -vf "fps=30,scale=480:-2,tile=6x2" out/cut.png
   # contact sheet of the whole film, 4 fps
   ffmpeg -v error -y -i out/draft.mp4 -vf "fps=4,scale=320:-2,tile=8x8" out/sheet.png
   ```
   Review at three zoom levels: **sheet** (first/middle/last of every frame: the shape of the piece), **strip** (every frame of a key moment: takes, stamps, transitions, ~0.4–0.6s), **crop** (full-resolution detail: faces, text, contacts, glows). Read timing like a viewer: step through a sheet at 0.1–0.15s intervals and ask at each frame where the eye is and whether the current read has landed; count the frames each read gets.
3. Look at every image. Compare each still against its frame check. Typical faults:
   - Text overlapping a device or another word; text clipped at a safe margin.
   - A word still mid-entrance at its check time (entrance too slow or late).
   - Two things moving at once where one should lead.
   - A transition midpoint that shows a blank frame or a flash of the old scene.
   - Fallback font (wrong letterforms), wrong colour, logo distorted or under minimum size.
   - Glass that looks like a flat tinted box (nothing moving behind it).
   - Twinning: two things entering or moving identically at the same moment.
   - A read that gets only a few frames, or shares frames with another read.
   - Text that labels what the picture already shows.
   - Dead frames: any stretch over 1.5s where only ambience moves. Measure it: `python3 recipes/motion-profile.py out/draft.mp4` prints the still share and every quiet run of 1s or more. Aim for no quiet run over 1.5s and fix the longest runs first. The still share is secondary: slow travelling pushes register as near-still, so a well-paced film can still read about 40%.
4. Fix, re-render, re-check. Two or three rounds is normal.
5. Hand over: the file path, duration, resolution, the stills you checked, and what you could not verify (audio feel, motion smoothness at full frame rate).

## §4 Updating the storyboard after the build

When the build is final, the code is the truth. Update the prompt file's times and any changed decisions so the storyboard matches the video, and note the changes at the top under `## Changes after build`.
