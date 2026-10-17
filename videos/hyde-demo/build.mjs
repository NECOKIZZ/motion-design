// Generates index.html from one edit table: footage segments, callouts, taps,
// zooms, voice-over, captions and sound effects all hang off the same clock.
// Run: node build.mjs
import { writeFileSync } from "node:fs";

const INTRO = 15.0;
const OUTRO_LEN = 24.0;
const VO_DUR = {
  i1: 5.248, i2: 2.944, i3: 3.925, d1: 4.544, d2: 1.237, d3: 5.205, d4: 4.8,
  d5: 5.781, d6: 1.131, d7: 4.971, d8: 4.181, d9: 5.291, d10: 4.48, d11: 4.48,
  o1: 1.749, o2: 4.587, o3: 4.757, o4: 5.867, o5: 2.197,
};

// ---------- footage segments (source seconds) ----------
const SEGS = [
  { id: "a", src: [35.3, 40.1], rate: 1 },
  { id: "b", src: [40.1, 44.3], rate: 1 },
  { id: "c1", src: [44.3, 57.6], rate: 2.5 },
  { id: "c2", src: [57.6, 59.3], rate: 1 },
  { id: "d", src: [59.3, 89.9], rate: 3.5 },
  { id: "e0", src: [89.9, 92.0], rate: 1.5 },
  { id: "e1", src: [92.0, 95.2], rate: 1 },
  { id: "e2", src: [95.2, 100.6], rate: 1.8 },
  { id: "f1", src: [100.6, 106.6], rate: 2 },
  { id: "f2", src: [106.6, 108.0], rate: 1 },
  { id: "g1", src: [108.0, 111.6], rate: 2 },
  { id: "g2", src: [111.6, 116.6], rate: 1 },
  { id: "h1", src: [117.0, 122.0], rate: 3 },
  { id: "h2", src: [122.0, 124.9], rate: 1.2 },
  { id: "h3", src: [124.9, 126.25], rate: 1 },
  { id: "i1", src: [127.3, 131.0], rate: 1.3 },
  { id: "i2", src: [131.0, 134.6], rate: 1 },
  { id: "j1", src: [136.5, 143.3], rate: 3 },
  { id: "j2", src: [143.3, 147.0], rate: 1.5 },
  { id: "j3", still: "assets/stills/solscan.png", len: 5.5 },
  { id: "k", still: "assets/stills/solscan.png", len: 7.5 },
];
let t = INTRO;
const S = {};
for (const s of SEGS) {
  s.start = t;
  s.len = s.len ?? (s.src[1] - s.src[0]) / s.rate;
  s.end = t + s.len;
  t = s.end;
  S[s.id] = s;
}
const DEMO_END = t;
const OUTRO = DEMO_END;
const TOTAL = OUTRO + OUTRO_LEN;
// global time of a source second inside a segment
const g = (id, src) => S[id].start + (src - S[id].src[0]) / S[id].rate;
const r3 = (n) => Math.round(n * 1000) / 1000;

// ---------- voice-over placement ----------
const VO = [
  ["i1", 0.6], ["i2", 6.4], ["i3", 9.8],
  ["d1", S.a.start + 0.2], ["d2", S.b.start + 1.0], ["d3", S.c1.start + 0.2],
  ["d4", S.d.start + 0.5], ["d5", S.e0.start + 0.5], ["d6", g("f1", 105.6) - 0.05],
  ["d7", S.g1.start + 0.4], ["d8", S.h1.start + 0.35], ["d9", S.i1.start + 0.2],
  ["d10", S.j2.start + 0.6], ["d11", S.k.start + 0.5],
  ["o1", OUTRO + 0.4], ["o2", OUTRO + 2.6], ["o3", OUTRO + 7.5],
  ["o4", OUTRO + 12.8], ["o5", OUTRO + 19.5],
];

