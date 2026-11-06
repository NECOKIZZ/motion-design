"""The cut: every shot, in order, and every named moment the graphics and the sound hang on.

Shot ids follow the production bible (1-15). Each shot takes source seconds [a, b] of one clip and plays them
over `dur` output seconds (so speed = (b - a) / dur). Run this file to print the cut and write
overlay/timeline.js, which the HyperFrames graphics read so text lands on the same frames as the picture.
"""
import json
import os

FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS_DIR = os.environ.get("CLIPS_DIR", os.path.join(HERE, "build", "clips"))

# the 21 Veo clips from the three zips, by short name
CLIPS = {
    "auctioneer": "Video__Auctioneer_conducting_art_auction_e0282fb1.mp4",
    "competing": "Video__Bidders_at_auction_competing_10c9f7a3.mp4",
    "silent": "Video__Bidders_at_silent_art_auction_132d1b2f.mp4",
    "ready": "Video__People_in_suits_ready_to_172b0903.mp4",
    "track": "Video__People_in_suits_running_track_aa105d39.mp4",
    "sprint": "Video__People_in_suits_sprinting_forward_fba8d1fb.mp4",
    "gallery": "Video_2__Bidders_in_gallery_room_5353270c.mp4",
    "envelopes": "Video_2__Bidders_submitting_sealed_envelopes_6a995616.mp4",
    "opening": "Video_2__Blindfolded_bidders_watching_f_d83a3b0e.mp4",
    "pistol": "Video_2__Hand_firing_pistol_starting_race_6b635a26.mp4",
    "robots_art": "Video_2__Robots_lifting_artwork_and_escaping_59799b23.mp4",
    "stunned": "Video_2__Three_people_standing_by_pedestals_3f9b4e7e.mp4",
    "fall": "Video_2__Woman_running_clutching_cash_falls_630e4633.mp4",
    "robots_race": "video_3__Men_and_robots_running_race_469bf29c.mp4",
    "overtake": "video_3__Men_running_and_robots_sprinting_a772941a.mp4",
    "crouch": "video_3__People_in_suits_holding_cash_8a2f8d02.mp4",
    "refund": "video_3__People_lifting_blindfolds_in_ga_5c81802f.mp4",
    "unmask": "video_3__People_removing_blindfolds_in_gallery_89731ce5.mp4",
    "grab": "video_3__Robots_lift_framed_panels_away_f2fb152b.mp4",
    "door": "new__Robot_peers_through_door_gap_43527765.mp4",
    "maya_win": "new__Woman_celebrates_auction_win_196621d2.mp4",
}

