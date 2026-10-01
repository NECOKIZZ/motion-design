# Builds assets/soundtrack.wav for v2: MusicGen bed (cand-a, shifted 4 beats so its stops land before P3, P5, P7) + SFX on the beat grid.
import numpy as np, librosa, soundfile as sf, scipy.signal as ss, os
SR = 48000; DUR = 42.0; N = int(SR * DUR); t = np.arange(N) / SR
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx")
PER, OFF, SHIFT = 0.428519, 0.183, 4 * 0.428519
P = lambda p, k=0: OFF + (8 * p + k) * PER - 0.017
A3, F0, F1, F2, S8, S9, L0, L1 = P(3), P(5, 4), P(6), P(7), P(8), P(9), P(10), P(11)

def load(path, sr=SR):
    y, _ = librosa.load(path, sr=sr, mono=False)
    return np.stack([y, y]) if y.ndim == 1 else y
def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
def env(pts): ts, gs = zip(*pts); return np.interp(t, ts, gs)

m = load(os.path.join(ROOT, "assets/bgm/cand-a.wav"))
i0 = int(SHIFT * SR); m = m[:, i0:i0 + N]; m = np.pad(m, ((0, 0), (0, N - m.shape[1])))
m *= 10 ** ((-16.5 - db(m)) / 20)
mix = m * env([(0, 0), (0.25, 1), (DUR - 1.6, 1), (DUR, 0)])

def sfx(name, at, g=1.0, rate=1.0, trim_start=0.0):
    y = load(os.path.join(SFX, name + ".mp3"), sr=int(SR * rate)) if rate != 1.0 else load(os.path.join(SFX, name + ".mp3"))
    y = y[:, int(trim_start * SR):]
    i = int(at * SR); j = min(N, i + y.shape[1])
    if i < N and j > max(i, 0): mix[:, max(i, 0):j] += y[:, max(0, -i):j - i] * g

sfx("whoosh-cinematic", 0.1, 0.25)
sfx("impact-bass-2", P(1, 2) - 0.02, 0.5)
sfx("impact-bass-1", P(2, 3) - 0.02, 0.45); sfx("sparkle", P(2, 3) + 0.1, 0.22)
sfx("whoosh", A3 - 0.45, 0.4)
for k in (3, 4, 5): sfx("click", P(3, k), 0.45)
sfx("click-soft", P(4, 2), 0.4); sfx("key-press", P(4, 2) + 0.06, 0.25)
sfx("whoosh-short", P(4, 4), 0.4); sfx("chime", P(4, 5), 0.3); sfx("pop", P(4, 5), 0.25)
sfx("whoosh-short", P(5) - 0.05, 0.28); sfx("key-press", P(5) + 0.2, 0.3); sfx("key-press", P(5) + 0.28, 0.3)
sfx("sparkle", P(5, 2), 0.28)
sfx("whoosh", F0 - 0.35, 0.38)
for i in range(5): sfx("ping", F0 + 1.0 + i * 0.09, 0.12, rate=1 / (1 + 0.07 * i))
riser = load(os.path.join(SFX, "riser.mp3")); rl = riser.shape[1] / SR
sfx("riser", F2 - rl, 0.3)
sfx("whoosh", F2 - 0.4, 0.45); sfx("impact-bass-1", F2 - 0.01, 0.85)
sfx("chime", F2 + 0.95, 0.3); sfx("pop", P(7, 4) + 0.1, 0.28)
sfx("whoosh", S8 - 0.3, 0.4)
for i in range(4): sfx("click-soft", P(8, 1) + i * 0.12, 0.22)
sfx("chime", P(8, 3) + 0.8, 0.25)
sfx("whoosh", S9 - 0.35, 0.4)
for i in range(10): sfx("click-soft", S9 + 0.05 + i * 0.07, 0.12)
sfx("whoosh-cinematic", L0 - 0.2, 0.3); sfx("impact-bass-2", L0 + 0.93, 0.6)
sfx("sparkle", L1 + 0.35, 0.22); sfx("click", P(11, 4), 0.5)

mix *= env([(0, 1), (DUR - 1.6, 1), (DUR, 0)])
pk = np.max(np.abs(mix)); mix = np.tanh(mix / max(pk, 1e-9) * 1.2) * 0.9
sf.write(os.path.join(ROOT, "assets/soundtrack.wav"), mix.T.astype(np.float32), SR, subtype="PCM_16")
print("ok rms", round(db(mix), 1))
