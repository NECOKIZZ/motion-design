# Kickoff · 30s motion design video · build prompt

<!--
  Written with the motion-storyboard skill. Hand this whole file to Claude Code (Opus) in the
  project folder that holds the assets below and say:
  "Build the video in kickoff-30s-video-prompt.md."
  It is self-contained: the builder needs HyperFrames, not the motion-storyboard skill.
-->

## 0. Your job

Build this video in HyperFrames exactly as storyboarded below. The creative decisions are made: do not redesign, add scenes, add text or swap transitions. If something in the storyboard cannot work, change the smallest thing that fixes it and list the change in your hand-off.

The bar is **perfect, smooth, futuristic**: glass that really refracts, 3D that really has depth, light that really travels, and a lot of calm white space. Smoothness beats busyness. If a moment looks cluttered, remove the extra element instead of shrinking things to fit.

Deliverable: `renders/kickoff-30s.mp4`, 1920×1080, **60 fps**, 30s, with the music. (Check `npx hyperframes render --help` for the fps flag; if 60 fps is not supported, render 30 fps and say so.)

## 1. Before writing anything

1. Read the HyperFrames skills: `hyperframes`, `hyperframes-core`, `hyperframes-animation` (install with `npx hyperframes skills update` if missing). They are the authority on how to build; this file is the authority on what to build.
2. Check these assets exist. If one is missing, stop and say which.
   - `assets/fonts/ClashDisplay-Semibold.woff2`, `assets/fonts/ClashDisplay-Medium.woff2` (Fontshare, free licence)
   - `assets/fonts/Fraunces-Italic-VariableFont.ttf` or `Fraunces-Italic.woff2` (Google Fonts, OFL)
   - `assets/fonts/Inter-Medium.woff2` (Google Fonts, OFL; UI labels only)
   - `assets/logo.svg`: if missing, create it from this exact markup (the official mark from kickoff.cash, never redrawn):
     ```svg
     <svg viewBox="0 0 500 502" xmlns="http://www.w3.org/2000/svg">
       <circle cx="400" cy="100" r="100" fill="#000000"/>
       <path d="M150 0L500 502H327.5L150 251.5V500H0V0H150Z" fill="#000000"/>
     </svg>
     ```
     It has two parts: the **K** (the path) and the **ball** (the circle). The film depends on animating them separately, so keep them as two elements with ids `#logo-k` and `#logo-ball`.
   - `assets/music.mp3`: a clean, modern electronic track (airy pads, crisp percussion, one clear drop). No vocals.
3. Music first: put the track in the composition as `<audio id="music" data-timeline-role="music" src="assets/music.mp3">`, run `npx hyperframes beats .`, and read the beat grid. The storyboard gives times as music positions `P<phrase>.<pulse>` (phrase = 8 pulses) with the seconds they resolve to at an **assumed 120 BPM** (pulse 0.5s, phrase 4.0s). **Re-derive every time from the measured grid** with a helper:
   ```js
   const BEATS = [/* beat times from the beat file */];
   const at = (phrase, pulse = 0, nudge = -0.017) => BEATS[phrase * 8 + pulse] + nudge; // land 1 frame early at 60fps
   ```
   If the measured tempo differs, keep the phrase structure and let the seconds move. If the track's drop is not near P4, tell me before building.

## 2. The video in one paragraph

Message: **"Closeness pays."** (Kickoff is a prediction market for Premier League football where you call the exact scoreline and get paid on how close you land, not just yes or no.) End line: **"Beat the pack. Keep the stack."**

**Concept: "The ball is the result."** The ball from the Kickoff logo is the spine. It starts as the knob of an old YES/NO switch, escapes it, and becomes the final score of a match: a glowing hyacinth sphere sitting in a vast white space. Every prediction is a glass tile that lands at its *distance* from the ball, on soft glowing rings that ripple out like a radar of closeness. A ring sweeps out to the median; everything inside it lights up, everything outside frosts and falls away into depth. The losing stakes flow into the winners as light, and the exact call's stack rises tallest, glowing green. At the end every tile is pulled back into the ball, the ball flies home to its place on the K, and the logo locks. The film opens and closes on the same image: one glowing ball in white space.

- **Spine:** the ball (persistent object), plus a colour rule: **hyacinth = Kickoff's system** (ball, rings, logo light), **neon green = money you keep** (it appears only on winnings, nowhere else).
- **Signature moments:** (1) the median ring sweeps out and splits the pack into lit and frosted. (2) On the drop, the losing stakes stream into the winners and the exact call's stack rises: "+232%".
- **Rhythm:** `hook-TURN-proof-SIGNATURE-PEAK-trust-SIGNOFF`; peak at P4 (16.0s) on the drop; the held breath is the end of Frame 6.
- **Feel:** futuristic, editorial, premium. White space is the material. Think a luxury watch launch crossed with a trading terminal, never a betting ad.

### Terrain (where every prop and transition comes from)

| Object | Native motion | Device | Transition | Proves |
|---|---|---|---|---|
| The ball (logo dot) | rolls, glows, is the result | glowing hyacinth sphere at the centre of every scene | **ball iris / ball carry**: the ball moves and the next scene opens from it | everything orbits the result |
| YES/NO switch | flicks between two states | glass toggle whose knob is the ball | the toggle track stretches into a distance line | "not just yes or no" |
| Scoreline | flips, locks | "2–1" in glass and as giant ghost numerals | numerals scale through camera | exact scorelines |
| Distance rings | ripple outward | thin glowing concentric rings around the ball | **ring wipe**: a ring expands past the frame edge and the next scene is inside it | closeness is measured |
| Prediction tiles | land, light, frost | glass tiles with a scoreline each | tiles carried into the next scene | the pack |
| Median gate | sweeps once | one brighter ring sweeping to the median distance | — | the closer half wins |
| The stack | rises | stacked glass discs with green light | — | keep the stack |

Signature props: the ball, the distance rings, the glass prediction tiles, the stack.
Avoid: dice, roulette, slot machines, casino chips, gold coins, cash notes, betting slips, footballer photos, stadium photos, a pitch texture, crowd noise, generic rising line graphs, "BET NOW" energy.
Native transition: the ring wipe (primary) and the ball carry (accent).

