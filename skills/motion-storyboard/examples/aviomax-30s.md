---
format: 1920x1080
duration: 30s
fps: 30
message: "Sell to all of Nigeria in one link."
endline: "Shop smart. Sell big."
arc: Pain → Turn → Proof (buyers) → Signature (one link) → Proof (sellers, peak) → Trust → Sign-off
audience: Nigerian small business owners selling on Instagram, TikTok and WhatsApp; shoppers burned by fake sellers
music: assets/music.mp3 (Afrobeats instrumental; assumed 108 BPM, pulse 0.556s, phrase = 8 pulses = 4.44s; replace with `npx hyperframes beats` output)
mode: collaborative
---

# AvioMax 30s storyboard v1 (worked example)

> This is a worked example of the format, written from the brief in the README. Times assume 108 BPM until the real beat grid is measured; the build re-derives every time from the grid with `at(phrase, pulse)`.

## Concept

**"One link, everywhere."** The seller's AvioMax store link is a red thread. It appears when the logo lands, carries the camera from scene to scene, gets pasted into three chats at once, comes back as orders and money, and finally ties itself into the logo. Red only ever appears on things AvioMax causes (colour rule), so the eye learns that red = AvioMax working.

- **Spine:** the red link line (persistent object + colour rule).
- **Signature moments:** (1) the link pasted into Instagram, TikTok and WhatsApp in one move; three "New order" pings answer. (2) A ₦10,000 sale splits on screen: ₦9,400 flies into the seller's wallet, a thin ₦600 sliver marked "6%" peels away.
- **Rhythm:** `hook-hook-TURN-proof-SIGNATURE-PEAK-trust-hold-SIGNOFF`; peak at P4 (17.8s) where the track builds.

## Terrain

| Object | Native motion | Device | Transition | Proves |
|---|---|---|---|---|
| Store link | is copied, pasted, travels | a red line with a link-chip head | **link-line wipe** (the line sweeps across; the new scene is revealed behind it) | sell anywhere |
| Chat bubbles (IG, TikTok, WhatsApp) | pop in, stack | the link lands in three bubbles at once | bubble expands into the next scene | social selling |
| Verified stamp | thuds | grey seller tag stamped red "Verified" | — | verified sellers |
| ₦ notes / sale | split, fly | ₦10,000 splits; ₦9,400 to wallet, ₦600 "6%" sliver | — | 6% commission |
| Dispatch box | sealed, shipped | box tape seals, "Delivered" | — | delivery |
| Paystack payment | card taps, seals | card number collapses into a sealed token | — | secure payments |

Signature props: the red link line, the three-chat paste, the naira split.
Avoid: shopping-cart icon, floating credit cards, 3D coins, "SALE" tags, generic rising graph.
Native transition: the link-line wipe.

## Look

- **Palette:** charcoal `#2D2D2D` (dark scenes) · white `#FFFFFF` (light scenes and text on dark) · accent red `#CC0000` (only on what AvioMax causes). Allowed tints: `#1F1F1F`, `#3A3A3A`, `#8A0000`, `#FF4D4D` (glow only). No blue, green or purple anywhere, including platform icons (draw IG/TikTok/WhatsApp marks as white or charcoal outlines).
- **Type:** Poppins Bold (`assets/fonts/Poppins-Bold.ttf`) for hero 200–240px and headlines 120–150px; Poppins Medium (`assets/fonts/Poppins-Medium.ttf`) for labels 44–56px and UI 28–36px. No monospace.
- **Material + light:** flat and bold throughout; one glass treatment on the trust cards (Frame 6) over red/charcoal blobs with drifting ghost type behind; one shine sweep + two glints on the end-card logo.
- **Background layer:** dark scenes = charcoal + two slow radial blobs (`#3A3A3A`, `#8A0000` at 35%) + grain 14% overlay; light scenes = white + faint 2px charcoal dot grid at 8% + grain 6%.
- **Logo:** `assets/logo.svg`, min height 120px, clear space = its own height; never recolour (white version only on red).

