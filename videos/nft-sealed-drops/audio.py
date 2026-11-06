"""Sound: three music cues from Openverse (Jamendo), sound effects, the voices, and the mix.

  python3 audio.py            → build/mix.wav (48 kHz stereo, -14 LUFS, -1 dBTP)

Effects come from sfx/ (Openverse, see sfx/credits.json) when a file is there; the rest are synthesized here,
so the mix always builds. The music bed follows the production bible: frantic percussion for the race, a
classical string loop for the open auction, a low synth pad for the Cloak room.
"""
import os
import subprocess

import numpy as np
import pyloudnorm
import soundfile as sf
from scipy.signal import butter, fftconvolve, sosfilt

import voice
from timeline import CUES, DURATION, END, START, VO

SR = 48000
N = int(DURATION * SR) + SR
HERE = os.path.dirname(os.path.abspath(__file__))
C = CUES
rng = np.random.default_rng(7)


# ─── helpers ────────────────────────────────────────────────────────────────
def filt(x, kind, hz, order=2):
    return sosfilt(butter(order, hz, kind, fs=SR, output="sos"), x, axis=0)


def decode(path, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start), "-i", path]
    if dur:
        cmd += ["-t", str(dur)]
    raw = subprocess.run(cmd + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def have(name):
    d = os.path.join(HERE, "sfx")
    for f in os.listdir(d):
        if os.path.splitext(f)[0] == name and os.path.getsize(os.path.join(d, f)) > 1000:
            return os.path.join(d, f)
    return None


def st(x):
    x = np.asarray(x, np.float32)
    return np.stack([x, x], 1) if x.ndim == 1 else x


def env(n, a=0.002, d=None, curve=4.0):
    t = np.arange(n) / SR
    e = np.minimum(t / max(a, 1e-4), 1)
    if d:
        e = e * np.exp(-t / d * curve / 4)
    return e


def noise(sec):
    return rng.standard_normal(int(sec * SR)).astype(np.float32)


def fade(x, fi=0.005, fo=0.02):
    x = x.copy()
    a, b = int(fi * SR), int(fo * SR)
    if a:
        x[:a] *= np.linspace(0, 1, a)[:, None] if x.ndim == 2 else np.linspace(0, 1, a)
    if b:
        x[-b:] *= np.linspace(1, 0, b)[:, None] if x.ndim == 2 else np.linspace(1, 0, b)
    return x


_ir = {}


def reverb(x, size=1.6, wet=0.3, tone=5000):
    key = (size, tone)
    if key not in _ir:
        n = int(size * SR)
        ir = np.stack([noise(size), noise(size)], 1) * np.exp(-np.arange(n) / SR * 6.9 / size)[:, None]
        _ir[key] = filt(ir, "low", tone) * 0.08
    x = st(x)
    w = np.stack([fftconvolve(x[:, c], _ir[key][:, c])[: len(x) + len(_ir[key]) - 1] for c in range(2)], 1)
    dry = np.vstack([x, np.zeros((len(w) - len(x), 2), np.float32)])
    return dry * (1 - wet) + w * wet


class Bus:
    def __init__(self):
        self.b = np.zeros((N, 2), np.float32)

    def add(self, t, x, gain=1.0, pan=0.0):
        x = st(x) * gain
        if pan:
            x = x * np.array([1 - max(pan, 0), 1 + min(pan, 0)], np.float32)
        i = int(round(t * SR))
        if i < 0:
            x, i = x[-i:], 0
        n = min(len(x), N - i)
        if n > 0:
            self.b[i:i + n] += x[:n]


# ─── synthesized effects ────────────────────────────────────────────────────
def whoosh(sec=0.45, up=True, bright=1.0):
    n = int(sec * SR)
    x = noise(sec)
    t = np.linspace(0, 1, n)
    out = np.zeros(n, np.float32)
    for k in range(8):  # a band-pass sweeping across the whoosh
        a, b = k * n // 8, (k + 1) * n // 8
        f = (300 + 3500 * bright * (t[(a + b) // 2] if up else 1 - t[(a + b) // 2]))
        out[a:b] = filt(x, "band", [max(80, f * 0.5), min(18000, f * 1.6)])[a:b]
    shape = np.sin(np.pi * t) ** 1.6
    w = out * shape
    return np.stack([w * np.linspace(1.2, 0.5, n), w * np.linspace(0.5, 1.2, n)], 1) * 0.9


def glitch_sfx(sec=0.3, seed=1):
    r = np.random.default_rng(seed)
    n = int(sec * SR)
    out = np.zeros(n, np.float32)
    i = 0
    while i < n:
        L = int(r.uniform(0.008, 0.05) * SR)
        kind = r.integers(0, 3)
        seg = np.arange(min(L, n - i))
        if kind == 0:
            s = np.sign(np.sin(2 * np.pi * r.uniform(80, 1800) * seg / SR))
        elif kind == 1:
            s = r.standard_normal(len(seg))
            s = np.round(s * 3) / 3
        else:
            s = np.zeros(len(seg))
        out[i:i + len(seg)] = s * r.uniform(0.2, 0.8)
        i += L
    out = filt(out, "high", 120)
    return fade(np.stack([out, np.roll(out, 90)], 1) * 0.5)


def pistol():
    n = int(1.4 * SR)
    crack = noise(1.4) * env(n, 0.0005, 0.05)
    crack = filt(crack, "high", 900) * 1.4 + filt(crack, "low", 2500)
    body = np.sin(2 * np.pi * 70 * np.arange(n) / SR * np.exp(-np.arange(n) / SR * 3)) * env(n, 0.001, 0.12)
    x = st(np.tanh((crack + body * 0.9) * 2.2) * 0.8)
    return reverb(x, 2.4, 0.45, 6000)  # outdoor slap off the stands


def gavel(hard=1.0):
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in
            [(310, 1.0, 38), (620, 0.6, 52), (1180, 0.45, 70), (2300, 0.25, 95), (155, 0.6, 30)])
    click = filt(noise(0.6), "high", 2500) * np.exp(-t * 400) * 0.8
    x = np.tanh((x + click) * 1.8 * hard) * 0.7
    return reverb(st(x), 1.4, 0.32, 4000)


def scratch():
    n = int(0.55 * SR)
    t = np.arange(n) / SR
    rate = np.concatenate([np.linspace(1, -1.6, n // 2), np.linspace(-1.6, 0.2, n - n // 2)])
    ph = np.cumsum(rate) / SR
    x = noise(0.55)
    x = filt(x, "band", [500, 4000])
    tone = np.sin(2 * np.pi * 220 * ph * 6) * 0.6 + np.sin(2 * np.pi * 523 * ph * 6) * 0.3
    y = (x * 0.35 + tone) * (0.4 + 0.6 * np.abs(rate) / 1.6) * env(n, 0.003)
    return fade(st(np.tanh(y * 1.5) * 0.6), 0.002, 0.08)


def servo(sec=1.2, f0=700, f1=1500, sad=False):
    n = int(sec * SR)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n) if not sad else np.linspace(f1, f0 * 0.5, n)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sign(np.sin(3 * ph))
    x *= 0.6 + 0.4 * np.sin(2 * np.pi * 38 * t)
    x = filt(x, "band", [300, 6000]) * np.sin(np.pi * t / sec) ** 0.6
    return fade(st(x * 0.35))


def plane(sec=3.0):
    n = int(sec * SR)
    t = np.arange(n) / SR
    x = filt(noise(sec), "low", 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 42 * t) ** 2)
    hum = sum(np.sin(2 * np.pi * h * 86 * (1 - 0.06 * t / sec) * t) / h for h in range(1, 6))
    y = (x * 0.8 + hum * 0.25) * np.sin(np.pi * np.minimum(t / sec * 1.1, 1)) ** 1.2
    return fade(np.stack([y * np.linspace(0.6, 1.2, n), y * np.linspace(1.2, 0.6, n)], 1) * 0.6, 0.3, 0.6)


def wind(sec):
    n = int(sec * SR)
    t = np.arange(n) / SR
    x = filt(noise(sec), "band", [180, 900]) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.31 * t + 1))
    return fade(st(x * 0.25), 0.4, 0.6)


def thud():
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 58 * t * np.exp(-t * 2)) * np.exp(-t * 9) + filt(noise(0.7), "low", 600) * np.exp(-t * 30) * 0.6
    return st(np.tanh(x * 2) * 0.8)


def flutter(sec=1.0, density=60, seed=3):
    r = np.random.default_rng(seed)
    out = np.zeros((int(sec * SR), 2), np.float32)
    for _ in range(int(density * sec)):
        L = int(r.uniform(0.01, 0.04) * SR)
        g = filt(r.standard_normal(L), "band", [1500, 7000]) * np.hanning(L) * r.uniform(0.1, 0.4)
        i = r.integers(0, len(out) - L)
        p = r.uniform(-1, 1)
        out[i:i + L, 0] += g * (1 - max(p, 0))
        out[i:i + L, 1] += g * (1 + min(p, 0))
    return out


def tick():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 300) + filt(noise(0.05), "high", 4000) * np.exp(-t * 500) * 0.5
    return st(x * 0.4)


