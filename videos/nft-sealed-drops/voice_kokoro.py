"""Voices: every line is synthesized locally with Kokoro (no API) and cached in build/vo/.

The narrator is Kokoro's deepest male voice pitched down with formants kept, plus chest and presence EQ.
The auction characters each get their own voice so they read as different people.
"""
import hashlib
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.environ.get("KOKORO_DIR", os.path.join(HERE, "build", "models"))
CACHE = os.path.join(HERE, "build", "vo_kokoro")

# name, speed, pitch ratio (rubberband, formants kept), EQ chain
CAST = {
    "narrator":   dict(voice="am_onyx",   speed=0.96, pitch=0.88, lang="en-us",
                       eq="highpass=f=60,equalizer=f=120:t=q:w=1:g=3.5,equalizer=f=350:t=q:w=1.2:g=-2,"
                          "equalizer=f=3200:t=q:w=1:g=2.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=120"),
    "auctioneer": dict(voice="bm_george", speed=1.12, pitch=0.94, lang="en-gb",
                       eq="highpass=f=90,equalizer=f=2500:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3"),
    "rival":      dict(voice="am_fenrir", speed=1.05, pitch=0.95, lang="en-us",
                       eq="highpass=f=80,equalizer=f=1800:t=q:w=1:g=3,acompressor=threshold=-22dB:ratio=4"),
    "smirker":    dict(voice="am_puck",   speed=0.82, pitch=0.97, lang="en-us",
                       eq="highpass=f=80,equalizer=f=4000:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3"),
    "neighbour":  dict(voice="bm_lewis",  speed=0.92, pitch=0.97, lang="en-gb",
                       eq="highpass=f=80,equalizer=f=2200:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3"),
}

_kokoro = None


def _engine():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"), os.path.join(MODEL_DIR, "voices-v1.0.bin"))
    return _kokoro


def line(text, who="narrator"):
    """Mono float32 at 48 kHz, silence trimmed."""
    c = CAST[who]
    key = hashlib.sha1(f"{c}|{text}".encode()).hexdigest()[:12]
    path = os.path.join(CACHE, f"{who}-{key}.wav")
    if not os.path.exists(path):
        os.makedirs(CACHE, exist_ok=True)
        samples, sr = _engine().create(text, voice=c["voice"], speed=c["speed"], lang=c["lang"])
        audio = resample_poly(samples.astype(np.float64), SR, sr).astype(np.float32)
        audio = _process(audio, c)
        loud = np.flatnonzero(np.abs(audio) > 0.012)
        audio = audio[max(loud[0] - 480, 0): loud[-1] + 2400]
        sf.write(path, audio, SR)
    audio, _ = sf.read(path, dtype="float32")
    return audio


def _process(audio, c):
    af = f"rubberband=pitch={c['pitch']}:formant=preserved:pitchq=quality,{c['eq']}"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                          "-af", af, "-f", "f32le", "-"], input=audio.tobytes(), capture_output=True, check=True).stdout
    out = np.frombuffer(raw, np.float32).copy()
    return out / (np.abs(out).max() + 1e-9) * 0.9


if __name__ == "__main__":
    who = sys.argv[1]
    for text in sys.argv[2:]:
        print(f"{len(line(text, who)) / SR:.2f}s  {text}")