const CAPTIONS = {
  d1: "Here's the recipient: a separate Solana wallet, | holding just under 1 USDC.",
  d2: "I copy its address,",
  d3: "and ask Claude, connected to my PayBox wallet, | to send 1 USDC there, privately.",
  d4: "Claude loads Hyde through PayBox | and asks for my approval before every step.",
  d5: "PayBox shows the transfer, | coming from my wallet: KnnL… | One tap to sign.",
  d6: "And it's confirmed.",
  d7: "Hyde sent it through MagicBlock's private rollup, | so it can't be linked on-chain back to me.",
  d8: "Now, the recipient's side. | The balance is up by exactly 1 USDC.",
  d9: "But look at the sender. It's not my wallet. | It's an address starting 5inNv.",
  d10: "Solscan agrees: | a successful transfer from that address to the recipient.",
  d11: "My wallet signed. A different address paid. | Nothing on-chain connects the two.",
};

// ---------- callouts (source-pixel boxes on the 720x1600 screen) ----------
// tone: "v" = violet (the point), "w" = white (context)
const CALLOUTS = [
  { at: g("a", 38.3), to: S.a.end, box: [195, 156, 495, 220], label: "Recipient wallet", tone: "w", pos: "below" },
  { at: g("a", 38.7), to: S.a.end, box: [18, 1306, 702, 1380], label: "Before: 0.988 USDC", tone: "v", pos: "above" },
  { at: g("b", 41.3), to: g("b", 43.1), box: [60, 918, 660, 1014], label: "Recipient address", tone: "v", pos: "above" },
  { at: S.c2.start + 0.1, to: S.c2.end, box: [36, 748, 668, 892], label: "The whole instruction", tone: "v", pos: "above" },
  { at: S.e1.start + 0.15, to: S.e1.end, box: [118, 704, 644, 748], label: "Sender: my PayBox wallet", tone: "w", pos: "above" },
  { at: g("f1", 105.6), to: S.f2.end, box: [26, 694, 694, 760], label: "Confirmed on Solana", tone: "v", pos: "below" },
  { at: S.g2.start + 0.25, to: S.g2.end, box: [26, 560, 694, 744], label: "Private route", tone: "v", pos: "above" },
  { at: S.h3.start + 0.1, to: S.h3.end, box: [18, 1030, 702, 1114], label: "After: 1.988 USDC  (+1)", tone: "v", pos: "above" },
  { at: g("i1", 129.6), to: S.i1.end, box: [130, 896, 288, 938], label: "Who sent this?", tone: "v", pos: "below" },
  { at: S.i2.start + 0.35, to: S.i2.end, box: [42, 1190, 308, 1280], label: "Not my wallet", tone: "v", pos: "below" },
  { at: S.j3.start + 0.3, to: S.j3.end, box: [176, 752, 378, 794], label: "Paid by 5inNv…bhHxuw", tone: "v", pos: "above" },
  { at: S.j3.start + 1.2, to: S.j3.end, box: [428, 752, 614, 794], label: "To the recipient", tone: "w", pos: "below" },
];

// ---------- taps ----------
const TAPS = [
  { at: g("b", 42.2), x: 360, y: 1066 },
  { at: g("c2", 59.0), x: 648, y: 938 },
  ...[65.0, 69.5, 76.5, 85.5, 89.5].map((s) => ({ at: g("d", s), x: 360, y: 1190 })),
  { at: g("e2", 99.5), x: 360, y: 725 },
  { at: g("i1", 127.6), x: 360, y: 518 },
  { at: g("i1", 130.8), x: 360, y: 895 },
];

// ---------- camera punch-ins on the screen (source-pixel centre, scale) ----------
const ZOOMS = [
  { at: S.b.start + 1.1, hold: 1.9, cx: 360, cy: 966, s: 1.14 },
  { at: S.c2.start, hold: 1.3, cx: 352, cy: 820, s: 1.1 },
  { at: S.e1.start, hold: 2.75, cx: 381, cy: 726, s: 1.3 },
  { at: S.i2.start + 0.15, hold: 3.0, cx: 230, cy: 1220, s: 1.6 },
  { at: S.j3.start, hold: 5.1, cx: 395, cy: 790, s: 1.55 },
];

const CHAPTERS = [
  [S.a.start, "01", "The recipient"],
  [S.c1.start, "02", "Ask privately"],
  [S.e0.start, "03", "Sign once"],
  [S.g1.start, "04", "Routed privately"],
  [S.h1.start, "05", "Check the receiver"],
  [S.j1.start, "06", "Check the chain"],
  [S.k.start, "07", "The proof"],
];

