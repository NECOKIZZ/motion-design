"""Voices: ElevenLabs text to speech, one request per line, cached in assets/vo/ (committed, so rebuilds cost nothing).

The API key is never in this code: the session's network proxy adds it to requests to api.elevenlabs.io.
Set VO_ENGINE=kokoro to fall back to the local Kokoro voices for a line that isn't cached yet.

  python3 voice.py narrator "Some line."     → prints the duration (generates and caches it if new)
"""
import hashlib
import json
import os
import subprocess
import sys
import urllib.request

import numpy as np
import soundfile as sf

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "assets", "vo")
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128"
MODEL = "eleven_multilingual_v2"

# ElevenLabs built-in voices (usable on every plan)
CAST = {
    "narrator":   dict(voice="pqHfZKP75CvOlQylNhV4", name="Bill",   stability=0.50, similarity=0.80, style=0.30, speed=1.00),
    "auctioneer": dict(voice="onwK4e9ZLuTAKqWW03F9", name="Daniel", stability=0.40, similarity=0.80, style=0.45, speed=1.12),
    "rival":      dict(voice="pNInz6obpgDQGcFmaJgB", name="Adam",   stability=0.30, similarity=0.80, style=0.65, speed=1.05),
    "smirker":    dict(voice="N2lVS1w4EtoT3dr4eOWO", name="Callum", stability=0.35, similarity=0.80, style=0.60, speed=0.88),
    "neighbour":  dict(voice="JBFqnCBsd6RMkjVDRZzb", name="George", stability=0.40, similarity=0.80, style=0.55, speed=0.95),
}
# lines performed with the expressive v3 model and a direction (the subtitles show the plain line)
DIRECTED = {
    ("narrator", "NFTs are art."): "[whispers] NFTs are art.",
    ("narrator", "Or are they?"): "[curious, a half smile] Or are they?",
    ("auctioneer", "One thousand."): "[briskly] One thousand.",
    ("auctioneer", "One thousand and one."): "[briskly] One thousand and one.",
    ("auctioneer", "Two thousand."): "[briskly, raising his voice] Two thousand!",
    ("auctioneer", "Sold."): "[firmly, final] Sold.",
    ("rival", "Ten thousand!"): "[shouting, confident] Ten thousand!",
    ("smirker", "Ten thousand... and one."): "[smugly, quietly] Ten thousand... [pause] and one.",
    ("neighbour", "Cheeky boy."): "[amused chuckle] Cheeky boy.",
}

# post: a little low cut, gentle compression, no pitch change (these voices are already the voices we want)
POST = "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=150"


def _key(text, who, speed):
    c = CAST[who]
    d = DIRECTED.get((who, text))
    parts = [MODEL, c, speed, text] if d is None else ["eleven_v3", c, speed, d]
    return hashlib.sha1(json.dumps(parts).encode()).hexdigest()[:12]


def path_for(text, who="narrator", speed=None):
    return os.path.join(CACHE, f"{who}-{_key(text, who, speed)}.wav")


def line(text, who="narrator", speed=None):
    """Mono float32 at 48 kHz, silence trimmed. `speed` overrides the cast speed (0.7 to 1.2)."""
    path = path_for(text, who, speed)
    if not os.path.exists(path):
        if os.environ.get("VO_ENGINE") == "kokoro":
            import voice_kokoro
            return voice_kokoro.line(text, who)
        os.makedirs(CACHE, exist_ok=True)
        c = CAST[who]
        d = DIRECTED.get((who, text))
        if d:  # v3 takes its direction from the tags; only stability applies
            body = json.dumps(dict(text=d, model_id="eleven_v3", voice_settings=dict(stability=0.5))).encode()
        else:
            body = json.dumps(dict(text=text, model_id=MODEL, voice_settings=dict(
                stability=c["stability"], similarity_boost=c["similarity"], style=c["style"],
                use_speaker_boost=True, speed=speed or c["speed"]))).encode()
        req = urllib.request.Request(API.format(voice=c["voice"]), data=body, method="POST",
                                     headers={"Content-Type": "application/json", "Accept": "audio/mpeg"})
        with urllib.request.urlopen(req, timeout=120) as r:
            mp3 = r.read()
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "-", "-af", POST, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                             input=mp3, capture_output=True, check=True).stdout
        audio = np.frombuffer(raw, np.float32).copy()
        loud = np.flatnonzero(np.abs(audio) > 0.01)
        audio = audio[max(loud[0] - 480, 0): loud[-1] + 2400]
        audio = audio / (np.abs(audio).max() + 1e-9) * 0.9
        sf.write(path, audio, SR, subtype="PCM_16")
    audio, _ = sf.read(path, dtype="float32")
    if who == "smirker":  # tighten his pause before "and one" to half a second, so the gavel can follow
        a, b = int(1.40 * SR), int(1.95 * SR)
        if len(audio) > b + SR // 2:
            audio = np.concatenate([audio[:a], audio[b:]])
    return audio


if __name__ == "__main__":
    who = sys.argv[1]
    for text in sys.argv[2:]:
        print(f"{len(line(text, who)) / SR:.2f}s  {text}")