## Motion system

- **Energy:** high. Entrances 0.15–0.3s; transitions 0.25–0.45s; UI moves 0.4–0.6s.
- **Entrance vocabulary:** scale slam, side snap, drop, rise, stamp, spring pop, mask rise, fly in on arc, count up.
- **Eases:** `expo.out` (arrivals) · `power4.out` (snaps) · `back.out(1.6)` (drops) · `back.out(2.5)` (stamps) · `power3.in` (outgoing) · `power3.inOut` (camera, reflow, wipes) · `none` (ambient).
- **Ambient:** every scene's `.world` drifts (scale 1 → 1.025 or x ±24px); blobs drift at 0.3×; no two consecutive scenes use the same ambient move.
- **Camera rig:** `.world` > `.bg` (0.3×) · `.mid` (1×) · `.fg` (1.4×).
- **Direction:** forward = leftward (new content enters from the right; the link line travels right → left).

## Beat grid (assumed 108 BPM; replace with measured)

| Phrase | Start | Section |
|---|---|---|
| P0 | 0.00 | intro |
| P1 | 4.44 | verse |
| P2 | 8.89 | verse |
| P3 | 13.33 | build |
| P4 | 17.78 | drop (peak) |
| P5 | 22.22 | drop |
| P6 | 26.67 | outro (fade 28.5–30.0) |

Pulse k of phrase p = p × 4.444 + k × 0.556 s.

## Seam map

| Cut | Time | From → to | Transition | Role | Carried by |
|---|---|---|---|---|---|
| 1 | P1.0 4.44s | Hook → Logo | Iris from the red full stop of "way." | accent | the full stop |
| 2 | P2.0 8.89s | Logo → Buyers | Link-line wipe, 0.45s | primary | the link line drawn from the logo |
| 3 | P3.0 13.33s | Buyers → One link | Link-line wipe, 0.4s | primary | the link line from the product card's Share button |
| 4 | P4.0 17.78s | One link → Sellers | Bubble morph into the dashboard, 0.45s | accent (signature) | the WhatsApp bubble |
| 5 | P5.0 22.22s | Sellers → Trust | Link-line wipe, 0.35s | primary | the link line leaving the wallet |
| 6 | P6.0 26.67s | Trust → End | Collapse into logo + red flood | hero | the three trust cards and the link line |

## Bans

- No slideshow: every cut is carried by the link line, the full stop or a bubble.
- No screensaver: blobs and drift never compete with action.
- No fades between scenes; no shopping-cart icon; no blue/green/purple; never distort or recolour the logo; no em dashes; never more than 3 words of message at once.

## Frame 1 — Hook: the old way

- time: P0.0–P1.0 (0.00–4.44s, 4.44s)
- role: hook (pain)
- why: Sellers recognise the pain before they hear the product.
- transition_in: cold open
- status: outline

**On screen (verbatim):** "Overpriced?" · "Low reach?" · "Better way."
**Layout:** "Overpriced?" left third, y 380, 150px white; "Low reach?" right third, y 560, 150px white; "Better way." centre, y 540, 220px red. Ghost word "SELL" 600px charcoal-tint `#3A3A3A` bottom-right bleeding off-frame.
**Depth:** BG charcoal + blobs + grain (0.3×) · MG words (1×) · FG two thin white streaks (1.4×) that pass during the slam.
**Material/light:** flat.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P0.1 (0.56s) | "Overpriced?" | SIDE SNAP | x −200, skewX 8°, blur 8px, opacity 0 → 0, 0°, 0, 1 | 0.2s | power4.out | arrives 1 frame early |
| P0.3 (1.67s) | "Low reach?" | DROP | y −180, opacity 0 → 0, 1 | 0.3s | back.out(1.6) | |
| P0.5 (2.78s) | "Overpriced?", "Low reach?" | REFLOW + DIM | scale 1 → 0.7, opacity → 0.35, y → toward top/bottom edges | 0.35s | power3.inOut | makes room on the same pulse |
| P0.5 (2.78s) | "Better way." | SCALE SLAM | scale 2.2, blur 12px, opacity 0 → 1, 0, 1 | 0.18s | expo.out | 10px frame shake decaying 0.2s; FG streaks cross |
| P0.6–7 | — | BREATHE | camera drift continues | — | none | nothing new enters |

