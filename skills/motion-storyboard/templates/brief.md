# Video brief (input to the prompt writer)

Fill what you know; leave the rest blank and Claude will propose defaults. Claude turns this into
`<slug>-video-prompt.md`, which you then give to a fresh Opus session to build the video.

```
Write the video prompt for a [length]-second [16:9 | 9:16 | 1:1] motion design video for [product].
Use the motion-storyboard skill. Show me the concept before the full storyboard.

Product (one sentence):
Audience (who, where they watch, what they already believe):
What they should remember (one line):
End-card line / tagline:
CTA (URL, app name):

Features I want shown (most important first):
1.
2.
3.

Terrain hints (the world this product lives in; objects, places, actions):
Things never to show or say:

Brand
- Fonts: [assets/fonts/...]  (only these)
- Colours: background [#], text [#], one accent [#]; banned colours: [...]
- Logo: [assets/logo.svg]  (never distort or recolour)
- Material feel: [flat | glass | chrome | paper | neon | let Claude choose]
- Product screens to recreate: [assets/...]

Music: [assets/music.mp3, genre]  (licensed? yes/no)
Reference videos (craft to borrow, not content to copy): [links or files]

Music BPM if known: [  ]  (otherwise the prompt assumes one and the builder re-measures)
```