// ---------- sound effects ----------
const SFX = [];
const sfx = (file, at, vol, dur) => SFX.push({ file, at: r3(at), vol, dur });
sfx("whoosh-cinematic", INTRO - 0.7, 0.5, 2.2);
for (const c of CALLOUTS) sfx("pop", c.at, 0.22, 0.6);
for (const tp of TAPS) sfx("click-soft", tp.at - 0.02, 0.7, 0.36);
sfx("typing", S.c1.start + 0.3, 0.18, 1.5);
sfx("typing", S.c1.start + 1.8, 0.18, 1.5);
sfx("typing", S.c1.start + 3.3, 0.18, 1.5);
sfx("whoosh-short", S.d.start - 0.1, 0.35, 0.57);
sfx("chime", g("f1", 105.6), 0.45, 2.5);
sfx("whoosh-short", S.h1.start - 0.1, 0.35, 0.57);
sfx("whoosh-short", S.j1.start - 0.1, 0.35, 0.57);
sfx("sparkle", S.j3.start + 0.3, 0.35, 1.8);
sfx("whoosh", S.k.start, 0.4, 0.57);
sfx("impact-bass-1", S.k.start + 2.05, 0.6, 2.1);
sfx("whoosh-cinematic", OUTRO - 0.5, 0.45, 2.5);
// intro: ledger ticks, the redaction swipe, the link snapping
[0.35, 0.65, 0.95, 1.25, 1.55, 1.85].forEach((s) => sfx("key-press", s, 0.25, 0.43));
sfx("whoosh-short", 6.15, 0.45, 0.57);
sfx("impact-bass-2", 6.85, 0.45, 2.5);
sfx("glitch-1", 11.75, 0.25, 1.2);
// outro: chain chips, payroll rows, button, lockup
[7.55, 8.25, 9.0, 9.7, 10.35, 10.9, 11.55].forEach((s) => sfx("pop", OUTRO + s, 0.25, 0.6));
[13.2, 13.6, 14.0, 14.4, 14.8].forEach((s) => sfx("key-press", OUTRO + s, 0.25, 0.43));
sfx("click-soft", OUTRO + 16.35, 0.7, 0.36);
sfx("chime", OUTRO + 16.5, 0.35, 2.5);
sfx("impact-bass-1", OUTRO + 19.4, 0.55, 2.1);

// ---------- markup ----------
const box = (b) => `left:${b[0]}px;top:${b[1]}px;width:${b[2] - b[0]}px;height:${b[3] - b[1]}px`;

const videos = SEGS.filter((s) => s.src).map((s) => `
        <video id="v-${s.id}" class="clip shot" src="assets/demo.mp4" muted playsinline
          data-start="${r3(s.start)}" data-duration="${r3(s.len)}" data-media-start="${s.src[0]}"${s.rate !== 1 ? ` data-playback-rate="${s.rate}"` : ""}
          data-track-index="0"></video>`).join("");

const stills = SEGS.filter((s) => s.still).map((s) => `
        <img id="v-${s.id}" class="clip shot" src="${s.still}" alt=""
          data-start="${r3(s.start)}" data-duration="${r3(s.len)}" data-track-index="0" />`).join("");

const callouts = CALLOUTS.map((c, i) => `
        <div id="co-${i}" class="clip callout tone-${c.tone} pos-${c.pos}" style="${box(c.box)}"
          data-start="${r3(c.at)}" data-duration="${r3(c.to - c.at)}" data-track-index="2">
          <div class="co-ring"></div>
          <div class="co-label"><span>${c.label}</span></div>
        </div>`).join("");

const taps = TAPS.map((tp, i) => `
        <div id="tap-${i}" class="clip tap" style="left:${tp.x - 60}px;top:${tp.y - 60}px"
          data-start="${r3(tp.at - 0.05)}" data-duration="0.75" data-track-index="3">
          <div class="tap-ring"></div><div class="tap-dot"></div>
        </div>`).join("");

const chapters = CHAPTERS.map(([at, n, label], i) => {
  const to = i + 1 < CHAPTERS.length ? CHAPTERS[i + 1][0] : DEMO_END;
  return `
      <div id="ch-${i}" class="clip chapter" data-start="${r3(at)}" data-duration="${r3(to - at)}" data-track-index="5">
        <span class="ch-n">${n}</span><span class="ch-t">${label}</span>
      </div>`;
}).join("");