**Camera:** `.world` scale 1 → 1.03 over the frame (none).
**Audio cue:** kick on each word; the slam on the snare.
**Transition out:** cut 1. The full stop of "way." (red disc ~36px) scales to cover the frame (`clip-path circle` iris from its centre, 0.35s `power3.in` → the logo scene's red disc, which then shrinks to become the logo's backing for the logo slam).
**Do not:** no plain fade between words; no question words in red (red is AvioMax only).
**Frame check:**
- @2.0s: "Overpriced?" and "Low reach?" sharp, no overlap, left/right balance.
- @3.4s: "Better way." centred, sharp, red; the other two dimmed and pushed apart.

## Frame 2 — Turn: AvioMax and the message

- time: P1.0–P2.0 (4.44–8.89s)
- role: turn (product appears) + message
- why: Names the answer and states the claim by the end of frame 2.
- transition_in: cut 1 (iris from the full stop)
- status: outline

**On screen (verbatim):** logo · "AVIOMAX" · "One link." · "All of Nigeria."
**Layout:** logo centre-left (x 620, 220px tall) on charcoal; "AVIOMAX" to its right, 180px white; then the message lines replace the wordmark area (reflow: logo slides left 120px).
**Depth:** BG charcoal + blobs · MG logo, words · FG link-chip head and line.
**Material/light:** flat; a soft red glow (radial, 25%) blooms behind the logo before it lands.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P1.0 | red disc (from iris) | SHRINK | full frame → logo backing size | 0.3s | power3.inOut | match cut into the logo |
| P1.1 | logo | SCALE SLAM | scale 1.8 → 1, blur 10 → 0 | 0.22s | expo.out | glow blooms 0.1s before |
| P1.2 | "AVIOMAX" | MASK RISE (per letter) | y 105% → 0, 0.04s stagger | 0.5s | expo.out | letters inside an overflow-hidden line |
| P1.4 | "AVIOMAX" | EXIT UP | y 0 → −105% | 0.2s | power3.in | covered by the next line rising |
| P1.4 | "One link." | MASK RISE | y 105% → 0 | 0.4s | expo.out | white |
| P1.5 | link line | DRAW | from the logo's edge, a red 6px line with a rounded chip head draws right 0 → 900px | 0.5s | power2.inOut | the spine appears |
| P1.5 | "All of Nigeria." | SIDE SNAP | x +160, blur 8 → 0 | 0.2s | power4.out | below "One link.", "Nigeria" in white (not red) |
| P1.6–7 | — | BREATHE | link chip idles (y ±4px, 2 cycles) | — | sine.inOut | |

**Camera:** `.world` x 0 → −24px (none).
**Audio cue:** logo slam on the strong beat; soft swish on the line draw.
**Transition out:** cut 2. The link chip whips right → left across the frame, the line trailing it; the buyers scene (white) is revealed behind the line's leading edge (`clip-path: inset(0 0 0 X%)` following the chip), 0.45s `power3.inOut`; the line stays as a hairline across the top of the next scene and fades to 0 over 0.3s.
**Do not:** never recolour or squash the logo; no tagline-word salad ("Empowering. Sellers. Delighting. Buyers." is cut: too many words for one frame).
**Frame check:**
- @5.6s: logo sharp at ≥220px, glow subtle, "AVIOMAX" fully risen.
- @7.9s: "One link." and "All of Nigeria." readable, link line drawn, nothing overlapping the logo.

## Frame 3 — Proof: buyers shop verified sellers

- time: P2.0–P3.0 (8.89–13.33s)
- role: proof (feature: verified sellers)
- why: Shoppers' first doubt is "is this seller real?"; we show a seller get verified.
- transition_in: cut 2
- status: outline

