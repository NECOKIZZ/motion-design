# 15 · Pace and flow: when to go fast, when to go slow

The numbers in this file are anchors, not laws. Learn the judgment behind them. It comes from putting two films for the same product side by side (`measured-references.md` §5). One was a rich 3D house-look film at 38s. The other was a flat UI film at 30s that covered twice the features. Viewers found the 3D film laggy and the flat one "on point" for pacing, beat sync, speed and movement. The flat film did not win with more motion. It never made the viewer wait.

## 1. What lag is

**Lag is the viewer finishing before the screen does.** The viewer has read the card, got the joke, seen the number, and the frame is still there. Nothing in the music or the frame tells them why they are waiting.

The opposite failure is **rush**: the next thing arrives before the last one registered. Rush gets the attention but loses the meaning, so the viewer remembers nothing.

Good pace sits on the edge between the two. Each new thing arrives just as the viewer finishes the last one. That is why reads (`13-reads-events-and-acting.md` §1) set every length. When a draft feels slow, the cause is almost never slow tweens. It is time after the reads have ended.

## 2. Three clocks

Music gives three units. Use each for what it is good at.

| Clock | At 120–130 BPM | Use it for |
|---|---|---|
| **Pulse** (one beat) | 0.46–0.5s | when each new element arrives: a word, a list row, a countdown number, a state flip, each piece of the end card |
| **Bar** (4 pulses) | 1.85–2s | **the default scene for one idea**: a claim, a single UI state change, a stat |
| **Phrase** (8 pulses) | 3.7–4s | a scene with two or three state changes (a demo), the hero moment, the end card |

Reference B ran 14 scenes in 30s. Almost every scene was exactly one bar (about 1.9s). Only the "pick a score" demo and the end card took two bars. The 38s film used a phrase or more for every scene (4–10s). Most of those scenes had one or two reads, so the rest of each scene was waiting.

Default: **size a scene to the bar or bars its reads need.** One read plus its words is usually one bar. Never give a scene a phrase just because phrases are tidy.

## 3. Sync at the pulse, not only at the cut

Cutting on phrase starts makes a film *edited*. Landing every arrival on a pulse makes it *on beat*. The 38s film cut on its phrases accurately. Inside each scene, though, arrivals were sparse and uneven (ball at 0.8s, card at 1.4s, headline at 2.4s, then nothing new until the cut at 4s), so the beat had nothing to grip between cuts. Reference B put almost everything on a pulse:

- countdown numbers one per pulse (3 · 2 · 1 · ball)
- YES / NO flipping on every pulse, then struck through on the next
- "Beat" · "the" · "pack." one word per pulse
- three checklist lines, one per pulse
- end card: mark, wordmark, tagline, status pill, CTA button, one per pulse

When a group arrives one item per pulse, **the reading happens during the build**. The viewer reads each item as it lands, so the hold after the last item can be short (0.5–1s). A group that appears all at once must then hold for the whole reading time. That is where waiting comes from.

Small secondary motion (a chip pop, a glint, a neighbour tinting) sits on the half-pulse between main hits. Don't put two main arrivals on the same pulse.

## 4. The hold budget: static camera vs moving camera

A hold is the time after the frame's last arrival. Its length depends on **how much there is to read** and **whether anything is still travelling**.

**Camera static, nothing travelling:** hold only as long as reading takes, then go.
- One short line or one big number, built word by word: 0.4–0.8s.
- Headline plus a simple card: about 1s.
- A dense frame (a 5×5 grid, a leaderboard, a chart with labels): 1–1.5s, the most reference B ever held.
- A URL or CTA the viewer must remember: up to 2s, or longer on an end card that keeps something alive (below).

A static frame does not feel dead in its first second. Stillness after a hit is a breath, and it makes the next hit land. It feels dead once the viewer has finished reading. **If the camera isn't moving, nothing earns extra time. Cut.**

**Camera travelling, or the content still changing:** a little more time is fine, because the viewer is getting something new.
- Typing text, a count-up, live footage, a ticker, a list filling in, a glow growing into a climax. B held its AI-agent card for over a second while the prompt typed itself. That is motion with meaning, so it does not read as a hold.
- A visible travelling push (1 → 1.05–1.1, gathering speed) can carry up to about 1.5s. Not more: a push is not new information.
- Ambient decoration does not count. Drifting curtains, a slow glint crawling along a bar, a bobbing ball or grain can't keep a frame alive by themselves. The 38s film's pool card held for 1.8s with only a glint moving. That was one of the stalls viewers felt.

