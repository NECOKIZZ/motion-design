# Builds assets/soundtrack.wav: MusicGen bed + build/drop shaping + synth drums + bundled SFX, all on the beat grid.
import numpy as np, librosa, soundfile as sf, scipy.signal as ss, os
SR = 48000; DUR = 30.0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx")
BEATS = [0.096,0.592,1.104,1.6,2.096,2.592,3.104,3.6,4.096,4.592,5.104,5.6,6.096,6.592,7.104,7.6,8.096,8.608,9.104,9.6,10.096,10.592,11.104,11.6,12.096,12.592,13.104,13.6,14.096,14.592,15.104,15.6,16.096,16.592,17.104,17.6,18.096,18.592,19.104,19.6,20.096,20.592,21.104,21.6,22.112,22.592,23.104,23.6,24.112,24.608,25.104,25.6,26.096,26.592,27.104,27.6,28.096,28.592,29.104,29.6]
P = lambda p, k=0: BEATS[p*8+k] - 0.017
C1,C2,C3,C4,C5,C6 = P(1),P(2),P(3),P(4),P(5),P(6)
N = int(SR*DUR); t = np.arange(N)/SR

def load(path, sr=SR):
    y, _ = librosa.load(path, sr=sr, mono=False)
    if y.ndim == 1: y = np.stack([y, y])
    return y
def rms_db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-12)
def env(points):  # piecewise-linear gain envelope [(time, gain)]
    ts, gs = zip(*points); return np.interp(t, ts, gs)

# ── music bed ──
m = load(os.path.join(ROOT, "assets/bgm/track.wav"))[:, :N]
m = np.pad(m, ((0,0),(0, N-m.shape[1])))
m *= 10**((-17 - rms_db(m))/20)                       # bring bed to about -17 dBFS RMS
b, a = ss.butter(4, 700/(SR/2), "low"); m_lp = ss.lfilter(b, a, m, axis=1)
b, a = ss.butter(2, 120/(SR/2), "high"); m_hp = ss.lfilter(b, a, m, axis=1)
# build (P3): filter opens; breath before the drop; drop full
full = env([(0,1),(C3-0.05,1),(C3+0.2,0.25),(C4-0.6,0.8),(C4-0.45,0.15),(C4-0.02,0.15),(C4,1),(28.4,1),(30,0)])
low  = env([(0,0),(C3-0.05,0),(C3+0.2,0.9),(C4-0.6,0.4),(C4-0.45,0.2),(C4-0.02,0.2),(C4,0),(30,0)])
mix = m*full + m_lp*low

# ── synth drums on the drop (C4 → C6) and the sign-off hit ──
def kick():
    n = int(0.42*SR); tt = np.arange(n)/SR
    f = 50 + 110*np.exp(-tt*28); ph = 2*np.pi*np.cumsum(f)/SR
    y = np.sin(ph)*np.exp(-tt*7.5) + 0.25*np.random.default_rng(1).standard_normal(n)*np.exp(-tt*120)
    return np.tanh(1.6*y)*0.9
def clap():
    n = int(0.25*SR); tt = np.arange(n)/SR; rng = np.random.default_rng(2)
    nz = rng.standard_normal(n); b,a = ss.butter(2,[900/(SR/2),5000/(SR/2)],"band"); nz = ss.lfilter(b,a,nz)
    e = np.zeros(n)
    for o in (0, 0.011, 0.022): e += (tt>=o)*np.exp(-(tt-o).clip(0)*60)
    e += (tt>=0.03)*np.exp(-(tt-0.03).clip(0)*16)*0.6
    return nz*e*0.55
def hat():
    n = int(0.06*SR); tt=np.arange(n)/SR; rng=np.random.default_rng(3)
    nz = rng.standard_normal(n); b,a = ss.butter(2,7000/(SR/2),"high"); return ss.lfilter(b,a,nz)*np.exp(-tt*70)*0.22
K, CL, H = kick(), clap(), hat()
drums = np.zeros(N)
def place_mono(buf, x, at, g=1.0):
    i = int(at*SR); j = min(N, i+len(x))
    if i < N: buf[i:j] += x[:j-i]*g
for bi, bt in enumerate(BEATS):
    if C4-0.03 <= bt < C6-0.1:
        place_mono(drums, K, bt, 0.85)
        if bi % 2 == 1: place_mono(drums, CL, bt, 0.9)
        place_mono(drums, H, bt + 0.248, 0.9)
    elif C3 <= bt < C4-0.6:                      # build: kick on each beat, rising
        place_mono(drums, K, bt, 0.35 + 0.4*(bt-C3)/(C4-C3))
# snare roll into the drop
roll_t = C4-0.6
for k in range(8):
    place_mono(drums, CL, roll_t + k*0.0625 + 0.06, 0.25 + 0.08*k)
place_mono(drums, K, C6, 0.9)
mix += np.stack([drums, drums])*0.8

# ── sfx ──
def sfx(name, at, g=1.0, rate=1.0):
    y = load(os.path.join(SFX, name+".mp3"), sr=int(SR*rate)) if rate != 1.0 else load(os.path.join(SFX, name+".mp3"))
    i = int(at*SR); j = min(N, i+y.shape[1])
    if i < N and j > max(i,0): mix[:, max(i,0):j] += y[:, max(0,-i):j-i]*g
LAND1 = P(1,1)+0.1; LAND7 = C6+0.35
sfx("whoosh-short", 0.2, 0.25)
sfx("click-soft", P(0,3)+0.3, 0.5); sfx("click-soft", P(0,4)+0.26, 0.5)
sfx("pop", P(0,5), 0.35)
sfx("whoosh", C1-0.4, 0.55)
sfx("impact-bass-2", LAND1-0.02, 0.6)
sfx("sparkle", P(1,5)+0.15, 0.3)
sfx("whoosh-cinematic", C2-0.75, 0.45)
for k,o in enumerate((0,0.2,0.42)): sfx("key-press", P(2,1)+o, 0.35)
for k,o in enumerate((0,0.25,0.45,0.65,0.85)): sfx("ping", P(2,4)+o+0.08, 0.18, rate=1/(1+0.06*k))
riser = load(os.path.join(SFX,"riser.mp3")); rl = riser.shape[1]/SR
sfx("riser", C4-min(rl, C4-C3+0.3), 0.35)
sfx("click-soft", P(3,4), 0.35)
sfx("impact-bass-1", C4-0.01, 0.9)
sfx("whoosh", C4-0.45, 0.5)
sfx("sparkle", P(4,1), 0.3)
sfx("chime", P(4,4)+1.0, 0.35)
sfx("whoosh-short", C5-0.3, 0.45)
for k,o in enumerate((P(5,1),P(5,2)+0.1,P(5,3)+0.2)): sfx("pop", o+0.1, 0.22)
sfx("sparkle", P(5,5), 0.3)
sfx("whoosh", C6-0.6, 0.5)
sfx("impact-bass-2", LAND7-0.02, 0.75)
sfx("pop", P(6,6)+0.1, 0.25)
sfx("sparkle", P(7,0)+0.3, 0.3)

# master: gentle glue + limiter, fade out
mix *= env([(0,1),(28.5,1),(30,0)])
peak = np.max(np.abs(mix)); mix = np.tanh(mix/max(peak,1e-9)*1.25)*0.89
sf.write(os.path.join(ROOT, "assets/soundtrack.wav"), mix.T.astype(np.float32), SR, subtype="PCM_16")
print("ok", rms_db(mix), "peak", np.max(np.abs(mix)))
