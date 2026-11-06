"""Picture: cuts, speed ramps, the art keyed into the green frames, per-act grades, transitions and the graphics.

  python3 edit.py [--no-overlay] [--from S --to S] [-o build/picture.mp4]

Reads the cut from timeline.py, the art from assets/art/, and (unless --no-overlay) the HyperFrames graphics
rendered as an RGBA PNG sequence in build/overlay/. Everything is deterministic: same inputs, same frames.
"""
import argparse
import os
import subprocess
from functools import lru_cache
from multiprocessing import Pool

import cv2
import numpy as np

from timeline import CLIPS, CLIPS_DIR, CUES, CUT, DURATION, END, FPS, START

W, H = 1920, 1080
SW, SH = 1280, 720
HERE = os.path.dirname(os.path.abspath(__file__))
OVERLAY = os.path.join(HERE, "build", "overlay")

# bible slots, left to right: D B A C E (A, the hero, sits in the centre)
ART_ORDER = {0: "A_frog", -1: "B_girl", 1: "C_cat", -2: "D_slime", 2: "E_horn", -3: "C_cat", 3: "B_girl"}

# ─── transitions and accents, by time ───────────────────────────────────────
# (kind, time, duration, strength)
C = CUES
FX = [
    ("fade_in", 0.0, 1.1, 1),
    # the one glitch in the open: a small skip on the record scratch
    ("glitch", C["SCRATCH"] - 0.02, 0.16, 0.45), ("punch", C["SCRATCH"], 0.35, 0.05),
    ("whip", START["3a"], 0.2, 1), ("whip", START["3b"], 0.14, -1), ("whip", START["3c"], 0.14, 1),
    ("neg", C["PISTOL"], 2 / FPS, 1), ("flash", C["PISTOL"] + 2 / FPS, 0.35, 0.8), ("shake", C["PISTOL"], 0.55, 20),
    ("whip", START["4b"], 0.16, 1), ("whip", START["5a"], 0.14, -1),
    ("shake", C["THUD"], 0.45, 14), ("slowblur", C["TRIP"], 0.5, 1),
    ("whip", START["5c"], 0.12, 1), ("whip", START["6a"], 0.14, -1),
    ("whip", START["6b"], 0.16, 1), ("rgb", START["6b"], END["6c"] - START["6b"], 0.4),
    ("whip", START["6c"], 0.14, 1), ("whip", START["7a"], 0.16, -1),
    ("whip", START["7b"], 0.12, 1), ("whip", START["7c"], 0.14, -1),
    # race → auction: a hard whip and a white flash
    ("whip", C["SMASH"], 0.24, 1.4), ("flash", C["SMASH"], 0.3, 0.55),
    ("dissolve", START["9b"], 0.25, 1), ("dissolve", START["9c"], 0.2, 1), ("whip", START["9d"], 0.14, 1),
    ("whip", START["10a"], 0.12, -1),
    ("neg", C["GAVEL"], 2 / FPS, 1), ("flash", C["GAVEL"] + 2 / FPS, 0.25, 0.6), ("shake", C["GAVEL"], 0.4, 16),
    # into Cloak: everything slows down, a long soft blur dissolve
    ("dissolve", C["TO_CLOAK"], 0.9, 1),
    ("dissolve", START["11b"], 0.45, 1), ("dissolve", START["12a"], 0.4, 1), ("dissolve", START["12b"], 0.3, 1),
    ("flash_teal", C["SEAL"], 0.3, 0.4), ("dissolve", START["12c"], 0.4, 1),
    ("bots", C["BOTS_FLASH"], 0.42, 1),
    ("flash", C["OPEN"], 0.35, 0.55),
    ("flash_amber", C["LINE"], 0.35, 0.45),
    ("dissolve", START["13b"], 0.35, 1), ("whip", START["13c"], 0.12, 1), ("dissolve", START["13d"], 0.3, 1),
    ("dip", C["STINGER"] - 0.25, 0.5, 1),
]


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def rand(seed):
    return np.random.default_rng(int(seed) & 0xFFFFFFFF)


# ─── sources ────────────────────────────────────────────────────────────────
@lru_cache(maxsize=2)
def clip_frames(name):
    cap = cv2.VideoCapture(os.path.join(CLIPS_DIR, CLIPS[name]))
    frames = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        frames.append(fr)
    return frames