## 3. Brief and assets

- Product: Kickoff (kickoff.cash), proximity prediction markets for every Premier League fixture. Call the final scoreline, stake USDC, and the pool pays on how close you land. Built on Robinhood Chain.
- Audience: football fans and prediction-market traders on X, Instagram and YouTube who find yes/no betting crude and like skill, numbers and clean tech.
- Proof (from kickoff.cash/docs, do not change these numbers): match ends **2–1**; picks **2–1, 1–0, 3–1, 1–1, 0–2** at $10 each; the median gate means only **2–1** and **1–0** win; the exact call returns **+232%**, the near call **+38%**. Fee: **10% of losing stakes only**. No house: your counterparty is the pool.
- Message (lands by the end of Frame 2): "Closeness pays."
- End line: "Beat the pack. Keep the stack."
- CTA: **kickoff.cash** · "Join the waitlist"
- Brand voice (from the brand book): competitive, technical, direct, confident. Aesthetic: editorial sportswear, vibrant tech-minimalism, digital pitch logic, high-stakes sophistication, data-driven energy.
- Assets: as listed in §1.2. Fonts only via local `@font-face`; the logo is never distorted, re-proportioned or redrawn.

## 4. Look

- **Palette (brand book, exact):**
  - Chalk White `#F7F5F0`: the main background (warm, premium).
  - Pure White `#FFFFFF`: glass highlights, light, the brightest whites.
  - Jet Black `#000000`: type and the logo. Use `#111210` for large type if pure black looks harsh on chalk (it is the site's ink colour).
  - Hyacinth Blue `#7B62F6`: the accent. Kickoff's system only: the ball, the rings, glows, the logo light, one word per frame at most.
  - Neon Green `#00C805`: **money you keep, only** (the stack, "+232%", "+38%"). Nowhere else.
  - Allowed tints: hyacinth deep `#4E3CB5` (3D extrusion sides, ring shadows), hyacinth light `#A897FF` (glow cores), hyacinth wash `rgba(123,98,246,.08–.18)` (blobs), green glow `rgba(0,200,5,.25)`.
  - Banned: red, orange, yellow, any other blue, gold, any dark full-frame background. The film is a light film.
- **Type:**
  - Headlines: **Clash Display Semibold**, 120–170px, tracking −2%, black on chalk.
  - Editorial accent (one word or phrase per frame, the emotional word): **Fraunces Italic** 300–400 weight, same size as the headline it sits in. Example: "Closeness *pays.*" with "pays." in Fraunces Italic hyacinth.
  - Numbers (scorelines, percentages): Clash Display Medium, tabular, 72–480px.
  - Labels and UI: Inter Medium 30–40px, black at 70%.
  - Never more than 3 words of a message on screen at once. No em dashes.
- **Glowing letters:** hero words get a hyacinth glow built from layered `text-shadow` (`0 0 6px rgba(123,98,246,.55), 0 0 22px rgba(123,98,246,.35), 0 0 60px rgba(123,98,246,.18)`) that **blooms in** after the letters land (opacity of a glow-copy layer 0 → 1, 0.5s `power2.out`), never permanently on everything. The accent word also gets a gradient sweep through the glyphs (`background-clip: text`, stops `#4E3CB5 → #7B62F6 → #FFFFFF → #7B62F6`, `background-position` 100% → 0%, 1.4s `power2.inOut`, one pass).
- **Medium / material: glass + light on white.** One primary treatment, glass, used consistently:
  ```css
  .glass {
    background: linear-gradient(135deg, rgba(255,255,255,.62), rgba(255,255,255,.22));
    -webkit-backdrop-filter: blur(26px) saturate(180%);
    backdrop-filter: blur(26px) saturate(180%);
    border: 1.5px solid rgba(255,255,255,.85);
    border-bottom-color: rgba(123,98,246,.22);
    border-radius: 36px;
    box-shadow: inset 0 1.5px 0 rgba(255,255,255,.95),
                inset 0 -18px 36px rgba(123,98,246,.06),
                0 30px 60px -20px rgba(78,60,181,.28),
                0 8px 18px -8px rgba(0,0,0,.10);
    overflow: hidden;
  }
  ```
  Light glass on a light background only reads if something coloured with edges is behind it. **Every glass surface in this film has hyacinth blobs, rings or ghost numerals drifting behind it.** If a glass tile ever looks like a white box, the thing behind it is missing.
- **The ball (hero object):** a CSS sphere, not a flat circle. Layers: base `radial-gradient(circle at 34% 30%, #FFFFFF 0%, #A897FF 18%, #7B62F6 48%, #4E3CB5 100%)`; a specular highlight (small white ellipse, blur 6px, top-left); a rim light (thin `#FFFFFF` crescent bottom-right at 40%); an outer glow (`radial-gradient` hyacinth 35% → 0, 1.8× its size); a contact shadow (soft ellipse beneath, only when it sits on something). The specular highlight stays fixed relative to the light (top-left) while the ball moves, so it reads as a lit 3D sphere.
- **3D:** CSS 3D only (`perspective: 1600px`, `transform-style: preserve-3d`), no WebGL needed. The K gets real depth with stacked extrusion layers (rule `3d-text-depth-layers`): 14 copies of `#logo-k` behind the face, each 2px further back in z, coloured `#4E3CB5` fading to `#7B62F6`, face in black (or white on the hyacinth flash in Frame 2). Glass tiles enter with rotationX/rotationY and flatten to ≤ 6° to be read.
- **Background layer (every scene):** chalk `#F7F5F0` + a very soft mesh of 3 hyacinth blobs (1,100–1,300px, `rgba(123,98,246,.10–.16)`, container `filter: blur(110px)`, `inset: -200px`) drifting with transforms only + grain overlay at 5% (`feTurbulence` tile, `mix-blend-mode: multiply`) to kill banding. Keep at least **55% of every frame visually empty** (chalk or soft blob only).
- **Light events:** a shine sweep on every glass tile as it lands (one pass, soft-light); glints on corners timed to sweeps; a rim light circling the median ring once; one anamorphic hyacinth streak behind the logo lock. Specified per frame.

## 5. Motion system

- **Energy:** controlled and fluid, never frantic. Entrances 0.5–0.9s; transitions 0.6–0.8s; camera moves 1.5–4s. Fast actions only on the peak (Frame 5). Smoothness rules: no linear eases on anything visible except ambient drift; no element ever stops dead (every arrival has a 2–4% settle); no hard cuts.
- **Entrance vocabulary:**
  - FLOAT IN: y +90, rotationX 18°, blur 10px, opacity 0 → 0, 0°, 0, 1 · 0.9s `expo.out` (glass)
  - MASK RISE: y 105% → 0 inside an overflow-hidden line, per word 0.06s stagger · 0.7s `expo.out` (headlines)
  - GLOW BLOOM: glow layer scale 0.6 → 1, opacity 0 → 1 · 0.6s `power2.out` (always 0.15s after the letters land)
  - DEPTH LAND: z −600, scale 0.7, blur 14px → z 0, scale 1, blur 0 · 0.8s `expo.out` (tiles arriving from far away)
  - ROLL: the ball travels along a path with rotation matched to distance (rotation = distance / radius in rad) · `power3.inOut`
  - RIPPLE: a ring scale 0.2 → 1, opacity 0 → 1 → 0.6 · 1.2s `power2.out`
  - COUNT UP: integers only · `power2.out`
  - RISE STACK: discs scale-y-free; each disc y +40, opacity 0 → 0, 1, 0.05s stagger · 0.35s `back.out(1.4)`
- **Ease palette:** `expo.out` (arrivals) · `power3.inOut` (camera, reflow, ball travel, wipes) · `power2.in` (outgoing into a cut) · `back.out(1.4)` (stack discs only) · `sine.inOut` (ambient). At most two tweens in a beat share an ease.
- **Ambient rule:** every hold has drift; blobs drift at 0.3× (x/y ±40px over 6–8s, `sine.inOut`); tiles bob y ±4px with phases offset by index (never in unison); the ball breathes (glow scale 1 → 1.06 → 1, 2s). Consecutive scenes never share the same camera drift direction.
- **Camera rig:** `.stage` (perspective 1600px) > `.world` (the camera) > `.bg` (0.3×: blobs, ghost numerals) · `.mid` (1×: ball, tiles, words) · `.fg` (1.4×: light streaks, glints, out-of-focus near particles blurred 12px). Entrances on elements; camera moves on `.world` only.
- **Depth of field:** in any frame with 3D depth, objects pushed back in z get blur proportional to depth (z −300 → 6px, z −600 → 12px). The subject is always sharp.
- **Direction rule:** the ball always leads. The first thing that moves in each frame is the ball or something the ball causes.

### Beat grid (assumed; replace with the measured grid)

| Phrase | Start | Section |
|---|---|---|
| P0 | 0.0 | intro |
| P1 | 4.0 | intro 2 |
| P2 | 8.0 | verse |
| P3 | 12.0 | build |
| P4 | 16.0 | drop (peak) |
| P5 | 20.0 | drop 2 / settle |
| P6 | 24.0 | outro (music fades 28.5–30.0) |

Pulse k of phrase p = p × 4.0 + k × 0.5 s.

## 6. Seam map (every transition, specified once; frames refer here)

| Cut | Time | From → to | Transition | Role | Carried by |
|---|---|---|---|---|---|
| 1 | P1.0 4.0s | Hook → Turn | Ball carry: the ball rolls off the stretched line and up into its place beside the K | accent | the ball |
| 2 | P2.0 8.0s | Turn → Result | Ball iris: camera dives into the ball; its hyacinth core opens into the result scene | accent | the ball |
| 3 | P3.0 12.0s | Result → Median gate | Continuous: no cut; the camera pulls back 15% and tilts in 3D (same set, new act) | continue | the ring field |
| 4 | P4.0 16.0s | Gate → Stack (peak) | Ring wipe: the median ring expands past the frame edge; inside it, the stack scene | primary (boldest) | the median ring |
| 5 | P5.0 20.0s | Stack → Trust | Ring wipe (softer): a ring ripples out from the stack's top disc | primary | a ring |
| 6 | P6.0 24.0s | Trust → Sign-off | Collapse into the ball, the ball flies home to the K | hero | the three glass panels and the ball |

Velocity matching on every cut: outgoing side accelerates (`.in`), incoming decelerates (`.out`), peak speed on the cut, landing on the phrase start. The transition is the exit; nothing fades out before a cut.

### Bans

- No slideshow: every cut is carried by the ball or a ring.
- No screensaver: ambient motion is always quieter than the action.
- No fades between scenes; no dark scenes; no gambling imagery; no player photos; no green except money kept; no red; no em dashes; never more than 3 words of message at once; never distort the logo.

## 7. Storyboard

### Frame 1 — Hook: yes or no?

- time: P0.0–P1.0 (0.0–4.0s)
- role: hook (the old way)
- why: Names the thing every other prediction market does (binary yes/no) so the turn has something to break.
- transition_in: cold open from chalk

**Event:** a YES/NO switch flicks back and forth, then its knob refuses the choice and escapes along a line.
**Reads:**
- 0.3–1.4 a glass switch in white space: YES / NO (the knob is a glowing ball)
- 1.5–2.5 "Yes or no?" (the question)
- 2.5–3.9 the knob pops out of the switch and rolls away along a line that stretches across the frame: there's more than two answers
**On screen (verbatim):** "YES" · "NO" (on the switch, Inter 34px) · "Yes or no?"
**Layout:** chalk, vast white space. Glass switch centred at (760, 540), 520×180, radius 90; labels "YES" left, "NO" right inside the track. "Yes or no?" left-aligned at x 160, y 300, 140px Clash Semibold black. Right 50% of the frame empty except the soft blobs.
**Depth:** BG chalk + blobs (0.3×) · MG switch, words · FG none (keep it pure).
**Material/light:** switch = `.glass` (radius 90); knob = the ball (150px). Shine sweep across the switch at 0.9s.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| 0.2s | switch | FLOAT IN | as vocabulary | 0.9s | expo.out | |
| 0.4s | ball (knob) | DEPTH LAND | into the YES side | 0.8s | expo.out | glow blooms 0.1s before it lands |
| 0.9s | switch | SHINE | band x −300 → 820 | 0.8s | power2.inOut | glint on top-right corner at 1.5s |
| P0.3 (1.5s) | "Yes or no?" | MASK RISE | per word | 0.7s | expo.out | "or" in Fraunces Italic |
| P0.3 | ball | FLICK | YES → NO (x +340) | 0.35s | power3.inOut | squash 1.08×0.94 at the end, recover 0.2s |
| P0.4 | ball | FLICK | NO → YES | 0.3s | power3.inOut | faster: impatience |
| P0.5 (2.5s) | ball | POP OUT | lifts out of the track (y −60, z +120, scale 1.15) | 0.4s | expo.out | the switch dips y +6 as if released |
| P0.6 (3.0s) | switch track | STRETCH INTO LINE | the track's glass morphs into a 4px hyacinth line extending right to the frame edge (scaleX 1 → 4 on a separate line element; the glass body fades its opacity 1 → 0 under the line) | 0.6s | power3.inOut | morph, not a fade: the line grows out of the track |
| P0.6+0.1 | ball | ROLL | along the line to x 1500 | 0.9s | power2.in | accelerating into the cut |

**Camera:** `.world` drift x 0 → −20px (none).
**Audio cue:** soft tick on each flick; airy whoosh as the ball pops out.
**Transition out:** cut 1. The ball, at peak speed, rolls off the line's right end and curves up (arc: x power2.out, y power3.inOut) to land top-right where the logo's ball sits in Frame 2; the line and "Yes or no?" are pushed out left by the camera truck (`.world` x −1920, 0.7s `power3.inOut`, starting P1.0 − 0.35s).
**Do not:** no red/green YES/NO colours (YES/NO stay black on glass); no betting slip; no question mark slam.
**Frame check:**
- @1.2s: switch reads as glass (blobs visibly blurred through it), ball sits on YES with a highlight.
- @2.3s: "Yes or no?" fully risen; ball on YES; 50%+ of frame empty.

### Frame 2 — Turn: Kickoff, and the message

- time: P1.0–P2.0 (4.0–8.0s)
- role: turn (brand) + message
- why: The ball that refused yes/no is Kickoff's ball; the brand names the alternative and states the claim.
- transition_in: cut 1 (ball carry)

**Event:** the ball lands on the K and the logo locks in 3D; the claim appears.
**Reads:**
- 4.0–5.2 the K turns in 3D and the ball clicks into place: it's the Kickoff logo
- 5.2–6.0 "Kickoff"
- 6.2–7.9 "Closeness pays." (the message; "pays." glows hyacinth)
**On screen (verbatim):** logo · "Kickoff" · "Closeness pays."
**Layout:** chalk. Logo left-of-centre at (700, 500), 300px tall. "Kickoff" to its right at x 920, 150px Clash Semibold. At P1.5 the logo slides left to x 420 and scales to 220px (reflow) and "Kickoff" is replaced by "Closeness pays." (two lines, x 700, y 420 and 580, 160px).
**Depth:** BG chalk + blobs + ghost giant "K" outline (stroke 2px hyacinth 10%, 1100px tall, 0.3×) · MG logo, words · FG one anamorphic hyacinth streak (1.4×).
**Material/light:** K = 3D extrusion (14 layers, §4) with black face; ball = the CSS sphere scaled to the logo's circle (r = 100/500 of the logo width). Anamorphic streak (900×3px hyacinth gradient, 60% opacity) crosses behind the logo when the ball locks.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P1.0 | K (with its extrusion stack) | TURN IN 3D | rotationY −70°, rotationX 12°, z −300 → 0, 0, 0 | 1.0s | expo.out | extrusion sides visible during the turn; DOF blur 8 → 0 |
| P1.1+0.1 (4.6s) | ball | SETTLE INTO PLACE | arrives from cut 1 onto the logo's circle position; scale 1.06 → 1 | 0.35s | back.out(1.4) | the K dips y +4 on contact (0.2s) |
| P1.2 (5.0s) | anamorphic streak | CROSS | x −600 → +600 behind the logo | 0.6s | power2.out | |
| P1.2 | "Kickoff" | MASK RISE | per letter, 0.04s stagger | 0.6s | expo.out | |
| P1.4 (6.0s) | "Kickoff" | EXIT UP | y 0 → −105% | 0.25s | power2.in | |
| P1.4 | logo | REFLOW | x 700 → 420, scale 1 → 0.73 | 0.5s | power3.inOut | same beat as the exit |
| P1.4+0.1 | "Closeness" | MASK RISE | | 0.7s | expo.out | black |
| P1.5 (6.5s) | "pays." | MASK RISE + GLOW BLOOM + GRADIENT SWEEP | Fraunces Italic hyacinth; glow blooms +0.15s; one gradient pass 1.4s | 0.7s | expo.out | the brightest thing on screen |
| P1.6–7 | — | BREATHE | ball breathes; blobs drift | — | sine.inOut | |

**Camera:** `.world` scale 1 → 1.03 (none), slight rotationY −2° → 0 (3D parallax with the ghost K).
**Audio cue:** a deep, soft "lock" on the ball settle; shimmer on the glow bloom.
**Transition out:** cut 2. Camera dives into the ball: `.world` scale-to-target around the ball's centre (rule `coordinate-target-zoom`), 1 → 14, 0.7s `power2.in`, starting P2.0 − 0.45s; at the cut the frame is filled by the ball's hyacinth-to-white core; Frame 3 opens from it (`clip-path: circle()` 0% → 150% from the same point, 0.6s `expo.out`) with the core shrinking back into Frame 3's ball.
**Do not:** never let the ball arrive anywhere but the exact logo position; never flatten the K to look 2D at rest (keep rotationY −8° at rest for depth, face fully legible).
**Frame check:**
- @5.6s: logo sharp, 3D extrusion visible on the K's right side, ball has specular highlight; "Kickoff" fully in.
- @7.6s: "Closeness pays." readable, "pays." in Fraunces Italic with glow; nothing overlapping the logo.

### Frame 3 — Proof: the result and the pack

- time: P2.0–P3.0 (8.0–12.0s)
- role: proof (feature: exact scorelines, measured by closeness)
- why: Shows how Kickoff thinks: the result is a point, every pick has a distance from it.
- transition_in: cut 2 (ball iris)

**Event:** the result locks at 2–1, rings ripple out, and five picks land at their distances.
**Reads:**
- 8.0–9.0 the ball shows "2–1": the final score (giant ghost "2–1" behind confirms it)
- 9.0–10.0 rings ripple out from it: distance
- 10.0–11.5 five glass tiles land on the rings, one by one: the pack, near and far
- 11.5–12.0 hold
**On screen (verbatim):** "2–1" (on the ball and ghost) · tiles "2–1", "1–0", "3–1", "1–1", "0–2" · "Call the score." (headline)
**Layout:** chalk. Ball at (1160, 540), 200px, with "2–1" in white Clash Medium 64px on its face. Ghost "2–1" 520px tall, hyacinth 7%, behind at (1160, 540), 0.3×. Rings: 5 thin rings (1.5px, hyacinth 30% → 10% outward) at radii 140, 264, 277, 411, 464. Tiles (glass, 200×120, radius 28, scoreline 64px Clash Medium black, a tiny "$10" Inter 26px under it):
  - "2–1" docks on the ball's top edge, centre (1160, 410)
  - "1–0" at (905, 472)
  - "3–1" at (1428, 612)
  - "1–1" at (869, 831)
  - "0–2" at (1392, 138)
  Headline "Call the score." left column x 150, y 470, 130px. Left 35% stays white apart from the headline.
**Depth:** BG chalk + blobs + ghost "2–1" (0.3×) · MG ball, rings, tiles · FG 6 tiny out-of-focus hyacinth particles (1.4×, blur 10px).
**Material/light:** glass tiles over the rings and ghost numerals (that is what they blur). Each tile gets one shine pass as it lands; glint on the "2–1" tile when it docks.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P2.0 | ball | SHRINK FROM IRIS | full frame core → 200px | 0.6s | expo.out | |
| P2.1 (8.5s) | "2–1" on ball | SCORE LOCK | digits flip from "0–0" → "1–0" → "2–0" → "2–1" (vertical ticker, rule `vertical-spring-ticker`) | 0.6s | power3.out | lands on P2.2 |
| P2.1 | ghost "2–1" | FADE UP + SCALE | scale 1.2 → 1, opacity 0 → 0.07 | 1.2s | power2.out | |
| P2.2 (9.0s) | rings 1–5 | RIPPLE | inner to outer, 0.1s stagger | 1.2s | power2.out | each ring then idles (opacity breathing ±0.05) |
| P2.3 (9.5s) | "Call the score." | MASK RISE | per word | 0.7s | expo.out | "score." in Fraunces Italic |
| P2.4 (10.0s) | tile "2–1" | DEPTH LAND → DOCK | z −600 → 0 onto the ball's top | 0.7s | expo.out | ball pulses scale 1 → 1.05 → 1 on contact; ring 1 flashes white |
| P2.4+0.25 | tile "1–0" | DEPTH LAND | from upper-left | 0.7s | expo.out | |
| P2.4+0.45 | tile "3–1" | FLOAT IN | from below-right | 0.8s | expo.out | different entrance on purpose |
| P2.4+0.65 | tile "1–1" | DEPTH LAND | | 0.7s | expo.out | |
| P2.4+0.85 | tile "0–2" | FLOAT IN | from above | 0.8s | expo.out | arrives last, farthest |
| each tile land +0.2 | tile | SHINE | one pass | 0.6s | power2.inOut | glint on "2–1" tile corner at +0.45s |
| P2.7 | — | BREATHE | tiles bob ±4px offset phases | — | sine.inOut | |

**Camera:** `.world` slow orbit: rotationX 0 → 8°, rotationY 0 → −6° over the frame (power2.inOut). The rings are drawn on a plane so the orbit makes them read as a 3D floor; tiles stay facing camera (counter-rotate so text stays ≤ 6° off).
**Audio cue:** ticker clicks on the score lock; one soft ping per tile landing, rising pitch.
**Transition out:** cut 3 (continuous). No cut. The camera keeps orbiting into Frame 4.
**Do not:** no team names, crests or player faces; no football pitch texture; tiles never overlap the headline.
**Frame check:**
- @9.4s: "2–1" locked on the ball, ghost "2–1" faintly visible, rings rippling.
- @11.7s: five tiles at their positions, all legible, glass visibly blurring the rings behind them, headline in, left 35% clean.

### Frame 4 — Signature: the median gate

- time: P3.0–P4.0 (12.0–16.0s)
- role: signature moment 1 (how winners are chosen)
- why: The single idea that makes Kickoff different: the closer half wins. Shown as one ring sweep.
- transition_in: cut 3 (continuous)

**Event:** a bright ring sweeps out to the median; the pack splits into lit and frosted.
**Reads:**
- 12.0–13.0 a brighter ring starts sweeping out from the ball (something is being measured)
- 13.0–14.0 it stops just past "1–0" and before "3–1": the line between winning and not
- 14.0–15.2 inside: "2–1" and "1–0" light up; outside: three tiles frost and sink back into depth
- 15.2–16.0 "Closer wins." (build in the music, tension before the drop)
**On screen (verbatim):** "Closer wins."
**Layout:** same set as Frame 3. The headline "Call the score." is replaced in place by "Closer wins." (same position).
**Depth:** losing tiles move to z −400 (blur 8px, opacity 0.45, saturate 0 so they turn grey glass); winning tiles move to z +60 (closer to camera, sharper shadow).
**Material/light:** median ring: 3px, white core with hyacinth glow (`box-shadow 0 0 18px #7B62F6`), plus a rim-light highlight travelling once around it (conic gradient, 1 turn in 1.6s, `none`). Winning tiles gain a hyacinth inner glow and a hyacinth border (`rgba(123,98,246,.6)`).

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P3.0 | median ring | SWEEP OUT | scale from radius 100 → 270 (between 1–0 at 264 and 3–1 at 277) | 1.6s | power3.inOut | slows into its stop: suspense |
| P3.1 | rim light on median ring | ORBIT | rotation 0 → 360° | 1.6s | none | |
| P3.4 (14.0s) | tiles "3–1", "1–1", "0–2" | FROST + SINK | z 0 → −400, blur 0 → 8px, opacity → 0.45, saturate → 0 | 0.6s | power2.inOut | stagger 0.08s by distance (nearest first) |
| P3.4 | tiles "2–1", "1–0" | LIFT + LIGHT | z 0 → 60, border → hyacinth, inner glow 0 → 1 | 0.5s | expo.out | "2–1" brighter than "1–0" (glow 1.0 vs 0.5) |
| P3.4+0.1 | "Call the score." | EXIT UP | y → −105% | 0.25s | power2.in | |
| P3.5 (14.5s) | "Closer wins." | MASK RISE | per word | 0.7s | expo.out | "wins." Fraunces Italic hyacinth + GLOW BLOOM |
| P3.6–7 | — | BUILD | camera push-in continues; ring glow pulses on P3.6 and P3.7 | — | sine.inOut | tension |

**Camera:** `.world` continues the orbit back to rotationX 4°, rotationY 0, and pushes in scale 1 → 1.08 toward the ball (power2.inOut), anticipating the drop.
**Audio cue:** a rising tone under the ring sweep that resolves when it stops; muted "tick" as tiles frost.
**Transition out:** cut 4 (primary, boldest). Starting P4.0 − 0.4s, the median ring expands from radius 270 to past the frame corners (scale × 9, 0.55s `power2.in`); the frosted tiles are swept outward with it (fg 1.4×). Inside the ring's edge Frame 5 is revealed (`clip-path: circle()` tied to the ring's radius). At the cut the ring's glowing edge passes the frame corners exactly on the drop.
**Do not:** never show distance numbers (1.25, 1.50) on screen; the picture shows it. No red on the losers (grey frost only).
**Frame check:**
- @13.8s: median ring visibly between "1–0" and "3–1", rim highlight on it.
- @15.4s: two lit tiles sharp and forward, three grey tiles blurred back, "Closer wins." readable.

