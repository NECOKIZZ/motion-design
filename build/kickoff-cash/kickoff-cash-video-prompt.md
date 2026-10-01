# kickoff.cash · 60s motion design video · build prompt

<!--
  Written with the motion-storyboard skill (house look). Self-contained: a builder needs
  HyperFrames, not the skill. The composition in this folder (index.html + scene3d.js) is the
  build of this prompt; where the two differ, the code is the truth (see "Changes after build").
-->

## 0. Your job

Build this video in HyperFrames exactly as storyboarded. The creative decisions are made: do not redesign, add scenes, add text or swap transitions. If something cannot work, change the smallest thing that fixes it and list it in your hand-off.

Deliverable: `renders/kickoff-cash.mp4`, 1920×1080, 30 fps, 60s, with the music.

## 1. Before writing anything

1. Read the HyperFrames skills `hyperframes`, `hyperframes-core`, `hyperframes-animation` (adapters `gsap.md`, `three.md`).
2. Check the assets in §3 exist. If one is missing, stop and say which.
3. Music: `assets/music.wav` is an original procedural track at a fixed **120 BPM**: pulse 0.5s, phrase `P` = 8 pulses = 4s. `P3.2` = phrase 3, pulse 2 = 13.0s. The structure is built to the storyboard (intro P0–1, groove P2–5, build P6–7 with a riser, a stop at 31.5s, **drop at P8.0 = 32s**, groove P10–12, logo hit at 54s, tail to 60s). Use `at(phrase, pulse)` for every time.

## 2. The video in one paragraph

**Message: "Close still pays."** On yes/no markets a near miss is a loss; kickoff.cash pays by how close you land. **Concept: one call, followed to the end.** A football drops out of the dark onto a glass pitch and the viewer's call appears on a glass ticket: 2-1. The match ends 2-0 and the old way stamps the ticket LOST; the ticket cracks and shatters into the product's own 5×5 scoreline grid in 3D. The full-time tile ignites, light radiates outward by distance, the ball lands on the 2-1 tile next door and it turns green: close still pays. The pool splits by stake × accuracy, the drop floods the frame in signal green with the payout in neon, chips stack up, then Player Perps (call the line) and the leaderboard (beat the pack) prove range, and the ball docks into the K as its dot. **Arc:** call → loss (old way) → turn (hero) → how → payoff (drop) → range ×2 → lockup. **Rhythm:** calm open, tension 8–16, hero hit at 16, build 28–31.5, silence, drop at 32, steady proof, final lock at 54. **Rhyme:** the ball that drops in the first shot is the dot of the logo in the last.

## 3. Brief and assets