// captions: split on "|" and time each chunk by its share of the characters
const capEls = [];
for (const [id, at] of VO) {
  const text = CAPTIONS[id];
  if (!text) continue;
  const parts = text.split("|").map((p) => p.trim());
  const total = parts.reduce((n, p) => n + p.length, 0);
  let c = at;
  parts.forEach((p, k) => {
    const len = (VO_DUR[id] * p.length) / total;
    const end = k === parts.length - 1 ? at + VO_DUR[id] + 0.25 : c + len;
    capEls.push(`
      <div id="cap-${id}-${k}" class="clip caption" data-start="${r3(c)}" data-duration="${r3(end - c)}" data-track-index="6">
        <p>${p}</p>
      </div>`);
    c += len;
  });
}

const voAudio = VO.map(([id, at]) => `
    <audio id="vo-${id}" class="clip" src="assets/vo/${id}.wav" data-start="${r3(at)}" data-duration="${VO_DUR[id]}" data-track-index="20" data-volume="1"></audio>`).join("");

const sfxAudio = SFX.map((s, i) => `
    <audio id="sfx-${i}" class="clip" src="assets/sfx/${s.file}.mp3" data-start="${s.at}" data-duration="${s.dur}" data-track-index="${30 + (i % 8)}" data-volume="${s.vol}"></audio>`).join("");