### Frame 5 — Peak: beat the pack, keep the stack

- time: P4.0–P5.0 (16.0–20.0s)
- role: proof (payout scales with closeness) + signature moment 2 (on the drop)
- why: The payoff: the closer you land, the more you keep. Exact pays most.
- transition_in: cut 4 (ring wipe)

**Event:** the losing stakes stream in as light; the exact call's stack rises tallest and counts up in green.
**Reads:**
- 16.0–16.8 two glass tiles, "2–1" and "1–0", stand on glass pedestals (the winners)
- 16.8–18.0 streams of light pour into both; "2–1"'s stack rises much higher
- 18.0–19.0 "+232%" counts up in green over "2–1"; "+38%" over "1–0"
- 19.0–19.9 "Keep the stack."
**On screen (verbatim):** "2–1" · "1–0" · "+232%" · "+38%" · "Keep the stack."
**Layout:** chalk. Two stacks right half: "2–1" stack at x 1300, "1–0" stack at x 1620, both rising from a baseline at y 900. Each stack = glass discs (240×44, radius 22, stacked 8px apart with slight perspective, rotationX 60° seen from above-front). "2–1": 12 discs; "1–0": 3 discs. Tile on top of each stack. Percentages above tiles, 96px Clash Medium green `#00C805` with green glow. "Keep the stack." left column x 150, y 520, 150px, "stack." Fraunces Italic hyacinth.
**Depth:** BG chalk + blobs + three faint frosted grey tiles far back (z −800, blur 14px, drifting out of frame: the pack you beat) · MG stacks, tiles, numbers · FG light particles streaming (1.4×).
**Material/light:** stack discs are glass with a hyacinth edge light; they glow green from inside as they fill (inner `box-shadow` green 0 → 0.35). Light streams: 24 small capsules (8×36px, gradient white → hyacinth → transparent) travelling on curved paths from the far grey tiles into the stacks (deterministic angles from index). One shine sweep up the "2–1" stack when it finishes rising. Three glints on the top disc edge.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P4.0 | world inside the ring | SETTLE | scale 1.1 → 1 | 0.6s | expo.out | the drop hits |
| P4.0+0.05 | both tiles + base discs | DEPTH LAND | from the positions they held in Frame 4 (carried) | 0.6s | expo.out | |
| P4.1 (16.5s) | light streams | STREAM | 24 capsules along arcs into the stacks, index-staggered 0.03s; 18 go to "2–1", 6 to "1–0" | 1.2s | power2.inOut | motion-blur streak on each (rule `motion-blur-streak`) |
| P4.2 (17.0s) | "2–1" stack | RISE STACK | 3 → 12 discs | 0.9s | back.out(1.4) per disc | tile rides up on top |
| P4.2+0.1 | "1–0" stack | RISE STACK | 1 → 3 discs | 0.4s | back.out(1.4) | smaller, quicker |
| P4.4 (18.0s) | "+232%" | COUNT UP | 0 → 232 | 1.0s | power2.out | green, GLOW BLOOM after landing |
| P4.4+0.2 | "+38%" | COUNT UP | 0 → 38 | 0.6s | power2.out | |
| P4.5 | "2–1" stack | SHINE + GLINTS | band bottom → top; glints at +0.3, +0.42, +0.5s | 0.7s | power2.inOut | |
| P4.6 (19.0s) | "Keep the stack." | MASK RISE | per word | 0.7s | expo.out | |
| P4.6+0.15 | "stack." | GLOW BLOOM + GRADIENT SWEEP | | 1.2s | power2.out | |
| P4.7 | — | BREATHE | stacks bob ±3px offset | — | sine.inOut | |

