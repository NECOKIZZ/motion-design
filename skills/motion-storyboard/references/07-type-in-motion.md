# 07 · Type in motion

Text in a motion video is read once, at speed, while things move. Everything here serves readability first, character second.

## 1. How much text, for how long

- At most 2–3 words of a message on screen at once; one line is best, two lines is the limit.
- Reading time: hold a phrase at least **0.3s per word + 0.5s** after it is fully in (a 3-word line holds ≥ 1.4s). A number or URL the viewer must remember holds ≥ 2s.
- Plain language. No em dashes, no semicolons, no jargon the audience would not use.
- One idea per phrase. Split long sentences into beats.

## 2. Type roles and sizes (1920×1080)

| Role | Size | Weight | Use |
|---|---|---|---|
| Hero / slam word | 160–280px | 700–900 | one word, the beat's payload |
| Headline | 96–160px | 600–800 | 2–4 word lines |
| Sticker / label | 40–64px | 600–700 | chips, pills, UI callouts |
| Body / caption | 32–44px | 400–500 | rare; supporting lines |
| Meta | 20–28px | 400–500 | tiny labels, numbers, coordinates (justify it) |

Tracking: tighten big type (−0.02 to −0.04em); loosen small caps (+0.04 to +0.1em). Line height 0.9–1.05 for headlines. Use the brand's fonts only, vendored locally (`@font-face` to a file), and say so in the storyboard.

## 3. Kinetic type techniques

| Technique | How | Use |
|---|---|---|
| **Word slam** | each word enters on a beat with a *different* entrance (scale slam, side snap, drop, rise); see `04-motion-language.md` §15 | punchy hooks (rule `kinetic-beat-slam`) |
| **Mask rise** | each line in an `overflow: hidden` wrapper; text `y 105% → 0`, 0.5–0.7s `expo.out`, 0.06–0.1s per line | editorial, premium |
| **Sliced letters (measured, Zajno)** | each letter is cut into horizontal slices that rise from a baseline mask at different offsets, then align; 0.4–0.6s total | big titles over imagery |
| **Letter stagger** | per-character y/opacity/blur, 0.03–0.05s apart | names, short words |
| **Tracking collapse** | letter-spacing from 0.5em → final while fading in; or exit by tracking out + scaleY squash (measured, Zajno) | elegant entrances and exits |
| **Inline media chips (measured, Zajno)** | small image pills appear inside a sentence between words, scaling from 0 | editorial storytelling |
| **Highlight / marker** | an accent block or underline draws behind a key word, 0.3s | emphasis (rule `css-marker-patterns`) |
| **Word swap** | a fixed line, one slot hard-cuts through options, lands on the answer | "for X, for Y, for you" |
| **Typewriter** | characters on with a caret, 0.03–0.05s per char, optional backspace | prompts, search, chat |
| **Scramble / decode** | characters cycle through glyphs (index-seeded, never random) before resolving | privacy, tech, hashes (rule `hacker-flip-3d`) |
| **Counter** | numbers count up, scale grows with value | stats (rule `counting-dynamic-scale`) |
| **Split-flap** | digits flip like a station board | scores, times, prices |
| **Text as mask** | huge type cut out of a panel shows the image or video behind | brand moments |
| **Zoom through a letter** | camera flies into a letter's counter into the next scene | transitions |
| **Gradient / chrome sweep** | a highlight travels through the glyphs once | premium emphasis (see `08-materials-and-light.md`) |

## 4. Rules

- Every word or chip in a sequence enters differently from its neighbour, but the *group* shares a logic (all from the left with rising speed, or each from a different edge in clockwise order).
- Big words land on strong beats; small words on weak beats or offbeats.
- The accent colour goes on one word per beat at most: the one that carries the claim.
- Text is never animated by `width`, `font-size` or `letter-spacing` layout tweens when a transform can do it; letter-spacing is acceptable on short words because it is a paint-only change in practice, but test it.
- Exits: faster than entrances, or covered by the transition.