def src_frame(name, t):
    """Source frame at second t, blending neighbours for slow motion."""
    fr = clip_frames(name)
    x = min(max(t * FPS, 0), len(fr) - 1)
    i = int(x)
    f = x - i
    if f < 0.2 or i + 1 >= len(fr):
        return fr[i]
    if f > 0.8:
        return fr[i + 1]
    return cv2.addWeighted(fr[i], 1 - f, fr[i + 1], f, 0)


@lru_cache(maxsize=None)
def art(name):
    return cv2.imread(os.path.join(HERE, "assets", "art", name + ".png"))


def key_art(img):
    """Fill every green-screen frame with a piece of the art, perspective-matched, occluders kept."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (40, 85, 45), (78, 255, 255))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, stats, cent = cv2.connectedComponentsWithStats(mask)
    comps = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 300]
    if not comps:
        return img
    big = max(stats[i, cv2.CC_STAT_AREA] for i in comps)
    # frames hang on walls and easels: drop specks and reflections low in the picture
    comps = [i for i in comps if cent[i][1] < 0.72 * SH and stats[i, cv2.CC_STAT_AREA] > 0.04 * big]
    # one slot per physical frame: pieces split by a head or the glass box share a slot by x position
    widths = sorted(stats[i, cv2.CC_STAT_WIDTH] for i in comps if stats[i, cv2.CC_STAT_AREA] > 1500) or [80]
    pitch = max(np.median(widths) * 1.25, 30)
    groups = {}
    for i in comps:
        cx = stats[i, cv2.CC_STAT_LEFT] + stats[i, cv2.CC_STAT_WIDTH] / 2
        key = None
        for g in groups:
            if abs(groups[g]["cx"] - cx) < pitch * 0.5:
                key = g
                break
        if key is None:
            key = len(groups)
            groups[key] = dict(cx=cx, ids=[])
        groups[key]["ids"].append(i)
    order = sorted(groups.values(), key=lambda g: g["cx"])
    # measure each group; frames in a row share one shape, so take it from the most complete one
    for g in order:
        g["m"] = np.isin(lab, g["ids"]).astype(np.uint8) * 255
        g["rect"] = cv2.boundingRect(cv2.findNonZero(g["m"]))
        x, y, w, h = g["rect"]
        g["area"] = int((g["m"] > 0).sum())
        g["fill"] = g["area"] / max(w * h, 1)
    biggest = max(g["area"] for g in order)
    order = [g for g in order if g["area"] > 0.12 * biggest and g["rect"][2] >= 14 and g["rect"][3] >= 14]
    if not order:
        return img
    full = [g["rect"][3] / g["rect"][2] for g in order if g["fill"] > 0.88]
    aspect = float(np.clip(np.median(full), 0.6, 1.6)) if full else 1.25
    mid = min(range(len(order)), key=lambda k: abs(order[k]["cx"] - SW / 2))
    out = img.astype(np.float32)
    for k, grp in enumerate(order):
        m = grp["m"]
        x, y, w, h = grp["rect"]
        if grp["fill"] > 0.88:
            hull = cv2.convexHull(cv2.findNonZero(m))
            poly = cv2.approxPolyDP(hull, 0.04 * cv2.arcLength(hull, True), True).reshape(-1, 2)
        else:
            poly = []
        if len(poly) == 4:
            sm = poly.sum(1)
            d = np.diff(poly, axis=1).ravel()
            quad = np.float32([poly[np.argmin(sm)], poly[np.argmin(d)], poly[np.argmax(sm)], poly[np.argmax(d)]])
        else:  # partly hidden: keep its visible top and width, take the height from the row
            h = w * aspect
            quad = np.float32([[x, y], [x + w, y], [x + w, y + h], [x, y + h]])
        a = art(ART_ORDER.get(k - mid, ["D_slime", "B_girl", "A_frog", "C_cat", "E_horn"][(k - mid) % 5]))
        ah, aw = a.shape[:2]
        tw = np.linalg.norm(quad[1] - quad[0]) + np.linalg.norm(quad[2] - quad[3])
        th = np.linalg.norm(quad[3] - quad[0]) + np.linalg.norm(quad[2] - quad[1])
        r = float(np.clip(tw / max(th, 1), 0.25, 4))
        if aw / ah > r:   # crop the art to the frame's shape (cover), never stretch it
            cw = int(ah * r)
            a = a[:, (aw - cw) // 2:(aw - cw) // 2 + cw]
        else:
            ch = int(aw / r)
            a = a[(ah - ch) // 2:(ah - ch) // 2 + ch]
        ah, aw = a.shape[:2]
        # pad the quad out by a pixel so no green rim survives
        c = quad.mean(0)
        quad = c + (quad - c) * 1.02
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [aw, 0], [aw, ah], [0, ah]]), quad)
        warped = cv2.warpPerspective(a, M, (SW, SH), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
        # match the room: the art takes the scene's light on the canvas (brightness of the surroundings)
        ring = cv2.dilate(m, np.ones((15, 15), np.uint8)) - cv2.dilate(m, np.ones((5, 5), np.uint8))
        room = img[ring > 0].mean() if (ring > 0).any() else 128
        gain = np.clip(0.55 + room / 255 * 0.7, 0.6, 1.15)
        alpha = cv2.GaussianBlur(cv2.dilate(m, np.ones((3, 3), np.uint8)), (5, 5), 0).astype(np.float32)[..., None] / 255
        out = out * (1 - alpha) + warped.astype(np.float32) * gain * alpha
    out = np.clip(out, 0, 255).astype(np.uint8)
    # despill: any leftover green fringe goes neutral
    b, g, r_ = cv2.split(out.astype(np.int16))
    lim = np.maximum(b, r_) + 18
    g = np.where(g > lim, lim, g)
    return cv2.merge([b, g, r_]).clip(0, 255).astype(np.uint8)


# ─── grades ─────────────────────────────────────────────────────────────────
_vig = None


def vignette(strength):
    global _vig
    if _vig is None:
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
        _vig = np.clip(d - 0.45, 0, 1)[..., None]
    return 1 - _vig * strength


def grade(img, look):
    f = img.astype(np.float32) / 255
    if look == "museum":
        f = np.clip((f - 0.03) * 1.12, 0, 1) ** 1.12
        f *= np.array([0.93, 0.98, 1.06])  # BGR: warm the gold
        f *= vignette(1.1)
    elif look == "race":
        lum = f @ np.array([0.114, 0.587, 0.299])
        f = lum[..., None] + (f - lum[..., None]) * 1.18
        f = np.clip((f - 0.5) * 1.12 + 0.5, 0, 1)
        f = f * np.array([0.9, 1.0, 1.04]) + np.array([0.0, 0.012, 0.02])  # signal yellow in the highlights
        f *= vignette(0.55)
    elif look == "auction":
        f = np.clip((f - 0.5) * 1.1 + 0.5, 0, 1)
        f *= np.array([0.88, 0.96, 1.08])  # tungsten, deep red
        f *= vignette(0.85)
    elif look in ("cloak", "end"):
        lum = f @ np.array([0.114, 0.587, 0.299])
        f = lum[..., None] + (f - lum[..., None]) * 0.86
        f = f * np.array([1.06, 1.01, 0.9]) + np.array([0.025, 0.018, 0.0])  # cool, teal shadows
        f = np.clip((f - 0.5) * 1.08 + 0.5, 0, 1)
        f *= vignette(0.9)
    elif look == "stinger":
        f = np.clip((f - 0.02) * 1.15, 0, 1) ** 1.1
        f *= vignette(1.0)
    return np.clip(f * 255, 0, 255).astype(np.uint8)


# ─── one shot frame ─────────────────────────────────────────────────────────
STINGER_FOCUS = (645 / SW, 175 / SH)  # the centre robot's red eye


def shot_frame(s, t_local):
    speed = (s["b"] - s["a"]) / s["dur"]
    st = s["a"] + t_local * speed
    img = src_frame(s["clip"], st)
    if s.get("key"):
        img = key_art(img)
    z0, z1 = s.get("zoom", (1.0, 1.0))
    p = ease(t_local / s["dur"])
    z = z0 + (z1 - z0) * p
    fx, fy = s.get("focus", (0.5, 0.5))
    scale = W / SW * z
    # keep the frame covered: clamp the centre so no edge shows
    cx = np.clip(fx * SW, SW / (2 * z), SW - SW / (2 * z))
    cy = np.clip(fy * SH, SH / (2 * z), SH - SH / (2 * z))
    M = np.float32([[scale, 0, W / 2 - cx * scale], [0, scale, H / 2 - cy * scale]])
    out = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
    if z < 1.6:
        blur = cv2.GaussianBlur(out, (0, 0), 1.2)
        out = cv2.addWeighted(out, 1.45, blur, -0.45, 0)  # gentle unsharp after the upscale
    out = grade(out, s["look"])
    if s["look"] == "end":
        p = ease(t_local / 1.8)
        if p > 0.01:
            out = cv2.GaussianBlur(out, (0, 0), 0.5 + 22 * p)
        out = (out.astype(np.float32) * (1 - 0.45 * p)).astype(np.uint8)
    return out


def shot_at(t):
    for k, s in enumerate(CUT):
        if t < s["start"] + s["dur"] - 1e-6:
            return k
    return len(CUT) - 1


# ─── effects ────────────────────────────────────────────────────────────────
def glitch(img, amt, seed):
    r = rand(seed)
    out = img.copy()
    h, w = img.shape[:2]
    # horizontal slice displacement
    for _ in range(int(6 + 18 * amt)):
        y = r.integers(0, h - 8)
        hh = int(r.integers(4, 18 + 90 * amt))
        dx = int(r.normal(0, 70 * amt))
        out[y:y + hh] = np.roll(out[y:y + hh], dx, axis=1)
    # RGB split
    sh = int(6 + 26 * amt)
    b, g, rr = cv2.split(out)
    rr = np.roll(rr, sh, axis=1)
    b = np.roll(b, -sh, axis=1)
    out = cv2.merge([b, g, rr])
    # block corruption
    for _ in range(int(3 + 10 * amt)):
        bw, bh = int(r.integers(40, 260)), int(r.integers(10, 60))
        x, y = int(r.integers(0, w - bw)), int(r.integers(0, h - bh))
        sx, sy = int(r.integers(0, w - bw)), int(r.integers(0, h - bh))
        out[y:y + bh, x:x + bw] = out[sy:sy + bh, sx:sx + bw]
    # scan lines and noise
    out[::3] = (out[::3] * (1 - 0.25 * amt)).astype(np.uint8)
    noise = r.normal(0, 18 * amt, (h // 4, w // 4, 1)).astype(np.float32)
    noise = cv2.resize(noise, (w, h), interpolation=cv2.INTER_NEAREST)[..., None]
    return np.clip(out.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def rgb_split(img, px):
    b, g, r = cv2.split(img)
    return cv2.merge([np.roll(b, -px, 1), g, np.roll(r, px, 1)])


def motion_blur(img, length):
    L = max(3, int(length / 2) | 1)
    k = np.full((1, L), 1 / L, np.float32)
    small = cv2.filter2D(cv2.resize(img, (W // 2, H // 2)), -1, k)
    return cv2.resize(small, (W, H))


def tint_flash(img, color, a):
    return cv2.addWeighted(img, 1 - a, np.full_like(img, color), a, 0)


_bots_cache = {}


def bots_frame(t):
    """A glimpse of the sniper's red eye, for "Not the bots"."""
    s = dict(clip="door", a=3.9, b=4.9, dur=1.0, look="stinger", zoom=(1.15, 1.25))
    return shot_frame(s, min(t * 1.6, 0.99))