# (bible shot, clip, src a, src b, output dur, look, extra)
#   look: museum | race | auction | cloak | end
#   extra: zoom=(from, to) camera push, key=True to fill green frames with the art, focus=(x, y) zoom centre 0..1
SHOTS = [
    ("1",   "auctioneer", 6.96, 9.90, 3.00, "museum",  dict(key=True, zoom=(1.0, 1.10), focus=(0.5, 0.47))),
    ("2",   "silent",     8.00, 9.95, 2.10, "museum",  dict(zoom=(1.06, 1.16))),
    ("3a",  "ready",      0.20, 1.70, 1.30, "race",    dict(zoom=(1.0, 1.05))),
    ("3b",  "crouch",     2.05, 3.95, 1.15, "race",    dict(zoom=(1.0, 1.06))),
    ("3c",  "crouch",     0.00, 1.95, 1.55, "race",    dict(zoom=(1.0, 1.06))),
    ("4a",  "pistol",     0.40, 1.95, 1.50, "race",    dict(zoom=(1.0, 1.04))),
    ("4b",  "pistol",     2.00, 3.50, 1.05, "race",    dict()),
    ("5a",  "fall",       0.55, 1.95, 1.35, "race",    dict()),
    ("5b",  "fall",       1.97, 3.90, 2.15, "race",    dict()),
    ("5c",  "fall",       3.93, 5.40, 0.95, "race",    dict()),
    ("6a",  "track",      1.50, 3.30, 1.30, "race",    dict()),
    ("6b",  "robots_race", 4.02, 6.00, 1.40, "race",   dict(zoom=(1.0, 1.08))),
    ("6c",  "overtake",   4.02, 5.95, 1.20, "race",    dict()),
    ("7a",  "grab",       0.00, 1.98, 1.60, "race",    dict(zoom=(1.0, 1.05))),
    ("7b",  "grab",       2.02, 3.98, 1.20, "race",    dict()),
    ("7c",  "grab",       4.02, 7.95, 2.05, "race",    dict()),
    ("8",   "stunned",    0.30, 4.00, 2.60, "race",    dict()),
    ("9a",  "auctioneer", 0.06, 2.95, 2.60, "auction", dict(key=True)),
    ("9b",  "auctioneer", 2.98, 4.94, 2.00, "auction", dict()),
    ("9c",  "auctioneer", 4.98, 6.90, 1.90, "auction", dict()),
    ("9d",  "silent",     2.02, 4.60, 1.60, "auction", dict(key=True)),
    ("10a", "competing",  0.00, 1.44, 1.46, "auction", dict()),
    ("10b", "competing",  1.48, 3.94, 2.50, "auction", dict()),
    ("10c", "competing",  3.98, 4.90, 0.94, "auction", dict()),
    ("10d", "competing",  4.94, 6.44, 1.40, "auction", dict()),
    ("10e", "competing",  6.48, 9.60, 2.60, "auction", dict(zoom=(1.0, 1.06))),
    ("11a", "gallery",    2.02, 3.94, 2.70, "cloak",   dict(zoom=(1.0, 1.08))),
    ("11b", "gallery",    3.98, 7.60, 3.00, "cloak",   dict(key=True, zoom=(1.0, 1.07))),
    ("12a", "envelopes",  0.00, 2.94, 2.40, "cloak",   dict(zoom=(1.0, 1.05))),
    ("12b", "envelopes",  2.98, 5.44, 2.30, "cloak",   dict()),
    ("12c", "envelopes",  5.48, 9.95, 3.60, "cloak",   dict(key=True, zoom=(1.0, 1.06))),
    ("12d", "opening",    0.00, 0.90, 0.90, "cloak",   dict(zoom=(1.0, 1.04))),
    ("13a", "opening",    1.48, 8.00, 5.40, "cloak",   dict()),
    ("13b", "maya_win",   2.90, 6.90, 3.20, "cloak",   dict(zoom=(1.0, 1.06))),
    ("13c", "refund",     2.48, 3.48, 1.00, "cloak",   dict()),
    ("13d", "refund",     3.52, 6.50, 2.40, "cloak",   dict()),
    ("14",  "refund",     6.50, 8.00, 5.50, "end",     dict(zoom=(1.0, 1.08))),
    ("15",  "door",       1.00, 7.60, 5.00, "stinger", dict()),
]


def build():
    out, t = [], 0.0
    for sid, clip, a, b, dur, look, extra in SHOTS:
        n = round(dur * FPS)
        out.append(dict(id=sid, clip=clip, a=a, b=b, start=round(t, 4), frames=n, dur=n / FPS, look=look, **extra))
        t += n / FPS
    return out, t


CUT, DURATION = build()
START = {s["id"]: s["start"] for s in CUT}
END = {s["id"]: s["start"] + s["dur"] for s in CUT}


def at(shot, src_t):
    """Output time of source second `src_t` inside shot `shot`."""
    s = next(x for x in CUT if x["id"] == shot)
    return s["start"] + (src_t - s["a"]) * s["dur"] / (s["b"] - s["a"])


# ─── named moments ──────────────────────────────────────────────────────────
CUES = dict(
    SCRATCH=START["2"],
    PISTOL=at("4a", 1.042),            # the shot cracks
    TRIP=at("5b", 2.55),               # heel catches
    THUD=at("5b", 3.25),               # she hits the track
    SERVO=START["6b"],
    GRAB=START["7a"],
    PLANE=START["7c"],
    SMASH=START["9a"],                 # race → auction
    GAVEL=at("10c", 4.22),             # "Sold."
    TO_CLOAK=START["11a"],
    SEAL=at("12b", 4.35),              # wax seal lands
    TIMER=START["12d"],
    OPEN=START["13a"],                 # timer hits zero, every envelope opens
    LINE=at("13a", 6.55),              # the clearing line drops
    CAP_SNIPED=START["10d"] + 0.10,    # "Fairer. Still sniped by $1."
    BOTS_FLASH=START["12c"] + 1.62,    # "Not the bots." a glitch of the sniper's eye
    UNMASK=at("13b", 3.45),            # Maya's blindfold comes off
    SPOT=at("13b", 3.75),              # her spotlight snaps on
    CAP_CLOAK=at("13b", 3.80),         # "No race. No bots. No cheeky boys."
    DOOR_SHUT=at("15", 5.40),          # the door closes on the sniper
    END=START["14"],
    STINGER=START["15"],
)