def chime(f=880):
    n = int(3.0 * SR)
    t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * d) for m, a, d in [(1, 1, 1.4), (2.0, 0.45, 2.2), (2.76, 0.3, 3), (5.4, 0.12, 5)])
    return reverb(st(x * env(n, 0.002) * 0.35), 2.5, 0.4, 9000)


def impact(sec=2.5, low=42):
    n = int(sec * SR)
    t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * low * t * np.exp(-t * 0.6)) * np.exp(-t * 1.6)
    hit = filt(noise(sec), "low", 3000) * np.exp(-t * 14) * 0.7
    braam = sum(np.sign(np.sin(2 * np.pi * low * 2 * k * t * (1 + 0.003 * k))) for k in (1, 1.5, 2)) * np.exp(-t * 1.2) * 0.12
    braam = filt(braam, "low", 900)
    return reverb(st(np.tanh((sub + hit + braam) * 1.6) * 0.8), 2.8, 0.35, 3000)


def riser(sec=1.5):
    n = int(sec * SR)
    t = np.arange(n) / SR
    x = noise(sec)
    out = np.zeros(n, np.float32)
    for k in range(10):
        a, b = k * n // 10, (k + 1) * n // 10
        f = 400 * 2 ** (k / 10 * 4)
        out[a:b] = filt(x, "band", [f * 0.6, min(f * 1.6, 20000)])[a:b]
    y = out * (t / sec) ** 2
    return fade(st(y * 0.5), 0.05, 0.01)