## 5. When to go slow, when to go fast

Speed is a choice per moment. Contrast between moments is what makes both read.

**Go fast (0.1–0.3s moves, one bar or less):**
- information: UI cards, labels, list rows, chips, headline entrances
- anything the viewer has seen before (a second state of a card already on screen)
- transitions between sections of the same story
- the problem setup and the cold open (the first 3–5s decide whether they keep watching)
- runs of parallel points (three features, three checks): staccato, one per pulse or bar

**Go slow (0.5–1.5s moves, up to a phrase):**
- a reveal with weight: the hero object, the logo assembling, the payoff number
- a build into a drop: a glow swelling, a push accelerating, elements accumulating while the music rises. Slow here is tension, not waiting: it must *accelerate* into the hit.
- a moment of emotion that needs a reaction (the stamp, the twist), and only after the cause has landed
- the last line of the film, so it can register before the end

**Never slow:**
- an element that only carries information sliding in for 0.6s or more
- the set being built before anything happens (a disc sliding into place for a second with nothing to read)
- a still frame placed on a quiet passage in the music. A breakdown is not a pause button. Keep one small thing changing per bar, or start the build.
- exits. Exits are faster than entrances, or there are none: the transition is the exit.

Reference B's moves, read from 10fps strips: masked text rises in about 0.2s, blur-ins in 0.1–0.2s, cards and grids appear in 0.2–0.3s with cells staggered over about 0.4s, count-ups take 0.5s, exits take 0.1–0.2s or are hard cuts. The house look can run 1.5× slower than that on its 3D and glass, but not 3×.

## 6. Fluidity is continuity, not camera moves

Reference B almost never moves a camera, yet it feels fluid. Its flow comes from continuity:

- **A persistent object that changes state on the beat.** One score-grid card stays on screen for four bars. It fills with scores, a cell gets picked with a "$10 on 2-1" chip, the scoreline ticks 1-0 then 2-0, and the near cell turns green: "still paid". Only the headline beside it changes. Changing one object is cheaper for the viewer than meeting a new one, so the film can go faster without losing them.
- **Persistent chrome.** A slim header with the logo and a match clock (14' → 17' → … → 90' → FT) stays across every scene. The clock ticks at each cut, so the whole film plays as one match.
- **Transitions that come from the content and land on the beat:** an iris from the logo's ball, panels that rise as bars from the pool chart, hard cuts on the downbeat, a zoom through the last headline into the end card.
- **Background colour as the section marker:** black → purple → cream → purple → cream → black → purple. A colour flip on a bar is the cheapest scene change there is, and the viewer feels the new section at once.

When you need flow, first reach for an object that carries over, then a carried transition. Use a camera move after those.

## 7. The energy shape of a 30–40s promo

Reference B's shape, which works for most launch promos:

1. **Cold open, fast:** a hook per pulse (countdown, flips) into the logo, all in under 4s.
2. **Problem → turn:** two bars, the old way struck out, the new idea in one line.
3. **Demo:** one persistent object, two to four state changes, one per pulse or half-bar. This is the only stretch where 1–1.5s holds on dense UI are normal.
4. **Proof run, staccato:** one bar per proof, a different set or colour each time.
5. **Build:** the music rises. Grow something (glow, scale, accumulation) and accelerate the camera into…
6. **The drop / payoff:** the boldest transition and the biggest moment.
7. **End card, built per pulse,** then kept alive with real motion (a ticker of crests, confetti, a CTA pulse) for 2–3s.

The middle can be calmer than the edges, but every bar still has an arrival.

## 8. Smells of lag (check the storyboard and the draft for these)

- A scene longer than its reads: its last read ends a second or more before the cut.
- A scene slot sized to a phrase that holds a single idea.
- Elements arriving at times that are not pulses.
- A whole group appearing at once and then holding for its reading time.
- An information element entering in 0.6s or more, or an `inOut` ease on an entrance.
- Opening seconds spent assembling a set before the first read.
- The only motion during a hold is decoration (glint, drift, bob).
- A quiet passage in the music matched with a still frame.
- Things fading out before the transition.
- An end card that freezes for 2s and then fades to black.

## 9. Not a formula

These defaults suit promos and launch clips. A brand film, a trailer or a calm explainer can go slower on purpose. If you choose slow, write down why, and make sure each slow moment still gives the viewer something new to look at. Fast is not the goal. **The goal is no waiting.**
