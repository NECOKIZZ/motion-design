# 10 · Showing the product working

Viewers believe what they see the product do. A static screenshot with a caption is a claim; a button pressed and the screen changing is proof.

## 1. Capture or recreate?

| Situation | Do |
|---|---|
| Real screens supplied (PNG) | Use them as the visual truth. Rebuild in HTML only the parts that must move (a number counting, a notification arriving, a list scrolling). Keep fonts, colours, spacing faithful. |
| Live site, no screens | `npx hyperframes capture <URL>` for screenshots and brand tokens. |
| No product yet / illustrative | Recreate in the brand style and label it if the audience could mistake it for the real app. |
| Never | Invent features, numbers or claims the product cannot back. Never an iframe (does not seek). |

## 2. The UI state machine

Explain a feature as a sequence of states on one surface, one state per beat pulse, each caused by something (a cursor, a tap, an incoming event):

```
idle → press (button dips 4%, ripple) → working (spinner, label "Processing") →
result (state flips, number counts, badge pops) → payoff (glint, confetti, or the surface lifts)
```

Rules:
- Transform the same object in place; never cut to a separate "after" screen.
- The cause comes first, then the effect, one pulse later.
- Annotate once: a single line or arrow drawn from a word to the UI element it describes, ~0.3s draw.
- Keep the UI big enough to read: a phone mockup at least 55–65% of frame height; a dashboard cropped to the relevant region and zoomed (target zoom), never shown whole and tiny.

## 3. Patterns (HyperFrames rule / blueprint names in brackets)

| Pattern | Use | Build |
|---|---|---|
| Cursor drives the UI | desktop workflows | cursor moves on an arc `power2.inOut`, click = scale 0.9 dip + ripple (`cursor-click-ripple`, blueprint `cursor-ui-demo`) |
| Tap on phone | mobile | translucent touch circle (registry `touch-indicator`) |
| Notification arrives | events, orders, payments | drops from top 0.35s `back.out(1.4)`, slight bounce, ping sound; stack pushes down (`anchored-layout-expand`) |
| Number climbs | sales, users, savings | count-up 0.8–1.5s `power2.out`, digits in tabular figures, a small "+₦" flies in first (`counting-dynamic-scale`) |
| List populates | catalogues, feeds | items arrive one per pulse or 0.08s stagger, each blur-resolving (`waterfall-entry`, blueprint `grid-card-assemble`) |
| Scroll | long screens | content translates inside the device's screen mask; ease `power2.inOut`, pauses on key items (`3d-page-scroll`) |
| Device as hero | app tours | phone/laptop floating tilted, screens cycle (blueprint `device-surface-showcase`, registry `parallax-device-dive`) |
| Prompt → result | AI tools, search | typewriter in the input, submit, result streams (blueprint `prompt-type-submit-generate`) |
| Before / after toggle | comparisons | segmented control clicked, second state slides in beside or replaces (blueprint `comparison-split`) |
| Live sync | editors, settings | control changes and target updates on the same beat (`control-target-sync`) |

## 4. Devices

- Phone: rounded rect, radius ~ 12% of width, bezel 10–14px, a subtle top-left highlight (see glass rim), soft shadow. Screen content in an `overflow: hidden` mask so scrolling clips.
- Dynamic island / notch only if it matches the platform the audience uses.
- Tilt the device while it moves; flatten it to ≤ 10° when the screen must be read.
- One device per frame is usually enough; two only for a "seller sees / buyer sees" split.

## 5. Writing UI beats in the storyboard

```
UI: Vendor dashboard (from assets/vendor-dashboard.png), recreated: header, "Today" sales card,
    orders list. Phone mockup, 62% frame height, right third, tilted rotationY −10° → 0 as it settles.
STATE SEQUENCE:
  P4.1 notification "New order! · Ada · ₦10,000" drops in from the top (0.35s back.out(1.4)), ping SFX
  P4.2 sales number counts ₦45,000 → ₦55,000 (1.0s power2.out), "+₦10,000" chip flies from the
       notification to the number (arc, 0.4s)
  P4.4 badge "6% commission" STAMPS onto the card's corner (0.25s back.out(2.5), 8px shake)
```