def lock_clunk():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(95, 1, 14), (410, 0.5, 30), (1870, 0.3, 60), (3300, 0.2, 90)])
    x += filt(noise(0.9), "high", 3000) * np.exp(-t * 200) * 0.9
    return reverb(st(np.tanh(x * 2) * 0.8), 0.9, 0.25, 5000)


def pen(sec=2.0, seed=5):
    r = np.random.default_rng(seed)
    out = np.zeros(int(sec * SR), np.float32)
    i = 0
    while i < len(out) - SR // 10:
        L = min(int(r.uniform(0.05, 0.25) * SR), len(out) - i)
        g = filt(r.standard_normal(L), "band", [2500, 9000]) * (0.4 + 0.6 * np.abs(np.sin(np.linspace(0, r.uniform(6, 20), L))))
        out[i:i + L] += g * np.hanning(L) * 0.12
        i += L + int(r.uniform(0.02, 0.15) * SR)
    return st(out)


def room_tone(sec, hz=350, g=0.04):
    return st(filt(noise(sec), "low", hz) * g)


def murmur(sec, seed=11):
    """A crowd bed: many formant-filtered noise voices (stand-in when no recording is here)."""
    r = np.random.default_rng(seed)
    n = int(sec * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    for _ in range(14):
        f = r.uniform(300, 1100)
        v = filt(r.standard_normal(n), "band", [f * 0.7, f * 1.4])
        syl = np.clip(np.sin(2 * np.pi * r.uniform(2.5, 5) * t + r.uniform(0, 6)), 0, 1) ** 2
        p = r.uniform(-0.8, 0.8)
        out[:, 0] += v * syl * (1 - max(p, 0))
        out[:, 1] += v * syl * (1 + min(p, 0))
    return fade(out * 0.03, 0.4, 0.4)


def recorded(name, start=0.0, dur=None, gain=1.0):
    p = have(name)
    return decode(p, start, dur) * gain if p else None


# ─── music ──────────────────────────────────────────────────────────────────
def music_bed():
    m = Bus()
    # race: "The Power of Nature", its full-band entry lands on the pistol
    race = decode(os.path.join(HERE, "music", "m_race_power.mp3"), 23.40 - (C["PISTOL"] - START["3a"]), 24)
    race_len = END["7c"] - START["3a"] + 0.6
    race = race[: int(race_len * SR)]
    t = np.arange(len(race)) / SR + START["3a"]
    g = np.where(t < C["PISTOL"], 0.6, 1.0)
    g = np.where(t > START["7c"] + 0.6, np.clip(1 - (t - START["7c"] - 0.6) / 1.4, 0, 1), g)
    m.add(START["3a"], fade(race * g[:, None], 0.8, 0.3), 1.25)
    # auction: Mozart, Duet for Violin and Viola K.423, Rondeau, warm and polite
    auc = decode(os.path.join(HERE, "music", "m_auction_rondeau.mp3"), 2.0, END["10e"] - START["9a"] + 1)
    t = np.arange(len(auc)) / SR + START["9a"]
    g = np.where(t < C["GAVEL"], 0.75, 0.45)  # the room goes quiet after "Sold."
    m.add(START["9a"], fade(filt(auc, "low", 7000) * g[:, None], 0.15, 0.6), 1.0)
    # cloak: "Saint Wave", low synth pad, its full section arrives when every bid opens
    off = 44.4 - (C["OPEN"] - START["11a"])
    cl = decode(os.path.join(HERE, "music", "m_cloak_saintwave.mp3"), off, END["14"] - START["11a"] + 0.5)
    t = np.arange(len(cl)) / SR + START["11a"]
    g = np.interp(t, [START["11a"], START["11a"] + 2, C["OPEN"] - 0.2, C["OPEN"], END["13d"], C["END"] + 0.3, END["14"] - 1.2, END["14"]],
                  [0.0, 0.85, 0.85, 1.0, 1.0, 1.0, 1.0, 0.0])
    m.add(START["11a"], cl * g[:, None], 0.85)
    return m.b


# ─── effects cues ───────────────────────────────────────────────────────────
def effects():
    fx = Bus()
    # open: a museum at night, one scratch of a record
    fx.add(0, room_tone(C["SCRATCH"] + 0.1, 300, 0.05) * np.linspace(0, 1, int((C["SCRATCH"] + 0.1) * SR))[:, None] ** 0.5)
    fx.add(0.3, chime(523) * 0.5, 0.5)
    fx.add(C["SCRATCH"] - 0.03, scratch(), 1.0)
    fx.add(C["SCRATCH"] - 0.03, glitch_sfx(0.32, 2), 0.6)
    # race
    crowd = recorded("crowd_large", 3, END["8"] - START["3a"])
    if crowd is None:
        crowd = recorded("crowd_unfa", 2, END["8"] - START["3a"])
    if crowd is None:
        crowd = murmur(END["8"] - START["3a"], 4) * 1.4
    tt = np.arange(len(crowd)) / SR + START["3a"]
    cg = np.interp(tt, [START["3a"], C["PISTOL"], C["PISTOL"] + 0.3, START["6b"], START["7c"] + 0.5, START["8"]], [0.8, 0.9, 1.3, 1.0, 0.6, 0.0])
    fx.add(START["3a"], crowd * cg[:, None], 0.6)
    fx.add(START["3a"] - 0.06, whoosh(0.4), 0.7)
    fx.add(START["3a"] - 0.06, glitch_sfx(0.22, 3), 0.4)
    for s in ("3b", "3c", "4b", "5a", "5c", "6a", "6c", "7a", "7b", "7c"):
        fx.add(START[s] - 0.2, whoosh(0.4, up=s[-1] in "ac"), 0.55)
    fx.add(START["4a"] + 0.2, riser(C["PISTOL"] - START["4a"] - 0.2), 0.5)
    fx.add(C["PISTOL"], pistol(), 1.1)
    fx.add(C["PISTOL"], impact(1.8, 50), 0.6)
    fx.add(START["4b"], flutter(1.6, 50, 4), 0.8)
    fx.add(START["5a"], flutter(4.0, 30, 5), 0.6)
    for k, cap in enumerate(("CAP_CRASH", "CAP_FAILED", "CAP_GAS")):
        fx.add(C[cap], glitch_sfx(0.14, 10 + k), 0.55)
    fx.add(C["TRIP"], whoosh(0.3, False, 0.6), 0.5)
    fx.add(C["THUD"], thud(), 1.0)
    fx.add(C["THUD"], flutter(1.2, 120, 6), 0.9)
    fx.add(C["SERVO"] - 0.3, servo(1.0, 600, 1700), 0.9)
    fx.add(C["SERVO"] - 0.05, glitch_sfx(0.3, 20), 0.6)
    fx.add(START["6c"] - 0.1, whoosh(0.5, True, 1.4), 0.9)
    fx.add(START["6c"], servo(1.1, 900, 1900), 0.7)
    fx.add(C["GRAB"] + 0.4, servo(0.7, 500, 1200), 0.6)
    fx.add(C["CAP_BOTS"], glitch_sfx(0.16, 21), 0.5)
    fx.add(START["7b"] + 0.3, flutter(1.2, 90, 7), 0.9)
    pl = recorded("airplane", 18, 3.2, 1.0)
    fx.add(C["PLANE"] - 0.3, pl if pl is not None else plane(2.8), 0.9)
    fx.add(START["8"], wind(END["8"] - START["8"] + 0.3), 2.2)
    # smash cut to the auction house
    fx.add(C["SMASH"] - 0.18, glitch_sfx(0.42, 30), 0.9)
    fx.add(C["SMASH"], impact(1.6, 46), 0.5)
    fx.add(C["SMASH"] + 0.05, gavel(0.6), 0.5)  # a gavel tap calls the room to order
    fx.add(START["9a"], murmur(END["10e"] - START["9a"], 9) * np.linspace(0.6, 1.3, int((END["10e"] - START["9a"]) * SR))[:, None], 0.7)
    fx.add(C["GAVEL"] - 0.01, gavel(1.3), 1.25)
    fx.add(C["GAVEL"], impact(1.4, 55), 0.35)
    fx.add(C["CAP_SNIPED"], glitch_sfx(0.16, 31), 0.45)
    # into Cloak: hush, pad, clean hits
    fx.add(C["TO_CLOAK"] - 0.22, glitch_sfx(0.5, 40), 0.85)
    fx.add(C["TO_CLOAK"] - 0.2, whoosh(0.7, False, 0.7), 0.6)
    fx.add(C["TO_CLOAK"], impact(2.8, 38), 0.55)
    fx.add(C["TO_CLOAK"], room_tone(END["13d"] - C["TO_CLOAK"], 250, 0.035))
    p = recorded("pen", 0, 3.0, 0.9)
    fx.add(START["12a"] + 0.2, p if p is not None else pen(2.2), 0.8)
    fx.add(START["12b"] + 0.15, flutter(0.5, 40, 8), 0.5)
    fx.add(C["SEAL"] - 0.03, gavel(0.35) * 0.6, 0.6)
    fx.add(C["SEAL"], chime(1318) * 0.5, 0.45)
    for k in range(5):  # envelopes dropping into the glass box
        fx.add(START["12c"] + 0.7 + k * 0.62, flutter(0.25, 40, 40 + k), 0.6)
        fx.add(START["12c"] + 0.9 + k * 0.62, thud()[: SR // 6] * 0.15, 0.6)
    fx.add(C["BOTS_FLASH"], glitch_sfx(0.42, 50), 0.8)
    fx.add(C["BOTS_FLASH"], servo(0.42, 900, 1400), 0.4)
    tk = recorded("tick", 1.0, END["12d"] - C["TIMER"] + 2.0)
    for k in range(int((C["OPEN"] - C["TIMER"]) * 2) + 4):
        tt_ = C["OPEN"] - 0.5 * (k + 1)
        if tt_ > START["12c"] + 1.4:
            fx.add(tt_, tick(), 0.6 + 0.3 * (k < 2))
    fx.add(C["OPEN"] - 1.2, riser(1.2), 0.45)
    fx.add(C["OPEN"], chime(880), 0.9)
    fx.add(C["OPEN"], impact(2.2, 44), 0.45)
    fx.add(C["OPEN"] + 0.3, flutter(2.0, 140, 9), 0.85)  # paper fan
    fx.add(C["LINE"] - 0.1, whoosh(0.35, False, 1.2), 0.5)
    fx.add(C["LINE"], chime(1046), 0.6)
    ap = recorded("applause", 0, 4.0, 0.7)
    fx.add(START["13b"] + 0.1, ap if ap is not None else murmur(3.0, 12) * 1.5, 0.45)
    fx.add(START["13d"] + 0.4, flutter(0.8, 60, 13), 0.6)
    fx.add(C["CAP_CLOAK"], glitch_sfx(0.14, 60), 0.3)
    # end card and stinger
    fx.add(C["END"] - 0.12, glitch_sfx(0.34, 70), 0.7)
    fx.add(C["END"] + 0.1, impact(3.0, 40), 0.75)
    fx.add(C["END"] + 0.15, chime(659), 0.6)
    fx.add(C["END"] + 2.25, chime(1318) * 0.4, 0.4)
    fx.add(C["STINGER"] - 0.05, glitch_sfx(0.25, 80), 0.7)
    fx.add(C["STINGER"] + 0.05, room_tone(3.2, 200, 0.05))
    fx.add(C["STINGER"] + 0.1, servo(0.9, 300, 700), 0.5)  # the door creaks open
    fx.add(C["STINGER"] + 1.0, servo(0.5, 1200, 1900), 0.5)  # a grin
    fx.add(C["STINGER"] + 1.9 - 0.02, lock_clunk(), 1.2)
    fx.add(C["STINGER"] + 2.15, servo(1.0, 800, 1500, sad=True), 0.45)  # sad servo whir
    return fx.b


# ─── voices ─────────────────────────────────────────────────────────────────
def voices():
    v = Bus()
    gains = dict(narrator=1.0, auctioneer=0.85, rival=1.0, smirker=0.8, neighbour=0.85)
    pans = dict(narrator=0, auctioneer=0, rival=-0.25, smirker=0.2, neighbour=0.3)
    for t, who, text in VO:
        x = voice.line(text, who)
        if who != "narrator":
            x = reverb(x, 1.3, 0.22, 5000)  # the auction room
        else:
            x = reverb(x, 0.8, 0.07, 7000)  # a little air around the narrator
        v.add(t, x, gains[who], pans[who])
    return v.b


def duck(bus, vo, depth, attack=0.04, release=0.35):
    e = np.abs(vo).max(1)
    k = int(0.03 * SR)
    e = np.convolve(e, np.ones(k) / k, "same")
    on = (e > 0.02).astype(np.float32)
    g = np.zeros_like(on)
    a, r = 1 / (attack * SR), 1 / (release * SR)
    cur = 0.0
    for i in range(0, len(on), 64):  # block-wise smoothing is plenty at 48 kHz
        target = on[i]
        cur = cur + (target - cur) * min(1, (a if target > cur else r) * 64)
        g[i:i + 64] = cur
    return bus * (1 - depth * g)[:, None]


def main():
    vo = voices()
    mus = duck(music_bed(), vo, 0.6)
    fx = duck(effects(), vo, 0.3)
    mix = mus * 0.62 + fx * 0.8 + vo * 1.25
    mix = mix[: int(DURATION * SR)]
    meter = pyloudnorm.Meter(SR)
    lufs = meter.integrated_loudness(mix)
    mix = mix * 10 ** ((-14 - lufs) / 20)
    # soft limit to -1 dBTP
    ceil = 10 ** (-1 / 20)
    mix = np.tanh(mix / ceil) * ceil
    out = os.path.join(HERE, "build", "mix.wav")
    sf.write(out, mix.astype(np.float32), SR, subtype="PCM_24")
    print(f"{out}  {lufs:.1f} LUFS before norm, peak {np.abs(mix).max():.3f}")
    # stems for checking
    sf.write(os.path.join(HERE, "build", "vo.wav"), vo[: len(mix)] * 1.25, SR, subtype="PCM_16")


if __name__ == "__main__":
    main()
