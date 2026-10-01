# 13 · Reads, events and acting

Lessons from the best Claude-made motion pieces (see `measured-references.md` §3, the P(doom) music video and its follow-up guide). They target the failures models make most often: everything at one brisk speed, things happening on top of each other, text doing the work pictures should do, and shots where nothing actually happens.

## 1. Model the viewer: reads

You know what happens because you wrote it. The viewer sees it once, at full speed, for the first time. For every moment, ask **what must the viewer understand, and how long will that take?**

A **read** is one thing the viewer must understand ("the seller card is grey", "it got stamped verified", "the money went to the wallet"). Every frame in the storyboard lists its reads in order, each with a start and an end:

```
reads:
  8.95–9.6   phone arrives; this is the AvioMax home feed        (eye: centre-right, big, moving)
  9.6–10.4   card 3's seller tag is grey                          (lead the eye: the scroll stops on it)
  10.4–11.2  it gets stamped "Verified"                           (the stamp is the brightest, fastest thing)
  11.2–12.4  "Verified sellers" + "Delivered": what this means    (words left; eye moves left after the stamp)
```

Rules:
- **One read at a time.** Don't start a read while the last is still landing. When two things happen at once, the viewer sees one of them. Cause, then reaction, in sequence.
- **Each read needs: time to find it, time to understand it, a beat to register.** Small, distant, fast or subtle things need longer than big, central, obvious ones. As a floor: a big obvious event 0.5s; a UI change 0.8s; a short line of words 0.3s/word + 0.5s; a number to remember 1.5s+.
- **Fast actions, slow meanings.** The motion can be very quick if it's anticipated; what it means needs held time after. Move fast through what doesn't matter, spend time on what does. That contrast is rhythm; one constant speed (fast or slow) is flat.
- **Lead the eye.** The viewer looks at what moves, is bright, is big, or is being looked at. Before an important read, get the eye there (the camera moves to it, it lights up or moves first, a character looks at it) and give the eye time to travel.
- **Let the reads set the length.** If a frame's reads don't fit its duration, lengthen the frame or cut a read. Never squeeze. In music-synced work, that may mean a frame spans two phrases instead of one.
- **The last read of the film needs time to land** before the video ends.

At review, count frames per read (30 frames = 1s). A read that gets a handful of frames, or shares its frames with another read, will be missed.

## 2. Something happens in every frame

