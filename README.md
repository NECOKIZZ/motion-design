# motion-storyboard

A Claude skill that **writes the prompt** for a motion design video. You give it a rough idea or a product brief; it gives you back one self-contained Markdown file, storyboard first, that you hand to Claude (Opus) in a separate Claude Code session to build the video in [HyperFrames](https://hyperframes.heygen.com).

The prompt file carries everything the builder needs and nothing it has to invent: the message and features, the product's visual *terrain*, a concept with a spine, the look, a motion system, a seam map of transitions, every frame specified (event, reads, words, layout, depth, motion with eases and durations, camera, materials such as glass, gradients, shine and glints, transition out, frame check), plus the build rules and the render-and-verify loop. The builder does not need this skill installed.

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

claude.ai: zip the `skills/motion-storyboard` folder and upload it as a custom skill in your skills settings; then ask for a video prompt in any chat.

The skill is only needed where you **write** prompts. The session that **builds** the video needs HyperFrames (`npx hyperframes skills update`), not this skill.

## Use

**Step 1: write the prompt (this skill).** In a Claude session that has the skill, describe the video, or fill `skills/motion-storyboard/templates/brief.md`:

> Write the video prompt for a 30-second 16:9 motion design video for AvioMax, a Nigerian online marketplace where verified sellers open stores and buyers shop safely, with Paystack payments and 6% commission. Audience: Nigerian shoppers and small sellers on Instagram, TikTok and WhatsApp. End line: "Shop smart. Sell big." Brand: Poppins Bold/Medium, charcoal #2D2D2D, white, accent #CC0000, no blue/green/purple. Assets: assets/logo.svg, assets/home.png, assets/vendor-dashboard.png, assets/music.mp3.

Claude works out the message, the terrain and five concepts, shows you its pick, then writes `aviomax-video-prompt.md`. The finished example is `skills/motion-storyboard/examples/aviomax-30s-prompt.md`.

**Step 2: build the video (any Opus session with HyperFrames).** Open Claude Code in the folder that holds the assets, add the prompt file, and say:

> Build the video in aviomax-video-prompt.md.

The builder reads HyperFrames' skills, measures the music's beats, builds frame by frame, renders, checks a still at every frame check, fixes, and hands you the MP4 with a list of anything it changed.

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
    11-storyboard-format.md       how each frame of the storyboard is specified
    12-build-and-review.md        self-review of the prompt; build and verify steps the prompt gives the builder
    13-reads-events-and-acting.md timing by reads, an event per frame, show-don't-write, sets, acting, medium
    14-house-look.md              the default look: dark premium, neon, glass, glints, real 3D
    hyperframes-map.md            capabilities, hard limits, term → building block
    measured-references.md        numbers measured from reference videos
  templates/
    video-prompt.md               the output: the prompt file's sections
    brief.md                      intake for a new video
  examples/aviomax-30s-prompt.md  a complete prompt, ready to hand to a builder
  recipes/
    materials.html                tested glass / gradient / chrome / shine / glint composition
    materials-render.jpg          frames from its render
    motion-profile.py             measures motion timing in reference videos
```

## Adding reference videos

Analyse new references with `recipes/motion-profile.py` and ffmpeg contact sheets (commands in `references/measured-references.md`), then add a section there: what it is, the numbers, the techniques worth borrowing. Learn craft, never copy content.
