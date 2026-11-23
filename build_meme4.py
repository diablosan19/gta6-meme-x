#!/usr/bin/env python3
"""Meme v4 for gta6-meme-x-01: a tombstone for the fan who died waiting for
GTA 6, while his AI agent (the make.fun ghost) sits on a pile of cash next
to it. Dark, instantly readable, one joke."""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1280
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fb(sz): return ImageFont.truetype(FONT, sz)
def fr(sz): return ImageFont.truetype(FONT_R, sz)

stops = [(0.0, (24, 8, 60)), (0.4, (90, 25, 120)), (0.66, (200, 40, 110)),
         (0.85, (245, 110, 30)), (1.0, (250, 180, 70))]
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(int(H * 0.78)):
    t = y / (H * 0.78)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
            break
    for x in range(W):
        px[x, y] = col
img = img.convert("RGBA")
d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, int(H * 0.78), W, H], fill=(30, 22, 38, 255))
d.rectangle([0, int(H * 0.78), W, int(H * 0.78) + 8], fill=(60, 45, 70, 255))

# distant small tombstones
for (tx, ty, s) in [(90, 930, 0.5), (1130, 945, 0.45), (1010, 905, 0.35)]:
    d.rounded_rectangle([tx, ty, tx + int(90 * s) + 30, ty + int(150 * s) + 40], radius=18,
                        fill=(70, 62, 84, 255))

# main tombstone
d.rounded_rectangle([130, 480, 620, 1010], radius=110, fill=(168, 165, 180, 255),
                    outline=(90, 88, 105, 255), width=6)
d.rectangle([130, 900, 620, 1010], fill=(168, 165, 180, 255))
d.line([(130, 1010), (620, 1010)], fill=(90, 88, 105, 255), width=6)
d.text((375, 560), "R.I.P.", font=fb(84), fill=(52, 50, 66), anchor="ma")
d.text((375, 690), "DIED WAITING", font=fb(52), fill=(52, 50, 66), anchor="ma")
d.text((375, 758), "FOR GTA 6", font=fb(52), fill=(52, 50, 66), anchor="ma")
d.text((375, 852), "2013 — 2027", font=fr(44), fill=(80, 78, 95), anchor="ma")

# cash pile under the ghost
for i, (cx, cy, ang) in enumerate([(700, 950, -14), (800, 972, 6), (905, 948, 16),
                                    (745, 905, 4), (855, 900, -8), (800, 862, 10)]):
    bill = Image.new("RGBA", (190, 96), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bill)
    bd.rounded_rectangle([3, 3, 187, 93], radius=10, fill=(34, 160, 60, 255),
                         outline=(190, 255, 200, 255), width=4)
    bd.text((95, 48), "$", font=fb(52), fill=(230, 255, 235), anchor="mm")
    bill = bill.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(bill, (cx, cy), bill)

ghost = Image.open(os.path.join(HERE, "ghost.png")).convert("RGBA")
big = ghost.resize((int(ghost.width * 330 / ghost.height), 330), Image.LANCZOS)
img.paste(big, (760, 545), big)
d = ImageDraw.Draw(img, "RGBA")

# speech bubble from the ghost, in the empty sky
d.rounded_rectangle([545, 110, 1245, 330], radius=36, fill=(255, 255, 255, 255))
d.polygon([(800, 330), (880, 330), (845, 420)], fill=(255, 255, 255, 255))
d.text((895, 145), "I already earned $500", font=fb(43), fill=(20, 20, 25), anchor="ma")
d.text((895, 205), "on make.fun bounties.", font=fb(43), fill=(20, 20, 25), anchor="ma")
d.text((895, 272), "he is still waiting.", font=fr(36), fill=(90, 90, 100), anchor="ma")

d.text((640, 1095), "HE WAITED. HIS AGENT DIDN'T.", font=fb(66), fill=(255, 255, 255),
       anchor="ma", stroke_width=5, stroke_fill=(0, 0, 0))
d.text((640, 1180), "agents earn real money on make.fun", font=fb(42), fill=(255, 230, 90),
       anchor="ma", stroke_width=4, stroke_fill=(0, 0, 0))

img.convert("RGB").save(os.path.join(HERE, "meme4.png"))
print("saved meme4.png", img.size)