**On screen (verbatim):** "Verified sellers" · "Delivered"
**Layout:** white scene. Phone mockup right third (62% frame height, centre x 1300) showing the recreated home screen (`assets/home.png`); words left third, top-aligned y 360, 120px charcoal; chips 52px.
**Depth:** BG white + dot grid · MG phone, words · FG a blurred parcel corner bottom-left (1.4×, blur 14px).
**Material/light:** flat UI; phone has a subtle top-left highlight.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P2.0+0.1 | phone | TILT-FLATTEN | rotationY −35°, x +160 → 0°, 0 | 0.6s | expo.out | perspective 1400 |
| P2.1 | home feed | SCROLL | y 0 → −420 | 1.6s | power2.inOut | cards pass; settles on card 3 |
| P2.3 | card 3 seller tag | STAMP | grey "Seller" → red check "Verified", scale 2.5, rot −25° → 1, −8° | 0.25s | back.out(2.5) | 6px phone shake |
| P2.3 | "Verified sellers" | SIDE SNAP | x −160, skew 8°, blur 8 → 0 | 0.2s | power4.out | "Verified" word in red |
| P2.5 | dispatch box icon + "Delivered" chip | RISE | y +80, opacity 0 → 0, 1 | 0.45s | power3.out | box tape draws closed 0.3s |
| P2.6–7 | — | BREATHE | drift | — | none | |

**Camera:** `.world` scale 1 → 1.025.
**Audio cue:** stamp thud on P2.3.
**Transition out:** cut 3. The card's "Share" button is tapped (touch circle, dip 0.9); the link line shoots out of it to the left and wipes into Frame 4 (charcoal), 0.4s `power3.inOut`.
**Do not:** no shopping-cart icon; phone never under 55% height; no fade on chips.
**Frame check:**
- @10.4s: phone flat and sharp; "Verified" stamp on card 3; heading fully in; no overlap.
- @12.4s: both chips visible; left column aligned on one x; only drift moving.

## Frame 4 — Signature: one link, three chats

- time: P3.0–P4.0 (13.33–17.78s)
- role: signature moment 1 (sell on social)
- why: The core promise made visible: one link reaches every place buyers already are.
- transition_in: cut 3
- status: outline

**On screen (verbatim):** "One link." · "Every chat."
**Layout:** charcoal. Three chat panels fanned across the right two-thirds (Instagram DM, TikTok inbox, WhatsApp chat), each 420×560, tilted ±4°, white outline platform marks (no brand colours). Words top-left, 130px white.
**Depth:** BG charcoal + blobs · MG chat panels · FG the link line and chips (1.4×).
**Material/light:** flat; bubbles white with charcoal text; the pasted link chip is red.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P3.0+0.05 | three panels | FLY IN ON ARC | from right edge, rot 12° → ±4°, 0.1s stagger | 0.4s | x power3.out, y power2.out | |
| P3.1 | "One link." | SCALE SLAM | scale 1.8 → 1 | 0.18s | expo.out | |
| P3.2 | link line | SPLIT + PASTE | the line forks into three and lands a red link bubble in each chat at once | 0.35s | power3.inOut | the signature beat |
| P3.3 | "Every chat." | DROP | y −160 → 0 | 0.3s | back.out(1.6) | |
| P3.4, P3.4+0.12, P3.4+0.24 | "New order" bubbles | SPRING POP | scale 0 → 1, one per chat | 0.3s each | back.out(2) | three pings, rising pitch |
| P3.6–7 | — | BREATHE | panels bob y ±5px, offset phases | — | sine.inOut | build in the music |