- Every frame has an **event**: something is different between its first and last frame. A product wants something, tries, fails, gets it; a state changes; something breaks, transforms, arrives, falls. "The dashboard is shown" is not a frame. "A new order arrives and the total jumps" is.
- **One focal action at a time**, with a clear silhouette and nothing competing.
- **Cause, then reaction.** When something happens, something reacts to it (a character's take, a counter jumping, a card lifting). The reaction is often the best part; give it time.
- **Pay it off.** Whatever a frame sets up (a grey tag, a broken old way, a closed box) is resolved on screen, in that frame or later.

## 3. Show it, don't write it

Models overuse text. Text is the most generic thing on screen; pictures are what only this video has.

- **Picture first.** Before writing any on-screen word, ask whether the picture already says it. If the stamp says "verified", the caption "Verified sellers" is a label repeating the picture: cut it, or keep it only if it carries a claim the picture can't (a number, a brand name, the message).
- **The classic failure is a sign that repeats the story.** A character holding a sign saying "I'm lost" is a failed shot; show them looking left, right, map upside down.
- **Reactions are marks, not words:** `!`, `?`, sweat drop, sparkle, heart, a bulb, a little cloud.
- **Sound-effect words** (BOOM, CHOMP, PING) are a stylised exception, used rarely and painted into the scene.
- **Product promos still need some words** (the brand, the message, the CTA, numbers). Keep them to the message line per act, the proof numbers, and the end card. Never label things the viewer can see.

## 4. Sets, not cards; props, not overlays

- **Sets, not cards.** Each act happens in one *place* (a market, a stage, a chat, a wallet, a stadium) and the camera moves through it. A "card" is a flat rectangle of content replaced by the next; a set has floor, depth, light and things in it.
- **The recurring set that escalates.** Return to the same set at each act or chorus and escalate it each time (P(doom): the same stage four times: party → pyro → paperclip flood → red alarm). The return gives structure; the escalation gives momentum.
- **Diegetic props, not overlays.** Put data inside the world as an object (a thermometer on the stage that a character pumps; a market scale whose needle swings; a cash box that fills), not as a floating HUD. A prop can be acted on, escalate, crack, overflow, and pay off at the end.

## 5. A cast and acting

A character gives the viewer someone to feel with. Not every product video needs one, but most get better with one.

- **Who can be the actor:** a mascot; a user (the seller, the buyer, the fan); the product itself (the logo mark, the app icon, the link chip) given eyes or just body language (squash, lean, hop); an object from the terrain (the ball, the parcel).
- **Give the cast an arc:** plan the emotion keys across the whole film (worried → hopeful → delighted), not per shot.
- **A foil:** a second character the action happens *to* makes the hero's effect visible (P(doom): the Researcher, dragged through every gag).
- **Faces act, they never snap:** a mood change is anticipation (squint), a squash-stretch "take", an emote pop, then the new expression with overshoot.
- **Show the thought:** notice → think → act. The eyes move first. The viewer understands a choice when they see it being made.
- **Size:** the actor is big. In a medium shot the hero fills ~30–40% of frame height; in close-ups more. Tiny characters only in wide establishing shots.

## 6. Character animation principles code gets wrong

Code moves every part at once, on the same curve, by the same amount. Undo that.

- **Strong key poses first.** Each frame's storytelling poses must read as stills (clear silhouette, body leaning into the action) before any motion goes between them. In the build, block key poses and check them as stills before animating.
- **Avoid twinning.** Code copies values: both arms at the same angle, both eyes blinking together, a crowd bouncing in unison, three cards entering identically. Give one side the action and the other something smaller; offset timings, phases and seeds.
- **Overlap and follow-through.** The eyes lead, the body follows; arms, hats, props, shadows drag behind, overshoot and settle last.
- **Weight.** Heavy things start slow, stop slow, land with little bounce; light things snap, bounce and flutter.
- **Exaggeration.** Push poses, squash, leans and takes further than feels natural. Subtle reads as nothing in a short film.
- **Secondary action.** A hat bob, an emote, grass stirring: supports, never competes.

## 7. One piece

- **Rhyme the ending with the opening:** the same place, pose or motif, changed (P(doom) opens and closes on a curtain; the final reveal recontextualises the whole film).
- **Colour arc:** the palette shifts with the story (cold → warm as the mood lifts; normal → alarm red at the climax). Within a strict brand palette, the arc can be in value and proportion (mostly charcoal → mostly red by the end card).
- **Screen direction:** if things travel right, keep them travelling right across cuts unless the story reverses.
- **Cut on action:** cut mid-move and finish the move in the next shot. The motion carries the eye across the seam.
- **Literalise the jargon:** each phrase or concept in the script becomes a physical gag (P(doom): "a sudden drop in training loss" is a character sledding down the loss curve). This is the terrain method applied line by line.

## 8. A medium, not the web default

Default HTML/CSS looks like a web page. Choosing a **medium** makes it look made:
- Hand-painted watercolour and ink with boiling linework (p5.js + p5.brush; lines re-jittered 12×/s with seeded noise so drawings wobble like hand animation).
- Cut-paper collage, risograph print, chalk on a board, flat vector poster, glass-and-light UI, clay.
- **Animate on twos** for handmade media: quantise time to 12 fps (`tq = Math.floor(t * 12) / 12`) for character and linework while the camera moves at full rate.
- The medium must be deterministic (seeded noise, no `Math.random`) and render within budget. Software-GPU containers render heavy canvas/brush fills slowly; budget per-frame cost (P(doom) aimed for ≤ 2.5s/frame).

Pick the medium in the Look stage and write it in the storyboard's Look section with its rules (what is painted, what is flat, what boils, what never does).
