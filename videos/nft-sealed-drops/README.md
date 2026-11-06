# Cloak · NFT Sealed Drops launch film

An 82 s, 16:9, 1920×1080 film cut from the 21 Veo clips in `Video (2).zip`, `Video 2.zip` and `video 3.zip` plus two later shots (the sniper at the door, Maya's win), following the production bible (*Cloak NFT Sealed Drops · Video Production Bible*, Nov 4). Every step is code, so any change is one command away.

**Render:** [`renders/cloak-nft-sealed-drops.mp4`](renders/cloak-nft-sealed-drops.mp4) · subtitles: [`cloak-nft-sealed-drops.srt`](cloak-nft-sealed-drops.srt) · shots still to generate: [`VEO-PROMPTS.md`](VEO-PROMPTS.md)

## The cut

| Bible shot | Time | What plays |
|---|---|---|
| 1–2 Open | 0:00 | Art A keyed into the gold frame, museum-lit, "NFTs are art." Record scratch and a glitch on "Or are they?" |
| 3–8 Race | 0:05 | Suits walk to the line, the five pieces at the finish, the pistol (negative flash, shake), Maya falls, the Snipers blur past (RGB split), grab the art and leave by plane, the Suits stand at empty pedestals. Gas meter HUD, "Site crashes. Failed transactions. Gas wars." |
| 9–10 Open auction | 0:27 | Glitch smash cut to the auction house. Live bid board climbs to $10,000, then $10,001, gavel (negative flash), SOLD. "Cheeky boy." "Fairer. Still sniped by $1." |
| 11–13 Cloak | 0:44 | The Cloak Auctioneer, blindfolded bidders, sealed envelopes ("BID SEALED"), "Who can read your bid" (bidders, bots, Cloak, all sealed), the timer, every envelope opens, the clearing line, blindfolds off, refunds. "No race. No bots. No cheeky boys." |
| 14 End card | 1:09 | Cloak mark, "NFT sealed drops. Live on Cloak.", the five pieces in their slots, cloak.boblabs.tech |
| 15 Stinger | 1:17 | A Sniper walks up to a door left ajar, its red eye fills the gap, the door shuts, SEALED lights up on it |

The five pieces (`assets/art/`, cut from the footage itself) keep the bible's slots everywhere, left to right D B **A** C E, with Art A in the gold frame at the centre. The keyer finds every green-screen frame, groups pieces split by heads or glass into one frame, and fills it with the right piece, perspective-matched, with the people in front kept.

Each act has its own grade, as in the bible: harsh warm midday with signal yellow for the race, tungsten and deep red for the auction, cool teal with amber for Cloak.

## Build

```bash
pip install numpy scipy opencv-python-headless pillow soundfile pyloudnorm kokoro-onnx
# build/clips/  = the 21 mp4s from the three zips (flat)
# build/models/ = kokoro-v1.0.onnx and voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases)
python3 timeline.py                  # print the cut, synthesize any new voice lines, write overlay/timeline.js
(cd overlay && npx --yes hyperframes@0.8.145 render --format png-sequence --fps 24 -o ../build/overlay)
python3 edit.py                      # → build/picture.mp4 (picture + graphics)
python3 audio.py                     # → build/mix.wav (-14 LUFS, -1 dBTP)
ffmpeg -i build/picture.mp4 -i build/mix.wav -c:v libx264 -preset slow -crf 23 -maxrate 12M -bufsize 24M \
  -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart renders/cloak-nft-sealed-drops.mp4
```

| File | What it decides |
|---|---|
| `timeline.py` | every shot (clip, source in/out, length, look), named moments, voice lines and their times |
| `edit.py` | speed ramps, keying, grades, glitches, negative flashes, whips, blur dissolves, shakes, grain |
| `overlay/index.html` | HyperFrames graphics: chapter tags, subtitles, captions, gas meter, bid board, sealed-bid HUD, clearing price, end card, stinger door |
| `audio.py` | the three music cues, every sound effect, the voices and the mix |
| `voice.py` | the cast: narrator and the four auction voices |
| `tools/openverse.py` | Openverse search and download with license info into `sfx/credits.json` |
| `tools/sheet.py` | contact sheets for review |

## Voices

All voices are [ElevenLabs](https://elevenlabs.io), generated once per line and cached in `assets/vo/` (committed, so rebuilds cost nothing). The narrator is **Bill**; the Old Auctioneer is **Daniel**, the Rival **Adam**, the Smirker **Callum**, the Neighbour **George**. Narration uses `eleven_multilingual_v2` (race lines read 8% quicker); the auction characters and the hushed open use the expressive `eleven_v3` with performance tags (`[whispers]`, `[shouting, confident]`, `[smugly, quietly] … [pause] …`, `[amused chuckle]`), listed in `DIRECTED` in `voice.py`. Every line was checked with ElevenLabs speech to text: all 32 transcribe exactly as written. `VO_ENGINE=kokoro` falls back to local Kokoro voices for uncached lines.

The API key is never in the code: the session's network proxy adds it to requests to api.elevenlabs.io.

## Sound

Music is from [Openverse](https://openverse.org) (Jamendo), cut so each act's music lands on the picture: the race track's full-band entry hits on the pistol, and the Cloak pad's lift arrives when every bid opens. The 39 sound effects are generated with ElevenLabs text to sound effects (`tools/sfx_gen.py`, prompts in `sfx_el/prompts.json`) and peak-normalized on load; `audio.py` falls back to synthesized stand-ins for any missing file. Transitions are whooshes, whip pans and blur dissolves; glitches are kept to the record scratch and the sniper's eye on "Not the bots".

## Credits (required for CC BY music)

- "The Power of Nature" by REC, [Jamendo](https://www.jamendo.com/track/1199522), CC BY 3.0
- "Duet for Violin and Viola, K.423 Rondeau" (W. A. Mozart) by Ivan Dolgunov, [Jamendo](https://www.jamendo.com/track/1545466), CC BY 3.0
- "Saint Wave" by Soft and Furious, [Jamendo](https://www.jamendo.com/track/1535210), CC BY 3.0

All three are edited (cut, filtered, levelled). Voices and sound effects: ElevenLabs. On ElevenLabs' free plan the output must credit ElevenLabs and isn't licensed for commercial use; a paid plan removes both. Suggested credit line for the post:

> Music: "The Power of Nature" by REC, Mozart's K.423 Rondeau by Ivan Dolgunov, "Saint Wave" by Soft and Furious (CC BY 3.0, via Jamendo).