**Camera:** `.world` push in scale 1 → 1.06 across the frame (power2.inOut), anticipating the drop.
**Audio cue:** paste "click" on P3.2; three message pings on P3.4.
**Transition out:** cut 4. The WhatsApp "New order" bubble expands to full frame (scale 1 → 12 around its centre, radius 28 → 0, 0.45s `expo.inOut`, starting at P4.0 − 0.25s); its white fill becomes Frame 5's background.
**Do not:** no platform brand colours (blue/green/purple banned); no more than 3 words of message on screen.
**Frame check:**
- @14.6s: three panels readable, link bubble red in all three, "One link." in.
- @16.6s: three "New order" bubbles visible; "Every chat." in; nothing clipped at the right edge.

## Frame 5 — Peak: sellers keep 94%

- time: P4.0–P5.0 (17.78–22.22s)
- role: proof (feature: 6% commission) + signature moment 2 (peak, on the drop)
- why: Sellers' second doubt is cost; the split shows exactly what they keep.
- transition_in: cut 4 (bubble morph)
- status: outline

**On screen (verbatim):** "₦10,000" → "₦9,400" · "6%" · "You keep more."
**Layout:** white. Vendor dashboard (recreated from `assets/vendor-dashboard.png`) as a large card left-centre (1100×640); wallet widget top-right of the card; words right third, 120px charcoal.
**Depth:** BG white + dot grid · MG dashboard · FG the ₦ notes and the "6%" sliver (1.4×).
**Material/light:** flat.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P4.0+0.05 | dashboard | SETTLE | scale 1.08 → 1 (inherits the bubble's expansion) | 0.4s | expo.out | |
| P4.1 | notification "New order! · Ada · ₦10,000" | DROP | from top of card, y −120 → 0 | 0.35s | back.out(1.4) | ping |
| P4.2 | ₦10,000 note | SPLIT | the note slides out of the notification, then cuts into two pieces: big piece "₦9,400", sliver "₦600" | 0.3s | power4.out | the drop hits here |
| P4.3 | "₦9,400" piece | FLY IN ON ARC → wallet | to the wallet widget | 0.4s | x power3.out, y power2.out | wallet bulges scale 1.08 → 1 (0.25s back.out) |
| P4.3 | wallet total | COUNT UP | ₦45,000 → ₦54,400 | 1.0s | power2.out | integers only |
| P4.4 | "₦600" sliver | PEEL | drifts off down-right, rotation 0 → 14°, opacity → 0.5 | 0.5s | power2.in | small "6%" red label stamps onto it |
| P4.4 | "You keep more." | MASK RISE | y 105% → 0 | 0.4s | expo.out | "more" in red |
| P4.6–7 | — | BREATHE | drift | — | none | |

**Camera:** punch-in scale 1 → 1.12 at P4.2 (0.2s expo.out) on the split, then ease back to 1.04 over 1s (power2.inOut).
**Audio cue:** drop at P4.0; cash "ching" at P4.3.
**Transition out:** cut 5. The link line leaves the wallet to the left and wipes into Frame 6 (charcoal), 0.35s `power3.inOut`.
**Do not:** never invent a commission other than 6%; no 3D coins; no rising line graph.
**Frame check:**
- @19.0s: note split visible: "₦9,400" and "₦600" both readable.
- @21.2s: wallet shows ₦54,400; "You keep more." readable; "6%" label on the sliver.

## Frame 6 — Trust: verified, secure, protected

- time: P5.0–P6.0 (22.22–26.67s)
- role: proof (trust: Paystack, buyer protection) + held frame
- why: Removes the last objection (safety) and gives the viewer a breath before the sign-off.
- transition_in: cut 5
- status: outline

**On screen (verbatim):** "Verified" · "Paystack secure" · "Buyer protection"
**Layout:** charcoal. Three glass cards in a row (each 460×300, gap 60), centred vertically; each card: icon (red badge, shield, box) + one label 52px white. Ghost type "TRUST" 520px `#3A3A3A` drifting behind the cards at 0.3×.
**Depth:** BG charcoal + red/charcoal blobs + ghost type · MG glass cards · FG small glints.
**Material/light:** **glass** (dark tint `rgba(20,20,20,.35)`, blur 28px, saturate 160%, top rim highlight) over the drifting ghost type and blobs so the glass reads; one shine sweep across all three cards at P5.5; glints on card corners.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P5.1 | card 1 "Verified" | DROP | y −200, rot −6° → 0, 0 | 0.3s | back.out(1.6) | badge inside STAMPS +0.08s |
| P5.2 | card 2 "Paystack secure" | RISE | y +120, rotationX 18° → 0, 0 | 0.45s | expo.out | card number collapses into a sealed token inside (0.3s) |
| P5.3 | card 3 "Buyer protection" | SIDE SNAP | x +200, blur 8 → 0 | 0.2s | power4.out | box lid closes |
| P5.5 | shine band | SWEEP | x −400 → 1900 across all cards | 0.8s | power2.inOut | soft-light |
| P5.5+0.25/0.45/0.62 | glints | GLINT | scale 0 → 1/0.7/0.5 → 0 on each card's top-right corner | 0.5s life | power3.out / power2.in | timed to the band |
| P5.6–7 | — | HELD FRAME | only ghost type and blobs drift | — | none | the breath before the sign-off |

**Camera:** `.world` x +20 → −20px (none) (opposite direction to Frame 5's drift).
**Audio cue:** three soft thuds on P5.1–5.3; shimmer on the sweep.
**Transition out:** cut 6 (hero). The three cards and the link line collapse into the screen centre (0.3s `power3.in`, 0.04s stagger), becoming the logo mark; red floods outward from the logo (`clip-path circle` 0 → 80%, 0.35s `expo.out`).
**Do not:** no generic shield-with-check stock icon in blue; no more than one word in red (the "Verified" badge).
**Frame check:**
- @24.0s: three cards in, glass visibly frosting the ghost type behind, labels readable (contrast ≥ 4.5:1).
- @25.2s: sweep mid-way across card 2, one glint visible.

## Frame 7 — Sign-off

- time: P6.0–end (26.67–30.00s)
- role: sign-off + CTA
- why: Leaves the brand, the line and where to go.
- transition_in: cut 6 (collapse + red flood)
- status: outline

**On screen (verbatim):** logo (white) · "Shop smart." · "Sell big." · "aviomax.store"
**Layout:** red `#CC0000` background. Logo centre, y 380, 200px tall; "Shop smart." / "Sell big." stacked y 600–760, 120px white; URL pill y 900, white pill with red text 48px.
**Depth:** BG red + faint darker-red blob (`#8A0000` 30%) + grain · MG logo, lines · FG one anamorphic white streak behind the logo.
**Material/light:** flat; one shine sweep across the logo + two glints on its top edge.

**Motion:**
| At | Element | Verb | From → to | Dur | Ease | Notes |
|---|---|---|---|---|---|---|
| P6.0+0.1 | logo | SETTLE | scale 1.15 → 1 | 0.4s | expo.out | anamorphic streak crosses behind (0.5s) |
| P6.1 | "Shop smart." | MASK RISE | y 105% → 0 | 0.4s | expo.out | |
| P6.2 | "Sell big." | SCALE SLAM | scale 1.8 → 1 | 0.18s | expo.out | 6px shake |
| P6.3 | logo | SHINE + GLINTS | band across the logo; glints at +0.3s, +0.42s | 0.7s | power2.inOut | |
| P6.4 | "aviomax.store" pill | RISE | y +80 → 0 | 0.45s | power3.out | |
| P6.5–end | — | HOLD | drift only; music fades 28.5 → 30.0s | — | none | URL readable ≥ 2.5s |

**Camera:** `.world` scale 1.02 → 1 (settling, none).
**Audio cue:** final hit on P6.0; fade out.
**Transition out:** none (final frame may fade to red at 29.8s).
**Do not:** never recolour the logo except the approved white version; no new information after the URL.
**Frame check:**
- @27.6s: logo sharp, "Shop smart." in.
- @29.5s: all four elements in, URL pill readable, nothing clipped.

## Total

4.44 × 6 + 3.33 = 30.0s. Seven frames; scene changes on P1–P6; peak on P4 (drop); held frame P5.6–7.
