# Hyde · PayBox hackathon demo edit

The edited demo video is `renders/hyde-demo.mp4` (1080×1920, 9:16, about 1:52).

It starts from the raw screen recording `screen-20261017-212235.mp4` (3:07, silent) at the repo root and adds:

- **Intro (0–15s):** a motion graphic. A public ledger fills up, its senders and recipients get redacted, the Hyde lockup appears, and the link between "You" and "Them" breaks. A violet frame then becomes the phone screen.
- **Demo (15–88s):** the recording, cut down to the actions and sped up through the waits (approvals run at 3.5×). It has seven chapters, callout boxes on every address and balance, tap ripples, punch-ins and captions. A proof card closes the demo: the wallet that signed (`KnnL…itiQ`) is not the address that paid (`5inNv…Hxuw`).
- **Outro (88–112s):** a motion graphic. One private USDC balance spendable on seven chains, private payroll for up to 25 people, and the lockup again.
- **Sound:** a HyperFrames TTS voice-over (Kokoro, voice `af_heart`), a MusicGen music bed, and HyperFrames' bundled sound effects.

Look: ink `#0A0B14` and Hyde violet `#9B7BFF`, set in Montserrat and JetBrains Mono.

## Editing

`index.html` is generated. Edit the tables in `build.mjs` (segments, callouts, taps, zooms, voice-over, captions, SFX), then run:

```bash
node build.mjs
npx hyperframes check
npx hyperframes render -o renders/hyde-demo.mp4 --fps 30
```

The intro and outro live in `compositions/intro.html` and `compositions/outro.html`.
