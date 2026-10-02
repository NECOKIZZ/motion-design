# Measured references

Numbers measured from real work, so defaults in this skill are grounded rather than guessed. Learn the **craft** (timing, easing, construction), never copy the **content** (stories, props, copy, scene order).

Add a section per new reference: what it is, how it was measured, the numbers, what to take from it.

## How to measure a reference video

```bash
# overview: 20 evenly spaced frames
ffmpeg -i ref.mp4 -vf "fps=20/DURATION,scale=360:-2,tile=5x4" sheet.jpg
# close-up of one moment at 10–30 fps
ffmpeg -ss 7.4 -t 2.4 -i ref.mp4 -vf "fps=10,scale=300:-2,tile=6x4" closeup.jpg
# timestamped 10fps strip of a 3s stretch, to read when each element arrives (times relative to -ss)
ffmpeg -ss 9 -t 3 -i ref.mp4 -vf "fps=10,scale=256:-2,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=14:fontcolor=red,tile=10x3" -frames:v 1 strip.jpg
# beats of its music (put the audio in a HyperFrames project as the music track)
npx hyperframes beats .
```
Whole-frame motion numbers miss small arrivals (a word, a chip) and can't tell an on-beat film from an off-beat one. For pace and sync, read the strips by eye and write down the arrival times.
Per-frame motion energy (mean absolute difference between consecutive grey frames) gives motion event durations, the share of time the frame is still, and where in each move the speed peaks (early peak = ease-out, middle = ease-in-out). A Python script that does this is in `recipes/motion-profile.py`.

## 1. Zajno: motion.zajno.com (UI/web motion principles)

A studio site teaching eight interface-motion techniques: easing, offset and delay, fade, transform/morph, masking, dimension, parallax, zoom. 40 example clips measured (2026-10-01).

**Numbers**
- Web/UI motion is slower than promo motion: median element motion **0.6–1.4s**; quick UI moves 0.3–0.5s.
- Lots of stillness: in site showcases the frame is still **35–60%** of the time. Motion is punctuation, not wallpaper.
- Speed peak sits near the middle of most moves (median ≈ 0.45 of the move): ease-in-out curves for things moving between positions; arrivals use ease-out.
- The "missing easing → correct easing → correct delay" lesson series lengthens moves from ~0.33s to ~0.5s as easing and stagger are added: good easing usually needs a little more time, not less.

**Techniques seen (craft to borrow)**
- *Letterbox slit transition:* black bars close top and bottom until the scene is a thin strip; the next image lives inside the strip; a title rises above it in sliced letters (each letter in horizontal slices arriving at different offsets).
- *Hairline collapse:* an image collapses to a 2px line from the bottom while the next layout is already there.
- *Text exit by tracking out + vertical squash + fade.*
- *Slit-open images:* images open as narrow vertical slits that widen, with stepped, puzzle-like corner masks.
- *Inline media chips:* tiny images appear between words of a sentence.
- *Exploded axonometric view:* a product's parts separate, one highlights, parts reassemble.
- *Active-list highlight:* a list (LUNCH / WORK / REST) where the active word is solid and the others are outlined/grey; the active state steps down the list.
- *Bookending:* the closing frame mirrors the opening frame.
- *Paper collage:* cut-out photos, pie charts and doodles on light paper with grain; colour panels rise to introduce chapters.
- *Floating doodles around a product:* line-art icons orbit and pop around a photographed hero (PS5 promo).

## 2. Fast product-launch promo (social, 15–20s)

From the Kickoff project's reference analysis (two launch videos by one creator; 210 BPM; light theme).

- Pulse 0.286s; strong hit every 8 pulses = **2.29s**; every scene change on a strong hit.
- Inside a phrase: one new thing per pulse on pulses 1–5, then a **~0.85s breath** (the music drops out) before the next hit.
- Sticker word: opacity 0, blur ~12px, scale ~1.08, rotation −3°, offset ~30px → sharp in **0.13s (4 frames)**, then settles to a ±1–2° tilt over ~0.3s.
- Hero wordmark: letters slam **0.1s apart**, each from a different oversized, skewed (−15°) position.
- Cards: fly up from below at −12° rotation, settle at ±2–4° in ~0.3s with slight overshoot.
- Transitions: diagonal two-tone wipe ~0.25s; circle iris ~0.17s; dark → light blur-dissolve ~0.25s; collapse-into-logo match cut ~0.3s.
- Layout: product UI on one side, words on the other, alternating sides; UI ~25–35% of frame width; lots of empty space; reflow when new content arrives.