// music bed: louder alone in the intro and outro, tucked under the demo voice
const bedVol = JSON.stringify({ version: 1, lanes: [{ target: "volume", points: [
  { t: 0, v: 0 }, { t: 0.8, v: 0.55 }, { t: INTRO - 0.5, v: 0.55 }, { t: INTRO + 0.6, v: 0.32 },
  { t: OUTRO - 0.6, v: 0.32 }, { t: OUTRO + 0.4, v: 0.55 }, { t: TOTAL - 2.5, v: 0.55 }, { t: TOTAL, v: 0 },
] }] });

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Hyde · private Solana payment demo</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0a0b14; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #0a0b14;
        font-family: Montserrat, sans-serif; color: #eeebff; }
      #stage { position: absolute; inset: 0; }
      .glow { position: absolute; border-radius: 50%; filter: blur(90px); }
      #glow-a { width: 900px; height: 900px; left: -380px; top: 200px; background: rgba(155, 123, 255, 0.22); }
      #glow-b { width: 800px; height: 800px; right: -360px; bottom: 120px; background: rgba(155, 123, 255, 0.16); }
      #grid { position: absolute; inset: 0; opacity: 0.5;
        background-image: linear-gradient(rgba(155,123,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(155,123,255,0.07) 1px, transparent 1px);
        background-size: 60px 60px;
        -webkit-mask-image: radial-gradient(ellipse at center, #000 30%, rgba(0,0,0,0) 75%); mask-image: radial-gradient(ellipse at center, #000 30%, rgba(0,0,0,0) 75%); }

      /* top band */
      #brand { position: absolute; left: 151px; top: 52px; display: flex; align-items: center; gap: 16px; }
      .mark { position: relative; width: 44px; height: 46px; }
      .mark i { position: absolute; top: 0; width: 11px; height: 46px; border-radius: 3px; background: #eeebff; }
      .mark i:first-child { left: 0; } .mark i:nth-child(2) { right: 0; }
      .mark b { position: absolute; left: -4px; right: -4px; top: 17px; height: 12px; border-radius: 3px; background: #9b7bff; }
      #brand .word { font-weight: 900; font-size: 38px; letter-spacing: -0.03em; }
      #brand .sub { font-family: "JetBrains Mono", monospace; font-size: 22px; color: #b9b2e0; margin-left: 6px; }
      .chapter { position: absolute; right: 151px; top: 52px; height: 48px; display: flex; align-items: center; gap: 12px; }
      .ch-n { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 22px; color: #0a0b14; background: #9b7bff; border-radius: 8px; padding: 6px 10px; }
      .ch-t { font-weight: 700; font-size: 28px; letter-spacing: -0.01em; }

      /* the phone screen window */
      #screen { position: absolute; left: 151px; top: 150px; width: 778px; height: 1728px; border-radius: 34px; overflow: hidden;
        background: #f6f5f1; box-shadow: 0 0 0 2px rgba(155,123,255,0.45), 0 30px 120px rgba(0,0,0,0.6), 0 0 80px rgba(155,123,255,0.18); }
      #scaler { position: absolute; left: 0; top: 0; width: 720px; height: 1600px; transform: scale(1.0805); transform-origin: 0 0; }
      #cam { position: absolute; left: 0; top: 0; width: 720px; height: 1600px; transform-origin: 0 0; }
      .shot { position: absolute; left: 0; top: 0; width: 720px; height: 1600px; object-fit: cover; }
      #dim { position: absolute; inset: 0; background: #0a0b14; opacity: 0; }

      /* callouts */
      .callout { position: absolute; }
      .co-ring { position: absolute; inset: -6px; border-radius: 12px; border: 4px solid #9b7bff;
        box-shadow: 0 0 0 4px rgba(155,123,255,0.22), 0 0 24px rgba(155,123,255,0.55); }
      .tone-w .co-ring { border-color: #0a0b14; box-shadow: 0 0 0 4px rgba(10,11,20,0.15), 0 0 18px rgba(10,11,20,0.25); }
      .co-label { position: absolute; left: -6px; white-space: nowrap; }
      .pos-above .co-label { bottom: calc(100% + 12px); }
      .pos-below .co-label { top: calc(100% + 12px); }
      .co-label span { display: inline-block; font-weight: 800; font-size: 22px; letter-spacing: 0.01em; color: #fff; background: #9b7bff;
        padding: 7px 12px; border-radius: 8px; box-shadow: 0 6px 18px rgba(10,11,20,0.25); }
      .tone-w .co-label span { background: #0a0b14; }

      /* taps */
      .tap { position: absolute; width: 120px; height: 120px; }
      .tap-ring { position: absolute; inset: 0; border-radius: 50%; border: 5px solid #9b7bff; }
      .tap-dot { position: absolute; left: 38px; top: 38px; width: 44px; height: 44px; border-radius: 50%; background: rgba(155,123,255,0.55); }

      /* fast-forward chip */
      #ff { position: absolute; left: 50%; top: 210px; margin-left: -110px; width: 220px; height: 64px; border-radius: 32px; display: flex; align-items: center; justify-content: center; gap: 10px;
        background: rgba(10,11,20,0.86); color: #eeebff; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 28px; box-shadow: 0 0 0 2px rgba(155,123,255,0.6); }
      #ff i { display: inline-block; width: 0; height: 0; border-top: 12px solid transparent; border-bottom: 12px solid transparent; border-left: 16px solid #9b7bff; }

      /* captions */
      .caption { position: absolute; left: 90px; right: 90px; top: 1640px; display: flex; justify-content: center; }
      .caption p { max-width: 900px; text-align: center; font-weight: 700; font-size: 38px; line-height: 1.25; letter-spacing: -0.01em; color: #fff;
        background: rgba(10,11,20,0.88); border-radius: 18px; padding: 16px 26px; box-shadow: 0 0 0 2px rgba(155,123,255,0.35), 0 12px 40px rgba(0,0,0,0.35); }

      /* the proof card */
      #proof { position: absolute; inset: 0; }
      .pcard { position: absolute; left: 70px; width: 940px; border-radius: 28px; padding: 30px 30px 34px; background: rgba(20,21,36,0.92);
        box-shadow: 0 0 0 2px rgba(155,123,255,0.35), 0 30px 80px rgba(0,0,0,0.5); }
      #pc-1 { top: 330px; } #pc-2 { top: 1110px; }
      .pk { font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.08em; color: #9b7bff; text-transform: uppercase; }
      .pv { margin-top: 10px; font-weight: 900; font-size: 64px; letter-spacing: -0.03em; }
      .pv em { font-style: normal; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 58px; color: #fff; }
      .crop { position: relative; margin-top: 22px; width: 880px; overflow: hidden; border-radius: 14px; background: #fff; }
      .crop img { position: absolute; }
      #neq { position: absolute; left: 0; right: 0; top: 820px; text-align: center; font-weight: 900; font-size: 240px; line-height: 240px; color: #9b7bff;
        text-shadow: 0 0 40px rgba(155,123,255,0.6); }
      #nolink { position: absolute; left: 0; right: 0; top: 1600px; text-align: center; font-weight: 900; font-size: 64px; letter-spacing: -0.03em; }
      #nolink span { color: #9b7bff; }

      .sub-comp { position: absolute; inset: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${r3(TOTAL)}" data-width="1080" data-height="1920">
      <div id="stage">
        <div id="glow-a" class="glow"></div>
        <div id="glow-b" class="glow"></div>
        <div id="grid"></div>
      </div>

      <div id="brand" class="clip" data-start="${INTRO}" data-duration="${r3(DEMO_END - INTRO)}" data-track-index="5">
        <div class="mark"><i></i><i></i><b></b></div><span class="word">Hyde</span><span class="sub">live demo</span>
      </div>
      ${chapters}

      <div id="screen">
        <div id="scaler">
          <div id="cam">${videos}${stills}${callouts}${taps}
          </div>
        </div>
        <div id="dim"></div>
      </div>

      <div id="ff" class="clip" data-start="${r3(S.d.start + 0.1)}" data-duration="${r3(S.d.len - 0.2)}" data-track-index="4"><i></i><i></i><span>3.5×</span></div>
      ${capEls.join("")}

      <div id="proof" class="clip" data-start="${r3(S.k.start)}" data-duration="${r3(S.k.len)}" data-track-index="7">
        <div id="pc-1" class="pcard">
          <div class="pk">Signed by · my PayBox wallet</div>
          <div class="pv"><em>KnnL…itiQ</em></div>
          <div class="crop" style="height:${Math.round(46 * 1.415)}px"><img src="assets/stills/paybox.png" alt="" style="width:${Math.round(720 * 1.415)}px;left:${-Math.round(18 * 1.415)}px;top:${-Math.round(704 * 1.415)}px" /></div>
        </div>
        <div id="neq">≠</div>
        <div id="pc-2" class="pcard">
          <div class="pk">Paid by · on-chain, per Solscan</div>
          <div class="pv"><em>5inNv…Hxuw</em></div>
          <div class="crop" style="height:${Math.round(48 * 1.313)}px"><img src="assets/stills/solscan.png" alt="" style="width:${Math.round(720 * 1.313)}px;left:${-Math.round(20 * 1.313)}px;top:${-Math.round(748 * 1.313)}px" /></div>
        </div>
        <div id="nolink">No on-chain <span>link.</span></div>
      </div>

      <div id="intro" class="sub-comp" data-composition-id="intro" data-composition-src="compositions/intro.html"
        data-start="0" data-duration="${INTRO}" data-track-index="10" data-width="1080" data-height="1920"></div>
      <div id="outro" class="sub-comp" data-composition-id="outro" data-composition-src="compositions/outro.html"
        data-start="${r3(OUTRO)}" data-duration="${OUTRO_LEN}" data-track-index="11" data-width="1080" data-height="1920"></div>
    </div>
    ${voAudio}
    <audio id="bed" class="clip" src="assets/bgm/bed.wav" data-start="0" data-duration="${r3(TOTAL)}" data-track-index="21" data-volume="1"
      data-automation='${bedVol}'></audio>
    ${sfxAudio}
    <script>
      const D = ${JSON.stringify({
        INTRO, DEMO_END, OUTRO,
        callouts: CALLOUTS.map((c) => r3(c.at)),
        taps: TAPS.map((tp) => r3(tp.at - 0.05)),
        zooms: ZOOMS.map((z) => ({ ...z, at: r3(z.at), hold: r3(z.hold) })),
        chapters: CHAPTERS.map((c) => r3(c[0])),
        captions: capEls.map((e) => [e.match(/id="([^"]+)"/)[1], Number(e.match(/data-start="([^"]+)"/)[1])]),
        ff: r3(S.d.start + 0.1),
        k: r3(S.k.start),
      })};
      const tl = gsap.timeline({ paused: true });

      // ambient background (finite, seek-safe)
      tl.fromTo("#glow-a", { x: 0, y: 0, scale: 1 }, { x: 120, y: 160, scale: 1.15, duration: ${r3(TOTAL / 2)}, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0);
      tl.fromTo("#glow-b", { x: 0, y: 0 }, { x: -140, y: -200, duration: ${r3(TOTAL / 2)}, ease: "sine.inOut", yoyo: true, repeat: 1 }, 0);

      // the screen window lands as the intro hands off
      tl.fromTo("#screen", { scale: 0.86, y: 40, opacity: 0 }, { scale: 1, y: 0, opacity: 1, duration: 0.55, ease: "expo.out" }, D.INTRO - 0.25);
      tl.fromTo("#brand", { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, D.INTRO + 0.15);

      // chapters: rise in fast
      D.chapters.forEach((at, i) => {
        tl.fromTo("#ch-" + i + " .ch-n", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "back.out(2)" }, at + 0.05);
        tl.fromTo("#ch-" + i + " .ch-t", { x: 30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, at + 0.12);
      });

      // callouts: ring snaps in from slightly larger, label pops after
      D.callouts.forEach((at, i) => {
        tl.fromTo("#co-" + i + " .co-ring", { scale: 1.25, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.32, ease: "back.out(2.2)" }, at);
        tl.fromTo("#co-" + i + " .co-label", { y: 10, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.26, ease: "power3.out" }, at + 0.12);
        tl.fromTo("#co-" + i + " .co-ring", { boxShadow: "0 0 0 4px rgba(155,123,255,0.22), 0 0 24px rgba(155,123,255,0.55)" },
          { boxShadow: "0 0 0 10px rgba(155,123,255,0.0), 0 0 36px rgba(155,123,255,0.8)", duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 1 }, at + 0.4);
      });

      // taps: dot presses, ring expands out
      D.taps.forEach((at, i) => {
        tl.fromTo("#tap-" + i + " .tap-dot", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.12, ease: "power2.out" }, at);
        tl.to("#tap-" + i + " .tap-dot", { scale: 0.7, opacity: 0, duration: 0.35, ease: "power2.in" }, at + 0.3);
        tl.fromTo("#tap-" + i + " .tap-ring", { scale: 0.3, opacity: 1 }, { scale: 1.5, opacity: 0, duration: 0.6, ease: "expo.out" }, at + 0.05);
      });

      // camera punch-ins (cam transform-origin is 0 0, so solve x/y for the centre)
      const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
      D.zooms.forEach((z) => {
        const x = clamp(360 - z.s * z.cx, 720 - 720 * z.s, 0);
        const y = clamp(800 - z.s * z.cy, 1600 - 1600 * z.s, 0);
        tl.fromTo("#cam", { scale: 1, x: 0, y: 0 }, { scale: z.s, x, y, duration: 0.55, ease: "power3.inOut", immediateRender: false }, z.at);
        tl.to("#cam", { scale: 1, x: 0, y: 0, duration: 0.45, ease: "power3.inOut" }, z.at + 0.55 + z.hold);
      });

      // fast-forward chip
      tl.fromTo("#ff", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(2)" }, D.ff);
      tl.fromTo("#ff i", { opacity: 0.35 }, { opacity: 1, duration: 0.35, ease: "none", yoyo: true, repeat: 23, stagger: 0.12 }, D.ff + 0.2);

      // captions: quick rise
      D.captions.forEach(([id, at]) => {
        tl.fromTo("#" + id + " p", { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: 0.22, ease: "power3.out" }, at);
      });

      // the proof: footage sinks back, cards land, the ≠ slams on the beat
      tl.fromTo("#dim", { opacity: 0 }, { opacity: 0.86, duration: 0.5, ease: "power2.out" }, D.k);
      tl.fromTo("#screen", { filter: "blur(0px)" }, { filter: "blur(6px)", duration: 0.5, ease: "power2.out" }, D.k);
      tl.fromTo("#pc-1", { y: -80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, D.k + 0.35);
      tl.fromTo("#pc-2", { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, D.k + 1.4);
      tl.fromTo("#neq", { scale: 2.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: "power4.in" }, D.k + 1.8);
      tl.fromTo("#neq", { rotation: 0 }, { rotation: -4, duration: 0.08, ease: "none", yoyo: true, repeat: 3 }, D.k + 2.1);
      tl.fromTo("#nolink", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, D.k + 4.2);

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
`;
writeFileSync(new URL("./index.html", import.meta.url), html);
console.log(JSON.stringify({ INTRO, DEMO_END: r3(DEMO_END), OUTRO: r3(OUTRO), TOTAL: r3(TOTAL),
  segs: SEGS.map((s) => [s.id, r3(s.start), r3(s.end)]), vo: VO.map(([id, at]) => [id, r3(at), r3(at + VO_DUR[id])]) }));
