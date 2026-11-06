"""Contact sheet of a video at given times: python3 tools/sheet.py video.mp4 out.png t1 t2 ... [--cols 4 --w 480]"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

args = sys.argv[1:]
cols = int(args[args.index("--cols") + 1]) if "--cols" in args else 4
w = int(args[args.index("--w") + 1]) if "--w" in args else 480
args = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or not args[i - 1].startswith("--"))]
video, out, times = args[0], args[1], [float(t) for t in args[2:]]
h = w * 9 // 16
tiles = []
for t in times:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", f"scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    im = Image.fromarray(np.frombuffer(raw, np.uint8).reshape(h, w, 3)) if len(raw) == w * h * 3 else Image.new("RGB", (w, h))
    ImageDraw.Draw(im).text((6, 4), f"{t:.2f}", fill="yellow")
    tiles.append(im)
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h))
for k, im in enumerate(tiles):
    sheet.paste(im, ((k % cols) * w, (k // cols) * h))
sheet.save(out)
print(out)