# narrator and cast: (time, speaker, line). Times are where each line starts.
VO = [
    (0.35, "narrator", "NFTs are art."),
    (START["2"] + 0.40, "narrator", "Or are they?"),
    (START["3a"] + 0.25, "narrator", "This is how they get sold."),
    (START["3c"] + 0.05, "narrator", "Thousands of buyers. One button."),
    (CUES["PISTOL"] + 0.42, "narrator", "Gas spikes."),
    (START["4b"] + 0.55, "narrator", "The site crashes."),
    (START["5a"] + 0.75, "narrator", "Transactions fail..."),
    (CUES["TRIP"] + 0.25, "narrator", "and you still pay the fees."),
    (START["6a"] + 0.05, "narrator", "While you're still refreshing..."),
    (START["6b"] + 0.30, "narrator", "the bots are already done."),
    (START["7a"] + 0.15, "narrator", "Bots don't wait in line."),
    (START["7b"] + 0.05, "narrator", "They take the whole drop..."),
    (START["7c"] + 0.45, "narrator", "and sell it back to you."),
    (START["8"] + 0.35, "narrator", "Welcome to the mint race."),
    (START["9a"] + 0.25, "narrator", "But art was never sold like this."),
    (START["9b"] + 0.15, "auctioneer", "One thousand."),
    (START["9b"] + 1.30, "auctioneer", "One thousand and one."),
    (START["9c"] + 1.15, "auctioneer", "Two thousand."),
    (START["10a"] + 0.2, "rival", "Ten thousand!"),
    (START["10b"] + 0.4, "smirker", "Ten thousand... and one."),
    (CUES["GAVEL"] + 0.4, "auctioneer", "Sold."),
    (START["10e"] + 0.55, "neighbour", "Cheeky boy."),
    (START["11a"] + 0.25, "narrator", "At Cloak, we take it one step further."),
    (START["12a"] + 0.20, "narrator", "Every bid is sealed."),
    (START["12a"] + 1.95, "narrator", "Nobody sees anyone else's."),
    (START["12c"] + 0.05, "narrator", "Not the other bidders."),
    (START["12c"] + 1.65, "narrator", "Not the bots."),
    (START["12c"] + 2.85, "narrator", "Not even us."),
    (START["13a"] + 0.15, "narrator", "When bidding closes, every bid opens at once."),
    (START["13a"] + 3.25, "narrator", "The highest bids win."),
    (START["13a"] + 5.05, "narrator", "And every winner pays the same price."),
    (START["14"] + 0.80, "narrator", "NFT sealed drops. Live on Cloak."),
]
RACE_SPEED = 1.08  # the race lines are read a touch quicker


def write_js(vo_durations=None):
    data = dict(fps=FPS, duration=DURATION, start=START, end=END, cues=CUES,
                vo=[dict(t=t, who=w, text=x, d=(vo_durations or {}).get(x, 1.5)) for t, w, x in VO])
    path = os.path.join(HERE, "overlay", "timeline.js")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("// generated by timeline.py, do not edit\nwindow.T = " + json.dumps(data, indent=1) + ";\n")
    return path


def vo_speed(t, who):
    return RACE_SPEED if who == "narrator" and START["3c"] <= t < START["9a"] else None


def vo_durations():
    import voice
    return {x: len(voice.line(x, w, vo_speed(t, w))) / voice.SR for t, w, x in VO}


if __name__ == "__main__":
    for s in CUT:
        sp = (s["b"] - s["a"]) / s["dur"] if s["clip"] else 0
        print(f'{s["id"]:>4}  {s["start"]:6.2f}  {s["dur"]:5.2f}s  x{sp:4.2f}  {s["look"]:<8} {s["clip"]}')
    print(f"total {DURATION:.2f}s")
    for k, v in CUES.items():
        print(f"  {k:<9} {v:6.2f}")
    print(write_js(vo_durations()))