def render_frame(i):
    t = i / FPS
    k = shot_at(t)
    s = CUT[k]
    img = shot_frame(s, t - s["start"])

    # dissolves and whips need the neighbouring shot
    for kind, at, d, amt in FX:
        if kind == "dissolve" and abs(t - at) < d / 2:
            kk = shot_at(at - 1e-3) if t >= at else shot_at(at + 1e-3)
            o = CUT[kk]
            other = shot_frame(o, min(max(t - o["start"], -0.5), o["dur"] + 0.5))
            p = (t - (at - d / 2)) / d
            w_new = ease(p)
            img = cv2.addWeighted(img, w_new if t >= at else 1 - w_new, other, 1 - w_new if t >= at else w_new, 0)
            bl = 1 - abs(p - 0.5) * 2
            if bl > 0.1:
                img = cv2.GaussianBlur(img, (0, 0), 1 + 7 * bl)
        if kind == "whip" and abs(t - at) < d:
            p = 1 - abs(t - at) / d
            img = motion_blur(img, 10 + 150 * p * p)
            shift = int(amt * (1 if t < at else -1) * 160 * p * p)
            img = np.roll(img, shift, axis=1)

    # the graphics go on before the global effects so text glitches with the picture
    if not ARGS.no_overlay:
        ov = cv2.imread(os.path.join(OVERLAY, f"frame_{i + 1:06d}.png"), cv2.IMREAD_UNCHANGED)
        if ov is None:
            ov = cv2.imread(os.path.join(OVERLAY, f"{i:06d}.png"), cv2.IMREAD_UNCHANGED)
        if ov is not None:
            if ov.shape[:2] != (H, W):
                ov = cv2.resize(ov, (W, H))
            if ov.ndim == 2:
                ov = cv2.cvtColor(ov, cv2.COLOR_GRAY2BGR)
            a = ov[..., 3:4].astype(np.float32) / 255 if ov.shape[2] == 4 else np.ones((H, W, 1), np.float32)
            img = (img.astype(np.float32) * (1 - a) + ov[..., :3].astype(np.float32) * a).astype(np.uint8)

    for kind, at, d, amt in FX:
        if not (at <= t < at + d):
            continue
        p = (t - at) / d
        if kind == "fade_in":
            img = (img.astype(np.float32) * ease(p) ** 1.4).astype(np.uint8)
        elif kind == "glitch":
            img = glitch(img, amt * (1 - p * 0.6), i * 7919 + int(at * 100))
        elif kind == "neg":
            img = 255 - img
        elif kind == "flash":
            img = tint_flash(img, (255, 255, 255), amt * (1 - p) ** 2)
        elif kind == "flash_teal":
            img = tint_flash(img, (203, 182, 108), amt * (1 - p) ** 2)
        elif kind == "flash_amber":
            img = tint_flash(img, (90, 169, 227), amt * (1 - p) ** 2)
        elif kind == "shake":
            r = rand(i * 31 + 7)
            mag = amt * (1 - p) ** 2
            dx, dy = r.normal(0, mag), r.normal(0, mag)
            M = np.float32([[1.03, 0, dx - W * 0.015], [0, 1.03, dy - H * 0.015]])
            img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        elif kind == "punch":
            z = 1 + amt * (1 - ease(p))
            M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
            img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        elif kind == "rgb":
            img = rgb_split(img, int(2 + 4 * amt * abs(np.sin(t * 7))))
        elif kind == "dip":  # a dip through black, centred on the cut
            img = (img.astype(np.float32) * min(1, abs(t - (at + d / 2)) / (d / 2)) ** 1.5).astype(np.uint8)
        elif kind == "blur_in":
            img = cv2.GaussianBlur(img, (0, 0), 0.1 + 14 * (1 - ease(p)))
        elif kind == "dim_in":
            img = (img.astype(np.float32) * (1.0 - 0.0 * p)).astype(np.uint8)
        elif kind == "slowblur":
            img = cv2.addWeighted(img, 0.75, cv2.GaussianBlur(img, (0, 0), 3), 0.25, 0)
        elif kind == "bots":
            r = rand(i * 17)
            bot = rgb_split(bots_frame(t - at), 8)
            if p < 0.12 or p > 0.88:
                bot = glitch(bot, 0.35, i * 3)
            img = bot

    # film grain, very light, so the upscaled Veo frames hold together
    g = rand(i * 2654435761).normal(0, 3.2, (H // 2, W // 2, 1)).astype(np.float32)
    g = cv2.resize(g, (W, H))[..., None]
    img = np.clip(img.astype(np.float32) + g, 0, 255).astype(np.uint8)
    return img.tobytes()


def _init(args):
    global ARGS
    ARGS = args


ARGS = None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-overlay", action="store_true")
    ap.add_argument("--from", dest="t0", type=float, default=0)
    ap.add_argument("--to", dest="t1", type=float, default=DURATION)
    ap.add_argument("-o", default=os.path.join(HERE, "build", "picture.mp4"))
    ap.add_argument("-j", type=int, default=os.cpu_count())
    args = ap.parse_args()
    ARGS = args
    frames = range(int(round(args.t0 * FPS)), int(round(min(args.t1, DURATION) * FPS)))
    os.makedirs(os.path.dirname(args.o), exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                            "-pix_fmt", "yuv420p", args.o], stdin=subprocess.PIPE)
    with Pool(args.j, initializer=_init, initargs=(args,)) as pool:
        for n, buf in enumerate(pool.imap(render_frame, frames, chunksize=12)):
            enc.stdin.write(buf)
            if n % 120 == 0:
                print(f"{n / FPS:6.1f}s", flush=True)
    enc.stdin.close()
    enc.wait()
    print(args.o)
