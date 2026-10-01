# Measured references

Numbers measured from real work, so defaults in this skill are grounded rather than guessed. Learn the **craft** (timing, easing, construction), never copy the **content** (stories, props, copy, scene order).

Add a section per new reference: what it is, how it was measured, the numbers, what to take from it.

## How to measure a reference video

```bash
# overview: 20 evenly spaced frames
ffmpeg -i ref.mp4 -vf "fps=20/DURATION,scale=360:-2,tile=5x4" sheet.jpg
# close-up of one moment at 10–30 fps
ffmpeg -ss 7.4 -t 2.4 -i ref.mp4 -vf "fps=10,scale=300:-2,tile=6x4" closeup.jpg
# beats of its music (put the audio in a HyperFrames project as the music track)
npx hyperframes beats .
```
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

## 3. Your references

(Add the user's reference videos here as they are analysed: what each is, the numbers, the techniques worth borrowing.)