**Camera:** punch-in 1 → 1.08 at P4.2 (0.25s expo.out) as the "2–1" stack starts to rise, then ease back to 1.02 over 1.2s (power2.inOut); slight rotationY 4° → 0 so the stacks read as 3D.
**Audio cue:** the drop at P4.0; rising shimmer under the stream; a clean chime when "+232%" lands.
**Transition out:** cut 5. A ring ripples out from the top disc of the "2–1" stack (scale 0 → past the frame, 0.6s `power2.in`, starting P5.0 − 0.35s); Frame 6 is revealed inside it.
**Do not:** no coins, no dollar bills, no "$" icons flying; no green anywhere except the percentages and the stack glow; never change +232% or +38%.
**Frame check:**
- @17.4s: light streams mid-flight, "2–1" stack visibly taller than "1–0".
- @19.6s: "+232%" and "+38%" final values in green, "Keep the stack." readable, at least 50% of the frame white.

### Frame 6 — Trust: how it stays fair

- time: P5.0–P6.0 (20.0–24.0s)
- role: proof (fairness, coverage) + held frame
- why: Removes the doubts a trader has (who is the house, what's the fee, which matches) and gives the breath before the sign-off.
- transition_in: cut 5 (ring wipe)

**Event:** three glass panels land in a row; a single light passes across all three.
**Reads:**
- 20.4–21.2 panel 1: "No house." (an empty ring where a house would be: just the pool)
- 21.2–22.0 panel 2: "10% of losers" with a small label "Winners pay 0"
- 22.0–22.8 panel 3: "Every EPL match" with a small "Robinhood Chain · USDC" label
- 22.8–24.0 held frame: the light passes; nothing new to read
**On screen (verbatim):** "No house." · "10% of losers" · "Winners pay 0" · "Every EPL match" · "Robinhood Chain · USDC"
**Layout:** chalk. Three glass panels (480×520, radius 40, gap 56) centred, y 540, slight fan in 3D (rotationY −10°, 0°, +10°, then all ease to −4°, 0°, +4°). Each panel: an icon at top (built from rings and the ball: panel 1 = ring with small balls on it = the pool; panel 2 = a ring with a 10% arc highlighted in hyacinth; panel 3 = a grid of 10 small dots = 10 fixtures a matchweek), headline 64px Clash Semibold black, label Inter 32px at 70%. Behind the panels: the ghost word "FAIR" 600px hyacinth 7%, drifting x at 0.3×.
**Depth:** BG chalk + blobs + ghost "FAIR" · MG panels · FG glints.
**Material/light:** `.glass` panels over the ghost word and blobs. One shine sweep across all three panels at P5.5 (one band passing behind/through each, timed by x). Glints on each panel's top-right corner as the band exits it.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P5.0 | ghost "FAIR" | FADE UP | opacity 0 → 0.07, x +80 → 0 | 1.5s | power2.out | |
| P5.1 (20.5s) | panel 1 | FLOAT IN | from below | 0.9s | expo.out | its icon ring draws (svg-path-draw, 0.6s) |
| P5.2+0.1 (21.1s) | panel 2 | DEPTH LAND | from z −500 | 0.8s | expo.out | its 10% arc fills hyacinth (0.5s) |
| P5.3+0.2 (21.7s) | panel 3 | FLOAT IN | from above (y −90, rotationX −18°) | 0.9s | expo.out | its 10 dots pop in 0.03s stagger |
| P5.5 (22.5s) | shine band | SWEEP | x −500 → 2100 across all panels | 1.0s | power2.inOut | soft-light |
| P5.5+0.3/+0.55/+0.8 | glints | GLINT | on each panel's top-right corner, sizes 1, 0.7, 0.5 | 0.5s life | power3.out / power2.in | timed to the band |
| P5.6–7 | — | HELD FRAME | only blobs, ghost word, panel bob ±3px | — | sine.inOut | the breath before the sign-off |

**Camera:** `.world` x +20 → −20 and rotationY 2° → −2° (none), opposite to Frame 5's drift.
**Audio cue:** three soft glass taps on the panel landings; airy shimmer on the sweep.
**Transition out:** cut 6 (hero). Starting P6.0 − 0.5s, the three panels fold toward the centre and shrink into a single point (scale → 0.05, rotationY → 0, 0.04s stagger, 0.45s `power2.in`), the point becomes the ball (glow flashes white 0.1s); the ball then flies (arc, 0.6s `power3.inOut`) to its place on the K in Frame 7.
**Do not:** no shield-with-check icon; no lock icon; no text smaller than 32px on glass; contrast ≥ 4.5:1 on every label.
**Frame check:**
- @22.9s: all three panels in, glass visibly blurring "FAIR", every word readable.
- @23.2s: shine band mid-way across panel 2, one glint visible.

### Frame 7 — Sign-off

- time: P6.0–end (24.0–30.0s)
- role: sign-off + CTA
- why: The ball returns home: the opening image resolved into the brand, the line and where to go.
- transition_in: cut 6 (collapse into the ball)

**Event:** the ball flies home, the logo locks in 3D, the line lands, the URL appears.
**Reads:**
- 24.0–25.3 the ball lands on the K: the Kickoff logo, in white space
- 25.3–27.0 "Beat the pack." then "Keep the stack."
- 27.0–30.0 "kickoff.cash" and "Join the waitlist" (final read gets 3 seconds; nothing new after it)
**On screen (verbatim):** logo · "Beat the pack." · "Keep the stack." · "kickoff.cash" · "Join the waitlist"
**Layout:** chalk, the emptiest frame of the film (≥ 65% white). Logo centred at (960, 380), 240px tall, rest angle rotationY −8°. Lines centred, y 610 ("Beat the pack.") and y 740 ("Keep the stack."), 110px Clash Semibold, "stack." in Fraunces Italic hyacinth with glow. URL pill at y 910: glass pill 520×96 with "kickoff.cash" 44px Clash Medium black and a small hyacinth ball (24px) at its left; "Join the waitlist" Inter 30px at 70%, y 985.
**Depth:** BG chalk + blobs + one large faint ring (radius 700, hyacinth 8%) centred on the ball (it rhymes with the distance rings) · MG logo, lines, pill · FG anamorphic hyacinth streak behind the logo.
**Material/light:** 3D extruded K (as in Frame 2); the CSS sphere ball; one shine sweep across the K's face; two glints on the ball; glass pill.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P6.0 | K | TURN IN 3D | rotationY 60° → −8°, z −400 → 0 (from the opposite side to Frame 2) | 0.9s | expo.out | extrusion visible |
| P6.0+0.35 | ball | LAND | arrives from cut 6 onto the logo circle | 0.35s | back.out(1.4) | K dips y +4; big faint ring ripples out once (1.2s power2.out) |
| P6.1 (24.5s) | anamorphic streak | CROSS | x −700 → +700 | 0.6s | power2.out | |
| P6.2+0.3 (25.3s) | "Beat the pack." | MASK RISE | per word | 0.7s | expo.out | |
| P6.3+0.4 (26.0s) | "Keep the stack." | MASK RISE | per word | 0.7s | expo.out | "stack." GLOW BLOOM + GRADIENT SWEEP |
| P6.6 (27.0s) | URL pill | FLOAT IN | from below | 0.8s | expo.out | its small ball rolls in from the left (0.6s) |
| P6.6+0.3 | "Join the waitlist" | MASK RISE | | 0.6s | expo.out | |
| P7.0 (28.0s) | K face | SHINE | band across the K | 0.8s | power2.inOut | light only, no new read |
| P7.0+0.35/+0.47 | glints | GLINT | on the ball's top-left highlight, sizes 1 and 0.6 | 0.5s life | power3.out / power2.in | |
| 28.0–30.0 | — | HOLD | ball breathes, blobs drift; music fades 28.5 → 30.0 | — | sine.inOut | |

**Camera:** `.world` scale 1.03 → 1 (settling, power2.out over 4s).
**Audio cue:** the last strong hit on P6.0 under the ball landing; fade out.
**Transition out:** none. The final 0.3s may fade to chalk `#F7F5F0`.
**Do not:** no new information after the URL; never recolour the K except black; never place text inside the logo's clear space (5% of its width on each side, per the brand book); logo never under 80px wide.
**Frame check:**
- @25.0s: logo sharp, ball seated exactly on the circle position, extrusion visible.
- @29.0s: logo, both lines, URL pill and "Join the waitlist" all in, nothing clipped, ≥ 65% of the frame white.

**Total:** 4.0 × 6 + 6.0 = 30.0s. Seven frames; scene changes on P1–P6; peak on P4 (drop); held frame P5.6–7.

## 8. Rules for the build (non-negotiable)

- One paused GSAP timeline registered on `window.__timelines`; nothing autoplays.
- Deterministic: no `Math.random`, `Date.now`, `performance.now`, no `repeat: -1`. Seed variation from indices (light-stream angles, particle positions, bob phases, glint sizes).
- `fromTo` with explicit start states; `immediateRender: false` on any `fromTo` that is not the element's first appearance.
- Animate only transforms (x, y, z, scale, rotation, rotationX/Y, skew), opacity, filter, clip-path, colours and `background-position` (gradient-text sweeps only). Never width, height, top or left.
- Never two concurrent transform tweens on one element: entrance on the element, drift/bob on a wrapper, camera on `.world`.
- Smoothness: render at 60 fps; `force3D: true` on 3D elements; no tweens shorter than 0.2s except glints; every arrival settles (no dead stops); no linear easing on visible motion except ambient drift and rim-light rotation.
- Do not tween `backdrop-filter` values. Glass that must "appear" tweens opacity/transform of a pre-blurred layer.
- Glass reads only with coloured edges behind it: keep blobs, rings or ghost numerals behind every glass surface.
- Shader-safety: gradients use `rgba(r,g,b,0)` stops, never the `transparent` keyword; every scene has an explicit `background-color: #F7F5F0`.
- Ambient loops live on the timeline with finite repeats.
- The transition is the exit: no fading elements out before a transition (Frame 7 may fade at the very end).
- Vendor GSAP and the fonts into `assets/`; no CDN dependencies.
- Search the registry before hand-building: `npx hyperframes catalog glass`, `... ring`, `... ticker`, `... light-sweep`, `... depth`. Use registry pieces when they match the spec; the spec wins on look and timing.
- Project bans: no em dashes; ≤ 3 words of message on screen at once; no red, orange, yellow, gold or extra blues; green only on money kept; no dark scenes; no gambling imagery, coins, cash or player photos; never distort, redraw or recolour the logo (black K, hyacinth sphere ball is the only stylised treatment, and only in motion; at rest in Frame 7 the shapes and proportions match `assets/logo.svg` exactly).

## 9. Verify, then hand off

1. `npx hyperframes check .` and fix every error. A wall of contrast errors usually means a wipe panel left covering the frame; intentional overlaps (tile docked on the ball, streak behind the logo, rim light) get `data-layout-allow-overlap` / `data-layout-allow-occlusion`.
2. Render a draft: `npx hyperframes render -o renders/draft.mp4`.
3. Extract a still at every **Frame check** time and compare it with its check:
   `ffmpeg -v error -ss <t> -i renders/draft.mp4 -frames:v 1 renders/check-<t>.png`
   Then a strip across each of the six cuts (`-ss <T-0.25> -t 0.5 -vf "fps=30,scale=480:-2,tile=5x3"`) and a contact sheet of the whole film (`-vf "fps=4,scale=320:-2,tile=8x8"`).
4. Look for: glass that looks like a flat white box; the ball losing its 3D highlight; overlaps and clipping; a word still mid-entrance at its check time; two things moving at once where one should lead; tiles bobbing in unison; blank or flashing transition midpoints; banding in the blobs (raise grain); fallback fonts; off-palette colours (any green that isn't money); frames with less white space than specified; jitter or stepping in slow moves (check for sub-pixel snapping, use transforms only).
5. Fix, re-render, re-check (2–3 rounds is normal). Then render `renders/kickoff-30s.mp4`.
6. Hand off: the file path, duration, resolution, fps, the stills you checked, every deviation from this storyboard and why, and what you could not verify (audio feel, motion at full speed).