## 3. "I'm Upping My P(doom)" music video (Claude Opus 5.5, 156s)

Source: github.com/JohnHeibel/PDoomVideo, and the author's follow-up starter kit github.com/JohnHeibel/ClaudeAnimationBase, whose guide was written from "an analysis of what the model did and didn't do well". Every frame is code: p5.js + p5.brush watercolour painted in headless Chrome, frames rendered in parallel, encoded with ffmpeg. Studied 2026-10-01 from the repos (storyboard, animation guide, code).

**What it did right that this skill now captures** (details in `13-reads-events-and-acting.md`):
- *A concept with a twist:* "a stage show that goes off the rails", opening and closing on the same painted curtain; the last line reveals the apocalypse was a play.
- *Rule for every shot:* something happens: a character does something, something breaks, transforms, chases or falls.
- *Text-light:* jokes told with pictures and acting; a handful of sound-effect words in the whole film; no labels, no captions repeating the lyric.
- *Sets, not cards:* each chapter happens in one place the camera moves through; the four choruses return to the same stage and escalate.
- *A diegetic prop:* the P(doom) meter is a thermometer on stage that the character pumps each chorus (8 → 34 → 61 → 86 → 99.9), cracks, and finally pops like a balloon.
- *A cast with acting:* a hero (Clawd) that grows across the film, a human foil, guest characters who return for the curtain call; mood changes are acted (squint, squash-stretch take, emote pop) never snapped.
- *Motivated transitions:* brush wipes only at chapter breaks; inside chapters the action carries the cut (a chomp to black, a fall, a zoom through an eye, a heart bubble popping, a bomb flash, crashing through a floor, a door slam).
- *Palette arc:* warm cream → sky → space violet and gold → steel and jazz blue → data-centre teal → alarm red → back to warm theatre crimson.
- *Literalised lines:* every lyric became a physical gag (training loss "drop" = sledding down the loss curve; "sharp left turn" = a go-kart hairpin that flings the foil off).
- *A real medium:* hand-painted watercolour with boiling linework (seeded jitter re-rolled 12×/s), paper grain and vignette.

**Numbers**
- Shots 1.4–4s, one focal action each; lead character ~40% of frame height in dance shots; 88 BPM, every hit on a beat.
- Character size guide: medium shot unit u ≈ 20–28 (character 8u tall); close-up 40–70; tiny (< 12) only in establishing shots.
- Render budget: ≤ 2.5s per frame, never more than ~4s.

**Process worth copying**
- Two generations: a first pass, then a storyboard rewritten with a style direction ("P5 brushstrokes, make each scene visually interesting, make every scene transition into the next"), then the final build.
- A written production guide (`ANIMATION_GUIDE.md`) briefed parallel subagents: one chapter per file, every shot a pure function of time, a shared character API (pose, face, hats, emotes, dances), shared helpers they must not edit, and how to check work.
- Review with contact sheets at chosen times, strips of every frame around a hit, and crops of faces; for each shot check the first and last frames and every 0.1s around hits.
- The author notes that the reasoning level tracks how extravagant and detail-oriented the result is; their test videos used the highest setting.

## 4. House-look promo pacing: one film at 60s and at 38s

The same 3D/glass football promo (house look, 120 BPM), built at two paces and measured with `recipes/motion-profile.py` plus a quiet-run pass (frame difference < 0.6 on 160×90 grey frames, runs ≥ 1s).

| | 60s cut (8s scenes) | 38s cut (4s scenes) |
|---|---|---|
| Scene length | 8s each | 4s each; 6s for the match and the hero |
| Quiet runs ≥ 1s | 5, longest 5.5s (a pool card filling, then a slow push) | 3, longest 2.0s |
| Viewer verdict | "slow, stalls in particular scenes" | right pace on its own; laggy next to a 30s flat cut (§5) |

