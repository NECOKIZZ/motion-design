# kickoff.cash · 60s motion graphic

Built with the `motion-storyboard` skill (house look: dark glass, purple light curtains, glints, real 3D) and rendered in HyperFrames.

- `kickoff-cash-video-prompt.md`: the storyboard prompt (concept, look, seam map, every frame).
- `index.html`: the composition (GSAP timeline, glass UI, footage, audio).
- `scene3d.js`: the Three.js layer (football, glass pitch, 5×5 scoreline grid, stake chips, extruded K logo), rendered from seek time.
- `tools/music.py`: generates `assets/music.wav`, an original 120 BPM track with the drop at 32s.

Footage is not committed (`*.mp4` is ignored). To rebuild, put the five clips in `assets/` (`stadium.mp4`, `match.mp4`, `celebrate.mp4`, `palmer.mp4`, `crowd.mp4`, re-encoded at 30 fps with `-g 30`) plus `goal-audio.wav` and `palmer-audio.wav`, then:

```bash
npx hyperframes check .
npx hyperframes render . -o renders/kickoff-cash.mp4
```
