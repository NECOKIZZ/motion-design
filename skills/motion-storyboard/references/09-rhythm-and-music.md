# 09 · Rhythm and music

Sync to music is the single biggest quality jump in a motion video. The viewer feels a cut that lands on the kick drum even if they never notice it; a cut a few frames off feels sloppy.

## 1. Get the grid first

1. Put the track in `assets/` and reference it as `<audio id="music" data-timeline-role="music" src="assets/music.mp3">`.
2. Run `npx hyperframes beats .` → a beat file with `beats: [{ time, strength }]` (strength ≈ 1 = strong).
3. Read it: tempo (BPM), the pulse length (60 / BPM), where strong beats fall, where sections change (density jumps, drops, breakdowns).
4. If the analysis reports low confidence, snap to the evident grid and ignore off-grid hits.

No music supplied: ask whether to proceed with a placeholder. Never use a reference video's audio. Always say the track is a placeholder.

## 2. Think in phrases, not beats

Music is grouped: 4 beats make a bar; 2 or 4 bars make a phrase (often 8 pulses). Strong hits (strength ≈ 1) usually mark phrase starts.

- **Scene changes land on bar starts; section changes on phrase starts.** Size each scene in bars by its reads: one idea is usually one bar (about 2s at 120–130 BPM), a demo with several state changes or the end card a phrase. (Measured: a 128 BPM launch film ran 14 one-bar scenes in 30s and felt on point; the same product's 38s film with phrase-or-longer scenes felt laggy. `measured-references.md` §5.)
- **Arrivals land on pulses:** one new thing per pulse (a word, a row, a flip, a chip), then a short breath, then the next bar hits. Pulse-level sync is what makes a film feel on beat; cutting on phrases alone only makes it feel edited. (Fast promo references: 210 BPM, phrase every 8 pulses ≈ 2.29s, breath about 0.85s.)
- **Flams** (two hits ~0.1s apart): main impact on the first, a secondary settle (badge, shadow, shake decay) on the second.
- **Follow the build:** when the track gets denser toward the end, put the demo climax and end card there and cut faster.
- **The drop** is the hero moment's slot. In the 1–2 bars before it, build: fewer new elements, but something growing and accelerating into the hit.

## 3. Address time by music, not seconds

Write every time in the storyboard as a music position and resolve it to seconds once:

```
P3.0  = phrase 3, pulse 0  (strong)  = 4.57s
P3.2  = phrase 3, pulse 2            = 5.14s
P3.6  = start of breath
```

In the build, put the beat times in a constant and place everything through a helper:

```js
const BEATS = [/* from the beat file */];
const at = (phrase, pulse = 0, nudge = -0.033) => BEATS[phrase * 8 + pulse] + nudge; // arrive 1 frame early
tl.fromTo("#word1", {...}, {...}, at(3, 2));
```

Never time an element by a hand-typed number that is not derived from the grid.

## 4. What lands where

| Music event | Gets |
|---|---|
| Phrase start (strong) | section change, the bolder transitions |
| Bar start | scene change for a one-idea scene |
| Downbeat inside phrase | a word slam, a card landing, a state change |
| Offbeat / hi-hat | small secondary motion: chips, glints, a shadow settle |
| Snare / clap | impact: stamp, shake, punch-in |
| Bass drop | the hero moment, the boldest transition, flash |
| Riser / build | accumulating elements, a glow or scale growing, a push that accelerates into the drop; slow here must speed up, never stall |
| Breakdown / quiet | fewer, smaller moves (one change per bar), the one line that must be read; never a still frame for the whole passage |
| Final hit | logo lock; end-card pieces arrive one per pulse (mark, wordmark, tagline, CTA), then 1.5–2s with something real still moving (ticker, particles, CTA pulse) while the music resolves |

Impacts *arrive* on the beat: start the tween so its landing frame is the beat (or 1–2 frames before). For a 0.2s slam, the tween starts ~0.17s early.

## 5. Audio mix (if voiceover or SFX)

- Music bed under voiceover: ~14 dB below the voice; total ≈ −16 LUFS for social.
- SFX only if licensed; mixed low; whoosh into transitions, thud on stamps, pop on badges, ping on notifications.
- Fade the music out over the last 1–2s unless the track ends on a hit.
- HyperFrames audio mixing: `/hyperframes-audio` (fades, ducking, automation).

## 6. Rhythm without music

Use a fixed tempo anyway (e.g. 120 BPM → 0.5s pulse, 8-pulse phrase = 4s). Rhythm is what makes a silent video feel edited rather than assembled.