**Take from it**
- Scenes sized to whole phrases by default (8s) left 3–5s holds wherever the reads ended early. One phrase per idea improved it; §5 shows one bar per idea goes further.
- A 1.02–1.03 drift over a 3–5s hold reads as stopped. Holds need a visible travelling push (1.05–1.1) that gathers speed into the cut.
- The still-share number stays near 40% even when the pace feels right, because slow pushes register as near-still. Judge by the quiet runs (none over ~1.5–2s), not the share alone.

## 5. Flat UI launch film vs the 38s house-look film (same product, side by side)

Another designer's 30s launch film for the same football prediction market. Flat UI on solid colour fields (black, purple, cream), serif headlines, almost no camera moves. Placed next to the 38s cut from §4, viewers judged it better for pacing, beat sync, speed and movement, though the 3D film looked richer. Measured from 10fps timestamped strips plus beat tracking, 2026-10-02. Its copy came to us as a 480p WhatsApp re-encode, so small timings are ±0.1s.

| | Flat 30s film | House-look 38s film |
|---|---|---|
| Tempo | ~128 BPM (pulse 0.47s, bar 1.88s) | 120 BPM (pulse 0.5s, bar 2s) |
| Scenes | 14; 12 of them one bar (1.6–2s); the demo and the end card two bars | 6; 4–10s each |
| Arrivals inside a scene | one per pulse: countdown 3·2·1·ball; YES/NO flip per pulse; "Beat"·"the"·"pack." per pulse; three checklist lines per pulse; end card mark·wordmark·tagline·pill·CTA per pulse | sparse and uneven, e.g. ball 0.8s, card 1.4s, headline 2.4s, then nothing new until the 4s cut |
| Information entrances | masked rise ~0.2s, blur-in 0.1–0.2s, card 0.2–0.3s, grid cells staggered over ~0.4s, count-up ~0.5s | card slide ~0.6s, words ~0.4s; 3D set assembles over the first ~0.8s before any read |
| Exits | 0.1–0.2s or hard cut | mostly carried by transitions |
| Longest still holds | ~1–1.5s, only on dense UI just after it lands (5×5 grid, leaderboard); ~0.6s after a word-by-word line | 1.3s on one card + one line (opening); 2.0s after "Close still pays" (3D grid static); 1.8s on the pool card with only a glint moving; quiet music passage matched with a static card |
| What keeps longer moments alive | typing (AI prompt), count-ups, a crest orbit, a scrolling crest ticker and confetti on the end card | live footage (works); decoration (glints, curtain drift) elsewhere (doesn't) |
| Continuity | one score card stays for 4 bars and changes state on beats (fill → pick + chip → score ticks 1-0, 2-0 → near cell turns green "still paid"); a header with a match clock ticking 14' → FT across every scene; background colour flips per section | each scene a new set; transitions carried by objects (ball, iris, zoom) |
| Transitions | 0.1–0.25s: iris from the logo dot, wipe-up, chart bars rising as panels, hard cuts on the downbeat, a slide, light → dark cut, a zoom through the last headline with a flash into the end card | 0.3–0.6s, mostly carried by 3D objects |

**Take from it** (written up as judgment in `15-pace-and-flow.md`)
- The bar, not the phrase, is the default scene for one idea. Phrase-sized scenes with one or two reads are where the lag lived.
- Sync arrivals to pulses, not just cuts to phrases. The 38s film's cuts were on the grid, yet it felt loose because nothing between cuts was.
- When items arrive one per pulse the viewer reads during the build, so the hold after can be short.
- A static frame is fine for as long as the viewer is reading, and no longer. Dense frames earn ~1.5s; a single line earns well under a second.
- Fast for information, slow only for weight and builds. The flat film's single slow moment is a green glow swelling under the last claim, and then it accelerates into the zoom-through.
- Flow without camera moves comes from continuity: a persistent object changing state, persistent chrome, colour flips per section.
- Learn the craft, not the content: the house look stays the default. Borrow the pace, not the flat style or the copy.

## 6. Your references

(Add the user's reference videos here as they are analysed: what each is, the numbers, the techniques worth borrowing.)
