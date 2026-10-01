# motion-storyboard

A Claude skill that directs motion design videos before they are built. Give it a product brief and it produces a beat-by-beat storyboard precise enough for Claude to build in [HyperFrames](https://hyperframes.heygen.com) without guessing: the message, the features and their proof moments, the product's visual *terrain*, a concept with a spine, and every beat specified with music position, layout, motion verbs, eases, durations, camera, transitions, materials (glass, gradients, chrome, shine, glints) and a frame check to verify the render against.

It is brand-agnostic: you supply the brand per project.

## Why

A prompt like "logo slams in, push transition out" leaves every decision to the build, and improvised motion comes out generic. This skill moves those decisions onto paper, where changing them is cheap, using:

- motion principles (easing, timing, offset, follow-through, masking, morph, parallax, zoom), from classic animation, [Zajno's motion principles](https://motion.zajno.com/) and measured promo work;
- a transition grammar (meaning, primary vs accent, velocity matching, object-carried transitions) with build numbers;
- a terrain method that turns a product's world into props and transitions (football → ball, pitch lines, scoreboard flips; privacy → redaction bars, hashes, frosted glass; prediction markets → YES/NO, probability bars);
- tested HyperFrames recipes for glass, mesh gradients, chrome text, shine sweeps, rim lights and glints;
- lessons from the P(doom) music video made with Claude: time every frame by what the viewer must understand (reads), make something happen in every frame, show instead of write, sets instead of cards;
- a map of every storyboard term to the HyperFrames rule, blueprint or registry item that builds it.

## Install

Claude Code (personal skills):
```bash
git clone https://github.com/NECOKIZZ/motion-design ~/motion-design
mkdir -p ~/.claude/skills
ln -s ~/motion-design/skills/motion-storyboard ~/.claude/skills/motion-storyboard
```
Or per project: copy `skills/motion-storyboard` into the project's `.claude/skills/`.

HyperFrames' own skills are needed for the build step: `npx hyperframes skills update`.

## Use

Ask for a video the usual way, or fill `skills/motion-storyboard/templates/brief.md`:

> Make a 30-second motion graphic video with HyperFrames for AvioMax, a Nigerian online marketplace where verified sellers open stores and buyers shop safely, with Paystack payments and 6% commission. Audience: Nigerian shoppers and small sellers on Instagram, TikTok and WhatsApp. End line: "Shop smart. Sell big." Brand: Poppins Bold/Medium, charcoal #2D2D2D, white, accent #CC0000, no blue/green/purple. Music: assets/music.mp3. Stop after the storyboard.

Claude runs seven stages: brief → terrain → concept (shown to you) → look → beat sheet (shown to you) → self-review → build and verify (if asked). See `examples/aviomax-30s.md` for a complete storyboard.

## Contents

```
skills/motion-storyboard/
  SKILL.md                        entry point: process, rules, reference map
  references/
    01-brief-and-features.md      message as a claim, features → proof moments, arcs
    02-terrain.md                 the product's visual world → props and native transitions
    03-concept.md                 five pitches, spine, signature moments, rhythm, bans
    04-motion-language.md         easing, timing, stagger, follow-through, verbs, entrance vocabulary
    05-transitions.md             meaning, grammar, catalogue with numbers, seam map
    06-camera-and-depth.md        camera rig, moves, parallax, dimension, depth of field
    07-type-in-motion.md          reading time, sizes, kinetic type techniques
    08-materials-and-light.md     gradients, glass, shine, chrome, glints, rim light, glow
    09-rhythm-and-music.md        beat grid, phrases, what lands where
    10-product-ui.md              UI state machines, devices, cursor/tap patterns
    11-storyboard-format.md       the STORYBOARD.md spec
    12-build-and-review.md        self-review checklist, build loop, render-and-inspect
    13-reads-events-and-acting.md timing by reads, an event per frame, show-don't-write, sets, acting, medium
    hyperframes-map.md            capabilities, hard limits, term → building block
    measured-references.md        numbers measured from reference videos
  templates/                      brief.md, storyboard.md
  examples/aviomax-30s.md         full worked storyboard
  recipes/
    materials.html                tested glass / gradient / chrome / shine / glint composition
    materials-render.jpg          frames from its render
    motion-profile.py             measures motion timing in reference videos
```

## Adding reference videos

Analyse new references with `recipes/motion-profile.py` and ffmpeg contact sheets (commands in `references/measured-references.md`), then add a section there: what it is, the numbers, the techniques worth borrowing. Learn craft, never copy content.
