"""Generate the film's sound effects with ElevenLabs (text to sound effects), once each, into sfx_el/.

  python3 tools/sfx_gen.py            → generates whatever is missing (about 10 credits per second)
  python3 tools/sfx_gen.py --list     → shows the list and the credits it would cost

The key comes from the session's network proxy, never from this file.
"""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "sfx_el")
API = "https://api.elevenlabs.io/v1/sound-generation"

# name: (seconds, prompt influence, prompt)
SFX = {
    # race
    "stadium_murmur": (14, 0.4, "Large outdoor athletics stadium, crowd murmuring and chattering before a race starts, anticipation, open air, distant"),
    "crowd_roar": (4, 0.5, "Stadium crowd erupts into a loud roaring cheer as a race starts, outdoor"),
    "starter_pistol": (2, 0.7, "A single starter pistol shot fired outdoors in a stadium, sharp crack with a slapback echo off the stands"),
    "running_footsteps": (5, 0.5, "A crowd of people in leather dress shoes sprinting fast on a rubber running track, heavy breathing, close"),
    "body_fall": (1.5, 0.6, "A person falls hard onto a rubber running track, heavy body thud with clothes rustle, no voice"),
    "cash_flutter": (3, 0.5, "A thick stack of paper banknotes thrown and scattering in the wind, bills fluttering through the air"),
    "servo_whine": (2.5, 0.6, "High pitched robotic servo motors whining as a fast humanoid robot sprints past, mechanical, sci-fi"),
    "robot_footsteps": (3, 0.6, "Heavy metal robot feet sprinting fast on asphalt, rhythmic mechanical clanks and hydraulic hiss"),
    "plane_flyby": (4, 0.5, "A small propeller plane flies low overhead and climbs away into the sky, engine roar fading"),
    "wind": (4, 0.4, "Desolate wind blowing across an empty stadium, lonely and quiet"),
    "stamp": (1, 0.7, "A heavy rubber stamp slammed down hard on paper, punchy thump"),
    "target_lock": (1, 0.6, "Electronic targeting system locks on, quick rising beeps ending in a sharp lock tone, sci-fi HUD"),
    "counter_up": (2, 0.6, "Digital counter rapidly ticking up, fast electronic clicks accelerating"),
    "error_buzz": (1, 0.6, "Computer error buzz, harsh low digital fail sound"),
    # auction
    "auction_murmur": (12, 0.4, "Posh auction house room tone, well dressed crowd murmuring quietly, wood panelled hall with soft reverb"),
    "gavel_tap": (1, 0.6, "A light single tap of a wooden gavel on a sound block in a large quiet room"),
    "paddle_swish": (1, 0.6, "Several cardboard bidding paddles raised quickly in an auction, quick swish of movement and cloth rustle"),
    "snort_laugh": (1.5, 0.6, "A single man gives a short amused snort of laughter through his nose, close up, indoors"),
    "crowd_gasp": (2, 0.5, "An auction room audience gasps in surprise together, then a murmur"),
    # cloak
    "pen_scratch": (3, 0.6, "A fountain pen writing on thick paper, close up, scratching strokes, quiet room"),
    "wax_seal": (1.5, 0.6, "A brass wax seal stamp pressed firmly into warm wax on an envelope, soft squish and solid press"),
    "envelope_drop": (1, 0.6, "A sealed paper envelope dropping into a glass box onto a pile of envelopes, soft papery thud"),
    "clock_tick": (4, 0.6, "A precise mechanical clock ticking, steady seconds, close and clean, final tick louder"),
    "chime": (3, 0.6, "A single crystal clear bell chime, elegant and bright, long shimmering tail, reveal moment"),
    "paper_fan": (3, 0.5, "Dozens of paper envelopes bursting out of a box and flying through the air, fluttering whoosh of paper"),
    "soft_applause": (4, 0.5, "A small elegant audience applauding softly and warmly in a gallery, with a delighted gasp"),
    # transitions
    "whoosh_fast_1": (1, 0.6, "Fast cinematic whoosh, air swish passing by quickly from left to right, clean"),
    "whoosh_fast_2": (1, 0.6, "Quick punchy whip pan whoosh transition, cinematic swish"),
    "whoosh_fast_3": (1, 0.6, "Short sharp cinematic swoosh with a slight low rumble, trailer transition"),
    "whoosh_soft": (1.5, 0.5, "Soft airy breathy whoosh transition, gentle and elegant"),
    "impact": (3, 0.6, "Deep cinematic trailer boom impact with a heavy sub bass tail"),
    "riser": (2, 0.6, "Cinematic tension riser building quickly up into a hit, rising noise and synth"),
    "logo_sting": (4, 0.5, "Elegant cinematic logo reveal, a soft deep impact then a shimmering synth swell and sparkle, premium and calm"),
    "record_scratch": (1, 0.7, "A vinyl record scratch stopping the music abruptly, comedic"),
    "glitch": (0.8, 0.6, "Short subtle digital glitch, data stutter"),
    # stinger
    "door_creak": (2, 0.6, "A heavy wooden door slowly creaking open in a quiet corridor"),
    "door_slam": (1.5, 0.6, "A heavy door slams shut hard, solid wooden bang with a short echo in a corridor"),
    "lock_clunk": (1, 0.7, "A heavy metal lock bolt clunks shut, deep mechanical click"),
    "sad_robot": (2, 0.6, "A disappointed robot powering down, sad descending servo whir and a low beep"),
}


def cost(names):
    return sum(SFX[n][0] for n in names) * 10


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    missing = [n for n in SFX if not os.path.exists(os.path.join(OUT, n + ".mp3"))]
    print(f"{len(missing)} to generate, about {cost(missing):.0f} credits")
    if "--list" in sys.argv:
        sys.exit()
    meta_path = os.path.join(OUT, "prompts.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    for n in missing:
        sec, infl, prompt = SFX[n]
        body = json.dumps(dict(text=prompt, duration_seconds=sec, prompt_influence=infl)).encode()
        req = urllib.request.Request(API, data=body, method="POST", headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
        except Exception as e:
            print("FAIL", n, e)
            continue
        open(os.path.join(OUT, n + ".mp3"), "wb").write(data)
        meta[n] = dict(seconds=sec, prompt_influence=infl, prompt=prompt)
        json.dump(meta, open(meta_path, "w"), indent=2)
        print("ok", n)