- Product: kickoff.cash, proximity markets for EPL fixtures on Robinhood Chain. Pick a scoreline, stake USDC; payouts scale with how close you land; the pool splits by stake × accuracy. Player Perps: call a player's fantasy points line.
- Audience: football fans who already predict scores and bet, crypto-native, on X / Instagram / TikTok.
- Message (on screen at 20.5s): "Close still pays."
- End line: "Beat the pack. Keep the stack." (the site's own tagline)
- CTA: "Enter the markets" · kickoff.cash
- Assets:
  - fonts (local `@font-face` only): `assets/fonts/clash-500/600/700.woff2` (Clash Display), `fraunces-italic.woff2` (Fraunces italic, variable), `inter.woff2` (Inter, variable)
  - logo: `assets/logo-white.svg` (K = bar + diagonal + a circle; never distort or recolour; face #f7f5f0 on dark)
  - footage (user supplied, 640×360 to 854×480, so always inside glass panels or as dark graded backdrops, never full-bleed sharp): `stadium.mp4` (aerial of a stadium), `match.mp4` (a late winner, goal at source 5.45s), `celebrate.mp4` (shirt-swinging celebration), `palmer.mp4` (Cole Palmer knee slide and celebration, broadcast bug cropped off), `crowd.mp4` (flag-waving home end)
  - audio: `music.wav`; `goal-audio.wav` (stadium roar and commentary for the goal); `palmer-audio.wav` (crowd)
  - libs: `assets/lib/gsap.min.js`, `three.module.js` (r170), `RoomEnvironment.js`, `RoundedBoxGeometry.js`

## 4. Look (the house look in kickoff's colours)

- Palette: background `#0b0b0a` (brand ink `#111210`); text pitch cream `#f7f5f0`, muted `rgba(247,245,240,.6)`; **accent purple `#7b62f6`** (deep `#4e3cb5`, tint `#c4b8ff`) for light, selection and the italic word; **signal green `#00c805`** (deep `#008c04`) ONLY for the payoff: your tile turning, the payout flood and numbers, the +$86 chip, the chip stack, the CTA. Loss red `#ff4d6d` only on the LOST stamp. Footage teams' colours appear only inside footage and two tiny team dots.
- Type: Clash Display 600 for captions (76–124px), numbers (92–280px); Fraunces italic for exactly one accent word per caption, tinted `#c4b8ff`; Inter 500/600 for meta labels (22px, uppercase, +0.16em). Sentence case, ≤ 3 words of message on screen at once, no em dashes, scores written with a hyphen "2-1".
- Stage: near-black; five soft vertical curtains of purple light (blurred 70px) drifting slowly; a faint 96px grid masked to the centre; a purple halo behind whatever is in focus; vignette; overlay grain jittering every 0.1s.
- Glass: dark smoked panels, backdrop blur 26px saturate 165%, 1.5px hairline with a brighter top and left edge, inset top highlight, deep shadow. Every glass surface has moving content behind it (curtains, footage). One shine sweep per surface on landing, one star glint where the light exits a corner, a conic rim light idling on the ticket and the pool card.
- 3D (Three.js, rendered on every seek from time): ACES tone mapping, a dim RoomEnvironment for reflections, a purple key spot from the upper left, a cool white rim from behind right.
  - **Football**: a true truncated-icosahedron pattern (12 deep ink-purple pentagons, 20 cream hexagons, dark seams), clearcoat, soft contact shadow.
  - **Glass pitch disc**: dark glossy disc with centre circle, halfway line and spot as purple emissive lines, metal rim.
  - **Scoreline grid (signature sculpture)**: the site's 5×5 score grid as rounded glossy tiles, label on each top face. Full time tile ignites cream with a light pillar; proximity glow travels outward as a wave and fades with distance; your tile turns green.
  - **Stake chips**: green metal chips with a chrome edge band.
  - **The K**: extruded logo, face flat cream exactly the logo colour (unlit), depth in dark glossy metal; the dot is a separate cylinder the ball docks into.

## 5. Motion system

- Energy: medium-high. Entrances 0.3–0.9s, transitions 0.3–0.45s, holds alive with drift.
- Entrance vocabulary: glass rise (y +120, rotationX 20° → 0, perspective 1400, 0.9s expo.out); word blur-up (y 34, blur 14 → 0, 0.5s expo.out, 0.12–0.16s stagger); side snap (x ±80 → 0, power3.out); spring (y 50, scale .96, back.out(1.6)); defocus (blur 10 → 0); flip digit (old rotationX 0 → 90 0.12s power2.in, new −90 → 0 0.2s back.out(2)).
- Ease palette: `expo.out` arrivals, `power3.in` exits and whips, `power3.inOut` reflows, `back.out` stamps and chips, `sine.inOut` ambience.
- Ambient: curtains drift 30s yoyo; panels and cards sway rotationY 2–7° over the act; 3D camera always moving slowly.
- Direction: forward is leftward (new content enters from the right).

## 6. Seam map

| Cut | Time | From → to | Transition | Role | Carried by | Spec |
|---|---|---|---|---|---|---|
| 1 | 8.0 | Call → Match | Whip pan following the kicked ball | primary | the 3D ball (kicked out left from 7.42s, power3.in) | old: canvas, caption, backdrop x 0 → −420, blur 0 → 22px, 0.3s power3.in from 7.7; new: panel x 420 → 0, blur 22 → 0, 0.32s power3.out at 8.0; ticket reflows to the right column (x +260, scale .72, 0.6s power3.inOut from 7.75) |
| 2 | 16.0 | Match → Grid | Shatter + flash into 3D | **hero** | the cracked ticket | cracks draw 15.2–15.65; at 15.86 six clipped copies of the ticket fly out (±700/520px, rotate 25–70°, scale 1.6, blur, 0.42s power3.in, 0.012s stagger); panel zooms through (scale 1.5, blur 14, 0.3s power3.in); white flash .85 at 16.0, out 0.45s; tiles rise beneath |
| 3 | 24.0 | Grid → Pool | Zoom through the 2-1 tile | accent | your tile | 3D camera dives into the tile 23.45–24.1 power3.in; canvas blurs out 0.12s; pool card scale .62 → 1, blur 16 → 0, 0.55s expo.out at 24.05 |
| 4 | 32.0 | Pool → Payoff | Green iris from your bar's tip | **drop** | the "You" fill bar | clip-path circle 0 → 2300px at (916, 620), 0.42s power3.in ending on the drop; swaps to the flood backdrop under the 3D |
| 5 | 40.0 | Payoff → Perps | Whip pan | primary | the chip stack sliding out | same numbers as cut 1 |
| 6 | 48.0 | Perps → Leaderboard | Whip pan into the crowd | primary | — | same numbers as cut 1 |
| 7 | 52.0 | Leaderboard → Lockup | Collapse into the logo | hero close | the rows | rows fly to centre-left, scale .2, 0.32s power3.in, 0.03s stagger; board and caption scale .3; crowd fades; the K turns in |

## 7. Storyboard

### Frame 1 — The call (P0–P2, 0–8s)
- why: every fan has a scoreline in their head; the product starts there.
- **Event:** a ball falls out of the dark and lands on a glass pitch, the pitch lights up, and the viewer's call appears: 2-1.
- **Reads:** 0.3–1.6 a football falls and lands (ripple, glint) · 2.4–4.0 we are at a stadium (aerial fades in behind haze) · 4.0–5.4 a glass ticket: your call is 2-1 · 6.0–7.5 "Call the score."
- **On screen:** ticket ("Your call", "Matchweek 38", Home · Away, "2-1", "Stake 50 USDC"); caption "Call the *score.*"
- **Layout:** disc and ball left of centre; ticket 500×600 at (1220, 236); caption top-left (170, 166), 76px.
- **Motion:** ball drops from y 6.2 at 0.3s with analytic bounces (restitution .42/.36/.30), contacts at 1.11 and 1.83 make purple ripples; pitch lines brighten on contact; stage fades up 0.1–1.9; stadium backdrop opacity 0 → .55, scale 1.08 → 1, 3.2s sine from 2.4; ticket glass rise at P1.0; score blur-pops at P1.2; shine at P1.3 with glints at the top-right corner (+0.62) and bottom-left (+0.2); caption blur-up at P1.4; ticket idle float.
- **Camera:** low hero angle, slow push and drift (0 → 8s linear).
- **Audio:** soft impact on the landing; pads and heartbeat kick.
- **Frame check:** @5.6s ticket sharp, 2-1 legible, ball resting on the disc, stadium visible behind.

### Frame 2 — The match (P2–P4, 8–16s)
- why: the near miss is the problem the product solves.
- **Event:** the match ends 2-0; the yes/no market stamps the 2-1 ticket LOST and it cracks.
- **Reads:** 8.0–9.5 a match is on (big glass broadcast panel) · 10.0 scorebug 1-0, 90+3' · 11.95–12.6 goal, 2-0 · 13.0 FT · 13.3–14.6 the 2-1 ticket is stamped LOST (YES / NO) · 15.2–16.0 it cracks.
- **On screen:** scorebug "HOME 1 - 0 AWAY | 90+3'" → "2 - 0" → "FT"; stamp "YES / NO · LOST".
- **Layout:** panel 1260×740 at (120, 170), slight rotationY 7° → 2°; ticket at right column.
- **Motion:** panel arrives with the whip; bug drops in at P2.2; panel shine P2.1; home digit flips on P3.0 with a purple pulse and glint; clock flips to FT on P3.2; stamp scale 2.3 → 1, rotation −14°, back.out(2.5) landing on P3.3; ticket desaturates (grayscale, brightness .6) and shakes; cracks draw from the impact point at 15.2.
- **Audio:** stadium roar and commentary under the goal (−10 dB), flip ticks.
- **Do not:** name the clubs or players in the footage.
- **Frame check:** @13.8 bug reads 2-0 FT, LOST stamp fully landed on the ticket.

### Frame 3 — Close still pays (P4–P6, 16–24s) · hero
- why: the message, shown as the product's own grid.
- **Event:** the full-time tile ignites, light spreads to its neighbours, the ball lands on 2-1 and it turns green.
- **Reads:** 16.0–17.2 a grid of scorelines rises · 17.95–18.6 2-0 lights up (full time) · 18.45–20.0 light spreads, weaker with distance · 19.35–20.45 the ball lands on 2-1, it turns green · 20.5–23.7 "*Close* still pays." · 21.6–23.7 legend: 2-0 Full time · 2-1 Your call.
- **On screen:** tile labels; caption "*Close* still pays." 124px centred at top over a dark scrim; chips "2-0 Full time", "2-1 Your call".
- **Motion:** tiles rise by distance from centre (0.09s/unit, back.out); camera climbs from a low angle to a 3/4 top view (16–18.6 inOut); full-time tile lifts 0.28 and turns cream with a pillar; proximity wave ring expands from it (18.4–20.6); glow arrives at each tile 0.28s per unit of distance, intensity exp(−d²/2.2); ball drops at 19.35 and bounces; your tile turns from purple to green (20.0–20.45) and lifts.
- **Audio:** impact at 16 on the flash.
- **Frame check:** @21.5 headline readable above the grid, 2-0 cream with dark label, 2-1 green with the ball on it, neighbours purple, far tiles dark.

### Frame 4 — Split the pool (P6–P8, 24–32s)
- why: how "close pays" works, in one picture.
- **Event:** a 12,400 USDC pool splits into bars by stake × accuracy; yours takes 31%.
- **Reads:** 24.1–25.6 a matchday pool, 12,400 USDC · 25.5–27.0 four positions: Exact, You, Close, Far · 26.6–28.5 "Stake x *accuracy.*" · 28.0–29.7 bars fill: 52 / 31 / 17 / 0 · 30–31.5 push towards your row · 31.5–32 silence, your bar gleams.
- **Motion:** card zooms in through the tile; counter 0 → 12,400 (1.3s power2.out); rows enter differently (side snap, spring, opposite snap, defocus); fills on P7.0–P7.3 (0.7s power3.out); card push scale 1 → 1.07 (power2.in) under the riser; row shine at 31.0, glint at 31.35.
- **Frame check:** @29.5 all four rows and percentages readable, "You" row outlined in purple.

### Frame 5 — The payoff (P8–P10, 32–40s) · drop
- why: the signal colour pays off; "keep the stack".
- **Event:** the frame floods green; +$1,284 counts up in neon; chips stack up on the beat.
- **Reads:** 32.0–33.6 your 2-1 call pays +$1,284 · 33.5 burst · 34.0–36.3 chips stack · 35.6–39.7 "Keep the *stack.*"
- **Motion:** flood gradient settles (scale 1.25 → 1, expo.out); payout punch-in (scale 1.6, blur 18 → 0); counter expo.out to 1,284; punch on 33.5 with two glints; 30 deterministic confetti flecks; ten chips land one per pulse from 34.0 (0.2s in, settle); celebration footage as an overlay duotone at 34% under everything; slow zoom 1 → 1.03.
- **Audio:** drop impact, payout chime at 33.

### Frame 6 — Player Perps (P10–P12, 40–48s)
- why: range; the same idea for players.
- **Event:** you call Palmer at 12 points; the final lands on 13; close pays +$86.
- **Reads:** 40.0–41.0 a deck of player cards, Cole Palmer on top (live footage) · 41.0–42.4 "Call the *line.*" · 42.5 your pin: 12 · 43.0–44.5 the result runs 0 → 13 · 44.55–45.5 the gap glows green, +$86.
- **Motion:** deck fans out (−9° / +6°); card sway; shine and glint; line panel glass rise; pin drops with back.out; result pin slides 1.5s power2.inOut with its number counting; arc and chip pop.

### Frame 7 — Beat the pack (P12–P13, 48–52s)
- **Event:** @you climbs from 4th to 1st on the season leaderboard.
- **Reads:** 48.2–49.0 leaderboard over the crowd · 48.5–49.8 "Beat the *pack.*" · 49.6–50.6 your points tick up, your row jumps to #1 and the others shift down.

### Frame 8 — Lockup (P13–P15, 52–60s)
- **Event:** the K turns in and locks; the ball from the first shot flies in and docks as its dot; the CTA is pressed.
- **Reads:** 52.0–54.0 the K turns in · 52.7–54.0 the ball arcs in and docks (impact, streak, glints) · 54.5 "kickoff.cash" · 55.4 "Beat the pack. *Keep the stack.*" · 56.2–57.5 "Enter the markets" is pressed · 57.5–59.1 hold, then fade.
- **Frame check:** @56 logo, wordmark and end line separated, nothing overlapping; @57.5 the button visibly released with a ring.

## 8. Rules for the build (non-negotiable)

- One paused GSAP timeline on `window.__timelines["main"]`; Three.js renders only from `hf-seek` time (no clocks, no rAF loop, no `Math.random`, no `repeat: -1`).
- `fromTo` with explicit start states; `immediateRender: false` on re-animations; transforms, opacity, filter, clip-path, colour only.
- The transition is the exit; only the last frame fades.
- Footage stays inside glass or behind dark grades; never full-bleed and sharp.
- Signal green appears only on payoff elements; red only on the LOST stamp.
- Local fonts and libs only.

## 9. Verify, then hand off

1. `npx hyperframes check .` (the deck, ticket stamp and flip clock overlaps are intentional).
2. `npx hyperframes snapshot . --at <frame checks>` and look at every still.
3. Render a draft, extract a contact sheet at 4 fps and 12-frame strips across each cut; fix; render final.

## Changes after build

- None to the storyboard structure. Coordinates and camera values above were tuned from the first snapshots (grid framed lower under a scrim so the headline reads; full-time tile label turns dark when lit; back player cards made opaque).
