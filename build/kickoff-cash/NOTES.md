# kickoff.cash · review notes

## What worked

The look is right: dark stage, purple light curtains, smoked glass, glints, signal green kept for the payoff, and real 3D (ball, pitch disc, scoreline grid, chips, extruded K). Keep it for the next pass.

## Observation from review: too slow, it stalls

The video stalls for too long in particular scenes. It should keep moving: even when a scene holds, something should be travelling across the frame or the camera should be moving into something, and a hold should be short. A first guess is that **about 1.5× faster** would be much better.

### Measured (recipes/motion-profile.py on the final render)

- Still share: **41%** of frames are effectively still. That suits a calm UI showcase (Zajno measured 35–60%), not a 60s football promo.
- Long quiet stretches, where only ambient drift is moving:

| Time | Length | Where |
|---|---|---|
| 2.6–4.0s | 1.4s | ball resting on the disc before the ticket appears |
| 6.0–7.5s | 1.5s | ticket and caption hold before the kick |
| 20.9–23.5s | 2.6s | grid hold after "Close still pays." |
| 25.6–31.1s | **5.5s** | pool card: rows and bars fill, then a slow push (the worst one) |
| 54.7–59.2s | 4.5s | lockup and end card |

- Mean motion per act (frame difference): Call 1.1 · Match 2.3 · Grid 2.5 · **Pool 1.2** · Payoff 5.1 · **Perps 1.3** · Leaderboard 1.7 · **Lockup 0.9**. The quiet acts are the ones that feel stalled.

### Why it happened

- Every act was given two full phrases (8s at 120 BPM). That gave each act room to breathe, but many acts don't have 8s of reads, so the spare time became holds.
- Ambient motion (curtain drift, slow card sway, 1.03× zooms) was kept deliberately quieter than the action, as the skill says. Over a 2–5s hold it reads as stopped, not alive.
- Inside the pool and perps acts, things fill and settle in place. Nothing travels across the frame and the camera doesn't move into anything.

### For the next pass (not applied)

- **Tempo:** 1.5× would put the film at about 40s. Or keep 60s and fit more events in: one phrase (4s) per idea instead of two, and two-phrase acts only for the hero (grid) and the drop.
- **Hold length:** cap any hold at about 1–1.5s, and only straight after a key read lands (the message, the payout).
- **Motion while holding:** while something holds, the camera should still be travelling: a push into the next subject, a truck across the set, or a rack focus. The next object should already be entering, so each hold hands off into the next move instead of waiting for the cut.
- **Specific spots:**
  - Pool: start the fills on arrival, cut the 3.4s push to under 1s, or carry the camera along the bars.
  - Perps: run the result marker faster and move on once +$86 lands.
  - Lockup: CTA press about 1s after the wordmark, then end.
  - Opening: drop the ball straight into the kick setup.
- **Music:** at 1.5× the track would need to be about 180 BPM, or keep 120 BPM and change scenes every phrase instead of every two.
- **Before building:** the skill should check a storyboard's still share against the reference it is matching, not only against UI-motion references.

Pending: compare against the reference video the user mentioned (not yet received) and record its numbers here.
